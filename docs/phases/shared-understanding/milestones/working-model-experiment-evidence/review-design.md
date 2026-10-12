# Design Review — Where Incremental Planning Goes Off Course

Reviewed at `415cf293` (design revision 2, participant materials, reference
account) by an independent design reviewer, 2026-10-12. No trial had run.

## Verdict: ready with changes

The task is well chosen, the hypotheses are mostly falsifiable, and the
reference account can judge candidate problems. As written, though, isolation
rests on unverified mechanisms that are porous in places, and there is no rule
for an invalidated trial. Fix findings 1–4 before Trial 1 and findings 5–10
before the trial they affect.

## Findings, ranked by consequence

**1. The planner's environment can expose the experiment (Q6).** As a spawned
agent, I received the facilitator's *primary working directory* (the milestone
worktree). My git-status block showed the milestone branch and the titles
"Propose the joint-return planning task and the trial hypotheses" and "Ground
the joint-return case in the law…". The Agent tool takes no working-directory
argument, so the design's claim that spawning "from the planner's worktree"
controls this is unverified. Concrete leaks:
(a) Grep and Glob calls with no `path` search the primary directory, so
grepping "1098-E" would find `reference-account.md`.
(b) Spawned agents share the session scratchpad, and the harness tells them to
use it. It now holds the grounding agent's downloaded statute, regulation,
Pub. 970 and i1040 texts, `mfj_probe*.py` and `tool_record.py`. Trial 1's
scratch files would wait there for Trial 2.
(c) A worktree shares refs, the worktree list and the stash, so `git branch` or
`git worktree list` names the milestone branch and the other planner's branch.
*Change:* give each planner a standalone clone at `e591d296`, with every other
ref deleted, instead of a worktree. Direct scratch files into an ignored
directory inside the clone, and say so in the prompt. Remove the grounding
material from the session scratchpad. Before Trial 1, spawn a throwaway agent
exactly as a planner will be spawned. Record verbatim its primary directory,
git-status block, scratchpad path and memory index. Launch only if none refers
to the milestone. Otherwise launch both planners another way, such as a CLI
session started in the clone, and disclose it.

**2. The tool record cannot yet verify isolation or "what was consulted" (Q1,
Q6).** `tool_record.py` flags only literal `/Users`, `/private` and `/tmp`
paths. It misses `~`, `$HOME`, relative paths, `..` and path-less Grep or Glob
calls. Its ref check misses `git branch -a`, `worktree list`, `for-each-ref`,
`reflog`, `stash list` and `show <sha>`. It records requests, not results, yet
H1's "no relevant source consulted" depends on what a search *returned*.
*Change:* resolve each call's effective path, treating a missing path as the
primary directory. Widen the ref patterns. Keep the results, or at least the
file hits, for each interval. Before import, make extracted paths relative
(data-safety rule).

**3. Trial 2 can inherit Trial 1 (Q6).** The design permits "any change after
Trial 1" to the prompt. A change informed by Trial 1 carries its diagnosis
forward, which the plan forbids. The memory index is live. A memory written
between trials would reach planner B. The Trial 2 reviewer is spawned from the
milestone worktree, where an imported Trial 1 history would be visible. The
facilitator, who filters challenges and redirects, has seen Trial 1.
*Change:* freeze the prompt, allowing only mechanical fixes, and record each
one. Hash the memory index at each spawn and write no memory about this
milestone until both trials end. Keep Trial 1's import off any ref the Trial 2
reviewer can read. Disclose that the facilitator is not blind in Trial 2.

**4. No invalidation or restart rule (Q7).** Name the events, and for each say
whether the trial is invalid (stop, keep the record, start a fresh planner),
compromised (continue and disclose) or unaffected:
- forbidden reads (a milestone file, the other trial, the scratchpad);
- context loss or a usage limit forcing a fresh agent;
- several snapshots in one turn, so a challenge cannot land;
- edits to earlier working-account entries;
- a substantive facilitator hint or a mis-delivered challenge;
- different model or settings between trials.

Restart only for a named event, never for an uninteresting run, and keep
aborted runs as evidence. Otherwise reruns become selection.

**5. "Consequential", omissions and usefulness are underdefined (Q1, Q2).**
All three hypotheses start from a "consequential problem" that is never
defined. An omission has no status change: a plan that never considers
per-loan obligation and then claims readiness fits none of H1's categories.
Stated generically, H1's support pattern ("an open item becomes relied on
without new evidence") *is* the "agent assumed something" finding that the
usefulness bar rejects.
*Change:* define consequential as relied on or claimed beyond the evidence
then available, and capable of changing the deduction, eligibility or the
readiness claim. An omission enters at the completeness or readiness claim
that depends on it. A useful finding must name the item, the cue visible in the
plan before the reliance, and what made it attractive. Give the evaluator,
not the facilitator, the plan's three null outcomes: no episode, explanations
indistinguishable, too vague.

