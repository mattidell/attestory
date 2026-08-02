# Evaluation — Attachment Ontology (D1), round 1

Foreman disposition record (Gate 5 triage), 2026-07-19. Advisory reviews:
`reviews/governance-r1.md`, `reviews/adversary-r1.md` (independent seats,
Medium/High). Owner decides disposition; Tier 3.

## Verdict: split — neither design converges as submitted

- **it1 (incumbent):** governance-sufficient on all three propositions (its
  state model reuses the ratified disposition triad, zero new machinery,
  ADR-0012-atomic). Adversary decision-blocking twice: its Part III
  completeness `choose` masks one answer behind the other, so a
  required-incomplete attachment can publish whole (the exact core-promise
  failure); and its divergence-guard citation misapplies committed behavior
  (`runner.py:279` fires only on the empty-family path), leaving the P2
  tie-out unguarded as designed.
- **it2 (rival):** adversary-clean (no decision-blocking finding; sound
  completeness `all(...)`, explicit supersession posture, stronger row
  pinning via a new, honestly-flagged `collect_members` mechanism).
  Governance decision-blocking once: it collapses not-required and
  required-complete into one `published` disposition distinguished by an
  embedded state value — departing from ADR-0012 atomicity.
- Both pass the mandatory generalization stub (case 6), the threshold
  boundary (over-$1,500, cited, testable), and block-propagation direction 1
  (verified against committed runner source: no line rule can reference the
  attachment symbol).

## Converged shape (foreman synthesis — requires confirmation, see below)

Each element is builder-designed and reviewer-checked; the synthesis
combines them: **it1's state model** (three states as atomic dispositions on
the ratified triad — resolves G1) carrying **it2's semantics** — `all(...)`
completeness over every required Part III answer (resolves it1's mask),
it2's supersession posture (an attachment never stays current over a
non-current answer), and it2's row pinning (`collect_members`, a named new
mechanism) with the tie-out as a declared relation whose violation is a
hard error using committed-consistent error semantics (it2's
`DEPENDENCY_INVALID` emission is not committed behavior — the correct code
is part of the confirmation pass). Shared fixes adopted: `SOURCE_SET_UNCLOSED`
(both cited a nonexistent code), and the 1099-shaped row model (payer +
single amount) recorded as a hardening note — the ADR's row citizen must
leave row shape to per-schedule content.

## Confirmation pass (recommended, per the ADR-0013 2026-07-15 amendment)

The synthesis is foreman-assembled and therefore defaults to a **scoped
confirmation pass** before it enters ratifiable ADR text — recommended
proactively, single reviewer seat, **High tier** (core-promise ground),
narrow charter. Named cases it must exercise, including the directions
opposite the original findings:

1. **Over-blocking (opposite of it1's finding):** a fully complete required
   attachment publishes — `all(...)` must not over-trigger (a "no" answer
   is an answer).
2. Each Part III fact absent individually blocks (under-blocking re-check).
3. Not-required as an atomic published disposition — the G1 resolution
   actually holds ADR-0012.
4. Tie-out divergence both directions (stale row vs stale line), hard error
   with a committed-consistent code.
5. Supersession both ways: late-contributed answer; superseded answer under
   a current attachment.
6. Generalization re-check of the synthesized citizen on the Schedule D
   stub.

## Cap state and authorization ask

Topic ≈ 1,560 lines with this record, inside the 1,600 target; the
confirmation pass (charter + synthesis note + one review) exceeds it. Owner
authorization is therefore required for the pass on both grounds (not
pre-authorized; cap). Estimated extension: ≤ 350 lines.

## Other dispositions

| Finding | Class | Disposition |
| --- | --- | --- |
| it1 A1-dir2 (completeness mask), A2 (guard citation) | Decision-blocking | Resolved in synthesis; confirmation case 1–2, 4. |
| it2 G1 (state-in-value) | Decision-blocking | Resolved in synthesis (it1 state model); confirmation case 3. |
| it2 tie-out error code | Non-blocking | Corrected in synthesis; confirmation case 4. |
| Both: 1099-shaped row model | Hardening | ADR text: row shape is per-schedule content. |
| Both: `SOURCE_SET_OPEN` naming | Minor | Corrected to `SOURCE_SET_UNCLOSED`. |
| it2 G3 (production-shaped ids vs `demo-*`) | Process nonconformance | Recorded; no data exposure (governance-verified). Charter language tightened next topic. |

## Outcome

No ratifiable shape yet. On owner approval of the confirmation pass: foreman
writes the synthesis note (≤80 lines), one High-tier reviewer exercises the
six named cases, and — findings permitting — candidate ADR-0036 is drafted
from the confirmed shape for Tier 3 ratification.
