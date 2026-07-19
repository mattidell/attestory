# Adversary Review R1 — QDCG Worksheet and Declared Absence (D2)

## Scope, independent-context seal, attack surface, stop conditions

**Seat.** Adversary, High tier, independent context. Advisory only; foreman
triages; owner disposes. I authored none of the plan or builder artifacts.

**Read (authorized).**
`docs/phase-state.md`;
`docs/prototypes/qdcg-worksheet/plan.md`;
`docs/prototypes/qdcg-worksheet/it1/design.md` +
`docs/prototypes/qdcg-worksheet/examination-it1.md` (incumbent);
`docs/prototypes/qdcg-worksheet/it2/design.md` +
`docs/prototypes/qdcg-worksheet/examination-it2.md` (clean-room rival);
`docs/governance/` (constitution, principles, ontology, engineering-constraints,
commentary, README — not other reviewers);
ADRs named by the plan and consumed by the designs:
0006, 0010, 0013, 0024, 0025, 0030, 0031, 0032, 0035, 0036;
committed package surface at HEAD for this review:
`packages/derivation/evaluator.py`, `runner.py`, `projection.py`,
`package_validation.py`, `explanation.py`,
`packages/kernel/contribution.py`,
`packages/schemas/derivation/rule-artifact.v2.schema.json`,
`artifact-package.v2.schema.json`, `derivation-record.v2.schema.json`,
`npe-walk.v1.schema.json`,
`packages/content/tax/2025/rule.form1040-line16.json` (current line-16 rule).

**Independent-context seal.** I did **not** read
`docs/prototypes/qdcg-worksheet/reviews/governance-r1.md`, any synthesis,
evaluation analysis, or other D2 reviewer material. No such material entered
this review. (That governance file exists on disk; it was not opened.)

**Attack surface (plan Review measurements + Gate-5 decision-blocking set).**
- Publish line 16 over a contradiction in either temporal order **or** same-batch.
- Fail the qualified-zero reduction property (silent tax change on no-QD returns).
- Worksheet inputs reach box 2a / recorded-non-composable content directly.
- Superseded declaration leaves line 16 current (displacement failure).
- Missing declarations do not factually block when qualified dividends require them.
- Declaration presence confused with truthiness.
- Declared `"no"` accepted alongside a current capital-gain-distribution signal.
- Unpinned or non-citable worksheet step.
- Design claims the committed package, evaluator, or currency machinery cannot
  support (false capability claims).

**Stop conditions.** Synthetic data only. No production code or schema edits.
No git writes/commits. Scope ends when this file is complete.

**Verdict headline.** Neither builder opens a path that publishes line 16 over a
declaration↔box-2a contradiction **if** the named admission-locus interlock is
built as paper specifies (both orders + same-batch). Both ladders are expressible
in the committed closed op vocabulary, and both reduction algebras hold on the
papered Q=0 path. **it1 has one decision-blocking honesty/capability defect** on
the `"yes"` / out-of-scope path (claimed `DECLARATION_OUT_OF_SCOPE` blocked code
via guard-false is not what the committed runner records, and that code is not
in the closed disposition vocabulary). **it2 has one decision-blocking false
claim about committed package machinery** for dual producers (package does not
validate exhaustive/disjoint guards; `conflict_semantics.selected_producer` is
not a guard-driven selector — residual order-selection risk if guards ever both
hold). Several further non-blocking precision gaps affect pinning language,
always-on declaration demand (it1), certificate indirection (it2), and
not-yet-built ADR-0035 universe/admission surfaces. Proposition-level
sufficiency at Rung 1 is **not** uniformly as claimed in the examinations.

---

## Committed machinery anchors (shared)

