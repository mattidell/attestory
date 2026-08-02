# Role: Governance Reviewer — Conditional Selectors, Round 2R (over it2)

Medium tier. Owner-launched external context. Reviews the clean-room rival's
iteration 2 (`it2/design.md`, `examination-it2.md`) under `charter-it2.md`.

**Exclusions — do not read:** the tainted rounds (`reviews/round-1-*.md`,
`round-1-triage.md`, `repair1/`, `charter-repair1.md`,
`examination-repair1.md`, `reviews/round-2-adversary.md`,
`reviews/round-2-governance.md`, `round-2-triage.md`),
`evaluation-analysis.md`, `docs/adr/0019-*.md`, `docs/adr/0020-*.md`, the
other round-2R review, and the `wip/`/`archive/` branches.

**Read:** `plan.md`, `charter-it2.md`, the it2 files, the round-1R reviews and
`round-1r-triage.md` (prior-round evidence), `docs/governance/`, ADRs
0002–0012 and 0016–0017, and committed `packages/derivation/` and
`packages/kernel/` source at `HEAD`.

**Assignment.** Measure it2 against CS-P1/CS-P2 and the governance set:
logic/parameter separation, displacement and edge integrity (Article 7,
ADR-0010), no implicit runner-resident policy (Articles 9/11), and whether the
charter's hard requirements are met — especially whether the round-1R failure
modes (CS-G1R executability, CS-G2R hardcoding, CS-A3R exhaustiveness, CS-A4R
overwrite hazard) are actually resolved, evaded, or correctly declared
unresolvable. Rule on the examination's proposition verdicts: is CS-P2's
settlement sound, and is CS-P1's deliberate non-settlement (the optional-input
absence gap) the contractually correct conclusion? Assess the two surfaced
authority questions: genuine contract gaps or resolvable within existing
contracts, and which body should resolve each. Classify every finding; do not
repair the design.

**Output:** `reviews/round-2r-governance.md`, findings labeled CS-G8R onward,
ending with a verdict on it2: accept / conditionally accept (conditions
listed) / reject, and a recommendation on CS-P1 disposition. Advisory: the
owner decides.
