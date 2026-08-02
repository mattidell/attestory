# Charter — The Entry Loop (synthetic), milestone close

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Last build unit: `146aede` (Track 4), inspected at
  `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-29-entry-loop-synthetic-track4-foreman-inspection.md`
- **This unit opens the close PR against `main-ui`.** It is the last unit in the
  milestone. There is no review gate; the PR is the gate, and the owner is the
  reviewer.

## What this milestone set out to do, and what happened

It set out to let a person go from an incomplete synthetic return to a computed
one by typing W-2 facts into a surface, without opening a text editor — and to
prove that with a usability evaluation written before the code existed.

The loop works. The evaluation failed on one row. That is the honest result and
the close reports it as such.

**The cell stays at L1.** Two independent evaluation rounds scored the W-2 cell;
the second returned FAIL on the accessibility baseline. Track 4 repaired the
defect, but nothing re-scored the surface afterwards, so the cell does not move.
Do not move it. Do not describe the repair as satisfying the criterion — it
removes the known cause of a failure that still stands as the recorded outcome.

## What to write

### 1. The milestone record

The plan document already carries per-track outcome sections through Track 4. Add
what is missing to close it: the overall outcome, the maturity disposition, and
the retrospective. Write for a reader who knows the product and not the record.

Say plainly:

- What a person can now do that they could not before, and what they still
  cannot.
- That the evaluation failed, on which row, and why the cell therefore stays at
  L1.
- That the durable deliverable of this milestone is the entry-field contract, not
  the surface. The surface may well be thrown away; `entry-field.v1` is meant to
  survive it.

### 2. The retrospective

Write it at `docs/milestone-retrospectives/2026-07-29-entry-loop-synthetic.md`.
The plan metadata already declares that path, and
`tools/foreman_context.py` refuses a `closing` state without it, so the file must
land in this unit.

Four things happened here that are worth a later reader's time. Cover them, and
be specific rather than diplomatic:

- **The criteria document held under pressure.** It was written before the code,
  scored twice unchanged, and both times it found something real. Two rounds of
  charters were explicitly forbidden from amending it. That is the mechanism
  working, and it is the strongest evidence this milestone produced about method
  rather than product.
- **Three rejections in Track 3, all correct.** The pattern in every one was the
  same: the build added machinery that asserted something untrue — a
  discriminator that did not discriminate, regressions that never reached the
  code they guarded, an equality check that could not be false. All three closed
  by **subtracting**. Name that pattern, because it will recur.
- **Two vacuous-test failures, one caught by a reviewer and one by the foreman.**
  The Track 3 F2 fixtures failed at a marker check before validation ran. The
  Track 4 focus test, mutation-tested naively, fails at the surface checksum gate
  before it measures anything. Both are the same shape: *a test that fails
  earlier than the thing you are probing tells you nothing.* Record the
  operational consequence — a content-tree mutation on this surface must be
  followed by `python3 -m tools.generate_entry_loop_t1_fixtures` before the
  result means anything.
- **The foreman's own two defects.** `milestone_state` was set to `track-2e`,
  which `tools/foreman_context.py` rejects, so **both** Track 2e evaluators ran
  with no orientation block. And the Track 4 charter's root-cause diagnosis was
  wrong — it blamed a per-context model that never included the input, when the
  actual cause was a Svelte scoped-style specificity tie. Both are already
  recorded in their own records; carry them into the retrospective rather than
  leaving them buried, because the pattern of phase-state pointer drift is now on
  its third occurrence.

### 3. Findings and limits carried out of the milestone

These are the open items. Each needs one honest sentence; none needs fixing here.

- **The harness cannot measure keyboard operability.** Four evaluators across two
  rounds could not verify Tab/Enter/Space behaviour, so a *mechanical* criterion
  has gone partly unverified twice. The foreman resolved it at source level — all
  controls are native `<button>`, so Enter/Space works by construction — but an
  evaluator was not permitted to do that. This is a gap in the instrument, not in
  the surface, and it is the most important thing to fix before the next
  evaluation.
- **The accessibility row bundles five requirements** into one Pass/Fail. A
  single defect in one of them fails all five, which loses information the
  scoring procedure needed. A future criteria revision should split it.
- **Criterion 2.3's "without guessing" bar conflates two things** — whether the
  format is stated, and whether it is stated well. Note it; do not amend the
  document.
