# Prototype Plan: Attachment Ontology (D1)

Audience: Agents

Status: **draft — proposed to owner** (principal foreman, 2026-07-18). Track 0,
topic D1 of the Dividends and Schedule B Slice milestone. Operates under
ADR-0030 per-ADR / per-track merges; owner may amend before builder launch.

Topic: **What a schedule attachment *is*.** Schedule B is the first form whose
*existence* the product computes: required when taxable interest or ordinary
dividends exceed $1,500, carrying payer itemizations (Parts I/II) derived from
statement facts already on record and taxpayer answers (Part III) contributed
as facts. The attachment citizen this topic designs is inherited by every
future schedule (D, 1, 2, 3…) — it is the milestone's designated hard trace
case: a walkable derivation whose conclusion is "a form exists," not "a line
equals $X."

## Why this topic exists (and why it is Tier 3)

Nothing in the ontology can currently represent a form's existence, its
completeness, or where *its* incompleteness blocks. Owner directions recorded
in the milestone plan bind and are not relitigated here: **all of Schedule B
is in scope** (determination, Part I/II itemizations, Part III in full,
yes-branch included; FinCEN 114 named, never produced); **dependency-form
completeness** (no structurally born-blocked attachment); **honest blocking
is for factual incompleteness only** — a required-but-incomplete attachment
blocks *on the attachment*, never on line values that remain computable.
Foreclosure principles: trace over answer (the $1,500 conditional's inputs,
threshold, and outcome are explanation content), schema-as-canon, honest
blocking. Exceptions escalate to Tier 3.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing | Gate-1 outcome |
|---|---|---|---|
| D1-P1 | **The attachment citizen.** What kind of thing an attachment disposition is: its schema; its states (not-required / required-and-complete / required-and-incomplete) as *published, walkable* dispositions; the requirement conditional as a declared rule over existing subtotals (interest 2b-side, ordinary dividends 3b-side); where incompleteness blocks (the attachment, structurally unable to block sibling lines); how "not required" publishes as a disposition rather than silence. | Primary | Score 7 — **prototype-eligible** (blast 2: every schedule inherits; migration 2: a wrong state model is data and content to repair; uncertainty 2: no precedent for form-existence dispositions; test 1). |
| D1-P2 | **Itemization content.** Part I/II payer-by-payer rows derived from statement facts on record (payer identity + amount per 1099-INT / 1099-DIV), subtotals, and the tie-out to lines 2b/3b — the first *repeating-row* form content (existing form fields bind single values). | Dependent, same contract surface | Score 6 — **prototype-eligible**, paper rung: the row-model over form-field citizens (ADR-0012) is genuinely new shape; machinery probes unnecessary if paper shows the binding. |
| D1-P3 | **Part III contributed facts.** Foreign-account and foreign-trust taxpayer assertions as fact types (the filing-status/over-65 assertion pattern), yes-branch content (7a FinCEN-114 question named-not-produced, 7b country), contributed via ADR-0032 as-is. | Dependent | Score 4 — **paper spike inside the round**; pattern-following, one case each branch. |

Out of scope: the QDCG worksheet and contradiction check (D2 — it consumes
ADR-0035's signal, not this topic's citizens); any dividend/interest
composition change (ADR-0026/0035 consumed as-is); rendering/human surface
(E8.1 deferred — itemizations are disposition *content*, not UI); other
schedules' content (only the citizen shape must generalize); e-file.

## Gate 1 — Eligibility

Recorded per proposition above. One bounded paper round covers all three;
P3 buys only its two branch cases.

## Gate 2 — Paper evidence

Each builder resolves these synthetic cases (`demo-*` throughout):

1. **Hard trace, both outcomes (mandatory).** (a) Ordinary dividends 1,600 /
   interest 900 → Schedule B **required**; walk the full trace: subtotal
   inputs, the $1,500 threshold with citation, per-trigger outcome
   (dividends trigger, interest does not). (b) Both under threshold →
   **not-required publishes as a disposition** with the same walkable trace
   — never silence. State the boundary semantics (exactly $1,500 is *not*
   over) and cite the instruction text.
2. **Required and complete.** The required attachment composes Part II rows
   from two 1099-DIV statement facts (payer + amount), subtotal ties to 3b;
   Part I likewise from 1099-INT facts tying to 2b; Part III answered no/no
   from contributed facts → the attachment **publishes whole**, pins to
   every consumed fact.
3. **Required and factually incomplete (mandatory kill-case).** Part III
   answers absent → the *attachment* blocks with a walkable explanation
   naming the missing contributable facts; **lines 2b/3b/3a still publish**.
   Show structurally why the attachment's block cannot propagate to sibling
   lines — by construction, not by convention.
