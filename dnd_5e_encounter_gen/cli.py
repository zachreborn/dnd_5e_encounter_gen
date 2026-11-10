"""Command-line interface; domain functions do not read input or print."""

import argparse
import random
import sys

from . import __version__
from .catalog import CatalogError, load_monsters, monster_types
from .engine import EncounterError, generate_encounter, positive_integer, xp_budget


def parser():
    result = argparse.ArgumentParser(description="Offline revised fifth-edition encounter generator (2024 rules).")
    result.add_argument("--version", action="version", version=__version__)
    result.add_argument("--party-size", type=int)
    result.add_argument("--level", type=int, help="Average party level, 1–20")
    result.add_argument("--difficulty", choices=("low", "moderate", "high"), default="moderate")
    result.add_argument("--type", dest="monster_type", type=str.lower, choices=("all", *monster_types()), default="all")
    result.add_argument("--seed", type=int, help="Repeatable results for identical catalogs, settings and Python version")
    result.add_argument("--max-monsters", type=int, default=20, help="Generation cap, not a rules multiplier (default: 20)")
    result.add_argument("--catalog", action="append", default=[], metavar="PATH", help="Add a local JSON pack; repeat in merge order")
    result.add_argument("--no-default-catalog", action="store_true", help="Load only explicitly supplied catalogs")
    result.add_argument("--allow-overrides", action="store_true", help="Explicitly allow last-pack-wins identity replacement")
    result.add_argument("--validate-catalog", action="store_true", help="Validate selected catalogs and exit")
    return result


def prompt_integer(prompt, maximum=None):
    while True:
        try:
            value = int(input(prompt))
            positive_integer(value, "Value")
            if maximum is not None and value > maximum:
                raise EncounterError(f"Value must be between 1 and {maximum}")
            return value
        except ValueError as error:
            print(f"Error: {error}; try again.")


def prompt_choice(prompt, default, choices, help_text=None):
    while True:
        value = input(prompt).strip().lower()
        if value == "":
            return default
        if value == "?" and help_text:
            print(help_text)
        elif value in choices:
            return value
        else:
            print("Error: choose one of: " + ", ".join(choices))


def display(encounter, size, level, difficulty, monster_type):
    monster = encounter.monster
    print(
        f"Randomized encounter (2024 rules):\nParty Size: {size}\nParty Level: {level}\n"
        f"Requested difficulty: {difficulty}\nMonster type: {monster_type}\n"
        f"{encounter.count}x {monster.name} [{monster.id}]\n"
        f"Challenge rating: {monster.challenge_rating}; XP each: {monster.xp}\n"
        f"Budget: {encounter.budget} XP; spent: {encounter.spent} XP; unused: {encounter.remaining} XP"
    )
    for reference in monster.references:
        page = f", page/reference: {reference['page']}" if "page" in reference else ""
        print(f"Source: {reference['publication']}{page}")
    if not monster.references:
        print("Source: user catalog (no publication reference supplied)")
    for warning in encounter.warnings:
        print(f"Warning: {warning}")
    print("Budget guidance is not a guarantee of encounter difficulty.")


def run(args):
    positive_integer(args.max_monsters, "Maximum monsters")
    monsters = load_monsters(args.catalog, not args.no_default_catalog, args.allow_overrides)
    if args.validate_catalog:
        print(f"Valid catalogs: {len(monsters)} unique monster records.")
        return 0
    interactive = args.party_size is None and args.level is None
    if not interactive and (args.party_size is None or args.level is None):
        raise EncounterError("--party-size and --level must be supplied together")
    if interactive:
        size = prompt_integer("Party size?> ")
        level = prompt_integer("Party average level?> ", maximum=20)
        difficulty = prompt_choice(
            f"Select difficulty: Low, Moderate, High [{args.difficulty.title()}]> ", args.difficulty,
            ("low", "moderate", "high"),
        )
        monster_type = prompt_choice(
            f"Select monster type: ? for choices, [{args.monster_type.title()}]> ", args.monster_type,
            ("all", *monster_types()), "Monster types: all, " + ", ".join(monster_types()),
        )
    else:
        size, level, difficulty, monster_type = args.party_size, args.level, args.difficulty, args.monster_type
    xp_budget(size, level, difficulty)
    rng = random.Random(args.seed)
    while True:
        encounter = generate_encounter(
            monsters, size, level, difficulty, monster_type, args.max_monsters, rng,
        )
        display(encounter, size, level, difficulty, monster_type)
        if not interactive or prompt_choice(
            "Run again? Y/N [Y]> ", "y", ("y", "yes", "n", "no"),
        ) in ("n", "no"):
            return 0


def main(argv=None):
    try:
        return run(parser().parse_args(argv))
    except (CatalogError, EncounterError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    except EOFError:
        print("\nInput ended.", file=sys.stderr)
        return 0
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130
