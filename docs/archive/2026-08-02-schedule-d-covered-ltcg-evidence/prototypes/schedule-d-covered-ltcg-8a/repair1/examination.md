# Repair 1 Examination

Audience: prototype committee. Evidence ceiling: **Rung 1, static paper**.

This examination measures only CA-02 and CA-04 against the selected rival at
`bbecd3f3aae6777cf06e4bdbe58d91545f4faedd`. It does not reopen topology
selection or reassess P1, CA-05, or CA-06.

## Repair disposition

| Finding | Status | Exact repaired evidence |
| --- | --- | --- |
| CA-02 | **Resolved at Rung 1 and explicitly adopted** | [P2-S5A](design.md#1-ca-02--adopted-p2-s5-replacement) states the closed-not-closed-empty boundary, zero behavior, once-only line-13 contribution, and non-expansion limits as a standalone numbered successor. [Shared case 7](design.md#32-schedule-d-route-only--shared-case-7-regression) confirms closed-empty behavior is unchanged; [shared case 6](design.md#33-both-gains--shared-case-6) proves closed-nonempty contribution once. |
| CA-04 | **Resolved at Rung 1** | [P3-S8](design.md#22-numbered-successor-sentence) gives the exact direct and Schedule-D `P` signatures, exact `TAX16` sets, no-tag rule, and direct/transitive boundary. The [four-row Decision 7 rewrite](design.md#23-adr-0050-decision-7-rewritten-in-terms-of-p) names every surviving declaration/conclusion pin and shows that none move or are new. |

## CA-02 examination

### Question

Is the selected P2-S5 boundary now a citable adopted successor rather than a
worked-example inference?

### Result

**Yes.** P2-S5A expressly supersedes only the milestone plan's
closed-empty-only wording for this bounded class:

- `B2` must have a current closure, whether empty or nonempty;
- closed-empty still contributes authoritative zero;
- under the Schedule-D producer, closed-nonempty contributes its current
  subtotal once at line 13; and
- the sentence does not widen the transaction family, edit ADR-0050, or add
  another line-9/QDCG path.

The arithmetic is recovered in two adversarial instances. Shared case 7 has
`B2` closed-empty and retains `L13=0`, `P=4,200`, and one downstream capital-
gain edge. Shared case 6 has `B2=1,200` and eligible transaction gain 4,000;
`L13=1,200`, `LD16=P=5,200`, and line 9 consumes only the resulting line 7a.
There is no second 1,200 edge.

### Official-form check

The repaired boundary matches the [2025 Schedule D instructions](https://www.irs.gov/pub/irs-prior/i1040sd--2025.pdf):
line 13 is the entry point for Form 1099-DIV box-2a capital-gain
distributions. The [2025 Form 1099-B instructions](https://www.irs.gov/pub/irs-prior/i1099b--2025.pdf)
continue to ground the separate eligible transaction class; P2-S5A does not
expand it.

## CA-04 examination

### Question

Can a route-neutral numeric `P` preserve ADR-0050's route-specific direct
line-16 pins without a route tag or a Rung-2 substrate answer?

### Result

**Yes, at the paper-contract level.** The current producer is recoverable
from `P`'s declared direct-pin lineage:

- direct `P` directly pins box-2a authority, C1-C4, and checked conclusion
  `"no"`; and
- Schedule-D `P` directly pins `LD16`, `ATT-D`, and `B1`-`B9`.

Those signatures are distinct without changing `P`'s numeric payload.
P3-S8 therefore conditions only the pin set, not the numeric state partition:

- with direct `P`, `TAX16` keeps ADR-0050 Decision 7's original branch pins;
- with Schedule-D `P`, `TAX16` carries no direct-route declaration or
  conclusion pin; and
- in both routes, upstream family/content/completeness authority stays
  transitive through `P` rather than being duplicated as direct line-16
  authority.

This is not an implicit “same pins” assertion. The repaired equation is:

```text
TAX16-direct-pins =
  COMMON16
  union Decision7-extra(Q,P)  when P has P-direct lineage
  union empty-set             when P has P-schedule-d lineage
```

`COMMON16` is exactly taxable income, filing status, rounding, `Q`, `P`, the
selected computation parameters, and exact citation. The Decision 7 extras
are exactly the four rows in the repair: `{declaration=no, conclusion=no}`;
`{conclusion=no}`; `{declaration=yes, conclusion=no}`; and `{}`.

No accepted pin moves. The checked conclusion remains a direct `TAX16` pin
in the three direct-route rows that require it, even though it is also
transitive through `P`. There are no new direct pins. C1-C4, B2 authority,
`LD16`, `ATT-D`, and `B1`-`B9` never become direct `TAX16` pins.

### Affected-case recovery

| Evidence | Recovered distinction |
| --- | --- |
| [Direct-only case](design.md#31-direct-route-only--positive-box-2a-no-eligible-transaction) | `P=1,200`, `Q=0`: `TAX16` directly carries `COMMON16` plus checked conclusion `"no"`, but not C1-C4 or B2 authority. |
| [Schedule-D-only case 7](design.md#32-schedule-d-route-only--shared-case-7-regression) | `P=4,200`, `Q=0`: `TAX16` carries exactly `COMMON16`; `LD16`, `ATT-D`, and `B1`-`B9` remain transitive. |
| [Both-gain case 6](design.md#33-both-gains--shared-case-6) | `P=5,200`, `Q=500`: `TAX16` carries exactly `COMMON16`; despite `Q>0/P>0`, it carries neither direct-route declaration nor conclusion because Schedule D produced `P`. |
| [Atomic outcome ledger](design.md#24-atomic-outcome-and-pin-ledger) | Blocked, direct guard-inapplicable, closure-backed zero, direct positive, and Schedule-D boundary failure remain distinct and have enumerated pins/walks. |
| [Forward correction](design.md#41-direct-to-schedule-d) | Direct authority is displaced, the honest intermediate block/guard is preserved, then new Schedule-D lineage publishes; no direct pin survives by numeric equality. |
| [Reverse correction](design.md#42-schedule-d-to-direct) | Schedule-D lineage is displaced, the intermediate state has no numeric `P`, then corrected C1/conclusion authority publishes a new direct chain; no old finding revives. |

### Route-tag and substrate boundary

A first-class route tag is **not required by the Rung-1 pin contract** because
the producer signature is recoverable from direct lineage. This finding does
not prove how the generic substrate enforces exactly one producer or exposes
the signature mechanically. That remains CA-06 and is intentionally
unresolved here. No schema, validator, evaluator, or content probe was used.

## Proposition status after repair

| Proposition | Status after repair | Exact basis |
| --- | --- | --- |
| P1 — independent anchor-keyed transaction family | **Unchanged; settled at Rung 1** | Selected `it2/design.md`, P1-S1 through P1-S7, and selected `it2/examination.md`, “P1 examination.” This repair makes no P1 statement. |
| P2 — direct multi-read completeness | **Settled at Rung 1; CA-02 resolved** | Selected P2-S1 through P2-S4 and P2-S6 through P2-S8 remain unchanged; [P2-S5A](design.md#1-ca-02--adopted-p2-s5-replacement) is the adopted replacement, with cases 6 and 7 rechecked. |
| P3 — shared selected preferential base | **Settled at Rung 1 for topology and pin location; CA-04 resolved** | Selected P3-S1 through P3-S5 and P3-S7 remain unchanged; P3-S6's state partition remains unchanged; [P3-S8](design.md#22-numbered-successor-sentence), the [four-row table](design.md#23-adr-0050-decision-7-rewritten-in-terms-of-p), and both correction traces close the direct-pin gap. CA-06 remains a separate production prerequisite. |

## Stop result

CA-02 and CA-04 are resolved at the authorized Rung-1 ceiling. The repair
does not touch P1, CA-05, CA-06, topology selection, governance text, an ADR,
code, schemas, content, fixtures, tests, or project pointers. Confirmation,
contract synthesis, implementation, and any Rung-2 work remain outside this
branch's assignment.
