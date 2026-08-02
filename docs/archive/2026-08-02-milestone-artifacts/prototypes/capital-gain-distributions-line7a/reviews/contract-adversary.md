# Contract / Adversary Review — Capital-Gain Distributions and Line 7a

Reviewer seat: Contract/adversary, High capability / high effort.
Charter:
`docs/archive/2026-08-02-milestone-artifacts/prototypes/capital-gain-distributions-line7a/charter-review-contract-adversary.md`.
Date: 2026-07-29.

---

## 1 — Review-object verification and independence attestation

### Review objects

| Label | Commit | Artifacts |
| --- | --- | --- |
| **Incumbent (it1)** | `1a7530faa68cd382f5216e2a4f1373416632a3ae` | `it1/design.md`, `it1/examination.md` |
| **Rival (it2)** | `099882e` (tip of `prototypes/capital-gain-distributions-line7a/it2`) | `it2/design.md`, `it2/examination.md` |

Both artifact sets were read at the above commits via `git show` (it1) and the
current working tree (it2). The plan (`plan.md`), both Builder charters
(`charter-it1.md`, `charter-it2.md`), and the review charter
(`charter-review-contract-adversary.md`) are verified at these commits.

### Independence attestation

I did not read the foreman's early incumbent check, either Builder's thread,
any uncommitted artifact, the expressiveness review, or any material outside
the committed artifacts enumerated above. No independence breach occurred.

### Envelope scans

```
python3 tools/envelope_scan.py --range origin/main..099882e          # clean
python3 tools/envelope_scan.py --range origin/main..1a7530faa68c…   # clean
```

Both scans returned clean (no personal data, no real values, no workspace
locations).

---

## 2 — Attack table

Each cell records the attack outcome (✓ survives, ✗ fails, ⚠ partial/noted)
and a compact citation. Rows are the charter's ten mandatory cross-products.

| # | Shared case | Criterion | it1 (conclusion) | it2 (component) |
| --- | --- | --- | --- | --- |
| 1 | Eligible single payer | Case 1 concrete, pins exact | ✓ S3.1 guard fires, line 7a = 400, all pins named (members, closure, SDR finding, citations). | ✓ Eligibility guard fires on 3 component facts + SDR checked conclusion, line 7a = 400, all pins named. |
| 2 | Eligible multiple payers | Case 2 concrete, subtotal correct | ✓ 2a-subtotal = 550, line 7a = 550, line 9 adds once, QDCG base = Q + 550. Pins include both members. | ✓ Same arithmetic, same pin discipline. Component guard requires both component facts current. |
| 3 | Authority missing (M1) | Line 7a blocked; walk names missing facts | ✓ Missing `schedule-d-required` → line 7a blocked with named walk `tax.us.2025.schedule-d-required`. No zero, no inference. | ✓ Missing any of the 3 components → line 7a blocked with walk naming the absent component. SDR checked conclusion also absent (no components → no conclusion). |
| 4 | Schedule D required (M4) | `guard_inapplicable`; no attachment | ✓ `schedule-d-required = "yes"` → `guard_inapplicable`; no line 7a publication, no Schedule D artifact. Clean. | ✓ SDR checked conclusion resolves `"yes"` → `guard_inapplicable`. Same posture. |
| 5 | Contradiction (M5) | Both orders + same-batch | ✓ Traces declaration-first, statement-first, same-batch; admission-locus rejection in all three; references loader.py `DECLARATION_SIGNAL_CONTRADICTIONS`. Mechanism unchanged from ADR-0038. | ✓ Same contradiction mechanism — the interlock is on `capital-gain-distributions` vs `CAPITAL_GAIN_DISTRIBUTION_RECORDED`, which both designs preserve identically since the signal source migrates to successor members identically. |
| 6 | Authority correction (M6) | Both directions; displacement cascades | ✓ SDR correction `"no"` → `"yes"` via free supersession: old SDR finding displaced, line 7a displaced (input edge), line 9/16 cascade. Reverse `"yes"` → `"no"` re-enables guard. Pins trace. | ⚠ Component correction is traced for the 3 component facts + SDR conclusion. **Finding CA-F01**: the checked-conclusion derivation from components introduces a derived intermediate; correction of one component displaces the conclusion, which displaces line 7a. The cascade is longer but remains structurally sound under ADR-0010. The extra derivation layer is noted but not a failure. |
| 7 | Family states (M7) | Closed-empty, open, undeclared, stale, corrected, removed | ✓ Case 3 (closed-empty → line 7a = 0), Case 7 sub-cases (open → blocked, undeclared → blocked, stale → blocked, corrected amount → same-horizon re-collect, removed member → horizon advance + stale → blocked). All concrete with demo-finding IDs. | ✓ Same family behavior — P2 is identical between the two designs. Family mechanics do not depend on the authority topology. All sub-cases traced. |
| 8 | Mixed-graph / reach-around (M8) | Historical + successor can't both be live | ✓ S2.7 exclusivity: package graph carrying both v1 `recorded-boxes` field `"2a"` consumers and v2 `box2a-capital-gain-distributions` family collectors → rejected at package resolution. Universe guard extended to successor. | ✓ Same S2.7 exclusivity rule. Component topology does not change the family-level guard. |
| 9 | Double-count / direct-read (M9) | Line 9 counts once; QDCG never reads raw | ✓ S3.3 adds `line7a-total` exactly once. S3.5 rejects rule graphs that ref raw box-2a members from line 9/16. Package validation enforces. | ✓ Same downstream — identical P3 sentences on the line-9/QDCG path. |
| 10 | Qualified-zero neighbor (M10) | Q = 0 reduces correctly | ✓ Case 10: `conditional_dependency_set` condition `Q > 0` is false → declarations not demanded → line 16 reduces to ordinary bracket fold. CG addend absent from worksheet (literally 0 or not demanded). | ✓ Same conditional_dependency_set behavior; when Q = 0, component facts and SDR are not demanded. Reduction property preserved. |

