# Track 0 findings — Nominee Allocation Assertion Recording

Working record. **T0-A is complete. T0-B and T0-C are not begun.**

Per-candidate detail is in `findings-candidate-1.md` and
`findings-candidate-2.md`; the executed probes are under `probes/`.

## T0-A — lifecycle mechanism selection

Two builders worked disjoint candidates against the real committed kernel. The
Foreman re-ran both probes independently; both reproduce.

| Case | Candidate 1 — individuated entity | Candidate 2 — source family |
| --- | --- | --- |
| A2 one owner | PASS | PASS |
| A3 several owners | PASS | PASS |
| A4 correct one owner, record identity | PASS | PASS |
| A5 same payer, two reports | PASS | PASS |
| A6 withdraw honestly | PASS | PASS |
| A11 re-assert after withdrawal | PASS, at a new fact id | **FAIL** |

### Convergent result: no route re-asserts at the same fact id

Both candidates were probed independently and reached the same wall. Nothing in
the kernel reactivates a withdrawn fact identity — there is no "reactivate"
applier, and each route forecloses it differently:

- **Candidate 1.** `facts.facts_of` projects facts only for currently-standing
  entities, so after the allocation entity is superseded its fact id is not
  merely closed but **absent from the lattice**. Asserting onto it is rejected
  with `finding references unknown fact`; re-superseding is rejected with
  `entity is not current`.
- **Candidate 2.** `state.withdrawn_fact_ids` grows by union only and a second
  removal is refused (`member fact already withdrawn`). A member-transition
  assert of the withdrawn id *writes a finding* yet still does not make it
  current — currency marks the new finding displaced and
  `_current_value_for_fact` still returns the sentinel. SC-R1 refuses plain
  assertion both on first entry and after withdrawal.

All three kernel claims the plan asserted **held under execution**.

### Where the candidates diverge: what a new fact id costs

Both need a new fact id for A11. The difference is what that does to per-owner
identity, and it is decisive.

- **Candidate 1** never put `(report, owner)` on the fact identity in the first
  place — each owner is a separate entity from the start. Re-assertion
  introduces a new allocation entity and asserts fresh. It becomes current, and
  **A4's per-owner separation is untouched**, because that separation never
  depended on the fact key.
- **Candidate 2** *does* key the fact on `(report, owner)`. Making a new id
  requires an extra `instance` component — after which **two Pat fact ids exist
  for the same report and owner** and the original stays permanently exhausted.
  That abandons the identity A4 depends on.

### Candidate 2 is independently disqualified on authority

`source-family.v2` **requires** `closure_claim` and `authorizes_subtotal`; a
family omitting them was rejected under execution, and empty strings also
failed. Hedged "recording-only" wording does schema-validate — but that is not
an honest instance, because those fields *are* a completeness claim about the
world and a subtotal authorization. Every transition additionally requires a
successor horizon citizen.

A recording-only milestone does not hold tax-consequence authority. **Candidate
2 is disqualified, not renegotiated.** This is independent of its A11 failure;
either alone would disqualify it.

### Candidate 3 not built

The charter authorizes a dedicated assertion-end act only if candidates 1 and 2
both fail. Candidate 1 did not fail. Candidate 3 was correctly not built.

### T0-A verdict

**Candidate 1 — the separately individuated allocation-statement entity, ended
by `act-entity-superseded.v1` with `replacement` omitted — is the surviving
mechanism.** It satisfies A2–A6 and A11, keeps owners uncoupled, retains full
history, and takes no authority the milestone lacks.

Attribution join, executed: `finding_id` → the committed act whose
`payload.finding.id` equals it → `act['actor']`, `act['at']`. **No actor or time
field exists on the finding citizen itself.** Every finding ever recorded was
retained; withdrawal removed currency, not history.

## T0-A findings carried forward

**T0-G1 — enforcement readers do not see entity supersession.**
`_current_value_for_fact` (`packages/kernel/findings.py:169-183`) consults only
`state.withdrawn_fact_ids` and never entity supersession. It has **eight call
sites** — gate values, subordinate/dominant subset invariants, and
companion-presence checks (`:235`, `:284`, `:287`, `:361`, `:371`, `:416`,
`:417`, `:451`). Under candidate 1, a withdrawn allocation is correctly absent
from read-model currency but would still yield a **current value** to any of
those enforcement paths.

