# Charter — The Entry Loop (synthetic), Track 0 repair: usability criteria for entry

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Repairing: `0ddc0a5` — `docs/phases/legible-entry/entry-usability-criteria.md`
- Against: `docs/reviews/2026-07-28-entry-loop-synthetic-track0-review.md` (`NOT READY`, F1–F8)

## What happened

Track 0 wrote the evaluation instrument that scores the entry loop's L2 claim.
The review found it directionally right and not yet executable: two defects make
it unrunnable by someone who did not write it, and six weaken it. Your job is to
close all eight. Findings only — do not redesign the instrument.

Read the review in full before touching the document. It is specific about what
is wrong and what would close each finding.

## The two blocking findings

**F1 — criterion 3.3 is labelled Mechanical but is not mechanically checkable.**
Its trigger is "if the user might reasonably expect them to," which is one
evaluator modelling a third person's expectations, and the document's own
Weakest Point section concedes it cannot be enforced mechanically. It sits in
the fatal scoring class.

Pick one of the review's three routes and say which you picked and why. If you
keep the criterion, the preference is to make it observable — a named set of
W-2-related derived lines that must show as unchanged when untouched — because
the thing it is reaching for is real and worth keeping if it can be made
checkable. Relabelling it to Judgement is acceptable. Dropping it is acceptable
if you keep the omission note explaining what was lost.

**F2 — the pass rule and the disagreement rule do not determine a unique
verdict.** A Disputed criterion is a Pass+Fail pair, and the text supports both
"Disputed judgement passes the cell" and "any Fail is fatal, so it doesn't."
Two people running the same transcripts get opposite answers.

**The rule to write, decided by the foreman so you do not have to guess:**

1. Each evaluator scores every criterion Pass or Fail. No third value at the
   evaluator level.
2. A split becomes **Disputed** at aggregation.
3. A cell passes if and only if every mechanical criterion is Pass/Pass, and no
   judgement criterion is Fail/Fail.
4. A **Disputed mechanical** criterion fails the cell.
5. A **Disputed judgement** criterion does not fail the cell. It escalates to
   the owner with both rationales.

That is one rule, in one place, and it matches the procedure's existing stance
that the owner decides and that disagreement is signal rather than something to
average away. State it as a single block. If you think it is wrong, say so in
your report rather than writing a different rule.

## The six weakening findings

**F3 — the ADR-0046 disposition is silently incomplete.** Requirement 6
(accessibility baseline: contrast, ARIA landmarks, keyboard reachability,
`:focus-visible`) and Foreclosure 2 (no derived value from invalid or blocked
input in the DOM) get no disposition at all, and Requirement 4's blast
containment is carried only halfway — the "no value whose evidence is broken"
clause is dropped. Dispose each of the three explicitly, the way zero-authority
and honest-blocking were disposed: carry it with an entry adaptation, or reject
it with a reason. Foreclosure 2 in particular is the entry-side version of the
surface lying about a computed value, which is close to the centre of what this
instrument exists to prevent.

**F4 — five mechanical criteria are under-specified for agreement** (1.2, 2.2,
3.2, 4.2, 5.2). Each sits in the fatal class while inviting a split. Give each
an observable floor, or a pass/fail example, or relabel the residual judgement
portion. For 3.2 and 4.2 a W-2-grounded expected derived set does the job
without designing the surface.

**F5 — evaluation premises are stated as setup facts.** The seeded synthetic
workspace, the servable surface URL, and observable completion are milestone
open questions and Track 1's work. Name them as dependencies of *running* the
evaluation. Do not confirm them — that is Track 1's job, and confirming them is
outside this charter.

**F6 — who evaluates is only exemplified.** "e.g., Builder and
Advisor/Reviewer" lets a second run pick a different pair and still claim
compliance. Fix the count, the roles or equivalent distinct briefs, and what
difference the two are required to embody.

**F7 — no verification record.** See below; this one you close by doing it.

**F8 — "submission posture" in criterion 5.2 over-reaches.** Filing is out of
scope for this phase. Define the complete state without it.

## Boundaries

- **Findings only.** F1–F8 and nothing else. If you spot a ninth problem,
  report it; do not fix it.
- **Do not weaken the instrument to make it runnable.** A criterion that is hard
  to satisfy is fine. A criterion that cannot be scored consistently is not.
  Those are different problems and only the second is yours.
- No per-field explanation schema — that still emerges from the build.
- No product code, no prototype, no surface. Documentation only.
- No maturity claim; nothing moves on any matrix.

## Verification

This is what F7 is about, so do it properly and record it. The CI `verify`
sequence or a stated subset with each omission justified, including the
data-safety scan, plus the commit you worked from. For a docs-only unit that
record is short — what ran, what did not and why, the scan result, the base SHA
— but it has to exist. Put it in the commit message.

Note there is no `.venv` in this worktree; use system `python3`.

## Report back

Which route you took on F1 and why; confirmation that the F2 rule is stated in
one place; how you disposed each of the three ADR-0046 gaps; what observable
floors you gave the five under-specified criteria; and anything in the review
you think is wrong.