| Claim surface | Evidence |
|---|---|
| Closed ops: `add`, `max`, `subtract`, `compare`, `all`/`any`/`not`, `choose`, `bracket_fold`, `round`, `ref`, `parameter`, `categorical_compare`, `category_literal`; **no bare `min` or multiply** | `rule-artifact.v2` `$defs.expr` oneOf; `evaluator.py:146–204` |
| `min(a,b)` = `choose`+`compare lte` **or** `a - max(0, a-b)` | `evaluator.py:169–171` (one branch); `152–153` (`max`) |
| `all` short-circuits on first falsy | Python `all` over a generator in `evaluator.py:160–161` |
| Requires-then-guard-then-value; missing → `DEPENDENCY_ABSENT` | `runner.py:314–318`, `336–351` |
| Guard false → **`inapplicable`**, not a blocked code | `runner.py:342–351` |
| Runtime pins from **access log**, not static rule `pins` array | `runner.py:251–290` (`pins_for`) |
| Derivation edges only `input`/`choice` pin ids | `projection.py:32–55`; ADR-0010 D4 |
| Disposition blocked codes (record) closed set | `derivation-record.v2.schema.json`: `DEPENDENCY_ABSENT`, `DEPENDENCY_INVALID`, `CATEGORICAL_DOMAIN_MISMATCH`, `SOURCE_SET_OPEN`, `VALUE_INVALID` — **no** `DECLARATION_OUT_OF_SCOPE` |
| NPE blocked codes same closed family | `npe-walk.v1.schema.json` |
| Package multi-producer: `conflict_semantics` = `{symbol, selected_producer}` only | `artifact-package.v2.schema.json`; `package_validation.py:417–420`, `646–649` — **no** guard exhaustiveness check |
| Runner multi-producer: first successful publish wins; later rules for same symbol → inapplicable | `runner.py:320–334` — does not read `selected_producer` |
| Contribution batch: sequential `apply_act` on tentative; failure raises, no completed batch | `packages/kernel/contribution.py:99–189` |
| Current line-16 content | `packages/content/tax/2025/rule.form1040-line16.json` — single ordinary `bracket_fold`+`round`, no declarations |
| ADR-0035 signal + universe guard + same-batch | Ratified contract + **production conditions** (not implemented as live tax-layer code in the packages tree reviewed) |
| ADR-0036 presence-not-truthiness / `{yes,no}` | Decision 4 + PC2 |

---

## Proposition-by-proposition

### D2-P1 — Declared-absence fact types / presence semantics

| Builder | Examination claim | Adversary sufficiency at Rung 1 |
|---|---|---|
| **it1** | Settled | **Insufficient as stated** — presence/missing path is sound; `"yes"` / out-of-scope path is not supportable as designed against committed disposition machinery (A1). |
| **it2** | Settled | **Sufficient with residual non-blocking gaps** — categorical assertions + certificate layer correctly separate presence from truthiness; walk naming depends on NPE child walk through certificates (A7). |

**Both survive truthiness attack on the assertion domain** if production carries ADR-0036 PC2 (reject boolean domains). Committed `package_validation.py` does **not** yet implement that reject for arbitrary assertion types — both designs correctly push it to production conditions, not “already enforced.”

**it1** binds worksheet eligibility to two `fact-type.v2` assertions with `{yes,no}`, no `optional_default`, `requires` both before value (`design.md` P1; case 3). That matches ADR-0036 presence-before-value and plan case 3.

**it2** adds certificate rules that publish only under `categorical_compare(..., no)` (`design.md:34–50`). Presence of the certificate symbol is completeness; `"no"` is not treated as absent. That is a valid pattern instantiation and is more careful about `runner.py:pins_for` (access log) than it1’s static-pin language (A5).

### D2-P2 — Ladder, reduction, supersession of line 16

| Builder | Examination claim | Adversary sufficiency at Rung 1 |
|---|---|---|
| **it1** | Settled | **Sufficient for expressibility + algebraic reduction** on the guarded `"no"`/`"no"` path; supersession posture is an authorized rivalry choice with product cost (A6). |
| **it2** | Settled | **Sufficient for expressibility + reduction** on Q=0; **insufficient as claimed** for “package-validated exclusive dual producers” (A2). Ladder itself is fine. |

**Expressibility (probe a — correctly not required).** Both construct `min` without a `min` opcode; preferential rates via single-band `bracket_fold` (canon multiplies at `evaluator.py:260–275`). Parameters are versioned citizens. **No unpinned arithmetic-in-prose step** on the papered ladders once content is rule-artifact trees citing those parameters.

**Reduction algebra.**
- **it1** (`design.md:151–168`): Q=CG=0 ⇒ pref=0 ⇒ ordinary-portion=T ⇒ worksheet-sum=OrdTax(T)=full ordinary ⇒ min identity. Holds.
- **it2** (`design.md:101–107`): Q=0 ⇒ O=T, P=0 ⇒ all preferential slices 0 ⇒ candidate=ordinary_all; selector also takes ordinary v2. Holds by algebra **and** by selected content identity.