No rule is declared over this fact type today, so nothing is presently wrong.
But the **next** milestone derives a nominee consequence from exactly this fact
type. If it declares a gate, subset invariant, or companion requirement over
allocation facts, enforcement would silently disagree with true currency and a
withdrawn allocation could still support a tax reduction.

**Disposition: owner disposition required.** This is not disposed here.

**T0-G2 — re-assertion is not linked to the withdrawal it follows.** Under
candidate 1, A11 produces a genuinely new fact id with no kernel-level link back
to the withdrawn one; the relationship is recoverable only by matching labels or
domain convention. The act log preserves the **order**, so "withdrawn, then
asserted again" is recoverable as a sequence — but "this statement replaces that
withdrawn one" is not an identity the kernel carries. T0-B must decide whether
the product needs to say that, and record the answer rather than inherit it.

**T0-G3 — `ActLog.append` validates shape, not semantics.** Append alone
performs JSON-Schema validation only; any writer must pre-apply semantically, as
`entry_loop.py` already does. Track 1 must not treat a successful append as
evidence that an act was accepted.

---

## T0-A′ — re-run after the rebuild onto ADR-0073

This milestone was rebuilt onto **Assertion Standing and Retraction Semantics**
(closed 2026-09-06, ratified by ADR-0073). T0-A above compared candidates 1 and
2 **before that contract existed**. It is retained as the record of why those
two routes were rejected; its verdict is superseded by this section.

`probes/candidate-4-retraction.py`, executed against the real committed kernel.

| Case | C1 entity | C2 family | **C4 retraction** |
| --- | --- | --- | --- |
| A2 / A3 / A4 / A5 | PASS | PASS | **PASS** |
| A6 withdraw honestly | PASS | PASS | **PASS** |
| A11 re-assert | new fact id | **FAIL** | **PASS, same fact id** |

### Why candidate 4 wins outright

Both earlier candidates failed the same way: they removed the **fact**, so the
proposition itself stopped existing and the identity had to be abandoned to
re-assert. Retraction ends the current support of one **finding** and never
retires the fact. The proposition survives, so:

- **A11 succeeds at the same `(report, owner)` fact id** — the identity neither
  earlier candidate could keep. Executed: retract `demo-f-pat-2`, then assert
  `demo-f-pat-3` on the identical fact id; it becomes current at `275`.
- **A6 stays honest.** The retraction payload is exactly `{"finding_id": ...}`.
  No value, replacement, or opposite claim is expressible. Both prior findings
  remain in history; Kim is untouched.
- **Revival by id reuse is still refused** (`finding already exists`), so
  history cannot be rewritten by re-using an id.

### T0-G1 — CLOSED by ADR-0073 Decision 5

The two current-standing readers now agree. Executed: after retraction,
`_current_value_for_fact` returns `<NO_CURRENT_VALUE>` and read-model currency
also reports the fact as not current. ADR-0073 Decision 5 unified every reader
onto the single `compute_currency` projection, which is exactly the defect T0-A
recorded as needing owner disposition. **No disposition is required; nothing is
carried into the tax-consequence milestone on this account.**

### T0-G2 — CLOSED

The retracted finding's displacement reasons are
`(correction by demo-f-pat-3, retraction by demo-act-010)`. Both the retraction
act and the finding that followed it are recoverable **by identity**, not by
label convention. ADR-0073 Decision 7 explains why the act id rather than the
fact id discriminates: a fact can be retracted, re-asserted, and retracted
again.

One product-meaning nuance for T0-B: the re-assertion is labelled a
**`correction`** of the retracted finding. That is the kernel's last-writer-wins
labelling and is not wrong, but "retracted, then answered again" and "corrected"
are different things to a reader, and the durable text should not conflate them.

### T0-G3 — still open, unchanged

`ActLog.append` validates shape, not semantics. The retraction milestone did not
change this. Track 1 must pre-apply semantically, as `entry_loop.py` does.

