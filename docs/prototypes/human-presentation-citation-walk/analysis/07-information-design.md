# 07 — Information Design / Communication Layer

Reference for a distinct evaluative layer, not covered by mechanical checks or
aesthetic taste. A future milestone will flesh out its persona and criteria; this
is a first-pass record + a first informal evaluation of this milestone's output
along the vector. No framework asserted.

## Three evaluative layers
| Layer | Question | Evaluated by |
|---|---|---|
| Technical / mechanical | correct & compliant? | script / harness |
| **Information design / communication** | conveys the right thing, well? | reasoned review vs principles |
| Aesthetic / perceptual | looks & feels right? | human taste |

Layer 2 ≠ layer 1 (not a pass/fail script) and ≠ layer 3 (not taste). It is
**agent-evaluable by reasoning with a dedicated persona**. Principle sources:
information theory / fidelity, information architecture, cognitive-load, Gricean
relevance (quantity/relevance), mental-model fit (Norman), Tufte data-ink/density.

**Distinct from real-user feedback:** layer 2 is expert-principled judgment;
real-user feedback is empirical validation of layers 2–3. The synthetic-only
regime precludes real users; empirical validation is deferred, not substituted.

## Why it is central to this product
"Auditable" is an information-design property. A return can pass **every**
mechanical check (correct numbers, compliant contrast, honest blocking) and still
fail to make its reasoning **followable**. That failure is invisible to layers 1
and 3. This layer is the product's core promise and was **not measured** this
milestone.

## Layer-2 criteria (named)
- **Hierarchy fidelity** — visual/structural salience tracks epistemic importance (a block is a louder signal than a published line; the line→source link is the product's point).
- **Relationship legibility** — reuse / composition / dependency are communicated, not reconstructed by the user.
- **Representational faithfulness** — encoding tells the truth about computation structure; derived vs sourced values are visually distinct; nothing implies the UI holds authority it does not.
- **Progressive-disclosure fit** — complexity unfolds at the pace of the user's question (the walk is inherently this shape).
- **Narrative / task comprehension** — a person with a real question can follow the surface as an argument and get the answer efficiently.

## First-iteration evaluation of this milestone's output (informal, retro-applied)
Re-reading existing cycle findings through layer 2:
- **Positive:** walk structure (line→subtotal→source) is inherently progressive-disclosure aligned; C5 reuse backlinks attempt relationship legibility; blocked line always carries reason+remedy (comprehension-supporting).
- **Gaps (already visible in cycle findings, re-labeled as layer-2):**
  - Reuse backlink buried inside a collapsed `<details>` [C4–C5] → **relationship-legibility** failure (the relationship is present but not discoverable pre-expansion).
  - Uniform salience across published vs blocked states [C1–C5] → **hierarchy-fidelity** failure (a block does not read as a louder signal).
  - Subtotal shown as a live client-side sum [C4 B-A] → **representational-faithfulness** risk (implies the UI performed authority-bearing computation).
  - Silent tie-out omission when unverifiable [C4 B-B] → **comprehension** gap (absence of a signal reads as "nothing to see").
- **Not evaluated:** narrative coherence and task-driven comprehension — no persona was applied; no layer-2 seat existed.

## Note on scope
Every layer-2 gap above was found *incidentally* by technical reviewers, not by a
dedicated lens — so coverage is unmeasured and likely partial. Some layer-2
criteria will crystallize into mechanizable checks (e.g. "source link reachable
within N interactions"; "salience order matches a declared importance ranking");
others remain reasoned. Establishing the persona and which criteria mechanize is
future work.
