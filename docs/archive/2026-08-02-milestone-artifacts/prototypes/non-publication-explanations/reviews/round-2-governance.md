# Governance Review: Non-Publication Explanations (Round 2)

- **Topic:** Non-Publication Explanations
- **Round:** 2 (it1 incumbent, unrevised since round 1, vs. it2 clean-room rival)
- **Reviewer:** Governance Reviewer (Round 2)
- **Date:** 2026-07-12
- **Scope:** `it1/design.md`, `examination-it1.md`, `it2/design.md`, `examination-it2.md` against `docs/governance/constitution.md`, `docs/governance/ontology.md`, and ADRs 0002, 0004, 0007, 0008, 0009, 0010, 0012, 0016, 0017. Cross-checked against the committed `packages/schemas/derivation/derivation-record.v1.schema.json` and its example fixture, since it2's authority questions make direct claims about that committed contract.
- **Independence:** did not read `reviews/round-2-adversary.md`.

Findings are numbered continuing from round 1 (`NPE-G1`). No design was repaired; only classified.

---

## Findings

### NPE-G2 — non-blocking — applies to: it1

**Summary.** `it1/design.md` and `examination-it1.md` are byte-identical in substance to what round-1-governance and round-1-adversary reviewed; they were not amended to state round-1's mandated resolution.

**Detail.** `round-1-triage.md` made NPE-G1 and NPE-A1 decision-blocking and prescribed a specific fix: a transient runner "Execution Map" plus explicit cycle detection/memoization in the walker. Gate 4 of `plan.md` pre-authorizes no repair pass, so this is process-conformant — the prototype documents are frozen evidence, and the fix is expected to be synthesized into the eventual ADR rather than written back into `design.md`. But a reader of `it1/design.md` and `examination-it1.md` alone (without `round-1-triage.md`) would come away believing Shape A is settled as described: on-demand AST/guard re-evaluation with "Zero Execution Overhead," no execution map, no visited-set, no memoization. The examination's recommendation text was never updated to note the refinement is required.

**Failure scenario.** An ADR drafter who cites `it1/design.md` and `examination-it1.md` as the evidence for adopting Shape A, without independently pulling `round-1-triage.md` into the citation chain, ratifies a design that still carries the out-of-sync risk and the missing cycle guard.

**Resolution.** Non-blocking: whoever drafts the ADR must cite `round-1-triage.md` alongside `design.md`/`examination-it1.md` as joint evidence for Shape A's accepted shape. No document needs to change.

---

### NPE-G3 — production condition — applies to: it1

**Summary.** `it1`'s `explanation-walk.v1` schema's top-level `disposition` enum includes `invalid` as a sixth sibling value alongside `blocked`, `guard_inapplicable`, etc. — contradicting ADR-0012 decision 4.

**Detail.** ADR-0012 decision 4 defines exactly five top-level disposition classes (`published_value`, `computed_zero`, `closure_backed_zero`, `blocked`, `guard_inapplicable`) and states: "Machine records may refine `blocked` into absent, invalid, open-source, or other schema'd codes." `invalid` is explicitly a *refinement code beneath* `blocked`, not a peer top-level disposition. `it1/design.md` line 56 declares `"disposition": { "enum": [..., "blocked", "guard_inapplicable", "invalid"] }` at the schema root — a target symbol's own disposition could be reported as the bare string `"invalid"`, which has no home in ADR-0012's vocabulary.

**Failure scenario.** A consumer branches on the walk payload's top-level `disposition` field, encounters `"invalid"`, and has no ADR-0012-defined rendering instruction for it (ADR-0012 decision 5 only names instructions for the five classes) — an unhandled case at the presentation boundary.

