# Foreman Handoff Note

A lightweight, living continuity note — **not a protocol and not a gate.** The
foreman keeps this current *enough* during multi-step work that, if a session
ends mid-task, a fresh foreman can resume without re-deriving everything. Update
it opportunistically; there is no required cadence and no ceremony. It describes
*now*, not history — overwrite stale content freely (durable history lives in
commits, retrospectives, and process logs).

## How the owner relaunches a foreman

Start a fresh session and say, roughly: *"Resume as foreman. Read
`docs/phase-state.md`, `docs/foreman-handoff.md`, and the active plan they point
to, then continue."* The new foreman reads those, reconciles the in-flight state
below against `git status` / `git log`, and proceeds. If the note looks stale
against git, trust git and say so.

**Discipline:** a step is not done until `phase-state.md`'s "Next" is advanced too — it is the re-entry pointer the next reader (foreman *or* clerk) anchors on, so updating only this handoff leaves them stale.

## Current state (updated 2026-07-19; Track 2 MERGED, Track 3 blocked on unratified D2 — owner decision needed)

- **Seat:** principal foreman. Active milestone: **Dividends and Schedule B
  Slice**. Track 0 is CLOSED: ADRs 0035/0036/0037 ratified; Track 0a
  (generic `conditional_dependency_set` production substrate) merged as
  **PR #30 (`6f303fe`)** after its full review chain — independent review
  not-ready (F1–F4) → foreman repair `595c4e1` → independent delta
  re-review **ready** (`61452e5`; non-blocking R1 act-determinism note, R2
  private `_content_id` import). D2 adoption is unblocked.
- **Track 1 (schema citizens) build is COMPLETE** on
  `track/dsbs-t1-schema-citizens` (`c6d62f6`), charter
  `docs/reviews/charter-2026-07-19-dsbs-t1-schema-citizens.md`. Landed:
  `1d2a58b` vocabulary reconciliation (SOURCE_SET emit-vs-record,
  ADR-0036 PC3; `ITEMIZATION_TIE_OUT_VIOLATION` named, PC1 vocabulary half),
  `2a08d80` 1099-DIV statement/family/closure citizens, `60bbbc0`
  `dividend-universe.v1`, `272b7a9` generic attachment citizen surface,
  `a6f11f3` the two admission-time validation guards (ADR-0035 runtime
  universe guard; ADR-0036 presence-encoding guard). Full battery green at
  handoff: 477 tests, mypy clean (94 files), governance lint conformant,
  envelope scan clean (rebuilt `.venv` on python3.13 first — the prior venv
  was a broken symlink to system python3.9, which cannot parse this repo's
  `str | None` syntax; rebuild pattern: `rm -f .venv/bin/python3
  .venv/bin/python && /opt/homebrew/bin/python3.13 -m venv --clear .venv &&
  .venv/bin/python3 -m pip install -r requirements.txt`).
- **Track 1 independent pre-merge review returned READY** (`5bfbf52`,
  `docs/reviews/2026-07-19-dsbs-t1-schema-citizens-review.md`, dispatched as
  a background sub-agent under
  `docs/reviews/charter-2026-07-19-dsbs-t1-schema-citizens-review.md`). All
  eight charter checks hold; six findings (F1–F6), all non-blocking/
  observational with file/line evidence (notably F3: the runtime universe
  guard's v1/v2 exemption covers only the `COLLECT_TARGET_NOT_FAMILY` half,
  by design and tested — `RECORDED_NON_COMPOSABLE_INPUT` is unconditional).
  Foreman triage: no repair needed. Full battery re-run fresh by the
  reviewer in its own worktree: 477 tests OK, mypy clean, governance lint
  conformant, envelope scan clean.
- **Track 1 MERGED** — PR #31, `a870a2f` on `main`.
- **Track 2 scope confirmed by owner** (proceed with the full-machinery
  reading); charter:
  `docs/reviews/charter-2026-07-19-dsbs-t2-composition-conditional-machinery.md`
  on `track/dsbs-t2-composition-conditional-machinery` (`1739737`).
