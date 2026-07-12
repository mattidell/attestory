# Tax Citizen Families Prototype - Process Log

Dated incident and event entries, written as they happen, never reconstructed.
Categories: hollow measurements, context leaks, no-progress iterations, charter
drift, wordsmithed dissent, role breaches, foreman errors, successions,
dispositions.

---

- **2026-07-11 (event)** - Process opened for First Tax Slice Track 0 after the
  planning commit `021569f`. Dispatch infrastructure committed: seat file,
  charter, roles, and round-0 review stub. Foreman seat held by the session that
  wrote the First Tax Slice plan. Known tension recorded at open: the foreman
  drafted the charter and process files, so round 0 reviews must measure fixture
  selection before any builder seat opens.

- **2026-07-11 (event, governance reviewer)** - Generic resumption claimed the
  open governance-reviewer seat for round 0. No same-round peer review or
  commit-message body was read before the review; one reviewer seat is held by
  this identity in this round.

- **2026-07-11 (event, governance reviewer)** - Governance review submitted at
  `reviews/round-0-governance.md`; the governance seat is complete. The review
  recommends two evidence-strengthening charter amendments before builder
  dispatch: an explicit evidence removal/re-upload peerage probe and strict
  validation/rejection results for positive and negative instances.

- **2026-07-11 (event, adversary reviewer)** - Generic resumption claimed the
  open adversary-reviewer seat. No same-round peer review or commit-message body
  was read before submission; one reviewer seat is held by this identity in
  this round.

- **2026-07-11 (event, adversary reviewer)** - Adversary review submitted at
  `reviews/round-0-adversary.md`. Six charter attacks remain open: 1099-INT
  edge semantics, document/fact identity collision, absence and invalidity,
  citation authority, cross-year evolution, and recomputable coverage. The
  review recommends charter amendments before builder dispatch; round-0
  disposition remains with the foreman/owner.

- **2026-07-11 (incident: identity ambiguity / process gap)** - Both completed
  round-0 review records and `SEAT.md` identify their holders generically as
  `codex (resume session, 2026-07-11)`. The process rule is one reviewer seat
  per identity per round, but the current local record does not distinguish
  whether these were separate identities/sessions or the same reasoning process.
  The reviews remain usable for charter amendment because both attest that no
  same-round peer output or commit-message body was read before submission, both
  are measurement-shaped, and both findings are independently checkable from
  the charter and cited sources. Remedy for this process: delta-confirmation
  seats are reopened with explicit one-seat-per-identity language; future seat
  claims should record a stable reviewer label beyond generic model family.

- **2026-07-11 (event, foreman)** - Round-0 conformance check complete.
  Governance review: six declared checks answered in check -> result -> exhibit
  shape, observations/dissent separated, independence attested - conformant
  with two amendment requests. Adversary review: six required attacks attempted
  with outcomes and exhibits, failed attacks reported, explicit dissent from
  builder dispatch as written - conformant with amendment requests. Convergent
  disposition: amend charter before opening the builder seat.

- **2026-07-11 (event, governance delta reviewer)** - Stable reviewer label
  `codex-governance-delta-2026-07-11` claimed the open governance
  delta-confirmation seat. No same-round peer delta output or commit-message
  body was read before the review; this identity holds only the governance
  delta seat in this round.

- **2026-07-11 (event, governance delta reviewer)** - Governance
  delta-confirmation submitted at
  `reviews/round-0-governance-delta.md`. Both prior governance findings were
  marked closed; no new governance gap was identified. The adversary delta
  seat remains open.

- **2026-07-11 (event, foreman)** - Charter amended to v2. Amendments adopted:
  evidence removal/re-upload peerage probe; validation results for positive and
  negative instances; 1099-INT box distinction/negative fixture; W-2 identity
  collision pressure; four-state absence/invalidity matrix; false-guard
  rendered absence; precise citation locator/year mutation and non-operative
  parity; old-year/later-year/mixed-year versioning probe; coverage rebuild and
  stale-projection probe. Round-0 delta-confirmation opened in
  `reviews/round-0-delta.md`; builder seat remains blocked.

