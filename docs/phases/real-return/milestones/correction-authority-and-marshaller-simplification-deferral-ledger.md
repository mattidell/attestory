# Correction Authority and Marshaller Simplification — Deferral Ledger

Audience: Shared (status); Product (planning input)

Written 2026-07-22 as the Track 3 completion record. Every deferral this
milestone created, retired, or re-affirmed, so that nothing is silently
closed. Each entry names its origin, why it was deferred (or retired), and
what reactivates it. Entries carried forward from the prior milestone's
ledger (`dividends-schedule-b-slice-deferral-ledger.md`) are marked
**carried**, with a disposition note on whether this milestone touched them.

## Retired this milestone

1. **Free supersession policy** — carried from the Dividends and Schedule B
   Slice ledger (entry 13) and the First Real Return Slice ledger (entry
   10); **retired 2026-07-22** (ADR-0041, Track 1, PR #53). The
   supersession-policy vocabulary is no longer an unrestricted no-op: it
   closes to `free`/`locked`/`closed-on-attestation`, enforced at the
   existing dispatch site in `packages/kernel/findings.py`. Every existing
   fact type still declares `free`, by choice — ADR-0041 compels no
   migration of existing content. The named production condition ("any
   actor supersedes any finding without restriction") is discharged: a
   restriction is now expressible and enforced wherever a fact type's
   content deliberately adopts one. Maturity matrix: Correction &
   supersession lifecycle row raised L3 → L4 across every domain.
2. **Marshaller binding-route duplication** — carried from the Dividends
   and Schedule B Slice ledger (entry 8); **retired 2026-07-22** (Track 2,
   PR #51). The four binding routes in `packages/derivation/marshal.py`
   (explicit input-binding, collectable-source, legacy fallback,
   `marshal_closure_authority`'s mapping loop) no longer each reimplement
   their own fact-id parsing and prefix matching — three shared helpers
   (`_fact_type_id`, `_fact_id_has_type`, `_input_role`) replace the
   duplication, and one dead branch (`mode == "required"` vs. an identical
   `else`) was removed. The four routes themselves were **not** collapsed
   into one loop and this is not a partial retirement: they have genuinely
   different multiplicity semantics (explicit binding takes the first
   match on multiple current findings; the legacy fallback does not dedupe
   by type and can emit one result per match), so forcing a single loop
   would have been an observable behavior change, out of this track's
   scope. The deferral this ledger tracked was the *duplicated logic*
   growing with every track that touched the file, re-flagged and never
   addressed — that risk is retired; the distinct route count is not a
   defect.

## New this milestone

3. **`closed-on-attestation` cross-scope projection** — new. ADR-0041's
   `closed-on-attestation` policy resolves its gate fact's identity by
   projecting the gated fact's own identity-key bindings onto the gate
   fact type's declared key names; this only works when the gate fact
   type's keys are a subset of the gated fact type's own keys (an
   `FindingModelError` is raised explicitly otherwise, never silently
   permitted). Family-level elections gated on a family-level closure fact
   satisfy this today; a per-statement item fact (e.g., a 1099-DIV box
   keyed by payer/statement) gated against a family-level closure fact
   does not share those keys and cannot adopt this policy as implemented.
   No real content needs this today. Reactivate: a future milestone that
   needs `closed-on-attestation` on a fact type not identically keyed to
   its gate.

## Boundary and infrastructure (carried, untouched)

4. **Guarded transport / credential confinement** — carried, **untouched**
   this milestone. Still the ledger's highest-priority entry; still holds
   the data-boundary row at L3 across every domain. Reactivate: a
   separately chartered OS, identity, or hosted-boundary topic (per the
   stopped H1 prototype's disposition).
5. **Operator-level bypass is detected, not impossible** — carried,
   **untouched**. Reactivate: owner decision or the credential-confinement
   hardening topic.
6. **GitHub remote stays private** — carried, **untouched**. Standalone
   owner decision to change; not a defect.

## Contract deferrals (carried, untouched)

7. **Dividend boxes 2a, 3, 5, 7, 12 named honest-block exclusions** —
   carried, **untouched**.
8. **Further positive interest sources and the subtractive-adjustment
   mechanism** (ADR-0026) — carried, **untouched**.
9. **ADR-0028 historical-v1 migration** — carried, **untouched** as a
   migration; this milestone's own schema work (`fact-type.v3`,
   `bundle.v3`) is a second confirmation that the "new version, old stays
   published" pattern generalizes cleanly, without itself constituting a
   migration.
10. **Track 4 F2 scaffold-visibility note** — carried, **untouched**.

## Explicitly not a deferral

- **The Track 1 schema-immutability incident** (an implementation attempt
  widened `fact-type.v1.schema.json` in place and hand-patched its
  checksum before an in-branch correction caught and squashed it, PR #53)
  was a *process defect, caught and corrected before merge*, not a
  deferral — nothing about it is carried forward as outstanding scope. See
  the milestone retrospective for the full account and the process lesson
  drawn from it.