- **The substitution seam's guarantee is untested.** `entry_loop.py` reads a JS
  `export const` by string-marker indexing plus one regex substitution, refusing
  when the match count is not 1. That refusal is what now guarantees the served
  format is this runtime's own, and it has no test of its own. It should be
  closed by whoever performs the canonical-JSON migration, which is the point at
  which a real equality constraint becomes necessary. Restate the migration
  recommendation with that condition attached.
- **The contract is extracted from one money field.** Whether `source`,
  `destination`, `purpose`, and `correction` survive as a shared core is unknown
  until a second fact family exists. `entry-field.v1` validates
  well-formedness and that `format` names a supported variant; it does not check
  that the variant is *correct* for the named source. A declaration naming an
  employer while claiming a currency format is a false declaration, not a
  malformed one, and nothing here catches that.
- **Two carried findings from earlier tracks:** the kernel's `apply_contribution`
  masks `entry_loop.py`'s staleness check; `launchChrome()` leaves an orphan
  process and a `mkdtemp` leak if the caller is killed.
- **New starting-state fingerprint**
  `sha256:ac7735a5d9ab4e057e193966aec89df7534e478ee329e47e9f7b8b19018b79e8`,
  superseding `sha256:212e525d…`. Any future re-score is against the new one.

### 4. The two ADRs go to the owner

**ADR-0049** (Surface Artifact) and **ADR-0051** (Entry Surface Contract) are both
`proposed`, and five tracks of dependent work now rest on them. **Do not change
their status.** Ratification is the owner's act on this PR.

What you must do is make them ratifiable: for each one, state in the PR body what
was built against it, what the milestone learned that the ADR does not yet say,
and whether anything in it turned out to be wrong. An owner should be able to
ratify or amend from the PR body without reading five tracks of history.

### 5. Phase state

Set `milestone_state` to `closing` and update the prose sections. Keep the
`milestone_state` value inside the allowed set — `closed`, `closing`, `planned`,
`planning`, `track-<n>` — and put any sub-unit detail in the prose fields, not in
the state token. Verify with `python3 tools/foreman_context.py --ref HEAD` after
committing, since the tool reads a committed ref rather than the worktree.

While you are there: the Re-entry section invokes `.venv/bin/python3`, and this
project has no `.venv`. Fix it to system `python3`.

Do **not** select the next milestone. The frontier is the owner's, and a
phase-boundary legibility audit is due and is owner-spawned.

## Boundaries

- Do not move the maturity matrix. The W-2 cell stays at L1.
- Do not re-score, and do not amend
  `docs/phases/legible-entry/entry-usability-criteria.md`. Two evaluation rounds
  rest on it at `1e48443`.
- Do not ratify, amend, or restatus ADR-0049 or ADR-0051.
- Do not fix any carried finding. Record them.
- No code changes beyond the phase-state path fix. If you find yourself editing
  `packages/`, stop and report instead.
- No second fact family, no real data, no residency locator, W-2 and synthetic
  throughout.

## Verification

Run the CI `verify` sequence and the data-safety scan, and record them in the
commit message: `python3 -m pytest -n auto -q`, `python3 -m mypy`,
`python3 tools/governance_lint.py`,
`python3 tools/envelope_scan.py --range origin/main-ui..HEAD`. The foreman
reproduced all of these at `146aede` — 723 passed / 3245 subtests, mypy clean on
135 source files, lint conformant, scan clean — so a deviation means this unit
introduced it.

No content tree changes here, so no fixture regeneration should be needed. If the
byte total moves, something is wrong; say so rather than regenerating.

Orient with `python3 tools/foreman_context.py --ref HEAD --format markdown` and
`python3 tools/build_orientation_block.py --ref HEAD`. If either refuses, stop and
report it. No `.venv`; use system `python3`.

## The PR

Base **`main-ui`**, not `main`. Title it as the milestone close. The body is the
owner's decision surface, so it needs, in this order: what a person can now do;
that the evaluation failed and the cell stays at L1; the two ADRs with what to
ratify and what to amend; the carried findings as a short list; and the
instrument gaps to fix before the next evaluation.

Keep it product-facing and plain. No governance commentary.

## Report back

The outcome and retrospective as written; the carried-findings list; for each ADR,
what the milestone proved and what it did not; the phase-state change and that the
capsule renders from the committed ref; and the PR number.
