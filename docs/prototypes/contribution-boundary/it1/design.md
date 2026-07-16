# D2 Contribution Boundary — Incumbent Design (Iteration 1)

Status: Rung-2 candidate for D2-P1 and D2-P2 only. This is a paper contract,
not production code. ADR-0031 is an input: every artifact below that contains or
describes a live contribution resides in the out-of-repository live workspace
`L`; the repository supplies code and public contracts read-only.

All examples are independently constructed from public schemas and contracts.
The names, identifiers, and values are synthetic.

## 1. Contract in one sentence

A contribution is one atomic `act.v1` of kind `contribution`: it captures the
documents and declarations the user contributed and applies ordinary kernel
evidence/entity admission, ADR-0023 member transitions, and same-fact
assertions as one complete workspace transition. Each resulting asserted
finding carries exact, non-standing provenance pins to that contribution act
and its source document version. A live derivation request carries only a
workspace revision plus adoption/package pins; the derivation boundary obtains
current findings from the kernel projection and has no field or capability for
contribution payloads, evidence content, or caller-supplied values.

## 2. Declared citizens and successor schemas

These are paper diffs. Published v1 schemas remain immutable.

### 2.1 `act-contribution.v1`

The contribution citizen is the `act.v1` envelope itself. Its `act_id` is the
contribution id; its kind-specific version is `v1`. The payload is closed:

```json
{
  "schema": "act.v1",
  "act_id": "demo-contribution-w2-a",
  "kind": "contribution",
  "actor": "demo-user",
  "at": "2026-01-02T00:10:00Z",
  "committed_against": 8,
  "payload": {
    "documents": [{"schema": "evidence.v1", "id": "demo-document-w2-a",
      "kind": "demo.document.w2", "label": "Synthetic W-2 document", "content": {}}],
    "entities": [{"schema": "entity.v1", "id": "demo-slip-a",
      "kind": "demo.w2-slip", "label": "Synthetic W-2 slip"}],
    "member_transitions": [{
      "family": {"id": "demo.family.w2", "version": "v1"},
      "scope": {"subject": "demo-subject", "tax-year": "2025"},
      "member": {"action": "assert", "finding": {
        "schema": "finding.v2", "id": "demo-finding-w2-a",
        "fact_id": "demo.w2.amount|slip=demo-slip-a,year=2025",
        "value": 40125, "basis": "documentary",
        "provenance": {
          "contribution": {"id": "demo-contribution-w2-a", "version": "v1"},
          "documents": [{"id": "demo-document-w2-a", "version": "v1"}]
        }
      }},
      "successor": {"id": "demo-w2-h1", "predecessor": "demo-w2-h0"}
    }],
    "assertions": []
  }
}
```

The schema has `additionalProperties: false` at every layer. `documents` and
`entities` are exact existing citizens. `member_transitions` is the closed
ADR-0023/`act-member-transition.v1` shape lifted only to carry `finding.v2`.
`assertions` is an array of `finding.v2` payloads admitted by the ordinary
assertion rules; in this charter it carries same-member corrections, while the
name remains honest for future non-family first assertions. At least one
transition or assertion is required. There is no
`raw_inputs`, `fields`, `draft`, or staging member.

The embedded evidence/entity declarations avoid a prerequisite product step:
one user-confirmed contribution may introduce everything its facts need. An
implementation may also reference already-current citizens, but must never
require a separate wizard step; that alternative would still be one event.

### 2.2 `finding.v2`

`finding.v2` succeeds `finding.v1`; it does not mutate it. It retains `id`,
`fact_id`, `value`, `basis`, and optional verbatim `capture`, and replaces bare
`evidence_ids` with exact provenance:

```json
"provenance": {
  "contribution": {"id": "demo-contribution-w2-a", "version": "v1"},
  "documents": [{"id": "demo-document-w2-a", "version": "v1"}]
}
```

