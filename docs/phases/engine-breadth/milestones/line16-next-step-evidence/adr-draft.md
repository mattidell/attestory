# ADR draft — Plain explanations for a recorded answer that holds up a line

- Status: **draft, not filed** (line16-next-step P0 evidence). If accepted, it
  would take the next free number under `docs/adr/`.
- Tier: 2. This is a content-citizen, package-admission and
  presentation-projection contract that later packages are written against.
- Evidence: [p0.md](p0.md), [scratch.diff](scratch.diff),
  [replay.json](replay.json).

## Context

line16-names (Decisions 6–8) made line 16, its four dependants, and the 23
preferential-base fields name exactly the Exception 1 criteria answered no,
when a return requires Schedule D and records no sale. The review parked
L16-R2: when those answers are right, the page gives no next step. It also
does not show the answer the filer gave.

The P0 inventory on core v108 found the following on all 21 target lists:

- each of the 28 blocked fields draws "This line has no result." and one
  "See the question and affected lines above" link per failing criterion;
- the question card draws the question and "An answer is recorded here.";
- no drawn text states an answer.

No accepted contract has a place for either missing piece:

- `presentation-model.v3` closes question groups and scopes
  (`additionalProperties: false`).
- `input-question.v1` carries only `question`.
- The Exception 1 fact types are plain `{yes, no}` enums. A successor fact
  type would unpin every recorded answer.
- `family-block-explanation.v1` (ADR 0088) is keyed and validated to
  source-family member-validation block codes.
- Rule `wording` is ADR 0076's per-subject reader sentence.

A raw value cannot be displayed as the answer either: whether "yes" means the
filer said yes depends on how the question is worded (line6b-reason
Decision 8).

## Decision

1. **New content citizen `answer-explanation.v1`, admitted by
   `artifact-package.v45`.** v45 is v44 plus this schema in the closed member
   and admitted-schema sets and the role `answer-explanation`. Each citizen
   declares:
   - `fact_type` (required `{id, version}` pin);
   - `value` (required string), one value of that fact type's declared
     domain;
   - `explanation` (required non-empty string), a plain sentence that says
     what this answer means for a line it holds up and what the filer does
     next.

   The sentence must be true wherever the answer holds up a line. It is a
   property of the answer, not of one line.

2. **Package validation** (for packages that adopt the role; earlier packages
   are unchanged):
   - `ROLE_MISMATCH`;
   - `ANSWER_EXPLANATION_FACT_TYPE_NOT_ADMITTED`: the pin is not in the
     package's fact surface;
   - `ANSWER_EXPLANATION_QUESTION_ABSENT`: no adopted `input-question` exists
     for that exact pin;
   - `ANSWER_EXPLANATION_VALUE_OUTSIDE_DOMAIN`: the value is not in the fact
     type's declared `enum`;
   - `ANSWER_EXPLANATION_DUPLICATE`: more than one citizen exists for one
     (fact type, value).

   Authorization-closure and reachability edges run from the citizen to its
   fact type's bundle, as for `input-question`.

3. **Projection on `presentation-model.v3`** (no presentation schema change):
   - The projection indexes adopted citizens by (fact type, version, value).
   - It maps each fact with exactly one current answer that has a declared
     sentence to that sentence. It does the same for a fact type when exactly
     one of its facts has one.
   - When `_closure_question_reasons` records a declared input question for a
     missing name (`record_input_fact`, the ADR 0086 names), it adds that
     fact's sentence as an unlinked reason. It uses the exact fact id, or the
     bare type only under the uniqueness rule above.
   - The linked question reason stays. Reasons stay sorted, so existing
     reasons keep their indices.
   - Unanswered answers, stale answers, and values with no declared sentence
     produce nothing new.
   - Roster-member walks (ADR 0087) are not extended.
   - `citation-walk.v1.html` is unchanged: it already draws an unlinked
     reason as a bullet.

4. **Content.** The next core adopts four citizens, each for value `no` of
   one Exception 1 fact type (`only-box2a-capital-gains`,
   `no-capital-losses`, `no-qof-deferral`, `no-boxes-2b-2c-2d`). The
   sentences and the 2025 instruction text behind them are in p0.md §2–3.

5. **What does not change.** No kernel, rule, fact type, input question,
   value, disposition or block code changes. When Schedule D is required,
   and the Exception 1 rules, are unchanged. No answer control or
   question-entry path is added. Earlier cores and `artifact-package.v44` and
   earlier keep their bytes and behavior. With no citizen adopted, the
   projection draws exactly as before (P0: published v108 under the new code
   is byte-identical).

## Consequences

- On a target return, each of the 28 blocked fields shows, after its links,
  one sentence per criterion answered no. That sentence states the answer and
  the next step.
- The scratch full-surface replay of v108 against v109 over 775 recorded and
  26 probe lists gave 801 passing and 0 unexpected. Sentences were added on 25
  lists, and the package version moved on the rest. No number, disposition,
  code or question link changed.
- Other questions can later declare explanations for their answers (for
  example the personal-loss boundary answers, still parked) without another
  contract.

## Owner decisions

1. Accept or reject the contract (Decisions 1–3).
2. **Where the answer shows.** Under **A** (this draft), the sentence goes in
   each blocked line's "Why:" list, on v3, with no page change; it repeats on
   every affected line. Under **B**, a `presentation-model.v4` group-level
   field carries the answer and the sentence, and the page draws them once in
   the question card. B needs a schema successor for every saved page, a page
   change, and a v3/v4 reader.
3. The four sentences, including their length (three short sentences each)
   and the repeated C1/C2 next step when both fail.

## Alternatives considered

- **B, `presentation-model.v4`:** see owner decision 2.
- **Conditional guidance in new input-question versions:** content only. It
  gives the next step but cannot show the answer the filer gave.
- **An `explanation` on a rule `block` (a rule-artifact successor):** it
  cannot say "this answer" without one composite sentence per tree leaf.
- **A hard-coded table in the projection or the page:** ADR 0088 rejected
  this, because the wording would sit outside package manifests and
  validation.
- **A fact-type successor with value descriptions:** it would unpin recorded
  answers.

## Links

- Plan: `docs/phases/engine-breadth/milestones/line16-next-step.md`
- Precedents: ADR 0046 (honest blocking: "what fact is missing and the
  remedy"), ADR 0050, ADR 0086, ADR 0087, ADR 0088; line16-names Decisions
  6–8 and L16-R2; line6b-reason Decision 8.
