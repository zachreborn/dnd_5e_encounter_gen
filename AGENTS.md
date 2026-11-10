# Agent Guide

## Project overview

Offline Python command-line random encounter generator for the 2024 revised
fifth-edition rules. Python 3.12+; continuous checks target 3.12–3.15. No
third-party runtime dependencies. uv manages development through
`[dependency-groups].dev` and the committed `uv.lock`; there is no `dev` extra.
Use uv 0.13.7 (the automated version). `.python-version` selects the Python 3.12
contributor baseline, not a narrower runtime support range.

The source package and distribution are `dnd_encounter_generator`, matching the
repository. The former `dnd_5e_encounter_gen` import/module path is retired; the
installed `dnd-encounter` command is unchanged. Keep metadata, package-resource
lookups, smoke checks, and documentation aligned with the new package name.

## Repository map

- `dnd_encounter_generator/catalog.py`: schema validation, JSON loading, immutable
  monster records, explicit pack merging.
- `dnd_encounter_generator/engine.py`: pure budget and bounded encounter generation.
- `dnd_encounter_generator/encounter_tables.py`: three revised difficulty budgets.
- `dnd_encounter_generator/cli.py`: argument parsing, interactive prompts, output,
  and exit codes.
- `dnd_encounter_generator/__main__.py`: module entry point.
- `dnd_encounter_generator/random_encounter_builder.py`: direct-script compatibility
  launcher; not the old helper API.
- `dnd_encounter_generator/data/`: versioned open JSON catalog and JSON Schema.
- `dnd_encounter_generator/NOTICE.txt`: mandatory open-content attribution and code
  licensing caveat. Do not remove from built artifacts.
- `legacy/monsters.py`: original unverified 511-record catalog. Preserved for
  migration only; excluded from wheel and source distributions.
- `tools/extract_srd.py`: development-only Poppler extraction and index check.
- `tools/migrate_legacy.py`: syntax-tree/literal conversion without execution.
- `tools/check_distribution.py`: isolated installed-artifact smoke checks.
- `tests/`: standard-library unit tests and subprocess smoke tests.
- `tests/fixtures/srd_index.json`: independently extracted official index.
- `examples/homebrew.json`: complete custom pack example.
- `.github/workflows/ci.yml`: CI workflow; pin actions to full commit hashes
  with release-version comments and retain distinct matrix check names.
- `pyproject.toml`: packaging, supported Python, development dependencies, lint
  and coverage. `setup.py` is only a shim; version is in `__init__.py`.
- `uv.lock`: committed universal development dependency lockfile.
- `.python-version`: local development interpreter default; automation explicitly
  selects each matrix interpreter.

## Running and validation

Install uv first, then run `uv sync --locked` from the repository root.
uv manages `.venv` and installs the project editable; no activation is required.
Exact synchronization can remove manually installed packages; preserve unrelated
user environments rather than deleting them.

```fish
uv run --locked dnd-encounter
uv run --locked python -B -m dnd_encounter_generator --party-size 4 --level 5 --seed 42
uv run --locked python -B dnd_encounter_generator/random_encounter_builder.py
uv run --locked dnd-encounter --validate-catalog
printf '4\n5\n\n\nn\n' | uv run --locked dnd-encounter
```

Installed command: `dnd-encounter`. Package-relative imports and resource loading
must work outside the checkout. Do not reintroduce bare sibling imports.

Plain `python3 -B -m dnd_encounter_generator` and direct-script execution remain
supported without uv. Never install into a managed system Python.
Use the locked development environment for validation:

```fish
uv sync --locked
uv lock --check
uv run --locked python -B -m unittest discover -s tests -v
uv run --locked python -B -m unittest discover -s tests/smoke -v
uv run --locked python -B -m coverage run -m unittest discover -s tests -v
uv run --locked python -B -m coverage report
uv run --locked ruff check .
uv build
uv run --locked python -B tools/check_distribution.py dist/*.whl dist/*.tar.gz
git diff --check
```

Add development dependencies with `uv add --dev PACKAGE`; use `uv lock` after
intentional metadata edits and `uv lock --upgrade-package NAME` for targeted
upgrades. Review and commit lockfile changes together with dependency changes.
Ordinary validation must use `--locked`, not silently regenerate the lockfile.
The lock covers development dependencies, not separately resolved isolated
setuptools build requirements. Do not claim builds are fully locked or offline.
Keep the artifact checker's pip installs in clean temporary environments as an
independent compatibility check for users without uv; do not replace them with
editable project installs. uv must not become a runtime dependency.

