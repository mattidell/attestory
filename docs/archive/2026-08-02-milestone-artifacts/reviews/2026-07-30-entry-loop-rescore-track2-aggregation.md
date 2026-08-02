# Entry Loop Re-score — Track 2 Aggregation

- Role: Builder, Track 3 (`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-30-entry-loop-rescore-track3.md`)
- Inputs re-derived directly from the two filed score sheets, row by row, not
  from the charter's or phase-state's summary of them:
  - `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-30-entry-loop-rescore-track2-evaluator-e.md`
    (Evaluator E, Builder brief; commit `b9c1afe`)
  - `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-30-entry-loop-rescore-track2-evaluator-f.md`
    (Evaluator F, Reviewer brief; commit `8509ae9`)
- Aggregation rule applied verbatim from the Scoring Procedure in
  `docs/phases/legible-entry/entry-usability-criteria.md` (read-only, not
  amended by this record).
- Criterion classification (Mechanical/Judgement) taken from the criteria
  document's own wording, not from this track's judgement: criteria 1.1, 1.2,
  2.1, 2.2, 3.1, 3.2, 3.3, 4.1, 4.2, 5.1, 5.2 are labelled **Mechanical**;
  criteria 1.3, 2.3, 4.3, 5.3 are labelled **Judgement**; all five
  ADR-0046-carried-over rows (sub-section blast containment, accessibility
  baseline, no derived value, fail-loud, blanket redaction) are stated by the
  document to be "an additional Mechanical criterion" (line 68 of the
  criteria document) and are classified **Mechanical** accordingly.

## Did the two files actually agree on all twenty rows?

**Yes.** Re-reading both score sheets independently, row by row, confirms the
charter's claim rather than assuming it: both E and F recorded **Pass** on
all twenty rows, with no third value used by either evaluator anywhere in
either file. There is no split anywhere in the matrix. Nothing here is
Disputed.

## The twenty-row matrix

| # | Criterion | Class | E | F | Aggregated | Cell effect |
| - | --- | --- | --- | --- | --- | --- |
| 1 | 1.1 — enumerated missing list | Mechanical | Pass | Pass | Pass | holds |
| 2 | 1.2 — missing list is the navigational guide | Mechanical | Pass | Pass | Pass | holds |
| 3 | 1.3 — person can state document completeness without guessing | Judgement | Pass | Pass | Pass | holds |
| 4 | 2.1 — field names source document and box | Mechanical | Pass | Pass | Pass | holds |
| 5 | 2.2 — field states destination and purpose | Mechanical | Pass | Pass | Pass | holds |
| 6 | 2.3 — person can state correct format without guessing | Judgement | Pass | Pass | Pass | holds |
| 7 | 3.1 — immediate acceptance indication | Mechanical | Pass | Pass | Pass | holds |
| 8 | 3.2 — expected-impact set shows changed + value | Mechanical | Pass | Pass | Pass | holds |
| 9 | 3.3 — untouched comparison set shows unchanged | Mechanical | Pass | Pass | Pass | holds |
| 10 | 4.1 — answered fact locatable/navigable, no restart | Mechanical | Pass | Pass | Pass | holds |
| 11 | 4.2 — correction updates expected-impact set, comparison set stays put | Mechanical | Pass | Pass | Pass | holds |
| 12 | 4.3 — person can differentiate empty vs. answered fact | Judgement | Pass | Pass | Pass | holds |
| 13 | 5.1 — singular unambiguous complete state | Mechanical | Pass | Pass | Pass | holds |
| 14 | 5.2 — complete state stops missing-prompting, stays distinct, keeps correction reachable | Mechanical | Pass | Pass | Pass | holds |
| 15 | 5.3 — person has no doubt the task is finished | Judgement | Pass | Pass | Pass | holds |
| 16 | Sub-section blast containment | Mechanical | Pass | Pass (with caveat, see below) | Pass | holds |
| 17 | Accessibility baseline | Mechanical | Pass | Pass | Pass | holds — see decomposition below |
| 18 | No derived value from invalid/blocked input | Mechanical | Pass | Pass | Pass | holds |
| 19 | Fail-loud | Mechanical | Pass | Pass | Pass | holds |
| 20 | Blanket redaction | Mechanical | Pass | Pass | Pass | holds |

No row is Disputed. No mechanical criterion is Disputed (rule 4 is moot). No
judgement criterion is Fail/Fail (rule 3's second clause is satisfied
vacuously — there is no Fail anywhere to trigger it). No judgement criterion
is Disputed (rule 5 is moot).

