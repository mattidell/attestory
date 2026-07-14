# Role: Adversary Reviewer — Non-Publication Explanations, Round 3 (ADR-0020 redraft)

Medium tier. Owner-launched external context. Subject: the redrafted
`docs/adr/0020-non-publication-explanation-walking.md` (durable Run Disposition
Ledger).

**Read:** the redrafted ADR-0020, the topic's `plan.md`, both designs and
examinations, all round-1/round-2 reviews and triages, `docs/governance/`,
ADRs 0002, 0004, 0006–0012, 0016, 0017, and committed `packages/derivation/`
source at `HEAD`. You may run read-only probes against the committed runner
and records in a scratch directory outside the repository.

**Do not read** the other round-3 review (within-round independence).

**Assignment.** Attack the redraft as a contract, not a design sketch: (1)
decision 1's single-surface fold — construct a run where the folded ledger and
the current `derivation-record.v1` surfaces would disagree, and check the fold
is actually specifiable without breaking existing record consumers; (2)
decision 4's `no_disposition_recorded` branch — interrupted-run recovery,
partially-written ledgers, and walks racing a run; (3) decision 5's
"expanded at most once" — is the entry-guarantee wording implementable, or
does it still permit the NPE-A9 double-expansion; (4) decision 6's currency
declaration — construct the stalest walk a consumer could be misled by and
check the payload makes the staleness detectable; (5) decision 3's multi-rule
nodes against declared conflict semantics; (6) any decision whose wording an
implementer could satisfy while violating its intent. State each attack
concretely. Classify every finding; do not redraft the ADR.

**Output:** `reviews/round-3-adversary.md`, findings labeled NPE-A12 onward,
verdict: ratification-ready / ready after listed corrections / not ready.
Advisory: the owner ratifies.
