# Adversarial Review — Round 1

Seat: adversary. Reviewed `examination-it1.md` (incumbent-informed) and
`examination-it2.md` (clean-room rival, fetched from
`prototypes/standing-authorization-successor/it2`). Cross-checked both
against real code: `packages/kernel/horizons.py`,
`packages/kernel/findings.py` (`_APPLIERS`, `KERNEL_ACT_KINDS`, `apply_act`),
`packages/derivation/source_authority.py`,
`packages/derivation/package_validation.py` (fact-surface compilation,
member-reachability BFS), and Seam 4's spike
(`docs/prototypes/standing-authorization-currentness/`). No
`clean-room-r1.md` exists yet, so the boundary counterexamples below are
constructed directly.

## Cases 1–3: exact match and mismatch classification

Both admission paths are strict tuple/key equality (`chain_key`/
`(subject_id, tax_year)` dict lookup) — no partial/prefix/default slippage
in either at paper. Both distinguish "wrong taxpayer"/"wrong year" from
generic absence via a second, non-admitting lookup: it1's
`_find_same_workspace_and_boundary`, it2's scan of current grants.

Attack: it1's classified-mismatch requires the near-match to also share
`package_boundary_id`. Since that boundary is computed per-composition
(SA-P2), two taxpayers running different calculations could compute
different boundaries even while both are "wrong taxpayer" cases; the
diagnostic then finds nothing and silently degrades to generic
`not_authorized` — the exact outcome it1 claims to avoid. it1 never names
this dependency. it2's mismatch scan keys only on `(subject_id, tax_year)`,
with no boundary co-requirement, so it lacks this fragility.
**Verdict: it2's case 2/3 handling is unconditionally robust; it1's is
correct only when boundaries happen to coincide — an unstated assumption.**

## Case 4: additions/removals never re-trigger validity

Both trace the real dispatch honestly. it1: `apply_member_transition`
touches only `findings`/`withdrawn_fact_ids`/`fact_state.entities`; no
payload names an authorization key. it2: the authorization fold does not
subscribe to `member-transition`/`assertion`, and identity has no horizon
key to displace. Both check out against `findings.py:834-867`.
**Verdict: both pass, on paper.**

## Case 5: does suspension/withdrawal need new kernel machinery?

it1 registers new act kinds into `findings.KERNEL_ACT_KINDS`/`_APPLIERS` —
real, honestly-named kernel-file edits, but they contradict the precedent
it1 itself could have used: `findings.py`'s own comment (846-851) shows
non-kernel kinds (the derivation family's `derived-publication`, confirmed
real in `packages/derivation/projection.py`) already ride the log via
`apply_act`'s compose-over pass-through, with zero kernel edits. it1 chose
the more invasive path without noting the cheaper one already exists in
production.

it2 explicitly takes the cheaper path — an out-of-kernel fold, same shape
as `derived-publication`/`projection.py` — and is honest that this is still
new code (fold, schemas, admission check), just not new kernel code.
**Verdict: it2's answer is architecturally cheaper and better precedented;
it1's is honest but more invasive than the codebase's own pattern requires.**

## Case 6: stale scope must stay inert

Both get the headline property right via a boundary/digest-keyed chain
(it1) or digest inequality plus `supersedes`-chain staleness (it2,
`AUTHORIZATION_STALE`).

Gap found only in it1: neither the citizen shape nor the six-case narrative
addresses **taxpayer-entity supersession**. it2 names it explicitly —
subject-entity supersession is a displacement root, the successor entity
does not inherit the grant, and `subject_id` is pinned to opaque
`entity.v1` identity. it1's `taxpayer_id` is never pinned to entity-identity
machinery; if the taxpayer entity is superseded, it1 has no stated answer
for whether the authorization silently keeps resolving on the unchanged
string — a candidate reintroduction of the exact "stale scope reused"
defect case 6 exists to rule out. Not a required case, but it2 covered it
and it1 did not.

## SA-P2 boundary rule: concrete counterexamples

**A — should NOT force re-auth (unrelated topic added).** A new 1099-DIV
box-2a bundle joins the package alongside the interest rule this
authorization actually covers. it1's boundary hash is scoped to
declarations "reachable from the specific rule(s) actually composed" — the
new bundle isn't in that closure, hash unchanged. **it1 gets this right**,
contingent on a closure computation that does not exist as-is:
`package_validation.py`'s only closure/BFS (`MEMBER_UNREACHABLE`, ~1494-1521)
is rooted at package entrypoints/form-fields for the *whole package*
(orphan detection), not "what does rule X depend on" — adjacent, not free.
it2's `universe_id` digests the **entire adopted package's** fact surface
(`package_validation.py`'s Q(P)) for the tax year, not the composed rule; the
new bundle's fact types enter that surface and change the digest, forcing
`AUTHORIZATION_UNIVERSE_SUPERSEDED` on a change the calculation never reads.
**it2 fails this counterexample**; its own text admits the rule is untested
("the six Gate-2 cases do not include a package-expansion fixture").

**B — SHOULD force re-auth (a depended-on rule is edited).** it1's hash set
includes "rule id+version," so a version bump inside the referenced closure
changes the hash — **correct in principle**, same rung-2 caveat as above.
it2's digest hashes only `families`/`fact_types` and its text states
plainly it does **not** cover "rules, parameters, quantity vocabulary" — a
rule edit never changes `universe_id`. But
`completeness-support-decision.md` names "the adopted calculation
vocabulary or package boundary" as in scope. **it2 fails this
counterexample, more seriously than A: it under-triggers on a case the
decision doc it implements explicitly puts in scope**, letting a stale
authorization admit a calculation whose rule content changed underneath it.

## Overall verdict

Neither design is decision-clean. it2 is architecturally cheaper and more
robust on cases 2/3/5, and closer to a real, already-computed artifact for
SA-P2 — but its SA-P2 stance is wrong in both directions: it over-triggers
on unrelated package growth and, more seriously, under-triggers on rule
edits the decision doc puts in scope. it1's SA-P2 stance is directionally
correct on both counterexamples but rests on a dependency-closure
computation that does not exist and is not a small extension of the
existing (differently-oriented) reachability BFS; it1 also carries an
unstated case 2/3 fragility and a silent gap on taxpayer-entity
supersession that it2 covers.

**Neither survives as a converged citizen shape.** SA-P2 is not settled by
either paper design — both need rung 2: it2 must be re-scoped to a
rule-specific closure (borrowing it1's framing) before its digest is
defensible; it1 must demonstrate that "reachable from the specific rule(s)
composed" is actually computable, since no such closure exists today. SA-P1's
identity/act-kind/fail-closed shape is closer to converged, preferring it2's
compose-over answer for case 5 and it2's unconditional mismatch
classification for cases 2/3. Recommend: do not select either design as-is;
carry it2's kernel-machinery and mismatch-classification answers plus it1's
SA-P2 scoping (rule-composition closure, not whole-package surface) into a
rung-2 prototype before ratifying an ADR.
