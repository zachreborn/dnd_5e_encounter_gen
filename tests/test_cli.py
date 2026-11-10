import contextlib
import io
import unittest
from dataclasses import replace
from unittest.mock import patch

from dnd_5e_encounter_gen import cli
from dnd_5e_encounter_gen.catalog import load_monsters
from dnd_5e_encounter_gen.engine import generate_encounter


class CliTests(unittest.TestCase):
    def call(self, argv, inputs=()):
        output, errors = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            with patch("builtins.input", side_effect=inputs):
                result = cli.main(argv)
        return result, output.getvalue(), errors.getvalue()

    def test_interactive_defaults_repeat_and_help(self):
        result, output, errors = self.call([], ["4", "5", "", "?", "", "bad", "", "n"])
        self.assertEqual(result, 0)
        self.assertEqual(errors, "")
        self.assertIn("Monster types:", output)
        self.assertIn("Requested difficulty: moderate", output)
        self.assertEqual(output.count("Party Size: 4"), 2)
        self.assertEqual(output.count("Party Level: 5"), 2)

    def test_integer_retries_and_choices(self):
        result, output, _ = self.call(
            [], ["bad", "-1", "0", "2", "21", "0", "1", "bad", "HIGH", "bad", "FEY", "no"],
        )
        self.assertEqual(result, 0)
        self.assertIn("try again", output)
        self.assertIn("Requested difficulty: high", output)
        self.assertIn("Monster type: fey", output)

    def test_missing_party_option_is_not_interactive(self):
        for argv in (["--party-size", "4"], ["--level", "5"]):
            result, _, errors = self.call(argv)
            self.assertEqual(result, 2)
            self.assertIn("supplied together", errors)

    def test_noninteractive_seed(self):
        arguments = ["--party-size", "4", "--level", "5", "--seed", "42"]
        first = self.call(arguments)
        self.assertEqual(first[0], 0)
        self.assertEqual(first, self.call(arguments))
        self.assertIn("Budget: 3000 XP", first[1])

    def test_validation(self):
        result, output, _ = self.call(["--validate-catalog"])
        self.assertEqual(result, 0)
        self.assertIn("357 unique monster", output)

    def test_empty_filter_and_bad_limit(self):
        for args in (
            ["--no-default-catalog", "--party-size", "4", "--level", "5"],
            ["--max-monsters", "0"],
            ["--catalog", "/nonexistent/catalog.json"],
        ):
            result, _, errors = self.call(args)
            self.assertEqual(result, 2)
            self.assertIn("Error:", errors)
            self.assertNotIn("Traceback", errors)

    def test_eof_and_interrupt(self):
        for error, code, message in ((EOFError(), 0, "Input ended"), (KeyboardInterrupt(), 130, "Cancelled")):
            result, _, errors = self.call([], [error])
            self.assertEqual(result, code)
            self.assertIn(message, errors)

    def test_display_optional_references_and_warnings(self):
        monster = load_monsters()[0]
        for references in ((), ({"publication": "Campaign"},)):
            selected = replace(monster, xp=10, challenge_rating="0", references=references)
            encounter = generate_encounter([selected], 1, 1)
            with contextlib.redirect_stdout(io.StringIO()) as output:
                cli.display(encounter, 1, 1, "moderate", "all")
            self.assertIn("Source:", output.getvalue())
            self.assertIn("Warning:", output.getvalue())
