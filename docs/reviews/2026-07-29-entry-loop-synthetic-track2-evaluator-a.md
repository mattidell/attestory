# Entry Loop (synthetic) — Track 2b Evaluation — Evaluator A (Builder brief)

Charter: `docs/reviews/charter-2026-07-29-entry-loop-synthetic-track2b-evaluator-a.md`
Criteria: `docs/phases/legible-entry/entry-usability-criteria.md`
Evidence pack: `docs/phases/legible-entry/entry-loop-synthetic-evidence-pack.md`

Evaluator: Evaluator A (Builder brief) — exercise every criterion as an
explicit system outcome; independently confirm system-level state, not just
what the surface displays.

## Raw transcript

- **Evaluator:** Evaluator A
- **Starting-state fingerprint:** `sha256:7d5abe2ed31df137a323043385b3de7c1c5a5359a0cba7184c43008a6500beb0`
- **Launcher output:** URL
  `http://127.0.0.1:60741/entry/ayzm--v8hhv2vYZefbrRAdo57dalM3e8PF3m-hUznf4/index.html`;
  W-2 Box 1 figure to enter: `90000`; corrected figure: `91000`.
- **Independent system channel used throughout:** the running server exposes
  `GET <route>/api/state`, which returns the runtime's authoritative snapshot
  (the same JSON payload the front end renders from). This is not part of the
  criteria's own text but is the mechanism named in this evaluator's brief for
  confirming "what actually happened" beneath the surface. All comparisons
  below are DOM (Playwright accessibility snapshot) vs. `/api/state` fetched
  independently via `curl`, run at the same points in the sequence.

### Actions and observed results, in order

1. Started `python3 -m packages.derivation.runners.entry_loop_evaluation` in
   the background; recorded URL, figures, fingerprint above.
2. `curl /api/state` before touching the browser: `missing` contained one W-2
   Box 1 entry; all 5 expected-impact lines `computed:false, value:null,
   change:"blocked"`; all 4 comparison lines `computed:true, change:"baseline"`
   with values 2b=1234, 3a=600, 3b=2000, 12=15000; `complete:false`,
   `revision:47`.
3. Navigated the browser to the URL. Page snapshot matched the API: one
   missing-fact list item ("W-2 from Demo Workshop — Box 1 wages", Form W-2
   Box 1), a `main` landmark, a `form` landmark named "W-2 Box 1 entry", all
   five expected-impact lines shown "blocked / Waiting for W-2", all four
   comparison lines shown "baseline" with the same dollar values as the API.
   One console error, `favicon.ico` 404 — cosmetic, not a validation signal.
4. Clicked "Enter this fact" (the missing-item action). Read
   `document.activeElement` afterward: it was the `#w2-box1` input itself
   (`aria-describedby="w2-box1-purpose w2-box1-format"`), not merely a scroll
   into view. This is the system-level confirmation for Criterion 1.2.
5. Typed `90000` into the focused input and submitted via "Add W-2 Box 1".
   Playwright network log showed `POST .../api/contributions => 200`.
   Immediately re-fetched `/api/state`: `accepted:true`, `last_action:
   "entered"`, `missing:[]`, `answered:[{value:90000}]`, `complete:true`,
   `computed:true`, `revision:50`. All five expected-impact lines
   `change:"changed"` with values 1a=90000, 9=93234, 11=93234, 15=78234,
   16=12222. All four comparison lines `change:"unchanged"` with the same
   values as step 2 (1234/600/2000/15000). The DOM snapshot taken at the same
   moment showed the identical labels and dollar figures for all nine lines,
   plus a new "Your entry is complete." heading, a "0 missing facts · fully
   computed" status region, a "Step 4 · Correct an entered fact" section with
   the answered value, and a "Step 5 · Know it is complete" section reading
   "Done — no further required entry". The Step 1 missing-fact list was gone
   entirely. DOM and system state agreed exactly.
6. Clicked "Correct this fact". `document.activeElement` was again `#w2-box1`
   (system-level confirmation for Criterion 4.1).
7. Typed `91000` (not yet submitted). Snapshot showed the Step 3 expected-
   impact list still at the *pre-correction* values ($90,000 / $93,234 / ...)
   — the unsubmitted keystroke had not reached the displayed derived lines.
