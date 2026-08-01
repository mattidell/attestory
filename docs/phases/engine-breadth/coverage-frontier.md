# Engine Breadth — Coverage Frontier

Audience: Product (selection instrument); Shared (status)

## How to read this frontier

A row is a coherent return class the engine either computes or honestly cannot
yet compute. Selection favors a bounded end-to-end change over a wide list of
input boxes. Status is one of:

- **named block** — the unsupported class is represented and refused honestly;
- **candidate** — the class is understood well enough to compare, but is not
  selected;
- **selected** — an owner-selected milestone plan exists;
- **contracted** — required scope contracts are accepted;
- **synthetic complete** — the authoritative path operates end to end on
  committed synthetic fixtures.

“Synthetic complete” is an engine-coverage claim, not a real-data claim.

## Frontier as of 2026-07-31

| Candidate slice | New computable class | Current blocker | Contract novelty | Evidence target | Status |
| --- | --- | --- | --- | --- | --- |
| Form 1099-DIV box 2a → Form 1040 line 7a, Schedule D not required | Returns whose only capital gains are eligible capital-gain distributions and whose contributed component authority establishes that Schedule D is not required | The prior recorded/non-composable box-2a block is retired only for this bounded class; Schedule-D-required and missing-authority cases remain honestly unavailable | ADR-0050 accepts four Exception-1 components, a horizon-closed successor box-2a family, distinct line 7a/7b publications, and the direct-route QDCG handoff | Production-shaped synthetic coordinator, lifecycle, package, explanation, and presentation evidence | **synthetic complete** |
| Capital transactions → Schedule D | Returns requiring Schedule D because the direct-line exception does not apply | No transaction source family, Form 8949 content, loss/carryover completeness, or Schedule D production content | Larger source-and-attachment contract; must not manufacture a schedule from box 2a alone | Separate milestone after its source scope and completeness boundary are selected | candidate |
| Schedule K-1 (Form 1065) box-5 interest → Form 1040 line 2b and Schedule B Part I | Returns with taxable partnership interest income reported in box 5 of a 2025 Form-1065 K-1 | ADR-0026 excludes K-1 interest from line 2b's declared universe; Schedule B Part I itemizes only the box-1 family | Add a distinct horizon-closed source family and five-slot composition successor; generalize attachment itemization so Part I is structurally complete against that composition | Production-shaped synthetic identity, correction, late-member, line-2b, Schedule-B, package, explanation, and presentation evidence | **selected** |
| Market-discount interest | Returns with accrued market discount includible as taxable interest | ADR-0026 excludes market discount from line 2b's declared universe | Select source authority and add a positive-interest family without silently importing the broader securities-transaction domain | Paper-grounded source boundary followed by synthetic closure, line-2b, and Schedule-B evidence | candidate |
| Interest subtractive adjustments | Returns with nominee, accrued, or premium adjustments | No subtractive-adjustment mechanism | New adjustment authority and explanation semantics | Paper-first contract evidence, then positive/negative adjustment goldens | candidate |
| Other recorded Form 1099-DIV boxes | Returns involving boxes 3, 5, 7, or 12 | Boxes are named recorded/non-composable exclusions with different downstream meanings | Not one coherent slice; each box needs its own downstream and completeness analysis | Split into independently selectable rows before planning | named block |
| New unrelated income domain | A return class outside the existing W-2/interest/dividend columns | No owner-selected source/form target | Unknown until a concrete source and downstream output are named | Owner selection and a fresh coverage row | candidate |

## Completed synthetic frontier

The first milestone, **Capital-Gain Distributions and Form 1040 Line 7a**,
closed on `main` in PR #128. Its synthetic-complete claim is bounded to the
selected box-2a-only direct-reporting class: production-shaped synthetic
returns reach line 7a, line 9, taxable income, line 16, explanation, package
resolution, and presentation. This is neither real-data evidence nor general
capital-gains support.

The engine will not create Schedule D merely because box 2a is present.
Schedule-D-required and missing-authority returns remain outside this direct
route. A later Schedule D milestone must bring the additional source and
completeness scope that makes the attachment genuinely required; it remains a
distinct candidate rather than the automatically selected successor.

The selected second milestone is **Schedule K-1 Box-5 Interest Breadth**. Its
claim is limited to 2025 Schedule K-1 (Form 1065) box 5. It does not include
other K-1 forms or boxes, market discount, subtractive adjustments, partnership
basis, or a real-data operation. Plan:
`milestones/k1-interest-breadth.md`.

Official tax-content grounding:

- [2025 Form 1040 instructions, line 7a](https://www.irs.gov/instructions/i1040gi)
  describe the direct-reporting exception and the Schedule-D-not-required
  indicator.
- [2025 Schedule D instructions](https://www.irs.gov/instructions/i1040sd)
  distinguish capital-gain distributions reported directly on Form 1040 from
  those reported through Schedule D.
- [Form 1099-DIV instructions](https://www.irs.gov/instructions/i1099div)
  define box 2a as total capital-gain distributions.

These sources establish the tax routing. They do not decide the project's
authority, closure, supersession, or explanation contracts; those are the
milestone's prototype questions.
