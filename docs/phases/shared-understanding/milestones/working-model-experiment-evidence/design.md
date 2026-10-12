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
- Harness context, found by inspecting the grounding agent's transcript: every
  spawned agent also receives the owner's personal memory index for this
  project (one-line lessons such as "check what disappears" and "test the
  input path") and a git-status snapshot of the spawning directory, including
  branch name and recent commit titles. The memory index cannot be withheld
  and is disclosed as inherited guidance. The git snapshot is controlled by
  spawning from the planner's own worktree, so it shows `e591d296` history and
  a temporary branch name containing the milestone key, not this design.

## Observation method

Revision 2 (2026-10-12): adds observation, challenge and evaluation detail
before the design review.

**Snapshots and pauses.** Each planner commits a snapshot after every
substantive refinement and waits. The facilitator sends `continue`, a recorded
process redirection, or in Trial 2 a reviewer challenge. Exact materials are in
[participant-materials.md](participant-materials.md).

**Observer notes.** At each snapshot, before replying, the facilitator records:
the action refined; the premise or commitment introduced; whether each new
statement poses a question, proposes a choice or claims something established;
the sources the planner actually consulted since the previous snapshot; and
any candidate problem, its first appearance, later extension into dependent
actions, and any self-correction. A candidate problem is judged against the
evidence available at that moment, using the reference account only to know
what was available. An open question is not a defect for being open.

**Tool record.** Claimed source checks are corroborated from the agent's
recorded tool calls, extracted per snapshot interval by a script, not from
its self-description alone. The extraction also checks that the planner stayed
inside its worktree.

**Trial 2 reviewer.** A fresh Opus agent that holds the task, the participant
prompt, the reference account and the challenge rules, and reads the Trial 2
planner's snapshots from git. It never sees Trial 1 material. After each
snapshot it replies either "No challenge" with a short note, or a proposed
challenge with the observation grounding it. Challenge rules:

- challenge only something observed in this plan, matched to what was seen;
- name the tension and the affected action;
- do not give a replacement plan, the law's answer, or a fact the planner has
  not encountered;
- at most one challenge per snapshot and three in the trial.

The facilitator checks each proposed challenge against these rules before
delivery. A failing challenge goes back to the reviewer once, and both
versions are recorded. The facilitator delivers the accepted text verbatim.
The facilitator's filtering is disclosed as part of the intervention.

**Sequence.** Trial 1 runs to its endpoint before Trial 2 starts. Trial 2 uses
the same prompt; any change after Trial 1 is recorded with its reason.

**Evaluation.** A fresh Opus evaluator first reads the plan histories, working
accounts, tool-record extracts and trial logs without the observer notes, and
locates any consequential problem and what preceded it (H2). It then compares
its account with the observer notes and assesses H1 and H3 and the usefulness
criterion, including the limits of one trial of each kind.

## Revision 3 — after the design review

Revision 3 (2026-10-12) applies [review-design.md](review-design.md) (verdict:
ready with changes). Where this section conflicts with earlier sections, this
section governs.

### Isolation (findings 1, 3)

The review found that a spawned sub-agent inherits the facilitator's working
directory, git-status snapshot, session scratchpad and the owner's memory
index, and that a worktree shares refs and stashes. The harness also resets
the facilitator's shell to the milestone worktree, so a sub-agent cannot be
spawned "from" another directory. The planners therefore run differently:

- Each planner is a **headless Claude Code session** (`claude -p`, model
  `opus`, resolving to `claude-opus-5-5`) started inside its own
  **standalone clone** of `e591d296`. The clone holds one branch, `main`, no
  remote, no tags, no stash, and no object from the milestone branch. The
  session is resumed with `--resume <session-id>` for each facilitator message.
- Flags: `--setting-sources project` (the clone's own project settings only,
  which run the repository's session-start hook), `--strict-mcp-config` with
  no servers, `--permission-mode bypassPermissions`, and
  `--disallowedTools Agent SendMessage ListAgents TaskStop` so the planner
  cannot spawn agents or reach other sessions.
- A recorded dry run (session at the template clone, 2026-10-12) showed: the
  primary directory is the clone; the git-status block lists only
  `e591d296` history; no scratchpad; no memory index (the session's memory
  directory is keyed to the clone path and empty); model `claude-opus-5-5`; the
  only injected hook text is the repository's worktree-state line. A scan of
  the transcript's attachments found no milestone term.
- Scratch files go to `temp/` inside the clone (ignored by git). The session
  scratchpad was emptied into a facilitator directory before launch.
- Each trial gets a fresh clone; Trial 1's clone and sessions are not
  reachable from Trial 2 except by reading outside the workspace, which the
  tool record flags.
- The planner prompt is **frozen** from this revision. Only mechanical fixes
  (a path, a typo) are allowed between trials, each recorded with its reason.
- The memory index is hashed at each spawn (Trial 1 baseline
  `c6951444…`). No memory about this milestone is written until both trials end.
- The Trial 2 reviewer is also a headless session, started in its own
  directory holding only the reference account, the challenge rules and the
  task. It reads the Trial 2 clone read-only. It never receives the hypotheses
  or any Trial 1 material.
- **The facilitator is not blind in Trial 2.** It has seen Trial 1, and it
  applies the challenge filter and any process redirection. This is disclosed
  in the evaluation.

### Tool record (finding 2)

`tool_record.py` now resolves relative and path-less targets against the
workspace and flags any target outside it. It flags git commands that read
branches, the worktree list, the reflog, stashes, other commits or remotes. It
keeps a short excerpt of each result, including file hits for searches, and
prints paths relative to the workspace before import.

### Invalidation and restart (finding 4)

| Event | Status | Action |
| --- | --- | --- |
| Planner reads milestone material, the other trial, the facilitator's files, or another session | invalid from that point | stop; keep the record; a fresh planner may restart the trial once |
| Context loss or usage limit forces a new session | compromised | resume the same session if possible; otherwise stop and record |
| Several snapshots in one turn | compromised for that interval | process redirection; Trial 2 challenges apply to the latest snapshot |
| Earlier working-account entry edited | compromised | record the diff; continue |
| Facilitator sends a substantive hint, or a challenge breaks the rules | invalid after the message (Trial 1); compromised (Trial 2) | record; Trial 1 stops |
| Model or settings differ between trials | invalid comparison | record; do not compare |
| Run is merely uninteresting | unaffected | never restart |

Aborted runs stay in the evidence.

### Definitions (finding 5)

- A **consequential problem** is a statement the plan relies on or claims
  beyond the evidence then available to the planner, where the difference
  could change the deduction amount, who may claim it or the readiness claim.
  A deliberate conservative block the planner accepts is not a problem.
- An **omission** enters the plan at the first completeness or readiness
  claim that depends on it, not at the snapshot where it might have been
  considered.
- A **useful finding** names the item, the cue visible in the plan before the
  reliance, and what made the reliance attractive at that point. "The agent
  assumed something" is not useful.

### H3 scoring (finding 6)

The challenge may supply the affected action and a known-versus-chosen frame,
so naming the premise and declaring it "chosen" earn credit only when the
tool record shows the claim is accurate. The evaluation weights new
investigation after the challenge and changes to dependent actions. At
delivery the facilitator records which actions depend on the challenged one.
Each episode is scored on its own.

### Blinding the evaluation (finding 7)

The evaluator works in three passes, recording each before the next:

1. With the plan histories, working accounts, tool records and trial logs
   only, it locates any consequential problem, its entry and what preceded it.
2. With the reference account added, it revises or confirms the reading.
3. With the hypotheses and observer notes added, it assesses H1–H3 and
   usefulness. It also judges which of the three null outcomes applies, if
   any: no relevant episode; explanations indistinguishable; observations too
   vague.

H2 concerns Trial 1. The Trial 2 reviewer receives each interval's tool-record
extract, so it does not challenge an evidenced claim as unevidenced.

### Challenge filter (finding 8)

A proposed challenge must cite grounds the planner can see: the snapshot text
and the sources it consulted. The facilitator checks only the listed rules,
never substance or likely effect, and records the reason for a rejection. If
the redraft also fails, nothing is delivered for that snapshot, and that is
recorded.

### Prompt (finding 9)

The prompt drops "an honest plan with open questions is a good result",
states the endpoint symmetrically, defines when to snapshot, and names the
workspaces neutrally (`workspace-<random>`).

### Observer notes (finding 10)

Each note is written and committed to the milestone branch before the
facilitator replies to the planner, and is never revised. Corrections are
appended as new entries.

### Reference account (finding 11)

Corrections are appended to the reference account, not edited into it.
