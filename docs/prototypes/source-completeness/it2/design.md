# Iteration 2 Rival Contract Design

Date: 2026-07-12

Evidence rung: 1 (paper only)

Fixture provenance: every name, identifier, and amount below was invented for
this document and has no personal source.

## SC-P3 — Source family

A **source family** is a declared tax-content grouping of repeatable source
instances whose complete enumeration is necessary before a `collect` operation
may treat absence as zero. It is identified by tax year, source-kind fact-type
family, and subject scope. It does not contain evidence, findings, or a stored
list of instances. A closure fact asks whether the user has completed that
grouping for that scope; member facts are individuated independently under the
source-kind fact type.

Examples used throughout:

| Family id | Year | Source-kind family | Subject scope |
|---|---:|---|---|
| `sf-interest-2097-demo` | 2097 | 1099-INT statement instance | `subject-demo-orbit` |
| `sf-w2-2097-demo` | 2097 | W-2 slip | `subject-demo-orbit` |

The definition permits many member instances and does not equate a family with
a payer, account, statement, document, or evidence set.

## SC-P1 — Mapping as an adopted rule parameter

### Candidate shape

The rival mapping is **not a dedicated mapping citizen**. Each collecting rule
artifact declares an immutable `closure_authority` parameter as part of that
artifact's own versioned content:

```yaml
rule_artifact: taxable-interest-total.rule.v7-demo
collect:
  member_fact_type: taxable-interest-by-statement.v1-demo
  source_family: sf-interest-2097-demo
closure_authority:
  closure_fact_type: interest-source-closure.v1-demo
  required_identity:
    tax_year: 2097
    subject: subject-demo-orbit
  admitted_value: true
```

Adoption pins `taxable-interest-total.rule.v7-demo`, including these parameter
bytes. The parameter therefore has no independent identity or lifecycle: a
change publishes and requires adoption of a new rule-artifact version. This is
meaningfully distinct from a mapping citizen that can be independently
published, adopted, and shared.

The runner projects closed membership only when all of these hold at the
evaluated workspace revision:

1. the collecting rule artifact is in the current adoption;
2. exactly one fact matches `closure_fact_type` and `required_identity`;
3. that fact has a current finding; and
4. the current finding's value equals `admitted_value` (`true`).

This projection feeds the real two-layer `collect` eligibility check. Layer 1
asks whether member findings exist. When none exist, layer 2 asks whether the
artifact's declared `source_family` is in projected closed membership. A true
current closure finding can add it; mere finding presence cannot. False,
absent, ambiguous, or displaced findings never enter membership, so an empty
Layer 1 result blocks at Layer 2 rather than becoming zero. No caller supplies
or augments the projected membership set.

### Interest positive: true closure permits empty-source zero

At revision `rev-demo-40`, `interest-source-closure.v1-demo` for year 2097 and
`subject-demo-orbit` has current finding `finding-close-interest-true-demo`
with attested value `true`. The current adoption pins
`taxable-interest-total.rule.v7-demo`. There are no current
`taxable-interest-by-statement.v1-demo` findings.

Layer 1 returns an empty collection. The parameter resolves the closure fact,
inspects the current finding's value, and projects `sf-interest-2097-demo` into
closed membership. Layer 2 admits the empty collection. The operation publishes
`finding-interest-total-zero-demo` with value `0`.

Required explanation pins:

```text
finding-interest-total-zero-demo
  -> input pin: finding-close-interest-true-demo
     -> assertion act: act-close-interest-demo
  -> artifact pin: taxable-interest-total.rule.v7-demo
     -> embedded parameter: closure_authority
  -> adoption pin: adopt-demo-rules-07
  -> run record: run-demo-41
```

The closure finding is a derivation input even though its value authorizes an
empty collection; it is not merely mentioned in the run record.

### W-2 positive: same shape, different instance

```yaml
rule_artifact: wage-total.rule.v5-demo
collect:
  member_fact_type: w2-wages-by-slip.v1-demo
  source_family: sf-w2-2097-demo
closure_authority:
  closure_fact_type: w2-source-closure.v1-demo
  required_identity:
    tax_year: 2097
    subject: subject-demo-orbit
  admitted_value: true
```

With current `finding-close-w2-true-demo`, no current W-2 slip wage findings,
and an adoption pinning `wage-total.rule.v5-demo`, the same four checks project
`sf-w2-2097-demo`; the same two collect layers publish a pinned zero. No
interest-specific runner behavior is required.

### Negative fixtures

**False closure.** `finding-close-interest-false-demo` is current and has value
`false`. Checks 1–3 pass; check 4 fails. Layer 1 is empty, Layer 2 does not find
the family in projected membership, and the rule blocks with
`source-family-not-affirmatively-closed`. It cannot publish zero.

**Displaced closure.** Historical `finding-close-interest-true-old-demo` has
value `true`, but `finding-close-interest-false-new-demo` supersedes it. The
old finding fails current-finding check 3; the new finding fails value check 4.
Layer 2 blocks for the same declared reason. Selecting “latest true” would be a
currency violation, not an alternative result.

**Absent closure.** No finding stands for the closure fact. Check 3 fails and
Layer 2 blocks. This confirms unknown is not false and neither authorizes zero.

