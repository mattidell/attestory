# Delta Review Charter — Foreman Context Loading M3

Status: **prepared; no reviewer is authorized by this charter.** The owner must
explicitly approve the delta reviewer dispatch under ADR-0034.

## Context Capsule

- **Source ref:** `repair/foreman-context-loading-m3`; resolve and record its
  commit immediately before dispatch.
- **Object:** `18ef0f5..repair/foreman-context-loading-m3`.
- **Role:** the original Foreman Context Loading reviewer, reused only along its
  own review lineage for this delta check.
- **Scope:** M3 only — the `AGENTS.md#Schema Publication Protocol` deep-read
  fragment, its capsule rendering, and the directly related re-entry records.
- **Stop conditions:** no real workspace, credential, remote, personal output,
  location, scope expansion, or new finding outside this delta.
- **Full reads before acting:** the original review report,
  `docs/adr/0042-foreman-context-capsule.md`, the active milestone plan,
  `AGENTS.md` Schema Publication Protocol, and this charter.

## Measurement

1. Resolve the source ref and render
   `tools/foreman_context.py --ref <resolved-ref> --format markdown`.
2. Confirm its `schema_or_fixture` target exactly names
   `AGENTS.md#Schema Publication Protocol` and that this heading exists in the
   selected committed blob.
3. Confirm the repair does not alter the renderer, deep-read map, role-capsule
   policy, or data boundary beyond the M3 heading/pointer-status records.
4. Rerun the focused capsule test and the verification floor named in the
   original review charter.

## Verdict

Return `READY` only if M3 is genuinely discharged. Otherwise return `NOT
READY` with the exact remaining mismatch. Do not reopen other already-passing
measurements or add new scope.
