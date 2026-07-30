# Evaluator D — The Entry Loop (synthetic), Track 2e

Evaluator: D (fresh reviewer brief)
Date: 2026-07-29
Scope: the six rows named by the charter only

## Run conditions

The required orientation command was run with `--ref HEAD`, but refused to
resolve the repository phase-state token `track-2e`. The freshness capsule
command failed on the same token. I did not infer review scope from either
failure. The live evaluation was run with the chartered launcher and the
surface was assessed without opening implementation, tests, or other review
records.

Runner URL: `http://127.0.0.1:55025/entry/0sRg0xT8LThjAd2wwSLOlaJvlLKr0jlP3dlsZ7yqHBY/index.html`

## Raw transcript

- Evaluator: D
- Starting-state fingerprint: `sha256:212e525dd6d29292cd4c692c72ba15b7e03a74fa2e6c17f3c46bae0aebe5c5a5`
- Launcher figures: first entry `90000`; correction `91000`.

### Actions and observations, in order

1. Read the surface's initial DOM. It exposed a `main` landmark, a named form
   `W-2 Box 1 entry`, one missing fact, `W-2 from Demo Workshop — Box 1
   wages`, and an `Enter this fact` action.
2. Clicked `Enter this fact` (unique count 1). The W-2 Box 1 textbox became
   active.
3. Before typing, recorded the field guidance: `Form W-2 · Box 1`, `Wages,
   tips, other compensation`; the amount feeds `Form 1040 line 1a` and
   resolves the missing wages needed to compute income; accepted syntax was
   dollars and cents, with or without comma grouping and an optional `$`
   prefix, examples `90000` and `90000.50`.
4. Attempted `Tab` from the textbox with Playwright, then with the browser
   keyboard API, then after a coordinate click. Focus remained on the
   textbox each time. Attempted `Shift+Tab` from the textbox with both browser
   keyboard APIs; focus again remained on the textbox. These attempts did not
   provide a usable traversal measurement.
5. Filled `abc` and clicked `Add W-2 Box 1` (unique count 1). A visible alert
   appeared: `Check this entry.` followed by the format error. The alert did
   not include `abc`; the textbox still visibly contained the rejected input.
6. Filled `90000`. Attempted `Enter` on the submit button; it became active
   but no submission occurred. Clicked `Add W-2 Box 1`; it changed to
   `Checking…` and then the surface reached `0 missing facts · fully
   computed`. The status said the entry landed through a contribution.
7. Observed first accepted result: expected-impact rows 1040 lines 1a, 9,
   11, 15, and 16 were each marked `changed` with values `$90,000.00`,
   `$93,234.00`, `$93,234.00`, `$78,234.00`, and `$12,222.00`; comparison
   rows 2b, 3a, 3b, and 12 were each marked `unchanged` with `$1,234.00`,
   `$600.00`, `$2,000.00`, and `$15,000.00`.
8. Clicked `Correct this fact` (unique count 1). The answered fact remained
   reachable and the textbox became active with `90000`.
9. Filled `91000`, clicked `Update W-2 Box 1` (unique count 1), and waited for
   the result. The surface remained complete; the status said the correction
   landed through a contribution. The displayed answered fact became
   `$91,000.00`; expected-impact values became `$91,000.00`, `$94,234.00`,
   `$94,234.00`, `$79,234.00`, and `$12,442.00`; comparison rows remained
   unchanged.
10. Filled `abc` in the completed-state textbox and clicked `Update W-2 Box
    1`. The same visible format alert appeared and did not echo `abc` in its
    error text; the previously computed result remained displayed.
11. Restored `91000` and clicked `Update W-2 Box 1`. The surface returned to
    the complete state. On this same-value re-submission the five
    expected-impact rows were displayed as `unchanged`; this is recorded as an
    observation touching unscored rows 3.2 and 3.3, not scored here.
12. Attempted `Space` on `Review W-2 Box 1` and then the browser keyboard
    `SPACE` API. The button became active/focus-visible, but neither attempt
    activated the action. This was not used as a definitive surface failure
    because the keyboard API also failed to advance Tab focus.

## Six-row score sheet

| Criterion | Score | Transcript reference and rationale |
| --- | --- | --- |
| 2.1 — field names source document and exact box | Pass | Steps 1–3. The field identifies `Form W-2 · Box 1` and the W-2 wages label before entry. |
| 2.2 — field states why the fact is asked for and its return destination | Pass | Step 3. Field-attached text names `Form 1040 line 1a` as the immediate destination and says the entry resolves missing wages needed to compute income. |
| 2.3 — accepted format can be stated without guessing | Pass | Step 3. The guidance explicitly states dollars/cents, comma grouping, optional `$`, and examples; steps 5–6 confirm the visible validation behavior is consistent with that guidance. |
| Carries over: Accessibility baseline | Fail | Steps 2, 4, 6, 9, and 12; landmarks and form naming were present, and all observed controls had `tabIndex=0`. Rendered measurements show focus failures: the textbox's `:focus-visible` rendering had a cream `rgb(255,253,248)` ring against a white `rgb(255,255,255)` field, 1.02:1; the review button's dark `rgb(23,37,31)` focus ring against the green review background `rgb(7,94,79)` was 2.06:1. Both are below the required 3:1. Actual Tab/Shift+Tab traversal and key activation could not be independently measured because the browser interaction attempts did not advance or activate. |
| Carries over: Fail-loud | Pass | Steps 5 and 10. Malformed `abc` produced a visible on-page `alert` with a specific format error. |
| Carries over: Blanket redaction | Pass | Steps 5 and 10. The visible error text did not contain the rejected value `abc`. |

