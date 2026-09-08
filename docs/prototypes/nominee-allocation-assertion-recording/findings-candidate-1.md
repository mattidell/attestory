# Candidate 1 findings — separately individuated allocation-statement entity

Track 0 charter, checkpoint T0-A:
Track 0, checkpoint T0-A.

Scope of this document: **candidate 1 only** — a separately individuated
allocation-statement `entity.v1` citizen, ended by `act-entity-superseded.v1`
with `replacement` omitted. Candidate 2 (adopted source family +
`act-member-transition.v3`) is out of scope here and is being evaluated
separately.

Probe executed: `docs/prototypes/nominee-allocation-assertion-recording/probes/candidate-1-entity.py`.
Run with `python3 docs/prototypes/nominee-allocation-assertion-recording/probes/candidate-1-entity.py`
against the real committed kernel (`packages/kernel/act_log.py`,
`packages/kernel/facts.py`, `packages/kernel/findings.py`,
`packages/kernel/currency.py`, `packages/kernel/read_models.py`) and the real
committed schemas in `packages/schemas/kernel/` — every claim below cites
executed output. No file under `packages/` or `tests/` was modified. Only
synthetic `demo.*` / `demo-*` identities and values were used.

## Candidate shape actually run

- A "report" (one identified Form 1099-INT report) is an ordinary
  `entity.v1` citizen, kind `demo.report-1099int`.
- The allocation statement itself — "a named user says a stated amount from
  this report belongs to a named other person" — is a **separately
  individuated `entity.v1` citizen**, kind `demo.nominee-allocation`, one
  per `(report, owner)` pair. The owner's name lives in the entity's `label`
  only (the `entity.v1` schema has no other free-text field); the owner's
  *identity* for kernel purposes is the entity id itself.
- One fact type, `demo.nominee-allocation.amount`, keyed on **both**
  entities (`report` and `allocation` identity keys), `supersession.policy:
  "free"`, `nature: "determinable"`, `value_schema: {"type": "number",
  "minimum": 0}`.
