from pathlib import Path

from packages.tax_engine.coverage_markdown import render_grouped_coverage_markdown
from packages.tax_engine.direct_mapping import load_direct_mapping_payload, run_direct_source_mapping
from packages.tax_engine.field_coverage import build_field_coverage, validate_field_coverage
from packages.tax_engine.source_document_drafts import load_source_document_draft_payload, normalize_source_document_draft
from packages.tax_engine.source_documents import source_document_from_payload, validate_source_document_payload


def build_field_coverage_from_drafts(draft_paths: list[Path]) -> dict:
    documents = []
    for draft_path in draft_paths:
        draft_payload = load_source_document_draft_payload(draft_path)
        source_document_payload = normalize_source_document_draft(draft_payload)
        validate_source_document_payload(source_document_payload)
        documents.append(source_document_from_payload(source_document_payload))

    mapping_payload = load_direct_mapping_payload()
    direct_mapping_result = run_direct_source_mapping(documents, mapping_payload)
    coverage = build_field_coverage(direct_mapping_result=direct_mapping_result, mapping_payload=mapping_payload)
    validate_field_coverage(coverage)
    return coverage


def build_markdown_coverage_from_drafts(draft_paths: list[Path]) -> str:
    return render_grouped_coverage_markdown(build_field_coverage_from_drafts(draft_paths))
