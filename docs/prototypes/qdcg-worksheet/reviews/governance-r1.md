# Governance Review — D2 QDCG Worksheet and Declared Absence (Round 1)

Reviewer: Governance, Medium tier, independent context. Advisory only.
Scope: `it1/design.md` + `examination-it1.md` (incumbent) and `it2/design.md`
+ `examination-it2.md` (clean-room rival), against `docs/prototypes/qdcg-worksheet/plan.md`
measurements, `docs/governance/constitution.md` Articles 7/9/10/12/13,
ADR-0006 (D1, D2, D7), ADR-0010 (D3–D6), ADR-0032, ADR-0035, ADR-0036, the
committed `rule-artifact.v2` schema, `artifact-package.v2` schema,
`packages/derivation/evaluator.py`, `package_validation.py`,
`projection.py`, and the current `rule.form1040-line16.json` (v1) content.

Data safety: no real personal values or workspace paths found in either
design or examination document; all amounts/parameters are synthetic
(`demo-*`), consistent with ADR-0031.

---

## D2-P1 — Declared-absence fact types (ADR-0036 pattern)

**IT1 — sufficient.** Two `fact-type.v2` citizens, `value_schema` categorical
`{yes,no}` (never boolean), no `optional_default`, presence-before-value
stated explicitly (ADR-0036 PC2), unconditional `input` pins on the final
worksheet rule. Matches the ratified pattern exactly; contributed via
ADR-0032 unchanged.

