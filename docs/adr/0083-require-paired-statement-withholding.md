# ADR 0083 — Require-Paired Statement Withholding

- Status: **accepted** (2026-11-06; owner-accepted after core v77 merged in PR #259)
- Tier: 2
- Date: 2026-11-04

## Context

Form 1040 lines 25b and 25a count federal income tax withheld. The count
compares how many income rows exist with how many withholding rows exist.
Two statements can satisfy that comparison when one statement carries both
answers and the other carries neither. The person is then never asked for
the missing withholding amount, and the line publishes the answered amount
as if every statement had been checked.

## Decision

`require_paired` is a guard on `rule-artifact.v15`, admitted by
`artifact-package.v40`. The node names one identity key, one withholding
fact type, and one or more income fact types.

It reads the identity keys of the current rows of those fact types. It
reads no values. A row whose amount is zero still counts, because the row
exists.

- A null or missing key blocks `DEPENDENCY_INVALID` and names that finding
  id. That check runs before the absence check.
- An uninstalled row slot blocks `DEPENDENCY_INVALID` with
  `link-coverage-scope-unbound`.
- An income row whose key has no withholding row on that same key blocks
  `DEPENDENCY_ABSENT` and names the withholding fact type, once. The
  existing input question for that amount is what shows.
- A withholding row with no income row is not a failure.
- The key is the name the rule writes (`statement` or `w2-slip`).

On a pass or an absent-withholding block it records every examined finding
id; on a null or missing key it records only the offending ids. The recorded
ids are pinned as inputs. It does not
sum, it does not change a line's value expression, and it does not invent
question wording.

## Consequences

- A successor rule can require each current income statement to carry its
  own withholding row, and a missing row still shows the question that
  fact type already has.
- Earlier rule and package versions do not contain the operation, so their
  published bytes stay as they are.
- This status is proposed. The text is not authority until it is accepted.

## Links

- Schema: `rule-artifact.v15`, `artifact-package.v40`
- Evidence: `docs/phases/engine-breadth/milestones/statement-withholding-pairing-evidence/track1.md`
