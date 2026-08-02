# ADR 0008 — Derivation Record Placement and Timing

- Status: accepted (ratified 2026-07-10)
- Tier: 2
- Date: 2026-07-10

## Context

Where do run records live relative to the act log (ADR-0002), and when are they written? The evidence chain runs through three exhibits: it0's run-record timing tension (`harvest-notes.md`), it1's finding that a final-only record is not enough (`examination-it1.md` Q9 negative evidence), and it2's implemented start/completion pair (`examination-it2.md` Q9) (`evaluation-analysis.md` C4).

## Decision

1. **Derivation records are their own citizen kind, not act-log entries.** Publication acts (ADR-0007) land in the act log; each references its `run_id`. Records account for runs; acts account for record-entering claims. The two are linked by id, never merged.
2. **Paired immutable records bound every run.** A run first writes an immutable record with phase `started`; publication acts may then accumulate; a separate immutable record with phase `completed`, `interrupted`, or `failed` closes the run with its outputs, blocks, and a declared `stop_reason`. Recovery after a crash adds a closing record — it never mutates the start record. This closes the orphan-publication window: any publication act is attributable to a started run even if completion never came (C4).
3. **The completion record is structured data**: published findings, schema'd blocked entries, governance/adoption pins, workspace revision. Narrative-free (charter Q3; both iterations).
4. **Completeness legibility condition**: the record vocabulary must let a reader distinguish evaluated-and-inapplicable rules from rules never reached — a completed record that is signature-identical to an unsaturated snapshot is a defect the evidence demonstrated (`round-2-adversary.md` attack 9; analysis C10c).

## Consequences

- Derivation Machinery implements record storage with the same append-only, immutability discipline as the act log, as a separate stream.
- Ratification condition inherited from the analysis (§5.5): the pair's crash-window guarantees are proven conceptually, not yet against real atomic storage writes (E6.1/E14.1); storage-level fault-injection evidence is required in the machinery milestone.

## Links

- Evidence: `docs/archive/2026-08-02-milestone-artifacts/prototypes/rule-language/evaluation-analysis.md` (C4, C10, §5)
- Prior contract: ADR-0002 (append-only act log)
- Companions: ADR-0006, ADR-0007
