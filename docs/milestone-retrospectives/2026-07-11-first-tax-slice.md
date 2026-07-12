# Retrospective — First Tax Slice

- Milestone: First Tax Slice (Foundation phase)
- Branch: `milestone/first-tax-slice`
- Merge commit: `c548766` (non-ff into `main`, 2026-07-11)

## Shipped

The Foundation thesis proved at the smallest real tax-content scale: a
synthetic W-2 box-1 finding flows through an adopted rule artifact into a
first-class 2025 Form 1040 line-1a form-field citizen, with trustworthy
identity, explanation, correction/displacement, explicit re-derivation, and
two-runner parity. Four implementation tracks (Track 0 — the citizen-family
prototype process — completed before this branch existed):

1. **W-2 vocabulary and form-field contract** — production `form-field.v1`
   schema (new checksum-manifested `packages/schemas/tax/` family) carrying
   all five ADR-0012 dispositions; the 2025 W-2 box-1 wage fact type and
   source-closure fact type under kernel `fact-type.v1` (ADR-0011); the Form
   1040 line-1a form-field citizen, its printed label verified against the
   official IRS 2025 Form 1040; hand-written positive examples and eleven
   isolated negatives.
2. **Synthetic W-2 workspaces and correction** — four committed workspaces
   over the real kernel adopting the production bundle: one slip, two
   same-employer slips (distinct facts, never colliding), a present numeric
   zero, and same-fact correction. An identity-collision negative reproduces
   the ADR-0011 rejected alternative (employer+year-only keying) and shows it
   really does collide two slips onto one fact — the exact failure the
   accepted slip-keyed identity avoids.
3. **Line-1a rule package and integration** — a field-mapping rule
   aggregating current box-1 findings, in a bounded package containing only
   that rule (rounding convention arrives as a workspace input, not a
   package parameter, so no parameter member was needed). Three scenarios
   threaded with the same synthetic finding ids as Track 2's fixtures, each
   proven byte-identical across the forward and reference runners, with CLI
   goldens and explanation walks for the nonzero and computed-zero cases.
4. **Correction cascade and explicit re-derivation** — one real workspace act
   log combining all three prior tracks: assert, derive, correct, and
   explicitly rerun. The mid-state golden shows the corrected source
   displacing the original derived finding with zero current derived
   findings until a run resolves it (proving no auto-rerun exists); the
   final-state golden shows the successor current and the original
   displaced.

## Verification

- `python3 -m unittest` → 232 passed (54 new tax tests across four modules).
- `python3 -m mypy` → clean, 58 source files, strict.
- `python3 tools/governance_lint.py` → conformant.
- `python3 -m packages.derivation.runners.derive --scenario packages/sample_data/tax/scenarios/two_w2_same_employer/scenario.json`
  → `tax.us.2025.wages.total-w2-box1 = 60000` with a two-source explanation
  tree.
- Data safety: every new fixture/content tree scanned for private markers and
  absolute local paths; all synthetic.

## Decisions

- **Tier 1 (recorded here, no ADR)** — kernel `fact-type.v1` has no
  `description` field. ADR-0011's "title and description" framing is carried
  in a single rich `title` string rather than minting a `fact-type.v2` for
  one field; the schema is immutable and a version bump was not warranted for
  this milestone's scope.
- **Tier 1** — the line-1a rule's `rounding.convention` dependency is
  supplied as a `RunContext` input finding, not a package parameter member.
  This mirrors the existing derivation demo pattern and kept the bounded
  package to its single rule member, matching the milestone's "only the
  existing machinery members it requires" scope line.
- **Tier 1** — Track 3's citation reference stayed a bare opaque string with
  no backing citizen, per ADR-0012's explicit deferral of citation semantic
  resolution; no new schema was introduced to back it.
- No Tier 2/3 decisions were made in this milestone; ADR-0011 and ADR-0012
  (ratified in Track 0) were the only architectural commitments this branch
  implemented against.

## Deviations

- None from the amended plan (`docs/phases/foundation/milestones/first-tax-slice.md`,
  narrowed 2026-07-11 after Track 0). All four tracks landed as scoped, one
  commit each, with no scope creep into 1099-INT, downstream Form 1040
  lines, closure-backed zeros, or citation resolution — all explicitly
  deferred by the plan's Non-Goals section.

## Data safety

All committed content is synthetic: demo employer/slip ids, manufactured W-2
amounts, no real documents or personal facts. Every new fixture tree carries
a dedicated data-safety test scanning for `/Users/`, `/private/`,
`local-data/`, and `uploads/` markers.

## Follow-ups

- **1099-INT and interest source identity** — roadmap item 6 (Source
  Completeness And Interest Slice): resolve source-instance identity and the
  adopted source-family-to-closure mapping this milestone deliberately left
  unimplemented.
- **Closure-backed empty-source publication** — the closure fact type exists
  as schema/content only; no rule in this milestone reads it. The
  `collect` operation's two-layer closure check (evaluator.py) is exercised
  generically by the derivation machinery's own tests but never by tax
  content yet.
- **Citation resolution** — `citation_ref` on the line-1a form field remains
  an inert opaque string; a resolver contract is unstarted (ADR-0012 "Not
  Decided").
- **Downstream Form 1040 lines** (9, 11, 12, 15, 16) and standard-deduction/
  tax-method condition structure — roadmap item 7.
- **Non-publication explanation** (blocked/invalid/guard-inapplicable walks)
  — the milestone exercised only published-value and computed-zero
  explanations, per ADR-0012's explicit deferral.

## Planning lessons

- **A milestone can complete four tracks in one sitting when the underlying
  machinery is already stable.** All of Track 1-4's actual computation
  (schema validation, currency, saturation runner, reference runner,
  explanation walker) was inherited unmodified from the Derivation Machinery
  and Kernel milestones; this milestone was pure content plus fixtures. The
  Track 0 prototype process front-loaded the only genuinely hard decisions
  (ADR-0011/0012), which is exactly the point of gating consequential
  decisions before implementation.
- **Grounding scenario/workspace fixtures in the same finding ids across
  tracks pays off.** Track 3's scenarios reused Track 2's exact synthetic
  finding ids (`demo-finding-w2-alpha-1-box1`, etc.), and Track 4's cascade
  fixture reused Track 3's rule verbatim. This made the correction-cascade
  golden's assertions read as a continuous story rather than three
  disconnected fixture sets, and meant no test had to reconcile diverging
  synthetic identities.
