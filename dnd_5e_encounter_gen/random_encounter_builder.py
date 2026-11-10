"""Compatibility launcher for direct execution from older installations."""

if __package__:
    from .cli import main
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from dnd_5e_encounter_gen.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
