import contextlib
import hashlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.extract_srd import extract, main, pdf_text


def page_text(page_number, content):
    pages = [""] * 364
    pages[page_number - 1] = content
    return "\f".join(pages)


class ExtractionTests(unittest.TestCase):
    def test_pdf_subprocess_has_timeout_and_utf8_decoding(self):
        result = subprocess.CompletedProcess([], 0, stdout="Will-o’-Wisp\n", stderr="")
        with patch("tools.extract_srd.subprocess.run", return_value=result) as run:
            self.assertEqual(pdf_text(Path("source.pdf"), "-layout"), "Will-o’-Wisp\n")
        self.assertEqual(run.call_args.args[0], ["pdftotext", "-layout", "source.pdf", "-"])
        self.assertEqual(run.call_args.kwargs.get("encoding"), "utf-8")
        timeout = run.call_args.kwargs.get("timeout")
        self.assertIsInstance(timeout, (int, float))
        self.assertGreater(timeout, 0)
        self.assertLessEqual(timeout, 180)

    def test_pdf_subprocess_timeout_propagates(self):
        with patch("tools.extract_srd.subprocess.run",
                   side_effect=subprocess.TimeoutExpired("pdftotext", 60)):
            with self.assertRaises(subprocess.TimeoutExpired):
                pdf_text(Path("source.pdf"))

    def test_generated_catalog_and_index_are_written_as_utf8(self):
        pack = {"monsters": [{"name": "Will-o’-Wisp"}]}
        manifest = {"entries": {"Will-o’-Wisp": 341}}
        native_write_text = Path.write_text

        def write_as_utf8(path, text, **kwargs):
            self.assertEqual(kwargs.get("encoding"), "utf-8")
            return native_write_text(path, text, **kwargs)

        with tempfile.TemporaryDirectory() as directory:
            catalog = Path(directory) / "catalog.json"
            index = Path(directory) / "index.json"
            arguments = ["extract_srd.py", "source.pdf", str(catalog), "--index-manifest", str(index)]
            with patch("sys.argv", arguments), patch("tools.extract_srd.extract", return_value=(pack, manifest)):
                with patch.object(Path, "write_text", autospec=True, side_effect=write_as_utf8):
                    with contextlib.redirect_stdout(io.StringIO()):
                        main()
            for path, expected in ((catalog, pack), (index, manifest)):
                text = path.read_bytes().decode("utf-8")
                self.assertIn("Will-o’-Wisp", text)
                self.assertEqual(json.loads(text), expected)

    def extraction(self, block, index="Test..........258", right=""):
        with tempfile.TemporaryDirectory() as directory:
            pdf = Path(directory) / "fixture.pdf"
            pdf.write_bytes(b"fixture")
            with patch("tools.extract_srd.SOURCE_SHA256", hashlib.sha256(b"fixture").hexdigest()):
                with patch("tools.extract_srd.pdf_text", side_effect=[
                    page_text(258, block), page_text(258, right), page_text(2, index),
                ]):
                    return extract(pdf)

    def test_plain_alternate_and_lair_values(self):
        for challenge, xp, count in (
            ("CR 1 (XP 200; PB +2)", 200, 1),
            ("CR 3 (700 XP; PB +2)", 700, 1),
            ("CR 1 (XP 200, or 450 in lair; PB +2)", 200, 2),
        ):
            pack, manifest = self.extraction(f"Test\nMedium Beast, Neutral\n{challenge}")
            self.assertEqual(pack["monsters"][0]["xp"], xp)
            self.assertEqual(len(pack["monsters"]), count)
            self.assertEqual(manifest["entries"], {"Test": 258})

    def test_swarm_and_cross_column_metadata(self):
        pack, _ = self.extraction(
            "Test\nMedium Swarm of Tiny Beasts, Neutral",
            right="CR 0 (XP 10; PB +2)",
        )
        self.assertEqual(pack["monsters"][0]["size"], "medium swarm of tiny")
        self.assertEqual(pack["monsters"][0]["monster_type"], "beast")

    def test_missing_and_mismatched_metadata_fail_closed(self):
        for block, index in (
            ("Test\nMedium Beast, Neutral", "Test.....258"),
            ("Test\nMedium Beast, Neutral\nOther\nSmall Fey, Neutral", "Test.....258"),
            ("Test\nMedium Beast, Neutral\nCR 1 (XP 200; PB +2)", "Other.....258"),
            ("Test\nMedium Beast, Neutral\nCR 1 (XP 200; PB +2)", "Test.....259"),
        ):
            with self.subTest(block=block, index=index), self.assertRaises(ValueError):
                self.extraction(block, index)

    def test_wrong_source_checksum(self):
        with tempfile.TemporaryDirectory() as directory:
            pdf = Path(directory) / "wrong.pdf"
            pdf.write_bytes(b"not the official source")
            with self.assertRaisesRegex(ValueError, "checksum"):
                extract(pdf)
