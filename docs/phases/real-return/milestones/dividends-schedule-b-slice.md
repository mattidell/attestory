# Milestone: Dividends and Schedule B Slice

Status: **approved — active** (owner approval 2026-07-18, recorded at merge
of the planning branch; ADR-0013 satisfied). Second milestone of the Real
Return phase; operates under ADR-0030 per-ADR / per-track merges and
ADR-0034 owner-approved dispatch. The owner's plan-stage scope directions
(Schedule B whole-form, dependency-form completeness, D2 declared-zero
narrowing) are recorded in their sections and were part of the approved
text.

## Decision summary (tiered)

- **Tier 3 (owner, prototype-backed): D1 — Schedule attachment ontology.**
  What an *attachment* is as a citizen: Schedule B's existence is itself a
  computed, explainable disposition (the designated first hard trace case —
  the product decides whether a *form* exists, not just a line value). Covers
  the >$1,500 conditional over both interest and ordinary dividends (the
  conditional reads an existing domain, so its shape touches ratified
  content). Product-visible and ontology-setting: every future schedule
  (D, 1, 2, 3…) inherits this shape. **Owner direction (2026-07-18, recorded
  at plan stage):** the attachment is a product concept, and *all of
  Schedule B is in scope* — the determination, Part I/II payer itemizations
  (derived from statement facts already on record, tying to 2b/3b), and
  Part III in full (the foreign-account and foreign-trust answers as
  contributed taxpayer-assertion facts, including the yes-branch form
  content). D1 designs the citizen shape; it does not relitigate this scope.
- **Tier 3 (owner, prototype-backed): D2 — Line 16 under qualified
  dividends.** Today line 16 is a declared rule over ordinary brackets. When
  qualified dividends exist, the correct tax comes from the Qualified
  Dividends and Capital Gain Tax Worksheet, which also reads capital-gain
  inputs this milestone does not cover. **Owner direction (2026-07-18,
  recorded at plan stage):** honest blocking is for *factual* incompleteness
  only, never designed-in incapacity, and a *declared* zero is factual
  completeness — the same ontology the source-closure design ratified (an
  empty declared set closes honestly; zero is never assumed, only declared).
  The rival space is therefore narrowed: the worksheet is implemented as a
  declared rule with its capital-gain inputs bound to contributed
  declared-absence facts; "block line 16 whenever 3a > 0" is retired by
  principle. **A declaration contradicted by facts on record (e.g. a
  contributed 1099-DIV carrying box 2a against a no-capital-gains
  declaration) is a hard error**, mirroring stale-closure semantics —
  otherwise declared-zero degrades into assumed-zero. D2's prototype designs
  the worksheet rule shape, the declared-absence fact types, and the
  contradiction check; the remaining rivals are worksheet *variants*, not
  whether to build it.
- **Tier 2 (default + veto, prototype-backed): D3 — 1099-DIV statement
  identity and dividend composition.** The 3b (ordinary) composition with a
  declared universe and the 3a (qualified) subset relationship (3a ≤ 3b as a
  structural invariant, not a hope), following the ADR-0015/0016/0026
  pattern. Gate 0 may find parts need no prototype; that finding is
  recorded, not assumed.
- **Tier 1 (log only):** 1099-DIV closure-mapping content under ADR-0014/0017
  (horizon-keyed, immutable); line-9 total-income content extension to
  include 3b under existing rule-artifact contracts; live-run harness
  extension.

## Objective

The owner contributes real 1099-DIV facts through the ratified contribution
boundary; the return slice grows lines **3a and 3b**, line 9 absorbs
dividends, and the product computes — with a full walkable trace — whether
**Schedule B** exists for this return, publishing the attachment disposition
or blocking honestly. Line 16's disposition under qualified dividends follows
D2. The repository continues to provably carry zero personal data.

## Why this milestone

Selected by the owner 2026-07-18 over a human presentation surface and
L3→L4 hardening. The matrix is breadth-limited: every covered cell is L3, and
the expensive machinery (data boundary, contribution, production resolver) is
paid for. This milestone is the first repeat purchase of the platform — it
measures whether the marginal cost of a new domain actually dropped, which is
the core scalability claim. It also lands the first *hard trace*: a
computation whose output is the existence of a form, exercising
explanation/conditional machinery on a qualitatively new disposition kind.

