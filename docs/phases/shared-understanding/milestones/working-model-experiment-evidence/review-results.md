# Review of results.md

Reviewed at commit `53a4d719` against the plan, design, trial logs, `trial-1/`,
`trial-2/`, the evaluation brief and `evaluation/`.

## Verdict: faithful with corrections

The hypothesis verdicts match pass 3, the participant records are intact, and
nothing is adopted. But in several places the summary is more favourable than
the evaluation, and it leaves out negatives the owner needs to weigh the phase.

## Findings, by consequence

1. **"A blind reader could locate reliably" overstates H2.** Pass 3's table
   shows mutual misses. The evaluator missed two of the observer's six
   episodes, including the snapshot 2 reliance, the only one shaped like H1.
   The observer missed T1-P2 and T1-P3. The evaluator found T1-P3 only with
   the reference account. Agreement holds only for episodes both saw. With one
   evaluator and one trial, "reliably" is a general claim. *Fix:* "Where both
   readers saw an episode, they placed it identically; each missed episodes
   the other found; they split on three of six classifications."

2. **The summary omits what the final plans still got wrong.** It reports only
   "not ready" and the defect both planners found. Uncorrected in Trial 1:
   T1-P1 ("the one input"), T1-P2 (2d resting on the open 2a), T1-P3
   ("filer-centred direction not yet challenged" despite the filer-as-student
   bound), and the misrouting to the advisor. Uncorrected in Trial 2: T2-P3,
   the unrevised C2, the D2 "state it as an assumption" candidate kept word for
   word, and the misdated history. T1-P2 and T1-P3 appear nowhere. *Fix:* add
   a short list, "What the final plans still got wrong".

3. **It never says the observer was the facilitator.** The design says "the
   facilitator records" the observer notes. One party wrote the hypotheses,
   the notes H2 is measured against, the filter decisions and this summary.
   Pass 3 lists five errors of judgement in the notes: the "one input"
   claim accepted as evidenced, the 2d/2a dependency missed, the obligor claim
   accepted, an inconsistent standard between trials, and the reference's A4
   inference treated as near-authority. `results.md` reduces these to
   "inconsistent". *Fix:* state the dual role under Limits and list the five.

4. **Challenge 1's independence is overstated.** The summary says the split
   by whose schooling "appeared only in the rejected draft, so the planner
   reached it independently". It did not. Trial 2's own snapshot 2 already said
   "a spouse's pre-marriage loan for their own schooling qualifies"
   (`trial-2/plan-history.patch`, action 3). The delivered text did not supply
   the split, so it remains evidence of diagnosis. But the planner re-applied
   its own earlier distinction. Pass 1 rated this episode only "partly
   separable". *Fix:* say exactly that.

5. **The usable finding is weaker in Trial 1 than stated.** The quoted moment
   ("a wording or disclosure matter") is Trial 2's. Trial 1 wrote that 2b "does
   not decide the joint-return representation". Its downgrade is only implied
   by "the one input that can give a wrong number". The evaluator rates T1-P1
   "borderline" and named the pattern after the fact; only the observer's
   dissent is reported. *Fix:* add both points.

6. **The recommendation goes beyond the evaluation and leaves out an
   alternative.** It asks reviewers to watch the "✓ resting on the wrong
   provision" cue, which pass 3 classed as a null outcome ("explanations
   indistinguishable"). "Further synthetic trials … would add little per unit of
   cost" is unargued. The sessions cost about US$11.60, and the main limit, one
   trial of each kind, is what replication addresses. Unstated alternatives:
   replicate with an observer and filter independent of the facilitator; use a
   second model family, given the monitors' shared blind spot; or rerun with a
   less leading challenge. *Fix:* drop or relabel the ✓ cue. Give the reason
   for preferring a prospective test, and list replication fairly. "Well
   supported" for concluding the phase is unearned; "supported" suffices.

7. **One application note contradicts another.** "Computes, correctly when
   every answer is 'yes'" conflicts with the C3b bullet: a C3b loan answered
   "yes" can still be overstated. Trial 2 said "truthfully 'yes'", and pass 1
   (rejected episode 6) limits the claim to the probed case. *Fix:* "correct in
   the probed cases (each spouse's own schooling)".

8. **"One error in the reference material" undercounts.** Pass 2 also reports
   R2, a dropped inference tag on non-obligated payment, the same inference the
   observer leaned on, and R3, Pub. 970 quoted inconsistently. *Fix:* "one
   error and two overstatements".

9. **Minor wording.**
   - The first draft did not "name the answer". It supplied the distinction to
     be found.
   - Planner B recorded catching only the Pub. 970 quotation; the observer
     noted the invented i1040 figures.
   - Planner A's misattribution "probably" came from a summary.
   - "So is obligated on the loan" is the evaluator's reading of
     § 1.6050S-3(b)(2), not settled law.
   - "Live hazard" should read "a hazard in both trials".

10. **Some conduct claims rest on the facilitator's word.** The evaluator's
    tool record is not imported, so README's account of its reads cannot be
    checked. Branch commits are imports and cannot show pass order: pass 3
    landed 3 minutes after pass 2, and `results.md` 77 s after pass 3. The
    evaluator cost and sub-agent token counts appear nowhere else. *Fix:* import
    the evaluator record and pass times, or say they are unrecorded.

## What was verified

- **History not rewritten.** `trial-1/` and `trial-2/` were each added in one
  commit and never changed. Replaying each `plan-history.patch` reproduces
  `plan-final.md` and `working-account.md` exactly. The commit IDs match the
  logs.
- **Quotations match.** Eight checked per trial (Trial 1: the snapshot 3
  narrowing, the snapshot 5 self-correction, 2b, 2d, "from memory", and three
  snapshot 7 lines; Trial 2: C3, both diagnoses, the D5 reclassification, the
  obligor line, "twice in miniature", "C3b is **not** qualified", and the
  "$2,500 per return" correction). Reviewer drafts 4, 4b and 7, and both
  delivered texts, are verbatim. Two reviewer notes in the log are cut at a
  sentence end without an ellipsis, with no change in meaning.
- **Timing.** Both logs are append-only. Every note or delivery commit precedes
  the planner's first tool call of the next interval, by 5–8 s in Trial 1 and
  5–42 s in Trial 2. That is consistent with README's 2–4 s, but the message
  timestamps behind that figure are not in evidence. The snapshot 4 note
  (23:09:00) precedes the reviewer's first read (23:09:06).
- **Filter.** Both delivered challenges are three sentences and cite only text
  the planner could see. Challenge 2 passed the rules yet led the planner; the
  rules could not prevent that.
- **Non-goals.** No model, practice or product change is adopted. The watch
  rule is a candidate, and the application points are labelled "not product
  decisions". General claims are limited to findings 1 and 9.
