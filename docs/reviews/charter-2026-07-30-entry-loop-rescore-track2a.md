# Charter — Re-score the Entry Loop, Track 2a: re-confirm the run dependencies

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-rescore.md`
- Branch: `track/entry-loop-rescore-track2a`, from `main-ui` after Track 1 merges
- Review gate: **no.** This unit produces a factual report and the evaluation
  launch materials; the milestone plan makes it a precondition, not a build.

## Why this exists

The milestone plan says, of Track 2:

> Before either evaluator is briefed, the four run dependencies named in the
> Scoring Procedure are re-confirmed against the current surface — they were
> established for a surface state that has since changed twice.

That is this unit. The surface has changed since the dependencies were last
established: Track 4 of Milestone 3 repaired the focus indicator, and Track 1
of this milestone added a keyboard-operability probe. Neither was supposed to
change surface behaviour, and the reviews found that neither did — but
"reviews found no behaviour change" is not the same fact as "the evaluation is
runnable today," and the Scoring Procedure is explicit that naming the
dependencies does not confirm them.

**If a dependency does not hold, the evaluation does not run.** Say so plainly;
do not work around it.

## The four dependencies

From the Scoring Procedure in
`docs/phases/legible-entry/entry-usability-criteria.md`, verbatim in substance:

1. A synthetic workspace can be seeded with every required non-W-2 fact, so
   **W-2 is the only missing family**.
2. The entry surface **can be served at a URL** and **can send contributions
   through the admission path**.
3. The surface makes the **fixed W-2 evaluation sets** and the **zero-missing,
   fully computed state** observable.
4. The evaluation fixture makes **every** expected-impact member change when
   the fixture's W-2 Box 1 value is entered or corrected, and leaves **every**
   untouched comparison member unchanged.

The fixed sets are defined in the criteria document and are not restated here;
read them there. Existing coverage lives in `tests/test_entry_loop_t1.py` as
`test_dependency_1_*` through `test_dependency_4_*` — use it, but confirm each
test still asserts the dependency it is named for rather than assuming the name
is accurate. Milestone 3 rejected a track for tests that never reached the code
they claimed to guard.

## What to produce

1. **A dependency report** at
   `docs/reviews/2026-07-30-entry-loop-rescore-track2a-dependencies.md`: each of
   the four, the evidence you ran, and a plain confirmed/not-confirmed. For
   anything not confirmed, name the specific artifact and what is missing.

2. **The evaluation launch materials**, so two evaluators can be briefed
   identically:
   - the command that serves the surface and what it prints
     (`python3 -m packages.derivation.runners.entry_loop_evaluation`),
   - the synthetic W-2 Box 1 first-entry figure and the corrected figure,
   - the starting-state fingerprint,
   - confirmation that
     `docs/phases/legible-entry/entry-loop-synthetic-evidence-pack.md` still
     matches what the launcher actually emits.

   If the evidence pack has drifted from the launcher, that is a finding —
   report it; **do not edit the criteria document**, and prefer reporting a
   drifted pack over silently rewriting it.

3. **A statement of what an evaluator will see**, factually and without
   evaluation: which controls exist, what states the surface can be in. Do not
   score anything, do not judge usability, and do not pre-empt the evaluators.

## Scope

- `docs/phases/legible-entry/entry-usability-criteria.md` is **read-only**, as
  it is for the whole milestone.
- No surface behaviour change. No repair of any defect you notice — report it.
- No real data; synthetic workspace only, per `AGENTS.md#Data Safety Rules` and
  `AGENTS.md#Fixture Rules`.
- Do not begin scoring, and do not write anything an evaluator would read as a
  hint about how the surface performs.

## Verification

Full quartet: `pytest -n auto`, `-m mypy`, `governance_lint`, `envelope_scan`.

**CI now runs on this line** — `verify` was added to `main-ui` in PR #116 and
passed green. Open no PR yourself, but when your branch is pushed the check
will run; reference it rather than substituting a self-report.

## Done when

1. All four dependencies are confirmed against the current surface, or the
   blocking one is named precisely.
2. The launch materials exist and an evaluator could be briefed from them
   without further questions.
3. The evidence pack is confirmed to match the launcher, or its drift is
   reported.
4. Your work is **committed and pushed**. Two builders on this milestone have
   now left work in an uncommitted working tree with no report; do not be the
   third.
