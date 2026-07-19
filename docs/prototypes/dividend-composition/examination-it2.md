# Examination — clean-room rival, Dividend Composition (D3), iteration 2

Sealed from incumbent. Synthetic `demo-*` only. Evidence: Rung 1 paper for
D3-P2/P3; Rung 2 probes for P3 case 2 only. Design:
`docs/prototypes/dividend-composition/it2/design.md`.

## Outcomes

### D3-P2 — **settled at Rung 1**

Ordinary line **3b** composes from box **1a** over closed family
`tax.us.2025.f1099div.1a`. Universe citizen `dividend-universe.v1` names
composable {1a, 1b} and recorded-non-composable {2a, 3, 5, 7, 12}. Excluded
boxes ride `recorded-boxes` findings (not family members). Box **2a** raises
return-level disposition `CAPITAL_GAIN_DISTRIBUTION_RECORDED` for D2; box **7**
is named recording only. Cases 1, 4, 5, 6 support; no machinery evidence
required beyond committed collect/closure/form-field patterns.

### D3-P3 — **settled at Rung 2 for the kill-case; Rung 1 for the rest**

Qualified line **3a** composes from box **1b** over family `…f1099div.1b`.
Structural subset **1b ≤ 1a** is enforced at **admission** (after
`value_schema`, before state mutation; contribution fails closed). Schema-only
enforcement is unrepresentable (probes P1–P5). Line **3a ≤ 3b** holds by
construction (sum inequality under admission pairing); families may block
independently without violating the inequality on published pairs. Case 2 is
probe-backed; cases 1 and 3 complete the subset story.

### D3-P1

Not in prototype scope — implement-normally under ADR-0015 (DIV statement
entity + sameness). Governance may check conformance in passing.

## Case disposition

| Case | Result under this design |
| --- | --- |
| **1a** single 900/600 | 3b=900, 3a=600 publish with citations; subset holds |
| **1b** two statements + 400/0 | 3b=1300, 3a=600; zero qualified admitted |
| **2** 1b>1a kill | Dies at **admission** (not schema); probes show schema accepts; batch fails; pair never current |
| **3** line-level subset | Proven: ΣQ ≤ ΣO under admission pairing; order-independent rules; open-1b blocks 3a only |
| **4** box 2a | Admits; records; 3a/3b publish; walk to `CAPITAL_GAIN_DISTRIBUTION_RECORDED` → D2; box 7 contrast |
| **5** empty / undeclared | Closed-empty → zeros publish; undeclared/open → both lines block |
| **6** universe creep | Composing 2a unrepresentable (no member predicate, forbidden collects, no authorized symbol) |

## Mandatory cases (2, 4, 6)

All three resolve on paper; case 2 additionally rests on Rung-2 demonstration
that committed Draft 2020-12 `value_schema` validation and
`_validate_finding` cannot express 1b≤1a, so the named locus must be admission
machinery (Track 2 production condition), not a schema regex.

## Unresolved / deferred (not decision-blocking for D3)

- Exact production schema ids/bytes and package-validation rule text (Track 1).
- D2 worksheet and contradiction implementation (consumes the named 2a
  disposition only).
- Schedule B itemization (D1 reads statement facts; does not reshape them).
- Defense-in-depth composition re-check of 3a≤3b (optional; admission is
  structural locus).

## Stop

Paper settles the enforcement locus and universe posture. No further rival
evidence purchased. No production composition code or schema edits in this
iteration.
