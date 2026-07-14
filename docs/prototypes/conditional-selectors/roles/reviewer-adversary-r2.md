# Role: Adversary Reviewer — Conditional Selectors, Round 2R (over it2)

Medium tier. Owner-launched external context. Attacks the clean-room rival's
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
`packages/kernel/` source at `HEAD`. You may re-run the committed evaluator
read-only on synthetic payloads in a scratch directory outside the repository
to verify or break the design's executability claims; no repository
modifications beyond your review file.

**Assignment.** Attack it2 with concrete counterexamples: reproduce or refute
its evaluator-execution claims for C1–C5 (numeric-string status comparison,
spouse scoping, bracket rows, threshold math at 10,000/11,000); probe the
five-filing-status cross-products for logic leaks; guard exclusivity and
fallback behavior; zero/negative income; the itemization override's
guard-inapplicable path and its downstream blocking; and stress the
examination's central negative claim — that no declared-content mechanism can
supply an honest optional default under current contracts. Try to construct
one (e.g. guard-on-absence patterns, staged rules, choice findings); if you
succeed, CS-P1's non-settlement is wrong and that is a major finding; if every
construction fails, say precisely which contract feature blocks each. State
each attack as input state → expected → observed/argued result. Classify every
finding; do not repair the design.

**Output:** `reviews/round-2r-adversary.md`, findings labeled CS-A10R onward,
ending with a verdict on it2: accept / conditionally accept (conditions
listed) / reject, and your ruling on the optional-input impossibility claim.
Advisory: the owner decides.
