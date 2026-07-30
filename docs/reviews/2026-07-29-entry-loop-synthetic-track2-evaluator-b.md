# The Entry Loop (synthetic) — Evaluator B Score Sheet

Role: Evaluator B (Reviewer brief). Approached the surface without
implementation context: read only `entry-usability-criteria.md` and
`entry-loop-synthetic-evidence-pack.md`, then drove the page with the
Playwright browser tools. Did not open `packages/`, any Svelte source, any
test, any Track 1/2a charter or review, the milestone plan, or Evaluator A's
score sheet.

## Raw transcript

**Evaluator:** B (Reviewer brief)

**Starting-state fingerprint (first run):**
`sha256:7d5abe2ed31df137a323043385b3de7c1c5a5359a0cba7184c43008a6500beb0`

**Second run (fresh restart, used for the initial-state / blast-containment
walkthrough below) produced the identical fingerprint:**
`sha256:7d5abe2ed31df137a323043385b3de7c1c5a5359a0cba7184c43008a6500beb0`

W-2 Box 1 figure to enter: `90000`. Corrected figure: `91000`.

### Actions and observed results, in order

1. Ran `python3 -m packages.derivation.runners.entry_loop_evaluation` in the
   background. Printed URL
   `http://127.0.0.1:51939/entry/uFIWkz_9T98nPDN6fNQOLxCipvPvxkG07aVuMa8EzLY/index.html`,
   figures 90000 / 91000, and the fingerprint above.
2. Navigated to the URL. Page title "W-2 entry · Attestory". One console
   error, a 404 for `favicon.ico` — not a page signal, ignored.
3. Snapshot of the initial state showed, top to bottom: a "Synthetic
   evaluation" banner; a heading "One document closes the gap."; a status
   region reading "1" / "Still needed" / "1 missing fact · W-2 Box 1"; a
   "Step 1 · Know what is missing" section with a list item "W-2 from Demo
   Workshop — Box 1 wages / Form W-2, Box 1" and a button "Enter this fact";
   a "Step 2 · Enter the fact" form ("Enter W-2 wages") with field label
   "Form W-2 · Box 1 / Wages, tips, other compensation", purpose text "This
   amount feeds Form 1040 line 1a and resolves the missing wages needed to
   compute income.", a `$`-prefixed textbox, format hint "Enter dollars and
   cents, for example 90000 or 90000.50.", and a button "Add W-2 Box 1"; a
   "Step 3 · See it land" section with an "Expected impact" list (1040 1a,
   9, 11, 15, 16, all status "blocked" / "Waiting for W-2") and a "Held
   still for comparison" list (1040 2b $1,234.00, 3a $600.00, 3b $2,000.00,
   12 $15,000.00, all status "baseline").
4. Clicked "Enter this fact". Checked `document.activeElement` via
   `browser_evaluate`: focus moved directly to `<input id="w2-box1"
   name="w2-box1" ...>` — no independent search for the field was needed.
5. Typed `90000` into the field, clicked "Add W-2 Box 1".
6. New snapshot: heading changed to "Your entry is complete."; status
   region now shows "✓" / "Return status" / "0 missing facts · fully
   computed" / "Accepted. The entry landed through a contribution."; the
   Step 1 missing-fact list is gone entirely; a new "Step 4 · Correct an
   entered fact" section appeared with the same form (now pre-filled
   `90000`, button relabeled "Update W-2 Box 1") plus "Answered fact / W-2
   Box 1: $90,000.00" and a "Correct this fact" button; the Expected-impact
   list now reads 1a $90,000.00, 9 $93,234.00, 11 $93,234.00, 15
   $78,234.00, 16 $12,222.00, all status "changed"; the Held-still list is
   unchanged: 2b $1,234.00, 3a $600.00, 3b $2,000.00, 12 $15,000.00, all
   status "unchanged"; a new "Step 5 · Know it is complete" section reads
   "Done — no further required entry" / "Zero facts are missing and every
   evaluation line is computed. Review the result above, or return to W-2
   Box 1 to make a correction." with a "Review W-2 Box 1" button.
7. Clicked "Correct this fact". Focus moved directly to the same input,
   pre-filled with the current value `90000` — confirmed via
   `document.activeElement`.
