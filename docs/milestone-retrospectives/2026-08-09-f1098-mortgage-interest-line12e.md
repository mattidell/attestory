# Retrospective — Form 1098 Home-Mortgage Interest through Schedule A and Form 1040 Line 12e

## What differed from the plan

- Track 0's paper-first analysis held up completely: the singleton closed
  Form 1098 family, the seven taxpayer-authority facts, the mechanical
  debt-limit proof (no Publication 936 average-balance worksheet needed),
  and the bounded-additive-successor decision on the 2025 deduction spine
  (line-12e/13a/13b/14) were all implemented exactly as chartered, with no
  scope renegotiation.
- The singleton-cardinality bound (a second Form 1098 statement must block)
  needed a genuinely new evaluator primitive: the closed-family/closure
  machinery proves "every statement is recorded," not "no more than one
  exists," and no non-throwing way to check family closure exists in the
  evaluator. Resolved with a small, additive `count` op (`rule-artifact.v4`)
  rather than inventing a heavier mechanism.
- Track 1 survived five repair rounds after its first build, all found by
  actually driving the rule through `live_coordinate_run` rather than by
  schema validation or mocked tests: a missing `rule-artifact.v4` runtime
  registration (the schema addition was never wired into `live.py`/
  `runner.py`/`package_validation.py`/`marshal.py`), a scope-block
  convention mismatch, an ADR-0016 collect-authority naming mismatch
  between the family's `authorizes_subtotal` and what the rule actually
  published, a `requires`-vs-`collect` gate mismatch, and (found only
  during Track 2's package build, since Track 1's own tests injected
  content via a resolver monkeypatch and never validated a real package) an
  invalid `citations` shape on the seven Schedule A boundary rules and a
  categorical `value_schema` shape that would have failed the
  attachment-completeness-answer guard.
- Track 2 needed a genuine architectural resolution for
  `tax.us.2025.schedule-a.total`: the runner's saturation scheduler only
  retries a rule across passes when its dependency is in its own declared
  `requires`, never merely referenced via `ref`; a rule with an empty
  `requires` gets exactly one eager attempt and permanently blocks if
  evaluated before its producer runs in the same pass. Resolved with two
  rules carrying mutually exclusive guards (`count == 0` /
  `count != 0`) publishing the same symbol, using the package's
  `conflict_semantics` allowlist — the corpus's first use of that
  mechanism, which exists in the schema specifically for this case.
- Three repair rounds in Track 2 each found genuinely new correctness
  defects, two of them security-shaped: round 1's fix for "a non-F1098
  return loses its line-12e producer" used an `optional_default`,
  default-`true` scope flag, which the foreman reproduced as a silent
  bypass — a return with a real, fully-authorized Form 1098 statement that
  simply omitted the new flag silently published an unrelated,
  unverified `deductions.itemized` figure instead of the derived value.
  Round 2's fix (a mandatory, blocking declaration, matching this corpus's
  established Path-A/B convention) closed that, but a follow-up
  independent review found the *contradictory* case — a return that
  explicitly declares "no Form 1098 statement" while a real, non-empty
  statement is actually on record — still bypassed the guard, because the
  round-2 fix checked the declaration alone without checking it against
  the observed family state. Round 3 closed this with an explicit
  `F1098_SCOPE_CONTRADICTION` block. The same review round also found that
  all seven Schedule A boundary "closed-absent" rules were unconditional
  (`when: true`, `requires: []`) with no taxpayer declaration behind them
  and no downstream consumer — a citation trail wrapped around a hardcoded
  `true`, present since Track 1's original build and missed by five prior
  repair rounds and two prior reviews — closed by adding nine new
  mandatory taxpayer-declaration facts wired into the Schedule A
  attachment's `completeness.required_answers` (the existing, proven
  ADR-0036 mechanism).
- No new ADR was required. Track 0 concluded the existing identity/closure
  (ADR-0015/0016/0017), attachment ontology (ADR-0036), and
  explanation/package/citation/presentation (ADR-0020/0027/0029/0033/0046)
  contracts were sufficient by content-level reuse, and that held for the
  whole milestone.
