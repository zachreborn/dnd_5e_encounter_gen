# Agent Guide

## Project overview

This is a Python command-line random encounter generator for Dungeons & Dragons
5th edition. It calculates an experience-point (XP) budget from party size, average
level, and difficulty; chooses a random monster within an XP allowance; and adjusts
the monster count for encounter size. It runs locally with static data and no
runtime dependencies outside the Python standard library.

## Repository map

- `dnd_5e_encounter_gen/random_encounter_builder.py`: interactive prompts,
  `Monster`, XP budgeting, random selection, encounter sizing, and script entry
  point.
- `dnd_5e_encounter_gen/encounter_tables.py`: per-character difficulty thresholds
  for levels 1–20 and the accepted monster-type filters.
- `dnd_5e_encounter_gen/monsters.py`: `cr_dict`, the monster catalog grouped by
  challenge rating.
- `dnd_5e_encounter_gen/__init__.py`: package author and version metadata.
- `setup.py`: setuptools packaging, with a legacy distutils fallback.
- `README.md`: user-facing overview, sample interaction, and future ideas.

## Running the program

Run commands from the repository root:

```fish
python3 -B dnd_5e_encounter_gen/random_encounter_builder.py
```

No installation is needed for this launch method. The README's shorter
`python random_encounter_builder.py` command assumes the package directory is the
working directory.

The builder uses bare sibling imports (`import monsters` and
`import encounter_tables`). Direct script execution supplies the required import
path; package import and `python3 -m dnd_5e_encounter_gen.random_encounter_builder`
are not currently supported by those imports. Do not recommend an installed
console command: `setup.py` defines no console entry point.

The README describes Python 3.4, but there is no declared minimum version,
supported-version matrix, or pinned interpreter. Do not treat that historical
description as a verified compatibility guarantee. Avoid silently requiring a
newer Python version when making unrelated changes.

## Implementation conventions and contracts

- Follow the existing four-space indentation, snake_case functions and variables,
  `Monster` class naming, and surrounding string/formatting style. Avoid
  repository-wide reformatting or dependency additions for small changes.
- Keep monster data in `monsters.py` and difficulty/type tables in
  `encounter_tables.py`, rather than duplicating them in the builder.
- Each `cr_dict` entry maps a unique monster name to exactly five positional
  values: `[page_reference, challenge_rating, xp, size, monster_type]`.
  `main()` expands these into `Monster(name, *values)`; preserve that order.
- Page references may be integers or strings such as `'MaD 31'`. Challenge ratings
  are strings, including fractions such as `'1/8'`. XP values are positive
  integers. Preserve supplementary catalog entries and string references.
- Difficulty keys are `easy`, `medium`, `hard`, and `deadly`. Each threshold list
  has 20 entries, indexed by `party_level - 1`; `xp_budget()` multiplies the
  threshold by party size. Valid levels are 1–20 and party size must be positive.
- Filter choices are lowercase, including the special value `all`. Selection
  compares a specific filter's capitalized spelling with the catalog's type
  field. Keep accepted choices and catalog types aligned.
- `xp_list_gen()` randomly chooses a budget divisor of at least 10 whose quotient
  is at most 20. `rnd_select_monster()` selects among monsters at the nearest
  eligible XP value without exceeding that allowance.
- `build_encounter_size()` applies the existing count thresholds and multipliers,
  including a special adjustment for parties of one or two. Treat changes to
  these rules as behavior changes requiring focused tests.
- `main()` populates the module-level `monsters_dict` before starting
  `script_run()`. Importing the module alone does not populate that dictionary.
- Repeating an encounter reuses the original party and filter inputs; it does
  not prompt for a new party on each iteration.
- Version metadata currently appears in both `setup.py` and `__init__.py`.
  Update both if a requested change includes a version bump.

## Validation

There are no tracked automated tests, continuous integration workflows, formatter
settings, or lint/type-check commands. Do not claim that a test suite passed when
only a smoke check was run, and do not assume pytest or other tools are installed.

A basic end-to-end smoke check uses four level-five characters, the default
medium difficulty, the default all-types filter, and exits after one encounter:

```fish
printf '4\n5\n\n\nn\n' | python3 -B dnd_5e_encounter_gen/random_encounter_builder.py
```

Expect party details, a monster count/name, a page reference, and a repeat prompt.
The monster and count vary randomly; do not assert an exact unseeded result.
The `-B` flag avoids leaving bytecode artifacts in this repository.

For behavior changes, add focused regression tests. Standard-library `unittest`
is an option without a new dependency, not an existing project test convention.
When testing the builder without changing its imports, explicitly make the
package directory available on the test import path. Initialize or clear
`monsters_dict` as needed to isolate tests. Control randomness with a fixed seed
or mocks, and mock `input()` for prompt tests.

Cover the relevant budget boundaries, each difficulty, small-party count
adjustments, all-types and specific-type selection, and invalid/default inputs.
For catalog/table changes, verify record shape, positive XP, type consistency,
unique dictionary keys, and 20 thresholds per difficulty.

## Existing limitations to account for

- `get_user_input_str()` uses `val is ''` instead of an equality comparison.
  Modern Python can emit a `SyntaxWarning`; do not copy this pattern into new
  code or conceal the warning as a documentation fix.
- A specific monster type may have no monster within the chosen allowance.
  Selection then calls `min()` on an empty collection and raises `ValueError`.
- Integer prompts reject non-integers but do not enforce valid party ranges.
  Range validation happens later in `xp_budget()`, and the interactive loop does
  not catch that exception.
- Although the monster-type prompt mentions `?`, it is not an accepted choice
  and does not display help.
- `xp_list_gen()` assumes a usable positive budget; arbitrary values with no
  eligible divisors can fail. Test its actual preconditions when changing it.

Keep unrelated bug fixes separate from documentation or data-only tasks. Update
the README when deliberately changing launch instructions or user-visible behavior.

## Change hygiene

- Work on a dedicated branch; never commit directly to `master` or `main`.
  Use `git branch` to create a branch and `git switch` to change branches.
- Keep changes focused and preserve existing user work. Do not commit or push
  unless requested; any requested commits must be signed.
- Do not add credentials, environment dumps, virtual environments, bytecode,
  build directories, or generated packaging metadata to version control.
- Before handing off, run applicable checks, inspect `git diff --check` and the
  final diff, and report what was verified and any known failures separately.