8. Typed `91000`, clicked "Update W-2 Box 1".
9. Snapshot: "Answered fact" now reads "W-2 Box 1: $91,000.00". Expected
   impact updated to 1a $91,000.00, 9 $94,234.00, 11 $94,234.00, 15
   $79,234.00, 16 $12,442.00, all "changed". Held-still list unchanged
   (same four values as before). Status message: "Accepted. The correction
   landed through a contribution."
10. Typed `abc` into the field (now holding the answered value 91000) and
    clicked "Update W-2 Box 1". Console showed a new 422 from
    `.../api/contributions`. Snapshot showed a visible `alert` region:
    "Check this entry. / Enter W-2 Box 1 as a positive dollar amount with
    no more than two decimal places." Critically: the Expected-impact and
    Held-still lists were **unchanged** from step 9 — still showing the
    prior accepted value ($91,000 line), not anything derived from `abc`.
    The alert text did not echo `abc`.
11. Killed the first run, restarted the launcher for a clean session
    (`Stop: Ctrl-C`, then the same command again). New URL, same figures,
    **same fingerprint** as step 1 above — confirms the fixture is
    deterministic.
12. Navigated to the fresh URL. Snapshot matched step 3 exactly (fresh
    missing-fact state).
13. On the never-yet-answered field, typed `-500` and clicked "Add W-2 Box
    1". Result: visible alert "Check this entry. / Enter W-2 Box 1 as a
    positive dollar amount with no more than two decimal places." The
    Expected-impact list remained "blocked" / "Waiting for W-2" for all
    five members — no derived value reached the DOM from the invalid
    entry. The alert did not echo `-500`.
14. Typed `90000`, clicked "Add W-2 Box 1" — reached the same accepted
    state as step 6.
15. To test whether the format hint's examples are literal, typed
    `90,000` (comma-grouped, a natural US convention) into the answered
    field and clicked "Update W-2 Box 1". Result: **rejected** — same
    "Check this entry." alert, same message. This confirms the two
    examples in the hint text ("90000 or 90000.50") are exhaustive of the
    accepted separators; a person who assumed comma-grouping was
    acceptable (a reasonable assumption given the `$`-prefixed field and US
    tax-document convention) would be wrong, and would only discover this
    by trial.
16. Restored `90000`, clicked "Update W-2 Box 1" to leave the surface in a
    valid, accepted state.
17. Accessibility checks (see below) were run against the state reached
    after step 9/14 (answered/complete state), by direct keyboard
    navigation and `browser_evaluate` computed-style inspection — not by
    reading source.

### Accessibility measurements

All computed via `getComputedStyle` in the live page (`browser_evaluate`)
and the WCAG relative-luminance/contrast formula, applied by hand in the
evaluate call — not read from any design token file or source.

**Landmarks:** `document.querySelectorAll('main')` → 1. Single named form
landmark: `document.querySelectorAll('form')` → 1, with
`aria-label="W-2 Box 1 entry"`.

**Keyboard traversal:** Starting from `document.activeElement.blur()` (no
focus), pressed Tab repeatedly and read `document.activeElement` after
each press. Order observed: link "attestory" (home) → input `#w2-box1` →
button "Update/Add W-2 Box 1" → button "Correct this fact" → button
"Review W-2 Box 1" → focus returns to `<body>` (end of page, no trap).
Shift+Tab from the end walked the same sequence in reverse
(`Review W-2 Box 1` → `Correct this fact`), confirmed directly. Every
interactive control the page exposes is reachable both directions.

**Standard-key operability:** With focus on "Correct this fact", pressed
`Enter` — button activated, focus moved into the input (same behavior as a
mouse click). Did not separately test `Space` on a button; the criterion
requires "Enter or Space" (either), so Enter alone is sufficient evidence.

**`:focus-visible`:** Found in the page's stylesheet via
`document.styleSheets`:
`button:focus-visible, input:focus-visible, a:focus-visible, [tabindex="-1"]:focus-visible { outline: rgb(155, 75, 0) solid 3px; outline-offset: 3px; }`.
Focused the home link by Tab and confirmed `outlineStyle: "solid"`,
`outlineWidth: "3px"`, `outlineColor: "rgb(155, 75, 0)"` on the live
element.