- The branch rebased twice: once onto the SSA-1099 milestone's own
  pre-merge WIP tip (to unblock schema-version reconciliation before that
  milestone had a PR-mergeable head), and again onto `origin/main` after
  SSA-1099 actually merged (PR #163). The second rebase's own squash
  reconstruction technique had a real bug: overlaying old commit snapshots
  onto the new base silently reverted four SSA-1099-owned files to their
  pre-curation content and dropped a legitimate `validate_projected_source_boundary`
  safety-check call SSA-1099's final curation had added to
  `packages/derivation/live.py` — caught only by a full content-hash sweep
  across every common file between the old and new bases, not by a
  file-name-only comparison (which had been tried first and wrongly
  concluded the trees were identical).

## Result

The engine computes a bounded, production-shaped synthetic path for 2025
individual returns reporting exactly one deductible Form 1098
home-mortgage-interest statement: deductible interest through Schedule A
line 8a, a composition-complete Schedule A for this bounded class,
deterministic standard-versus-itemized selection at Form 1040 line 12e
(guarding the generic `tax.us.2025.deductions.itemized` raw assertion off
whenever a Form 1098 statement is genuinely on record, including the
contradictory-declaration case), the correct 2025 line-13a/13b/14
deduction-spine succession into taxable income, Schedule A attachment
disposition, package resolution, citations, and production-shaped
presentation.

The result does not implement multiple mortgages, second homes,
refinancing, home-equity or mixed-use debt, points, mortgage-insurance
premiums, refunded interest, the mortgage-interest credit, pre-2017-12-16
grandfathered debt, shared-borrower allocation, seller-financed interest,
interest not reported on a Form 1098, any Schedule A category besides the
Form 1098 interest itself, QBI, Schedule 1-A deductions, or voluntary
itemization when it does not exceed the standard deduction.

## Evidence and review disposition

- Paper boundary and contracts: `docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md`
  (Track 0 record, Track 1/Track 2 charters).
- Track 1 review (2026-08-06) found the `rule-artifact.v4` runtime-wiring
  gap, a scope-block mismatch, a collect-authority naming mismatch, and a
  `requires`-vs-`collect` gate mismatch, plus two further defects (invalid
  boundary-rule citations, a categorical value-schema shape) surfaced only
  once Track 2's package build actually ran real `package_validation`
  against Track 1's content for the first time. All closed and
  independently re-verified.
- Track 2 review round 1 (2026-08-09) found a real correctness regression
  (a non-F1098 return losing its `line-12e` producer entirely) plus five
  smaller findings (a CI-blocking mypy gate, an overly broad data-safety
  test exemption, an inaccurate additive-only claim, missing required
  evidence, a citation `form_id` inconsistency). The regression's first fix
  was itself rejected on foreman verification — an `optional_default`
  scope flag reopened a worse, silent bypass than the original defect —
  and replaced with a mandatory, blocking declaration in round 2.
- Two independent reviews against the post-rebase branch (2026-08-09) both
  found and reproduced live the same critical bug (the contradictory-
  declaration bypass) plus two further defects (the fabricated Schedule A
  boundary authorities, and an `artifact-package.v22` exact-entrypoint
  validation gap). All three closed in round 3, each independently
  re-verified by the foreman against the source before acceptance.
- The foreman independently reproduced every P1/critical finding live
  before accepting each repair as closed, rather than accepting builder
  self-reports — this caught one case where a repair's own report
  mischaracterized a self-inflicted regression (a BSD-`sed` bracket-
  expression bug that silently corrupted a test file during a
  documentation-hygiene pass) as "pre-existing."
- Working review records, repair-round charters, and owner-launch prompts
  were working instruments of a long in-flight correction; their material
  findings are distilled above and their files are removed at this
  closeout per `PROJECT_PLANNING.md`, "Milestone Publication Curation."
- Full suite green (1218 passed, 20 skipped, 0 failures) on the curated
  head prior to this closeout pass. mypy clean on every file this
  milestone owns. `governance_lint.py` conformant, `envelope_scan.py`
  clean, `git diff --check` clean. The curated PR head still requires a
  fresh independent review of the exact final range and the repository CI
  gate before the owner can merge.

## What it cost

- One paper-first Track 0, two Track 1 builder rounds (initial build plus
  five repair rounds folded into one), two Track 2 builder rounds (initial
  build plus three repair rounds), one rebase onto an in-flight WIP
  dependency, one rebase onto the same dependency's actual merge, and five
  independent-review passes across the milestone's lifetime (two on Track
  1, three on Track 2, two of the Track 2 reviews run in parallel against
  the same head).
- No rival prototype, no new ADR.

## Follow-ups

- The Schedule A boundary category authority pattern (nine mandatory
  taxpayer-declaration facts feeding an attachment's
  `completeness.required_answers`) generalizes to any future milestone
  that needs to prove multiple deduction/income categories are genuinely
  absent, not merely unimplemented — worth citing as precedent rather than
  re-deriving from ADR-0036 each time.
- The `count`/cardinality-guard and `conflict_semantics` multi-producer
  patterns are both now real, load-bearing, first-use precedent in this
  corpus for future milestones needing a singleton-cardinality bound or a
  disjoint-guard multi-producer symbol.
- Multiple mortgages, refinancing, points, PMI, the mortgage-interest
  credit, and general Schedule A support remain independently selectable
  frontier candidates.
- Leave the next frontier row unselected until the owner chooses.

## Closeout lesson

A rule with an empty `requires` list is not "unconditional" in this
engine's runner — it is eagerly attempted on the very first saturation
pass, and if a `ref`/`collect` inside its `when`/`value` targets a symbol
another rule hasn't published yet in that same pass, it blocks
permanently with no retry. The only correct way to express "this rule's
true dependency is conditional" is to split into rules with genuinely
disjoint guards, not to omit the dependency from `requires` and rely on
value-level branching. This surfaced twice in this milestone under
slightly different shapes and cost real debugging depth both times.

"Optional, safely-defaulting" is the wrong shape for any fact whose
absence should be a completeness gap, not a default — this corpus's own
convention (every genuine Path-A/B declaration blocks on absence) said so
before this milestone re-derived it the hard way, twice: once for the
line-12e scope flag (round 1's rejected fix), and implicitly for the
Schedule A boundary rules' complete lack of any declaration at all
(present since the very first Track 1 build). A completeness-shaped
question always gets a completeness-shaped answer: block honestly, never
default silently, regardless of which symbol sits on the critical path.

Static schema validation and mocked tests are not sufficient evidence for
a rule that will run inside the real production package. Every latent
defect this milestone found after its first Track 1 build (six of them)
was invisible to schema validation and only surfaced once something
actually drove the content through `live_coordinate_run` against a real,
assembled package — several only surfaced when Track 2's package build ran
`package_validation` against Track 1's content for the first time, months
after Track 1 was "done." A rule is not verified until it has been run.

An independent verifier should re-run the reported reproduction, not just
the reported test suite. A builder's self-report that a suite is green can
still be built on top of a self-inflicted regression the builder
introduced and didn't notice — caught here only because the foreman
independently re-derived and re-ran the exact failing scenario rather than
trusting the summary.
