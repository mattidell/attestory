# Examination — Citation Resolution it2 Clean-Room Rival

## Method and boundary

This Rung-2 examination is a paper contract trace against the committed
`form-field.v1`, package-validator, and 2025 reference shapes.  No repository
implementation, fixture, schema, or source content was changed.  The proposed
successor names below are contract sketches, not adopted schemas.

The trace checks the predeclared Gate-2 cases in
[`plan.md` § Gate 2](plan.md), against the P1/P2 clauses in
[`it2/design.md`](it2/design.md).  “Accept” means static package validation
would report no citation issue; it never means legal correctness.

## Proposition disposition

| Proposition | Result | Why |
| --- | --- | --- |
| CIT-P1 | **settled-at-static-level** | A citation citizen plus exact attachment pin gives independent immutable content without a second membership authority. |
| CIT-P2 | **settled-at-static-level** | Strict schema, exact package closure, and published-byte checks define a bounded resolver without legal/network semantics. |

## Seven-case paper trace

| Gate-2 case | Synthetic setup and observed static result | Contract evidence |
| --- | --- | --- |
| 1 — positive field | `form-field.v2` line 1a carries `{id:"demo.citation.1040-line1a",version:"v1"}`; P includes the same `citation` member, which validates as `irs-form`. **Accept**; trace is field → exact pin → member → registry-verified bytes. | [plan case 1](plan.md); [P1 attachment](it2/design.md#attachment-and-adoption); [P2 algorithm](it2/design.md#resolution-algorithm-and-outcomes) |
| 2 — positive rule | A `rule-artifact.v2` attaches one exact `us-code` citation member. **Accept**; it is explanatory only and leaves `when`, `value`, and `publishes` unchanged. | [plan case 2](plan.md); [P1 attachment](it2/design.md#attachment-and-adoption) |
| 3 — opaque residual | A residual-closed field supplies only `citation_ref: "see 1040 instructions"`. **Reject** with `CITATION_OPAQUE_RESIDUAL`; no dual read is proposed. | [plan case 3](plan.md); [P1 issue map](it2/design.md#p1-issue-map) |
| 4 — malformed structure | A citation declares `authority_family:"us-code"` but omits `section`, or supplies a locator not matching its family. **Reject** with `CITATION_SCHEMA_INVALID`; no repair/coercion occurs. | [plan case 4](plan.md); [P1 decision](it2/design.md#decision); [P2 issue map](it2/design.md#resolution-algorithm-and-outcomes) |
| 5 — registry miss | A structurally valid locator names no external corpus entry. **Neither legal accept nor legal reject is claimed:** static resolution may accept only its schema/package identity, and reports no `legal_verified` status. A future corpus registry is a separate contract. | [plan case 5](plan.md); [P2 decision](it2/design.md#decision) |
| 6 — Article 11 overreach | A proposed resolver branch fetches an IRS page or decides that a Code locator supports a rule condition. **Reject/redesign** as `CITATION_RESOLVER_OVERREACH`; declared schema checks are permitted, tax interpretation is not. | [plan case 6](plan.md); [P2 decision](it2/design.md#decision) |
| 7 — lifecycle | P@v1 attaches C@v1 and validates.  A successor P@v2 attaches C@v2. P@v1 still resolves C@v1. Offering changed bytes for C@v1 causes `CITATION_IMMUTABILITY_VIOLATION` and P@v1 is rejected, not rewritten. | [plan case 7](plan.md); [P1 decision](it2/design.md#decision); [P2 issue map](it2/design.md#resolution-algorithm-and-outcomes) |

## Constraint checks

| Check | Result |
| --- | --- |
| ADR-0003 / Article 9 | Citizen schema, opaque id, exact version, strict validation, and registry-backed immutable bytes; no tolerant reader. |
| ADR-0006 | Package remains closed; all defects accumulate as contained issues before invalid package rejection. |
| ADR-0012 | Field citation is presentation content; dispositions, values, and field-to-symbol one-way binding remain unchanged. |
| ADR-0027 / 0028 | `artifact-package` remains the sole member/adoption authority; citation is a typed exact member and non-derivation join, not a path or side manifest. |
| Article 11 | No fetch, legal corpus interpretation, applicability, or hard-coded authority meaning in the runner. |

## Remaining non-static questions

An external authority corpus, canonical human display, link policy, legal
correctness, and other jurisdictions remain deliberately unresolved.  None is
needed to reject opaque, malformed, unpinned, or rewritten citation content.
