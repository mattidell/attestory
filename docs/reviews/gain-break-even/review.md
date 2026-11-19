# Review: gains and break-even sales reach Schedule D

Charter: `docs/reviews/gain-break-even/charter-review.md`. Range:
`github/main..HEAD` at `571f463c` (7 commits, 0 behind). Reviewer, fresh
context; governance not read.

## Verdict

**READY with notes.** The hand values are right by the 2025 instructions and
were computed from inputs only. The census claim holds. Every mutation I tried
for the four named failures made a test fail, with one exception: the code W
probe cannot tell `CODE_W_ON_GAIN` from the overlapping
`ADJUSTMENT_EXCEEDS_LOSS` (GBE-R1). Decision 2's bounds are correct. Counts are
exact.

Mechanical gate: PR #291 is a draft. On `571f463c`, `quick` passed and
`verify` stopped at "Draft PRs do not run the full gate", so the full suite has
not run on this head. This review does not anticipate that result.
`envelope_scan --range github/main..HEAD` exited 0.

## Findings

**GBE-R1 (Low, evidence).** `tests/test_gain_break_even_v96.py:112-120`. The
probe asserts the rule and `DEPENDENCY_INVALID`, plus a text grep for
`CODE_W_ON_GAIN` in the family file. Neither observes which constraint fired.
On any row with box 1g > 0 and proceeds >= basis, `ADJUSTMENT_EXCEEDS_LOSS`
(`family.f1099b-covered-w-st.v2.json:91-116`, g > floor_zero(e - d) = 0) fires
with `CODE_W_ON_GAIN`.

- **Reproduction (in memory, separate process):** patch
  `Evaluator.evaluate_member` to drop the `CODE_W_ON_GAIN` constraint. The probe
  still blocks and the test passes. Drop both constraints and line 16 publishes
  20,500, so the test fails.
- **Consequence:** the dollar block is protected, but the ADR-0062 Decision 2
  reason is not. If the code-W-on-gain constraint were deleted or rewritten,
  this test would not notice, and the page would explain the block only as an
  "adjustment exceeds loss".
- **Repair:** the saved page's line 1b section carries both meanings as reason
  sentences (verified). Assert the code-W-on-gain meaning sentence on line 1b.
  This needs the harness, or the test, to keep non-question reason sentences
  (track1.md already notes the harness drops them). Then drop the content grep.

**GBE-R2 (Info, documentation).** `gain-break-even-evidence/cases.py:9,11`
(and `compare.py:10`). The docstring says code B is "box B/E" and names "two
code W probes". The code (`hand.ROUTE`, p0.md) uses box A/D code B to lines
1b/8b, and `keys()` builds four probes. The code and the hand values are
right; only the prose is wrong. Repair: correct the docstrings.

**GBE-R3 (Info, cost).** `tests/test_gain_break_even_v96.py:19-22`. "A return
runs once" holds by construction: each key belongs to exactly one test, and the
probe and the ordinary keys are disjoint. The docstring gives no measured
figure. I measured both modules: 45 passed in 26 s wall, 227 CPU-s user on 10
workers. The slowest calls took about 22 s each under contention, against
about 3 s per warm run in one process. Repair: state the CPU cost beside the
wall time.

**GBE-R4 (Info, authority).** `gain-break-even.md:85-88` and
`p0.md:163-171`. The bound is correct, but the cited basis is weaker than it
needs to be. The Form 1040 instructions' Exception 1 (i1040gi line 7a: "no
capital losses, and your only capital gains are capital gain distributions")
is literally met by a return whose only sale nets zero, and it says "don't have
to", not "must not". The binding text is the Form 8949 instructions, Line 1:
"Enter all sales and exchanges of capital assets ... even if you didn't receive
a Form 1099-B". Filing is therefore required, or at least permitted with no
dollar effect. Repair: cite i8949 Line 1 in Decision 2.

## Questions

