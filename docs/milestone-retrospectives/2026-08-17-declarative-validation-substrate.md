# Retrospective — Declarative Structured Validation and Consumer Dependency Substrate

## What differed from the plan

- The plan's original numerical caps on Builder/repair/Reviewer iterations
  (two Builder iterations, one repair pass, two independent Reviewers) were
  suspended by owner direction on 2026-08-13: continue until defects are
  fixed, for this milestone only. Track 2 alone went through seven repair
  rounds before its review returned zero findings. This is recorded in
  `docs/prototypes/declarative-validation-substrate/plan.md`, "Owner-directed
  continuation."
- Track 3's migration changed a different milestone's observable contract
  without anyone noticing at build or review time.
  `runner.py`'s blocked-disposition normalization (needed so declarative
  family-validation block codes don't violate `derivation-record.v6`'s closed
  enum) had a side effect: an unrelated MFS tax-bracket gap that used to
  escape as an uncaught `SchemaValidationError` now surfaces as a clean
  `blocked` disposition instead. The behavior change is a genuine improvement
  (a crash became a citable, fail-closed finding), but the test asserting the
  old crash shape kept passing right up until the owner-advisor product
  review bisected a suite-wide failure to `d8905d2c` and found it. Neither
  Track 3's own review nor its builder's test run caught it, because neither
  ran the affected sibling milestone's test module — it wasn't in Track 3's
  required-verification list, and had no reason to be; it belongs to a
  different, already-closed milestone.
- A different shared-boundary break *was* caught by Track 3's own independent
  review: `packages/tax/loader.py`'s `tax_registry()` hard-required
  `source-family.v1`, and the eight new `source-family.v2` covered-W family
  citizens broke it for F1098/1099-DIV/1099-G/1099-INT/W-2 tests that have
  nothing to do with Form 8949. Repaired same-day at `0604f2fb`. Both
  incidents are the same underlying lesson stated twice: a milestone's own
  required-verification list, however carefully charted, cannot see every
  file a change touches by side effect. Only the full suite can.
- The Track 4 build correctly discovered, and correctly declined to fix, a
  pre-existing `reference_runner.py` gap: the second (backward demand-driven)
  scheduler had no dispatch branch for attachment-rule citizens at all,
  meaning it could not execute *any* content in this milestone's family —
  not a covered-W-specific defect. This matched a limitation Track 0's own
  adversarial closure had already disclosed and dispositioned ("verdict-gated
  and attachment-free"), so the foreman chartered a same-milestone repair
  (Repair 1) rather than treating it as new scope; the fix was a genuine
  two-line dispatch correction, not a rewrite.
- The owner separately reported four substrate defects mid-milestone
  (`marshal.py` under-registered version sets, `runner.py`'s unguarded
  constraint evaluator, dead `evaluate_constraints` code, and a bool/numeric
  equality conflation in `field_equals`). All four were independently
  re-verified by the foreman before chartering — not accepted on the report's
  word — and one adjacent instance of the same under-registration defect
  (`attachment-rule.v8` missing from the same `marshal.py` function as the
  reported `rule-artifact.v5` gap) was found during that verification and
  folded into the same repair.
- A subsequent owner-advisor product review found and repaired a failing
  type gate (`mypy --strict` reported 48 errors across 4 files — the branch
  could not have gone CI-green) that had accumulated silently because the
  foreman's own iteration loop ran only the touched modules' mypy, never the
  whole tree, per this project's own "Test lanes" cost discipline. The one
  genuine engine-signature fix inside that batch (`list` invariance on
  `Evaluator.evaluate_member`/`identity_tuple`, widened to `Sequence`) was a
  real defect; the other 45 were test-local annotation debt.

## What it cost

- Track 2: seven repair rounds, each independently reviewed; final review
  zero findings across an eight-hash-seed adversarial probe matrix.
- Track 3: one independent review (CHANGES REQUESTED on one finding), one
  same-day repair, one reconfirmation review (ACCEPTED) run after the fact
  because the original repair was never re-verified against the actual tip
  before this closeout.
- Track 4: one build, two repairs (reference-runner scheduler dispatch;
  four-defect substrate hardening), no independent review of its own before
  the owner-advisor product review covered it as part of the whole branch.
- One owner-advisor product review covering the full branch, with two
  repairs applied directly in that review's own commit (type gate,
  cross-milestone test).
- Zero new ADRs. ADR-0066 (accepted before Track 1 began) is the sole
  product contract this milestone implements; nothing here required a new
  or amended ADR.
- Final package is the additive union core **v32** / published **v27** /
  release **v25** / adopt **v32**, over the merged core v31 base.

## Follow-ups

- **P1 — nine hand-maintained rule-artifact/attachment-rule capability
  allowlists** across `live.py`, `marshal.py`, `presentation_projection.py`,
  `package_validation.py`, and `runner.py`. Three consecutive milestones have
  each independently missed a different member of this set. Scoped, not
  built:
  `docs/phases/engine-breadth/milestones/rule-artifact-capability-table-consolidation.md`.
  Trigger: owner selects it as its own milestone.
- **P2 — `accounts_for` exact-agreement coupling cost.** Deliberate and
  correct (it is what makes an incomplete authoring declaration detectable),
  but adding a constraint set to an existing family is a breaking change for
  every consumer that reaches it; the coupling is superlinear in family
  count. Not a defect. Recorded so a future family addition budgets for it.
  Trigger: none — informational, revisit if the coupling cost is ever felt
  as a real blocker.
- The `SYNTHESIZED_PREREQUISITE_OMITTED` issue-order nondeterminism disclosed
  during Track 2 Repair 7 remains unrepaired: content and identities are
  deterministic, only the order among multiple independent omitted-edge
  issues is not. Non-blocking; unchanged from that review's own disposition.
  Trigger: a future consumer of ordered issue output.

## What should change in the next plan

- **Run the full suite, not just the touched-module subset, before treating
  any track or repair as done — including type-checking.** Every incident
  above (the MFS contract-shape surprise, the loader break, the accumulated
  type-gate debt) was caught either late or by a separate reviewing party
  precisely because the iteration loop stayed narrowly scoped to assigned
  paths, per the project's own cost-conscious "Test lanes" discipline. That
  discipline is correct for inner-loop iteration speed and wrong as the last
  check before calling a unit complete. This milestone's own
  `AGENTS.md` "Test lanes" section (introduced mid-milestone by an unrelated
  process commit) already states the rule this milestone needed from the
  start: any change under `packages/kernel/`/`packages/derivation/` runs the
  full suite, not the fast lane. Apply it to `packages/tax/` too — the loader
  break happened there, not in `packages/derivation/`.
- **When a repair changes shared machinery's observable output shape
  (not just its correctness), grep for every test elsewhere in the repo that
  asserts the old shape**, not only the tests in the charter's own
  required-verification list. A charter cannot enumerate every sibling
  milestone's assertions in advance; a repo-wide search for the specific
  disposition/exception/code string being changed is cheap and would have
  caught the MFS test before merge instead of after.
- **A reviewer re-verifying a repair should always run against the actual
  current tip, not just the repair's own commit.** Track 3's loader finding
  was fixed correctly at `0604f2fb` but not re-confirmed ACCEPTED until this
  closeout, after three more tracks and two more repairs had landed on top —
  purely a bookkeeping gap, not a doubt about the fix, but one this closeout
  had to spend a full review pass closing that a same-day re-confirmation
  would have avoided.
