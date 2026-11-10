import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "dnd_encounter_generator"


class CommandSmokeTests(unittest.TestCase):
    def command(self, *args, inputs=None, direct=False, cwd=ROOT):
        target = [str(PACKAGE / "random_encounter_builder.py")] if direct else ["-m", "dnd_encounter_generator"]
        return subprocess.run(
            [sys.executable, "-B", *target, *args], input=inputs,
            capture_output=True, text=True, timeout=15, cwd=cwd,
        )

    def test_interactive_module_and_direct_script(self):
        for direct in (True, False):
            result = self.command(inputs="4\n5\n\n\nn\n", direct=direct)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Party Size: 4", result.stdout)
            self.assertRegex(result.stdout, r"\b[1-9][0-9]*x ")
            self.assertIn("Source: SRD 5.2.1", result.stdout)
            self.assertIn("Run again?", result.stdout)
            self.assertNotIn("Traceback", result.stderr)

    def test_direct_script_outside_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.command("--party-size", "4", "--level", "5", direct=True, cwd=directory)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_seed_help_and_version(self):
        args = ("--party-size", "4", "--level", "5", "--seed", "123")
        first, second = self.command(*args), self.command(*args)
        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(self.command("--help").returncode, 0)
        self.assertEqual(self.command("--version").returncode, 0)

    def test_custom_and_additive_catalogs(self):
        catalog = str(ROOT / "examples/homebrew.json")
        result = self.command("--validate-catalog", "--catalog", catalog)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("358 unique", result.stdout)
        result = self.command(
            "--catalog", catalog, "--no-default-catalog", "--party-size", "4", "--level", "5",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("15x Moss Guardian", result.stdout)
        self.assertIn("page/reference: Forest 1", result.stdout)

    def test_collision_and_override(self):
        catalog = str(ROOT / "examples/homebrew.json")
        args = ("--validate-catalog", "--no-default-catalog", "--catalog", catalog, "--catalog", catalog)
        self.assertEqual(self.command(*args).returncode, 2)
        self.assertEqual(self.command(*args, "--allow-overrides").returncode, 0)

    def test_error_exit_codes(self):
        for args in (
            ("--level", "21", "--party-size", "4"),
            ("--level", "5", "--party-size", "0"),
            ("--level", "5", "--party-size", "not-an-integer"),
            ("--difficulty", "deadly"),
            ("--catalog", "/nonexistent/data.json", "--validate-catalog"),
            ("--no-default-catalog", "--party-size", "4", "--level", "5"),
        ):
            with self.subTest(args=args):
                result = self.command(*args)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("Traceback", result.stderr)

    def test_invalid_json_catalog(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text(json.dumps({"schema_version": 2}))
            result = self.command("--catalog", str(path), "--validate-catalog")
            self.assertEqual(result.returncode, 2)
            self.assertIn(str(path), result.stderr)

    def test_eof(self):
        result = self.command(inputs="")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Input ended", result.stderr)
