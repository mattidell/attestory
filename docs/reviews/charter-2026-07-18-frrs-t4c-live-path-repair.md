# Charter: Track 4c — Live Path Repair (F1–F3)

Date: 2026-07-18. Status: **independent review complete; merge-ready awaiting
owner disposition**.
Origin: the foreman's live-path findings record
(`2026-07-18-frrs-t4-live-path-findings.md`). Branch:
`repair/frrs-t4-record-pin-origin`. The owner holds the merge and, per
ADR-0034, dispatches the review seat.

## Deliverables

1. **F1 (carried, implemented):** `derivation-record.v2` pin `$def` aligned
   with `rule-artifact.v2` (`parameter` role; `origin` with the input-pin
   conditional); `published.json` row regenerated. The alignment adds the
   `parameter` role and requires `origin` on input pins; review confirms no
   committed input pin lacks it and that no release/adoption byte changes.
2. **F2 (implemented):** publish `rounding.convention@v1` as an adopted vocabulary fact
   type in a v3 content cycle via `tools/generate_frrs_t4_content.py`
   (immutable v3 bundle + package; registry, Track-3 release, and adoption
   pins regenerated deterministically; every published v1/v2 byte preserved).
   If the builder instead judges rounding an adopted default/parameter, that
   is a **blocking decision surfaced to the owner**, not a silent redesign.
3. **F3 (implemented):** the W-2 closure fact type gains its `family-horizon` entity
   identity key in the same v3 cycle; the closure mapping pins the successor.
4. **The missing golden class (implemented):** an executed test that builds an
   authoritative act log (adoptions, horizons, contribution batches with
   findings, closures, package adoption), runs `live_coordinate_run`, and
   asserts lines publish with values, the paired records validate, and the
   report is the declared output. Plus negative goldens: F2's former
   dead-end (rounding absent → named block) and F3's former unknown-fact
   rejection.
5. **Implemented:** scaffold helper updated for v3 pins (rounding act prefilled; W-2 closure
   restored); remains uncommitted unless the owner promotes it.

## Scope fence

Synthetic only; no personal data, locator, or real-run artifact. No ratified
ADR edits. No new tax lines, UI, or coverage. v1/v2 published bytes are
preserved; repairs are successor versions per the RG-1 precedent.

## Verification

Focused suite incl. the new golden class; full unittest; mypy; governance
lint; regeneration idempotence (generator reproduces committed bytes); data
safety scan; envelope-gate verify.

## Review gate

Author-independent reviewer, chartered at
`charter-2026-07-18-frrs-t4c-live-path-repair-review.md`, dispatched by the
owner (ADR-0034). Measures each deliverable, runs the counter-probes named in
the findings record, and classifies findings before the owner merges.
