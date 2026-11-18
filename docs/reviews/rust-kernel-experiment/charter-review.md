# Charter: fresh review of the Rust kernel experiment (P0 + Track 1)

Role: Reviewer, fresh context. Source HEAD on
milestone/rust-kernel-experiment-2025. Plan:
docs/phases/engine-breadth/milestones/rust-kernel-experiment.md (read it
whole). Evidence: rust-kernel-experiment-evidence/p0.md and track1.md
with their scripts and JSON. Range under review: `github/main..HEAD`
(compare against main at 7c043135). Do not read governance.

## Questions

1. **Identity.** Does the evidence prove that every recorded list's
   result, page and error is byte-identical before and after Track 1?
   Check how the baseline was produced (a pristine export of 0763f572),
   what the dump hashes, and whether anything a filer sees could differ
   yet hash the same. Re-run the comparison on a sample if cheap.
2. **Memo safety.** For each memo or index in `packages/derivation/`
   (package-validation memo in production_resolver.py, the source-family
   index, the closure-walk memo, the marshal precompute): can any input
   change reach a stale entry in a long-lived process, a test that
   monkeypatches, or a package whose member bytes change? Is the memo's
   lifetime and size bounded? Is any mutable value shared between
   callers that could be mutated after caching?
3. **Validation order.** Is the claim "same multiset always, same order
   under a fixed seed" true of the pristine code and the changed code?
   Does any consumer depend on order?
4. **Tests.** Do the new tests fail when their memo is wrong (stale hit,
   missed key field, changed walk)? Are the live markers honest?
5. **Conclusions.** Do P0 and Track 1 support the plan's Decisions 1-2
   and the claim that a kernel port does not pay on recorded lists
   today? Is anything overstated?

## Output

docs/reviews/rust-kernel-experiment/review.md: a verdict (READY,
READY with notes, or NOT READY), numbered findings (RKE-R1 …) each with
file:line, a concrete failure scenario and a severity, and what you ran.
Commit it under `$(git rev-parse --git-dir)/collaboration-commit.lock`
(mkdir … rmdir), staging that one path. No code edits, no push, no
spawn. Run pytest only to confirm a specific failing claim.
Synthetic demo.* only; no absolute paths in committed files.
