# Track 3b — Bounded external-comparison brief

- Phase: Grammar Census
- Milestone: Engine Language Map (`grammar-census`)
- Track: 3b — bounded external-comparison brief
- Role: Builder
- Status: in progress
- Source ref verified: `HEAD` `af766540adbc5a1963e0a8f6a6100fc39909bdb8`
  on `milestone/grammar-census-engine-language-map`
- Assigned path: this file only
- Primary inputs: Track 2 reconciliation `f276cc5b` (166 constructs),
  representative traces `3dba1a80` (6 traces), tension catalog `5ba385c1`
  (9 entries); Track 0 boundary map; Foreman correction
  `docs/reviews/2026-08-20-grammar-census-foreman-correction-5b-ii-ruling-reasoning.md`;
  carried-forward candidate dimensions from
  `docs/reviews/2026-08-19-grammar-census-track-0-boundary-map-external-critique.md`
  ("Standing value beyond this repair")
- Charter: `docs/reviews/2026-08-20-grammar-census-track-3-synthesis-and-comparison-charter.md`
  (Track 3b section)

This brief **scopes** a later comparative review. It does not conduct one.
It makes no grammar change, product contract, ADR, governance
interpretation, or external-standards claim. It selects nothing. The
phase stays open; the next milestone is owner-held.

Every statement about **this engine** cites a reconciled construct
(`U-###`), a catalog entry (`T#`), a named trace, a committed path with
version, or an execution shown under `#Source checks this stream ran`.
Every characterisation of an external system is **external and
unverified**: this stream did not read those systems' artifacts, and
this milestone's evidence ceiling does not cover them. Where the
characterisation is a recollection rather than a checkable claim, the
text says so.

Do not cite the sibling Track 3a map. The census is the source.

## What this brief is

The plan's `#External comparison brief`
(`docs/phases/grammar-census/milestones/engine-language-map.md`) requires
five statements:

1. which semantic dimensions are now worth comparing;
2. which external systems appear relevant to each dimension;
3. what questions a comparison could answer;
4. what evidence would change an engine decision;
5. which comparisons would be superficial or inapplicable.

Exit criterion 7 is that a follow-on comparative review can be scoped
from those questions rather than from a generic survey of other
languages. A paragraph that summarises what Catala or OpenFisca *is*
has failed that criterion; a paragraph that says "compare us to Catala
on X, because the census found Y, and answer Z would be relevant to
the owner call already named in T#" has met it.

The candidate corpora the plan names — Catala, OpenFisca, DMN/FEEL,
Datalog/RIF, LegalRuleML, provenance standards, other tax-computation
systems — are **candidates to attach to a dimension**, not a checklist
to tour. None is presumed a model to adopt.

## Method

1. Start from the tension catalog's expressiveness entries (T8, T9)
   and from the census facts the traces selected as semantic contrasts
   (two expression grammars; false-`when` is inapplicable; source-set
   closure; blocking-code collapse; producer conflict). Those pressure
   the dimension list harder than the Track 0 consultation's six
   suggestions.
2. For each of the six carried-forward candidates, say keep or drop,
   with the census purchase that decides it. A drop is a finding about
   this engine, not a gap in the brief.
3. For each kept dimension: name the engine facts, name the external
   systems that appear relevant, write the questions, name the owner
   call a positive or negative answer would be relevant to, and name
   the superficial comparison on that same dimension.
4. Do not originate an engine finding from an external recollection.
   If the census did not pressure a dimension, drop it.
5. Re-check load-bearing engine facts against source in this worktree
   (shown under `#Source checks this stream ran`).

## Carried-forward candidates: keep or drop

These six arrived as an external-model consultation, recorded in
`docs/reviews/2026-08-19-grammar-census-track-0-boundary-map-external-critique.md`
as "a substantive first draft of comparison dimensions for Track 3's
brief" and as "an external model consultation, never as authority."
This stream treats each as a candidate to assess.

