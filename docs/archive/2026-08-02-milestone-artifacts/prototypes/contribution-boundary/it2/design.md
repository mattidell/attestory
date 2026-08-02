# D2 Contribution Boundary — Iteration 2 Design (Clean-Room Rival)

Builder: clean-room rival, High tier. Date: 2026-07-16. Evidence: Rung 2 —
paper schema diffs plus throwaway synthetic probes against the committed
kernel/derivation machinery at `HEAD` and scratch out-of-repo workspaces.

**Seal attestation.** This design was derived solely from the committed
contracts (Constitution Articles 7/10/12/14, Ontology, Engineering
Constraints, ADR-0023, ADR-0031), the topic `plan.md`, `charter-it2.md`, and
the committed `packages/kernel/` and `packages/derivation/` source and
schemas. No incumbent material (`it1/`, `examination-it1.md`,
`charter-it1.md`) was read. Every value, payer, and identifier below is
synthetic.

## 1. The shape in one paragraph

A **contribution** is a recorded product event — an act of a new declared
kind — that anchors a batch of manual entries to the source document they
were read from. The contribution act carries a small **contribution citizen**
(identity + source-document reference + entry mode), exactly parallel to how
`evidence-submitted` carries `evidence.v1`. The values themselves then enter
through the **existing** finding-producing acts — `member-transition` for new
family members, plain `assertion` for same-member corrections (ADR-0023) —
each produced finding pinning its contribution by id (`finding.v2`). The raw
entry batch is never stored: like a proposal, it is transient, and what
persists verbatim is the capture inside each finding (Article 2). A run
consumes findings marshalled from projected record state and nothing else;
the raw-input path is not restricted but **unrepresentable**. All of this
happens only inside the ADR-0031 live workspace `L`: contribution acts carry
real values, so every artifact they touch classifies `NEVER_CROSSES`.

## 2. D2-P1 — The contribution event

### 2.1 New citizens (Article 10: schemas before instances)

Paper diff 1 — `packages/schemas/kernel/contribution.v1.schema.json` (new):

```json
{ "$id": "kernel/contribution.v1",
  "title": "Contribution",
  "description": "A recorded product event anchoring entered values to their source: which document, by what mode. Immutable; never superseded; a correction is a NEW contribution. Findings pin it (finding.v2); it is not a rule input and not a standing-affecting edge.",
  "type": "object",
  "properties": {
    "schema": { "const": "contribution.v1" },
    "id": { "type": "string", "minLength": 1 },
    "mode": { "enum": ["manual-entry"] },
    "evidence_id": { "type": "string", "minLength": 1 },
    "label": { "type": "string", "minLength": 1 } },
  "required": ["schema", "id", "mode", "evidence_id", "label"],
  "additionalProperties": false }
```

Paper diff 2 — `act-contribution.v1.schema.json` (new act payload, mirroring
`act-evidence-submitted.v1`): `{ "contribution": { "schema": "contribution.v1" } }`,
required, no additional properties. The act envelope (`act.v1`) is unchanged.

Paper diff 3 — `finding.v2.schema.json` (new version; v1 stays published):
identical to v1 plus one optional property:

```json
"contribution_id": { "type": "string", "minLength": 1 }
```

Paper diff 4 — `contribution-record.v1.schema.json` (new, record kind): the
Article 14 account of one entry session — `contribution_id`, workspace
revision span, `committed_act_ids`, `rejected` (each: submitted shape,
deterministic rejection reason), `stop_reason`. Immutable; lives in `L`
(sensitivity by description, Ontology §8); never consumed by derivation
(E14.2).

Ontology register additions (versioned governance diff, owner-ratified with
the ADR): **contribution** — kind `citizen` (thing), §3-adjacent;
**contribution act** — kind `act`; **contribution record** — kind `record`.
Later ingestion modes (OCR, import) extend the `mode` enum by new schema
version, changing nothing else — the event is the precedent, the mode is a
detail.

### 2.2 Admission semantics (kernel fold, paper)

- `contribution` act: rejects a duplicate `contribution_id`; rejects an
  `evidence_id` that is not current evidence (same reference-integrity rule
  findings already obey). Contributions have no lifecycle beyond existence:
  no supersession, no withdrawal — the event happened.
- `finding.v2` with `contribution_id`: rejects if the contribution is not
  recorded (declaration precedes reference), or if the contribution's
  `evidence_id` is not a member of the finding's `evidence_ids` (the
  provenance chain must be internally consistent).
- Everything else is the existing fold unchanged: ADR-0023 routes new members
  to `member-transition` and same-member corrections to plain `assertion`;
  horizons, currency, and supersession are untouched.

**Deliberately not an edge.** `contribution_id` is provenance, never
standing: contributions are immutable and unsupersedable, so no displacement
can originate at one, and the two-edge doctrine (Article 7, ADR-0010/0017:
derivation and individuation edges only) is preserved without exception. This
is why the pin rides as a plain field and not inside `pins` — `pins` declares
derivation-edge dependencies; a contribution reference must never be walked
as one.

