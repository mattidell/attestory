# Design — Iteration 1: Nested-Identity, Synthesized-Conclusion Incumbent

Builder, Rung 1 (static paper instantiation only). Source ref
`prototypes/schedule-d-covered-ltcg-8a/it1`. This document is a contract
design, not implementation pseudocode: every successor sentence is stated
precisely enough for a later ADR to adopt or reject it verbatim. All facts,
identities, amounts, and pins below use `demo.*`/`demo-*` synthetic values
only.

---

## P1 — Transaction source family and identity

### Topology

P1 extends the statement-instance pattern (ADR-0015) one level deeper,
mirroring the two existing nested-member-under-statement precedents:
`family.form1065-k1-box5.json` (K-1 box 5 interest) and
`family.f1099int-b10.json` (1099-INT box 10 market discount). Both existing
precedents key a member fact to `{payer-or-partnership(entity),
statement(entity), tax-year(literal)}`. P1 needs one additional identity
component — the transaction itself is not the statement, it is a member
*within* the statement, so the member fact type must carry a fourth identity
key.

**Member fact type** `tax.us.2025.f1099b.covered-ltcg-txn` (new, `.v1`):

```json
{
  "schema": "fact-type.v2",
  "id": "tax.us.2025.f1099b.covered-ltcg-txn",
  "version": "v1",
  "identity_keys": [
    { "name": "broker", "kind": "entity" },
    { "name": "statement", "kind": "entity" },
    { "name": "transaction", "kind": "entity" },
    { "name": "tax-year", "kind": "literal" }
  ],
  "value_shape": {
    "proceeds": "amount",
    "basis": "amount",
    "basis_reported_to_irs": "categorical(yes,no)",
    "long_term_reported": "categorical(yes,no)",
    "adjustment_code_present": "categorical(yes,no)"
  },
  "supersession": "free"
}
```

`statement` is the logical 1099-B statement identity (peer to ADR-0015's
statement instance — never a file/upload/scan id). `transaction` is the
logical transaction identity *within* that statement. Two transactions
reported on the same statement are two distinct `transaction` identities
under the same `statement`; a correction to one transaction re-asserts the
same `{broker, statement, transaction, tax-year}` tuple and free-supersedes
only that member, exactly as ADR-0015 lets a corrected copy supersede prior
findings without disturbing a separate original individuation.

**Family** `family.f1099b-covered-ltcg` (new, `.v1`), following
ADR-0016's declared-closure-claim/member-predicate/authorizes-subtotal shape:

```json
{
  "schema": "source-family.v1",
  "id": "family.f1099b-covered-ltcg",
  "version": "v1",
  "closure_claim": "every 1099-B transaction for tax year 2025 that is covered, basis-reported-to-the-IRS, long-term, gain-only, and free of box-1f/1g adjustment codes",
  "member_predicate": "long_term_reported = yes AND basis_reported_to_irs = yes AND adjustment_code_present = no AND proceeds >= basis",
  "authorizes_subtotal": "tax.us.2025.schedule-d.line8a-subtotal"
}
```

**Closure fact type** `tax.us.2025.f1099b.covered-ltcg-family.closure`
(new, `.v1`), family-horizon-keyed, mirroring the existing closure fact
shape used by K-1 box 5 and market discount:

```json
{
  "schema": "fact-type.v2",
  "id": "tax.us.2025.f1099b.covered-ltcg-family.closure",
  "version": "v1",
  "identity_keys": [
    { "name": "family-horizon", "kind": "entity" },
    { "name": "tax-year", "kind": "literal" }
  ],
  "value_shape": { "state": "categorical(open,closed-empty,closed-with-members,undeclared,stale)" },
  "supersession": "free"
}
```

**Closure mapping** `closure-mapping.f1099b-covered-ltcg` (new, `.v1`),
linking member ↔ family ↔ closure via `admission.condition:
current-literal-true`, exactly as the K-1 box-5 precedent does — this is
where the eligibility predicate (member_predicate above) is enforced as an
*admission* gate, not a downstream filter:

```json
{
  "schema": "source-closure-mapping.v2",
  "id": "closure-mapping.f1099b-covered-ltcg",
  "version": "v1",
  "member_fact_type": { "id": "tax.us.2025.f1099b.covered-ltcg-txn", "version": "v1" },
  "family": { "id": "family.f1099b-covered-ltcg", "version": "v1" },
  "closure_fact_type": { "id": "tax.us.2025.f1099b.covered-ltcg-family.closure", "version": "v1" },
  "admission": { "condition": "current-literal-true" }
}
```

A transaction that fails `member_predicate` (case 11 — non-covered or
carrying an adjustment code) is never admitted to
`family.f1099b-covered-ltcg`. It does not enter as a member and get
filtered later; it is structurally absent from `collect_members` over this
family from the moment it is contributed, exactly as ADR-0016 forecloses
using a narrow closure to authorize a broader claim.

**Subtotal rule** `rule.f1099b-covered-ltcg-subtotal` (new, `.v1`), using
`collect_members` over the family, mirroring `rule.form1065-k1-box5-subtotal.json`:

```json
{
  "op": "collect_members",
  "member_fact_type": { "id": "tax.us.2025.f1099b.covered-ltcg-txn", "version": "v1" },
  "source_family": { "id": "family.f1099b-covered-ltcg", "version": "v1" },
  "publishes": {
    "tax.us.2025.schedule-d.line8a-proceeds": "sum(proceeds)",
    "tax.us.2025.schedule-d.line8a-basis": "sum(basis)",
    "tax.us.2025.schedule-d.line8a-gain": "sum(proceeds) - sum(basis)"
  }
}
```