**IT2 — sufficient, with an added machinery layer.** Same categorical `{yes,
no}` fact types, same presence-not-truthiness framing. IT2 additionally
interposes two derived "certificate" rules (categorical assertion → literal
`true`) between the declaration and the worksheet, and pins the worksheet to
the certificates rather than to the declarations directly. Checked against
`projection.py` (`_DEPENDENCY_ROLES = {input, choice}`, "edges chain through
derived-on-derived") and precedent in committed content
(`rule.form1040-line2b.json` pins another rule's derived subtotal with
`role: input, origin: assertion`) — a two-hop input-pin chain is an
established, conforming pattern; it does not add a third edge kind and does
not weaken displacement (Article 7).

**G1 (non-blocking).** IT2's certificate rules state that "a `yes` answer
makes its certificate inapplicable; an absent answer blocks its certificate"
and claims these "distinguish the two outcomes," but the design never states
distinct block codes/dispositions for the two cases. As specified, both a
`yes` declaration and a missing declaration collapse to "certificate not
current," which risks the worksheet reporting `DEPENDENCY_ABSENT` for both —
conflating a *complete, out-of-scope* answer with *factual incompleteness*.
This is the same shape of hazard ADR-0036 rejected in its own incumbent
(masking one Part III answer's disposition behind another), though IT2's
design does not go as far as that rejected alternative and the plan's
mandatory case 3 (missing-only) is still satisfied on its own terms. IT1
avoids this by naming `DECLARATION_OUT_OF_SCOPE` distinctly from
`DEPENDENCY_ABSENT`. Recommend IT2 name the two dispositions explicitly if
carried forward.

---

## D2-P2 — Worksheet ladder, reduction property, supersession posture

**Ladder expressibility — sufficient for both**, verified directly against
`evaluator.py`: `add`, `subtract`, `max`, `compare`, `choose`, `bracket_fold`,
`round` are all present; no `min` and no bare `multiply` op exists (confirmed
by the op dispatch table), so both designs' `min` encodings are required, not
optional, and both are algebraically correct — IT1's
`choose(when: compare(a,b,lte), then:a, else:b)`, IT2's `a - max(0,a-b)`.
`bracket_fold`'s implementation (`(top-lower)*rate` per band) supports both
designs' use of single-band parameter tables to realize the 15%/20% rate
multiplications without a multiply op. Rung-2 probe (a) was correctly not
consumed by either.

**Reduction property algebra — sufficient for both**, mechanically checked:
both correctly show `Q=0 ⇒` all preferential portions collapse to 0 and the
worksheet total equals the existing ordinary bracket computation.

**Supersession posture — this is where the two designs conflict, and
neither is fully sufficient as written.**

**G2 (decision-blocking — IT2).** IT2's conditional-selector posture rests
on the package's `conflict_semantics` mechanism to let two rules
(`form1040-line16` v2, guarded `Q==0`; `form1040-line16-qdcg` v1, guarded
`Q>0`) publish the same symbol, claiming the package "validates the guards
as exhaustive and disjoint" so "the runner's published-output protection
... never selects tax policy by traversal order." This is not what the
committed contract provides. `artifact-package.v2.schema.json`'s
`conflict_semantics` is `{symbol, selected_producer}` — one **static**
member reference per symbol. `package_validation.py:417-419` confirms the
validator only checks that a single named `selected_producer` exists among
package members when a form-field's bound symbol has multiple producers;
there is no guard-exhaustiveness or guard-disjointness validation anywhere
in `package_validation.py` or `runner.py`, and no runtime dispatch that
picks between two same-symbol producers per return based on `when`
evaluation. As designed, `conflict_semantics` cannot express "publish from
whichever of these two rules' guards is satisfied for this return" — it
resolves package-authoring-time ambiguity to one fixed producer, full stop.
This is exactly the kind of claim Rung-1 requires be **cited from contract
text**, not asserted; the citation given does not support the claimed
behavior. Per the charter's own stop condition ("If a design needs a
contract change you cannot represent as a versioned schema/canon diff on
paper, stop and report"), this needed either Rung-2 probe (a) or an honest
unrepresentable-as-designed report — not a "settled at Rung 1" verdict.
Plan Gate 5 marks the supersession posture decision-blocking; this finding
applies there.

**G3 (decision-blocking — IT1).** IT1's chosen posture — one v2 successor
rule, unique symbol ownership (ADR-0006 D7's default, exactly the shape of
every existing rule in `packages/content/tax/2025/`) — is representationally
sound and requires no unverified mechanism. However, IT1's final rule
`requires` **unconditionally** lists both capital-gain declarations for
*every* return, not only returns with dividend income. The design's own
reduction-property proof (`§D2-P2`) only goes through once both declarations
are current and bound to `"no"`; it does not address the case where the
declarations were never contributed at all (a genuine wages-only return).
As specified, such a return would block on line 16 pending two new
declarations about capital-gain distributions and Schedule D that have no
possible bearing on it. Line 3a's dividend family is already
`require_closed` on every return (ADR-0035 D2), so this is incremental to an
existing universal-closure gesture rather than a wholly new UX class — the
finding is therefore about the *design's own justification*, not a novel
constitutional breach: IT1's table argues its posture wins on "anti-wizard"
and "honest-blocking" grounds without addressing that its `requires` clause
imposes the same two declarations on returns definitionally outside the
worksheet's scope, which is in tension with the charter's own framing ("line
16 ... correct for a wages-and-interest return"). IT2's conditional-selector
answer to this same question is structurally better (Q=0 returns need no
capital-gain declarations at all, per its case 2) but is undermined by G2.
Plan Gate 5 marks the supersession posture decision-blocking; this finding
applies there too.

**Net for P2:** ladder and reduction are settled at Rung 1 for both designs.
Supersession posture is **not settled** for either as currently written —
IT1 conforms to ratified unique-ownership/versioning mechanics (Article 9,
ADR-0006 D7) but its `requires` scope needs justification or narrowing; IT2
correctly targets the honest-blocking concern IT1 leaves open but cites a
package mechanism that does not do what the design says it does. Neither
should be accepted on the supersession question without repair.

---

## D2-P3 — Bidirectional contradiction mechanism

**Both — sufficient.** Both name "admission-locus mutual exclusion" as the
mechanism, structurally identical to ADR-0035's ratified 1b≤1a subset
invariant: after per-finding `value_schema` validation, before state
mutation, fail-closed on contribution. Both correctly cover all three
temporal cases (declaration-then-statement, statement-then-declaration,
same-batch) and both correctly state the resulting hard error prevents any
state where a `"no"` declaration and a current `CAPITAL_GAIN_DISTRIBUTION_RECORDED`
signal (box_2a ≠ null) coexist — satisfying "by construction, not policy"
and Article 7's "no third edge" foreclosure (the check gates admission; it
does not add a displacement edge). Both correctly reject currency-only and
derivation-time-only alternatives for permitting a transient both-current
window, matching the charter's binding ruling.

**G4 (non-blocking — schema-as-canon distinction, informational).** IT1
implements the mechanism as new admission-time validation logic reusing the
already-ratified ADR-0035 check pattern — no new package-member schema kind
is proposed. IT2 proposes a new adopted citizen, `admission-constraint.v1`,
not currently in `artifact-package.v2`'s `admitted_schemas` enum. Proposing
a new schema before any instance of it exists is consistent with Article 10
("if it is in the workspace, its schema was there first") at paper stage,
and IT2 states it plainly as new contract, not implemented — so this is not
a violation. It is, however, materially more machinery for Track 2/3 to
build and ratify than IT1's reuse of the existing check family. Foreman
triage may weigh this as a build-cost consideration; it is not a governance
defect on either side.

**Case 6 (no reach-around) — sufficient for both.** Verified against
`evaluator.py`/schema: no worksheet expression in either design references
`CAPITAL_GAIN_DISTRIBUTION_RECORDED`, a recorded-boxes fact type, or a
box-2a `collect`. Both correctly rely on ADR-0035's runtime universe guard
and package validation to make this unrepresentable rather than merely
untested, and both correctly restrict the contradiction check to consuming
the ADR-0035 signal rather than reading box 2a directly — the design
respects the recorded-non-composable universe (measurement 7) in both
cases.

---

## Summary table

| Proposition | IT1 | IT2 |
|---|---|---|
| D2-P1 (declared-absence pattern) | Sufficient | Sufficient (G1 non-blocking) |
| D2-P2 — ladder + reduction | Sufficient | Sufficient |
| D2-P2 — supersession posture | **Not settled (G3, decision-blocking)** | **Not settled (G2, decision-blocking)** |
| D2-P3 (bidirectional contradiction) | Sufficient (G4 informational) | Sufficient (G4 informational) |

## Findings index

- **G1 — decision-blocking (IT2, P2).** `conflict_semantics` is a static
  `{symbol, selected_producer}` package mechanism (confirmed in
  `artifact-package.v2.schema.json` and `package_validation.py:417-419`);
  it does not support IT2's claimed per-return dynamic dispatch between two
  guarded same-symbol producers. The design's "settled at Rung 1" verdict on
  supersession posture is not supported by the contract text it cites.
- **G2 — decision-blocking (IT1, P2).** The single-successor rule's
  `requires` clause unconditionally demands both capital-gain declarations
  on every return, including returns with no dividend income at all; the
  design does not justify or narrow this against its own anti-wizard/
  honest-blocking argument.
- **G3 — non-blocking (IT2, P1/P3).** Certificate mechanism does not specify
  distinct block dispositions for a `yes` declaration vs. a missing
  declaration; recommend explicit disposition naming if carried forward.
- **G4 — informational/out-of-scope-reroute (IT2, P3).** New
  `admission-constraint.v1` citizen is schema-compliant to propose at paper
  stage but represents materially more new machinery than IT1's reuse of
  the ADR-0035 check pattern; a build-cost note for foreman triage, not a
  governance defect.

No finding concerns D2-P1's fact-type conformance or D2-P3's bidirectional
mechanism/universe-guard conformance in either design — both are sufficient
there. The open decision-blocking ground is confined to D2-P2's supersession
posture, where both designs have a real defect and neither should be
adopted as written without repair (IT1: narrow or justify the `requires`
scope; IT2: replace the `conflict_semantics` claim with a mechanism the
runner actually supports, or escalate to Rung 2 / report unrepresentable).
