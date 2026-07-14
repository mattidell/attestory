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
- **Milestone:** Core Tax Conditions And Presentation Integration — remediation
  essentially complete; implementation not restarted but now **unblocked** —
  both rule-language engine decisions are ratified. ADR status: 0019 rejected
  (retained); 0023 **accepted** (ratified at patch merge `bf23517`); 0024
  **accepted** (owner ratification 2026-07-13); 0025 **accepted** (owner
  ratification 2026-07-14); 0018/0020/0021/0022 proposed.
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
  Six of eight fixes are ADR-text/vocab/concurrent-schema corrections; two are
  substantive and need the owner's eye — **NPE-A13** (published finding
  returns `no_disposition_recorded` after an interrupted run — a false "no
  explanation" vs Articles 8/15) and **NPE-A12b** (the only *new* decision:
  canonical disposition of an unselected conflict-loser, which the forward and
  reference runners currently record differently).
- **Git hygiene notes:** use the project `.venv` (system python lacks
  jsonschema); owner-launched threads drop uncommitted files into this
  working tree — check `git status` before any `git add -A` and split
  deliveries from your own doc changes. Milestone roadmap/handoff will
  conflict with `main`'s at merge; resolve toward the milestone versions.
- **Pending owner decisions:** (1) ratify ADR-0020 after NPE round 3; (2)
  milestone-plan revision + Tracks 1–3 re-run — **now unblocked** (Track 1
  conditional-structure schemas rebuild under ADR-0024, not the rejected 0019;
  Track 3 rebuilds under ADRs 0024 + 0025; ELX production conditions PC1–PC3
  land here); (3) milestone-level process retrospective on the delegation
  experiment — the CS→ELX arc is now complete, so its strongest evidence
  (single-builder rounds would likely have ratified the unsound
  `default_superseded` mechanism the two-builder round caught, ELX-A1) is in
  hand; timing owner's.
- **Side thread (not foreman scope):** product naming — front-runner
  "Attestory"; `attestory.com` is a 2026-01-30 GoDaddy registration with a
  "Launching Soon" page and no other footprint; owner's USPTO check decides.
