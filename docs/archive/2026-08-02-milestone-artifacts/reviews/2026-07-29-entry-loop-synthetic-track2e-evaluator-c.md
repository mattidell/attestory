# Entry Loop (synthetic), Track 2e — Evaluator C scores

Evaluator: C (Builder brief)
Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-29-entry-loop-synthetic-track2e-evaluator-c.md`
Scope: the six chartered rows only. No aggregation, cell verdict, maturity claim, or score of the other fourteen rows is made here.

The required orientation command was attempted with `--ref HEAD` and with the explicit reviewer fallback. Both were refused because `docs/phase-state.md` contains milestone state `track-2e`, which the tool reports as invalid. I adopted the reviewer seat instructions and continued under this charter; the charter controls the evaluation scope.

## Raw transcript

1. Started `python3 -m packages.derivation.runners.entry_loop_evaluation` with system `python3` and no `.venv`.

   - First URL: `http://127.0.0.1:51503/entry/wPLoWrsqZzdLQiZOew_jhn8RJdvmGq_xYi9SGW6uIFE/index.html`
   - Box 1 entry: `90000`; correction printed: `91000`.
   - Starting-state fingerprint: `sha256:212e525dd6d29292cd4c692c72ba15b7e03a74fa2e6c17f3c46bae0aebe5c5a5`.

2. Loaded the surface. The initial DOM exposed one `main` landmark and a form named `W-2 Box 1 entry`. The only input's visible field text was `Form W-2 · Box 1` / `Wages, tips, other compensation`. Field-attached purpose text said the amount feeds Form 1040 line 1a and resolves the missing wages needed to compute income. Format text said dollars and cents, optional comma grouping, optional `$` prefix, with examples `90000` and `90000.50`.

3. Focus and keyboard checks on the initial surface:

   - The home link, missing-fact button, and primary submit button could each be focused with a keyboard-style locator action and each matched `:focus-visible`; their focus styles were observable.
   - The amount input also matched `:focus-visible`, but its computed style was `outline-style:none`, `outline-width:0px`, with only its unchanged base shadow `rgb(255, 253, 248) 0 0 0 2px`. No focus-specific visible indicator was present.
   - Attempts to advance with `Tab` and `Shift+Tab` through the browser control left the active element unchanged. `Enter` and Space-style locator presses focused buttons but did not activate their handlers; clicking the same controls did. These keyboard sub-checks were therefore not independently confirmable with this browser-control surface.

4. Filled the amount input with `90abc`. Pressing the submit control with Enter and Space produced no state change. Clicking `Add W-2 Box 1` produced an on-page `alert`:

   `Check this entry.`
   `Enter W-2 Box 1 as a positive dollar amount with or without comma grouping and an optional $ prefix and with no more than 2 decimal places.`

   The rejected string did not occur in the alert or other visible body text. The textbox retained the typed value as an editable control, but the error message did not echo it. Browser console logs contained no error or warning entries.

5. Queried `GET /api/state` independently after the rejected submission. The runtime reported `accepted:false`, `answered:[]`, `complete:false`, and revision `47`; no contribution had been admitted.

6. Replaced the input with `90000` and clicked `Add W-2 Box 1`. After the request settled, the surface showed `0 missing facts · fully computed`, `Accepted. The entry landed through a contribution.`, and the answered fact `W-2 Box 1: $90,000.00`. The input remained reachable in the review form.

7. Queried `GET /api/state` independently after acceptance. The runtime reported `accepted:true`, `complete:true`, `computed:true`, `last_action:"entered"`, answered value `90000`, and revision `50`. This confirmed the accepted value at the system boundary rather than relying only on the page's success text.

8. On the completed surface, focused `Review W-2 Box 1` with a keyboard-style action. It matched `:focus-visible` and had `outline: 2px solid rgb(255, 253, 248)` plus `box-shadow: rgb(23, 37, 31) 0 0 0 5px` against the dark-green completion region. The completed status region also became keyboard-visible when the accepted response landed.

9. Submitted `90abc` once more from the answered form. The rendered error context was `rgb(255, 240, 236)` with border `rgb(155, 44, 23)` and text `rgb(103, 26, 12)`; the raw rejected value was absent from the error text. Reloading restored the accepted state without another accepted contribution.

10. Stopped the first launcher and performed the charter's clean restart. The second URL was `http://127.0.0.1:57227/entry/IakxdQsBygkO7bvcEShIXQLRHgVny0_a2njvBKpz1Lg/index.html`; it printed the same starting-state fingerprint `sha256:212e525dd6d29292cd4c692c72ba15b7e03a74fa2e6c17f3c46bae0aebe5c5a5`. On this clean initial surface, the missing-fact button focus ring was measured against the missing-card background, and the primary submit button focus ring was measured against its dark-green background.

## Contrast measurements

Contrast ratios use the WCAG relative-luminance calculation from the actual computed rendered RGB colours. The 11 colour contexts observed were `#f2efe8` page, `#fffdf8` cards, `#fff3d7` missing card, `#8a5a00` missing marker, `#fff` input, `#f8fbf9` currency prefix, `#f2f1ec` comparison panel, `#edf4ef` complete page/answered fact, `#f5fff8` completed status card, `#075e4f` completion region, and `#fff0ec` validation error.

