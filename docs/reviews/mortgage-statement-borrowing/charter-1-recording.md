# Track 1 — Record one borrowing without merging its reports

Role: Builder. Action: implementation. Milestone: mortgage-statement-borrowing.
Branch: milestone/mortgage-statement-borrowing-same-loan.
Base: the committed charter on top of core v53 / registry v51 / release v51.

## Purpose and actions

Let a person identify one continuing mortgage borrowing, connect exact Forms
1098 to it, and give clearly scoped answers. Keep their documents and answers
separate so later calculation can distinguish support from uncertainty.
First inspect the existing SLI recorder and mortgage answer recorder, turn
the cases below into focused tests, then build and commit this recording
unit. Do not build the calculation or reader in this assignment.

## Context and readiness

Run `python3 tools/build_orientation_block.py --ref HEAD`; verify its SHA,
read the Builder seat, OWNER_MODEL, concurrent-work protocol and ADR index.
The active plan's **Track 0 adversarial closure** selects the connected
contract after independent Sol READY. Read that declaration, **Production
sequence**, and the contract sections **Recorded claims and scope**,
**Restored design: explicit exit and suitable shared answers**, and
**Lifecycle and correction consequences**. Read exact accepted ADR-0073
when implementing retractions; use existing schema contracts, not new ones.

Existing entrypoints: `packages/tax/sli_relationship_recording.py` has opaque
reference, exact relationship, evidence/contribution and revision-checked
batch mechanics; it is a mechanism precedent, not mortgage authority.
`packages/tax/f1098_statement_recording.py` already records/corrects/withdraws
nine report-local answers, but `_require_current_statement` additionally
requires a globally single report. Remove only that obsolete global stop
for the exact-source recording operation. The offered review/UI remains a
later unit, not silently declared multi-report-ready here.

Core v53 has all incumbent F1098 sources, family/closure and v2 local
vocabulary; the new mortgage relationship vocabulary is not yet a member.
This unit explicitly loads/adopts its new bundle for recording. Track 2
will publish a complete package successor before the production coordinator
can consume it. Do not claim a calculated deduction from recorder tests.

## Implementation boundary and ownership

- Add `packages/content/tax/2025/mortgage-borrowing.bundle.json` using an
  existing published bundle/fact-type shape and distinct mortgage entity kind.
  Implement exact identifiers/keys/outcomes in the selected connected contract:
  borrowing/year recognition outcomes, four-key report inclusion outcomes,
  numeric annual ceiling, borrowing/year other-debt answer and all five
  separately typed shared answers. Do not change published schema bytes.
- Add `packages/tax/mortgage_borrowing_recording.py` and a narrowly scoped
  loader in `packages/tax/loader.py`. Expose durable introduction,
  record/correct/withdraw operations and revision-checked atomic explicit
  clear. Reuse safe existing primitives where appropriate; do not retrofit
  mortgage meanings into SLI or add a general recorder framework.
- Modify only the exact-source restriction in
  `packages/tax/f1098_statement_recording.py` and its affected tests/docstring.
  Preserve v1/v2 adoption, evidence shape and all singleton semantics.
- Add `tests/test_mortgage_borrowing_recording.py`; optional small shared test
  helpers only if directly needed. Existing tests may change only where their
  assertion is the deliberately removed global multi-report prohibition.
- Record concise results in `docs/reviews/mortgage-statement-borrowing/track1-build-report.md`.
  Do not edit the plan, phase-state, review verdicts, production packages,
  registries, releases, derivation/kernel code or source review/UI modules.

## Observable cases

| Case / mutation | Required observation |
| --- | --- |
| Introduce two equally labeled references | Different opaque IDs; current correct-kind entity required, label never matches a loan. Wrong-kind/ended reference refuses without writing. |
| Two exact current reports | Each receives its own nine local answers/evidence through the real durable recorder; changing A leaves B byte-for-byte supported. Missing/non-current exact report refuses. |
| Recognition and exact pair | Affirm/deny/cannot-tell/correct/withdraw have distinct current carriers. Replacing one outcome atomically ends the prior carrier; withdrawn is not a negative answer or absence. Other pair remains unchanged. |
| Annual ceiling | Finite nonnegative numeric upper bound, evidence records its actual meaning. Reject invalid numeric input (including booleans/nonfinite). Correct/withdraw exact A/year only. Do not choose a Box 2 or compute tax. |
| Other debt | Exact prompt excludes this borrowing; key is borrowing/year. No answer for A can become B's answer. Yes/no/cannot-tell remain distinct. |
| Five shared answers | Separate explicit new claims with adopted v2 vocabularies; never copy local findings. In particular `no-one-else-owes-it=yes` means no other obligor. Corrections/withdrawals affect only the exact shared claim, not independently recorded local support. |
| Clear A/year | One revision-checked batch ends its recognition/outcome carriers, all its pair outcomes, five shared answers and ceiling. Keeps sources/Box1/2/3, local answers, A's other-debt answer, entity, family closure and history. Preserves B/other-year claims where schema supports them. Does not assert no debt. |
| Clear A, introduce B | A's retained other-debt answer still names A; no B coverage finding appears. Same A/year can retain its still-current answer. |
| Amount-only source correction | Same report identity and loan relationship/ceiling remain independently supported; no automatic propagation by matching values. Source change does not invent a new link. |
| Stale revision, incomplete tail, reused operation/evidence | Refusal is atomic: no partial evidence/claim/retirement. Reload/replay recovers exactly the committed outcomes. |
| History compatibility | Existing one-report v1/v2 save/correct/withdraw tests stay valid except the explicit multi-report recording stop. No existing fact or category is reinterpreted as shared. |

Use actual ActLog, projection/currency and durable recorder APIs. Synthetic
workspace construction can supply document facts and entities, explicitly
labeled; it may not supply the new relationship findings instead of invoking
the recorder being tested. No hand-built RunContext or inference about tax
acceptance. Late family-transition/closure integration is a later unit.

## Verification, review and stop conditions

Run focused recorder/bundle/loader tests and repository mypy for typed Python.
Use normal pytest parallel settings, not repeated full suites. CI remains the
broad gate. Foreman reviews exact scope, atomicity and omitted adversarial
cases; no separate independent production review is scheduled for this unit.

Stop for a new schema/engine requirement, new tax or claim-scope decision,
inability to preserve atomicity/current outcome distinctions, or an out-of-
scope code change. Propose the smallest specific boundary change rather than
silently enlarging the assignment. Do not allocate a package version.

Before editing, echo scope, evidence ceiling and stop conditions. Commit small
meaningful completed increments with the shared commit lock and explicit
staging; keep all work on this primary branch. Return named commits, actual
commands/results, limitations and clean assigned paths. Never spawn.
