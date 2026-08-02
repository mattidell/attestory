# Review — The Entry Loop (synthetic), Track 0: usability criteria for entry

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-28-entry-loop-synthetic-track0-review.md`
- Branch: `milestone/entry-loop-synthetic`, at `c98b4c4`
- Under review: `0ddc0a5` — `docs/phases/legible-entry/entry-usability-criteria.md`
- Builder charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-28-entry-loop-synthetic-track0.md`
- Envelope scan: `python3 tools/envelope_scan.py --range main..HEAD` — clean, exit 0, no output.

## Orientation note

`python3 tools/build_orientation_block.py --ref main` reports a topic mismatch
(`docs/phase-state.md` on `main` still names a prior Real Return topic). That
is expected mid-cycle state: this milestone's phase-state lives on
`milestone/entry-loop-synthetic` and has not merged. I oriented from the review
charter, this branch's `docs/phase-state.md` (`current_role` names this Track 0
review), `docs/roles/reviewer.md`, the unit at `0ddc0a5`, the Builder charter,
the milestone plan, and ADR-0046. I did not read builder working context or any
prior review for this track (there is none).

HEAD `c98b4c4` matches the charter's stated tip. Object `0ddc0a5` is a single
file add: `docs/phases/legible-entry/entry-usability-criteria.md` (60 lines).
No product code in the unit.

## Verdict: NOT READY

The document is a serious first draft of an evaluation instrument — five loop
steps, labelled criteria, an ADR-0046 disposition, and a five-part scoring
procedure that correctly refuses to average disagreement. It is not yet
executable as a scorer by someone who did not write it. Two defects make the
instrument unrunnable; several others weaken it.

---

## Measurement results

### 1. The sharpness test — FAIL on specific criteria

Applied criterion by criterion: two competent evaluators, same surface, same
verdict without negotiating.

| Criterion | Label | Sharp? | Notes |
| --- | --- | --- | --- |
| 1.1 | Mechanical | Yes | Finite enumerated missing list is observable. |
| 1.2 | Mechanical | Borderline | "Primary navigational guide" vs "diagnostic report beside a separate form" will split on multi-panel layouts that are neither pure form-beside-report nor pure list-driven wizard. |
| 1.3 | Judgement | Acceptable as judgement | Possession-of-documents is inherently personal; label matches. |
| 2.1 | Mechanical | Yes | Source document + box/line is checkable text on the field. |
| 2.2 | Mechanical | Borderline | "State why … and its role" has no floor for how much explanation counts. One evaluator accepts "feeds Form 1040 line 1a"; another wants causal tax narrative. |
| 2.3 | Judgement | Acceptable as judgement | Format expectations are judgement. |
| 3.1 | Mechanical | Mostly | "Immediate" and "accepted by the system" can split under multi-stage or async admission, but a visible accept signal is still a real check. |
| 3.2 | Mechanical | Borderline | "Which derived values … changed" does not say *all* changed values, *salient* ones, or a named set. Without a bound, two evaluators score different completeness. |
| **3.3** | **Mechanical** | **No** | Trigger is "if the user might reasonably expect them to." That is a second evaluator's model of a third person's expectations. The document's own Weakest Point section admits it cannot be mechanically enforced. Two evaluators will split, and the split is not a rare edge — it is the criterion. |
| 4.1 | Mechanical | Yes | Locatable without session restart is observable. |
| 4.2 | Mechanical | Borderline | "All dependent derived values" requires the evaluator to know the dependency graph. Without a named expected set for the W-2 path, "all" is aspirational. |
| 4.3 | Judgement | Acceptable as judgement | Empty vs answered is a readability judgement. |
| 5.1 | Mechanical | Mostly | Singular complete state is checkable; "fully computed" needs a visible computed-return signal, which the text implies but does not pin. |
| 5.2 | Mechanical | Borderline | "Guided-entry posture" vs "review or submission posture" is visual rhetoric. "Blocking further prompted entry of required facts" is sharper; the posture language is not. |
| 5.3 | Judgement | Acceptable as judgement | "No doubt" is correctly labelled. |

