from packages.tax_engine.coverage_read_model import build_field_detail_read_model, build_grouped_coverage_read_model
from packages.tax_engine.coverage_summary import build_coverage_summary


STATUS_LABELS = {
    "directly_populated": "Direct",
    "requires_computation": "Computed",
    "missing_required_source_data": "Missing Source",
    "optional_not_populated": "Optional",
}


def format_value(value) -> str:
    if isinstance(value, dict) and {"amount", "currency", "scale"} <= value.keys():
        amount = value["amount"] / (10 ** value["scale"])
        return f"${amount:,.2f}"
    if value is None:
        return ""
    return str(value)


def format_values(values: list) -> str:
    if not values:
        return ""
    return ", ".join(format_value(value) for value in values)


def format_sources(source_attributions: list[dict]) -> str:
    if not source_attributions:
        return ""
    return ", ".join(
        f"{source.get('source_document_label', source['source_document_type'])}, field {source['source_field_number']}: {source.get('source_field_label', source['source_field_id'])} (`{source['source_field_id']}`)"
        for source in source_attributions
    )


def render_grouped_coverage_markdown(coverage: dict) -> str:
    read_model = build_grouped_coverage_read_model(coverage)
    summary = build_coverage_summary(coverage)
    lines = [
        f"# Federal Field Coverage ({read_model['tax_year']})",
        "",
        "## Summary",
        "",
        f"- Fields in scope: {summary['field_count']}",
        f"- Directly populated: {summary['status_counts'].get('directly_populated', 0)}",
        f"- Requires computation: {summary['status_counts'].get('requires_computation', 0)}",
        f"- Missing required source data: {summary['status_counts'].get('missing_required_source_data', 0)}",
        f"- Optional not populated: {summary['status_counts'].get('optional_not_populated', 0)}",
        "",
    ]

    for form in read_model["forms"]:
        lines.extend([
            f"## {form['form_id']}",
            "",
            "| Field | Status | Value | Source |",
            "| --- | --- | --- | --- |",
        ])
        for field in form["fields"]:
            status = STATUS_LABELS.get(field["status"], field["status"])
            lines.append(
                f"| `{field['field_id']}`<br>{field['label']} | {status} | {format_values(field['values'])} | {format_sources(field['source_attributions'])} |"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_field_detail_markdown(coverage: dict, field_id: str) -> str:
    detail = build_field_detail_read_model(coverage, field_id)
    status = STATUS_LABELS.get(detail["status"], detail["status"])
    lines = [
        f"# {detail['label']}",
        "",
        f"- Field: `{detail['field_id']}`",
        f"- Form: `{detail['form_id']}`",
        f"- Status: {status}",
        f"- Population mode: {detail['population_mode']}",
        f"- Required: {'yes' if detail['required'] else 'no'}",
    ]
    if detail["values"]:
        lines.append(f"- Value: {format_values(detail['values'])}")
    if detail["source_attributions"]:
        lines.append(f"- Source: {format_sources(detail['source_attributions'])}")
    if detail["needed_source_field_ids"] and not detail["values"]:
        lines.append(f"- Needed source field: {', '.join(detail['needed_source_field_ids'])}")
    return "\n".join(lines) + "\n"
