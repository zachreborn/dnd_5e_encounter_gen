import random
import unittest
from dataclasses import replace

from dnd_encounter_generator.catalog import load_monsters, monster_types
from dnd_encounter_generator.engine import EncounterError, generate_encounter, xp_budget


class BudgetTests(unittest.TestCase):
    # Independently transcribed by row from SRD 5.2.1 p.202, not imported tables.
    ROWS = (
        (50, 75, 100), (100, 150, 200), (150, 225, 400), (250, 375, 500),
        (500, 750, 1100), (600, 1000, 1400), (750, 1300, 1700),
        (1000, 1700, 2100), (1300, 2000, 2600), (1600, 2300, 3100),
        (1900, 2900, 4100), (2200, 3700, 4700), (2600, 4200, 5400),
        (2900, 4900, 6200), (3300, 5400, 7800), (3800, 6100, 9800),
        (4500, 7200, 11700), (5000, 8700, 14200), (5500, 10700, 17200),
        (6400, 13200, 22000),
    )

    def test_all_levels_and_difficulties(self):
        for level, row in enumerate(self.ROWS, 1):
            for difficulty, amount in zip(("low", "moderate", "high"), row):
                for size in (1, 2, 4, 6):
                    with self.subTest(level=level, difficulty=difficulty, size=size):
                        self.assertEqual(xp_budget(size, level, difficulty), amount * size)
        self.assertEqual(xp_budget(4, 5), 3000)
        self.assertEqual(xp_budget(5, 3), 1125)
        self.assertEqual(xp_budget(6, 15, "high"), 46800)

    def test_invalid_input(self):
        for size, level, difficulty in (
            (0, 1, "low"), (-1, 1, "low"), (True, 1, "low"),
            (1.5, 1, "low"), (1, 0, "low"), (1, 21, "high"),
            (1, False, "low"), (1, "5", "low"), (1, 1, "deadly"),
        ):
            with self.subTest(size=size, level=level, difficulty=difficulty):
                with self.assertRaises(EncounterError):
                    xp_budget(size, level, difficulty)


class GenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.monsters = load_monsters()
        cls.goblin = next(monster for monster in cls.monsters if monster.name == "Goblin Warrior")

    def test_single_type_exact_fit_and_small_party(self):
        monster = replace(self.goblin, xp=50)
        for size in (1, 2, 4):
            encounter = generate_encounter([monster], size, 1, "low", rng=random.Random(1))
            self.assertEqual(encounter.count, size)
            self.assertEqual(encounter.spent, encounter.budget)
            self.assertEqual(encounter.remaining, 0)

    def test_under_budget_and_count_cap(self):
        monster = replace(self.goblin, xp=30)
        encounter = generate_encounter([monster], 4, 1, "low")
        self.assertEqual(encounter.count, 6)
        self.assertEqual(encounter.remaining, 20)
        capped = generate_encounter([monster], 4, 20, max_monsters=3)
        self.assertEqual(capped.count, 3)
        self.assertTrue(any("limit reached" in warning for warning in capped.warnings))
        self.assertFalse(any("two creatures" in warning for warning in capped.warnings))

    def test_warnings(self):
        monster = replace(self.goblin, xp=10, challenge_rating="2", tags=("in-lair",))
        encounter = generate_encounter([monster], 1, 1)
        self.assertEqual(encounter.count, 7)
        self.assertEqual(len(encounter.warnings), 3)
        self.assertTrue(any("lair" in warning for warning in encounter.warnings))

    def test_no_eligible_creature(self):
        for monsters, monster_type in (
            ([], "all"),
            ([replace(self.goblin, xp=0)], "all"),
            ([replace(self.goblin, xp=100000)], "all"),
            ([self.goblin], "plant"),
        ):
            with self.subTest(monster_type=monster_type, monsters=monsters):
                with self.assertRaisesRegex(EncounterError, "No positive-experience"):
                    generate_encounter(monsters, 1, 1, monster_type=monster_type)

    def test_invalid_filter_and_limits(self):
        for options in ({"monster_type": "invalid"}, {"max_monsters": 0}, {"max_monsters": True}):
            with self.assertRaises(EncounterError):
                generate_encounter(self.monsters, 4, 5, **options)

    def test_seed_and_catalog_order(self):
        one = generate_encounter(self.monsters, 4, 5, rng=random.Random(42))
        two = generate_encounter(reversed(self.monsters), 4, 5, rng=random.Random(42))
        self.assertEqual(one, two)

    def test_invariants_across_levels_types_and_seeds(self):
        for level in range(1, 21):
            for kind in ("all", *monster_types()):
                for seed in range(5):
                    with self.subTest(level=level, kind=kind, seed=seed):
                        eligible = [monster for monster in self.monsters if
                                    0 < monster.xp <= xp_budget(4, level)
                                    and (kind == "all" or kind == monster.monster_type)]
                        if not eligible:
                            with self.assertRaises(EncounterError):
                                generate_encounter(self.monsters, 4, level, monster_type=kind)
                            continue
                        result = generate_encounter(
                            self.monsters, 4, level, monster_type=kind, rng=random.Random(seed),
                        )
                        self.assertGreater(result.count, 0)
                        self.assertLessEqual(result.count, 20)
                        self.assertLessEqual(result.spent, result.budget)
                        self.assertGreaterEqual(result.remaining, 0)
                        self.assertIn(result.monster, eligible)