## Scope

1. **1099-DIV source family (D3 + Tier 1 content).** Statement-instance
   identity, family claim, horizon-keyed closure mapping; boxes in the
   declared universe: 1a (ordinary), 1b (qualified). The owner's real family
   closes over their declared set.
2. **Lines 3a/3b (D3).** Ordinary-dividend composition with a declared
   universe; qualified as a structurally enforced subset; both lines flow to
   form-field dispositions with citations like every existing line.
3. **Line 9 extension (Tier 1).** Total income includes 3b, under existing
   contracts — content, not a reopened contract.
4. **Schedule B attachment disposition (D1) — the whole form.** The
   attachment citizen; the >$1,500 conditional over interest *and* ordinary
   dividends; Part I/II payer itemizations derived from the statement facts
   already on record, subtotaled and tied to lines 2b/3b; Part III answered
   through two new contributed taxpayer-assertion fact types (foreign
   financial account; foreign trust), yes-branch form content included. A
   return that requires Schedule B and cannot complete it blocks honestly —
   on the *attachment*, never on line values that remain computable. (The
   FinCEN 114 filing Part III can point to is a separate non-1040 filing,
   not an attachment of this return; naming that obligation when triggered
   is in scope, producing it is not.)
5. **Line 16 under qualified dividends (D2).** The QDCG worksheet as a
   declared rule; capital-gain inputs bound to contributed declared-absence
   facts; the contradiction check as a hard error. Line 16 blocks only when
   a required declaration is factually missing or contradicted.
6. **Live-run integration.** The owner's real run over the widened slice;
   acceptance evidence is the non-descriptive attestation, same form as the
   First Real Return Slice.

## Non-goals and deferred boundaries

- **No Schedule D / capital gains.** 1099-DIV box 2a (capital gain
  distributions) is outside the declared universe; if the owner's real
  1099-DIV carries box 2a, that is a named blocked disposition, never silent
  omission. Likewise boxes 3, 5 (§199A), 7 (foreign tax), 12
  (exempt-interest dividends): outside the universe, honest blocking if
  present. D3's prototype confirms which exclusions actually bind for the
  owner's shapes.
- **No document parsing/OCR** — manual contribution remains the mode.
- **No human presentation surface** — the attachment disposition renders
  through existing form-field/CLI/JSON surfaces; E8.1 stays on the frontier.
- **No hardening scope** — the deferral ledger (guarded transport first) is
  untouched unless the owner separately directs a rider after Track 0
  economics are known.
- ADR-0026's interest deferrals (K-1, market discount, subtractive
  adjustments) remain deferred; Schedule B Part I reads the *existing* 2b
  composition, it does not widen it.

## Contracts

### Existing (build on, do not reopen)

ADR-0011/0014–0017 (identity, closure, horizons), ADR-0015/0016 as the
statement/family pattern D3 instantiates, ADR-0019/0024/0025 (selectors,
conditionals, expressions — the $1,500 conditional's substrate), ADR-0026
(2b composition, read-only here), ADR-0020/0029 (explanations, citations),
ADR-0027/0028/0033 (packages, production resolution), ADR-0031/0032 (data
boundary, contribution), ADR-0030/0034 (process).

### Decided here

D1 attachment ontology, D2 line-16-under-qualified-dividends, D3 dividend
composition — each through the ADR-0005/0013 prototype process with an
owner-approved `docs/prototypes/<topic>/plan.md` before first charter, rival
evidence per ADR-0013, per-ADR no-ff merge on ratification.

## Data safety

Standing rules unchanged and in force: real values never appear in commits,
fixtures, goldens, charters, reviews, or retrospectives; per-review safety
scans; installed envelope gates byte-verified in every clone. The owner's
real 1099-DIV shapes inform synthetic fixtures only by re-expression, with
the synthesis method stated in the introducing track.

## Verification

- Full in-repo suite, mypy, governance lint stay green and fully synthetic.
- **Promoted lesson (First Real Return Slice retrospective), now a standing
  charter requirement:** every behavior track's charter names its
  authoritative-surface golden class explicitly. For this milestone that
  means coordinator-from-facts goldens driving `live_coordinate_run` from an
  authoritative fact log for: 3a/3b publication, line 9 with dividends, the
  Schedule B attachment disposition (both existence outcomes; the complete
  form with Part I/II itemizations tying to 2b/3b; Part III answered via
  contributed facts, both branches; and the honest block when required
  answers are absent), and line 16 under D2's ratified shape. A green suite
  without these named goldens is not evidence.
- Acceptance evidence for the real run is the owner's non-descriptive
  attestation in this section — ran the slice, dispositions observed in
  quarantine, no artifact crossed the boundary — never which lines or
  attachments published or blocked.

## Exit criteria

1. D1/D2/D3 ratified with rival-backed evidence; per-ADR merges on `main`.
2. The synthetic battery drives the full widened slice from the
   authoritative surface, including the named golden classes above.
3. The owner has contributed real 1099-DIV facts and run the widened slice;
   the non-descriptive attestation is recorded.
4. The 1099-DIV family closes over the owner's declared set (horizon-keyed;
   stale closure remains a hard projection error).
