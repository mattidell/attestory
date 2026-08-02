# Examination (Iteration 2, Clean-Room Rival)

Design under examination: `it2/design.md` — the **Run Disposition Ledger and its
Projection Walk**. Evidence class: Rung 2 static (JSON Schema + paper
walkthroughs). No execution. This examination judges NPE-P1 and NPE-P2
separately at the static level, citing all three required cases.

## Boundary and exclusions honored

Paper only; no runner code, no python, no git writes. Grounding limited to
`plan.md`, `charter-it2.md`, governance, ADRs 0002/0004/0006–0012/0016/0017, and
committed schema/contract files. Did not read it1, examination-it1, reviews,
triage, evaluation-analysis, SEAT, process-log, ADR-0019/0020, other topics'
material, or the uncommitted `evaluator.py`/`runner.py` working-tree changes.

## NPE-P1 — no act-log pollution with mock values or empty findings

**Verdict: SETTLED at the static level.**

The non-publication evidence is a **disposition-ledger row in the closing
derivation record** (`derivation_records.jsonl`), which ADR-0002/0008 decision 1
make a citizen kind *separate from the act log*. The act log admits only kernel
acts and real `derived-publication` acts carrying a complete `derived-finding.v1`
(ADR-0010 decision 1); a blocked or inapplicable artifact produces no finding and
no act. The walker is read-only and writes nothing. So no mock value, empty
finding, or stub citizen can reach the authoritative store — by construction, not
by discipline.

- **Case 1 (blocked line 2b → 9/11/12/15/16):** six empty lines, zero findings
  and zero acts emitted; six ledger rows (`OPEN_SOURCE` / `UNREACHED`) in the run
  account. `acts.jsonl` is untouched.
- **Case 2 (inapplicable itemization override):** one `inapplicable` ledger row;
  no finding for the non-applied branch. The applied branch
  (`standard_deduction_applied`) publishes a real finding normally.
- **Case 3 (invalid input):** the invalid input remains its own (invalid) kernel
  finding; the consuming artifact emits a `blocked/INVALID` ledger row, not a
  finding. No stub enters the log.

*Residual, non-blocking:* NPE-P1's completeness (a row per eligible artifact)
rests on ledger **totality**, which the committed record schema does not yet
compel (design §9.1). Totality affects how *complete* the walk is, not whether
the log is polluted — pollution is impossible regardless. So P1 is settled;
totality is a P2/completeness contract question below.

## NPE-P2 — lineage distinguishes missing deps from unsatisfied guards

**Verdict: SETTLED at the static level, conditional on one record-schema
obligation (guard_result required on inapplicable rows).**

The distinction is enforced by the walk schema itself, not merely represented:

- a `blocked` node carries `block_code` and an `unmet[]` array reached by
  `edge_kind = unmet_dependency` — the missing-dependency frame;
- an `inapplicable` node carries `guard{result:false, read:[…]}` and is
  **schema-forbidden** from carrying `unmet` (`"not": {"required": ["unmet"]}`) —
  the unsatisfied-guard frame; its guard inputs, if shown, are `guard_input`
  edges, never `unmet_dependency`.

Two different node kinds, reached by two different edge kinds: a consumer cannot
conflate "empty because a dependency is missing" with "empty because a guard is
false."

- **Case 1** exercises the *missing-dependency* frame: every node is `blocked`
  with `unmet` edges, terminating at `OPEN_SOURCE` naming one source-family
  declaration — one root cause across five downstream lines, surfaced via
  `ref{shared}` pointers.
- **Case 2** exercises the *unsatisfied-guard* frame: an `inapplicable` node with
  `guard.result=false`, `guard.read` listing the pins consulted, and
  `selected_alternative` naming the branch that did apply — and **no** `unmet`.
- **Case 3** shows the distinction is *layered*: the top-level split
  (blocked vs inapplicable) is undisturbed while `block_code` refines *blocked*
  into `INVALID` (present-but-invalid, with `invalid_input`) vs `ABSENT`
  (missing), exactly the ADR-0012 decision-4 refinement, beneath NPE-P2's split.

Why this is the *right* shape, not just a working one: whether a line is empty
for a missing dependency or a false guard is a **run fact** (which guard was
false, which symbol was absent for *this* input state), not derivable from the
static rule text. Recording it at evaluation time is the only shape that keeps
the walk a pure projection rather than a re-evaluation (design §1).

*Condition:* the committed `derivation-record.v1` makes `guard_result` optional
(design §9.4). NPE-P2's inapplicable frame needs `guard_result = false` present
whenever `disposition = inapplicable`. This is a one-line record-schema
obligation, not a design gap — hence "settled, conditional."

## Cross-cutting checks

- **No re-evaluation / retention sufficiency (Rung 2):** every node folds a
  committed row or pin; the only walk-time computation is a static
  `symbol → artifact` index from adopted `publishes` fields. The ledger + adopted
  artifacts retain enough structure to walk unexecuted rules (design §8).
- **Cycles/diamonds terminate:** `visited.active` cuts rule-reference cycles to
  `ref{cycle}`; `shared` memoizes diamonds to `ref{shared}`. Each artifact
  expands at most once; walk is O(|artifacts| + |edges|) and halts (design §8).
- **Zero refinements** (`computed_zero`/`closure_backed_zero`) are projected from
  the published finding's lineage, not the ledger (design §6) — preserving
  ADR-0012 decision 6 with no new authority.

## Unresolved authority questions (reported, not resolved)

1. **Ledger totality** — is the runner obliged to emit a disposition row per
   eligible artifact, including `UNREACHED` down-cascade rows? (design §9.1)
2. **Two committed blocked surfaces** — reconcile top-level `blocked[]` with
   `dispositions[disposition="blocked"]`; is folding `{code,missing}` onto the row
   acceptable? (design §9.2)
3. **Zero-refinement division of labor** between ledger and lineage (design §9.3).
4. **`guard_result` required on inapplicable rows** — the one condition on the P2
   verdict (design §9.4).
5. **Vocabulary** — record `inapplicable` vs ADR-0012 `guard_inapplicable`;
   pin one canonical term (design §9.5).

## Summary

NPE-P1: **settled** (recorded evidence lives outside the act log; walker writes
nothing). NPE-P2: **settled, conditional** on `guard_result` being required for
inapplicable rows; the missing-dependency vs unsatisfied-guard split is
schema-enforced, demonstrated across all three cases. Both verdicts hold at the
static level; the open items are record-schema/runner-contract obligations the
walker consumes and cannot ratify alone.