**Contrast ratios (WCAG relative luminance formula, computed in-page):**
- Focus outline (`rgb(155,75,0)`) against its surrounding panel background
  (`rgb(237,244,239)`): **5.53:1** (bar: 3:1 for focus indicators — pass).
- Money-input control boundary (`rgb(83,97,89)`, 2px solid) against form
  panel background (`rgb(255,253,248)`): **6.41:1** (bar: 3:1 — pass).
- Body/paragraph text sampled across the page (field purpose text, format
  hint, step labels, status message, held-still values, expected-impact
  values, error alert text): ratios ranged **6.90 – 15.64:1** against
  their effective (nearest non-transparent ancestor) background (bar:
  4.5:1 for normal text — pass in every sampled case).
- Buttons: "Update/Add W-2 Box 1" (white on `rgb(3,72,60)`) **10.52:1**;
  "Correct this fact" (`rgb(7,94,79)` on `rgb(237,244,239)`) **6.90:1**;
  "Review W-2 Box 1" (`rgb(7,94,79)` on `rgb(255,253,248)`) **7.59:1**.
  All well above 4.5:1.
- I did not exhaustively sample every text node on the page (e.g., the
  small "Synthetic evaluation" banner text, the `$` prefix glyph). What I
  did sample — every distinct text role that carries scoring-relevant
  information (labels, purpose text, format hint, values, status,
  buttons, error) — passed with margin. I am not asserting 100% coverage
  of every pixel of text on the page.

## Inference list — every point the surface required a guess

This is the part of the file the Builder-brief evaluator cannot produce by
construction; each entry states what I could not get from the surface
alone and what I did to resolve it.

1. **The exact accepted numeric format (bears on 2.3).** The format hint
   ("Enter dollars and cents, for example 90000 or 90000.50.") shows two
   positive examples but never explicitly states whether comma-grouping
   (`90,000`), a leading `$` inside the field, or negative signs are
   accepted or rejected. I could only resolve this by submitting `90,000`
   and `-500` and observing rejection. A person with a physical W-2 in
   front of them, following ordinary US currency convention, would
   plausibly type `90,000` first, hit the fail-loud error, and only then
   infer the real rule by trial and error. That is a guess forced by the
   surface, not knowledge given by it.
2. **Whether "Enter this fact" always lands you in the right field when
   more than one fact is missing.** This fixture has exactly one missing
   fact (W-2 Box 1), so criterion 1.2's "direct to its corresponding
   input" behavior was clean and unambiguous to verify. I cannot state
   from the surface alone whether the same one-click-to-field guarantee
   holds when multiple missing facts are listed together — the evidence
   pack and fixture never present that case. I did not extrapolate; I am
   flagging it as untested and out of scope of the criterion's own
   evaluation-set constraints.
3. **Whether "your other synthetic facts are already in place" (page copy)
   corresponds to a complete return outside this single W-2 family.**
   Criterion 5.3 asks whether a person has "no doubt... they do not need
   to look for additional forms." The completion copy says "Every
   required fact **in this evaluation** is present and the return is
   fully computed" (emphasis on the qualifier) alongside the unqualified
   "the return is fully computed." I read this as a real return-completion
   claim, not merely an evaluation-scoped one, because the second clause
   is unqualified and repeated in the Step 5 section ("Zero facts are
   missing and every evaluation line is computed"). But the phrase "in
   this evaluation" is the one place on the surface a careful reader could
   snag on, and I want the owner to know I had to decide it did not
   undermine the completion claim rather than being handed an unambiguous
   single sentence.
4. **Whether the "1.3 — do I have the documents I need" judgement
   generalizes past one document.** The missing-fact description ("W-2
   from Demo Workshop — Box 1 wages") is specific enough (named employer,
   named box) that I could positively match it against a hypothetical
   physical document without guessing, for this one-fact fixture. I have
   no evidence about how the surface would identify documents if two
   employers' W-2s were both missing (e.g., would it disambiguate "W-2
   from Employer A" vs "W-2 from Employer B" clearly, or could two
   generically-labeled items become ambiguous). I scored 1.3 Pass on the
   evidence actually presented, not on an assumption about the
   multi-document case.
