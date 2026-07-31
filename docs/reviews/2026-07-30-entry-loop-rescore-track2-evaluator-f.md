# Entry Loop Re-score — Track 2, Evaluator F (Reviewer brief)

- Role: Evaluator F, Reviewer brief (no implementation context)
- Commit scored: `0e66b6097d5944b7946f4eafa93c816da5ffb959` (branch
  `track/entry-loop-rescore-track2-evaluator-f`, from `origin/main-ui`)
- Documents read: `docs/phases/legible-entry/entry-usability-criteria.md`,
  `docs/phases/legible-entry/entry-loop-synthetic-evidence-pack.md`. No other
  file under this milestone was opened.

## Raw transcript

**Evaluator:** F (Reviewer brief)
**Starting-state fingerprint (primary run):**
`sha256:ac7735a5d9ab4e057e193966aec89df7534e478ee329e47e9f7b8b19018b79e8`
**Primary run URL:** `http://127.0.0.1:65277/entry/MFfpZF3ovN3N9ABaAmjtdmkIc7DK4UZuehymZxpe3g4/index.html`
**Figures printed:** first entry `90000`, corrected `91000`.

A second, later instance of my own runner was started solely to capture the
pre-entry ("blocked") visual state and additional focus-ring contexts without
disturbing the primary run's state. Its fingerprint printed identically:
`sha256:ac7735a5d9ab4e057e193966aec89df7534e478ee329e47e9f7b8b19018b79e8`
(URL `http://127.0.0.1:56854/entry/7JmDReYGRsyoNDrlDiV8V90gCmxwjPlLBr1sc2TTqCQ/index.html`).
The fingerprint being identical across two independent process launches
suggests it is either fixed by design in this build or was not actually
randomized per-process; I record what was printed either way, per instructions.

### Actions and observed results, in order

