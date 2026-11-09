"""Convert a literal legacy cr_dict to a private JSON pack, without executing it."""

import argparse
import ast
import json
import re
from pathlib import Path


def convert(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    dictionaries = [
        node.value for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "cr_dict"
                for target in node.targets)
    ]
    if len(dictionaries) != 1 or not isinstance(dictionaries[0], ast.Dict):
        raise ValueError("Expected exactly one literal cr_dict dictionary")
    literal = dictionaries[0]
    names = [ast.literal_eval(key) for key in literal.keys]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate legacy monster names")
    source = ast.literal_eval(literal)
    records = []
    for name, values in source.items():
        if not isinstance(values, list) or len(values) != 5:
            raise ValueError(f"{name}: expected five positional fields")
        page, cr, xp, size, monster_type = values
        records.append({
            "id": "legacy:" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"),
            "name": name,
            "challenge_rating": cr,
            "xp": xp,
            "size": size.lower(),
            "monster_type": monster_type.lower(),
            "rules_revision": "legacy",
            "references": [{"publication": "Legacy catalog (source unverified)", "page": str(page)}],
            "extensions": {"legacy_values": values},
        })
    if len({record["id"] for record in records}) != len(records):
        raise ValueError("Legacy identity collision")
    return {
        "schema_version": 1,
        "pack_id": "legacy",
        "pack_version": "1",
        "source": {"title": "Existing repository catalog; redistribution provenance unverified"},
        "license": "UNVERIFIED - private migration only",
        "monsters": records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path, help="Keep outside the repository; do not redistribute uncleared data.")
    args = parser.parse_args()
    pack = convert(args.source)
    # Exclusive creation avoids overwriting existing user catalogs.
    with args.destination.open("x", encoding="utf-8") as output:
        json.dump(pack, output, indent=2)
        output.write("\n")
    print(f"Migrated {len(pack['monsters'])} records; original values retained per record in extensions.legacy_values.")


if __name__ == "__main__":
    main()