### 2.3 Provenance linkage (Article 12)

Chain, walked from any manually entered value:

```
finding (value, basis, capture)
  ── contribution_id ──▶ contribution (mode, label)
  ── evidence_id ──────▶ evidence (the source document citizen)
  ── admitting act ────▶ who, when, against which revision
```

"Version" of the source document is its immutable evidence id: evidence
replacement mints a successor id (`apply_evidence_replaced`), so an id **is**
a version pin, and a corrected document is a different pin. The finding's
existing `evidence_ids` stays: direct documentary standing (Article 1) and
contribution anchoring are different questions, and the admission rule above
keeps them consistent.

### 2.4 Runs consume facts, not inputs — structural enforcement

Four walls, three of them already committed:

1. **No raw-input citizen exists.** The entry batch (keystrokes, staged
   values) is transient, exactly as proposals are (Ontology §3, E2.1): the
   workspace keeps no store of it, nothing reads it, nothing hardens. What is
   preserved verbatim is the `capture` inside each finding (Article 2). A
   thing with no schema and no store cannot be consumed (Article 10 read in
   reverse).
2. **The run context is finding-shaped by type.** `RunContext` (committed,
   `packages/derivation/runner.py`) enumerates everything a run reads:
   rules, parameters, canon, `InputFinding`s, `SourceFact`s, closure record
   state, pins. There is no evidence field, no contribution field, no raw
   field. Probed: constructing a `RunContext` with a `raw_inputs` argument is
   a `TypeError`; constructing an `InputFinding` without a `finding_id` is a
   `TypeError`. The invariant is enforced by the shape of the type, not by a
   check inside it.
3. **Absence blocks; it never falls through.** Probed on the committed
   runner: withhold one finding while its value sits in scratch evidence
   content — the dependent rule blocks `DEPENDENCY_ABSENT`, publishes
   nothing, and the disposition is recorded. The raw value was reachable in
   the workspace directory and the runner still could not consume it,
   because no door exists.
4. **Contribution is not a permissible rule dependency.** E14.2's static
   check (rule dependency declarations vetted against register kinds)
   extends to exclude the contribution kind alongside records. A rule
   declaring a contribution input fails validation before it ever runs.

Production condition (named, not claimed at Rung 2): the only constructor
path for a live `RunContext` must be the marshal layer over projected record
state (`marshal.py` pattern), made structural in the D3 resolver — a caller
hand-assembling `InputFinding`s with invented ids is the remaining soft spot,
today confined to synthetic scenario fixtures.

## 3. D2-P2 — Manual entry, any order, correction by supersession

### 3.1 The event, without a wizard

One contribution = one act sequence the user initiates with any batch:

```
contribution (anchors document D, mode manual-entry)
evidence-submitted (D itself, if not already on record)
member-transition | assertion   × one per value      (ADR-0023 routing)
contribution-record (the session account, Article 14)
```

There is no forced sequence between contributions and no step-completion
dependency inside one: each act is a complete transition (Article 6), a
batch abandoned halfway leaves the workspace incomplete-never-wrong, and the
only intra-batch ordering is reference integrity (the contribution and
evidence must be on the record before a finding pins them) — the same class
of constraint findings already have toward evidence, not a flow. A design
that required source families to be entered in a fixed order would violate
the foreclosure clause; this one cannot express such a requirement, because
no act consults any other family's state.

**Any-order, probed (mandatory case 3).** Two scratch workspaces, identical
declarations, then a synthetic W-2 batch and a synthetic 1099-INT batch
applied in opposite orders. The full read models (current findings, facts,
histories, open facts, horizons) are **equal as values**. Commutativity is
structural: independent contributions touch disjoint family horizon chains
and disjoint facts, and currency is derived from the record, not from
arrival order.

### 3.2 Correction by supersession (Article 7)

A corrected value is a **new contribution** (new act, new contribution
citizen, usually new evidence — the W-2c), producing a plain `assertion` of
the same fact. Probed: currency moves to the correcting finding; the prior
finding remains on the record, non-current, with its original contribution
provenance intact; both contributions stand; the family horizon does **not**
advance (ADR-0023: same-member corrections take the assertion path — closure
authority survives a value correction). Displacement of any dependent derived
findings propagates along the existing derivation edge; nothing is edited,
nothing is withdrawn by hand, and no third mechanism appears. Removing a
wrongly-entered member is the already-committed `member-transition` remove —
also a later act, never an edit.

## 4. The six Gate-2 cases

Each: claim → contract change → kernel/derivation behavior → produced fact
and provenance pins. Probe script: `probe_d2_it2.py` (throwaway, scratchpad;
15/15 checks pass; synthetic values 41000 / 230 / 42000).