- Recording = `entity-introduced` (allocation entity) + `assertion`
  (the amount, `basis: "attested"`, citing the report's evidence).
- Correction = an ordinary second `assertion` on the **same** fact id
  (permitted by the "free" supersession policy).
- Withdrawal = `act-entity-superseded.v1` naming the allocation entity, with
  `replacement` **omitted**.

Every act was committed by first applying it semantically against a running
`findings.FindingState` (`findings.apply_act`) and only then appending to a
real `ActLog` — mirroring the real production writer
(`packages/derivation/entry_loop.py:824-845`, which calls
`apply_contribution_batch`/`project` before ever calling `self._log.append`).
This distinction matters: **`ActLog.append` alone validates only JSON-Schema
shape, never kernel semantics** — see the "Bonus" result below, executed
separately on a throwaway log.

## Per-case result

### A2 — one owner's allocation records: **PASS**

Executed: introduced report entities + evidence, adopted the bundle,
introduced allocation entity `demo-alloc-r001-pat`, asserted
`demo-finding-pat-r001-v1` (value 600) on fact id
`demo.nominee-allocation.amount|report=demo-report-1099int-001,allocation=demo-alloc-r001-pat`.

```
current finding ids: ['demo-finding-pat-r001-v1']
A2 executed result: current=True
```

### A3 — several owners are distinguishable: **PASS**

Executed: introduced a second allocation entity `demo-alloc-r001-kim` on the
**same** report, asserted `demo-finding-kim-r001-v1` (value 400).

```
fact id for Kim/report-001: demo.nominee-allocation.amount|report=demo-report-1099int-001,allocation=demo-alloc-r001-kim
current finding ids: ['demo-finding-kim-r001-v1', 'demo-finding-pat-r001-v1']
fact ids distinct: True
A3 executed result: True
```

Pat's and Kim's fact ids differ because they are keyed on different
allocation entities; nothing else distinguishes them from the fact type's
point of view. No coupling of any kind was needed to keep them apart — this
falls straight out of individuation.

### A4 — correcting Pat leaves Kim at the same identity and revision, no act written on Kim's behalf: **PASS**

Executed: recorded Kim's finding dict by value *before* correcting Pat
(`kim_finding_before`), asserted `demo-finding-pat-r001-v2` (value 650) on
Pat's **same** fact id (an ordinary correction, permitted by the fact
type's `supersession.policy: "free"`), then re-read Kim's finding dict
(`kim_finding_after`) and asked for **Python `dict` equality**, not value
comparison — i.e. record identity, exactly as the charter asks.

```
Kim's finding record identical before/after (dict equality): True
Kim's finding still current after Pat's correction: True -> True
Pat v1 displaced, reason: (DisplacementReason(kind='correction', by='demo-finding-pat-r001-v2'),)
Pat v2 current: True
acts newly written during the correction: ['demo-act-009']
any new act names Kim: False
A4 executed result: True
```

Exactly one act was written by the correction (`demo-act-009`, Pat's own
new assertion); no act mentioning Kim exists anywhere in the log after it.
Kim's finding is still supported by her own original act
(`demo-act-008`, see the attribution table below) — nothing about her
identity, revision, or supporting act changed.

### A5 — an allocation on report A cannot attach to or be mistaken for report B from the same payer: **PASS** (with one clarified boundary)

Executed: introduced a second report entity `demo-report-1099int-002`
(same payer, `demo-payer-inc`), its own evidence, a second allocation
entity `demo-alloc-r002-pat` for Pat, and asserted `demo-finding-pat-r002-v1`
(value 900).

```
report-001 Pat fact id: demo.nominee-allocation.amount|report=demo-report-1099int-001,allocation=demo-alloc-r001-pat
report-002 Pat fact id: demo.nominee-allocation.amount|report=demo-report-1099int-002,allocation=demo-alloc-r002-pat
fact ids distinct across reports: True
current value under report-001+alloc-r002-pat (should be open/no-current, never 900): '<no current value>'
current value under report-001+alloc-r001-pat: 650
current value under report-002+alloc-r002-pat: 900
A5 executed result (fact-identity separation): True
```

Because the report is one of the fact type's own identity keys, an
allocation amount can *only ever* answer the fact id that names both the
correct report entity and the correct allocation entity — the constructed
cross-report fact id (`report=001, allocation=demo-alloc-r002-pat`, a
combination that was never asserted) resolves to no current value at all,
never to 900.

**Clarified boundary, executed as a dry run and never committed to the real
log or state**: nothing at the kernel level stops an assertion against
report A's *own* fact id from citing report B's evidence in
`evidence_ids` — evidence is provenance, never identity (per
`packages/schemas/kernel/evidence.v1.schema.json`'s own description, and
`findings.py`'s `_validate_finding`, which checks only that cited evidence
is *current*, never that its content matches the fact's own identity
keys):

```
DRY RUN (never committed): cross-report evidence citation on report-001's own fact id blocked: False
  (kernel allows this at the semantic layer -- evidence is provenance, not identity; this is a
  documentary-quality concern, never a fact-identity leak, since the amount still only ever
  answers report-001's own fact id)
```

This is a real, executed limitation, but it is not the failure mode A5
asks about: the *amount* still only ever answers report A's fact id
regardless of which evidence a sloppy assertion cited. Mis-cited
provenance is a documentary-quality question a review workflow would
catch, not a structural mix-up of which report an allocation belongs to.

### A6 — withdrawal without a negative claim, authorship survives: **PASS**

Executed: `entity-superseded` naming `demo-alloc-r001-pat`, `replacement`
key **omitted** from the payload entirely.

```
Pat v2 current before withdrawal: True
Pat v2 current after withdrawal: False
Pat v2 displaced after withdrawal: True, reason kinds: ['individuation']
Pat v2's recorded value unchanged (still 650, not 0/false/negative): True
Kim unaffected by Pat's withdrawal: True
withdrawal act payload: {'entity_id': 'demo-alloc-r001-pat'} (no finding/member key -> no finding written)
withdrawal wrote a finding: False
authorship of withdrawn finding demo-finding-pat-r001-v2 recoverable: act_id=demo-act-009 actor=demo-user-matt at=2026-09-05T00:00:10Z
A6 executed result: True
```

The withdrawal act's entire payload is `{"entity_id": "demo-alloc-r001-pat"}`
— no `value`, no `false`, no opposite-ownership claim, nothing zeroed. The
withdrawn finding's own recorded value (650) is untouched in
`state.findings`; `currency.compute_currency` displaces it via the
`individuation` displacement edge (root: the now-superseded entity), which
is the same mechanism `tests/test_currency.py`'s
`test_individuation_edge_displaces_finding_when_keyed_citizen_is_superseded`
already exercises for a `replacement`-carrying entity-superseded act — this
probe additionally confirms the `replacement`-omitted case behaves
identically for displacement purposes. Kim is untouched. Authorship of the
withdrawn finding is still recoverable by the same join described below.

### A11 — can `(report, owner)` become current again after withdrawal? **PASS, at a new fact identity — not the same one**

This is the case the charter calls out as the discriminator. Three things
were actually run, in order:

**1. Attempt to un-supersede / re-supersede the same entity** (dry run,
never committed):

```
DRY RUN: supersede the withdrawn entity again -> blocked: True
  error: entity is not current: demo-alloc-r001-pat
```

`packages/kernel/facts.py:143` (`apply_entity_superseded`) requires
`existing.status == "current"`; there is no applier anywhere in
`packages/kernel/facts.py` or `packages/kernel/findings.py` that flips a
superseded entity back to current. This is monotonic, structurally, for
the same reason candidate 2's `withdrawn_fact_ids` is monotonic — it is
just a different field (`entities[...].status`, not `withdrawn_fact_ids`).

**2. Attempt to assert a brand-new finding onto the exact same fact id the
withdrawn entity answered** (dry run, never committed):

```
DRY RUN: assert a NEW finding on the SAME fact id
(demo.nominee-allocation.amount|report=demo-report-1099int-001,allocation=demo-alloc-r001-pat)
after withdrawal -> blocked: True
  error: finding references unknown fact:
  demo.nominee-allocation.amount|report=demo-report-1099int-001,allocation=demo-alloc-r001-pat
```

This is the mechanism, confirmed by execution: `facts.facts_of` (the
derived fact lattice) only ever projects facts for **current** entities
(`packages/kernel/facts.py:268-274`, `include_displaced=False` by
default). Once the allocation entity is superseded, its fact id is not
merely "closed" — it is **absent from the lattice entirely**, so
`findings._validate_finding` rejects any new finding against it as
"references unknown fact." Reassertion at the same fact id is not just
policy-forbidden here, it is structurally impossible without a new
kernel primitive.

**3. The one path that does work** — a brand-new allocation entity for the
same `(report, owner)` proposition:

```
re-assertion fact id: demo.nominee-allocation.amount|report=demo-report-1099int-001,allocation=demo-alloc-r001-pat-2
re-assertion current: True
re-assertion fact id is a NEW/different fact id from the withdrawn one: True
the OLD (withdrawn) fact id is NOT answered by any current finding, per true
read-model currency (currency.compute_currency): True
Kim's identity/revision still untouched by the whole withdraw+reassert sequence: True
A11 executed result: same-fact-identity reassertion possible: False
A11 executed result: new-fact-identity reassertion possible: True
```

`entity-introduced` for a new entity id (`demo-alloc-r001-pat-2`) plus an
ordinary `assertion` succeeds, is current, and answers a genuinely
*different* fact id than the withdrawn one. **What this does to A4's
per-owner identity**: nothing — A4's per-owner separation was already
achieved by giving each owner their own entity from the start, so a
second, later entity for the same owner is simply one more instance of the
same pattern; it does not touch Kim's entity, fact, or finding at all, and
it does not need to touch or reinterpret the withdrawn Pat entity either.
The cost lands elsewhere: the reasserted proposition has **no kernel-level
identity link back to the withdrawn one** — reconnecting "this is the same
real-world statement, made again" is only possible by domain convention
(e.g., matching the `label` text, or an out-of-band correlation the
kernel does not model), never by fact-id equality or any other citizen
reference the kernel provides.

**One executed caveat, distinct from the true-currency answer above**:
`findings._current_value_for_fact` — the internal reader used *only* by
specific enforcement checks (`_enforce_subset_invariants`,
`_enforce_companion_presence`, `_enforce_companion_equalities`,
`_enforce_closed_on_attestation`; see `packages/kernel/findings.py:169-182`)
— consults `state.withdrawn_fact_ids` (populated only by
`member-transition` remove/reclassify) and **never** consults entity
supersession. Executed:

```
CAVEAT -- executed, not inferred: findings._current_value_for_fact (the internal reader used
ONLY by subset-invariant / companion-presence / closed-on-attestation enforcement, never by the
read model) still returns 650 for the withdrawn fact id -- it consults state.withdrawn_fact_ids
(member-transition only) and never entity supersession, so it disagrees with true currency here.
```

No domain rule declared in this probe's bundle uses that reader against
`demo.nominee-allocation.amount`, so this does not affect any result
above and is not a disqualifier for this recording-only milestone. It is
flagged because a *later* subset-invariant or companion-presence rule
declared over this fact type (not proposed here, not in scope) would
silently treat a withdrawn allocation's old value as still live inside
those specific enforcement checks, even though the read model and every
other consumer of `currency.compute_currency` correctly shows it
withdrawn. This is a real, executed asymmetry in the kernel between two
different "current" readers, not a property specific to candidate 1's
design choice — candidate 2 does not have this asymmetry for its own
withdrawal mechanism, since `_current_value_for_fact` *does* consult
`state.withdrawn_fact_ids` directly.

## Bonus, executed: `ActLog` alone enforces schema shape only, never kernel semantics

Run against a throwaway log, never mixed into the real results above:

```
ActLog accepted an entity-superseded act naming an entity that was never introduced -- schema
validation alone permits this; only findings.project()/facts.apply_act() over the read-back acts
raises:
  project() raises on replay: unknown entity: demo-entity-that-was-never-introduced
semantic error only surfaces on projection/replay, not on append: True
```

This mirrors the real production writer's own structure
(`packages/derivation/entry_loop.py:824-845`, which calls
`apply_contribution_batch`/`project` and only then `self._log.append`):
any future writer for candidate 1 must perform the same semantic
pre-check before committing, exactly as this probe's `Workspace.commit`
helper does. This is a property of the kernel's layering generally, not
something specific to candidate 1's shape, but it had to be discovered by
running the log, not by reading it — an earlier version of this same
probe silently committed a semantically-illegal act before this was
caught.

## History, attribution, and coupling — executed reads

```
total committed acts: 15
total distinct fact ids the read model has ever projected: 6
all finding ids ever recorded (never deleted -- history_by_fact retains all):
  ['demo-finding-kim-r001-v1', 'demo-finding-pat-r001-reasserted-v1', 'demo-finding-pat-r001-v1',
   'demo-finding-pat-r001-v2', 'demo-finding-pat-r002-v1']
current finding ids (final):
  ['demo-finding-kim-r001-v1', 'demo-finding-pat-r001-reasserted-v1', 'demo-finding-pat-r002-v1']
  demo-finding-kim-r001-v1: actor=demo-user-matt at=2026-09-05T00:00:09Z act_id=demo-act-008
  demo-finding-pat-r001-reasserted-v1: actor=demo-user-matt at=2026-09-05T00:00:18Z act_id=demo-act-014
  demo-finding-pat-r001-v1: actor=demo-user-matt at=2026-09-05T00:00:07Z act_id=demo-act-006
  demo-finding-pat-r001-v2: actor=demo-user-matt at=2026-09-05T00:00:10Z act_id=demo-act-009
  demo-finding-pat-r002-v1: actor=demo-user-matt at=2026-09-05T00:00:12Z act_id=demo-act-011
```

- **History retained**: every finding ever asserted stays in
  `state.findings` forever, including displaced/withdrawn ones
  (`demo-finding-pat-r001-v1`, superseded by correction, and
  `demo-finding-pat-r001-v2`, later withdrawn by entity supersession, are
  both still present with their original values). Nothing is deleted or
  rewritten; only currency (a derived read, `currency.compute_currency`)
  changes.
- **Attribution join, exact and executed**: a finding citizen
  (`finding.v1`/`finding.v2`) carries **no actor and no timestamp field at
  all** (`packages/schemas/kernel/finding.v1.schema.json`'s `required` list
  has neither). The only recoverable actor/time is on the **act envelope**
  (`act.v1`'s `actor` and `at`, both required —
  `packages/schemas/kernel/act.v1.schema.json`). The join used throughout
  this probe (`act_for_finding` in the probe script) is: scan committed
  acts for the one whose `payload.finding.id` (assertion) or
  `payload.member.finding.id` (member-transition, not used by candidate 1)
  equals the target finding id. This is an O(n) linear scan over the act
  log in this probe — acceptable for a probe, and the exact shape any
  candidate-1 read-model builder would need to replicate or index.
- **Owners coupled anywhere?** No. Executed: correcting Pat wrote exactly
  one new act and named Kim in none of them (A4); withdrawing Pat's
  allocation entity displaced only findings individuated on that one
  entity, confirmed by `Kim unaffected by Pat's withdrawal: True` (A6);
  the two owners never share a fact id, an entity, or an act.
- **What individuation displacement does to history**: nothing to the
  underlying record — the displaced finding's `value`, `basis`, and
  `evidence_ids` are byte-identical before and after. What changes is
  purely a derived read: `currency.compute_currency`'s
  `current_finding_ids` / `displaced_finding_ids` sets, recomputed fresh
  from the acts every time, never stored as a flag on the finding itself.

## What I ran vs. what I inferred

**Ran** (all output above is copy-pasted probe stdout, not paraphrased):
bundle adoption; entity introduction (reports and allocations); evidence
submission; assertion (initial recording, correction, cross-report,
reassertion, same-fact-id-after-withdrawal attempt); entity-superseded
(withdrawal, and the blocked re-supersede attempt); `currency.compute_currency`
over every intermediate state; `findings._current_value_for_fact` directly,
to expose the internal-reader caveat; `read_models.build_read_model`;
`findings.project` over a deliberately semantically-invalid throwaway log.

**Inferred** (stated as inference, not asserted as executed): that the
`entities[...].status` monotonicity is "for the same reason" candidate 2's
`withdrawn_fact_ids` monotonicity holds — this is a structural
resemblance read from `packages/kernel/facts.py` and
`packages/kernel/findings.py`'s source and comments, not something a
side-by-side probe run compared; candidate 2's own behavior was not
re-executed by this probe (it is out of this document's scope) and is
being verified independently by the parallel builder.

## Verdict

**Candidate 1 is viable for this recording-only milestone.**

- A2, A3, A4, A5, A6 all PASS by execution, with no coupling between
  owners anywhere, no negative/zeroed claim on withdrawal, and full
  history retention.
- A11 PASSES in the only sense a recording-only milestone needs:
  re-assertion after withdrawal is achievable by the exact same two acts
  (`entity-introduced` + `assertion`) that recorded it the first time —
  no new kernel primitive, no new act kind, nothing beyond what this
  milestone's own boundaries already permit. It does **not** pass in the
  stronger sense of "the same fact identity becomes current again" — that
  is structurally impossible on this candidate (the withdrawn entity can
  never return to `current`, and the lattice will never again offer its
  old fact id to `_validate_finding`). Whether "genuinely the same
  proposition, reopened" or "a new statement of the same content" is the
  right product meaning is exactly the kind of question the charter
  reserves for the owner (`## Boundaries`: "Do not select among survivors
  that carry materially different product meanings — that is the owner's").
  What this probe settles is only the mechanical question: reassertion is
  possible, cheaply, at a new identity, with no data-level linkage back to
  the withdrawn one beyond domain convention (matching labels/report/owner
  by hand, not by any kernel-provided reference).
- One caveat, not a disqualifier: `findings._current_value_for_fact` (used
  only by subset-invariant/companion-presence/closed-on-attestation
  enforcement, none of which this milestone declares over the allocation
  fact type) does not see entity-supersession withdrawal — only
  `currency.compute_currency` (the read model's actual currency) does.
  This should be carried forward as an open note if a later milestone ever
  wants to declare such a rule over an entity-individuated fact type.

No negative result to report for candidate 1 itself: every case the
charter names was executed and passed. The one adversarial finding worth
carrying forward (the `ActLog`-vs-semantics gap, and the
`_current_value_for_fact`-vs-currency gap) are general kernel-layering
facts, not specific to or caused by candidate 1's design.
