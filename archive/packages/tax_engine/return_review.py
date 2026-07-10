STATUS_LABELS = {
    "resolved_direct": "Direct",
    "resolved_computed": "Computed",
    "blocked_missing_source": "Blocked: missing source",
    "blocked_missing_computation": "Blocked: missing computation",
    "optional_not_populated": "Optional not populated",
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


def render_return_review_markdown(return_artifact: dict) -> str:
    summary = return_artifact["resolution_summary"]
    lines = [
        f"# Federal Return Review ({return_artifact['tax_year']})",
        "",
        "## Resolution Summary",
        "",
        f"- Fields in scope: {summary['field_count']}",
        f"- Resolved direct: {summary['status_counts'].get('resolved_direct', 0)}",
        f"- Resolved computed: {summary['status_counts'].get('resolved_computed', 0)}",
        f"- Blocked missing source: {summary['status_counts'].get('blocked_missing_source', 0)}",
        f"- Blocked missing computation: {summary['status_counts'].get('blocked_missing_computation', 0)}",
        f"- Optional not populated: {summary['status_counts'].get('optional_not_populated', 0)}",
        "",
    ]

    for form in return_artifact["forms"]:
        lines.extend([
            f"## {form['form_id']}",
            "",
            "| Field | Status | Value |",
            "| --- | --- | --- |",
        ])
        for field in form["fields"]:
            lines.append(
                f"| `{field['field_id']}`<br>{field['label']} | {STATUS_LABELS[field['status']]} | {format_values(field['values'])} |"
            )
        lines.append("")

    if summary["blocked_fields"]:
        lines.extend([
            "## Blocked Fields",
            "",
            "| Field | Status | Blocking Fields |",
            "| --- | --- | --- |",
        ])
        for field in summary["blocked_fields"]:
            lines.append(
                f"| `{field['field_id']}`<br>{field['label']} | {STATUS_LABELS[field['status']]} | {', '.join(field['blocking_field_ids'])} |"
            )
        lines.append("")

    if summary["optional_unpopulated_fields"]:
        lines.extend([
            "## Optional Unpopulated Fields",
            "",
            "| Field | Status |",
            "| --- | --- |",
        ])
        for field in summary["optional_unpopulated_fields"]:
            lines.append(
                f"| `{field['field_id']}`<br>{field['label']} | {STATUS_LABELS[field['status']]} |"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