**Cell verdict, per the rule stated in the criteria document:** *"A cell
passes if and only if every mechanical criterion is Pass/Pass, and no
judgement criterion is Fail/Fail."* Every mechanical criterion above is
Pass/Pass. No judgement criterion is Fail/Fail. **The W-2 cell passes.**

### Row 16 caveat, not a split

F scored row 16 (sub-section blast containment) **Pass, with caveat**: the
observable half of the criterion (an invalid entry produces no derived value
and hides nothing) held; the sibling-field half is structurally untestable on
a surface with exactly one input field, and F says so explicitly (inference
point I4) rather than silently asserting the untestable half. E scored the
same row **Pass** without flagging the untestable half. Both evaluators
recorded the identical Pass/Fail value (Pass); the caveat is evidentiary
texture on an agreed value, not a second value, so it is not a split and
nothing here is Disputed. The caveat is preserved verbatim in the "criterion
defects" section below as an input to the later criteria revision, since it
identifies a genuine gap between what the criterion assumes (multiple
sibling fields) and what this one-field surface can prove.

## Accessibility baseline — five sub-requirements, both evaluators' measurements

The criteria document (Relationship to ADR-0046 section) states the
accessibility row bundles: normal-text contrast ≥4.5:1; large-text, control
boundary, and focus-indicator contrast ≥3:1; a `main` landmark and a named
form landmark; Tab/Shift+Tab reachability with standard Enter/Space
operability; and focus visibility through `:focus-visible`. A Pass on the row
asserts all five hold; this is the row Milestone 3 failed on and the reason
this milestone exists, so each sub-requirement is broken out here rather than
left folded into the row-17 Pass above.

The two evaluators decomposed the bundle into five items each, but not with
identical boundaries — E kept "control-boundary contrast" and
"focus-indicator contrast" as two separate items and folded `:focus-visible`
measurement into the focus-indicator item; F kept "control boundary and
focus indicator contrast" as one combined item and gave `:focus-visible`
matching its own separate item. Both decompositions cover the same five
requirements named by the criteria document; the difference is instrument
boundary, not disagreement, and is carried into "accumulated criterion
defects" below since the row's own five sub-parts are not enumerated in the
criteria document itself.

### 1. Normal text contrast ≥ 4.5:1

| | E | F |
| --- | --- | --- |
| Method | Programmatic WCAG relative-luminance walk, own `color` vs. nearest non-transparent ancestor background, both phases | Same method, both phases plus supplementary pre-entry instance |
| Sample count | 125 text-bearing elements | 19 named elements/contexts |
| Minimum ratio observed | **5.927:1** (white "1" missing-count badge on `rgb(138,90,0)`) | **5.93:1** (same "1" count badge) |
| Verdict | Pass | Pass |

Both evaluators independently found the same element as the tightest margin
and report matching ratios to two decimal places, from very different sample
counts (125 vs. 19) and independent measurement runs.

### 2. Non-text contrast ≥ 3:1 for control boundaries and focus indicators

| | E | F |
| --- | --- | --- |
| Control boundaries, minimum ratio | 6.997:1 ("Enter this fact" border) | 7.59:1 ("Enter this fact" border) |
| Dark-green/teal region (the region the first-round failure was in) | 7.712:1 (resting border, "Review W-2 Box 1") | not separately isolated as resting-border; see focus-ring figure below |
| Focus indicators, minimum ratio | 2.062 (box-shadow component alone, "Review W-2 Box 1") but 7.586 on the outline component, and the criterion needs only one component to hold | 14.22:1 (link), 14.43:1 (button), 15.90:1 (input) |
| Scope note | Decorative card/section borders excluded as not "controls" (as low as 1.721:1, not scored) | Not separately addressed |
| Verdict | Pass | Pass |

Both measured the same region the first-round failure occurred in (the
dark-green/teal completion banner and its controls) and both found it clears
3:1, with E showing the specific component-level margin that makes the
"Review W-2 Box 1" button's combined indicator pass (outline component
7.586:1, since the box-shadow component alone is only 2.062:1).

### 3. `main` landmark and a named form landmark

| | E | F |
| --- | --- | --- |
| Method | `document.querySelectorAll("main").length === 1`, `form[aria-label=...]` read in both phases | `document.querySelector('main')` truthy check, accessibility-tree read of `form "W-2 Box 1 entry"` |
| Result | `mainCount: 1` both phases; form `aria-label="W-2 Box 1 entry"` present both phases | `main` present; form has accessible name `"W-2 Box 1 entry"` |
| Verdict | Pass | Pass |

### 4. Tab/Shift+Tab reachability with standard Enter/Space operability

