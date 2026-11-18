<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "plain-line-texts",
  "status": "Open. Track 0 passed; Decisions 1-10; Track 1 chartered.",
  "scope": [
    "every text a filer can see on a saved page says what the line is and why it is blocked in plain words, without engine terms such as derived finding, closed-empty, authority or subtotal 0",
    "every recorded return keeps its numbers, dispositions, refusal codes and missing names; only the changed sentences differ"
  ],
  "non_goals": [
    "no engine, schema, projection, page or kernel change unless P0 shows content cannot do it, and then only after the foreman decides",
    "no change to which answer a path needs or to any refusal code",
    "rule descriptions and other texts no filer can see stay as they are",
    "repeated shared questions and the stale Schedule D line 9 reason belong to the blocked-sale-pages milestone",
    "the citation button label (id@version) and line 12d's two-section boxes stay parked"
  ],
  "deep_reads": {
    "planning": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions",
      "docs/phases/engine-breadth/milestones/plain-line-texts.md"
    ],
    "implementation": [
      "docs/process/planning-and-development.md",
      "docs/phases/engine-breadth/milestones/plain-line-texts.md"
    ],
    "review": [
      "docs/process/planning-and-development.md",
      "docs/roles/qualitative-review.md",
      "docs/phases/engine-breadth/milestones/plain-line-texts.md"
    ],
    "new_milestone": [
      "docs/phases/engine-breadth/milestones/plain-line-texts.md",
      "docs/phases/engine-breadth/engine-breadth-roadmap.md#Parked work and open questions"
    ]
  }
}
-->

# Every Line Speaks Plainly (2025)

Milestone key: plain-line-texts.
Branch: milestone/plain-line-texts-2025.
Phase: Engine Breadth, bounded return. Opening plan: 2026-11-17.
Starting point: main at `0bde6638` (core v95, registry v93, release v93).
Expected target: core v96, registry v94, release v94.

## What we are trying to accomplish

Since core v78 every line a filer sees has a plain text, and since core
v92 no numeric line lacks one. The parked list still records that
several kept texts say "derived finding" or "closed-empty". A filer who
reads "a current derived finding publishes zero through honest
closed-empty authority" learns nothing about their return. The useful
outcome is that every sentence a filer can see on a saved page says, in
plain words, what the line holds and why it is blocked, with the same
numbers and the same blocks as today.

## What we know

- 313 content files under `packages/content/tax/2025` contain
  "derived finding" or "closed-empty". Most are rule descriptions that no
  page draws. Which of them reach a filer (a line's explain text, a
  blocked reason, a categorical render text, a question) is not measured.
- The saved page hides a blocked line's own text when it shows questions,
  so some jargon is visible only on a computing return or a blocked line
  with no question.

**What we do not know.** Which texts a filer actually sees on the
published core across computing, blocked and refused returns; which
field each comes from; whether each can be replaced by a content
successor alone; and how many citizens a fix touches.

## Actions the team will take

1. **P0: census, trace and design** on published v95 and a scratch
   successor.
2. **Decide.**
3. **Track 0 adversarial closure.**
4. **Track 1 build.**
5. **Fresh review, repair, close.**

## Cases that will shape the design

The recorded returns (all 775 lists) as the census population, plus
synthetic `demo.*` act lists for a wage-only return, a return with
interest and dividends, a Schedule D return with a sale, the
blocked-names-question cases, a refused return, and single, joint and
separate statuses.

## P0 result

Stopped at the charter's page-change boundary. Six synthetic saved pages
from seven live v95 cases exposed 38 flagged content texts from 35 citizens,
plus raw IDs and engine terms assembled by the page's support traces, badges
and blocked banners. Content successors cannot replace those page-owned
labels while preserving names and pins. The citation-button exception does
not cover support-trace labels.

This is partial evidence: the 775-list census, scratch successor, comparative
replay and mutation controls were not run after the stop. Foreman must
disposition the trace/banner scope and coordinate any page work with
blocked-sale-pages before rechartering. See
[P0 evidence](plain-line-texts-evidence/p0.md), `census.json`,
`content-trace.json` and `page-trace.json` in that evidence directory.

## Decisions

Foreman, 2026-11-17, on the P0 stop (`plain-line-texts-evidence/p0.md`).

