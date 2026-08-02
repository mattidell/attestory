# Prototype Plan: Conditional Multi-Dependency Non-Publication

Audience: Agents

Status: **approved — held** (owner, 2026-07-18). This topic is a D2
prerequisite. The owner also approved the first exact charter, but expressly
directed no dispatch. Every other role remains unauthorized until separately
released.

## Topic

When a declared condition activates several factual dependencies, a rule must
honestly non-publish with an explanation naming every currently absent member,
without demanding those dependencies while the condition is inactive. The
contract must keep the dependency set in declared artifacts, preserve ordinary
currency and pin discipline, and add no tax-specific runner branch.

The immediate D2 consumer is qualified-positive line 16, which requires two
declared-absence facts. This plan decides the generic substrate only; D2 will
consume it after its own decision concludes.

## Gate 0 — Decision inventory

The owner-authorized inventory is
decision-inventory.md in this directory. Its three propositions are the whole
topic:

| Id | Proposition |
|---|---|
| CMDN-P1 | An active declared condition can jointly require a declared set of factual dependencies and name every absent member in the non-publication disposition and explanation. |
| CMDN-P2 | Conditional dependency sets and their missing-member reporting are declared artifact semantics, not runner policy or post-processing. |
| CMDN-P3 | Later contribution or supersession of a member respects currency without a third standing-affecting edge and does not demand dependencies while the condition is inactive. |

Out of scope: arbitrary validation aggregation, form-level presentation,
optional defaults, multi-form orchestration, tax-specific conditions, D2's
worksheet arithmetic, the meaning of any declaration, and production code.

## Gate 1 — Eligibility

CMDN-P1, CMDN-P2, and CMDN-P3 each scored 8/8 in the approved inventory:
cross-cutting blast radius, migration cost, unresolved semantic shape after
paper examples, and inability to validate by a local D2 patch. The topic is
therefore prototype-eligible.

## Gate 2 — Paper evidence

Each clean-room builder must paper the following synthetic cases before code:

1. **Inactive positive:** condition false; every conditional member absent;
   the consumer publishes its unaffected result and names no conditional
   member as missing.
2. **Active positive:** condition true; all members present; the consumer
   publishes and pins the declared active dependencies.
3. **Active multi-absence negative:** condition true; two members absent; one
   blocked/non-publication disposition and its NPE walk name both factual
   members, in a declared and stable order or as an explicitly unordered set.
4. **Active partial-absence negative:** condition true; one member present
   and one absent; the same surface names only the absent member.
5. **Lifecycle trace:** inactive with no members → condition becomes active →
   both absent block → one contribution and re-run → one absent block → second
   contribution and re-run → publishes → supersede a member → published
   consumer loses currency under existing derivation edges.
6. **No reach-around:** a proposed rule cannot obtain its missing list from a
   tax-specific runner, UI, form, or hidden post-processing list.

Every design includes a producer → authority → consumer → failure map for all
three propositions. If paper distinguishes the contract shapes and cites a
representable declared mechanism, stop at paper. If it proves that a specific
committed evaluator/record surface cannot express the selected shape, record
that exact substrate gap before climbing one rung.

## Gate 3 — Evidence ladder

Authorized initially: **Rung 1**, static schema/content/paper instances only.
One Rung-2 throwaway evaluator/record mutation is permitted only if both
builders converge on a declared shape but cannot establish whether it can
produce a multi-member missing disposition through the committed record/NPE
contract. The probe must test only that one boundary; it is never production
code and never an end-to-end tax slice.

## Gate 4 — Cost caps

- One paper round: one High-tier incumbent and one High-tier sealed clean-room
  rival, each covering all six cases.
- Two owner-approved default reviewers, Medium tier: governance and adversary.
- At most one owner-approved repair pass, then a fresh confirmation reviewer
  only if a foreman-authored repair or a decision-blocking finding requires it.
- Builder and review documents have no length cap. Their stop conditions are
  the declared scope, six paper cases, proposition-by-proposition examination,
  evidence rung, and measurement charter; no topic Markdown target applies.

## Gate 5 — Triage

The foreman classifies every finding before another iteration:

| Finding type | Classification |
|---|---|
| A candidate silently names only the first absent member; a conditional member is demanded while inactive; missing-member semantics live in runner/UI code; or a lifecycle needs a third edge | decision-blocking |
| A selected declared shape needs a schema, evaluator, record, NPE, package, or coordinator change | production condition |
| A proposed mechanism fixes general validation aggregation, optional defaults, or form presentation beyond this topic | separate decision or deferred breadth |
| Ambiguous set ordering, wording, or fixture naming without semantic effect | non-blocking defect |

Only an owner-ratified amendment may enlarge scope. D2 does not reopen during
this topic; it consumes the selected substrate afterward.

## Gate 6 — Minimum converged subset

The topic may conclude only with one generic declared shape that:

1. conditionally requires a defined member set without inactive over-blocking;
2. reports all and only the currently absent factual members in a walkable
   non-publication disposition;
3. preserves declared-artifact meaning, complete pins on publication, and the
   existing two-edge currency model; and
4. separates named production conditions from claimed HEAD behavior.

It may partially ratify this substrate while deferring ordering/presentation
detail, but it may not ratify a D2-specific exception.

## Gate 7 — Production boundary

Only prototype documents merge from this topic. Accepted commitments become a
new Tier-2 or Tier-3 ADR as evidence warrants, with its plain-language
analysis. Production reimplementation is a prerequisite track before D2
adoption: schemas/records first, evaluator and explanation machinery second,
then coordinator-from-facts goldens. No prototype code becomes production
evidence by similarity.

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | High | Cross-cutting taxonomy, currency, and D2 boundary stewardship |
| Incumbent builder | High | Novel declared dependency/record/explanation shape |
| Clean-room rival | High | Same difficulty, independent alternative |
| Governance reviewer | Medium | Articles 7, 11, 12, and 15 conformance |
| Adversary reviewer | Medium | Inactive over-blocking, first-missing leakage, hidden runner policy, and currency attacks |
| Confirmation reviewer | Medium | Narrow post-repair measurement only if needed |

Every role requires the owner’s immediate, explicit approval of its exact
current charter before dispatch. This plan grants no standing launch authority.

## Review measurements

Governance measures whether each dependency set, condition, missing-member
outcome, record field, and explanation relation is schema/canon-declared;
whether published outputs pin members; and whether currency uses only existing
edge kinds. Adversary attacks all six paper cases, especially condition-false
with all members absent, two absent active members, a partial contribution,
and supersession after publication. Both reviewers must distinguish proposed
production conditions from HEAD behavior.

## Data safety

All examples, identifiers, values, and cases use synthetic demo labels. No
personal data, workspace detail, or real return result belongs in this topic.
