# Examination — D2 Contribution Boundary, Iteration 1

Date: 2026-07-16. Evidence ceiling: Rung 2. All probes used independently
constructed synthetic data and an ephemeral workspace outside the repository.
Repository code, schemas, tests, and fixtures were read-only.

## Verdict by proposition

**D2-P1 — settled at Rung 2 as a candidate contract, with named production
conditions.** The event is one atomic `contribution` act; asserted
`finding.v2` citizens pin that act and exact document versions; a separate
contribution record accounts for the process. The live run request contains
only revision/adoption/package pins, and a sealed projection boundary supplies
current findings. Raw contribution input is unrepresentable at that boundary.

The committed fixture scenario adapter is not conforming as a live boundary:
the Case-6 probe supplied an unprojected synthetic source and it silently
published `777`. This is useful negative evidence, not an accepted exception.
Production must make that adapter unreachable from live runs and implement the
closed request/projection boundary before D2-P1 is discharged.

**D2-P2 — settled at Rung 2 as a candidate contract.** Manual contribution is
one self-contained event, canonicalized independently of entry order. New
members reuse ADR-0023 transitions. A correction is a later contribution whose
same-fact finding uses ordinary assertion; record-derived currency displaces
the old finding, and existing derivation edges displace dependents. No edit,
withdrawal, forced product sequence, or third standing edge is introduced.

## Required-case examination

### 1. Provenance-bearing facts

- Claim: one contribution produces asserted findings with exact provenance.
- Paper diff: `act-contribution.v1`, `finding.v2`,
  `contribution-record.v1`.
- Behavior: the contribution atomically reuses existing admission semantics.
- Pins: each finding names contribution `{id,version}` and one or more exact
  document `{id,version}` pins.
- Result: positive paper instance validated; a detached contribution id failed
  the declared semantic equality check.

### 2. Runs consume findings, not inputs (mandatory)

- Claim: the live evaluator receives only current projected findings and
  adopted artifacts.
- Paper diff: closed `run-request.v1`; no value-bearing members.
- Behavior: kernel projection + computed currency marshal the current finding
  view; derivation pins the finding actually read.
- Result: a synthetic run published `52000` and pinned asserted-finding id
  `demo-finding-w2-alpha-1-box1`; the candidate live marshaller owns the
  current-state proof that the fixture adapter does not provide.
- Boundary: the run received neither contribution nor evidence content.

### 3. Any-order equivalence (mandatory)

- Claim: W-2/1099-INT contribution order does not govern current fact state.
- Paper diff: self-contained contribution plus canonical internal ordering.
- Probe: two out-of-repository workspaces applied W-2 then interest and the
  reverse using committed member-transition projection.
- Result: both current states were exactly
  `{demo.contrib.interest|tax-year=2025:875,
  demo.contrib.w2|tax-year=2025:40125}` by fact id/value.
- Record order differed, correctly; no step required the other to complete.

### 4. Correction by supersession

- Claim: a later contribution corrects the same fact without editing history.
- Paper diff: `assertions` contains a provenance-bearing `finding.v2` routed
  through ordinary assertion admission.
- Probe: committed ordinary assertion/currency machinery.
- Result: `demo-finding-w2` displaced,
  `demo-finding-w2-corrected` current, family horizon unchanged at
  `demo-w2-h1`; both findings remained in the record.
- Edge result: same-fact correction is the existing root; dependent findings
  use existing derivation edges. No third edge or withdrawal appeared.

### 5. D1 interlock

- Claim: contribution writes only to ADR-0031 live residency `L`.
- Paper diff: none to D1; require its write capability and read-only repo mount.
- Probe: scratch workspace resolved outside the repository; repository status
  showed no change. A throwaway target-gate mutation rejected a repository
  descendant and accepted the scratch root.
- Result: act, findings, and contribution records remain in `L`; no locator,
  value, disposition, or descriptive artifact crosses by contract. The actual
  capability wall remains ADR-0031 production work, not D2 Rung-2 evidence.

### 6. Run reaching raw input (mandatory kill-test)

- Claim: an unasserted value cannot silently reach live derivation.
- Negative probe: the synthetic scenario adapter accepted an unprojected source
  id/value and published `777`; it is explicitly prohibited as a live surface.
- Paper mutation: adding `inputs`, `sources`, `raw_inputs`, or `contribution` to
  `run-request.v1` failed strict validation in every case.
- Result: the candidate boundary closes the bypass structurally; a missing
  current finding can only block. Production must prove adapter unreachability.

## Contracts that emerged

1. The contribution id is the outer act id; no duplicate event identity exists.
2. Contribution/document pins are provenance only, never fact identity or a
   standing edge.
3. The product batch is one atomic act; internal dependency order is not a user
   flow and is canonical rather than entered.
4. Contribution records and derivation records are separate declared kinds.
5. The live evaluator's authority boundary is the current-finding projection,
   not the convenient `RunContext` constructor used by synthetic fixtures.
6. Same-member correction must remain ordinary assertion and must not advance a
   family horizon, exactly as ADR-0023 requires.

## Stop/production boundary

No contribution code, schema, kernel, derivation, test, or fixture was changed.
Required later work is limited to production implementation of the declared
schemas, atomic applicator/record, finding marshaller, and live run boundary,
with the Case-5/Case-6 kill tests. OCR, UI, imports, D1 redesign, D3 package
resolution, multi-party authority, and new tax content remain out of scope.