| | E | F |
| --- | --- | --- |
| Instrument | Track 1's mechanised CDP probe (`entry_loop_keyboard_operability_client.mjs`), automated | Manual keyboard walk via `activeElement` reads, hand-driven |
| Reverse traversal | `mismatchIndex=null`, `returnedToSeed=true`, empty `forwardOnly`/`backwardOnly`, both phases | 5 forward stops, exact reverse on Shift+Tab, confirmed by `activeElement` at every step |
| Activation | Every actionable control activated with its standard key (Space/Enter), confirmed by observed effect, not absence-of-error | Every control tested with both Space and Enter where applicable, each confirmed by observed state change |
| Mouse events | 0 dispatched | Not applicable (manual walk); no pointer events used |
| Verdict | Pass | Pass |

This is the sub-requirement the milestone exists to make measurable. It was
confirmed twice, by two different instruments: E's automated CDP probe
(Track 1's new machinery) and F's independent hand walk, denied the harness
by its own brief and driven manually via `activeElement` reads at every step.
Both found the same order and the same operability, with no divergence.

### 5. Focus visible through `:focus-visible`

| | E | F |
| --- | --- | --- |
| Method | Contrast-ratio measurement of the rendered focus ring per control (outline and box-shadow components), Track 4's existing probe | Direct `el.matches(':focus-visible')` boolean check plus computed-style ring read, on three sampled controls |
| Result | All 7 Tab-reachable controls in both phases clear 3:1 on at least one ring component | All three tested controls (link, button, input) return `true` for `:focus-visible` with ring contrast ≥14.22:1 |
| Verdict | Pass | Pass |

F's approach directly tests the `:focus-visible` pseudo-class match (the
literal wording of this sub-requirement); E's approach tests the ring's
rendered contrast across every reachable control rather than the pseudo-class
boolean directly. Neither evaluator found a control where a focus indicator
was rendered but failed the contrast bar, or a control where `:focus-visible`
did not fire on keyboard focus.

**Row-17 aggregate: Pass on all five sub-requirements, from both
evaluators, independently.**

## Environmental hazard — first-class limitation, not softened

Both evaluators independently and unpromptedly disclosed, in their own
transcripts, that the evaluation ran under a disclosed environmental fault
during Track 2. The owner decided 2026-07-30 to aggregate this evidence with
the hazard recorded rather than re-run the evaluation.

**What happened, in both evaluators' own words:**

- **The MCP Playwright browser was contended.** E: mid-run, a
  `browser_snapshot`/`browser_type` call landed on a different URL, port, and
  token, already in a complete state E never drove it to — a foreign
  concurrent process (almost certainly F's own run) was winning races for
  the shared browser's active tab. F: its active tab was silently replaced
  twice by a different running instance's page (different port, different
  URL token, reset state), discovered only when a keyboard walk produced an
  impossible result (focus leaving the document after 3 stops instead of 5).
- **The working checkout was shared, not isolated as the dispatch
  intended.** E: `git status` in the shared directory reported the branch as
  `track/entry-loop-rescore-track2-evaluator-f` — a branch E never created.
  F: the checkout it was instructed to work in had already been switched
  underneath it to E's branch by the time it went to file.

**Both evaluators improvised mitigations mid-run**, unprompted:

- E moved every load-bearing check off the shared MCP browser onto a
  privately launched Chrome over CDP (`launchChrome`), a separate process
  per invocation never observed to cross over, and used the shared browser's
  DOM-level evidence only as non-load-bearing corroboration captured before
  the contention was discovered.