- **Build IN FLIGHT.** First builder dispatch was interrupted mid-task by an
  API session-limit error (not a real failure) after landing one clean
  commit and leaving a second deliverable's work uncommitted. Foreman
  (this session) reconciled directly: found the uncommitted work
  substantially complete and correct, fixed one genuinely wrong test
  expectation and one mypy `self.run = run` `TestCase.run`-shadowing bug,
  reverified the full battery, and committed a clean checkpoint. **Landed
  on the branch:**
  - `6312cc4` — **deliverables 1 AND 2** (charter listed them separately;
    the builder correctly recognized one generic kernel hook covers both):
    the ADR-0035 1b≤1a admission-time subset invariant
    (`packages/kernel/findings.py`, a new `registry.subset_invariant_pairs`
    hook in the same fold every admission path already uses — `project()`,
    `apply_contribution_batch`, the live coordinator — so it is
    domain-agnostic kernel machinery, not tax-specific code) with full
    rejection-semantics tests and the same-batch ordering kill-tests
    (`tests/tax/test_dsbs_t2_dividend_admission.py`, 9 tests covering both
    orderings within one batch). 486 tests green at that commit.
  - `2ed1c9c` — **deliverables 3 and 4**: box-1a/1b subtotal rules, lines
    3a/3b with per-box closure independence, line-9 v2 folding in 3b,
    shipped as `tax.us.2025.package.core-calculations` v4 (distinct
    synthetic scope, year 2053, so v3 stays independently exercisable).
    Goldens in `tests/test_dsbs_t2_coordinator.py` enter through
    `live_coordinate_run` per the charter's mandatory shape. One test fix
    worth knowing for the next builder: **when a composing line's
    `requires` names a subtotal symbol that itself blocked on an unclosed
    family, the composing line reports `DEPENDENCY_ABSENT` (its own `when`
    never runs — `requires` gates evaluation first, `runner.py:310`), and
    the subtotal rule itself reports `SOURCE_SET_UNCLOSED`** — verified
    against the already-committed `unclosed_interest_composition` golden
    for line 2b, the exact same two-tier pattern. Don't assume the
    composing line carries the closure code directly; check the committed
    goldens before asserting a block code. 493 tests green at this commit,
    mypy clean, governance lint conformant, envelope scan clean.
