# D3 Iteration 2 — Adversary Review

Date: 2026-07-16  
Seat: Adversary reviewer, Medium. Evidence is Rung-2 paper/probe review;
every example below is synthetic.

## Verdict

**D3-P1 and D3-P2 do not survive at Rung 2. ADR-0033 is not supportable.**
Both builds retain the required direction — registry comparison, pin-directed
projection, and an `ok == True` pre-graph gate — but neither establishes the
two authorities on which that direction depends: the exact immutable registry
being read, and one current valid user adoption act. The incumbent additionally
launders most of the required condition ledger into false D3 discharges.

## Measurements

### A1 — Trust-anchor substitution — **decision-blocking, both builds**

Synthetic supply: `demo.package@v1` and `demo.rule@v1` have registry digests
`P`/`M`; an attacker supplies changed bytes `P'`/`M'` plus an `L` catalog that
agrees with them.

- **it3:** §1 calls the registry public and §2 pins a `trust_anchor_pin`, but
  does not define a versioned registry/release citizen, how its bytes are
  compared to that pin, or a required equality between that release and the
  registry used for checks. `L` is therefore not the stated authority, but the
  asserted registry has no independently checked authority either. The committed
  `load_published_*_checksums(path)` APIs likewise accept a caller-selected file
  and authenticate only entries, not registry bytes. **Bypass remains possible
  at the contract boundary.**
- **it4:** §1.1 names an exact release/registry pin, but §1.2–1.3 never require
  the bytes of the repo-resident registries actually read to equal that pin.
  Replacing the selected working-tree registry with one carrying `P'`/`M'`
  makes all specified comparisons agree. Calling it immutable is not a
  verification rule. **Same authority hole.**

ADR-0027 D6/PC3 requires registry-verified package and citizen bytes, not a
registry selected by assertion. A release identity/digest must be verified before
it authenticates the package and every member.

### A2 — Adoption forgery and staleness — **decision-blocking, both builds**

Synthetic workspace `L` contains two otherwise valid adoption records in the
same scope: user act `A` for `demo.safe@v1`, then stale/attacker act `B` for
`demo.changed@v1`; alternatively `B` names actor `automation`.

- **it3:** `AdoptionRecord` has no declared schema/version or current-act rule,
  and its permitted actor is “System or automation.” The Ontology currently
  defines the user as the sole actor; Article 4 requires the user's recorded
  adoption. A caller can choose either record because no currency/supersession
  selection is declared. **Bypassed.**
- **it4:** proposing `act-package-adoption.v1` fixes the missing noun, but
  “current, valid” is asserted rather than defined: no rule selects one act by
  actor, scope, revision, supersession, or exact package/trust-anchor pair.
  Its stale-act examination supplies no such rule. **Authority remains
  caller-selectable.**

The current runner reinforces the risk: its fixture path passes a
caller-supplied `adoption_pin`, and `start_run` checks only that its package id
is in an `adopted_packages` set. D3 must define the replacement live boundary,
not infer one from that fixture helper.

### A3 — Graph injection / enumeration race — **mixed; not independently blocking**

For a synthetic unpinned `demo.evil@v1`, a missing pinned member, and two
different same-key candidates, it4's pin-directed, checksum-matching candidate
admission rejects changed or absent bytes before graph construction and is
independent of glob order. This would preserve ADR-0027 D1/D7 **if A1 and A2
were closed**. it3 says only “locate” each member and declares glob artifacts
inert; it does not state duplicate candidate handling or an order-independent
selection/refusal rule. It therefore does not itself close the same-key race.

### A4 — Fail-open and ledger laundering — **D3-P2 decision-blocking**

Both papers correctly require `validation.ok == True` before a graph, execution,
or rendering. Their clean synthetic success and eight-issue core refusal support
keeping RG-1 as a MUST production prerequisite; the committed fixture runner is
not evidence of production safety because it explicitly continues when
`validation.ok` is false.

- **it3 ledger:** claims all ADR-0027 PC1–PC4 and ADR-0028 PC1–PC3 discharged,
  despite its own D1/D2 installed-wall and marshal proofs being deferred. It also
  collapses ADR-0028 D1–D9 into one sentence. That neither maps each decision
  nor distinguishes contract discharge from Track-3/4 implementation evidence.
  **False discharge / incomplete ledger.**
- **it4 ledger:** is materially more explicit, but marks ADR-0027 PC4 and
  ADR-0028 PC3 merely “Acknowledged,” not a disposition, and says the D1/D2
  interlocks are “honored via” a read-only capability and exclusive marshaller.
  ADR-0031/0032 say those installations remain production conditions; the
  committed `RunContext` is still caller-constructible and value-bearing.
  **Partial ledger laundering.**

### A5 — Residency and contribution boundary — **no paper bypass shown; deferred**

Neither design specifies a resolver write/export/report path from `L` to the
repository, and both limit examples to synthetic scratch `L`. That is consistent
with consuming ADR-0031, not proving its wall. Neither may claim a D2
marshal-only installation: ADR-0032 expressly defers that live-entrypoint
kill-test. These remain carried production conditions, not D3 discharge.

## Proposition result

| Proposition | Result |
| --- | --- |
| D3-P1 | **Fails.** Registry anchor verification and current user adoption authority are both undefined; it3 also leaves same-key supply arbitration underspecified. |
| D3-P2 | **Fails.** it3 is non-exhaustive/overclaims; it4 leaves required entries unclassified and overstates D1/D2 installation. |

The next evidence must exercise a registry-release byte mismatch and competing,
stale/non-user adoption acts, then carry an item-by-item ledger that classifies
rather than asserts every named ADR-0027/0028 condition.