`require_closed` gates this rule exactly as ADR-0050's box-2a subtotal rule
gates on its own family closure: the rule cannot publish while
`tax.us.2025.f1099b.covered-ltcg-family.closure` is `open`, `undeclared`, or
`stale`.

★ Insight ─────────────────────────────────────
The reason the closure fact needs its own identity key (`family-horizon`)
distinct from the member's identity keys is the same reason ADR-0023
introduced horizon-keyed closure in the first place: closure is a claim
*about the whole family as of a moment*, not a property of any one member.
If closure were instead a field on the member fact, there would be no way
to express "I am asserting the universe of transactions is now closed" as
a single, supersedable, independently-timed statement — you'd have to
infer closure from the absence of new members, which is exactly the
`SOURCE_SET_OPEN` vs `SOURCE_SET_UNCLOSED` distinction ADR-0036 already
had to draw a hard line around.
─────────────────────────────────────────────────

### Concrete instances

All identities below use `demo.broker.*`, `demo.stmt.*`, `demo.txn.*`.
Tax year is `2025` throughout.

**Case 1 — eligible single broker, single transaction (positive).**
`{broker: demo.broker.alpha, statement: demo.stmt.alpha-2025, transaction: demo.txn.alpha-001, tax-year: 2025}`,
`proceeds: 12000.00`, `basis: 9000.00`, `basis_reported_to_irs: yes`,
`long_term_reported: yes`, `adjustment_code_present: no`. Admitted.
Family closure asserted `closed-with-members` for
`family-horizon: demo.horizon.f1099b-ltcg-2025`. Subtotal publishes
`line8a-gain = 3000.00`.

**Case 2 — eligible single broker, multiple transactions (positive).**
Same broker/statement as case 1, plus a second transaction
`demo.txn.alpha-002`: `proceeds: 5000.00`, `basis: 4000.00`, same
eligibility flags. Both admitted as distinct members under one statement.
Subtotal: `line8a-proceeds = 17000.00`, `line8a-basis = 13000.00`,
`line8a-gain = 4000.00`. This demonstrates two sales from one broker
remaining distinct members, per the charter's incumbent constraint.

**Case 3 — eligible multiple brokers.**
Add `{broker: demo.broker.beta, statement: demo.stmt.beta-2025,
transaction: demo.txn.beta-001, tax-year: 2025}`, `proceeds: 8000.00`,
`basis: 6000.00`. Three members total across two brokers, one family
(family identity is not broker-scoped — brokers are entities *within* the
member identity, not separate families). `line8a-gain = 6000.00`.

**Case 4 — transaction correction (mandatory negative/lifecycle).**
`demo.txn.alpha-001` is re-reported by the broker with corrected
`proceeds: 12500.00` (basis unchanged). The correction asserts the same
`{demo.broker.alpha, demo.stmt.alpha-2025, demo.txn.alpha-001, 2025}`
tuple and free-supersedes the prior finding for that member only.
`demo.txn.alpha-002` (distinct transaction identity) is untouched — its
prior value remains the current finding for its own identity. Post-
correction subtotal recomputes over current members:
`line8a-proceeds = 17500.00`, `line8a-gain = 4500.00`. **Displaced state:**
the pre-correction `proceeds: 12000.00` finding for `demo.txn.alpha-001`
remains queryable as history (free supersession does not delete), but
`collect_members` over the family reads only the current finding per
member — exactly one row per transaction identity, never both.

**Case 8 — family lifecycle (closed-empty, open, undeclared, stale-horizon).**
- *Undeclared:* no closure fact contributed yet for
  `demo.horizon.f1099b-ltcg-2025` — `collect_members` and the subtotal rule
  are both blocked, `DEPENDENCY_ABSENT` naming the closure fact type.
- *Open:* closure fact contributed with `state: open` — same block; the
  filer has not yet asserted the universe is complete.
- *Closed-empty:* closure fact `state: closed-empty`, zero members
  admitted. Subtotal publishes `line8a-gain = 0` (a closure-backed zero,
  not a fabricated one — same disposition category as ADR-0050's box-2a
  closed-empty path).
- *Stale-horizon:* a new tax-year-2025 amendment horizon opens after the
  original closure; the old closure fact's horizon no longer matches the
  live horizon token. `require_closed` reads this as not-currently-closed
  and blocks, `DEPENDENCY_ABSENT`, until a fresh closure is asserted
  against the live horizon.

**Case 9 — historical/raw-member reach-around attack (mandatory negative).**
An attempt to read `tax.us.2025.f1099b.covered-ltcg-txn` members directly
(bypassing `collect_members`/family closure) to assemble a gain total
before the family is closed, or to include a member whose current finding
has been superseded (reading the pre-correction `demo.txn.alpha-001`
value from case 4 instead of its current finding). Both are foreclosed by
construction: the subtotal rule's only sanctioned read path is
`collect_members` scoped to `source_family:
family.f1099b-covered-ltcg`, which is defined to read exactly the current
finding per admitted member and to require `require_closed`. There is no
contract that authorizes reading the member fact type outside that path
for Schedule D purposes — a rule attempting a bare `ref` to the member
fact type is not expressible in `rule-artifact.v3`'s admitted operand set
for this purpose without inventing an unaccepted `op`.

