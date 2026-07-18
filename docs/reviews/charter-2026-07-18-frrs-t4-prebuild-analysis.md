# Charter: Track 4 Prebuild Analysis — W-2 Closure and Live-Run Integration

Date: 2026-07-18. Owner-authorized planning analysis for the active First Real
Return Slice Track 4. This is read-only reconnaissance before the implementation
charter; it does not authorize code, fixture, schema, ADR, or Git changes.

## Shared constraints

- Build only on accepted ADRs: ADR-0014, ADR-0027/0028, ADR-0031/0032/0033.
  Surface a missing contract instead of inventing one.
- No personal data, live-workspace locator, real-run disposition, or absolute
  machine path may enter the repository or report.
- Track 3's F1 repair is merged (`8c7af6d`). Carry the remaining original review
  items accurately: F2/F4/F5/F6 are non-blocking; F3/F7 and the ADR-0033
  PC(T4) ledger are Track-4 conditions.
- Report exact paths, exact existing tests/fixtures, and a minimal ordered change
  list. Do not recommend broader tax coverage, UI, OCR, or a new ADR unless an
  accepted contract truly cannot express the required behavior.

## Seat A — W-2 closure content and publication-chain analyst

Measure the existing W-2 fact type, closure fact type, source-family/mapping,
bundle/package, registry, release, and adoption fixtures. Determine the minimal
synthetic content and pin regeneration needed to make the W-2 family close under
ADR-0014 and remain production-resolvable under ADR-0033. Identify exact tests
that prove a closure-backed zero, present W-2 aggregation, displaced/false/absent
closure refusal, and package/release byte integrity.

## Seat B — live pipeline and quarantine-attestation analyst

Measure the current contribution, workspace bootstrap, production resolver,
marshaller, executor, runner, and reporting surfaces. Determine the minimal
synthetic live-run harness that connects current adoption → verified graph →
record-state run inside a bootstrapped workspace without accepting caller-selected
authority. Specify how the owner later performs the real run in quarantine and
records only the allowed non-descriptive attestation. Identify the exact Track-4
ADR-0033 PC(T4), ADR-0031 F3, and review F2/F4/F5/F6 carry items that must be
discharged or explicitly deferred.

## Output

Each seat replies with a concise evidence-backed report. The foreman synthesizes
the reports into the implementation charter; neither seat writes a repository
artifact, reviews future implementation, or dispatches another agent.
