# Prototype Plan: Dividend Composition (D3)

Audience: Agents

Status: **draft — proposed to owner** (principal foreman, 2026-07-18). Track 0,
topic D3 of the Dividends and Schedule B Slice milestone. Operates under
ADR-0030 per-ADR / per-track merges; owner may amend before builder launch.

Topic: **How a 1099-DIV becomes lines 3a and 3b.** Statement-instance identity
and source-family membership for 1099-DIV (the ADR-0015 pattern), the
ordinary-dividend composition for line 3b with a declared universe (the
ADR-0016/0026 pattern), and the qualified subset for line 3a — the first
*coupled* line pair, where one line is by definition a subset of the other
(3a ≤ 3b) and the contract must decide where that invariant is structurally
enforced.

## Why this topic exists (and why it is Tier 2)

The statement→family→composition→line pipeline is ratified, twice-proven
contract ground (1099-INT: ADR-0015/0016/0026; W-2 closure: ADR-0014/0017).
D3 instantiates it for a new document, which alone would be Tier 1 content.
Two things raise it to Tier 2 (default + veto, prototype process): the
**declared universe** for dividends must name its exclusions (boxes 2a, 3, 5,
7, 12 → honest blocks, per the approved milestone plan), and the **qualified
subset** is a new contract shape — no existing composition couples two lines
by a subset relation, and the enforcement point (per-statement box 1b ≤ box
1a at admission; line-level 3a ≤ 3b by construction or by check) is
undesigned. **Owner-defaulted at milestone planning, veto window open:**
the subset is *structurally enforced* — an entry where qualified exceeds
ordinary is rejected, not recorded.

Milestone foreclosure principles binding here: schema-as-canon (new citizens
get schemas before instances), honest blocking (out-of-universe boxes block
by name, never silently drop), and the D2 interplay — box 2a's *presence* on
a contributed statement must be visible to D2's contradiction check, so D3's
statement schema must carry out-of-universe boxes as **recorded but
non-composable** content, not refuse them at the door. That interplay is a
named paper case below, not a new decision.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing | Gate-1 outcome |
|---|---|---|---|
| D3-P1 | **1099-DIV statement identity and family.** Statement-instance identity keys, source-family claim, horizon-keyed closure participation — the ADR-0015 pattern applied to a new document. | Pattern instantiation | Score 3 — **implement normally** under existing contracts; recorded here, no prototype evidence bought (ADR-0013 Gate 0: the finding is recorded, not assumed). Reviewed as ordinary track work. |
| D3-P2 | **Ordinary-dividend composition (line 3b) with declared universe.** Box 1a composes; boxes 2a/3/5/7/12 are named exclusions that block honestly when present; statements carry them as recorded, non-composable content (the D2-contradiction-check feed). | Pattern instantiation + named exclusions | Score 4 — **paper spike + ADR draft**; the universe declaration and the recorded-but-non-composable posture need paper cases, not machinery evidence. |
| D3-P3 | **Qualified subset (line 3a) with structural enforcement.** 3a composes from box 1b; the invariant 1b ≤ 1a per statement and 3a ≤ 3b per line is enforced structurally. Open question: *where* — JSON Schema cannot express cross-field numeric comparison, so enforcement must land in admission machinery, the composition contract, or both. | Primary | Score 6 — **prototype-eligible**; the enforcement locus is the topic's single open question. |

