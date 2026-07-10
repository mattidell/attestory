import json
from pathlib import Path

import jsonschema

from packages.tax_engine.source_documents import SourceDocument


ROOT = Path(__file__).resolve().parents[2]
DIRECT_MAPPING_SCHEMA_PATH = ROOT / "packages" / "schemas" / "direct-source-mapping.schema.json"
DIRECT_MAPPING_PATH = ROOT / "packages" / "tax_engine" / "definitions" / "direct_source_to_form.federal.2025.json"

STATUS_DIRECTLY_POPULATED = "directly_populated"
STATUS_MISSING_REQUIRED_SOURCE_DATA = "missing_required_source_data"
STATUS_OPTIONAL_NOT_POPULATED = "optional_not_populated"


def load_direct_mapping_payload(path: Path = DIRECT_MAPPING_PATH) -> dict:
    payload = json.loads(path.read_text())
    schema = json.loads(DIRECT_MAPPING_SCHEMA_PATH.read_text())
    jsonschema.validate(payload, schema)
    return payload


def source_status_for_field(source_field) -> str:
    if source_field is None:
        return STATUS_MISSING_REQUIRED_SOURCE_DATA
    if source_field.has_value:
        return STATUS_DIRECTLY_POPULATED
    if source_field.required:
        return STATUS_MISSING_REQUIRED_SOURCE_DATA
    return STATUS_OPTIONAL_NOT_POPULATED


def build_source_attribution(document: SourceDocument, source_field) -> dict | None:
    if source_field is None or not source_field.has_value:
        return None
    return {
        "source_document_id": document.source_document_id,
        "source_revision_id": document.source_revision_id,
        "source_document_label": document.label,
        "source_document_type": document.document_type,
        "entered_at": document.entered_at,
        "source_field_number": source_field.field_number,
        "source_field_id": source_field.source_field_id,
        "source_field_label": source_field.label,
    }


def run_direct_source_mapping(
    source_documents: list[SourceDocument],
    mapping_payload: dict | None = None,
) -> dict:
    payload = mapping_payload or load_direct_mapping_payload()
    results = []

    for mapping in payload["mappings"]:
        matching_documents = [
            document
            for document in source_documents
            if document.document_type == mapping["source_document_type"]
        ]
        for document in matching_documents:
            source_field = document.field(mapping["source_field_id"])
            status = source_status_for_field(source_field)
            results.append(
                {
                    "mapping_id": mapping["mapping_id"],
                    "destination_field_id": mapping["destination_field_id"],
                    "destination_form_id": mapping["destination_form_id"],
                    "destination_label": mapping["destination_label"],
                    "source_document_id": document.source_document_id,
                    "status": status,
                    "value": source_field.value if source_field and source_field.has_value else None,
                    "source_attribution": build_source_attribution(document, source_field),
                }
            )

    return {
        "schema_version": "1.0.0",
        "tax_year": payload["tax_year"],
        "jurisdiction": payload["jurisdiction"],
        "direct_mappings": results,
    }