| Element and context | Foreground / background | Ratio |
| --- | --- | ---: |
| Initial body copy / page | `#17251f` / `#f2efe8` | 13.85:1 |
| Missing-card heading/body | `#17251f` / `#fff3d7` | 14.43:1 |
| Missing marker | `#ffffff` / `#8a5a00` | 5.93:1 |
| Entry and impact card text | `#17251f` / `#fffdf8` | 15.64:1 |
| Entry secondary copy | `#3f5149` / `#fffdf8` | 8.31:1 |
| Currency symbol / input | `#17251f` / `#ffffff` | 15.90:1 |
| Currency prefix panel | `#35463f` / `#f8fbf9` | 9.60:1 |
| Comparison panel text | `#17251f` / `#f2f1ec` | 14.06:1 |
| Complete page text | `#17251f` / `#edf4ef` | 14.22:1 |
| Completed status text | `#17251f` / `#f5fff8` | 15.55:1 |
| Accepted status accent | `#075e4f` / `#f5fff8` | 7.54:1 |
| Completion-region body text | `#ffffff` / `#075e4f` | 7.71:1 |
| Completion-region step text | `#cde9dd` / `#075e4f` | 5.98:1 |
| Completion-region explanatory text | `#eef9f4` / `#075e4f` | 7.16:1 |
| Validation error text | `#671a0c` / `#fff0ec` | 10.94:1 |

Visible control-boundary measurements by background context:

| Control and context | Boundary / surrounding background | Ratio |
| --- | --- | ---: |
| `Enter this fact` / missing card | `#075e4f` / `#fff3d7` | 7.00:1 |
| `Add W-2 Box 1` / entry card | `#075e4f` / `#fffdf8` | 7.59:1 |
| Amount input / input background | `#17251f` / `#ffffff` | 15.90:1 |
| Amount input / entry-card surround | `#17251f` / `#fffdf8` | 15.64:1 |
| `Update W-2 Box 1` / entry card | `#075e4f` / `#fffdf8` | 7.59:1 |
| `Review W-2 Box 1` / completion region | `#ffffff` / `#075e4f` | 7.71:1 |

Focus-indicator measurements:

| Focused control and context | Indicator colour / background | Ratio |
| --- | --- | ---: |
| `Enter this fact` / missing card | outer `#17251f` / `#fff3d7` | 14.43:1 |
| `Enter this fact` / missing card | inner `#fffdf8` / `#fff3d7` | 1.08:1 |
| `Add W-2 Box 1` / dark-green button | inner `#fffdf8` / `#075e4f` | 7.71:1 |
| `Review W-2 Box 1` / dark-green completion region | inner `#fffdf8` / `#075e4f` | 7.71:1 |
| `Review W-2 Box 1` / dark-green completion region | outer `#17251f` / `#075e4f` | 1.00:1 |
| Amount input / white input background | computed focus outline: none; base shadow `#fffdf8` / `#ffffff` | 1.02:1, not a focus indicator |

The dark outer ring and light inner outline are a two-colour indicator. Where one component is below 3:1, the other component is the visible contrasting component; the amount input has no such contrasting focus-specific component.

## Six-row score sheet

| Criterion | Score | Transcript reference and rationale |
| --- | --- | --- |
| 2.1 — field names source document and exact box | Pass | Transcript 2. The sole input visibly names `Form W-2 · Box 1` and `Wages, tips, other compensation`; the missing-document card also identifies `Form W-2, Box 1`. |
| 2.2 — field states why the fact is asked for and its return destination | Pass | Transcript 2. Field-attached text names the immediate destination, Form 1040 line 1a, and the completion purpose, resolving the missing wages needed to compute income. This exceeds the required minimum and is not merely `required`. |
| 2.3 — accepted format can be stated without guessing | Pass | Transcript 2. Before entry, the surface states dollars and cents, optional comma grouping, optional `$` prefix, and concrete examples `90000` and `90000.50`. |
| Carries over: Accessibility baseline | Fail | Transcripts 3, 8, and 10 plus the measurements above. Text contrast and visible control boundaries measured above their thresholds, and named `main`/form landmarks were present. However, the amount input matched `:focus-visible` while computing to no outline and only a 1.02:1 base shadow against the input background; its keyboard focus was not visibly indicated. The Tab/Shift+Tab and Enter/Space sub-checks were also not independently confirmable with the browser-control key operation. The missing focus indicator alone fails the bundled baseline. A Pass would require a focus-specific indicator on the amount input with a component measuring at least 3:1 against its surrounding background, plus a successful keyboard traversal/activation check. |
| Carries over: Fail-loud | Pass | Transcript 4. A malformed value caused a visible on-page `role=alert` with a specific validation message; it was not console-only. Transcript 5 confirms the backend state did not change. |
| Carries over: Blanket redaction | Pass | Transcripts 4, 5, and 9. The malformed value `90abc` was rejected and absent from the visible error text; the message used a generic format explanation. The input's retained editable value is not an echoed error message. |

## Notes and limits

- I did not open or inspect either other evaluator file, the first-run evaluator files, or the aggregation record.
- The direct Tab/Shift+Tab and standard Enter/Space operations could not be completed through the available browser-control key interface; I have not inferred a pass for those sub-requirements.
- No ambiguity in 2.1, 2.2, 2.3, Fail-loud, or Blanket redaction prevented scoring.
- No observation requiring a note on any of the fourteen unscored rows was made.
