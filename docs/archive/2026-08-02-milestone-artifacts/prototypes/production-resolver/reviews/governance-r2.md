# D3 Iteration-2 — Governance Review

Date: 2026-07-16  
Seat: Governance reviewer (Medium)  
Evidence: Rung-2 paper/probe review. All named examples are synthetic.

## Verdict

- **D3-P1:** not converged across the pair. `it4` is conformant at Rung 2 on
  the proposed resolver shape; `it3` has a decision-blocking adoption-authority
  defect. The `it4` shape is a usable ADR basis only after the conditions below
  are carried forward.
- **D3-P2:** not conformant. Neither ledger accurately separates a settled
  resolver contract from an installed Track-3 discharge or gives the required
  decision-by-decision disposition.
- **ADR-0033:** not yet supportable. Do not adopt either design wholesale.

## Measurements

### 1. Publication authority — both conform on the repaired axis

`it4` §§1.1–1.3 makes the versioned act pin an exact package checksum and
release/registry anchor; its sole authority is the repo-resident public registry,
while `L` supplies only candidates matching the registry. Its pin-directed member
lookup therefore meets ADR-0027 D6/PC3: package-instance and citizen bytes are
both checked against immutable publication authority, including a recomputed
package checksum (`examination-it4` items 3–5).

`it3` §§1–3 likewise says the registry, not an `L` catalog, authenticates package
and member bytes; its substitution probe is adequate. The finding here is not a
publication-authority defect in the repaired incumbent.

### 2. Adoption authority — decision-blocking for `it3`; conformant direction in `it4`

`it3` §2 calls `AdoptionRecord` an Article-4 carrier but leaves it unversioned and
allows its `actor` to be a “System or automation identity.” Ontology §1 defines
the only current actor as the user, and §4 defines adoption as that user's
immutable, current act over a specific, scoped, versioned body of machinery.
The stated carrier is consequently neither a declared versioned act nor a valid
actor claim; its undeclared-carrier probe cannot establish Article-4 authority.

`it4` §1.1 instead declares `act-package-adoption.v1`, requires a current valid
act, and carries actor, scope, provenance, exact package checksum, and immutable
anchor pin. Read with the current Ontology actor definition, this is the required
Article-4 direction. Track 3 must implement its schema, record/currency handling,
and entrypoint gate; the paper must not imply that those are already installed.

### 3. Exclusive graph and strict superset — conformant resolver direction

`it3` §3 and `it4` §§1.3–1.4 admit only registry-pinned members, make unpinned
co-located bytes unreadable/inert, and refuse before graph/execution/rendering
unless `validation.ok == True`. This preserves ADR-0027 D1/D4/D7 and is stricter
than the committed fixture CLI: `runners/derive.py` currently glob-loads corpus
bytes and expressly does not raise when `validation.ok` is false.

The strict gate is therefore a required production condition, not a reason to
repair or allowlist issues. The committed synthetic core package measures
`ok=False` with eight issues; `examination-it3` and `examination-it4` report that
count correctly. Both designs must name the RG-1 validator-reachability repair
and v1-generation content debt as MUST prerequisites, rather than the vague
“fix/repaired” wording in `it3` §5 and `it4`'s ledger.

### 4. D3-P2 ledger — decision-blocking for both

`it3` §4 is not an exhaustive disposition matrix: its grouped claims that
ADR-0027 PC1–PC4 and ADR-0028 D1–D9/PC1–PC3 are “Discharged” give no individual
contract/installed/deferred status or reason. In particular, source isolation is
simultaneously called discharged and later deferred, and a strict validation gate
does not itself discharge ADR-0028's versioned fact/bundle, nested-set, mapping,
quantity, and composition contracts.

`it4` §2 enumerates rows but still overclaims. Its rows for ADR-0027 D6/PC3 and
D7/PC1 call an unimplemented production resolver “Discharged,” and its grouped
ADR-0028 D1–D4 and D5–D8 rows do not state the distinct mechanisms or whether
they are carried fixture-contract obligations versus Track-3 proof. “Acknowledged”
for ADR-0027 PC4 is not one of the required dispositions. Both correctly reject,
not defer, embedded schema-byte checksums (ADR-0027 D3).

The carry-forward ledger must separately account for ADR-0027 D1–D7 and PC1–PC4
and ADR-0028 D1–D9 and PC1/PC1b/PC1c/PC2/PC3, marking each as contract settled
here, production condition with owning track, deferred with reason, or N/A.

### 5. D1/D2 interlocks — production condition

ADR-0031 D1 is consumed, not discharged: `L` supplies live bytes under its
read-only/no-egress capability wall. ADR-0032 D3 is likewise consumed: the
marshal-only `RunContext` and live-entrypoint kill test remain MUST Track-2/3
work. `it3` §4 and `it4` §2 must describe these as prerequisites, not installed
“source isolation” or an existing “exclusive RunContext feed.” No D3 paper path
weakens the wall, and both examinations appropriately make no installed claim.

## Classification

| Finding | Class |
| --- | --- |
| `it3` undeclared/non-user adoption carrier | Decision-blocking |
| Incomplete and overclaimed D3-P2 ledgers | Decision-blocking |
| RG-1 named repair/debt and eight-issue hard gate | Production condition |
| ADR-0031/D2 installed wall and marshal-only proof | Production condition |
