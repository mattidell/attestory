# Fresh review: box C and F losses are limited and carried

Charter: `docs/reviews/cf-loss-limit/charter-review.md`. Object:
`github/main..HEAD` on `milestone/cf-loss-limit-2025` at `b3a7e292` (6
commits: plan, P0 evidence, decisions, Track 1 tests, review charter).
Fresh context; governance not read; builder threads not read.

## Verdict

**READY with notes.** The semantic claim holds and the tests are
load-bearing: P0's hand values match the 2025 Schedule D instructions,
and every chartered mutation is caught. The notes below are about
accuracy and cost, not about behaviour. Mechanical gate: PR #289 is a
draft, so `verify` has not run the full suite on this head. Only the
`quick` lane is green. Publication waits on a green `verify` on the
exact head.

## Findings (ordered by consequence)

**CFL-R1 (Low, evidence cost).** `tests/test_cf_loss_limit_v96.py:17-19`
says runs are "memoised per worker process so a control is run once
however many assertions read it". Under the repo's `-n auto --dist
worksteal`, the three tests that read one return land on different
workers. Measured with a counting wrapper around `live_coordinate_run`:
83 coordinator runs for 30 distinct returns (23 returns ran 3 times, 7
ran twice), 325 CPU-s user for 40 s wall on 10 workers. Scenario: each
full-suite run pays about 2.8x the necessary CPU for this module (about
5.4 CPU-min instead of about 2). Smallest repair: assert lines, boundary
and parity in one test per key (the parity test reads the control's
memoised run), or group a key's tests onto one worker. Then restate the
cost.

**CFL-R2 (Low, evidence accuracy).**
`cf-loss-limit-evidence/track1.md:8,16,39` says the module runs "24 of
P0's 90 returns" with "6 A/D controls", and that the boundary test runs
"on all 24 returns". `AD_KEYS` (`tests/test_cf_loss_limit_v96.py:41`) is
3 shapes x 2 statuses x 2 sizes = 12 controls, so 30 returns. The 72-test
count agrees with 30 (30 + 12 + 30), not 24. Scenario: a later reader
sizing cost or coverage from track1.md undercounts the controls by half.
Repair: correct the counts. The run-time line also needs correcting with
R1.

**CFL-R3 (Low, plan consistency).** The plan's machine-read header
(`docs/phases/engine-breadth/milestones/cf-loss-limit.md:8`) still
scopes the milestone to "the right 2026 carryover". Decision 1 narrowed
the milestone to the limit. `build_orientation_block.py` prints the
header scope, so this review's own Orientation Block states a scope the
milestone has decided not to meet. Scenario: a closeout or later reader
checking scope against outcome sees an unmet deliverable. Repair: narrow
the header scope (and the title, if desired) to match Decision 1, and
point at the parked item.

**CFL-R4 (Low, boundary evidence strength).**
`test_no_2026_carryover_published` (`tests/test_cf_loss_limit_v96.py:106-114`)
detects an outbound carryover only by name. It looks for a published
symbol containing "carry" or "2026" outside a three-name allowlist
(`cases.py:192-193`). It would not detect an outbound amount published
under a symbol without those substrings, or an amount shown only in
page text. The parity test (`:94-100`) compares `carryover_published`
but not `carry_or_2026_symbols` or `page_carryover_mentions`, both of
which `compare.py:83` did compare in P0. Scenario: a future content
change adds line-21 page text saying "2,000 carries to 2026" for one
route. The live module stays green. Repair: assert that
`page_carryover_mentions` carries no 2026 amount, and add the two
fields to the parity loop. The mutation below that injects a carryover
symbol is caught; this finding only bounds what the test can see.

**CFL-R5 (Info, test isolation).** `cases.py:38-48` loads
`audit_harness.py` and `hand.py` through its own `importlib` `_load`
rather than `tests/evidence_loader`. So the harness is a process-global
`sys.modules` entry, not the owning module's private, snapshot-guarded
copy. Compare `tests/test_plain_line_texts_v96.py:41`, which preloads
the harness through `evidence_loader`. Today this is harmless: the names
are unique, and the harness's only engine write (`audit_harness.py:107-112`,
loader entries) runs only for a scratch core with `loader_from`, which
v96 does not set, and is restored in `finally`. The test's own preload of
`hand.py` (`tests/test_cf_loss_limit_v96.py:56`, `cfl_t1_hand`) is dead
code: `_hand` uses `cases.hand` (`cfl_p0_hand`). The tests also depend on
two evidence directories (`cf-loss-limit-evidence` and
`sale-family-audit-evidence`). An edit to either changes what the tests
build. Repair, if wanted: preload the harness through `evidence_loader`
under the name `cases.py` uses, and drop the unused load.

**CFL-R6 (Info, decision wording).** Decision 1 says ADR-0058 and ADR-0060
"forbid" the 2026 carryover. Both Decision 7 texts are accurate as
quoted (accepted; ADR-0058 line 120, ADR-0060 line 150). ADR-0058's,
however, is phrased as "This milestone ... does not derive or publish".
Whether computing the 2026 carryover needs a superseding ADR or a new
one is the owner's question that Decision 2 already parks. The parked
wording question is stated accurately. No repair is needed for this
milestone.

## Answers to the charter questions

1. **Hand values are correct and independent.** `hand.py` imports
   nothing from the engine. I checked the rules it cites against the local
   2025 sources:
   - i1040sd "Capital Losses" (limit $3,000, or $1,500 married filing
     separately).
   - Line 21: a carryover exists when the line 16 loss exceeds the line 21
     loss, or when line 15 would be negative.
   - Capital Loss Carryover Worksheet lines 1-13. `hand.py` reproduces
     them, including the line 1 "would be a loss" (`raw_line15`) and the
     zero floors.
   - i1040gi 2025 standard deductions: 15,750, 31,500 and 23,625.

   I recomputed by hand: separately, split 1,750/1,750 gives line 21
   (1,500), line 15 32,750, and carryover 250 short-term and 1,750
   long-term. Single, split 2,500/2,500 gives 0 short-term and 2,000
   long-term. Joint, 3,500 short-term, gives line 15 15,500 and 500
   carried. All agree with the companion's literals. Every status is
   covered in P0 (90 returns), including separately at 1,500 and above it.
2. **The tests assert hand values and catch the named defects.** Results
   of in-memory mutations, each run as a pytest plugin in a separate
   process with nothing written to the worktree:
   - Separate-return limit set to 3,000 (patched
     `live._parameters_by_exact_version`): 6 failures, every separately
     `above` return in both routes.
   - Box C dropped from Schedule D line 7 (line 3 ref replaced with 0 in
     the resolved rule): 20 failures (`st` and `both` C/F returns, lines
     and parity).
   - Box F dropped from line 15 (line 10 ref replaced with 0): 20 failures.
   - Injected publication `capital-loss-carryover-to-2026.short-term`: 30
     failures, every boundary test.
   - Setting `hand.LIMIT` separately to 3,000 makes `hand.values` return
     line 21 of -3,000 where the companion expects -1,500, so the companion
     catches drift in the hand function.

   The mutation evidence covers coverage. The isolation caveat is CFL-R5,
   and the strength of the name-based boundary check is CFL-R4.
3. **Decision 1 is supported.** P0 reports 900/900 line checks and C/F
   equal to A/D on 45 pairs. The live module reproduces this on 30
   returns. Decisions 2-3 are stated accurately (CFL-R6).
4. **Cost is proportionate but misreported.** 40 s wall is reasonable for
   30 coordinator-and-page returns, and the live mark is honest. The
   memoisation claim and the counts are wrong (CFL-R1, CFL-R2).

## What I ran

- `build_orientation_block.py --ref HEAD --charter ... --role reviewer`:
  SHA `b3a7e292` equals HEAD. `github/main...HEAD` is 0 behind and 6
  ahead.
- `pytest tests/test_cf_loss_limit_v96.py tests/test_cf_loss_limit_hand_values.py`:
  82 passed, 40.9 s.
- The four in-memory mutation runs of the live module (above), plus one
  run with a coordinator-call counter under `/usr/bin/time` (83 calls, 30
  distinct, 325 s user).
- A hand-function mutation in a separate `python3 -I` process.
- `mypy` on the two test modules: clean. `tools/governance_lint.py`:
  conformant. `tools/envelope_scan.py --range github/main..HEAD`: exit 0.
  No absolute or temporary paths found in the committed evidence or
  tests.
- `gh pr checks 289`: `quick` pass; `verify` fails only on the draft
  guard ("Draft PR: the full suite has not run on this head").
