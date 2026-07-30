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

## Frontier as of 2026-07-28

| Candidate slice | New computable class | Current blocker | Contract novelty | Evidence target | Status |
| --- | --- | --- | --- | --- | --- |
| Form 1099-DIV box 2a → Form 1040 line 7a, Schedule D not required | Returns whose only capital gains are eligible capital-gain distributions and whose contributed declaration says Schedule D is not required | Box 2a is recorded/non-composable; ADR-0038 deliberately has no route from the signal to line 16 | Decide the authority/completeness shape for the direct-line exception, promote box 2a into a closed family, and define the QDCG handoff | Rival-backed contract followed by production-shaped synthetic coordinator, lifecycle, and presentation evidence | **selected** |
| Capital transactions → Schedule D | Returns requiring Schedule D because the direct-line exception does not apply | No transaction source family, Form 8949 content, loss/carryover completeness, or Schedule D production content | Larger source-and-attachment contract; must not manufacture a schedule from box 2a alone | Separate milestone after its source scope and completeness boundary are selected | candidate |
| Further positive interest sources | Returns with K-1 box 5 interest or market discount | ADR-0026 excludes both from line 2b's declared universe | Extend source families and the coextensive composition | Synthetic multi-family closure and line-2b tie-out | candidate |
| Interest subtractive adjustments | Returns with nominee, accrued, or premium adjustments | No subtractive-adjustment mechanism | New adjustment authority and explanation semantics | Paper-first contract evidence, then positive/negative adjustment goldens | candidate |
| Other recorded Form 1099-DIV boxes | Returns involving boxes 3, 5, 7, or 12 | Boxes are named recorded/non-composable exclusions with different downstream meanings | Not one coherent slice; each box needs its own downstream and completeness analysis | Split into independently selectable rows before planning | named block |
| New unrelated income domain | A return class outside the existing W-2/interest/dividend columns | No owner-selected source/form target | Unknown until a concrete source and downstream output are named | Owner selection and a fresh coverage row | candidate |

## Selected frontier

The first milestone is **Capital-Gain Distributions and Form 1040 Line 7a**.
Its boundary follows the 2025 Form 1040 direct-reporting exception: the engine
will not create Schedule D merely because box 2a is present. A later Schedule D
milestone must bring the additional source and completeness scope that makes
the attachment genuinely required.

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
