# Charter: P0 of line explanations

Role: Builder. Source HEAD on milestone/line-explanations-2025.
Plan: docs/phases/engine-breadth/milestones/line-explanations.md (read it
whole). Do not read governance.

## Scope

On core v77 (`package.core-calculations.v77.json`, its registry and its
release):

1. **Inventory.** Every form-field member of v77: id, version, form, line,
   label, and the five disposition texts. Classify each text as specific
   (says what the line adds, why it is zero, or why it shows no value) or
   generic ("blocked", "guard false", "closure zero", a bare label, or
   boilerplate shared across lines). Give counts by form and by
   disposition.
2. **Where a filer reads it.** Through `live_coordinate_run` and the
   presentation projection and page, run the plan's cases with synthetic
   `demo.*` findings. Show where each text appears (page row, explanation
   walk, blocked panel) and what sits beside it (the missing-input
   questions). Note any text a filer never sees.
3. **Draft.** For each generic text, a plain replacement drawn from the
   line's own instruction words (the citation and the local instruction
   source the citation names) and the rule the field binds. Say what the
   line adds; for a zero, why it is zero; for a block, what kind of input it
   waits for; for a guard, which condition does not hold. Where one static
   text cannot say which of several guards failed, say so and propose the
   most honest general text. Short, plain sentences; no internal ids.
4. **Mechanics.** What pins the current texts: goldens, tests, validators,
   length or pattern limits in `form-field.v2`. Whether a successor field
   version and a package successor are enough. Count the files a v78
   successor touches. Prototype a few successors in a scratch copy under
   the evidence directory (never under packages/content) and render one
   case on it.

Stop and report if the change needs a schema, engine or projection change;
give the cause and the smallest change.

## Deliverables

docs/phases/engine-breadth/milestones/line-explanations-evidence/:
p0-inventory-and-draft.md (inventory table, where-read findings, draft
wording table, mechanics, and a one-paragraph recommendation), the probe
script and its JSON output, the prototype and its output. Fill the plan's
"P0 result" section (a short summary that links the evidence). No
production, test or content edits.

## Rules

Synthetic demo.* only; no absolute paths in committed files. Commit
incrementally with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
retry every 10 s up to 5 min if held); never --no-verify; never bare git
stash. Foreground commands only; no pgrep or sleep waiters. No push or
spawn. Do not edit packages/kernel/.