Both pins require `{id, version}` and reject extras. A documentary finding
requires at least one document pin. Admission requires the contribution pin to
equal the outer act id/version and every document pin to name an embedded or
already-current evidence citizen at that exact schema version. These are
provenance relations, not fact identity and not derivation/individuation edges.
The document pin's id identifies the immutable evidence citizen and `version`
identifies its schema version; a replacement document has a new evidence id.
Evidence replacement changes standing; it never rewrites this historical pin.

### 2.3 `contribution-record.v1`

Contribution and run remain distinct Article-14 processes. A contribution has
a started and a completed/failed immutable process record in `L`, carrying:

- record id, phase, starting workspace revision, governance pins;
- the contribution `{id, version}` when admitted;
- produced finding pins and displaced finding pins on completion;
- a closed stop reason and validation failures, without a second raw-value copy.

The started record precedes admission. The complete contribution is one act-log
append, so interruption before it leaves only a started record and interruption
after it leaves a valid committed act plus an open process record. Neither cut
requires a later fact write to make the workspace true.

### 2.4 `run-request.v1` and the finding projection boundary

The live run request is also closed:

```json
{
  "schema": "run-request.v1",
  "run_id": "demo-run-a",
  "workspace_revision": 9,
  "adoption": {"id": "demo-adoption-a", "version": "v1"},
  "package": {"id": "demo-package-a", "version": "v1"}
}
```

It has `additionalProperties: false`. In particular, `inputs`, `sources`,
`raw_inputs`, `contribution`, `evidence`, and value-bearing fields are absent and
therefore invalid. The production boundary performs this fixed composition:

```text
run request -> act-log revision -> kernel projection -> computed currency
            -> current finding view -> package bindings -> sealed evaluator
```

The evaluator receives typed projected findings `(fact id, finding id, schema
version, value)` and adopted artifacts. It receives neither the act log nor
evidence/contribution citizens. Its existing internal `InputFinding` and
`SourceFact` values are therefore marshalling products of current findings, not
caller inputs. The synthetic scenario loader remains a fixture-only adapter and
is not a live-run entrypoint.

## 3. Admission canon

1. Validate the closed contribution payload and all nested declared citizens.
2. Require the outer contribution pin and document pins on every finding.
3. Resolve documents/entities against the tentative state; reject dangling,
   wrong-version, non-current, or cross-contribution pins.
4. Canonicalize embedded operations by family, scope, fact id, then finding id;
   construct and validate each same-family horizon-successor chain in that
   canonical order. User entry order is not execution order and carries no
   meaning.
5. Apply evidence/entity introductions to a tentative projection.
6. Apply each new member through the existing ADR-0023 member-transition
   validator, including exactly one valid horizon successor per transition.
7. Apply each `assertions` member through the existing ordinary assertion
   validator; for a family member, reject it unless the same fact is already
   current, so a new member cannot bypass ADR-0023.
8. If any check fails, append no contribution act. If all pass, append the one
   complete act against its declared revision; replay reconstructs the same
   state by the same canon.

This is a specialized act, not a generic tagged transaction container. It adds
no standing-affecting edge. Same-fact correction creates the existing correction
root; downstream displacement follows existing derivation edges. Horizon
succession remains the existing individuation root.

## 4. Required cases

### Case 1 — provenance-bearing contribution

Claim: a manually entered batch becomes asserted findings in one event.
Contract change: `act-contribution.v1`, `finding.v2`, and
`contribution-record.v1`. Kernel behavior: strict validation, tentative reuse of
existing evidence/entity/member-transition/assertion applicators, one atomic
append. The paper validator accepted the positive shape and the semantic
outer-id equality check rejected a detached contribution pin. Result:
`demo-finding-w2-a` pins contribution
`demo-contribution-w2-a/v1` and document `demo-document-w2-a/v1`; neither pin
participates in fact identity or standing cascades.

### Case 2 — a run consumes findings, not contribution input

