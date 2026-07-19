# Prototype Plan: QDCG Worksheet and Declared Absence (D2)

Audience: Agents

Status: **draft — proposed to owner** (principal foreman, 2026-07-19). Track 0,
topic D2 of the Dividends and Schedule B Slice milestone. Operates under
ADR-0030 per-ADR / per-track merges; owner may amend before builder launch.

Topic: **What happens to line 16 when qualified dividends exist.** The
Qualified Dividends and Capital Gain Tax Worksheet as a declared rule, its
capital-gain inputs bound to contributed declared-absence facts, and the
contradiction check that keeps declared-zero honest.

## Why this topic exists (and why it is Tier 3)

Line 16 is currently a declared rule over ordinary brackets — correct for a
wages-and-interest return, wrong the moment qualified dividends publish.
Owner directions recorded at milestone planning bind and are not relitigated:
**the worksheet is built** (block-on-3a retired by principle); **declared
zero is factual completeness** (the source-closure precedent — zero is never
assumed, only declared); **a declaration contradicted by facts on record is
a hard error** (stale-closure semantics — otherwise declared-zero degrades
into assumed-zero). The remaining rivalry is between worksheet *variants*:
how the ladder is expressed, where the contradiction check sits, and how the
existing line-16 rule is superseded. Tier 3 because the outcome is the
owner's actual tax number.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing | Gate-1 outcome |
|---|---|---|---|
| D2-P1 | **Declared-absence fact types** for the worksheet's capital-gain inputs (no capital-gain distributions; no Schedule D requirement) on the taxpayer-assertion pattern — categorical `{yes, no}` domains with presence semantics and unconditional pinning, exactly the ADR-0036 Part III shape. | Pattern instantiation | Score 4 — **paper spike inside the round**; the pattern is now twice-ratified (filing status; ADR-0036). |
| D2-P2 | **The worksheet as declared rule content.** The QDCG ladder (splitting taxable income into ordinary and preferential portions, the 0/15/20% breakpoints as filing-status-keyed parameter declarations, min/max steps) in the committed expression language; the **reduction property** (qualified = 0 ⇒ worksheet result = ordinary-bracket result); supersession of the existing line-16 rule by versioned content. | Primary | Score 6 — **prototype-eligible**; the single open question is expression-language expressibility of the ladder. |
| D2-P3 | **The contradiction check.** A declared-absence fact and a `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal (ADR-0035, box 2a on a contributed statement) may never both be current — a **hard error in both temporal orders** (declaration first, statement later; statement first, declaration attempted). Locus and mechanism: admission-time rejection, currency displacement, or both. | Primary | Score 7 — **prototype-eligible**; the bidirectional-currency mechanism is genuinely new (D3's admission check was one-shot; this one must hold across later contributions). |

Out of scope: Schedule D and any actual capital-gains computation (the
declarations *assert absence*; computing presence is a future milestone);
1099-DIV boxes beyond ADR-0035's universe; ADR-0026 interest deferrals;
Schedule B (ADR-0036, consumed as-is); the ordinary tax computation itself
(the worksheet's ordinary-tax sub-steps reuse the existing ratified line-16
computation content unchanged); foreign tax credit; any human surface.

## Gate 1 — Eligibility

Recorded per proposition above. One bounded paper round covers all three;
P1 buys only its instantiation cases.

## Gate 2 — Paper evidence

Each builder resolves these synthetic cases (`demo-*` throughout; synthetic
incomes and brackets fine — cite the parameter declarations, don't invent
authority):

1. **Worksheet positive.** Qualified 600 on taxable income well above the
   0% breakpoint: walk the full ladder — split, per-rate portions,
   comparison step, final min — every step a citable expression over
   declared parameters; result strictly below the ordinary-bracket result;
   trace pins the 3a finding, the declarations, and the parameters.
2. **Reduction property (mandatory).** Qualified = 0 (or 3a blocked-empty
   family publishing zero): show the worksheet result *equals* the
   ordinary-bracket result — by algebra on the ladder, not by assertion —
   and state the supersession posture: the worksheet rule supersedes the
   existing line-16 rule as versioned content for all returns (one rule,
   reduction guaranteed), or conditionally selects (two rules, a selector).
   Justify against the anti-wizard and honest-blocking principles.
3. **Missing declaration blocks (mandatory; owner-amended 2026-07-18).**
   Qualified > 0, no declared-absence facts → line 16 blocks with a walkable
   explanation naming a currently encountered contributable declaration —
   factual incompleteness, ADR-0036 presence semantics. The explanation need
   not enumerate every absent declaration in one evaluation: after that fact is
   contributed, a re-run must expose any remaining factual gap. It may never
   imply zero, publish ordinary tax, or make the declarations unconditional on
   qualified-zero returns.
4. **Contradiction kill-case, both orders (mandatory).** (a) Declarations
   current, then a 1099-DIV with box 2a contributed: the contribution (or
   the resulting signal) hard-errors — show where, and what the user is
   told. (b) Box-2a statement current, then a declaration attempted: rejected
   at admission. In neither order may both be current; in neither order may
   line 16 publish over the contradiction. Show the mechanism, not policy.
5. **Declared-zero publishes.** Declarations current ("no"/"no"), qualified
   600: the worksheet publishes with capital-gain inputs bound to the
   declaration findings; pins give supersession an input edge (a superseded
   declaration displaces line 16 to non-current).
6. **Negative — no reach-around (mandatory).** The worksheet cannot read
   box 2a or any recorded-non-composable content directly (ADR-0035
   universe guard): the *only* route from a real capital-gain distribution
   to line 16 is the contradiction hard-error. Show unrepresentable, not
   untested.

Producer → authority → consumer → failure map per proposition. Cases 2, 3,
4, and 6 are mandatory. **If paper settles the ladder and the contradiction
mechanism, stop at paper.**

## Gate 3 — Evidence depth per question

Authorized: **Rung 1** for all propositions, with **rung-2 throwaway probes
for two named questions only**: (a) whether the committed expression
language (ADR-0006/0025) expresses the ladder's min/max/split steps — probe
the committed evaluator only if paper cannot cite the expressibility from
contract text; (b) whether the committed currency machinery (ADR-0010) can
displace line 16 when a pinned declaration is superseded — cite or probe.
No production code; implementation is milestone Tracks 2–3.

## Gate 4 — Cost caps

- One paper round: incumbent plus **clean-room rival** (sealed), each
  producing all six cases and all three propositions.
- No repair pass pre-authorized; a foreman-assembled synthesis, if needed,
  defaults to a scoped confirmation pass per the ADR-0013 2026-07-15
  amendment (as exercised in D1).
- Two reviewers (Governance Medium, Adversary **High**), independent
  contexts.
- Charter ≤ 90 lines; design ≤ 300 lines; examination ≤ 100 lines; reviews
  lean but uncapped; **total topic Markdown target ≤ 1,500 lines** through
  committee.

## Gate 5 — Triage

Foreman classifies every finding. Decision-blocking only: the ladder's
expressibility and reduction property (P2, cases 1–2), the supersession
posture for the existing line-16 rule (P2, case 2), the contradiction
mechanism in both orders (P3, cases 4 and 6), and declaration
presence/blocking (P1/P3, cases 3 and 5). Deferred, never absorbed: actual
capital-gains computation (→ future milestone), tax-table-vs-schedule
fidelity questions in the ordinary sub-computation (→ existing ratified
content, untouched), Schedule B interactions (→ ADR-0036, ratified),
rendering (→ presentation frontier).

## Gate 6 — Minimum converged subset

The floor: a worksheet rule whose ladder is citable expression content with
the reduction property shown by algebra; capital-gain inputs bound only to
declared-absence facts with presence semantics; line 16 blocking on a
currently encountered missing declaration (with progressive re-run disclosure
of any remaining factual gap); and the contradiction hard-error demonstrated
in **both** temporal orders with no state in which both a declaration and a
box-2a signal are current. Without the bidirectional contradiction mechanism
the topic does not converge — one-directional checking is declared-zero
degrading to assumed-zero on a delay.

## Gate 7 — Production boundary

Only documents merge. Accepted structures become a Tier-3 ADR (**candidate
number 0037**), ratified on owner decision (ADR-0030 per-ADR merge). The
milestone's Track 2 implements the declaration and contradiction machinery,
Track 3 the worksheet rule content, discharging named production conditions.

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium | Scope steward; triage; evidence-ladder enforcement |
| Incumbent builder | High | The ladder and the bidirectional contradiction mechanism are novel contract ground |
| Rival builder | High | Clean-room, sealed from the incumbent; same six cases |
| Governance reviewer | Medium | Conformance to ADR-0006/0024/0025 (expressions), 0010 (currency), 0035/0036 (consumed contracts), the assertion pattern, Articles 7/10/12/14 |
| Adversary reviewer | **High** | The failure modes are the owner's actual tax number: publish line 16 over a contradiction (either order), break the reduction property so a no-dividend return's tax silently changes, sneak a worksheet input past the declarations, defeat displacement on superseded declarations |

Reviewer seats are named here; owner approval of this plan is the standing
authorization to dispatch them as sub-agents in independent contexts
(ADR-0013 reviewer-dispatch amendment).

## Review measurements

Governance: worksheet steps are declared expression content with parameter
citations (no arithmetic in prose); declarations follow the ratified
assertion pattern with presence semantics; the superseded line-16 rule
follows versioned-content discipline (Article 7); pins complete (Article
12); no new standing-affecting edge. Adversary: the four attacks above,
plus: contribute the box-2a statement and the declaration in the *same
batch* (ordering attack, the D3/D1 lesson), and a superseded declaration
whose line 16 stays current (displacement failure).

## Data safety

All incomes, amounts, payers, and identifiers in every case, charter, and
review are synthetic (`demo-*`); real shapes inform cases only by stated
re-expression (ADR-0031). Real facts exist only in the quarantined
workspace and never appear in this topic's Markdown.
