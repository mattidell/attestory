# Charter: fresh review of member files are read once

Role: Reviewer, fresh context. Source HEAD on
milestone/member-reads-once-2025. Plan:
docs/phases/engine-breadth/milestones/member-reads-once.md (read it
whole). Evidence: member-reads-once-evidence/track1.md with its scripts
and JSON. Range under review: `github/main..HEAD`. Do not read
governance.

## Questions

1. **Staleness.** Can any caller ever receive a parse or checksum for
   bytes other than the ones it read in that call? Check the key, the
   read path, every consumer of `_member_candidates` (including
   surface_resolver.py) and the interaction with the validation memo
   from rust-kernel-experiment.
2. **Sharing and mutation.** Can a caller mutate a cached parse through
   the read-only view, a nested container inside it, or a body handed
   out without a copy? Is the copy deep enough for every consumer that
   mutates?
3. **Bounds.** Is the 4,096-entry LRU (about 79 MiB) acceptable under
   the test suite's parallel workers and CI? Is there any growth path
   the bound does not cover?
4. **Identity and timing.** Does the evidence prove 775/775
   byte-identical and the validation errors unchanged? Are the timing
   claims fair given the loaded machine (ratios against a pristine
   export under the same load)?
5. **Tests.** Do the new tests fail when the cache is wrong (stat-only
   key, shared mutable body, missing clear)? Mutate in memory to check;
   do not commit mutations.

## Output

docs/reviews/member-reads-once/review.md: a verdict (READY, READY with
notes, or NOT READY), numbered findings (MRO-R1 …) each with file:line,
a concrete failure scenario and a severity, and what you ran. Commit it
under `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir …
rmdir), staging that one path. No code edits, no push, no spawn. Run
pytest only to confirm a specific failing claim. Synthetic demo.* only;
no absolute paths in committed files.
