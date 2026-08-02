# Prototype Plan: Real-Data Residency Boundary (D1)

Audience: Agents

Status: **draft — proposed to owner** (principal foreman, 2026-07-16). Track 0,
topic D1 of the First Real Return Slice milestone (Real Return phase). Operates
under ADR-0030 per-ADR / per-track merges; owner may amend before builder launch.

Topic: **Where live tax data lives, and what may ever cross into the repository
or any remote.** D1 is the milestone's data-residency contract: a declared
out-of-repo location for live workspaces, a data-classification rule stating
what may enter the repo (nothing personal — code, contracts, synthetic fixtures
only), the mechanized enforcement surface that holds the line, and the rule by
which synthetic fixtures are derived from real document *shapes* without carrying
real values.

## Why this topic exists (and why it is Tier 3)

Foundation ran entirely on synthetic `demo-*` data; nothing defines where *real*
data may live or what stops it entering the record. This milestone crosses that
boundary, so D1 is the first decision where a mistake puts personal data
somewhere it cannot be recalled. **The failure mode is irreversible — a leak
cannot be unleaked** — which is why D1 is owner-directed (Tier 3) and why its
enforcement must be *demonstrated*, not asserted.

The surface widened under the ADR-0030 amendment (§C.8, ratified 2026-07-16): a
push is publication regardless of repo visibility, so live data must never be in
the repository **or on any remote**, and D1's kill-test list must include the
push surface. The private-remote posture is interim and must not be load-bearing.

D1 **interlocks with D2** (contribution writes real values into the residency
boundary): the two plans may share synthetic fixtures, but they ratify as
separate ADRs. **D3** (production resolver) follows D1 ratification — the
resolver must know where live content lives. This plan decides residency only.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing |
|---|---|---|
| D1-P1 | The **residency boundary**: the declared out-of-repo location for live workspaces; the **data-classification rule** partitioning every artifact into *may-cross* (code, contracts, synthetic fixtures) vs *never-crosses* (anything personal); and the **enforcement surface** that mechanically rejects a never-crosses artifact at every crossing point — extending the existing fixture-safety scan to the new boundary and to the **push/publication** surface (ADR-0030 §C.8). | Primary |
| D1-P2 | The **synthetic-derivation rule**: how a real document's *shape* becomes an in-repo synthetic fixture that provably carries no real value, so real-shaped test coverage can exist safely. A stated, checkable re-expression — not an ad-hoc scrub. | Dependent, same contract surface |

No contribution mechanics (D2), no resolver (D3), no new tax content, and no UI
enter this topic. The concrete filesystem path is an owner choice at bootstrap;
this plan decides the *rule* for the location, not the bytes of the path.

## Gate 1 — Eligibility

- Future blast radius: **3** — every later milestone that touches real data inherits this boundary; the failure mode is irreversible, so precedent set here is load-bearing for the life of the product.
- Migration cost: **2** — the location and classification rule are cheap to author now, but the boundary *shape* is precedent; content written against a weaker boundary later re-expresses across more surface.
- Residual paper uncertainty: **2** — the classification mechanism and the full enforcement-surface enumeration are undesigned; irreversibility raises the cost of a missed surface.
- Inability to test cheaply: **1** — a synthetic leak attempt against the scan and a scratch out-of-repo workspace verifies enforcement cheaply.

Total: **8**. Prototype-eligible.

## Gate 2 — Paper evidence

Each builder resolves these cases; all values, payers, paths, and identifiers
synthetic:

1. **Clean boundary.** A live workspace at the declared out-of-repo location; a run reads it and produces dispositions; the repo scan is green and the workspace is nowhere in the repo tree or index.
2. **Leak attempt — commit surface.** A never-crosses (personal-classified) artifact staged inside the repo tree → the scan **rejects** it. Must show *which* rule fired.
3. **Leak attempt — push surface.** A never-crosses artifact reachable from a push (staged on a unit branch) → the **pre-push** gate rejects it (ADR-0030 §C.8). Distinguishing this from case 2 is mandatory — a boundary that only guards commit is a decision-blocking gap.
4. **Synthetic derivation.** A real-shaped document → re-expressed as a synthetic fixture carrying the *shape* (fields, cardinality, closure structure) but no real value; show the re-expression rule and that no real value survives into the committed fixture.
5. **Negative — classification ambiguity.** A borderline artifact (e.g. a workspace path string embedded in a config, a contribution-provenance record) — the classification rule must **decide** it deterministically, not leave it ambiguous. An artifact the rule cannot classify is a boundary hole.
6. **Kill-test enumeration (mandatory).** The complete list of surfaces where data could cross — commit, push, test fixture, golden, charter, review, process log, retrospective, scratch directory, run output/ledger — each paired with its enforcement point, or an explicit argument that the surface cannot carry data. Omitting a surface is the failure this case exists to prevent.

