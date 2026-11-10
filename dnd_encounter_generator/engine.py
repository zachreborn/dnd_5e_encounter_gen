"""Pure, bounded encounter generation for the revised fifth-edition rules."""

import random
from dataclasses import dataclass
from fractions import Fraction

from .catalog import Monster, monster_types
from .encounter_tables import XP_DIFFICULTIES


class EncounterError(ValueError):
    """Invalid party settings or no eligible creature for the requested encounter."""


@dataclass(frozen=True)
class Encounter:
    monster: Monster
    count: int
    budget: int
    warnings: tuple[str, ...]

    @property
    def spent(self):
        return self.monster.xp * self.count

    @property
    def remaining(self):
        return self.budget - self.spent


def positive_integer(value, field):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise EncounterError(f"{field} must be a positive integer")
    return value


def xp_budget(party_size, party_level, difficulty="moderate"):
    positive_integer(party_size, "Party size")
    positive_integer(party_level, "Party level")
    if party_level > 20:
        raise EncounterError("Party level must be between 1 and 20")
    if difficulty not in XP_DIFFICULTIES:
        raise EncounterError("Difficulty must be low, moderate, or high (revised rules)")
    return XP_DIFFICULTIES[difficulty][party_level - 1] * party_size


def generate_encounter(
    monsters, party_size, party_level, difficulty="moderate", monster_type="all",
    max_monsters=20, rng=None,
):
    budget = xp_budget(party_size, party_level, difficulty)
    positive_integer(max_monsters, "Maximum monsters")
    if monster_type not in ("all", *monster_types()):
        raise EncounterError("Unknown monster type")
    candidates = sorted(
        (monster for monster in monsters
         if 0 < monster.xp <= budget
         and (monster_type == "all" or monster.monster_type == monster_type)),
        key=lambda monster: monster.id,
    )
    if not candidates:
        raise EncounterError(
            f"No positive-experience {monster_type} creature fits the {budget} XP budget. "
            "Choose another filter, catalog, level, or difficulty."
        )
    monster = (rng if rng is not None else random.Random()).choice(candidates)
    count = min(max_monsters, budget // monster.xp)
    warnings = []
    if Fraction(monster.challenge_rating) > party_level:
        warnings.append("Creature challenge rating exceeds party level; a single action may be lethal.")
    if count > 2 * party_size:
        warnings.append("More than two creatures per character; use fragile creatures and consider action economy.")
    if count == max_monsters and budget // monster.xp > max_monsters:
        warnings.append("Creature limit reached; substantial budget may remain unspent.")
    if "in-lair" in monster.tags:
        warnings.append("Lair variant selected; use its lair conditions and higher experience value.")
    return Encounter(monster, count, budget, tuple(warnings))