- **2026-07-11 (event, adversary delta reviewer)** - Stable reviewer label
  `codex-adversary-delta-2026-07-11` claimed the open adversary
  delta-confirmation seat. No same-round peer delta output or commit-message
  body was read before the review; this identity holds only the adversary delta
  seat in this round.

- **2026-07-11 (event, adversary delta reviewer)** - Bounded delta-confirmation
  submitted at `reviews/round-0-adversary-delta.md`. Findings A1, A2, A4, A5,
  and A6 are closed by v2. A3 is partially closed: the four-state and
  non-publication requirements are present, but per-state explanation-walk
  evidence is not explicit. Builder dispatch remains subject to foreman/owner
  disposition of that residual gap.

- **2026-07-11 (event, foreman)** - Round-0 delta conformance check complete.
  Governance delta: bounded to the two prior governance findings, both marked
  closed with charter exhibits, no new review work - conformant. Adversary
  delta: bounded to six prior attacks, five closed and A3 partially closed with
  one explicit residual evidence-shape gap - conformant. Foreman disposition:
  amend the charter to state the A3 explanation-walk requirement rather than
  opening the builder under an implicit qualification.

- **2026-07-11 (disposition, foreman)** - Charter amended to v3. F5 and F7 now
  require explanation-walk evidence for each absence, invalidity, and rendered-
  absence state; Evidence Expected carries the same obligation. Round 0 is
  closed. Builder it1 seat opened on branch
  `prototypes/tax-citizen-families/it1`; rival and reviewer seats remain closed
  until iteration 1 is built and examined.

- **2026-07-11 (event, foreman)** - Builder it1 dispatched under stable label
  `codex-builder-it1-2026-07-11`. Branch
  `prototypes/tax-citizen-families/it1` created from main at `953dab4` in
  worktree `/tmp/tax-citizen-families-it1`. Builder instructions: follow
  `roles/builder.md`, produce prototype artifacts and `examination-it1.md` on
  the branch, do not touch production `packages/`, report negative results, and
  leave the primary checkout on `main`.

- **2026-07-11 (event, builder)** - it1 build complete on branch
  `prototypes/tax-citizen-families/it1` at `88f0139`. Builder produced
  candidate contract, draft schemas, positive/negative examples, source catalog,
  synthetic scenario, validator, and `examination-it1.md`. Foreman verification
  reran in the prototype worktree: `python3
  docs/prototypes/tax-citizen-families/it1/validators/validate_it1.py` passed;
  `python3 tools/governance_lint.py` passed; JSON parse check over all it1 JSON
  passed. Prototype and primary worktrees were clean.

- **2026-07-11 (event, foreman)** - it1 examination copied to main as
  `examination-it1.md`; prototype artifacts remain on the prototype branch and
  are not merged. Round 1 assembled in `reviews/round-1.md` with governance,
  expressiveness, adversary, and context-starved legibility review seats.

- **2026-07-11 (event, governance reviewer)** - Round 1 governance review
  submitted at `reviews/round-1-governance.md`. Round 1 remains open; outcome
  summary withheld until the context-starved legibility seat lands or the owner
  disposes without it.

- **2026-07-11 (event, adversary reviewer)** - Round 1 adversary review
  submitted at `reviews/round-1-adversary.md`. Round 1 remains open; outcome
  summary withheld until the context-starved legibility seat lands or the owner
  disposes without it.

- **2026-07-11 (event, expressiveness reviewer)** - Round 1 expressiveness
  review submitted at `reviews/round-1-expressiveness.md`. Reviewer disclosed
  the required ordering point in the review. Round 1 remains open; outcome
  summary withheld until the context-starved legibility seat lands or the owner
  disposes without it.

- **2026-07-11 (event, legibility reviewer)** - Round 1 legibility review
  submitted at `reviews/round-1-legibility.md` by owner-launched context-starved
  session. Scope was limited to `roles/reviewer-legibility.md`, `reviews/round-1.md`,
  and the files listed in the round file.

