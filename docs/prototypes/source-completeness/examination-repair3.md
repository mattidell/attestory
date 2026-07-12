# Examination: Repair Pass 3 — Shape-A Authority Construction Boundary

Date: 2026-07-12. Original it1 builder (deliberate continuity). Evidence level:
focused refinement over the repair1/repair2 throwaway code (no production import,
edit, or execution). Branch `prototypes/source-completeness/repair3`; artifacts
under `repair3/`. **Shape A only** — shape B stays rejected (rule-evolution
outage) and is not restored.

## Correspondence to the round-2 finding

`reviews/round-2-adversary.md` found that repair2 proved *sole use* of the
authority carrier but not *sole construction*: `ResolvedMembership` and
`ClosureAuthority` are public dataclasses and `Env` accepts any one, so a caller
fabricates authority (fake finding + mapping), publishes a zero, and pins the
fabrication; duplicate same-family authorities also slip through the carrier.
Frozen state prevents mutation, not construction. Round-2 recommendation: make
one-authority-per-family unforgeable **or validate the carrier at construction**.
This pass takes the validation route and states its limits honestly.

## What was built

- `repair3/authorized_eval.py` — `AuthorizedMembership` (carrier with mapping
  provenance, duck-compatible with repair2 `Env`); `authorize()` (sole sanctioned
  producer, runs shape-A `resolve_A`); **`validate_membership()`** (the boundary:
  re-derives from declared inputs and rejects any mismatch); three evaluator
  entry points — `run_rule_authorized` (no external carrier), `run_rule_with_carrier`
  (validates a presented carrier), `run_rule_trusting` (the unvalidated bypass
  mutant).
- `repair3/test_authority.py` — 11 cases.

Reuses the repair2 faithful two-layer `collect` unchanged; this pass adds only
the construction/validation layer in front of it.

## The guarantee, stated precisely (not overclaimed)

Python cannot make an object un-constructible, so this is **not** language-level
unforgeability. The contract is **re-derivation**: the evaluator trusts a carrier
only after `validate_membership` re-runs shape-A resolution over the declared,
pinned inputs (adopted mapping citizen + current closure findings) and confirms
the carrier equals that fresh output exactly — matching mapping provenance, one
authority per family, each retained pin being the current literal-true finding.
A fabricated, duplicate, stale, or mapping-mismatched carrier cannot equal fresh
resolver output over real inputs, so it is rejected before publication. The
production-shaped path (`run_rule_authorized`) takes no external carrier at all.

## Commands and results

```
$ cd docs/prototypes/source-completeness/repair3
$ python3 -m unittest -v test_authority
... 11 tests ... OK   (Ran 11 tests in 0.001s)
```

## Measured cases (shape A, through publication)

| Case | Result | Test |
|---|---|---|
| genuine true closure → zero + exact pin (`clo-true`@v5) | publish | `test_true_closure_publishes_zero_with_exact_pin` |
| present members → aggregate 34, no closure consult/pin | publish | `test_present_members_do_not_consult_or_pin_closure` |
| false / absent / displaced / truthy-int / truthy-str / ambiguous | **block** | `test_all_negatives_block` |
| bare family, nothing resolved | **block** | `test_bare_family_cannot_publish` |
| **fabricated** carrier (fake finding, empty real findings) | **reject** | `test_fabricated_authority_rejected` |
| genuine resolver-output carrier | publish | `test_genuine_carrier_accepted` |
| carrier mapping provenance mismatch | **reject** | `test_mapping_provenance_mismatch_rejected` |
| **duplicate** same-family authorities, either order | **reject** | `test_duplicate_same_family_rejected_either_order` |
| stale-first/current-second: pin is the successor; stale-pin carrier rejected | publish/​reject | `test_stale_first_current_second_cannot_select_stale_pin` |

## Negatives disclosed (every one)

- Six value/currency/ambiguity negatives block through publication (not just at
  resolver output), same as repair1/repair2, now under the authorized path.
- **Fabricated authority rejected**: a hand-built carrier claiming `totally-fake-finding`
  over empty real findings raises `AuthorityInvalid` — the round-2 attack, closed.
- **Provenance mismatch rejected**: a real carrier presented against a different
  declared mapping raises, so authority cannot be replayed under the wrong mapping.
- **Duplicate rejected regardless of ordering**: both `(a1,a2)` and `(a2,a1)` raise.
- **Stale pin unusable**: with a superseded true history in either order, the
  published pin is always the successor (`new-true`), and a carrier asserting the
  stale `old-true` pin is rejected.
- **Constructor-bypass mutant killed twice**: `run_rule_trusting` publishes both
  the fabricated and the duplicate carrier that the validated paths reject —
  the divergence is the kill (deliverable 4).

## Sufficiency call

**The shape-A construction/invariant boundary is closed at the executable level.**
The evaluator accepts completeness authority only through validated shape-A
resolution: fabricated and duplicate carriers are rejected before publication, a
stale pin can neither publish nor be selected, and a genuine empty-source zero
still pins exactly one current literal-true finding per family under the declared
mapping version. Combined with repair1 (admission) and repair2 (sole *use* on the
real two-layer path), SC-P1 shape A now has an executable enforcement chain
sufficient to draft the ADR against.

**Residual — production-only enforcement facts this boundary cannot model**
(not prototype gaps):

1. **System-wide sole entry.** The prototype proves the *authorized path*
   validates; it cannot prove production routes **every** run through it and
   retains no alternate `Environment`/`RunContext.closed_sets` constructor. That
   removal + a no-other-caller proof is milestone **Track 2**.
2. **Adopted-mapping identity.** `validate_membership` trusts the passed mapping
   citizen as "declared"; in production the mapping must itself be pinned by a
   real adoption act (Article 4) and the run must re-derive against the *adopted*
   version, not a caller-passed object. Adoption-surface work is **Track 2/3**.
3. **Persisted displacement.** Withdrawal of a closure finding displacing a
   published zero across a real run (ADR-0010 currency end-to-end) is rung-4 /
   **Track 3**, deliberately not modeled.

## Handoff

Construction/invariant question answered; stop condition reached (residuals name
production-only facts, none absorbed). SC-P2, SC-P3, SC-D1 remain deferred as the
triages left them; shape B stays rejected. Committed on `repair3` only — not
merged, tagged, or deleted. Integration, exhibit tagging, and the SC-P1 shape-A
ADR draft are the foreman/owner's.