5. **Console 422 vs on-page signal race.** Each invalid submission
   produced both a console error (422 from the contributions API) and a
   visible on-page alert. I inferred these were the same underlying
   validation failure surfaced twice (once as a network-level artifact
   invisible to a real user, once as the fail-loud UI signal), rather than
   two independent problems, because the alert text and timing lined up
   with each submission. A person without dev tools open would only ever
   see the on-page alert, which is what the Fail-loud criterion actually
   requires — I note the console errors only because I had them open, not
   because they matter to the criterion.

## Criterion score sheet

| Criterion reference | Pass or Fail | Transcript reference and rationale |
| --- | --- | --- |
| Criterion 1.1 | Pass | Step 3: status region shows "1" / "1 missing fact · W-2 Box 1"; list item names the exact document and box ("W-2 from Demo Workshop — Box 1 wages", "Form W-2, Box 1"). Finite, enumerated, specific. |
| Criterion 1.2 | Pass | Step 4: clicking "Enter this fact" moved DOM focus directly to `#w2-box1` (confirmed via `document.activeElement`), with no independent search of the page required. Step 7: the same holds for "Correct this fact". |
| Criterion 1.3 | Pass | Step 3: the missing-fact description names a specific employer ("Demo Workshop") and a specific box ("Box 1 wages" / "Form W-2, Box 1"), specific enough that a person holding a W-2 could positively match it without guessing. Caveat: only tested against a single-missing-fact fixture; see inference item 4 — I did not extrapolate to a multi-document case the surface never presented. |
| Criterion 2.1 | Pass | Step 3/6: field shows "Form W-2 · Box 1" and "Wages, tips, other compensation" directly above the input — source document and exact box named. |
| Criterion 2.2 | Pass | Step 3/6: purpose text reads "This amount feeds Form 1040 line 1a and resolves the missing wages needed to compute income." — names both the immediate return destination (1040 line 1a) and the completion purpose, meeting the criterion's own stated minimum bar exactly. Not a bare "required" label. |
| Criterion 2.3 | Fail | Step 15 (and inference item 1): the format hint's two examples never explicitly rule out comma-grouping or other conventional formats. I submitted `90,000` — a plausible good-faith format given the `$`-prefixed field and US currency convention — and it was rejected with a generic error, not a format-specific correction. A person cannot state the exact accepted format from the hint text alone without risking (and receiving) a rejection; this is what the criterion's "without guessing" bar is meant to catch. What would make it Pass: the hint stating explicitly what is *not* accepted (e.g., "no commas, no currency symbol") or the field silently normalizing conventional input (stripping commas) rather than rejecting it. |
| Criterion 3.1 | Pass | Step 6: immediately after acceptance, status region shows "✓", "0 missing facts · fully computed", and "Accepted. The entry landed through a contribution." — clear, immediate on-page signal. |
| Criterion 3.2 | Pass | Step 6: Expected-impact list shows 1a, 9, 11, 15, 16 all with status "changed" and their resulting dollar values, immediately after acceptance. |
| Criterion 3.3 | Pass | Step 6: Held-still list shows 2b, 3a, 3b, 12 all with status "unchanged" and unchanged dollar values, immediately after acceptance. |
| Criterion 4.1 | Pass | Step 6/7: "Correct this fact" button and "Answered fact" display are present directly in the main loop surface (Step 4 section), no restart or navigation away required; confirmed reachable and operable by keyboard alone (Tab order and Enter-key test). |
| Criterion 4.2 | Pass | Step 9: correcting 90000→91000 immediately updated 1a, 9, 11, 15, 16 to new "changed" values, while 2b, 3a, 3b, 12 remained exactly unchanged. |
| Criterion 4.3 | Pass | Steps 3 vs 6: multiple redundant, non-subtle signals distinguish empty-missing from answered-needing-correction — page heading text ("One document closes the gap." vs "Your entry is complete."), the status counter ("1 missing fact" vs "0 missing facts · fully computed" with a ✓), the action button's label ("Enter this fact" vs "Correct this fact"), and the presence of an "Answered fact" block with the current value only in the answered state. No single ambiguous cue to read; the differentiation does not require guessing. |
| Criterion 5.1 | Pass | Step 6: "0 missing facts · fully computed" plus a ✓ badge is a singular, unambiguous state. |
| Criterion 5.2 | Pass | Step 6: the Step 1 missing-fact list and "Enter this fact" prompt disappear entirely on completion; a visibly distinct review/done section (Step 4 "Review W-2 wages" / Step 5 "Done — no further required entry") replaces it, and the previously answered fact remains reachable via "Correct this fact". |
| Criterion 5.3 | Pass | Step 6: "Your entry is complete." plus "Every required fact in this evaluation is present and the return is fully computed." plus a separate Step 5 block "Done — no further required entry" / "Zero facts are missing and every evaluation line is computed." Multiple redundant, unambiguous statements of completion. Noted in inference item 3: the qualifier "in this evaluation" is the one phrase that could give a careful reader pause, but the unqualified restatements resolve it — I want the owner aware I had to make that call rather than being handed one clean sentence. |
| Carries over: Sub-section blast containment | Pass | Steps 10 and 13: invalid entries (`abc`, `-500`) never altered or hid the Expected-impact/Held-still lists, which continued to show either the last-accepted values or the pre-entry "blocked"/"baseline" state — never a value derived from the invalid input. |
| Carries over: Accessibility baseline | Pass | See Accessibility measurements above: contrast ratios 5.53–15.64:1 against 4.5:1/3:1 bars; one `main` landmark; one named `form` landmark ("W-2 Box 1 entry"); full Tab/Shift+Tab reachability of every control with no trap; Enter-key operability confirmed; explicit `:focus-visible` rule present and visually distinct (3px outline, 5.53:1 contrast). |
| Carries over: No derived value from invalid or blocked input | Pass | Same evidence as blast containment (steps 10, 13): no invalid/blocked entry ever produced a value in the Expected-impact or Held-still lists. |
| Carries over: Fail-loud | Pass | Steps 10, 13, 15: every invalid submission (`abc`, `-500`, `90,000`) produced a visible on-page `alert` region with a specific message; never console-only (a real user without dev tools would still see the alert). |
| Carries over: Blanket redaction | Pass | Steps 10, 13, 15: the alert text ("Enter W-2 Box 1 as a positive dollar amount with no more than two decimal places.") never echoed the rejected values `abc`, `-500`, or `90,000` back to me. |

