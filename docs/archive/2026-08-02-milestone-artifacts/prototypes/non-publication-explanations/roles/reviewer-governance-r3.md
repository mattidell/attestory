# Role: Governance Reviewer — Non-Publication Explanations, Round 3 (ADR-0020 redraft)

Medium tier. Owner-launched external context. Subject: the redrafted
`docs/adr/0020-non-publication-explanation-walking.md` (durable Run Disposition
Ledger), which folds the round-2 triage's five decision-blocking repairs into
decision text.

**Read:** the redrafted ADR-0020, the topic's `plan.md`, both designs
(`it1/design.md`, `it2/design.md`) and examinations, all round-1/round-2
reviews and triages, the reopened `evaluation-analysis.md`, `docs/governance/`,
ADRs 0002, 0004, 0006–0012, 0016, 0017, and committed `packages/derivation/`
(especially `records.py`, `runner.py`, `explanation.py`) at `HEAD`.

**Do not read** the other round-3 review (within-round independence).

**Assignment.** Rule whether the redraft is ratification-ready: (1) does each
of the seven decisions faithfully implement its cited findings (NPE-A4, G6,
A5, A6, A7, A9, G8/A10, G3/G7) without reinterpreting them; (2) is the
single-surface ledger fold consistent with ADR-0008's record contract as
committed, and is the required `guard_result` change correctly scoped; (3) are
the production conditions genuinely production-deferrable rather than
decision-shaped; (4) do the Alternatives honestly represent the rejected
transient Execution Map and stub-act shapes; (5) any conflict with Articles
7/12/13 or the ADR-0012 disposition vocabulary. Classify every finding; do not
redraft the ADR.

**Output:** `reviews/round-3-governance.md`, findings labeled NPE-G9 onward,
verdict: ratification-ready / ready after listed corrections / not ready.
Advisory: the owner ratifies.
