<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth (closed)",
  "topic": "engine-breadth-phase-close",
  "active_plan": "docs/phases/engine-breadth/engine-breadth-roadmap.md",
  "milestone_state": "closed",
  "retrospective": "docs/milestone-retrospectives/2026-08-18-engine-breadth.md",
  "status": "Engine Breadth closed 2026-08-18 by owner judgment, not frontier exhaustion. No active milestone and no successor phase selected or named. Remaining frontier rows and filed hardening are unselected.",
  "current_role": "none — between phases",
  "current_prompt": "docs/phase-state.md#None — between phases"
}
-->

# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Curated history and architectural decisions live in retrospectives
and `docs/adr/`; historical execution records live under `docs/archive/`.

## High Level Briefing

**Engine Breadth closed on 2026-08-18.** The phase widened the classes of 2025
federal returns the engine computes through synthetic authoritative surfaces,
including additional interest and dividend sources, Schedule D and Form 8949
capital paths, Schedule 1 income and adjustment paths, Social Security and IRA
income, mortgage interest, and student-loan interest through AGI.

Read that completion as computation breadth. It did not change the user's input
workflow: facts are still entered by hand-editing JSON. It also did not make a
return fileable. Those gaps were already named when Real Return closed, were
outside Engine Breadth's frontier, and remain open.

The frontier is not exhausted. General Form 1116, other Schedule D sources,
other Schedule K-1 boxes, and a re-cut noncovered-basis/Form 8949 contract
remain live recorded candidates. The phase closes by owner judgment because
further rows would add instances of a vertical shape already proved roughly
twenty times, not because no coverage work remains.

## Operational State

- **Phase:** Engine Breadth — **CLOSED 2026-08-18**.
- **Active milestone:** none.
- **Named successor phase:** none.
- **Next move:** open owner selection. No frontier row, hardening plan, or
  archived draft is selected by this close.
- **Closed selection instrument:**
  `docs/phases/engine-breadth/coverage-frontier.md`.
- **Phase close record:**
  `docs/phases/engine-breadth/engine-breadth-roadmap.md#Phase close — 2026-08-18`.
- **Phase retrospective:**
  `docs/milestone-retrospectives/2026-08-18-engine-breadth.md`.
- **Archived noncovered-basis Track 0 evidence:**
  `docs/archive/2026-08-18-f8949-noncovered-basis-track0/`.
- **Filed but deliberately unselected hardening:**
  `docs/phases/engine-breadth/milestones/rule-artifact-capability-table-consolidation.md`.

## None — between phases

There is no Builder or Reviewer charter, no active milestone, and no selected
successor. The owner holds the next choice. Re-entry should read the phase close
and retrospective, then stop at that open selection rather than treating any
remaining frontier row as chosen.

The advisory repository capsule remains available for mechanical consistency
checks:

```sh
python3 tools/foreman_context.py --ref HEAD --format markdown
```
