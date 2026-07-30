# Charter — The Entry Loop (synthetic), Track 1 repair review

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Under review: `2e62c4a` — 2 files, 272 insertions, tests only
- Repair charter: `docs/reviews/charter-2026-07-29-entry-loop-synthetic-track1-repair.md`
- Prior review: `docs/reviews/2026-07-29-entry-loop-synthetic-track1-review.md` (`NOT READY`)
- Verdict: `READY` or `NOT READY` **for Track 1 as a whole**, with numbered findings.

## What changed since the last review

The prior review returned `NOT READY` on three findings. One of them is gone by
decision rather than by work, and you should read that decision before the
review it disposes.

**F1 is withdrawn.** It enforced ADR-0048's requirement that an entry surface
launch with spellcheck's network path affirmatively closed by a vehicle-level
flag. The owner withdrew that requirement on 2026-07-29. **ADR-0051**
(`docs/adr/0051-entry-surface-contract.md`) supersedes ADR-0048 Decision 1:
browser and workstation behaviour are the owner's trusted environment, not the
entry surface's contract. ADR-0048 Decision 2 — the contribution boundary — is
untouched and still binds.

The prior review is not rewritten and is not wrong. It applied the rule in
force. Your job on F1 is to dispose it: confirm the premise changed, and
confirm nothing in the source or its comments presents `spellcheck="false"` (or
any other browser setting) as a security control, which ADR-0051 does forbid.

F2 and F3 are what the builder worked on.

## Measurements

**1. Are the seven fail-closed tests non-vacuous?** This is the main spend. The
prior reviewer manually exercised wrong content type, oversized body, malformed
JSON, JSON type confusion, template tampering, duplicate submission, and
out-of-order submission, and found all seven already failing closed. So these
tests were written against behaviour that already passed — the exact condition
under which a test can assert nothing and still be green. For each: break the
thing it guards and confirm it fails. A test that only checks a status code has
not covered the finding; the prior review's concern was fail-closed in three
parts — the refusal, no echo of the rejected value, and no advance of the act
log. Say which of the three each test actually asserts.

**2. Does the browser test drive the real compiled client?** F3's gap was that
nothing exercised the built page's own relative `./api/*` requests. The repair
launches real Chrome through the presentation harness and drives the built
page. Check that the assertions rest on the client's own requests and observed
state rather than on anything the test issues itself, and that a contribution
entered this way reaches the act log the same way the Python-side tests show.

**3. Is that test real coverage or a test that never runs?** It is guarded by
`skipUnless` on Node, a local Chrome, and the vendored tree. A skipped test is
not coverage, and this project already carries six surface tests that skip
without the vendored tree. Say plainly whether this one runs on the machine of
record and whether it runs in CI, and if it does not, whether F3 is actually
closed or merely written.

**4. Data safety, with a live browser in the loop.** A test that launches
Chrome is new for this suite. No residency locator in launch arguments,
profile paths, page URLs, console output, or failure text. Confirm the browser
runs against the synthetic workspace only, and that a failed or timed-out run
leaves nothing behind that a later run or a scan would trip over. Run the scan,
then read for what a scan cannot see.

**5. Regression and scope.** The diff should be tests plus one helper, and no
product code. Confirm that. Confirm the four Phase A dependency tests are
untouched — you mutation-tested them last time and they held; a repair that
adjusted them would be the thing most worth catching here.

**6. Verification.** `2e62c4a` records the full sequence from `5275ed0` with no
omissions and 711 tests passing. Re-run it and say whether the claims hold.

## Boundaries

- Do not fix anything. Report findings.
- Do not score the usability criteria. That is Track 2, under a fixed
  two-evaluator procedure, and doing it here would preempt it.
- No maturity claim; nothing moves on any matrix.
- Do not reopen F1 on its merits. If you think ADR-0051 is wrong, say so as a
  note to the owner, separately from the verdict.

## Verdict

`READY` or `NOT READY` for Track 1 as a whole — this is the gate that lets
Track 2 run the evaluation against this surface. Number each finding, say what
is wrong and what would close it, and separate findings that block from
findings that weaken.

Orient with `python3 tools/build_orientation_block.py --ref HEAD`. No `.venv`;
use system `python3`. Ratified line `origin/main-ui`, derived for you; the
merged PR #109 is this milestone's opening plan PR and does not mean the
workspace is spent.

## Report back

The verdict; each measurement; which of the seven refusals you broke and what
happened; whether the browser test runs or skips where it matters; and the
single thing most likely to be wrong that you could not prove either way.
