# Charter — Core Tax Conditions Milestone Remediation

Date: 2026-07-15. Chartered by the principal foreman on owner direction, following the retrospective pre-merge review (`2026-07-15-core-tax-conditions-premerge-review.md`). Branch: `milestone/core-tax-conditions` @ `95e574a` (reopened; `main` holds the premature merge pending owner decision).

## Premise

The development code is sound and kept. The milestone was closed prematurely with two ADR-0027 conditions undischarged (one decision-blocking) and without an independent review. Remediation discharges those conditions, adds an independent re-review, and re-closes honestly. **No re-doing of correct work.**

## Remediation items

### R1 — ADR-0027 decision 9: exclusive execution projection (closes PMR-1, decision-blocking)
Adopt-then-project so that derivation and rendering receive **only** the resolved member graph of the adopted package(s); co-located unpinned content is inert (not adopted, not executable, not renderable). Replace the Track-6 fixture composition helper with a real resolved-graph projection at the runner/render boundary.
- **Golden (required):** a package with a co-located unpinned rule/form-field for an adopted symbol → the unpinned content does **not** affect derivation or rendering after adoption (ACM-A1 case).
- Reuse the committed membership graph from Track 4; this is the projection/boundary, not new membership logic.

### R2 — ADR-0027 ACM-A5: member-citizen byte verification (closes PMR-2, production condition)
Extend published-byte verification from the package instance to every **resolved member citizen** (registry-verified content, not bare id/version string equality).
- **Golden:** a member whose bytes changed under an unchanged `(id, version)` → reject at adoption.

### R3 — Re-verification
`.venv/bin/python3 -m unittest`, `-m mypy`, `tools/governance_lint.py` all green after R1–R2, including the new goldens.

### R4 — Independent re-review (not foreman self-review)
An **owner-launched independent-context reviewer** examines the R1–R2 delta against ADR-0027 (d9, ACM-A1/A5) and confirms no new hole (e.g. the projection does not itself over- or under-include, per the ADR-0013-amendment discipline for fixes to findings). Verdict: ready / not ready.

### R5 — Honest re-close
On R4 "ready": update the milestone doc and roadmap to complete; **rewrite the milestone retrospective's Deviations** to include PMR-3–7 (the process violations the first retrospective omitted). Then the owner decides the `main` reconciliation (revert-and-re-merge, or hold-and-fast-forward) — the foreman does not rewrite `main`'s merge unprompted.

## Sequencing & authority
R1 → R2 → R3 → R4 → R5, owner-paced. Per the standing directive, **the owner authorizes execution and launches any seat**; the foreman prepares, integrates under custody, and does not proceed autonomously. Candidate: no new ADR (this implements accepted ADR-0027); if R1/R2 surface a genuine contract ambiguity, stop and charter a decision, do not improvise.
