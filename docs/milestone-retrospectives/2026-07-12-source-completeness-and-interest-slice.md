# Retrospective — Source Completeness And Interest Slice

- Milestone: Source Completeness And Interest Slice (Foundation phase)
- Branch: `milestone/source-completeness`
- Merge commit: `382a7af` (non-ff into `main`, 2026-07-12)
- Implementation commits: Track 1 `9797b66`, Track 2 `e4a0e4d`, Track 3
  `41a9948`, Track 4 `871ae60`, Track 5 `7cab080`, plus this Track 6
  completion-documentation commit `4c16360`.

## Shipped

The reusable closure/horizon authority substrate plus the first honest
taxable-interest content: a Form 1099-INT box-1 subtotal and an
exact-claim coverage surface that cannot masquerade as total taxable
interest. Track 0 (three decision topics, ADR-0014 through ADR-0017) was
complete before this branch started; Tracks 1–5 were production
reimplementation from the ratified contracts, one commit each.

1. **Contract schemas** — `source-family.v1` and
   `source-closure-mapping.v1` in the derivation family;
   `family-horizon.v1`, `act-horizon-genesis.v1`, and
   `act-member-transition.v1` in the kernel family. The atomic
   transition states family/scope once, so a differently scoped
   successor is unrepresentable; half transitions fail required-field
   validation; the admission vocabulary is a one-value enum
   (`current-literal-true`). A W-2-flavored instance corpus proves the
   shapes are not interest-specific, and the admission-negative corpus
   (wrong/future predecessor, replayed successor, duplicate genesis) was
   committed in Track 1 as the agreed rejection contract Track 2 then
   satisfied.
2. **Horizon projection and currency** — `packages/kernel/horizons.py`
   folds horizon chains from accepted acts; member transitions are one
   pure state step (horizon half validated first, then the member half),
   so rejection is atomic by construction. Horizons project into the
   fact lattice as `kernel.family-horizon` entities, which makes
   succession an ordinary individuation root: closure findings keyed on
   a superseded horizon displace through the existing two edges, and
   `currency.py`'s edge model is untouched. Member withdrawal is a
   displacement root (like correction), never a third edge.
3. **Single dispatch** — `RunContext.closed_sets` is removed, not
   renamed. Admission is resolved inside the runner from adopted
   declarations/mappings plus marshalled record state; false, absent,
   displaced, truthy, duplicate, and missing-chain authority all leave
   the family unadmitted so the unchanged two-layer `collect` check
   blocks. Fabricated/duplicate/mismatched mappings raise loudly, and
   `audit_collect_authority` rejects any rule publishing a symbol its
   collected family does not authorize. A closure-backed zero pins the
   exact mapping and declaration versions and the exact closure finding
   (input role, so withdrawal cascades); present-source aggregation
   never consults closure. A source-scan test keeps any caller-carrier
   reintroduction from passing review silently.
4. **1099-INT box-1 content** — statement-instance identity (payer +
   logical statement + tax year, no evidence key kind exists to smuggle
   in), the first production closure fact type keyed on the family
   horizon, the exact B1 family claim with its line-2b non-claim stated
   inside the claim text, the adopted mapping pair-validated at load,
   one computation rule publishing `tax.us.2025.interest.b1-subtotal`,
   and `packages/tax/statements.py` for deterministic sameness,
   anti-duplication, and correction-versus-new-original classification.
   No form field binds the subtotal; no line-2b citizen exists.
5. **Lifecycle and coverage** — `marshal.py` (record state → run
   context) and `packages/tax/coverage.py`, which reuses the runner's
   own admission resolution so coverage and calculation can never
   disagree about closedness. One real act log proves the signature
   sequence: closure over the empty family publishes an explained zero;
   a late member's atomic successor makes the old closure and zero
   noncurrent with no manual withdrawal; removal resurrects nothing;
   re-attestation plus explicit rerun publishes the distinct successor
   zero. The closed-empty and open-empty dispositions are pinned as
   distinct CLI goldens.

Final verification: 314 tests, governance lint conformant, mypy clean,
two-runner byte parity on every scenario, data-safety scans including
account-identifier digit runs over interest content.

## Economic goals and outcome

The milestone set out to correct the prior prototype's main economic failure:
pay for the cheapest evidence capable of changing each decision, bound repair
and review growth, and prevent Track 0 from speculatively implementing the
milestone. The result is mixed but materially improved.

### What became cheaper

