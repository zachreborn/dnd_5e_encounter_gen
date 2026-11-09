"""Extract encounter metadata from the version-pinned, official SRD PDF.

Development only; requires Poppler's pdftotext. No network access is performed.
The independent index manifest is extracted separately from the stat blocks.
"""

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

SOURCE_URL = "https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf"
SOURCE_SHA256 = "8974902d109d6e63672d7c490bde9ccf052410503d9cfa768237154fbc5e3d87"
SIZES = r"(?:Tiny|Small|Medium|Large|Huge|Gargantuan)"
TYPES = (
    r"(?:Aberration|Beast|Celestial|Construct|Dragon|Elemental|Fey|Fiend|"
    r"Giant|Humanoid|Monstrosity|Ooze|Plant|Undead)"
)
DESCRIPTOR = re.compile(
    rf"^({SIZES}(?: or {SIZES})?|{SIZES} [Ss]warm of {SIZES}) ({TYPES})s?\b"
)
CR = re.compile(r"^CR (\d+(?:/\d+)?) \(XP ([\d,]+)(?:, or ([\d,]+) in lair)?;")


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def pdf_text(pdf, *options):
    return subprocess.run(
        ["pdftotext", *options, str(pdf), "-"],
        check=True, text=True, capture_output=True,
    ).stdout


def extract(pdf):
    digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
    if digest != SOURCE_SHA256:
        raise ValueError("Unexpected PDF checksum; review a source update before changing the pinned checksum")
    # Page dimensions are 594 x 783 points; split at the central gutter.
    columns = [
        pdf_text(pdf, "-layout", "-x", str(x), "-y", "0",
                 "-W", "297", "-H", "770").split("\f")
        for x in (0, 297)
    ]
    records = []
    pending = None
    for page in range(258, 365):
        for column in columns:
            lines = [line.strip() for line in column[page - 1].splitlines()]
            for index, line in enumerate(lines):
                descriptor = DESCRIPTOR.match(line)
                if descriptor:
                    if pending is not None:
                        raise ValueError(f"Missing challenge metadata for {pending}")
                    name = next(value for value in reversed(lines[:index]) if value)
                    pending = {
                        "id": "srd-5.2.1:" + slug(name),
                        "name": name,
                        "size": descriptor[1].lower(),
                        "monster_type": descriptor[2].lower(),
                        "rules_revision": "2024",
                        "references": [{
                            "publication": "SRD 5.2.1",
                            "page": str(page),
                            "url": SOURCE_URL,
                        }],
                    }
                normalized = re.sub(r"\(([\d,]+) XP;", r"(XP \1;", line)
                challenge = CR.match(normalized)
                if challenge and pending is not None:
                    pending["challenge_rating"] = challenge[1]
                    pending["xp"] = int(challenge[2].replace(",", ""))
                    if pending["name"] == "Archmage":
                        pending["extensions"] = {
                            "source_note": "Page 305 explicitly gives 8,000 XP; page 256's general CR 12 table gives 8,400. The stat block is preserved."
                        }
                    records.append(pending)
                    if challenge[3]:
                        variant = dict(pending)
                        variant.update(
                            id=pending["id"] + "-in-lair",
                            name=pending["name"] + " (in lair)",
                            xp=int(challenge[3].replace(",", "")),
                            tags=["in-lair"],
                        )
                        records.append(variant)
                    pending = None
    if pending is not None:
        raise ValueError(f"Missing challenge metadata for {pending}")
    # Separate extraction of the book's index, not a snapshot of parsed monsters.
    layout = pdf_text(pdf, "-layout").split("\f")
    index_entries = {}
    for page in layout[1:4]:
        for match in re.finditer(r"([A-Za-z][A-Za-z ’'–—-]+)\.[. ]*(\d{3})", page):
            name, reference = match[1].strip(), int(match[2])
            if 258 <= reference <= 364 and name not in ("Monsters A–Z", "Animals"):
                index_entries[name] = reference
    base_records = [record for record in records if not record.get("tags")]
    parsed_names = {record["name"] for record in base_records}
    if parsed_names != index_entries.keys():
        raise ValueError(
            f"Index mismatch: missing={index_entries.keys() - parsed_names}, "
            f"unexpected={parsed_names - index_entries.keys()}"
        )
    for record in base_records:
        if int(record["references"][0]["page"]) != index_entries[record["name"]]:
            raise ValueError(f"Index page mismatch for {record['name']}")
    pack = {
        "schema_version": 1,
        "pack_id": "srd-5.2.1",
        "pack_version": "1",
        "source": {
            "title": "System Reference Document 5.2.1",
            "url": SOURCE_URL,
            "sha256": digest,
            "extractor_version": "1",
            "verification_date": "2026-11-09",
            "verification": "Stat-block identities and pages checked against the independent PDF index.",
        },
        "license": "CC-BY-4.0",
        "monsters": sorted(records, key=lambda record: record["id"]),
    }
    manifest = {
        "source_sha256": digest,
        "origin": "SRD 5.2.1 index of stat blocks, pages 2–4; independently extracted from stat blocks.",
        "entries": dict(sorted(index_entries.items())),
    }
    return pack, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--index-manifest", type=Path, required=True)
    args = parser.parse_args()
    pack, manifest = extract(args.pdf)
    for path, document in ((args.catalog, pack), (args.index_manifest, manifest)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n")
    print(f"Extracted {len(manifest['entries'])} stat blocks; {len(pack['monsters'])} including lair variants.")


if __name__ == "__main__":
    main()
