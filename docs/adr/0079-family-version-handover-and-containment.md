# ADR 0079 — Family-Version Handover and Containment

- Status: **accepted** (2026-10-19, by the owner, after independent review of
  the proposal and of its implementation).
- Tier: 2 — a kernel and schema contract governing horizon lifecycle, cross-version succession, and source authority, not a product-thesis or governance-meaning decision.
- Date: 2026-10-19

## Context

The multiple-statement circumstances milestone consolidates circumstance routes (such as Form 1099-K personal item sales) so each statement keeps its own account, answers, and result, combining figures into a return entry (e.g. Schedule 1) only where tax rules combine them. Supporting multiple statements requires versioned source families to evolve across package iterations (for example, the Form 1099-K family's successor that authorizes a multi-statement sum, published separately as `family.f1099k.v2.json`).

An earlier exact-version candidate narrowed horizon lookup in `packages/derivation/marshal.py` to `c_ver == version`. In doing so, it newly admitted workspaces containing multiple current horizon chains for the same family ID and scope (the "both-current" defect: independent review showed that a member added through the other current version left the selected version's closure and its saved zero current). When a successor version was recorded beside an existing v1 chain, both chains remained current in `HorizonState.current_by_chain`. The adopted version was silently admitted, masking the absence of true succession and potentially allowing contradictory or uncoordinated version authorities to coexist.

Furthermore, synthesizing version upgrades from existing acts (such as `entity-superseded` followed by a new `act-horizon-genesis.v1`) proved deficient:
1. `apply_entity_superseded` marks entities superseded in the fact lattice, but leaves `HorizonState.current_by_chain` active, permitting later transitions on the old version.
2. `act-horizon-genesis.v1`'s published schema definition mandates `predecessor: null` before members exist, making it unsuitable for upgrades that explicitly succeed an existing horizon.
3. Disk atomicity without a prospective kernel fold leaves replayed logs vulnerable to late crashes during projection.

A durable, explicit contract is required to govern the atomic handover of write authority between source-family versions, remember the retirement of superseded versions, and contain ambiguous historical logs.

## Decision

Establish the family-version handover contract, remembered retirement, and containment rules across the kernel, schema registry, and derivation marshal layers, recording the owner's choices on trigger and fold scope.

### 1. Dedicated Handover Act (`act-family-handover.v1`)

Introduce a dedicated act kind `family-handover` with published payload schema `act-family-handover.v1` (`packages/schemas/kernel/act-family-handover.v1.schema.json`). The envelope `act.v1` admits the kind by pattern; its payload resolves through `_payload_schema_id` without envelope modifications.

The payload carries coordinates only:
- `predecessor`: `family` (`id`, `version`), `scope`, and `horizon_id`.
- `successor`: `family` (`id`, `version`), `scope`, and `horizon_id`.

Handover is admitted if and only if all of the following hold atomically:
1. **Identity & Scope Match:** `predecessor.family.id == successor.family.id` and `predecessor.scope == successor.scope`.
2. **Version Distinction:** `predecessor.family.version != successor.family.version`.
3. **Predecessor Currency:** `predecessor.horizon_id == current_by_chain[(family.id, predecessor.version, scope)]`, `state.horizon_state.horizons[predecessor.horizon_id].status == "current"`, and `state.fact_state.entities[predecessor.horizon_id].status == "current"`.
4. **Single Active Chain:** Across all versions for that `(family.id, scope)`, exactly one chain key exists in `state.horizon_state.current_by_chain`.
5. **Absent & Unretired Target:** `(family.id, successor.version, scope)` is absent from `current_by_chain` and not in `state.horizon_state.retired_chains`.
6. **Fresh Successor Horizon ID:** `successor.horizon_id` is unrecorded in `state.horizon_state.horizons` and `state.fact_state.entities`.

Failure of any precondition results in an atomic `HorizonModelError` rejection leaving workspace state completely unmutated:
- Predecessor not current: `"predecessor horizon is not current"`.
- Successor chain already exists or multiple chains active: `"successor chain already exists or ambiguous active authority"`.
- Successor chain previously retired: `"successor chain is retired"`.
- Reused successor horizon ID: `"horizon id already recorded"`.
- Scope mismatch or identical versions: `"malformed handover payload"`.

### 2. Cross-Version Predecessor (Supplement to ADR-0017 Decision 1)

ADR-0017 Decision 1 established:
> *"Each versioned source-family declaration and scope has an ordinary recorded membership-horizon citizen with explicit succession."*

This decision supplements ADR-0017 Decision 1 by explicitly norming cross-version lineage for initial successor horizons. When `family-handover` establishes the successor horizon citizen (`family-horizon.v1`), its `predecessor` field names the predecessor horizon ID across family versions.

Published `family-horizon.v1.schema.json` already defines `predecessor` as string or null; published `act-horizon-genesis.v1` continues to represent genesis before any member exists (`predecessor: null`). Neither published schema is modified.

### 3. Remembered Retirement

`HorizonState` maintains `retired_chains: frozenset[ChainKey]`. Upon handover, the predecessor chain key `(family.id, predecessor.version, scope)` is removed from `current_by_chain` and added to `retired_chains`.

In the pure fold:
- `apply_genesis` refuses any genesis whose chain key is present in `retired_chains` with `HorizonModelError("family version is retired")`.
- `apply_transition` refuses any member-transition whose chain key is present in `retired_chains` with `HorizonModelError("family version is retired")`.
- `apply_handover` refuses any downgrade or reverse handover whose successor chain key is present in `retired_chains` with `HorizonModelError("successor chain is retired")`.

### 4. Containment Rule for Both-Current Logs

`marshal_closure_authority` in `packages/derivation/marshal.py` refuses closure authority when more than one version chain is current for the same family ID and scope, raising `SourceAuthorityError("family has multiple active version chains")`.

A workspace log that historically contains multiple current chains remains readable via `ActLog.read` and `project`, but its ambiguous authority is refused during calculation. The saved zero or prior result stays current, and calculation fails closed. Handover is refused on such a log under Precondition 4 ("Single Active Chain"). There is no supported handover repair for a both-current log.

### 5. Owner Choices: Handover Trigger and Pre-Save Fold Scope

The owner approved two production design choices:
1. **Automatic Handover on Successor Write (Option A):** When a durable writer opens a horizon under a successor version and finds an active predecessor chain in scope, it stages `family-handover` in the same all-or-none `append_batch` save as the first successor write. Writers avoid creating concurrent version chains without requiring an out-of-band manual upgrade step.
2. **Targeted Pre-Save Fold Scope:** In `ActLog.append` and `append_batch`, prospective fold validation before persistence covers lifecycle act kinds only (`horizon-genesis`, `member-transition`, `family-handover`), alongside the new-write second-genesis refusal rule. Direct closure assertions against a retired horizon are not folded at save time; they fail later during workspace `project`.

### 6. Invariants and Reliance on ADR-0017 and ADR-0077

- **ADR-0017 Decision 3 (Member Transitions):** Same-version member transitions remain unchanged. Handover is an explicit act kind for version transitions, not an overloaded member-transition.
- **ADR-0017 Decision 5 (Individuation Root):** Predecessor horizon supersession in `fact_state.entities` feeds the existing superseded-entity root (`packages/kernel/facts.py:228`) and individuation cascade (`packages/kernel/currency.py:156-168, 225`). Closure facts keyed on the predecessor horizon entity drop automatically. Retained statement facts (whose identity keys are e.g. payer, statement, tax-year) survive intact. No new currency root or third edge is introduced.
- **ADR-0017 Decision 6 & 7 (Currency and Re-attestation):** Currency projection agrees across rebuilds. Displaced closures stay displaced. Handover authorizes nothing by itself: an explicit fresh closure attestation and rerun under the successor version are required before successor closure-backed results can publish.
- **ADR-0077 Decision Part 5 (New-Write Step):** The pre-persistence boundary on `ActLog.append` and `append_batch` enforces prospective fold checks and the new-write-only second-genesis rule. Historical replay (`project`) never gains the second-genesis rule.

## Consequences

1. **Older engine compatibility:** An older engine lacking the `act-family-handover.v1` schema will fail to parse any log containing a handover act, raising `ActLogCorruption` on `ActLog.read`. Historical-prefix replay is valid only up to the slice preceding the handover.
2. **Completeness re-attestation:** Handover drops earlier closure facts and their derived figures (such as pinned zeros or subtotals). A person must answer completeness again under the successor version before closure-backed results can publish.
3. **Both-current containment:** A workspace containing historical concurrent version chains has no supported repair within handover; it remains readable, but calculation refuses authority and fails closed.

## Not Decided

1. **Successor family shapes:** The shape, predicates, and closure claim of any successor family are outside this ADR. The Form 1099-K successor is published as `family.f1099k.v2.json` by the multiple-statement milestone.
2. **Full pre-save fold:** A general pre-save fold for non-lifecycle acts (such as assertions) is not built; targeted lifecycle validation covers chain-moving acts only.
3. **Recovery of both-current logs:** No automated repair or migration is provided for logs containing concurrent version chains.
4. **Untouched workspace reader presentation:** Presentation surface indicators for an untouched workspace (where earlier v1 figures stand while a new package does not calculate) are outside kernel scope.

## Evidence

- Proposal: `docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances-evidence/family-handover-contract-proposal.md`
- Lifecycle comparison: `docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances-evidence/family-version-lifecycle.md`
- Executed lifecycle evidence: `track0-closure-evidence.md` and `test_track0_closure_probe.py` in the same directory, and the handover tests (`tests/test_family_handover_*.py`).