**Case 11 — non-covered/adjustment-code transaction rejected (mandatory
negative).** `demo.txn.gamma-001` on `demo.broker.gamma`'s statement
reports `basis_reported_to_irs: no` (non-covered). It is contributed as a
`tax.us.2025.f1099b.covered-ltcg-txn` fact but `member_predicate` evaluates
false at admission — it never becomes a member of
`family.f1099b-covered-ltcg`, so it is invisible to `collect_members` and
cannot contribute to `line8a-gain` under any closure state, including
closed-with-members. A second variant, `demo.txn.delta-001`, reports
`adjustment_code_present: yes` (box-1f/1g style adjustment) and is
rejected on the same admission gate.

### Producer → authority → consumer → failure map

| Stage | Contract |
|---|---|
| Producer | Broker-contributed `tax.us.2025.f1099b.covered-ltcg-txn` facts (per transaction), plus a filer/preparer-contributed closure fact for `tax.us.2025.f1099b.covered-ltcg-family.closure` |
| Authority | `family.f1099b-covered-ltcg` (closure claim + member predicate) via `closure-mapping.f1099b-covered-ltcg` — this is the sole authority for "which transactions count" |
| Consumer | `rule.f1099b-covered-ltcg-subtotal` (P1) → Schedule D attachment content (P3) → line 7a successor (P3) |
| Failure | `require_closed` blocks `DEPENDENCY_ABSENT` on open/undeclared/stale; admission gate silently excludes (not "fails" — a rejected transaction is not an error state, it is correctly outside the family) non-covered/adjusted transactions; correction failure mode is n/a — free supersession has no rejected state at this layer (contradiction interlock is a P2/P3 concern, not identity) |

### Accepted contracts consumed unchanged

- ADR-0015 (statement-instance identity): the `statement` identity key and
  its peer-to-evidence discipline are reused verbatim.
- ADR-0016 (source-family claim and composition): `closure_claim`,
  `member_predicate`, `authorizes_subtotal` shape reused verbatim; the
  admission-gate technique that keeps a narrow closure from authorizing a
  broader claim is reused, not reinterpreted.
- The K-1 box-5 and market-discount `source-closure-mapping.v2` pattern
  (`admission.condition: current-literal-true`) is reused verbatim as the
  mechanism binding member → family → closure.
- ADR-0023 (member-transition/horizon) horizon-keyed closure is reused
  verbatim for `family-horizon`.

### Proposed successor contract sentences

1. A new `fact-type.v2` instance `tax.us.2025.f1099b.covered-ltcg-txn.v1`
   is added, with a four-component identity key
   `{broker, statement, transaction, tax-year}` — this is additive; it
   does not alter any existing fact type's identity key shape, including
   the three-key statement-level pattern ADR-0015 established.
2. A new `source-family.v1` instance `family.f1099b-covered-ltcg.v1` and
   paired `source-closure-mapping.v2` instance
   `closure-mapping.f1099b-covered-ltcg.v1` are added, instantiating
   ADR-0016 without modification to that ADR's decision text.
3. Two sales from one broker are always distinct members; a correction
   supersedes only the corrected transaction's own identity tuple, never
   the statement's or a sibling transaction's. This sentence is a direct
   restatement of the charter's incumbent constraint as a contract
   obligation on any future implementation of this family.

### Production conditions