8. Submitted "Update W-2 Box 1". Re-fetched `/api/state`: `last_action:
   "corrected"`, `answered:[{value:91000}]`, all five expected-impact lines
   `change:"changed"` with values 1a=91000, 9=94234, 11=94234, 15=79234,
   16=12442; all four comparison lines still `change:"unchanged"` at
   1234/600/2000/15000, `revision:52`. DOM snapshot taken at the same moment
   showed identical labels/values for all nine lines. DOM and system state
   agreed exactly, and this is the correction figure the launcher printed
   (91000).
9. Clicked "Correct this fact" again, then typed `not-a-number` into the
   input and submitted. Playwright network log showed
   `POST .../api/contributions => 422`. Console showed the 422 as a browser
   network log entry (not a hidden failure — see next point) plus the
   pre-existing favicon 404. The DOM immediately showed a visible `alert`
   region: "Check this entry. — Enter W-2 Box 1 as a positive dollar amount
   with no more than two decimal places." The rejected string
   `not-a-number` was not echoed anywhere in that message or elsewhere on the
   page. Re-fetched `/api/state`: `revision` unchanged at `52`, `answered`
   value still `91000`, all nine lines identical to step 8 — the invalid
   submission mutated nothing, and no sibling value was hidden or altered.
10. Reset focus to `<body>`, then drove the page with real `Tab` key
    presses (not scripted `.focus()`) and recorded `document.activeElement`
    after each press. Full tab-order enumeration in the "complete" state:
    wordmark link → `#w2-box1` input → "Update W-2 Box 1" (submit) →
    "Correct this fact" → "Review W-2 Box 1". No element in the interactive
    surface was unreachable by Tab; `Shift+Tab` was implicitly exercised by
    the reverse traversal used to re-check element identity between screenshots.
11. With "Correct this fact" focused via real Tab, pressed `Enter`: focus
    moved to `#w2-box1`, same effect as a click. Confirms Enter operates a
    button per the keyboard-operability sub-rule.
12. Typed `91000` again, Tabbed to "Update W-2 Box 1", pressed `Space`:
    the form submitted (network log showed a further `POST
    .../api/contributions => 200`; `/api/state` `revision` advanced to `54`,
    lines showed `change:"unchanged"` since the value hadn't actually
    changed from 91000 — correctly distinguishing "resubmitted same value"
    from "changed"). Confirms Space operates a button.
13. Inspected the page's stylesheets via `document.styleSheets`: found one
    `:focus-visible` rule — `button:focus-visible, input:focus-visible,
    a:focus-visible, [tabindex="-1"]:focus-visible { outline: rgb(155, 75,
    0) solid 3px; outline-offset: 3px; }`.
14. Measured text contrast programmatically: walked every leaf text node,
    read `getComputedStyle().color`, walked up the DOM for the first opaque
    background, and computed WCAG relative-luminance contrast ratios. Lowest
    normal-text ratio observed was 6.28:1 ("unchanged" labels on the
    comparison card); lowest ratio on any measured text was 5.98:1 (Step 5
    intro line, white-ish text on dark green). All measured text ratios were
    ≥ 4.5:1 (in fact all ≥ 5.9:1).
15. Measured the focus indicator's own contrast. Reset focus to `<body>`,
    drove real `Tab` presses to reach "Update W-2 Box 1", screenshotted the
    viewport, and scanned the PNG for the outline colour `rgb(155,75,0)`:
    found 1,765 matching pixels, confirming the indicator renders on real
    keyboard focus (an earlier attempt using scripted `.focus()` after a
    mouse click showed *no* outline pixels at all — Chromium's
    focus-visible heuristic suppresses the ring after a pointer interaction;
    this is expected browser behaviour, not a surface defect, and is why the
    real-Tab method in step 10 onward was used for every focus measurement).
16. Repeated the same screenshot-and-scan for "Review W-2 Box 1" (which sits
    inside the dark-green "done" section) reached via real `Tab`: found
    1,184 outline pixels at `rgb(155,75,0)`, bounding box x∈[509,690],
    y∈[663,718]. Sampled the pixels immediately adjacent to the outline on
    all sides: dominant surrounding colour was `rgb(7,94,79)` (the section's
    dark green), 1,592 of the sampled adjacency pixels. Computed contrast of
    the outline colour against that green: **1.25:1**. The criterion
    requires ≥ 3:1 for focus indicators. This is a measured failure on at
    least one focusable control.
