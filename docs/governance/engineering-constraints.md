---
artifact: engineering-constraints
version: "0.1"
status: ratified
date: 2026-07-09
---

# Engineering Constraints

*Versioned governance artifact, subordinate to Constitution and Ontology. Entries are keyed to articles; each states the foreclosed pattern, the permitted alternative, and a detection — how violation is caught in review, test, or by a checking agent. Entries bind implementations; detections are the conformance suite's specification.*

---

**Part I — Authority**

**E1.1 (Peerage) — No document-child schemas.** Foreclosed: facts or findings modeled as children, rows, or fields of a document record; foreign keys from finding to file as identity. Permitted: provenance references from findings to evidence. *Detection:* schema review — no fact-type identity key references a source-flavor citizen; deleting an evidence row in a test workspace must alter no finding's content or identity, only its evidentiary standing.

**E1.2 (Peerage) — No re-upload rewrite.** Foreclosed: intake paths that update findings when a document is replaced. Permitted: re-extraction producing new proposals. *Detection:* integration test — re-upload a modified document; assert zero finding mutations and ≥0 new proposals.

**E2.1 (Proposal) — No pending store.** Foreclosed: tables, queues, or caches of unresolved proposals that any flow reads, escalates, or requires resolved. Permitted: regeneration on demand; captured proposals inside act records. *Detection:* destroy all proposal-bearing transient state; no workspace behavior changes except suggestions needing regeneration. Any schema whose name or use implies "pending" fails review.

**E2.2 (Proposal) — Verbatim capture.** Foreclosed: assertion paths that record a normalized, re-derived, or re-rendered claim rather than the presented one. Permitted: capture plus separate normalized projections. *Detection:* golden test — present claim, mutate the proposing model, assert; captured content must equal what was presented, byte-stable.

**E3.1 (Judgment) — No operative defaults.** Foreclosed: configuration or code defaults that flow into derivation for elective-natured facts. Permitted: recommended values presented as proposals. *Detection:* run saturation on a workspace with all elective facts open; every rule requiring one must block, none may fire.

**E4.1 (Adoption) — Adoption gate.** Foreclosed: any run against artifacts lacking a current adoption act in scope. Permitted: proposing adoption; running on synthetic workspaces under test adoptions. *Detection:* runner entry point statically requires an adoption reference; run records failing to pin one fail schema validation.

---

**Part II — State**

**E5.1 (Containment) — Destroy-and-rebuild.** Foreclosed: components whose destruction loses accepted state. Permitted: caches, indexes, queues, checkpoints. *Detection:* the containment drill — destroy every store except the workspace in a staging environment; rebuild; diff authoritative state. Zero loss or the component owning the delta is in violation.

**E5.2 (Containment) — No staging of accepted input.** Foreclosed: wizard or flow session state holding user-accepted input for later commit. Permitted: uncommitted UI state for unconfirmed input. *Detection:* kill the session after each acceptance step; accepted input must already be workspace state.

**E6.1 (Atomicity) — Interruption safety.** Foreclosed: multi-write operations whose partial completion misstates history. Permitted: transactions, sagas publishing complete outputs. *Detection:* fault-injection suite — kill each pipeline between every pair of writes; workspace must validate as incomplete-but-true at every cut point.

**E7.1 (Supersession) — Derived currency.** Foreclosed: stored current/superseded flags updated alongside acts. Permitted: materialized currency views rebuilt from the record. *Detection:* recompute currency from the act log alone; diff against any materialization; mismatch is the violation.

**E7.2 (Supersession) — No third edge.** Foreclosed: displacement triggered by anything but declared derivation or individuation edges. *Detection:* schema review — every cascade path in code maps to a declared edge; cascade tests enumerate edges and assert closure equality.

**E8.1 (Reachability) — Step-off test.** Foreclosed: state visible only inside a flow; work discarded on exit. *Detection:* UI test per flow — exit at every step; assert all collected state reachable from the workspace root and no data lost.

---

**Part III — Meaning**

**E9.1 (Canon) — No tolerant readers.** Foreclosed: consumers that accept undeclared shapes, coerce, or repair malformed instances. Permitted: boundary parsers producing proposals; strict validation with rejection. *Detection:* fuzz each consumer with near-valid instances; any acceptance of a schema-invalid instance fails. Code review flags catch-and-continue on validation errors.