- **2026-07-11 (event, foreman)** - Round-1 conformance verdict and close.
  Governance: declared governance checks answered with exhibits; no dissent from
  it1 as iteration evidence; conformant. Expressiveness: reproduction checks
  run before opening the examination, ordering point disclosed, six required
  checks reported with commands and exhibits; conformant. Adversary: eleven
  attacks including failed attacks, official-source probes, observations and
  dissent separated; conformant. Legibility: starved scope respected, per-
  artifact recovery with confidence and gaps; conformant. Outcome: it1 is useful
  evidence but not ratifiable as-is. Convergent findings: the companion-family
  direction is strong; `fact-type.v1` alone is insufficient; form-field,
  source-field, citation, rule-binding, tax-fact companion, and coverage-report
  families are plausible. Open weaknesses: incomplete F3/F6 coverage; 1040 line
  1z and standard-deduction/line-16 guard defaults; engagement identity not yet
  independently individuated; invalid source value modeled as a finding; source
  citation and mixed-year consistency are asserted or stringly checked rather
  than schema/resolver enforced; stale coverage and parity/hash evidence are
  scenario assertions; fresh reader could recover the family boundaries but not
  a closed explanatory slice from the listed artifacts alone. Disposition:
  conclude it1 and proceed to a clean-room rival on the same charter v3, with
  round-1 findings as lenses for later comparison rather than charter edits.

- **2026-07-11 (disposition, foreman)** - it1 preserved as exhibit tag
  `exhibits/tax-citizen-families/it1` at `88f0139`; prototype branch ref and
  worktree removed after confirming cleanliness. Rival builder seat opened for
  owner launch on branch `prototypes/tax-citizen-families/it2`. Per owner
  instruction, no subagent is spawned for the builder role.

- **2026-07-11 (event, rival builder)** - Clean-room it2 build complete on
  branch `prototypes/tax-citizen-families/it2` at `989d9fe`. Builder produced
  two new draft citizen families (`form-field.v1`, `source-citation.v1`),
  tax content authored on existing kernel fact types, rule artifacts,
  parameters, synthetic fixtures, and a harness. Foreman verification reran from
  a branch archive: `PYTHONPATH=/tmp/tcf-it2-review python3
  /tmp/tcf-it2-review/docs/prototypes/tax-citizen-families/it2/tools/harness.py`
  passed all 77 checks. No prototype worktree remains open.

- **2026-07-11 (event, foreman)** - it2 examination copied to main as
  `examination-it2.md`; prototype artifacts remain on the it2 branch and are
  not merged. Round 2 assembled in `reviews/round-2.md` as a comparative review
  of it2 against the charter and it1 evidence. Governance, expressiveness,
  adversary, and context-starved legibility review seats opened. Per owner
  instruction, any review subagents use `gpt-5.6-luna` with high reasoning.

- **2026-07-11 (event, governance reviewer)** - Round 2 governance review
  submitted at `reviews/round-2-governance.md`. Round 2 remains open; outcome
  summary withheld until the context-starved legibility seat lands or the owner
  disposes without it.

- **2026-07-11 (event, adversary reviewer)** - Round 2 adversary review
  submitted at `reviews/round-2-adversary.md`. Round 2 remains open; outcome
  summary withheld until the context-starved legibility seat lands or the owner
  disposes without it.

- **2026-07-11 (event, expressiveness reviewer)** - Round 2 expressiveness
  review submitted at `reviews/round-2-expressiveness.md`. Reviewer disclosed
  the required ordering point in the review. Round 2 remains open; outcome
  summary withheld until the context-starved legibility seat lands or the owner
  disposes without it.

- **2026-07-11 (event, legibility reviewer)** - Round 2 legibility review
  submitted at `reviews/round-2-legibility.md` by owner-launched context-starved
  session. Scope was limited to `roles/reviewer-legibility.md`,
  `reviews/round-2.md`, and the files listed in the round file.

