# Charter: P0 of line 12d's boxes being shown

Role: Builder. Source HEAD on milestone/line12d-boxes-2025.
Plan: docs/phases/engine-breadth/milestones/line12d-boxes.md (read it
whole). Precedent: age-blindness-asked-evidence/ (p0.md, law.json,
prototype.py, track0.py) and saved-page-observation findings on the
categorical renderer. Do not read governance.

## Scope

1. **Trace.** How a categorical Form 1040 field is declared, published and
   rendered today (form-field citizens, field-mapping rules, the
   presentation model and the saved citation-walk renderer), with an
   existing checkbox-like field as the example. Cite file:line.
2. **Law.** Quote the 2025 Form 1040 line 12d instruction (when each box
   is checked; head of household; qualifying surviving spouse; a separate
   return), reusing age-blindness-asked-evidence/law.json and checking
   its checksum.
3. **Design.** The smallest content change that shows the four boxes from
   the recorded answers, with their citations, only where the instructions
   check them. Prototype it as scratch core v90 on published v89, loaded
   from published content, never by editing packages/. Probe each case in
   the plan through `live_coordinate_run` and the presentation model:
   the box states shown against the instructions.
4. **Rerun.** Replay the recorded lists with
   `python3 tools/recorded_replay.py` on v89 and scratch v90 (at most 4
   workers), answered as their records imply (age and blindness false,
   per tests/helpers). Classify every change; the target is identical
   numbers and only the new fields added.

Stop and report if the design needs an engine, schema, projection or
renderer change; name the smallest one.

## Deliverables

In docs/phases/engine-breadth/milestones/line12d-boxes-evidence/: p0.md
(trace, law, design, probe results, rerun classification,
recommendation, decisions for the foreman), the scripts and their small
JSON outputs. Fill a "P0 result" section in the plan. No production, test
or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Never --no-verify or a bare git stash. Foreground commands only.
- No push and no spawn. Do not edit packages/.
