import json
from pathlib import Path

import jsonschema

from packages.tax_engine.direct_mapping import (
    STATUS_DIRECTLY_POPULATED,
    STATUS_MISSING_REQUIRED_SOURCE_DATA,
    STATUS_OPTIONAL_NOT_POPULATED,
)
from packages.tax_engine.field_catalog import FederalField, load_field_catalog


ROOT = Path(__file__).resolve().parents[2]
FIELD_COVERAGE_SCHEMA_PATH = ROOT / "packages" / "schemas" / "field-coverage.schema.json"

STATUS_REQUIRES_COMPUTATION = "requires_computation"


def mapping_source_fields_by_destination(mapping_payload: dict) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for mapping in mapping_payload["mappings"]:
        out.setdefault(mapping["destination_field_id"], []).append(mapping["source_field_id"])
    return out


def direct_results_by_destination(direct_mapping_result: dict) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for item in direct_mapping_result["direct_mappings"]:
        out.setdefault(item["destination_field_id"], []).append(item)
    return out


def status_for_direct_field(field: FederalField, direct_results: list[dict]) -> str:
    if any(item["status"] == STATUS_DIRECTLY_POPULATED for item in direct_results):
        return STATUS_DIRECTLY_POPULATED
    if any(item["status"] == STATUS_MISSING_REQUIRED_SOURCE_DATA for item in direct_results):
        return STATUS_MISSING_REQUIRED_SOURCE_DATA
    if direct_results and all(item["status"] == STATUS_OPTIONAL_NOT_POPULATED for item in direct_results):
        return STATUS_OPTIONAL_NOT_POPULATED
    return STATUS_MISSING_REQUIRED_SOURCE_DATA if field.required else STATUS_OPTIONAL_NOT_POPULATED


def build_field_coverage(
    *,
    direct_mapping_result: dict,
    mapping_payload: dict,
    field_catalog: list[FederalField] | None = None,
) -> dict:
    fields = field_catalog or load_field_catalog()
    results_by_destination = direct_results_by_destination(direct_mapping_result)
    source_fields_by_destination = mapping_source_fields_by_destination(mapping_payload)
    coverage_fields = []

    for field in fields:
        direct_results = results_by_destination.get(field.field_id, [])
        if field.population_mode == "computed":
            status = STATUS_REQUIRES_COMPUTATION
        else:
            status = status_for_direct_field(field, direct_results)

        coverage_fields.append(
            {
                "field_id": field.field_id,
                "form_id": field.form_id,
                "label": field.label,
                "required": field.required,
                "population_mode": field.population_mode,
                "status": status,
                "values": [
                    item["value"]
                    for item in direct_results
                    if item["status"] == STATUS_DIRECTLY_POPULATED
                ],
                "source_attributions": [
                    item["source_attribution"]
                    for item in direct_results
                    if item["source_attribution"] is not None
                ],
                "needed_source_field_ids": source_fields_by_destination.get(field.field_id, []),
            }
        )

    return {
        "schema_version": "1.0.0",
        "tax_year": direct_mapping_result["tax_year"],
        "jurisdiction": direct_mapping_result["jurisdiction"],
        "fields": coverage_fields,
    }


def validate_field_coverage(payload: dict) -> None:
    schema = json.loads(FIELD_COVERAGE_SCHEMA_PATH.read_text())
    jsonschema.validate(payload, schema)
