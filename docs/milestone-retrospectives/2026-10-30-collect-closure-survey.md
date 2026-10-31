# Retrospective — Every Sum Waits for Its Statements (2025)

## Result

- **Seven partial sums no longer publish on core v62.** Form 1099-DIV box
  2a, Form 1099-R line 4b, SSA-1099 benefits and the four non-wash Form
  1099-B basis and proceeds families each block their line until confirmed
  complete. Five successor rules; no engine, schema or question change. A
  complete return computes exactly as on v61.
- **A regression test now watches the whole package.** It fails if any
  `collect` reaches a form-field line or an attachment without a closure
  guard, outside two named lists of known gaps.
- **Nine interest families are still open.** An unconfirmed Form 1099-INT
  box 1 moves AGI from 50,000 to 51,000 on v62, as on v61.

## What the evidence changed

- **The worst gap was a regression, not an oversight.** Line 2b v6 and v7
  guarded every interest family; v8 (core v38, 2026-09-12) replaced the rule
  with a selection rule whose shape the package validator fixes: top-level
  `when` must be `true`, and `require_closed` is forbidden in its paths. The
  guard cannot come back as content. That is an owner question now.
- **A static graph is not a survey.** P0's first classification marked 22
  entries unguarded that live runs showed were held downstream; the live
  pass is what made the list trustworthy.
- **"Published" is wider than form-field lines.** The review found Schedule
  D publishing partial proceeds while line 8a blocked; attachments read
  subtotals directly. The survey and test now count attachments: 24 source
  sets still reach one unguarded.
- **A design read is not an entrypoint check.** P0 said none of the six rules
  was an entrypoint; four were. The generator caught it.

## Process

- Sonnet 5.5 sub-agents throughout. Track 1 met its stop condition at line
  2b and stopped; the foreman split the milestone the same hour rather than
  waiting, which kept the other gaps moving.
- The milestone is stacked on withholding-closure (#233) by owner direction,
  so its package is core v62.

## Follow-ups

- Guard the attachments (next milestone).
- Owner question: lift the line 2b v8 validator restrictions.
- The three held-downstream entries that rest on a root block only
  (1099-DIV box 7, 1098-E, 1099-INT b8) could get live comparisons.
