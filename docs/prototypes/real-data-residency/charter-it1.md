# Charter: Iteration 1 — Real-Data Residency Boundary (Incumbent)

Date: 2026-07-16. Plan approved by owner (PR #2, merged `c33cd66`). Track 0,
topic D1 of the First Real Return Slice milestone. Owner directed D1 solo.

- **Builder:** incumbent, High tier, independent context.
- **Working location:** `docs/prototypes/real-data-residency/it1/`; foreman holds git custody.
- **Evidence:** Rung 2 — paper classification-rule/enforcement diffs, plus **throwaway probes** in a scratch directory **outside** the repository (a synthetic out-of-repo workspace and synthetic leak attempts). No repository modifications beyond the two outputs; no git write commands.
- **Questions:** D1-P1 (residency location rule + deterministic classification rule + enforcement surface on **commit and push**) and D1-P2 (synthetic-derivation rule).

## Current enforcement (binding context — extend, do not assume complete)

The only enforcement that exists today is one test,
`tests/test_kernel_fixtures.py::test_committed_kernel_fixtures_have_no_absolute_local_paths`:
it scans **one directory** (`packages/sample_data/kernel`) for a handful of path
markers (`/Users/`, `/private/`, `local-data/`, `uploads/`). There are **no git
hooks** and **no push-surface guard** of any kind. Treat this as the narrow floor
you must widen — not as a model to copy. ADR-0030 §C.8 (ratified) requires the
boundary to hold on the **push/publication** surface, and the interim
private-remote posture must never be load-bearing. The milestone plan's "Data
safety" section enumerates the surfaces real values must never reach.

## Assignment

Design both propositions against the committed contracts at `HEAD`:

1. **D1-P1.** (a) The **location rule** for live workspaces: a declared
   out-of-repo residency, stated as a *rule* (not a concrete path — the owner
   picks bytes at bootstrap), and why a run may read it while the repo cannot
   contain it. (b) A **deterministic data-classification rule** partitioning
   *every* artifact class into may-cross (code, contracts, synthetic fixtures)
   vs never-crosses (anything personal); an artifact the rule cannot decide is a
   boundary hole. (c) An **enforcement surface** that rejects a never-crosses
   artifact at *every* crossing point, covering both the **commit** surface and
   the **push** surface (ADR-0030 §C.8), expressed as versioned diffs to the
   classification rule and the scan's surface list. (d) A **complete kill-test
   enumeration**: every surface where data could cross — commit, push, test
   fixture, golden, charter, review, process log, retrospective, scratch dir,
   run output/ledger — each paired with its enforcement point or an explicit
   no-carry argument. Omitting a surface is a decision-blocking gap.

2. **D1-P2.** The **synthetic-derivation rule**: how a real document's *shape*
   (fields, cardinality, closure structure) becomes an in-repo synthetic fixture
   that provably carries **no real value**. A checkable re-expression, not an
   ad-hoc scrub; show that no real value survives into a committed fixture.

## Required cases

The plan's six Gate-2 cases: (1) clean boundary; (2) leak attempt — commit
surface rejected; (3) leak attempt — **push** surface rejected (must be distinct
from case 2); (4) synthetic derivation carries shape not value; (5) classification
ambiguity negative — the rule must decide a borderline artifact; (6) **kill-test
enumeration** (mandatory, decision-blocking). For each: claim →
classification-rule/enforcement change → scan/gate behavior → observed
reject/accept. Cases 3 and 6 are mandatory and must be *probed*, not asserted.

## Outputs

- `docs/prototypes/real-data-residency/it1/design.md`
- `docs/prototypes/real-data-residency/examination-it1.md` (≤120 lines) stating
  D1-P1 and D1-P2 separately as settled-at-Rung-2 or unresolved, citing every case.

Read: the topic `plan.md`, this charter, `docs/governance/`, ADR-0030 (esp. the
§C.8 amendment), the First Real Return Slice milestone plan's Data-safety section,
and `tests/test_kernel_fixtures.py`. Before writing, echo scope, the Rung-2 /
outside-repo boundary, and stop conditions.

## Stop conditions

Stop at the two static files. No enforcement code committed, no scan edits in the
repo, no git writes. If a design needs a contract change you cannot represent as a
versioned classification-rule/scan diff on paper, stop and report rather than
improvising. Every value, payer, path, and identifier in your outputs is synthetic.