### Cross-product attacks (charter-required)

| Cross-product | it1 | it2 |
| --- | --- | --- |
| Authority missing × closed/open/stale box-2a | ✓ Blocked on authority regardless of family state. Family state independently blocks or not; both conditions must be met. | ✓ Same — component absence blocks authority resolution independently. |
| Q = 0 × missing authority | ✓ Line 16 does not demand authority (CDS false-reduction). Line 7a still blocked but line 16 is independently satisfied via ordinary path. | ✓ Same. |
| Q = 0 × Schedule D required | ✓ Line 16 ordinary path; line 7a `guard_inapplicable`. Both correct. | ✓ Same. |
| Zero-valued box 2a × contradiction signal | ✓ A present box-2a member with amount 0 is still a **present member** — the `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal fires from non-null `"2a"` (ADR-0035). Contradiction interlock with `CGD = "no"` still triggers. Correctly traced. | ✓ Same — the signal is presence-based, not value-based. Both designs correctly note this. |
| Forward auth correction + full cascade | ✓ SDR `"no"` → `"yes"`: line 7a displaced, line 9 displaced, TI displaced, line 16 displaced. All re-derive on new authority. | ✓ Component → conclusion → line 7a: one extra derivation hop but same cascade completeness. |
| Reverse auth correction + full cascade | ✓ SDR `"yes"` → `"no"`: line 7a re-publishes. Cascade valid. | ✓ Same after conclusion re-derives. |
| Mixed historical/successor workspace | ✓ Package resolution rejects. | ✓ Same. |

---

## 3 — Findings

### CA-F01 — it2 checked-conclusion derivation adds an extra displacement hop

- **Proposition:** P1
- **Design:** it2 (component-backed)
- **Evidence:** it2 design §1, examined in it2 examination P1 item 3.
- **Description:** The rival introduces three component-level eligibility
  assertions (`no-1099b`, `no-capital-loss-carryover`,
  `only-capital-gains-box-2a`) and derives `schedule-d-required` as a
  **checked conclusion** from their conjunction. This adds a derived
  intermediate finding between the contributed components and the line-7a
  guard. Under ADR-0010, correction of any component displaces the
  conclusion, which displaces line 7a, creating a **three-hop** displacement
  chain (component → conclusion → line 7a → line 9/16) versus the
  incumbent's **two-hop** chain (SDR → line 7a → line 9/16).
- **Assessment:** Structurally sound under ADR-0010. The extra hop is a
  **topology cost**, not a contract violation. No stale result survives
  correction. However, the cost is real: three contributed facts must all be
  current and correct for the conclusion to publish, and the displacement
  blast radius is wider (any one component correction cascades through the
  entire line-7a → line-9 → line-16 chain).
- **Gate-5 recommendation:** Observation (informational). Not a defect.

### CA-F02 — it2 checked conclusion inverts the presence-before-value discipline

- **Proposition:** P1
- **Design:** it2 (component-backed)
- **Evidence:** ADR-0038 decision 1; it2 design §1 sentences S1.2–S1.4.
- **Description:** ADR-0038 decision 1 establishes `schedule-d-required` as a
  contributed categorical fact with domain `{yes, no}`, no default, and
  **presence-before-value** discipline. The rival design reinterprets this
  fact type as a **derived conclusion** whose presence depends on three
  component facts being current. This means `schedule-d-required` is no
  longer owner-contributed through ADR-0032's contribution boundary — it is
  machine-derived.

  The rival's examination P1 acknowledges this and argues the successor
  contract would replace ADR-0038's definition with a new one where SDR is
  a checked conclusion. However, this is a **semantic weakening** of the
  accepted contract: ADR-0038 decision 1 specifically established these
  facts as owner-declared-absence assertions under the ADR-0036 categorical
  pattern. The rival does not propose superseding ADR-0038; it proposes a
  successor version of the fact type that changes its nature from
  contributed to derived.
- **Assessment:** The rival's approach is internally consistent and the
  examination acknowledges the departure. The charter's measurement 1
  ("accepted history is edited or semantically weakened instead of extended
  by an explicit successor") is triggered if the successor is not framed as
  an **explicit replacement** of the ADR-0038 contract sentence. The rival
  design does frame it as a successor version; whether this framing is
  sufficient for the ADR to adopt is a **plan question**, not a design
  defect.
- **Gate-5 recommendation:** Plan-question (for the foreman and owner).
  The design is not defective but the authority departure from ADR-0038
  decision 1 requires an explicit owner/ADR disposition. Rung-1 paper
  cannot resolve this.

### CA-F03 — it2 component-fact necessity is unproven at Rung 1

- **Proposition:** P1
- **Design:** it2 (component-backed)
- **Evidence:** it2 charter constraint "Do not reward extra component facts
  merely for being finer grained. Measure whether each is necessary
  authority."
- **Description:** The rival introduces three component facts:
  `no-1099b-received`, `no-capital-loss-carryover`, and
  `only-capital-gains-are-box-2a`. The charter requires measuring whether
  each is **necessary** authority. At Rung 1 (paper), the rival states
  these are the three conditions from the 2025 Form 1040 line-7a
  instruction that determine direct-route eligibility. The rival's
  examination P1 declares the necessity is grounded in the IRS instruction
  text.

  However, the necessity argument is **external** (IRS instruction text) not
  **endogenous** (required by the engine's contract system). The incumbent
  achieves the same declared effect with a single contributed assertion.
  The rival's three facts are finer-grained but the paper evidence does not
  show a failure mode of the incumbent that the component facts prevent —
  the only correctness the components add is making the owner unable to
  answer `"no"` to `schedule-d-required` when they should have answered
  `"yes"`, which is a **contribution discipline** question (the owner's
  honesty) not an engine authority question.
- **Assessment:** The rival honestly states the topology cost (+3 fact
  types, +1 derived conclusion). The plan's decision inventory
  intentionally tests both topologies. This finding does not invalidate the
  rival; it records that the necessity of component facts is **not resolved
  by Rung-1 paper evidence** and requires a policy/owner decision.
- **Gate-5 recommendation:** Plan-question (for the foreman and owner).

### CA-F04 — it1 relies on owner honesty for direct-route correctness

- **Proposition:** P1
- **Design:** it1 (conclusion-level)
- **Evidence:** it1 design §1 S1.1, S1.5; it1 examination P1 unresolved
  question.
- **Description:** The incumbent's sole authority for the direct route is
  the owner's contributed `schedule-d-required = "no"`. The design
  explicitly acknowledges (S1.5 and the examination) that the engine does
  not verify whether Schedule D is actually not required — it trusts the
  owner's declaration. If the owner incorrectly answers `"no"` when they
  have a 1099-B, capital loss carryover, or non-box-2a capital gains, the
  engine will incorrectly publish a direct-route line 7a.

  This is **by design** for the conclusion-level topology: the incumbent
  argues that the owner's declaration is an ADR-0032 contribution like any
  other, and that validating the answer's correctness against external
  documents is outside the engine's current scope.
- **Assessment:** The incumbent is honest about the reliance. The plan
  explicitly tests both topologies to evaluate whether this is acceptable.
  The reliance is a **topology characteristic**, not a contract violation.
  It mirrors how the engine handles other contributed declarations (e.g.,
  `capital-gain-distributions`).
- **Gate-5 recommendation:** Observation (topology-distinguishing, not a
  defect).

### CA-F05 — Both designs: P2 family promotion is substantively identical

- **Proposition:** P2
- **Design:** Both
- **Evidence:** it1 design §3 S2.1–S2.8; it2 design §3 S2.1–S2.8.
- **Description:** Both designs propose the same box-2a family promotion:
  - New fact type `tax.us.2025.f1099div.box2a-capital-gain-distributions`
    @ v1 with the same identity keys as 1a/1b.
  - New family `tax.us.2025.f1099div.2a` @ v1 with its own horizon and
    closure.
  - Successor `dividend-universe.v2` promoting 2a to composable.
  - Successor `recorded-boxes` @ v2 dropping field `"2a"`.
  - `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal migrated to successor
    members.
  - Package exclusivity guard (S2.7) preventing mixed representations.
  - Contradiction interlock preserved.

  The P2 sentences are byte-for-byte substantively identical across both
  designs. This is expected: P2 is about family mechanics, not authority
  topology.
