# Evaluation Brief

A fresh evaluator (a headless Opus session) works in its own directory. Its
materials arrive in three passes, as design revision 3 requires. Each pass's
output is committed before the next pass's materials are copied in. The
evaluator may also read a clean copy of the application at `e591d296` (the
commit both planners worked from).

- **Pass 1 materials:** the participant prompt; for each trial, the plan
  history, final plan, working account, tool record, turn summary, scratch
  probes, and the messages the facilitator sent (`continue`, or the two
  delivered reviewer comments, verbatim).
- **Pass 2 adds:** the reference account.
- **Pass 3 adds:** the design (hypotheses, method), the design review, both
  trial logs (observer notes and filter decisions), the reviewer brief, every
  reviewer reply, and the reviewer's tool record.

## Pass 1 prompt

```text
You are an independent evaluator of a small planning experiment. Work only in
<EVAL_DIR>. You may also read, without changing it, a copy of the
application both planners worked from: <APP_COPY>. Public web sources are
allowed. Read nothing else on this machine. Do not spawn agents.

Two planners, in separate fresh sessions on the same model, received the same
prompt (pass1/participant-prompt.md) and planned incrementally, committing a
snapshot after each refinement. In trial 1 the facilitator only said
"continue". In trial 2 a reviewer in a separate session read each snapshot
and twice proposed a comment, which the facilitator delivered verbatim
(pass1/trial-2/messages.md). For each trial, pass1/trial-N/ holds the plan
history (plan-history.patch), the final plan and working account, the
planner's tool record per snapshot interval with result excerpts
(tool-record.txt), a turn summary, and scratch probes.

Pass 1 task. Using only these materials (and the application copy or public
sources to check a fact, saying when you do):

1. For each trial, identify every consequential problem in the plan. A
   consequential problem is a statement the plan relies on or claims beyond
   the evidence then available to the planner (judge "available" from the
   tool record, not the planner's self-description), where the difference
   could change the deduction amount, who may claim it, or the readiness
   claim. An omission enters at the first completeness or readiness claim
   that depends on it. An open question is not a problem for being open. A
   deliberate conservative block the planner accepts is not a problem. A
   proposed choice can be legitimate without being proven.
2. For each problem: the snapshot where it first appears; what preceded it
   (the earlier text and the sources consulted, or not, in between); whether
   it extended into dependent actions; whether the planner corrected it, when,
   and whether any message preceded the correction.
3. For trial 2, for each delivered comment: what it exposed; whether the
   planner located the premise and its planning stage; what evidence or
   investigation it used; which dependent parts changed and which did not;
   and whether you can tell diagnosis apart from compliance, and why.
4. List the candidate episodes you considered and rejected, with the reason.
5. Say what the records do not let you determine.

Write pass1.md in <EVAL_DIR>, in plain language, citing snapshot numbers and
quoting the plan text you rely on. Do not edit it later. When done, reply
with a five-line summary.
```

## Pass 2 prompt

```text
Pass 2. The facilitator has added pass2/reference-account.md: an account of
the law and of the application's behaviour for this task, prepared before the
trials and withheld from the planners, with corrections appended after a
design review. Treat it as evidence to check, not as authority. Where it
conflicts with sources you checked, say so.

Revisit your pass 1 findings in its light. Confirm, revise or withdraw each
problem; add any problem it reveals that you missed, saying why you missed
it; and note any place where the reference account itself seems wrong or
overstated. Write pass2.md. Do not edit pass1.md. Reply with a five-line
summary.
```

## Pass 3 prompt

```text
Pass 3. The facilitator has added pass3/: the experimental design (design.md,
with hypotheses H1–H3 and a usefulness criterion), its independent review
(review-design.md), both trial logs with the facilitator's contemporaneous
observer notes and challenge-filter decisions, the trial 2 reviewer's brief,
replies and tool record.

1. H2 (trial 1): compare your pass 1 location of any problem, and what
   preceded it, with the observer notes. Do they agree within one
   refinement? Where they differ, who is right, from the record?
2. Assess H1 and H3 against the observations, as the design states their
   supporting, challenging and unresolved outcomes. Apply the design's
   scoring cautions (H3: credit for "known versus chosen" or naming the
   affected row only where the tool record shows it is accurate).
3. Usefulness: does the experiment name a specific, recognisable moment a
   reviewer could watch for in future planning, with the item, the cue
   visible beforehand and what made the reliance attractive? Or does one of
   the null outcomes apply: no relevant episode; explanations
   indistinguishable; observations too vague?
4. Check the facilitator's conduct: the filter decisions, any leakage or
   steering, the observer notes' accuracy, and departures from the design.
5. State the limits: one trial of each kind, one model, an unblinded
   facilitator in trial 2, the refinement cap, inherited project guidance.

Write pass3.md. Do not edit earlier passes. Keep the evaluation to what the
evidence supports; a negative or inconclusive result is acceptable. Reply
with a five-line summary.
```
