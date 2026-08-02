# Role: Adversary Reviewer — Non-Publication Explanations, Round 4 (ADR-0020 confirmation)

Medium tier. Owner-launched external context. Subject: the round-4 redraft of
`docs/adr/0020-non-publication-explanation-walking.md`, which folds the round-3
triage's seven decision-blocking findings and NPE-A14 into decision text.

This is a **confirmation review, scoped to the changes**, not a fresh full
review — the durable-ledger shape (conclusions C1–C3 in `evaluation-analysis.md`)
is settled and out of scope. Attack only whether the round-4 corrections
actually close their findings without opening new loopholes. A single adversary
seat this round by design (the shape is not reopened); there is no sibling
round-4 review to exclude.

**Read:** the round-4 ADR-0020, `round-3-triage.md`, `reviews/round-3-adversary.md`
and `reviews/round-3-governance.md`, the topic `plan.md`, `it2/design.md` and its
examination, `docs/governance/`, ADRs 0006 (conflict semantics), 0007–0009, 0012,
and committed `packages/derivation/` (`records.py`, `runner.py`,
`reference_runner.py`, `explanation.py`) and the `derivation-record.v1` schema at
`HEAD`. You may run read-only probes in a scratch directory outside the repo.

**Assignment.** For each round-3 blocker, rule whether the round-4 text closes it
and introduces no new defect:

1. **NPE-G9/G11 (ledger vocabulary).** Does the vocabulary-layering section plus
   decisions 1 and 7 use the committed `derivation-record.v1` enum at the ledger
   level and ADR-0012 terms at the payload level, with a total, unambiguous
   mapping?
2. **NPE-A12a (fold / consumers).** Is `blocked[]` as a *derived compatibility
   read-model* actually consistent — can it ever disagree with the ledger rows it
   is derived from? Does any committed consumer read `blocked[]` in a way the
   derivation breaks?
3. **NPE-A12b (conflict-loser).** Attack decision 1a: construct a rule that is
   *both* a conflict-loser *and* has genuinely absent dependencies — is recording
   it `inapplicable` honest, or does it hide a real block? Do the two runners now
   provably agree for every conflict/scheduling case?
4. **NPE-A13 (act-log-first).** Does "walk the act log first" fully close the
   sparse-ledger lie? Construct a published finding whose pins reference a
   superseded or withdrawn input, and a walk during an active (open) run.
5. **NPE-A16 (multi-rule schema).** Do the decision-3 array and the `npe-walk.v1`
   schema now agree, and does the all-producers lookup stay well-defined?
6. **NPE-A17 (pin walker).** Is the "additive optional shared-table parameter,
   committed behavior preserved when absent" claim implementable, or does the
   shared table still force a behavior change on the single-branch path?
7. **NPE-A18 (ledger totality).** Does "per rule and selector artifact in the
   adopted package" plus decision 5 give the walker a total ledger with no
   static reconstruction?
8. **NPE-A14 (memoization).** Does the canonical-shared-store + inline-vs-
   reference-is-rendering resolution actually remove the entry-guarantee tension?

Classify every finding; do not redraft the ADR.

**Output:** `reviews/round-4-adversary.md`, findings labeled NPE-A19 onward,
verdict: ratification-ready / ready after listed corrections / not ready.
Advisory: the owner ratifies.
