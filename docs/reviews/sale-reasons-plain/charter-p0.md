# Charter: P0 of sale reasons speaking plainly

Role: Builder. Source HEAD on milestone/sale-reasons-plain-2025.
Plan: docs/phases/engine-breadth/milestones/sale-reasons-plain.md (read
it whole). Precedent and tooling: plain-line-texts-evidence/ (census,
strict replay classifier, mutation controls) and its p0c.md and
track0.md for how wording was checked against every drawn state. Do not
read governance.

## Scope

1. **Census.** On published core v96, find every place either reason is
   drawn on a saved page: which content files and fields carry it (the
   sale family files under packages/content/tax/2025/ hold both texts,
   for example family.f1099b-noncovered-st.json and the covered-w
   families), which page fields show it, on how many of the 775 recorded
   lists, and in which states (holding-period mismatch; wash-sale
   amount block with the adjustment family open, closed, or the
   computation refusing). Cite file:line. Record any other filer-visible
   sentence in the same citizens that still carries an engine term
   (formula names, block codes, ids, "family"), and list but do not fix
   texts outside these citizens.
2. **Draft.** One plain sentence (or a small set if states differ) per
   reason, checked against the 2025 Form 8949 and Schedule D
   instructions in the local sources. Say what is wrong and what the
   filer can check (the date acquired and sold, the box the broker
   checked, the wash-sale amount in box 1g). Each sentence must be true
   in every state where it is drawn; if one sentence cannot be, say how
   the states split.
3. **Scratch successor.** Content successors of the citizens that carry
   the sentences, on published v96, loaded from published content,
   never by editing packages/. Name every successor, its new version and
   how the package and registry must change; say whether the package
   validator's successor-graph table (packages/derivation/
   package_validation.py, `_successor_graphs`) pins any of them.
4. **Strict replay.** Replay the 775 lists on v96 and the scratch
   successor in parallel shards (CPU count minus one); compare every row
   and page field and fail any value, disposition, refusal code,
   missing-name or question change before labelling a change expected.
   Include mutation controls. Expected: only the replaced sentences
   change. Time pairs on a loaded machine are not needed; report wall
   time only.

Stop and report if a reason cannot be made true without an engine,
schema, projection or page change, or if it is supplied by the page
rather than content; name the smallest change.

## Deliverables

In docs/phases/engine-breadth/milestones/sale-reasons-plain-evidence/:
p0.md (census, trace, draft and source check, successor list, replay
classification, recommendation, decisions for the foreman), scripts and
small JSON outputs. Fill a "P0 result" section in the plan. No
production, test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn. Do not edit packages/ or
  tests/.
