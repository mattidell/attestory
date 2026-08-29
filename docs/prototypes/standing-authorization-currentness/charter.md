# Charter: Standing Authorization and Currentness (Seam 4)

Date: 2026-08-28. Foreman-issued.

Route: `PROJECT_PLANNING.md` **Frontier Reduction and Direct-Build Routing**
— "the semantics are settled but one technical capability is uncertain" ->
one bounded spike at the cheapest evidence rung. No rival builder; the
milestone plan names this a focused implementation probe, not an
architectural contest.

- **Branch:** `prototypes/standing-authorization-currentness/it1`
- **Evidence rung:** 1 (static/paper), climbing to rung 2 only if the paper
  design cannot show fail-closed behavior against the real workspace
  authorization schema/consumer.
- **Builder seat:** `roles/builder.md`, Medium tier (medium effort) — this is
  implementation-shaped, not novel synthesis.

## Question

Can one standing workspace authorization supply calculation currentness
without becoming another taxpayer's or another year's authority?

**Constraint: this probe must not involve accrued-interest tax semantics.**
Test authorization currentness alone, independent of Seams 1–3/5.

## Required test cases

- correct taxpayer and year;
- wrong taxpayer;
- wrong year;
- ordinary additions and removals to the standing authorization;
- suspension or withdrawal of the authorization;
- no renewed per-family confirmation (i.e. currentness must not silently
  assume a stale confirmation is still good).

## Deliverables

- `examination.md` (≤ 200 lines): each test case traced against the real
  standing-authorization/workspace schema and its consumer(s); exact failure
  mode for each negative case (wrong taxpayer, wrong year, suspended,
  withdrawn); a stated conclusion on whether the existing mechanism already
  supplies currentness or needs an additive successor.
- If a genuinely second materially different currentness mechanism emerges
  during the probe, stop and report it as a decision-blocking finding rather
  than building it — that would upgrade this seam to a rival comparison,
  which needs a Gate 1 score first.

## Committee

Full three-seat committee (clean-room, adversarial, eligibility) reviews the
single build. The eligibility reviewer's job here is specifically to confirm
this seam was correctly routed as a spike rather than a full prototype.

## Constraints

- Work only on the charter branch and `docs/prototypes/standing-authorization-currentness/`.
- No accrued-interest tax content, rules, or fixtures.
- All fixture data synthetic.
