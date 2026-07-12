# Round 2 Adversary Review — Source-Family Semantics

Date: 2026-07-12  
Seat: adversary reviewer, Medium/medium  
Evidence rung: paper and static-table only

I reviewed `round-2.md`, this seat's charter, the two paper rivals, the
round-1 triage, and the integrated repair evidence. I did not read the
same-round peer review. No code or production contract was available to run;
the exhibits below are the declared paper behavior and the repair's ordered
state table.

## Dissent

I dissent from treating SFS-P3 as settled. The repair correctly identifies the
state that must result from a late member, correction, or removal, and it
correctly shows that ADR-0010 cannot reach a member that was not an input to the
old empty zero. But the required freshness-currency relation is named rather
than demonstrated. Until that separate boundary is decided and evidenced, the
paper does not establish that a false closure-backed zero cannot remain
current.

SFS-P1 and SFS-P2 are settled at the semantic paper level in the repair,
subject to the stated production validation obligations. The original rivals'
prose points in the same direction, but their naming and wiring defenses are
not as explicit or complete as the repair's authoritative declaration.

## Method

I reapplied every round-2 attack to `it1`, `it2`, and `repair1`:

1. a consistently misleading family name;
2. a shortened/broadened coverage label;
3. wiring a narrow subtotal as a broader final result;
4. a late member asserted after an empty closure, without manual withdrawal;
5. correction of an existing member; and
6. displacement/removal of a member.

For each attack, an attack is resisted only where the paper's named claim,
predicate, consumer boundary, or state transition actually rejects the
substitution. A statement that a future validator or currency mechanism must
reject it is recorded as a requirement, not as evidence that it already does.

## P1/P2 substitution measurements

### 1. Consistent mislabel: box-1 family named `taxable-interest`

- **it1 — partially resists, but the attack remains a naming seam.** It1 says
  the declaration, not a reused label, supplies meaning, and its failure map
  rejects a claim saying “all interest” when the members are box 1. However,
  it does not make the exact claim the authoritative presentation required of
  every consumer. A family can still be consistently called
  `taxable-interest` while its internal box-1 declaration is narrower.
  **Exhibit:** `it1/design.md:9-24,81-90`.
- **it2 — partially resists, with the same residual seam.** The
  closure-domain invariant says a label cannot broaden the named predicate,
  and the rejected alternative demonstrates why the broad claim is false.
  But “surrounding artifacts must name the same proposition” is a paper
  constraint, not a demonstrated authoring/display check. **Exhibit:**
  `it2/design.md:8-16,42-56,156-166`.
- **repair1 — resists semantically.** The versioned declaration makes the exact
  claim and canonical predicate jointly authoritative. A misleading id/title
  remains only an alias; an exact “all taxable interest” claim fails authoring
  when the predicate excludes non-form and box-3 members. **Exhibit:**
  `repair1/design.md:9-32`; `examination-repair1.md:7-17`.

### 2. Shortened coverage label: “interest complete” for B1

- **it1 — stated resistance, not independently load-bearing evidence.** Its
  coverage consumer is the box-1 family and its case 6 rejects “taxable
  interest complete,” but the paper does not require coverage to present or
  pin the exact closure claim. A shortened readout remains the attack surface
  triage identified. **Exhibit:** `it1/design.md:14-18,53-65,83-89`.
- **it2 — stronger stated resistance.** Coverage is explicitly `K(B1)`, and
  the design says it reports neither TI nor L2B coverage. The attack is
  rejected by the invariant if the consumer honors its declaration; no
  implementation evidence proves that a display/rollup cannot replace the
  subject with a shorter label. **Exhibit:** `it2/design.md:42-56,104-110,120-131`.
- **repair1 — resists semantically.** Coverage is bound to the exact claim and
  current records; an alias cannot become a coverage-complete conclusion.
  This is the clearest repair of the shortened-label attack. **Exhibit:**
  `repair1/design.md:13-26`; `examination-repair1.md:7-17,26-35`.

### 3. Narrow-as-final wiring: use `S(B1)` as line-2b/TI

- **it1 — resists by declaration, but not by a structural contract.** It
  separates the box-1 subtotal from line 2b and says a mapping/calculation
  mismatch must be rejected. It does not define the final-result input
  contract or an explicit composition check, so a future consumer could wire
  the subtotal by symbol or convenience. **Exhibit:** `it1/design.md:31-49,81-90`.
- **it2 — resists on paper.** It names B1, TI, and L2B as different universes;
  a broader calculation must declare additional families, and the failure map
  leaves L2B blocked while TI is open. This rejects an implicit promotion, but
  still delegates enforcement to a future validator. **Exhibit:**
  `it2/design.md:58-80,94-110,120-131`.
- **repair1 — resists semantically and states the required validation.** A
  final result must consume an identical universe or an explicit,
  proven-coextensive composition; ids, labels, and symbols cannot substitute
  for that contract. The validator requirement is not production evidence,
  but the semantic boundary is now explicit. **Exhibit:**
  `repair1/design.md:34-54`; `examination-repair1.md:19-35`.

### Substitution conclusion

The repair defeats all three P1/P2 substitutions at the paper level. The two
original rivals state the right outcomes for the six cases, but leave the
authoritative claim/coverage presentation and final-input enforcement less
specified. No repair paper permits a B1 closure to honestly produce a broader
TI/L2B zero or broader coverage-complete result; the remaining risk is the
unimplemented validation boundary, not a semantic alternative endorsed by the
paper.

