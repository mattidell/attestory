# ADR 0011 - Tax Fact Identity and Source-Set Closure

- Status: accepted (ratified 2026-07-11)
- Tier: 2
- Date: 2026-07-11

## Context

First Tax Slice must publish real tax fact types before rules and fixtures can
depend on them. Three contract questions are foundational for that content:

1. whether real tax questions require a specialized tax-fact-type schema or fit
   the kernel `fact-type.v1` family;
2. what individuates W-2 wage facts when documents are submitted, replaced, or
   corrected; and
3. whether a source-set closure assertion is a tax election, an ordinary
   determinable fact, or a separate citizen family.

Per ADR-0005, this proposal is supported by
`docs/archive/2026-08-02-milestone-artifacts/prototypes/tax-citizen-families/evaluation-analysis.md`. The analysis
synthesizes two rival designs (`exhibits/tax-citizen-families/it1` and `it2`),
two targeted integration iterations (`it3` and `it4`), and four committee
rounds. It deliberately narrows the decision after the committee rejected the
full prototype corpus as ratification-ready.

## Decision

1. **The exercised core tax questions use the existing kernel
   `fact-type.v1` family.** W-2 wages, interest-by-box, filing status, rounding,
   itemization, and source-set closure need no specialized tax-fact-type schema.
   Their tax meaning is declared in ordinary fact-type citizens through identity
   keys, nature, value schema, supersession policy, title, and description.
   Companion content families may bind those facts to forms, rules, citations,
   or rendering without subclassing the kernel fact type. (Analysis C1.)

2. **A W-2 wage fact is keyed by the W-2 slip as a thing, never by submitted
   evidence.** Its identity includes the employer, tax year, and a W-2-slip
   citizen, plus any enclosing taxpayer/workspace scope required by the kernel.
   The slip citizen is peer to evidence. A scan, upload, replacement document,
   or evidence id is forbidden from the fact's identity keys. (Analysis C2;
   Constitution Article 1.)

3. **Two slips from the same employer and tax year are two facts.** Distinct
   W-2-slip citizens preserve distinct questions and aggregate through declared
   rules. A corrected or reissued value for the same slip answers the same fact
   again: the new finding supersedes the prior finding under the fact type's
   declared policy. ADR-0010 currency displaces dependent derived findings;
   re-derivation may publish successors. A different slip is succession/new
   individuation, not correction of the first fact. (Analysis C2.)

4. **Source-set closure is a determinable fact with an attested basis, not an
   elective fact.** It records that the user has completed a named source family
   for a declared scope. The assertion reports completeness; it does not
   constitute a tax-law choice. Closure uses ordinary `fact-type.v1`, with
   identity keys for the relevant scope (including tax year where applicable),
   `nature: determinable`, and the ordinary supersession policy appropriate to a
   correctable attestation. (Analysis C3.)

5. **Closure authority is affirmative-only.** A current true finding means the
   source family is closed. A false finding, if the content model records one,
   means explicitly not closed and never authorizes empty-source publication;
   no current finding means closure is unknown/not established. Every mapping
   or runner projection must inspect the current value and admit only true into
   closed membership. Round-4 negative evidence rejects the value-insensitive
   adapter behavior that treated a false finding as closed. (Analysis C3.)

6. **Evidence and correction provenance remain separate from fact identity.**
   Findings may cite evidence through their basis and evidence relations, but
   evidence replacement never rekeys the fact. This ADR settles same-fact
   mechanical correction, not the legal/documentary workflow for Form W-2c.

## Not Decided

This ADR does not decide:

- the closure-fact-to-source-family/collect mapping;
- `RunContext.closed_sets` or any replacement for it;
- how closure mappings become adopted and pinned rule inputs;
- standard-deduction eligibility or line-16 method condition structure;
- W-2c previously-reported/corrected-value and evidence-replacement workflow;
- 1099-INT statement/account source-instance identity;
- package/adopted-content closure; or
- any prototype artifact id, schema bytes, or package as production content.

Those boundaries are expressly excluded by the evaluation analysis and require
separate decisions or production conditions. In particular, this ADR must not
be cited as approval of caller-supplied `closed_sets`.

## Consequences

- First Tax Slice can author its bounded tax vocabulary using the published
  kernel schema rather than introduce a parallel tax-fact hierarchy.
- W-2 corrections preserve question identity while evidence history and finding
  history remain append-only and independently inspectable.
- Multiple same-employer slips no longer collide.
- Closure entry surfaces distinguish affirmative closure from explicit
  not-closed and unknown; they never treat false as closure or describe closure
  as an election.
- Empty-source publication remains blocked until a separately ratified mapping
  and runner boundary can consume current closure findings authoritatively.
- Production fixtures must preserve the two-slip and same-fact correction/
  displacement cases demonstrated by the exhibits.

## Alternatives Considered

- **Introduce `tax-fact-type.v1` as a specialized kernel-adjacent family.**
  Rejected for the exercised facts: it1 made useful domain pressure visible,
  but it2-it4 require no additional kernel fact-type field. Form, citation,
  binding, and rendering meaning belong in companion citizens.
- **Key wage facts by document or evidence id.** Rejected: evidence replacement
  would change the question, two documents could duplicate one question, and
  correction could not preserve same-fact history. It violates Article 1.
- **Key wages only by employer and year.** Rejected: two slips from one employer
  collide; the it3/it4 two-slip fixture demonstrates the failure.
- **Model source closure as elective.** Rejected: completeness reports a
  condition; it is not a tax-law choice. Round-2 dissent and the it3 mini-spike
  resolve the distinction.
- **Treat any present closure finding as affirmative closure.** Rejected: it4
  demonstrates that a false value can leak into closed-set membership when a
  projection checks only fact presence. Closure authority must inspect current
  value and accept only true.
- **Create a separate closure citizen family.** Not required for nature or
  lifecycle: ordinary `fact-type.v1` and `finding.v1` express the bounded
  closure assertion. A future adopted source-family mapping may still be its
  own artifact without changing the closure fact family.

## Links

- Evidence: `docs/archive/2026-08-02-milestone-artifacts/prototypes/tax-citizen-families/evaluation-analysis.md` C1-C3
- Process and exclusions:
  `docs/archive/2026-08-02-milestone-artifacts/prototypes/tax-citizen-families/process-retrospective.md`
- Milestone: `docs/archive/2026-08-02-milestone-artifacts/phases/foundation/milestones/first-tax-slice.md`, Track 0
- Precedents: ADR-0002 (act log), ADR-0003 (schema citizens and opaque ids),
  ADR-0005 (prototype evidence), ADR-0010 (derived currency)
- Exhibits: `exhibits/tax-citizen-families/it1` through `it4`
