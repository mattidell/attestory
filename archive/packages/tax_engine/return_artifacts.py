import json
from pathlib import Path

import jsonschema

from packages.tax_engine.field_resolution import (
    STATUS_BLOCKED_MISSING_COMPUTATION,
    STATUS_BLOCKED_MISSING_SOURCE,
    STATUS_OPTIONAL_NOT_POPULATED,
    STATUS_RESOLVED_COMPUTED,
    STATUS_RESOLVED_DIRECT,
)


ROOT = Path(__file__).resolve().parents[2]
RETURN_ARTIFACT_SCHEMA_PATH = ROOT / "packages" / "schemas" / "return-artifact.schema.json"

RETURN_READY_STATUSES = {
    STATUS_RESOLVED_DIRECT,
    STATUS_RESOLVED_COMPUTED,
}
BLOCKED_STATUSES = {
    STATUS_BLOCKED_MISSING_SOURCE,
    STATUS_BLOCKED_MISSING_COMPUTATION,
}


def build_return_artifact(field_resolution: dict) -> dict:
    forms_by_id: dict[str, dict] = {}

    for field in field_resolution["fields"]:
        if field["status"] not in RETURN_READY_STATUSES:
            continue
        form = forms_by_id.setdefault(
            field["form_id"],
            {
                "form_id": field["form_id"],
                "fields": [],
            },
        )
        form["fields"].append(
            {
                "field_id": field["field_id"],
                "label": field["label"],
                "status": field["status"],
                "value": field["value"],
                "values": field["values"],
            }
        )

    artifact = {
        "schema_version": "1.0.0",
        "tax_year": field_resolution["tax_year"],
        "jurisdiction": field_resolution["jurisdiction"],
        "forms": list(forms_by_id.values()),
        "resolution_summary": build_resolution_summary(field_resolution),
    }
    validate_return_artifact(artifact)
    return artifact


def build_resolution_summary(field_resolution: dict) -> dict:
    status_counts: dict[str, int] = {}
    form_counts: dict[str, dict[str, int]] = {}
    blocked_fields = []
    optional_unpopulated_fields = []

    for field in field_resolution["fields"]:
        status = field["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

        form_status_counts = form_counts.setdefault(field["form_id"], {})
        form_status_counts[status] = form_status_counts.get(status, 0) + 1

        if status in BLOCKED_STATUSES:
            blocked_fields.append(summary_field(field))
        if status == STATUS_OPTIONAL_NOT_POPULATED:
            optional_unpopulated_fields.append(summary_field(field))

    return {
        "field_count": len(field_resolution["fields"]),
        "status_counts": status_counts,
        "form_counts": form_counts,
        "blocked_fields": blocked_fields,
        "optional_unpopulated_fields": optional_unpopulated_fields,
    }


def summary_field(field: dict) -> dict:
    return {
        "field_id": field["field_id"],
        "form_id": field["form_id"],
        "label": field["label"],
        "status": field["status"],
        "blocking_field_ids": field["blocking_field_ids"],
    }


def validate_return_artifact(payload: dict) -> None:
    schema = json.loads(RETURN_ARTIFACT_SCHEMA_PATH.read_text())
    jsonschema.validate(payload, schema)