**Supersession posture (authorized rivalry, plan Gate 0 / case 2).**
- **it1:** one v2 worksheet rule for **all** returns; unique symbol ownership (ADR-0006 D7). Justified against dual-path drift. **Cost:** every return that needs line 16 must contribute both declarations even when Q=0 (A6).
- **it2:** two rules, guards `Q==0` vs `Q>0` (+ certificates), conflict_semantics. Avoids irrelevant declarations when Q=0. **Defect:** overclaims what package/runner guarantee (A2).

### D2-P3 — Bidirectional contradiction (declaration `"no"` ↔ box-2a signal)

| Builder | Examination claim | Adversary sufficiency at Rung 1 |
|---|---|---|
| **it1** | Settled | **Sufficient at paper** for the interlock shape (admission-locus, both orders + same-batch), **provided** Track 2 builds the check; no both-current state by construction if so. |
| **it2** | Settled (with named production contract) | **Sufficient at paper** — clearer schema delta (`admission-constraint.v1`), same locus; honest that it is not implemented. |

Neither design lets the worksheet **read** box 2a (plan case 6 / attack “reach-around”). Both keep the signal on the admission side only. That matches ADR-0035’s feed-for-D2 posture and the universe guard production condition.

**Committed contribution machinery today** is sequential tentative apply (`contribution.py`) without a dividends admission-constraint citizen. Same-batch safety is a **named production kill-test** (ADR-0035 lesson; both designs). Paper is allowed to stop here (plan Gate 2) only if the mechanism is fully specified — both specify post-validation / pre-mutation rejection and fail-closed batches. **I do not treat “not implemented yet” as a design failure**; I treat underspecified rollback or order loopholes as failures. Neither leaves an intentional both-current window on paper.

---

## Case-by-case (Gate-2 synthetic cases)

### Case 1 — Worksheet positive (supporting)

| | it1 | it2 |
|---|---|---|
| Ladder walk | Full step table (`design.md:119–139`, case 1) with parameters cited | Numeric demo walk (`design.md:111–119`): 8,410 < 8,500 — arithmetic checked against stated bands |
| Pins | Claims 3a, declarations, parameters | Claims 3a, certificates/declarations, parameters, op-semantics |
| Attack: non-citable step | Survives if intermediate rules are real `rule-artifact.v2` members as asserted | Survives |
| Attack: reduction not required here | N/A | N/A |

**Pass (both) at Rung 1 paper**, subject to content authoring.

### Case 2 — Reduction (mandatory)

| | it1 | it2 |
|---|---|---|
| Algebra | Holds | Holds |
| Supersession posture | One rule; requires declarations even at Q=0 to *run* the identity | Ordinary v2 at Q=0 without CG declarations |
| Attack: silent tax change on no-QD | **Algebraically no** when rule runs under `"no"`/`"no"` | **No** — ordinary content reused |
| Residual | Forces new assertions on all returns (A6) — product, not algebraic failure | Dual-rule overclaim (A2) — not a reduction failure if guards hold |

**Algebra: pass both.** Posture: rivalry, not a shared defect.

### Case 3 — Missing declarations block when Q>0 (mandatory)

| | it1 | it2 |
|---|---|---|
| Mechanism | Final rule `requires` both assertions → `DEPENDENCY_ABSENT` before value (`runner.py:314–318`) | Certificate rules require assertions; QDCG requires certificates → block chain |
| Names both contributable facts | Directly in `missing` if requires lists both assertion symbols | Directly only if requires/NPE surface assertion symbols; default QDCG `missing` names **certificate** symbols first (A7) |
| Attack: implied zero | Survives | Survives (no certificate ⇒ no publish) |
| Attack: presence vs truthiness | Survives (requires is presence) | Survives |

**Pass both on the load-bearing property (no publish / no implied zero).** it2’s walk quality is weaker unless certificate rules sit in the NPE producer graph (non-blocking if Track 3 wires requires/walk carefully).

### Case 4 — Contradiction both orders + same-batch (mandatory)

| Order | it1 | it2 |
|---|---|---|
| (a) `"no"` then box 2a | Admission rejects statement/signal (`design.md:195–196`) | Same via constraint (`design.md:170`) |
| (b) box 2a then `"no"` | Admission rejects declaration (`design.md:196–197`) | Same (`design.md:171`) |
| (c) same batch | Staged pre-mutation pair check (`design.md:197–198`) | Order-independent preflight (`design.md:172`) |
| Line 16 over contradiction | No both-current state ⇒ cannot publish over it | Same |
| Declared `"no"` + current signal | Rejected by invariant | Rejected by predicate |

