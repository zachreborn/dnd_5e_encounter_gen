import tomllib
import unittest
from importlib.resources import files
from pathlib import Path

import dnd_encounter_generator

ROOT = Path(__file__).resolve().parents[1]


class PackageIdentityTests(unittest.TestCase):
    def test_distribution_and_entry_points_use_current_package(self):
        config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(config["project"]["name"], "dnd_encounter_generator")
        self.assertEqual(config["project"]["scripts"]["dnd-encounter"], "dnd_encounter_generator.cli:main")
        self.assertEqual(config["tool"]["setuptools"]["packages"],
                         ["dnd_encounter_generator", "dnd_encounter_generator.data"])
        self.assertEqual(config["tool"]["setuptools"]["dynamic"]["version"]["attr"],
                         "dnd_encounter_generator.__version__")

    def test_source_and_resources_live_under_current_package(self):
        self.assertEqual(Path(dnd_encounter_generator.__file__).parent, ROOT / "dnd_encounter_generator")
        resources = files("dnd_encounter_generator")
        self.assertTrue(resources.joinpath("data/srd_5_2_1.json").is_file())
        self.assertTrue(resources.joinpath("data/catalog.schema.json").is_file())
        self.assertTrue(resources.joinpath("NOTICE.txt").is_file())
        self.assertFalse((ROOT / "dnd_5e_encounter_gen").exists())