### Constraints this milestone now inherits from ADR-0073

1. **The allocation fact type must not be `locked`.** Decision 3: `locked`
   refuses retraction unconditionally, because a single-shot fact whose one
   answer was ended has no remedy. The probe uses `free`.
2. **Declaring an admission invariant over the allocation fact would fence its
   own retraction.** Decision 8: the sixth refusal re-runs the four admission
   enforcers over the prospective post-retraction state, which is what fences
   fifteen fact types today. If this milestone declares a subset, companion, or
   declaration/signal relation involving the allocation amount — the obvious
   temptation is A8, over-allocation against the report amount — it would make
   its own retraction inadmissible. **A8 says preserve what was asserted and do
   not clamp, so no such invariant should be declared. This must be a stated
   contract decision, not an accident.**
3. **An admitted retraction does not mean the original author withdrew.**
   Decision 3 is explicit: any recorded actor may end support for any finding
   the state gate permits, and admission never consults actor identity. See the
   open question below.

### T0-G4 — the one gap the retraction milestone left for this one

**A6's product meaning and the kernel's retraction meaning are not the same
statement, and this milestone is the first place that difference bites.**

This milestone's A6 is *"the user withdraws Pat's allocation"* — a named person
taking back **their own** ordinary statement. That is the whole subject of the
milestone: an attributed personal assertion and its lifecycle.

What ADR-0073 Decision 3 actually delivers is narrower: **a recorded actor has
ended the workspace's current support for one identified finding.** Admission
never consults actor identity; who retracts is envelope provenance only. The ADR
states plainly that this "does not establish that the finding's original author
personally withdrew their statement," that durable text "must not claim the
original person no longer stands behind the answer," and that whether ending
support should require the original author is "a real product question,
unanswered here."

For the retraction milestone that deferral was reasonable — it was building a
substrate contract, and answering would require the identity concept ADR-0041
deliberately declined to build. But this milestone cannot inherit the deferral
silently, because:

- A6 and exit criterion 5 are written in the user's voice, and the mechanism
  cannot carry that meaning;
- the milestone's exit criterion 3 requires attribution to be preserved, and
  attribution of the *retraction* is provenance the contract says is not
  load-bearing;
- any reader-facing wording this milestone produces would be the first text in
  the product tempted to say "you withdrew this," which ADR-0073 forbids.

**This is not a defect in ADR-0073 and does not reopen it.** It is a product
question that milestone consciously left open and that this milestone is the
first consumer to actually need. It is owner-held, and it is the single
outstanding decision blocking a clean T0-B.

---

## T0-B — contract selection and instantiation

### The seven contract decisions

1. **Canonical proposition.** One fact type,
   `<ns>.nominee-allocation.amount`, `nature: determinable`: *the amount from
   one identified Form 1099-INT report that the asserting person says belongs
   to one named other person.* The value is the amount alone. No field
   expresses a nominee characterization, a Schedule B consequence, or a
   reporting conclusion, which is what makes exit criterion 1 checkable
   structurally rather than by prose.

2. **Identity and cardinality.** Identity keys are exactly
   `report` (entity kind `…report-1099int`) and `owner` (entity kind
   `…person`). Executed: A3 distinguishes owners, A4 corrects one without
   touching the other's record, A5 keeps two same-payer reports apart, and
   **A11 returns to the same fact id**. No allocation-entity indirection and no
   `instance` component — both were forced by candidates 1 and 2 and are
   unnecessary once retraction ends a finding rather than the fact.

3. **Report association: name the report directly (R-A).** The user's statement
   is *about* an identified report, so the report is an identity key rather
   than a matched association.

   **Checked against ADR-0068, which P2 did not read.** ADR-0068 does not bind
   this. Its association exists because an *acquisition* and a *report* are
   separately known and must be matched — Decision 4's two tiers, Decision 5's
   separately answered `confirmed_report_match`. Here there is nothing to
   match: the report is named in the statement itself. Two properties of 0068
   are nevertheless inherited deliberately: its association is **derived and
   re-evaluated, never a stored independently corrected object** (Decision 7),
   and **tax arithmetic stays out** (Decision 9). Both hold here.

   R-A versus R-B is therefore **not** reopened. A6/A11 discriminated the
   lifecycle candidates, not the association shapes.

