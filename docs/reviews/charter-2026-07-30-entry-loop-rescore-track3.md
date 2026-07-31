# Charter — Re-score the Entry Loop, Track 3: aggregate and close

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-rescore.md`
- Branch: `track/entry-loop-rescore-track3`, from `main-ui` after PRs #122 and #123 merge
- Criteria: `docs/phases/legible-entry/entry-usability-criteria.md` (**read-only**, as for the whole milestone)
- Evaluator files: `docs/reviews/2026-07-30-entry-loop-rescore-track2-evaluator-e.md` (Builder brief), `…-evaluator-f.md` (Reviewer brief)
- Review gate: **no.** The aggregation rule is mechanical; the owner is the decider.

## What Track 2 returned

Both evaluators scored all twenty rows independently and returned **Pass on
every row**. There are no splits, so there is nothing Disputed and nothing to
escalate.

Do not take that from this charter. **Re-derive it from the two files.** Read
each evaluator's score sheet row by row and build the matrix yourself. If the
two files do not in fact agree on all twenty, this charter is wrong and the
files win — say so plainly and aggregate what is actually there.

## Aggregate under the unchanged rule

From the Scoring Procedure, applied exactly as written and not adjusted:

1. Each evaluator scores every criterion Pass or Fail. No third value at the
   evaluator level.
2. A split becomes **Disputed** at aggregation.
3. A cell passes if and only if every mechanical criterion is Pass/Pass, and no
   judgement criterion is Fail/Fail.
4. A **Disputed mechanical** criterion fails the cell.
5. A **Disputed judgement** criterion does not fail the cell; it escalates to
   the owner with both rationales.

Classify each row as mechanical or judgement from the criteria document's own
wording, not from your reading of what it ought to be.

## File the aggregation record

At `docs/reviews/2026-07-30-entry-loop-rescore-track2-aggregation.md`:

- the twenty-row matrix, E's score and F's score side by side, with the
  aggregated value;
- the cell verdict the rule produces;
- for any Disputed or Failed row, both rationales in full;
- the accessibility row broken into its five sub-requirements with both
  evaluators' measurements, since a Pass there asserts all five and the row is
  why this milestone exists.

## Record the environmental hazard as a first-class limitation

**This is not optional and must not be softened.** The evaluation ran under a
disclosed environmental fault, and the owner has decided (2026-07-30) to
aggregate the evidence with the hazard recorded rather than re-run.

Both evaluators independently reported, unprompted, that:

- the **MCP Playwright browser was contended** by the other evaluator's
  process mid-run — E observed a foreign URL and state appear unbidden; F had
  its active tab silently swapped twice;
- the **working checkout was shared**, not isolated as the dispatch intended —
  E hit an unexpected branch switch; F found the checkout already on E's
  branch.

Both improvised mitigations mid-run: E moved all load-bearing checks to a
privately launched Chrome over CDP; F pinned a dedicated tab and re-verified
`location.href` before every measurement, then filed from a worktree it
created itself.

State in the record what the foreman established from Git rather than from the
evaluators' accounts: **score independence held.** F committed at 17:06:11 and
E at 17:07:00; the shared checkout never contained either evaluator's report
file, because each was committed only inside its author's own worktree.
Neither evaluator could have read the other's scores, because the other's
scores did not exist anywhere reachable. What the hazard threatened was
**measurement integrity, not independence** — and say exactly that, rather
than letting a reader conclude the run was either fine or ruined.

Record F's one unresolved observation without resolving it: a one-time stale
input value on reload (the field showed `90000` while the recorded answer was
`$91,000`), which did not reproduce and which F declined to score as a surface
defect because it could not be separated from the browser contention. Do not
adjudicate it. It is a loose end, and a loose end recorded is worth more than a
loose end tidied away.

The harness defect itself — evaluator isolation that did not isolate — is
**deferred by owner decision** to a follow-up milestone. Record it as a known
defect; do not fix it here.

## Move the matrix if and only if the rule says so

If the rule produces a cell pass, move the **W-2 column to L2** in
`docs/phases/legible-entry/legible-entry-roadmap.md`, and correct the roadmap's
current statement that no cell in this phase has reached L2. If it does not,
change nothing on the matrix.

L2 means synthetic end-to-end **and** usability evaluation passes. It does not
mean L3, and nothing here is operated on real data. Do not overstate it.

## Write the close

In the milestone plan, or a close section beside it:

- what the score was;
- **what the harness gap turned out to hide, or not hide.** This is the
  substantive question of the milestone. Keyboard operability was unmeasurable
  in both prior rounds and a Pass on the accessibility row silently asserted
  it. Now it is measured. Say whether measuring it changed the answer —
  E's probe run and F's independent hand-walk are the evidence — and say
  plainly if the honest answer is that the gap was hiding nothing. "We built
  the instrument and it found no defect" is a real and reportable result, and
  it is not a failure of the milestone.
- the **accumulated criterion defects** as a stated input to the later criteria
  revision. Both evaluators flagged rows that were awkward to score as written;
  F filed nine inference points. Collect them. Do not amend the criteria
  document — collect them *for* the revision that will.

## Boundaries

- **Do not amend `entry-usability-criteria.md`.** Read-only for this entire
  milestone, including this track.
- Do not re-score anything, do not overrule an evaluator, and do not resolve a
  row by reasoning about the surface yourself. You aggregate what was filed.
- Do not open a repair track. If the verdict were FAIL, the milestone closes at
  FAIL; a repair is the owner's next selection, not this track's.
- No real data anywhere.

## Verification

Full quartet: `pytest -n auto`, `python3 -m mypy`,
`python3 tools/governance_lint.py`, `python3 tools/envelope_scan.py`. CI
`verify` runs on this line; reference the check rather than substituting a
self-report.

## Done when

The aggregation record, the matrix decision, and the close are committed and
**pushed**, and a PR is open against `main-ui` (per-track PRs as of
2026-07-30) — not merged. Update `docs/phase-state.md`'s front matter in the
same commit as the close, so the pointer does not survive the milestone it
describes.

Several units on this milestone have left work in an uncommitted working tree
with no report. Do not be the next.