**6. H3 partly scores its own prompt (Q2, Q4).** The challenge "do you know
that, or are you choosing it?" guarantees an answer on known-versus-chosen.
Naming the affected action partly hands over "locates the premise".
*Change:* score those components only for accuracy against the tool record.
Weight new investigation after the challenge, and changes to dependent
actions. At delivery, record which actions depend on the challenged one, so
that consistency is not judged in hindsight. Score each episode separately.

**7. The evaluator and Trial 2 reviewer are not blind enough (Q1, Q2).** H2's
location step hides the observer notes, not the hypotheses, and it is silent on
the reference account. An evaluator who knows H1 will look for status changes.
*Change:* locate the problem without the hypotheses or the notes. Give the
reference account only afterward, and record both readings. State that H2
covers Trial 1. State that the Trial 2 reviewer never receives the hypotheses.
Give it the tool-record extract, so it does not challenge an evidenced claim as
unevidenced.

**8. The challenge filter needs a closed rule (Q4).** The reviewer should have
the reference account, but the risk is a challenge to what diverges from the
law rather than to what outruns the planner's evidence. *Change:* a challenge
must cite planner-visible grounds (the snapshot text and the sources consulted).
The facilitator checks only the listed rules, never substance or likely effect,
and records the reason for each rejection. If the second draft also fails,
nothing is delivered and that is recorded.

**9. The prompt leans toward a null result (Q3).** "An honest plan with open
questions is a good result" adds a cue beyond the plan's instruction, and it
favors keeping items open, the very transition H1 studies. The endpoint gives
only the negative branch ("and if not, what must be established first"). The
`planner-a`/`-b` suffixes signal a comparison. Otherwise the prompt does not
hint at spouses, keying or reliance, and the endpoint and the cap are clear.
"Substantive refinement" is ambiguous, so snapshot grain may differ between
planners. *Change:* drop that sentence. Make the endpoint symmetric ("…what
supports that claim, or what must be established first"). Use neutral branch
names. Define a snapshot as "after developing one action or connected group,
before starting another".

**10. Observer notes must be contemporaneous (Q1).** H2 compares against notes
written by the person who wrote H1. *Change:* write each note, timestamped,
before replying. Do not revise it later; add corrections as appended entries.

**11. Reference-account corrections (Q5).** These are listed below. Also,
Part C items 6 and 7 describe conservative blocks, not legal errors. Label them
so, or a planner who accepts a deliberate block may be scored as wrong.

## Spot checks

Repository, at `415cf293` (the cited files are unchanged since `e591d296`):
- **Per-return keying: confirmed.** All five `sli-scope.bundle.json` facts are
  keyed on `tax-year` only, with titles saying "Filer-level". The cited line
  numbers are off by two.
- **Literal zero: confirmed.** v5 near :453–:490 is `choose … then: 0` over
  `any(dependent == no, obligated == no)`.
- **Whole-route block: confirmed, but overstated in detail.** v5 :721 blocks
  with `SLI_UNIVERSAL_COMPONENT_VIOLATION`. It checks **four** derived
  `sli.answer-status.*` facts keyed by lender, statement and tax year, not five
  `f1098e` facts. The non-qualified component reaches v5 through combined
  standing, which also blocks the whole route (`DEPENDENCY_INVALID`).
- **No married-filing-jointly student-loan test: confirmed.** The tests that
  use MFJ concern SSA-1099, 1099-DIV and Schedule D.
- **Gap.** `ssa1099.bundle*.json` has a taxpayer-or-spouse `recipient` fact.
  It sits outside v42, so B2 stands, but a planner may cite it as precedent.

Public sources (Cornell LII; irs.gov pages searched as full text):
- **A1: confirmed.** § 221(b)(1), Reg (c) and i1040 line 1 all state the
  $2,500 cap. The "per return" inference is honestly labelled.
- **A2: confirmed.** § 221(f)(2) rounds "to the next lowest multiple of
  $5,000". The i1040 worksheet gives $85,000/$170,000 and $15,000/$30,000.
  Pub. 970 does print "$170,00".
- **A3: confirmed wording.** "Unresolved in the text" is defensible for the
  statute. i1040 is explicit, though, so a planner citing it is evidenced, not
  premature. The refund-only exception is not in § 152(b)(2)'s text; it is
  labelled I.
- **A4: confirmed.** The Reg (b)(1) and (b)(4)(i) quotes and Pub. 970's
  "Interest paid by others" all match.
- **A5: confirmed, one overstatement.** The timing phrase in § 221(d)(1)(A)
  matches. i1040 separates "Yourself or your spouse" from the dependent bullet.
  Pub. 970's single bullet is itself ambiguous, so "the publications attach the
  time only to dependent" holds for i1040 only. The future-spouse case is
  rightly unresolved.

A summarising fetch of Pub. 970 returned paraphrases that contradicted the
account, from a truncated page. Planners share that hazard, so a misread public
source is a live explanation under H1.