4. **Act and basis.** No new act kind. `act-assertion.v2` carries the finding;
   `basis: "attested"` with `nature: "determinable"`, the committed precedent at
   `packages/tax/obligation_acquisition_mapping.py:599-601` for a statement about
   one's own circumstance. The actor comes from the act envelope supplied by the
   caller and is never manufactured by a mapper.

5. **Lifecycle.** `act-finding-retracted.v1` ends the current support of one
   identified finding. Payload is exactly `{"finding_id": …}`, closed, so no
   replacement value or opposite proposition is expressible. Supersession policy
   is **`free`**; `locked` would refuse retraction outright (ADR-0073 Decision 3).
   Asserting again afterwards uses the ordinary assertion path at the same fact
   id.

6. **Attribution recovery.** `finding_id` → the act whose `payload.finding.id`
   equals it → `actor`, `at`. For a retraction, the displacement reason
   `("retraction", <act id>)` → that act's envelope. Executed: an assertion by
   `demo-user-matt` and a retraction of it by `demo-user-alex` are recovered as
   **two distinct actors and times**, with the original assertion still in
   history. That is the provenance separation the owner's selected operation
   requires.

   **The limit is preserved exactly.** Admission never consults actor identity;
   the different-actor retraction was **admitted**. This records provenance, not
   enforcement, and is not evidence that the original author recanted. A
   same-actor case is also exercised and is explicitly *not* offered as proof
   that same-author retraction is required or checked.

7. **Packaging boundary.** One content bundle declaring the fact type and the
   two entity kinds. **No source family, no `closure_claim`, no
   `authorizes_subtotal`, no horizon.** No cross-fact admission invariant
   against the report amount — a scoping decision for this milestone only, not a
   claim that retractable facts cannot participate in invariants.

### Payload Instantiation Gate — discharged

Two committed positive instances, both validated against the published schemas
by `SchemaRegistry` and both folded through the real kernel by the probe:

- `instances/act-assertion-allocation.v1.example.json` → `act-assertion.v2`
- `instances/act-finding-retracted-allocation.v1.example.json` →
  `act-finding-retracted.v1`

Resolution stopped at `finding.v2` and `act-finding-retracted.v1`, both of which
already carry committed positive instances; those are cited, not re-expanded.
**No invariant collision and no reserved-boundary contact.** `basis` is the only
field that could have collided, and `attested` carries it honestly.

### The three carried questions — settled

1. **Track 2's production/coordinator boundary: it exists.**
   `packages/kernel/contribution.py::apply_contribution_batch` is the real
   admission boundary, and
   `packages/tax/obligation_acquisition_mapping.py::contribute_ordinary_acquisition`
   is the precedent producer that maps ordinary answers and admits them through
   it in one step. Track 2 binds to that boundary and is an **integration task,
   not a contract decision**.

2. **A10's routing owner: none exists.** A search for erroneous-report or
   document-correction routing across `packages/` returned **no module at all**.
   A10 is therefore a boundary this milestone can state but **cannot
   demonstrate**. Stated honestly: A10's requirement is narrowed to *no
   nominee-allocation assertion is written for an erroneous-report answer* —
   a negative this milestone can show. Where such an answer should instead be
   routed is **not this milestone's to establish**, and no claim that routing
   exists may be made.

3. **ADR-0067 and ADR-0068: read, and they do not disturb decisions 2 or 3.**
   ADR-0068 as above. ADR-0067 concerns a `field` selector on `ref_expr` for
   rules reading canonical acquisition fields; this milestone publishes no rule
   and reads no field, so it does not apply.

### T0-B verdict

The contract is selected and instantiated with no stop condition reached. No
product requirement for personal recantation or actor-specific permission has
surfaced: every case is satisfied by ordinary removal from current workspace
use. T0-C may proceed.

---

## T0-D — design repair, and a correction to T0-B/T0-C

