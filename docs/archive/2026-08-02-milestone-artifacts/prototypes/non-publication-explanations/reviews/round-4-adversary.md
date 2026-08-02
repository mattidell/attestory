# Adversary Review — Round 4: Non-Publication Explanations (ADR-0020 confirmation)

- **Topic:** Non-Publication Explanations in the Derivation Cascade
- **Round:** 4 (confirmation of the round-4 ADR-0020 redraft)
- **Reviewer:** Adversary Reviewer (Round 4)
- **Date:** 2026-07-14
- **Subject:** Round-4 redraft of `docs/adr/0020-non-publication-explanation-walking.md` (folding the round-3 triage's seven decision-blocking findings and NPE-A14)
- **Scope:** Confirmation only — the durable-ledger shape (conclusions C1–C3) is settled and out of scope. Attack: whether each round-3 blocker is closed without a new loophole.
- **Independence:** single adversary seat this round by design; no sibling round-4 review read.
- **Evidence read:** round-4 ADR-0020; `round-3-triage.md`; `reviews/round-3-adversary.md` and `reviews/round-3-governance.md`; topic `plan.md`; `it2/design.md` and `examination-it2.md`; `docs/governance/`; ADRs 0006–0009, 0012; committed `packages/derivation/` (`records.py`, `runner.py`, `reference_runner.py`, `explanation.py`, `projection.py`) and `derivation-record.v1` / publication-act schemas at `HEAD`.
- **Verdict:** **ready after listed corrections**

---

## Executive Summary

Six of the eight round-3 blockers are closed by the round-4 text without reopening the durable-ledger shape. Two are **not** closed cleanly:

1. **Decision 1a (NPE-A12b)** still forces a conflict-loser to `inapplicable` **regardless of whether its dependencies are present**, which collapses NPE-P2 / ADR-0012's blocked-vs-inapplicable frames and invents a non-evaluated "superseded" guard fact.
2. **Decision 4 (NPE-A13)** correctly prefers a live publication over an empty interrupted ledger, but **"act-log first, regardless of the ledger"** is under-specified and, as written, can attach the wrong finding when multiple runs have published the same symbol.

Vocabulary layering, the `blocked[]` derived read-model, multi-publisher schema agreement, pin-walker shared-memo authorization, ledger totality wording, and the shared-table rendering resolution are sound. The durable shape remains ratification-worthy once the two corrections below land.

---

## Assignment Rulings (eight points)

| # | Round-3 blocker | Round-4 ruling |
|---|---|---|
| 1 | NPE-G9/G11 ledger vocabulary | **Closed.** Vocabulary-layering section + decisions 1 and 7 use committed ledger enum `{published, blocked, inapplicable}` and ADR-0012 payload terms; mapping is total via decision 7 (`inapplicable` → `guard_inapplicable`). |
| 2 | NPE-A12a fold / consumers | **Closed.** `blocked[]` is a derived compatibility read-model over ledger rows with `disposition = blocked`. By construction it cannot disagree with those rows once the concurrent schema fold puts `code`/`missing` on the ledger row (stated in decision 1; NPE-G10 prerequisites). Committed consumers (`records.py::recover_interrupted`, tests writing `blocked=[]`) keep a stable surface. |
| 3 | NPE-A12b conflict-loser | **Not closed.** Decision 1a makes both runners agree, but the agreement is on a dishonest class when the loser also has absent deps — see **NPE-A19**. |
| 4 | NPE-A13 act-log-first | **Partially closed.** The interrupted empty-ledger case is fixed in intent; the written rule opens a multi-run finding-selection loophole and underspecifies run-scoping — see **NPE-A20**. Superseded-pin walks of a correctly selected historical finding are honest projections (pins are on the finding; Article 12 displacement does not erase history). |
| 5 | NPE-A16 multi-rule schema | **Closed** for the stated contradiction (array `rule_references[]` + all-producers lookup vs singular `artifact_id` / `publisher_of`). Residual mixed-disposition projection detail is production-time schema work — see **NPE-A21**. |
| 6 | NPE-A17 pin walker | **Closed.** Retracts "unchanged"; authorizes an additive optional shared-table parameter on `explanation.py` with committed single-branch behavior when absent. Implementable against the current `_seen: frozenset` cycle-only API without forcing a behavior change on the no-parameter path. |
| 7 | NPE-A18 ledger totality | **Closed.** "Per rule and selector artifact in the adopted package" removes the eligible-only loophole; production conditions still compel schema totality. Residual "selector" wording is stale vs ADR-0024 — **NPE-A22** (non-blocking). |
| 8 | NPE-A14 memoization | **Closed.** Shared table is the canonical store of expanded results; inline vs reference is rendering; entry-guarantee no longer tensions with "diamonds only." |

---

## Findings

### NPE-A19 — Decision 1a records conflict-losers with absent dependencies as `inapplicable`, hiding a real block

**Severity: decision-blocking.**  
**Applies to: Decision 1a (conflict-loser disposition).**  
**Closes? NPE-A12b — no (new honesty defect).**

#### The check (charter attack)

Construct a rule that is **both** an unselected conflict sibling **and** has genuinely absent dependencies.

#### Input state

Package declares `conflict_semantics` for output symbol `S` (ADR-0006 decision 7). Two rules:

| Rule | `requires` | `publishes` | Priority / schedule |
|---|---|---|---|
| `R_winner` | `{A}` (present) | `S` | First to fire under either runner's producer order |
| `R_loser` | `{B}` (**absent**) | `S` | Never eligible |

Workspace: `A` present, `B` missing. Run saturates.

#### Expected honest ledger

- `R_winner`: `published` (produced `S`).
- `R_loser`: **`blocked` / `BLOCK_ABSENT` with `missing: ["B"]`** — it never competed; its dependency gap is a real run fact (NPE-P2 missing-dependency frame; ADR-0012 decision 4 `blocked`; ADR-0006 decision 8 blocking discipline).

#### What decision 1a requires

> recorded `inapplicable` (guard result: superseded by the selected publisher), **not** `blocked` — **regardless of whether its own dependencies are present**.

So both runners must emit:

- `R_loser`: `inapplicable`, with a required `guard_result` implying a guard that was never evaluated (the rule was never eligible; `when` did not run).

#### Why this fails

1. **Hides a real block.** The ledger answers "why no contribution from `R_loser`?" with "superseded by the winner" when the truth is "could not run: `B` absent." If the winner is later removed or reordered, `R_loser` still cannot publish. The conflict story is counterfactual.
2. **Collapses NPE-P2.** Payload mapping sends ledger `inapplicable` → `guard_inapplicable`. The walk of `R_loser` shows an unsatisfied-guard frame (no `unmet[]`) for a pure missing-dependency case — exactly the conflation NPE-P2 forbids.
3. **Invented guard fact.** Decision 2 forbids re-evaluating guards; decision 1 requires `guard_result` when `inapplicable`. Decision 1a supplies a synthetic "superseded" guard without evaluation. That is a new authority: a disposition class that is neither an evaluated false `when` nor a recorded dependency gap.
4. **Portability of the *wrong* answer.** Both runners can implement "if `publishes` is already in `symbols`, record `inapplicable` in `finalize_unreached` / the saturation loop" and agree — NPE-A12b's *disagreement* is fixed, but they agree on a falsehood for the absent-deps case. Agreement is necessary, not sufficient.

#### Contrast: deps present, true conflict

When `B` is also present and `R_loser` is eligible but unselected because `S` is already published, recording `inapplicable` is defensible (the rule could have run; conflict policy selected another publisher). That half of 1a is sound. The defect is the **regardless of dependencies** clause.

#### Correction shape (advisory — do not redraft here)

Classify in order:

1. If any declared dependency is absent → `blocked` / `BLOCK_ABSENT` with `missing` (even if a sibling already published `S`).
2. Else if output symbol already published by another producer under declared conflict semantics → `inapplicable` (conflict-loser; document how `guard_result`/pins are filled without inventing a false `when` evaluation — e.g. explicit conflict-supersession evidence, or a dedicated ledger sub-code under `inapplicable`).
3. Else evaluate `when` / value as today.

Both runners apply the same order in `attempt` and `finalize_unreached`.

---

### NPE-A20 — Decision 4's unconditional "act-log first" can walk the wrong finding (multi-run / wrong-run)

**Severity: decision-blocking.**  
**Applies to: Decision 4 (sparse-ledger honesty, act-log first).**  
**Closes? NPE-A13 — partially (interrupted empty ledger yes; selection rule no).**

#### What round-4 correctly fixes

Interrupted run: publications land in the act log; `recover_interrupted` writes `published=[]`, `dispositions=[]` (`records.py` at `HEAD`). Walking only the ledger yields `no_disposition_recorded` for a live value (NPE-A13). Preferring a publication present in the act log restores Articles 8/15 for that case.

#### Attack A — multi-run same symbol

1. Run `R1` publishes finding `F1` for symbol `S` (completed ledger has a `published` row → `F1`).
2. Run `R2` publishes finding `F2` for `S` (later revision).
3. Consumer requests a walk of **run `R1`** for `S`.

Decision 4: *"first consults the workspace act log: **if the finding is published there**, the walker walks it via the pin-lineage walker **regardless of the ledger's state**."*

As written, "the finding" is not bound to:

- `payload.run_id == R1` on the derived-publication act (schema requires `run_id` on the act payload), nor
- the ledger row's finding reference when the ledger is complete.

An implementer who takes "any / latest act-log publication of `S`" walks **`F2` while claiming to explain `R1`** — wrong pins, wrong rule, wrong currency story — and is still conforming to the letter of decision 4 because a finding for `S` is "published there" and the ledger was ignored "regardless."

#### Attack B — interrupted run + later successful run

1. Run `R1` publishes `F1` for `S`, then crashes; recovery ledger is empty.
2. Run `R2` completes and publishes `F2` for `S`.
3. Walk of `R1` under naive act-log-first attaches `F2` (or current currency's finding) instead of `F1`.

NPE-A13's empty-ledger lie is avoided only if the act-log lookup is **run-scoped**. The redraft never says so.

#### Attack C — superseded / withdrawn pins (charter)

Given a **correctly selected** finding `F` for the run under explanation:

- `F` pins input `I@v1`; later acts supersede `I`; derivation currency displaces `F` (Article 12 / `projection.py` compose-over).
- Pin-lineage walk of `F` still projects committed pins (historical justification). That is honest for a **run-scoped** historical walk and matches Article 15 (explanation from the record, not current state).
- Decision 6's `run_id` + `workspace_revision` let consumers detect staleness vs the live workspace. No new defect **once finding selection is run-scoped**.

The residual risk is not superseded pins per se; it is selecting the wrong finding before the pin walk begins.

#### Open-run residual (non-blocking)

Walks mid-flight while a run is still open (no closing record) for symbols not yet published still fall into `no_disposition_recorded`, and the text only names completion states `interrupted` / `recovered`. Acceptable if product only explains closed runs; pin as implementation note, not a ratification blocker.

#### Correction shape

Order of consultation for walk of run `R`, symbol `S`:

1. If the closing ledger for `R` has a **`published`** row for the producing artifact / symbol with a finding id → walk **that** finding via the pin walker.
2. Else if the act log contains a `derived-publication` whose `payload.run_id == R` and whose finding publishes `S` → walk that finding (covers interrupted empty `published[]`).
3. Else if the ledger has a non-published row for a producer of `S` → project the ledger row (blocked / inapplicable).
4. Else → `no_disposition_recorded` naming the run's closing phase (or open).

Never consult "some publication of `S`" without a run binding. Do not ignore a complete ledger's finding reference in favor of a later act.

---

### NPE-A21 — Multi-publisher nodes: array of references without mixed-disposition projection rules

**Severity: production condition.**  
**Applies to: Decision 3 (multi-publisher nodes).**  
**Closes? NPE-A16 — yes for schema singularity; residual at implementation.**

Decision 3 and the stated `npe-walk.v1` change fix the singular `artifact_id` / `publisher_of` contradiction. Remaining gap: when producers of `S` have **mixed** ledger rows (one `published`, one `inapplicable` conflict-loser, one `blocked`), the decision says the node carries `rule_references[]` and that the walker resolves all producers, but not:

- which single `node_kind` the symbol node takes, or
- where each producer's disposition evidence attaches (per-reference sub-nodes vs annotations).

This does not reopen NPE-A16's text/schema disagreement; pin it when the schema lands. Not ratification-blocking for the ADR's decision core.

---

### NPE-A22 — "Selector artifact" totality wording is stale under ADR-0024

**Severity: non-blocking / correction.**  
**Applies to: Decision 1 / production conditions (totality).**  
**Closes? NPE-A18 — yes on substance.**

ADR-0024 (accepted) rejects first-class selector citizens; conditional structure is ordinary guarded rules. Round-4 totality language still says "per rule and **selector** artifact." Harmless if the selector set is empty, but it invites implementers to invent a package member kind that is no longer in authority. Prefer "per rule artifact (and any other derivation-producing package member kinds actually adopted)" or simply "per rule artifact in the adopted package." Does not reopen the eligible-only sparsity loophole.

---

## Closed blockers (brief evidence)

### NPE-G9 / G11 — vocabulary

Ledger enum matches `derivation-record.v1` (`published` | `inapplicable` | `blocked`). Payload uses ADR-0012 (`guard_inapplicable`, `invalid` as blocked refinement). Decision 7 maps; no `executed` / ledger-level `guard_inapplicable` remain.

### NPE-A12a — `blocked[]` derived read-model

Decision 1: ledger authoritative; `blocked[]` = rows with `disposition = blocked`. Concurrent prerequisite lands the fold + repairs the self-contradictory sample fixture (`demo.rule.tax-table-line16` is both top-level `blocked` and disposition `inapplicable` at `HEAD` — NPE-G10). No second authority surface.

### NPE-A16 — multi-rule schema

Decision 3 requires `rule_references[]` and all-producers resolution; text and intended schema agree. (See NPE-A21 for residual projection detail.)

### NPE-A17 — pin walker shared memo

`explanation.py` today passes `_seen` by value (cycle-only). Optional shared-table parameter is additive; absent parameter preserves single-branch behavior. "Unchanged" retracted.

### NPE-A18 — totality phrasing

"Per rule … in the adopted package" (not "eligible") matches the pure-projection requirement and `finalize_unreached` intent. Schema totality remains a production condition.

### NPE-A14 — shared table vs diamonds

Canonical store on first expansion; inline vs reference is rendering; entry-memo no longer implies illegal "always flatten" under a diamonds-only reading.

---

## Verdict and corrections required

### Verdict: **ready after listed corrections**

The durable Run Disposition Ledger shape stands. Ratification should wait only on decision-text corrections to 1a and 4 (and the already-listed concurrent fixture/schema fold). No shape reopening.

### Listed corrections (advisory)

1. **NPE-A19 — Decision 1a:** Drop "regardless of whether its own dependencies are present." Absent deps → `blocked` with `missing`; only eligible, unselected conflict siblings → `inapplicable`. Define non-fictional evidence for that `inapplicable` (no synthetic unevaluated guard). Require both runners to use the same classification order in `attempt` / `finalize_unreached`.
2. **NPE-A20 — Decision 4:** Replace unconditional "act-log first regardless of ledger" with run-scoped selection: ledger `published` finding ref for run `R` first; else act-log `derived-publication` with `payload.run_id == R`; else ledger non-published row; else `no_disposition_recorded`. Preserve the interrupted empty-ledger recovery without allowing a later run's finding to explain an earlier run.
3. **Already required (NPE-G10):** Land single-surface schema fold + repair `derivation-record.completed.json` concurrently with ratification.
4. **Non-blocking polish:** NPE-A22 selector wording; NPE-A21 mixed multi-publisher projection when `npe-walk.v1` is written.

### Explicitly not reopened

Durable ledger placement; pure-projection walker; Articles 12/13 act-log purity; ADR-0012 payload vocabulary; cycle/memo entry-guarantee architecture; currency declaration (NPE-A15 remains advisory).

---

*Advisory only — the owner ratifies.*