- The admission gate (`member_predicate`) must be implemented as a true
  admission filter (excluding non-conforming contributions from
  `collect_members`'s visible set), not a post-hoc validation that flags
  but still includes them — case 11 depends on this distinction.
- `family-horizon` tokens must be generated/rotated using the same
  mechanism already governing box-2a and K-1 horizons (ADR-0023), so a
  stale-horizon closure fails closed by construction rather than by a new,
  parallel staleness check.
- The subtotal rule's publishable symbols
  (`schedule-d.line8a-proceeds/basis/gain`) must be minted as new,
  unused symbols — they are not a reuse of any existing box-2a or K-1
  symbol name.

### Unresolved questions

- Whether `transaction` should itself decompose further (e.g., lot-level
  identity for partial-lot corrections) is out of scope for this
  milestone's supported source class (no taxpayer-side basis adjustment)
  and is not answered here — flagged as a future-slice question, not a
  P1 gap.
- Whether the admission gate belongs in the closure-mapping's `admission`
  block (as modeled above) or as a separate declared eligibility fact
  read by the mapping is a real implementation choice neither this
  paper spike nor the existing K-1/market-discount precedents needed to
  resolve, because neither of those families has a *rejecting* admission
  predicate this rich (they admit unconditionally). This is named as an
  open production condition, not resolved at Rung 1.

---

## P2 — Completeness-boundary declaration shape

### The heterogeneity problem

The milestone plan's nine-part boundary is not nine facts of the same
kind. Reading them against the existing repository primitives:

| # | Boundary condition | Kind |
|---|---|---|
| 1 | eligible LT family is closed | **closure state** of `family.f1099b-covered-ltcg` (open/closed-empty/closed-with-members/undeclared/stale) |
| 2 | box-2a family is closed empty | **existing accepted closure state** of `tax.us.2025.f1099div.2a` (ADR-0050 Decision 2) — not a new fact at all |
| 3 | no short-term transactions | **declared-absence categorical fact**, `{yes,no}`, ADR-0038 style |
| 4 | no current capital losses | declared-absence categorical fact |
| 5 | no inbound capital-loss carryovers | declared-absence categorical fact |
| 6 | no Form 8949 transactions/adjustments | declared-absence categorical fact |
| 7 | no other Schedule D sources (K-1 gains, 2439, 4684, 4797, 6252, 6781, 8824) | declared-absence categorical fact (one composite claim, not seven) |
| 8 | lines 18/19 special-rate sources absent | declared-absence categorical fact |
| 9 | no Form 1099-DA or QOF flow | declared-absence categorical fact |

Component 1 is a closure state, not a categorical yes/no answer — an open
or undeclared family is not "no," it is not yet answerable. Component 2 is
not a new fact at all; it is a citation into an already-accepted ADR-0050
closure state, consumed unchanged. Components 3–9 are seven genuine new
declared-absence categorical facts, matching ADR-0038's `{yes,no}`,
free-supersession, no-default pattern exactly.

★ Insight ─────────────────────────────────────
This is the exact tension the milestone plan flagged when it scored P2's
residual paper uncertainty at 2: "nine distinct absent-source claims of
different kinds ... is the widest completeness surface the project has
attempted." The existing `checked-conclusion-binding.v1` schema (built for
ADR-0050's C1–C4) was never asked to synthesize a closure *state* and a
categorical *answer* into one conclusion — its `components` array assumes
every component is a presence-checked categorical fact. Component 1 breaks
that assumption, which is why P2 cannot just add five more C-style
components to the existing binding; it needs a successor binding schema
with a typed component role.
─────────────────────────────────────────────────

### Topology

**Seven new declared-absence fact types** (mirroring
`qdcg.bundle.json`'s `capital-gain-distributions`/`schedule-d-required`
shape — categorical `{yes,no}`, free supersession, no default):

- `tax.us.2025.schedule-d-boundary.no-short-term`
- `tax.us.2025.schedule-d-boundary.no-current-losses`
- `tax.us.2025.schedule-d-boundary.no-loss-carryovers`
- `tax.us.2025.schedule-d-boundary.no-f8949-sources`
- `tax.us.2025.schedule-d-boundary.no-other-schedule-d-sources`
- `tax.us.2025.schedule-d-boundary.no-lines-18-19-sources`
- `tax.us.2025.schedule-d-boundary.no-f1099da-or-qof`

**Proposed successor schema** `checked-conclusion-binding.v2` (additive to
`.v1`, never in place): adds a `role` enum on each component —
`categorical_presence` (existing v1 behavior, unchanged) and
`family_closure_state` (new). For a `family_closure_state` component: the
component reads "present" once the referenced closure fact is contributed
at all; it reads as satisfying the "yes" side of the truth table when the
closure state is any *closed* variant (`closed-empty` or
`closed-with-members`); it reads as satisfying the "no" side when the
closure state is a value the boundary condition forbids (not applicable
here — closure has no forbidding value, only a not-yet-closed value); and
it is treated as **missing** (not "no") when the closure state is `open`,
`undeclared`, or `stale` — an open family is honestly unanswered, never
inferred violating.

**Binding instance** `schedule-d-boundary.conclusion-binding` (new,
`checked-conclusion-binding.v2`):

```json
{
  "schema": "checked-conclusion-binding.v2",
  "id": "schedule-d-boundary.conclusion-binding",
  "version": "v1",
  "components": [
    { "alias": "D1", "role": "family_closure_state", "fact_type": { "id": "tax.us.2025.f1099b.covered-ltcg-family.closure", "version": "v1" } },
    { "alias": "D2", "role": "family_closure_state", "fact_type": { "id": "tax.us.2025.f1099div.2a", "version": "v1" } },
    { "alias": "D3", "role": "categorical_presence", "fact_type": { "id": "tax.us.2025.schedule-d-boundary.no-short-term", "version": "v1" } },
    { "alias": "D4", "role": "categorical_presence", "fact_type": { "id": "tax.us.2025.schedule-d-boundary.no-current-losses", "version": "v1" } },
    { "alias": "D5", "role": "categorical_presence", "fact_type": { "id": "tax.us.2025.schedule-d-boundary.no-loss-carryovers", "version": "v1" } },
    { "alias": "D6", "role": "categorical_presence", "fact_type": { "id": "tax.us.2025.schedule-d-boundary.no-f8949-sources", "version": "v1" } },
    { "alias": "D7", "role": "categorical_presence", "fact_type": { "id": "tax.us.2025.schedule-d-boundary.no-other-schedule-d-sources", "version": "v1" } },
    { "alias": "D8", "role": "categorical_presence", "fact_type": { "id": "tax.us.2025.schedule-d-boundary.no-lines-18-19-sources", "version": "v1" } },
    { "alias": "D9", "role": "categorical_presence", "fact_type": { "id": "tax.us.2025.schedule-d-boundary.no-f1099da-or-qof", "version": "v1" } }
  ],
  "truth_table": {
    "all_present_all_satisfied": "complete",
    "all_present_any_violating": "incomplete",
    "any_missing": "blocked"
  },
  "direct_pin_boundary": { "conclusion_only": true }
}
```

Note the truth-table vocabulary is deliberately **not** ADR-0050's
`{yes,no}` — it is `{complete, incomplete}` with a `blocked` state, because
D3–D9 answering "yes" means the boundary condition is *satisfied*
(source is absent), the inverse polarity from ADR-0050's C1–C4 where "yes"
on a component meant an *exception applied*. Stating this polarity
difference explicitly is itself a successor obligation (see below) — a
future reader must not assume this binding's truth table reads like
ADR-0050's by analogy.

### Concrete instances

**Case 5 — completeness component missing, each of the nine, in turn
(mandatory negative, worked for all nine).** Baseline: all nine components
present and satisfied except the one under test.

1. D1 missing (family closure undeclared) → `blocked`,
   `DEPENDENCY_ABSENT` naming `D1`.
2. D2 missing (box-2a family still `open`) → `blocked`,
   `DEPENDENCY_ABSENT` naming `D2`. (Reuses ADR-0050's own closure states —
   this is the case that proves component 2 is not a new fact: the same
   `open` state that blocks ADR-0050's line 7a box-2a route also blocks
   this conclusion.)
3. D3 missing (`no-short-term` never contributed) → `blocked`,
   `DEPENDENCY_ABSENT` naming `D3`.
4. D4 missing → `blocked`, naming `D4`.
5. D5 missing → `blocked`, naming `D5`.
6. D6 missing → `blocked`, naming `D6`.
7. D7 missing → `blocked`, naming `D7`.
8. D8 missing → `blocked`, naming `D8`.
9. D9 missing → `blocked`, naming `D9`.

In every one of the nine, the conclusion is `blocked(DEPENDENCY_ABSENT)`
naming exactly the one missing component — never `incomplete`, never a
default `complete`. This is the presence-before-value, no-default
requirement made concrete nine separate ways.

**Case 5b — violating value present (two meaningful negatives).**
`D3` (`no-short-term`) is contributed with value `no` (a short-term
transaction genuinely exists) while D1, D2, D4–D9 are present and
satisfied → conclusion `incomplete`. Separately, `D7`
(`no-other-schedule-d-sources`) is contributed `no` (a K-1 capital gain
exists) with all else satisfied → conclusion `incomplete`. Both
demonstrate: a present violating source, not a missing one, produces
`incomplete` rather than `blocked` — the two failure modes are distinct
and must not be collapsed.

**Case 6 — box-2a present and nonzero (mandatory).** D2 reads `closed`
(specifically `closed-with-members`, box-2a subtotal `450.00` per
ADR-0050 Decision 2) — this still satisfies D2 under the
`family_closure_state` rule above (D2 only requires *closed*, any variant;
"closed empty" is the milestone's boundary condition #2, but the *binding
component* only needs closure to answer, while the P3 line-16/line-7a
routing layer is what actually branches on empty-vs-nonempty — see P3
below). All other components satisfied → P2 conclusion `complete`. This
is deliberate: P2's completeness boundary is about whether the source
*universe* is fully accounted, not about whether box-2a happens to be
zero — that distinction is load-bearing for P3's coexistence design.

**Case 7 — box-2a closed empty (mandatory, positive).** D2 reads
`closed-empty` → satisfies D2 → conclusion `complete` (all else
satisfied). Two positives for P2 overall: this case, and the case-1/2/3
baseline family instantiated above.

**Two positive instances:** (a) case 7 as stated; (b) the case-1 baseline
with D1 `closed-with-members` (gain `3000.00`), D2 `closed-empty`, D3–D9
all `yes` → `complete`.

**Lifecycle trace:** D7 is first undeclared (blocked, naming D7) → then
contributed `no` with a K-1 gain fact present (incomplete) → the K-1 gain
source is later corrected/withdrawn and D7 is re-asserted `yes` (free
supersession) → conclusion re-evaluates to `complete`, assuming D1–D6,
D8–D9 unchanged and satisfied throughout.

### Producer → authority → consumer → failure map

| Stage | Contract |
|---|---|
| Producer | Filer/preparer declared-absence facts (D3–D9); the two closure facts (D1 new, D2 already-accepted ADR-0050) |
| Authority | `schedule-d-boundary.conclusion-binding` (`checked-conclusion-binding.v2`) — sole synthesizer of the nine-part boundary into one conclusion |
| Consumer | P3's Schedule D attachment `completeness` block and the line-7a/line-16 successors, which read the conclusion, never the nine components directly |
| Failure | `blocked(DEPENDENCY_ABSENT)` naming every missing component (case 5); `incomplete` for any present violating component (case 5b), never inferred, never defaulted |

### Accepted contracts consumed unchanged

- ADR-0050 Decision 1's presence-before-value, no-default,
  `conditional_dependency_set`-driven blocked-naming pattern is reused
  verbatim as the mechanical shape (only the truth-table vocabulary and
  component-role typing are new).
- ADR-0050 Decision 2's box-2a closure states (`open`,
  `closed-empty`, `closed-with-members`, `undeclared`, `stale`) are read,
  never redefined — D2 is a citation into that existing closure fact, not
  a new fact.