1. **Scope narrows to content-supplied text.** This milestone replaces
   the sentences content supplies to a filer-visible field: a line's
   disposition explanations, attachment titles, blocked reasons and
   question sentences. Support-trace captions (role, symbol, finding and
   rule IDs, "Show ..." buttons, dependency rows), status badges and the
   fixed "No value published" and "Missing dependency code(s)" banners
   are page-owned and stay out. They are parked as one page wording
   item, to be sequenced after blocked-sale-pages, which owns the same
   page surface.
2. **Visible means drawn without opening a support trace.** The census
   counts the initial page plus every detail surface that draws a
   content property (including the mortgage calculation detail that can
   read a member's notes, description or title), and reports separately
   any content property seen only inside a support trace.
3. **Terms are flags, not replacements.** A flagged sentence is replaced
   only where the term is engine language to a filer. Plain words follow
   the 2025 instructions' own names; a zero explanation keeps saying
   which absence or completed calculation supports it.
4. **P0b** completes the census over all 775 recorded lists, designs the
   wording against the local sources, builds a scratch core v96 successor
   (content successors only, one package) and runs the strict replay
   with mutation controls. Charter `docs/reviews/plain-line-texts/charter-p0b.md`.


## P0b result

Complete census: all 775 recorded lists were attempted on published v95;
691 produced saved pages and 84 errored before a page. Nine synthetic cases
add eight pages and one refusal. The content census flags 57 displayed
properties from 50 citizens, including five detail-only mortgage notes and
no support-trace-only prose. Draft wording and 50 byte-preserving scratch
citizens are recorded in [P0b evidence](plain-line-texts-evidence/p0b.md).

Stopped at scratch validation: `NOMINEE_RETURN_SUCCESSOR_GRAPH_MIXED` fixes
line-2b field v6 in the graph inherited by core v96 and rejects the required
wording successor v7. A bounded new v96 graph entry needs an engine edit;
none was made. No valid scratch package, strict comparative replay or
mutation controls exist. Foreman must disposition the validator change or
explicitly park line 2b before rechartering; the two line-2b texts affect
all 691 successful recorded pages.

## Decisions on P0b

Foreman, 2026-11-17, on `plain-line-texts-evidence/p0b.md`.

5. **The validator admits line 2b field v7 from core v96.** The
   interest-composition successor-graph table in
   `packages/derivation/package_validation.py` gains one additive `"v96"`
   entry identical to `"v68"` except `tax.us.2025.form1040.line-2b` at
   `form-field.v3` v7. Earlier entries, the code and the fall-forward rule
   are unchanged. This is the pattern core v68 used for the same field's
   last wording successor (871a42e0); it is derivation validation, not
   kernel, schema, projection or page. Track 1 makes the edit and adds a
   test that v96 with field v6 and v95 with field v7 are each rejected.
6. **P0c** finishes P0b's scope items 3 and 4: the scratch harness
   injects the v96 table entry at runtime (no edit to packages/), builds
   the scratch core v96 from the 50 prepared citizens, and runs the strict
   775-list replay with mutation controls. Charter
   `docs/reviews/plain-line-texts/charter-p0c.md`.


## P0c result

Completed with the Decision 5 entry injected only in the harness. Scratch
core v96, registry v94 and release v94 validate; v96 with line-2b field v6
and v95 with field v7 reject, while unchanged v95 stays valid. All 50 citizen
byte-undo witnesses pass. The active 57-property wording manifest refines
16 P0b replacements (principally rounding) and keeps 41.

Strict replay reuses the complete v95 baseline: 691 recorded lists have
only declared wording changes, 84 retain identical pre-page errors, and
none is unexpected. Eight synthetic pages and one refusal also match.
The comparison covers 223,157 rows and 60,114 form fields; all 16 mutation
controls reject. Successor replay wall time: 701.372 seconds. All 699
successor pages draw without alerts; all 57 new texts have the original
census coverage and no old flagged text remains on in-scope surfaces.

See [P0c evidence](plain-line-texts-evidence/p0c.md), the active
`p0c-wording.json`, `p0c-validation.json`, `p0c-replay.json` and
`p0c-mutations.json`. The reusable full comparison part remains outside the
repository, named in the private report. Proceed to independent Track 0;
Track 1 still makes the authorized production validator entry and tests.

## Decisions on P0c

Foreman, 2026-11-17, on `plain-line-texts-evidence/p0c.md`.

7. **The P0c wording manifest is the candidate.** `p0c-wording.json`
   (57 properties, 50 citizens, including P0c's 16 refinements) is what
   Track 0 tests and Track 1 publishes. Attachment titles change only
   their drawn part before the first colon; the rest of a title is not
   drawn and is left as written.
8. **Track 0 adversarial closure** runs in a fresh context and reuses
   P0c's part files. It asks, sentence by sentence, whether each new
   text is true in every state it is drawn in and plain to a filer, and
   whether any old sentence proved something the new one drops. Charter
   `docs/reviews/plain-line-texts/charter-track0.md`.

## Track 0 adversarial closure

Completed in a fresh context under `docs/reviews/plain-line-texts/charter-track0.md`.
First verified P0c's part files and 50 scratch citizen SHA-256 digests unchanged
and re-ran the strict classifier without running the engine (`track0-p0c-reuse-check.json`:
691 recorded `expected_sentences`, 84 `same_error`, 8 synthetic `expected_sentences`,
1 `same_refusal`, 0 `unexpected`).

Sentence-by-sentence audit across all 699 drawn pages from the census plus 7
supplementary `demo.t0.*` synthetic act lists (covering MFS lived-with, MFJ
spouse records, closed-empty W-2 with interest-only, sub-50-cent rounding zeros
across all rounded lines, single-source vs dual-source `line-2a` and
`schedule1.line-10`, `sch8812.line-6` with `no-other-dependent = no` and zero
qualifying dependents, corrected answers, `finding-retracted` acts, and
`member-transition` removals) retained 35 P0c replacements and refined 22:

- **10 `computed_zero` explanations drawn on closed-empty returns** (`sch8812.line-6`,
  `form1040.line-25a`, `line-25b`, `line-25c`, `line-2a`, `line-2b`, `line-3a`,
  `line-3b`, `line-7a`, `schedule-d.line-13`): because their producer rules pin
  `rounding.convention` or a scope/absence fact, `_classify_numeric` in
  `presentation_projection.py` selects `computed_zero` on closed-empty families
  as well as when recorded amounts round to zero; P0c's sentences claimed that
  recorded forms, dependent records, adjustments, or box 2a distributions existed
  on returns that had none.
- **Single-source vs dual-source `published_value` states** (`form1040.line-2a`,
  `schedule1.line-10`), **non-required Schedule B** (`form1040.line-2b` when
  taxable interest is $1,500 or less and Schedule B is `guard_inapplicable`),
  **blocked dependencies** (`form1040.line-6b` blocked on required income when
  `ssa1099.benefits` is already closed-empty; `form1040.tax-after-credits` v2
  waiting for the computed `line-19` credit rather than v1's retired line-19
  absence fact), **closed-empty absence on `schedule1.line-21`**, and
  **completeness, whole-dollar rounding, and 2025 Form 1040 instruction naming**
  (`form1040.line-8`, `line-10`, `line-3b`, `line-4b`, `line-7b`,
  `schedule-d.line-13`, `schedule1.line-7`).

Rebuilt scratch `core v96` (`c9fbc4776be9bc54a5164f03c91336e93381a6b0ad768f8517bb6f353a888ef4`),
`registry v94`, and `release v94` (`track0_validate.py`); all 50 byte-undo
proofs and all 3 Decision 5 negative/positive validator controls pass. Re-ran
the full 784-list strict replay and 16 mutation controls against the preserved
v95 baseline (`p0c-replay.json`, `track0-replay.json`, `p0c-mutations.json`,
`track0-mutations.json`): 691 recorded `expected_sentences`, 84 `same_error`,
8 synthetic `expected_sentences`, 1 `same_refusal`, and 0 `unexpected` across
223,157 rows and 60,114 page fields (wall time 726.68s), with all 16 mutation
controls rejected. Drew all 699 replay pages plus all 7 supplementary `demo.t0.*`
pages (706 pages total) in headless Chrome (`p0c-drawn-check.json`,
`track0-drawn-check.json`): all 57 new texts appear where expected with 0 render
alerts, 0 old flagged texts on in-scope surfaces, 0 non-loopback requests, and
plain attachment headings before the first colon.

See [Track 0 evidence](plain-line-texts-evidence/track0.md), the updated active
`p0c-wording.json` (and `track0-wording.json`), `track0-wording-changes.json`,
`track0-state-matrix.json`, `track0-validation.json`, `track0-replay.json`,
`track0-mutations.json`, and `track0-drawn-check.json`. Ready for Track 1.

## Track 0 disposition

Foreman, 2026-11-17, on `plain-line-texts-evidence/track0.md`. All five
items pass on the refined manifest.

9. **Track 0's manifest is final.** `track0-wording.json` (57
   properties, 50 citizens; 35 P0c texts kept, 22 refined) replaces P0c's
   as the candidate (amends Decision 7). The refinements that name both
   the absence and the rounding basis of a zero are accepted: the
   projection draws `computed_zero` on closed-empty families too.
10. **Track 1** publishes the 50 content successors byte-identical to
    Track 0's scratch citizens, core v96, registry v94 and release v94,
    the Decision 5 validator entry with its controls, and tests.
    Charter `docs/reviews/plain-line-texts/charter-track1.md`.

## Track 1 result

Charter `docs/reviews/plain-line-texts/charter-track1.md`.

- **Content.** The 50 successor citizens are published in `packages/content/tax/2025/`,
  byte-identical to Track 0's citizens (all 50 digests match `track0-validation.json`;
  checked again by `tests/test_plain_line_texts_v96_package.py`).
