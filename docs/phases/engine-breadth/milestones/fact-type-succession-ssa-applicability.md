<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "fact-type-succession-ssa-applicability",
  "milestone_state": "planned",
  "status": "SPLIT RECORD. The owner approved splitting the prerequisite into two milestones, applicability repair first: (1) ssa-no-activity-applicability, chartered on its own branch and PR; (2) fact-type-succession-neutral-schedule1, chartered only after (1) merges. They do not share a PR. This document charters nothing; it is the split record and Milestone 2's inherited Track 0 input. Two owner corrections govern: docs/archive/ is NEVER product authority, so the governing text is the ratified docs/governance/ontology.md (fact types and facts at §2, migration artifact at §5, two-edge invariant and correction-versus-succession at §7), and INTAKE_ONTOLOGY.md is historical corroboration only, cited nowhere; and the applicability repair does NOT reduce how many literal-keyed facts a workspace instantiates (§2: such facts 'arrive with the territory, instantiated when a body of fact types is adopted'), it reduces unnecessary questions users must answer and prospectively the number of predecessor findings created, so Milestone 2 must still handle predecessor facts that are OPEN as well as answered and preserve the full upgrade matrix. Verified substrate carried forward: all 23 ss-benefits-scope fact types keyed on a single literal {tax-year: 2025} with no entity citizen, contributed so no derivation pins — nothing reaches them under §7's two edges; thirteen are the shared Schedule 1 absences and no-schedule1-line24z-writein already exists in the predecessor bundle; fact-type.v3 allocated but unused and carries no succession field; no migration schema family exists. Owner governance reading for Milestone 2: superseding an adoption MAY authorize the transition but adoption currency may NOT become an undeclared third displacement channel — the contract must expose the predecessor fact type or its adoption as an explicit individuation root, or map every displacement through one of the two recognized edges; reject any design that merely removes types from a flat runtime dictionary or filters by current adoption without declaring the dependency responsible for their standing. Presume Milestone 2 needs an ADR that narrows and instantiates the Ontology rather than amending it. Adoption-currency is a HYPOTHESIS TO TEST, not an accepted design; prototype only after the paper rung identifies the smallest remaining empirical question.",
  "current_role": "Foreman (split record complete; Milestone 1 chartered on its own branch)",
  "current_prompt": "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md#Mechanism inventory (preserved for Milestone 2's Track 0)",
  "scope": [
    "record the owner-approved split into two ordered milestones that do not share a PR",
    "correct the archive-as-authority citation error to the ratified docs/governance/ontology.md",
    "correct the ordering rationale: the repair narrows the finding population, never the fact population",
    "preserve the mechanism inventory, negative controls, and owner governance reading as Milestone 2's Track 0 input"
  ],
  "non_goals": [
    "chartering or implementing either successor milestone from this document",
    "citing docs/archive/ as product authority",
    "treating the adoption-currency idea as an accepted design",
    "reading, quoting, staging, or committing any tax-instruction PDF"
  ],
  "deep_reads": {
    "paper": [
      "docs/roles/builder.md",
      "docs/governance/ontology.md",
      "docs/adr/0025-expression-language-extensions.md",
      "docs/adr/0028-package-fact-surface-and-composition-obligation.md",
      "docs/adr/0041-correction-authority-policy.md",
      "packages/kernel/facts.py",
      "packages/kernel/currency.py",
      "packages/schemas/kernel/fact-type.v3.schema.json",
      "AGENTS.md#Data Safety Rules"
    ],
    "implementation": [
      "docs/roles/builder.md",
      "docs/process/concurrent-work.md",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md#Governing corrections",
      "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md#Mechanism inventory (preserved for Milestone 2's Track 0)",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->

# Split record — SSA applicability repair, then fact-type succession

**Key:** `fact-type-succession-ssa-applicability` (retired as a single milestone)
**Branch:** `milestone/fact-type-succession-ssa-applicability-design`
**Base:** `origin/main` @ `f60e7d1`
**State:** split approved by the owner. This document is the **split record** and
Milestone 2's inherited Track 0 input. It charters nothing.

The Form 1098-E milestone stopped at design: its MAGI base needs thirteen shared
Schedule 1 absence propositions that exist only as Social Security Benefits
Worksheet-scoped declarations, and the engine has no mechanism by which a fact
question can be succeeded by a differently identified fact question.

The owner approved splitting the prerequisite in two, in this order:

| # | Milestone | Key | State |
| --- | --- | --- | --- |
| 1 | SSA no-activity applicability repair | `ssa-no-activity-applicability` | Chartered on its own branch and PR |
| 2 | Fact-type succession with neutral Schedule 1 vocabulary | `fact-type-succession-neutral-schedule1` | Not chartered; charter after Milestone 1 merges |

The fresh Form 1098-E implementation milestone begins after both merge.

**Milestones 1 and 2 do not share a PR.** The applicability repair does not wait
on Milestone 2's prototype and ADR cycle.

## Governing corrections

**1. `docs/archive/` is never product authority.** The governing text is the
ratified `docs/governance/ontology.md`, which independently carries every
contract this work depends on:

- **§2 — Claims, facts, findings.** Fact type, fact, open fact, finding,
  supersession.
- **§5 — Derivation machinery.** Migration artifact.
- **§7 — Supersession and lifecycle.** The single mechanism, currency, the two
  edges, correction versus succession.

`docs/archive/2026-07-09-intake/INTAKE_ONTOLOGY.md` is **historical corroboration
only** and is cited nowhere in the plans or orientation blocks. The prior draft
of this plan cited it as governing intent; that was wrong and is corrected here.

**2. The ordering rationale was wrong and is corrected.** The applicability
repair does **not** reduce how many literal-keyed facts a workspace instantiates:
§2 states that such facts "arrive with the territory, instantiated when a body of
fact types is adopted," so adoption instantiates all of them regardless. What the
repair reduces is the number of **unnecessary questions a user must answer**, and
prospectively the number of **predecessor findings users create** before migration
exists.

**Milestone 2's succession design must therefore handle predecessor facts that are
open and predecessor facts that carry findings, and preserve the full upgrade
matrix.** The repair narrows the finding population, never the fact population.

The ordering stands because the applicability repair is independently correct,
content-level unless contrary evidence emerges, immediately valuable, separable
from generic succession machinery, and prevents future no-SSA workspaces from
accumulating unnecessary SSA-scope attestations before migration exists.

## Verified substrate (carried into Milestone 2)

- `ss-benefits-scope.bundle.json` — `bundle.v2`, `v1`, **23** fact types, all
  `fact-type.v2`, `nature: determinable`, domain `{yes, no}` with no default,
  `supersession.policy: free`.
- **Every one of the 23 is keyed on a single identity key
  `{kind: literal, name: tax-year, values: ["2025"]}`.** No entity citizen
  appears in any key.
- **Thirteen** are the shared Schedule 1 absence propositions:
  `no-sch1-line11-educator`, `-line12-business-expenses`, `-line13-hsa`,
  `-line14-moving`, `-line15-deductible-se`, `-line16-se-retirement`,
  `-line17-se-health`, `-line18-penalty`, `-line19-alimony-paid`,
  `-line20-ira-deduction`, `-line23-archer-msa`, `-line25-other-adjustments`,
  and `no-schedule1-line24z-writein`. **Thirteen total.** The thirteenth is
  **already declared in the predecessor bundle** — required, not newly
  discovered.
- Every one of the 23 titles opens "Social Security Benefits Worksheet
  completeness component:" and closes "for the bounded Social Security worksheet
  claim." Declared authority scope is the worksheet claim, not the return.
- `rule.ss-benefits-worksheet.json` (`rule-artifact.v3`, `v1`) is the **only**
  producer of `tax.us.2025.social-security.line6b` corpus-wide, and carries
  **33** `requires`.
- `rule.form1040-line9.v7.json` has `"when": true` and requires
  `tax.us.2025.social-security.line6b` unconditionally.
- `fact-type.v3` is allocated, **unused by content**, and declares no succession
  field. No migration schema family exists under `packages/schemas/`.

### The consequence

The thirteen are **contributed**, so they carry no derivation pins. They are
keyed on a **literal**, so no keyed-on citizen exists for an individuation edge
to reach. Under §7's two edges, **nothing currently reaches them.**

§2 explains why: facts of this shape "arrive with the territory, instantiated
when a body of fact types is adopted," rather than being "individuated into
existence when the citizens they're keyed on appear." Adoption-instantiated facts
have no declared individuation root today. That undeclared dependency is the
whole of Milestone 2's problem.

## Mechanism inventory (preserved for Milestone 2's Track 0)

| Candidate | Status |
| --- | --- |
| Declared migration artifact / adopted succession citizen (§5) | Live candidate |
| Adoption-level fact-type replacement | **Hypothesis to test, not an accepted design** |
| New neutral facts with dormant predecessors | **Owner-rejected** — leaves obsolete questions current indefinitely |
| Same-identifier redeclaration | **Owner-rejected** — broadens the meaning of existing findings |

The two rejected shapes survive only as **negative controls** explaining why the
selected mechanism is necessary.

### Owner's governance reading (governs Milestone 2)

- Superseding an adoption **may** be the act that authorizes the transition.
- Adoption currency **may not** become an undeclared third displacement channel.
- The selected contract must expose the predecessor fact type **or its adoption**
  as an explicit **individuation root** for predecessor facts, or otherwise map
  every displacement through one of §7's two recognized edges.
- The migration artifact may instantiate successor facts.
- Successor facts begin **open**.
- No predecessor finding is copied, converted, or treated as answering the
  successor.
- Derived findings depending on predecessor findings are displaced through
  declared edges.
- All predecessor acts, facts, findings, and adoptions remain reachable as
  history.

**Rejection rule.** If the design merely removes old types from a flat runtime
dictionary, or filters them by current adoption, **without declaring the
dependency responsible for their standing**, reject it as an undeclared third
edge.

### Precedent, correctly bounded

ADR-0025 ratified a successor-claim migration for the ADR-0024 code→label change:
a versioned mapping artifact, a presented successor claim, and a required user
assertion so a human finding is never silently converted. That is useful
precedent for the **user-facing ethic**. It does **not** specify a fact-lattice
migration mechanism, and is not cited as one.

### Prototype posture

A prototype is appropriate **only after** the paper rung identifies the smallest
remaining empirical question. The adoption hypothesis must be tested against at
least: fresh adoption; upgrade with **open** predecessor facts; upgrade with
**answered** predecessor facts; predecessor-derived findings; replay from the
immutable act history; successor re-attestation; correction after succession; and
rejection of old identifiers by successor consumers.

### ADR posture

**Presume Milestone 2 requires an ADR.** §5 admits migration, but Milestone 2
would introduce the first migration schema family, artifact shape, adoption
semantics, fact-lattice transition, and kernel execution contract that future
artifacts will be written against. The ADR **narrows and instantiates** the
Ontology; it does not amend it.

No governance version change is presently indicated. **Stop for advisor
consultation** if the paper design cannot express displacement through a
derivation or individuation edge, or if it requires broadening §7's definition of
either edge.

### Open question inherited from Milestone 1

Milestone 1's Track 0 tests whether the SSA family closure alone establishes the
no-activity zero. The family's own `closure_claim` disclaims RRB-1099, SSA-1042S,
and foreign systems, while
`tax.us.2025.ss-benefits-scope.no-rrb-or-foreign-social-benefit` asserts exactly
that absence. If Milestone 1 finds that declaration load-bearing for an honest
zero, it is a **source-existence** proposition wearing worksheet-scope wording —
a **fourteenth** migration candidate for Milestone 2, not a thirteenth Schedule 1
absence. Milestone 1 records the finding; Milestone 2 disposes of it.

## Standing constraints for both milestones

**Authority boundary.** Foreman, Builders, and Reviewers do not read
tax-instruction PDFs — no opening, quoting, summarizing, staging, or committing.
Use the verified authority packets. Inadequate authority is a **stop** requiring a
bounded authority review, never a source read.

**Deferred, in scope only if the selected mechanism necessarily touches them:**
the `schedule1-part1-scope.bundle.json` consumer-scoped-title defect; the
`attachment-rule.v5` provenance defect.

**Not carried forward from the stopped 1098-E branch:** its chronological Track
0a/0b/0c narrative, withdrawn settlements, obsolete alternatives, and accumulated
charter history. Carried forward: the Durable findings register, the owner ruling
and stop-condition result, the retrospective, the verified authority packets, the
kernel observations supporting the stop, and applicable accepted ADRs.