1. **Contribution produces provenance-bearing facts.** Claim: a manual W-2
   batch yields member-transition findings pinning contribution + document +
   version. Change: diffs 1–3 (§2.1). Behavior: probed at the committed
   layer — evidence + member-transition admit finding `demo-f-w2-a1`
   (41000) on fact `…box1-wages|w2-slip=demo-slip-a1…`; the paper layer adds
   `contribution_id` to that finding and the admission consistency rule.
   Pins: finding → contribution `demo-c1` → evidence `demo-ev-w2-a1` (id =
   version) → admitting act.
2. **Runs consume facts, not inputs (mandatory kill-test).** Claim: a run
   has no path to raw inputs. Change: none — committed shape, plus the E14.2
   extension. Behavior: probed — value present only as raw content, rule
   blocks `DEPENDENCY_ABSENT`, zero publications; with the finding present
   the same rule publishes, and every input/choice pin on the published
   derived finding resolves to a real finding id. Rejection is structural
   (§2.4), not policy.
3. **Any-order equivalence (mandatory).** §3.1; read models equal as values
   under opposite batch orders; no step consults another batch.
4. **Correction by supersession.** §3.2; probed: current finding is the
   correction, prior retained non-current, both on record, horizon unmoved.
5. **Contribution stays in quarantine (D1 kill-test).** Claim: a
   contribution writes only into `L`. Change: none — ADR-0031 is consumed,
   not reopened. Behavior: the contribution appender receives the `L`
   locator solely as the runtime capability (ADR-0031 Decision 1); the
   ordinary environment cannot construct it, and a live run mounts the
   repository read-only, so a repo-directed write fails at the OS wall even
   if reached. Every contribution artifact (acts with real values, the
   contribution record, the log) has personal provenance →
   `NEVER_CROSSES` (Decisions 2, 7); the commit/push envelope gates are the
   independent backstop. Probed at Rung 2: the residency relation predicate
   (canonicalized ancestor/descendant disjointness) accepts the scratch `L`
   and rejects a repo-internal path; scratch workspaces lived outside the
   worktree throughout and `git status` shows no repository change.
6. **Run reaching a raw input (mandatory kill-test).** Claim: it cannot
   silently succeed. Behavior: probed three ways — `raw_inputs` kwarg is a
   `TypeError`; a findingless `InputFinding` is a `TypeError`; a withheld
   finding blocks loudly with a recorded disposition (case 2). The failure
   is a rejection or a block, never a silent read: there is no code path
   from `RunContext` to evidence content or to any contribution payload.

## 5. Residuals and production conditions (named for Track 2 / D3)

- **Fold-before-append.** Probe observation: `ActLog.append` validates
  schema and revision only; semantic admission (`FindingModelError`) fires at
  projection. The production contribution appender must project current
  state and apply the candidate act *before* committing it, so an
  inadmissible act is refused rather than poisoning later folds. (Kill-probes
  here were run as folds for exactly this reason.)
- **Marshal-only run construction** (§2.4) — discharged by the D3 resolver.
- **E14.2 static-check extension** to the contribution kind — Track 2.
- **Contribution-record kind registration** and its sensitivity handling
  (never leaves `L`) — Track 2, under ADR-0031 Decision 7.
- **No grant is involved**: manual entry is the user acting directly, not a
  consultative process (Article 16 untouched). An OCR mode later will need a
  grant + consultation record; the contribution shape above already leaves
  the seam (mode enum, proposals→capture path).

## 6. Alternatives rejected

- **Composite batch act** (one act carrying the whole entry batch): rejected
  — it re-nests existing act kinds inside a generic container (E10.1),
  duplicates admission semantics, and makes batch atomicity a transaction
  where Article 6 wants complete-per-act increments.
- **Contribution reference in the act envelope only** (no finding field):
  rejected — Article 12 pins live on findings, and the explanation walk
  (Article 15) reads finding pins; burying provenance in the envelope makes
  the walk archaeological.
- **Raw batch persisted as a staged citizen** ("entry session" store):
  rejected — a load-bearing pending store (E2.1, E5.2) and the very thing
  the runs-consume-facts invariant exists to foreclose; if it existed, a
  path to it could be built.
- **Contribution as supersedable citizen** (edit/void a contribution):
  rejected — it would create a third displacement root; correction is a new
  contribution, and history only accumulates (Article 7).

## 7. Divergence note

Sealed from the incumbent; no comparison was possible. Positions most likely
to be genuine committee signal if the incumbent chose otherwise: the
contribution as a *thin anchor citizen carried by its own act* rather than a
batch-carrying event; provenance as a plain `finding.v2` field explicitly
kept out of `pins` and out of the edge doctrine; the raw batch as
deliberately unstored (transience, not encryption or quarantine, as the
enforcement); and fold-before-append as a named appender obligation.
