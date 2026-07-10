def build_coverage_summary(coverage: dict) -> dict:
    status_counts: dict[str, int] = {}
    form_counts: dict[str, dict[str, int]] = {}
    missing_required_fields = []
    computed_fields = []

    for field in coverage["fields"]:
        status_counts[field["status"]] = status_counts.get(field["status"], 0) + 1
        form_status_counts = form_counts.setdefault(field["form_id"], {})
        form_status_counts[field["status"]] = form_status_counts.get(field["status"], 0) + 1

        if field["status"] == "missing_required_source_data":
            missing_required_fields.append(
                {
                    "field_id": field["field_id"],
                    "label": field["label"],
                    "needed_source_field_ids": field["needed_source_field_ids"],
                }
            )
        if field["status"] == "requires_computation":
            computed_fields.append(
                {
                    "field_id": field["field_id"],
                    "label": field["label"],
                }
            )

    return {
        "schema_version": "1.0.0",
        "tax_year": coverage["tax_year"],
        "jurisdiction": coverage["jurisdiction"],
        "field_count": len(coverage["fields"]),
        "status_counts": status_counts,
        "form_counts": form_counts,
        "missing_required_fields": missing_required_fields,
        "computed_fields": computed_fields,
    }