## Fails — what would make them Pass

- **Criterion 2.3:** See rationale above. Fix: state explicitly in the
  format hint which separators/symbols are and are not accepted (e.g.,
  "digits and an optional decimal point only — no commas, no `$`"), or
  make the field tolerant of conventional formatting (auto-strip commas)
  so the examples given are not a trap for a good-faith guess.

## What I could not measure

- I did not exhaustively test contrast for every text node on the page
  (e.g., decorative "Synthetic evaluation" banner text, the `$` prefix
  glyph) — I sampled every text role that carries scoring-relevant
  meaning and all passed with wide margin, but I am not claiming 100%
  pixel coverage.
- I did not test `Space`-key activation of a button separately from
  `Enter`; the criterion requires either, and Enter was confirmed
  sufficient, so I did not treat this as a gap worth flagging as
  unmeasured, but I note the asymmetry for completeness.
- I could not evaluate how criteria 1.1–1.3 behave when more than one
  fact is missing at once (multi-document disambiguation), because this
  fixture is single-fact by design (per the Scoring Procedure's stated
  dependency that "W-2 is the only missing family"). This is not a gap in
  what I measured — it is a case the fixture never presents — but I want
  it on record rather than silently assumed away.

## Ambiguous criteria

- Criterion 2.3's "without guessing" bar is, in my reading, close to
  unscoreable in the strict sense the criteria document intends for any
  free-text numeric field, because no finite set of examples can rule out
  every plausible alternative format a person might try. I scored it
  against the concrete evidence I gathered (a plausible good-faith format
  was rejected), not against a demand for exhaustive format documentation.
- Criterion 5.3's "no doubt" bar is a genuinely personal, unmeasurable
  quantity — I scored it against the actual page copy's clarity and
  redundancy, and disclosed the one qualifier phrase that gave me pause,
  rather than asserting I know what every person would feel.
