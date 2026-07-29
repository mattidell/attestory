# Repair 1 Confirmation — Component Authority and QDCG Handoff

**Seat and boundary.** Author-independent focused Confirmation Reviewer under
`charter-repair1-confirmation.md`. Launch commit verified at
`70aba98afd5ff7c33a93cac70ebea65e61ea044d`. Exact object: repair commit
`a60e2d1f6c5699cd22a907a39912834fd2cbd07c` (`repair1/design.md`,
`repair1/examination.md`), measured only against `charter-repair1.md`,
findings T-F1/T-F2 in `round-1-triage.md`, and retained P2/P3 boundaries of
the selected design at `099882e`. Rung 1 static paper only. No production
edits, probes, contract synthesis, ADR draft, pointer advance, push, or
merge. `repair1/examination.md` self-report is not used as evidence.

**Safety.** `python3 tools/envelope_scan.py --range main..HEAD` completed with
exit 0. All cited amounts and identities are synthetic `demo.*` paper
instances.

---

## Status lines

1. **T-F1: NOT CONFIRMED**
2. **T-F2: NOT CONFIRMED**
3. **REGRESSION BOUNDARY: INTACT**
4. **Overall verdict: NOT READY**

---

## Measurement method

For each charter confirmation clause, the measurement is whether
`repair1/design.md` alone makes the repaired rule and required cases
recoverable with exact synthetic facts, authority, pins, current/displaced
states, and dispositions. Claimed successor sentences without recoverable
cases fail. Retained `it2/design.md` material is read only to detect
contradiction or incomplete supersession, not to reassess unrelated it2
propositions.

Controlling tax text used for T-F2 (as recorded in `round-1-triage.md` and
the milestone tax-content boundary): 2025 Form 1040 Exception 1 includes the
boxes 2b/2c/2d absence condition; when Schedule D is not required and line 7a
reports capital-gain distributions, the Qualified Dividends and Capital Gain
Tax Worksheet applies; worksheet line 3 takes Form 1040 line 7a when Schedule
D is not filed. This confirmation does not climb a rung or reopen topology
selection.

---

## T-F1 — Complete Exception-1 component authority

| # | Confirmation clause | Result | Recoverable evidence in `repair1/design.md` |
| --- | --- | --- | --- |
| 1 | All four Exception 1 conditions represented | **Partial (rule only)** | Successor sentence 1 names four fact types including `tax.us.2025.exception1.no-boxes-2b-2c-2d`. |
| 2 | Boxes 2b/2c/2d as contributed `{yes,no}`, no default, presence-before-value | **Partial (rule only)** | Same sentence claims domain/presence-before-value; no admission/validation case shows rejection of a default or non-domain value. |
| 3 | Independently correctable/pinned; named absence; no fake source families | **Partial** | Case 11 names the missing fact type exactly and states no Schedule D fabrication; Case 16 asserts supersession without pin/finding versions. |
| 4 | Distinct from box-2a family closure | **Pass (paper claim)** | Sentence 1 states distinctness; Cases 11–12 keep family closed while the new component varies. |
| 5 | All four current `"yes"` for E; Schedule-D-required consistent | **Partial (rule only)** | Sentence 2 and Cases 11–12 state E/conclusion behavior for the new component; base eligible topology is not re-instantiated with four components. |
| 6 | Eligible, missing, `"no"`, forward and reverse correction with exact facts and dispositions | **Fail** | See findings F1–F2. |

### Required-case recoverability (T-F1)

| Required repaired case (`charter-repair1.md`) | Artifact support |
| --- | --- |
| Eligible single payer with every repaired component current | **Insufficient.** No dedicated repaired eligible case. Case 13 assumes “E is true (all four `"yes"`)” and line 7a=`1500.00` without listing the four component findings, member/closure facts, pins, line 7b, line 9, taxable income, or line 16 dispositions. |
| Authority missing for boxes 2b/2c/2d | **Partial.** Case 11: member `1500.00`, three components `"yes"`, fourth absent; E false; conclusion undefined; walk names `tax.us.2025.exception1.no-boxes-2b-2c-2d`; neither line 7a nor Schedule D publishes. Does not use exact `blocked` disposition vocabulary or pin tables. |
| Condition current `"no"` so Schedule D required | **Partial.** Case 12: fourth component `"no"`; direct route “inapplicable”; conclusion `"yes"`; no line 7a; no Schedule D; QDCG inapplicable. Omits explicit `guard_inapplicable` and pin set. |
| Forward and reverse supersession tracing 7a, 9, TI, 16 | **Insufficient.** Case 16 narrates displace/republish without finding ids, pin versions, current vs displaced identities, or numeric dispositions on line 9 / taxable income / line 16. |

### Retained it2 contradiction under repaired E

`repair1/design.md` opening sentence keeps all other `it2/design.md` sentences,
topology fragments, **and cases** unchanged unless explicitly superseded. The
repair supersedes/extends P1 inventory and E for four components, but does not
supersede:

- Component semantics map: “all **three** current `"yes"` (E)” (`it2/design.md`);
- Producer map: “three Exception-1 facts”;
- Topology cost “**+3**”;
- E-yes shorthand: only three components (`it2/design.md` Case section);
- Case 1 publications: “pins member + **three** components…”.

