# Governance Review — Round 1 — Dividend Composition (D3)

Reviewer: Governance, Medium tier, independent context. Advisory only —
foreman triages, owner disposes. Did not author either artifact.

Scope: D3-P2 and D3-P3 sufficiency per design (it1 incumbent, it2 rival);
D3-P1 conformance checked cheaply, not re-litigated. Measurements per
`docs/archive/2026-08-02-milestone-artifacts/prototypes/dividend-composition/plan.md`: (1) declared universe with
named exclusions; (2) out-of-universe boxes recorded, not composed; (3)
empty-family posture vs. ratified source-closure ontology; (4) subset
invariant as contract text; (5) no new standing-affecting edge beyond
ADR-0010/0017; (6) schema-as-canon; (7) D3-P1 conformance, cheap check.
Also checked against the milestone plan's owner directions (boxes
2a/3/5/7/12 recorded-non-composable, 2a visible to D2; 1b>1a rejected
structurally).

## Data safety

Scanned both designs and examinations for real values/paths. Clean — all
identifiers are `demo-*`, all values small synthetic integers, no real
paths. No flag required.

## D3-P1 (conformance, cheap check)

**it2**: conforms. Cites the committed `packages/tax/statements.py` pattern,
keys statement sameness on payer + tax year + payer_ref, correctly treats
the statement as a logical furnished-return entity peer to evidence
(ADR-0015 decisions 1–2). Sufficient.

**it1**: states conformance ("payer/subject/year/instance keys") but does
not cite the committed pattern or module, and — more materially — its P2/P3
design choice (below, G1) folds multiple box values into a single fact per
statement, which is a modeling choice with consequences for family
granularity that ADR-0015 itself doesn't settle but ADR-0016/0026 do.
Conformance of the identity/keying claim itself is adequate; the downstream
consequence is scored under P2.

## D3-P2 — Ordinary-dividend composition, declared universe

**it2 — sufficient.** Two independent family declarations
(`tax.us.2025.f1099div.1a`, `…1b`), each with its own member fact type,
closure claim, and horizon (ADR-0014/0016/0017 pattern applied per box,
exactly mirroring the ratified 1099-INT precedent where box 1 and box 3 are
separate families despite appearing on one physical statement — ADR-0026
decision 3). The universe citizen names composable {1a,1b} and
recorded-non-composable {2a,3,5,7,12} explicitly, with an honesty clause
("does not claim 'all dividend income complete' beyond {1a,1b}") that
mirrors ADR-0026 decision 7's honesty gate. Excluded boxes ride a distinct
non-member `recorded-boxes` fact — never composed, never a family member.
Case 4/6 walks are concrete and cite specific mechanisms (forbidden-collect
list enforced at package validation). Measurements 1, 2, 5, 6 satisfied.

**it1 — insufficient as designed; G1 (decision-blocking).** it1 declares a
single statement fact type (`f1099div-stmt`) whose `value_schema` carries
*all* boxes (1a, 1b, 2a, 3, 5, 7, 12) as fields of one value object, and
speaks throughout of "the 1099-DIV family" (singular) rather than two
independently declared families. Design text: "the family composition
`div_ordinary` is strictly tied to 1a, and `div_qualified` to 1b" and later
"An empty family... yields subtotal 0 for both 3a and 3b" — both phrasings
describe one underlying family/mapping, not two. This conflicts directly
with ratified precedent:

- ADR-0016 decision 5: closure of one box's statement items "may authorize
  only [that] box's subtotal... It does not authorize [a broader] zero" —
  the box-specific-closure discipline exists precisely to prevent one box's
  closure from silently covering another's.
- ADR-0026 decision 3: even though box 1 and box 3 appear on the *same*
  physical 1099-INT statement, they are modeled as *separate* fact types
  with *separate* families, each independently closable. it2 correctly
  instantiates this; it1 does not.
- ADR-0014 decision 2: a mapping declares "source-family identity/scope,
  member fact type" (singular) — a design where one fact type carries both
  1a and 1b cannot cleanly support two independent mappings/closures
  without further undesigned machinery, because the "member fact type" for
  both would-be families is identical.

