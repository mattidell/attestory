<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "f8949-noncovered-basis",
  "active_plan": "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md",
  "milestone_state": "track-0",
  "status": "**ENGINE BREADTH / BROKER-FURNISHED NONCOVERED BASIS THROUGH FORM 8949 BOXES B/E AND SCHEDULE D LINES 2/9 — TRACK 0 IN FLIGHT.** Owner approved the plan and authorized dispatch on 2026-08-10, and disposed the one open closure item in favour of the recommendation: the identity-key collision kill-test covers all fifteen pairs across all six Form 1099-B transaction fact types, closing the pre-existing cross-term gap inside this milestone. **Track 0 stopped before drafting either ADR**: the plan's Topic 6 mechanism (a `no-other-form8949-adjustments` v2 successor pinned per completeness path) is not expressible — the runtime binds findings to symbols by fact-type id only and never reads the version pin, so v1 and v2 are one symbol with one answer. The foreman verified this against `marshal.py` and `runner.py`. A chained-discriminator replacement is recommended; the disposition is with the owner. See the plan's "Track 0 stop (2026-08-10)" section. Base: origin/main f60e7d1, core-calculations v29 / published v24 / release v22 / adopt v29. Concurrent milestone `f1098e-student-loan-interest-line21` (PR #169) competes for the same version numbers; the plan carries a Parallel Work Manifest and an additive-union-at-publication rule.",
  "retrospective": null,
  "current_role": "Track 0 Builder",
  "current_prompt": "docs/phases/engine-breadth/milestones/f8949-noncovered-basis.md#Track 0 charter (2026-08-10)"
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
  The paper-rung decision inventory and the adversarial-closure declaration
  are settled inside it; no closure item remains open.
* **In flight — stopped, awaiting owner disposition:** Track 0 was chartered
  to draft ADR-0063 and ADR-0064 at the paper rung and stopped before drafting
  either. The plan's Topic 6 completeness mechanism is not expressible: the
  runtime binds findings to symbols by fact-type **id** only and never reads
  the version pin, so a `no-other-form8949-adjustments` v1/v2 pair is one
  symbol carrying one answer, and a Path C return would satisfy Path B's value
  check. Verified against `packages/derivation/marshal.py` and
  `packages/derivation/runner.py`. Recommended replacement is a chained
  discriminator declaration; see the plan's "Track 0 stop (2026-08-10)"
  section, which also records five plan corrections independent of that
  decision.
* **Owner disposition on record:** the identity-collision kill-test covers all
  fifteen pairs across all six Form 1099-B transaction fact types, closing the
  pre-existing cross-term gap in this milestone. The cross-term kill-test
  fixture is mandatory in Track 1.
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
* **Next:** owner disposition of the Topic 6 completeness mechanism, then
  relaunch Track 0 against the revised plan.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
