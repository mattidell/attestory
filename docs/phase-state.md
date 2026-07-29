<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Legible Entry",
  "topic": "entry-loop-synthetic",
  "active_plan": "docs/phases/legible-entry/milestones/entry-loop-synthetic.md",
  "status": "Milestone 3 (The Entry Loop - synthetic) is OPEN. Tracks 0, 1, 2a, 2b, and 2c are complete. Track 2 evaluation resulted in FAIL (W-2 maturity cell did not move to L2 due to focus/boundary contrast defects and a disputed format validation handling). Repairs landed in 2c (contrast fixed, format extracted). Track 2d is active to make the w2-box1-format declaration govern runtime behavior rather than just presentation. Standing owner directive: Model entry usability as SCHEMA and field contracts rather than accumulating mechanical UI checks.",
  "current_role": "Builder — The Entry Loop (synthetic), Track 2d: make the format declaration honour itself",
  "current_prompt": "docs/reviews/charter-2026-07-29-entry-loop-synthetic-track2d.md"
}
-->
# Phase State

This is the **single re-entry document** pointing to the current state of the
project. Detailed history, review records, and architectural decisions live in
Git, `docs/reviews/`, and `docs/adr/`.

## Operational State: Legible Entry

* **Active Milestone:** Milestone 3 — The Entry Loop (synthetic)
* **Current Track:** Track 2d — Make format declaration govern behavior
* **Maturity Status:** W-2 cell remains at L1 (Track 2 evaluation failed; pending Track 2d completion and evaluator re-run)

### Standing Directives

* **UI Modeling:** Model usability criteria and field contracts as schema rather than accumulating specific HTML/CSS assertions.
* **Entry-Field Contract:** Define source document, box, destination line, purpose, accepted format, and correction affordance centrally.

## Re-entry

Render the advisory capsule from an explicit committed ref:

```sh
.venv/bin/python3 tools/foreman_context.py --ref HEAD --format markdown
```