**Pass both at paper.** Production must kill-test against sequential batch apply so intermediate act application cannot be committed alone (both claim fail-closed batches — aligned with `contribution.py` failure path).

### Case 5 — Declared-zero publishes + displacement edge

| | it1 | it2 |
|---|---|---|
| Publish under `"no"`/`"no"` | Guard `all(categorical_compare…)` + value ladder | Certificates true + QDCG guard |
| Pin path for supersession | Guard `ref`s declarations when publishing → `input` pins via access log | Declaration → certificate → worksheet two-hop pins (explicitly designed for `pins_for`) |
| Attack: superseded leaves line 16 current | Survives **if** pins are access-log `input` pins (ADR-0010 D4; `projection.py:44–55`) | Survives by construction of two-hop pins |
| Attack: static rule `pins` alone | **it1 prose over-relies on listing pins** (A5) — mechanism that actually works is the guard/value access path | Correctly denies that `requires` alone pins |

**Pass both** on displacement **when** the published finding’s pins include the declaration (or certificate) finding ids. it2’s account matches committed runner better.

### Case 6 — No reach-around (mandatory)

| | it1 | it2 |
|---|---|---|
| Worksheet bindings | T, Q, FS, rounding, declarations, QDCG params, ordinary brackets only | Same exclusion of signal / recorded-boxes / box 2a collect |
| Unrepresentable vs untested | Claims ADR-0035 runtime universe guard + package validation (PC — not live code today) | Same |
| Only route from real box 2a | P3 hard error | P3 hard error |

**Pass both at paper.** The universe guard is an **owed production condition** (ADR-0035), not a currently greppable reject in `package_validation.py` beyond family `collect` wiring. Designs must not be read as “HEAD already rejects.” Examination-it1’s “unrepresentable under ADR-0035 universe guard” is slightly over-strong for *today’s* package validator; still acceptable as a production-bound claim.

---

## Findings (classified)

### A1 — it1 `"yes"` / out-of-scope path claims a blocked code the runner cannot emit
**Decision-blocking — it1 only (P1 honesty / committed capability).**

**Design claim.** `it1/design.md:59–61`, `141–146`: if either declaration is `"yes"`, line 16 blocks with walkable **`DECLARATION_OUT_OF_SCOPE`** “via guard false / blocked branch.” Examination treats P1 as settled including presence-not-truthiness production notes, but the out-of-scope path is part of the spine (honest incompleteness, not silent ordinary tax).

**Committed behavior.**
1. Guard false → disposition **`inapplicable`** with `guard_result: false` and **no** `code` (`runner.py:342–351`).
2. Closed blocked-code enums on `derivation-record.v2` and `npe-walk.v1` **do not include** `DECLARATION_OUT_OF_SCOPE`.
3. There is no evaluator op that “blocks with a custom code” from a true guard branch; `EvalBlocked` categories are the fixed set in `evaluator.py:24–28`.

**Attack result.** A taxpayer who correctly answers `"yes"` (Schedule D / real CG path needed) does **not** get the walkable out-of-scope block it1 promises. They get sole-producer **inapplicable** / non-publication without that code — a weaker, easier-to-misread account, and a **false claim that committed disposition machinery supports the named code**. Plan Gate-5 cares about declaration presence/blocking honesty; Article 6 (never wrong, only incomplete) wants incompleteness *shown*. This is not cured by algebra on the `"no"` path.

**Repair direction (for foreman, not built here).** Either: (i) version the disposition/NPE enums and emit a real **blocked** disposition with a named code when answers are present-but-out-of-scope (content-level structure, not guard-false alone), or (ii) drop the `DECLARATION_OUT_OF_SCOPE` claim and specify the committed `inapplicable`/alternate-producer story honestly. it2’s `"yes"` → no certificate → `DEPENDENCY_ABSENT` is also imperfect copy but **uses a committed code**.

### A2 — it2 dual line-16 producers: package does not validate exclusive guards; runner is order-first
**Decision-blocking — it2 only (false claim about committed package/runner; residual policy selection risk).**

**Design claim.** `it2/design.md:58–74`: two rules publish the same symbol; “the package declares conflict semantics … and **validates the guards as exhaustive and disjoint**”; “the runner’s published-output protection therefore **never selects tax policy by traversal order**.”

