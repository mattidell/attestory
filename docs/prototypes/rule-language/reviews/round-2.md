# Review Round 2 — Rival (it2) Artifacts, and the Comparison

Artifacts under review: the it2 rival design on branch `prototypes/rule-language/it2` (tip `623957c`), directory `rival-rule-language/`. Examination: `examination-it2.md` (on `main`). Charter: `charter-it1.md` v2 (the shared exam). The incumbent for comparison: tag `exhibits/rule-language/it1`.

Retrieval (branch and tag are not checked out on `main`):

```sh
git show prototypes/rule-language/it2:rival-rule-language/artifacts/rules.json
git show exhibits/rule-language/it1:prototype-rule-language-it1/artifacts/federal-1040-core-2025.package.json
```

This round is comparative. Prior-round materials (round-1 reviews, it1 exhibits, both examinations) are fair game for the unstarved seats — the independence rule forbids only *same-round* peer reviews. **Contract tightness is an explicit axis alongside legibility:** schema-declared expression grammar, package closure, output ownership, record linkage, year identity.

## Seats for this round

- **Governance** (`roles/reviewer-governance.md`): the six checks against it2; state per check whether it2 is tighter, looser, or equal to it1 (cite round-1-governance findings). Output: `round-2-governance.md`.
- **Expressiveness** (`roles/reviewer-expressiveness.md`): rerun it2's tests and evaluator from the branch (`python3 -m unittest discover -s rival-rule-language/tests -v`); reproduce or refute every examination claim; hard-class mechanisms compared to it1. Output: `round-2-expressiveness.md`.
- **Adversary** (`roles/reviewer-adversary.md`): re-run every round-1 successful attack against it2 — expression smuggling (attack 2), duplicate-output ordering (attack 4), year identity (attack 5), package closure (attack 6), record/act looseness (attack 7), optional-many-to-zero (attack 3 secondary) — plus new attacks earned by it2's own shapes (guarded clauses, closed packages, bracket_fold). Attack parity matters: same attacks, both designs, comparable outcomes. Output: `round-2-adversary.md`.
- **Legibility** (`roles/reviewer-legibility.md`): **starved seat — owner-launched only.** Scope below. Freshly launched; the round-1 legibility session must not be reused.

## Legibility scope

The legibility reviewer reads ONLY its role file, this section, and these artifact files (via `git show` as above; both examinations, the charter, and it1 materials are off-limits):

- `rival-rule-language/artifacts/package.json`
- `rival-rule-language/artifacts/rules.json`
- `rival-rule-language/artifacts/parameters.json`
- `rival-rule-language/schemas/prototype.schema.json`

Owner launch line for this round (paste as the FIRST message of a fresh session, ideally a different model family):

> You are the legibility reviewer for the rule-language prototype, round 2. Read ONLY: `docs/prototypes/rule-language/roles/reviewer-legibility.md`, then the "Legibility scope" section of `docs/prototypes/rule-language/reviews/round-2.md`, then only the artifact files that section lists (via the git show command it gives). Do not read anything else in this repository. Write your recovery attempts to `docs/prototypes/rule-language/reviews/round-2-legibility.md`.

## After all four reviews

Foreman scores legibility recoveries (comparably to round 1), conformance-checks, logs, and presents the owner disposition: iterate further (a convergence it3 is a live option) or conclude to the evaluation analysis and ADR proposals.
