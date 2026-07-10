from packages.tax_engine.source_documents import SourceDocument


def build_source_validation_report(documents: list[SourceDocument]) -> dict:
    document_reports = []
    for document in documents:
        missing_required_fields = [
            {
                "source_field_id": field.source_field_id,
                "field_number": field.field_number,
                "label": field.label,
            }
            for field in document.fields
            if field.required and not field.has_value
        ]
        document_reports.append(
            {
                "source_document_id": document.source_document_id,
                "source_revision_id": document.source_revision_id,
                "document_type": document.document_type,
                "label": document.label,
                "missing_required_fields": missing_required_fields,
                "valid": not missing_required_fields,
            }
        )

    return {
        "schema_version": "1.0.0",
        "documents": document_reports,
        "valid": all(report["valid"] for report in document_reports),
    }


def render_source_validation_report_markdown(report: dict) -> str:
    lines = [
        "# Source Document Validation",
        "",
        f"- Documents: {len(report['documents'])}",
        f"- Valid: {'yes' if report['valid'] else 'no'}",
        "",
    ]

    for document in report["documents"]:
        lines.extend(
            [
                f"## {document['label']}",
                "",
                f"- Document type: {document['document_type']}",
                f"- Source document ID: `{document['source_document_id']}`",
                f"- Revision: `{document['source_revision_id']}`",
                f"- Valid: {'yes' if document['valid'] else 'no'}",
            ]
        )
        if document["missing_required_fields"]:
            lines.extend(["", "| Missing Field | Field Number |", "| --- | --- |"])
            for field in document["missing_required_fields"]:
                lines.append(f"| `{field['source_field_id']}`<br>{field['label']} | {field['field_number']} |")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
