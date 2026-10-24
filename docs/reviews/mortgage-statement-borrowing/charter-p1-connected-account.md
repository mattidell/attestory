# P1 — connect the reports without losing their separate accounts

Audience: Builder.

## Purpose

Design the bounded account a person can give for two Forms 1098 concerning
one continuing home borrowing. Keep each report's amounts and support, while
making explicit which circumstances apply to the borrowing. Establish how
that account could support the full-deduction branch before choosing its
software representation. This is design work, not a production build.

P0 established independent recording, transport, calculation and reader
restrictions. In particular, a second report's published reason used the first
report's answers when their values agreed. A subject label is not evidence
of subject-local support. Do not carry that fallback into the new design.

## A — first account and unresolved choices, then return

Begin with a short sequence of actions you will take, in plain language.
Develop the following account in the assigned working design, then return
for Foreman feedback before detailed mechanism selection:

1. Walk through what the person sees and recognizes: two distinct reports,
   one original borrowing, one main home, and a change in the company
   collecting interest. Contrast this with refinancing, two loans and a
   correction/duplicate. Do not infer the relationship from similar labels,
   addresses, amounts or dates, or require independent institutional
   verification of what the person can ordinarily affirm.
2. Propose a finite set of ordinary confirmations and their normalized
   meanings. Distinguish recognizing the continuing borrowing from claiming
   a favorable tax result. Show what cannot-tell, no answer and withdrawal
   mean. Do not invent support for unrelated life statements.
3. Separate report-local matters (including each reported amount and who paid
   that interest) from borrowing/home circumstances and legitimate return-wide
   inputs such as filing status. A shared borrowing may justify shared
   circumstances only through an explicit scope and support relationship,
   not numerical agreement or a copied answer. This does not require asking
   the same genuine loan-wide question twice; establish its meaning and
   scope rather than minimize or maximize the number of facts.
4. State the debt proposition the full-deduction branch needs across the year,
   and compare ways to support it from available information, ordinary
   answers or an explicitly disclosed application assumption. Two dated Box 2
   observations are not an annual average or automatically an upper bound.
   The incumbent single-report premise is a starting point, not authority
   to broaden its scope. Avoid a general debt/proration calculator and avoid
   asking the person to determine tax eligibility themselves.
5. Give a few paper examples showing what the application would know,
   calculate or leave unresolved. Identify consequential owner choices with
   value, cost, risk and displaced work; separate those from mechanical
   implementation choices. Recommend a bounded direction without calling it
   accepted or implementing it.

The first return may leave a choice unresolved. It must explain the actual
choice, not replace it with a vague requirement to "support" or "validate"
the relationship. No prototype, schema allocation or production edit in A.

## B — connected design after Foreman continuation

Use feedback to develop one connected design covering recording, transport,
the combined entry, current family closure, corrections/withdrawals and the
saved explanation. Refine only as far as the settled meaning supports.

### Paper cases the design must answer

| Case or change | What the account must preserve or decide |
| --- | --- |
| Two distinct reports, one continuing borrowing, different interest and dated principal observations | Identify the borrowing, preserve both reports and show the specific basis for the full-deduction treatment; don't add principal observations as separate debts. |
| A claimed common borrowing beside materially contrary report information | Identify what needs clarification; neither a person's link nor a form label silently erases the other account. |
| Equal-looking reports/answers but different or unknown borrowing relationship | No inferred common borrowing, no borrowed answer authority and no favorable partial sum. |
| One report lacks a needed answer or has a contrary answer | Explain whether the missing matter is report-local, covered by an explicitly supported shared circumstance, or unresolved; name the actual consequence. |
| Correct one interest amount without changing the borrowing; separately correct a material relationship | Identify which answers/links remain supported and why, rather than invalidate everything or preserve everything by default. |
| Withdraw or correct the shared account, remove a report and re-record it | End the affected support without asserting its opposite; don't accidentally resume a favorable old route/default. Preserve unrelated current answers and saved history. |
| Add a report after closure, then close again | Existing membership/closure behavior must protect the total; any account about a report set must have an explicit lifecycle. |
| No report, incumbent single report, over-limit or excluded borrowing | Preserve the existing no-activity and single-report behavior; distinguish unsupported calculation from a determined zero and from unresolved information. |

### Existing-first mechanism comparison

- Inspect the adopted student-loan explicit relationship and ordinary
  subtotal/subject-result patterns, and the sale route's bounded keyed-input
  emission. Name what transfers and what does not. Examine all needed
  report-local inputs, not principal alone; correct pins and correction
  dependency matter even when values agree.
- Compare the smallest adequate recording/content designs on paper. A new
  mortgage vocabulary or content version is not automatically a new published
  schema. Do not allocate a schema version or presume a general engine change.
