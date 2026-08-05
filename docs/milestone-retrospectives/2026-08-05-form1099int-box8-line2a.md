# Retrospective — Form 1099-INT Box 8 Tax-Exempt Interest to Form 1040 Line 2a

## What differed from the plan

- Before publication the branch was rebased onto the ratified line after Form
  8949 (covered code-W wash-sale) merged. Core package **v19** was regenerated
  from the ratified **v18** predecessor so Form 8949 members and the box-8
  succession are both present (232 members). `artifact-package.v16` admits
  both `quantity-vocabulary.v7` and `v8`.

- Track 0 settled Alternative B (additive `rule.form1040-line2a` successor with
  exact dual-family claims) rather than a new tax-exempt composition schema.
  No new ADR was required.
- Path A / Path B completeness for `no-f1099int-tax-exempt` was implemented with
  a live-path declaration/signal contradiction so Path A plus a non-empty box-8
  member fails honestly, in addition to the box-9 companion-presence pair.
- Box-9 companion enforcement was installed on the live production path from the
  first implementation (the prior box-12 live-path omission was not repeated).
- Packaging used the owner-confirmed higher-version stack relative to the
  ratified predecessor: quantity-vocabulary.v8, artifact-package.v16,
  package.core-calculations.v19, published-packages.v14, demo.release.2025.v12,
  and adopt-core-v19. Predecessors remain byte-immutable.
- External publication review raised High/Medium/Low findings (box-9
  displacement pins, evidence honesty, stale packaging docs). A findings-only
  repair addressed them; companion pin edges now displace line 2a on box-9
  correction.
- Form 8949 wash-sale support merged to `main` before publication; this
  milestone rebased and unioned its package onto core v18 rather than racing
  for colliding v18/v13 filenames.

## Result

The engine has a bounded, production-shaped synthetic path for 2025 returns
that report nonnegative Form 1099-INT box-8 tax-exempt interest (box 9 absent
or zero), aggregated with the closed Form 1099-DIV box-12 family (or closed-
empty box-12) onto Form 1040 line 2a under a two-path Form 1099-INT
completeness gate. Line 2a remains reported-but-not-directly-taxable: it does
not enter line 9 or taxable-income arithmetic, and is not Schedule B Part I
taxable interest.

Path A preserves box-12-only returns via `no-f1099int-tax-exempt = yes`.
Path B admits closed box-8 with box-9 companions. Residual scope absences
(OID, unreported, premium, excluded consumers) remain unconditional.
Historical line-2a@v1 and box-12 package routes remain resolvable.

## Evidence and review disposition

- Plan and Track 0: `docs/phases/engine-breadth/milestones/form1099int-box8-line2a.md`.
- Publication review retained at
  `docs/reviews/2026-08-05-form1099int-box8-line2a-final-review.md`.
- First independent publication review returned **NOT READY** with High/Medium/Low
  findings: same-statement box-9 corrections did not displace line 2a (missing
  ADR-0010 companion pin edges), presentation evidence honesty gaps (P10–P12/N7),
  and stale packaging/base docs after the Form 8949 rebase. A findings-only
  repair wired companion authorities into collect sources and pin edges, hardened
  the evidence matrix, and corrected plan/retro packaging language.
- A repeat review confirmed the box-9 displacement repair but returned **NOT
  READY** again on two Medium findings (companion provenance could still fail
  open via swallowed loader errors / unmatched pins; presentation golden auto-
  create and N7 non-projector path) plus Low closeout-doc contradictions. A
  second findings-only repair made companion load and pin matching fail closed
  (with a shared box-13 regression), required the committed presentation golden
  with stronger section contract checks, drove N7 through the real projector
  path, and aligned this retrospective with the actual repair history.
- Focused suites cover the evidence matrix (Path A/B, companions, lifecycle,
  residual scope, reported-only, package exclusivity, presentation golden via
  `live_coordinate_run`) plus box-12, schema-registry, and companion fail-closed
  unit coverage. Governance and envelope scans were clean on the implementation
  range. CI on the curated PR head remains the merge gate.

## What it cost

- One paper-first Track 0, one integrated Builder, independent Reviewers, and two
  findings-only repair cycles after first publication review (no new ADR).
- No personal or real tax data entered the branch, fixtures, review, or output.

## Follow-ups

- Form 1099-OID tax-exempt stated interest / OID, unreported tax-exempt
  interest, premium adjustments, and nonzero box 9 / Form 6251 remain separate
  frontier rows.
- Form 8949 wash-sale support is already on `main` (merged before this
  publication); this branch rebased onto that line and carries core v19 as the
  additive union. No parallel packaging race remains for this milestone.
- Leave the next breadth milestone owner-unselected.

## Closeout lesson

Live-path install of companion and declaration/signal pairs should be in the
first production wiring checklist, not only in adversarial review — and
companion marshalling / pin matching must fail closed, not swallow drift.
Presentation evidence must require committed goldens and exercise the real
projector path; dictionary mutation is not proof. Cross-track package version
numbers remain unreserved until rebase against the ratified line at packaging
time.