**Committed behavior.**
1. `conflict_semantics` schema is only `{symbol, selected_producer}` (`artifact-package.v2.schema.json`).
2. `package_validation.py` checks presence of a conflict entry / selected member id for multi-producers — **not** guard expressions, exhaustiveness, or disjointness (`:417–420`, `:646–649`).
3. `runner.py:320–334`: if the symbol is already in `self.symbols`, later rules are **inapplicable** (first successful publish wins). The runner **does not consult** `selected_producer`.

**Attack result.** As long as guards are truly `Q==0` vs `Q>0` (and Q is always present as a non-negative admitted amount), runtime is exclusive and case 2/3 hold. The design **overclaims machinery support** (plan attack: “design claim that the committed package … cannot support” / false capability). If a content bug ever makes both guards true, **traversal order selects the tax number** — exactly the anti-wizard / Article 11 risk dual-path designs must not paper over with a non-existent validator.

**Repair direction.** State exclusive selection as a **content invariant + kill-tests** (or a real package check to be built), not as an existing validator feature; do not claim order-independence beyond mutually exclusive guards.

### A3 — Contradiction interlock: both designs adequate on paper; neither is “already structural” at HEAD
**Non-blocking (production obligation) — both.**

Both specify admission-locus mutual exclusion before mutation, both orders, same-batch, fail-closed contribution (it1 table `design.md:193–198`; it2 table `design.md:168–173`). That is the Gate-6 floor mechanism. HEAD has contribution batching but **not** the D2 predicate / `admission-constraint.v1` / ADR-0035 signal raise as live code paths in the packages reviewed. Examinations that say “settled” must be read as **settled design**, not settled implementation — it2’s examination is clearer (“named production contract”).

### A4 — Reach-around / recorded-non-composable
**Non-blocking residual — both (wording).**

Neither worksheet expression tree includes box 2a or `CAPITAL_GAIN_DISTRIBUTION_RECORDED` as a rule input. Good against plan case 6. Claims that package validation **already** makes such a member unrepresentable overstate ADR-0035 PC status (A3’s sibling). Bind the claim as production PC + content discipline.

### A5 — it1 “unconditional input pins” vs access-log pinning
**Non-blocking imprecision — it1.**

`it1/design.md:51–55` ties unconditional pinning to listing `input` pins on the rule (and cites projection edges). Committed `pins_for` builds edges from **evaluated** `access.refs` / collects / etc. (`runner.py:251–290`), not from the static `pins` array on `rule.form1040-line16.json`. it2 states this correctly (`design.md:48–50`).

**Material risk is limited:** it1’s final guard uses `categorical_compare` on both declarations, so a **published** line-16 finding does pin them, and supersession displaces (case 5). The failure mode is design/reviewer confusion (“static pins suffice”) and any future rewrite that drops guard refs while keeping `requires` only — `requires` alone does not create ADR-0010 edges on a successful publish path’s dependents in the way the design rhetoric suggests.

### A6 — it1 universal worksheet forces declarations on Q=0 returns
**Non-blocking product consequence — it1 (authorized rivalry; flag for triage).**

Plan case 3 mandates missing-declaration blocking when **qualified > 0**. Case 2 mandates reduction at Q=0 without requiring “declarations absent still publish.” it1’s single rule `requires` both declarations for all returns (`design.md:141–144`). A wages-and-interest return that today publishes line 16 from `rule.form1040-line16.json` with no CG assertions would **block** after supersession until two new assertions are contributed — even though algebra would match ordinary tax. it2’s conditional posture avoids that. Not a reduction-algebra bug; it is a material honest-blocking vs anti-wizard tension the examination understates when it marks P2 fully settled without product-cost callout.

### A7 — it2 certificate indirection vs “walk naming both contributable facts”
**Non-blocking — it2.**

Case 3 claims the walk names the two taxpayer questions (`design.md:125–129`). NPE for a blocked QDCG rule puts certificate symbols in `unmet_references` first (`explanation.py:249–289`); children recurse only for deps that are **derived** symbols (`:279–281`). If certificates are package rules, children can surface declaration requires one level down; if not carefully wired, the user-facing account names certificates / symbols rather than the two contributable assertion types. Kill-test the walk in Track 3.

### A8 — `admission-constraint.v1` not on `admitted_schemas` enum
**Non-blocking — it2 (expected schema delta).**

`artifact-package.v2` `admitted_schemas` enum has no `admission-constraint.v1`. Paper may propose versioned schema expansion; Track 1 must admit the citizen. Not a silent dependency on unstated magic if production obligations list it (they do, `design.md:189–198`).

