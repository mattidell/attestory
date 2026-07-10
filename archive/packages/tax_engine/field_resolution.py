import json
from pathlib import Path
from typing import Any

import jsonschema

from packages.tax_engine.computed_fields import ComputedField, computed_fields_by_destination, load_computed_field_definitions


ROOT = Path(__file__).resolve().parents[2]
FIELD_RESOLUTION_SCHEMA_PATH = ROOT / "packages" / "schemas" / "field-resolution.schema.json"

STATUS_RESOLVED_DIRECT = "resolved_direct"
STATUS_RESOLVED_COMPUTED = "resolved_computed"
STATUS_BLOCKED_MISSING_SOURCE = "blocked_missing_source"
STATUS_BLOCKED_MISSING_COMPUTATION = "blocked_missing_computation"
STATUS_OPTIONAL_NOT_POPULATED = "optional_not_populated"


def build_field_resolution(
    coverage: dict,
    computations: list[ComputedField] | None = None,
) -> dict:
    computation_by_destination = computed_fields_by_destination(computations or load_computed_field_definitions())
    resolved_by_id: dict[str, dict] = {}
    resolved_fields = []

    for coverage_field in coverage["fields"]:
        if coverage_field["population_mode"] == "computed":
            resolved_field = resolve_computed_field(
                coverage_field,
                computation_by_destination.get(coverage_field["field_id"]),
                resolved_by_id,
            )
        else:
            resolved_field = resolve_direct_field(coverage_field)
        resolved_fields.append(resolved_field)
        resolved_by_id[resolved_field["field_id"]] = resolved_field

    resolution = {
        "schema_version": "1.0.0",
        "tax_year": coverage["tax_year"],
        "jurisdiction": coverage["jurisdiction"],
        "fields": resolved_fields,
    }
    validate_field_resolution(resolution)
    return resolution


def resolve_direct_field(coverage_field: dict) -> dict:
    values = coverage_field["values"]
    if coverage_field["status"] == "directly_populated":
        status = STATUS_RESOLVED_DIRECT
        blocking_field_ids = []
    elif coverage_field["status"] == "missing_required_source_data":
        status = STATUS_BLOCKED_MISSING_SOURCE
        blocking_field_ids = coverage_field["needed_source_field_ids"]
    else:
        status = STATUS_OPTIONAL_NOT_POPULATED
        blocking_field_ids = []

    return {
        "field_id": coverage_field["field_id"],
        "form_id": coverage_field["form_id"],
        "label": coverage_field["label"],
        "required": coverage_field["required"],
        "population_mode": coverage_field["population_mode"],
        "status": status,
        "value": single_value_or_null(values),
        "values": values,
        "dependency_field_ids": [],
        "blocking_field_ids": blocking_field_ids,
        "source_attributions": coverage_field["source_attributions"],
    }


def resolve_computed_field(
    coverage_field: dict,
    computation: ComputedField | None,
    resolved_by_id: dict[str, dict],
) -> dict:
    if computation is None:
        return blocked_computed_field(coverage_field, [], [coverage_field["field_id"]])

    dependencies = [
        resolved_by_id.get(field_id)
        for field_id in computation.input_field_ids
    ]
    missing_dependency_ids = [
        field_id
        for field_id, dependency in zip(computation.input_field_ids, dependencies)
        if dependency is None
    ]
    if missing_dependency_ids:
        return blocked_computed_field(coverage_field, list(computation.input_field_ids), missing_dependency_ids)

    blocking_source_ids = [
        blocking_field_id
        for dependency in dependencies
        if dependency["status"] == STATUS_BLOCKED_MISSING_SOURCE
        for blocking_field_id in dependency["blocking_field_ids"]
    ]
    if blocking_source_ids:
        return blocked_computed_field(coverage_field, list(computation.input_field_ids), blocking_source_ids, STATUS_BLOCKED_MISSING_SOURCE)

    blocking_computation_ids = [
        dependency["field_id"]
        for dependency in dependencies
        if dependency["status"] == STATUS_BLOCKED_MISSING_COMPUTATION
    ]
    if blocking_computation_ids:
        return blocked_computed_field(coverage_field, list(computation.input_field_ids), blocking_computation_ids)

    input_values = [
        value
        for dependency in dependencies
        for value in dependency["values"]
    ]
    computed_value = compute_value(computation.operation, input_values)
    values = [] if computed_value is None else [computed_value]

    return {
        "field_id": coverage_field["field_id"],
        "form_id": coverage_field["form_id"],
        "label": coverage_field["label"],
        "required": coverage_field["required"],
        "population_mode": coverage_field["population_mode"],
        "status": STATUS_RESOLVED_COMPUTED,
        "value": computed_value,
        "values": values,
        "dependency_field_ids": list(computation.input_field_ids),
        "blocking_field_ids": [],
        "source_attributions": [],
    }


def blocked_computed_field(
    coverage_field: dict,
    dependency_field_ids: list[str],
    blocking_field_ids: list[str],
    status: str = STATUS_BLOCKED_MISSING_COMPUTATION,
) -> dict:
    return {
        "field_id": coverage_field["field_id"],
        "form_id": coverage_field["form_id"],
        "label": coverage_field["label"],
        "required": coverage_field["required"],
        "population_mode": coverage_field["population_mode"],
        "status": status,
        "value": None,
        "values": [],
        "dependency_field_ids": dependency_field_ids,
        "blocking_field_ids": blocking_field_ids,
        "source_attributions": [],
    }


def compute_value(operation: str, input_values: list[Any]) -> Any:
    if operation == "copy":
        return single_value_or_null(input_values)
    if operation == "sum":
        return sum_money_values(input_values)
    raise ValueError(f"Unsupported computed field operation: {operation}")


def single_value_or_null(values: list[Any]) -> Any:
    if len(values) == 1:
        return values[0]
    return None


def sum_money_values(values: list[Any]) -> dict | None:
    if not values:
        return None
    currency = values[0]["currency"]
    scale = values[0]["scale"]
    return {
        "amount": sum(value["amount"] for value in values),
        "currency": currency,
        "scale": scale,
    }


def validate_field_resolution(payload: dict) -> None:
    schema = json.loads(FIELD_RESOLUTION_SCHEMA_PATH.read_text())
    jsonschema.validate(payload, schema)
