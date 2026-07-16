# Charter: Iteration 2 — Real-Data Residency Boundary (Clean-Room Rival)

Date: 2026-07-16. Plan approved by owner (PR #2, merged `c33cd66`). Track 0,
topic D1 of the First Real Return Slice milestone. Owner directed D1 solo.

- **Builder:** clean-room rival, High tier, independent context, **sealed from
  the incumbent**.
- **Working location:** `docs/prototypes/real-data-residency/it2/`; foreman holds git custody.
- **Evidence:** Rung 2 — paper classification-rule/enforcement diffs, plus **throwaway probes** in a scratch directory **outside** the repository. No repository modifications beyond the two outputs; no git write commands.
- **Questions:** D1-P1 (residency location rule + deterministic classification rule + enforcement surface on **commit and push**) and D1-P2 (synthetic-derivation rule).

## Clean-room seal (mandatory)

You are the independent rival. **Do not read** `it1/`, `examination-it1.md`, or
any incumbent output; if you encounter incumbent material, stop and report rather
than continue. You derive the boundary independently from the committed contracts
and the plan. Genuine rivalry per round is required (ADR-0013 amendment
2026-07-13): your evidence must be built in this context alone. Where you reach
the same conclusion as the boundary must be by independent justification, not
inheritance; where you diverge, say so and why — divergence is signal for the
committee.

## Current enforcement (binding context — extend, do not assume complete)

The only enforcement today is one test,
`tests/test_kernel_fixtures.py::test_committed_kernel_fixtures_have_no_absolute_local_paths`,
scanning **one directory** (`packages/sample_data/kernel`) for a few path markers
(`/Users/`, `/private/`, `local-data/`, `uploads/`). There are **no git hooks**
and **no push-surface guard**. This is the narrow floor to widen, not a model.
ADR-0030 §C.8 requires the boundary to hold on the **push/publication** surface;
the interim private-remote posture must never be load-bearing.

## Assignment

Design both propositions against the committed contracts at `HEAD`:

1. **D1-P1.** (a) The **location rule** for live workspaces: a declared
   out-of-repo residency stated as a rule (not a concrete path), and why a run
   may read it while the repo cannot contain it. (b) A **deterministic
   data-classification rule** partitioning every artifact class into may-cross
   (code, contracts, synthetic fixtures) vs never-crosses (anything personal);
   an undecidable artifact is a boundary hole. (c) An **enforcement surface**
   rejecting a never-crosses artifact at every crossing point, covering both the
   **commit** and the **push** surface (ADR-0030 §C.8), as versioned diffs. (d) A
   **complete kill-test enumeration** of every crossing surface — commit, push,
   test fixture, golden, charter, review, process log, retrospective, scratch
   dir, run output/ledger — each with an enforcement point or explicit no-carry
   argument. Omitting a surface is decision-blocking.

2. **D1-P2.** The **synthetic-derivation rule**: how a real document's *shape*
   becomes an in-repo synthetic fixture provably carrying **no real value** — a
   checkable re-expression, not an ad-hoc scrub.

## Required cases

The plan's six Gate-2 cases: (1) clean boundary; (2) leak — commit rejected;
(3) leak — **push** rejected (distinct from case 2); (4) synthetic derivation
carries shape not value; (5) classification-ambiguity negative; (6) **kill-test
enumeration** (mandatory, decision-blocking). For each: claim →
classification-rule/enforcement change → scan/gate behavior → observed
reject/accept. Cases 3 and 6 must be *probed*, not asserted.

## Outputs

- `docs/prototypes/real-data-residency/it2/design.md`
- `docs/prototypes/real-data-residency/examination-it2.md` (≤120 lines) stating
  D1-P1 and D1-P2 separately as settled-at-Rung-2 or unresolved, citing every case.

Read: the topic `plan.md`, this charter, `docs/governance/`, ADR-0030 (esp. §C.8),
the milestone plan's Data-safety section, and `tests/test_kernel_fixtures.py`.
**Do not read incumbent material.** Before writing, echo scope, the seal, the
Rung-2 / outside-repo boundary, and stop conditions.

## Stop conditions

Stop at the two static files. No enforcement code committed, no scan edits, no git
writes. If a design needs a contract change you cannot represent as a versioned
diff on paper, stop and report. Every value, payer, path, and identifier is synthetic.
