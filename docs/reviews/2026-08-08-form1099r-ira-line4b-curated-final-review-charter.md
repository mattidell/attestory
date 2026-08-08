# Final Review Charter — Fully Taxable IRA Distributions to Form 1040 Line 4b

Audience: Reviewer

## Review target

Review the complete curated milestone range from `origin/main` through the
current milestone head. This is the final independent review before PR #162
can be marked ready. The candidate contains the plan, one Track 1 commit, and
one Track 2 commit; no review or repair checkpoint is part of the durable
history.

## Required questions

- Does the implementation satisfy the bounded 2025 Form 1099-R IRA-family,
  code-7, box-1/box-2a-equality, explicit box-2b-negative class without
  calculating basis, rollover eligibility, or special treatment?
- Do line 4b, line 9, AGI, taxable income, regular tax, explanation, citations,
  package resolution, and presentation preserve the plan's authority and
  exclusion contracts?
- Does the production resolver preserve historical package behavior for v17,
  v23, v24, and v25 while enforcing exact entrypoints for the v26 successor?
- Do the focused tests exercise source admission, closure, compatibility,
  stale/dangling entrypoint hard refusal, and the named sibling regressions?
- Are published schemas, manifests, historical package bytes, fixtures, and
  data-safety boundaries intact, and are transient working records absent?

## Evidence required

Inspect the exact pushed head and its complete `origin/main..HEAD` diff. Run
the applicable focused tests and static/governance checks, then report a
falsifiable READY or BLOCKED verdict tied to this head. A new product decision,
lost upstream semantic-ledger member, altered producer selection, lost schema
admission, lost composition obligation, or scope expansion is blocking and
must return to the owner.

## Owner-launch prompt

> Resume as Reviewer for this charter. Orient from HEAD, verify the exact
> curated range against the tool-derived ratified line, inspect the plan and
> both implementation commits, and review the complete final diff. Exercise
> the production resolver compatibility matrix and exact-entrypoint refusal
> boundaries, verify published-history and data-safety integrity, and return a
> READY or BLOCKED verdict for the exact head. Do not modify the candidate.