- **Evidence depth was proposition-specific.** Statement identity stopped at
  paper. Source-family semantics stopped at paper plus a static state table.
  Only closure admission/dispatch and late-member currency advanced to small
  executable probes. No proposition was forced through persisted integration
  merely because it shared an iteration with another question.
- **Losing designs were abandoned rather than repaired.** The embedded mapping,
  payer/account identity, computed-divergence freshness root, and broad line-2b
  interpretation were rejected once their discriminating failures were visible.
- **Prototype code stayed out of production.** The implementation branch began
  only after ADR-0014 through ADR-0017 were ratified. Tracks 1–5 then landed in
  the planned order, one green commit each, with no corrective implementation
  commit or planning rewrite on the milestone branch.
- **The contract-first implementation was economical.** From planning tip to
  Track 5, production changed 85 files with 4,239 insertions and 193 deletions.
  The negative corpus committed in Track 1 became Track 2's admission contract;
  later tracks reused the same horizon, mapping, finding, and scenario ids.
  Final verification remained 314 tests / mypy clean without a stabilization
  track.
- **Partial ratification worked.** ADR-0014/0015 were accepted while source-
  family semantics and freshness moved into smaller follow-on topics. This
  prevented adjacent uncertainty from invalidating settled decisions.

### Where the economic controls failed

The documentation budgets did not hold:

| Decision topic | Markdown lines | Plan target | Reviews |
|---|---:|---:|---:|
| Source Completeness | 3,816 | ≤1,800 | 11 |
| Source-Family Semantics | 1,764 | ≤900 | 4 |
| Closure Freshness | 1,841 | ≤1,200 | 5 |
| **Total** | **7,421** | **≤3,900** | **20** |

The decision sequence from the first Source Completeness planning commit through
ADR-0017 ratification spans 87 mainline commits. This is far smaller in code and
integration scope than the prior monolithic prototype, but it is not yet an
economical documentation process.

The main causes were:

1. **Caps operated as warnings, not design constraints.** The one-repair and
   Markdown targets were crossed, then reconciled through delegated continuation.
   The extra rounds found real defects, but the plan did not force consolidation
   of the evidence record after each stop-and-decide.
2. **Every repair tended to receive a full committee-shaped record.** Even when
   one prior finding alone was under test, round files, three reviews, triage,
   examination, seat, log, and handoff updates accumulated around it.
3. **The process counted document length but not duplicated restatement.** Short
   capped reviews caused reviewers to spend time trimming; removing the cap
   improved their work, but there was no replacement control on repeated context
   and evidence inventories.
4. **Runtime-surface acceptance was declared too late.** Source Completeness
   needed four repairs because successive designs proved sole use, then
   construction validation, then still exposed duck/alternate call paths. Naming
   the supported public dispatch surface in the first executable charter would
   likely have collapsed several rounds.
5. **A semantic question hid a machinery question.** The first source-family
   lifecycle assumed manual closure withdrawal. Only adversary review exposed
   that a future member required a new currency contract, creating the separate
   Tier-3 topic. The event that changes standing should have been declared in the
   original decision inventory.

### Medium-tier model assessment

The owner's subjective read is supported: Medium-tier models generally
functioned as well as expected from a higher-intelligence reviewer for these
bounded roles.

They successfully:

- found same-account identity collisions and correction rekeying;
- distinguished claim/member alignment from consistent mislabeling;
- found the undefined late-member withdrawal trigger;
- rejected a comparison-derived freshness root as a disguised third dependency;
- isolated the recorded-horizon rival and specified the exact reducer probe;
- reproduced incremental/rebuild equality and adversarial transition cases; and
- kept reviews scoped, independent, and evidence-cited after the briefs improved.

Observed misses included wrong output paths, evidence-level mislabeling, an
overstatement of Python privacy, one unsupported evolution claim, and a missed
computed-zero fixture. Those misses matter, but they did not correlate cleanly
with insufficient intelligence: explicit full output paths fixed the path issue;
fixture checklists and independent commands exposed the measurement issues; and
foreman sampling caught the overclaims. The Medium reviewers' substantive
adversarial contributions outweighed their defects.

Future allocation should therefore default bounded governance, adversary, and
expressiveness review to **Medium/medium** (currently GPT-5.6 Terra where model
selection is available). Reserve High/high for novel builder synthesis,
cross-proposition foreman triage, and genuinely open Tier-3 alternatives—not for
routine review by default. Capability should be raised only after a concrete
review failure, not because the decision is important in the abstract.

### Economic improvements for the next prototype

1. **Budget review operations, not prose lines.** No review line cap. Instead,
   each review gets a fixed measurement checklist, one independent reproduction
   budget, and a stop when every item is `pass`, `fail`, or `not run`.