- T1. Navigated to the primary URL. Snapshot showed Step 1 ("Bring this
  document to the entry") with one missing-fact list item ("W-2 from Demo
  Workshop — Box 1 wages", "Form W-2, Box 1") and an "Enter this fact" button.
  Step 2 entry form showed field-attached text: "Form W-2 · Box 1 / Wages,
  tips, other compensation", "This amount feeds Form 1040 line 1a and resolves
  the missing wages needed to compute income.", and a format hint ("Enter
  dollars and cents with or without comma grouping and an optional $ prefix,
  for example 90000 or 90000.50."). Step 3 showed the expected-impact set
  (1040 1a/9/11/15/16) all as "blocked · Waiting for W-2" and the
  untouched-comparison set (1040 2b/3a/3b/12) as "baseline" with dollar
  values already populated ($1,234.00 / $600.00 / $2,000.00 / $15,000.00).
- T2. Clicked "Enter this fact". Verified via `document.activeElement` that
  focus moved directly to `input#w2-box1` — no independent search for the
  field was required.
- T3. Typed `90000` into the field, clicked "Add W-2 Box 1". Page transitioned
  to a "Your entry is complete." heading, a green checkmark status region
  reading "0 missing facts · fully computed" / "Accepted. The entry landed
  through a contribution.", a Step 4 "Review W-2 wages" section with the
  answered fact ("Answered fact — W-2 Box 1: $90,000.00", "Correct this
  fact" button), and Step 3's expected-impact set all now "changed" with
  correct computed values ($90,000 / $93,234 / $93,234 / $78,234 / $12,222);
  the untouched-comparison set all "unchanged" with the same baseline values.
  Step 5 ("Know it is complete") appeared with heading "Done — no further
  required entry".
- T4. Clicked "Correct this fact". Focus moved directly to the input again
  (verified via `activeElement`), pre-filled with the current answer.
- T5. Typed `91000` (the corrected figure), clicked "Update W-2 Box 1".
  Expected-impact set updated immediately to $91,000 / $94,234 / $94,234 /
  $79,234 / $12,442; untouched-comparison set unchanged. "Accepted. The
  correction landed through a contribution."
- T6. Clicked "Correct this fact" again, typed `not-a-number`, clicked
  "Update W-2 Box 1". Result: an `alert` region appeared reading "Check this
  entry." / "Enter W-2 Box 1 as a positive dollar amount with or without comma
  grouping and an optional $ prefix and with no more than 2 decimal places."
  The rejected string "not-a-number" was **not** echoed anywhere in the error
  text. The expected-impact and untouched-comparison sets were unaffected —
  they continued to display the prior valid state ($91,000 line), not any
  value derived from "not-a-number". A console entry also logged a 422 from
  `POST .../api/contributions`, but the failure was independently signalled
  on-page via the `alert` region — not console-only.
- T7 (environmental incident — see note below). While attempting to continue
  the transcript, my active browser tab was silently replaced with a
  different running instance's page (different port `50230`, different URL
  token, and reset to the pre-entry state) not started by me. I did not
  realize this until a keyboard walk produced an impossible result (focus
  leaving the document after only 3 stops). I recovered by opening a new,
  dedicated tab pinned to my own instance's URL and verifying `location.href`
  before every subsequent action. Full detail in "Environmental note" below.
- T8. Re-established primary session (state persisted server-side: the
  "Answered fact" value was still $91,000.00 after the fresh navigation,
  confirming the fix in T5 survived past a full page reload — but see the
  input pre-fill anomaly noted under T8a).
- T8a. On this particular reload, the *editable* `input#w2-box1` element's
  `.value` read `"90000"` (the original first-entry figure) even though the
  "Answered fact" bold text correctly read "$91,000.00". This did not
  reproduce on a later reload of the same URL (T11 showed the input correctly
  pre-filled with `91000`). I cannot fully rule out that this was itself an
  artifact of the tab/session interference in T7 rather than a genuine
  surface bug; I record it as an unresolved observation, not a scored
  criterion failure (see "Could not measure / ambiguous" below).
- T9. Performed a full keyboard walk from `document.body.focus()`. **Forward
  order (Tab):** (1) link "attestory" (home) → (2) `input#w2-box1` → (3)
  button "Update W-2 Box 1" → (4) button "Correct this fact" → (5) button
  "Review W-2 Box 1" → focus leaves the document (`document.activeElement`
  becomes `BODY`). **Backward order (Shift+Tab) from that end point:**
  (5) "Review W-2 Box 1" → (4) "Correct this fact" → (3) "Update W-2 Box 1" →
  (2) input → (1) link "attestory" — exactly the reverse of the forward
  order, confirmed by `activeElement` reads at every step.
- T10. Operability tests, each confirmed via `activeElement`/state change
  after the keypress, not by assumption:
  - Link "attestory": focused programmatically, `Enter` pressed → page
    navigated/reloaded (standard link operability confirmed).
  - Input: typed `91000` and pressed `Enter` (`submit: true`) → form
    submitted, "$91,000" appeared in the body text (standard text-input
    Enter-to-submit confirmed).
  - Button "Correct this fact": focused programmatically, `Space` pressed →
    focus moved to input (activation confirmed). Re-tested with `Enter` →
    same result (activation confirmed both ways).
  - Button "Review W-2 Box 1": focused programmatically, `Enter` pressed →
    focus moved to input.
  - Button "Update W-2 Box 1": value set to `91500` via a synthetic `input`
    event, button focused, `Space` pressed → "$91,500" appeared in body text
    (activation confirmed).
- T11. On this later reload, `input#w2-box1.value` correctly read `91500`
  (matching the last accepted answer) — the T8a mismatch did not recur.
- T12. Captured computed-style contrast measurements (see Accessibility
  section) across all backgrounds reachable in this session: the default page
  background, the "done" status-card background, the form/entry-panel
  background, the impact-panel background, the untouched-comparison list
  background, the dark-teal "review/done" banner background, and (via the
  supplementary instance) the pre-entry missing-fact card background and the
  "blocked" badge background.
- T13. Captured keyboard focus-ring computed styles (`:focus-visible`
  match, `outline-*`, `box-shadow`) for the link, a primary button, and the
  text input, each against their respective underlying background, via the
  supplementary instance in its fresh pre-entry state.
- T14. Verified `document.querySelector('main')` is truthy (a `main`
  landmark exists) and that the `<form>` element carries an accessible name
  ("W-2 Box 1 entry") via the accessibility tree (`form "W-2 Box 1 entry"`
  in the Playwright snapshot) and by reading its computed accessible name
  path in the DOM.
- T15. Attempted (and abandoned) a Tab-count check on a hijacked tab (T7)
  that appeared to show focus leaving the document after only 3 stops
  (skipping "Correct this fact" and "Review W-2 Box 1" entirely). This did
  **not** reproduce once I was confirmed to be on my own isolated instance
  (T9 above shows all 5 stops present, symmetric both directions). I record
  the failed attempt because the charter requires it, and because it is a
  direct illustration of why I re-verified `location.href` on every
  subsequent read.

### Environmental note (not a criterion finding)

The Playwright browser instance used to drive this evaluation was, at least
twice during my session, not exclusively mine: my "current" tab was silently
replaced by a page belonging to a different running instance (different port,
different URL token, reset state), and a tab I explicitly opened later
disappeared and was replaced with another instance's tab at index 0. I infer
a second evaluator (or another concurrent process) was driving a browser
through the same MCP server. Separately, I discovered the `finances-ui`
checkout I was initially instructed to work in was itself a **shared,
non-isolated working directory** — the branch had already been switched
underneath me to `track/entry-loop-rescore-track2-evaluator-e` by the time I
went to file this report, even though I had checked out my own branch there
at the start of the session. I created a dedicated `git worktree` for my own
branch to file this report safely, rather than writing into the shared
checkout. I mitigated the browser-sharing hazard by: (a) always opening a
new, dedicated tab pinned to my own runner's URL rather than trusting
"current tab", (b) reading `location.href` before treating any measurement as
valid, and (c) killing only the OS processes I had myself started (verified
by matching listening port to the URL my own runner printed), not any process
I did not launch. Both hazards are testing-infrastructure issues, not defects
of the surface under evaluation, and neither affects any score below — every
measurement reported was re-verified against my own confirmed URL, and this
report was written and committed only inside my own isolated worktree.

## Criterion score sheet — all twenty rows

| Criterion reference | Pass/Fail | Transcript ref | Rationale |
| --- | --- | --- | --- |
| 1.1 | **Pass** | T1 | A finite, enumerated missing-fact list is present: one explicit item, "W-2 from Demo Workshop — Box 1 wages" / "Form W-2, Box 1". |
| 1.2 | **Pass** | T2, T4 | "Enter this fact" and "Correct this fact" both moved keyboard focus directly to `input#w2-box1` (verified via `activeElement`, not inferred from a screenshot). No independent search for the input was needed. |
| 1.3 | **Pass** | T1 | Exactly one document is named as missing ("W-2 from Demo Workshop — Box 1 wages"), and the surface states "Your other synthetic facts are already in place." A person can say yes/no to "do I have this document" without ambiguity about what is being asked. (See inference point I3 below on trusting that "already in place" claim.) |
| 2.1 | **Pass** | T1 | Field-attached text names the source document and the exact box: "Form W-2 · Box 1 / Wages, tips, other compensation." |
| 2.2 | **Pass** | T1 | "This amount feeds Form 1040 line 1a and resolves the missing wages needed to compute income." Names the immediate return destination (1040 line 1a) *and* the completion purpose (resolves missing wages to compute income) — not a bare "required" label. |
| 2.3 | **Pass** | T1 | "Enter dollars and cents with or without comma grouping and an optional $ prefix, for example 90000 or 90000.50" — a concrete example is given before typing. |
| 3.1 | **Pass** | T3 | "Accepted. The entry landed through a contribution." appears immediately after acceptance, alongside a checkmark status region. |
| 3.2 | **Pass** | T3 | All five expected-impact members (1040 1a/9/11/15/16) explicitly show "changed" plus the correct resulting dollar value immediately after acceptance. |
| 3.3 | **Pass** | T3 | All four untouched-comparison members (1040 2b/3a/3b/12) explicitly show "unchanged" with the same values held constant. |
| 4.1 | **Pass** | T4 | The answered fact is directly reachable from the main loop surface via "Correct this fact" with no session restart; server-side state persisted across a full page reload (T8). |
| 4.2 | **Pass** | T5 | Changing Box 1 from $90,000 to $91,000 immediately updated all five expected-impact values to their correct post-correction figures; the four untouched-comparison values did not move. Re-confirmed with a second correction to $91,500 (T10). |
| 4.3 | **Pass** | T1, T3 | Pre-entry, the missing item shows no value and an "Enter this fact" action under "Still needed". Post-entry, the same fact is shown as "Answered fact — W-2 Box 1: $X" with a "Correct this fact" action, in a different step section entirely. The two states are structurally distinct, not just a toggled icon. (Caveat: T8a's one-time stale input value — see "Could not measure" below — is a soft spot in this otherwise clear distinction; it did not recur and did not change my score.) |
| 5.1 | **Pass** | T3 | "0 missing facts · fully computed" is a single, unambiguous heading, paired with a checkmark and "Accepted" copy. |
| 5.2 | **Pass** | T3 | Step 1 ("Bring this document to the entry" / missing-fact list) is entirely absent once complete — replaced by Step 4's review form. Step 5 ("Know it is complete" / "Done — no further required entry") is visually distinct (dark-teal banner, white text) from the entry-form sections (cream background). The answered fact remains reachable via "Correct this fact". |
| 5.3 | **Pass** | T3 | "Zero facts are missing and every evaluation line is computed. Review the result above, or return to W-2 Box 1 to make a correction." leaves no ambiguity that the task is finished and names the only further action available (correction, not a new form). |
| Sub-section blast containment | **Pass**, with caveat | T6 | The testable half of this criterion held: an invalid entry ("not-a-number") produced no derived value in the DOM — the expected-impact/comparison sets kept showing the prior valid state, not anything computed from the rejected string, and nothing else on the page was hidden or invalidated. The "sibling fields" half of the criterion is structurally untestable here: this surface exposes exactly one input field, so there is no second, correct sibling field whose survival I could verify against a neighboring invalid entry. I scored Pass on the observable behavior and flag the untested half explicitly — see inference point I4. |
| Accessibility baseline | **Pass** | T9, T10, T12, T13, T14 | All five bundled sub-requirements passed independently — see the dedicated section below with full measurements. |
| No derived value from invalid or blocked input | **Pass** | T1, T6 | Pre-entry, the expected-impact set shows "blocked / Waiting for W-2", not a placeholder number. After an invalid entry, the set continued showing the last valid accepted values, never anything derived from the rejected input. |
| Fail-loud | **Pass** | T6 | The malformed-input rejection produced a visible on-page `alert` region with explanatory text. A console 422 also appeared, but the on-page signal is present and primary — not console-only. |
| Blanket redaction | **Pass** | T6 | The error text ("Enter W-2 Box 1 as a positive dollar amount...") never echoed the rejected string "not-a-number". |

**Summary: 20/20 Pass.** I deliberately re-scrutinized the rows most likely to
be marginal (1.3, 4.3, sub-section blast containment) given the charter's
explicit reminder that a second Fail is legitimate and that I should not
shade toward Pass. My honest read of the surface, from its own wording alone,
did not surface a defensible Fail on any of the twenty rows. Where I found
real softness — the untestable sibling-field half of blast containment, the
one-time stale input value, the "already in place" trust requirement — I have
recorded it as a caveat or inference point rather than silently rounding to
Pass. I recognize this diverges from the earlier "accessibility failed the
first run" framing in my charter; I did not use that framing to anchor my own
measurement, per my brief's instruction to score independently.

## Accessibility baseline — five separate findings

The carried-over rule bundles five requirements. Each is scored and measured
separately, as required.

### 1. Text contrast ≥ 4.5:1 (normal text)

Measured programmatically (WCAG relative-luminance formula, computed styles,
walking up the DOM to the first non-transparent background) across every
background context reached in this session:

| Element / text | Foreground | Background | Context | Ratio |
| --- | --- | --- | --- | --- |
| `h1` heading | rgb(23,37,31) | rgb(237,244,239) | default page bg | 14.22 |
| Eyebrow paragraph "2025 FEDERAL RETURN · W-2" | rgb(63,81,73) | rgb(237,244,239) | default page bg | 7.56 |
| Body paragraph (intro) | rgb(53,70,63) | rgb(237,244,239) | default page bg | 8.95 |
| "RETURN STATUS" label | rgb(63,81,73) | rgb(245,255,248) | status/done card | 8.27 |
| "Accepted. The correction landed..." | rgb(7,94,79) | rgb(245,255,248) | status/done card | 7.54 |
| Step labels / field text | rgb(63,81,73) | rgb(255,253,248) | entry-panel card | 8.31 |
| "Done — no further required entry" heading | rgb(255,255,255) | rgb(7,94,79) | dark review/done banner | 7.71 |
| "Zero facts are missing..." paragraph | rgb(238,249,244) | rgb(7,94,79) | dark review/done banner | 7.16 |
| Button text "Update W-2 Box 1" | rgb(255,255,255) | rgb(7,94,79) | primary button fill | 7.71 |
| Button text "Correct this fact" | rgb(7,94,79) | rgb(237,244,239) | answered-fact row | 6.90 |
| Button text "Review W-2 Box 1" | rgb(7,94,79) | rgb(255,253,248) | entry-panel card | 7.59 |
| Expected-impact values (`strong`) | rgb(23,37,31) | rgb(255,253,248) | impact-panel | 15.64 |
| Untouched-comparison values (`strong`) | rgb(23,37,31) | rgb(242,241,236) | comparison list | 14.06 |
| Input text | rgb(23,37,31) | rgb(255,255,255) | text input | 15.90 |
| Status badge "changed" | rgb(7,94,79) | rgb(255,253,248) | impact-panel | 7.59 |
| Status badge "unchanged" | rgb(75,92,84) | rgb(242,241,236) | comparison list | 6.28 |
| Status badge "blocked" (pre-entry) | rgb(75,92,84) | rgb(255,253,248) | impact-panel, pre-entry | 6.98 |
| Status badge "baseline" (pre-entry) | rgb(75,92,84) | rgb(242,241,236) | comparison list, pre-entry | 6.28 |
| "1" missing-count badge | rgb(255,255,255) | rgb(138,90,0) | count badge (own bg) | 5.93 |

Lowest measured ratio: **5.93:1** ("1" count badge). Every measured element
clears 4.5:1. **Finding: Pass.**

### 2. Non-text contrast ≥ 3:1 (control boundaries and focus indicators)

| Element | Border/ring colour | Background | Ratio |
| --- | --- | --- | --- |
| Text input border (2px) | rgb(23,37,31) | rgb(255,255,255) | 15.90 |
| "Enter this fact" button border (1px) | rgb(7,94,79) | rgb(255,253,248) | 7.59 |
| Focus ring, link "attestory" | rgb(23,37,31) (box-shadow) | rgb(237,244,239) | 14.22 |
| Focus ring, "Enter this fact" button | rgb(23,37,31) (box-shadow) | rgb(255,243,215) missing-fact card | 14.43 |
| Focus ring, text input | rgb(23,37,31) (box-shadow) | rgb(255,255,255) | 15.90 |

Every measured control boundary and focus ring clears 3:1 by a wide margin
(minimum observed 7.59:1 for boundaries, 14.22:1 for focus rings).
**Finding: Pass.**

### 3. `main` landmark and a named form landmark

`document.querySelector('main')` returned a truthy element (T14): a `main`
landmark is present and wraps the entire loop. The `<form>` element carries
an accessible name — the Playwright accessibility snapshot reports it as
`form "W-2 Box 1 entry"`, and this was confirmed programmatically as well.
**Finding: Pass.**

### 4. Tab/Shift+Tab reachability with standard Enter/Space operability

**Forward order (Tab), five stops, confirmed by `activeElement` reads:**
1. link "attestory" (home)
2. `input#w2-box1`
3. button "Update W-2 Box 1"
4. button "Correct this fact"
5. button "Review W-2 Box 1"
— focus then leaves the document.

**Backward order (Shift+Tab) from that end point:** 5 → 4 → 3 → 2 → 1,
exactly the reverse. Confirmed by `activeElement` reads at each step (T9).

**Operability, confirmed by observed state change after the keypress (not
assumed):**
- Link: `Enter` → navigation occurred.
- Text input: `Enter` (as form submit) → form submitted, value accepted.
- "Correct this fact" button: both `Space` and `Enter` → focus moved to
  input (activation confirmed both ways).
- "Review W-2 Box 1" button: `Enter` → focus moved to input.
- "Update W-2 Box 1" button: `Space` → form submitted, new value accepted.

I initially recorded an apparent failure here — focus leaving the document
after only 3 Tab stops, skipping two buttons entirely (T7/T15) — which did
not reproduce once I confirmed I was on my own isolated browser tab. I record
this as an attempt that did not work, per the charter's instruction, and note
that it was caused by the shared-browser environmental issue, not the
surface. On the verified, isolated instance, all five stops were reachable
and reversible, and every control type responded to its standard key.
**Finding: Pass.**

### 5. Focus visible through `:focus-visible`

Tested on the link, the "Enter this fact" button, and the text input by
actually tabbing to each with the keyboard and reading `el.matches(':focus-visible')`
plus the live computed `outline`/`box-shadow`:

| Element | `:focus-visible` matches | Ring | Ring vs. background ratio |
| --- | --- | --- | --- |
| link "attestory" | true | outline 2px solid + box-shadow ring 5px, rgb(23,37,31) | 14.22 |
| button "Enter this fact" | true | same ring, rgb(23,37,31) | 14.43 |
| `input#w2-box1` | true | same ring, rgb(23,37,31) | 15.90 |

Every focused control I tested returned `true` for `:focus-visible` and
showed a consistent, high-contrast ring (minimum 14.22:1). **Finding: Pass.**

## List of every point where the surface required inference

1. **I1 — What counts as a "control boundary."** Criterion wording (the
   carried-over accessibility rule) does not define which visual elements
   are "control boundaries." I inferred this to mean the input's and
   buttons' visible borders, based on general familiarity with the WCAG
   1.4.11 non-text contrast requirement — the criteria document itself does
   not name or illustrate an example.
2. **I2 — What states/backgrounds to enumerate for the accessibility row.**
   Neither of my two permitted documents lists the surface's reachable
   states. I had to explore the live page myself (pre-entry, post-entry,
   post-invalid-entry, post-correction) to discover what backgrounds exist
   to measure against, rather than being told.
3. **I3 — Trusting "Your other synthetic facts are already in place."**
   Criterion 1.3 requires a person to state, without guessing, whether they
   have all needed documents. The surface's only support for "this is the
   only thing you need" is that one line of prose; a real user has no
   independent way to verify it (no inventory list, no count of other fact
   families). I passed the criterion on the theory that stating there is
   exactly one missing item, clearly named, is enough — but the "nothing
   else is missing" guarantee itself rests on trusting unverifiable copy,
   which the criterion's wording does not explicitly address either way.
4. **I4 — Sub-section blast containment with a single-field surface.** The
   criterion assumes sibling fields exist that could be wrongly hidden or
   invalidated by an invalid entry elsewhere. This surface has exactly one
   input field, so I could not exercise that half of the criterion at all. I
   inferred that "no siblings exist to violate" is an acceptable basis for
   Pass on the observable half, rather than an automatic Fail or an
   unscoreable row — the criteria document does not say what to do when the
   surface under test doesn't have the shape the criterion assumes.
5. **I5 — What "a full restart of the session" means (4.1).** I treated a
   full browser page reload against the same server-backed URL as *not* a
   session restart, because the answered value persisted across it. Neither
   permitted document defines "session" or "restart" for this surface; I
   inferred it from observed persistence rather than being told.
6. **I6 — Whether the one-time stale input value (T8a) is a scoreable
   defect.** I could not determine, from the surface's own guidance, what
   the "correct" pre-fill behavior on reload should be, and could not
   reliably reproduce the anomaly. I inferred it was more likely a transient
   hydration/timing artifact — possibly entangled with the environmental tab
   interference — than a defect that should flip 4.3, but I record the
   inference rather than treating it as confirmed either way.
7. **I7 — Whether "Update," "Correct this fact," and "Review W-2 Box 1" are
   one action or three.** The surface never states this explicitly. I
   inferred, purely from observing that all three route focus to the same
   single input and operate on the same underlying fact, that they are the
   same logical action surfaced under different labels depending on step
   context.
8. **I8 — What "immediately" means quantitatively (3.1, 4.2).** The local
   synthetic backend responded fast enough that I never observed an
   intermediate/pending state between submitting and seeing "Accepted." I
   inferred "immediately" was satisfied by the absence of any visible delay,
   but I cannot rule out a pending state existing that I simply never caught
   at this response speed.
9. **I9 — Combining 2.3's format example with the fail-loud error text to
   learn the full valid input space.** Criterion 2.3's field-attached text
   only gives positive-looking examples ("90000 or 90000.50"); the fact that
   negative amounts are invalid was only discoverable by reading the
   *error* message text after triggering a validation failure, which
   supplies "a positive dollar amount." A person relying only on the
   pre-entry format guidance (as 2.3 requires) would not know negative
   values are rejected until they tried one.

## What would have made a Fail a Pass

Not applicable — no row was scored Fail in this run. If asked to identify the
single most fragile Pass, it is sub-section blast containment (I4): a surface
with two or more fields, where an invalid entry in one demonstrably left a
correct sibling untouched, would have let me confirm the full criterion
rather than only its single-field-compatible half.

## Could not measure / found ambiguous

- **Sub-section blast containment, sibling-field half:** genuinely untestable
  on a one-field surface; see I4. I do not consider this row fully proven,
  only its testable half.
- **T8a stale input value:** observed once, did not reproduce, cannot be
  conclusively separated from the environmental tab-interference incident
  (T7). I did not let it change any score, but I did not verify it as
  benign either.
- **Pending/loading state between submit and accept:** never observed at
  this response latency; I cannot confirm whether one exists and, if so,
  whether it would independently satisfy or violate any criterion (e.g., a
  hypothetical pending state that briefly showed a stale derived value would
  bear on "no derived value from invalid or blocked input").
- **Large-text 3:1 threshold vs. 4.5:1 normal-text threshold:** I applied the
  stricter 4.5:1 bar to every text element I measured, including headings
  that would qualify as "large text" under the carried-over rule's own
  18pt/14pt-bold threshold and so would only need 3:1. Since every measured
  ratio cleared 4.5:1 regardless, this distinction did not change any
  verdict, but I did not separately verify the large-text threshold in
  isolation.
- **Criterion 1.3's reliance on trusted copy** ("your other synthetic facts
  are already in place") rather than a verifiable inventory — see I3. I
  scored Pass but flag this as the softest Pass on the "Judgement" rows.
- **The word "synthetic" in the page's own chrome** ("Synthetic evaluation",
  "your other synthetic facts") — I treated this as evaluation-harness
  framing rather than product copy a real end user would see, and did not
  score against it. I could not resolve from either permitted document
  whether that framing is considered in-scope surface text or out-of-scope
  scaffolding; I flag it as ambiguous for the owner.
- **Shared browser and shared checkout, both discovered mid-session** — see
  the "Environmental note" in the transcript. Neither hazard changed a
  score, but both cost time and both are worth the owner's attention before
  the next multi-evaluator rescore is scheduled.