- **2026-07-11 (event, foreman)** - Round-2 conformance verdict and close.
  Governance: measured the requested governance fidelity checks against it2,
  separated observations and dissent, and verified same-round isolation;
  conformant. Expressiveness: ran reproduction checks before opening the
  examination, reported passing harness claims separately from coverage
  failures, and disclosed ordering; conformant. Adversary: reported successful
  and failed attacks, comparative disposition, and verification probes;
  conformant. Legibility: starved scope respected, with per-artifact
  recoverability and confidence labels; conformant.

  Evidence status against the charter: it2 is useful evidence and materially
  improves on it1 in exercised 1099-INT box mapping, closure pin visibility,
  concrete form-field citizens, strict schema negatives, inert citation text,
  dual-runner parity, and a narrow mixed-package evolution check. It is not
  sufficient for Tier 2 ratification as-is. Converged gaps include incomplete
  two-source W-2 identity pressure, line 1z omission, under-specified standard
  deduction and line 16 method eligibility, missing all-elective-open fixture
  evidence, citation links not attached to non-form fact/rule/parameter
  content, incomplete cross-year/content-package checks, coverage rebuilt from
  fixture booleans rather than authoritative records, explanation walks only
  for the closure-backed zero, and fresh-reader join gaps between fact types,
  rule inputs, citations, package membership, and scenarios.

  Incidents since last check-in: none requiring reset or review invalidation.
  The context-starved legibility seat landed after the unstarved reviews and was
  committed as an event-only review before outcome summary.

  Recommendation: do not ratify it2 yet. Proceed to a third iteration focused
  on the converged gaps, especially authoritative coverage records, closure
  load-bearing semantics, cross-citizen citation/year/package relationships,
  line 1z and line 12/16 guard coverage, source-instance identity, and complete
  explanation evidence. Iteration 2 remains on branch
  `prototypes/tax-citizen-families/it2` pending owner disposition; no exhibit
  tag or branch cleanup has been applied yet.

- **2026-07-11 (disposition, owner/foreman)** - Owner accepted a targeted
  repair-and-decision pass instead of a full clean-room third prototype.
  Iteration 2 preserved as exhibit tag `exhibits/tax-citizen-families/it2` at
  `989d9fe`; branch `prototypes/tax-citizen-families/it3` opened from the same
  commit; branch `prototypes/tax-citizen-families/it2` removed after confirming
  no worktree was attached. Charter `charter-it3.md` created with explicit
  repair gates R1-R13 and clean-room mini-spikes limited to closure semantics,
  citation attachment, line-boundary strategy, and source-instance identity.
  Builder it3 seat is owner-launch pending. Per owner instruction, no builder
  subagent is spawned by the foreman.

- **2026-07-11 (event, builder/foreman)** - Owner reported the owner-launched
  it3 builder complete. Foreman inspected clean checkpoint `d5ace21` on branch
  `prototypes/tax-citizen-families/it3` and reran `PYTHONPATH=. python3
  docs/prototypes/tax-citizen-families/it3/tools/harness.py`; its core checks
  passed. The handoff is not charter-complete: `examination-it3.md` and its
  required R1-R13 evidence checklist are absent, the harness says gate-specific
  checks remain for later increments, and the README still identifies the
  artifact as it2. Round 3 was not opened. The branch remains intact and the
  seat is returned to the same owner-launched builder for mandatory closeout.

- **2026-07-11 (event, builder)** - Iteration 3 closeout completed on branch
  `prototypes/tax-citizen-families/it3` at `be72d63`. Builder added the required
  `examination-it3.md`, corrected the handoff README, and extended the harness
  with gate-specific evidence mapped to R1-R13.

- **2026-07-11 (event, foreman)** - Foreman independently reran `PYTHONPATH=.
  python3 docs/prototypes/tax-citizen-families/it3/tools/harness.py`; all 203
  checks passed. `python3 tools/governance_lint.py`, JSON parsing for every it3
  JSON file, and `git diff --check` also passed. Both worktrees were clean.
  Iteration 3 was preserved as exhibit tag
  `exhibits/tax-citizen-families/it3` at `be72d63`; the active prototype branch
  and temporary review worktree were removed after verifying the tag. The it3
  examination was copied to main and round 3 assembled in
  `reviews/round-3.md`. Governance, expressiveness, adversary, and owner-launched
  context-starved legibility review seats opened.

- **2026-07-11 (event, foreman)** - Round 3 governance, expressiveness, and
  adversary reviewers dispatched in parallel as `Lovelace`, `Nietzsche`, and
  `Hume`, respectively. Each uses `gpt-5.6-luna` with high reasoning, owns one
  round-3 review file, and was instructed not to read same-round peer outputs or
  commit-message bodies. The context-starved legibility seat remains reserved
  for owner launch.

