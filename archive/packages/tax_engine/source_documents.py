import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DOCUMENT_SCHEMA_PATH = ROOT / "packages" / "schemas" / "source-document.schema.json"


@dataclass(frozen=True)
class SourceField:
    source_field_id: str
    field_number: str
    label: str
    required: bool
    value: Any

    @property
    def has_value(self) -> bool:
        return self.value is not None


@dataclass(frozen=True)
class SourceDocument:
    source_document_id: str
    source_revision_id: str
    document_type: str
    tax_year: int
    entered_at: str
    label: str
    fields: tuple[SourceField, ...]

    def field(self, source_field_id: str) -> SourceField | None:
        return next((field for field in self.fields if field.source_field_id == source_field_id), None)


def load_source_document_payload(path: Path) -> dict:
    payload = json.loads(path.read_text())
    validate_source_document_payload(payload)
    return payload


def validate_source_document_payload(payload: dict) -> None:
    schema = json.loads(SOURCE_DOCUMENT_SCHEMA_PATH.read_text())
    jsonschema.validate(payload, schema)


def source_document_from_payload(payload: dict) -> SourceDocument:
    return SourceDocument(
        source_document_id=payload["source_document_id"],
        source_revision_id=payload["source_revision_id"],
        document_type=payload["document_type"],
        tax_year=payload["tax_year"],
        entered_at=payload["entered_at"],
        label=payload["label"],
        fields=tuple(
            SourceField(
                source_field_id=field["source_field_id"],
                field_number=field["field_number"],
                label=field["label"],
                required=field["required"],
                value=field["value"],
            )
            for field in payload["fields"]
        ),
    )


def load_source_document(path: Path) -> SourceDocument:
    return source_document_from_payload(load_source_document_payload(path))