**Most of the mechanical set is sharp enough.** Criterion **3.3 is not**, and it
is labelled in the fatal class. Borderline cases 1.2, 2.2, 3.2, 4.2, and 5.2
are weaknesses rather than automatic fails of the whole instrument.

### 2. The mechanical/judgement split — FAIL (labelling defect)

The scoring procedure treats the two classes differently: mechanical failure is
fatal (both evaluators must Pass); judgement tolerates Disputed escalation.

**Defect:** Criterion **3.3 is labelled Mechanical** while its applicability
condition ("if the user might reasonably expect them to") is pure judgement,
and the Weakest Point section states it "relies heavily on surface-level
heuristics" and is "difficult to mechanically enforce." That is a
misclassification, not a close call. A mechanical label on a judgement call
makes arbitrary or negotiated Fail/Pass outcomes *cell-fatal*.

Borderline (weaker, not separately blocking): 1.2, 2.2, and 5.2 carry enough
judgement that a strict reading of "mechanical = fatal" over-weights them.
They are less severe than 3.3 because each still has a large observable core.

Judgement labels on 1.3, 2.3, 4.3, and 5.3 fit.

### 3. Implementation independence — PASS with one mild note

No criterion names a layout library, component tree, URL shape, or specific
widget. Lists, field labels, accept signals, and complete-state transitions are
stated as outcomes a surface must achieve, not as a particular interaction
model.

Mild note (not a finding that fails this measurement): Criterion 5.2's
"review or **submission** posture" and "blocking further prompted entry"
narrow the complete-state design more than "done must be definite" requires.
The milestone forbids filing; "submission posture" is slightly premature
product language. It does not by itself force one implementation.

Scope of the unit is documentation only — confirmed against `0ddc0a5`
(`Adocs/phases/legible-entry/entry-usability-criteria.md` only).

### 4. The ADR-0046 disposition — PARTIAL (wrongly silent on load-bearing rules)

Checked each document claim against `docs/adr/0046-presentation-surface-contract.md`
(Requirements 1–6, Foreclosures 1–6, blocked-state salience).

| Document claim | ADR source | Verdict |
| --- | --- | --- |
| Carries over: sub-section blast containment | Req 4: broken part must not hide/invalidate correct siblings, and must not show a value whose evidence is itself broken | **Partial.** Sibling half is correctly adapted to invalid entry fields. Second half (no value whose evidence is broken) is dropped without comment — that half is exactly the entry-time risk when a bad field still feeds a rendered subtotal. |
| Carries over: fail-loud | Req 3 / Foreclosure 3 | **Correct.** Visible on-page signal; never console-only. |
| Carries over: blanket redaction | Foreclosure 6 | **Correct.** No echo of rejected values into visible error text. |
| Does not carry over: zero-authority projection | Req 1 | **Correct.** Entry must emit authority (`act-contribution.v1`); a pure projector cannot be the entry surface. |
| Does not carry over: honest blocking (absence-of-key) | Req 2 | **Correct inversion.** Read-only surfaces block on missing keys; entry must render a field *because* the key is missing. |

**Rules with no disposition (both directions matter):**

1. **Accessibility baseline (Req 6)** — contrast, ARIA landmarks, keyboard
   reachability, `:focus-visible` are load-bearing for *any* human-facing
   surface in the ADR. Silently neither carried nor rejected. An entry loop
   that fails keyboard reachability could still pass every written criterion.
2. **No derived value from invalid or blocked input in the DOM (Foreclosure 2)** —
   highly relevant to entry and to "see it land." If a malformed or not-yet-accepted
   field still paints a computed-looking subtotal, the surface lies. The
   document's blast-containment carry-over covers sibling *fields*, not this
   derived-value side-channel. Wrongly dropped without saying so.
3. **Structural citation identity (Req 5)** — presentation-walk specific; omitting
   it without comment is acceptable for an entry usability instrument.