- F pinned a dedicated tab, re-verified `location.href` before treating any
  measurement as valid, killed only the OS processes it had itself started
  (verified by matching listening port to its own runner's printed URL), and
  created its own `git worktree` to file its report rather than writing into
  the shared, contended checkout.

**What the foreman established from Git, independent of either evaluator's
account:** commit timestamps confirm score independence held regardless of
the contention. F committed its report at `8509ae9` (2026-07-30 17:06:11
-0700) and E committed its report at `b9c1afe` (2026-07-30 17:07:00 -0700) —
fifty-one seconds apart. The shared checkout never contained either
evaluator's report file at any point either evaluator could have read it,
because each was written and committed only inside its author's own isolated
worktree (E's own account of moving authorship into its real worktree once
it discovered the mismatch; F's own account of creating a dedicated worktree
to file safely). Neither evaluator could have read the other's scores,
because the other's scores did not exist anywhere reachable from the shared,
contended checkout at any time before both were independently filed.

**What the hazard threatened was measurement integrity, not independence.**
Say exactly that, not that the run was "fine" or "ruined": the browser and
checkout contention created a real risk that a load-bearing measurement
would be taken against the wrong server instance, the wrong URL, or a stale
DOM state — and both evaluators demonstrably caught and mitigated that risk
mid-run rather than being protected from it by the harness. It did not
threaten, and Git confirms it did not in fact compromise, the independence of
the two evaluators' scoring — neither could see the other's answers before
filing its own, regardless of what either could see in the shared browser or
checkout.

**F's one unresolved observation, recorded without resolution.** At T8a, on
one page reload, the editable `input#w2-box1` element's `.value` read
`"90000"` (the original first-entry figure) while the "Answered fact" bold
text correctly read `"$91,000.00"`. This did not reproduce on a later reload
of the same URL (T11 showed the input correctly pre-filled with `91000`). F
declined to score this as a surface defect because it could not be
separated from the browser/tab contention documented in T7, immediately
before it. This record does not adjudicate it: it is not resolved as benign,
not resolved as a defect, and not folded into any row's score by this
aggregation. It stands as a loose end for the owner's attention.

**The harness defect itself — evaluator isolation that did not isolate — is
a known defect, deferred by owner decision to a follow-up milestone.** It is
recorded here as a limitation on how this evidence was gathered, not fixed
in this track.

## Accumulated criterion defects — input to the later criteria revision

Collected here for the revision that will act on them; **not acted on by
this track**, per the charter's boundary and the milestone plan's own
restriction that the criteria document is read-only through this milestone.

From E:

- **"Visible control boundaries" scope is undefined.** The criteria
  document's carried-over accessibility wording does not say whether a
  card/section border counts as a "control boundary" for the 3:1 test. E
  scored only actual operable controls (input, button) and treated
  decorative card/section dividers as out of scope, tracking WCAG 1.4.11's
  own scoping to UI components — several such dividers measure below 3:1
  (as low as 1.721:1) and were not scored against the row.
- **Criteria 1.3 and 4.3 are judgement calls tested against a one-fact
  surface.** Neither has been tested against a surface with multiple
  concurrent missing facts or multiple answered/unanswered fields side by
  side, which is plausibly the harder case these criteria exist for.
- **The accessibility row's five sub-requirements are not separately
  enumerated by the criteria document itself**, only bundled in prose; both
  evaluators had to independently decide how to decompose them for scoring,
  and (as shown above) decomposed them along slightly different boundaries.

From F (nine inference points filed in full; summarized, not resolved,
here):

1. **I1 — "control boundary" is undefined** by the criteria document; F
   inferred it from general WCAG 1.4.11 familiarity, not from the document.
2. **I2 — the states/backgrounds to enumerate for the accessibility row are
   undocumented**; F had to explore the live surface itself to discover
   which backgrounds exist to measure.
3. **I3 — criterion 1.3 rests on trusting unverifiable copy** ("your other
   synthetic facts are already in place"), with no inventory or count a
   person could independently verify against.
4. **I4 — sub-section blast containment assumes sibling fields exist**; this
   surface has exactly one field, so the sibling-survival half of the
   criterion is structurally untestable here (see row-16 caveat above).
5. **I5 — "a full restart of the session" (criterion 4.1) is undefined**; F
   inferred that a page reload against the same server-backed URL does not
   count as a restart, from observed value persistence, not from either
   permitted document.
6. **I6 — whether the T8a stale-input-value observation is a scoreable
   defect is unresolved**, entangled with the environmental contention (see
   above); not resolved by this record either.
7. **I7 — whether "Update," "Correct this fact," and "Review W-2 Box 1" are
   one logical action or three is never stated by the surface**; F inferred
   one action from all three routing to the same underlying fact.
8. **I8 — "immediately" (criteria 3.1, 4.2) has no quantitative
   definition**; F inferred it was satisfied by the absence of any visible
   delay at the response latency observed, but could not rule out an
   unobserved pending state.
9. **I9 — the full valid input space (e.g., that negative amounts are
   rejected) is only discoverable by triggering a validation failure**,
   since criterion 2.3's pre-entry format guidance only gives positive
   examples; a person relying solely on the pre-entry text would not know
   negative values are invalid until trying one.

Both evaluators also independently flagged that the word **"synthetic"**
appearing in the page's own on-screen chrome ("Synthetic evaluation", "your
other synthetic facts") is ambiguous as to whether it is in-scope surface
text or out-of-scope evaluation-harness framing — neither resolved it, and
neither folded it into a score.

## What this record does not do

Per the charter's boundaries: this record does not amend
`entry-usability-criteria.md`, does not re-score any criterion, does not
overrule either evaluator, and does not resolve F's T8a observation or the
"synthetic" chrome ambiguity by reasoning about the surface directly. It
aggregates what was filed.
