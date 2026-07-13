# Adversary Review — Round 2: Non-Publication Explanations

- **Reviewer:** Adversary Reviewer (Round 2, sub-agent)
- **Designs under attack:** `it1/design.md` + `examination-it1.md`, as refined by
  `round-1-triage.md` (Execution Map + cycle detection/memoization); `it2/design.md`
  + `examination-it2.md` (Run Disposition Ledger / `npe-walk.v1`)
- **Grounding:** committed `packages/derivation/records.py`, `runner.py`,
  `reference_runner.py`, `explanation.py` (all read at `HEAD`, not the
  uncommitted working-tree diff), `packages/schemas/derivation/derivation-record.v1.schema.json`,
  ADR-0006/0008. No python executed. Round-1 reviews and triage read per the
  role's standing permission (round-2-governance.md was **not** read).
- Findings continue the round-1 numbering: **NPE-A4** onward.

Each finding: concrete input state → expected lineage → where the design
fails or survives.

---

## NPE-A4 — it1's "transient Execution Map" cannot outlive the run's process

**Severity: decision-blocking. Applies to: it1 (as refined by round-1 triage).**

Round-1's NPE-G1 resolution requires the runner to "compile a lightweight,
transient Execution Map (rule status log) during evaluation... stored as run
metadata, not as findings in the log," which the walker then queries instead
of re-evaluating guards. The triage text is explicit that this map is
**transient**.

**Input state → expected lineage → failure:** A return is computed today
(runner process P1 runs, saturates, exits — `run_and_record` in the committed
`runner.py` writes only the closing `derivation-record.v1` to
`derivation_records.jsonl`; no execution-map artifact is persisted anywhere in
the committed record schema). Tomorrow, in a new server process P2, a user
opens the return and clicks "why is line 2b blank?" Expected lineage: the same
blocked/inapplicable tree the run actually produced. Where it fails: P2 has no
access to P1's in-memory Execution Map — it was never written to disk, and the
committed `derivation-record.v1` schema (the only durable run-level artifact)
has no field for it. Either (a) the map is silently made durable after all —
in which case it1 has covertly reinvented it2's ledger without documenting the
convergence or reconciling its "transient" framing, or (b) it remains
in-memory-only and every walk request issued after the runner process exits —
which is the *normal* explanation-UI usage pattern, not an edge case — has
nothing to query. it1's design and its round-1 refinement do not state which.
This is not a hypothetical: `records.py`/`runner.py` at `HEAD` show the *only*
durable per-run artifact is the closing record, and it carries `published`,
`blocked`, `dispositions` — not an "Execution Map."

---

## NPE-A5 — it2's ledger is contractually empty for every interrupted run

**Severity: decision-blocking. Applies to: it2.**

`records.py::recover_interrupted` (committed, `HEAD`) is explicit and
deliberate (ADR-0008 decision 2: "recovery never mutates the start record"):
it closes an open run with `published=[], blocked=[], dispositions=[]` and
`stop_reason="interrupted"`. Publications that landed before the crash remain
in `acts.jsonl`, but the *closing record* — the only thing it2's walker reads
(`ledger = record_stream.closing(run).dispositions`) — accounts for **zero**
artifacts.

**Input state → expected lineage → failure:** Run publishes line 2b, then
crashes before evaluating lines 9/11/12/15/16; a later process calls
`recover_interrupted`. A user requests "why is line 16 blank?" Expected
lineage (per NPE-P2/the brief's "down-cascade never-reached" probe): a chain
of `blocked` nodes bottoming out wherever the run actually stopped. Where it
fails: `ledger.row_for(artifact.id)` returns nothing for **every** artifact,
including `rule.form1040-line2b`, which actually published. it2's algorithm
(§5) is written as `row = ledger.row_for(artifact.id)` followed by an
unconditional `case row.disposition of` — there is no branch for "no row
found." The design never states what the walk returns here: a crash, a
silently empty/`None` node, or (worse) a misleading claim that a genuinely
published line 2b is "blocked" with no evidence. This is the concrete,
already-designed-for version of the brief's "what does the walk return for a
rule the scheduler never visited?" — it2's own admitted "weakest point" (§10,
totality) turns out to have a real, already-shipped code path that produces
total sparseness, not partial sparseness, and the design has no case for it.

---

## NPE-A6 — declared multi-publisher conflict semantics break it2's `publisher_of(symbol)` index; it1's schema was (incidentally) built for this

