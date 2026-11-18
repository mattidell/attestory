# Charter: Track 1 of the Rust kernel experiment (Python algorithmic fixes)

Role: Builder. Source HEAD on milestone/rust-kernel-experiment-2025.
Plan: docs/phases/engine-breadth/milestones/rust-kernel-experiment.md
(read it whole, especially Decisions 1-4). Evidence:
rust-kernel-experiment-evidence/p0.md and its scripts (p0_timing.py,
p0_profile.py). Do not read governance.

## Scope

0. **Baseline first, before any code change.** Write a dump script in the
   evidence directory that replays all 775 recorded lists (parallel
   shards, CPU count minus one) and records, per list, a SHA-256 of the
   canonical result, of the saved page bytes, and for erroring lists the
   exception class and message. Run it on the unchanged code; keep the
   full dump outside the repository and commit only a small summary
   (counts and a digest of the per-list hashes). Also record package
   validation's full error list for the published v96 package and for
   at least three invalid package mutations, so the order of errors can
   be compared.
1. **Validation index** (`packages/derivation/package_validation.py`,
   the member-inside-member scan P0 cites near lines 3268-3274): index
   the members once so the source-family check is linear. Same errors,
   same order.
2. **Validate once per package bytes.** Remove the second validation of
   identical package bytes in one replay (P0: prep's handover and the
   run each validate; 7252 files read each run). Prefer a memo keyed on
   a content checksum of the exact bytes, scoped so a changed file can
   never hit a stale entry; say where the memo lives and its lifetime.
   If the duplicate is only in the evidence harness, fix it in `tools/`.
3. **Closure-walk memo** (`packages/derivation/presentation_projection.py`,
   the walk near lines 535-633): memoize per projection call so shared
   blocked rows are walked once, and index resolved members so
   `meaning_for` does not rescan. Keep it inside the walk functions
   (Decision 4).
4. **Marshal precompute** (`packages/derivation/marshal.py`,
   `_rule_required_symbols` near line 715): compute once per rule.
5. **Prove and measure.** Rerun the dump on the changed code: every list
   byte-identical to the baseline, and the validation error lists
   identical. Then re-time all 775 lists as P0 did and re-profile the
   median, slowest and K13 workloads; report the new layer table and
   what now dominates. Add focused tests: each memo returns the same
   output as the unmemoized path on a synthetic case, and a changed
   input misses the memo.

No edit under `packages/kernel/`. Stop and report if a fix cannot be
made byte-identical, or needs a schema, content or kernel change.

## Deliverables

Code changes in packages/derivation/ (and tools/ if item 2 lands there),
tests under tests/, and in the evidence directory: track1.md (each fix,
the identity proof, before/after timing and layer tables, what dominates
now, whether a kernel port now pays), the dump and timing scripts and
small JSON summaries. One commit per item where practical. This is
substrate work: run the full suite (`pytest`) and `python3 -m mypy` per
the repository's configuration before you finish, and report both.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks, so a usage limit
  does not lose it; update it when the checks finish.
- Never --no-verify or a bare git stash. Foreground commands only; do not
  leave background jobs running when you finish.
- No push and no spawn. Do not edit packages/kernel/, packages/content/
  or packages/schemas/.