Under the repaired E (all four current `"yes"`), retained Case 1 is missing
`no-boxes-2b-2c-2d` and would not authorize publication. The repair never
reinstates an eligible four-component case with recoverable pins.

---

## T-F2 — QDCG selection and binding

| # | Confirmation clause | Result | Recoverable evidence in `repair1/design.md` |
| --- | --- | --- | --- |
| 1 | Select QDCG when Q>0 **or** applicable direct-route line 7a >0 | **Partial** | Repaired P3 sentence states the OR selection; Cases 13–14 assert selection. Retained it2 Case 10 contradicts the Q=0 ∧ line7a>0 arm. |
| 2 | Bind worksheet line 3 to selected line-7a publication when Schedule D not filed | **Partial (rule + thin case)** | Sentence names worksheet line 3; Case 13 binds capital-gain input to line 7a `1500.00`. No pin set from line-16 publication to the line-7a finding. |
| 3 | Preferential treatment for Q=0 with positive line 7a | **Fail as settled paper** | Case 13 claims preferential computation; it2 Case 10 still says ordinary-bracket only for the same shape. |
| 4 | Preserve QD path for Q>0 with closure-backed line 7a=0 | **Partial** | Case 14: E true, closed-empty line 7a=`0`, Q=`50`, QDCG selected, capital-gain input `0`. No line 9 / TI / line 16 pins. |
| 5 | Ordinary tax only when both inputs are closure-backed zero | **Partial / incomplete** | Case 15: Q=`0`, line 7a=`0`, ordinary reduction. Does **not** state closed-empty / closure-backed zero for line 7a (unlike Case 14). |
| 6 | Never zero blocked/guard-inapplicable line 7a; no raw box-2a reads; no incidental operand ordering | **Partial (rule only)** | Sentence forbids defaults and raw reads and claims ordering-independent structure. No expression tree or case shows blocked line 7a not coerced to zero in line 16; no structure demonstrating ordering independence. |
| 7 | Exact current/displaced states and pins through 7a, 9, TI, 16 | **Fail** | Cases 13–16 omit recoverable pin/current/displaced tables for that chain. |

### Required-case recoverability (T-F2)

| Required repaired case | Artifact support |
| --- | --- |
| Q=0, positive line 7a → QDCG + preferential CG input | **Insufficient for confirmation.** Case 13 states selection and binding; no worksheet/line-16 disposition value; contradicted by retained Case 10. |
| Q>0, line 7a=0 → qualified-dividend path preserved | **Partial.** Case 14 only. |
| Q=0, closed-empty line 7a=0 → ordinary reduction | **Insufficient.** Case 15 omits closed-empty authority for the zero. |
| Forward/reverse component supersession through 7a/9/TI/16 | **Insufficient.** Case 16 narrative only (same as T-F1). |

### Instruction alignment (paper)

Against the triage/milestone reading of the 2025 instructions, the **repaired
successor sentences** for selection (Q>0 **or** positive direct-route line 7a)
and worksheet line 3 binding to the selected line-7a publication are directionally
correct. That is not enough: the confirmation charter requires the repaired
**cases** to make selection, binding, preferential treatment, and ordinary
reduction recoverable, and requires testing the corrected Case-10 shape directly.
The retained it2 Case 10 still reduces Q=0 ∧ line 7a=`1500` to ordinary tax and
treats preferential CGD-when-Q=0 as a production flag / unresolved question —
exactly the T-F2 defect triage called decision-blocking.

---

## Regression boundary (P2 / retained P3 honesty)

| Boundary element | Result | Evidence |
| --- | --- | --- |
| Successor/historical box-2a graph exclusivity | **Intact** | Repair does not rewrite P2 exclusivity or Cases 8a/8b; does not introduce a historical collect path. |
| Non-null box-2a presence signal and contradiction interlock | **Intact** | Case 5 in it2 retained; repair does not weaken `CAPITAL_GAIN_DISTRIBUTION_RECORDED` interlock. |
| Closure-backed zero rather than assumed absence | **Intact as retained rule** | Repair does not redefine closed-empty; Case 14 still uses closed-empty for line 7a=`0` in the Q>0 path. Case 15’s omission is a T-F2 evidence gap, not a redefinition of closure. |
| No raw downstream box-2a reads | **Intact** | Repaired P3 binding forbids raw box-2a and historical recorded content; it2 Cases 9a/9b retained. |
| Honest non-publication when Schedule D required or component authority missing | **Intact as stated** | Cases 11–12: no line 7a publication; no Schedule D artifact; QDCG inapplicable when conclusion `"yes"`. |

No repair text was found that reopens owner topology selection or softens these
boundaries. Bare assertion at the end of Case 16 that “regression statements
… hold true” is not additional positive evidence; non-regression is measured by
absence of weakening edits plus retained it2 negative cases.

---

## Numbered findings

### F1 — Decision-blocking (T-F1)

**Unmet charter clause:** T-F1 items 5–6; `charter-repair1.md` required
evidence item 1 (eligible single payer with every repaired component current).

