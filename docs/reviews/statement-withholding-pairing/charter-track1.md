# Charter: Track 1 of statement withholding pairing

Role: Builder. Source HEAD on milestone/statement-withholding-pairing-2025.
Plan: docs/phases/engine-breadth/milestones/statement-withholding-pairing.md
(read it whole: P0 result, Decisions, Tracks). P0 evidence:
statement-withholding-pairing-evidence/p0-reproduce-and-design.md, its
probe and prototype. Do not read governance.

## Scope

1. **The operation.** A guard expression in `packages/derivation/evaluator.py`
   that, over current sources, checks every row of each named income fact
   type has at least one current row of the named withholding fact type on
   the same identity key (`statement`, or `w2-slip`). Name it plainly (for
   example `require_paired`). On failure it raises `EvalBlocked` with
   `BLOCK_ABSENT` and `missing` naming the withholding fact type, so the
   v72 input question for that amount still shows. A null or missing key
   blocks, as `shared_key_count` does. It reads no values. A withholding
   row with no income row is not a failure. Record what it read in the
   access log the way `count` and `shared_key_count` do, so pins and
   presentations are honest. Check `authorization_closure.py` and any
   other op walker that must learn the new op.
2. **Schema.** `rule-artifact.v15` adds only the operation, under the
   AGENTS.md "Schema Publication Protocol" (`write_manifest`, add-only
   manifest diff, `pytest tests/test_schema_registry.py`). Any package
   schema that must admit v15 rules follows the same protocol.
3. **ADR 0083, status proposed** (`docs/adr/0083-...md` and a row in
   `docs/adr/INDEX.md`): the operation's contract — what it reads, when it
   blocks and with what, the key, what it does not do. Short.
4. **Content.** Line 25b and line 25a successors on `rule-artifact.v15`
   that keep their current `when` closures and value, and replace the count
   comparisons with the pairing check: line 25b over the ten subject fact
   types in P0's table (INT boxes 1, 3, 8, 10; DIV 1a, 2a, 12; IRA box 1;
   1099-G box 1; SSA-1099 box 5), line 25a over W-2 box 1 on `w2-slip`.
   Core v77, registry v75, release v75 with `tools/package_successor.py`;
   a loader companion entry sharing v76's declaration.
5. **Cases.** `tests/test_statement_withholding_pairing.py`: P0's 44 rows
   and the W-2 rows on v77 through `live_coordinate_run`. The ten 25b
   defect rows and the W-2 4600 row block naming the withholding fact and
   show its existing question; every answered row, the $0 answer and the
   withholding-only extra publish v76's amount; a return with no Form 1099
   and a joint return with one statement per spouse are unchanged. v76
   and earlier byte-identical.
6. **Run** mypy on changed files, the fast lane, and the full suite
   (substrate change). Write `statement-withholding-pairing-evidence/track1.md`
   (what landed, cases table, suite lines) and fill the plan's "Track 1
   result" section.

## Stop conditions

Stop and report if the operation cannot name the missing withholding fact
without a change under `packages/kernel/`, if a published schema or
manifest entry would change, or if an earlier core's golden or byte output
moves. Do not edit `packages/kernel/`.

## Rules

Synthetic demo.* only; no absolute paths in committed files. Commit
incrementally with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
retry every 10 s up to 5 min if held); never --no-verify; never bare git
stash. Foreground commands only; no pgrep or sleep waiters. No push or
spawn.
