<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "fact-type-succession-ssa-applicability",
  "active_plan": "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md",
  "milestone_state": "planned",
  "status": "**ENGINE BREADTH / FACT-TYPE SUCCESSION AND SOCIAL SECURITY APPLICABILITY \u2014 TRACK 0 (PAPER), NO IMPLEMENTATION CHARTERED.** Prerequisite engine milestone opened because the 2025 Form 1098-E milestone stopped at design: the thirteen shared Schedule 1 absence propositions its MAGI base needs exist only as Social Security Benefits Worksheet-scoped declarations, and the engine has no mechanism by which a fact question can be succeeded by a differently identified fact question. Verified at this base: all 23 ss-benefits-scope fact types are keyed on a single LITERAL {name: tax-year, values: ['2025']} \u2014 no entity citizen in any key \u2014 and are contributed, so they carry no derivation pins either; therefore NO existing displacement edge can reach them. fact-type.v3 is allocated, unused by content, and declares no succession field; no migration schema family exists. The Ontology already names the migration artifact (INTAKE_ONTOLOGY.md:128, 'a fact type re-keyed... migration may instantiate successor facts... closer to adoption than to arithmetic'), the two-edge invariant ('there is no third edge', :154), and correction-vs-succession (:156); ADR-0025's successor-claim migration is precedent for the ethic at FINDING level, not proof of a FACT-TYPE mechanism. Leading hypothesis to test first, explicitly unverified: currency already treats ADOPTIONS as displaceable, so deriving fact-type currency from its adopting bundle's adoption may give succession without a third citizen-to-citizen edge \u2014 apply_bundle_adoption keeps no bundle provenance today, so this is kernel work. Track 0 settles T0-1 succession semantics, T0-2 mechanism inventory (dormant predecessors and same-identifier redeclaration are owner-rejected, admissible only as negative controls), T0-3 fresh-adoption vs upgrade, T0-4 neutral vocabulary, T0-5 SSA applicability repair, T0-6 impact envelope; then the split decision, the adversarial-closure gate, and the cost inventory BEFORE any build charter. Foreman's entering recommendation for Track 0 to confirm or overturn: the owner's A/B seam may be miscut \u2014 vocabulary is inseparable from substrate, while the no-activity applicability repair looks independent of succession entirely and should go FIRST to shrink the migration surface. AUTHORITY BOUNDARY: no seat reads tax-instruction PDFs; an inadequate authority packet triggers a bounded authority review, never a source read. No schema/rule/package/registry/version number is allocated until the split decision and allowed-impact envelope are settled.",
  "current_role": "Foreman (Track 0 charters prepared for owner launch; dispatch not authorized)",
  "current_prompt": "docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md#Track 0 \u2014 mandatory questions"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Curated history and architectural decisions live in retrospectives
and `docs/adr/`; historical execution records live under `docs/archive/`.

## High Level Milestone Briefing

The engine computes the closed Engine Breadth synthetic routes through Form
1099-DIV box 2a and box 12, Schedule K-1 box-5 interest, market-discount
interest, Schedule B adjustments, covered Form 1099-B capital paths including
inbound carryovers and Form 8949 wash-sale (code W) lines 1b/8b, Form 1099-INT
box 8 tax-exempt interest on line 2a, Form 1099-G box-1 unemployment through
Schedule 1 into Form 1040 line 8, the bounded Form 1099-DIV box-7 direct
foreign tax credit, the merged IRA line-4b route, the bounded SSA-1099
Benefits Worksheet route through Form 1040 lines 6a/6b, and the bounded Form
1098 home-mortgage interest route through Schedule A and Form 1040 line 12e.

This branch opens no new tax route. It is a **prerequisite engine milestone** —
the first work whose subject is the shape of the question-space itself rather
than a form. It exists because the next tax route, Form 1098-E student-loan
interest through Schedule 1 line 21, cannot be built honestly until a fact
question can be succeeded by a differently identified fact question.

## Operational State: Engine Breadth

* **Active milestone (this branch):** Fact-type succession and Social Security
  applicability — a **prerequisite engine milestone**, at **Track 0 (paper)**.
  No implementation is chartered and no version numbers are allocated.
* **Why it exists:** the 2025 Form 1098-E milestone stopped at design. Its MAGI
  base needs thirteen shared Schedule 1 absence propositions that exist only as
  **Social Security Benefits Worksheet-scoped** declarations, and the engine has
  no mechanism by which a fact question can be succeeded by a differently
  identified fact question.
* **The hard finding:** all 23 `ss-benefits-scope` fact types are keyed on a
  single **literal** `{name: tax-year, values: ["2025"]}` — no entity citizen in
  any key — and are **contributed**, so they carry no derivation pins. Neither
  of the two displacement edges can reach them as those edges are currently
  rooted. `fact-type.v3` is allocated, unused by content, and declares no
  succession field; no migration schema family exists.
* **Governing prior art:** the Ontology already names the **migration artifact**
  (`INTAKE_ONTOLOGY.md:128`), the **two-edge invariant** (`:154`, "there is no
  third edge"), and **correction versus succession** (`:156`). ADR-0025's
  successor-claim migration is precedent for the ethic at the **finding** level,
  not proof of a **fact-type** mechanism.
* **Leading hypothesis (unverified, to test first):** currency already treats
  **adoptions** as displaceable, so deriving a fact type's currency from its
  adopting bundle may yield succession without a third citizen-to-citizen edge.
  `apply_bundle_adoption` keeps no bundle provenance today, so this is kernel
  work, not free.
* **Split decision is open.** The foreman's entering recommendation — for Track 0
  to confirm or overturn — is that the owner's A/B seam may be miscut: the
  neutral vocabulary is inseparable from the substrate, while the no-activity
  applicability repair looks independent of succession entirely and should go
  **first**, shrinking the migration surface.
* **Authority boundary:** no seat reads tax-instruction PDFs. An inadequate
  authority packet triggers a **bounded authority review**, never a source read.
* **Branch / worktree:** `milestone/fact-type-succession-ssa-applicability-design`
  in the `engine-succession` worktree, cut fresh from `origin/main` (`f60e7d1`).
* **Plan:** `docs/phases/engine-breadth/milestones/fact-type-succession-ssa-applicability.md`.
* **Inherited inputs:** the stopped 1098-E milestone's Durable findings
  register, owner ruling, retrospective, verified authority packets, and kernel
  observations. Its Track 0a/0b/0c narrative is **not** carried forward.
* **Blocked behind this:** a fresh Form 1098-E milestone, to be re-cut from
  `main` on the first dependency-safe Schedule 1 Part II → Form 1040 AGI
  vertical slice once this settles and merges.
* **Next:** owner launches the Track 0 charters; dispatch is not authorized.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