**E10.1 (Declaration) — No shadow nouns.** Foreclosed: generic containers with type tags, side tables accreting meaning, repurposed fields. *Detection:* periodic audit — any table, payload type, or enum consumed by more than one component must map to a register entry; unmapped ones are violations or retirement candidates.

**E11.1 (Legibility) — Purity.** Foreclosed: rule evaluation touching clock, randomness, environment, network, or any state outside declared inputs. *Detection:* execute rules in a sealed sandbox denying all such access; any escape attempt fails the artifact. Double-run equality: same inputs, twice, byte-identical outputs.

**E11.2 (Legibility) — Portability.** Foreclosed: engine behavior that adds tax meaning. *Detection:* the portability test — a second minimal reference runner executes the artifact corpus against fixture workspaces; any finding divergence from the production runner is a violation in one of them.

**E11.3 (Legibility) — No orchestrated traversal.** Foreclosed: form order, cross-form bridges, or applicability living in scheduler code. *Detection:* delete a rule artifact; every behavior difference must be attributable to that artifact. Grep-level review: the runner contains no form identifiers.

---

**Part IV — Computation and Record**

**E12.1 (Contract) — Pin completeness.** Foreclosed: derived findings missing input or artifact version pins. *Detection:* schema validation requires pins; replay audit — re-derive from pins alone in a clean environment; inequality means an unpinned dependency exists.

**E13.1 (Publication) — Delete-and-rerun.** Foreclosed: derivation results not reproducible from asserted findings plus adopted artifacts. *Detection:* the canonical test — delete every derived finding; saturate; assert identical findings and provenance return.

**E13.2 (Publication) — No lockstep totals.** Foreclosed: rollups maintained synchronously with inputs as authoritative values. Permitted: display aggregates as views. *Detection:* mutate an input without running derivation; any authoritative total that changed was lockstep-maintained.

**E14.1 (Record) — No silent execution.** Foreclosed: processes touching authoritative state without a record, including failures. *Detection:* process entry points acquire a record handle before their first read; chaos test — crash processes mid-flight and assert a record exists describing the failure.

**E14.2 (Record) — Records are not inputs.** Foreclosed: rule artifacts declaring record-kind citizens as dependencies. Permitted: pre-assertion processes consulting rejection records. *Detection:* static check on artifact dependency declarations against register kinds.

**E15.1 (Explanation) — No dead ends.** Foreclosed: explanation chains terminating at code locations, log lines, or absent records. *Detection:* walk every value on a saturated fixture workspace to its grounds; any terminal that is not an act, finding, artifact, or record fails.

---

**Part V — Boundary**

**E16.1 (Grant) — Consultation gate.** Foreclosed: assistive processes reading workspace state without a grant reference; context assembled from the workspace at large. *Detection:* consultation APIs require a grant token scoping reads; access outside scope is denied structurally and the denial logged. Consultation records missing grant pins fail validation.

**E17.1 (Context) — Inspectable assembly.** Foreclosed: context assembly whose inclusion/exclusion cannot be rendered to the user; summaries replacing underlying records. *Detection:* for every consultation record, the operative context must be reconstructable and displayable; destructive-distillation check — the detail behind every summary remains reachable.

**E18.1 (Quarantine) — Structural walls.** Foreclosed: network paths, credentials, or mounts from non-quarantine environments to personal data. *Detection:* infrastructure audit as code — environment manifests prove no route exists; a canary probe from each lower environment must fail to reach production data.

**E18.2 (Quarantine) — Egress hygiene.** Foreclosed: logs, traces, error reports, prompts, or telemetry carrying personal content outside. *Detection:* seeded-marker test — plant synthetic-but-marked values in a quarantine workspace; scan all egress sinks for markers; any hit is the violating pipeline.

**E18.3 (Quarantine) — Synthetic provenance.** Foreclosed: test data derived from identifiable records however altered. *Detection:* fixture provenance manifest — every fixture names its generator and constraints; fixtures without manufacturing provenance are quarantined pending replacement.

**E19.1 (Filing) — Fixed representation.** Foreclosed: transmission pipelines that re-render, recompute, or inject values after the shown representation is adopted. *Detection:* byte-comparison between the representation captured by the filing act and the transmitted payload; any operative delta fails.