- **2026-07-11 (event, expressiveness reviewer)** - Round 3 expressiveness
  review submitted at `reviews/round-3-expressiveness.md`. Reviewer disclosed
  the required ordering point and reported reproduction, independent probes,
  and gate dispositions. Round 3 remains open; outcome summary is withheld
  until the remaining seats land or the owner disposes without them.

- **2026-07-11 (event, governance reviewer)** - Round 3 governance review
  submitted at `reviews/round-3-governance.md`. Reviewer reported measurements,
  observations, dissent, independent probes, and tagged-harness reproduction.
  Round 3 remains open; outcome summary is withheld until the remaining seats
  land or the owner disposes without them.

- **2026-07-11 (event, adversary reviewer)** - Round 3 adversary review
  submitted at `reviews/round-3-adversary.md`. Reviewer reported attacks for
  R1-R13, including failed attacks, independent probes, primary-source checks,
  observations, and explicit dissent. Round 3 remains open; outcome summary is
  withheld until the context-starved legibility seat lands or the owner
  disposes without it.

- **2026-07-11 (event, legibility reviewer)** - Round 3 legibility review
  submitted at `reviews/round-3-legibility.md` by an owner-launched
  context-starved session. The reviewer attested to the restricted scope,
  reported per-artifact recoverability with required confidence labels, and
  did not treat unexecuted harness claims as observed results.

- **2026-07-11 (event, foreman)** - Round-3 conformance verdict and close.
  Governance: measured R1-R13 against the governance set, reproduced the tagged
  harness, separated observations and dissent, and respected same-round
  isolation; conformant. Expressiveness: ran reproduction and independent
  probes before opening the examination, disclosed ordering, and separated
  green checks from contract sufficiency; conformant. Adversary: attacked every
  R1-R13 claim, reported successful and failed attacks, checked primary tax
  sources, and kept observations and dissent separate; conformant. Legibility:
  starved scope respected, with per-artifact recovery, confidence labels, and
  explicit stops where machinery knowledge was required; conformant.

  Evidence status against the charter: it3 materially strengthens the evidence
  for determinable/attested closure semantics, an honest line-1z completeness
  boundary, explicit standard-deduction and tax-method guard behavior,
  all-elective-open saturation, rendered-absence distinctions, W-2 slip identity
  as a peer to evidence, and inert citation attachments. It is not sufficient
  for the contract-foundational Tier 2 decision. Convergent blockers are that
  W-2 correction is not exercised through supersession; closure, eligibility,
  and tax-method projections are supplied by fixture/harness state rather than
  authoritative findings; `closed_sets` remains load-bearing machinery outside
  a versioned adopted package; coverage and several explanation checks are
  harness-local reconstructions rather than end-to-end record consumers;
  citation roles and cross-citizen year/package joins are incompletely enforced;
  scenario provenance strings are not resolved; and committed negatives do not
  cover every materially changed relationship.

  Incidents since last check-in: one builder handoff was returned because the
  mandatory examination and gate-specific checks were absent. A hollow-
  measurement incident remains: all 203 checks genuinely pass, but several
  checks are tautological, helper-local, or bypass the authoritative boundary
  named by the gate, so the aggregate pass count overstates evidentiary closure.
  Foreman error: the starved round packet requested R1-R13 reporting without
  restating the gate definitions available only in the excluded charter; the
  legibility review's artifact findings remain valid, but its gate numbering is
  not used for cross-review convergence.

  Recommendation: do not ratify and do not open a fourth broad prototype. The
  three-iteration cap requires owner disposition. If the effort continues,
  authorize one bounded iteration-4 integration proof from the it3 exhibit,
  with no new domain breadth or citizen families. Its acceptance checks should
  require scenarios to materialize authoritative findings and acts, execute
  declared projections through adopted/pinned content, resolve package and
  provenance joins, rebuild coverage and all five explanations from actual
  records, exercise correction/supersession, reject wrong citation roles, and
  commit positive/negative examples for each changed relationship. Failure of
  any such end-to-end check should be recorded as a design escalation rather
  than replaced by another helper assertion.

