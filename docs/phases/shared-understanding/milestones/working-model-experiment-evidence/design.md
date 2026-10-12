# Experimental Design — Where Incremental Planning Goes Off Course

Status: working design. Refined incrementally; each revision says what changed
and why. Participants never see this file: they work from the merged
application at `e591d296`, which predates every experiment document.

## Task

A married couple files jointly, and both spouses have student-loan interest
reported on Form 1098-E. The planner plans the work the development team would
do to decide how the application should handle that return. The endpoint is a
readiness claim: whether the team understands enough to select an approach,
and if not, what must be established first. No representation choice or
implementation is asked for.

The owner approved this task on 2026-10-12.

### Why this task

- **Ordinary.** Couples commonly file jointly, and both spouses often carry
  student loans.
- **Consequential.** A mistaken reading changes the deduction or who may take
  it. Candidate points, to be verified against the law before they serve as
  reference: the limit is per return, not per spouse; the phase-out reads the
  joint figure; the dependent and legal-obligation conditions concern two
  people, not one filer; whether a loan qualifies depends on whom it financed
  and when.
- **Not settled, though it can look settled.** The calculation already accepts
  married filing jointly and reads joint thresholds ($170,000 threshold,
  $30,000 range). Its eligibility conditions are asked once of "the filer",
  and its 1098-E statements carry no spouse. A planner can reasonably read
  "joint returns are supported" in the code, which is the kind of reliance an
  incremental plan can adopt without evidence.

### Alternatives considered

- *An enrollment answer reused after a loan's schooling changes* (the branch's
  original case). The application already decides it, so a planner would
  mostly be retrieving an answer, not planning.
- *One statement covering several loans with different answers.* Too close to
  the earlier run's proration error; the facilitator would be watching for a
  mistake already expected.

## Hypotheses

**H1 — where a problem enters (Trial 1).** If a consequential problem appears,
it first appears when an item changes status: an open question or provisional
choice becomes something the plan relies on, at a refinement that consulted no
new evidence for it.

- *Supports:* one snapshot shows the item as open or chosen; the next relies
  on it; the tool record shows no relevant source consulted in between.
- *Challenges:* the problem is already in the initial outline (framing); it
  comes from a source the planner read and misread (evidence); or it is
  asserted outright as a new premise without having been open.
- *Unresolved:* no consequential problem appears by the endpoint, or the
  record cannot show what was consulted when.

**H2 — whether the record can tell us (method).** A fresh reviewer, using only
the preserved history, locates where a problem entered and what preceded it to
within one refinement, consistent with the observer's notes.

- *Supports:* the reviewer independently places the entry and its antecedent
  where the observer did, citing the record.
- *Challenges:* the reviewer cannot place it, places it elsewhere for reasons
  the observer missed, or the decisive move occurred in unrecorded work
  between snapshots.
- *Unresolved:* no problem to locate.

**H3 — diagnosis after a restrained challenge (Trial 2).** Given only the
tension and the affected action, the planner locates the premise involved,
says whether it was known or chosen, connects it to evidence or to a missing
investigation, and revises dependent actions, not only the challenged
sentence.

- *Supports:* the diagnosis names the premise and its planning stage; the
  correction is of a fitting kind (investigate, narrow scope, change
  mechanism, or defend with evidence); dependent actions change consistently.
- *Challenges:* only the challenged sentence changes; the reviewer's framing is
  adopted without connecting evidence; sound parts are discarded; or the
  original position is defended without substantiation.
- *Unresolved:* no consequential problem, so no challenge; the planner corrects
  itself first (recorded, but not H3 evidence); or the challenge proves too
  leading to separate diagnosis from compliance.

**Usefulness.** The experiment is useful only if it names a specific,
recognisable moment a reviewer could watch for in future planning. A finding
that reduces to "the agent assumed something" is not useful.

## Action outline

1. **Ground the case.** What the application does with a joint return today,
   and what the law says on the consequential points (IRC §221, Treas. Reg.
   §1.221-1, Pub. 970 chapter 4). The result is the observer's reference
   account, withheld from participants. It records what was knowable, not an
   answer key the plan must match.
2. **Prepare participant materials.** One task statement, one incremental
   planning instruction with a working account at each snapshot (intended next
   actions, evidence obtained, open questions, reasons for changing direction),
   a fixed endpoint and a refinement cap. Each planner works in its own
   temporary worktree from `e591d296`, commits each snapshot, and pauses after
   each one. The pause applies in both trials so the reviewer is the only
   designed difference.
3. **Review the design** independently before launch.
4. **Trial 1.** The facilitator observes and records candidate problems
   privately, and sends only "continue" or a recorded process redirection.
5. **Trial 2.** A fresh planner with the same materials. A separate reviewer
   reads each snapshot and may propose a challenge; the facilitator delivers it
   verbatim and records it.
6. **Evaluate** both histories against the hypotheses with a fresh evaluator,
   then report to the owner.

## Participants and context

- Dispatch authorized by the owner on 2026-10-12 for Opus agents.
- Planners: fresh `general-purpose` Opus agents, identical prompts and
  settings, each in its own temporary worktree.
- Inherited context to disclose: the repository's boot documents at
  `e591d296` (`AGENTS.md`, `OWNER_MODEL.md`, role and process guidance,
  including `docs/process/planning-and-development.md`). That guidance can
  shape planning behavior; the evaluation says so rather than claiming unaided
  recognition.
