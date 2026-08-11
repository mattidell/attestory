<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f8949-noncovered-basis",
  "active_plan": "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md",
  "milestone_state": "track-0",
  "status": "**ENGINE BREADTH / BROKER-FURNISHED NONCOVERED BASIS THROUGH FORM 8949 BOXES B/E AND SCHEDULE D LINES 2/9 \u2014 TRACK 0 REOPENED A THIRD TIME.** The owner's five blockers of 2026-08-11 (B1\u2013B5) are answered: ADR-0065 publishes `attachment-rule.v7` (additive union of v6's row model and v4's value-checked answers, plus family-occupancy applicability, `completeness.required_closures`, and `branch_requirements[].asserts_families_empty`), and ADR-0063 Decision 4 restates the correction/membership boundary as a rule. An external review of head `88b4628` then returned **NOT READY** and the closure-gate declaration is **retracted to FAIL**. Three blockers remain: (C1) `required_closures` is specified to run only once the attachment is required, but `runner.py:822\u2013830` returns `inapplicable` before completeness runs, so all-empty transaction families plus one unclosed scalar companion still yields Schedule D inapplicable while line 2/9 blocks \u2014 the exact B3 disagreement; (C2) ADR-0065's exact-equality validator cannot be implemented generically because no attachment citizen declares which line symbols it accounts for, so Track 1 would have to key it on Schedule D's rule id \u2014 the mechanism B5 rejected; (C3) the gate cannot self-declare PASS while documenting two residuals that are counterexamples to its own bar \u2014 **narrowing the bar is an owner decision and is with the owner now**. Mechanical repairs R1\u2013R4 are already made by the foreman. Three ADRs remain `proposed`; **no implementation charter may be filed**. Base: origin/main f60e7d1, core-calculations v29 / published v24 / release v22 / adopt v29. `f1098e-student-loan-interest-line21` (PR #169) contends for the package numbers but **not** for the `attachment-rule.v7` filename \u2014 it proposes `rule-artifact.v5`; the earlier collision claim is withdrawn.",
  "retrospective": null,
  "current_role": "Track 0 Builder",
  "current_prompt": "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#Track 0 charter, reopened a third time (2026-08-11)"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Curated history and architectural decisions live in retrospectives
and `docs/adr/`; historical execution records live under `docs/archive/`.

## High Level Milestone Briefing

The engine computes the closed Engine Breadth synthetic routes through Form
1099-DIV box 2a and box 12, Schedule K-1 box-5 interest, market-discount
interest, Schedule B adjustments, covered Form 1099-B capital paths including
inbound carryovers and Form 8949 wash-sale (code W) lines 1b/8b, Form 1099-INT
box 8 tax-exempt interest on line 2a, Form 1099-G box-1 unemployment through
Schedule 1 into Form 1040 line 8, the bounded Form 1099-DIV box-7 direct
foreign tax credit, the merged IRA line-4b route, the bounded SSA-1099
Benefits Worksheet route through Form 1040 lines 6a/6b, and the bounded Form
1098 home-mortgage interest route through Schedule A and Form 1040 line 12e.
The selected next milestone extends the Form 1099-B capital path to
transactions whose basis the broker shows to the recipient but does not report
to the IRS, routing them through Form 8949 boxes B and E into Schedule D
lines 2 and 9.

## Operational State: Engine Breadth

* **Active milestone:** Broker-Furnished Noncovered Basis through Form 8949
  Boxes B/E and Schedule D Lines 2/9 — **track-0**. Owner approved the plan
  and authorized dispatch on 2026-08-10.
* **Plan:** `docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md`.
  Controlling sections: "Track 0 charter, reopened a third time (2026-08-11)",
  "Attachment substrate decision (B2)", and "The chosen shape". The rerun
  closure gate's declaration is **retracted to FAIL**; earlier expressibility
  and closure sections are retained with SUPERSEDED banners and are not
  authority.
* **In flight:** Track 0, reopened a third time after an external review of head
  `88b4628` returned NOT READY. That review accepted the tax routing, the
  transaction model, ADR-0063's authority and correction/membership boundary,
  and occupancy as the right applicability concept. Three contract blockers
  (C1–C3) are in the third charter; the foreman verified each against committed
  source before filing and made the four mechanical repairs (R1–R4) itself.
* **Awaiting owner decision — C3, the gate's scope.** ADR-0063, ADR-0064, and
  ADR-0065 stay `proposed`; **do not ratify yet**, because C1 and C2 change
  ADR-0065's text. The question that is the owner's alone: the cannot-disagree
  bar currently has two documented counterexamples (below), both outside this
  milestone's supported class. Either the milestone widens to close them
  declaratively, or the owner narrows the bar to the supported class in
  writing. Track 0 may not dispose of them a third time on its own authority.
