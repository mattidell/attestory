# Clean-room review R1: Standing Authorization Successor (Seam 4b)

Reviewer read cold: `plan.md`, `charter-it1.md`, `charter-it2.md`,
`examination-it1.md` (on `it1`), and `examination-it2.md` (copied out of
`it2`, that branch not checked out). Independently traced cited code
(`packages/kernel/horizons.py`, `packages/kernel/findings.py`,
`packages/kernel/currency.py`, `packages/derivation/production_resolver.py`,
`packages/derivation/marshal.py`, `packages/derivation/source_authority.py`,
`packages/derivation/package_validation.py`). No commit messages, process
logs, or the Seam 4 spike were read for either verdict.

## it1 — legibility verdict: MET

**(a) Shape/identity.** Fully recoverable. New entity kind
`authorization.standing-workspace`, chain-keyed like `horizons.py`'s
`(family, version, scope)` on `(workspace_id, taxpayer_id, tax_year,
package_boundary_id)`, with a trailing `#gN` grant-sequence suffix so
re-grant after withdrawal doesn't collide. The worked JSON example and the
`resolve_standing_authorization` sketch reconstruct the shape unaided.

**(b) Six cases.** All six worked with named inputs/outputs and a distinct
disposition code per failure mode (`authorization_scope_mismatch:taxpayer`/
`:tax_year`, `authorization_suspended`, `authorization_withdrawn`,
`authorization_boundary_superseded`, `not_authorized`). Case 4 (ordinary
additions/removals) is an absence-of-wiring claim checkable directly against
`findings.py`'s dispatch table — confirmed: `member-transition`'s applier
touches only `findings`, `withdrawn_fact_ids`, `fact_state.entities`.

**(c) Grounded vs asserted.** All load-bearing citations check out:
`chain_key`/`current_by_chain` in `horizons.py`; `KERNEL_ACT_KINDS`/
`_APPLIERS` dispatch in `findings.py`; `marshal_closure_authority` and
`resolve_closure_admissions` exist exactly where cited. Each case states an
explicit rung disposition (settled-at-paper vs needs-rung-2), e.g. case 2:
"needs-rung-2 to confirm the diagnostic lookup stays cheap against a real
chain index." Honest about what paper evidence can and cannot prove.

**(d) SA-P2 stance.** A mechanical rule: `package_boundary_id` is a content
hash over declarations **"reachable from the specific rule(s) the
authorized calculation actually composes"** — the composition's dependency
closure, not the whole adopted package. Names its own open question:
whether the adopted-content graph already exposes that closure cheaply, or
whether this successor must build it. Legible, falsifiable.

No legibility defects found.

## it2 — legibility verdict: MET

**(a) Shape/identity.** Recoverable, though it takes closer reading than
it1's worked JSON: `workspace-calculation-authorization.v1`, a "thing-flavor
permission citizen" explicitly distinguished from a finding, an Ontology
Grant, and package-adoption, keyed on `(workspace, subject_id, tax_year)`
for currentness, with `universe_id` carried on the citizen but not part of
the identity key. Grant/end are two act kinds
(`calculation-authorization`, `calculation-authorization-end`), the second
overloaded with a `suspend`/`withdraw` mode rather than it1's four distinct
kinds. The identity key must be assembled from prose across two sections
rather than read off one literal.

**(b) Six cases.** All six worked, each with a named code
(`AUTHORIZATION_TAXPAYER_MISMATCH`, `_YEAR_MISMATCH`, `_SUSPENDED`/
`_WITHDRAWN`, `_UNIVERSE_SUPERSEDED`, `_STALE`, `_ABSENT`) — one more
distinct code than it1 (`_STALE`, for a run naming a specific non-current
authorization id). Case 4's structural argument is comparably strong:
"identity has no horizon key, so family-member individuation cannot
displace G1."

**(c) Grounded vs asserted.** Cited functions are real:
`select_current_adoption` (`production_resolver.py`), `compute_currency`,
`_member_withdrawals`, `_migration_supersessions` (`currency.py`), the
`act-package-adoption.v1` `supersedes` pattern (line 177 and the schema
file). The rung table is equally honest about paper's limits: "today's live
admission is Boolean horizon-keyed findings. Paper cannot prove the real
path consults this citizen and cannot fall through to `closed_sets`."

**(d) SA-P2 stance.** A checkable rule: `universe_id` is a SHA-256 digest
over sorted `families`/`fact_types` drawn from "the currently adopted
packages' fact surface ... whose year-scope includes the authorization
year." Flags its own residual uncertainty: "The six Gate-2 cases do not
include a package-expansion fixture, so this rule is a stated stance, not
forced unique by those cases" — see convergence analysis for what that
costs.

No legibility defects found; shape assembly costs one notch more effort
than it1's, but the document does not hide or assert past that effort.

## Convergence analysis: is it genuine?

Surface convergence is real: both propose an uncoupled citizen (never
touched by `member-transition`/`assertion`/horizon appliers), an explicit
end act distinct from absence, taxpayer/year scope-mismatch as classified
(not generic) refusals, and a content-digest re-authorization boundary. Both
independently derived that per-family closure cannot carry taxpayer/year
identity, without reading each other or the Seam 4 spike.

**But the two digests are not the same mechanism, and the difference is
material.** it1's `package_boundary_id` is scoped to declarations
"reachable from the specific rule(s) the authorized calculation actually
composes" — a per-composition dependency closure. it2's `universe_id` is
scoped to "the currently adopted packages' fact surface ... whose
year-scope includes the authorization year." Traced against real code:
`package_validation.py`'s `fact_surface` (built in `validate_package`,
~line 804) accumulates **every** fact-type/source-family citizen the
package declares for that scope — not filtered to any one rule's
dependency closure. it2's own text confirms this reading: the forcing
condition is a source fact type/family "entering or leaving **that
surface**" (the whole adopted surface), not the composition this
authorization covers.

**Concrete test: a new tax rule is added to the adopted package that
introduces a wholly new source family/fact type this taxpayer's
acquisition/interest composition never references** (e.g., a new document
type for an unrelated credit).

- **it1 correctly does not force re-authorization**: the new rule/family is
  not reachable from the composition's dependency closure, so the hash is
  unchanged.
- **it2 incorrectly forces re-authorization**: the new source family enters
  the package/year fact surface, so `universe_id` changes and every existing
  authorization for that tax year — including ones that never touch the new
  family — flips to `AUTHORIZATION_UNIVERSE_SUPERSEDED` on the next run.

This is not charitable resolution of ambiguity: it2's text states the
boundary at the package/year fact surface, and its own limitations note
that Gate-2 never exercised a package-expansion fixture — this exact
scenario was never checked. When checked, it2's rule fails the stated goal
both designs claim to serve ("a new bundle, family, or rule the composition
does not reference ... does not change the hash," it1's phrasing) without
it2 noticing the tension.

**Conclusion:** convergence is genuine at the level of citizen shape,
end-act design, and classified-refusal codes, but not at the re-
authorization boundary rule. it1's SA-P2 answer satisfies the plan's own
framing ("which changes alter the meaning of the calculation universe
itself"); it2's answer, as specified, over-catches by keying the boundary
to the whole adopted-package fact surface rather than the referenced
dependency closure of the specific composition an authorization covers.
Decision-blocking for SA-P2 if it2's rule is adopted as written — not a
legibility defect in either document; both state their rule precisely
enough that this difference is checkable mechanically, which is how this
review found it.
