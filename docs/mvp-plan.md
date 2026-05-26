# MVP Plan: Federal Source-To-Form Mapping

## Purpose

The MVP proves the smallest useful tax workflow: an individual taxpayer can enter federal source-document data and see how that data directly maps onto in-scope federal tax form fields.

This is not a full return-preparation product. The MVP deliberately stops before full tax computation, PDF generation, state returns, e-file, document OCR, or tax advice.

## User And Scope

Primary user:
- An individual taxpayer preparing or reviewing their own federal return data.

In scope:
- Federal-only workflow.
- Manual entry for W-2 and 1099-INT.
- Saving, viewing, and editing entered source document data.
- A form-field coverage view for in-scope federal tax form fields.
- Direct source-to-form mappings where no computation is required.
- Field status labels that explain whether a field is populated, missing source data, optional, or requires computation.
- Source attribution for directly populated fields.

Out of scope:
- State returns.
- OCR or automatic document parsing.
- Official PDF generation.
- E-file or filing submission.
- Payment, refund, or account integrations.
- Full computation trace for computed fields.
- Tax advice or correctness guarantees.

## Functional Requirements

1. Users can manually enter, save, view, and edit data from federal income-related source documents, starting with W-2 and 1099-INT.
2. Users can view all in-scope federal tax form fields and see each field's status: directly populated from saved source document data, requires computation, missing required source data, or optional/not populated.
3. Users can select a directly populated tax form field and view its source attribution, including source document type, entry date, source field number, and source field identifier.
4. The destination tax form field identifier is visible in the form-field view.
5. When users update saved source document data, the tax form field statuses and direct-source attribution refresh after the source document is saved.

## Personal Data Guardrails

The MVP refactor must not rely on personal tax documents or personal current-year fact instances remaining in the shareable project.

Personal source documents, personal current fact instances, personal manual entries, prior returns, state outputs, and generated personal artifacts must live outside this branch. Demo files must be synthetic and clearly labeled as demo or synthetic data.
