# Retrospective: Two Members With the Same Name Each Get Their Question

Milestone key: same-label-members. Plan:
`docs/phases/engine-breadth/milestones/same-label-members.md`.
Closed 2026-11-26. Projection only; no package, schema or page change.

## What happened

eic-child-answers parked ECA-R7: two roster members recorded with the same
label share one question reason. P0 found the cause in one place. The
question walk recorded a member's missing answer by fact type and label,
so two children named "Sam" who each missed an answer got one question. It
also found that telling the two apart needs a field ADR 0087 did not
decide, because an entity has only an id, a kind and a label.

The foreman split the work. Keying by the member is what ADR 0087 already
says, so Track 1 built that as a defect fix. The new `memberOrdinal` field
went into a draft ADR for the owner. The full-surface replay was identical
on all 775 recorded lists. Only the 9 probe returns with same-named members
missing the same answer changed, each by the added questions. The fresh
review was READY with two small repairs: three more live cases and a
miscounted sentence. Two notes carry to Track 2.

## What worked

- Splitting the defect fix from the new contract let the fix ship without
  waiting on an owner decision.
- Tests that fail on the parent commit, checked by the reviewer in a
  separate worktree, made "this fixes it" a tested claim.

## What to change

- The reviewer stalled for two hours on its last command, a heredoc that
  writes the report. The foreman recovered the text from the transcript.
  Check a quiet reviewer's transcript at the first heartbeat, not the
  third.
- A proposed ADR filed on the branch would have merged unaccepted. Keep an
  unaccepted ADR as an evidence draft and file it only on acceptance.