1. **Hand values: correct and independent.** `hand.py` reads only the case
   inputs. Checks I made against the local 2025 text extractions:
   - Standard deductions are 15,750 and 31,500. Worksheet line 6 is
     48,350/96,700 and line 13 is 533,400/600,050 (i1040gi 2476-2488).
   - The worksheet is not used when line 15 or 16 is zero or less and there are
     no qualified dividends (i1040sd 1077-1080).
   - Every Tax Table row the cases use matches the table text: single 5,000
     (503), 34,250 (3,875), 51,750 (6,305), 54,250 (6,855); joint 18,500
     (1,853), 36,000 (3,846), 38,500 (4,146).
   - I reran every worksheet by hand from line 1 to line 25. Single long-term
     gain: 885 + 3,875 = 4,760. Joint: all gain at 0%, 1,853. Mixed `lt-gain`:
     435 + 3,875 = 4,310; joint 1,853. Mixed `three`: line 9 = 7,500, line 17
     = 0, so 3,875; joint 1,853. Mixed `st-gain`: line 15 = -2,500, so the
     Tax Table applies.
   - Code B (g) = reported basis - correct basis, with (e) the reported basis.
     Code W full disallowance gives (h) 0.
   - Routing is A/D with an adjustment to 1b/8b, B/E to 2/9, C/F to 3/10, and
     covered with no adjustment to 1a/8a with no Form 8949.
2. **Census: sound.** I read the plugin and `census.py`.
   - The patch is installed in `pytest_configure`, before test modules and
     `live_session`/`entry_loop` bind `live_coordinate_run`, so session-driven
     runs are recorded too.
   - The family regex covers every 2025 sale family in content.
   - `census.json` shows v96 runs only on loss cells (covered st/lt, no1099b
     st/lt) and zero runs in `no1099b/lt/even`.
   - Independent grep: of the main-line tests that reference v96, only
     `test_cf_loss_limit_v96.py` and `test_plain_line_texts_v96.py` carry live
     sales. Both are in the census.
   - Limit: subprocess and tool-driven runs (for example `recorded_replay`) are
     outside a pytest plugin's view. The claim is about tests, so this does not
     change it.
3. **Tests: load-bearing except GBE-R1.** In-memory mutations of real
   observations (`codeb/st/gain`, `no1099b/lt/even`, `covered/lt/gain`,
   `mixed/st-gain`, `w/st/even`, the probe). Baselines passed and all 12
   mutations failed:
   - a gain's line 1b set to 0;
   - a gain's line 16 or 7a blocked;
   - a break-even's line 16 set to 1;
   - a break-even's line 10 set to -1;
   - the code W adjustment part dropped;
   - Schedule D left unfiled on a break-even;
   - QDCG skipped (table tax of 6,855);
   - worksheet line 17 wrong alone;
   - a preferential base on a long-term loss;
   - the probe computing;
   - the probe blocked by a different rule;
   - the probe asking a question.

   Engine-level mutation: GBE-R1. The QDCG skip is also caught by line 16 on
   every preferential case, because table tax and worksheet tax differ in each
   (6,855 vs 4,760; 4,146 vs 1,853; 4,775 vs 3,875).
4. **Decision 2: correct.**
   - Break-even filing: see GBE-R4 for the stronger citation.
   - Worksheet intermediates on non-preferential returns: with line 3 = 0, line
     5 equals line 1, so line 25 = min(table, table) = table. The engine's line
     16 equals what the instructions' Tax Table route gives. That is pinned by
     the line 16 value on every such return.
5. **Cost and counts: honest.**
   - Live: 28 tests (1 count, 26 ordinary, 1 probe) and 27 runs. Fast: 17 tests
     (7 + 8 + 1 + 1). Both match track1.md and plan Decision 1.
   - Wall time matches (26 s). CPU cost is not stated (GBE-R3).

## What I ran

- Orientation (`--ref HEAD`, review charter), with SHA verified. `git rev-list`
  against `github/main`: 0 behind, 7 ahead.
- I read every file in the range.
- `pytest tests/test_gain_break_even_v96.py
  tests/test_gain_break_even_hand_values.py --durations=5`: 45 passed, 26 s.
- Scratch scripts outside the repository, run in separate processes:
  - observation mutations through the test functions;
  - an `evaluate_member` patch that drops the code W constraints;
  - a saved-model read of the probe's line 1b reasons;
  - a Tax Table row check against the local i1040gi text.
- `python3 tools/envelope_scan.py --range github/main..HEAD`: exit 0.
- `gh pr checks 291`: `quick` passed; `verify` is the draft stop.
