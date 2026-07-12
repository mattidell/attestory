# Round 2 Governance Review — Closure Freshness

Date: 2026-07-12. Seat: governance reviewer. Review performed against the
round-2 charter, the governance set, ADR-0009/0010/0011/0014/0016, and the
repair1 exhibit. No peer review was consulted.

## Recommendation

Advance the recorded-horizon shape as a conditional answer to CF-P1 and
CF-P2, but do not treat this review as production or governance adoption. The
reducer demonstrates that a horizon successor can be an ordinary
individuation root and that the resulting closure-finding-to-zero cascade uses
only the two existing Article 7 edges. It does not yet establish the complete
production citizen/act contract: actor attribution, schema/version identity,
revision/concurrency, family-declaration binding, and the authenticated
producer of a successor remain outside the reducer.

The main governance condition is therefore precise: a production contract may
use this shape only if the horizon is a declared citizen whose succession is
an effect of one complete recorded user act, not a caller-supplied freshness
assertion, derived authority, or reducer repair.

## CF-P1 — legitimate individuation

**Result: passes conditionally.** The contract gives the horizon a stable
family-declaration/scope identity and a distinct successor occurrence
(`repair1/contract.md:7-14`). The closure fact identity includes the horizon,
and the successor retains the family/scope pair while naming the current
predecessor (`repair1/contract.md:16-20,35-41`). This is a legitimate
individuation relation under the Ontology §7 and Article 7: the closure
question changes when the citizen that keys it changes. It is not a freshness
bit, a derived finding, or a second authority about closure.

The reducer's standing inventory is correspondingly coherent:

| Effect | Declared relation | Governance result |
| --- | --- | --- |
| A member-changing act makes the old horizon noncurrent | recorded predecessor horizon → successor horizon | Legitimate succession/individuation, provided the horizon is a real declared citizen and the act is authoritative. |
| The old horizon displaces closure findings keyed on it | horizon → closure finding | Legitimate individuation edge; the reducer materializes it at `reducer.py:160-165`. |
| A closure-backed zero leaves current state | closure finding → zero | Ordinary derivation edge from the zero's exact closure pin; `reducer.py:165-166`. |
| A same-member value correction leaves the family horizon unchanged | no horizon edge | Correct governance distinction: same question corrected, not family membership changed (`reducer.py:110-126`; `contract.md:28-33,49-51`). |
| Re-attestation and rerun publish a replacement zero | no new displacement edge | Lazy recomputation after a new asserted finding, consistent with Article 13 and ADR-0010 decision 6. |

The computed root set is the set of recorded superseded horizons
(`reducer.py:170-180`), not a comparison result, listener callback, or stored
staleness field. That fits Article 7's rule that displacement is a consequence
of the record and currency is derived, and E7.1/E7.2's prohibition on stored
currency and third edges.

The condition matters because the reducer accepts synthetic acts directly.
`_validate_horizon` checks novelty, pair preservation, and predecessor
continuity (`reducer.py:53-62`), but it cannot prove that an external producer
was authorized to create the new horizon. The examination expressly leaves
actor, presentation form, production schema, and integration unsettled
(`examination-repair1.md:50-54`). A production implementation must supply
those Article 1/2/4/6/9/10/14 obligations; otherwise “valid successor” would
be a caller-created standing root under a new label.

## CF-P2 — closure authority and the cascade

**Result: passes for the bounded model.** Closure remains user-attested:
`closure_attested` admits only literal `true`, while `derived_closure` is
rejected (`reducer.py:129-156`). The zero requires an asserted closure, the
closure's fact must still name the current horizon, and a current relevant
member blocks publication (`reducer.py:142-152`). This respects ADR-0011's
affirmative-only closure rule and its warning that closure is not derived or
presence-only authority. It also avoids the reserved T1 derived-finding
authority: the reducer displaces the asserted input closure and never creates
an authority-bearing derived closure, consistent with ADR-0009 and ADR-0010.

The executed proof is substantive. `python3 -m unittest test_reducer.py`
passes all five tests. The required scenario establishes F and G zeroes,
adds F member M1, performs a value correction, changes its predicate, adds
and removes M2, then re-attests and reruns (`test_reducer.py:18-33`). The
assertions show:

