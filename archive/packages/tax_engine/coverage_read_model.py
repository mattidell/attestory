STATUS_REQUIRES_COMPUTATION = "requires_computation"


def build_grouped_coverage_read_model(coverage: dict) -> dict:
    forms: dict[str, dict] = {}
    for field in coverage["fields"]:
        form = forms.setdefault(
            field["form_id"],
            {
                "form_id": field["form_id"],
                "fields": [],
                "status_counts": {},
            },
        )
        form["fields"].append(field)
        form["status_counts"][field["status"]] = form["status_counts"].get(field["status"], 0) + 1

    return {
        "schema_version": "1.0.0",
        "tax_year": coverage["tax_year"],
        "jurisdiction": coverage["jurisdiction"],
        "forms": list(forms.values()),
    }


def build_field_detail_read_model(coverage: dict, field_id: str) -> dict:
    field = next((item for item in coverage["fields"] if item["field_id"] == field_id), None)
    if field is None:
        raise KeyError(f"Unknown field_id: {field_id}")

    return {
        "schema_version": "1.0.0",
        "tax_year": coverage["tax_year"],
        "jurisdiction": coverage["jurisdiction"],
        "field_id": field["field_id"],
        "form_id": field["form_id"],
        "label": field["label"],
        "required": field["required"],
        "population_mode": field["population_mode"],
        "status": field["status"],
        "values": field["values"],
        "source_attributions": [] if field["status"] == STATUS_REQUIRES_COMPUTATION else field["source_attributions"],
        "needed_source_field_ids": field["needed_source_field_ids"],
    }