- ADR-0038's declared-absence categorical `{yes,no}`, free-supersession,
  no-default fact shape is reused verbatim for D3–D9.

### Proposed successor contract sentences

Following ADR-0050 Decision 9's own supersession-table pattern:

| Accepted clause | Successor graph effect |
|---|---|
| `checked-conclusion-binding.v1`'s `components` array (implicitly all `categorical_presence`) | `checked-conclusion-binding.v2` adds an explicit `role` field, `categorical_presence` \| `family_closure_state`, additive — every existing `.v1` binding (including ADR-0050's own `schedule-d-required.conclusion-binding`) remains valid as-is with an implicit `categorical_presence` role; no existing binding is edited. |
| ADR-0050 Decision 1's `{yes,no}` truth-table vocabulary | Not superseded — reused unmodified for `schedule-d-required.conclusion`. `schedule-d-boundary.conclusion-binding` is a *new, independent* binding instance with its own `{complete,incomplete,blocked}` vocabulary; the two conclusions are never conflated and never read each other. |
| ADR-0050 Decision 2's box-2a closure states | Not superseded — cited by reference as component D2's `family_closure_state`, read-only. |

### Production conditions

- `checked-conclusion-binding.v2`'s `family_closure_state` role must
  define, at the schema level, exactly which closure states count as
  "closed" for truth-table purposes (`closed-empty` and
  `closed-with-members`) versus "missing" (`open`, `undeclared`,
  `stale`) — this cannot be left to per-rule interpretation, or two
  different rules could disagree about whether `stale` is missing or
  violating.
