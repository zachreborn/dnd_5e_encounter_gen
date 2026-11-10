"""Inspect and install both build artifacts, then smoke-test outside the checkout."""

import argparse
import json
import subprocess
import tarfile
import tempfile
import venv
import zipfile
from pathlib import Path


def command(arguments, cwd, inputs=None):
    result = subprocess.run(
        arguments, cwd=cwd, input=inputs, text=True, capture_output=True, timeout=180,
    )
    if result.returncode:
        raise RuntimeError(f"Command failed: {arguments}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def check(artifact):
    if not artifact.name.startswith("dnd_encounter_generator-"):
        raise RuntimeError(f"{artifact.name}: unexpected distribution name")
    if artifact.suffix == ".whl":
        with zipfile.ZipFile(artifact) as archive:
            names = archive.namelist()
    else:
        with tarfile.open(artifact, "r:gz") as archive:
            names = archive.getnames()
    for suffix in ("data/srd_5_2_1.json", "data/catalog.schema.json", "NOTICE.txt"):
        if not any(name.endswith(suffix) for name in names):
            raise RuntimeError(f"{artifact.name}: missing {suffix}")
    if any("/legacy/" in "/" + name or name.endswith("/monsters.py") for name in names):
        raise RuntimeError(f"{artifact.name}: unverified legacy data included")
    with tempfile.TemporaryDirectory(prefix="dnd-installed-") as directory:
        root = Path(directory)
        environment = root / "venv"
        venv.create(environment, with_pip=True)
        python = str(environment / "bin/python")
        command([python, "-I", "-m", "pip", "install", "--no-deps", str(artifact)], root)
        module = [python, "-I", "-B", "-m", "dnd_encounter_generator"]
        output = command([*module, "--party-size", "4", "--level", "5", "--seed", "42"], root)
        if "Budget: 3000 XP" not in output:
            raise RuntimeError("Incorrect installed generation result")
        output = command([*module, "--validate-catalog"], root)
        if "357 unique" not in output:
            raise RuntimeError("Bundled catalog is incomplete")
        console = str(environment / "bin/dnd-encounter")
        command([console, "--help"], root)
        output = command([console], root, "4\n5\n\n\nn\n")
        if "Run again?" not in output:
            raise RuntimeError("Installed interactive command failed")
        # Ensure the runtime works with sockets unavailable; install/build may use
        # networking for build tools, but catalog loading and generation must not.
        offline = (
            "import socket; from unittest.mock import patch; "
            "from importlib.metadata import metadata; "
            "from importlib.resources import files; "
            "from dnd_encounter_generator.cli import main; "
            "assert metadata('dnd_encounter_generator')['Name'].replace('-', '_') == 'dnd_encounter_generator'; "
            "assert 'Creative Commons' in files('dnd_encounter_generator').joinpath('NOTICE.txt').read_text(); "
            "p=patch.object(socket, 'socket', side_effect=AssertionError('network forbidden')); "
            "p.start(); raise SystemExit(main(['--party-size','4','--level','5']))"
        )
        command([python, "-I", "-B", "-c", offline], root)
        example = root / "custom.json"
        example.write_text(json.dumps({
            "schema_version": 1, "pack_id": "test", "pack_version": "1",
            "source": {"title": "Installed test"}, "license": "CC0-1.0",
            "monsters": [{
                "id": "test:guardian", "name": "Guardian", "xp": 200,
                "challenge_rating": "1", "size": "medium",
                "monster_type": "plant", "rules_revision": "2024-homebrew",
            }],
        }))
        command([console, "--catalog", str(example), "--no-default-catalog",
                 "--party-size", "4", "--level", "5"], root)
    print(f"Verified {artifact.name}: contents, clean install, command, module, custom data, offline runtime.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifacts", type=Path, nargs="+")
    args = parser.parse_args()
    for artifact in args.artifacts:
        check(artifact.resolve())


if __name__ == "__main__":
    main()
