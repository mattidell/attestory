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

## Current state (updated 2026-07-13, end of remediation session; branch `milestone/core-tax-conditions` at `d13d1fb`)

- **Seat:** Claude is principal foreman (owner-appointed 2026-07-13, relieving
  the previous Codex foreman after the governance remediation — full history in
  the two topics' process logs). Standing owner directives, formalized in the
  ADR-0013 amendment and AGENTS.md (2026-07-13): rival evidence every round;
  non-accepted ADRs are inert; rejected ADRs retained, never deleted; **no
  foreman-spawned agents without a fresh owner go** (owner has been launching
  seats from foreman-issued prompts; integrate their outputs from the working
  tree, commit with foreman custody, and always split unrelated deliveries
  into separate commits).
- **Milestone:** Core Tax Conditions And Presentation Integration — plan
  **revised 2026-07-14** (see the milestone doc's revision note). Track 0 is
  **2 of 5 topics settled**; the owner directed remediation of all three
  remaining topics (interest 0021, manifests 0022, citations 0018) with
  conforming rival-backed rounds before any implementation track opens. **Next
  action: draft the Track 0.a taxable-interest-composition prototype plan**
  (owner approves, then owner-launches incumbent + clean-room rival, same
  pattern as the three topics just closed). Implementation tracks 1–7 rebuild on
  the ratified ADRs and inherit their production conditions (threaded per track
  in the plan). ADR status: 0019 rejected
  (retained); 0023 **accepted** (ratified at patch merge `bf23517`); 0024
  **accepted** (owner ratification 2026-07-13); 0025 **accepted** (owner
  ratification 2026-07-14); 0020 **accepted** (owner ratification 2026-07-14);
  0018/0021/0022 **proposed but non-conforming** — single-author paper spikes,
  no rival-backed prototype rounds (see 2026-07-14 Track-0 finding below).
- **Source Completeness reconciliation: CLOSED.** Review → patch → pre-merge
  review → corrections → owner non-ff merge `bf23517` → ADR-0023 ratified and
  roadmap updated on `main` (`7a90f89`). 316 tests/lint/mypy green post-merge.
  Optional follow-up SC-PR3 (thicken the committed SC-R1 probe end-to-end)
  can ride any future kernel track.
- **CS topic: closed for decision.** it2 accepted with CS-A10R/A11R errata;
  `evaluation-analysis.md` rewritten (complete); **ADR-0024** (Conditional
  Structures in the Rule Language) **accepted** (owner ratification
  2026-07-13). Track 3 rebuild is now gated only on the ELX topic outcome
  (its decisions 5–6 upgrade content written under 0024).
  Track 3's old implementation stays parked at `wip/track3-core-conditions`
  (`c8be492`), reference only.
- **ELX topic (expression-language-extensions): CLOSED. ADR-0025 accepted
  (owner ratification 2026-07-14).** Both exhibits committed (incumbent
  `a9e4b9c`, rival `b2b9022`); both committee reviews under custody
  (`reviews/round-1-governance.md` ELX-G1–G6, `reviews/round-1-adversary.md`
  ELX-A1–A8); `evaluation-analysis.md` written. Unanimous committee outcome:
  rival (it2) carried for both propositions; incumbent's `default_superseded`
  root class and generic `match` op rejected. ADR-0025 adopts the rival's
  same-`fact_id` correction-fold default (`optional_default` on `fact-type.v2`,
  `resolved_input` branch, `origin` pins, `input_bindings`) and
  `categorical_compare` + `category_literal` with governed code→label migration;
  resolves ADR-0024's delegated decisions 5–6. Three production conditions carry
  to implementation: PC1 transitive `origin` pins; **PC2 — new
  `CATEGORICAL_DOMAIN_MISMATCH` disposition reason amends the ADR-0012
  vocabulary** (the one cross-contract reach — implementers must update the
  disposition/explanation contracts); PC3 unexecuted-at-HEAD (needs
  correction-fold validation, two-runner parity, five cases as fixtures).
- **NPE topic: round 3 CLOSED; ADR-0020 NOT ratification-ready; round-4
  redraft outstanding.** Both round-3 reviews committed under custody
  (`reviews/round-3-governance.md` NPE-G9–G11 "ready after corrections";
  `reviews/round-3-adversary.md` NPE-A12–A18 "not ready"). Foreman triage
  `round-3-triage.md` confirms **seven decision-blocking findings** (the
  adversary's "not ready" is the correct disposition; the reviewers examined
  different surfaces, so findings are additive). `evaluation-analysis.md`
  rewritten for the through-round-3 state (converged shape C1–C3 endorsed;
  decision text not yet correct). **Pending owner disposition:** commission a
  round-4 ADR-0020 redraft (foreman custody, as the round-2→round-3 redraft
  was) folding the seven blockers + NPE-A14 into decision text and the
  `npe-walk.v1` schema, then a light confirmation review before ratification.
  **DONE (2026-07-14):** round-4 redraft of ADR-0020 written in foreman custody,
  folding all seven blockers + NPE-A14 (vocabulary-layering section, ledger
  totality, `blocked[]` as derived read-model, new decision 1a conflict-loser
  `inapplicable`, act-log-first walk, `rule_references[]` array, retracted
  "unchanged" pin walker, shared-table canonical store; fixture repair moved to
  prerequisites). Confirmation review chartered:
  `roles/reviewer-adversary-r4.md` (single adversary seat, scoped to the
  changes). **DONE (2026-07-14):** review committed (`reviews/round-4-adversary.md`,
  NPE-A19–A22, "ready after listed corrections"); six of eight round-3 blockers
  confirmed closed; two new decision-blocking defects in the round-4 draft
  (NPE-A19 absent-deps conflict-loser masked as inapplicable; NPE-A20 unscoped
  act-log-first walks the wrong run's finding). Both applied in a **round-5
  corrective redraft** of ADR-0020 (foreman custody, `round-4-triage.md`):
  decision 1a is now a fixed classification order (absent dep → `blocked`; else
  already-published → `inapplicable` conflict-loser with `superseded_by`, no
  synthetic guard; else evaluate), and decision 4 is run-scoped selection.
  **ADR-0020 ACCEPTED (owner ratification 2026-07-14)**, with the NPE-G10
  fold+fixture-repair prerequisite to land concurrently in implementation. NPE
  topic CLOSED.
- **Git hygiene notes:** use the project `.venv` (system python lacks
  jsonschema); owner-launched threads drop uncommitted files into this
  working tree — check `git status` before any `git add -A` and split
  deliveries from your own doc changes. Milestone roadmap/handoff will
  conflict with `main`'s at merge; resolve toward the milestone versions.
- **Pending owner decisions:** (1) approve the Track 0.a interest-composition
  prototype plan once drafted, then launch its seats; (2) milestone-level
  process retrospective on the delegation experiment — the CS→ELX arc and the
  NPE five-round arc are both complete, rich evidence in hand (single-builder
  rounds would likely have ratified the unsound `default_superseded` mechanism,
  ELX-A1; NPE's authored-vs-transcribed defect pattern across four drafts);
  timing owner's.
- **Track-0 finding (2026-07-14):** the prior Codex foreman's ADRs 0018/0021/
  0022 are non-conforming single-author paper spikes (0018 has no artifact at
  all), inert per the ADR-0013 amendment. Owner directed remediation of all
  three. This is the same skipped-rival defect class that reopened CS/NPE —
  worth a line in the retrospective about how far it propagated.
- **Side thread (not foreman scope):** product naming — front-runner
  "Attestory"; `attestory.com` is a 2026-01-30 GoDaddy registration with a
  "Launching Soon" page and no other footprint; owner's USPTO check decides.