- after the first F successor, root `H0` displaces `K0` by individuation and
  `Z0` by derivation (`test_reducer.py:37-45`);
- the same-member value correction leaves currency unchanged
  (`test_reducer.py:45`);
- later transitions do not resurrect `Z0`, while the independent G zero stays
  current (`test_reducer.py:46-48`);
- only the new closure finding and explicit rerun produce current `Z4`
  (`examination-repair1.md:21-29`).

The replay assertion is also the right governance check for this question:
after every accepted act, incremental currency equals a full ordered replay
(`reducer.py:206-217`; `examination-repair1.md:13-19`). Rebuild is explicitly
not allowed to repair an invalid historical act (`contract.md:53-54`), which
protects Article 5/6 record integrity.

The negative checks cover the declared boundary rather than merely the happy
path. Missing successor is rejected (`test_reducer.py:50-54`); a malformed
successor leaves both horizon and member state unchanged, proving atomic
admission (`test_reducer.py:56-64`); future closure, mis-scoped successor,
wrong predecessor, derived closure, half removal, and global horizon are
rejected (`test_reducer.py:78-93`). The direct-root/staleness mutant is killed:
`currency` has no injected-root parameter and an unknown caller flag is
rejected (`test_reducer.py:66-76`). These results support E6.1, E7.1, and
E7.2 for the synthetic reducer.

## Source-family and closure-contract limits

The horizon must not weaken ADR-0016. A real family declaration remains the
semantic authority: exact claim plus canonical member predicate; shorthand,
labels, and rule symbols cannot broaden it (ADR-0016 decisions 1–4,
`docs/adr/0016-source-family-claim-and-composition.md:18-27`). The repair
contract names `family` and `scope`, but its reducer does not validate a
versioned declaration or predicate; `relevant` is only a synthetic boolean
(`reducer.py:88-126`). Therefore the evidence proves freshness mechanics for
an already-declared family/scope, not family semantic correctness.

Likewise, the reducer intentionally leaves mapping, declaration, rule,
adoption, run, and actor references as synthetic provenance
(`repair1/contract.md:16-20`). That is acceptable within this charter, but a
production closure-backed zero must still pin the exact adopted mapping and
current true closure finding under ADR-0014, while remaining limited to the
family claim under ADR-0016. The reducer cannot be cited as approval to remove
the ADR-0014 mapping gate, restore caller-supplied `closed_sets`, or authorize
a broader result.

## Governance disposition by question

| Question | Finding | Required follow-up |
| --- | --- | --- |
| Horizon as individuation | Supported for the bounded model; not a disguised third edge. | Define the horizon schema, identity, actor-bearing successor act, and family-declaration binding before production adoption. |
| Closure authority | Correctly remains affirmative user assertion; no T1 construction. | Preserve actor/basis/presentation and exact current-value validation in the adopted contract. |
| Atomic member change | Reducer validates the successor before mutating member state and kills the half-transition mutant. | Implement transaction/revision semantics and reject malformed acts at the workspace boundary. |
| Correction versus membership change | Value correction does not advance the horizon; predicate change/add/remove do. | Bind this classification to the declared member predicate and correction policy, not a generic boolean convention. |
| Currency/rebuild | Incremental and replay currency agree after every accepted synthetic act. | Repeat with production citizens and the complete act-log registry; rebuild must reject, never repair, invalid history. |
| Family isolation/no resurrection | F roots do not affect G; old roots remain displaced after later removal. | Preserve exact family declaration plus scope in all identity and edge extraction. |

## Final recommendation

Recommend the foreman mark CF-P1 and CF-P2 as evidenced conditionally at the
reducer rung, with no governance amendment and no production adoption. The
surviving design is governance-compatible because its standing effects are
fully accounted for by horizon individuation followed by the existing
closure-finding derivation edge. The unresolved items are production
conditions and contract work, not grounds to add a third edge, a stored
freshness flag, a manual withdrawal, or derived closure authority.
