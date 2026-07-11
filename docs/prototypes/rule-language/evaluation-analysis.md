# Prototype Evaluation Analysis — Rule Language

Foreman, 2026-07-10. The evidence document required by ADR-0005 and the Rule Language Design milestone (Track 4). Every conclusion cites followable exhibits; a conclusion without an exhibit is not usable by the ADRs.

Status: complete; committee sign-off pending (see §7).

## 1. The decision under evidence

From the milestone: *what is the rule artifact's operation vocabulary and expression encoding?* — judged against real rules (W-2/1099-INT/1040 core; rounding conventions, tables/brackets, applicability, form-line mappings, cross-form bridges, dependency declaration, method delegation). Companion decisions the same evidence must settle: the publication act kind for derived findings, and where run records live relative to the act log.

## 2. Evidence base

| Exhibit | What it is |
|---|---|
| tag `exhibits/rule-language/it0` | pre-process derivation spike; mined for lessons only (`harvest-notes.md`) |
| tag `exhibits/rule-language/it1` @ `362f8a3` | primary design: expression trees, open grammar, jsonschema-wired validation; `examination-it1.md` |
| tag `exhibits/rule-language/it2` @ `623957c` | clean-room rival: guarded single-publication clauses, schema-enumerated vocabulary, closed packages, start/completion records; `examination-it2.md` |
| `reviews/round-0*` | charter review: governance + adversary, amendment to charter v2, dissent withdrawn by delta-confirmation |
| `reviews/round-1*` | four-instrument review of it1 (+ foreman legibility scoring) |
| `reviews/round-2*` | comparative four-instrument review of it2 vs it1 (+ foreman legibility scoring) |
| `process-log.md` | incidents, dispositions, conformance verdicts, round-close outcome summaries |

The ADR-0005 rivals rule is satisfied: two genuinely different encodings, built clean-room on the same charter v2 fixtures, with the rival's launch context forbidding it1 materials (round-1 disposition entry, process log). Both examinations answer all charter questions Q1–Q11 with disclosed negative results.

## 3. Convergent design conclusions (strongest evidence class)

Two builders who never saw each other's work made the same four choices. Independent convergence under a shared fixture charter is the strongest evidence this process can produce, and all four choices survived both review rounds without a contrary finding.

**C1 — Expression trees, not a closed tax-operation enum.** F7 (line-16 worksheet vs table) forced both. it1: "A fixed operation enum either grows into tax-specific operations or hides worksheet meaning in code" (`examination-it1.md` Q4). it2: "A fixed flat operation record does not survive F7" (`examination-it2.md` Q4). No reviewer dissented from the tree form; round-2 adversary states the open question "is not 'expression trees vs. flat operations' (both builders converged there)" (`round-2-adversary.md`, Dissent).

**C2 — Parameters as separate versioned citizens, cited by id, never inlined.** `examination-it1.md` Q2; `examination-it2.md` Q2; exercised by F5/F7 in both corpora. No contrary finding in any round.

**C3 — Pins carry roles.** Bare id bags do not support explanation; both designs give pins roles (input, choice, parameter, rule, mapping, bridge, adoption, governance, engine). `examination-it1.md` Q8 ("Pins need roles"); `examination-it2.md` Q8 ("Roles earn their place"); legibility round 2 independently recovered the pin contract as "a result is inseparable from the pinned inputs that made it" (`round-2-legibility.md` §E).

**C4 — A distinct derived-publication act kind, deterministic ids, and a start/completion record pair.** Both designs kept derived publication apart from assertion and derived ids as content hashes (`examination-it1.md` Q9/Q10; `examination-it2.md` Q9/Q10). The record-timing lesson traces through three exhibits: it0's run-record timing tension (`harvest-notes.md`), it1's "a final-only run record is not enough... implies a start/completion pair" (Q9 negative evidence), it2's implemented `started` → `completed`/`interrupted`/`failed` immutable pair (Q9). Feeds ADR-0007/0008.

## 4. Comparative conclusions (what round 2 settled)

**C5 — The operation vocabulary must be closed and schema-enumerated.** it1's open grammar (`$defs.expression` accepting any JSON) drew four independent round-1 findings: governance check 5 fail, adversary attack 2 success (undeclared-operation smuggling), legibility semantic-closure fail, examination Q4's own negative evidence (round-1 conformance verdict, process log). it2 closed the enum and the round-2 fresh reader called the closed grammar "the single biggest legibility asset" (`round-2-legibility.md` §G). Enumeration is necessary — and, per C6, not sufficient.

**C6 — The declared schema must be the runtime authority; this is the central unresolved contract problem.** it2 ships the stricter schema document but never loads it — a looser hand-rolled validator governs, and a contract-passing artifact with an undeclared op aborts the entire run (`round-2-adversary.md` parity 1 and 6; `round-2-governance.md` check 5, naming it a regression against it1's genuine `jsonschema`-wired validation; `round-2-legibility.md` L-4: schema-valid exprs can be semantically malformed because per-op required keys aren't bound). Governance's synthesis line is the analysis' recommendation: "A design that adopted it2's schema content and it1's validator wiring would beat both" (`round-2-governance.md` check 5). The adversary frames the residual ADR question exactly: "how does the declared schema become the thing that actually runs" (`round-2-adversary.md`, Dissent).