**Severity: decision-blocking for it2. Non-blocking / comparative note for it1.**

ADR-0006 decision 7: "Unique output ownership is package-contract-enforced:
no two members may publish the same symbol **unless the package declares
conflict semantics as content**." This is not theoretical — the committed
`reference_runner.py` (`HEAD`) structurally assumes it:
`producers: dict[str, list[dict[str, Any]]]` is built as
`producers.setdefault(rule["publishes"], []).append(rule)`, i.e. the
scheduler is written to expect **more than one** rule per output symbol, with
ties broken by list order and an early `break` once one producer succeeds.

**Input state → expected lineage → failure:** A symbol (e.g. a deduction
amount) has two rule artifacts under declared conflict semantics: a base rule
and an override rule, both `publishes: "deduction_amount"`. The override's
guard is false this run; the base rule publishes. Expected lineage: one node
for `deduction_amount` showing it published via the base rule *and* citing
that the override rule targeted the same symbol but did not apply. Where it2
fails: `walk()`'s first line is `artifact = artifacts.publisher_of(symbol)` —
singular — and `node_id = artifact.id + "@" + symbol`. There is no mechanism
to enumerate a second artifact targeting the same symbol; `publisher_of` is
undefined behavior (arbitrary pick, or crash) the moment declared conflict
semantics are exercised. it2's own Case 2 example (§7) sidesteps this
entirely by inventing two *different* symbol names
(`itemized_deduction_applied` vs `standard_deduction_applied`) for what the
plan's Case 2 actually describes as one line (line 12) with an override — so
the required case is answered by construction-avoidance, not by solving the
real ADR-0006-sanctioned scenario. it1's `explanation-walk.v1` schema, by
contrast, already models a symbol node as `rules: array` (its own Case 2
payload shows *two* rule entries — `demo.rule.standard-deduction-selector`
published, `demo.rule.itemized-deduction-override` inapplicable — under one
symbol) — structurally closer to correct for this case, though it1 never
argues this was intentional and doesn't discuss declared-conflict-semantics
by name either.

---

## NPE-A7 — it2's published-lineage diamonds are not deduplicated (delegated, unmodified `explanation.py` has no cross-branch memo)

**Severity: decision-blocking for it2 (confirmed defect). Open/unknown for it1 (unaddressed).**

it2 §3 states: "for `published` rows, the workspace derived findings, walked
by the existing pin-lineage walker (`explanation.py`) unchanged," and §8
claims "each artifact is fully expanded at most once" as a general property of
the walk. I read `packages/derivation/explanation.py` at `HEAD`: `explain()`
takes a `_seen: frozenset[str]` threaded *by value* down each recursive call
(`seen = _seen | {finding_id}`), which only detects a finding recurring **on
its own active path** (a true cycle) — it is reset/rebuilt per branch and
carries no shared, cross-branch memo table. Two sibling children that both
depend on the same ancestor finding (a diamond, not a cycle) each
independently call `explain(that_finding_id, ...)` and each **fully
re-expands** its entire subtree.

**Input state → expected lineage → failure:** AGI feeds both `taxable_income`
(line 11) and, say, a phase-out threshold consumed elsewhere in the same
explained tree (a realistic wide-fan-out shape — the brief explicitly asks
for "combinatorial growth ... on wide fan-out rulesets"). Expected: the
`shared`/O(artifacts) guarantee it2 claims in §8 holds end-to-end. Where it
fails: that guarantee is true *only* for the ledger-native `blocked`/
`inapplicable` nodes it2 introduces; the moment a walk reaches a `published`
node with fan-out, control passes to `explanation.py`, which re-expands the
shared ancestor's full pin-lineage subtree at every occurrence — genuine
combinatorial blowup on exactly the topology (deep, wide-fan-out published
ancestors feeding many downstream lines) the round asks to probe. it1 does
not specify how published lineage is walked at all (no explicit hookup to
`explanation.py` is described in either the original design or the round-1
refinement), so the same risk is neither confirmed nor ruled out for it1 —
flagged as an open gap rather than a demonstrated defect.

---

## NPE-A8 — two-runner parity is proven only for published findings, not for the non-publication bookkeeping either design walks

**Severity: production condition. Applies to: both (a substrate risk, not walker-local).**

