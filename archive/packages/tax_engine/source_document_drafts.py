import json
from pathlib import Path
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DOCUMENT_DRAFT_SCHEMA_PATH = ROOT / "packages" / "schemas" / "source-document-draft.schema.json"

SOURCE_FIELD_DEFINITIONS = {
    "w2": [
        {
            "source_field_id": "w2.box1.wages",
            "field_number": "1",
            "label": "Wages, tips, other compensation",
            "required": True,
        },
        {
            "source_field_id": "w2.box2.federal_income_tax_withheld",
            "field_number": "2",
            "label": "Federal income tax withheld",
            "required": False,
        },
    ],
    "1099-int": [
        {
            "source_field_id": "1099_int.payer.name",
            "field_number": "payer",
            "label": "Payer name",
            "required": True,
        },
        {
            "source_field_id": "1099_int.box1.interest_income",
            "field_number": "1",
            "label": "Interest income",
            "required": True,
        },
        {
            "source_field_id": "1099_int.box4.federal_income_tax_withheld",
            "field_number": "4",
            "label": "Federal income tax withheld",
            "required": False,
        },
    ],
}


def load_source_document_draft_payload(path: Path) -> dict:
    payload = json.loads(path.read_text())
    schema = json.loads(SOURCE_DOCUMENT_DRAFT_SCHEMA_PATH.read_text())
    jsonschema.validate(payload, schema)
    return payload


def field_values_by_id(draft_payload: dict) -> dict[str, Any]:
    return {
        field_value["source_field_id"]: field_value["value"]
        for field_value in draft_payload["field_values"]
    }


def normalize_source_document_draft(draft_payload: dict) -> dict:
    definitions = SOURCE_FIELD_DEFINITIONS[draft_payload["document_type"]]
    values = field_values_by_id(draft_payload)
    return {
        "schema_version": "1.0.0",
        "source_document_id": draft_payload["source_document_id"],
        "source_revision_id": draft_payload["source_revision_id"],
        "document_type": draft_payload["document_type"],
        "tax_year": draft_payload["tax_year"],
        "entered_at": draft_payload["entered_at"],
        "label": draft_payload["label"],
        "fields": [
            {
                "source_field_id": definition["source_field_id"],
                "field_number": definition["field_number"],
                "label": definition["label"],
                "required": definition["required"],
                "value": values.get(definition["source_field_id"]),
            }
            for definition in definitions
        ],
    }
