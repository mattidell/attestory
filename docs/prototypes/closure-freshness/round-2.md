# Committee Round 2 — Recorded-Horizon Reducer

Date: 2026-07-12. Medium/medium executable-evidence review.

Evidence: `exhibits/closure-freshness/repair1`, `charter-repair1.md`, paper
exhibits, round-1 reviews/triage, governance, ADR-0009/0010/0011/0014/0016.

- Governance: decide whether the recorded horizon citizen and atomic transition
  use legitimate individuation plus derivation, preserve attested closure, and
  avoid reserved T1/third-edge authority.
- Adversary: attempt missing/fabricated/future/replayed/mis-scoped/global
  successors, half transitions, correction misclassification, resurrection,
  rebuild divergence, cross-family contamination, derived closure, and injected
  staleness roots/flags.
- Expressiveness: independently run/reproduce every case, prefix rebuild check,
  mutation kill, and root/edge inventory before reading the examination.

Failure: malformed transition enters the log; incremental differs from rebuild;
old zero resurrects; wrong family is affected; reducer invents a root not backed
by recorded horizon succession; or any standing effect lacks a declared
individuation/derivation edge.

Outputs, no line caps:

- `docs/prototypes/closure-freshness/reviews/round-2-governance.md`
- `docs/prototypes/closure-freshness/reviews/round-2-adversary.md`
- `docs/prototypes/closure-freshness/reviews/round-2-expressiveness.md`

Reviewers work independently and recommend only; no production/governance
adoption is authorized by a passing review.