Default discovery includes smoke tests. Subprocesses must have timeouts. Tests
must control randomness or assert invariants rather than exact unseeded results.
Coverage measures branches with a 90% floor. Full schema parity needs the
development-only `jsonschema` package; without it that one check is skipped.
Do not describe a skipped check or an unrun platform matrix as passed.

## Rules and generation contracts

- Difficulties are `low`, `moderate`, `high`; default `moderate`. Budgets are
  independently transcribed from SRD 5.2.1 p.202, 20 levels each.
- Party size is positive, average level is 1–20. No legacy monster-count or
  small-party multipliers. Do not silently alias legacy difficulty names.
- Generation chooses one feasible creature and its greatest count under both
  budget and `max_monsters` (default 20). Mixed groups are not implemented.
- Require positive counts and experience spend no greater than budget.
  Zero-XP creatures are valid data but excluded from automatic generation.
- Empty or impossible filters raise `EncounterError`; never silently relax a
  filter or return an empty encounter.
- Inject a local random-number generator and sort candidates by stable IDs.
  Never use global mutable catalog initialization or randomness.
- Output reports requested difficulty, spend, and unused budget, not a false
  exact difficulty match. Retain danger/count/lair warnings and balance caveats.
- Repeating an encounter reuses party/filter inputs and advances the generator.
- Exit codes are 0 for success/clean EOF, 2 for user/catalog/encounter errors,
  and 130 for interruption. Normal input errors must not print tracebacks.

## Catalog and source contracts

- JSON only. Version-one envelope and named records are defined in the bundled
  schema. Preserve one source of truth: the small runtime schema interpreter and
  full-validator parity tests must be extended together with any schema changes.
- IDs are pack-qualified; never key by display name alone. Duplicate JSON keys
  and in-pack identities are errors. Cross-pack overrides require explicit
  `--allow-overrides`, with later packs winning. Bundled data loads first.
- Preserve exact challenge-rating strings, nonnegative integer experience,
  source revisions, optional string page references, aliases, tags, and custom
  extensions. Runtime rejects booleans and float tokens as integer fields.
- Never execute a catalog, follow reference URLs, or download content at runtime.
  Keep catalog size/error handling and tests for malformed data.
- Validate tag/alias types before set-based uniqueness checks. Monster reference
  and extension containers must be detached and recursively immutable, including
  records constructed directly or with `dataclasses.replace`.
- Bound `pdftotext` calls with a 60-second timeout and use explicit UTF-8 decoding
  and output encoding when regenerating the catalog and index manifest.
- Bundle all 330 indexed SRD 5.2.1 stat blocks plus 27 explicit lair variants
  (357 records). This does NOT mean the entire commercial Monster Manual.
  Additional content needs authorized user-supplied packs.
- Verify source names, pages and metadata against the versioned official
  document, the independent index manifest and the challenge-rating reward
  table. Do not generate an expected fixture from the same parsed catalog.
- Preserve the source's Archmage discrepancy: p.305 says 8,000 experience;
  the general rating-12 table says 8,400. The record includes an explicit note.
  Lair variants use their printed higher reward with the base challenge rating.
- Retain the exact required Creative Commons Attribution 4.0 notice and
  document adaptations. Source checksum/extraction provenance must be updated
  deliberately. Automated source checks are not an independent human review.
- The code's prior “BSD” declaration has no tracked license text. Do not choose
  a license variant or imply a new grant without the owner's decision.
- Keep unverified legacy data out of distributable artifacts. Migration must
  preserve all five original positional values per record and supplementary
  string references, without relabeling them as modern/open content.

## Change hygiene

- Follow four-space indentation and focused, readable changes. Keep rules, data,
  domain logic and presentation separated.
- Work on a dedicated branch. Use `git branch` then `git switch`; never commit
  directly to main/master.
- Preserve user work. Do not commit or push unless requested; all requested
  commits must be signed.
- Do not track credentials, environment dumps, virtual environments, private
  catalogs, bytecode, build artifacts, or generated package metadata.
- Review final diff and `git diff --check`, run applicable tests/lint/build/
  installed-artifact checks, and report actual results and limitations.
- Update `README.md` and this guide when changing behavior, launch paths,
  data contracts, or supported validation commands.