**Evidence:** `repair1/design.md` adds `tax.us.2025.exception1.no-boxes-2b-2c-2d`
and requires all four current `"yes"` for E, but does not re-instantiate eligible
publication with four component findings, pins, and downstream dispositions.
Retained `it2/design.md` E-yes shorthand, Case 1 pin line (“three components”),
component semantics map (“all three”), and producer map remain three-component.
Under repaired E, retained Case 1 is authority-incomplete.

**Falsifier:** A repaired eligible case that lists all four current component
finding ids, pins them on line 7a (and checked conclusion), and shows line 9 /
taxable income / line 16 dispositions would close this finding.

### F2 — Decision-blocking (T-F1)

**Unmet charter clause:** T-F1 item 6; `charter-repair1.md` required evidence
item 4 (forward and reverse supersession of the new component tracing line 7a,
line 9, taxable income, and line 16); requirement to distinguish `blocked`,
`guard_inapplicable`, closure-backed zero, and published value.

**Evidence:** Case 16 states that superseding `no-boxes-2b-2c-2d` `"yes"`→`"no"`
displaces line 7a, 9, taxable income, and line 16 and that reverse supersession
republishes line 7a, without finding versions, pin edges, displaced identities,
or exact dispositions. Cases 11–12 use informal “non-publication” /
“inapplicable” language without the disposition kinds the repair charter
required.

**Falsifier:** Lifecycle tables with `demo.finding.*` versions, pin lists, and
explicit disposition rows for both directions would close this finding.

### F3 — Decision-blocking (T-F2)

**Unmet charter clause:** T-F2 items 1 and 3; triage T-F2 / Case-10 correction;
`charter-repair1.md` required evidence item 5.

**Evidence:** `repair1/design.md` supersedes it2 P3 point 4 with QDCG selection
when Q>0 **or** line 7a >0 and preferential computation when Q=0 and line 7a
positive (Case 13). The same file leaves it2 cases unchanged unless superseded;
it2 Case 10 still publishes line 16 as ordinary-bracket tax only for Q=0 and
line 7a=`1500.00` and flags preferential CGD-when-Q=0 as unresolved. Composite
paper is contradictory on the exact Case-10 shape confirmation was ordered to
test.

**Falsifier:** Explicit supersession/retirement of it2 Case 10 plus a single
repaired case with recoverable Q=0 / line7a>0 preferential path (and no
competing ordinary-only case) would close this finding.

### F4 — Decision-blocking (T-F2)

**Unmet charter clause:** T-F2 items 5–7; `charter-repair1.md` required evidence
items 5–7 (exact facts, pins, states through the chain; ordinary reduction only
for closed-empty zeros).

**Evidence:** Cases 13–15 state selection/binding outcomes without pin sets or
line 9 / taxable income / line 16 current values. Case 15 sets line 7a=`0`
without closed-empty / closure-backed authority. Ordering-independent
“declared conditional structure” is asserted without an expression tree or
case distinguishing structure from incidental `all`/`any` operand order
(contrast ADR-0038 / it2 P3 substrate language).

**Falsifier:** Full chain tables for Cases 13–15, closed-empty authority on the
both-zero reduction case, and a declared expression structure whose false
paths do not depend on operand order would close this finding.

### F5 — Non-blocking observation (regression)

**Charter clause:** Regression boundary only.

**Evidence:** Repair does not edit P2 exclusivity, signal interlock, or raw-read
rejection cases; reaffirms no raw box-2a reads and honest non-publication in
Cases 11–12. No regression finding is raised. This is not positive re-proof of
P2; it is absence of regression in the repair object.

---

## Rung-1 uncertainty

Rung 1 cannot mechanically execute the repaired line-16 expression (none is
given beyond prose) or prove evaluator short-circuit independence. That
uncertainty is already covered by F4 as an unmet paper obligation
(ordering-independent structure must be recoverable on paper). No Rung-2 climb
is authorized or needed to issue **NOT READY**: the decision-blocking gaps are
recoverability and internal contradiction at Rung 1.

Whether production would implement four components by updating retained it2
Cases 1–6 is outside this confirmation; on the committed repair artifact, those
cases are not superseded and therefore remain part of the composite design.

---

## Overall verdict

**NOT READY.**

T-F1 is not confirmed: the fourth Exception-1 component is named in successor
sentences, but eligible / lifecycle paper does not recover four-component
authority with exact facts, pins, and dispositions, and retained three-component
eligible cases were not superseded.

T-F2 is not confirmed: selection/binding sentences align with the cited 2025
worksheet direction, but the corrected Q=0 ∧ positive line 7a case is not
settled against the still-live it2 Case 10, and Cases 13–16 lack recoverable
pins and chain dispositions.

Regression boundary is **INTACT**: the repair does not weaken successor/
historical exclusivity, the presence-signal interlock, closure-backed zero as a
concept, no raw downstream reads, or honest non-publication when authority is
missing or Schedule D is required.

Contract synthesis, ADR drafting, production, and pointer advance remain
blocked under the charter until a further owner-directed repair (if authorized)
closes F1–F4.