Claim: a live run can name only a workspace revision and adopted machinery.
Contract change: closed `run-request.v1` plus the current-finding projection
boundary. Kernel/derivation behavior: currency chooses current findings; package
bindings marshal those findings; derived outputs pin the finding ids actually
read. Result: the committed-run probe published synthetic value `52000` and its
derived finding pinned `demo-finding-w2-alpha-1-box1`, the asserted-finding id
supplied by the committed synthetic scenario. The proposed live marshaller—not
that fixture adapter—must establish that the supplied id is current. No
contribution/document citizen was supplied to the evaluator.

### Case 3 — anti-wizard / any order

Claim: W-2 then 1099-INT and 1099-INT then W-2 reach the same current fact
state. Contract change: one self-contained event, canonical operation order, no
prerequisite flow state. Kernel behavior: the throwaway probe appended the two
ADR-0023 transitions in both orders to separate synthetic workspaces. Result in
both: `{demo.contrib.interest|tax-year=2025: 875,
demo.contrib.w2|tax-year=2025: 40125}`. Act history may differ—as it must—but
the current fact/value state does not; the paper pins bind event identities,
not sequence positions.

### Case 4 — correction by supersession

Claim: correction is a later contribution, never an edit or withdrawal.
Contract change: the later contribution places `finding.v2` in `assertions`.
Kernel behavior: ordinary same-fact assertion and record-derived currency.
Probe result: synthetic `demo-finding-w2` became displaced,
`demo-finding-w2-corrected` became current, and the W-2 horizon stayed
`demo-w2-h1`. Both contribution acts and both findings remain in history;
dependent derived findings displace through existing derivation edges.

### Case 5 — D1 quarantine interlock

Claim: a contribution can write only within `L`. Contract change: none to D1;
the contribution entrypoint requires the ADR-0031 write capability for `L`, has
the repository mounted read-only, and returns no descriptive artifact across
the boundary. Kernel behavior: act and contribution records use workspace-local
stores. Probe result: both synthetic scratch workspaces resolved outside the
repository and repository status remained unchanged. A throwaway mutation of
the proposed target gate rejected a repository descendant and accepted the
outside scratch root. This is Rung-2 contract evidence, not a claim that D1's
production capability wall is already installed; contribution must require
that wall when Tracks 1/3 discharge ADR-0031.

### Case 6 — explicit raw-input kill-test

Claim: a caller cannot make a live run elaborate a value that has no current
finding. The probe found the present synthetic scenario adapter will accept an
unprojected source id/value and publish `777`; that adapter therefore cannot be
the live boundary. Under `run-request.v1`, throwaway strict validation rejected
each injected field: `inputs`, `sources`, `raw_inputs`, and `contribution`.
Because a contribution persists accepted values only as findings (and evidence
kept behind the projection boundary), the evaluator has no alternate raw store
to consult. A missing current finding blocks through the existing dependency
disposition; it cannot silently succeed.

## 5. Rung-2 findings and production conditions

The paper schemas accepted the positive contribution and run request, rejected
a finding detached from its outer contribution, and rejected every raw-input
run field. Committed kernel probes established any-order convergence and
correction semantics. Committed derivation probes established both compatibility
with projected finding pins and the synthetic fixture adapter bypass that the
live boundary must foreclose.

Production must add the versioned schemas/manifest entries, atomic contribution
applicator and records, finding-to-run marshaller, and a live entrypoint whose
only request is `run-request.v1`. Its kill tests must prove: direct fixture
scenario loading is unreachable from the live entrypoint; unknown/non-current
finding ids block; injected value-bearing request fields reject; the evaluator
cannot receive evidence or contribution citizens; and all writes remain inside
the ADR-0031 capability. These are implementation conditions, not authorization
to change production in this iteration.

OCR/parsing, UI sequencing, import modes, multi-party authority, D1 mechanics,
new tax content, and production package resolution remain outside D2-P1/P2.
