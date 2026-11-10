import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dnd_5e_encounter_gen.catalog import (
    CatalogError,
    _validate,
    catalog_schema,
    load_catalog,
    load_default,
    load_monsters,
    merge_catalogs,
    parse_catalog,
)
from dnd_5e_encounter_gen.cli import display
from dnd_5e_encounter_gen.engine import generate_encounter

ROOT = Path(__file__).resolve().parents[1]


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.example = load_catalog(ROOT / "examples/homebrew.json")

    def parse(self, document):
        return parse_catalog(json.dumps(document), "test.json")

    def test_optional_fields_and_extensions(self):
        record = self.example["monsters"][0]
        record.pop("references")
        record["aliases"] = ["Green guardian"]
        record["challenge_rating"] = "1/8"
        monster = merge_catalogs([self.parse(self.example)])[0]
        self.assertEqual(monster.references, ())
        self.assertEqual(monster.aliases, ("Green guardian",))
        self.assertEqual(monster.challenge_rating, "1/8")
        self.assertIn("encounter_hook", monster.extensions)

    def test_unique_string_arrays_do_not_scan_all_preceding_items(self):
        comparisons = 0

        class CountedString(str):
            __hash__ = str.__hash__

            def __eq__(self, other):
                nonlocal comparisons
                comparisons += 1
                if comparisons > 100_000:
                    raise AssertionError("Uniqueness validation rescans preceding values")
                return super().__eq__(other)

        schema = catalog_schema()
        rule = schema["$defs"]["monster"]["properties"]["tags"]
        values = [CountedString(f"tag-{index}") for index in range(10_000)]
        _validate(values, rule, schema, "tags")
        self.assertLessEqual(comparisons, 100_000)
        with self.assertRaisesRegex(CatalogError, "duplicate array item"):
            _validate([*values, values[-1]], rule, schema, "tags")

    def test_unique_items_schema_only_uses_strings(self):
        def check(rule):
            if isinstance(rule, dict):
                if rule.get("uniqueItems"):
                    self.assertEqual(rule["items"]["type"], "string")
                for value in rule.values():
                    check(value)
            elif isinstance(rule, list):
                for value in rule:
                    check(value)

        check(catalog_schema())

    def test_unhashable_tag_and_alias_items_are_validation_errors(self):
        for field in ("tags", "aliases"):
            for item in ({}, []):
                with self.subTest(field=field, item=item):
                    doc = copy.deepcopy(self.example)
                    doc["monsters"][0][field] = [item]
                    with self.assertRaisesRegex(CatalogError, rf"{field}\[0\].*expected string"):
                        self.parse(doc)

    def test_merged_records_detach_and_recursively_freeze_metadata(self):
        record = self.example["monsters"][0]
        record["aliases"] = ["Green guardian"]
        record["extensions"]["nested"] = {"notes": [{"text": "original"}], "empty": {}}
        monster = merge_catalogs([self.example])[0]
        record["references"][0].clear()
        record["references"].clear()
        record["tags"].append("changed")
        record["aliases"].clear()
        record["extensions"]["nested"]["notes"][0]["text"] = "changed"
        record["extensions"]["nested"]["notes"].append({"text": "new"})
        record["extensions"].clear()
        self.assertEqual(monster.references[0]["publication"], "My campaign notes")
        self.assertEqual(monster.tags, ("forest",))
        self.assertEqual(monster.aliases, ("Green guardian",))
        self.assertEqual(monster.extensions["nested"]["notes"][0]["text"], "original")
        self.assertEqual(len(monster.extensions["nested"]["notes"]), 1)
        with self.assertRaises(TypeError):
            monster.references[0]["publication"] = "changed"
        with self.assertRaises(TypeError):
            monster.extensions["nested"]["notes"][0]["text"] = "changed"
        with self.assertRaises(TypeError):
            monster.extensions["nested"]["empty"]["new"] = True
        with self.assertRaises(AttributeError):
            monster.extensions["nested"]["notes"].append("new")
        with contextlib.redirect_stdout(io.StringIO()) as output:
            display(generate_encounter([monster], 4, 5), 4, 5, "moderate", "plant")
        self.assertIn("My campaign notes", output.getvalue())

    def test_direct_record_construction_freezes_tuple_contents(self):
        from dataclasses import replace

        monster = merge_catalogs([self.example])[0]
        reference = {"publication": "Notes"}
        nested = {"notes": ({"text": "original"},)}
        replaced = replace(monster, references=(reference,), extensions=nested)
        reference.clear()
        nested["notes"][0].clear()
        self.assertEqual(replaced.references[0]["publication"], "Notes")
        self.assertEqual(replaced.extensions["notes"][0]["text"], "original")
        with self.assertRaises(TypeError):
            replaced.extensions["new"] = "value"

    def test_metadata_freezing_depth_errors_are_reported(self):
        with patch("dnd_5e_encounter_gen.catalog._freeze", side_effect=RecursionError("too deep")):
            with self.assertRaisesRegex(CatalogError, "homebrew:moss-guardian.*nested too deeply"):
                merge_catalogs([self.example])

    def test_invalid_record_fields(self):
        for field, value in (
            ("xp", True), ("xp", -1), ("xp", 1.5), ("xp", "50"),
            ("challenge_rating", "1/3"), ("challenge_rating", "31"),
            ("size", "Medium"), ("monster_type", "unknown"), ("id", "no-pack"),
            ("name", ""), ("references", [{}]), ("tags", ["forest", "forest"]),
            ("tags", [False]), ("aliases", [""]), ("extensions", []),
            ("references", [{"publication": "notes", "url": "file:///private"}]),
            ("references", [{"publication": "notes", "page": 1}]),
            ("references", [{"publication": "notes", "extra": "value"}]),
        ):
            with self.subTest(field=field, value=value):
                doc = copy.deepcopy(self.example)
                doc["monsters"][0][field] = value
                with self.assertRaisesRegex(CatalogError, "test.json"):
                    self.parse(doc)

    def test_invalid_pack_fields(self):
        for field, value in (
            ("schema_version", 2), ("schema_version", True), ("pack_id", "Bad pack"),
            ("pack_version", ""), ("source", []), ("license", None), ("monsters", {}),
        ):
            with self.subTest(field=field, value=value):
                doc = copy.deepcopy(self.example)
                doc[field] = value
                with self.assertRaises(CatalogError):
                    self.parse(doc)
        for field in self.example:
            doc = copy.deepcopy(self.example)
            del doc[field]
            with self.assertRaisesRegex(CatalogError, "missing field"):
                self.parse(doc)
        self.example["unexpected"] = 1
        with self.assertRaisesRegex(CatalogError, "unknown field"):
            self.parse(self.example)

    def test_missing_record_field_and_duplicates(self):
        del self.example["monsters"][0]["name"]
        with self.assertRaisesRegex(CatalogError, "missing field name"):
            self.parse(self.example)
        self.setUp()
        self.example["monsters"].append(copy.deepcopy(self.example["monsters"][0]))
        with self.assertRaisesRegex(CatalogError, "duplicate identity"):
            self.parse(self.example)
        for text in ('{"schema_version":1,"schema_version":1}', "{", '{"x":NaN}', '{"x":Infinity}'):
            with self.assertRaises(CatalogError):
                parse_catalog(text, "bad.json")

    def test_recursion_error_is_reported(self):
        with patch("dnd_5e_encounter_gen.catalog.json.loads", side_effect=RecursionError("too deep")):
            with self.assertRaises(CatalogError):
                parse_catalog("[]")

    def test_oversized_catalog_and_integer_are_reported(self):
        with patch("dnd_5e_encounter_gen.catalog.MAX_CATALOG_CHARACTERS", 5):
            with self.assertRaisesRegex(CatalogError, "limit"):
                parse_catalog(" " * 6)
        # Python's integer-token safety limit must not become a CLI traceback.
        with self.assertRaises(CatalogError):
            parse_catalog('{"x":' + "9" * 5000 + "}")

    def test_file_failures(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.json"
            with self.assertRaisesRegex(CatalogError, "cannot read"):
                load_catalog(path)
            path.write_bytes(b"\xff")
            with self.assertRaisesRegex(CatalogError, "UTF-8"):
                load_catalog(path)

    def test_add_replace_and_explicit_override(self):
        default_count = len(load_monsters())
        example_path = ROOT / "examples/homebrew.json"
        self.assertEqual(len(load_monsters([example_path])), default_count + 1)
        self.assertEqual(len(load_monsters([example_path], include_default=False)), 1)
        self.assertEqual(load_monsters(include_default=False), ())
        replacement = copy.deepcopy(self.example)
        replacement["monsters"][0]["xp"] = 501  # Homebrew experience need not match standard challenge rating.
        with self.assertRaisesRegex(CatalogError, "duplicate identity"):
            merge_catalogs([self.example, replacement])
        merged = merge_catalogs([self.example, replacement], allow_overrides=True)
        self.assertEqual(merged[0].xp, 501)
        replacement["monsters"][0]["id"] = "other:moss-guardian"
        self.assertEqual(len(merge_catalogs([self.example, replacement])), 2)

    def test_schema_parity(self):
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("Install .[dev] for full JSON Schema parity checks")
        schema = catalog_schema()
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        validator.validate(load_default())
        validator.validate(self.example)
        fields = schema["$defs"]["monster"]["properties"]
        values = [None, True, False, -1, 1.5, "", [], {}, "bogus"]
        for field in fields:
            for value in values:
                doc = copy.deepcopy(self.example)
                doc["monsters"][0][field] = value
                expected = validator.is_valid(doc)
                try:
                    self.parse(doc)
                    actual = True
                except CatalogError:
                    actual = False
                with self.subTest(field=field, value=value):
                    self.assertEqual(actual, expected)


class SourceCoverageTests(unittest.TestCase):
    def test_independent_index_manifest(self):
        pack = load_default()
        manifest = json.loads((ROOT / "tests/fixtures/srd_index.json").read_text())
        base = [record for record in pack["monsters"] if "in-lair" not in record.get("tags", [])]
        actual = {record["name"]: int(record["references"][0]["page"]) for record in base}
        self.assertEqual(actual, manifest["entries"])
        self.assertEqual(pack["source"]["sha256"], manifest["source_sha256"])
        self.assertEqual(len(base), 330)
        self.assertEqual(len(pack["monsters"]), 357)
        self.assertEqual({record["name"] for record in base if record["xp"] == 0},
                         {"Seahorse", "Shrieker Fungus"})

    def test_standard_challenge_rewards_and_variants(self):
        # SRD 5.2.1 p.256. Lair XP is explicitly higher without changing CR.
        rewards = {
            "1/8": 25, "1/4": 50, "1/2": 100,
            **dict(zip(map(str, range(1, 31)), (
                200, 450, 700, 1100, 1800, 2300, 2900, 3900, 5000, 5900,
                7200, 8400, 10000, 11500, 13000, 15000, 18000, 20000,
                22000, 25000, 33000, 41000, 50000, 62000, 75000,
                90000, 105000, 120000, 135000, 155000,
            ))),
        }
        monsters = {monster.id: monster for monster in load_monsters()}
        for monster in monsters.values():
            with self.subTest(monster=monster.id):
                if "in-lair" in monster.tags:
                    base = monsters[monster.id.removesuffix("-in-lair")]
                    self.assertGreater(monster.xp, base.xp)
                    self.assertEqual(monster.challenge_rating, base.challenge_rating)
                elif monster.challenge_rating == "0":
                    self.assertIn(monster.xp, (0, 10))
                elif monster.id == "srd-5.2.1:archmage":
                    self.assertEqual(monster.xp, 8000)  # Verified source discrepancy, p.305.
                    self.assertIn("source_note", monster.extensions)
                else:
                    self.assertEqual(monster.xp, rewards[monster.challenge_rating])
        self.assertEqual(monsters["srd-5.2.1:gold-dragon-wyrmling"].xp, 700)
        self.assertEqual(monsters["srd-5.2.1:goblin-warrior"].monster_type, "fey")
        self.assertIn("swarm of tiny", monsters["srd-5.2.1:swarm-of-bats"].size)
        self.assertEqual(monsters["srd-5.2.1:commoner"].size, "medium or small")
