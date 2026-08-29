# Adversary review r1: Ordinary Input Mapping (Seam 6)

Reviewed `packages/tax/obligation_acquisition_mapping.py`,
`tests/test_obligation_acquisition_translation.py`, and
`packages/kernel/contribution.py` / `packages/kernel/findings.py` /
`packages/kernel/facts.py` (the real admission boundary this module calls
into) on `prototypes/ordinary-input-mapping/it1`. All attacks below were run
against the real functions via throwaway scripts (not reasoned about
abstractly); scripts are not committed (scratchpad only).

## 1. Smuggling a classification into the emitted fact

- Extra field `tax_treatment` on the answer set: rejected by
  `validate_ordinary_answers` and by `map_ordinary_acquisition_answers`
  itself (schema `additionalProperties: false`). Held.
- Free-text classification words inside `obligation_description` (e.g.
  `"taxable bond, election under 171 to reduce basis; schedule b line 1"`):
  **accepted and emitted verbatim** into `value.obligation.description`.
  This is not a structural violation of the charter — the field is
  documented as free-text identifying information, and nothing downstream
  in this seam reads or classifies it — but it means the "no tax
  classification requested or supplied" guarantee rests entirely on no
  future rule ever pattern-matching this description field. Worth naming
  explicitly as a residual risk for Seam 5's authors, not fixed here.
- Injection-like content (`<script>...`, `DROP TABLE...`) in
  `obligation_description`: accepted and stored as an opaque string; no
  downstream code path evaluates or executes it in this module or the
  kernel functions exercised. Held (not a code-injection surface here).

## 2. Emitting more than one canonical fact / a derived conclusion

Could not construct an answer set that produces more than one
`finding.v2` or a value field outside the five named ones — the emitted
`value` is checked against `_CIRCUMSTANCE_VALUE_SCHEMA`
(`additionalProperties: false`) **twice**: once implicitly by construction
in the mapper, and again independently at admission (`_validate_finding`
in `findings.py`, `fact_type["value_schema"]`). Tampering the finding's
`value` post-mapping to add a `tax_classification` key and pushing it
through `apply_contribution_batch` directly (bypassing the mapper) was
**rejected** at admission: `"Additional properties are not allowed
('tax_classification' was unexpected)"`. Held — the guarantee is enforced
at the boundary, not just by the mapper being well-behaved.

## 3. Defeating contribution admission

- Direct `apply_act(..., {"kind": "assertion", ...})` skipping the
  contribution act entirely, citing a `contribution_id` that was never
  admitted: **rejected** (`references unknown contribution`).
- Contribution act with `kind` spoofed to `"demo-note"`: **rejected**
  (`apply_contribution_batch` requires `kind == "contribution"`).
