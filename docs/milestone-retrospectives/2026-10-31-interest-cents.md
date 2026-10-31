# Retrospective — Interest With Cents (2025)

## Result

- **Interest with cents works on core v68.** Schedule B Part I attaches with
  cents, and line 2b rounds the cents total once, as the 2025 instructions
  say. This closes the last part of the statements-with-cents work.
- **Two narrow validator changes,** both under the owner's approval: a v68
  entry in the interest successor-graph table, and the Social Security
  succession check accepting worksheet v3 or later.

## What the evidence changed

- **Line 2b had two pins, not one.** The successor-graph table was the
  known blocker; the Social Security succession check pinned the worksheet
  that reads line 2b at exactly v3. The second was found only by building.
- **A validator can make content brittle without anyone choosing it.** Both
  checks pinned an exact version where they meant "this version or a
  successor". The table was built to be extended; the worksheet check was
  not.

## Process

- One Sonnet 5.5 builder across four tracks, resumed once after a usage
  limit with its uncommitted work intact.

## Follow-ups

- `interest-positive-total` rounds with a literal `half_up`; revisit if the
  rounding convention ever admits another mode.
