# Role: Adversary Reviewer — Expression Language Extensions (Committee)

Medium tier. Owner-launched external context (2026-07-13). This is the committee
round over **two independent designs** of the same two propositions: the
incumbent (`it1/`) and the clean-room rival (`it2/`). Attack both. A construction
that breaks one design but not the other is your most valuable finding — it tells
the foreman which mechanism to carry forward.

**Independence exclusions — do not read:** the Governance reviewer's output
(`reviews/round-1-governance.md`), any draft or notes toward ADR-0025, and any
uncommitted working-tree changes under `packages/` or `tests/`. There is no
prior ELX review to exclude.

**Read:** the topic `plan.md`, `charter-it1.md`, `charter-it2.md`,
`it1/design.md`, `examination-it1.md`, `it2/design.md`, `examination-it2.md`,
`docs/governance/`, ratified ADRs 0002, 0004, 0006–0012, 0016, 0017, 0023, and
**0024 (accepted 2026-07-13)**, and committed `packages/derivation/` and
`packages/kernel/` source to ground attacks. The conditional-selectors
`evaluation-analysis.md` defines the three refuted workarounds; use it. Paper
attacks only; no python execution against the repo (throwaway scratch probes
outside the repo are allowed to check a claim).

**Assignment.** Against **each design**, mount concrete counterexamples:

- **The three refuted workarounds.** Try to show each design is secretly one of
  multi-publisher staging, closure-aggregation misuse, or an evaluation-order
  trick. Push hardest on the taxpayer's own age flag, where no false guard
  exists to short-circuit on.
- **Displacement ordering.** assert-after-run, assert-then-supersede,
  default-then-remove: does displacement re-fire correctly and only through the
  two existing edge kinds? Can you resurrect a superseded default, orphan a
  consumer, or make a default overwrite an asserted finding?
- **Pin-origin integrity.** Can a consumer end up unable to state whether its
  input came from a default or an assertion? Can the same fact carry both at
  once?
- **Categorical (ELX-P2).** `married_filing_jointly` matches / `single` does not
  with no decimal coercion; then break it: type-mismatch operands, enum-invalid
  assertions, a legacy numeric code meeting a label guard, deadlock or silent
  fallback on mismatch. Attack the ADR-0024 code→label migration for any window
  where a value is silently converted or dual-read.
- **Case-5 floor.** A non-optional absent input must still block exactly as
  today under both designs.

State each attack as input state → expected result → where each design fails or
survives. Classify every finding (decision-blocking / production condition /
non-blocking). Do not repair designs.

**Output:** `reviews/round-1-adversary.md`, findings labeled ELX-A1, ELX-A2, …,
each naming the design(s) it applies to, ending with a verdict **per proposition
per design**: accept / conditionally accept (conditions listed) / reject.
Advisory: the owner decides disposition.