4. **No fabricated value / no innerHTML (Foreclosures 1, 5)** — build-time /
   projection constraints more than usability-scoring criteria; silence is
   tolerable here (Track 1 still inherits ADR-0046 where it applies as a
   presentation surface).
5. **Section-level blocked-state salience** — presentation-walk structure; entry
   replaces it with missing-facts-as-guide (1.1–1.2). Reasonable not to inherit.

So the three explicit carry-overs and two explicit non-carry-overs that the
document *does* state are directionally right. The defect is **silent drop of
Req 6 and Foreclosure 2**, and the incomplete blast-containment adaptation.
That weakens the bar the instrument will enforce; it does not by itself make
scoring unrunnable.

### 5. Is the scoring procedure runnable, twice? — FAIL (pass rule)

The five required slots are present in form:

| Slot | What the document says | Runnable from text alone? |
| --- | --- | --- |
| Who evaluates | Two agent evaluators; example pairing Builder + Advisor/Reviewer; difference = system prompts / operational constraints | Partially. Count is clear. Pairing is "e.g.", so a second run could pick a different pair and still claim compliance. "Different mental models" is asserted, not operationalized (no distinct briefs, tasks, or constraints). |
| What they are given | Synthetic workspace seeded with all facts except the target family; surface URL; synthetic source document data (e.g. W-2 JSON) | Directionally clear; not re-runnable as a fixed evidence pack (no fixture id, seed procedure, transcript format, or per-criterion score sheet). Expected pre-surface, but the gaps remain. |
| Disagreement | A Pass + B Fail → Disputed with both rationales; not averaged | Clear at criterion level. |
| What a pass is | Mechanical: Pass from **both**. Judgement: no Fail; Disputed acceptable for escalation; Fail fatal | **Inconsistent as written** — see below. |
| Who decides | Owner, with raw transcripts, Pass/Fail/Disputed matrix, rationales for Disputed/Failed | Clear. |

**Pass-rule inconsistency (blocks "runnable twice"):**

Disagreement aggregation says a split becomes **Disputed**. The judgement pass
rule says criteria "must not receive any **Fail** verdicts" *and* "(Disputed is
acceptable for escalation, but a Fail is fatal)."

A Disputed criterion *is* a Pass+Fail pair. Two conductors can read this as:

- **(A)** Aggregate first → status Disputed → judgement cell-pass allows it; or
- **(B)** Raw verdicts → any Fail is fatal → every Disputed judgement fails the cell.

Both readings are available from the same paragraph. That means the same two
evaluator transcripts can produce opposite cell verdicts depending on who runs
the procedure. For mechanical criteria the text is tighter (both must Pass, so
Disputed fails the cell), but that asymmetry is never stated in one place.

Also missing for a second independent run: order of evaluation, whether
evaluators may confer, what artifact they file, and how "Disputed" is written
into the matrix vs raw Pass/Fail. Those are weakenings; the pass-rule fork is
the unrunnable core.

### 6. Coverage of the five steps — PASS

| Step | Criteria | Adequate? |
| --- | --- | --- |
| Know what is missing | 1.1–1.3 | Yes. Enumerated gap, navigation role, document-readiness judgement. Matches the milestone's "missing-facts as guide, not a side report." |
| Enter a fact | 2.1–2.3 | Yes. Source/box, why/role, format-before-typing. Matches the builder charter's "before they type" bar. |
| See it land | 3.1–3.3 | Covered in intent (accepted, what changed, what did not). Quality of 3.3 is a sharpness/label problem (Measurements 1–2), not missing coverage. |
| Correct an entered fact | 4.1–4.3 | Yes for find / update dependents / empty-vs-answered. "Understand the result" leans on 4.2 plus the see-it-land set on re-entry; thin but present. |
| Know the return is complete | 5.1–5.3 | Present, which the milestone asked for on the least-obvious step: singular done state, posture shift, person-level certainty. |