`reference_runner.py`'s own docstring (committed, `HEAD`) is precise about
scope: "a byte-identical **published-finding** set across both runners proves
the derived record is a function of (artifacts, canon, inputs) alone." It
makes no claim about `blocked`/`dispositions` parity. Combined with
`producers: dict[str, list[...]]` (NPE-A6): under declared conflict
semantics, the demand-driven reference runner's `resolve()` tries producers in
list order and `break`s on the first success — a sibling rule that never gets
its own `attempt()` call is still swept by `finalize_unreached()`, which marks
it `blocked` / `BLOCK_ABSENT` with `missing = [req for req in rule["requires"]
if req not in self.symbols]`. If that sibling's own `requires` happen to be
fully satisfied (the winning rule used the same inputs), `missing` is
**empty** — a "blocked" row naming nothing missing.

**Input state → expected lineage → failure:** Same conflict-semantics symbol
as NPE-A6, walked once under the forward runner and once under the reference
runner for the same input state. Expected lineage (walk determinism, the
brief's explicit requirement): identical `npe-walk.v1`/`explanation-walk.v1`
trees. Where both designs fail: neither payload schema (it1's `disposition`
enum: `published`/`blocked`/`inapplicable`; it2's `block_code` enum:
`ABSENT`/`INVALID`/`OPEN_SOURCE`/`UNREACHED`) has a vocabulary slot for "lost
to a sibling under conflict-resolution priority, nothing actually missing." A
future scheduler swap, or even today's dual-runner setup, can produce a
self-contradictory `blocked, missing: []` row that both walkers would render
as "blocked" with no explanation of *why* — worse than either honest
disposition. This is a runner/record-schema gap that both walk designs
inherit and neither surfaces as an authority question (it2 lists five
authority questions in §9; none of them is this one).

---

## NPE-A9 — it2's memoization pseudocode contradicts its own "expanded at most once" claim

**Severity: production condition. Applies to: it2.**

§8 states as an invariant: "Each artifact is fully expanded **at most once**;
all other encounters are constant-size refs." The §5 pseudocode cannot
deliver this. Its cache-population step is: expand the node, then *after*
expansion, `if node_id was reached more than once: shared[node_id] = node;
return ref(shared, node_id)`. There is no forward-looking mechanism (e.g. a
static in-degree pre-pass over the adopted package's dependency graph) that
would let the *first* reach know a second is coming.

**Input state → expected lineage → failure:** A true diamond visited exactly
twice — Case 1's own topology (line 11 and line 15 both funnel through
blocked line 2b). Trace: `walk` reaches line-2b's node via line 11's branch
first. At that point `node_id` is not yet in `shared` (nothing has told the
algorithm a second reach is coming), so it fully expands, unwinds, and — per
the pseudocode — is *not yet* known to be "reached more than once," so it is
returned inline, not cached. Later, line 15's branch reaches the same
`node_id` again: not in `visited.active` (first expansion already unwound),
not in `shared` (never populated) — so it is **fully re-expanded a second
time**. Only now, after this second complete expansion, does the "reached
more than once" check fire and populate `shared` for any *third* occurrence.
Net: the artifact is expanded **twice**, not once, directly contradicting
§8's stated guarantee. For Case 1 specifically this is cheap (a two-node
subtree), but the brief's "combinatorial growth ... on wide fan-out
rulesets" attack generalizes it: every node with in-degree exactly 2 pays for
one full duplicate expansion before the cache engages, and the design's
complexity claim (`O(|artifacts| + |edges|)`) is not delivered by the
described algorithm without an unstated static pre-pass.

---

## NPE-A10 — stale-ledger-vs-current-workspace: it2 exposes the signal, it1's schema has no way to detect it at all

