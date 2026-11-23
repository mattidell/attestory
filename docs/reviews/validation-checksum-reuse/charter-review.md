# Charter: fresh review of validation reuses member checksums

Role: Reviewer, fresh context. Source HEAD on
milestone/validation-checksum-reuse-2025. Plan:
docs/phases/engine-breadth/milestones/validation-checksum-reuse.md (read it
whole, especially Decisions 1-2). Evidence:
validation-checksum-reuse-evidence/track1.md. Range: `github/main..HEAD`.
Do not read governance.

## Questions

1. **Correctness first.** Can a reused checksum ever stand for bytes other
   than the ones being validated? Construct the cases: a citizen file
   changed on disk after a cached read; two files with the same bytes at
   different paths; a cache entry from another corpus or release; the
   cache cleared, half-cleared or not cleared between runs; a mutated
   in-memory view. For each, does validation still catch the change, and
   does the memo key still change?
2. **Byte identity.** Does the evidence (775 lists byte-identical) support
   "no output changed"? Rerun a sample of at least 100 lists yourself
   before and after.
3. **Speed claim.** Do the paired timings support the stated gain, and is
   it worth the added code?
4. **Scope.** No `packages/kernel/` edit; no package, content, schema or
   projection change; the clear hooks clear the new state.
5. **Tests.** Do the new tests fail if reuse ignores a byte change, if the
   memo key stops including a member checksum, or if a clear hook stops
   clearing? Mutate in a scratch copy; do not commit mutations.

## Output

docs/reviews/validation-checksum-reuse/review.md: a verdict (READY, READY
with notes, or NOT READY), numbered findings (VCR-R1 …) each with
file:line, a concrete failure scenario and a severity, and what you ran.
Commit only that file under `$(git rev-parse --git-dir)/collaboration-commit.lock`
with separate simple commands. Bound every command that can hang; never
`rm -rf`. No code edits, no push, no spawn.
