import json
from dataclasses import dataclass
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[2]
COMPUTED_FIELD_DEFINITIONS_SCHEMA_PATH = ROOT / "packages" / "schemas" / "computed-field-definitions.schema.json"
COMPUTED_FIELD_DEFINITIONS_PATH = ROOT / "packages" / "tax_engine" / "definitions" / "computed_fields.federal.2025.json"


@dataclass(frozen=True)
class ComputedField:
    computation_id: str
    destination_field_id: str
    operation: str
    input_field_ids: tuple[str, ...]


def load_computed_field_definitions_payload(path: Path = COMPUTED_FIELD_DEFINITIONS_PATH) -> dict:
    payload = json.loads(path.read_text())
    schema = json.loads(COMPUTED_FIELD_DEFINITIONS_SCHEMA_PATH.read_text())
    jsonschema.validate(payload, schema)
    return payload


def load_computed_field_definitions(path: Path = COMPUTED_FIELD_DEFINITIONS_PATH) -> list[ComputedField]:
    payload = load_computed_field_definitions_payload(path)
    return [
        ComputedField(
            computation_id=computation["computation_id"],
            destination_field_id=computation["destination_field_id"],
            operation=computation["operation"],
            input_field_ids=tuple(computation["input_field_ids"]),
        )
        for computation in payload["computations"]
    ]


def computed_fields_by_destination(computations: list[ComputedField]) -> dict[str, ComputedField]:
    return {
        computation.destination_field_id: computation
        for computation in computations
    }