**Severity: non-blocking (production condition for it1's schema specifically).**

Concrete scenario (the brief's required attack): run R closes with line 2b
`blocked`/`OPEN_SOURCE`. The user then asserts a new 1099-INT finding that
closes the source family — workspace revision advances — **without**
re-running derivation. A walk is now requested.

- **it2:** the walk is explicitly pinned to one run
  (`ledger = record_stream.closing(run).dispositions`) and the payload schema
  requires both `run_id` and `workspace_revision` (§4, `required` list). The
  walk will correctly and consistently report the stale run's blocked state,
  self-labeled with the revision it was computed against — a caller can at
  least detect staleness by comparing `workspace_revision` to the workspace's
  current revision. The design never states *who* is responsible for that
  comparison or for triggering a re-run (an open, non-blocking question — not
  answered in §9 either), but the data needed to detect the problem is in the
  payload.
- **it1:** `explanation-walk.v1` (§2 of `it1/design.md`) has **no** `run_id` or
  `workspace_revision` field anywhere in the schema. Whatever the walk is
  grounded in (rule ASTs directly, or the round-1-refined Execution Map), the
  returned payload gives a consumer no way to tell whether the explanation
  reflects the current workspace state or a stale prior run at all — the
  schema-level staleness signal that it2 has is simply absent from it1.

---

## NPE-A11 — it2 overstates its own weakest point; the real gap is narrower than §9/§10 claim (informational, redirects rather than adds risk)

**Severity: non-blocking / clarifying. Applies to: it2.**

it2 flags ledger totality (§9.1) as its central unresolved authority question
and names it the design's "weakest" point (§10), framing it as a general,
open risk for all down-cascade never-reached rows. Reading the committed
`runner.py::finalize_unreached()` shows this is *narrower* than claimed: for
any **normally completed** run (not interrupted), every rule that never
becomes eligible is unconditionally swept into a `blocked`/`BLOCK_ABSENT` row
by construction — totality already holds today, structurally, for the
saturated case. The real, sharp gaps are (a) the interrupted-run case
(NPE-A5, which is total *sparseness*, not partial), and (b) a vocabulary
gap: the committed runner emits `BLOCK_ABSENT` uniformly whether the missing
symbol is the rule's own direct, first-hop dependency or a cascade ancestor
five hops up — there is no runtime distinction between "leaf absent" and
"never reached because an ancestor blocked." it2's schema invents an
`UNREACHED` code (§2, §9.1) that the grounding runner does not currently
emit anywhere; it2 is right to flag this as an authority question, but should
not conflate it with a general totality risk that the committed forward
runner has already resolved.

---

## Verdicts

### it1 (Shape A + round-1's Execution Map/cycle-detection refinement)

**Conditionally accept.** Conditions:
1. Resolve NPE-A4: state explicitly whether the Execution Map is durably
   persisted (and where, and under what schema) or explain how a walk
   requested in a process/session after the runner exits is served at all.
   "Transient" as currently written makes the design non-functional for the
   ordinary explanation-UI usage pattern.
2. Add run identity / workspace-revision fields to `explanation-walk.v1`
   (NPE-A10) so staleness is at least detectable.
3. Specify how published-lineage traversal integrates with the existing
   `explanation.py` (or a modified version of it), including diamond/cycle
   behavior there — currently unaddressed (related to NPE-A7).
4. Explicitly own the multi-publisher/declared-conflict-semantics case its
   own `rules: array` shape already accommodates structurally (NPE-A6), so it
   isn't accidental.

### it2 (Run Disposition Ledger / `npe-walk.v1`)

**Conditionally accept.** Conditions:
1. Resolve NPE-A5: define walker behavior when `ledger.row_for` returns no
   row (interrupted-run recovery is a real, already-implemented code path
   that empties the ledger entirely, not a hypothetical).
2. Resolve NPE-A6: extend the publisher index / node-id scheme to represent
   declared multi-publisher conflict semantics (confirmed live in
   `reference_runner.py`'s `producers: dict[str, list[...]]`), and revise
   Case 2 to exercise the real same-symbol-override scenario rather than a
   two-symbol stand-in.
3. Resolve NPE-A7: either wire genuine cross-branch memoization into
   `explanation.py` (a change outside this design's stated boundary) or
   explicitly retract the "O(artifacts)" claim for trees that reach published
   fan-out ancestors.
4. Fix or soften NPE-A9: the §5 pseudocode does not deliver the §8
   "expanded at most once" guarantee; either add the static in-degree
   pre-pass the guarantee requires, or restate the bound honestly (expanded
   at most twice per artifact, then cached).
5. Both designs additionally depend on a runner/record-schema fix for NPE-A8
   (conflict-semantics dispositions have no vocabulary and no cross-runner
   parity guarantee) — this is out of either walker design's scope to fix
   alone but must be tracked as a shared blocking dependency before either
   ships.

Neither design is rejected outright; both survive the cyclic-block, basic
diamond, and invalid-input-depth attacks as specified. The decision-blocking
findings above are concentrated in persistence lifetime (it1), ledger
sparseness on the interrupted-run path (it2), and a shared substrate gap
(declared multi-publisher conflict semantics, it2 structurally more exposed
than it1) that both hand off to the runner/record-schema layer rather than
resolving in the walker.