Gate-1 axis scores — P1: blast 1, migration 1, uncertainty 0, test-cost 1.
P2: blast 1, migration 1, uncertainty 1, test-cost 1. P3: blast 2 (first
subset-coupled composition; Schedule D's 3a-adjacent shapes will inherit it),
migration 2 (an unenforced subset admitted now is data to repair later),
uncertainty 1 (paper narrows the loci; only a probe proves rejection),
test-cost 1.

Out of scope: Schedule B (D1's topic — the itemization *reads* D3's statement
facts, it does not shape them), line 16 / the QDCG worksheet (D2 — D3 only
guarantees box-2a visibility), line-9 content growth (Tier 1 track work),
contribution mechanics (ADR-0032, consumed as-is), any widening of the
interest composition (ADR-0026 untouched).

## Gate 1 — Eligibility

Recorded per proposition above. Net: this topic runs **one bounded paper
round** covering P2 + P3, with machinery probes authorized for P3 only. P1
carries no prototype evidence; its conformance is checked by the round's
governance reviewer in passing (cheap) and enforced at the implementation
track's normal review gate.

## Gate 2 — Paper evidence

Each builder resolves these synthetic cases (all payers, values, identifiers
synthetic; `demo-*` convention):

1. **Two positives.** (a) A single 1099-DIV with 1a=900, 1b=600 → 3b=900,
   3a=600, both lines publishing with citations and the subset visibly
   holding. (b) Two statements composing: 1a=900/1b=600 and 1a=400/1b=0 →
   3b=1300, 3a=600 — the second statement legitimately contributes nothing
   qualified.
2. **The subset kill-case (mandatory).** A statement with 1b > 1a. Show
   exactly where it dies: at contribution admission, at composition, or both
   — and why that locus (not schema regex; JSON Schema cannot compare
   fields). A design that records the violating statement and "handles it
   later" is a foreclosure violation (silent wrongness), not a valid answer.
3. **Line-level subset by construction or by check.** Show whether 3a ≤ 3b
   can be violated when every statement individually satisfies 1b ≤ 1a
   (it cannot, if both compose over the same closed family — *prove* that,
   don't assert it), and what guards the case where the two lines' declared
   sets could ever diverge.
4. **Out-of-universe box, honest block (mandatory).** A statement carrying
   box 2a: the statement admits, 2a is recorded non-composable, 3a/3b still
   publish, and the *return-level* consequence is a named disposition
   feeding D2's contradiction check — walk the trace. Contrast with box 7
   (foreign tax): recorded, named, no D2 linkage.
5. **Empty family closes honestly.** No 1099-DIV, closed-empty declared set →
   3a=3b=0 publish (the source-closure precedent, applied); an *undeclared*
   family blocks both lines.
6. **Negative — universe creep.** Show that composing box 2a into any line
   is unrepresentable under the declared universe, not merely untested.

Producer → authority → consumer → failure map per proposition. Cases 2, 4,
and 6 are mandatory. **If paper settles the enforcement locus, stop at paper**
— the probe rung exists for the rejection demonstration only.

## Gate 3 — Evidence depth per question

Authorized: **Rung 2 for P3's case 2 only** — throwaway probes against the
committed validation/admission machinery demonstrating the 1b > 1a rejection
at the chosen locus (and that the schema-only route genuinely cannot express
it). P2 stays at rung 1 (static schema/content examples). No production
composition code; that is the milestone's Tracks 1–2.

## Gate 4 — Cost caps

- One paper round: incumbent builder plus **clean-room rival** (sealed from
  the incumbent), each producing all six cases (ADR-0013 rivalry amendment).
- No repair pass pre-authorized.
- Two reviewers (Governance Medium, Adversary Medium), independent contexts.
- Charter ≤ 80 lines; design ≤ 250 lines; examination ≤ 100 lines; reviews
  lean but uncapped; **total topic Markdown target ≤ 1,200 lines** through
  committee — below the D2-topic cap because two of three propositions
  bought no prototype evidence.

## Gate 5 — Triage

Foreman classifies every finding. Decision-blocking only: the subset
enforcement locus and its rejection semantics (P3, cases 2–3); the declared
universe with recorded-non-composable exclusions and the box-2a visibility
guarantee (P2, cases 4 and 6). Deferred, never absorbed: Schedule B shapes
(→ D1), worksheet/contradiction mechanics (→ D2), any 1099-DIV box beyond
1a/1b entering the universe (→ future breadth milestone), P1 refinements
(→ implementation track review).

## Gate 6 — Minimum converged subset

The floor: a declared dividend universe where box 1a composes to 3b, box 1b
composes to 3a, 1b > 1a is **rejected at a named locus with a probe showing
it**, out-of-universe boxes are recorded non-composable with box 2a's
presence visible to a return-level disposition, and a closed-empty family
publishes zeros. Without the enforced subset the topic does not converge —
recording both lines independently is the status quo, not a decision.

## Gate 7 — Production boundary

Only documents merge. Accepted structures become a Tier-2 ADR (**candidate
number 0035**), ratified per-ADR (ADR-0030) after the owner's veto window.
The milestone's Track 1 implements the schema citizens, Track 2 the
composition behavior, discharging the ADR's named production conditions.
P1's "implement normally" finding is carried into the Track 1 charter text.

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium | Scope steward; triage; evidence-ladder enforcement |
| Incumbent builder | High | The subset-enforcement design is the one open question and it sets precedent for every future coupled line |
| Rival builder | High | Clean-room, sealed from the incumbent; same six cases |
| Governance reviewer | Medium | Conformance to ADR-0015/0016/0026 patterns, ADR-0014/0017 closure, schema-as-canon; P1 conformance in passing |
| Adversary reviewer | Medium | Failure modes are bounded and reversible (bad data rejected vs. admitted); attack: sneak 1b > 1a past the locus, compose 2a into a line, make an undeclared family publish zeros |

Adversary is Medium (not High, unlike D2's seat): the worst outcome here is
a wrong synthetic number caught by review, not an irreversible boundary
leak. Reviewer seats are named here; owner approval of this plan is the
standing authorization to dispatch them as sub-agents in independent
contexts (ADR-0013 reviewer-dispatch amendment).

## Review measurements

Governance: the universe is declared, exclusions named, no new
standing-affecting edge; statements carry out-of-universe boxes without
composing them; the empty-family posture matches the ratified source-closure
ontology; the subset invariant is contract text, not implementation habit.
Adversary: the three attacks above, plus order-dependence between the two
lines' compositions (3a must not depend on 3b's evaluation order or vice
versa).

## Data safety

All statements, payers, and values in every case, charter, and review are
synthetic (`demo-*`); the owner's real 1099-DIV shapes inform cases only by
re-expression, with the synthesis method stated where used (ADR-0031
independent-construction rule). Real documents and values exist only in the
quarantined workspace and never appear in this topic's Markdown.