- The seven new D3–D9 fact types must ship as one `bundle.v2`
  (`schedule-d-boundary.bundle`), mirroring `qdcg.bundle.json`'s
  packaging of its two fact types together, so they version and release
  as one unit.

### Unresolved questions

- Whether `checked-conclusion-binding.v2` is the right locus for the
  closure/categorical heterogeneity, versus doing the D1/D2
  closure-to-categorical folding in a small upstream derivation rule and
  keeping the binding schema untouched at `.v1`, is not resolved here —
  both are paper-viable; this spike could not distinguish them without a
  rung-2 question about whether existing `.v1` binding consumers would
  need to change behavior under either choice (case citation: this
  question is the direct paper-spike analog of case 5's D1/D2 rows).
- Component 7 ("no other Schedule D sources, including K-1 gains, Forms
  2439, 4684, 4797, 6252, 6781, or 8824") is modeled here as one composite
  declared-absence fact rather than seven. Whether the milestone's real
  source data can honestly attest a single composite claim, or whether
  each named form needs its own component (making this ten or more
  components, not nine), is unresolved at Rung 1 and is named as a
  direct question for the owner/plan, since it changes the boundary's
  arity, not just its shape.

---

## P3 — Schedule D content and QDCG/line-16 binding (paper spike)

### Schedule D attachment content

Instantiated on the existing ADR-0036 `attachment-rule.v2` ontology,
following the Schedule B (`rule.attachment.schedule-b.v3.json`) precedent
directly:

```json
{
  "schema": "attachment-rule.v2",
  "id": "attachment.schedule-d",
  "version": "v1",
  "title": "Schedule D — Capital Gains and Losses (covered LT gain-only slice)",
  "scope": { "tax_year": 2025, "jurisdiction": "us", "family": "family.f1099b-covered-ltcg" },
  "attachment": { "authority": "irs", "form_id": "1040-schedule-d", "tax_year": 2025, "jurisdiction": "us" },
  "publishes": "tax.us.2025.schedule-d.line16",
  "itemizations": [
    {
      "part_id": "part-ii-line-8a",
      "label": "Line 8a — Totals for transactions reported on Form 1099-B, basis reported to IRS",
      "authority": { "kind": "single_family", "source_family": { "id": "family.f1099b-covered-ltcg", "version": "v1" } },
      "row_sets": [
        {
          "rows": { "op": "collect_members", "member_fact_type": { "id": "tax.us.2025.f1099b.covered-ltcg-txn", "version": "v1" }, "source_family": { "id": "family.f1099b-covered-ltcg", "version": "v1" } },
          "subtotal_symbol": "schedule-d.line8a-gain"
        }
      ],
      "tie_out": { "line_symbol": "schedule-d.line15" }
    }
  ],
  "completeness": {
    "required_answers": [
      { "symbol": "schedule-d-boundary.conclusion", "fact_type": { "id": "schedule-d-boundary.conclusion", "version": "v1" }, "check": "presence" }
    ]
  }
}
```

Line 15 (Part II net long-term gain) ties out to `line8a-gain` directly —
there is only one Part II source row set in this slice's scope (no
short-term, no other Part II lines, per the completeness boundary). Line
16 combines Part I (short-term, out of scope, structurally absent) and
Part II; within this slice's supported class, line 16 equals line 15.

### The threshold-vs-categorical schema gap

★ Insight ─────────────────────────────────────
`attachment-rule.v2`'s `requirement` block (read directly from
`packages/schemas/tax/attachment-rule.v2.schema.json`) is not optional
shape — `subtotals`, `threshold_parameter`, and `comparison: const
"strictly_greater_than"` are all `required`. That block was built for
Schedule B's actual rule ("is interest/dividend income over $1500"), a
genuine numeric threshold. Schedule D's "required" disposition is not a
threshold at all — it is the `schedule-d-required.conclusion` checked
conclusion (ADR-0050 Decision 1) or, in this milestone's boundary, the
`schedule-d-boundary` conclusion. There is no dollar amount to compare
against a parameter. This is exactly the same *category* of gap as
finding an `int` field in a schema built for a `bool` — the schema's
author reasonably generalized from the one instance they had (a
threshold), and Schedule D is the first content that needs a categorical
"required" disposition instead.
─────────────────────────────────────────────────