Consequence: it1's design cannot represent the case where box 1a is closed
(3b eligible) while box 1b's membership is still open (3a must block) or
vice versa — a case the plan's Gate-2 case 5 and it2's own examination
explicitly cover ("open-1b blocks 3a only... 3b may still publish"). it1's
design text never demonstrates or even claims this independent-blocking
behavior; its case-5 treatment ("If the family is undeclared/unclosed, it
remains an open input, blocking both lines") reads as blocking *both* lines
together, which is either an unstated stronger (and undesirable) coupling
or an unresolved gap. Either way this is not "contract text" settling the
declared-universe granularity — it is an implementation-habit-level
ambiguity precisely where the plan (measurement 3) requires the
ratified closed-empty/undeclared-blocks ontology to be shown per
proposition, not per topic.

This is decision-blocking: it bears directly on the plan's stated floor
(Gate 6) that "box 1a composes to 3b, box 1b composes to 3a" as the two
independently-evaluable propositions the topic exists to settle, and it
silently narrows the box-specific closure discipline that is themselves
ratified, binding contract (ADR-0016 decision 5) that the charter told
builders to "build on, do not reopen."

**G2 (non-blocking).** it1's box-2a return-level disposition is named
`requires-schedule-d`. The milestone's non-goals section places Schedule D
determination entirely out of scope for this milestone ("No Schedule D /
capital gains... D3's prototype confirms which exclusions actually bind");
D3's authorized job is presence-visibility only, not a legal/filing
conclusion. A disposition name that asserts "requires Schedule D" states a
tax conclusion beyond what D3's universe declaration is authorized to make
(the actual requirement determination is D1/D2/future-breadth territory).
it2's neutral `CAPITAL_GAIN_DISTRIBUTION_RECORDED` names the fact without
asserting the legal consequence and is the better-scoped choice. Easily
renamed; not structural. Non-blocking — flag for the disposition-naming
production condition in Track 1/2.

## D3-P3 — Qualified subset, structural enforcement

Both designs land on **admission-time rejection** as the named locus,
which is the correct answer and is well-supported by direct precedent:
ADR-0023 (SC-R1) already rejects a new-member plain assertion at admission
with `FindingModelError` when it would bypass the member-transition chain
— the same admission-time, fail-closed, no-new-edge shape both designs
propose for 1b > 1a. Neither design introduces a new standing-affecting
edge (measurement 5): rejection at admission prevents the pair from ever
becoming current members, so no derivation/individuation edge is ever at
stake — consistent with Article 7's two-edge doctrine and ADR-0010/0017.

**it2 — sufficient.** The line-level proof (Σ Q ≤ Σ O under admission
pairing) is explicit and correct; the divergence guard (independent
horizons; open-1b blocks 3a only, without breaking the inequality on
published pairs) is stated and consistent with the two-family design. The
probe table (P1–P5) concretely demonstrates that JSON Schema (plain,
object-required, constant `maximum`, and `$data`-relative `maximum`) cannot
express the cross-field/cross-finding comparison, satisfying the charter's
Rung-2 mandatory evidence for case 2. Measurement 4 (subset invariant as
contract text) is satisfied by a named, specific locus description
consistent with the ADR-0023 precedent shape (admission-time semantic
check, not a generic mechanism) rather than open-ended machinery.

**it1 — evidentiary gap, non-blocking (G3).** The mechanism itself (a new
`invariants` array on `fact-type.v2`, evaluated by `_validate_finding`) is
a defensible locus in principle and does create no new edge. But: (a) it is
a materially larger contract change than the charter's "instantiate the
pattern" framing anticipates — a generic cross-field/cross-finding
expression-evaluation capability added to the kernel's `fact-type.v2`
schema and general validation path, rather than a named, scoped admission
check in the specific 1b/1a case (contrast ADR-0023, which is itself
scoped, hardcoded semantic logic, not a general invariant DSL); this is a
larger, more open-ended kernel capability than the topic's blast-radius
budget (Gate 0: blast 2 for P3) appears to have contemplated, and it is
not clearly bounded to the dividend domain. (b) The Rung-2 probe evidence
in `examination-it1.md` case 2 is a single narrative sentence ("a throwaway
probe against `_validate_finding` confirms...") with no probe table or
itemized demonstration of the schema-only routes tried and rejected,
unlike it2's five-probe ladder. This is thinner evidence for a charter-
mandatory case than the charter's Rung-2 bar implies, though I leave the
adequacy-of-evidence-depth judgment primarily to the Adversary reviewer's
remit; I flag it here because it also bears on measurement 4 (a design
compelled to lean on a broader, less-precedented mechanism because a
narrower one wasn't explored on paper is weaker "contract text" than one
that is demonstrably the minimal necessary locus). Given G1's blocking
defect already unsettles it1's P2/P3 substrate (the same family boundary
underlies both propositions), I do not separately block on this, but it
should not be adopted without repair even if G1 is fixed.

The line-level proof in it1 (case 3) is directionally correct (sum
inequality under admission pairing) but inherits G1's single-family
ambiguity: if 1a/1b are fields on one fact rather than members of two
independently-closable families, "closed family" in the proof's premise is
undefined per-box, weakening the proof's applicability to the divergence
guard the plan explicitly demands ("if the declared sets could ever
diverge, name the guard").

## Dissent

The two designs' shapes conflict in a way governance **can** reconcile,
not one where it cannot: it2's two-family design is directly precedent-
conforming (ADR-0016 decision 5, ADR-0026 decision 3) and it1's
single-family design is not. This is not a case of two valid but
irreconcilable contract shapes requiring owner adjudication between
competing goods — it is one design conforming to binding, already-ratified
contract text and one not. I recommend the foreman triage G1 as
decision-blocking against it1 specifically (not against the topic), and
treat it2's family/closure shape as the converged answer for Track 1,
pending the Adversary's independent read.

## Findings summary

| Id | Finding | Design | Classification |
| --- | --- | --- | --- |
| G1 | Single-fact/single-family conflation of boxes 1a/1b breaks per-box independent closure (ADR-0016 dec. 5, ADR-0026 dec. 3 precedent); cannot represent independent block/publish per line | it1 | **Decision-blocking** |
| G2 | Box-2a disposition name `requires-schedule-d` asserts an out-of-scope legal conclusion beyond presence-visibility | it1 | Non-blocking (rename in Track 1/2) |
| G3 | Rung-2 evidence for case 2 is thin (one sentence vs. it2's 5-probe ladder); locus mechanism (`invariants` DSL) is broader than the scoped precedent shape (ADR-0023) | it1 | Non-blocking (subsumed by G1; would need repair regardless) |

## Verdict

it2 is sufficient on D3-P2 and D3-P3 as designed, with no decision-blocking
governance findings. it1 is **not sufficient** on D3-P2 (G1) and its P3
design inherits the same defect; it1 needs repair before it can stand as a
converged answer alongside or instead of it2.
