<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "noncovered-sales",
  "status": "Open. P0 done: a content successor (core v79) with no engine or schema change. Owner decided the class, the misroute fix and C3. Track 0 adversarial closure runs before Track 1.",
  "scope": [
    "a return with a Form 1099-B sale whose basis the broker did not report to the IRS (Form 8949 box B or E) computes Schedule D and Form 1040 line 7 from a basis the filer supplies",
    "every return core v78 computes computes the same on the successor, and earlier cores render byte-identically",
    "what stays outside the class is refused by an answer, never computed partially"
  ],
  "non_goals": [
    "no digital assets, no short sales, no other Schedule D sources (K-1, Forms 2439, 4684, 4797, 6252, 6781, 8824)",
    "no basis worksheet or lot-selection tool beyond the amount the filer supplies",
    "no recording surface or entry-loop change unless P0 shows the class cannot be answered without one, and then only after owner direction",
    "no edit to packages/kernel/",
    "no edit to any published schema, adopted package or rule version; only successors"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/coverage-frontier.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/noncovered-sales.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/noncovered-sales.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/noncovered-sales.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/noncovered-sales.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Sales Whose Basis Was Not Reported (2025)

Milestone key: noncovered-sales.
Branch: milestone/noncovered-sales-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-06.
Starting point: `github/main` at `e73d32cf` (PR #260 merged; core v78 is
the latest).

## What we are trying to accomplish

The last ten milestones made the existing return honest and legible: every
missing answer is asked, each statement is checked for its own withholding,
and every line says what it adds. None added a filer the engine could not
serve before. This one returns to breadth. A brokerage filer who sold
shares bought before the broker had to track basis, or shares transferred
in, gets a Form 1099-B with box 12 (basis reported to the IRS) unchecked,
often with box 5 (noncovered) checked and box 1e blank. That
sale goes on Form 8949 box B (short-term) or E (long-term), with the basis
the filer supplies. Today such a return is refused by the Schedule D
boundary answer. The useful outcome is that it computes.

## What we know

- **The boundary.** `schedule-d-boundary-form8949-w.bundle.json` asks
  whether the return has no adjustment codes other than W, no multi-code
  rows, and no noncovered or basis-not-reported sources (ADR-0061
  Decision 4). A "no" refuses the return.
- **What exists.** Form 8949 attachment v2, Schedule D lines 1a, 1b, 7,
  8a, 8b, 15, 16 and 21, covered short- and long-term families, wash-sale
  adjustments (code W) on Form 8949 boxes A and D.
- **The frontier row.** `coverage-frontier.md` marks noncovered and
  basis-not-reported Form 8949 transactions "unblocked — requires re-cut
  contract" against ADR-0066's validation substrate, with an open closure
  gate question (C3). ADRs 0067-0071 (acquisition field access, acquisition
  report identity, basis consequences) landed after that row was written
  and may already supply part of it.
- **What we do not know.** What a noncovered sale does on core v78 through
  the real coordinator; whether the existing families can carry a
  filer-supplied basis or a new family is needed; what the 2025 Form 8949
  and Schedule D instructions require for boxes B and E (and C and F, no
  Form 1099-B); whether one return may mix covered and noncovered sales;
  what question the filer answers for the basis.

## Actions the team will take

1. **P0: law, state and design.** From the local 2025 Form 8949 and
   Schedule D instruction sources, what boxes B and E require. On core v78
   through `live_coordinate_run`, what each case does today. What the
   acquisition ADRs and the ADR-0066 substrate already provide, and what
   the frontier's C3 question is now. The smallest successor set, with a
   scratch prototype. Stop and report if an engine, schema or recording
   change is needed.
2. **Decide.** The class, the questions, and any contract (owner, if a
   schema, ADR or recording change is needed).
3. **Track 0 adversarial closure.** The six artifacts of
   `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate", over the
   decided design, each with built evidence. No row may pass beside a
   standing counterexample (C3). A `FAIL` returns to design or the owner.
   (Ran 2026-11-06: four FAIL. Owner sent it to P0b.)
3b. **P0b: engine and recording change.** One answer closes several
   families; the covered-family flag stops publishing line 8a; scalar
   identity exclusivity kept or dropped. Designed and proved on scratch,
   with the schema, ADR and loader contract named. Then the owner accepts
   the contract, Track 0 reruns over the changed design, and Track 1
   builds the engine change and core v79 together.
4. **Track 1: build.** Successors, core v79 and its registry and release,
   cases through the real coordinator and the page, v78 and earlier
   pinned, full suite.
5. **Close.** Fresh-reader review, exact-head CI, retrospective, roadmap,
   frontier row and parked list.

## Cases that will shape the design

- One noncovered long-term sale at a gain, basis supplied: Form 8949 box
  E, Schedule D line 9, line 15, line 16, Form 1040 line 7, and the
  preferential tax.
- One noncovered short-term sale at a loss: box B, Schedule D line 2, and
  the $3,000 limit on line 21.
- A return with both covered and noncovered sales, one each term.
- A noncovered sale with a wash-sale adjustment.
- A noncovered sale whose basis the filer has not supplied: blocks and
  asks.
- Every return core v78 computes: identical on the successor.

## Process

Dispatch is to grok CLI agents in this worktree (owner direction). P0 and
Track 1 are builder units; the close is a fresh-reader review. Each unit
commits on this branch as it goes. Stop means stop.

## P0 result

Recorded in
`docs/phases/engine-breadth/milestones/noncovered-sales-evidence/p0-law-state-design.md`.
Core v78 has no line 2 or line 9. A sale whose basis was not reported,
placed on a covered family, publishes on line 1a or 8a and is not
refused. Answering both Form 8949 boundaries no blocks Form 1040 line
7a and leaves Schedule D published. A missing basis is a schema
rejection or the covered-family question. The smallest successor is
content only: new families, lines 2 and 9, the line 7 and 15 sums, a
third preferential arm, Form 8949 boxes B and E, one boundary fact, and
a line 7a successor the scratch v79 package did not yet include. No
engine, schema, expression, or recording-surface change. C3 remains an
open owner question. The scratch loss and wash runs match Schedule D
and not line 7a until that successor is re-measured.

## Decisions

Owner, 2026-11-06, on P0:

1. **C3: no counterexample may stand beside a `PASS`.** A Track 0 closure
   row passes only when each counterexample its evidence records is fixed
   or refused by an answer, and the row says which. Written into
   `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate". This
   milestone runs that gate before Track 1.
2. **Fix the v78 misroute and partial Schedule D on v79.** A sale recorded
   on a covered family with `basis_reported_to_irs` no is refused (or
   routed to box B or E), and a "no" to the Form 8949 boundary blocks
   Schedule D instead of publishing lines 8a, 15 and 16 while line 7a
   blocks.
3. **One question closes the new families.** "Did you sell any securities
   whose basis was not reported to the IRS?" A "no" closes all eight new
   families empty. If one answer cannot do that without an engine or
   schema change, Track 1 stops and reports.
4. **Code W is in the class** on boxes B and E, with the column (g)
   mechanics of boxes A and D. Other adjustment codes, boxes C and F,
   digital assets and short sales stay out, refused by answer.

Foreman:

5. Track 1 includes P0's line 7a successor so a pure noncovered loss is
   Schedule D activity, and re-measures the loss and wash cases (expected
   line 7a -3000 and tax 3515; -2000 and 3635).
6. Families use `source-family.v2` constraints and identity exclusivity
   against the covered families, with `accounts_for` extended to match.

Owner, 2026-11-06, on P0b:

7. **Accept the P0b contract.** `source-closure-mapping.v4` lets one
   yes/no answer cover the eight noncovered families; the next
   artifact-package version admits it; one new ADR records it. No kernel
   change. The ADR text comes to the owner for acceptance before the PR
   goes ready.
8. **A "yes" goes stale like today's closures.** A later sale strips the
   answer for that sale's families and the question returns, the same
   lifecycle per-family closures have.
9. **The covered-flag refusal has its own reason.** A covered sale with
   `basis_reported_to_irs` no blocks with a dedicated code and an
   explanation telling the filer to record it as a noncovered sale, not
   `SOURCE_SET_UNCLOSED`. Measured on all five covered sale objects.

## Track 0 adversarial closure

Evidence: `docs/phases/engine-breadth/milestones/noncovered-sales-evidence/track0-closure.md`. Scratch core v79, `live_coordinate_run`, digest `track0-output.json`. Source ref `bb766465641abe3fb367a527701a5ca7393fb488`.

- Authority-lifecycle table: FAIL — one shared closure fact does not admit the eight families (`one_finding`, `eight_findings`); a shared horizon id is `HorizonModelError` (`duplicate_horizon`). Admission requires exactly one current true finding per family horizon, and marshalling appends a shared fact type once per mapping.
- Empty/nonempty authority matrix: FAIL — closed-empty with eight true closures matches the wage return, and a boundary `no` blocks a recorded noncovered sale (`boundary_no_gain`). A covered sale with `basis_reported_to_irs` no still publishes line 8a at 4000 (`covered_flag_no_path_a`, `covered_flag_corrected_to_no`). Scalar identity exclusivity is an engine change and is not installed.
- Late-member lifecycle: FAIL — add-without-reclose blocks line 9 and Form 8949; reclose publishes line 9 = 4000. The one-question `no` never becomes that close. Correcting the covered flag from yes to no leaves line 8a at 4000.
- Neighboring capability dependency diff: FAIL — wage, foreign tax 601, exempt interest 50, and student loan 200 match v78 only after eight new closure findings. Without them the wage return blocks Form 1040 (`wage_unclosed`). No other v78 live return was measured. No content-only change makes one answer close eight families.
- Reused-claim semantic/lifecycle equivalence: PASS — `no-form8949-sources` and `no-other-form8949-adjustments` keep their proposition, tax-year identity, and free supersession. The preferential gate is v7 with a third arm and is not reused. Covered closure fact types are not reused.
- Integration surface: PASS — one publisher each for lines 2, 7, 9, 15, 16, 21, line 7a, the preferential base, and Form 8949. Disposition paths built: published gain, published loss, `computed_zero`, `closure_backed_zero`, and blocked. `validate_presentation_model` passed on every saturated case.
- Known limitations affecting correctness: owner disposition required

Track 1 does not start. A PASS here would need one answer to close the eight new families, and the covered-family flag `no` to stop publishing line 8a, without an engine, schema, or recording change. Neither holds on the scratch package.

Owner, 2026-11-06, on this FAIL: change the engine and recording surface
first (P0b), then rerun Track 0 and build v79.

### Track 0 rerun

Evidence: `docs/phases/engine-breadth/milestones/noncovered-sales-evidence/track0-closure.md`, section "Rerun over the P0b contract". Scratch core v79 / release v77, 41 members, `live_coordinate_run`, digest `track0b-output.json`. Source ref `0a7fc60f5ab42ed8d568362f1a5c9a750d7394c0`.

- Authority-lifecycle table: PASS — one shared answer (`tax.us.2025.f1099b.noncovered-sold.source-closure`) admits the eight families. `one_finding` publishes the wage return at 34250 / 3875 with lines 2 and 9 at `closure_backed_zero`. `wage_unclosed` blocks lines 2, 9, 15, and 16 and shows the question. A later member-transition strips only that family (`late_yes_stale`); a later answer admits it (`late_yes_reanswered`, line 9 = 4000). `duplicate_horizon` is still `HorizonModelError` on `demo.ns.p0b.shared.h0`.
- Empty/nonempty authority matrix: PASS — one `no` and no member computes every harness return at its v78 line 15 and line 16. A long-term member after `no`, or after `yes`, or a later `no` beside that member, blocks line 9 and leaves line 2 at 0. `st_loss` reaches line 7a at −3000 and tax 3515. `wash` reaches line 7a at −2000 and tax 3635. Covered `basis_reported_to_irs` no blocks line 8a or line 1a, or the wash line, with `missing: [BASIS_NOT_REPORTED_ON_COVERED]`.
- Late-member lifecycle: PASS — attest and close are the shared answer. `late_member_unclosed` blocks line 9. `late_member_reopened` publishes line 9 = 4000. `covered_flag_corrected_to_no` blocks line 8a. `covered_flag_corrected_to_yes` publishes line 8a = 4000.
- Neighboring capability dependency diff: PASS — wage, foreign tax, exempt interest, exempt dividend, student loan, gambling loss, mortgage, itemized, and part II-B match v78 line 15 and line 16 under one `no`. `wage_unclosed` blocks Form 1040. v78 `covered_flag_no_path_a` still publishes line 8a at 4000.
- Reused-claim semantic/lifecycle equivalence: PASS — `no-form8949-sources` and `no-other-form8949-adjustments` keep their proposition, tax-year identity, and free supersession. The preferential gate and the covered closure facts are not reused. Scalar exclusivity stays off the number families. The ADR-0082 companion pairs were not installed in this scratch.
- Integration surface: PASS — published gain, published loss, `computed_zero`, `closure_backed_zero`, and the blocked paths above were built. `validate_presentation_model` passed on every saturated case. `covered_both_boundaries_no` leaves the Schedule D attachment `blocked` (missing `schedule-d.line-8a-gain`). The four covered objects on this package show the sentence "Record this sale as a noncovered sale. The broker did not report its basis to the IRS." The row `code` is `DEPENDENCY_INVALID`; the dedicated token is the `missing` entry. `covered-ltcg` is not a member of core v78 or this successor, so it has no publisher here.
- Known limitations affecting correctness: none

Each counterexample in the rerun section is fixed, or refused by an answer. `covered-ltcg` is refused because the family is not on the package. `duplicate_horizon` is refused because a shared horizon id stays illegal. Scalar exclusivity is refused because Decision 7 dropped it. Track 1 is a separate unit.

## P0b result

Recorded in
[p0b-engine-design.md](noncovered-sales-evidence/p0b-engine-design.md).
Scratch runs: `noncovered-sales-evidence/p0b-output.json`.

One yes/no fact admits the eight new families (`source-closure-mapping.v4`).
`no` closes each empty family. A recorded sale under that `no` reopens only
the families the sale belongs to; correcting the answer to `yes` publishes
line 9 at 4000. The nine v78 live returns the current-core harness builds
keep their Form 1040 line 15 and line 16 dollars with that one `no`. A
covered object member with `basis_reported_to_irs` no loses covered-family
admission, so line 8a stops publishing, and no family handover is required.
Scalar identity exclusivity stays on the sale object; scalar families use
companion pairs instead. No kernel change. Track 0 reruns after the owner
accepts the contract.

## Track 1 result

Core `tax.us.2025.package.core-calculations` v79 (`artifact-package.v41`), registry `published-packages.v77.json`, release `demo.release.sli-worksheet-integration.2025.v77.json`. Package checksum `95728e35919867fecafd3801d400d8d025b2924cea1172134b418a89392f4c93`. Registry sha256 `bdd19f75dfcb46b12dcc565c9c2c1960310fbe61ce66653619ad975156cd0cb1`. Release sha256 `b89f5cfb2c4093d0c56a031989de7f4e1202d413508fbb6927082f7d07b95c26`. 876 members, 372 entrypoints. The package admits `source-closure-mapping.v4`.

Schemas added, manifests add-only: `source-closure-mapping.v4` (`4381cb8d33f3331bfc1fd11b118a233268a0448a74bf1df7bb6a33d7f85a23f6`) and `artifact-package.v41` (`99adceccf2cc94a69e87cf138d56bbeda9bf9dfb225845b8433aab9a9e94d57a`). Core v78 stays `artifact-package.v40`, checksum `ab13e399445e8c5d5ad3fd71c8ea9bd1a96b05581aef640fa950105daf2d2eb1`, and does not admit v4.

ADR 0084 is proposed. It supplements ADR-0014. The owner accepts it before this PR is ready.

The Track 0 rerun cases run through the coordinator on core v79 (`tests/test_noncovered_sales_v79.py`). One `no` publishes the nine current-core returns at the same Form 1040 line 15 and line 16 as v78. Those nine, plus `covered_flag_no_path_a`, pinned to v78 keep the v78 dollars; pinned v78 still publishes line 8a at 4000 for that covered flag. `duplicate_horizon` is `HorizonModelError` on `demo.ns.p0b.shared.h0`. A covered sale with `basis_reported_to_irs` no blocks with `missing: [BASIS_NOT_REPORTED_ON_COVERED]` and the sentence "Record this sale as a noncovered sale. The broker did not report its basis to the IRS." A member recorded after `yes` strips only that family (`late_yes_stale` stays blocked; `late_yes_reanswered` publishes line 9 at 4000). The blocked noncovered wash page shows the short family sentences, including "A wash-sale disallowance is recorded on a sale that is not a loss."

`pytest -m "not live"`: 1675 passed, 8 skipped, 4013 subtests (16.87s). Full `pytest`: 4389 passed, 24 skipped, 8277 subtests (1367.44s). `python3 -m mypy`: no issues in 464 source files.

The v4 reason walk names each listed family without rebinding the disposition row. Staleness reads `payload.member.action` on a recorded member-transition. A removal does not strip. The required-but-unread allowlist follows line 1a v4 and line 8a v5, the same closure-check witnesses the replaced versions declared.

ADR 0084 is not accepted. The scalar-without-its-sale case calls the kernel companion enforcer directly. Cores before v78 were not live-rerun; `tests/test_noncovered_sales_v78_switch.py` checks that those packages do not name the refusal map. CI `verify` remains the merge gate.
