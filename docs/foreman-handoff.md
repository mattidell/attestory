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

## Current state (updated 2026-07-15; branch `milestone/core-tax-conditions`)

- **Seat:** Claude is principal foreman (owner-appointed 2026-07-13). Standing
  owner directives (ADR-0013 amendment + AGENTS.md): rival evidence every round;
  non-accepted ADRs are inert; rejected ADRs retained, never deleted; **no
  foreman-spawned agents without a fresh owner go** — the owner launches every
  builder/reviewer seat from foreman-issued prompts; the foreman integrates
  their dropped files from the working tree, commits with custody, and **splits
  each owner-launched delivery into its own commit, separate from foreman doc
  changes**.

- **The working rhythm (every remediation topic follows it):** foreman drafts
  `plan.md` → owner approves → foreman writes `charter-it1.md`, owner launches
  the incumbent → foreman conformance-checks + commits the exhibit → foreman
  writes `charter-it2.md` (clean-room rival, sealed from it1 **and** any prior
  spike/ADR), owner launches it → conformance + commit → foreman charters two
  committee reviewers (Governance + Adversary, independent contexts, both read
  both designs), owner launches them → foreman triages into
  `evaluation-analysis.md` → foreman drafts the ADR → owner ratifies. Conformance
  is scope-only (two files, exam ≤120 lines, all required cases incl. the
  mandatory ones, Rung boundary held); merits go to the committee.

- **Milestone:** Core Tax Conditions And Presentation Integration — plan
  **revised 2026-07-14** (`docs/phases/foundation/milestones/core-tax-conditions-and-presentation-integration.md`,
  see its revision note). Track 0 (contract decisions) must fully ratify before
  any implementation track opens; implementation tracks 1–7 rebuild on the
  ratified ADRs and inherit their production conditions (threaded per track).

- **Track 0 status — 5 of 5 topics settled (contract remediation complete):**
  - ✅ Conditional structures → **ADR-0024** accepted; expression extensions → **ADR-0025** accepted.
  - ✅ Non-publication explanations → **ADR-0020** accepted.
  - ✅ Taxable-interest composition → **ADR-0026** accepted (Track 0.a).
  - ✅ Adopted-content manifests → **ADR-0027** + **ADR-0028** accepted (Track 0.b floor + residual).
  - ✅ Citation resolution → **ADR-0029** accepted (Track 0.c; supersedes inert ADR-0018).

- **Implementation tracks OPEN (2026-07-15).** Track 0 complete. Track **1 active**
  (contract schemas + payload instances per ADRs 0020/0024–0029). Tracks 2–7
  open and sequenced after Track 1 as the plan requires.

- **➡️ NEXT ACTION: execute Track 1 per the work order** —
  `docs/phases/foundation/milestones/core-tax-conditions-track-1-plan.md`
  (foreman-prepared 2026-07-15). It enumerates every new/changed schema in
  dependency layers A→E (quantity vocab, role canon, fact-type.v2/bundle.v2,
  package.v2, derived-finding.v2, rule-artifact.v2, operation-semantics.v2,
  source-closure-mapping.v2, derivation-record fold, npe-walk.v1,
  taxable-interest-composition.v1, citation.v1, form-field.v2 + ADR-0012 vocab),
  with per-schema positive/negative payloads, schema tests, and registry
  immutability. **Scope fence:** schemas + payloads + tests + `published.json`
  only — validator dispatch is Track 4, content is Tracks 2/3, runner/walker is
  Track 5. **Open question for owner:** who drives Track 1 — an owner-launched
  implementation seat or the foreman directly under owner go (repo code, not a
  decision round, so the rival discipline does not apply). Then Track 2
  (line 2b / ADR-0026) unless reprioritized.

- **ADR ledger:** 0019 rejected (retained); 0020, 0023, 0024, 0025, 0026, **0027**,
  **0028**, **0029 accepted**; 0021 superseded by 0026; 0022 superseded by 0027;
  0018 superseded by 0029. ADR-0013 amendment still **proposed** (foreman-authored
  fixes default to confirmation) for the process retrospective.

- **Git/env hygiene:** use the project `.venv` (system python lacks jsonschema);
  check `git status` before any `git add -A` (owner threads drop uncommitted
  files); the owner sometimes commits a delivery directly (e.g. the TIC
  governance review `15e90f3`) — reconcile against git, don't assume custody.
  Milestone roadmap/handoff will conflict with `main`'s at merge; resolve toward
  the milestone versions.

- **Pending / deferred (owner-timed, not blocking Track 0.b):**
  - Milestone-level **process retrospective** on the delegation experiment —
    rich evidence now in hand across four topics: the two-builder rivalry caught
    an unsound mechanism (ELX-A1 `default_superseded`) and a substantive omission
    (TIC-A1 OID); NPE showed an authored-vs-transcribed defect pattern across
    four drafts; and the skipped-rival defect propagated to 3 inert Track-0 ADRs.
    **Proposed ADR-0013 amendment awaiting ratification here:** foreman-authored
    fixes to adversary/governance findings default to a scoped confirmation pass
    (foreman recommends it proactively; owner is never asked to adjudicate
    "is this in-evidence?"). See ADR-0013 "Amendment (2026-07-15, proposed)".
    Origin: the ADR-0028 decision-7 over-trigger handback.
  - The ADR-0026 deferred follow-ons (further positive interest sources; the
    subtractive-adjustment mechanism) are future decision topics, not this
    milestone's blockers.
  - **Side thread (not foreman scope):** product naming — front-runner
    "Attestory"; `attestory.com` is a 2026-01-30 GoDaddy "Launching Soon"
    registration; owner's USPTO check decides.