For each design: the clean case, both leak attempts (commit + push), the
derivation, the ambiguity negative, and the kill-test enumeration; and for each
proposition, claim → classification-rule/enforcement change → scan/gate behavior
→ observed reject/accept. If paper makes the boundary clear, stop at paper.

## Gate 3 — Evidence depth per question

Authorized level: **Rung 2** — static examples plus throwaway probes against the
committed fixture-safety scan and a scratch out-of-repo workspace (read-only
w.r.t. the repo). Authorized above paper because the failure mode is
irreversible: every claimed *reject* on the commit and push surfaces must be
**probed** (actually run a synthetic leak attempt and observe the rejection), not
asserted. Contract changes are shown as versioned diffs to the classification
rule and the scan's surface list on paper. No production enforcement code is
written in the prototype — that is milestone Track 1/3.

## Gate 4 — Cost caps

- Two paper builders: incumbent plus **clean-room rival** (sealed from the
  incumbent), each producing all six cases and both propositions.
- No repair pass pre-authorized.
- Two Medium/High reviewers (Governance and Adversary), independent contexts.
- Charter ≤ 100 lines; examination ≤ 120 lines; total topic Markdown target
  ≤ 900 lines.

## Gate 5 — Triage

Foreman classifies every finding. Decision-blocking only: the classification
rule's completeness and determinism, the enforcement surface covering **both**
commit and push (D1-P1), the kill-test enumeration's completeness, and the
synthetic-derivation rule's integrity (D1-P2). Deferred: the exact scan
implementation bytes, the concrete filesystem path (owner picks at bootstrap),
and all D2 contribution mechanics.

## Gate 6 — Minimum converged subset

The floor is D1-P1: a deterministic classification rule plus an enforcement
surface that **provably rejects a synthetic personal-data leak on both the commit
and push surfaces**, backed by a complete kill-test enumeration. Without the push
surface (ADR-0030 §C.8) the subset does not converge.

## Gate 7 — Production boundary

Only documents merge. Accepted structures become a Tier-3 ADR (**candidate
number 0031**). The extended scan, the classification rule as an enforced
artifact, and live-workspace bootstrap land in the milestone's Tracks 1 and 3
afterward, discharging this ADR's named production conditions.

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium | Scope and conformance steward; owns triage and the evidence ladder |
| Incumbent builder | High | First design; classification rule, enforcement surface, kill-test enumeration, and derivation rule |
| Rival builder | High | Clean-room rival, sealed from the incumbent; all six cases, both propositions |
| Governance reviewer | Medium | Conformance to the milestone data-safety rules and ADR-0030 §C.8 (push-is-publication); classification determinism; kill-test completeness |
| Adversary reviewer | **High** | Leak-hunting is the crux and the failure is irreversible: construct a personal artifact that reaches the repo or a remote through a surface the boundary missed; break the derivation rule so a real value survives; find an unclassifiable artifact |

Reviewer seats are named here; owner approval of this plan is the standing
authorization for the foreman to dispatch them as sub-agents in independent
contexts (ADR-0013 reviewer-dispatch amendment), subject to the sub-agent
confirmation gate for any non-reviewer spawn.

## Review measurements

Governance: every artifact class is deterministically classified; enforcement
covers commit **and** push (ADR-0030 §C.8); the kill-test enumeration lists every
crossing surface with an enforcement point or a no-carry argument; the derivation
rule is checkable and leaves no real value in-repo; the interim private-remote
posture is nowhere load-bearing. Adversary: land a synthetic personal artifact in
the repo tree, the index, or a pushed branch through any surface not guarded;
defeat the derivation rule; and exhibit an artifact the classification rule
cannot decide.

## Data safety

This is the topic that defines data safety, so it is held to its own standard
from the first line: all values, payers, paths, and identifiers in every case,
charter, examination, and review are synthetic. No real account numbers, real
documents, or private filesystem paths appear anywhere in the topic's Markdown.
Any real-shaped fixture states how it was synthesized (the D1-P2 rule this plan
is establishing).
