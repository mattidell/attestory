# Governance Review — Conditional Selectors, Round 1R

Date: 2026-07-12
Reviewer seat: Governance reviewer, Medium tier
Evidence reviewed: `plan.md`, `charter-it1.md`, `it1/design.md`,
`examination-it1.md`, the ratified governance set, ADRs 0002–0012 and
0016–0017, and the committed derivation/kernel contracts at `HEAD`.

The review measures the two iteration-1 shapes against CS-P1 and CS-P2,
Articles 7, 11, 12, and 13, and the related declared contracts. It does not
judge the excluded repair, review, evaluation, proposed-ADR, or uncommitted
Track 3 material.

## Findings

### CS-G1R — Decision-blocking — both shapes: filing-status guards do not execute under the committed expression contract

Both shapes use expressions such as `compare(ref(filing_status), eq,
"single")` and `compare(..., "married_filing_jointly")` in their case/guard
logic. The committed evaluator's comparison path converts both operands to
decimal values; those strings therefore produce a contained invalid-dependency
block, not a boolean result. The rule schema permits the expression tree, but
schema acceptance is not runtime conformance (ADR-0006 decision 3).

Consequently, the claimed positive cases 1–4 cannot resolve as traced for
either shape, and CS-P1 is not settled. The design must use a contractually
supported representation/operation for categorical status, or the operation
semantics and evaluator contract must be versioned and adopted before either
shape can be accepted.

### CS-G2R — Decision-blocking — Shape B: policy values are embedded in selector logic

Shape B hardcodes `15000`, `30000`, `2000`, and `1550` in selector case
expressions while its tax calculation also references a parameter table. This
violates CS-P2 and ADR-0006 decision 5's separation of policy values from rule
logic. It also makes the selector's claimed 2025 content non-reusable or
version-controlled through parameter citizens. Every tax amount and rate table
used by the selector must be a separate versioned parameter citizen and a
declared package member, with the selector carrying only logic and references.

### CS-G3R — Decision-blocking — Shape B's proposed optional contract is not the committed selector schema

The design declares `optional` as an array of symbol strings and says missing
references become `null` or `false`. The committed `selector-artifact.v1`
schema instead requires optional entries to be objects containing both
`symbol` and an explicit scalar `default`. The design payload is therefore not
valid against the committed schema, and its missing-reference behavior is an
implicit runner rule rather than declared content. This conflicts with
Articles 9 and 11 and E9.1/E11.1. The default and its applicability must be
declared in the versioned schema/instance contract; a silent null/false policy
cannot be accepted.

### CS-G4R — Decision-blocking — Shape B requires an unlicensed runner pathway and does not define its contract boundary

Shape B introduces a new citizen and says the runner evaluates it natively,
including optional dependency resolution and case sequencing. The committed
derivation runner schedules `rule-artifact.v1` clauses; the design does not
define the selector's package-member role, adoption closure, operation
semantics pins, derived-finding lineage, run dispositions, or how selector
inputs become `input`/`choice` derivation edges. It therefore does not show a
contract-conforming path through Articles 4, 7, 11–14, ADR-0006, ADR-0007,
ADR-0008, ADR-0009, or ADR-0010.

This is more than an implementation detail: native selector execution would
be a new runner pathway whose semantics must be declared, schema-validated,
adopted, recorded, and portable. No such pathway is licensed by the reviewed
contracts. A selector design could be reconsidered only with those boundaries
specified and evidence that it introduces no third displacement edge.

### CS-G5R — Production condition — Shape A's default-injection rules need an explicit determinism and fact-nature contract

Shape A makes absent spouse inputs operative by publishing `false` through
`spouse-over-65-default` and `spouse-blind-default`. This is visible rule
content rather than runner-resident state, which is the correct direction, but
the design does not declare the corresponding input fact types, their nature,
or why absence for each non-married filing status is a determinable
consequence rather than an elective fact left open. E3.1 and Article 3 forbid
operative defaults for elective facts. Before production use, the package must
declare the input semantics and include negative cases showing that an open
elective dependency still blocks and that only the explicitly scoped
non-married case receives the rule-produced false.

### CS-G6R — Production condition — Shape A must show complete publication and displacement lineage

Shape A is structurally compatible with the existing guarded rule language:
parameters are separate citizens, each rule publishes one symbol, and the
cascade can represent ordinary derivation edges. However, the design's traces
stop at output symbols. They do not map each output to the committed
`derived-finding.v1` shape, role-bearing pins, the `derived-publication-act`,
adoption/governance pins, run records, or the Article 7 displacement walk.

Before production admission, the implementation must demonstrate that every
intermediate and final output pins the actual input/choice findings and
parameter/rule versions, that parameter/adoption/governance pins are not
displacement edges, and that superseding an asserted input displaces all
dependent derived findings without mutation or a third edge kind.

### CS-G7R — Non-blocking — documentation overstates iteration-1 settlement

The examination says both CS-P1 and CS-P2 are settled and describes Shape B as
robust, but the design contains no valid execution for categorical status under
the committed evaluator, embeds Shape B policy values, and uses a payload that
does not conform to the committed selector schema. The examination should be
reclassified as unresolved for Shape B and as conditional for Shape A until
CS-G1R and the applicable production conditions are addressed.

## Verdicts

### Shape A — conditionally accept

Shape A is the only iteration-1 shape that preserves the existing rule-driven
derivation architecture and can use the existing parameter, publication,
pinning, and displacement contracts without a new citizen family or runner
pathway. Conditions are: resolve CS-G1R with a supported categorical-status
representation; satisfy CS-G5R for default semantics; and demonstrate CS-G6R
through package/adoption, record, pin, portability, and displacement evidence.

### Shape B — reject

Reject in its iteration-1 form. CS-G2R, CS-G3R, and CS-G4R are
decision-blocking, in addition to the common CS-G1R failure. The proposed
selector may be a future rival design only after a fresh charter declares the
new citizen and runner contracts, separates all policy parameters, and
predeclares the required lineage and edge-integrity measurements.
