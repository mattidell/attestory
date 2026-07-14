# Round 3 Triage — Non-Publication Explanations (ADR-0020 redraft)

Foreman, 2026-07-14. Advisory to the owner. Classifies every round-3 finding
against the redrafted `docs/adr/0020-non-publication-explanation-walking.md` as
committed. I checked each finding against the actual decision text and the
committed `packages/` code it cites; my classification is my own, not a relay of
the reviewers' severities.

## Verdict

**ADR-0020 is NOT ratification-ready.** Seven decision-blocking findings stand.
The Adversary's "not ready" is the correct disposition. Governance's "ready
after listed corrections" is not in conflict — its assignment was
decision↔finding fidelity and the ADR-0008 fold, which it passed; it did not
attack the walker/schema representation or the committed record consumers, which
is where the Adversary found the blocking defects. The findings are additive.

## Decision-blocking (must be resolved before ratification)

| Finding | Decision | Defect | Fix shape |
|---|---|---|---|
| **NPE-G9** | 1 | Ledger enum stated as `executed`/`guard_inapplicable`; committed `derivation-record.v1` schema and `runner.py` use `published`/`inapplicable`/`blocked`. | ADR-text: state the ledger enum as the committed record values. |
| **NPE-G10** | Prod. conditions | Repair of the self-contradictory `derivation-record.completed.json` fixture (same artifact `blocked` *and* `inapplicable`) is deferred, but round-2 classed it decision-blocking for any single-surface fold. | Land the fixture + schema fold **concurrently** with the ADR, not deferred. |
| **NPE-A12** | 1 | (a) Folding removes the top-level `blocked[]` surface, breaking `records.py::recover_interrupted` and its tests. (b) Inter-runner divergence: a conflict-loser is recorded `inapplicable` by the forward runner but swept `blocked`/empty-missing by the reference runner's `finalize_unreached()`, so the walk is non-portable. | (a) Spec consumer migration (or derive `blocked[]` as a read model). (b) **New sub-decision:** define the canonical disposition of an unselected conflict-loser and require both runners to record it identically. |
| **NPE-A13** | 4 | `no_disposition_recorded` is returned for a finding that is *published and present in the act log* when an interrupted run wrote an empty ledger — a false "no explanation" for a live value, violating Articles 8/15. | Amend decision 4: the walker consults the act log first; a published finding walks via the pin-lineage walker regardless of ledger; `no_disposition_recorded` applies only when a symbol is neither published nor in the ledger. |
| **NPE-A16** | 3 | Decision text says a node carries an *array* of publishing rules, but the adopted `npe-walk.v1` schema (it2) defines singular `artifact_id` and a singular `publisher_of` lookup. Text and adopted schema contradict. | Amend the `npe-walk.v1` schema diff to arrays (`rule_references[]`) and the walker lookup to resolve all producers under declared conflict semantics. |
| **NPE-A17** | 2 | Decision delegates published nodes to the existing pin walker "unchanged" *and* under a "shared" memoization table, but committed `explanation.py` passes `_seen` by value and has no shared cross-branch memo (round-2 NPE-A7). The two constraints cannot both hold. | Retract "unchanged"; explicitly authorize modifying `explanation.py` to accept the shared memo table. |
| **NPE-A18** | 1 | "one disposition row per **eligible** artifact" — "eligible" has a precise runner meaning that excludes unreached rules, making the ledger sparse and forcing the walker into static reconstruction (violating pure projection). | Reword to "one disposition row per rule and selector artifact in the adopted package"; reconcile with the ledger-totality production condition. |

## Production condition (implementation-time)

- **NPE-A14** (decision 5). The "expanded at most once, enforced at entry"
  guarantee tensions with the schema's "`shared` map is for diamonds only": naive
  entry-caching puts every node in `shared` and flattens the inline tree. This is
  a schema-semantics detail to pin down when the `npe-walk.v1` schema lands, not
  an architectural reversal — but it must be resolved there, not left open.

## Non-blocking

- **NPE-G11** (decision 1). `guard_result` required-when references
  `guard_inapplicable`; at the ledger level the term is `inapplicable`. Same root
  as NPE-G9; fix together.
- **NPE-A15** (decision 6). Passive staleness carries a revision but no delta, so
  a consumer can detect but not characterize staleness. Advisory; the currency
  declaration meets its stated intent (NPE-G8/A10).

## Recommendation

Commission a **round-4 redraft** of ADR-0020 folding the seven decision-blocking
findings and NPE-A14 into decision text (foreman custody, as the round-2→round-3
redraft was). Six of the eight are ADR-text / vocabulary / concurrent-schema
corrections; two are substantive and worth the owner's eye:

- **NPE-A13** (published-finding lineage vs sparse ledger) — the redraft's own
  "honesty" principle, applied to the published case, produced a falsehood. The
  fix (walk the act log first) is clear and strengthens the contract.
- **NPE-A12(b)** (conflict-loser canonical disposition) — the only genuinely
  *new* decision this round surfaced: what a runner records for a rule a
  competing runner never reached. Small and nameable, but a real choice.

Given those two are substantive rather than cosmetic, a **light round-4
confirmation review** of the redraft is advisable before ratification. Owner
paces both the redraft and whether to run the confirmation.
