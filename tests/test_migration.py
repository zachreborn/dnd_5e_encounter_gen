import ast
import json
import tempfile
import unittest
from pathlib import Path

from dnd_5e_encounter_gen.catalog import merge_catalogs, parse_catalog
from tools.migrate_legacy import convert

ROOT = Path(__file__).resolve().parents[1]


class MigrationTests(unittest.TestCase):
    def test_every_legacy_field_is_preserved(self):
        path = ROOT / "legacy/monsters.py"
        original_tree = ast.parse(path.read_text())
        original = next(ast.literal_eval(node.value) for node in original_tree.body
                        if isinstance(node, ast.Assign) and any(
                            isinstance(target, ast.Name) and target.id == "cr_dict" for target in node.targets
                        ))
        pack = convert(path)
        self.assertEqual(len(pack["monsters"]), 511)
        parsed = parse_catalog(json.dumps(pack))
        self.assertEqual(len(merge_catalogs([parsed])), len(original))
        for record in pack["monsters"]:
            page, cr, xp, size, kind = original[record["name"]]
            with self.subTest(name=record["name"]):
                self.assertEqual(record["extensions"]["legacy_values"], original[record["name"]])
                self.assertEqual(record["references"][0]["page"], str(page))
                self.assertEqual(record["challenge_rating"], cr)
                self.assertEqual(record["xp"], xp)
                self.assertEqual(record["size"], size.lower())
                self.assertEqual(record["monster_type"], kind.lower())
                self.assertEqual(record["rules_revision"], "legacy")

    def test_never_execute_catalog_code(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.py"
            sentinel = Path(directory) / "must-not-exist"
            source.write_text(
                f"open({str(sentinel)!r}, 'w').write('unsafe')\n"
                "cr_dict = {'Test': [1, '0', 10, 'Tiny', 'Beast']}\n"
            )
            self.assertEqual(len(convert(source)["monsters"]), 1)
            self.assertFalse(sentinel.exists())
            source.write_text(f"cr_dict = __import__('pathlib').Path({str(sentinel)!r}).touch()")
            with self.assertRaises(ValueError):
                convert(source)
            self.assertFalse(sentinel.exists())

    def test_invalid_literals_and_collisions(self):
        for text in (
            "x = {}", "cr_dict = []", "cr_dict={}; cr_dict={}",
            "cr_dict={'A':[1,'0',10,'Tiny','Beast'], 'A':[1,'0',10,'Tiny','Beast']}",
            "cr_dict={'A':[1,'0']}",
            "cr_dict={'A B':[1,'0',10,'Tiny','Beast'], 'A-B':[1,'0',10,'Tiny','Beast']}",
        ):
            with self.subTest(text=text), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "invalid.py"
                path.write_text(text)
                with self.assertRaises(ValueError):
                    convert(path)