4. **Row derivation fidelity.** The tie-out is a declared relation: the sum
   of Part II rows must equal line 3b's published value (same closed family,
   same horizon). Show what guards a row set diverging from the line
   (statement superseded between reads, horizon advance) — the stale-closure
   analogue for itemizations.
5. **Part III yes-branch.** Foreign-account = yes → 7a FinCEN-114 obligation
   *named* in the disposition (never produced), 7b country content required;
   missing country = factual incompleteness (case-3 posture). Foreign-trust
   branch analogous.
6. **Negative — generalization check (mandatory).** Instantiate the citizen
   shape on paper for a *different* attachment (Schedule D stub: required-by
   a different trigger, rows from different facts) using **zero
   Schedule-B-specific schema surface. **If the shape cannot express the
   second schedule without modification, the ontology is Schedule-B-shaped,
   not an ontology — redesign, don't annotate.

Producer → authority → consumer → failure map per proposition. Cases 1, 3,
and 6 are mandatory. **If paper settles the citizen shape, stop at paper.**

## Gate 3 — Evidence depth per question

Authorized: **Rung 1** (static schema/canon diffs, paper cases) for all
propositions. The single question that alone would justify a climb to rung 2:
whether the ratified conditional/selector machinery (ADR-0019/0024/0025) can
express the threshold conditional and the completeness gate *as committed* —
if paper cannot show the expression by citing committed contract text, a
throwaway probe against the committed evaluator is authorized for that
question only. No production code; implementation is milestone Tracks 1–3.

## Gate 4 — Cost caps

- One paper round: incumbent builder plus **clean-room rival** (sealed),
  each producing all six cases and all three propositions.
- No repair pass pre-authorized.
- Two reviewers (Governance Medium, Adversary High), independent contexts.
- Charter ≤ 90 lines; design ≤ 300 lines; examination ≤ 100 lines; reviews
  lean but uncapped; **total topic Markdown target ≤ 1,600 lines** through
  committee (Tier 3, three propositions, novel ontology — above D3's 1,200,
  below the D2-contribution topic's 1,800).

## Gate 5 — Triage

Foreman classifies every finding. Decision-blocking only: the citizen's
state model and blocking placement (P1, cases 1–3), the row/tie-out relation
(P2, case 4), the generalization check (case 6). Deferred, never absorbed:
worksheet/contradiction mechanics (→ D2), rendering (→ presentation
frontier), other schedules' real content (→ future milestones), FinCEN 114
production (→ named non-goal), interest-universe changes (→ ADR-0026
deferrals).

## Gate 6 — Minimum converged subset

The floor: an attachment citizen with the three states as published walkable
dispositions, a declared requirement conditional over existing subtotals,
incompleteness that blocks the attachment and structurally cannot block
sibling lines, rows that tie to their line by declared relation, and the
shape demonstrated on a second schedule stub without Schedule-B-specific
surface. Without case 6 the topic does not converge — a Schedule-B-only
design is milestone content, not an ontology decision.

## Gate 7 — Production boundary

Only documents merge. Accepted structures become a Tier-3 ADR (**candidate
number 0036**), ratified per-ADR (ADR-0030) on owner decision. The
milestone's Track 1 implements the schema citizens, Track 2 the conditional
and itemization behavior, discharging named production conditions.

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium | Scope steward; triage; evidence-ladder enforcement |
| Incumbent builder | High | Novel ontology; the state model and blocking placement set precedent for every schedule |
| Rival builder | High | Clean-room, sealed from the incumbent; same six cases |
| Governance reviewer | Medium | Conformance to ADR-0012 (form fields), 0019/0024/0025 (conditionals), 0020/0029 (explanation, citation), 0032/0035 (consumed contracts), Articles 10/12/14 |
| Adversary reviewer | **High** | The failure modes are the product's core promise: make the attachment's block silently swallow a publishable line (or vice versa — publish a required-incomplete form), break the row/line tie-out unnoticed, and defeat the generalization claim by finding the hidden Schedule-B assumption |

Reviewer seats are named here; owner approval of this plan is the standing
authorization to dispatch them as sub-agents in independent contexts
(ADR-0013 reviewer-dispatch amendment).

## Review measurements

Governance: every state is a published disposition (no silent not-required);
the conditional is declared rule content with citations; rows pin to
statement facts (Article 12); Part III fact types follow the assertion
pattern; no new standing-affecting edge; the second-schedule stub uses only
the generic surface. Adversary: the three attacks above, plus threshold
boundary (exactly $1,500), a Part III answer contributed *after* the
attachment published (supersession posture), and a statement superseded
after its row was derived (stale itemization).

## Data safety

All payers, values, answers, and identifiers in every case, charter, and
review are synthetic (`demo-*`); the owner's real shapes inform cases only
by stated re-expression (ADR-0031). Real facts exist only in the quarantined
workspace and never appear in this topic's Markdown.