| Candidate as carried | Decision | Census purchase, or the absence of one |
| --- | --- | --- |
| Peer languages versus one grammar with satellites (DMN/FEEL vs boxed expressions vs tables) | **Keep** as dimension 1 | The census has two expression grammars that share op *strings* and are not the same constructs (reconciliation naming table; U-008 vs U-114; U-015 vs U-121; U-010/U-011 vs U-122/U-123). Trace 6 exists because traces 1–5 do not exhibit the second grammar. Track 0 reversed 5b-i from adjacent to proper after finding `$defs/term` / `$defs/predicate` on `source-family.v2`, not on any attachment-rule schema. |
| Embedded versus standalone (where meaning is allowed to live) | **Keep** as dimension 2 | T1 (ADR-0066 decision 2 is not what admission does to term trees), T5 (`bracket_fold` loads canon `spec` and does not read it), T6 (required clause `blocked` is authored, not consumed), T7 (`OPERATION_VOCABULARY` is a 14-name leftover), T8 (exclusive-graph axioms live as Python tax ids). The census pressured *locus*, not a textbook language-design category. |
| Object language versus observational theory (traces as productions) | **Keep, narrowed** as dimension 5 | T3: evaluator-native codes (`LOOKUP_MISS`, `FAMILY_VALIDATION_BLOCKED`) and later record codes (`SLI_*`) do not survive onto the walk the explanation path can legally carry. That is a produced-record fidelity question the census actually found. The broader question "are these artifacts the law, or a description of it?" is not a catalog entry and is dropped as framed. |
| Defeasibility — whether rules can be overridden by other rules, as a paradigm rather than a blocking enum | **Drop as framed.** A narrower residue is kept as dimension 6 | The census did not find a missing yield-to operator, a priority lattice, or an exception-to-default form. What it found is T4: `selected_producer` *permits* two publishers at admission; the runner never reads the field; runtime is first-eligible-wins (U-044, U-072, U-073). Current committed conflict is guard-partitioned (`count == 0` vs `count != 0`). Blocking is a disposition (Trace 2, Trace 3, U-006), not an override. Comparing "does Catala have defeasible rules" would be the generic survey the plan forbids. |
| Period and horizon semantics, as OpenFisca handles them | **Drop** | Surface 8 records family-horizon succession (U-157) and the act/fact/entity/horizon substrate (U-154) as **grammar-adjacent store**. All 49 `source-closure-mapping` files write `admission.condition` `current-literal-true` (U-144). The clause language has no period operator in the 23-op dispatcher (U-027). No catalog entry treats that absence as a gap. An OpenFisca-period tour would not be answering a question the census asked. |
| Constitutive versus prescriptive rules, as LegalRuleML distinguishes them | **Drop** | The census did not pressure a deontic/constitutive split. Rule-artifacts compute and publish (U-033, U-034); `when` false is inapplicable, not forbidden (Trace 2, U-032, U-043); `block` is an expression op that raises `EvalBlocked` (U-006). T8's exclusive-graph axioms are the nearest constitutive *form*, and they already drive dimension 3. A LegalRuleML constitutive/prescriptive survey would not be answering a census question. |

The two drops that are findings about this engine, restated: **this
engine's clause language does not encode period as an expression-level
feature**, and **this engine does not have a defeasibility paradigm**.
Those are census observations (U-027, U-144, U-157; T4, Trace 2), not
comparative conclusions. They are why those two carried-forward
dimensions do not earn a comparison.

## Census-pressured dimensions (the list that should drive a later unit)

Seven dimensions. Order is consequence for a later comparative review,
not a ranking of tax importance, and not a recommendation.

| # | Dimension | Driven by | External systems that appear relevant |
| --- | --- | --- | --- |
| 1 | Two expression grammars that share names and do not share meaning | Trace 6; reconciliation naming table; Track 0 5b-i reversal | DMN/FEEL and its peer notations; Catala (whether it is one language); Datalog (whether it is one) |
| 2 | Where a construct's meaning is allowed to live | T1, T5, T6, T7, T8 | Catala; OpenFisca; DMN (FEEL spec vs host) |
| 3 | Exclusive-graph / non-confusion axioms as content or as host-language literals | T8, U-085; contrast U-110 | Datalog-style integrity constraints; DMN hit-policy UNIQUE; RIF (uncertain) |
| 4 | Whether `ref` / `collect` names are typed against a fact schema | T9, Track 0 gap 5, U-153 | DMN item definitions / FEEL names; OpenFisca registered variables; Datalog predicate schemas |
| 5 | What the produced explanation record is allowed to say | T3, D5, D14, Trace 6's remap ending | provenance standards (W3C PROV); Catala explanation traces; DMN decision traces |
| 6 | Conflict: admission permit versus runtime winner; applicability versus override | T4, U-044, U-072, U-073; Trace 2 | DMN hit policies; Catala default/exception (uncertain as a mapping); OpenFisca formula replacement (uncertain) |
| 7 | Empty versus nonempty source-set closure | Trace 1 S4 surprise; Trace 3; D8; U-004, U-005, U-026 | OpenFisca empty collections; DMN collect; Catala aggregates (all unverified) |

Each dimension is written out below. The `#Superficial or inapplicable`
section then names the comparisons that would bound a later unit even
if that unit never opens these seven.