- **Validator (Decision 5).** `package_validation.py` gains the `"v96"` successor-graph
  entry, equal to `"v68"` except `tax.us.2025.form1040.line-2b` at `form-field.v3` v7.
- **Packages.** Core v96 (`c9fbc4776be9bc54a5164f03c91336e93381a6b0ad768f8517bb6f353a888ef4`),
  registry v94 and release v94 were generated by `tools.package_successor` from published
  v95 and equal Track 0's candidates byte for byte. The v96 loader entries carry v95's.
- **Replay** (`track1_replay.py`, `track1-replay.json`, `track1-mutations.json`): published
  v95 against published v96 on all 775 recorded lists and 9 synthetic lists: 691
  `expected_sentences` and 84 `same_error` recorded, 8 `expected_sentences` and 1
  `same_refusal` synthetic, 0 `unexpected`; 223,157 rows and 60,114 page fields compared;
  all 16 mutation controls rejected; 9 workers, successor replay wall time 720.4 s
  (774.8 s with startup). The part file is kept outside the repository.
- **Tests.** `test_plain_line_texts_v96.py` (6 live cases on published v95 and v96),
  `test_plain_line_texts_v96_package.py` (7 fast), `test_plain_line_texts_v96_validator.py`
  (4, live: corpus load 15 s), plus the version pins in
  `test_noncovered_sales_v78_switch.py`, `test_capital_gain_distributions_line7a_t1_citizens.py`
  and `test_dsbs_t1_schema_citizens.py`.