- **Assessment:** Both P2 designs survive all ten cases. No finding against
  either.
- **Gate-5 recommendation:** No finding.

### CA-F06 — Both designs: P3 handoff is substantively identical

- **Proposition:** P3
- **Design:** Both
- **Evidence:** it1 design §3 S3.1–S3.6; it2 design §3 S3.1–S3.6.
- **Description:** Both propose the same declared binding path: line 7a
  rule → line 9 v3 (adds line7a-total once) → line 16 v3 (QDCG
  preferential base = Q + line7a-total). Guard structure, conditional
  dependency set expansion, citation paths, and package validation are
  identical.

  The only difference is that the it2 line-7a guard consumes the derived
  SDR conclusion instead of the contributed SDR declaration — a P1
  difference manifested in P3.
- **Assessment:** Both P3 designs survive all ten cases. The guard-input
  difference is a P1 consequence, already captured in CA-F01 and CA-F02.
- **Gate-5 recommendation:** No separate finding.

### CA-F07 — it2 component fact `only-capital-gains-are-box-2a` couples the authority to future source families

- **Proposition:** P1
- **Design:** it2 (component-backed)
- **Evidence:** it2 design §1 S1.3; plan non-goals.
- **Description:** The rival's third component fact,
  `only-capital-gains-are-box-2a`, asserts that the taxpayer's capital gains
  consist only of box-2a amounts. If a future milestone introduces another
  capital-gain source family (e.g., Form 8949 short-term gains), this
  component's domain and semantics must expand or be superseded. The
  milestone plan explicitly lists "other capital-gain source families"
  as a non-goal.

  The incumbent avoids this coupling: `schedule-d-required` is a conclusion
  that does not enumerate its reasons, so a future source family would
  simply change the owner's answer from `"no"` to `"yes"` without a
  contract revision.
