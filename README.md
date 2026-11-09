# Revised fifth-edition encounter generator

An offline Python encounter generator for the **2024 revised fifth-edition
Dungeons & Dragons rules**, with customizable JSON monster catalogs.
Requires **Python 3.12 or newer**; automated checks target Python 3.12–3.15.
There are no third-party runtime dependencies.

## Rules and monster coverage

The default catalog includes **all 330 stat blocks in System Reference Document
(SRD) 5.2.1**, including animals, plus **27 explicitly listed in-lair variants**:
357 selectable records in total. These are encounter-selection metadata, not
complete combat stat blocks. Publication references point to the SRD, not to
Monster Manual page numbers.

This supports the revised rules underlying the 2024 rulebooks and 2025 Monster
Manual. It does **not** bundle every commercial Monster Manual creature.
Some monsters, such as the Beholder, are excluded from the open SRD. Add
authorized additional content and homebrew through local JSON packs; ownership
of a book does not itself establish redistribution rights. Nothing is fetched
or scraped at runtime.

The revised rules use **Low, Moderate, High** difficulty budgets, with Moderate
as the default. Monster experience points (XP) are summed directly, without the
legacy group-size or small-party multipliers. Four level-five characters have
a Moderate budget of 3,000 XP.

Generation selects a feasible creature at random and spends as much of the
budget on that creature as possible, up to `--max-monsters` (default 20).
This is a generation cap, not an official rules multiplier. Results can leave
substantial XP unused; output shows the **requested** difficulty, budget, spend,
and remainder rather than claiming an exact difficulty match.
Zero-XP creatures remain in the catalog but are excluded from automatic
generation. Empty filters produce a clear error, not a relaxed filter.

Warnings flag creatures above party level, more than two creatures per
character, count limits, and lair variants. Party composition, abilities, terrain,
and action economy still affect danger. Budget guidance is not a balance guarantee.
The initial generator uses one creature stat block per encounter; mixed groups
and location filtering are not implemented.

## Run without installing

From the repository root:

```fish
python3 -B -m dnd_5e_encounter_gen
```

The older direct-script launch path remains available:

```fish
python3 -B dnd_5e_encounter_gen/random_encounter_builder.py
```

Interactive mode prompts for party size, average level (1–20), difficulty, and
monster type. Enter `?` at the type prompt for choices. Repeating an encounter
reuses party settings and advances the random generator.

For a single noninteractive encounter:

```fish
python3 -B -m dnd_5e_encounter_gen --party-size 4 --level 5 --difficulty moderate --type undead --seed 42
```

Supply `--party-size` and `--level` together. `--seed` reproduces a sequence for
the same catalog contents, arguments, generator implementation, and Python
version; it is not a permanent cross-version encounter identifier.

Exit codes: `0` for success or clean end-of-input, `2` for bad arguments,
catalogs, or an impossible encounter, and `130` for interruption.

## Install locally

Use an isolated environment, not a system Python install:

```fish
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/dnd-encounter --party-size 4 --level 5
```

After activation, the installed command is `dnd-encounter`. The installed module
also runs from any working directory; catalogs are loaded as package resources.

## Customize monsters

Copy `examples/homebrew.json` into a private location and edit its named fields.
JSON is the canonical format; YAML is not supported in this release.
The schema is `dnd_5e_encounter_gen/data/catalog.schema.json`.

Each pack supplies `schema_version` (currently `1`), `pack_id`, `pack_version`,
`source` (at least a title), `license`, and a `monsters` array. Each monster
requires `id`, `name`, `challenge_rating`, `xp`, `size`, `monster_type`, and
`rules_revision`. See the example for the complete envelope.

```json
{
  "id": "my-campaign:moss-guardian",
  "name": "Moss Guardian",
  "challenge_rating": "1",
  "xp": 200,
  "size": "medium",
  "monster_type": "plant",
  "rules_revision": "2024-homebrew",
  "references": [{"publication": "Campaign notes", "page": "Forest 1"}],
  "tags": ["forest"],
  "extensions": {"encounter_hook": "Protects a forgotten grove."}
}
```

IDs are stable and pack-qualified; display names need not be unique. Sizes and
creature types are lowercase. Challenge ratings are strings: `"0"`, `"1/8"`,
`"1/4"`, `"1/2"`, or integers `"1"`–`"30"`. XP must use a nonnegative JSON
integer token, not a string, boolean, or float; homebrew XP need not follow the
official challenge-rating table. Both zero and ten XP are supported at rating zero.
Size options and swarms can retain values such as `"medium or small"` and
`"medium swarm of tiny"`. `"colossal"` is supported for legacy/custom data.

References, aliases, tags, and an `extensions` object are optional. Page
references are strings, preserving entries such as `"MaD 31"`. Add custom
metadata under `extensions`; unknown monster fields are rejected to catch typos.
This small schema can be extended through a future schema version without
changing encounter generation.