**Resolution.** Schema change: `invalid` must move to a nested refinement field on a `blocked`-disposition node (as `it1`'s own `failures[].type` already partially does for dependency-level invalidity), never appear as a sibling of `blocked` at the root `disposition` enum. Compare `it2`, which gets this layering right (`INVALID` is a `block_code` value under `node_kind: "blocked"`, never a root `node_kind`).

---

### NPE-G4 — production condition — applies to: it2 (and the underlying committed schema)

**Summary.** Confirmed genuine contract gap. The committed `derivation-record.v1.schema.json` does not require `guard_result` on a `dispositions[]` row whose `disposition` is `inapplicable`.

**Detail.** Read directly from `packages/schemas/derivation/derivation-record.v1.schema.json`: the `dispositions[]` item's `required` array is `["artifact_id", "disposition", "pins"]` — `guard_result` is present as an optional property only. NPE-P2's unsatisfied-guard frame is exactly the evidence `guard_result = false` supplies; without a schema-level requirement, a compliant runner could emit an `inapplicable` row with no `guard_result`, and `it2`'s walk (§5, `inapplicable` branch) would have nothing to place in `guard.result`.

**Failure scenario.** A runner implementation omits `guard_result` on an inapplicable row (schema-valid, since it's optional); the walker either fabricates a value (reconstruction, forbidden by Article 15) or fails to render the case-2-style explanation at all.

**Resolution.** Schema change to `derivation-record.v1`: add a conditional requirement (`if disposition == "inapplicable" then required guard_result`), mirroring the pattern `it2`'s own `npe-walk.v1` already uses for its `inapplicable` node. This is `it2`'s own authority question 4; I confirm it as CONFIRMED, not merely plausible.

---

### NPE-G5 — production condition — applies to: it2 (and the underlying committed schema)

**Summary.** Confirmed genuine contract gap. `derivation-record.v1` does not require `dispositions[]` to cover every eligible artifact in the adopted package (no totality constraint of any kind in the schema).

**Detail.** ADR-0008 decision 4 requires the record vocabulary to let a reader "distinguish evaluated-and-inapplicable rules from rules never reached," and calls a signature-identical-to-unsaturated record a defect. `it2`'s entire completeness argument (§8, "Retention sufficiency") and its `UNREACHED` block code depend on every eligible artifact getting a row. Nothing in the schema enforces this; a runner could emit a sparse `dispositions[]` array and remain schema-valid.

**Failure scenario.** A down-cascade artifact several hops from the actual failure is simply absent from `dispositions[]`; the walker (per `it2`'s own fallback, §9.1) must reconstruct its never-reached status by walking adopted `requires` edges instead of reading a row — a weaker, non-record-grounded claim that `it2` itself flags as inferior.

**Resolution.** This is `it2`'s own authority question 1, correctly self-identified as a runner-contract/record-schema decision, not the walker's to resolve. I confirm it as CONFIRMED. Resolution path: either (a) amend ADR-0008/the schema to mandate totality (e.g., a `minItems` tied to the adopted package's eligible-artifact count, checked at record-validation time), or (b) accept `it2`'s weaker fallback and document it as the production contract explicitly, rather than leaving it silently unenforced.

---

### NPE-G6 — decision-blocking — applies to: it2's proposed row-fold (and the underlying committed schema/fixture)

**Summary.** The committed schema's two "blocked" surfaces (`blocked[]` top-level array and `dispositions[disposition="blocked"]`) are not merely a theoretical join ambiguity — the shipped example fixture disagrees between them for the same artifact.

**Detail.** In `packages/sample_data/derivation/examples/derivation-record.completed.json`, `demo.rule.tax-table-line16` appears in `blocked[]` as `{code: "OPEN_TAX_TABLE_ROW", missing: ["demo.form1040.line15", "filing_status"]}` **and** in `dispositions[]` as `{disposition: "inapplicable", guard_result: false, pins: [...]}` — two different dispositions (`blocked` vs `inapplicable`) recorded for the same `artifact_id` in the one committed fixture that is supposed to demonstrate a valid closing record. This is a live defect in the currently-shipped evidence, not a hypothetical.

**Failure scenario.** Any walker (`it2`'s or otherwise) that joins on `artifact_id` across the two arrays, as the current schema forces it to, gets a genuinely contradictory answer for this artifact — is it blocked on a missing tax-table row, or inapplicable because its guard evaluated false? The fixture cannot both be right.

**Resolution.** `it2`'s proposed fix — fold `{code, missing}` onto the `dispositions[]` row so one row is self-contained (§9.2, authority question 2) — is the right direction, but it is a schema change to `derivation-record.v1` plus a corrected fixture, and it must land before any ADR adopts `it2`'s ledger-fold as the production contract; an ADR that assumes the fold without actually amending the schema would ratify a design built on a currently-contradictory data model. I mark this decision-blocking for the ADR (not for accepting `it2`'s *shape*, which correctly proposes the fix) because the fold is a stated but unimplemented precondition of the design's own completeness claims.

---

### NPE-G7 — non-blocking — applies to: it2 (and ADR-0012 cross-reference)

**Summary.** Disposition-term mismatch: the committed record schema and `it2`'s own `npe-walk.v1` both use `inapplicable`; ADR-0012 decision 4 and `plan.md`'s own statement of NPE-P2 use `guard_inapplicable`.

**Detail.** `it2` surfaces this for the *ledger* (authority question 5) but does not extend the same scrutiny to its own walk-payload schema, which it fully controls (a prototype artifact, unconstrained by the committed record schema). `node_kind: "inapplicable"` in `npe-walk.v1` could have used the already-ratified ADR-0012 term directly at the walk-payload layer even while flagging the ledger-schema mismatch as a separate open item — the walk payload is the surface closest to the form-field disposition vocabulary ADR-0012 actually governs.

**Resolution.** Triage note or small ADR addendum pinning one canonical term (`guard_inapplicable` is the ratified one; `inapplicable` should either be retired or explicitly declared a ledger-internal shorthand with a documented 1:1 mapping) across the record schema, the form-field disposition vocabulary, and any future production walk-payload schema.

---

### NPE-G8 — production condition — applies to: both it1 and it2 (architectural, cross-cutting)

**Summary.** Neither design establishes a currency/freshness contract between the explanation it returns and the *current* workspace revision.

**Detail.** The Ontology's **Derivation record** entry is explicit: "Coverage observed by a run belongs to its record — the boundary that run reached; coverage available *now* is always a fresh query against present facts, never a stored copy." `it2`'s entire architecture answers "why did run R not publish symbol S" by reading run R's closing disposition ledger — a legitimate record-grounded historical answer per Article 15. But nothing in `it2`'s design establishes that this is synchronized with *current* workspace state: if the user asserted the previously-missing fact after run R completed and before a new run executed, `it2`'s walk still reports the stale `blocked/ABSENT` reason from run R. The payload carries a `workspace_revision` field, but that only labels the staleness — it doesn't resolve or surface it to the consumer as "this explanation may be out of date."

`it1`'s Shape A sidesteps exactly this problem: its algorithm explicitly "retrieve[s] S's status in current workspace run" and evaluates guards against presently-asserted values, so it always answers the "now" question — at the cost of the re-evaluation/out-of-sync risk that is NPE-G1's whole complaint. The two designs sit on opposite horns of a freshness-vs-reconstruction tradeoff, and neither one's authority-question list (it2 names five; it1 names none) surfaces this as an open item. `it2`'s stronger claim to Article-15 conformance ("grounded in the record, never reconstructed") is true only for the run it references, and the design does not say which run that is, or what happens when it is stale.

**Failure scenario.** A user fixes the missing 1099-INT closure, checks "why is line 2b still empty" before the next saturation run, and is told — correctly per the last closing record, incorrectly per their current situation — that the source family is still unclosed.

**Resolution.** An ADR-level decision is needed, not currently held by any cited ADR: either (a) an explanation-serving invariant that refuses or visibly labels an explanation whose referenced run's `workspace_revision` is behind the workspace's current revision (and/or triggers a re-run before answering), or (b) an explicit, governance-recorded "explains the last completed run, not live state" product framing that the UI must surface. This is orthogonal to which design shape wins; it must be closed before either design ships.

---

## Cross-cutting confirmations (not new findings, offered as grounding for the verdicts)

- **Article 12/13, ontology "open fact"/"record" doctrine vs. Shape B (it1):** round-1's rejection stands. Writing "stub finding" citizens for unexecuted rules turns an open fact into a fact bearing a finding (Ontology, Open fact), and exposes non-published, in-run-only state as if it were workspace truth (Article 13's foreclosure of "partial results exposed as truth"). `it1`'s own examination already recommends against Shape B; this review does not disturb that.
- **NPE-G1 (out-of-sync risk) and NPE-A1 (cycles/diamonds), answered by it2:** `it2` closes both natively. Grounding the walk in the already-ratified ADR-0008 closing record (an immutable, versioned citizen — Article 14) is a *stronger* answer than round-1-triage's own suggested "transient Execution Map...stored as run metadata": a genuinely transient (non-citizen, discardable) structure would itself sit awkwardly against Article 14's demand for an immutable process record of every run. `it2`'s `visited.active` (cycle cutting) and `shared` (diamond memoization, demonstrated concretely in Case 1's five-line cascade collapsing to one expanded subtree) directly answer both of round-1-adversary's Shape-A counterexamples (infinite recursion and redundant multi-path evaluation).
- **Edge/record placement (ADR-0008/0010):** both designs place things correctly where they touch committed contracts. `it2`'s ledger lives in the record stream, never the act log; its walk never writes; it never touches `currency.py` or the derivation-edge graph (ADR-0010 untouched, correctly out of scope).
- **Gate 7 (production boundary):** both designs correctly label their schemas as prototype-only, non-merging.

---

## Verdict per design

### it1 (Shape A recommended, Shape B rejected)

**Reject as a standalone, production-ready design; accept as diagnostic evidence only, to be carried into ADR drafting jointly with `round-1-triage.md`.**

Shape B's rejection is sound and stands. Shape A correctly identifies the out-of-sync risk (NPE-G1) but, as literally written, does not resolve it — no execution map, no cycle detection stated in the algorithm (NPE-G2) — and its own schema misclassifies `invalid` as a disposition peer of `blocked` rather than a refinement, contradicting ADR-0012 decision 4 (NPE-G3, production condition). None of this is a defect in round-1's process (Gate 4 forbade repair); it means `it1`'s design.md cannot be cited alone as the accepted shape — the ADR must synthesize `design.md` + `round-1-triage.md`'s resolution + a corrected disposition enum.

### it2 (Run Disposition Ledger + projection walk)

**Conditionally accept.** This is the governance-preferred direction of the two. NPE-P1 is airtight by construction (ledger lives in the record stream, never the act log; walker writes nothing). NPE-P2 is schema-enforced, not merely represented (`inapplicable` nodes are schema-forbidden from carrying `unmet`). It fully and more strongly answers NPE-G1 and NPE-A1 than `it1` does, and its `block_code` layering correctly conforms to ADR-0012 decision 4 where `it1`'s does not.

Conditions before this becomes the basis of a production ADR:
1. Close NPE-G4 (`guard_result` required when `inapplicable`) — schema change to `derivation-record.v1`.
2. Close NPE-G5 (ledger totality) — schema/ADR decision, `derivation-record.v1`.
3. Close NPE-G6 (contradictory `blocked[]`/`dispositions[]` surfaces, confirmed in the shipped fixture) — schema change plus fixture correction; decision-blocking for any ADR that assumes the fold.
4. Close NPE-G7 (disposition vocabulary term) — triage note or ADR addendum.
5. Close NPE-G8 (record-freshness/currency contract) — ADR decision; applies equally to `it1` and is not resolved by either design as written.

None of these conditions requires reshaping the design's core proposal (the ledger, its totality/fold refinements, and the schema-enforced node/edge split); they are contract-hardening steps the design itself correctly identifies it cannot resolve unilaterally.
