# Charter - Iteration 4 Bounded Integration Proof

Version 1 (2026-07-11). Status: approved by owner at the three-iteration
disposition point.

Iteration 4 is an exceptional bounded integration proof based on exhibit
`exhibits/tax-citizen-families/it3` at `be72d63`. It is not a fourth broad
domain prototype, a clean-room rival, or an invitation to add tax coverage.
Its only purpose is to determine whether the useful it3 contract decisions can
operate through authoritative workspace boundaries rather than through
fixture booleans, hard-coded indexes, or harness-local helper assertions.

## Build Boundary

The builder works only on branch
`prototypes/tax-citizen-families/it4`. Candidate artifacts live under
`docs/prototypes/tax-citizen-families/it4/` on that branch. The builder may
copy the it3 artifact tree, but must identify every change from it3.

Do not add new tax forms, income families, deductions, credits, filing
statuses, jurisdictions, or years. Do not broaden the fixture-minimal Tax
Table. A schema or citizen-family amendment is allowed only when it is the
smallest necessary expression of an integration relationship required below.
Reserved T1/T2 doctrine remains off-limits.

The builder writes
`docs/prototypes/tax-citizen-families/examination-it4.md`. It must report each
gate as closed with end-to-end evidence, failed with evidence, or escalated for
owner/governance decision. A gate may not be marked closed by a helper that is
not used by the ordinary scenario-to-run path.

## Non-Substitution Rule

For every gate, the evidence command must exercise the same path the prototype
claims a conforming workspace would use. The following do not close a gate:

- hashing two hand-written copies of a key;
- constructing both an authoritative finding and its projection from the same
  fixture boolean;
- creating a stale dictionary that no consumer reads;
- validating only the supplied positive set;
- resolving relationships with a harness-only hard-coded map;
- inspecting a blocked record entry and calling it an explanation walk; or
- describing a load-bearing contract in prose without adopting and pinning it.

Mutation evidence must reach the ordinary path and produce a different
authoritative result, block, or validation failure for the declared reason.

## Required Integration Gates

- **I1 - Authoritative scenario materialization.** Scenario inputs for closure,
  standard-deduction eligibility, and tax-computation method must materialize
  typed facts and findings with identity, basis, and acts where required. The
  ordinary runner path must consume declared projections of those findings; it
  must not receive semantically equivalent booleans directly from fixtures.
- **I2 - Adopted and pinned projections.** Every load-bearing projection,
  including `closed_sets` and any eligibility or method projection, must be a
  versioned declared artifact included in the adopted package/content scope and
  pinned by resulting records/findings. Withholding, substituting, or changing
  the projection artifact must block or change execution through the ordinary
  path. If this cannot be expressed without a machinery decision, fail and
  escalate rather than simulating the contract in the harness.
- **I3 - W-2 correction lifecycle.** Materialize an original W-2 finding and a
  corrected/reissued finding or act for the same W-2 slip identity. Exercise
  supersession, current-state reading, downstream displacement, and successor
  derivation. A second distinct slip from the same employer/year must remain a
  distinct fact. Evidence identity must remain separate throughout.
- **I4 - Closed package and provenance joins.** Resolve scenario -> package ->
  bundle/fact types -> rules/parameters -> symbol bindings -> citations and
  attachments -> form fields. Package/content scope, tax year, jurisdiction,
  ids, and versions must be checked across every included citizen role. Commit
  later-year positives and mixed-year negatives for fact types, rules,
  parameters, citations, bindings, form fields, and scenario provenance.
- **I5 - Record-derived coverage.** Build coverage from actual derivation
  records emitted by the ordinary run path and declared content that identifies
  covered families. A contradictory stored projection must be supplied to the
  real coverage consumer and demonstrably ignored or rejected. Missing
  non-closure dependencies must be represented honestly rather than silently
  reported as family closure.
- **I6 - Record-grounded explanations.** Execute explanation walks for present
  numeric zero, closure-backed zero, no source/no closure, invalid source, and
  false guard. Every walk must begin at the requested form/output disposition
  and terminate through actual pins in authoritative findings, declared rules,
  adoption/projection artifacts, and persisted process records. Removing the
  real input or record must make the walk incomplete or invalid.
- **I7 - Citation semantic attachment.** Enforce the allowed relationship among
  subject kind/id, content role, citation locator, tax year, and jurisdiction.
  Commit negatives for wrong line, wrong year in both directions, wrong content
  role, and a valid citation attached to the wrong subject. Enforcement must be
  declared content or a versioned resolver contract used by the normal package
  validation path.
- **I8 - Relationship examples.** Commit hand-written positive and negative
  examples for each relationship added or materially changed by it4, including
  projection adoption/pins, correction/supersession, package membership,
  provenance resolution, coverage reconstruction, explanation termination, and
  citation-role validation. Harness mutations may supplement but not replace
  them.
- **I9 - Bypass resistance.** Add negative probes that attempt the exact it3
  bypasses: direct fixture booleans, unpinned projection content, unresolved
  provenance strings, hard-coded coverage maps, hard-coded explanation input
  indexes, and schema-valid but semantically wrong citation attachments. The
  ordinary validation/run path must reject or block each bypass. The examination
  must name the authoritative component that rejects it.

## Evidence and Handoff

The examination must include:

- a checklist mapping I1-I9 to artifact paths and exact commands;
- an it3-to-it4 change inventory;
- normal-path positive runs and negative/bypass runs;
- committed positive and negative instances;
- actual process records and explanation outputs where required;
- every failed or escalated gate, without replacing it with a prose claim; and
- a concise statement of which it3 design conclusions remain supported even if
  an integration gate fails.

The builder does not review the work. Prototype artifacts never merge to
`main`; only the examination and process/review documents may later merge.