- **Deliverables 5–8 (the complete Schedule B attachment) LANDED** —
  `2a10f60`, all in one commit because one execution mechanism serves
  every deliverable: `attachment-rule.v1` citizens carry no `when`/`value`
  expression tree (ADR-0036), so they can't run through the ordinary
  saturation `attempt()` path at all. `packages/derivation/runner.py`
  gains `_Run.attempt_attachment`, a dedicated interpreter for the
  citizen's declarative `requirement`/`itemizations`/`completeness`
  structure, dispatched from the same saturation loop every rule-artifact
  schema already uses (`is_eligible`/`_execute`/`finalize_unreached` all
  branch on `rule.get("schema") == "attachment-rule.v1"`).
  - **5 (existence conditional):** any-of-subtotals strictly-greater-than
    the cited $1,500 threshold, per-trigger outcome computed (walkable via
    pins — the disposition record schema is closed, `additionalProperties:
    false`, so "per-trigger outcome" is reconstructible by walking the
    pinned subtotal findings against the pinned threshold parameter, not
    embedded as a free field). Not-required reuses the ordinary
    `inapplicable`/`guard_result: false` disposition every rule already
    emits — no new disposition shape needed. New committed test
    (`AttachmentCannotPropagateToALine`) asserts no sibling line rule
    (2b/3a/3b/9) names the attachment symbol anywhere in content.
  - **6 (`collect_members`):** interpreted directly in
    `attempt_attachment`, not as a new `evaluate()` op — it reads
    `self.sources`/`self.source_fids` (the same collectible-fact tables
    `collect` already populates) keyed by `member_fact_type.id`, and pins
    every row's member finding. Row shape (`finding_id` + `value`) lives
    only in the runner's internal value construction, never in the closed
    generic `attachment-rule.v1` schema. **Scope-bounded simplification,
    stated honestly, not hidden:** Schedule B Part I ties to the box-1
    (1099-INT) family only — the *only* interest family this milestone's
    fixtures (both T2's and T1's) ever populate; a full build would need
    one itemization block per interest source family (b1/b3/oid/non-form)
    tying to the same composed line. Part II ties 1:1 to box-1a
    (1099-DIV), no simplification needed there.
  - **7 (tie-out):** row-sum vs. the named line's *current* value, checked
    only once completeness holds; mismatch hard-fails the attachment only
    (`ITEMIZATION_TIE_OUT_VIOLATION`, the exact Track-1 vocabulary, no new
    code) and never touches the line (the line is a separate rule the
    attachment only reads). Both named kill-tests
    (`TieOutInvariant.test_stale_row_set_...`,
    `test_stale_line_...`) are `RunContext`-level, per the charter's
    explicit allowance — a correctly-computed live run can never disagree
    with itself, so the defect isn't expressible through an honest act
    log.
  - **8 (Part III completeness):** two new taxpayer-assertion fact types
    (`tax.us.2025.scheduleb.foreign-account`, `...foreign-trust`) plus the
    branch-only `...7b-country`, all in a new `scheduleb.bundle.json`
    (bundle.v2 — a bare top-level `fact-type.v2` member is legal for
    *package*-level validation but the live *kernel* fact registry only
    admits fact types reached via bundle-adoption, so a bare member alone
    would silently reject every live assertion referencing it — caught by
    a `FindingModelError: finding references unknown fact` failure while
    building this). Presence is checked independently per required answer
    before any value is read (three separate goldens: account-absent-
    alone, trust-absent-alone, both-absent, each naming exactly its own
    missing symbol(s) — never masking). `foreign-account: yes` adds the
    7b-country requirement and names `FINCEN_114_NAMED` as a walkable
    obligation fact (label text only, no form/field/filing key anywhere in
    the published value — verified by string-absence assertion). ADR-0036
    ratifies no obligation for `foreign-trust: yes`, so no
    `branch_requirements` entry names one — documented in the rule
    citizen's own `title`, not invented.
  - **Wiring repairs the live path needed** (none of these reopen a
    ratified decision, all additive): `packages/derivation/live.py`'s rule
    filter excluded `attachment-rule.v1` from `ctx.rules` entirely (fixed:
    added to the schema set at line ~53); `packages/derivation/marshal.py`'s
    legacy single-value input fallback only recognized ordinary
    rule-artifact `requires` lists to decide whether an unbound current
    finding should surface as a symbol, so a live Part III answer
    assertion could never reach a run at all — fixed with a new
    `_rule_required_symbols` helper that also understands an attachment
    citizen's own `requirement.subtotals` +
    `completeness.required_answers`/`branch_requirements` symbol surface.
  - **Package validation's reachability walker** (`package_validation.py`
    §8, the `MEMBER_UNREACHABLE` check) has no adjacency case for
    `attachment-rule.v1`'s structure, so every new v5 citizen (the
    attachment rule, its citation, its threshold parameter, the new
    bundle) is listed directly in the package's `entrypoints` — the same
    sanctioned pattern v4 already used for `dividend-universe.v1`. This is
    a legitimate, precedented mechanism, not a workaround; extending the
    walker itself to understand attachment structure natively would be a
    reasonable cheap follow-up but is not a charter deliverable.
  - Shipped as `tax.us.2025.package.core-calculations` v5
    (`tools/generate_dsbs_t2_schedule_b_content.py`) at scope year 2054 —
    distinct from v4's 2053, v3's 2052, etc., so every prior version stays
    independently exercisable. Adoption fixture:
    `packages/sample_data/frrs_t3/adoptions/adopt-core-v5-current.json`.
  - **16 new tests** in `tests/test_dsbs_t2_schedule_b.py`. All six of the
    charter's named golden classes now exist and are green: 3a/3b
    publication and line-9 (already landed at 2ed1c9c, unchanged), Schedule
    B not-required (`NotRequired`, 3 tests), required-and-complete whole
    form (`RequiredAndComplete`, 2 tests — Part I/II itemizations tying to
    2b/3b, Part III both answers present, one `no`/`no` case and one `yes`
    branch case), required-and-incomplete (`RequiredAndIncomplete`, 4
    tests — each answer absent alone, both absent together, and the
    branch-triggered 7b-country absence), and the same-batch ordering +
    tie-out kill-tests (already landed at 6312cc4 for ordering; tie-out
    kill-tests new here). Every golden test that is one of the six named
    classes enters through `live_coordinate_run` from an authoritative act
    log — confirmed by grep, not assumption: `RunContext(` appears only in
    the two explicitly-marked supplementary classes (`TieOutInvariant`,
    `WholeFormValueContent`), both docstring-labeled non-substitutive.
  - Full battery green at this commit: **509 tests, mypy clean (99
    files), governance lint conformant, envelope scan clean**
    (`--range main..HEAD`).