2. **Use delta reviews after the first committee.** A repair review reads the
   prior finding and new exhibit only. Re-run the full committee only when the
   contract surface changes, not for every defect repair.
3. **Maintain one living evidence matrix.** Proposition × fixture × evidence
   depth × disposition should replace repeated evidence inventories across
   examinations, rounds, and triage documents. Preserve dissent as linked notes.
4. **Declare the supported public surface before executable work.** List every
   accepted constructor/entry and every forbidden alternate path in the charter;
   attack reachability in the first code round.
5. **Declare the standing-changing event in the paper charter.** Every lifecycle
   must answer what recorded act, citizen succession, or existing edge changes
   currency. Desired before/after states alone do not count as a lifecycle.
6. **Keep two default reviewers at Medium.** Add expressiveness only when code
   runs; add a third specialist only for a named uncertainty. Do not repeat a
   peer review merely to increase confidence after two independent measurements
   converge.
7. **Make cap crossings choose among three explicit actions:** conclude
   partially, split a new topic, or replace the current artifact set with a
   consolidated analysis. “Continue and keep every intermediate process
   document active” should not be the default fourth option.
8. **Measure decision-to-implementation conversion.** Track which production
   tests and contracts cite each accepted conclusion. An iteration is economical
   when it changes the final contract or kills a design; rounds that do neither
   trigger consolidation or stop.

## Decisions and deviations

- **Genesis act kind added (Tier 1).** ADR-0017 left act-kind names
  undecided; the empty-family closure scenario needs a current horizon
  before any member transition exists, so `horizon-genesis` establishes
  the chain and `member-transition` always requires a non-null
  predecessor. This kept the half-transition rejections structural.
- **Horizons ride the entity lifecycle.** Rather than a new fact-type
  key kind (which would have forced `fact-type.v2`), closure fact types
  key on horizon citizens through the existing entity key kind
  (`kernel.family-horizon`). The horizon citizen and its entity record
  are projections of the same acts — no second store.
- **Closure pins reuse published roles.** The `derived-finding.v1` pin
  role enum is immutable, so the mapping/declaration pin as `package`
  and the closure finding as `input` — which is also what routes
  displacement through the existing derivation edge. Horizon identity
  travels inside the pinned closure finding's fact key rather than as
  its own pin.
- **`collect.source_set` now names the family declaration id.** One
  string drives admission, the subtotal-authority audit, and
  explanation pins. Legacy demo/W-2 source-set names were preserved by
  giving demo fixtures family ids equal to the old strings; the W-2
  family itself remains unmapped (its empty collect still blocks),
  which is the honest state until a W-2 closure mapping is adopted.
- **Kernel does not police predicate membership.** A member asserted
  through a plain assertion act (outside any transition) would not
  advance the horizon; the kernel cannot see member predicates (adopted
  content). Routing membership changes through transitions is the
  contract of the layers that consume the declaration — recorded here
  as a known boundary for the workspace-service layer to enforce.

## Data safety

All committed fixtures are synthetic and publishable: manufactured
payers ("Bank Alpha Savings"), statement references, and amounts. The
data-safety test forbids private path markers and long digit runs
(account-identifier shaped) across interest content, with hex
lookarounds exempting content-addressed hash ids.

## Follow-ups

- Adopt a W-2 closure mapping so the W-2 family gains the same
  closure-backed-zero path (currently only 1099-INT B1 is mapped).
- Workspace-service enforcement that member-predicate-matching
  assertions route through member transitions (kernel boundary noted
  above).
- Roadmap item 7 (downstream lines) still owns line 2b: it requires a
  broader taxable-interest universe or a proven coextensive composition
  per ADR-0016 before any line-2b publication.
- SFS-P3 late-member freshness follow-on was resolved by ADR-0017; the
  Tier-3 record is closed.

## Planning lessons

- Committing the admission-negative corpus in Track 1 as schema-valid
  instances gave Track 2 a fixed rejection contract to satisfy — the
  Payload Instantiation Gate generalized from positives to negatives,
  and it caught the validation-order question (horizon half first)
  before any machinery existed.
- The five-track shape (schemas → kernel machinery → dispatch →
  content → lifecycle) let every track end green with the full suite,
  because each track's consumers arrived only after its contracts were
  already published and tested.
- mypy caught a leaked loop variable in the admission resolver that the
  tests could not, because the fixture had exactly one family. Fixture
  diversity, not suite size, is what exercises resolver code paths —
  worth remembering when the family count grows.