**C7 — Packages are closed manifests with exact member versions and scope-as-content; year does not live in artifact ids.** Round-1 attacks 5 (year identity) and 6 (advisory membership) succeeded against it1; the identical attacks fail against it2's `validate_contract` (symmetric-difference closure; per-dimension scope check) (`round-2-adversary.md` parity 4, parity 5 — both reported as failed attacks/design held). This is the cleanest before/after evidence pair the process produced.

**C8 — Guarded single-publication clauses; output ownership must be contract-enforced.** it2's one-clause-one-publication shape let the starved reader confirm single-producer behavior for all three doubled outputs from artifacts alone (`round-2-legibility.md` §G) — unrecoverable in it1 (round-1 attack 4). But the contract still permits two artifacts to claim one symbol, resolved by an undeclared evaluator tie-break (`round-2-adversary.md` parity 3, partial). The ADR must require package-level unique output ownership or declared conflict semantics.

**C9 — Rounding: convention as an asserted elective fact plus a staged `round` operation; semantics need versioned canon.** F9/F13/F14 pass in both designs with no operative defaults (`examination-it2.md` Q3/Q6; `round-2-expressiveness.md` check 5). But tie-break arithmetic, `range_lookup`/`bracket_fold` semantics, and band boundaries are evaluator-carried in both iterations — found by every instrument in both rounds and disclosed by it2's own examination (negative 6). Two clean-room builders leaving the same gap is evidence the charter under-specified it (`round-2-governance.md`, Observations); the ADR must place these semantics in versioned canon, not code.

**C10 — Blocking vocabulary is right in shape and incomplete in three declared ways.** Schema'd block codes with named missing symbols work and are fresh-reader legible (`round-2-legibility.md` L-15). Open defects, each with an exhibit: (a) absent-source vs asserted-zero indistinguishable, and it2 has no declaration site to close it (`round-2-adversary.md` parity 2; `round-2-governance.md` check 1; `round-2-legibility.md` L-14 — `requires` is not a complete input manifest); (b) present-but-invalid values degrade into leaked exception strings (`round-2-adversary.md` attack 8); (c) evaluated-and-inapplicable is indistinguishable from never-reached in a completed record (`round-2-adversary.md` attack 9; `round-2-governance.md` check 1).

**C11 — Artifact legibility is achieved; semantic closure is not.** Two starved fresh readers, different rounds, zero wrong recoveries across both corpora (`round-1-legibility-scoring.md`; `round-2-legibility-scoring.md`). What fails recovery is systematic and identical in class across both designs: the arithmetic leaves where the evaluator carries meaning. Both examinations also concede raw JSON needs a purpose-built renderer for nontechnical adoption review (Q4 in each) — a product requirement for any adoption surface, not a language defect.

## 5. What the evidence does not settle (ratification conditions, not open questions)

Each traces to a disclosed negative result or review finding; the ADRs carry them as conditions rather than silently inheriting them:

1. **Schema-as-runtime-authority wiring**, including per-operation required-field constraints in schema (C6; `examination-it2.md` negative 3).
2. **Versioned operation-semantics canon** for `round`, `range_lookup`, `bracket_fold` (C9; `examination-it2.md` negative 6).
3. **Source-set closure vocabulary** — declaring "this collection is closed" vs "unpopulated" (C10a).
4. **Second-runner portability (E11.2)** — unproven by both iterations (`examination-it1.md` Q1 caveat; `examination-it2.md` negative 4).
5. **Storage-level record evidence (E6.1/E14.1)** — record pair proven conceptually, not against real atomic writes (`examination-it2.md` negative 5).
6. **Form-field/fact-type citizen families** — both corpora reference them as bare id strings (`examination-it1.md` Q11 negative evidence; `round-2-legibility.md` L-10).
7. **One role vocabulary** across artifact, package member, and pin (`round-2-adversary.md` attack 7; `round-2-legibility.md` L-8).

## 6. Dissent record

No reviewer dissented from concluding the prototype effort. Standing dissents, all honored by this analysis: round-1 and round-2 unanimous "not ratifiable as-is" for each corpus (the ADRs ratify the language *contract* synthesized from both, not either corpus); governance round-2 dissent from single-successor framing (`round-2-governance.md`, Dissent — this analysis scores no scalar winner); expressiveness round-2 conditional consent, requiring the analysis to record the operation-semantics and portability conditions (`round-2-expressiveness.md`, Dissent — recorded as §5.2 and §5.4).

## 7. Committee sign-off

The milestone exit requires recorded committee agreement that the evidence suffices. Round-2 review positions consenting to conclusion are on record (§6); sign-off on *this document* — that it traces their findings faithfully — is a bounded delta-confirmation per seat, pending in `SEAT.md`.