Validate a pack without starting an encounter:

```fish
python3 -B -m dnd_5e_encounter_gen --no-default-catalog --catalog examples/homebrew.json --validate-catalog
```

To add a pack to the open default catalog, use `--catalog PATH`. Repeat that
option for multiple packs. To use only your packs, add `--no-default-catalog`.
Duplicate IDs within a pack are always errors. Across packs they are errors
unless `--allow-overrides` is explicitly supplied, in which case later packs
replace earlier records with the same ID. The bundled catalog loads first.
An override record retains the original ID, even when its enclosing pack has
a different ID. Same-name creatures with different IDs remain distinct.

Duplicate JSON keys, nonstandard numeric constants, unsupported versions,
invalid fields, invalid UTF-8, and catalogs over 10,000,000 characters are rejected.
The loader never evaluates code or fetches reference links.

## Migrate an existing catalog

The original 511-record catalog is preserved unchanged at `legacy/monsters.py`.
It mixes legacy official and supplementary material with unverified
redistribution provenance, so it is **not included in wheel or source
distributions**, not loaded by default, and not relabeled as modern open content.

From a repository checkout, migrate it into a private location outside the
repository:

```fish
python3 -B tools/migrate_legacy.py legacy/monsters.py /absolute/private/path/legacy.json
python3 -B -m dnd_5e_encounter_gen --no-default-catalog --catalog /absolute/private/path/legacy.json --validate-catalog
```

The destination must not already exist. The converter reads literal dictionary
data with Python's syntax parser; it does not import or execute a Python catalog.
Every migrated record retains its exact original five values under
`extensions.legacy_values`, which serves as the per-record migration report.
Names and references are preserved, while size/type capitalization is normalized.
The loader accepts the nonstandard legacy `colossal` size. Review source rights
before sharing migrated packs.

Legacy difficulty names (`easy`, `medium`, `hard`, `deadly`) are deliberately
replaced, not silently mapped to revised difficulties. The old global dictionary
and helper-function interfaces are not preserved as a public library interface.

## Source verification and updates

The bundled pack records the official PDF URL, SHA-256 checksum, extractor
version, and verification date. Its 330 identities and page references are
checked against a separately extracted index manifest in
`tests/fixtures/srd_index.json`. Tests also check standard XP values, explicit
lair variants, fractional ratings, zero-XP entries, and important revised types.

One verified source discrepancy is preserved: **Archmage has 8,000 XP on page
305**, although the general challenge-rating table on page 256 gives 8,400 for
rating 12. Its `extensions.source_note` records that difference; no guessed
correction is applied. Gold Dragon Wyrmling also uses an alternate printed XP
format that the extractor explicitly handles.

To reproduce extraction, obtain the version-pinned PDF from the official
[SRD page](https://www.dndbeyond.com/srd), install Poppler's `pdftotext`, then run:

```fish
python3 -B tools/extract_srd.py /path/to/SRD_CC_v5.2.1.pdf dnd_5e_encounter_gen/data/srd_5_2_1.json --index-manifest tests/fixtures/srd_index.json
```

PDF tooling is development-only. Review source changes and catalog diffs before
updating the pack and its independent index fixture. Do not update a fixture
merely to make a failing test pass. Automated extraction/index checks are not
a claim that an independent human has reviewed every field.

## Development and validation

```fish
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -B -m unittest discover -s tests -v
.venv/bin/python -B -m unittest discover -s tests/smoke -v
.venv/bin/python -B -m coverage run -m unittest discover -s tests -v
.venv/bin/python -B -m coverage report
.venv/bin/ruff check .
.venv/bin/python -m build
.venv/bin/python -B tools/check_distribution.py dist/*.whl dist/*.tar.gz
git diff --check
```

The default test discovery includes the smoke suite; its separate command is
useful during focused checks. Standard-library tests run without development
dependencies, except that the full-schema parity check is skipped unless
`jsonschema` is installed. Coverage enforces a 90% floor with branch measurement.
The artifact checker installs both build formats in clean temporary environments,
runs from outside the checkout, verifies notices and bundled data, exercises
custom packs, and tests runtime generation with socket creation blocked.
Build/install steps may access a package index for build tools; runtime needs
no network.

GitHub Actions runs unit, catalog, smoke, lint, coverage, build, and installed-
artifact checks on Linux with Python 3.12–3.15 and on macOS with Python 3.15.
Development-only dependencies do not become runtime requirements.

## Licensing

This work includes material from the System Reference Document 5.2.1 (“SRD 5.2.1”) by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2.1 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.

See `dnd_5e_encounter_gen/NOTICE.txt` for adaptations and licensing boundaries.
The original code metadata said “BSD” without a license text. The repository
owner must clarify the code license before public redistribution; the open game
content license does not license application code.
