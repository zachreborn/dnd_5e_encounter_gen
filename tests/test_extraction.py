import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.extract_srd import extract


def page_text(page_number, content):
    pages = [""] * 364
    pages[page_number - 1] = content
    return "\f".join(pages)


class ExtractionTests(unittest.TestCase):
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
