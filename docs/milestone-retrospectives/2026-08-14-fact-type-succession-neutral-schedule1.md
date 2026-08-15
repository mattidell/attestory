# Retrospective — Fact-type succession with neutral Schedule 1 vocabulary

## What differed from the plan

- Track 0's paper named individuation from the predecessor fact type as
  the displacing edge. Independent review returned **STOP FOR ADVISOR**
  on that one finding (F1): the reading was live but not the unique
  composition the kernel determines, and the Ontology-turn stop fired.
  The owner corrected the paper rather than approving it. Adoption of
  an explicit migration artifact is a **direct supersession root** — a
  fourth named root beside correction findings, `_member_withdrawals`,
  and superseded-entity ids — not an individuation edge and not a new
  cascade edge. The Amended Track 1 charter replaced the paper's
  original Track 1 proposal. No Ontology amendment. Track 1 independent
  review then returned **APPROVE**. F1 is decided by ADR-0063.
- Mid-build, `artifact-package.v23`'s member-schema enum and
  `packages/derivation/loader.py`'s `ROLE_VOCABULARY` both omitted
  `migration-artifact.v1`. Reading the diff did not catch it; running
  the suite did. Both admissions were added in the Track 1 unit.
- Two deep-read anchors introduced while writing the Track 1 charter
  did not resolve. Anchors match markdown headings exactly, including
  bold markers; a numbered list item is never an anchor target. Folded
  into the disposition/charter unit.

This milestone adds **no new tax route**. Form 1098-E, Schedule 1 line
21, Form 1040 line 10, and AGI remain Part 3, unselected.

## What it cost

- Two independent reviews: Track 0 STOP FOR ADVISOR (F1 only), then
  Track 1 APPROVE with no findings.
- One owner disposition that corrected, not merely blessed, T0-5.
- One schema/loader admission repair found by execution, not by reading.
- One charter-anchor hygiene repair.
- No rival prototype. One new ADR (0063). Publication is core **v31** /
  published-packages **v26** / release **v24**.

## Follow-ups

- Form 1098-E / Schedule 1 line 21 / Form 1040 line 10 / AGI 11a/11b
  remain the next vertical slice and stay owner-unselected. Trigger:
  owner selects Part 3. Consume the thirteen *successor* ids; do not
  revive a predecessor; do not migrate `no-rrb-or-foreign-social-benefit`.
- `audit_collect_authority` still does not audit `count` /
  `require_closed` standing. Durable deferral from Milestone 1;
  unchanged here.
- Deep-read anchors must be real headings, including any markdown
  emphasis. Trigger: any new `deep_reads` entry. The orientation-block
  suite already fails a missing heading.

## What should change in the next plan

- Do not treat a live Ontology reading as a settled composition. If
  two edges could host the same shape, stop for the owner before
  building.
- Admit a new member role in both the package schema enum and
  `ROLE_VOCABULARY` in the same change, and run the suite before
  calling the unit done.
