# Round 2 Adversary Review — Source Completeness

Date: 2026-07-12
Seat: adversary, High tier / high effort
Evidence rung: 3 (resolver plus throwaway calculation path)

## Method and observations

I reran A1, A2, A6, and SC-P1 A7 with equal cases and assertions against
shape A (dedicated mapping citizen) and shape B (embedded adopted-rule
parameter). An attack resists only when the executable construction boundary,
not merely the intended resolver call, forecloses publication.

The supplied suites pass: repair1 15/15 and repair2 11/11. They kill the
declared presence-only, currency-blind, truthy, and caller-union mutants. A new
writer attack nevertheless found a shared untested constructor seam:
`ResolvedMembership` and `ClosureAuthority` are public dataclasses, and `Env`
accepts any `ResolvedMembership`. Frozen state prevents mutation after
construction, not unauthorized construction. These are prototype observations;
production API closure remains the already-routed production condition.

## Measurements: attack → outcome → exhibit

### A1 — false-closure / presence-value trap

- **Shape A: resists through its resolver and publication path.** False,
  absent, displaced true, truthy non-booleans, and ambiguous current findings
  all block. Its presence-only mutant publishes on false and is killed by the
  same end-to-end case. **Exhibit:** `repair1/resolver.py:70-122,185-208`;
  `repair2/test_end_to_end.py:78-101,167-175`.
- **Shape B: resists with equal evidence.** The same admission function is
  reached through the embedded parameter's literal-`True` guard; every negative
  blocks publication and the same mutant dies. **Exhibit:**
  `repair1/resolver.py:231-257`; `repair2/test_end_to_end.py:78-101,167-175`.

### A2 — caller-set smuggle / new authority writer

- **Shape A: attack succeeds after the resolver boundary.** A caller can build
  `ClosureAuthority(FAM,"caller-fake",...)`, wrap it in
  `ResolvedMembership`, and pass it to `Env`; empty input publishes zero and
  pins the fabricated finding and mapping although no closure finding or
  adopted mapping was resolved. **Exhibit:** public constructors at
  `repair1/resolver.py:129-156`; unchecked `Env.resolved` consumption at
  `repair2/prototype_eval.py:54-65,88-102` (adversary reproduction: value `0`,
  pins `caller-fake`/`caller-map`).
- **Shape B: attack succeeds identically.** Substituting artifact role
  `adopted-rule` fabricates B authority without any rule, adoption, or finding.
  The evaluator cannot distinguish this from `resolve_B` output. **Exhibit:**
  same constructor and consumer paths. The existing tests reject a
  `closed_sets=` keyword and a bare string, but never construct the accepted
  carrier (`test_end_to_end.py:141-152`).

### A6 — stale-pin / ambiguity overwrite

- **Shape A: resolver-originated authority resists.** Duplicate mapping entries
  and duplicate current findings block; re-attested true pins the new id and
  version. **Exhibit:** `resolver.py:187-208`;
  `test_end_to_end.py:104-130`.
- **Shape B: resolver-originated authority resists.** Duplicate adopted rules,
  duplicate findings, and displaced pins block or select the exact current
  finding as declared. **Exhibit:** `resolver.py:235-249`;
  `test_end_to_end.py:104-122,132-138`.
- **Both shapes: attack succeeds through the shared carrier seam.** Constructing
  one `ResolvedMembership` with two authorities for the same family admits the
  family, while `pin_for` silently returns the first. My reproduction ordered
  `stale/v1` before `current/v2`; zero published with the stale pin. **Exhibit:**
  `resolver.py:146-156`; `prototype_eval.py:97-117`. Thus ambiguity blocking is
  a resolver property, not an invariant of the object the evaluator trusts.

### A7 (SC-P1) — mapping evolution divergence

- **Shape A: resists the next-year/new-member attack at this rung.** Authority
  is independently mapped; a new collecting rule or member does not duplicate
  the family authority, and a new family/year is one mapping entry/version.
  No fact rekeying is introduced by SC-P1. **Exhibit:**
  `it1/sc-p1-mapping-design.md`, mapping instances; `resolver.py:170-208`.
- **Shape B: attack succeeds as an evolution outage/tradeoff.** Adding a second
  adopted collecting rule for the same family—even with the same closure
  parameter—makes the family count two and blocks *both* projections. The
  supplied “duplicate rule” test demonstrates exactly this result. A new box or
  calculation rule therefore requires rewriting/re-adopting the existing rule,
  splitting the family, or changing the divergence guard; shape A needs none of
  those. **Exhibit:** `resolver.py:231-243`;
  `test_end_to_end.py:132-138`; `it2/design.md`, embedded parameter tradeoff.

## Dissent and recommendation

I dissent from `examination-repair2.md`'s claim that resolved authority is the
sole possible writer “by construction.” The tests establish sole use of the
carrier, but the carrier itself is caller-constructible and accepts duplicate
authority. A2 and A6 therefore remain reproducible at the prototype boundary
for both shapes; this is not evidence that false/absent findings pass either
resolver.

Recommend the foreman classify the constructor invariant under the existing
production condition: production must make resolver provenance and one
authority per family unforgeable or validate the carrier at `Env` construction.
Preserve shape B's same-family rule-evolution outage as selection evidence or a
production condition. Do not enlarge SC-P1 into schema, SC-P2, SC-P3, SC-D1,
or persisted integration work.