- Tampered evidence: built a real contribution/assertion pair, then
  rewrote the assertion's `finding.evidence_ids` to point at unrelated
  evidence after mapping (per the charter's own scenario 4): **rejected**,
  contribution's `evidence_id` is not a member of the finding's
  `evidence_ids`.
- Exact duplicate resubmission (same `contribution_id`/`finding_id`
  replayed): **rejected** (`contribution already exists`).
All four held — admission is real, not a rubber stamp.

## 4. Malformed / boundary / hostile values

Ran via `validate_ordinary_answers` and, where it survived, through the
full `contribute_ordinary_acquisition` pipeline.

| Input | Result |
|---|---|
| Future acquisition date (`2099-01-01`) | **Accepted** — no temporal bound in the schema. Named, not fixed: this seam does not claim to validate against "today"; a later seam (constraint/consistency) may need to. |
| Zero accrued interest | Accepted (schema allows `minimum: 0`) |
| Negative accrued interest | Rejected (schema `minimum: 0`) |
| Extremely large amount (`1e18`) | Accepted, admitted end to end |
| **`inf` accrued interest** | **Accepted by `validate_ordinary_answers`, admitted end to end through the real contribution boundary, terminal phase `completed`.** JSON Schema `"type": "number"` in this validator does not exclude non-finite floats, and neither the mapper's own schema nor the kernel's admission-layer value-schema check catches it either — Python's `jsonschema` treats `float('inf')` as a valid number satisfying `minimum: 0`. |
| **`nan` accrued interest** | **Same as above — fully admitted, `completed`, stored value is NaN** (`value != value` confirmed True in the committed finding). This is worse than the `inf` case: a NaN dollar amount silently enters the fact lattice as a "canonical circumstance," and any later arithmetic over it (Seam 3/5) will silently propagate NaN rather than fail closed. |
| Wrong-but-plausible currency (`"usd"` lowercase) | Rejected (`const: "USD"`) |
| Missing `tax_year` | Rejected (required) |
| Fractional `tax_year` (`2025.5`) | Rejected (`type: integer`) |
| Unicode payer name | Accepted (no charset restriction; no injection risk observed) |
| Whitespace-only payer name (`"   "`) | **Accepted** — `minLength: 1` counts whitespace as content. A person cannot ordinarily identify a payer from an all-whitespace name; minor, but it means "payer_name present" is not actually enforced, only "payer_name non-empty-string". |
| String-typed amount (`"42.5"`) | Rejected (`type: number`, no coercion) |
| Spoofed `fact_id` override pointing at an unrelated fact type | Rejected at admission (`references unknown fact`) |

## 5. Idempotency — resubmitting the same ordinary answers

Submitted the identical valid answer set twice against the same bundle,
using a **fresh** `contribution_id`/`finding_id`/`evidence_id` binding each
time (i.e., what a real UI would generate on a second, distinct submit —
not a literal double-click replay of the same ids, which is separately and
correctly rejected as shown in §3).

Result: **both submissions completed.** `state.findings` ends up holding
two independent findings (`demo.finding.acq-a`, `demo.finding.acq-a-2`)
sharing the same `fact_id`. This is not "double counting" in the sense of
summed values — `findings.py::_current_value_for_fact` treats the
last-inserted finding as current — but it is **silent, unflagged
duplication**: nothing in this module or the kernel's `"free"` supersession
policy (which this module's own fixture bundle declares for its fact type)
requires the second submission to reference, supersede, or even acknowledge
the first. A user who resubmits after a UI glitch gets two live
contributions and two live findings for the same real-world circumstance,
with no correction record and no rejection. The examination.md explicitly
names the `"free"`-policy fixture as "not a claim about the identity/
association mechanism production will select" (Seam 1–3's job) — so this
is a disclosed scope limitation, not a hidden defect, but it is a real
fail-open gap in the current instantiation of the charter's "contribution
admission validates output" requirement as far as idempotency goes.

## Verdict

The core structural guarantees the charter cares about most —
**closed-schema classification exclusion** and **contribution admission
being real, not a rubber stamp** — held under every attack tried, including
tampered evidence, spoofed act kinds, direct-assertion bypass, and
tampered post-mapping values. Those are genuinely load-bearing, not
decorative.

Two real defects survived attack, both numeric-boundary gaps rather than
classification leaks:

1. **`inf`/`nan` for `accrued_interest_paid_to_seller` are accepted by the
   ordinary-answers schema and admitted all the way through the real
   contribution boundary as a `completed` fact.** This is a fail-*open*
   result on a hostile numeric input the test suite does not cover, and it
   is the one finding in this review that I would call disqualifying for
   "fail closed on hostile input" as literally stated in the charter and
   examination — it should be closed (e.g. `jsonschema` `format` guard, or
   an explicit finiteness check before `validate_ordinary_answers` returns)
   before this seam is treated as production-ready.
2. Whitespace-only `payer_name` and undated-bound (future) `acquisition_date`
   both pass; lower severity, worth a follow-up but not fail-closed
   violations of a stated guarantee.

Idempotency (§5) is a disclosed, named scope limitation rather than a
silent defect, but a reviewer approving this seam for anything beyond a
prototype should treat "resubmission does not require correction" as an
open item for whichever seam adopts the real identity/association shape.

No tax-classification smuggling attempt succeeded structurally; the
free-text `obligation_description` field is a real but inherent residual
risk of any free-text field, not a defect unique to this mapper.
