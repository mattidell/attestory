<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f8949-noncovered-basis",
  "active_plan": "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md",
  "milestone_state": "track-0",
  "status": "**ENGINE BREADTH / BROKER-FURNISHED NONCOVERED BASIS THROUGH FORM 8949 BOXES B/E AND SCHEDULE D LINES 2/9 \u2014 TRACK 0 REOPENED A SECOND TIME.** The owner reviewed ADR-0063 and ADR-0064 on 2026-08-11 and did **not** ratify. The new-id / non-selection completeness shape is approved in principle, and the family topology, fifteen-pair collision rule, boxes B/E, and lines 2/9 direction are preserved. Five contract-level blockers must be settled first: (B1) an ordinary same-member value correction must not advance the family horizon or displace closures \u2014 only a membership or identity transition does; (B2) Form 8949 may not stay presence-only on attachment-rule.v6, so an **additive published schema successor is now authorized** (combining v6's row model with v4's value-checked answers) and a schema-intent ledger event becomes mandatory; (B3) whole-transaction-family closure must be declaratively load-bearing on Schedule D completeness, not inferred from the scalar companions; (B4) the proceeds>0 attachment-requirement proxy is replaced by a true family-occupancy mechanism, with zero-proceeds/positive-basis and zero/zero boundary fixtures; (B5) the Path A contradiction must be declared in versioned content or schema, not a rule-id-keyed runner guard. The adversarial-closure section and much of the expressibility subsection are superseded and do not pass. Track 0 must settle B2 first, revise the plan and both proposed ADRs in place, rerun the five-artifact gate, and return evidence that attachment applicability, attachment completeness, and line calculation cannot disagree. Base: origin/main f60e7d1, core-calculations v29 / published v24 / release v22 / adopt v29. Concurrent milestone `f1098e-student-loan-interest-line21` (PR #169) also proposes schema work and competes for the same package version numbers; the plan carries a Parallel Work Manifest and an additive-union-at-publication rule.",
  "retrospective": null,
  "current_role": "Track 0 Builder",
  "current_prompt": "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#Track 0 charter, reopened again (2026-08-11)"
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
  **The plan's adversarial-closure section is superseded and does not pass**,
  and the expressibility subsection is partly superseded. Both must be
  rewritten before any implementation charter is filed.
* **In flight:** Track 0, reopened a second time on 2026-08-11. ADR-0063 and
  ADR-0064 are drafted, `proposed`, and **not ratified** — the owner returned
  five contract-level blockers (B1–B5). Charter: the plan's "Track 0 charter,
  reopened again (2026-08-11)". Settle B2 (the attachment-substrate decision)
  first; B3, B4, and B5 depend on what the successor schema can express.
* **Standing non-goal lifted:** an additive published `attachment-rule`
  successor version is now authorized (blocker B2). It remains additive — no
  published version is edited — and it makes a schema-intent ledger event
  mandatory before the schema edit. A new schema *kind*, a new evaluator
  operator, and `source-family.v2` remain non-goals and stop conditions.
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
* **Next:** Track 0 settles the attachment-substrate decision, revises the plan
  and both ADRs in place, reruns the five-artifact closure gate, and returns
  evidence that attachment applicability, attachment completeness, and line
  calculation cannot disagree. Then owner ratification, then the Track 1
  implementation charter.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
