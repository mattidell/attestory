# Round 3 Governance Review — Source Completeness

Date: 2026-07-12  
Seat: governance fidelity  
Evidence rung: 3 — resolver plus throwaway two-layer evaluator

## Result

**Dissent: repair3 does not close the construction boundary under the round's
failure definition.** Its new wrapper entry points validate a carrier correctly,
but the imported copied evaluator remains an accepted alternate entry point and
publishes a zero from a caller-fabricated carrier. This is the same authority
defect, now bypassing the wrapper rather than its validator.

## Measurements

1. **ADR-0011 decision 5 — pass for the wrapper path; fail for the claimed
   complete boundary.** `authorize()` calls `resolve_A()`, whose sole admission
   site selects exactly one current finding with `value is True`; false, absent,
   displaced, truthy, and ambiguous cases block through `run_rule_authorized()`.
   `test_authority.py` exercises all six negatives. But a fabricated carrier
   reaches publication through the still-imported copied evaluator (below), so
   the iteration cannot establish that closure membership is admitted *only*
   through current-true resolution. **Exhibits:** `repair1/resolver.py:65-122,
   185-208`; `repair3/test_authority.py:68-84`.

2. **Caller-supplied `closed_sets` — pass, with a material alternate authority
   writer.** None of the repair3 wrapper signatures accepts `closed_sets`, and
   repair2 `Env` has only `sources` and `resolved`. The rejected construction
   path is not a bare set; it is a fabricated `AuthorizedMembership`, which is
   equally sufficient to make `E.Env(...).closed_families` contain the family.
   ADR-0011 expressly does not approve any caller-supplied replacement for
   `closed_sets`. **Exhibits:** `repair2/prototype_eval.py:54-65`;
   `repair3/authorized_eval.py:103-117`.

3. **One-authority-per-family and exact pins — wrapper pass; alternate-entry
   fail.** `validate_membership()` checks carrier provenance, duplicate families,
   and exact set equality with a fresh shape-A resolution. Genuine empty-source
   zero pins `clo-true@v5`; stale-first histories pin `new-true`; fabricated,
   duplicate, and mapping-mismatched wrapper carriers reject. **Exhibits:**
   `repair3/authorized_eval.py:77-100`; `repair3/test_authority.py:57-134`.
   Independent reproduction nevertheless called
   `A.E.run_rule(RULE, A.E.Env({}, authored(FAM, "fake-direct")))`: it returned
   `0` with `closure-authority fake-direct@v1` and mapping pin
   `map.demo.v1@v1`. This bypasses `validate_membership()` because
   `prototype_eval.run_rule()` accepts `Env` directly. **Exhibits:**
   `repair2/prototype_eval.py:121-130`; `repair3/authorized_eval.py:120-124`.

4. **Article 1 / SC-P2 identity — not exercised, correctly out of scope.** No
   SC-P2 identity key or multi-account/same-payer fixture is introduced; thus
   this pass neither proves nor regresses the Article 1 requirement. **Exhibit:**
   `charter-repair3.md` Scope excludes SC-P2 and SC-P3.

5. **Articles 9/10 — production condition, not established by this prototype.**
   `AuthorizedMembership` is a prototype dataclass rather than a declared,
   versioned citizen/schema with instance validation. The charter explicitly
   excludes schemas and persistence, so this is not scope creep, but it cannot
   be carried as production conformance. **Exhibits:**
   `charter-repair3.md` Scope/Stop conditions; `authorized_eval.py:51-57`.

6. **Article 11 — production condition.** The prototype declares mapping id and
   version and preserves them in authority, but mapping/closure/citation meaning
   is still executable Python (`resolve_A`, `validate_membership`, and pin
   building), not declared versioned content. Its prototype-only status is
   explicit; production must express this meaning in adopted artifacts rather
   than runner behavior. **Exhibits:** `repair1/resolver.py:170-208`;
   `repair2/prototype_eval.py:97-117`; `charter-repair3.md`.

7. **Scope — pass.** Repair3 is shape A only, does not restore shape B, and adds
   no SC-P2, SC-P3, SC-D1, schema, persistence, or production edits. This is a
   bounded rung-3 construction check authorized by the plan. **Exhibits:**
   `charter-repair3.md`; `plan.md` Gates 3 and 6; `round-2-triage.md`.

## Verification

- `python3 -m unittest -v test_resolver.py` — 15 passed.
- `python3 -m unittest -v test_end_to_end.py` — 11 passed.
- `python3 -m unittest -v test_authority.py` — 11 passed.
- Direct alternate-entry reproduction above — fabricated authority published;
  this is not covered by the passing repair3 suite.

## Recommendation

Do not make the repair3 sufficiency call. The foreman should classify the
alternate accepted evaluator entry as the still-open decision-blocking
construction-boundary finding; this review does not enlarge scope or prescribe
the next repair.