**Caller injection.** A caller offers `sf-interest-2097-demo` in a runtime set.
The set is not a declared rule input and is ignored/rejected at the boundary;
only the adopted parameter projection can supply Layer 2 membership.

### Lifecycle trace

1. `act-close-interest-demo` asserts attested `true`, producing
   `finding-close-interest-true-demo` for the enduring closure fact.
2. `adopt-demo-rules-07` adopts `taxable-interest-total.rule.v7-demo`, including
   its embedded parameter. The earlier finding is not retroactively derived.
3. `run-demo-41` sees no members, resolves the true current closure, and
   publishes pinned `finding-interest-total-zero-demo`.
4. `act-withdraw-close-interest-demo` corrects the same closure fact with
   attested `false`, producing `finding-close-interest-false-demo` and
   displacing the true finding.
5. The derivation edge from the zero to its pinned true closure finding eagerly
   displaces the zero in the same logical transition; history remains.
6. Explicit `run-demo-42` records an empty Layer 1 and failed Layer 2, publishes
   nothing, and stops blocked on `source-family-not-affirmatively-closed`.

### Producer → authority → consumer → failure map

| Stage | Declared participant | Authority carried | Failure and result |
|---|---|---|---|
| Producer | User assertion | Current attested finding of closure fact | absent/false/ambiguous/displaced → no authority |
| Authority | Current adoption of collecting rule | Pins rule version and embedded parameter | unadopted/wrong scope/version → rule ineligible |
| Projection | Thin runner applying parameter | Current finding must equal literal `true` | presence-only projection → contract violation |
| Consumer L1 | `collect` member lookup | Current member findings | members present → aggregate them normally |
| Consumer L2 | `collect` empty guard | Projected family membership | empty and not admitted → declared block |
| Publisher | Derivation run | Pins closure finding, rule, adoption, inputs | missing pin → invalid derived finding |
| After correction | Currency derivation | Derivation edge from closure to zero | old zero displaced; rerun blocks |

## SC-P2 — Statement-instance identity

### Chosen key

`taxable-interest-by-statement.v1-demo` uses identity keys:

```text
(tax_year, subject, payer, form_1099_int_statement_instance)
```

A `form_1099_int_statement_instance` is a peer workspace citizen representing
one logical information-return statement furnished by a payer for a recipient
and year. It is not paper, a file, an upload, a scan, or other evidence. It is
individuated when the user asserts which logical statement a reported item
belongs to; evidence may support that assertion but cannot key it. A corrected
copy continues the same statement instance when it corrects that logical
return; an additional original Form 1099-INT instantiates another.

This is rival to account-composite identity: the chosen key does not include an
account citizen or account number. The IRS instructions support the pressure
case rather than dictate the workspace key: an account number is required when
a payer files more than one Form 1099-INT for a recipient with multiple
accounts, and the general correction instructions preserve an originally
reported account number on a correction. Official sources:
`https://www.irs.gov/instructions/i1099int` and
`https://www.irs.gov/publications/p1099` (consulted 2026-07-12).

### One payer, two accounts: distinct statements

Synthetic payer `payer-nebula-kites-demo` furnishes two logical statements for
2097 to `subject-demo-orbit`:

| Account label (non-key provenance) | Statement citizen | Box 1 finding |
|---|---|---:|
| `ACCT-DEMO-ALPHA-NOT-REAL` | `stmt-int-comet-demo` | 11 |
| `ACCT-DEMO-BETA-NOT-REAL` | `stmt-int-pulsar-demo` | 23 |

The statement citizens differ, so the facts differ and the two values aggregate
to 34. Account labels explain payer reporting but do not individuate the facts.

### Same-fact correction lifecycle

`finding-comet-interest-11-demo` answers the fact keyed by year 2097, subject,
payer, and `stmt-int-comet-demo`. A corrected statement reports 13. The user
asserts `finding-comet-interest-13-demo` against the same fact; it supersedes
11 and displaces dependent totals through derivation edges. The correction's
new PDF is new evidence, but neither fact identity nor statement-citizen
identity changes. A rerun may publish a successor total of 36.

### Rejected rivals

**Payer-only key:** `(tax_year, subject, payer)` collides: both invented account
statements address one fact, causing 11 and 23 to appear as rival answers rather
than additive sources. Rejected because it fails the concrete two-account case.

**Account-composite key:** `(tax_year, subject, payer, account)` distinguishes
this fixture, but is not chosen because the reporting unit exercised here is a
logical information-return statement: a payer may furnish a statement without
a usable account number or may issue multiple statements concerning one
account. Those cases would require invented account identity or collision. This
remains a viable competing design where a separately declared account citizen
is the intended source unit; paper distinguishes its semantics from this one.

**Evidence/document key:** `(tax_year, payer, evidence_file_id)` is rejected
under Constitution Article 1 and Engineering Constraint E1.1. Re-uploading or
replacing a PDF would rekey or duplicate the question, and two files could
represent one correction chain. Evidence belongs in finding basis and
explanation provenance only.

## Paper disposition

The examples distinguish both axes without executable artifacts. The adopted
parameter makes mapping lifecycle inseparable from the collecting rule's
version and adoption; the statement-instance key makes logical information
returns, rather than accounts, the repeatable source unit. SC-P1's semantics are
fully stated on the two-layer path, but static paper cannot demonstrate the
absence of a value-insensitive adapter in production execution.
