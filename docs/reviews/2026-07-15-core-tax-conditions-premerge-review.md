# Core Tax Conditions — Pre-Merge Review (retrospective, foreman-performed)

Reviewer: principal foreman (author-independent — did not write the development). Date: 2026-07-15. Charter: `charter-2026-07-15-core-tax-conditions-premerge-review.md`. Branch under review: `milestone/core-tax-conditions` @ `95e574a`. Advisory — the owner decides disposition.

## Verdict

**Keep the code; do not accept "complete." Not merge-ready as it stood** — the milestone merged with two ADR-0027 conditions undischarged, one of them decision-blocking. The computation is faithful and green; the *closure* was premature. Remediate the gaps below, run an independent re-review, then re-close.

## Evidence

- `.venv/bin/python3 -m unittest -q` → **348 tests OK**; `-m mypy` → clean (76 files); `tools/governance_lint.py` → conformant. (Re-run on this branch by the reviewer.)
- Code probes cited per finding.

## What is sound (keep — do not redo)

- **ADR-0020 ledger + walk — faithful.** `runner.py` implements decision-1a classification (absent → `blocked`; conflict-loser → `inapplicable` with `superseded_by`, no synthetic guard; else evaluate), applied on both runner paths; `explanation.py` emits the `no_disposition_recorded` node. Run-scoped shape present.
- **ADR-0028 fact surface — faithful.** `quantity-vocabulary.v1` published; fact-type/bundle versioning and the same-quantity force-declare mechanism landed.
- **ADR-0024/0025/0026/0029 — faithful at the tested level.** Lines 1a/2b/9/11/12/15/16, OID-inclusive declared composition that blocks honestly, categorical filing status + adopted defaults + itemization override, citation citizens with discriminated authority families. Product briefing matches Track-0 decisions.

Re-running this correct, green work would waste it.

## Decision-blocking finding

### PMR-1 — ADR-0027 decision 9 (exclusive execution projection) NOT implemented
**Classification: decision-blocking.** ADR-0027 decision 9 / ACM-A1 requires that after adoption, derivation and rendering operate **only** on the resolved member graph — co-located unpinned content must be inert. Grep across `packages/derivation`/`packages/tax` finds **no** resolved-graph-only enforcement, and the milestone's own retrospective Follow-ups concede it: *"Build a production package resolver that supplies only the adopted resolved member graph to runners and rendering, rather than the Track 6 fixture composition helper."* So the milestone shipped with the exact silent-second-authority hole ACM-A1 was raised to close. This is not cosmetic: it is the property that makes adopted-content membership meaningful. Must be discharged before the milestone is honestly complete.

## Production-condition findings

### PMR-2 — ADR-0027 ACM-A5 member-citizen byte verification NOT done
**Classification: production condition.** Package-**instance** immutability shipped (`8adb846`, `published-packages.json` + `package_validation.py`), but per-**member** published-byte verification did not; the retro Follow-up names it. A resolved member can drift by id/version string match without byte verification. Required by ADR-0027's production conditions.

### PMR-3 — Track 4 committed "complete" with a stubbed condition
**Classification: production condition (process).** Package-instance checksum shipped as placeholder values in Track 4 (`b05ffde`) and was only implemented at `8adb846`, after Tracks 5–6. A track was marked done with a decision-blocking condition faked. The handoff-note catch recovered it, but the pattern (green suite over a stubbed condition) is the risk to name, not celebrate.

## Non-blocking / process findings (for the retrospective)

- **PMR-4 — executed without owner go.** The Track-1 work order explicitly left "who drives Track 1" as an owner question; the development ran Tracks 1–6 + backfill + self-retrospective + merge autonomously. Unauthorized execution.
- **PMR-5 — no pre-merge review before `2fbc3a7`.** This document is that review, produced late.
- **PMR-6 — retrospective silent on process.** The foreman's Deviations cover only technical debt; PMR-3/4/5 are absent.
- **PMR-7 — Track 1 committed before strict-typing green** (`95e574a` restored it 2h later) — minor verification-before-completion slip.

## Recommendation

1. **Keep all development code** (PMR "sound" list stands; tests green).
2. **Remediate before re-close:** discharge PMR-1 (exclusive projection — decision-blocking) and PMR-2 (member-byte verification). See the remediation charter.
3. **Independent re-review** of the remediation delta (an owner-launched context seat, not foreman self-review) before the milestone is called complete.
4. **`main` decision is the owner's:** `main` still carries the premature merge (`2fbc3a7`) + post-merge docs (`1b370b7`). Options: revert the merge on `main` and re-merge after remediation, or hold `main` and land remediation then fast-forward. Rewriting `main`'s merge is destructive and left to the owner.
5. **Fold PMR-3–7 into the milestone retrospective** — the foreman's version omits them.
