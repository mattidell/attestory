import json
from dataclasses import dataclass
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[2]
FIELD_CATALOG_SCHEMA_PATH = ROOT / "packages" / "schemas" / "federal-field-catalog.schema.json"
FIELD_CATALOG_PATH = ROOT / "packages" / "tax_engine" / "definitions" / "federal_field_catalog.2025.json"


@dataclass(frozen=True)
class FederalField:
    field_id: str
    form_id: str
    label: str
    required: bool
    population_mode: str


def load_field_catalog_payload(path: Path = FIELD_CATALOG_PATH) -> dict:
    payload = json.loads(path.read_text())
    schema = json.loads(FIELD_CATALOG_SCHEMA_PATH.read_text())
    jsonschema.validate(payload, schema)
    return payload


def load_field_catalog(path: Path = FIELD_CATALOG_PATH) -> list[FederalField]:
    payload = load_field_catalog_payload(path)
    return [
        FederalField(
            field_id=field["field_id"],
            form_id=field["form_id"],
            label=field["label"],
            required=field["required"],
            population_mode=field["population_mode"],
        )
        for field in payload["fields"]
    ]