- **Checks.** `pytest -m "not live"`, `python3 -m mypy` and the envelope scan are clean;
  the full `pytest` passed (7058 passed, 25 skipped).

### Deviations

1. `track1_replay.py` is `p0c_replay.py` without the validator injection (its assertion that
   `v96` is absent would now fail), run on published cores instead of scratch.
2. The validator test is `@pytest.mark.live` with a measured reason instead of fast.
3. Two existing tests pinned the newest `form-field` versions of line 7b (v3) and line 2b (v6);
   they now pin v4 and v7, the successors this build publishes.

## Review disposition

Foreman, 2026-11-17, on `docs/reviews/plain-line-texts/review.md`
(READY, two notes).

11. **PLT-R2 is repaired here.** The census term list missed "computed
    zero", "closure-backed zero", "conclusion", "absence", "disposition
    is inapplicable" and "floors", so drawn texts on line 6a (693 pages),
    line 6b, line 7b and tax after credits still read as engine output.
    The repair replaces the census's term filter with a reading of every
    distinct drawn content text: each active text on the 699 saved pages
    is listed once and judged plain or not. Texts in citizens this branch
    adds (not yet on main) are edited in place; a citizen already
    published (line 6a v2) gets a successor. Core v96, registry v94 and
    release v94 are rebuilt in place, since they are not yet published.
12. **PLT-R1 (test reads every declared disposition, not only the drawn
    one) is fixed with the repair:** the live test checks the active
    disposition's text, attachment headings and mortgage notes, and
    asserts no flagged term in any drawn content text.
Repair charter `docs/reviews/plain-line-texts/charter-repair.md`.