- **Assessment:** This is a legitimate **topology cost** of the component
  approach. The rival acknowledges it in its examination. It is not a
  contract violation; it is a future-maintenance cost.
- **Gate-5 recommendation:** Observation (topology cost).

---

## 4 — Proposition sufficiency

### P1 — Direct-route authority

| Design | Sufficiency | Rationale |
| --- | --- | --- |
| it1 (conclusion) | **Sufficient at Rung 1** | All ten cases traced with exact findings, pins, and states. Authority topology is simple, owner-honest, and structurally complete. The topology's reliance on owner honesty is acknowledged and intentional (CA-F04). No accepted contract is violated. |
| it2 (component) | **Sufficient at Rung 1 with plan-questions** | All ten cases traced. The checked-conclusion departure from ADR-0038's contributed-fact pattern (CA-F02) and component necessity (CA-F03) are plan-questions, not paper defects. The design is internally consistent. |

### P2 — Box-2a family promotion

| Design | Sufficiency | Rationale |
| --- | --- | --- |
| it1 | **Sufficient at Rung 1** | Identical P2 sentences survive all cases. |
| it2 | **Sufficient at Rung 1** | Same. |

### P3 — Line 7a and QDCG handoff

| Design | Sufficiency | Rationale |
| --- | --- | --- |
| it1 | **Sufficient at Rung 1** | Line 7a → line 9 → line 16 chain fully traced with pins and citations. |
| it2 | **Sufficient at Rung 1** | Same, with the guard-input difference attributable to P1. |