This is named here as an **unresolved question**, not worked around: this
paper spike is not authorized to edit `attachment-rule.v2.schema.json`
(Rung 1, and the schema is production content). The proposed successor
need (stated precisely, not implemented) is an `attachment-rule.v3` whose
`requirement` block accepts a `oneOf` — the existing threshold shape,
unmodified, or a new `categorical_conclusion` shape referencing a checked
conclusion's `{complete, incomplete, blocked}` (or ADR-0050's `{yes,no}`)
vocabulary directly, with `comparison` dropped in that branch. Until that
successor exists, this design's `attachment.schedule-d.v1` instance above
is intentionally left with its `requirement` block unspecified — it is
not expressible against the accepted schema, and pinning a fabricated
threshold (e.g., "gain > $0") would misstate the actual eligibility
condition, which is categorical (the completeness conclusion), not
numeric.

### Line-7a and line-16 successor design

ADR-0038's Alternatives Considered explicitly rejects "dual line-16
producers with dynamic conflict_semantics selection," and ADR-0027
Decision 5 requires exactly one reachable adopted package producer per
symbol. Both foreclose a design where a box-2a line-7a rule and a
Schedule-D line-7a rule compete as two rules for the same symbol. The
route selection must live **inside one successor rule**.

**Proposed `rule.form1040-line7a.v2.json` (successor to the existing
`rule.form1040-line7a.json`, additive, new version):**

```
match (schedule-d-boundary.conclusion, tax.us.2025.f1099div.2a closure, schedule-d.line16):
  schedule-d-boundary.conclusion = blocked        -> blocked(DEPENDENCY_ABSENT)
  schedule-d-boundary.conclusion = incomplete     -> blocked(DEPENDENCY_ABSENT)   # boundary violated; Schedule D not trustworthy as sole source
  schedule-d-boundary.conclusion = complete:
    require Schedule D family (D1) closure state
    if D1 = closed-with-members:
      require schedule-d.line16 (attachment must have published)
      -> published(schedule-d.line16)                       # Schedule-D route, exactly once
    if D1 = closed-empty:
      require existing box-2a route inputs (ADR-0050 C1-C4 + conclusion + 2a-subtotal), unchanged
      -> existing ADR-0050 v1 behavior, unmodified           # falls through to accepted box-2a route
```

This is stated as a `match` over the boundary conclusion and the P1
family's own closure variant (empty vs. with-members), not a new
`conflict_semantics` selector — it is one rule, one producer, choosing
between two already-accepted numeric sources it never mixes. When D1 is
`closed-with-members`, Schedule D's line 16 is the sole contributor to
line 7a; the existing ADR-0050 box-2a route is not consulted at all for
that publication (case 10, below). When D1 is `closed-empty` (no eligible
LT transactions this year), the rule falls through unchanged to the
existing accepted box-2a route — this is the coexistence-without-double-
counting statement the charter requires: **the two routes are mutually
exclusive by construction inside one rule, gated on which family
actually closed with members**, never both contributing.

**Proposed `rule.form1040-line16.v4.json`** (successor to
`rule.form1040-line16.v3.json`, extending ADR-0050 Decision 7's branch
structure with a Schedule-D-sourced case, additive, new version):

```
match selected_line7a:
  blocked            -> blocked; STOP
  guard_inapplicable -> guard_inapplicable; STOP
  published numeric L, sourced from Schedule-D route (D1 = closed-with-members):
    QDCG                                                 # Schedule D LT gain is unconditionally QDCG-eligible content in this slice's scope
  published numeric L, sourced from box-2a route (existing ADR-0050 v3 behavior):
    require Q (box-2a-adjacent qualified-dividend input, unchanged from v3)
    blocked Q -> blocked; STOP
    if Q > 0 or L > 0 -> QDCG
    else if Q = 0 and L = 0 -> ordinary
```

The new branch does not read `Q` at all for the Schedule-D-sourced case —
per the incumbent constraint, QDCG here consumes only the selected line-7a
*publication* (a number, already the single output of the match above),
never raw transaction or statement content, and never re-derives
eligibility from box-2a facts that have nothing to do with this route.

### Concrete instances

**Case 9 — historical/raw-member reach-around (P3-specific).** An attempt
to have the line-16 successor or QDCG binding read
`tax.us.2025.f1099b.covered-ltcg-txn` members or the pre-correction
history from P1's case 4 directly, bypassing the Schedule D attachment's
published `line16` symbol. Foreclosed: the line-16 successor's only input
for the Schedule-D branch is `selected_line7a`, which is itself sourced
only from the attachment's `publishes: schedule-d.line16` — there is no
pin from the line-16 or QDCG rule to the member fact type or the family
at all.

**Case 10 — downstream double-count attack (mandatory).** Two variants:
(a) box-2a is `closed-with-members` (nonzero) *and* D1 is
`closed-with-members` in the same return — the line-7a match above
requires exactly one of the two `if D1 = ...` branches to fire, and D1
takes precedence when `closed-with-members` (Schedule-D route sourced);
box-2a's own value is never read into `selected_line7a` in that branch,
so it cannot double-contribute. This is a real named design choice —
precedence, not summation — and is called out as needing owner/ADR
ratification, not asserted as self-evidently correct (see Unresolved,
below). (b) QDCG reading raw transaction content: foreclosed by
construction, as stated in case 9 — the QDCG binding's only readable
input is `selected_line7a`.

