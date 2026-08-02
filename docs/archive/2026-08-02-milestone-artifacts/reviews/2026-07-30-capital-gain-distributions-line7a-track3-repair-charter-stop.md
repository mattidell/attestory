# Capital-Gain Distributions / Line 7a — Track 3 Repair Charter Stop

Audience: Owner and Foreman.

Status: **resolved as a repair-charter scope defect; no implementation landed.**

## Clean stop

The continuing Track-3 Builder oriented at
`b2d0c167d253f945c5f111223bbdab2512cf212e`, probed the required universal
field-citation chain, and stopped before committing. The worktree was restored
cleanly to the charter commit.

The probe showed that established valid v8 presentation fields, including
line 11, declare a field citation while their owning historical rules do not
declare a `citations` list. Requiring every published form field to prove its
field citation through an owning-rule citation therefore rejects existing
goldens and would require historical rule/package changes. Both outcomes are
outside the Track-3 repair boundary.

## Foreman triage

This is a charter defect, not evidence that F1–F3 require a new contract or
substrate. The reviewed Track-3 obligation is exact citation validation for the
new line-7a/line-7b paths, whose owning rules already declare citations. The
repair can stay generic and preserve legacy behavior by applying the
rule-to-field exactness check whenever the owning resolved rule declares
citations, while rejecting duplicate resolved citation identities globally.
No line-specific identifier, historical content edit, model-version change, or
valid-output change is needed.

The amended repair charter records that narrower invariant. The single repair
pass remains unconsumed because no implementation commit was created.