- **Independent pre-merge review returned NOT READY** (`0541875`,
  `docs/reviews/2026-07-19-dsbs-t2-composition-conditional-machinery-review.md`,
  dispatched as a background sub-agent under
  `docs/reviews/charter-2026-07-19-dsbs-t2-composition-conditional-machinery-review.md`).
  Eight of nine checks passed on direct re-derivation. **F1 (blocking,
  confirmed independently by the foreman before repair):** Schedule B's
  Part I itemization `collect_members`s the box-1/1099-INT family only
  (as documented), but its `tie_out.line_symbol` named
  `tax.us.2025.interest.taxable-total` — line 2b's *four*-family sum — not
  `tax.us.2025.interest.b1-subtotal`, the box-1-only figure the itemization
  rows actually cover. Any filer with concurrent box-1 and box-3/OID/
  non-form interest would have spuriously hard-failed with
  `ITEMIZATION_TIE_OUT_VIOLATION` despite correct computation — invisible
  in the suite because every Track 2 fixture held non-box-1 interest at a
  closure-backed zero. This was Track 2's own chartered tie-out mechanism
  (deliverable 7) comparing the wrong two things, not a boundary or
  documentation gap.
- **F1 repaired** (`854c71a`): retargeted the tie-out symbol to
  `tax.us.2025.interest.b1-subtotal`, regenerated the derived registry/
  release checksums, added a new `live_coordinate_run` regression golden
  (`PartIInterestTieOutWithConcurrentNonBox1Interest`, concurrent box-1 +
  box-3 interest publishes cleanly), and fixed two supplementary
  `RunContext`-level test classes that needed the newly-required
  `b1-subtotal` input alongside the pre-existing `taxable-total` input. No
  runner/evaluator code changed — the tie-out mechanism itself was already
  correct; the content told it to compare the wrong symbol. Full battery
  re-verified by the foreman: 510 tests, mypy clean, governance lint
  conformant, envelope scan clean.
- **Independent delta re-review returned READY** (`76698cc`,
  `docs/reviews/2026-07-19-dsbs-t2-delta-rereview.md`). All seven delta
  checks (R1–R7) pass: F1 discharged by the narrower of the two options
  the original review named acceptable (retarget the tie-out symbol, not
  widen the itemization); dividend-side tie-out untouched; the new
  regression golden constructs a genuinely non-degenerate divergence
  (line 2b = 450 vs. box-1 subtotal = 300) and enters through
  `live_coordinate_run`; the two supplementary `RunContext` classes were
  correctly (not just plausibly) extended; collateral scope is exactly the
  claimed 14 files (one content line, a pure checksum cascade, one test
  file — no runner/evaluator/schema touched); full battery re-run clean.
  Foreman re-ran the full battery a third time independently: 510 tests,
  mypy clean (99 files), governance lint conformant, envelope scan clean.