**Two positives:** (a) D1 `closed-with-members`, gain `4500.00`
(case 4's post-correction total) → line 7a publishes `4500.00`, line 16
routes QDCG. (b) D1 `closed-empty`, box-2a `closed-with-members` at
`450.00` → line 7a publishes `450.00` via the unchanged box-2a route,
line 16 uses existing v3 behavior unmodified.

**Two negatives:** (a) `schedule-d-boundary.conclusion = incomplete`
(case 5b's short-term-present scenario) → line 7a `blocked`,
`DEPENDENCY_ABSENT`, never falls through to box-2a even if box-2a's own
inputs are otherwise satisfied — an incomplete boundary blocks the whole
symbol, it does not selectively degrade. (b) case 11's non-covered
transaction, even if contributed and even if D1 reads
`closed-with-members` from *other* legitimately-admitted transactions,
never appears in `line8a-gain` — it was never admitted to the family
(P1's admission gate), so there is nothing downstream to reject a second
time; the negative is enforced entirely at P1.

**Lifecycle trace:** D1 undeclared → boundary blocked → D1 closes empty,
all D3-D9 satisfied, D2 closes empty → boundary complete, line 7a falls
through to box-2a (also empty) → publishes `0` (closure-backed) → later,
a covered LT transaction is contributed and D1's horizon is stale
relative to the new contribution → line 7a returns to blocked until a
fresh D1 closure is asserted over the expanded membership.

### Producer → authority → consumer → failure map

| Stage | Contract |
|---|---|
| Producer | `attachment.schedule-d` (Part II line 8a/15 content), P1's subtotal rule, P2's boundary conclusion |
| Authority | `rule.form1040-line7a.v2` (single producer, route-selecting match) |
| Consumer | `rule.form1040-line16.v4` (QDCG binding), then the existing unmodified `rule.form1040-line9.v3` (adds `selected_line7a` exactly once, no change needed since it already reads the symbol, not the route) |
| Failure | boundary `incomplete`/`blocked` → line 7a `blocked`, never falls through; D1/D2 both `closed-with-members` → precedence rule fires (named unresolved, below), never summed |

### Accepted contracts consumed unchanged

- ADR-0036's `attachment-rule.v2` itemization/row-set/tie-out/completeness
  shape, instantiated for Schedule D without any schema change (except
  the named `requirement`-block gap, left unresolved, not worked around).
- ADR-0050 Decision 5's line 7a/7b disposition discipline (neither
  guard_inapplicable nor blocked becomes numeric zero) reused verbatim for
  the box-2a fallback branch.
- ADR-0050 Decision 6's line-9 successor is consumed **unchanged** — no
  new line-9 successor is proposed, since it already adds
  `selected_line7a` exactly once regardless of which route produced it.
- ADR-0050 Decision 8's pin/citation/kill-test discipline is the template
  for both new rules' pin sets (not fully enumerated at Rung 1 — named as
  a production condition).

### Proposed successor contract sentences

| Accepted clause | Successor graph effect |
|---|---|
| `rule.form1040-line7a.json` (single box-2a producer) | `rule.form1040-line7a.v2` supersedes additively: adds a Schedule-D-sourced branch selected by D1's closure state, falls through unchanged to the existing box-2a branch when D1 is closed-empty. The existing `.v1`/current rule's behavior is fully preserved as the closed-empty fallthrough — not altered, wrapped. |
| `rule.form1040-line16.v3.json` Decision 7's `match selected_line7a` | `rule.form1040-line16.v4` supersedes additively: adds one new case distinguishing Schedule-D-sourced publications (unconditional QDCG) from box-2a-sourced publications (existing Q-gated logic, verbatim). |
| ADR-0036 Decision 2 (threshold-shaped requirement) | Not superseded here — named as a gap requiring a future `attachment-rule.v3` successor with a `oneOf` requirement shape; this design does not propose that successor's full text, only its need. |

### Production conditions

- The line-7a match's D1-vs-box-2a precedence choice (case 10a) needs
  explicit owner/ADR ratification before production — this design states
  precedence, not summation, as the incumbent's proposal, but flags it as
  a named decision point, not a settled fact.
- `attachment.schedule-d`'s `requirement` block cannot be published until
  the `attachment-rule.v3` categorical-requirement successor exists or an
  alternative composition is chosen.
- The seven-vs-more-than-seven arity question for boundary component D7
  (P2's unresolved item) must resolve before `attachment.schedule-d`'s
  `completeness.required_answers` can be finalized, since it currently
  points at the single synthesized `schedule-d-boundary.conclusion`
  symbol.

### Unresolved questions

- D1-vs-box-2a precedence when both close with members simultaneously
  (case 10a) is a genuine open design question, not settled by this
  paper spike — named explicitly rather than defaulted to either
  precedence or summation.
- The `attachment-rule.v2` → `.v3` categorical-requirement successor is
  named but not drafted; `attachment.schedule-d.v1`'s `requirement` block
  is left unspecified pending that successor.
- Whether QDCG eligibility for the Schedule-D route is truly
  unconditional within this slice's supported source class (no
  collectibles, no special rate, no adjustment codes — all already
  excluded by P1's admission gate and P2's D8) or needs its own guard
  symbol is asserted here as unconditional based on the supported source
  class definition, but is flagged for reviewer scrutiny since it is the
  one branch in the line-16 successor that reads no gating input at all.
