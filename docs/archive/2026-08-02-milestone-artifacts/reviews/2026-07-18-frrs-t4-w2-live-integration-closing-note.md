# Track 4 closing note — W-2 closure and live integration

Status: implementation landed on its Track-4 branch; review and owner merge are
still required. This note contains synthetic evidence only. It does not record a
workspace locator, personal value, personal identifier, disposition, report, or
real-run attestation.

## What this closes

The immutable `tax.us.2025.package.core-calculations@v2` repairs RG-1 without
changing a published v1 byte. Its W-2 source family and closure mapping are
adopted members, pin exact v2 W-2 fact types, use a family-horizon identity, and
give wages the declared `wages` quantity in the admitted quantity vocabulary.
Only exactly one current literal-boolean `true` closure admits an empty W-2
family; false, absent, displaced, non-boolean, and duplicate closure evidence
does not. Present W-2 wages still aggregate without closure authority.

The live coordinator starts from a runtime `WorkspaceCapability`, fixed revision,
declared scope, and the authoritative act sequence. It bootstraps `L`, resolves
the sole current user adoption through the verified release/registry/package
chain, derives run material from the exclusive resolved graph, marshals record
state, writes a paired run account and exactly one declared report below `L`.
A resolution refusal returns before a run record or output is created.

## ADR-0033 §4 ledger disposition

| Row | Track-4 disposition |
| --- | --- |
| ADR-0027 D2 role canon | `role-canon.v1` is an immutable core-v2 member and a graph dependency. |
| ADR-0027 D5 form-field producer integrity | Enforced by the hard package validator over the repaired v2 graph. |
| ADR-0027 PC1 / PC2 | Existing exclusive-graph goldens continue; Track 4 adds a physical-layout duplicate probe. |
| ADR-0028 D1–D4 | Versioned bundle/fact members, dual fact surface, mapping exact pins, and wholesale package validation are exercised by core-v2 resolution. |
| ADR-0028 D5–D8 | Package-declared composition, full binding, closed quantity vocabulary, and same-quantity force-declare remain enforced by `validate_package`; core-v2 passes with no allowlist. |
| ADR-0028 D9 / PC1 / PC1b | Successor schemas are admitted and the validator’s reject/accept probes run in the focused suite. |
| Track-3 F2/F3/F4/F6/F7 | Sealed marshal token; installed integrity-checked envelope entrypoints; physical layout probe; exact byte-substitution refusal; one resolver-to-record-state coordinator. |

## Explicit deferrals

- ADR-0028 historical-v1 migration remains deferred. Core v1 intentionally
  remains a hard-gate refusal with its original eight contained issues.
- The owner-held real run is not performed by this Track. No report or
  disposition from it may enter Git.

## Owner-held quarantined run boundary (after merge only)

At runtime, outside this repository, the owner supplies a `WorkspaceCapability`
for the quarantined live residency and calls `live_coordinate_run` with the
authoritative live act sequence, revision, scope, request, and publication
surface. No locator is accepted from repository content. The permitted later
attestation states only: the run occurred in quarantine, dispositions were
observed there, and no artifact crossed the boundary. It must not say which
disposition occurred or describe any value.
