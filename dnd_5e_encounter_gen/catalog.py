"""Versioned monster catalogs. Local data only; no executable imports or fetching."""

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from importlib.resources import files
from pathlib import Path
from types import MappingProxyType

MAX_CATALOG_CHARACTERS = 10_000_000


class CatalogError(ValueError):
    """An unreadable, invalid, or conflicting catalog."""


def _freeze(value):
    """Copy JSON containers into recursively immutable, detached containers."""
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


@dataclass(frozen=True)
class Monster:
    id: str
    name: str
    challenge_rating: str
    xp: int
    size: str
    monster_type: str
    rules_revision: str
    references: tuple = ()
    tags: tuple = ()
    aliases: tuple = ()
    extensions: Mapping[str, object] = field(default_factory=dict, compare=False, hash=False)

    def __post_init__(self):
        try:
            for name in ("references", "tags", "aliases", "extensions"):
                object.__setattr__(self, name, _freeze(getattr(self, name)))
        except RecursionError as error:
            raise CatalogError(f"{self.id}: metadata is nested too deeply") from error


def catalog_schema():
    resource = files("dnd_5e_encounter_gen").joinpath("data/catalog.schema.json")
    return json.loads(resource.read_text(encoding="utf-8"))


def monster_types():
    return tuple(catalog_schema()["$defs"]["monster"]["properties"]["monster_type"]["enum"])


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CatalogError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise CatalogError(f"non-JSON numeric constant: {value}")


def _validate(value, rule, root, location):
    """Interpret the deliberately small JSON Schema subset used by our schema.

    This keeps runtime validation and the published schema in one source of truth.
    Tests also compare acceptance with a full Draft 2020-12 validator.
    """
    if "$ref" in rule:
        rule = root["$defs"][rule["$ref"].removeprefix("#/$defs/")]
    types = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
    }

    def fail(message):
        raise CatalogError(f"{location}: {message}")

    expected = rule["type"]
    if not types[expected](value):
        fail(f"expected {expected}")
    if "const" in rule and value != rule["const"]:
        fail(f"must equal {rule['const']!r}; unsupported schema version")
    if "enum" in rule and value not in rule["enum"]:
        fail(f"must be one of {rule['enum']}")
    if "minimum" in rule and value < rule["minimum"]:
        fail(f"must be at least {rule['minimum']}")
    if expected == "string":
        if len(value) < rule.get("minLength", 0):
            fail("must not be empty")
        if "pattern" in rule and re.search(rule["pattern"], value) is None:
            fail("invalid value or format")
    if expected == "object":
        properties = rule.get("properties", {})
        for key in rule.get("required", []):
            if key not in value:
                fail(f"missing field {key}")
        for key, item in value.items():
            if key in properties:
                _validate(item, properties[key], root, f"{location}.{key}")
            elif rule.get("additionalProperties") is False:
                fail(f"unknown field {key}; use extensions for custom metadata")
    if expected == "array":
        seen = set()
        for index, item in enumerate(value):
            _validate(item, rule["items"], root, f"{location}[{index}]")
            # The published schema uses uniqueItems only for string arrays.
            # Validate first so malformed/unhashable items remain CatalogErrors.
            if rule.get("uniqueItems"):
                if item in seen:
                    fail("duplicate array item")
                seen.add(item)


def parse_catalog(text, origin="<catalog>"):
    try:
        if len(text) > MAX_CATALOG_CHARACTERS:
            raise CatalogError("catalog exceeds the 10,000,000-character limit")
        document = json.loads(
            text, object_pairs_hook=_unique_object, parse_constant=_reject_constant,
        )
        schema = catalog_schema()
        _validate(document, schema, schema, origin)
        identities = set()
        for index, record in enumerate(document["monsters"]):
            if record["id"] in identities:
                raise CatalogError(f"{origin}.monsters[{index}].id: duplicate identity {record['id']}")
            identities.add(record["id"])
        return document
    except (ValueError, RecursionError) as error:
        raise CatalogError(f"{origin}: {error}") from error


def load_catalog(path):
    try:
        with Path(path).open(encoding="utf-8") as source:
            return parse_catalog(source.read(MAX_CATALOG_CHARACTERS + 1), str(path))
    except (OSError, UnicodeError) as error:
        raise CatalogError(f"{path}: cannot read UTF-8 catalog ({error})") from error


def load_default():
    resource = files("dnd_5e_encounter_gen").joinpath("data/srd_5_2_1.json")
    return parse_catalog(resource.read_text(encoding="utf-8"), "bundled SRD 5.2.1")


def merge_catalogs(documents, allow_overrides=False):
    monsters = {}
    for document in documents:
        for record in document["monsters"]:
            identity = record["id"]
            if identity in monsters and not allow_overrides:
                raise CatalogError(
                    f"duplicate identity {identity}; use --allow-overrides for explicit last-pack-wins replacement"
                )
            values = dict(record)
            monsters[identity] = Monster(**values)
    return tuple(monsters[key] for key in sorted(monsters))


def load_monsters(paths=(), include_default=True, allow_overrides=False):
    documents = [load_default()] if include_default else []
    documents.extend(load_catalog(path) for path in paths)
    return merge_catalogs(documents, allow_overrides)