No step is empty. Step 5 is not under-served relative to the other four; its
risk is dependency on seedability (Measurement 8), not missing criteria.

### 7. Scope — PASS

- **Accomplishments, not schema:** Fields must name source/box, state role, and
  support format understanding. No JSON shape, component API, or
  per-field explanation schema is specified. Matches the milestone's "emerge
  from the build and write down at close."
- **Documentation only:** `0ddc0a5` adds one markdown file. No product code, no
  prototype, no matrix movement.
- W-2 is used for examples; criteria are not W-2-only rules. Fine.

### 8. Stated dependencies — FAIL (honesty)

The evaluation setup rests on premises this milestone has **not** confirmed
against the code. The milestone plan names them as open questions before
Track 1. The criteria document states them as facts of the procedure:

1. **A synthetic workspace can be seeded with every fact family except the
   target (W-2)** so that "zero facts missing" and "return fully computed" are
   reachable by entering only W-2. Milestone open question 1; load-bearing for
   step 5 and for the scoring setup paragraph.
2. **An entry surface URL can be served** to evaluators. Milestone open
   question 2 (serve path + contribution path).
3. **Derived values and a complete/computed state are observable on that
   surface** after contribution — presupposes Track 1's build and the
   admission path.

The document is **not honest that it rests on these**. It says evaluators "are
given" a seeded workspace and a URL, as if those were settled inputs. It does
not mark them as unconfirmed premises. Naming them would not require confirming
them (Track 1's job); silence does.

### 9. Verification — FAIL (absent)

Builder charter required: CI `verify` sequence or a stated subset with each
omission justified; include the data-safety scan; state the commit worked from.

Checked:

- Commit message of `0ddc0a5` — no verification section, no scan, no base commit.
- Body of `entry-usability-criteria.md` — no verification section.
- No companion note or track record on the branch that records a Track 0 verify run.

**The track did not record verification at all.** For a docs-only unit the
justified subset would be short (envelope/data-safety scan; suite N/A with
reason; worked-from SHA). That record is missing.

Reviewer-run envelope scan on `main..HEAD` is clean (exit 0). That is this
review's safety obligation, not a substitute for the builder's stated
verification.

---

## Findings

### Make the instrument unrunnable

**F1. Criterion 3.3 is labelled Mechanical but is not mechanically checkable.**

- **Wrong:** Fatal scoring class applied to a criterion whose trigger is "user
  might reasonably expect," which the document itself calls hard to enforce
  and heuristic.
- **Close by:** Relabel 3.3 as Judgement, *or* rewrite it to a mechanical
  observable (e.g. a named set of W-2-related derived lines that must show
  unchanged-when-untouched), *or* drop it and keep the omission note. Whatever
  remains in the mechanical set must be checkable without negotiating what a
  user "might expect."

**F2. The cell-pass rule and the disagreement rule do not determine a unique
cell verdict for judgement criteria.**

- **Wrong:** Split → Disputed, but judgement pass says both "no Fail" and
  "Disputed is acceptable." Conductors can treat Disputed judgement as cell-pass
  or cell-fail from the same text.
- **Close by:** State aggregation order and cell rules in one place, e.g.:
  (1) each evaluator scores Pass/Fail per criterion; (2) split → Disputed;
  (3) cell passes iff every mechanical criterion is Pass/Pass (not Disputed)
  and no judgement criterion is Fail/Fail; Disputed judgement escalates to the
  owner without failing the cell (or the opposite rule, if that is intended —
  but one rule only).

### Make the instrument weaker

**F3. ADR-0046 disposition silently drops Accessibility (Req 6) and
no-derived-from-invalid (Foreclosure 2), and only half-carries blast containment.**

- **Wrong:** Entry will render inputs and derived values; those two rules are
  load-bearing for honest entry UX and are neither inherited nor explicitly
  rejected. Blast containment omits "no value whose evidence is broken."
- **Close by:** For each, carry with an entry adaptation, or explicitly reject
  with a reason. At minimum dispose Req 6 and Foreclosure 2 the way zero-authority
  and honest-blocking were disposed.

**F4. Several Mechanical criteria remain under-specified for agreement (1.2, 2.2, 3.2, 4.2, 5.2).**

- **Wrong:** "Primary navigational guide," "state why," unbounded "which …
  changed," "all dependent derived values," and "review/submission posture"
  invite split verdicts while sitting in the fatal class.
- **Close by:** Add observable floors or examples of pass/fail for each, or
  relabel the residual judgement portion. For 4.2/3.2, a W-2-grounded expected
  derived set would help without designing the surface.

**F5. Evaluation premises are stated as setup facts, not as unconfirmed dependencies.**

- **Wrong:** Seeded synthetic workspace, servable URL, and observable completion
  are milestone open questions / Track 1 work; the procedure treats them as given.
- **Close by:** Name them as dependencies of running the evaluation (not of
  writing the criteria), without confirming them here.

**F6. Who evaluates is only exemplified, not fixed.**

- **Wrong:** "e.g., Builder and Advisor/Reviewer" does not lock the pairing or
  the operational difference that is supposed to matter.
- **Close by:** Fix count, roles (or equivalent distinct briefs), and what
  difference they are required to embody so two runs use the same method.

**F7. No builder verification record.**

- **Wrong:** Charter-required verify subset, data-safety scan, and worked-from
  commit are absent from `0ddc0a5` and from the deliverable.
- **Close by:** Add a short verification note (commit message or doc section):
  what ran, what was omitted and why (docs-only), envelope/data-safety result,
  base SHA.

**F8. Criterion 5.2's "submission posture" over-reaches milestone scope.**

- **Wrong:** This milestone has no filing; "submission" invites a posture the
  build is not chartered to provide.
- **Close by:** Say "review / done posture" (or similar) without submission, or
  define complete-state only by zero-missing + computed + no further prompted
  required entry.

---

## Criteria judged unsharp or mislabelled

| Id | Issue |
| --- | --- |
| **3.3** | Mislabelled Mechanical; unsharp by construction ("might reasonably expect"). **Blocking (F1).** |
| 1.2 | Mechanical label OK only with a clearer pass floor for "primary" navigation. |
| 2.2 | Mechanical label strained; "why / role" needs a minimum observable. |
| 3.2 | Mechanical but unbounded "which changed." |
| 4.2 | Mechanical but "all dependents" needs a known expected set. |
| 5.2 | Mechanical posture language soft; "submission" out of scope (F8). |

Judgement labels on 1.3, 2.3, 4.3, 5.3 are appropriate.

## ADR-0046 check (summary)

Opened full ADR text. Confirmed three carry-overs (blast containment partial,
fail-loud, blanket redaction) and two non-carry-overs (zero-authority, honest
blocking) against Requirements 1–4 and Foreclosure 6. Found silent omission of
Requirement 6 (accessibility) and Foreclosure 2 (no derived value from
invalid/blocked input), plus incomplete adaptation of Requirement 4's second
clause. Detail under Measurement 4 and F3.

## Single thing most likely to go wrong in a real run

Track 2 puts two agents on a built surface; they **split on 3.3** (and likely
on 1.2 or 2.2). The conductor cannot tell from the text whether that split
fails the cell, and 3.3's mechanical label pressures someone to force a fatal
Pass or Fail on a judgement call. The L2 claim then rests on a negotiated or
arbitrary resolution of the instrument's own weakest criterion — exactly the
failure mode writing the criteria *before* the surface was meant to prevent.

Secondary likely failure: step 5 cannot be exercised because the synthetic
seed premise was never confirmed, and the procedure never named that
dependency, so the evaluation is improvised mid-flight.

## What this review does not do

- No rewrite of the criteria.
- No surface evaluation (none exists).
- No product code, no matrix movement, no phase-state pointer change.
- No PR.

Repair is a separate charter if the owner authorises one.