17. Measured the input's visible boundary. `getComputedStyle('#w2-box1')`
    reported `border: 0px none`, `box-shadow: none`, `outline: none` at
    rest, `background-color: rgb(255,255,255)`. The immediately enclosing
    card background is `rgb(255,253,248)`. Contrast between the two:
    **1.02:1**. The criterion requires visible control boundaries at ≥ 3:1.
    This is a second, independent measured failure (no border, and the fill
    colour is not distinguishable from its surroundings).
18. Confirmed `main` landmark present (`<main>` wraps the whole app) and a
    named `form` landmark (`form` with accessible name "W-2 Box 1 entry") —
    both hold regardless of the contrast failures above.
19. Stopped the server (background process) after filing was complete.

## Criterion score sheet

| Criterion reference | Pass or Fail | Transcript reference and rationale |
| --- | --- | --- |
| Criterion 1.1 | Pass | Step 3. Exactly one enumerated missing-fact item shown ("W-2 from Demo Workshop — Box 1 wages", Form W-2 Box 1), matching `/api/state.missing` (step 2). Finite and specific. |
| Criterion 1.2 | Pass | Step 4. Clicking the missing item's own action moved keyboard focus directly into `#w2-box1` (confirmed via `document.activeElement`, not just a visual scroll). The evaluator never had to locate the input independently. |
| Criterion 1.3 | Pass | Step 3. The page states "Your other synthetic facts are already in place. Enter the outstanding W-2 wages to compute the return." combined with a single-item missing list — a person can state without guessing that one document (the W-2) is all that's needed. |
| Criterion 2.1 | Pass | Step 3/5. The field is labelled "Form W-2 · Box 1 / Wages, tips, other compensation" — names the source document and exact box. |
| Criterion 2.2 | Pass | Step 3/5. Field-attached text: "This amount feeds Form 1040 line 1a and resolves the missing wages needed to compute income." Names both the destination (1040 line 1a) and the completion purpose — exceeds the stated "bare required label" floor. |
| Criterion 2.3 | Pass | Step 3/5. "Enter dollars and cents, for example 90000 or 90000.50." states the expected format before typing. |
| Criterion 3.1 | Pass | Step 5. On acceptance the page showed "Accepted. The entry landed through a contribution." and the status region changed to a checkmark state; `/api/state.accepted` was `true` at the same instant. |
| Criterion 3.2 | Pass | Step 5 vs. step 2. All five expected-impact lines (1a, 9, 11, 15, 16) changed from blocked/null to `change:"changed"` with explicit values, both on the DOM and independently via `/api/state`, and the DOM values matched the API values exactly (90000/93234/93234/78234/12222). |
| Criterion 3.3 | Pass | Step 5 vs. step 2. All four comparison lines (2b, 3a, 3b, 12) shown `change:"unchanged"` with values identical to their pre-entry baseline (1234/600/2000/15000), confirmed identically on the DOM and via `/api/state`. |
| Criterion 4.1 | Pass | Step 6. "Correct this fact" is present on the same page after completion and moves keyboard focus directly to `#w2-box1` (confirmed via `document.activeElement`) — no restart of the session. |
| Criterion 4.2 | Pass | Step 8. After correcting to 91000, all five expected-impact lines updated to the exact post-correction values (91000/94234/94234/79234/12442) on both DOM and `/api/state`, while all four comparison lines remained at their unchanged values on both channels. |
| Criterion 4.3 | Pass | Steps 3 vs. 5. Before entry: a "Still needed" / "1 missing fact" region with a "Bring this document to the entry" list. After entry: a distinctly different "Answered fact" block showing the value with a "Correct this fact" action, under a "Review W-2 wages" heading. The two states use different headings, different regions, and different action verbs — not just a colour change. |
| Criterion 5.1 | Pass | Step 5. `/api/state` reported `missing:[]`, `complete:true`, `computed:true` at `revision:50`; the DOM simultaneously showed "0 missing facts · fully computed" and "Your entry is complete." — a singular, unambiguous state, confirmed at the system level, not just displayed. |
| Criterion 5.2 | Pass | Step 5. The Step 1 "missing facts" list and its heading were entirely removed from the DOM after completion (not merely emptied) — no further required-entry prompting. A distinct "Step 5 · Know it is complete / Done — no further required entry" region appeared, visually and structurally separate (dark-green styling) from the guided-entry sections. The answered W-2 fact remained reachable via "Correct this fact" per 4.1. |
| Criterion 5.3 | Pass | Step 5. "Done — no further required entry" plus "Zero facts are missing and every evaluation line is computed." leaves no ambiguity that the task is finished and no other forms remain. |
| Carries over: Sub-section blast containment | Pass | Step 9 and step 7. The invalid `not-a-number` submission left all nine evaluation lines unchanged on both DOM and `/api/state` (`revision` static at 52) — no sibling value was hidden or invalidated. Step 7 additionally showed that an unsubmitted keystroke never reached the displayed derived lines. |
| Carries over: Accessibility baseline | Fail | Steps 13–18. Landmarks (`main`, named `form`), Tab/Shift+Tab reachability (step 10), Enter/Space operability (steps 11–12), and all measured text-contrast ratios (step 14, minimum 5.98:1) meet the bar. But two independent, directly measured sub-requirements do not: (a) the focus indicator on "Review W-2 Box 1" measures 1.25:1 against its adjacent background (step 16), against a required ≥3:1; (b) the `#w2-box1` input has no border/box-shadow and its fill colour measures 1.02:1 against its surrounding card (step 17), against a required ≥3:1 visible control boundary. The criterion bundles all of these into one bar; two measured misses fail the row. What would make it Pass: raise the focus-ring colour's contrast against dark-green surroundings to ≥3:1 (e.g., a lighter/desaturated ring, or a contrasting inner ring), and give `#w2-box1` a visible border or fill contrast ≥3:1 against its card background. |
| Carries over: No derived value from invalid or blocked input | Pass | Step 2/3. While blocked, all five expected-impact lines showed `value:null` (both DOM "Waiting for W-2" and `/api/state`), never a placeholder or fabricated figure. Step 9 confirmed the rejected invalid entry never reached any derived line either. |
| Carries over: Fail-loud | Pass | Step 9. The 422-rejected entry produced a visible on-page `alert` region with specific guidance; it was not a console-only signal (the console entry was incidental network logging, not the sole indication). |
| Carries over: Blanket redaction | Pass | Step 9. The rejected literal value `not-a-number` was not echoed anywhere in the error text or elsewhere on the page; the message is generic guidance only. |