## Contrast measurements

Ratios are computed from the rendered RGB values. Text uses the 4.5:1 bar;
visible control boundaries and focus indicators use the 3:1 bar.

| Context | Element / rendered colors | Ratio | Result |
| --- | --- | ---: | --- |
| Initial missing state, gold missing-fact panel | `Enter this fact`: text `rgb(7,94,79)` on button `rgb(255,253,248)` | 7.59:1 | Pass |
| Initial missing state, gold missing-fact panel | `Enter this fact` teal boundary `rgb(7,94,79)` against panel `rgb(255,243,215)` | 7.00:1 | Pass |
| Initial missing state, cream entry panel | W-2 textbox text `rgb(23,37,31)` on field `rgb(255,255,255)` | 15.90:1 | Pass |
| Initial missing state, cream entry panel | W-2 textbox dark boundary `rgb(23,37,31)` against panel `rgb(255,253,248)` | 15.64:1 | Pass |
| Initial/error state, cream entry panel | `Add W-2 Box 1`: white text on teal `rgb(7,94,79)` | 7.71:1 | Pass |
| Initial/error state, cream entry panel | Add button teal boundary against panel `rgb(255,253,248)` | 7.59:1 | Pass |
| Validation-error state | Alert text `rgb(103,26,12)` on `rgb(255,240,236)` | 10.94:1 | Pass |
| Validation-error state | Alert border `rgb(155,44,23)` on `rgb(255,240,236)` | 6.84:1 | Pass |
| Accepted/corrected state, cream entry panel | `Update W-2 Box 1`: white text on teal `rgb(7,94,79)` | 7.71:1 | Pass |
| Accepted/corrected state, cream entry panel | Update button teal boundary against panel `rgb(255,253,248)` | 7.59:1 | Pass |
| Accepted/corrected state, green review panel | `Review W-2 Box 1`: teal text `rgb(7,94,79)` on button `rgb(255,253,248)` | 7.59:1 | Pass |
| Accepted/corrected state, green review panel | Review button white boundary `rgb(255,255,255)` against panel `rgb(7,94,79)` | 7.71:1 | Pass |
| All entry-panel input states | Textbox `:focus-visible` cream ring `rgb(255,253,248)` against white field `rgb(255,255,255)` | 1.02:1 | Fail |
| Accepted/corrected green review context | Focus ring `rgb(23,37,31)` around Review button against green panel `rgb(7,94,79)` | 2.06:1 | Fail |

The observed update-button focus state in the cream entry panel also showed a
dark `rgb(23,37,31)` ring against `rgb(255,253,248)` at 15.64:1, and a cream
outline against the teal button at 7.59:1. Those portions pass; the input and
green review contexts above do not.

## Points where the surface required inference

1. The missing-fact card says `W-2 from Demo Workshop — Box 1 wages`, so I
   treated that as the document identity and exact source box; no outside tax
   knowledge was needed.
2. I treated “dollars and cents” plus the two examples as the complete format
   guidance, rather than inferring a different precision or sign convention.
3. I inferred that the visible status phrase `0 missing facts · fully
   computed` was the complete state only because its adjacent text explicitly
   said every required fact was present and the return was fully computed.
4. The surface did not expose a control-specific focus-color explanation. I
   therefore measured the rendered focus ring and its adjacent background
   rather than inferring that the persistent dark textbox border was a focus
   indicator.
5. The browser interaction layer did not make Tab/Shift+Tab or Enter/Space
   traversal observable. I did not infer success from `tabIndex=0` or from a
   focused control, and did not convert those failed measurement attempts into
   an additional accessibility claim.

## What would make the failed row pass

Provide a focus-visible indicator whose rendered contrast is at least 3:1 in
every reachable context: a contrasting focus ring around the textbox rather
than a 1.02:1 cream-on-white ring, and a contrasting ring around controls in
the green review panel rather than the 2.06:1 dark-on-green ring. Then verify
Tab/Shift+Tab traversal and Enter/Space operation with a keyboard path that
actually advances and activates controls.

## Unmeasured, ambiguous, and out-of-scope observations

- Unmeasured: reliable Tab/Shift+Tab reachability and keyboard activation;
  the browser control attempts did not move focus or activate actions.
- The focus indicator interpretation is explicit: the persistent textbox
  border was treated as a control boundary, while the focus-specific cream
  ring was measured as the focus indicator.
- Out-of-scope observation: the first accepted entry showed the expected-impact
  set as changed and the untouched set as unchanged; the same-value correction
  re-submission later showed the expected-impact set as unchanged. This would
  touch rows 3.2 and 3.3, which are not scored in this partial re-score.

