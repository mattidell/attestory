# First Tax Slice — Planning Inputs

Status note (2026-07-11): preserved broad source material. Track 0 concluded
with ADR-0011/0012 and the implementation milestone was narrowed to W-2 box 1
-> Form 1040 line 1a. Unresolved inputs here are deferred to later roadmap
milestones; they are not current First Tax Slice implementation scope.

Audience: Agents (planning material; not a milestone plan)

Accumulated inputs for the First Tax Slice milestone (roadmap item 5). These inputs have been converted into the milestone plan at `first-tax-slice.md`; this file remains as source material so the plan inherits evidence, not folklore.

## Carried obligations

- **Form-field and fact-type citizen families** (evaluation-analysis §5.6, deferred by the Derivation Machinery plan 2026-07-10): both prototype corpora referenced form fields and fact types as bare id strings (`examination-it1.md` Q11 negative evidence; `round-2-legibility.md` L-10 — box meanings are imported IRS knowledge). Derivation Machinery ships schema hooks only; this milestone designs the families against real content, where they can earn their shape. Production adoption of real rules is gated on them (ADR-0006 consequences).

## Product findings from the rule-language evidence (2026-07-11, owner-reviewed)

- **Closure assertions are the first operationalization of "done."** The source-set closure mechanism (ADR-0006 clause 8; Derivation Machinery Track 4 design note) requires user-facing assertions of the form "this source set is complete" ("that's all my W-2s," "I have no other interest income") — elective-class, supersedable facts that the published zeros pin. Aggregated across a return's source sets, these assertions are the concrete substance of "ready to file," previously an ordinary word with no term of art (definitions-work frontier). First Tax Slice should treat the closure-assertion vocabulary per real source set as content design, and the coverage read model should surface open (unclosed) source sets as first-class gaps.
- **Rendered-absence semantics are form content, not machinery.** Guard-based mutual exclusivity (the F8 pattern) means the unselected output fact does not exist; whether the rendered form shows a blank, a zero, or "N/A" on that line is a form-instructions decision to be encoded per line as rendering content. Three distinct "nothings" must never be conflated in rendering: a computed zero (real claim, pinned), a closure-backed zero from an empty source set (pinned to the closure assertion), and non-existence from a false guard (explained by the run record's inapplicable disposition, ADR-0008 point 4).

## Standing constraints inherited

- Real rule artifacts cite authoritative sources (project posture); synthetic workspace values only.
- Ratification conditions for adopted production use remain: second-runner portability re-proof on real content scale, and the operation-semantics canon covering the full real table/bracket corpora (evaluation-analysis §5.2/§5.4; the prototype tables were fixture-minimal by declared design).
