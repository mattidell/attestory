# Review Round 1 — Iteration 1 Artifacts

Artifacts under review: the it1 primary design on branch `prototypes/rule-language/it1` (tip `362f8a3`), directory `prototype-rule-language-it1/`. Examination: `examination-it1.md` (on `main`). Charter: `charter-it1.md` v2.

Retrieval: the branch is not checked out on `main`. Read files with, e.g.:

```sh
git show prototypes/rule-language/it1:prototype-rule-language-it1/artifacts/federal-1040-core-2025.package.json
```

## Seats for this round

All four reviewer seats. Independence rule applies: no reading same-round peer reviews before submitting.

- **Governance** (`roles/reviewer-governance.md`): the six declared checks against the it1 schemas and artifact corpus. Output: `round-1-governance.md`.
- **Expressiveness** (`roles/reviewer-expressiveness.md`): rerun the evaluator from the branch; reproduce or refute every examination claim; the six declared checks. Output: `round-1-expressiveness.md`.
- **Adversary** (`roles/reviewer-adversary.md`): the five attack surfaces against real artifacts now, plus anything charter v2 still missed. Output: `round-1-adversary.md`.
- **Legibility** (`roles/reviewer-legibility.md`): **starved seat — owner-launched only.** Scope below.

## Legibility scope

The legibility reviewer reads ONLY its role file, this section, and these artifact files (via `git show` as above; the examination and charter are off-limits — they contain intended meanings):

- `prototype-rule-language-it1/artifacts/federal-1040-core-2025.package.json`
- `prototype-rule-language-it1/schemas/rule-artifact.v1.prototype-it1.schema.json`
- `prototype-rule-language-it1/schemas/parameter-declaration.v1.prototype-it1.schema.json`

Owner launch line for this round (paste as the FIRST message of a fresh session, ideally a different model family):

> You are the legibility reviewer for the rule-language prototype, round 1. Read ONLY: `docs/archive/2026-08-02-milestone-artifacts/prototypes/rule-language/roles/reviewer-legibility.md`, then the "Legibility scope" section of `docs/archive/2026-08-02-milestone-artifacts/prototypes/rule-language/reviews/round-1.md`, then only the artifact files that section lists (via the git show command it gives). Do not read anything else in this repository. Write your recovery attempts to `docs/archive/2026-08-02-milestone-artifacts/prototypes/rule-language/reviews/round-1-legibility.md`.

## After all four reviews

Foreman scores the legibility recoveries against intended meanings, conformance-checks all reviews, logs incidents, and presents the owner disposition: iterate it1 / proceed to the rival (it2) / conclude (rivals rule forbids concluding without a rival).