5. The repository contains zero personal data, mechanically checked.
6. Maturity matrix updated (Dividends column L0→L3 across aspects;
   Schedule-attachments column L0→L3 for the aspects Schedule B exercises,
   with honest footnotes for the rest); phase-state briefing rewritten;
   retrospective written; deferral ledger for this milestone recorded, and
   any prior-ledger entries this milestone touches dispositioned by name.

## Tracks

Per ADR-0030, each decision topic and each track is its own short-lived
branch with its own review gate and no-ff merge; dependency order, not a
single-branch plan.

### Track 0 — Contract decisions (D1, D2, D3)

Three prototype topics, each with an owner-approved plan before first
charter. D3 (composition) can start immediately — it instantiates a proven
pattern. D1 (attachment) and D2 (line 16) are the genuinely new ground; D2
depends on D3's qualified-subset shape and may run after it ratifies. Gate-0
economics are reported to the owner before charters are cut; if breadth is
as cheap as the matrix predicts, the owner may at that point direct a
hardening rider as a separate track (not assumed here).

### Track 0a — ADR-0037 conditional multi-dependency prerequisite — planned

**Goal.** Reimplement ADR-0037's generic
`conditional_dependency_set` evaluator-node contract in the production rule
language, so a condition can activate several factual references, report all
and only the absent active members in one durable non-publication walk, and
pin every evaluated input through the existing derivation edges. This is a
prerequisite to D2 adoption, not D2 implementation.

**Boundary.** This track does not add the QDCG worksheet, declared-absence
fact types, dividend content, Schedule B behavior, a tax-specific missing-list
path, a UI aggregation rule, or a third currency edge. It does not reopen
D1/D3 or change existing `rule-artifact.v1`/`v2` citizens. It introduces no
real-workspace access, personal data, or live-run attestation.

**Inputs.** ADR-0037 and its cited CMDN evidence; the closed
`rule-artifact.v2` language and schema loader; evaluator access logging and
the two existing runners; `derivation-record.v2` and `npe-walk.v1`; and the
authoritative-fact entrypoint `live_coordinate_run`. The existing
multi-entry `missing` arrays are the presumed record and NPE surface; changing
either schema is permitted only if implementation demonstrates that it cannot
represent the ordered list faithfully.

**Outputs and execution order.**

1. Publish `rule-artifact.v3` with `conditional_dependency_set`: one declared
   condition expression and a non-empty ordered `members` array whose entries
   are `ref` expressions only. Commit a hand-written, fully resolved synthetic
   positive rule artifact alongside the schema, plus schema-validation
   negatives for an empty member array, a non-`ref` member, and malformed
   condition/member shapes. The positive is the Payload Instantiation Gate
   evidence: it names every required rule field and every new expression field
   concretely, and cites the already-committed referenced-citizen examples
   rather than leaving a payload implied.
2. Implement the node in the shared evaluator. It evaluates the condition
   first; a false condition succeeds without reading, naming, or pinning a
   member. A true condition evaluates every member exactly once, accumulates
   `DEPENDENCY_ABSENT` results in declared member order, and propagates any
   non-absence failure normally. The primary runner and reference runner must
   both admit the new version through their ordinary schema/validation path;
   no runner-private rule identifier or tax/form branch is allowed.