- **2026-07-11 (disposition, owner/foreman)** - Owner authorized the recommended
  bounded integration proof at the three-iteration cap. Branch
  `prototypes/tax-citizen-families/it4` opened from immutable it3 exhibit
  `be72d63`. Charter `charter-it4.md` limits the iteration to I1-I9 end-to-end
  integration gates, prohibits new tax breadth, and rejects helper-local or
  tautological checks as gate closure. Builder it4 is owner-launch pending; per
  owner instruction, the foreman does not spawn a builder subagent.

- **2026-07-11 (charter clarification, foreman)** - Builder asked whether the
  it4 authoritative path requires a persisted synthetic workspace, whether
  production packages may be consumed, how much it3 content remains in scope,
  how machinery gaps are escalated, and the required change-inventory shape.
  Charter advanced to v2 with binding answers: use `ActLog`, adoption-gated
  `run_and_record`, `RecordStream`, `append_publications`, and ADR-0010
  `workspace_currency`; consume but do not modify `packages/`; retain the it3
  domain breadth while selecting minimal representative integration scenarios;
  continue independent gates and commit failing tests for machinery gaps; and
  provide both per-artifact and per-gate change inventories. The clarification
  records that `run_and_record` does not itself append publication acts.

- **2026-07-11 (event, builder/foreman)** - Owner reported it4 complete at
  `8fc3a53`. Foreman independently reran the authoritative-path harness (70
  checks), the 14-scenario it3 regression, governance lint, JSON parsing, and
  `git diff --check`; all passed and the worktree was clean. The handoff is not
  charter-complete: I4 lacks required mixed-year negatives for fact types,
  citations, symbol bindings, and scenario provenance; I7 tests only one of the
  required wrong-year directions; I8 does not commit examples for projection
  adoption/pins, correction/supersession, package membership, provenance
  resolution, coverage reconstruction, or explanation termination; and I9
  omits the required hard-coded coverage-map and explanation-index bypass
  probes. Round 4 was not opened. The branch remains intact at `8fc3a53` and is
  returned to the same owner-launched builder for mandatory evidence closeout.

- **2026-07-11 (event, builder)** - Iteration 4 evidence closeout completed at
  `9debc4d`. Builder added the returned I4 mixed-year checks, both I7 year
  directions, committed I8 relationship examples, and the two missing I9
  bypass probes; `examination-it4.md` and captured evidence were updated.

- **2026-07-11 (event, foreman)** - Foreman independently reran the expanded
  authoritative-path harness (92 checks), 14-scenario it3 regression,
  governance lint, JSON parsing, and `git diff --check`; all passed and both
  worktrees were clean. Iteration 4 was preserved as exhibit tag
  `exhibits/tax-citizen-families/it4` at `9debc4d`; the active branch and
  temporary review worktree were removed after tag verification. The it4
  examination was copied to main and round 4 assembled in
  `reviews/round-4.md`. Governance, expressiveness, adversary, and
  owner-launched context-starved legibility review seats opened.

- **2026-07-11 (event, foreman)** - Round 4 governance, expressiveness, and
  adversary reviewers dispatched in parallel as `Ampere`, `Lorentz`, and
  `Harvey`, respectively. Each uses `gpt-5.6-luna` with high reasoning, owns one
  round-4 review file, and was instructed not to read same-round peer outputs or
  commit-message bodies. The context-starved legibility seat remains reserved
  for owner launch.

- **2026-07-11 (event, owner/foreman)** - Owner directed that the three active
  round-4 review agents be aborted. Foreman shut down `Ampere`, `Lorentz`, and
  `Harvey`; each was still running. No partial review file or review commit
  landed, so no output from those sessions is admitted as evidence. Round 4
  remains open with reviewer dispatch stopped pending owner direction. The
  context-starved legibility seat was not launched.

- **2026-07-11 (event, owner/foreman)** - Owner immediately withdrew the abort
  direction. Foreman resumed the same three review sessions under their
  original identities; each accepted resume. Round 4 returned to active status.
  The interruption produced no review artifact and does not alter reviewer
  scope or independence requirements.

- **2026-07-11 (event, governance reviewer)** - Round 4 governance review
  submitted at `reviews/round-4-governance.md` after the resumed session
  completed. Reviewer reported I1-I9 measurements, command reproduction,
  production conditions, observations, and explicit dissent. Round 4 remains
  open; outcome summary is withheld until the remaining seats land or the owner
  disposes without them.