Owner direction 2026-09-07. The probe was rewritten against the **committed**
Form 1099-INT identity model and rerun; all results below are executed.

### The selected workspace model, stated explicitly

The canonical fact is **one shared current workspace answer** per identified
payer report and named allocation recipient. It is **not** a separately
individuated personal statement belonging to its author.

Each assertion or correction act records **which actor supplied that answer and
when**. A later recorded actor may replace or retract the current answer.
History preserves every actor and value. **None of this establishes that an
earlier actor recanted or changed their belief.** Actor is provenance only; the
kernel enforces no permission.

A product needing several users' independent assertions to coexist would require
an **author-indexed proposition** with conflict and reconciliation behaviour.
**Deferred** until a concrete collaborative use case requires it.

### Vocabulary, now used consistently

| Term | Meaning |
| --- | --- |
| **actor** / workspace operator | the person recorded on an act (Matt, Alex) |
| **allocation recipient** / named other person | Pat, Kim — the person interest is allocated to; **never an author here** |
| **taxpayer** / workspace subject | the person whose return this is |
| **payer report** | the documentary Form 1099-INT box-1 report |

Earlier passages saying "Pat changes `$300` to `$250`" and "Kim's original
assertion act" were **false**: Pat and Kim are recipients, and every act in the
probe was authored by a workspace actor. Corrected throughout.

### The canonical proposition no longer embeds its speaker

The fact type's question is now:

> *The amount of interest reported on this identified Form 1099-INT that is
> allocated to this named other person.*