- Trace the candidate from ordinary confirmation to durable assertion,
  current support, admitted sources, scoped evaluation, aggregate, Schedule A
  and saved explanation. Identify real entrypoints and the origin of each
  input/default. Read questions beside their consuming predicates.
- Explain compatibility with already recorded single-report answers and the
  current family claim. Claim reuse requires meaning, scope and lifecycle,
  not a matching field name. Do not require a family successor solely because
  a current consumer is singleton.
- Propose the cheapest discriminating execution only if a consequential
  mechanism question remains. State supplied/manual versus real production
  steps and the observable failure before asking to execute. A paper design
  does not establish production feasibility.

Return the connected design and integration cost. Independent Sol review of
the connected design and any required evidence precedes a production charter.
Track 0 closure remains pending until its requirements are actually met.

## Consequential decisions

Keep a short section in the design for decisions that shape the product:
what the person affirms, what is report-local or shared, which premise the
application assumes, what defeats it, and what a correction changes. Mark
proposals versus owner dispositions. Do not make a ledger of every code
observation, review turn or housekeeping change.

## Connected repair after outside and independent review

Repair the account once against the owner's outside findings and
`p1-independent-review.md`; do not execute the probe or select the pending
owner choice. The Foreman owns plan, phase-state, Git and review records.

- Present two real alternatives before the experiment: all nine incumbent
  ordinary answers stay report-local, with only the new borrowing account
  facts shared; or genuinely loan-wide ordinary assertions use per-report
  intermediate joins. Compare person effort, content/recording/lifecycle
  costs and provenance risk. Neither is selected. Repetition in the local
  option is a product trade-off, not an invalid model or storage mistake.
- For either option, inspect the real student-loan answer-status rules using
  `joined_contains_subject`. Compare meaningful scoped rules that actually
  read their answer or observation against new mortgage admission code.
  Existing `subject`/`joined` discovery is the first candidate; an inert dummy
  declaration is not evidence. Do not claim it works before the experiment.
- Keep raw Box 3 observations report-local and derive one borrowing-wide
  category from their agreement. Disagreement is a named unresolved conflict.
  Preserve the incumbent pre-1987 exclusion and conservative $750k/$375k
  parameter; explain the unmodeled higher pre-2017 acquisition-debt limit.
  Include one isolated conflicting-Box-3 mutation in either experiment option.
- Repair every contradictory closed-empty instruction, especially the
  integration recommendation. Keep the current affirmative-orphan-link case
  distinct from retained borrowing facts and withdrawn links.
- State the absence of a supported connected-account exit as a deliberate
  proposed limit for owner disposition, not a silent permanent-routing rule.
  A future explicit clear-account operation would have to end the current
  connected scope without deleting history or report-local answers. This
  experiment does not implement or establish that operation.
- Make the experiment conditional on the owner choice: the report-local
  option has no shared-answer intermediate or producer-removal control;
  the shared option includes both. Both test real report-local transport,
  tax-category reconciliation and one authorized line8a result. No further
  paper refinements are required once this connected repair and owner choice
  are settled; actual experiment evidence still receives its planned review.

Read the P1 review and this section together. Return the repaired account and
a brief owner-choice comparison. No production, schema allocation, test run,
package edit or experiment execution in this unit.

## Context Capsule

- Resolve `HEAD` at launch and reconcile with Git. Milestone
  `mortgage-statement-borrowing`; primary branch
  `milestone/mortgage-statement-borrowing-same-loan`; ratified `origin/main`.
  Use the managed primary worktree supplied at launch, never the concurrent
  performance worktree.
- Role: fresh Luna Builder. No subagents, staging, commit or push.
- Assigned write only:
  `docs/phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing-evidence/p1-connected-account.md`.
- Read Builder boot, Owner Model, concurrent protocol, planning guidelines,
  active plan, completed P0 account and independent review/recheck, and the
  named mortgage/consolidation retrospectives. Inspect exact question, save,
  content, transport, dispatch and saved-reader sources relevant to a proposed
  reuse. Read accepted ADRs in full only when relying on their exact contracts.
- Use P0's verified primary 2025 sources; browse primary sources for any new
  tax proposition. Do not treat source research as evidence that a proposed
  recorder or rule ran.
- Evidence ceiling: first a plain-language/paper account, then a connected
  design only after continuation. No execution, tests, schemas, production
  artifacts, package adoption or dependency/configuration changes authorized.
- Stop and return a clear owner choice if the selected case needs broader
  allocation, refinancing, institutional verification, general identity or
  engine redesign. Do not quietly drop the shared-borrowing goal to fit the
  incumbent engine. Stop for private data or governance interpretation.