---

## 5 — Does paper distinguish the authority topologies?

**Yes.** The two topologies are distinguishable at Rung 1 on exactly one axis:

- **Correction blast radius (CA-F01):** The component topology introduces a
  three-hop displacement chain versus the incumbent's two-hop chain. Both are
  correct under ADR-0010, but the component topology's correction cascade
  is wider.
- **Contract departure (CA-F02):** The component topology changes
  `schedule-d-required` from a contributed fact (ADR-0038 decision 1) to a
  derived conclusion. This is a policy-level difference that paper reveals
  but cannot resolve.
- **Necessity (CA-F03 vs CA-F04):** Paper exposes the trade-off (component
  necessity vs owner honesty) but cannot prove which is correct. This is the
  plan's intended Rung-2 or owner-disposition question.
- **Future coupling (CA-F07):** The component topology binds to the current
  capital-gain source inventory; the conclusion topology does not.

Paper sufficiency is achieved: the topologies are structurally distinct and
their trade-offs are visible. The plan's decision between them is an owner/ADR
question, not a Rung-1 evidence gap.

---

## 6 — Is the plan's single Rung-2 validator question still genuinely open?

The plan identifies one Rung-2 question: **whether a validator probe can
show that the conclusion-level topology permits an incorrect direct-route
publication that the component topology prevents.**

This question **remains genuinely open.** At Rung 1, both designs correctly
handle all ten cases. The difference between them is a policy trade-off
(owner honesty vs. component verification) that paper evidence cannot
resolve. A Rung-2 probe could test whether a deliberately incorrect
`schedule-d-required = "no"` (when a 1099-B exists in the workspace) leads
to a publishable direct route under the incumbent but is blocked under the
rival. This probe would distinguish the topologies empirically.

However, this reviewer notes that such a probe would test the **contribution
discipline boundary** (what the owner is allowed to assert) rather than the
**engine contract** (whether the engine correctly processes what the owner
asserts). Both designs correctly process their inputs; the question is
whether the engine should validate the owner's declaration against other
evidence. This framing should be explicit in any Rung-2 charter.

---

## 7 — Verdict

Both designs are **internally consistent**, survive all ten mandatory cases,
preserve all accepted contracts, maintain immutability of published
schemas/content, and produce clean envelope scans.

Neither design has a contract-level failure. The differences are:

1. **CA-F02/CA-F03** (plan-questions): The component topology's departure from
   ADR-0038's contributed-fact pattern requires an owner/ADR disposition.
2. **CA-F01/CA-F04/CA-F07** (observations): The topologies have different costs
   (displacement hops, owner reliance, future coupling) that are visible at
   Rung 1 but not resolvable.

### Recommendation

**READY** — both designs are ready for Gate-5 disposition by the foreman and
owner. P1, P2, and P3 are all sufficient at Rung 1 for both designs. The
plan-questions (CA-F02, CA-F03) require owner disposition but do not block
the milestone's progression through the review gate.