The finding supplies the current answer with `basis: "attested"`. The enclosing
assertion act supplies **who** stated it and **when**. A later tax rule — not
this fact — decides any nominee-interest consequence. The prior wording ("the
amount the asserting person says belongs to…") violated the predecessor
milestone's separation of proposition from authorship and is withdrawn.

### Report identity is now the committed one — the material repair

The earlier probe **invented** `demo.report-1099int` and never touched the
committed model. It now adopts the committed
`packages/content/tax/2025/f1099int.bundle.json`, performs horizon genesis for
family `tax.us.2025.f1099int.b1`, and contributes the documentary box-1 report
through `contribute_1099int_report` → `apply_contribution_batch` — the real
admission boundary. Admitted: `completed`.

Allocation identity is keyed **payer + statement + tax-year + recipient**, with
payer and statement derived by the committed document-side conventions in
`packages/tax/report_statement_identity.py`:

```
box1:       tax.us.2025.f1099int.box1-interest|payer=Demo Savings Bank,
              statement=Demo Savings Bank::statement::demo-stmt-a,tax-year=2025
allocation: demo.nominee-allocation.amount|payer=Demo Savings Bank,
              statement=Demo Savings Bank::statement::demo-stmt-a,tax-year=2025,
              recipient=demo-recipient-pat
```

`tax-year` is a **literal** identity key, matching the committed bundle's own
shape; a `scalar` key was refused by `fact-type.v1`.

| Required demonstration | Result |
| --- | --- |
| Two reports from the same payer stay distinct (A5) | **PASS** — statements A and B differ |
| Same statement reference, different tax year, no collision (A5b) | **PASS** — 2025 and 2024 differ |
| Box-1 correction does not detach the allocation (A7) | **PASS** — `1200.0 → 1300.0` at the same box-1 fact id; the allocation stays current |
| Allocation joins the exact current box-1 finding a rule would consume | **PASS** — shared payer/statement/tax-year components |

A7 also surfaced a real mechanic: correcting an existing family member goes on
the **ordinary assertion path**, not another member-transition (SC-R2).

### Cross-actor behaviour — both directions

| Case | Result |
| --- | --- |
| A4 — a workspace actor changes the allocation to Pat from `$300` to `$250`; the current allocation to Kim remains the identical finding, supported by the same original assertion act and actor | **PASS** |
| **A4b — cross-actor correction.** Matt supplies `$300`, then `$250`; Alex supplies `$275` at the same fact identity. Matt's finding becomes historical and remains present; Alex's is current; both actors and times recoverable | **PASS** |
| **A6 — cross-actor retraction.** Alex removes from current use the allocation to Pat that Matt previously supplied. The current allocation disappears; Matt's assertions remain historical; Alex's retraction is separately recorded | **PASS** |
| A11 — assert again at the same fact identity afterwards | **PASS** |

**This is shared-workspace revision behaviour, not evidence that Alex speaks for
Matt, and nothing here says Matt recanted.** The kernel enforces no permission
to perform the edit: admission never consults actor identity, and the
cross-actor correction and retraction were both simply **admitted**. Actor is
provenance only.

### Corrections to T0-B and T0-C

- **The claim-reuse proof in T0-C was FALSE and is withdrawn.** It stated that
  "the payer report fact … is read as the report identity." The probe at that
  time read no report fact; it minted an unrelated demo entity. **Corrected
  claim, now true and executed:** the allocation *shares the box-1 report's own
  identity components* — payer entity, statement entity, tax year — derived by
  the committed convention, with the documentary report admitted through the
  real boundary in the same probe. It is a **shared identity**, not a derived
  association, and it does not restate or redefine the box-1 proposition.
- **The Payload Instantiation Gate was not fully discharged at T0-B.** The two
  committed instances proved generic schema validity but used the invented
  report entity, so they did not instantiate the selected production
  report-association shape. The instances are regenerated against the committed
  identity below.
- **R-A is bounded honestly.** A direct report-linked fact is appropriate for
  this report-specific production slice. It **does not refute or permanently
  reject R-B.** *R-B remains deferred* for a future case involving an allocation
  known independently of a particular report, or one that must survive
  report-identity replacement.
- **The ADR-0068 "derived and re-evaluated association" claim is withdrawn.** A
  direct shared identity is not a derived association, and that property does
  not hold here. ADR-0068 Decision 9 (tax arithmetic stays out) does still hold,
  and is retained on its own terms.

---

## T0 status — what the probe does and does not establish

Stated here so no later track over-reads it.

**Established** against the committed kernel and the committed Form 1099-INT
report identity: the four-key allocation identity; correction, cross-actor
correction, retraction, and assert-again at the same identity; that both
current-standing readers agree; and that box-1 correction does not detach the
allocation.

**Not established.** The probe does **not** prove the production producer, the
contribution path, recipient identity, or the persistence contract. It builds
acts directly and folds state in memory. Specifically:

- **Recipient identity was unresolved; it is now settled by owner decision
  (2026-09-07).** The probe introduces `demo.person` entities by hand. **No
  committed natural-person or allocation-recipient entity kind exists** — the
  corpus does carry obligations, pairings, family horizons, and adjustment
  instances, so it is not only institutions and statements. The committed
  institution convention derives identity from trimmed display text, which would
  make correcting a misspelled recipient name produce a *different* fact
  identity. **Selected instead: an application-minted opaque workspace recipient
  id**, under a bounded role-specific entity kind, with the typed name recorded
  as a non-authoritative display label. Entity labels are immutable
  (`packages/kernel/facts.py:122`, `:128-144`), so **display-name correction is
  deferred**, with a concrete need to edit labels without displacing
  recipient-linked facts as the reopening trigger.
- **`apply_contribution_batch` cannot carry a retraction.** Its successor kinds
  are exactly `{"assertion", "member-transition"}`
  (`packages/kernel/contribution.py:21`). The production retraction surface is a
  separate bounded operation Track 1 must build; the probe's direct
  `findings.apply_act` call is not that surface.
- **Production content is `bundle.v2` / `fact-type.v2`**, per
  `packages/content/tax/2025/f1099int.bundle.json`. The probe's
  `bundle.v1` / `fact-type.v1` is a demo shape, not the production precedent.
- **Attribution must not be copied from the cited precedents.** Both
  `report_statement_identity.py` and `obligation_acquisition_mapping.py`
  hard-code `"actor": "user"`. They guide contribution shape only.
- **The probe holds state in memory.** `apply_contribution_batch`'s returned
  state is an in-memory fold, not evidence of durable persistence. A real
  round-trip through `ActLog` and back is Track 1 evidence, not Track 0's.