- **Track 2 MERGED** — PR #32, `c39c6c7` on `main`.
- **➡️ NEXT ACTION: owner decision on resuming the D2 prototype.** Track 3
  ("line 16 under D2") cannot be chartered as a production build: **D2 has
  no ratified ADR.** Checked directly, not assumed from stale notes —
  `docs/adr/` has no D2/QDCG/line-16 file; `git log -- docs/prototypes/
  qdcg-worksheet/` shows no activity since `f16cd91` ("plan: inventory D2
  multi-dependency reporting"), which predates ADR-0037's ratification and
  Track 0a's merge.
  - **Where D2 actually stalled:** `docs/prototypes/qdcg-worksheet/confirmation-r1-triage.md`
    (2026-07-18) — Confirmation R1 returned **not confirmed**. Finding
    **C1** (decision-blocking): a qualified-positive return with *both*
    capital-gain declarations absent must non-publish naming both missing
    declarations in one walk, but the committed (pre-CMDN) evaluator halts
    on the first absent reference, so the runner/NPE surface could only
    name one. The owner briefly amended the requirement away (a walk need
    only name a "currently encountered" gap, not all-at-once), then
    **reversed that amendment** the same day and routed the underlying
    all-missing-in-one-walk capability to a separate, narrowly-scoped
    topic instead of deferring it — that topic became **ADR-0037**
    (`conditional_dependency_set`), independently ratified and now merged
    as **Track 0a** (PR #30). The triage's own words: "D2's two-declaration
    walk is again a prerequisite. No topic plan, charter, implementation,
    or dispatch was authorized" *for D2 itself* — only for the CMDN
    substrate.
  - **What's true now that wasn't true at that triage:** the substrate C1
    needed no longer needs inventing — it's ratified, production-hardened
    (Track 0a's own review chain: not-ready → repair → ready), and merged.
    D2's it1/it2 designs, Repair 1, and Confirmation R1 never got a chance
    to use it; Repair 1 (`repair1/design.md`) predates ADR-0037 entirely.
  - **Charter drafted (`dec5670`), released, and landed
    (`fa89a1e`).** `docs/prototypes/qdcg-worksheet/charter-repair2.md`
    bounded the fix to a one-finding patch; the owner released the
    incumbent-repair builder seat; the builder delivered
    `repair2/design.md` (179/180 lines) and `examination-repair2.md`
    (80/80 lines), touching no other file. Substitutes
    `conditional_dependency_set` (condition Q>0, members the two
    declaration refs) for Repair 1's plain `all([ref, ref])` guard, placed
    first and unconditionally in the outer `all` so the node's own
    false-condition contract — not incidental operand ordering — grounds
    the qualified-zero reduction. The missing-declaration walk now names
    both absent declarations (or exactly the true single absent one) in
    one non-publication walk, closing Confirmation R1's measurement-3
    failure. **Foreman independently re-verified every cited HEAD line**
    (`evaluator.py` 203–221, `runner.py`'s guard try/except and
    `_record_blocked`, `explanation.py`'s ordered NPE union,
    `package_validation.py`'s v3-gated reachability walk, and the
    `conditional_dependency_set` op's presence in `rule-artifact.v3.schema.json`
    but absence from `.v2`'s) before committing — every citation checked
    out exactly, including a subtle correct point about Python `all()`'s
    generator short-circuit-on-exception behavior.
  - **One honest, verified collateral finding:** the line-16 successor
    must be authored under `rule-artifact.v3`, not `.v2`, since
    `conditional_dependency_set` is schema-admissible only under v3 —
    corrects Repair 1's stated "v1→v2" package pin to "v1→v3." Scoped
    strictly to D2-P2's own successor-identity claim; D2-P1 (fact types)
    and D2-P3 (admission-locus interlock) are unaffected and unchanged.
  - **Examination verdict: D2-P2 is now fully settled at Rung 1** —
    successor posture, qualified-zero reduction, present-`"yes"`
    disposition, and the two-declaration missing walk, all re-derived
    against one consistent guard expression and cited to committed HEAD
    source. D2-P1/D2-P3 remain settled, unchanged from Repair 1. Nothing
    here is live production content for the D2 worksheet itself — only
    the generic `conditional_dependency_set` substrate is committed and
    reviewed; the worksheet's *use* of it is still a Rung-1 paper design.
  - **Confirmation R2 charter drafted, released, dispatched, and
    confirmed (`41d1e29`).** All eight measurements passed on independent
    re-derivation against committed HEAD source (`evaluator.py`,
    `runner.py`, `explanation.py`, `package_validation.py`, both
    `rule-artifact.v2`/`v3` schemas) by a reviewer with no access to the
    Repair 2 builder's session or the foreman's prior verification pass.
    D2-P1/D2-P3 confirmed genuinely untouched by direct comparison against
    `repair1/design.md`, not the design's own claim. Foreman independently
    spot-checked two of the most load-bearing citations before committing
    (the `use_v2` gating in `runner.py`, the schema grep) — both held
    exactly. One non-blocking note: a path discrepancy in the charter's
    stated vs. actual examination-file locations (documents only, not a
    finding against the design).
  - **All three D2 propositions (P1, P2, P3) are settled at Rung 1**
    across the full round 1 → repair 1 → confirmation 1 → repair 2 →
    confirmation 2 arc. Foreman wrote the disposition record
    (`docs/prototypes/qdcg-worksheet/evaluation-analysis.md`) and drafted
    **candidate ADR-0038** (`docs/adr/0038-qdcg-worksheet-and-declared-absence.md`,
    status **proposed**, Tier 3) from the confirmed shape, both landed
    together at `146887a`.
  - **➡️ NEXT ACTION: owner Tier 3 ratification decision on ADR-0038.**
    This is the owner's actual tax number — no default-window or
    auto-escalation path applies the way it might at Tier 1/2; the owner
    decides directly. Only after ratification can the milestone plan's
    Track 3 be chartered as a production build — the same sequence D3/D1
    (ADR-0035/0036) already went through this milestone.
  - **Foreman is not proceeding to charter Track 3 or take any other
    action on D2 without explicit owner direction.**
- **Boundary discipline (standing):** values, dispositions, refusal reasons,
  and the workspace location never enter the repository, a review, or a chat
  session; only the three-fact attestation crossed. Owner-held run tooling
  (`tools/scaffold_live_acts.py`, `workspace-seed/`) stays untracked.

## Historical record — Core Tax Conditions remediation (closed 2026-07-15)

- **Seat:** principal foreman.
- **✅ MILESTONE COMPLETE (2026-07-15, remediated re-close).** Tracks 0–7 landed and remediated; retrospective written (`docs/milestone-retrospectives/2026-07-15-core-tax-conditions-and-presentation-integration.md`); closure records (milestone doc, roadmap, phase-state) updated; ADR-0013 amendment + **ADR-0030** ratified; owner reconciled `main` (reset to `7a90f89`). Verification green: 350 tests, mypy, governance lint. **➡️ Next: the owner performs the single no-ff merge of this branch to `main`** (per ADR-0030 Transition — this milestone merges once; per-ADR/per-track granularity starts next phase). **After merge: next-phase planning is owner-directed — do not infer it.** The R1–R5 remediation trail below is the "how we got here" record; the retrospective is the durable account.
- **Milestone REOPENED for remediation (owner-directed 2026-07-15).** The Core
  Tax Conditions implementation was executed Tracks 1–6 and merged to `main`
  (`2fbc3a7`) in one autonomous run **without owner go and without a pre-merge
  review**. Owner rewound state to the last development commit `9dfcd62` on a
  recreated `milestone/core-tax-conditions` branch. **`main` still carries the
  premature merge (`2fbc3a7`) + post-merge docs (`1b370b7`) — an owner decision
  on how to reconcile `main` is pending; the foreman has NOT rewritten `main`.**
- **What's on this branch:** all development code — Track 0 (ADRs 0020, 0024–0029
  accepted) + Tracks 1–6 schemas/content/engine, package-instance checksum
  (`2329469`), strict-typing restore (`9dfcd62`). Verification currently green:
  348 tests, mypy clean (76 files), governance lint conformant.
- **Retrospective pre-merge review done** (`docs/reviews/2026-07-15-core-tax-conditions-premerge-review.md`,
  author-independent foreman): **keep the code; not merge-ready as closed.**
  Sound/faithful — ADR-0020 ledger+walk, ADR-0028 quantity surface, 0024/0025/
  0026/0029. **PMR-1 decision-blocking:** ADR-0027 decision 9 exclusive execution
  projection (ACM-A1) NOT implemented — co-located content is not inert. **PMR-2
  production condition:** ADR-0027 ACM-A5 member-byte verification absent. PMR-3
  Track 4 shipped with a stubbed checksum; PMR-4–7 process (no owner go, no
  pre-merge review, retrospective silent on process, Track 1 pre-typing-green).
- **Remediation chartered** (`docs/reviews/charter-2026-07-15-core-tax-conditions-remediation.md`):
  R1 exclusive projection (decision-blocking), R2 member-byte verification,
  R3 re-verify, R4 **independent** re-review, R5 honest re-close + retrospective
  rewrite + owner `main` reconciliation.
- **R1 landed:** `85ce351` implements ADR-0027 decision 9's exclusive execution
  projection and adds the required ACM-A1 golden. The scenario's JSON output
  matches its committed golden; `tests.tax.test_track6_integration` is green.
- **R2 landed (`351c880`):** member-citizen bytes are registry-verified during
  package resolution; the required unchanged-identity mutation golden passed
  in `tests.derivation.test_package_validation` (13 tests). The ad-hoc checksum
  generator used to produce registry entries is preserved under ignored `temp/`.
- **R3 chartered:**
  `docs/reviews/charter-2026-07-15-core-tax-conditions-r3-reverification.md`
  assigns an owner-launched verifier the complete suite, mypy, and governance
  lint. Failures stop for foreman triage; passing evidence opens R4 only.
- **R3 passed:** all three required commands are green; durable evidence is
  `docs/reviews/2026-07-15-core-tax-conditions-r3-verification.md`. R4 is now
  eligible for its owner-launched independent review.
- **R4 chartered:**
  `docs/reviews/charter-2026-07-15-core-tax-conditions-r4-independent-rereview.md`
  assigns a fresh independent reviewer four falsifiable checks over R1/R2 and
  requires an explicit `ready` / `not ready` verdict. The foreman will not
  review the artifact's merits.
- **R4 returned `not ready` (`30c4248`):** the R1 mechanism is sound, but its
  required ACM-A1 golden is not run by any committed test. Triage is recorded
  in `docs/reviews/2026-07-15-core-tax-conditions-r4-triage.md` as
  decision-blocking, without reopening the ADR contract.
- **Repair1 chartered:**
  `docs/reviews/charter-2026-07-15-core-tax-conditions-repair1-acm-a1-execution.md`
  permits only wiring the existing ACM-A1 scenario into the executed golden
  suite. Then repeat R3 verification and fresh independent R4 review.
- **Repair1 landed (`6c6f42f`):** the ACM-A1 scenario is now in Track 6's
  executed golden set and has an explicit absence assertion; the focused Track
  6 integration suite passed (4 tests).
- **R3R chartered:**
  `docs/reviews/charter-2026-07-15-core-tax-conditions-r3r-reverification-after-repair1.md`
  repeats complete verification before the required fresh independent R4R
  review.
- **R3R passed:** all three required commands are green; durable evidence is
  `docs/reviews/2026-07-15-core-tax-conditions-r3r-verification.md`. Fresh
  independent R4R review is now eligible.
- **R4R chartered:**
  `docs/reviews/charter-2026-07-15-core-tax-conditions-r4r-independent-rereview.md`
  assigns a fresh independent reviewer to measure that Repair1 made ACM-A1 an
  executed guard without reopening the settled R1/R2 mechanisms.
- **R4R returned `ready` (`696ef88`):** its four measurements pass; the
  decision-blocking ACM-A1 guard is now executed, and the repair remained
  strictly test-only.
- **R5 chartered:**
  `docs/reviews/charter-2026-07-15-core-tax-conditions-r5-honest-reclose.md`
  scopes the honest closure records and preserves the owner's sole authority
  to select `main` reconciliation.
- **R2 charter (completed):**
  `docs/reviews/charter-2026-07-15-core-tax-conditions-r2-member-byte-verification.md`
  bounds the required registry-verified member-byte check and its mutation
  golden. It expressly reserves full verification for R3 and stops on any new
  identity, membership, or registry contract question. The active remediation
  seat is `docs/reviews/SEAT.md`; any clerk or owner-launched builder starts
  there before the charter.
- **➡️ NEXT ACTION: owner performs the no-ff merge of `milestone/core-tax-conditions` into `main`.** R5 is complete (closure records staged; retrospective written; ADRs ratified; `main` reconciled). Foreman does not merge `main` autonomously. After the merge, the next phase is owner-directed.

- **Git/env hygiene:**
  - Run all tests via `.venv/bin/python3 -m unittest` (project `.venv`).
  - Validate conformance via `.venv/bin/python3 tools/governance_lint.py`; mypy via `-m mypy`.
  - Commit per logical unit; owner authorizes execution and launches seats.
