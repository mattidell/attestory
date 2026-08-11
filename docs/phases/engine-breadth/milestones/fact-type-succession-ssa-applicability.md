<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "fact-type-succession-ssa-applicability",
  "milestone_state": "planned",
  "status": "Track 0 (paper). Prerequisite engine milestone opened by the 1098-E stop condition: the thirteen shared Schedule 1 absence propositions exist only as Social Security Benefits Worksheet-scoped declarations, and no mechanism exists by which a fact question can be succeeded by a differently identified fact question. Verified: all 23 ss-benefits-scope fact types are keyed on a literal tax-year value with no entity citizen, and are contributed, so neither displacement edge reaches them. No implementation chartered; no version numbers allocated.",
  "current_role": "Foreman (Track 0 charters prepared for owner launch; dispatch not authorized)",
  "current_prompt": "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md#Track 0 — mandatory questions",
  "scope": [
    "settle exact fact-type succession semantics against the Ontology's migration-artifact concept and two-edge invariant",
    "inventory and verify the mechanisms the kernel actually supports, with the two owner-rejected shapes as negative controls",
    "separate fresh-adoption from upgrade behaviour across five product cases",
    "mint honestly named neutral return-level Schedule 1 absence propositions",
    "repair the Social Security no-activity route so a return with no applicable source publishes its legal zero without the worksheet-scope declarations",
    "state the impact and publication envelope, then make the split decision before any build charter"
  ],
  "non_goals": [
    "Form 1098-E implementation or student-loan phaseout arithmetic",
    "general deletion, retirement, or redaction",
    "automatic migration of answers across different propositions",
    "reinterpreting existing findings under broader wording",
    "a universal migration framework beyond the minimum declared succession contract",
    "UI or persistence work",
    "the schedule1-part1-scope naming defect and the attachment-rule.v5 provenance defect, unless the selected mechanism necessarily touches them",
    "reading, quoting, staging, or committing any tax-instruction PDF"
  ],
  "deep_reads": {
    "paper": [
      "docs/roles/builder.md",
      "docs/archive/2026-07-09-intake/INTAKE_ONTOLOGY.md",
      "docs/adr/0011-tax-fact-identity-and-source-closure.md",
      "docs/adr/0025-expression-language-extensions.md",
      "docs/adr/0028-package-fact-surface-and-composition-obligation.md",
      "docs/adr/0038-qdcg-worksheet-and-declared-absence.md",
      "docs/adr/0041-correction-authority-policy.md",
      "packages/kernel/facts.py",
      "packages/kernel/currency.py",
      "packages/schemas/kernel/fact-type.v3.schema.json",
      "packages/content/tax/2025/rule.form1040-line9.v7.json",
      "AGENTS.md#Data Safety Rules"
    ],
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md#Contracts",
      "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md#Verification",
      "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md#Stop conditions",
      "docs/process/concurrent-work.md",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md#Objective",
      "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md#Verification",
      "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md#Exit criteria",
      "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md#Stop conditions",
      "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md#Track 0 adversarial closure",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->

# Milestone — Fact-type succession and Social Security applicability

**Milestone key:** `fact-type-succession-ssa-applicability`
**Primary branch:** `milestone/fact-type-succession-ssa-applicability-design`
**Base:** `origin/main` @ `f60e7d1`
**State:** Track 0 (paper). No implementation chartered.

This is a **prerequisite engine milestone**, not a Form 1098-E implementation
track. It exists because the 2025 Form 1098-E milestone stopped at design: the
shared Schedule 1 absence propositions its MAGI base needs already exist, but
declare Social Security Benefits Worksheet scope in their own titles, and the
engine has no mechanism by which a fact question can be succeeded by a
differently identified fact question.

Inputs carried forward from that stopped milestone are the **Durable findings
register**, the **owner ruling and stop-condition result**, the **retrospective**,
the **verified authority packets**, and the **kernel observations supporting the
stop**. Its chronological Track 0a/0b/0c narrative, withdrawn settlements, and
obsolete alternatives are not carried forward.

## Objective

Establish the minimum honest mechanism and content repair required before a
Form 1098-E milestone can use shared return-level Schedule 1 absence authority:

1. An old fact question may be succeeded by a differently identified fact
   question without deleting history and without any old answer being treated
   as an answer to the new question.
2. Honestly named neutral return-level Schedule 1 absence facts exist.
3. The applicable Social Security worksheet route consumes those neutral facts.
4. A return with no applicable Social Security source publishes its legally
   authorized zero without the worksheet-scope declarations.
5. A stable handoff contract exists for a fresh Form 1098-E implementation
   milestone.

## Current state

### Verified at this base

- `packages/content/tax/2025/ss-benefits-scope.bundle.json` — bundle
  `tax.us.2025.ss-benefits-scope.vocabulary`, `bundle.v2`, `v1`, **23** fact
  types, every one `fact-type.v2`, `nature: determinable`, value domain
  `{yes, no}` with no default, `supersession.policy: free`.
- **Every one of the 23 is keyed on a single identity key
  `{kind: literal, name: tax-year, values: ["2025"]}`.** There is no entity
  citizen in any of their keys.
- **Thirteen** of the 23 are the shared Schedule 1 absence propositions:
  `no-sch1-line11-educator`, `-line12-business-expenses`, `-line13-hsa`,
  `-line14-moving`, `-line15-deductible-se`, `-line16-se-retirement`,
  `-line17-se-health`, `-line18-penalty`, `-line19-alimony-paid`,
  `-line20-ira-deduction`, `-line23-archer-msa`, `-line25-other-adjustments`,
  and `no-schedule1-line24z-writein`. The thirteenth is **already declared**;
  the stopped milestone recorded it as newly required, which was correct as to
  requirement and wrong as to novelty.
- Every one of the 23 titles opens "Social Security Benefits Worksheet
  completeness component:" and closes "for the bounded Social Security
  worksheet claim." The declared authority scope is the worksheet claim, not
  the return.
- `packages/content/tax/2025/rule.form1040-line9.v7.json` publishes
  `tax.us.2025.income.total-income` with `"when": true` and `requires`
  including `tax.us.2025.social-security.line6b`.
  `rule.ss-benefits-worksheet.json` is that symbol's only producer corpus-wide.
- `packages/schemas/kernel/fact-type.v3.schema.json` is **allocated and unused
  by content**. It widens the supersession-policy vocabulary per ADR-0041. It
  declares **no** succession, migration, or replacement field.
- No migration or succession schema family exists under `packages/schemas/`.

### Kernel observations supporting the stop

- `packages/kernel/facts.py:84-101` — `apply_bundle_adoption` merges declared
  fact types into a flat `state.fact_types` dict keyed by id. Re-adoption under
  a revised bundle overwrites by id. There is **no deletion path**, and the
  merged entry retains **no provenance back to its adopting bundle**.
- `packages/kernel/currency.py:137-174` — `compute_currency` admits exactly
  three displacement roots: same-fact correction (`:79-94`), member withdrawal
  (`:97-114`), and superseded entities (`:151`).
- `packages/kernel/findings.py:556-576` — the sole consumer of
  `supersession: {"policy": "free"}`; it fires only on the same `fact_id`.

### The consequence, stated plainly

The thirteen propositions are **contributed**, so they have no derivation pins.
They are keyed on a **literal**, so no entity supersession reaches them.
Therefore **no existing displacement edge can reach them at all.** Whatever the
mechanism turns out to be, it cannot be a re-use of either edge as those edges
are currently rooted.

### Governing prior art

`docs/archive/2026-07-09-intake/INTAKE_ONTOLOGY.md` already names both halves of
this problem and constrains the answer:

- **Migration artifact** (:128): "where a version change alters identity
  itself — a fact type re-keyed, a concept split — migration may instantiate
  successor *facts*, not just findings. Ordinary rules never create questions,
  only answers; migration touches the lattice… migration artifacts sit closer
  to adoption than to arithmetic."
- **The two edges** (:154): derivation and individuation. "There is no third
  edge."
- **Correction versus succession** (:156): succession is "an individuating
  citizen replaced… or a migration reshapes the lattice — old facts displaced,
  successor facts instantiated, findings following by derivation."
- **Currency** (:152): current state is "the set of findings, **adoptions**, and
  grants not displaced by later acts."

ADR-0025 ratified a **successor-claim migration** for ADR-0024's categorical
code→label change: a versioned migration mapping artifact, a presented successor
claim citing the old value, and a required user assertion, so that a human
finding is never silently converted. That is the correct governance shape at the
**finding** level. This milestone asks whether the same shape reaches the
**fact-type** level. It is a precedent for the ethic, not proof of the mechanism.

### Leading hypothesis, explicitly unverified

Currency already treats **adoptions** as displaceable. If a fact type's
currency were derived from the currency of the bundle adoption that declared it,
then superseding that adoption would displace the fact type and its facts
without introducing a third edge between citizens — because it operates on the
adoption dimension of currency rather than on an edge. `apply_bundle_adoption`
does not record that provenance today, so this is kernel work, not free.

**This is a hypothesis to test first, not a selected design.** The stopped
milestone's recorded method failure was pricing a repair on an unverified
mechanism, twice. Track 0 verifies before it prices.

## Scope

Track 0 is paper and settles the six questions below. Implementation scope is
set by Track 0's split decision and allowed-impact envelope, and is not
pre-authorized here.

## Non-goals

- Form 1098-E implementation; student-loan phaseout arithmetic.
- General deletion, retirement, or redaction.
- Automatic migration of answers across different propositions.
- Reinterpreting existing findings under broader wording.
- A universal migration framework beyond the minimum declared fact-type
  succession contract.
- UI or persistence work.
- The `schedule1-part1-scope.bundle.json` consumer-scoped-title defect and the
  `attachment-rule.v5` provenance defect — recorded deferrals, in scope only if
  the selected mechanism necessarily touches them.
- Reading tax-instruction PDFs (see Authority boundary).

## Authority boundary

Foreman, Builders, and Reviewers **do not read tax-instruction PDFs**. Do not
open, quote, summarize, stage, or commit any PDF present locally.

Use the verified SSA and 1098-E authority packets and committed authority
conclusions. Where they do not establish the no-activity zero or the exact
meaning of a proposed neutral fact, **stop that question and request a bounded
authority review**. Do not repair an inadequate packet by reading the source.

## Track 0 — mandatory questions

### T0-1 Exact succession semantics

State the before-and-after of: the predecessor fact type; predecessor facts and
findings; currentness of predecessor-derived findings; the successor fact type;
successor facts; whether successor facts begin open; the authorizing act; the
edges causing displacement; and what remains permanently reachable as history.

Required semantic outcome: predecessor history remains; predecessor questions
cease to be current; successor questions become current and **open**;
predecessor answers are not copied, bridged, coerced, or reinterpreted; the user
must attest to the successor proposition; no deletion or redaction mechanism is
introduced.

Test against the Ontology's migration-artifact concept and the two-edge model.
**If the work turns on interpretation of governance text, or cannot fit the
two-edge model, stop and escalate to the owner for advisor consultation.** Do
not improvise doctrine.

### T0-2 Mechanism inventory and alternatives

Verify what the kernel supports by reading it. Do not infer capability from
names, comments, W-2 bundle succession, or repeated identifiers.

Compare at minimum:

| Candidate | Status |
| --- | --- |
| Declared migration artifact / adopted succession citizen | Live candidate |
| Adoption-level fact-type replacement (leading hypothesis above) | Live candidate |
| New neutral facts with dormant predecessors | **Owner-rejected** — leaves obsolete questions current indefinitely |
| Same-identifier redeclaration | **Owner-rejected** — broadens the meaning of existing findings |

The two rejected shapes appear only as negative controls explaining why the
selected mechanism is necessary.

Score the primary proposition against the Gate 1 axes and state whether rival
prototypes are required. Gate 2 governs: if paper distinguishes the
alternatives, stop at paper. If paper exposes a missing production substrate,
route it as a separate decision rather than absorbing it.

### T0-3 Fresh-adoption and upgrade behavior

Treat as separate product cases: a fresh workspace adopting only the successor
package; a workspace with predecessor SSA facts and findings; a workspace with
derived SSA results pinned to predecessor findings; a workspace whose
predecessor questions were never answered; and rebuild/replay from the immutable
act record. For each, state which fact types, facts, findings, and derived
results are current, displaced, open, or historical.

### T0-4 Neutral Schedule 1 vocabulary

Inventory the exact shared propositions rather than inheriting a count. For each
proposed neutral fact record: its real-world proposition; identity and
lifecycle; authority scope; invalidating events; consumers; whether the
predecessor proposition is genuinely different; and why an old answer cannot
satisfy it automatically. Use neutral identifiers; do not retain an
`ss-benefits-scope` prefix merely to avoid migration.

### T0-5 Social Security applicability

Draw the current dependency cone from a return with no Social Security source to
Form 1040 line 9 and demonstrate why the existing route requires the
worksheet-scope declarations. Specify a closed-empty/no-activity authority route
publishing the legally authorized zero without reading worksheet-only
declarations. **Its zero must carry the exact closure or absence authority that
establishes it; it must not be a default.** The existing unconditional burden is
**not** a precedent.

Prove also: a nonempty applicable SSA route still requires the appropriate
neutral facts; incomplete SSA source authority blocks honestly; the repair does
not silently bypass a recorded SSA statement; and line 9 and every existing
income route retain their values and provenance.

### T0-6 Impact and publication envelope

Enumerate new schemas/schema versions; migration or succession citizens; kernel,
currency, contribution, marshal, or runner changes; fact bundles and successor
SSA rules; package, published-package, and release versions; registries and
checksums; fixtures and goldens; presentation and coverage effects; reverse
consumers; and data-migration and compatibility tests.

**Distinguish semantic edit sites from total publication churn.** Maintain the
cross-milestone schema-intent ledger
(`docs/process/concurrent-work.md`) and require its drift check after rebases
and before publication.

## Split decision

Track 0 decides whether this is one milestone or two, and may re-cut the seam.
The recorded starting positions are:

- **A** — fact-type succession substrate.
- **B** — neutral SSA vocabulary plus no-activity applicability repair.

Keep them together only if the selected succession mechanism is bounded,
reviewable, and provable through the SSA migration without obscuring either
contract. Split them if the generic mechanism requires substantial
schema/kernel architecture, an independent ADR or prototype cycle, or a broader
migration surface than the SSA proving case.

**A desire for one PR does not determine the product boundary.**

**Foreman's entering recommendation, for Track 0 to confirm or overturn:** the
A/B seam as stated may be the wrong cut. The neutral vocabulary (T0-4) cannot
move without the substrate (T0-1/T0-2), so it is not separable from A; whereas
the no-activity applicability repair (T0-5) appears independent of succession
entirely — it is a rule/route defect on `rule.form1040-line9.v7`. If that holds,
the honest cut is **{substrate + vocabulary}** and **{applicability repair}**,
and the applicability repair should go **first**, because it reduces the
population of returns instantiating the thirteen propositions and therefore
shrinks the migration surface the substrate work must reason about. This is a
recommendation from the current-state reading above, not a settled finding.

## Contracts

To be stated by Track 0. No schema, rule, bundle, package, registry, or version
number is allocated until the split decision and allowed-impact envelope are
settled. Any chosen schema family and version is appended to the schema-intent
ledger before the corresponding edit.

## Fixtures

To be stated by Track 0, derived from the T0-3 product cases and the T0-5
applicability proofs. Synthetic only.

## Verification

The implementation plan must include at least:

1. Predecessor answer exists → succession occurs → predecessor is historical and
   successor is open.
2. A predecessor answer does not satisfy the neutral successor.
3. Successor attestation enables the nonempty SSA route.
4. Predecessor-derived SSA results are displaced through declared edges.
5. Fresh adoption exposes only the intended current vocabulary.
6. Upgrade preserves immutable history without duplicate current questions.
7. Closed-empty SSA source publishes zero without the worksheet-scope
   declarations.
8. A present SSA source cannot take the closed-empty route.
9. Incomplete source authority blocks.
10. Correction and replay produce the same current state.
11. Delete-and-rerun reproduces derived results and provenance.
12. Existing W-2, interest, dividend, IRA, capital-gain, unemployment,
    foreign-tax, and mortgage routes retain their established outputs.
13. Schema registry, data-safety, governance, typing, and CI gates pass.

## Data safety

Synthetic fixtures only. No personal document, statement, or real return value
enters the repository. No tax-instruction PDF is opened, staged, or committed.
No absolute workstation path is committed.

## Exit criteria

- Track 0 adversarial closure is complete with no unresolved `FAIL`.
- The split decision is made and recorded with its reasoning.
- The allowed-impact envelope is stated explicitly before the first
  implementation charter.
- The implementation and governance cost inventory (T0-6) is recorded **before**
  the build is chartered.
- The selected mechanism satisfies every required semantic outcome in T0-1.
- Every verification scenario above passes.
- A stable handoff contract exists for the fresh Form 1098-E milestone.

## Tracks

| Track | Content | State |
| --- | --- | --- |
| 0 | T0-1 … T0-6, split decision, adversarial closure, cost inventory | Open |
| 1+ | Set by the split decision | Not chartered |

## ADR posture

ADR count is not a budget. Determine whether the selected succession mechanism
needs an ADR **because future artifacts will be written against it**.
Content-only SSA applicability decisions may remain in this plan where existing
contracts fully govern them.

## Stop conditions

Stop and report to the owner if:

- succession cannot be expressed without a third displacement edge;
- the proposed mechanism makes an old answer current for a broader successor;
- predecessor questions remain current after claimed migration;
- implementation requires deletion or mutation of history;
- fresh and upgrade semantics disagree without a declared migration contract;
- the SSA zero lacks sufficient verified authority;
- the milestone cannot remain bounded to fact-type succession and its SSA
  proving case;
- governance interpretation is required.

## Track 0 adversarial closure

`PENDING` — all five artifacts required by `PROJECT_PLANNING.md`
("Track 0 Adversarial Closure Gate") before the first implementation charter:
authority-lifecycle table, empty/nonempty authority matrix, late-authority
counterexample, claim-reuse proof, and neighboring-capability dependency diff.
No unresolved `FAIL` may remain.
