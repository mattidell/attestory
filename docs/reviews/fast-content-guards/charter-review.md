# Charter: fresh review of content guards run in the fast lane

Role: Reviewer, fresh context. Source HEAD on
milestone/fast-content-guards-2025. Plan:
docs/phases/engine-breadth/milestones/fast-content-guards.md. Evidence:
fast-content-guards-evidence/track1.md. Range: `github/main..HEAD`. Do not
read governance.

## Questions

1. **Same guard.** Reconstruct every removed size guard from github/main
   yourself and compare with `tests/test_content_file_sizes.py`: same files
   (including files added later that a glob would pick up), same caps,
   every exception kept with its reason. Is any guard that checked a
   non-rule file, or a different glob, lost? Are there size guards the
   inventory missed (`git grep st_size -- tests`)?
2. **Fast and honest.** Is the module collected under `-m "not live"`, and
   does it fail the fast lane when a covered file grows past its cap
   (mutate a scratch copy; restore)? Does it fail when a new
   `rule.qdcg-worksheet.*` file appears?
3. **Observer test.** Does clearing FORCE_COLOR and NO_COLOR in the child
   weaken what the test checks? Does it still fail if the observer writes
   anything besides the JSON record?
4. **Nothing else moved.** Tests only; no cap or exception changed;
   tests/conftest.py unchanged.

## Output

docs/reviews/fast-content-guards/review.md: a verdict (READY, READY with
notes, or NOT READY), numbered findings (FCG-R1 …) each with file:line, a
concrete failure scenario and a severity, and what you ran. Commit it
under `$(git rev-parse --git-dir)/collaboration-commit.lock` with
separate simple commands (mkdir lock; git add that one path; git commit
-F file; rmdir lock). Bound every command that can hang; never `rm -rf`.
No code edits, no push, no spawn.