3. Thread the result through the existing blocked disposition, record, and
   NPE walker. The durable record and walk must preserve all and only the
   accumulated absent members in declared order; a present member never enters
   the list. Published results pin the evaluated condition and every active
   member via the existing access log and derivation edges. Inactive members
   produce neither access-log entry nor pin. If the current record/NPE schemas
   prove sufficient, retain their versions and cover the behavior with tests;
   a required schema version is a separately explained migration in the track
   review, not an implicit shape change.
4. Add one fully synthetic coordinator-from-facts fixture family and executed
   goldens covering the six CMDN paper cases: inactive/no members,
   active/all present, active/two absent, active/one absent, the contribution
   and member-supersession lifecycle, and the no-reach-around mutation. The
   goldens must enter through `live_coordinate_run` from an authoritative act
   log, not a downstream `RunContext` shortcut.

**Verification.** The focused schema, evaluator/runner, record, NPE,
portability, and live-coordinator tests must cover the four output stages
above. The coordinator fixtures assert the complete ordered missing list in
the completed record and NPE walk; inactive isolation; active publication
pins; member and condition supersession displacement through the existing
two-edge model; primary/reference byte equality; and rejection of a mutation
that omits an active-member pin or tries to obtain a missing list outside the
declared node. Before review and merge, run the full `.venv/bin/python3 -m
unittest`, `.venv/bin/python3 -m mypy`, `.venv/bin/python3
tools/governance_lint.py`, and `.venv/bin/python3 tools/envelope_scan.py
--verify`. The authoritative-surface golden class is mandatory evidence; a
green unit suite without it is insufficient.

**Migration risk and data safety.** Existing rule artifacts stay historical;
only new v3 corpus and new synthetic goldens are added. No existing golden is
regenerated unless this new language contract demonstrably changes it. All
identifiers, actors, facts, statement shapes, and values are manufactured
`demo-*` data; the safety scan must cover every new fixture and generated
golden, with no local workspace path or real-run detail committed.

**Execution and review gate.** This is one integrated, short-lived per-track
branch and review unit under ADR-0030: schema/record evidence precedes
evaluator/explanation work, which precedes coordinator goldens, but the track
lands only when the complete contract is verified. It has no parallel-work
manifest because all stages change the same language, evaluator, record, and
canonical golden surfaces. Implementation and every reviewer dispatch remain
separately owner-authorized under ADR-0034; this planning approval authorizes
neither a dispatch nor D2 adoption.

### Track 1 — Schema citizens

Schema/contract citizens from the ratified ADRs (statement instance, family,
composition, attachment disposition), with positive examples, named
negatives, registry rows, and schema-validation tests. No runtime behavior.

### Track 2 — Composition and conditional machinery

3a/3b composition behavior, line-9 content extension, the Schedule B
existence conditional and its trace, over synthetic fixtures. Charter names
its authoritative-surface golden class per the Verification section.

### Track 3 — Line 16 under D2

The ratified line-16 shape implemented with honest blocking; goldens for
qualified-present and qualified-absent paths from the authoritative surface.

### Track 4 — 1099-DIV closure content and live integration

Closure-mapping content (ADR-0014/0017 pattern), live-run harness extension,
the owner's real run, attestation recorded.

### Track 5 — Completion

Matrix, phase-state, retrospective, deferral ledger; itself reviewed and
merged as a records track.

## Principles touched (foreclosure clause)

- **Honest blocking:** a return that requires Schedule B and cannot complete
  it, or a line 16 the ratified shape cannot certify, blocks with a walkable
  explanation — never a silently ordinary-bracketed tax or a missing
  attachment.
- **Trace over answer:** the attachment disposition must be *walkable* — the
  $1,500 conditional's inputs, threshold, and outcome are explanation
  content, not an opaque boolean.
- **Dependency-form completeness (owner-ratified at plan stage,
  2026-07-18):** a form this milestone's return depends on is either fully
  in scope or an explicit prerequisite track — the milestone may not ship an
  attachment that is *structurally* born blocked (blocked because scope
  excluded content the form requires). Honest blocking remains for *factual*
  incompleteness (the user has not yet contributed an answer), never for
  designed-in incapacity. This principle binds future milestone plans that
  introduce attachments.
- **Schema-as-canon:** the attachment disposition is a new noun and gets a
  schema like every citizen; no attachment exists outside its schema.
- **Runs consume facts, not inputs; the user controls the context:**
  unchanged and binding on all new machinery.
- Exceptions auto-escalate to Tier 3 per the standing protocol.