* **Standing non-goal lifted and taken:** an additive published
  `attachment-rule` successor is authorized (blocker B2) and ADR-0065 takes it
  as `attachment-rule.v7`. No published version is edited; the schema-intent
  ledger event is appended on `milestone-schema-ledger` (`e80fdd7`, `propose` /
  `additive`). A new schema *kind*, a new evaluator operator, a new
  `derivation-record` enum value, and `source-family.v2` remain non-goals and
  stop conditions.
* **Named residuals (both outside the supported class, both recorded in
  ADR-0065 Consequences):** the ADR-0062 per-transaction row guards and the
  identity-key collision kill-test are dispatched on `rule_id` for the line
  rules and the Form 8949 attachment but never for `attachment.schedule-d`, so
  in those states Form 8949 and lines 1b/8b block while Schedule D reads
  complete. No wrong number escapes, but Schedule D's disposition is wrong.
  Both need a declared row- and identity-constraint vocabulary. **They cannot
  be closed by extending the existing guards' dispatch** — `_LINE_GUARD_BOX_KEYS`
  (`runner.py:176–179`) and the `rule_id` equality at `runner.py:863` are not
  version-gated, so widening them would change dispositions on already-published
  adoptions.
* **Owner dispositions on record:**
  - *2026-08-10* — the identity-collision kill-test covers all fifteen pairs
    across all six Form 1099-B transaction fact types, closing the pre-existing
    cross-term gap. The cross-term kill-test fixture is mandatory in Track 1.
  - *2026-08-11 (second ruling)* — ADR-0063/0064 not ratified. The new-id /
    non-selection shape is approved **in principle**, and the family topology,
    fifteen-pair collision rule, boxes B/E, and lines 2/9 direction are
    preserved. Five contract-level blockers: correction lifecycle must not
    displace closures on an ordinary same-member value correction (only a
    membership or identity transition does); Form 8949 may not stay
    presence-only; whole-family closure must be declaratively load-bearing on
    Schedule D completeness; the `proceeds > 0` requirement proxy is replaced
    by true family occupancy; and the Path A contradiction must live in
    versioned content or schema, not a rule-id-keyed runner guard.
  - *2026-08-11* — completeness shape. `no-other-form8949-adjustments` v1 stays
    published, unchanged, and selected only by historical packages. The
    successor package selects a newly identified wider declaration in its
    place. Discrimination between wash-sale and noncovered activity comes from
    the contributed transaction fact type and its family closure, not from a
    new taxpayer answer; closed-empty families establish which supported
    classes are absent. The no-Form-8949 path is unchanged with a contradiction
    guard whenever a supported Form 8949 family is genuinely nonempty. The
    accepted neighbouring change: a code-W-only return adopting the successor
    package answers the replacement boundary question instead of v1 — a
    substitution, not an extra checkbox — justified by the widened supported
    universe.
* **Superseded record:** the foreman's chained-discriminator recommendation
  was rejected as duplicated authority; the Track 0 stop of 2026-08-10 and its
  five plan corrections stand (guard uses `BLOCK_INVALID`, not a new
  `derivation-record` enum value; the fifteen-pair kill-test needs run-path
  wiring; `attachment-rule` v4 is the only version admitting value-checked
  answers).
* **Base:** origin/main `f60e7d1`; core-calculations **v29**, published
  **v24**, release **v22**, adoption **v29**. No successor version is
  reserved — `milestone/f1098e-student-loan-interest-line21` (PR #169) is
  concurrent and competes for the same numbers.
* **Just closed:** Form 1098 Home-Mortgage Interest through Schedule A and
  Form 1040 Line 12e, closed 2026-08-10. Plan:
  `docs/phases/engine-breadth/milestones/f1098-mortgage-interest-line12e.md`;
  retrospective:
  `docs/milestone-retrospectives/2026-08-09-f1098-mortgage-interest-line12e.md`.
* **Prior closed (record defect, not repaired here):** the SSA-1099 and IRA
  line-4b routes are merged on the ratified line (PR #163 `48d46f9`, PR #162
  `9cecf30`) and their plans remain committed, but neither has a file under
  `docs/milestone-retrospectives/` and both plan capsules still read
  `track-2`. The coverage frontier's status rows were reconciled to the
  committed source in this milestone's planning commit; the missing
  retrospectives are recorded here rather than backfilled, because writing
  them is not this milestone's work.
* **Next:** Track 0 closes C1 (make calculation-relevant closure gate the
  not-required disposition too) and C2 (add the declarative "accounts for"
  surface so the validator is a graph walk, not a rule-id branch), then reruns
  the gate leaving C3 for the owner's answer. Then ratification of all three
  ADRs; then the Track 1 charter, whose first unit is
  `packages/schemas/tax/attachment-rule.v7.schema.json` and the additivity
  demonstration (both existing attachment bodies validate under v7 with only
  their `schema` string changed) before any successor's real edits.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
