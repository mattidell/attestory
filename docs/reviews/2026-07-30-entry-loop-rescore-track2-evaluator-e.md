# Entry Loop Re-score — Track 2, Evaluator E (Builder brief)

Scoring commit: `0e66b6097d5944b7946f4eafa93c816da5ffb959` (merge of PR #121).
Branch: `track/entry-loop-rescore-track2-evaluator-e`.

Evaluator: E, Builder brief — exercise every criterion as an explicit system
outcome and preserve the action/result transcript. Where a row is about
behaviour, confirm it at the system level (direct HTTP against the runtime's
own `/api/state` and `/api/contributions`, and CDP-driven private-Chrome
probes), not only by reading what the rendered page displays.

## A note on run isolation, read first

Two things happened during this run that bear on how to read the transcript
below, neither of which changed my own findings but both worth recording
plainly:

1. **The MCP Playwright browser tool is shared, not private to this
   evaluation.** Mid-run, a `browser_navigate` to my own server's URL
   returned my correct incomplete-state page, but the very next
   `browser_snapshot`/`browser_type` call landed on a *different* URL
   (a different port and token) already sitting in a *complete, corrected*
   state I never drove it to. `browser_tabs` showed only one tab, so a
   concurrent process — almost certainly Evaluator F's own run, launched
   independently — was driving the same shared browser session and winning
   races for the active tab. I did not use that tool for anything
   load-bearing after discovering this: every behavioural claim below (entry
   accepted, entry rejected, correction applied, keyboard reachability,
   contrast) is backed by either a direct HTTP call against **my own**
   server port/token, verified independently against the same-request DOM
   read, or a **privately launched** Chrome via CDP (`launchChrome`), which
   is a separate process per invocation and was never observed to cross
   over.
2. **The shared working-copy directory I initially ran commands against
   (a top-level `finances-ui` checkout) is not actually my isolated
   worktree** — my real sandbox is this run's dedicated agent worktree.
   Partway through, `git status` in the shared directory reported the
   current branch as `track/entry-loop-rescore-track2-evaluator-f` — a
   branch I never created — meaning a concurrent evaluator's `git checkout`
   ran against that same shared path while I had commands in flight there.
   All of my actual system-level testing (HTTP calls, CDP probes) targeted
   my own server processes' ports, not that shared directory's file state,
   and the directory's working tree was clean at every point I inspected it,
   so the testing evidence below is unaffected. But I moved this file's
   authorship — the fetch, branch creation, and this write — into my real
   isolated worktree once I discovered the mismatch, to stop compounding the
   contention. I'm recording this so the owner can judge whether other
   Track 2 material needs a second look for the same reason.

## Raw transcript

**Runs used for scoring** (all against the same code, confirmed by the
identical starting-state fingerprint on every restart — the fingerprint is
content-derived, not instance-derived, per the Track 2a dependency report):

- Fingerprint (all runs): `sha256:ac7735a5d9ab4e057e193966aec89df7534e478ee329e47e9f7b8b19018b79e8`
- Run A — `http://127.0.0.1:56045/entry/a02jpJNMHq8YoYBIWUUg-2ttcI_QFpLZomlOEzR0LIA/index.html` — used for the DOM/contrast probe (a purpose-built script paralleling `entry_loop_focus_indicator_client.mjs`'s method, privately-launched Chrome).
- Run B — `http://127.0.0.1:57123/entry/0nysbDuRfGE64o1YNVcVo0JfCfA0Euf4weUMwzZmECc/index.html` — used for the focus-indicator probe (`tests/helpers/entry_loop_focus_indicator_client.mjs`).
- Run C — `http://127.0.0.1:57651/entry/J9z2uefT3BCT4997k1mPbUMngv-_vQuBYQJZu1UdG50/index.html` — used for the keyboard-operability probe (`tests/helpers/entry_loop_keyboard_operability_client.mjs`) and the direct HTTP entry/correction/rejection transcript below.
- W-2 Box 1 figure to enter: `90000`. Corrected figure: `91000`.

Each was launched with `python3 -m packages.derivation.runners.entry_loop_evaluation`, run in the background, and stopped with `kill` on its own PID after use (verified via `lsof -nP -iTCP -sTCP:LISTEN` that only my own PID was bound to the port I was about to stop, before stopping it — never touched other listeners found on the same host belonging to a concurrent process).

### Actions and observed results (Run C, direct HTTP against `/api/state` and `/api/contributions`)

1. `GET /api/state` (initial): `missing=[{"id":"w2-box1", "label":"W-2 from Demo Workshop — Box 1 wages", "document":"Form W-2", "box":"Box 1", ...}]`, `complete=false`, `revision=47`, all five `expected-impact` lines `{"change":"blocked","value":null}`, all four `untouched-comparison` lines `{"change":"baseline", value: 1234/600/2000/15000}`.
2. `POST /api/contributions` with `content.w2_box1 = "not-a-number"`: **HTTP 422**, body `{"error":"Enter W-2 Box 1 as a positive dollar amount with or without comma grouping and an optional $ prefix and with no more than 2 decimal places."}`. Re-fetched `/api/state`: `revision` still `47`, `missing` unchanged, `complete=false` — the rejected submission produced no server-side state advance at all.
3. Same malformed value driven through the **rendered UI** (typed into `#w2-box1`, clicked "Add W-2 Box 1"): surface showed a `role="alert"` block, `"Check this entry."` plus the identical message from step 2; the entered text `"not-a-number"` does **not** appear anywhere in the alert's text; `/api/state` re-checked immediately after: `revision` still `47`. Surface behaviour and system state agree.
4. `POST /api/contributions` with `content.w2_box1 = 90000` (valid): response `complete=true`, `answered=[{"id":"w2-box1","value":90000}]`, `revision=50` (three acts admitted: contribution, member-transition, assertion — one round-trip). All five expected-impact lines: `change="changed"`, numeric values populated (`1a=90000`, `9=93234`, `11=93234`, `15=78234`, `16=12222`). All four comparison lines: `change="unchanged"`, values identical to step 1 (`1234/600/2000/15000`).
5. `POST /api/contributions` with `content.w2_box1 = 91000` (correction, using the prior response's own `contribution` template — same-field reuse, no restart): response `complete=true`, `answered=[{"id":"w2-box1","value":91000}]`. All five expected-impact lines moved again: `1a=91000`, `9=94234`, `11=94234`, `15=79234`, `16=12442` — every one differs from step 4's value. All four comparison lines: `change="unchanged"`, values byte-identical to steps 1 and 4 (`1234/600/2000/15000`).

This is the system-level backbone for criteria 3.1, 3.2, 3.3, 4.1, 4.2, and the blast-containment/no-derived-value/fail-loud/blanket-redaction carryovers. DOM-level corroboration (Run A's browser snapshot, taken before the shared-browser tab contention described above) showed the same shape: "Accepted. The entry landed through a contribution." / "Accepted. The correction landed through a contribution.", an "Answered fact" block, a "Correct this fact" control, and identical dollar values to what `/api/state` reported.

### Structural transcript (Run A, DOM read at initial navigation, before tab contention)

- One `<main>` landmark. One `<form aria-label="W-2 Box 1 entry">`.
- Missing-facts list item: `"W-2 from Demo Workshop — Box 1 wages"` / `"Form W-2, Box 1"`, paired with an "Enter this fact" control.
- Field label: `"Form W-2 · Box 1"` / `"Wages, tips, other compensation"`.
- Field purpose text (`id="w2-box1-purpose"`): `"This amount feeds Form 1040 line 1a and resolves the missing wages needed to compute income."`
- Format hint (`id="w2-box1-format"`): `"Enter dollars and cents with or without comma grouping and an optional $ prefix, for example 90000 or 90000.50."`
- Complete-state heading: `"Your entry is complete."`, sub-text `"Every required fact in this evaluation is present and the return is fully computed. You can still review or correct W-2 Box 1 below."`; Step 5 block: `"Done — no further required entry"` / `"Zero facts are missing and every evaluation line is computed."`

### Contrast probe (Run A) — method

A privately launched Chrome (`launchChrome`, same helper Track 1/4 use — not the shared MCP browser), driven via CDP `Runtime.evaluate`, walked every visible element with own text or a rendered border in both the incomplete and complete phase, computed the WCAG relative-luminance contrast ratio between (a) each text node's `color` and its own element's nearest non-transparent background, and (b) each bordered element's `border-top-color` and its parent chain's nearest non-transparent background. This is the same algorithm Track 4's focus-indicator probe already uses for its half of the check, extended to resting-state text and borders. Full JSON retained in my working notes; summarized below.

### Keyboard probe (Run C) — what it reported, read directly from its output, both phases

```
mouseEventsDispatched: 0
reverseTraversal:
  incomplete: matches=true, returnedToSeed=true, forwardOnly=[], backwardOnly=[], mismatchIndex=null
  complete:   matches=true, returnedToSeed=true, forwardOnly=[], backwardOnly=[], mismatchIndex=null
activation (phase, control, actionable, activatedWith):
  incomplete "Enter this fact"        actionable=true  activatedWith=Space
  incomplete #w2-box1 (input)         actionable=false activatedWith=null   (bare input, correctly exempt)
  incomplete "Add W-2 Box 1"          actionable=true  activatedWith=Space
  complete   #w2-box1 (input)         actionable=false activatedWith=null
  complete   "Update W-2 Box 1"       actionable=true  activatedWith=Space
  complete   "Correct this fact"      actionable=true  activatedWith=Space
  complete   "Review W-2 Box 1"       actionable=true  activatedWith=Space
navigation:
  incomplete wordmark link "attestory" navigated=true (Page.loadEventFired observed)
```

Reading it: the forward Tab order and the Shift+Tab order from the last-reached control agree **positionally**, not just as sets, in both phases (`mismatchIndex=null` in both — the probe would report a numeric index at the first point the two orders diverge, and found none). Every control the probe's own DOM-shape classifier called actionable (link, button, submit-role) activated with its standard key and produced an observed page-fingerprint change; the one non-actionable item is the bare text input, which the classifier correctly exempts (a text input has no "standard activation key" — Enter on a single-field form submits the *form*, which is a different, already-separately-tested control). Zero `Input.dispatchMouseEvent` calls across the whole run. The control set is not identical between phases (three controls exist only once the fact is answered — "Update", "Correct", "Review" — and "Enter this fact" and "Add W-2 Box 1" exist only before), and the probe re-ran both checks against the actual control set present in the phase, not a fixed list.

My read: this is what "Tab/Shift+Tab reachability with standard-key operability" asks for, measured rather than eyeballed, in both control-set configurations the surface has. I score it a Pass on the strength of this instrument, not in spite of it.

## Twenty-row score sheet

| Criterion | Pass/Fail | Transcript ref | Rationale |
| --- | --- | --- | --- |
| 1.1 | Pass | Structural transcript, Run A | Missing-facts section lists exactly one finite, enumerated item — `"W-2 from Demo Workshop — Box 1 wages"` — naming the source document (`Form W-2`) and box (`Box 1`). `/api/state`'s `missing` array (action 1) is the same single item; nothing else is silently missing. |
| 1.2 | Pass | Keyboard probe, "Enter this fact" activation | The missing item's own control is the navigational path: activating "Enter this fact" (confirmed by CDP key-dispatch, not just visual inspection) moves keyboard focus directly to `#w2-box1` — the fingerprint's `focusedKey` changes from the button to the input as the *observed effect* of the keypress, not merely a documented affordance. The evaluator never had to find the input independently. |
| 1.3 | Pass | Structural transcript | The single missing item names both the exact document ("Synthetic Form W-2 from Demo Workshop") and the exact box (Box 1); nothing is left to infer about what physical/digital document to gather. Given this surface's one-fact scope, a person can state without guessing that they need one W-2 and which box on it. |
| 2.1 | Pass | Structural transcript | Field label reads `"Form W-2 · Box 1"` with `"Wages, tips, other compensation"` directly beside the input — source document and exact box, verbatim, matching the criterion's own example. |
| 2.2 | Pass | Structural transcript, `w2-box1-purpose` text | `"This amount feeds Form 1040 line 1a and resolves the missing wages needed to compute income."` — names the immediate return destination (1040 line 1a) and the completion purpose (resolves missing wages needed for income), not a bare "required" label. Matches the criterion's own worked example almost verbatim. |
| 2.3 | Pass | Structural transcript, `w2-box1-format` text | `"Enter dollars and cents with or without comma grouping and an optional $ prefix, for example 90000 or 90000.50."` gives concrete worked examples of the exact accepted format before any typing. |
| 3.1 | Pass | Action 4 (HTTP) + DOM corroboration | `/api/contributions` response and immediate `/api/state` re-check show acceptance (`revision` advances, `answered` populated) synchronous with the request; the surface additionally renders "Accepted. The entry landed through a contribution." and an "Answered fact" block. Both system and surface agree. |
| 3.2 | Pass | Action 4 | All five expected-impact lines (`1a,9,11,15,16`) show `change="changed"` with populated numeric values in the same response that reports `complete=true`, read directly off `/api/state`, not inferred from the page. |
| 3.3 | Pass | Action 4 | All four comparison lines (`2b,3a,3b,12`) show `change="unchanged"` with values identical to the pre-entry baseline (`1234/600/2000/15000`), same response. |
| 4.1 | Pass | Keyboard probe, "Correct this fact" activation | Once answered, "Correct this fact" is reachable in the normal Tab order (see reverse-traversal, complete phase) and its CDP-observed activation effect is a focus move to `#w2-box1` with no `Page.loadEventFired` — i.e. no restart, confirmed as an absence-of-navigation, not just an absence of a visible reload spinner. |
| 4.2 | Pass | Action 5 | Correction (91000) response: every expected-impact value changed again (`1a=91000, 9=94234, 11=94234, 15=79234, 16=12442`, each different from the entered-value snapshot), every comparison value stayed byte-identical to both prior snapshots. |
| 4.3 | Pass | Structural transcript | The missing state renders a "Still needed" / missing-facts section with an "Enter this fact" control and no answered value; the answered state renders a distinct "Answered fact" block naming the actual value (`"W-2 Box 1: $91,000.00"`) with a "Correct this fact" control. The two states share no DOM shape — an empty field vs. an answered one is not a subtle distinction here. |
| 5.1 | Pass | Action 4/5 | `complete=true` and `computed=true` (via `all(line.computed)`, confirmed in the Track 2a dependency report's own re-verification) come from a single, unambiguous system field, not an inferred combination. |
| 5.2 | Pass | Structural transcript, Run A complete-state read | Once complete, the missing-facts section is gone entirely (no listitem), the entry form no longer prompts for a first-time required entry (it now reads "Update W-2 Box 1" / review framing), and a Step 5 "Done — no further required entry" block appears — visibly distinct from the guided-entry state's Step 1–3 framing. The answered fact remains reachable via "Correct this fact". |
| 5.3 | Pass | Structural transcript | `"Your entry is complete. Every required fact in this evaluation is present and the return is fully computed."` plus `"Zero facts are missing and every evaluation line is computed."` — unambiguous completion language, no hedging, no reference to other forms to check. |
| Sub-section blast containment | Pass | Action 2/3 | The rejected malformed submission produced zero state change (`revision` unchanged) and the comparison-set values were never touched by the rejected attempt (nothing to blast, since nothing advanced) — confirmed at the HTTP layer, not just by the absence of a visible error elsewhere. |
| Accessibility baseline | Pass | See decomposed findings below | All five sub-requirements measured and passed; see below. A Pass here asserts all five. |
| No derived value from invalid/blocked input | Pass | Action 1, Action 2 | While `w2-box1` is missing, every expected-impact line's `value` is `null` (not a placeholder zero or a partial derivation) with `change="blocked"`. The rejected malformed submission produced no line-value change at all. |
| Fail-loud | Pass | Action 3 | `role="alert"` block rendered on-page (`"Check this entry."` + message) for the malformed submission; this is in addition to, not instead of, the network-level 422 log — the on-page signal is present regardless of whether the evaluator inspects the console. |
| Blanket redaction | Pass | Action 3 | The literal rejected value `"not-a-number"` does not appear anywhere in the alert text (checked by direct string search over the rendered alert's `textContent`); the message is the fixed format-guidance string from the field contract, not an echo. |

## Accessibility baseline — five separate findings

The row bundles five requirements. Each is scored independently below; the row's overall Pass above asserts all five hold.

**Background contexts enumerated across the whole run: 10 distinct rendered background colours**, across both phases:

| # | RGB | Where it occurs |
| - | --- | --- |
| 1 | `242,239,232` | Page body / `<html>` / `<main>` (incomplete, and the base layer under `<main>` in complete) |
| 2 | `237,244,239` | `<main class="complete">` — the pale-green completion wash |
| 3 | `245,255,248` | `.status-card.done` (complete-phase status card) |
| 4 | `255,243,215` | `.missing` section (pale amber "still needed" card) |
| 5 | `255,253,248` | `.impact-panel` / `.entry-panel` cards, and the "Add/Update W-2 Box 1" button's own resting label track |
| 6 | `255,255,255` | `.money-input` wrapper (immediate background behind the `#w2-box1` input and its `$` prefix) |
| 7 | `242,241,236` | `.line-list.comparison` (untouched-comparison list background, subtly distinct from its card) |
| 8 | `138,90,0` | `.status-mark` (the "1" missing-count badge, incomplete phase) |
| 9 | `248,251,249` | The `$` prefix span's own background |
| 10 | `7,94,79` | `.review` section and the `.primary` button's own fill — **the dark-green/teal completion region** the charter names as one of the two contexts the first run's failures were found in |

### 1. Text contrast ≥ 4.5:1 (normal text)

**Pass.** 125 text-bearing elements measured across both phases (each element's own `color` against its own nearest non-transparent background, walking up from the element itself — not skipping to the parent, which would have wrongly measured e.g. the "Review W-2 Box 1" button's white-on-teal text against the *page* background instead of the button's own teal fill). **Minimum ratio observed: 5.927:1** (the "1" missing-count digit, white text `rgb(255,255,255)` on `rgb(138,90,0)`), comfortably above 4.5:1. No large-text exemption was needed anywhere — every measured node cleared 4.5:1 outright. Closest margins above threshold: 5.927:1 and 5.984:1 (`"1"` badge; `"Step 5 · Know it is complete"` label) — both roughly 1.4:1 of headroom, not a photo-finish.

### 2. Non-text contrast ≥ 3:1 for visible control boundaries

**Pass**, scoped to actual interactive controls (input, button) that render a boundary at rest. Measured:

| Control | Phase | Border colour | Background | Context | Ratio |
| --- | --- | --- | --- | --- | --- |
| `#w2-box1` input | incomplete | `23,37,31` | `255,255,255` | `.money-input` wrapper | **15.899** |
| `#w2-box1` input | complete | `23,37,31` | `255,255,255` | `.money-input` wrapper | **15.899** |
| "Enter this fact" | incomplete | `7,94,79` | `255,243,215` | `.missing` card | **6.997** |
| "Add W-2 Box 1" | incomplete | `7,94,79` | `255,253,248` | `.entry-panel` card | **7.586** |
| "Update W-2 Box 1" | complete | `7,94,79` | `255,253,248` | `.entry-panel` card | **7.586** |
| "Review W-2 Box 1" | complete | `255,255,255` | `7,94,79` | `.review` section (dark-green) | **7.712** |

The two contexts the charter names as the first run's failure sites are both here: the input's own boundary against its card (`15.899:1`) and a control against the dark-green completion region (`7.712:1`, on the resting border — see finding 3 below for the same region's focus ring). Both clear 3:1 with wide margin.

**Note on scope, not a finding against the surface:** the same border-contrast sweep also measured *decorative* section/card dividers (`.status-card`, `.entry-panel`, `.impact-panel`, the line-list `<ul>`, the missing-item `<li>`, the `<form>` element) and several of those fall below 3:1 (as low as `1.721:1` for the form's top border). I did not count these against the criterion: WCAG 1.4.11, which this row's wording tracks, applies to the boundaries of *UI components* (things a person operates), not to layout dividers between cards of static content. None of the sub-3:1 borders belong to an operable control. I flag this scoping choice explicitly in the "ambiguous" section below since the criterion's own wording ("visible control boundaries") doesn't spell out whether a card is a "control."

### 3. Focus indicators ≥ 3:1

**Pass.** Track 4's existing focus-indicator probe (privately-launched Chrome, `entry_loop_focus_indicator_client.mjs`), re-run against my own instance: all 7 controls reachable by Tab in either phase have a focus style that differs from resting and clears 3:1 on at least one component (outline or box-shadow):

| Control | Phase | Outline ratio | Box-shadow ratio | Passes |
| --- | --- | --- | --- | --- |
| wordmark link | incomplete | 1.130 | 13.845 | yes (box-shadow) |
| "Enter this fact" | incomplete | 1.084 | 14.425 | yes (box-shadow) |
| `#w2-box1` input | incomplete | 1.017 | 15.899 | yes (box-shadow) |
| "Add W-2 Box 1" | incomplete | 1.000 | 15.640 | yes (box-shadow) |
| "Update W-2 Box 1" | complete | 1.000 | 15.640 | yes (box-shadow) |
| "Correct this fact" | complete | 1.100 | 14.224 | yes (box-shadow) |
| "Review W-2 Box 1" | complete | **7.586** | 2.062 | yes (outline) |

"Review W-2 Box 1" is the control sitting in the dark-green (`7,94,79`) completion region the charter calls out; its outline component alone clears 3:1 at 7.586:1 (the box-shadow component doesn't, at 2.062, but the criterion only needs one component to hold, and the probe's `combinedFocusIndicator` check reflects that).

### 4. `main` landmark and named form landmark

**Pass.** Measured directly via `document.querySelectorAll("main").length === 1` and reading the form's `aria-label`, in both phases: `mainCount: 1` in both, `form[aria-label="W-2 Box 1 entry"]` present in both. No change in landmark shape between incomplete and complete.

### 5. Tab/Shift+Tab reachability with standard-key operability

**Pass.** See the Keyboard probe section of the raw transcript above for the full read. Reverse traversal matches positionally in both phases (`mismatchIndex=null`, `returnedToSeed=true`, empty `forwardOnly`/`backwardOnly`); every actionable control activates with its standard key with an observed fingerprint change; zero mouse events across the whole run.

## What would have made a Fail a Pass

No row scored Fail on this run — see the closing note below on why that itself is worth flagging to the owner.

## Could not measure / ambiguous

- **"Visible control boundaries" scope.** The criterion's carried-over wording from ADR-0046 doesn't define whether a card/section border counts as a "control boundary" for the 3:1 requirement, only that visible boundaries of controls must clear it. I scored the row on the controls that are actually operable (input, button) and treated card/section dividers as decorative, since WCAG 1.4.11 (the rule this wording tracks) is scoped to UI components. Several decorative borders sit below 3:1 (as low as 1.721:1, the entry-panel form's top border) — not scored against the row, but worth the owner's eye if the intent was broader than "operable controls."
- **1.3 and 4.3 are judgement calls scored against a one-fact synthetic surface.** Both criteria ask what a person "can state without guessing" — with only one missing fact and one field in the whole evaluation, the bar is easy to clear structurally; neither criterion has been tested against a surface with multiple concurrent missing facts or multiple answered/unanswered fields side by side, which is the harder case these criteria plausibly exist for. Scored Pass against the surface as it stands, per the charter's instruction to score from the surface that exists, not a hypothetical one.
- **Shared-browser and shared-worktree contamination**, described at the top of this file, is a process/tooling finding, not a criterion finding — recorded for the owner, not folded into any row's score.

## Second FAIL note

None of this run's twenty rows scored Fail. The charter is explicit that a second Fail is a legitimate outcome and that a marginal row should not be shaded toward Pass because the surface has already failed twice. I did not find a marginal row: the accessibility row's five sub-findings all cleared their thresholds with meaningful margin (minimum text-contrast headroom ~1.4:1 above the 4.5:1 bar; minimum control-boundary and focus-indicator margins each above 3:1 by at least ~2×; the keyboard probe's positional match was exact, not approximate), and the twelve remaining rows either matched their own worked examples near-verbatim (2.2, 2.1) or were confirmed by a direct HTTP round-trip independent of the DOM (3.1–3.3, 4.1–4.2, the four carryovers). I am not asserting the milestone's aggregate verdict — that is not mine to predict — only that, row by row, I did not encounter a close call I talked myself into passing.