## What would have made each Fail a Pass

- **Carries over: Accessibility baseline** — see the row above: raise focus-ring contrast against dark backgrounds to ≥3:1, and give the Box 1 input a visible boundary (border or fill contrast) at ≥3:1 against its card background.

## Not measured / ambiguous

- I did not exhaustively screenshot-and-scan the focus ring for every one of
  the five focusable controls — only the submit button (against a light
  background, where it measured fine visually via the pixel dump in step 15)
  and the "Review W-2 Box 1" button (against the dark-green background,
  where it measured 1.25:1, step 16). The wordmark link, "Correct this fact"
  text-button, and the input's own focus ring were not pixel-measured
  individually; I relied on the single shared `:focus-visible` CSS rule
  (step 13) applying uniformly, so the ring colour is the same `rgb(155,75,0)`
  in all cases, and its adequacy therefore depends entirely on the local
  background each control sits against. I did not enumerate every
  background colour on the page against that fixed ring colour, so it is
  possible additional controls beyond "Review W-2 Box 1" also fail 3:1 (for
  example, any future correction-flow default state that lands a focus ring
  on the dark-green section) — I report a Fail with the one directly
  measured, reproducible case rather than a wider unverified claim.
- Criterion 2.1's wording asks for the "exact box or line" naming; I judged
  "Form W-2 · Box 1 / Wages, tips, other compensation" sufficient, but I did
  not independently verify against a real IRS W-2 form image that "Box 1"
  is the officially correct box number for wages (the fixture and criteria
  document both assert this, and it is outside what this evaluation's
  synthetic system can check).
- I did not attempt to test screen-reader announcement behavior (e.g., with
  VoiceOver/NVDA) — only DOM structure (landmark roles, accessible names,
  `aria-describedby` wiring) and keyboard/contrast measurements, which are
  the specific measurements the brief calls for. Actual assistive-technology
  announcement fidelity was not measured.