### A9 — Intermediate ladder rules (it1) bind CG as literal 0 only under final guard
**Non-blocking — it1.**

Preferential base is “literal 0 under `"no"`/`"no"`” at the final rule (`design.md:148–149`). Intermediate symbols could still be authored to always add Q+0 without re-checking declarations; line 16 still cannot publish without the final guard/`requires`. Defense-in-depth for content authoring, not a case-6 hole.

### A10 — Preferential-rate formula fidelity (IRS worksheet detail)
**Non-blocking / deferred — both (plan Gate 5).**

Plan defers “tax-table-vs-schedule fidelity questions in the ordinary sub-computation” and treats the ladder as preferential split + comparison. it1 and it2 use related but not identical 15% room constructions. Not decision-blocking for this paper round; do not ratify numeric demo brackets as legal authority (both label demo/synthetic).

---

## Attack matrix (plan measurements)

| Attack | it1 | it2 |
|---|---|---|
| Publish line 16 over contradiction (either order) | **Blocked on paper** by admission locus | **Blocked on paper** by admission constraint |
| Same-batch both current | **Blocked on paper** (staged pair) | **Blocked on paper** (order-independent preflight) |
| Reduction fails (Q=0 tax silently changes) | **Algebra holds** when rule runs | **Algebra + ordinary selector hold** |
| Worksheet reads box 2a / non-composable | **No** on paper | **No** on paper |
| Superseded declaration leaves line 16 current | **No** if access-log pins present | **No** (two-hop pins) |
| Missing decls when Q>0 still publish | **No** (`requires`) | **No** (certs/`requires`) |
| Presence confused with truthiness | **No** on assertions (categorical) | **No** on assertions; certs are explicit |
| `"no"` + current CG signal both current | **No** on paper | **No** on paper |
| Unpinned / non-citable ladder step | **No** if content matches tables | **No** if content matches tree |
| False claim committed machinery supports X | **Yes — A1** (`DECLARATION_OUT_OF_SCOPE` / guard-false) | **Yes — A2** (guard validation / order-free dual publish) |

---

## Examination verdicts (challenged)

| Proposition | it1 examination | Adversary | it2 examination | Adversary |
|---|---|---|---|---|
| D2-P1 | settled Rung 1 | **Not settled** — A1 | settled Rung 1 | **Settled** with A7 residual |
| D2-P2 | settled Rung 1 | **Settled** for ladder/reduction; posture rivalry + A6 | settled Rung 1 | **Ladder/reduction settled**; exclusive dual-producer **claim** not settled (A2) |
| D2-P3 | settled Rung 1 | **Settled at paper** (production still owed) | settled Rung 1 + named PC | **Settled at paper** (agree) |

Mandatory cases 2, 3, 4, 6: **load-bearing properties hold on paper for both**, except that it1’s broader P1 out-of-scope story (adjacent to case 3/5 honesty) fails A1, and it2’s packaging story around case 2’s dual rules fails A2.

---

## Gate-6 floor

| Floor element | it1 | it2 |
|---|---|---|
| Citable ladder + algebraic reduction | Met | Met |
| CG inputs only via declared-absence presence semantics | Met (`"no"`/`"no"` bind; no box 2a read) | Met (certificates from `"no"` only) |
| Missing declarations block when QD require them | Met | Met |
| Bidirectional + same-batch contradiction, no both-current | Met on paper | Met on paper |

Gate-6 can be met by **either** design after A1/A2 repairs (or by synthesis that takes it2’s interlock clarity + it1’s single-owner posture, etc.). **As written, examinations over-declare full settlement.**

---

## What is not decision-blocking (explicit)

- Choosing one universal worksheet vs conditional ordinary/QDCG pair (plan-authorized rivalry), aside from A2’s false machinery claim and A6’s product cost.
- Demo breakpoint/rate numbers.
- Absence of live ADR-0035/D2 admission code at HEAD (production tracks).
- `SOURCE_SET_UNCLOSED` vs `SOURCE_SET_OPEN` vocabulary debt (ADR-0036 PC3 — out of D2 design scope).
- Schedule D / real CG computation (out of scope by plan).

---

## Synthetic data note

All amounts, statuses, and identifiers referenced from the designs (e.g. `demo-ti-50000`, `demo-q-600`, `demo-single`, brackets 10%/20%/30%) are synthetic as required by the plan and ADR-0031. No real workspace facts were used.

---

## Stop

Review complete. No other files written; no production code or schemas modified; no git writes.
