# Charter: Track 3 — Production Resolver & Live Workspace Bootstrap — Pre-Merge Review

Date: 2026-07-18. Chartered under **owner authorization** in this session for one
author-independent pre-merge reviewer on **PR #13**
(`track/frrs-t3-resolver-bootstrap`). Milestone: First Real Return Slice; Track 3.
Owner-held merge (ADR-0030); owner-approved dispatch of this exact seat (ADR-0034).
**Do not merge.** Report the review verdict and findings only.

## Why this review exists

Track 3 implements ADR-0033 production package resolution, D1 live-workspace
bootstrap behind the ADR-0031 capability wall, and the ADR-0032 F1 evaluator
fence. Implementation landed as commit `66a3497` (plus docs tip `f2311fc`) on
`track/frrs-t3-resolver-bootstrap`, opened as PR #13. The implementation charter
requires an author-independent pre-merge review before the owner merges. This
charter is that review seat.

## Reviewer posture

- **Author-independent:** the reviewer must not be the implementer of `66a3497`
  and must not redesign ratified contracts (ADR-0031/0032/0033 or Track-1
  schemas). Measure the delta against the charter and the ADRs.
- **Advisory:** findings are classified; the owner decides disposition and merge.
- **One seat:** a single pre-merge reviewer; no rival committee, no follow-on
  seats without a fresh owner authorization.

## Scope (delta under review)

- Branch: `track/frrs-t3-resolver-bootstrap` (PR #13 vs `main`).
- Primary implementation commit: **`66a3497`**
  (`track: implement FRRS Track 3 resolver bootstrap`).
- Docs tip recording await-review state: **`f2311fc`** (in scope only as process
  state; not an implementation claim).
- Base: merge-base with `main` / post–Track-2 tip **`b8c90f7`** (Track 3 plan
  merge). Focus measurement on the implementer commit `b8c90f7..66a3497`.
- Implementation charter:
  `docs/reviews/charter-2026-07-18-frrs-t3-resolver-bootstrap.md`.
- Contracts: **ADR-0033** (primary), **ADR-0031** (live residency bootstrap /
  installed gates), **ADR-0032 F1** (raw evaluator closed as a live path).

## What to measure (falsifiable)

1. **Charter deliverables 1–7.** Release-rooted current-user adoption resolver;
   verify release bytes before registry authenticates supply; exclusive verified
   member graph or refuse; live workspace bootstrap at D1 residency location with
   installed gates active; raw evaluator closed as a live path (F1); named
   ADR-0027/0028 production conditions for Track 3 discharged and PC(T4) carried;
   synthetic kill/golden corpus **executed**, not asserted stubs.
2. **ADR-0033 faithfulness.** Sole-current-user adoption; supersession and unique
   max revision; zero candidates / tied max **refuse** with typed reasons; forged
   release / replaced registry / changed package-or-member bytes fail closed with
   **executed** kill-tests; hard gate: no graph/execution/rendering unless
   `validation.ok == True`; co-located unpinned files inert; order-independent.
3. **F1 / Track-2 carry (T2 pre-merge F1).** Production path cannot reach a
   hand-assembled `InputFinding` / public raw `run` / fixture `_context` as a live
   route — structural barrier preferred over policy flags.
4. **Scope fence.** No real personal data; no RG-1 core-package content repair
   (default Track 4); no W-2 closure mapping, live-run smoke harness, first real
   run, OCR, or UI; no edits to ratified ADRs or Track-1 schema citizens.
5. **Verification integrity (re-run and report):**
   - focused Track-3 suite `tests.test_frrs_t3_resolver_bootstrap`
   - full `python3 -m unittest`
   - `python3 -m mypy packages tools tests`
   - `python3 tools/governance_lint.py`
   - data-safety scan of the Track-3 delta (synthetic `demo.*` only)
6. **Process honesty.** Claims in phase-state / foreman-handoff match what the
   branch actually delivers.

## Output

Write **exactly one** durable review file:

`docs/reviews/2026-07-18-frrs-t3-resolver-bootstrap-premerge-review.md`

Required structure (match Track-2 pre-merge style):

1. Header: reviewer posture, date, branch, delta SHAs, charter + contract refs,
   advisory notice.
2. **Verdict** — explicit merge-ready / not merge-ready, with blocking count.
3. **Evidence** — commands re-run and results (counts, green/red).
4. **Deliverable-by-deliverable** (charter 1–7).
5. **Findings** — each classified as one of:
   - `blocking`
   - `scope defect`
   - `production condition` (name owning track if deferred)
   - `non-blocking`
   Each finding: description, file:line when possible, suggestion.
6. **Scope fence** assessment.
7. **Recommendation** to the owner (merge / hold / carry items). Do **not** merge.

## Constraints

- Do **not** modify implementation source, fixtures, tests, ADRs, or schemas.
- Do **not** merge the PR, push, or open/close GitHub review objects.
- Do **not** repair findings; only report them.
- Prefer independent structural probes (imports, signatures, call graph) over
  trusting test names alone when assessing F1 and hard-gate refusal.
- If verification is red, record the failure as evidence; do not "fix" the tree.