## Late-member and lifecycle measurements

### 4. Late member after an empty closure, without manual withdrawal

- **it1 — attack succeeds.** The lifecycle says a late `S-LATE` is discovered
  and then a later act withdraws or supersedes the old closure. Without that
  manual act, the old true closure remains the authority named by the design's
  zero pin, and the paper supplies no event or edge from the newly asserted
  member to that zero. Its “displace/withdraw” row is an outcome requirement,
  not a trigger. **Exhibit:** `it1/design.md:67-79,83-90`.
- **it2 — attack succeeds.** It2 repeats the same later-withdrawal step. It
  says the old zero must not remain current, but expressly leaves the precise
  transition mechanics as implementation work. A late member that is asserted
  without manual closure withdrawal has no existing pin into the old empty
  result. **Exhibit:** `it2/design.md:133-154`.
- **repair1 — semantic outcome resists, mechanism remains unresolved.** The
  static table says that the member assertion crosses the horizon, makes the
  closure stale, makes the zero noncurrent, and opens coverage; it also says
  no automatic successor is produced. The repair separately acknowledges that
  ADR-0010 cannot handle this case because the old zero pins no future member.
  Thus it rejects the false-current state as a requirement, but does not prove
  a mechanism that makes the state true in a record-derived projection.
  **Exhibit:** `repair1/design.md:56-72,74-88,90-109`; `examination-repair1.md:37-53`.

### 5. Existing member correction

- **it1 — not covered.** Its six-case paper and lifecycle discuss a late new
  member, not a same-fact correction after a member subtotal has been
  published. ADR-0015 is cited for identity, but no result-currency transition
  is stated for changing that member's amount. **Exhibit:**
  `it1/design.md:14-18,51-79`; the omission is also visible in its case table.
- **it2 — not covered.** It2 defines source instances and says members have
  current amounts or are open, but its lifecycle has no correction state and
  does not say how a present-member subtotal is displaced. **Exhibit:**
  `it2/design.md:20-40,82-116,133-154`.
- **repair1 — resists for the known-input path.** State 5 keeps the closure
  effective when membership is unchanged, while the subtotal depending on the
  old amount becomes noncurrent through the member-finding input edge. This is
  exactly the path ADR-0010 supplies. It does not claim that a correction
  auto-runs a successor. **Exhibit:** `repair1/design.md:74-88,90-95`.

### 6. Member displacement/removal

- **it1 — not covered.** It says a new closure is needed if members later
  become empty, but does not distinguish a member finding being displaced from
  a genuine new empty domain, nor say that the old closure/zero cannot be
  resurrected when the member disappears. **Exhibit:** `it1/design.md:67-79`.
- **it2 — not covered.** Its late-member lifecycle ends at a new assertion and
  rerun; it has no removal/open-member state and no no-resurrection rule.
  **Exhibit:** `it2/design.md:133-154`.
- **repair1 — required outcome is stated, but freshness remains open.** State
  6 treats removal/displacement as leaving the member question open, makes the
  closure stale and the zero noncurrent, and requires a new true assertion
  before any future empty zero. That correctly blocks resurrection. However,
  the path again depends on the unnamed freshness-currency relation rather
  than an exercised edge or projection rule. **Exhibit:**
  `repair1/design.md:76-88,97-109`.

### Late-state conclusion

Repair1 completely names the required observable states:

```
empty true closure → current B1 zero
late member assertion → stale closure, noncurrent zero, open coverage
no re-attestation → incomplete, no automatic successor
new true closure → explicit rerun may publish current subtotal
member correction → known-input subtotal displacement
member removal/open question → stale closure, no zero resurrection
```

Only the correction of a known member is covered by the already-described
ADR-0010 edge. The late assertion and removal cases require new
freshness-currency machinery. The repair explicitly declines to choose its
citizen, edge expression, schema, or implementation, so this is an escalation
boundary, not evidence of a hidden implementation. The failure condition
remains live: without that decision, a system following only existing
ADR-0010 edges can leave the old empty zero current.

## Proposition disposition

| Proposition | Adversary disposition | Reason |
|---|---|---|
| SFS-P1 | Settled at paper level in repair1 | Versioned exact claim and predicate are authoritative; names and rollups cannot broaden them. |
| SFS-P2 | Settled at paper level in repair1 | A B1 subtotal is distinct from TI/L2B; only identical or explicitly proven composition may fill a final universe. |
| SFS-P3 | Unresolved / decision-blocking | The state requirement is clear, but late-member and removal freshness cannot be reached by ADR-0010 alone; no production machinery has been selected or demonstrated. |

## Recommendation

Carry SFS-P1/P2 forward as converged paper semantics, preserving the exact
claim, coverage subject, and subtotal/final-result distinction as conditions on
any production contract. Do not ratify SFS-P3 or claim that the current
ADR-0010 edges solve it. The next decision must define and prototype-evaluate
the smallest record-derived freshness mechanism that makes a later member or
member removal displace closure authority and every dependent zero, with
rebuildable currency and no reserved derived-finding authority construction.

No implementation, resolver, schema, UI, taxonomy, or production artifact is
proposed by this review.
