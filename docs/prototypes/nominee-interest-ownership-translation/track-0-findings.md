# Track 0 findings — T0-A (semantics); T0-B (traces)

Track 0 record for the Nominee Interest Ownership Translation milestone. All three checkpoints — T0-A semantics, T0-B traces, T0-C synthesis — are complete. Retained as the evidence required to recover the milestone's accepted dispositions.

| | |
| --- | --- |
| Seat | Builder, Track 0 checkpoint T0-A |
| Source ref | `HEAD` at pickup = `fa2d4fcf233fc6879f96f48a6f7c7519723ad731` |
| Plan blob (authoritative pin) | the milestone plan |
| Branch | `milestone/nominee-interest-ownership-translation` |
| Evidence rung | PAPER. No prototype code, tests, or experiments. Quotes are from committed artifacts. |
| Writable path | this file only |

---

## 1. Identity and inputs reused

**This checkpoint reuses Gate P2's tax and artifact map as established input.** It does not re-verify A1–A4, D1, H1, bounded Branch B, the N8 compatibility surfaces, or the N9b circumstance split. It does not retrieve tax sources.

Closed inputs, not re-derived: P1-D1 (explicit "no" is transient; N1a and N1b converge in durable state); the three reporting formulations remain authority-indexed and unreconciled; R-A vs R-B is deferred; attribution stays on the act; the attributed ordinary statement is bounded evidence for a supported tax determination and does not "establish belonging"; N10/N12 non-inference; durable derived-publication persistence is orthogonal — this checkpoint observes run-local `RunResult` provenance only.

Synthetic identities, if named, use `demo.*` / `demo-*` only.

---

## 2. Ordinary-question / routing box

This is a **product property**, not interface copy. No wording, screens, or ordering is selected.

**Elicit circumstance before an allocation is captured.** An affirmative answer to the gating ownership question is not yet a nominee circumstance. Case N9b is the falsifying control: a bond buyer reimbursing a seller for accrued interest the form will report to them can answer the gating question with almost the same ordinary sentence as N2. A bare who/how-much captured at that point would manufacture a nominee reduction out of a purchase reimbursement.

After an affirmative gating answer, intake must elicit enough ordinary context to route to one of:

| Route | Ordinary circumstance | Product consequence |
| --- | --- | --- |
| Nominee path (this milestone) | Interest received or held for another owner | Only then may an allocation (who, how much of the reported interest) be captured. The product, not the user, applies "Nominee Distribution." |
| Accrued-interest path (already accepted) | Bond purchase between interest dates; buyer reimbursed the seller for pre-acquisition accrual | Route **away from** nominee treatment. Derive **no** nominee reduction. Hand the circumstance to the accrued-interest translation. |
| Other / uncertain | Neither of the above is established | Qualify or follow up. Do not default into nominee allocation or accrued treatment. |

**Never ask the user to choose a tax label.** The user is not asked for "nominee distribution," "accrued interest," a Schedule B line, or a tax result. The product classifies.

**Asymmetry of "no" (P1-D1, closed).** Silence is never attributed as a denial. During the active interaction the product may acknowledge a just-given "no." After the interaction, "no" supplies no durable workspace claim. Durable state converges with N1a. Later explanations may say only that **no nominee allocation is recorded**.

**N9a remains a separate wrong-problem control** (erroneous form amount → document correction, no nominee reduction). It is not the N9b split.

Established P2 ordinary-fact split (reused, not re-researched): nominee vs N9b differ in who the other person is, whether acquisition of the instrument is the distinguishing event, who is taxed on that slice, and companion consequence (possible information return vs basis reduction). The committed accrued mapper (`packages/tax/obligation_acquisition_mapping.py`) is one circumstance only and fails closed on unrecognized fields; the legacy nominee type has no acquisition date, seller, basis publication, or report association.

---

## 3. Attribution-exposure paper trace

One ordinary allocation statement (illustrative: after N9b routing, the user states that `$450` of a `$1,200` box-1 report is another person's). Four layers.

### 3.1 Finding — the answer, and its finding id

`finding.v2` carries `schema`, `id`, `fact_id`, `value`, `basis`, `evidence_ids`, and optionally `capture`, `pins`, `contribution_id`. Required fields do **not** include `actor` or `at`.

Quoted from `packages/schemas/kernel/finding.v2.schema.json` (required list, lines 78–85):

```json
"required": [
  "schema",
  "id",
  "fact_id",
  "value",
  "basis",
  "evidence_ids"
]
```

`additionalProperties` is `false`. The finding is the answer (`value` against `fact_id`) and its finding id (`id`). It is not the attribution.

The assertion payload wraps that finding and nothing else. Quoted from `packages/schemas/kernel/act-assertion.v2.schema.json` (lines 6–16):

```json
"properties": {
  "finding": {
    "type": "object",
    "properties": { "schema": { "const": "finding.v2" } },
    "required": ["schema"]
  }
},
"required": ["finding"],
"additionalProperties": false
```

### 3.2 Enclosing assertion act — actor, at, committed_against

Attribution lives on the `act.v1` envelope. Quoted from `packages/schemas/kernel/act.v1.schema.json` (lines 8–19):

```json
"act_id": { "type": "string", "minLength": 1 },
"kind": { "type": "string", "pattern": "^[a-z][a-z-]*[a-z]$" },
"actor": { "type": "string", "minLength": 1 },
"at": {
  "type": "string",
  "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(Z|[+-][0-9]{2}:[0-9]{2})$"
},
"committed_against": { "type": "integer", "minimum": 0 },
"payload": { "type": "object" }
```

Required: `schema`, `act_id`, `kind`, `actor`, `at`, `committed_against`, `payload`. `committed_against` is the workspace revision the act commits against.

The kernel projection **drops the envelope**. `packages/kernel/findings.py` `apply_act` (lines 1040–1052) dispatches kernel acts as `_APPLIERS[kind](state, act["payload"], registry)` — payload only. `apply_assertion` (lines 619–642) stores `findings[finding["id"]] = finding`. `FindingState.findings` therefore holds the answer and finding id, not `actor` / `at` / `committed_against`.

The act log retains the full envelope (`packages/kernel/act_log.py` `_parse_committed_line` validates the envelope then the payload). Given a finding id, the asserting act is recoverable by reading the log for `kind == "assertion"` whose `payload.finding.id` equals that id, then reading that act's `actor`, `at`, and `committed_against`.

### 3.3 Derived `RunResult` — input pin to that finding id

Marshalling projects current findings into `InputFinding(symbol, value, finding_id, role)` (`packages/derivation/runner.py` lines 52–59; constructed at `packages/derivation/marshal.py` lines 296–302 and 376–382). There is no `actor` field.

The runner records that finding id on the derived finding's pins. `packages/derivation/runner.py` `_Run.__init__` (lines 251–260) maps each input to `self.symbol_pin[i.symbol] = (i.finding_id, "v1", i.role, provenance)`. `dependency_pins_for_access` (lines 370–377 for refs; 378–385 for collects) emits `{role, id: finding_id, version}` (and `origin` on v2 input pins). `pins_for` (lines 455–471) composes those with the rule, citation, adoption, and governance pins.

`RunResult` (`packages/derivation/runner.py` lines 125–137) carries `publications` (each a `Publication` with `act` payload and `finding`). The derived finding shape is `derived-finding.v2`: `symbol`, `value`, `version`, `pins`; no actor (`packages/schemas/derivation/derived-finding.v2.schema.json`). An input pin names the ordinary finding id. It does not name the assertion act.

`append_publications` exists and writes `actor`/`at` onto a `derived-publication` envelope (`packages/derivation/runner.py` lines 1729–1749). That envelope's actor is the persistence-boundary actor of the *publication*, not the ordinary-statement asserting actor. Production does not call it (P3-D1, closed). This checkpoint observes run-local `RunResult` pins only.

### 3.4 Current explanation projection — what a reader is shown

`ExplanationNode` (`packages/derivation/explanation.py` lines 22–31):

```python
class ExplanationNode:
    finding_id: str
    role: str
    kind: str
    symbol: str | None
    value: str | None
    version: str
    produced_by: dict[str, Any] | None
    children: tuple["ExplanationNode", ...]
```

`explain()` walks pins. A human-input leaf (lines 111–123) copies `finding_id`, `role`, `kind` from `inputs` metadata `role`, `symbol`, `value`, and hard-codes `version="v1"`. The `inputs` index built by `packages/derivation/runners/derive.py` (lines 174–180) is `{finding_id: {symbol, value, role}}`. No actor, no timestamp.

`render_text` (lines 167–176) prints role, symbol or finding id, value, and producing rule id.

The production reader-facing projector does not call `explain()`. `packages/derivation/presentation_projection.py` `_citation_site` (lines 217–218) emits `{siteId, pinId, pinVersion, context}` where `pinId` is the leaf finding id. `_evidence_label` (lines 201–214) is the finding's current evidence label, or none. `_resolve_field_row` (lines 262–274) joins those into `citationGroups`. No actor, no `at`.

`walk_npe` (`explanation.py` lines 264–270) records `finding_id` on a published node and delegates lineage to `explain()`. Its loss is **stronger** than the other two. `explain()` interprets the pins; `walk_npe` then iterates `exp_node.children` and retains **only children whose symbol is in `derived_symbols`** — the set of symbols published by rules (`explanation.py` line 213, filter at line 261). That filter **drops direct ordinary-input leaves entirely**, rather than merely stripping actor and time from them, and the published `finding_id` identifies the **derived** finding.

`live_coordinate_run` exposes in-memory `publications` so a caller can walk `explain()` without a `RunContext` shortcut (`packages/derivation/live.py` lines 57–64). That walk still cannot show actor/`at`, because neither the derived finding nor the explanation node carries them.

Root `explain(..., authorization=...)` may attach an `authorization` sibling (`explanation.py` lines 133–151): grant id and standing-authorization *status*. That is ADR-0069 workspace authorization, not the ordinary-statement asserting actor.

### 3.5 Consumer-by-consumer exposure

The three reader-facing consumers do **not** fail identically, and the
differences matter. Corrected per consumer:

| Consumer | What it retains for an ordinary input | Actor / time? |
| --- | --- | --- |
| `ExplanationNode` (`packages/derivation/explanation.py`) | **May retain the ordinary input finding id.** Its fields are `finding_id`, `role`, `kind`, `symbol`, `value`, `version`, `produced_by`, `children` | **No.** The module contains no `actor` reference at all |
| presentation `citationSites` (`packages/derivation/presentation_projection.py`) | **May retain the ordinary leaf `pinId`** | **No** |
| `walk_npe` (`npe-walk.v3`) | **Weakest of the three.** It retains only derived-symbol children — pins whose role is a rule role become `produced_by`, dependency roles recurse, and it **can drop direct ordinary-input leaves entirely**. Its published `finding_id` identifies the **derived** finding, not the ordinary assertion | **No** |

So the loss is graded, not uniform: two consumers keep an identifier that could
reach the assertion, while `walk_npe` may not retain the ordinary leaf at all
and names a derived finding instead.

### 3.6 Three-state determination

| Question | Result |
| --- | --- |
| Recoverable from underlying records? | **Yes.** The act-log envelope of the assertion act carries `actor`, `at`, and `committed_against`; the derived finding pins the finding id. Recoverability rests on the log, not on any projection |
| Available to the current explanation consumer? | **No** — for all three consumers above, by different routes |
| Exposing it to a reader? | **Requires a bounded explanation extension** |

**State that holds: attribution is recoverable but not currently exposed.**

**The missing product property**, stated without choosing how to supply it: a
reader shown a derived nominee determination cannot, from what the current
consumers emit, see **who supported the ordinary statement it rests on**. Plan
P-T1's failure condition names exactly this — a recoverable chain that a required
explanation surface cannot surface.

This checkpoint **does not select a projection, join, retention, or schema
design** for closing that gap, and does not decide which consumer should carry
it. It does not reopen durable publication, and it does not relocate attribution
into the finding — that placement stays closed.

---

## 4. Authority-lifecycle table

Columns are the `PROJECT_PLANNING.md` Track 0 Adversarial Closure Gate set. Storage identity is not authority scope.

**Non-claim state (not a row that asserts).** "No allocation recorded" (N1a, and N1b after the interaction) has **no user author**, does **not** assert taxpayer ownership of the reported amount, and **ends** when an affirmative allocation becomes current. It is the absence of a current allocation statement, not a recorded denial, and not a closed-empty ownership universe. **No absence declaration is manufactured for it.** Line 2b's closed-empty *box-1* or *legacy-nominee* closures are different objects (below); they close those families' own claims, they do not attest "the taxpayer owns the whole amount."

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| Payer report: current finding of `tax.us.2025.f1099int.box1-interest` | A particular payer statement reported a box-1 amount. Documentary evidence of what the payer reported. **Does not** say who economically owns any portion (P2 E17, reused). | That statement instance: payer + 1099-INT statement entity + tax year 2025 (`packages/content/tax/2025/f1099int.bundle.json` identity_keys). Not tax-year-only: two same-payer reports in one year are distinct (N11; ADR-0015). | The assertion (or contribution) that currently answers that fact; current evidence refs if documentary. | Same-identity amount correction (N6a: `$1,200`→`$1,000` on the same fact). Member withdrawal / successor statement identity (not instantiated in N1a–N12). Currency displacement of the pinned finding (ADR-0010 input pin). |
| Box-1 family closure: current `tax.us.2025.f1099int.b1.source-closure` true | Every furnished 1099-INT box-1 statement item for 2025 is recorded as of the named family-horizon (bundle title, same file). Authorizes the box-1 subtotal only, including subtotal zero — not line 2b completeness, not ownership of any remainder (ADR-0016 Decision 5). | Family `tax.us.2025.f1099int.b1` on the attested family-horizon, tax year 2025. | Current-literal-true admission (`closure-mapping` pattern as P2 E19 for the sibling nominee mapping). Horizon currentness (ADR-0017). | Member-transition adding or removing a box-1 member advances the horizon and stale-closes this attestation (ADR-0023 Decision 1). Correction of the boolean to false. Horizon succession without re-attestation. |
| Ordinary allocation statement (canonical type **not selected**; R-A/R-B deferred) | Attributed ordinary statement that a stated amount of interest reported in the taxpayer's name is a named other non-spouse person's, after N9b routing. Bounded evidence the product accepts to support applying the Schedule B classification. **Does not** establish belonging, nominee classification, or any reporting formulation (claim boundary, closed). | The allocation as currently asserted: one actual owner, the amount, and — at evaluation time — the specific report it is attached to (N11). Owner cardinality is per statement (N4); this row is one owner. Scope is **not** "the tax year" and **not** "all reports from this payer." | The enclosing assertion act (`actor`, `at`, `committed_against`). The current amount of the attached report, for supportability (not for the meaning of the statement). Independent of any payment/credit fact (N10). | Same-identity correction of the amount or owner (N7). Withdrawal / supersession of the finding. Supportability failure of the attached set (N5, N6b, N11b) does not rewrite the statement; it makes the *derived* reduction unusable. Routing that this was N9b would mean this statement should never have been captured as a nominee allocation. |
| Payment, credit, or setting-apart fact (no committed fact type) | Ordinary cash/account fact: whether the taxpayer paid, credited, or set the interest apart so the other person could draw it, including deemed-paid (P2 A3 / E9, reused). **Necessarily** required for the literal § 6049(a)(2) evaluation, whose second conjunct is about payments, and **also a dependency of any regulation-attributed statement that actually reads** payment, credit, setting-apart, collection, or intermediary facts. **Never** a gate or pin on the belonging-supported Schedule B reduction, and not a Schedule B condition. | That person, that interest so received, that calendar year — as far as the scenario states. Not inferred from the allocation (N10). Not a reporting-obligation finding. | Its own assertion act, when present. | Correction or withdrawal of that fact. Must **not** displace a belonging-supported reduction (P-T1a pin-set constraint). Absence is not a negative payment declaration. |
| Legacy nominee amount: current `tax.us.2025.scheduleb.adjustment.nominee.amount` | A nonnegative preclassified nominee-adjustment amount for one logical Schedule B adjustment instance. Establishes that a fact type can carry that number. **Does not** establish actual-owner identity, report association, allocation basis, or why the amount belongs elsewhere (P2 E18, reused). | That adjustment instance in tax year 2025 (`scheduleb-adjustment.nominee.bundle.json` identity_keys: tax-year literal + `tax.us.scheduleb-adjustment-instance`). Tax-year key is storage identity, not a claim that the proposition is year-scoped independently of family membership. | The assertion/member-transition that currently answers that fact. Family membership of `tax.us.2025.scheduleb.adjustment.nominee`. | Free same-identity correction (`supersession.policy: "free"`). Member withdrawal. **Not** silently converted into the ordinary allocation statement (N8; ADR-0072 posture as transfer question). |
| Legacy nominee family closure: current `….nominee.source-closure` true | Every contributed nominee-distribution amount within the bounded Schedule B interest-adjustment surface is recorded as a logical adjustment instance for 2025 (`family.scheduleb-adjustment.nominee.json` `closure_claim`). Authorizes `scheduleb-nominee-subtotal` only. Says nothing about other adjustment classes, total interest, or ownership. | Family `tax.us.2025.scheduleb.adjustment.nominee` on its current family-horizon, tax year 2025. | Current-literal-true admission (`closure-mapping.scheduleb-adjustment.nominee.json`). | Member-transition that changes membership (ADR-0023). Boolean correction. Horizon succession without re-attestation. Closed-empty true is **not** "no allocation recorded" as a user denial, and **not** an ordinary-allocation absence declaration. |
| Derived nominee-distribution reduction (run-local; no production type selected) | Supported Schedule B determination: amount allocated away from the taxpayer on the belonging-supported path, with provenance to the assertion, payer report, rule, and authority. Arithmetic remainder (share) is reported amount minus recorded reductions — **not** an ownership finding (plan N1a note). | The attached report's current amount and the current supportable allocation set against that report. Not the payment fact. Not a normalized reporting obligation. | Current allocation statement(s); current attached report amount; adopted rule; supportability verdict. Run-local `RunResult` publication (P3-D1). | Correction of allocation (N7) or report amount (N6a/N6b). Supportability failure: composing reductions retracted; dependent result blocks; never a negative remainder (P-T1b inherit). Stale run-local value is not reused: re-derive from current facts. |
| Authority-indexed reporting evaluation (not a single claim) | Per formulation, a record of which scenario facts are present or absent, and only the instruction or conclusion that authority expressly supports, attributed to that authority; otherwise qualify or defer. Applicability itself remains unresolved. | Each formulation's own authority (statute / form instruction / regulation). Not combined. Not ranked. | The facts **that particular attributed statement reads**: allocation facts always; the payment/credit fact **necessarily** for literal § 6049(a)(2); for a regulation-attributed statement, payment/credit/setting-apart/collection/intermediary facts **only where that statement relies on them**, and not where it is limited to the actually-owned-portion language. | Correction of the facts that formulation's own terms read. Correcting payment must not invent or suppress a belonging-supported reduction. Correcting allocation must not invent a normalized reporting obligation. |
| Pairing-scoped current-year adjustment subtotal (neighbor, accrued path) | Sum of pairing-scoped accrued current-year-adjustment findings; empty pairing set publishes 0 (`rule.interest.current-year-adjustment-subtotal.json` notes). Not a nominee family. | Accrued pairing publications in the run, grouped by associated report for aggregate supportability (ADR-0070). | ADR-0068 pairing; ADR-0070 verdicts; ADR-0071 pairing-scoped rules. | Accrued supportability block; pairing displacement; migration/coexistence rules (ADR-0072). N9b routes here rather than into a nominee allocation. |

No reused declaration is treated as proving the taxpayer owns an unreduced remainder.

---

## 5. Empty/nonempty authority matrix

### 5.1 Enumeration (read first; not assumed)

Committed source families inspected against this feature's consumers and the neighbors those consumers join.

**Direct consumers of this feature (legacy path, H1/H2 reused):**

- `tax.us.2025.scheduleb.adjustment.nominee` — member predicate `tax.us.2025.scheduleb.adjustment.nominee.amount`; authorizes `scheduleb-nominee-subtotal` (`family.scheduleb-adjustment.nominee.json`). Collected by `rule.scheduleb-adjustment.nominee-subtotal.json` (`collect` + `source_set` that family). Line 2b v6 `require_closed` on that family. Schedule B v5 adjustment row `nominee_distribution` `collect_members` on that family.

**Report family this feature allocates against:**

- `tax.us.2025.f1099int.b1` — member predicate `tax.us.2025.f1099int.box1-interest`; authorizes `b1-subtotal`. Line 2b v6 `require_closed`. Schedule B v5 Part I first `row_set`.

**Line 2b v6 `when` `require_closed` source_sets** (`rule.form1040-line2b.v6.json` lines 88–96), which gate the neighboring taxable-interest result even when nominee arithmetic is locally fine:

- `tax.us.2025.f1099int.b1`
- `tax.us.2025.f1099int.b3`
- `tax.us.2025.f1099oid.b1`
- `tax.us.2025.non-form-interest`
- `tax.us.2025.form1065-k1.box5`
- `tax.us.2025.f1099int.b10`
- `tax.us.2025.f1099oid.b5`
- `tax.us.2025.scheduleb.adjustment.nominee`
- `tax.us.2025.scheduleb.adjustment.abp-adjustment`

Line 2b v6 also *requires* `tax.us.2025.interest.current-year-adjustment-subtotal` but does **not** `require_closed` a source family for it. The aggregator "does not collect the incumbent Schedule B form-row family. An empty pairing set publishes 0." **No pairing source family exists.** None is invented.

**Schedule B v5 Part I** additionally collects the same seven positive families plus nominee and ABP adjustment rows. Requirement is a threshold on `interest.positive-total` and `dividends.ordinary-total`, not `family_nonempty` on nominee.

**Neighboring accrued legacy family (N9b destination historically; retired as a v6 line-2b subtractand):**

- `tax.us.2025.scheduleb.adjustment.accrued-interest` — still a committed family. Line 2b v6 notes it is not referenced; v6 cannot double-subtract lingering legacy accrued findings. N9b routes to the pairing-scoped accrued translation, not this family's member predicate.

**Inspected, not qualifying (emptiness/membership does not affect this feature or a neighboring result of this feature):**

- Every other committed family under `packages/content/tax/2025/family.*` (1099-B, 1099-R, W-2, 1098, SSA, wash-sale, …). No committed consumer on this feature's path reads their membership.
- **Canonical nominee-allocation family, payment/credit family, owner family, pairing-for-nominee family:** not committed. **Not invented.** No closure declaration or eligibility contract is written for the deferred canonical representation.

**Qualifying families** (emptiness or membership actually affects this feature and/or a neighboring result this feature's output joins): the nine line-2b `require_closed` families; `tax.us.2025.f1099div.1a`, which reaches the **shared Schedule B disposition**; and the committed accrued-interest family as an N9b/coexistence neighbor.

`tax.us.2025.f1099div.1a` qualifies through the **shared Schedule B
disposition** and is exercised in §5.7.

No committed eligibility contract exists for the deferred canonical allocation. For families that *do* exist, "nonempty ineligible" is **not** invented as a new membership predicate. Where the family has no eligibility beyond its member predicate, ineligibility is the **product applicability** already named by the cases (wrong report; legacy amount is not an ordinary allocation; N9b circumstance). Track 0 chooses those explicitly below rather than inheriting a convenient guard.

Neighboring result in every row: Form 1040 line 2b (`tax.us.2025.interest.taxable-total`) and Schedule B Part I, unless a narrower neighbor is named.

### 5.2 `tax.us.2025.f1099int.b1`

| Family state | Universe / absence authority | Eligibility or applicability | Expected feature result | Expected neighboring result |
| --- | --- | --- | --- | --- |
| Closed empty | Current box-1 source-closure true on the current horizon; no members | Negative / inapplicable: there is no box-1 report to allocate | No nominee translation of a 1099-INT box-1 occurs; no allocation is captured against a report that does not exist. **Scope of what this closure supports: "no current box-1 report exists in the `f1099int.b1` family."** It does **not** support the global claim "no nominee allocation is recorded," because the **independent legacy family `tax.us.2025.scheduleb.adjustment.nominee` may still contain members** — its closure is separate and is exercised in §5.3. Must not say the user owns all taxable interest, and must not treat closed-empty box-1 as a denial of other ownership. | `b1-subtotal` is the family's authorized zero (ADR-0016 Decision 5). Line 2b `require_closed` on this family **passes**. Line 2b still depends on the other eight closures. Schedule B Part I lists no box-1 rows. |
| Closed empty | Required box-1 closure missing (no current true closure, or stale horizon) | Any | Feature must **not** treat the universe as known-empty. Cannot conclude "no reports, therefore no allocation." Unanswered ownership question remains a non-claim. | Line 2b **blocks** (`require_closed` this source_set fails). Schedule B box-1 collect has no closed universe. Blast is this family's dependency, not a nominee-specific extra gate. |
| Nonempty | Complete; members are current box-1 amounts (N2, N11a report A/B) | Eligible as documentary reports. An allocation, if captured, is applicable only against the report it is attached to. | Preserve each report. Allocation against A reduces A only (N11a). Silence/no-allocation: remainder equals that report's amount; not an ownership finding (N1a). | Each member lists on Schedule B Part I; `b1-subtotal` sums them; line 2b adds that subtotal (then subtracts closed adjustments). |
| Nonempty | Members present; allocation attached to a different report, or amount unsupportable on the attached report (N11b, N5) | **Ineligible as the support base for that allocation.** Explicit choice: ineligibility is report-scoped supportability, not expulsion from the family. The other report remains an eligible documentary member. | No leakage, no borrowed support. Unsupportable attached set contributes no reduction; N5/N6b inherited block of the dependent nominee result; never a negative remainder. Report B remainder stays that report's amount. | Every current box-1 member still lists and still adds into `b1-subtotal`. Line 2b **blocks** if the nominee-subtotal (the dependent result) blocks under inherited ADR-0070 Decision 10; report B is unaffected *as a report remainder*, not as a licence to publish line 2b under an unstated confidence. |

### 5.3 `tax.us.2025.scheduleb.adjustment.nominee` (committed legacy family)

| Family state | Universe / absence authority | Eligibility or applicability | Expected feature result | Expected neighboring result |
| --- | --- | --- | --- | --- |
| Closed empty | Current nominee source-closure true; no amount members | Negative: no legacy nominee adjustment is recorded. **Not** an ordinary-allocation absence declaration and **not** a user denial (N1a). | No legacy nominee reduction. Canonical ordinary allocation, if later captured, is a different proposition (N8). Remainder of each report equals the reported amount minus *other* recorded reductions. | Nominee subtotal is this family's authorized zero. Line 2b `require_closed` **passes**. Schedule B nominee row collect is empty (no "Nominee Distribution" member rows). |
| Closed empty | Required nominee closure missing | Any | Must not treat legacy nominee as known-empty. Must not invent an absence declaration. Ordinary non-claim "no allocation recorded" still holds for the *canonical* statement, which this family is not. | Line 2b **blocks** on `require_closed` of this family. Blast is the existing line-2b dependency, already present in v4/v5/v6 (P2 compatibility surfaces). |
| Nonempty | Complete; current nonnegative amount members (H1) | Eligible **as legacy preclassified amounts**. The family member predicate is the amount type; value_schema `minimum: 0`. | Committed arithmetic consumes the amounts: subtotal collects them; line 2b subtracts the subtotal; Schedule B renders "Nominee Distribution" (P2 E20–E23, reused). This is **not** ordinary-language translation. No owner, no report association, no reporting evaluation from these members. | Line 2b reduced by the subtotal once. Schedule B shows nominee rows. Neighboring addends unchanged. |
| Nonempty | Live legacy members present; used as if they were ordinary allocations, or present alongside a new ordinary-fact-derived reduction of the same dollars (N8) | **Ineligible as canonical ordinary allocation evidence.** Explicit choice: no owner/report/basis fields exist on the type (P2 E18). Ineligibility is product applicability, not a new family predicate. Members remain eligible *as legacy amounts*. | Do not silently convert the amount into an ownership claim. Do not double-subtract. One subtraction or an explicit migration/refusal: reduction `$450`, share `$750` in the N8 figures — never `$900` / `$300`. | Line 2b and Schedule B still consume the legacy subtotal until a successor producer and coexistence contract exist (N8 remains paper until T0-C proposes one). |

### 5.4 `tax.us.2025.scheduleb.adjustment.abp-adjustment` (neighboring subtractand)

| Family state | Universe / absence authority | Eligibility or applicability | Expected feature result | Expected neighboring result |
| --- | --- | --- | --- | --- |
| Closed empty | Current ABP closure true; no members | Inapplicable to nominee. ABP is a different adjustment class (`family.scheduleb-adjustment.abp-adjustment.json` closure_claim). | Nominee translation and legacy nominee path unchanged. | ABP subtotal authorized zero. Line 2b `require_closed` passes. Schedule B has no ABP rows. |
| Closed empty | ABP closure missing | Any | Nominee feature locally unchanged. | Line 2b **blocks** on this family's `require_closed`. A supported nominee reduction cannot reach a filed line 2b until ABP is closed. Justified by the existing composition, not by a new nominee gate. |
| Nonempty | Complete; eligible ABP members | Eligible for ABP subtotal only. | Nominee feature unchanged. No ABP member is a nominee allocation. | Line 2b subtracts both nominee and ABP subtotals (and current-year-adjustment). Schedule B lists both adjustment labels. |
| Nonempty | ABP members present; treated as nominee or as ordinary allocation | **Ineligible for nominee treatment.** Explicit: ABP closure_claim excludes other adjustment classes. | Do not route ABP amounts into nominee reduction or reporting evaluation. | ABP still subtracts as ABP. Nominee still subtracts only nominee members. |

### 5.5 Line 2b co-required addend families

Applies identically to each of: `tax.us.2025.f1099int.b3`, `tax.us.2025.f1099oid.b1`, `tax.us.2025.non-form-interest`, `tax.us.2025.form1065-k1.box5`, `tax.us.2025.f1099int.b10`, `tax.us.2025.f1099oid.b5`.

This milestone's box is 2025 Form 1099-INT **box-1** reports. These families are not nominee-allocation universes.

| Family state | Universe / absence authority | Eligibility or applicability | Expected feature result | Expected neighboring result |
| --- | --- | --- | --- | --- |
| Closed empty | That family's own current closure true; no members | Inapplicable to nominee. Each family's closure_claim is box- or source-specific (ADR-0016). | Box-1 nominee translation unchanged. | That family's subtotal is its authorized zero. Line 2b `require_closed` passes for that source_set. Schedule B Part I has no rows from that family. |
| Closed empty | That family's required closure missing | Any | Nominee feature locally unchanged (box-1 allocation neither proven nor disproven by an open box-3 universe). | Line 2b **blocks** on that `require_closed`. Justified by the existing taxable-interest composition. |
| Nonempty | Complete; members eligible for that family's own subtotal | Eligible for that subtotal only. | Nominee feature unchanged. Do not allocate box-1 belonging from a box-3 (or OID, K-1, …) member. | Line 2b adds that subtotal. Schedule B lists those rows. |
| Nonempty | Members present; used to support a box-1 allocation or to borrow support (N11b analog) | **Ineligible as a box-1 allocation base.** Explicit: no cross-family borrowed support. | A box-1 allocation is supportable only against its attached box-1 report. These members cannot rescue N5/N11b. | Those members still compose *their* subtotals. Line 2b still adds them. |

### 5.6 `tax.us.2025.scheduleb.adjustment.accrued-interest` (N9b neighbor)

Three distinct things govern this neighbor and are kept apart.

| # | Distinct thing | What it is |
| --- | --- | --- |
| 1 | **A current closed-empty legacy family** | The family is admitted, its closure is current and true, and it has **no members**. |
| 2 | **Absence of that family from a package** | The family is **not admitted at all**. `package.core-calculations.v34` carries `citation.scheduleb-adjustment.accrued-interest`, `closure-mapping.scheduleb-adjustment.accrued-interest`, **and** `rule.scheduleb-adjustment.accrued-interest-subtotal`. **Of those three legacy-family artifacts, v35 carries only the citation** — v35 does also contain migration and succession artifacts (`interest.accrued-interest-migrated.vocabulary`, `rule.relationship.accrued-supported`, `scheduleb-accrued-interest.succession`), so this is a statement about the three family artifacts, not about everything accrued-related in the package. Retirement is **not** emptiness (ADR-0072: the legacy input surface is retired for new obligations). |
| 3 | **An empty pairing-scoped adjustment set** | `tax.us.2025.interest.current-year-adjustment-subtotal` publishes `0` when no pairing-scoped consequence exists. **No pairing source family exists**, so this is not a family state, and none is invented. |

**Legacy-family closure does not determine whether the pairing set is empty.**
Both v34 and v35 admit `rule.interest.current-year-adjustment.pairing-scoped`,
whose emptiness is a function of pairing findings, not of the legacy family's
closure or admission.

**Package composition**, read from the member pins:

| Package | Line 2b | Schedule B attachment |
| --- | --- | --- |
| `v34` | `rule.form1040-line2b` **v5** | `rule.attachment.schedule-b` **v4** |
| `v35` | `rule.form1040-line2b` **v6** | `rule.attachment.schedule-b` **v5** |

#### Under package v34 (legacy family admitted; line 2b v5 + Schedule B v4)

Schedule B **v4 carries the legacy `accrued_interest` adjustment row**
(`adjustment_rows[1]`, label "Accrued Interest"), collecting the legacy
accrued-interest family and tying out to
`tax.us.2025.interest.scheduleb-accrued-interest-subtotal`. Schedule B v5 drops
that row. **Neither version carries a pairing-scoped
current-year-adjustment row.** Line 2b **v5 consumes both** the legacy accrued
subtotal and the pairing-scoped current-year-adjustment subtotal; v6 consumes
only the pairing one.

| Family state | Universe / absence authority | Eligibility or applicability | Expected feature result | Expected neighboring result |
| --- | --- | --- | --- | --- |
| Closed empty | Legacy accrued closure current and true; no members | Inapplicable to nominee | N9b must still route *away* from nominee; the destination is the pairing-scoped accrued translation, not this family's emptiness. No nominee reduction from an N9b sentence | **Line 2b v5 consumes** the family's authorized zero. Schedule B v4 presents its **accrued-interest row with no member rows**. The attachment's disposition still depends on its own threshold and prerequisites, and independently on the pairing-scoped current-year-adjustment subtotal |
| Closed empty | Required closure **missing** while the family is admitted | Any | Nominee feature not authorized to treat accrued as known-empty | **Line 2b v5 blocks** on the missing closure. If Schedule B is **not required**, it is **inapplicable before itemization is reached**. If it **is required**, it **blocks**, because its itemization depends on the line-2b result that is now unavailable |
| Nonempty, eligible | Live legacy accrued members, closure current | Eligible as **accrued** legacy amounts, not as nominee | N9b must not capture them as nominee allocations | **Line 2b v5 consumes** the legacy subtotal, **which may itself be zero** — the amount fact's value schema is `minimum: 0`, so a nonempty family can sum to zero. Schedule B v4 **itemizes the legacy accrued amount through its own row**, so that amount ties out. **Only a nonzero pairing-scoped current-year adjustment creates the missing-row tie-out mismatch**, because that is the subtractand no Schedule B version itemizes |
| Nonempty, ineligible for nominee use | Accrued members present, correctly classified as accrued (the N9b failure mode is treating them as nominee) | **Ineligible for nominee treatment** — Schedule B label and taxable person differ (P2 Part D, reused) | Derive no nominee reduction from them; the companion consequence is basis plus current-year adjustment, not a nominee 1099-INT to the seller. Nominee classification is forbidden | **Their accrued treatment is preserved, not suppressed**: line 2b v5 still consumes the legacy accrued subtotal, and Schedule B v4 still itemizes them through the accrued-interest row. What must not happen is their appearing in `scheduleb-nominee-subtotal` or in v4's nominee row |

#### Under package v35 (legacy family retired; line 2b v6 + Schedule B v5)

State 2 is the operative one: the family is **not admitted**, so "closed empty"
is not a state it can be in on this package, and the nominee feature must not
read its emptiness as authority.

#### The current-year-adjustment presentation limitation

This is **established committed behavior**, and it spans **both** packages:

- `rule.form1040-line2b` **v5 and v6 both subtract**
  `tax.us.2025.interest.current-year-adjustment-subtotal`;
- **neither** `rule.attachment.schedule-b` **v4** nor **v5** carries an
  adjustment row tying out to it. Their `adjustment_rows` are, in v4:
  `nominee_distribution`, `accrued_interest`, `abp_adjustment`; in v5:
  `nominee_distribution`, `abp_adjustment`. **No row in either version names the
  pairing-scoped subtotal.** This is distinct from the legacy accrued row, which
  v4 does carry and which does tie out to
  `scheduleb-accrued-interest-subtotal`.

So a **nonzero** pairing-scoped current-year adjustment is subtracted at line 2b
while being unrepresented in the Schedule B itemization, on either package.

**When the violation actually occurs.** `ITEMIZATION_TIE_OUT_VIOLATION`
(`packages/derivation/runner.py`, constant at line 163; raised on the attachment
tie-out path near line 1229, hard-failing the attachment only) fires **only when
Schedule B is required and execution reaches the itemization tie-out check**. If
the attachment is **not required** — no subtotal strictly exceeds the `$1,500`
threshold — the attachment is **inapplicable before that check is reached**, and
no violation occurs. If a required subtotal is **absent**, the attachment blocks
earlier still, with `BLOCK_ABSENT`.

**Status.** The limitation is **established**; only its future repair is
unknown. It is a **neighboring-capability constraint** that a nominee row joining
the same attachment inherits — not a nominee defect, and not repaired here. It
belongs in T0-C's neighboring-capability diff.

### 5.7 `tax.us.2025.f1099div.1a` (shared Schedule B disposition)

Qualifies because it reaches the **same attachment** this feature's nominee row
appears on. It authorizes `tax.us.2025.dividends.1a-subtotal` via
`rule.f1099div-1a-subtotal`, which feeds `rule.form1040-line3b`, and the
Schedule B attachment requirement reads `tax.us.2025.dividends.ordinary-total`
alongside `interest.positive-total`.

Two committed behaviors govern every row below.

**The attachment is atomic.** `attempt_attachment`
(`packages/derivation/runner.py`) collects `requirement["subtotals"]`, and if
**any** required subtotal is absent from `self.symbols` it calls
`_attachment_block(rule_id, BLOCK_ABSENT, missing_subtotals, …)` and returns
`"blocked"` — **before** it reads `threshold_parameter` and before any
itemization or tie-out processing. So an absent `dividends.ordinary-total`
blocks the **whole Schedule B attachment**, Part I included. Part I is **not**
independently available in that state.

**The threshold is strictly exceeded, not merely met.** The requirement is an
"any subtotal over threshold" test against
`tax.us.2025.parameter.schedule-b-threshold`, whose committed value is
**`1500`**. A positive subtotal at or below `$1,500` does **not** independently
require Schedule B.

| Family state | Universe / absence authority | Eligibility or applicability | Nominee arithmetic and line 2b | Schedule B / line 3b |
| --- | --- | --- | --- | --- |
| Closed empty | Current 1a closure true; no members | Inapplicable — no ordinary dividends | **Locally unaffected.** The nominee reduction and remainder derive as they would otherwise; no dividend fact is read, and line 2b is unchanged | `dividends.1a-subtotal` is the family's authorized zero, so `ordinary-total` is present and zero. The attachment is **not blocked** by absence. Whether Schedule B is required then rests on interest alone: required only if `interest.positive-total` **strictly exceeds `$1,500`** |
| Closed empty | Required 1a closure **missing**, so `dividends.ordinary-total` is absent from the run's symbols | Any | **Locally unaffected.** Nominee arithmetic is not gated on a dividend closure, and **line 2b still computes and still subtracts the nominee reduction** | **Line 3b blocks**, and **the entire Schedule B attachment blocks** with `BLOCK_ABSENT` naming the missing subtotal — before threshold or itemization processing. Part I does not publish. The nominee row has no surface, even though its figure is correct |
| Nonempty, eligible | Live box-1a members, closure current | Positive | **Locally unaffected** | `dividends.1a-subtotal` is nonzero and `line 3b` computes. **Nonempty does not by itself require Schedule B**: the attachment is required only where a subtotal **strictly exceeds `$1,500`**. At or below that, dividends do not independently require it; above it, Schedule B is required and the nominee row must be present and tie out |
| Nonempty, ineligible | Members admitted by the family's member predicate that are not, in substance, ordinary dividends for this line | Negative **for nominee use only** | **Locally unaffected.** A misclassified dividend member is not nominee evidence and must never be read as an ownership allocation | **No silent exclusion is available, and none is claimed.** The family carries only a fact-type member predicate, and `rule.f1099div-1a-subtotal` `collect`s **every admitted member** of `tax.us.2025.f1099div.1a` — there is no committed eligibility filter. A misclassified admitted member is therefore **counted** in `dividends.1a-subtotal` and can carry the attachment over the threshold. The route is **correction or refusal of that member**, not an unbuilt filter quietly dropping it |

The interaction to carry forward is one-directional: **dividend state can decide
whether the nominee row's surface exists at all, while never changing the
nominee figure or line 2b.**

---

## 6. Paper transfer dispositions (P-T1 / P-T1a / P-T1b)

Each seam of the plan transfer table receives exactly one disposition.

### P-T1 — do the accrued-interest translation seams transfer?

#### Seam: Canonical object-valued ordinary fact + field-ref access

**Disposition: new decision.**

Distinguishing product behavior: N4 requires two distinguishable allocations with separable per-owner reporting evaluation; N7 requires that correcting one owner's amount (`$450`→`$400`) not rewrite the other owner's current statement. A **single** current fact holding the whole allocated-away set makes N7 a whole-fact replacement and couples per-owner explanation. Accrued interest is one circumstance / one object-valued fact (`obligation-acquisition-circumstance`, ADR-0067 field-ref of `accrued_interest_paid_to_seller`). That "one current fact" shape does not transfer unchanged to arbitrary owner cardinality.

ADR-0067's field-ref *reading* pattern is available if a later object-valued allocation fact is selected; that is not this seam's discriminator. ADR-0068 Decision 6 (multiple acquisitions on one report) is acquisition-specific text and is **not** read as governing nominee representation — resemblance is not transfer (charter closed item 4). R-A vs R-B is a different axis and stays deferred. This checkpoint does not choose per-owner facts versus any other multi-owner shape.

#### Seam: Report association

**Disposition: bounded extension.**

Added property: an allocation is **evaluated against one named report's current amount**. N11a: reduction `$450` / remainder `$750` stay on report A; report B remainder `$800`; same-payer identity must not collapse the reports. N11b: `$450` attached to report A (`$300`) is unsupportable on A and must not borrow report B (`$800`). N6a: recompute against the current amount of the **same** report identity.

Affected consumers: supportability (per-report, not pooled); Schedule B / line 2b remainders described per report; N6a/N6b same-identity correction.

What is **not** selected: whether the allocation's own identity includes the report (R-A) or a separate pairing names it (R-B). No N1a–N12 case discriminates those representations (P3-F1, closed). ADR-0068's pairing text names acquisition-to-report, not nominee allocation; it is not claimed as contract transfer of the representation.

#### Seam: Supportability (also P-T1b)

**Disposition: transfer unchanged** — inherit ADR-0070 Decisions 8–10.

Relevant proposition, authority, and consumer properties match:

| Property | Accrued (ADR-0070) | Nominee (N5, N6b, N11b) |
| --- | --- | --- |
| Proposition | Claimed amount(s) against the associated report's own amount; aggregate over-claim is internal inconsistency, not proof that no adjustment applies | `sum(allocated away)` against the attached report's current amount; over-allocation is the same inconsistency |
| Authority | Adopted tax rule; detect and exclude; **no allocation policy** (Decision 8) | Product cannot choose whose claim to drop (plan N5) |
| Per-item vs aggregate | Per-pairing vs report-group (Decisions 3, 6) | Per-allocation vs set on one report (N4 individual vs N5 aggregate); N11b is per-report, not a pooled `$1,100` |
| Retract composing claims | Decision 9 | Over-allocated set as a whole contributes no reduction; no still-supportable subset |
| Dependent consumer | Current-year subtotal **blocks entirely**; never an unreduced remainder as a settled, differently-scoped number (Decision 10) | Dependent result **blocks**; never a negative remainder; never a characterized unreduced share as ordinarily computed |

N11b's "report B is unaffected at `$800` regardless" is **no leakage / no borrowed support**, not a deviation that would publish line 2b while report A's allocation set is unsupportable. Under Decision 10 the dependent nominee-subtotal / line 2b blocks; B's *report remainder* is still `$800`.

No product difference is named that would make the posture inapplicable. **P-T1b: inherit.** No deviation is returned.

#### Seam: Rule-owned consequences (also P-T1a)

**Disposition: bounded extension.**

Added property: **independently gated** consequences with **independent explanation** (independent pin sets).

ADR-0071 Decision 2 already publishes two findings via two rule artifacts, **gated on the same supportability verdict**. That shared gate is the accrued precedent and is **not** the open question. N10 forbids gating the belonging-supported reduction on payment. N12 forbids inferring a reduction from payment. Reporting evaluations must not be inferred from belonging, and must not be combined into one normalized obligation.

Affected consumers: Schedule B / line 2b reduction (pins: allocation finding id, attached report, supportability, rule — **not** the payment finding); each authority-indexed reporting evaluation (pins: the facts **that particular attributed statement reads** — formulation 1 necessarily reads payment/credit; a regulation-attributed statement pins payment, credit, setting-apart, collection, or intermediary facts only where that statement relies on them, and not where it is limited to the actually-owned-portion language); explanation walks that must not couple their correction behavior (ADR-0071 Decision 6: shared pins displace together — putting payment on the reduction's pin set would be the kill).

Expressibility at paper: ADR-0024 Decision 1 (guarded rules, `choose`/`all`, inapplicable dispositions) plus ADR-0071 Decision 2 (one finding per rule id, so two rules) plus Decision 5 (independent succession). This is not a technical-capability uncertainty that paper cannot settle. No executable spike is returned.

**P-T1a: yes — separately supported consequences require independently gated rules and independent explanation.** Shared-gate dual publication does not transfer.

#### Seam: Ordinary-input mapping

**Disposition: bounded extension.**

Added property: **circumstance routing before any nominee allocation is captured**; N9b routed to the existing accrued translation; never a tax-label question.

The accrued mapper (`packages/tax/obligation_acquisition_mapping.py` lines 9–30, 66–114) is closed (`additionalProperties: false`) on one acquisition circumstance. It cannot accept nominee fields and must not be overloaded to do so. Bounded Branch B (reused): no ordinary-language producer of the legacy nominee amount in the searched production tree.

Affected consumers: any future nominee intake (none exists today); the accrued mapper as N9b *destination*, not as a shared solicitor; N9a document-correction routing as a separate control.

This is the T0-A paper box. Production intake, screens, and wording are out of scope.

#### Seam: Legacy coexistence

**Disposition: bounded extension.**

Added property: **no-silent-conversion** transfers as posture; ADR-0072's accrued-specific retirement, same-amount collision trigger, and migration-adoption **do not** already migrate nominee.

ADR-0072 Decision 1: "The legacy accrued-interest input surface is retired for new obligations; the legacy fact type is never edited, deleted, or reinterpreted." Nominee is not named (P2 E26, reused). The posture that transfers: do not edit, delete, or reinterpret `tax.us.2025.scheduleb.adjustment.nominee.amount`; do not upgrade it into an ownership claim it never contained.

What differs: Branch B means there is no production ordinary producer to "retire" for new obligations — attested legacy facts still exist (tests inject them), so N8 is a live compatibility case. ADR-0072 Decision 2's amount-equality collision is an analogy (legacy nominee also lacks owner/report identity), not an inherited mechanism.

Affected consumers: line 2b subtractand `scheduleb-nominee-subtotal`; Schedule B nominee rows; `package_validation.py` adjustment slots; core-calculations admissions (P2 compatibility list, reused). Double subtraction is the N8 kill. A concrete successor producer would make the integration-surface artifact mandatory (T0-C); none is proposed here.

### P-T1 summary

| Seam | Disposition |
| --- | --- |
| Object-valued fact + field-ref / cardinality | new decision (per-owner correction and per-owner reporting vs one combined fact) |
| Report association | bounded extension (report-scoped evaluation; representation deferred) |
| Supportability | transfer unchanged (ADR-0070 Decisions 8–10) |
| Rule-owned consequences | bounded extension (independent gates and pin sets) |
| Ordinary-input mapping | bounded extension (route before capture; no tax label) |
| Legacy coexistence | bounded extension (no-silent-conversion posture; not ADR-0072 migration) |

---

## Findings

### T0-F1 — Attribution is recoverable, not explained; exposure needs a bounded extension

- **Class.** Gap.
- **Evidence.** §3.5–3.6, consumer by consumer. `act.v1` carries `actor`/`at`/`committed_against`, so the chain is recoverable. `ExplanationNode` may retain the ordinary input finding id but no actor or time; presentation `citationSites` may retain the ordinary leaf `pinId` but no actor or time; `walk_npe` retains only derived-symbol children, can drop direct ordinary-input leaves entirely, and publishes a `finding_id` identifying the **derived** finding. No projection, join, or schema design is selected.
- **Depends later.** T0-B traces that name a reader-facing kill for "determination without who supported it"; any later explanation-extension charter. Not T0-B's job to design it.

### T0-F2 — Owner cardinality is a new decision, distinct from deferred R-A/R-B

- **Class.** Gap (decision to return, not a defect in the cases).
- **Evidence.** N4 + N7 vs ADR-0067's one-circumstance object. Not inferred as R-B.
- **Depends later.** T0-C contract proposal. Do not prototype rivals in T0-B.

### T0-F3 — Independently gated consequences are a bounded extension of ADR-0071, not a shared-gate copy

- **Class.** Gap (named extension; paper-sufficient).
- **Evidence.** ADR-0071 Decision 2 shared supportability gate vs N10/N12. ADR-0024 guards exist.
- **Depends later.** T0-B N10/N12 kill traces (formulation × facts × surface). No climb.

### T0-F4 — Legacy nominee family is live and ineligible as ordinary allocation evidence

- **Class.** Deferral of successor/coexistence mechanism; posture is settled as no-silent-conversion.
- **Evidence.** §5.3 nonempty ineligible; N8; ADR-0072 does not migrate nominee.
- **Depends later.** T0-C N8 compatibility account; integration-surface artifact only if a successor producer is proposed.

### T0-F5 — both packages subtract a current-year adjustment neither Schedule B version itemizes

- **Class.** Established limitation; neighboring-capability constraint, not a nominee defect.
- **Evidence.** §5.6. `rule.form1040-line2b` **v5 and v6 both** subtract `tax.us.2025.interest.current-year-adjustment-subtotal`. **Neither** `rule.attachment.schedule-b` **v4** nor **v5** carries an adjustment row tying out to that symbol: v4's rows are `nominee_distribution`, `accrued_interest`, `abp_adjustment`; v5's are `nominee_distribution`, `abp_adjustment`. The limitation is specific to the **pairing-scoped** subtotal — the **legacy** accrued amount is itemized by v4's `accrued_interest` row and is not part of this finding. Package v34 pairs line 2b v5 with Schedule B v4; v35 pairs line 2b v6 with Schedule B v5.
- **When it fires.** `ITEMIZATION_TIE_OUT_VIOLATION` (`packages/derivation/runner.py`, constant line 163; attachment tie-out path near line 1229, hard-failing the attachment only) occurs **only when Schedule B is required and execution reaches the itemization tie-out check**. If no subtotal strictly exceeds the `$1,500` threshold the attachment is inapplicable before that check; if a required subtotal is absent it blocks earlier with `BLOCK_ABSENT`.
- **Depends later.** T0-C neighboring-capability diff. A nominee row joining that attachment inherits the constraint.
- **Status.** The limitation is established; only its future repair is unknown. Not repaired here — outside this milestone's boundary and not caused by nominee interest.

### T0-F6 — Dividend family state decides whether the nominee row's surface exists

- **Class.** Verified neighboring dependency. No missing nominee capability is identified, so this is not recorded as a product gap.
- **Evidence.** §5.7. `tax.us.2025.f1099div.1a` authorizes `dividends.1a-subtotal` via `rule.f1099div-1a-subtotal`, feeding `rule.form1040-line3b`; the Schedule B requirement reads `dividends.ordinary-total` alongside `interest.positive-total`. The attachment is atomic: an absent required subtotal blocks the whole attachment, Part I included, before threshold or itemization processing.
- **Depends later.** T0-B traces must not assume the Schedule B attachment exists or is required; T0-C neighboring-capability diff.
- **Direction is one-way.** Dividend state can decide whether the nominee row's surface is required or published at all; it never changes the nominee figure or line 2b.

No defect is recorded against the plan blob this charter executes.

---

## Explicit unknowns

1. **R-A vs R-B.** No discriminator in N1a–N12. Reopening trigger remains a consumer that behaves differently (plan).
2. **Per-owner shape** once cardinality is decided (T0-F2): not chosen here.
3. **Relationship among the three reporting formulations.** Unreconciled. Not ranked, combined, or selected.
4. **Whether N12's onward transfer independently falls within another § 6049 route.** Preserved from P2. Not closed by reasoning.
5. **Explanation-extension shape.** Named as required for exposure (T0-F1); not designed.
6. **Whether implementation will appear to require a unified reporting predicate.** Unknown until T0-C. Owner posture then, not unresolved law.
7. **Production intake outside P2's searched tree.** P2 unknown 6. Out of scope.
8. **How the current-year-adjustment itemization limitation is repaired.** T0-F5 establishes the limitation on both packages and the exact condition under which `ITEMIZATION_TIE_OUT_VIOLATION` fires; what is unknown is only its future repair, which is outside this milestone. Carried to T0-C's neighboring-capability diff.
9. **What Schedule B requirement state a nominee row is published under.** T0-F6: dividend family state can decide whether the attachment is required, or block it entirely. T0-B traces must not assume the attachment exists or is required.

---

## Questions returned rather than answered

None at T0-A. Independent gating is expressible at paper (T0-F3). Supportability inherits (P-T1b). No executable spike is requested.

T0-A COMPLETE

---

# T0-B — traces

| | |
| --- | --- |
| Seat | Builder, Track 0 checkpoint T0-B |
| Source ref | `HEAD` at pickup = `577d53701f371ef78a6ec0e13d5818cd2e70ba2b` |
| Plan blob (authoritative pin) | the milestone plan |
| Branch | `milestone/nominee-interest-ownership-translation` |
| Evidence rung | PAPER. No prototype code, tests, or experiments. Quotes are from committed artifacts. Running an existing test would be a labelled observation; none was required. |
| Established input | T0-A in this file. Dispositions T0-F1–T0-F6, P-T1/P-T1a/P-T1b, the authority-lifecycle table, and the empty/nonempty matrix are not reopened. |
| Writable path | this file only |


This checkpoint produces the N1a–N12 paper traces with named kill conditions, the formulation × facts × surface tables for every reporting-touching case, the late-authority trace (adversarial-closure artifact 3), and the claim-reuse proof (artifact 4).

**Closed, not reopened:** P2's tax map; the three reporting formulations (never selected, combined, or ranked); P1-D1; R-A vs R-B; attribution placement on the act; the claim boundary (nothing may "establish belonging"); N10/N12 non-inference; the durable-publication gap.

**No rival implementations. No formulation-ranking experiment. No code.**

---

## 7. Trace conventions

### 7.1 Synthetic identities

Amounts and identifiers are synthetic (`demo.*` / `demo-*` only).

| Token | Stands for |
| --- | --- |
| `demo.payer.alpha` | One interest payer (`tax.us.interest-payer`) |
| `demo.1099int.statement-a` | One logical 1099-INT statement instance (report A) |
| `demo.1099int.statement-b` | A second logical 1099-INT statement instance from the same payer (report B) |
| `demo.owner.pat` | First named non-spouse actual owner |
| `demo.owner.kim` | Second named non-spouse actual owner |
| `demo.actor.user` | Asserting actor on the `act.v1` envelope |

Tax year is 2025 throughout. Other line-2b addend families (`b3`, OID, non-form, K-1 box 5, box 10, OID box 5) and the ABP adjustment family are treated as **closed empty** unless a case says otherwise, so they do not independently change the arithmetic. Legacy nominee family is **closed empty** except in N8.

### 7.2 Reduction and share

Plan `## Fixed product cases`: reduction is the amount allocated away; share is the computed remainder (reported amount minus recorded reductions). A share is arithmetic, **not** a finding that the taxpayer economically owns that amount.

### 7.3 Schedule B attachment surface (T0-F6, T0-F5)

Traces do **not** assume the Schedule B attachment exists or is required. Where a case's observable would be a Schedule B row, the trace states what happens when there is no attachment.

Committed requirement, walked from `packages/content/tax/2025/rule.attachment.schedule-b.v5.json` (`.requirement`; v4 is identical on this point):

```json
"comparison": "strictly_greater_than",
"subtotals": [
  "tax.us.2025.interest.positive-total",
  "tax.us.2025.dividends.ordinary-total"
],
"threshold_parameter": {
  "id": "tax.us.2025.parameter.schedule-b-threshold",
  "version": "v1"
}
```

`packages/content/tax/2025/parameter.schedule-b-threshold.json` `"values": 1500`.

`tax.us.2025.interest.positive-total` is the seven-family **line-1 basis before nominee subtraction**. Quoted from `packages/content/tax/2025/rule.interest-positive-total.json` `notes`: "Publishes the exact seven-family positive-interest line-1 basis for Schedule B threshold admission. It is not taxable interest after the three explicit adjustment classes".

So a single box-1 report of `$1,200` with the other six families at authorized zero yields `interest.positive-total = 1200`, which is **not** strictly greater than `$1,500`. Interest alone does **not** require Schedule B in N1a–N10, N11b, N12. **N11a** sums two box-1 reports `$1,200 + $800 = $2,000`, which **does** independently require the attachment.

Atomic block, quoted from `packages/derivation/runner.py` `attempt_attachment` (lines 997–1002): missing required subtotals call `_attachment_block(rule_id, BLOCK_ABSENT, missing_subtotals, …)` and `return "blocked"` **before** the threshold is read. An absent `dividends.ordinary-total` therefore blocks the **whole** attachment, Part I included. Line 2b is not gated on that dividend subtotal (T0-A §5.7; T0-F6).

If no subtotal strictly exceeds the threshold, `attempt_attachment` records `disposition: "inapplicable"` and returns `"inapplicable"` (lines 1028–1036) **before** itemization or tie-out. `ITEMIZATION_TIE_OUT_VIOLATION` (`runner.py` line 163; raised near lines 1224–1232) fires **only** when the attachment is required and execution reaches that check. T0-F5: neither Schedule B v4 nor v5 itemizes the pairing-scoped current-year-adjustment subtotal. **A trace must not attribute that failure to nominee interest.**

**Surface states used below.** For each case, "Schedule B nominee row" means one of:

| Attachment state | What a reader can see of a nominee row |
| --- | --- |
| **Not required** (`inapplicable`) | No Schedule B attachment, so **no nominee row**. The operational result is still on line 2b (`tax.us.2025.interest.taxable-total`) and in the run-local derived reduction. |
| **Blocked** (`BLOCK_ABSENT`, typically missing `dividends.ordinary-total`) | Whole attachment unpublished. **No nominee row**, even when the nominee figure is correct. Line 2b still computes. |
| **Required and published** | Nominee row exists only if a current member of `tax.us.2025.scheduleb.adjustment.nominee` is collected, **or** a future canonical producer publishes an equivalent row. Until a successor producer is proposed (T0-C), the committed row is the legacy collect. A paper-canonical reduction without a legacy member has **no committed Schedule B row** even when the attachment is required. |

Unless a case states otherwise, the default for `$1,200`-only interest is **not required**. The kill is then observed on line 2b / the run-local derived finding / explanation, not on a Schedule B row.

### 7.4 Reporting-formulation method

Plan `## Fixed product cases` (after the table): "No case may resolve the unresolved relationship among the reporting formulations." Every reporting-touching required result is: evaluate each authority-indexed formulation on its own terms; record which scenario facts are present or absent; surface only what that authority expressly supports, with the authority named; otherwise qualify or defer. Applicability itself remains unresolved.

The three formulations, from the plan `### A2` table (the milestone plan), are **not ranked, combined, or selected**:

| # | Formulation | Authority |
| --- | --- | --- |
| 1 | Literal IRC § 6049(a)(2): receive as a nominee **and** make payments aggregating `$10` or more with respect to the interest so received | statute |
| 2 | 2025 General Instructions for Certain Information Returns, "Nominee/middleman returns"; and the Schedule B TIP | form instruction |
| 3 | 26 CFR 1.6049-4: payor includes collector/middleman; middleman includes a nominee who pays, collects, or acts as intermediary; a person is a middleman as to any portion actually owned by another | regulation |

Quoted operative text is reused from P2's evidence map (established input, not re-retrieved): E6 (statute), E11 and E3 (filing instructions), E7–E9 (regulation). Publication 550 is explanatory and not controlling (plan Sources and locators).

Tables below **do not** manufacture three competing legal conclusions. Each cell is: facts present or absent for that authority's own terms, then only the instruction or sentence that authority states, attributed to it. A product finding that "the taxpayer has a 6049 obligation" would be a forbidden normalization.

Reporting-touching cases: **N2, N4, N10, N11a, N12** (N2, N4, N10, N12 required at minimum; N11a's required result also demands formulation evaluation). N3, N5, N6a, N6b, N7, N8, N9a, N9b do not supply a reporting required-result and do not get a table.

### 7.5 Kill-condition shape

A trace without a kill condition is decoration. Each kill names (1) what a **lying implementation** would do and (2) the **observation** that would catch it. Observations are paper: inspect the run-local `RunResult` publications, line 2b, explanation nodes, and — only when the attachment is required and published — Schedule B rows.

### 7.6 Entry conditions discharged

| Entry condition | Where the traces discharge it |
| --- | --- |
| T0-F6 attachment atomic / dividend block | §7.3; every case's "Schedule B surface" paragraph |
| T0-F5 tie-out is neighboring, not nominee | §7.3; N9b surface note |
| T0-F2 owner-cardinality discriminator | N4, N7; no shape selected |
| T0-F1 reader-facing kill | N2 kill **N2-ATTR**; cross-check on N4/N7/N10 |
| T0-F3 independent gating | N10, N12 (kills and formulation tables) |
| T0-F4 legacy ineligible; N8 is claim-reuse | N8; artifact 4 |

---

## 8. N1a–N12 paper traces

### N1a — no recorded allocation, no response

**Facts.** One box-1 report: `demo.payer.alpha` / `demo.1099int.statement-a` / 2025 = `$1,200`. Workspace holds **no nominee allocation and no response** to the ownership question. "No allocation recorded" is a **non-claim state** (T0-A §4): no user author, does not assert taxpayer ownership, ends when an affirmative allocation becomes current. No absence declaration is manufactured.

Box-1 identity, walked from `packages/content/tax/2025/f1099int.bundle.json` `fact_types[0]` `tax.us.2025.f1099int.box1-interest`: `identity_keys` are payer `tax.us.interest-payer`, statement `tax.us.1099int-statement`, tax-year `"2025"`. Title: "Multiple originals from one payer - including several concerning one account - are distinct statement instances."

**Required result.** Operational: no nominee reduction; remainder `$1,200` continues into taxable interest (P2 baseline). Product claim: the product **may** say that no nominee allocation is recorded. It **may not** say the user denied other ownership, and may not treat the unanswered question as establishing economic ownership of the full amount. Plan: "Silence is not an assertion."

**Schedule B surface.** `interest.positive-total = 1200` ≯ `1500` → attachment **not required**. No nominee row. If `dividends.ordinary-total` is absent, the attachment **blocks** (`BLOCK_ABSENT`) and there is still no nominee row. Line 2b still carries `$1,200` (minus other closed-empty adjustments at zero).

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N1a-SILENCE** | Treats the unanswered question as a denial, or explains later that the user denied other ownership | Durable state or explanation contains a negative allocation fact, a "user said no" claim, or an absence declaration manufactured for ownership |
| **N1a-OWN** | Treats remainder `$1,200` as a finding that the taxpayer economically owns the whole amount | A derived finding, citation, or reader-facing sentence that "establishes belonging" of the `$1,200` to the taxpayer |
| **N1a-RED** | Derives a nominee reduction from document structure (payer, form, account title) without an allocation | Line 2b / run-local nominee reduction ≠ `$0` |

---

### N1b — explicit negative response

**Facts.** Same report `$1,200`. The user is asked the gating question and **answers no**. P1-D1 (closed): the "no" is transient; it creates no durable allocation fact; durable state **converges with N1a**.

**Required result.** Same arithmetic as N1a: reduction `$0`, remainder `$1,200`. During the active interaction the product may acknowledge the answer just given. After the interaction, later explanations may say only that no nominee allocation is recorded, never that the user previously denied other ownership.

**Schedule B surface.** Same as N1a: attachment not required by `$1,200`; no nominee row; line 2b still `$1,200`.

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N1b-DURABLE** | Persists the "no" as a durable workspace claim (negative allocation fact, closed-empty ownership universe, or retained denial) | After the interaction, current findings include a negative allocation, or an explanation that the user previously denied other ownership |
| **N1b-DIVERGE** | Durable remainder or reduction differs from N1a | N1a and N1b durable line 2b / run-local reduction disagree |
| **N1b-OWN** | Reads the transient "no" as proving the taxpayer owns `$1,200` | Same class as N1a-OWN |

---

### N2 — partial allocation (reporting-touching; T0-F1 kill lives here)

**Facts.** Report `$1,200` on `demo.1099int.statement-a`. After N9b circumstance routing (T0-A §2), the user states `$450` belongs to `demo.owner.pat` (non-spouse), and **separately** that `$450` was paid on to that owner. The case supplies the payment fact; it does **not** decide that the payment fact is what makes reporting required.

The ordinary allocation is bounded evidence for applying the Schedule B classification. It does **not** establish belonging (claim boundary, closed). Provenance of the reduction must identify the assertion, payer report, rule, and authority.

**Required result.** Preserve the reported `$1,200`. Derive reduction `$450`, remainder `$750`. Evaluate each reporting formulation on its own terms (table below). Do not manufacture three competing legal conclusions.

**Reader-facing kill (T0-F1).** Attribution is recoverable from the assertion act (`actor`, `at`, `committed_against` on `act.v1`) and not exposed by current consumers (T0-A §3.5–3.6). This trace **names** the kill; it does **not** design the fix.

Quoted from `packages/derivation/explanation.py` `ExplanationNode` (lines 23–31): fields are `finding_id`, `role`, `kind`, `symbol`, `value`, `version`, `produced_by`, `children` — no `actor`, no `at`. `render_text` (lines 167–176) prints role, symbol or finding id, value, and producing rule id. Presentation `_citation_site` (`packages/derivation/presentation_projection.py` lines 217–218) emits `{siteId, pinId, pinVersion, context}`. `walk_npe` (lines 256–269) retains only children whose symbol is in `derived_symbols` and publishes the **derived** finding id.

**Schedule B surface.** Attachment **not required** by `$1,200`. No nominee row unless dividends independently require the attachment. Operational result is on line 2b (`$1,200 − $450 = $750` once a canonical or legacy subtractand is current) and in the run-local derived reduction. If dividends are absent, attachment blocks; line 2b is unaffected.

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N2-ATTR** | Shows the `$450` determination (or `$750` remainder) **without who supported the ordinary statement** | A reader of `ExplanationNode`, `citationSites`, or `walk_npe` cannot name `demo.actor.user` (or any asserting actor) or the assertion `at`. Current committed consumers already fail this observation (T0-A §3.6). That is the named reader-facing kill, not a licence to relocate attribution into the finding |
| **N2-BELONG** | Treats the ordinary statement as proving beneficial ownership or "establishing belonging" | Derived finding, label, or explanation claims proven ownership rather than a supported Schedule B determination |
| **N2-ARITH** | Reduction ≠ `$450` or remainder ≠ `$750`, or drops the payer report | Report amount not `$1,200`; line 2b / run-local reduction wrong |
| **N2-PAYGATE** | Gates the belonging-supported reduction on the payment fact (shared-gate copy of ADR-0071 Decision 2) | Absence or correction of the payment finding suppresses or displaces the `$450` reduction. Kill observation: payment appears on the reduction's pin set (ADR-0071 Decision 6: shared pins displace together) |
| **N2-NORM** | Emits one normalized "reporting obligation: yes" finding | A single product conclusion that selected, combined, or ranked the three formulations |

#### N2 formulation × facts × surface

| Formulation | Facts present | Facts absent | What may be surfaced (authority named) | Qualify or defer |
| --- | --- | --- | --- | --- |
| **1. Literal IRC § 6049(a)(2)** (statute, P2 E6) | Ordinary statement of nominee receipt of the `$450`; separate ordinary statement that `$450` was paid to `demo.owner.pat`; `$450 ≥ $10` | Nothing the statute's two conjuncts and threshold ask for, **as scenario facts**. Applicability of (a)(2) to these facts is still not a product-selected rule | Attributed to **IRC § 6049(a)(2)**: that section's own sentence — a person who receives interest as a nominee and who makes payments aggregating `$10` or more with respect to the interest so received shall make a return setting forth the aggregate amount of such payments and the name and address of the person to whom paid | Do **not** convert this attributed statutory sentence into "the" product reporting obligation, and do not treat it as writing a payment conjunct into Schedule B |
| **2. IRS filing instructions** (1099GI E11; Schedule B TIP E3) | Form 1099 received for amounts the ordinary statement treats as belonging to `demo.owner.pat`; named other owner; allocable amount `$450` | These paragraphs do **not** ask for a later-payment conjunct (P2 A2). Spouse exception does not apply (`demo.owner.pat` is non-spouse) | Attributed as **IRS filing-instruction guidance** (not as a finding that § 6049(a)(2) is satisfied): 1099GI — if you receive a Form 1099 for amounts that actually belong to another person, file one return per other owner showing the amounts allocable to each; Schedule B TIP — if you received interest as a nominee, you must give the actual owner a Form 1099-INT and file Forms 1096 and 1099-INT | Do **not** suppress this attributed guidance because the statute's payment conjunct is a different formulation. Do not treat the TIP as amending the statute |
| **3. 26 CFR 1.6049-4** (E7–E9) | Ordinary statement that a portion (`$450`) is actually another's; a payment fact is also present; deemed-paid rule is not needed because a payment is stated | Ranking of the actually-owned-portion sentence against (a)(2) (P2 unknown 5). Whether middleman status is (a)(1) or (a)(2) | Attributed to **26 CFR 1.6049-4**: quote only that authority's own sentences — payor includes a collector/middleman; middleman includes a nominee who pays, collects, or acts as intermediary; a person is a middleman as to any portion actually owned by another; interest is deemed paid when credited or set apart (E9), which is surplus here because a payment is already stated | Do **not** rank this as implementing or expanding (a)(2). Do not combine it with formulation 1 or 2 into one obligation |

This table records facts and attributed sentences. It is **not** three legal conclusions that the taxpayer is (or is not) required to file.

---

### N3 — full allocation

**Facts.** Report `$1,200`. All `$1,200` belongs to `demo.owner.pat`. Payment is **not** the variable; no payment fact is supplied and none is invented.

**Required result.** Reduction `$1,200`; share `$0` **with provenance**, not disappearance of the payer report.

**Schedule B surface.** Attachment not required by `$1,200`. No nominee row. Line 2b remainder `$0` is still a computed taxable-interest figure sitting on a preserved `$1,200` report, not a deleted statement.

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N3-DROP** | Drops, hides, or un-lists the payer report because the remainder is `$0` | `demo.1099int.statement-a` is absent from box-1 membership, Schedule B Part I (when the attachment is required), or the explanation of line 2b |
| **N3-ZERO** | Publishes share `$0` without provenance, or treats `$0` as "no interest was reported" | Zero with no pin to the assertion / report / rule; or box-1 subtotal rewritten to `$0` instead of `$1,200` minus `$1,200` |
| **N3-BELONG** | Treats full allocation as proving the taxpayer owns nothing, as a beneficial-ownership finding | Same class as N2-BELONG, inverted |

---

### N4 — several owners (reporting-touching; T0-F2 discriminator)

**Facts.** Report `$1,200`. `$300` belongs to `demo.owner.pat` and `$150` to `demo.owner.kim`. A **distinct** onward-payment fact is supplied for each owner, so payment is not the variable under test.

**Required result.** Two **distinguishable** allocations; aggregate reduction `$450`; remainder `$750`, on the same supported-determination footing as N2. Per owner, evaluate each formulation on its own terms (tables below). Keep each owner's consequence and explanation separable. Allocation alone does not establish literal § 6049(a)(2)'s payment conjunct (the case happens to supply payment **separately** per owner). Must not be treated as proving one normalized reporting obligation.

**T0-F2 discriminator, no shape selected.** T0-A P-T1: owner cardinality is a **new decision**, distinct from deferred R-A/R-B. Accrued interest is one circumstance / one object-valued fact. Distinguishing product behavior: correcting one owner's amount must **not** rewrite the other owner's **current statement**. This trace exposes that discriminator. It does **not** choose per-owner facts versus any other multi-owner shape.

**Schedule B surface.** Attachment not required by `$1,200`. Aggregate `$450` is on line 2b / run-local derived reduction. Per-owner separability is observed on the allocation statements and their explanations, not on a Schedule B row.

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N4-COLLAPSE** | Stores or explains the two allocations as one combined `$450` current statement, so that a later correction of `demo.owner.pat`'s `$300` rewrites `demo.owner.kim`'s current `$150` | After a same-identity correction of Pat's amount, Kim's current finding id, value `$150`, owner identity, and asserting act are no longer the pre-correction statement |
| **N4-MIXEXPL** | One explanation walk that cannot say which `$300` vs `$150` belongs to which owner, or that couples their correction behavior | A reader cannot separate Pat's `$300` from Kim's `$150`; correcting one displaces the other's derived reporting evaluation because they share a pin set they should not share |
| **N4-NORM** | One normalized reporting obligation for "the `$450`" | A single product reporting conclusion covering both owners, or a ranking/combination of formulations |
| **N4-ATTR** | Same reader-facing gap as N2-ATTR, per owner | Determination shown without who supported **that** owner's ordinary statement |
| **N4-ARITH** | Aggregate ≠ `$450` or remainder ≠ `$750` | Line 2b / run-local reduction wrong |

#### N4 formulation × facts × surface — per owner

Payment is present **per owner** as a scenario fact. Each owner's table is independent. `$300 ≥ $10` and `$150 ≥ $10`.

**Owner `demo.owner.pat` (`$300` allocated; `$300` paid).**

| Formulation | Facts present | Facts absent | What may be surfaced (authority named) | Qualify or defer |
| --- | --- | --- | --- | --- |
| **1. Literal § 6049(a)(2)** | Nominee-receipt statement for `$300`; payment to Pat `$300`; ≥ `$10` | Kim's facts are not this evaluation's facts | Attributed to **IRC § 6049(a)(2)**: that section's return-for-payments sentence, about payments to Pat | Do not fold Kim into Pat's return; do not select this formulation as the product rule |
| **2. IRS filing instructions** | Belonging/allocable `$300` to Pat; non-spouse | Later-payment conjunct not asked by E11/E3 | Attributed as **IRS filing-instruction guidance**: one 1099-INT showing amounts allocable to Pat | Do not suppress; do not treat as proving § 6049(a)(2) |
| **3. 26 CFR 1.6049-4** | Portion actually owned by Pat; payment to Pat present | Ranking unknown (P2 unknown 5) | Attributed to **26 CFR 1.6049-4**: middleman / actually-owned-portion sentences as they apply to this portion | Do not rank; do not combine with Pat's formulation 1 or 2 |

**Owner `demo.owner.kim` (`$150` allocated; `$150` paid).** Same three rows with Kim's `$150` substituted. A lying implementation that emits **one** formulation table for the aggregate `$450` is N4-NORM / N4-COLLAPSE.

---

### N5 — over-allocation (inherited ADR-0070 Decisions 8–10)

**Facts.** Report `$1,200`. Allocations total `$1,250`. T0-A P-T1b: inherit. This trace **applies** that disposition; it does not re-decide it.

Quoted ADR-0070 Decision 8: "No allocation policy, at either tier. This decision detects and excludes an over-claimed individual pairing or report-group; it does not decide how much of a report an acquisition, or a group of acquisitions, is 'really' entitled to." Decision 9: an aggregate block "retracts the individual claims that composed it — it does not leave them published alongside the block." Decision 10: the dependent subtotal "blocks entirely rather than excluding the failed group and publishing the remainder as a settled, differently-scoped number."

**Required result.** Preserve the payer report. The over-allocated set as a whole contributes **no** reduction (no still-supportable subset). Full retraction of composing claims. Dependent result **blocks**. Never a negative remainder (`-$50`).

**Schedule B surface.** Attachment not required by `$1,200`. The block is on the dependent nominee result / line 2b, not on a Schedule B row. If the attachment is independently required (dividends > `$1,500`) and execution reaches itemization, a **neighboring** T0-F5 tie-out can still fire from a nonzero pairing-scoped current-year adjustment; that is **not** this case's nominee over-allocation.

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N5-SUBSET** | Drops one owner's claim to make `$1,200` fit (an allocation policy) | A published reduction of `$1,200` or any still-supportable subset; product chose whose claim to drop |
| **N5-NEG** | Remainder `-$50` | Line 2b or run-local share negative |
| **N5-GROSS** | Publishes unreduced `$1,200` as a settled, differently-scoped taxable-interest number while the allocation set is unsupportable | Line 2b published as `$1,200` "ordinarily computed" rather than blocked (Decision 10) |
| **N5-STALE** | Leaves composing `$1,250` claims published alongside the block | Individual allocation-derived reductions still `published` (Decision 9) |
| **N5-DROP** | Drops the payer report | Report identity gone |

---

### N6a — corrected report, allocation still supportable

**Facts.** Same logical report `demo.1099int.statement-a` corrected `$1,200` → `$1,000`. Allocations total `$450` (still ≤ `$1,000`). ADR-0015 Decision 4: "A corrected copy of the same logical return answers the same fact and supersedes its prior finding." Bundle title: "a corrected copy of the same logical return answers this same fact and supersedes its prior finding."

**Required result.** Recompute against the **current amount on that same identity**: reduction `$450`, remainder `$550`, without rewriting history. Report identity is unchanged; only its amount moved. Plan: that is the whole case. R-A vs R-B is not discriminated (P3, closed).

**Schedule B surface.** `$1,000` ≯ `$1,500` → still not required by interest. No nominee row. Line 2b / run-local: `$550`.

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N6a-STALE** | Reuses the pre-correction remainder `$750` or report amount `$1,200` | After recompute, reduction/share not `$450`/`$550` |
| **N6a-REKEY** | Treats the correction as a new statement instance (new `demo.1099int.*`) | Report identity changed; N11-style split or a second box-1 member |
| **N6a-REWRITE** | Rewrites the historical `$1,200` assertion in place rather than superseding | Act log / prior finding no longer records `$1,200` as a superseded answer |
| **N6a-DISP** | Claims ADR-0010 act-log displacement of a durable derived publication | The milestone observes **run-local re-derivation** (charter closed item 8; artifact 3). Production does not persist derived publications (P3-D1) |

---

### N6b — correction creates over-allocation

**Facts.** Same logical report corrected `$1,200` → `$400` while an allocation of `$450` remains attached. The allocation was supportable before and is not after.

**Required result.** No stale reuse of the `$450`. Never remainder `-$50`. Resolves under N5's inherited posture: composing claims retracted; dependent result **blocks**.

**Schedule B surface.** `$400` ≯ `$1,500`. Block is on line 2b / dependent nominee result, not on a Schedule B row.

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N6b-STALE** | Keeps reduction `$450` against the new `$400` report | Run-local reduction still `$450` after recompute |
| **N6b-NEG** | Remainder `-$50` | Negative share |
| **N6b-GROSS** | Publishes `$400` as a settled unreduced taxable-interest number | Line 2b published rather than blocked (Decision 10) |

---

### N7 — corrected allocation (T0-F2 discriminator)

**Facts (specified case).** The amount allocated to one other owner changes `$450` → `$400`. Prior consequences become non-current; replacement reduction `$400`; taxpayer's replacement share `$800`.

**Discriminator exposure (T0-F2), without selecting a shape.** The specified numbers are the N2 lifecycle (one `$450` owner). The cardinality discriminator is the product behavior T0-A named: if a **second** owner's current statement exists (N4: `demo.owner.kim` `$150`), correcting Pat's amount must not rewrite Kim's current statement. This trace states that observation. It does not choose per-owner facts, a list-valued object, or any other shape, and it does not reopen R-A/R-B.

**Schedule B surface.** Attachment not required. Replacement `$400` / `$800` observed on line 2b / run-local derived finding.

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N7-STALE** | Leaves reduction `$450` / share `$750` current | After recompute, not `$400` / `$800` |
| **N7-REWRITE-OTHER** | A whole-set replacement that rewrites another owner's current statement | Given Kim `$150` current, after Pat `$300`→`$250` (or N2's `$450`→`$400` in a two-owner workspace), Kim's finding id, value, owner, and asserting act are not the pre-correction statement. This is the T0-F2 discriminator. Catching it does **not** select the shape that would prevent it |
| **N7-ATTR** | Replacement determination shown without who supported the corrected ordinary statement | Same reader-facing gap as N2-ATTR on the new `$400` |
| **N7-DISP** | Claims ADR-0010 displacement as the currency mechanism | Run-local re-derivation only (artifact 3) |

---

### N8 — legacy and canonical coexistence (T0-F4; claim-reuse case)

**Facts.** Legacy `$450` adjustment (`tax.us.2025.scheduleb.adjustment.nominee.amount`) **and** a new ordinary-fact-derived `$450` consequence describe the **same circumstance**. Same dollars; **not** the same proposition (artifact 4).

Legacy type, walked from `packages/content/tax/2025/scheduleb-adjustment.nominee.bundle.json` `fact_types[0]`: `identity_keys` are literal tax-year `"2025"` and entity `tax.us.scheduleb-adjustment-instance`; `value_schema` `{minimum: 0, type: number}`; `supersession.policy: "free"`; title: "identity is exactly the tax year plus logical adjustment instance and never an evidence, file, upload, scan, or document identifier." No owner, no report, no allocation basis (P2 E18, reused).

Family `packages/content/tax/2025/family.scheduleb-adjustment.nominee.json`: `member_predicate.fact_type` is that amount; `authorizes_subtotal` `tax.us.2025.interest.scheduleb-nominee-subtotal`.

Line 2b v6 `value` (`packages/content/tax/2025/rule.form1040-line2b.v6.json`): `subtract` of an `add` that includes `tax.us.2025.interest.scheduleb-nominee-subtotal` and `tax.us.2025.interest.current-year-adjustment-subtotal`. A second ordinary-fact-derived subtractand that also reached line 2b would double-count.

**Required result.** One subtraction **or** an explicit migration/refusal: reduction `$450`, share `$750`. **Never** doubled reduction `$900` and share `$300`. No silent conversion of the legacy amount into an ordinary ownership claim (T0-A P-T1 legacy seam; ADR-0072 Decision 1 posture, nominee not named).

**Schedule B surface.** If the attachment is required, v4/v5 `collect_members` will itemize the **legacy** amount as "Nominee Distribution" (`rule.attachment.schedule-b.v5.json` `itemizations[0].adjustment_rows[0]`). A canonical ordinary-fact-derived reduction has **no committed row**. Default `$1,200` still does not require the attachment; the double-subtraction kill is on line 2b.

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N8-DOUBLE** | Subtracts both the legacy `$450` and the ordinary-fact-derived `$450` | Line 2b reduced by `$900`; share `$300` |
| **N8-CONVERT** | Treats the legacy amount as the ordinary allocation (owner, report, belonging, reporting evaluation) | Legacy finding used as if it named `demo.owner.pat` or `demo.1099int.statement-a`, or as formulation-1/2/3 evidence |
| **N8-REUSE** | Treats the two `$450`s as the same claim because the dollars match | Fails artifact 4's three tests (below) and still publishes one fused proposition |

---

### N9a — wrong-problem control, erroneous form

**Facts.** User says the payer's form amount itself is erroneous.

**Required result.** Route to corrected-document handling; do not manufacture nominee ownership. No nominee reduction.

**Schedule B surface.** No nominee row; attachment state unchanged by this routing.

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N9a-NOM** | Captures a nominee allocation or derives a nominee reduction from "the form is wrong" | Any current nominee allocation or nonzero nominee reduction |
| **N9a-LABEL** | Asks the user to choose the tax label "nominee" vs "corrected form" | Intake requests a Schedule B / 6049 / nominee classification |

---

### N9b — wrong-problem control, accrued interest (claim-reuse of the gating "yes")

**Facts.** The taxpayer bought a bond between interest dates and reimbursed the seller for interest the form will report to them, and answers the gating question **"yes, some of this belongs to someone else."** The ordinary sentence is nearly identical to N2's.

Committed accrued mapper (`packages/tax/obligation_acquisition_mapping.py` lines 9–30, 66–114): subject is exactly that acquisition circumstance; `ORDINARY_ANSWERS_SCHEMA` is `additionalProperties: false` and has `accrued_interest_paid_to_seller`, not a nominee owner/amount. It cannot accept nominee fields.

**Required result.** Route to the **accrued-interest** translation already accepted; derive **no nominee reduction**; manufacture no nominee ownership. Distinguish circumstances by what is elicited, not by the words "yes" / "belongs to someone else." Do not reopen accrued-interest semantics.

**Schedule B surface.** No nominee row. Under package v34, Schedule B v4 may itemize a **legacy accrued** row; under v35, Schedule B v5 has no accrued row. A nonzero **pairing-scoped** current-year adjustment is subtracted at line 2b on **both** packages and itemized by **neither** (T0-F5). If the attachment is required and tie-out runs, `ITEMIZATION_TIE_OUT_VIOLATION` may fire from that neighboring subtractand. **Do not attribute that failure to nominee interest.** N9b's nominee kill is "no nominee reduction," observed on the nominee subtractand / allocation capture, not on that tie-out.

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N9b-CAPTURE** | Captures a nominee allocation from the gating "yes" without eliciting circumstance | A current nominee allocation to the seller; nominee reduction ≠ `$0` |
| **N9b-YES** | Treats the same gating "yes" as the same circumstance as N2 | Artifact 4 fails: N2's nominee proposition and N9b's purchase-reimbursement proposition are fused |
| **N9b-MAPPER** | Overloads `obligation_acquisition_mapping.py` with nominee fields | Mapper accepts a nominee owner/amount (schema forbids unrecognized fields; overloading would be a schema/product change this rung does not make) |
| **N9b-TIE** | Attributes a Schedule B `ITEMIZATION_TIE_OUT_VIOLATION` to nominee interest | The violation's missing row is the pairing-scoped current-year-adjustment subtotal (T0-F5), not `nominee_distribution` |

---

### N10 — ownership without established payment (T0-F3 kill trace; reporting-touching)

**Facts.** Report `$1,200`. User states `$450` belongs to `demo.owner.pat`. **No** onward payment, credit, or distribution to that owner has been established. Absence of payment is **not** a negative payment declaration (T0-A §4).

**Required result.** Reduction **supported**: `$450` / remainder `$750`. Must **not** be suppressed for want of payment. Schedule B's stated condition is belonging, "even if you later distributed some or all of this income to others" (P2 E1/E2, plan A1). Ownership alone does **not** establish literal § 6049(a)(2)'s payment conjunct, does not prove one normalized reporting obligation, and does not satisfy every formulation. It **may** support explicitly attributed IRS filing-instruction guidance, which must not be suppressed.

**Independent gating and statement-specific dependency** (T0-A P-T1a / T0-F3). The belonging-supported reduction pins the allocation finding, attached report, supportability, and rule — **not** the payment finding. Each authority-indexed output pins the facts **its own attributed statement actually reads**: formulation 1 **necessarily** requires the payment/credit fact, since its second conjunct is about payments; a **regulation-attributed statement pins payment, credit, setting-apart, collection, or intermediary facts only where that statement relies on them**, and one limited to the actually-owned-portion language does not invent or pin payment. The formulations remain unreconciled and no blanket claim is made about them. **Payment never gates or pins the belonging-supported reduction.** Payment/credit is **necessarily** an input to formulation 1, whose second conjunct is about payments. For the other, unreconciled formulations the dependency is **statement-specific**: a regulation-attributed statement relying on payment, credit, setting-apart, collection, or intermediary facts pins those facts; one limited to the actually-owned-portion language does not invent or pin payment. Payment never gates or pins the belonging-supported reduction.

**Schedule B surface.** Attachment not required by `$1,200`. Reduction is on line 2b / run-local derived finding even when there is no nominee row.

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N10-SUPPRESS** | Suppresses the `$450` reduction because payment is absent | Reduction `$0` or dependent result blocked **for want of payment** |
| **N10-PIN** | Gates or pins the belonging-supported reduction on payment, so a payment fact would displace it | **Not observable on N10's own facts, and deliberately not asserted as if it were.** N10's defining fact is that **no payment finding exists**, and committed pin construction cannot pin an absence: `packages/derivation/runner.py` lines 365–372 skip a ref whose source is `None` ("Absence is recorded in the disposition's missing list; it has no finding identity to pin"), and `derived-finding.v2` pins are `minItems: 1` refs with no absent form. So "pins include a payment/credit finding id" is **vacuously false for a conforming run and for a shared-gate run alike** — the latter is caught by `N10-SUPPRESS` (missing-list block), not here. **The pin-topology contract for this seam is `N2-PAYGATE`**, where a payment finding actually exists; T0-C must copy that one. If a later-payment sequence is ever instantiated — compute the belonging-supported `$450`, then attest payment **without** changing belonging, then recompute — the observation is that the new run-local reduction remains `$450` and its **`input`/`choice`** pins (the ADR-0010 Decision 4 roles that make shared pins displace) still exclude the payment finding id |
| **N10-NORM** | Silently asserts one information-reporting obligation from the allocation | A product finding "6049 required" / "must file" with no authority name, or a ranking of the three formulations |
| **N10-TIPDROP** | Suppresses attributed IRS filing-instruction guidance because the statutory payment conjunct is unestablished | Formulation 2's attributed TIP/1099GI sentence is omitted **because** formulation 1's second conjunct is absent |
| **N10-ATTR** | Determination shown without who supported the ordinary `$450` statement | N2-ATTR on this path |
| **N10-INFERPAY** | Infers that payment, credit, or setting-apart occurred from the allocation | A payment fact appears in current findings with no assertion of payment |

#### N10 formulation × facts × surface

| Formulation | Facts present | Facts absent | What may be surfaced (authority named) | Qualify or defer |
| --- | --- | --- | --- | --- |
| **1. Literal § 6049(a)(2)** | Ordinary nominee-receipt statement for `$450` | **Payment, credit, or setting-apart** with respect to that interest; therefore the `$10` aggregation of such payments is also unestablished | Attributed to **IRC § 6049(a)(2)**: the statute is conjunctive. The second conjunct is unestablished in this scenario. **Do not** surface a statutory return as required | Qualify: formulation 1's own terms are not met on the stated facts. Do not infer the conjunct from belonging |
| **2. IRS filing instructions** | Form 1099 in the taxpayer's name; ordinary statement that `$450` actually belongs to `demo.owner.pat`; non-spouse | Later-payment conjunct (not asked by E11/E3) | Attributed as **IRS filing-instruction guidance** (1099GI E11; Schedule B TIP E3): receiving a 1099 for amounts that actually belong to another person / receiving interest as a nominee — file one return per other owner showing amounts allocable. This is **not** a finding that § 6049(a)(2) is satisfied | Must **not** be suppressed. Must not be rewritten as the statute |
| **3. 26 CFR 1.6049-4** | Ordinary statement of an actually-owned portion `$450` | Payment / credited-or-set-apart fact. Ranking of the actually-owned-portion sentence (P2 unknown 5) | Attributed to **26 CFR 1.6049-4(f)(4)**: the retrieved actually-owned-portion sentence does not, in the retrieved text, restate a subsequent-payment conjunct. Quote that sentence only, named as the regulation | **Defer** any product conclusion that this sentence, without payment, is or is not the Secretary's implementation of (a)(2). Do not rank it against formulation 1 or 2 |

Honest surface (P2 N10 outcome, reused): reduction evaluated on belonging; reporting evaluated on its own predicate, which on the statute is not met; form-instruction guidance may be explained as form-instruction authority.

---

### N11a — two same-payer reports, one valid allocation (reporting-touching)

**Facts.** Two distinct box-1 reports, same payer `demo.payer.alpha`, same year: report A `demo.1099int.statement-a` `$1,200`; report B `demo.1099int.statement-b` `$800`. Allocation `$450` attached to **report A only**. Payment is **not** supplied (not invented).

ADR-0015 Decisions 1 and 3: a 1099-INT fact is keyed by tax year, subject, payer, and a logical statement-instance; "Multiple original returns from one payer are distinct statement instances, including multiple returns concerning one account." Bundle `identity_keys` include both payer and statement; same-payer identity must not collapse the reports.

**Required result.** Reduction `$450` and remainder `$750` stay **associated with report A**. Report B: reduction `$0`, remainder `$800`. **No leakage.** Evaluate formulations on their own terms for any information-reporting result.

**Schedule B surface.** `interest.positive-total = 1200 + 800 = 2000` > `1500` → interest **independently requires** Schedule B, provided `dividends.ordinary-total` is present (including authorized zero). If dividends are absent, the **whole** attachment blocks (`BLOCK_ABSENT`); **no** Part I rows for A or B and **no** nominee row, while line 2b still computes A `$750` / B `$800` into the box-1 subtotal then the nominee subtractand. When required and published, Part I must list **both** reports; a paper-canonical reduction still has no committed nominee member row unless a legacy amount is also present (N8 is a different case).

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N11a-LEAK** | Allocation reduces report B | B remainder ≠ `$800` or B carries a `$450` reduction |
| **N11a-COLLAPSE** | Same-payer identity merges A and B into one `$2,000` report | One statement instance; or supportability evaluated against `$2,000` |
| **N11a-SWAP** | Reduction `$450` associated with B or with the payer rather than with A | Report-scoped remainder A ≠ `$750` |
| **N11a-ROW** | Assumes a Schedule B nominee row exists even when the attachment is blocked or not required | A test or explanation that requires `nominee_distribution` rows while `dividends.ordinary-total` is absent, or while no subtotal exceeds `$1,500` (this case *does* exceed on interest, so the dividend-absent block is the live T0-F6 path) |

#### N11a formulation × facts × surface

Payment is **absent** (not in the case). Allocation is report-A-scoped.

| Formulation | Facts present | Facts absent | What may be surfaced (authority named) | Qualify or defer |
| --- | --- | --- | --- | --- |
| **1. Literal § 6049(a)(2)** | Nominee-receipt statement for `$450` of **report A** | Payment/credit/setting-apart; any allocation on report B | Attributed to **IRC § 6049(a)(2)**: second conjunct unestablished. Do not surface a statutory return as required. Do not evaluate (a)(2) against report B's `$800` | Qualify formulation 1. Do not leak A's allocation into B's reporting evaluation |
| **2. IRS filing instructions** | 1099 for A; ordinary belonging `$450` of A's interest to a named non-spouse | Payment conjunct (not asked); belonging statement about B | Attributed as **IRS filing-instruction guidance** for the allocable `$450` of **A**. B has no belonging statement, so do not surface a nominee 1099 for B | Do not suppress A's attributed guidance. Do not treat B's same-payer 1099 as A's |
| **3. 26 CFR 1.6049-4** | Actually-owned-portion statement for `$450` of the interest payment reported on A | Payment onward; any such statement about B; ranking unknown | Attributed to **26 CFR 1.6049-4**, scoped to the portion of **A**. Quote the regulation's own sentences only | Defer ranking. Do not treat B as middleman-evidence |

---

### N11b — allocation unsupportable on its own report

**Facts.** Same payer, same year: report A `$300`, report B `$800`, allocation `$450` attached to **A only**. `$450` exceeds A alone and is less than the combined `$1,100`.

**Required result.** `$450` is **not supportable** against the report it is attached to and contributes no reduction. Output follows N5, applied to report A: composing claims retracted; A's dependent nominee result **blocks**. **Report B is unaffected at `$800` regardless.** Under no disposition may `$450` be accepted by drawing on the combined `$1,100`. T0-A: B's *report remainder* `$800` is no-leakage / no borrowed support, not a licence to publish line 2b while A's set is unsupportable. Under Decision 10 the dependent nominee-subtotal / line 2b **blocks**.

**Schedule B surface.** `interest.positive-total = 300 + 800 = 1100` ≯ `1500` → interest does **not** independently require Schedule B. No nominee row unless dividends require it. The block is on line 2b / A's dependent result. If dividends require the attachment, both reports still list; A's unsupportable allocation still contributes no reduction.

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N11b-MERGE** | Evaluates supportability against combined `$1,100` and accepts `$450` | Reduction `$450` published; A remainder `$−150` or `$0` by borrowing B |
| **N11b-BORROW** | Leaves A and B distinct but uses B's `$800` as slack for A's `$450` | Same published `$450` reduction; B remainder reduced below `$800` **or** A treated as supportable |
| **N11b-LEAK** | Reduces B | B remainder ≠ `$800` |
| **N11b-GROSS** | Publishes line 2b as unreduced `$1,100` (or `$300+$800`) as ordinarily computed | Decision 10 violation: dependent result published rather than blocked |
| **N11b-TIE** | Attributes any `ITEMIZATION_TIE_OUT_VIOLATION` to this unsupportable nominee allocation | Tie-out, if it fires, is T0-F5's pairing-scoped gap or a missing required subtotal, not "nominee over-allocation" |

Merging and borrowed support are **separately** observable (plan N11b "What it tests").

---

### N12 — payment without established ownership (T0-F3 converse kill trace; reporting-touching)

**Facts.** Report `$1,200`. An onward payment, credit, transfer, or distribution to `demo.owner.pat` **is** established. **No** ownership allocation has been established. "No allocation recorded" is the N1a non-claim, not a denial.

**Required result.** Reduction `$0`, remainder `$1,200`. **Payment alone does not establish belonging or the Schedule B reduction.** Ask for the missing ordinary ownership fact rather than inferring it. Nominee receipt is unestablished. Whether the transfer independently falls within another § 6049 route (e.g. (a)(1) "payments of interest" as defined by (b)) is a **preserved unknown** and must **not** be closed by reasoning (plan A4 / P2 unknown 1).

**Schedule B surface.** Attachment not required by `$1,200`. No nominee row. Line 2b remainder `$1,200`.

**Kills.**

| ID | Lying implementation | Observation that catches it |
| --- | --- | --- |
| **N12-INFEROWN** | Infers a `$450` (or any) nominee reduction from the payment | Reduction ≠ `$0` |
| **N12-BELONG** | Treats cash movement as establishing that the interest "actually belongs" to the payee | An allocation statement or belonging finding appears with no ownership assertion |
| **N12-A1** | Closes the preserved unknown by reasoning that the onward transfer is § 6049(a)(1) "payments of interest" | A product finding of an (a)(1) original-payor obligation from this transfer |
| **N12-NORM** | Infers a normalized reporting obligation from payment alone | "Must file 1099" with no authority name, or a selected/combined formulation |
| **N12-SHARED** | Shared-gate: the reduction and the reporting evaluation hang off one payment gate, so payment alone drives both | **Pin observation, which N12 can actually support** because a payment finding *does* exist here. Whatever the reduction's disposition, inspect its **`input`/`choice`** pins (ADR-0010 Decision 4 roles): the payment finding id must **not** appear among them, and no published reduction may take the payment finding as a dependency pin. This is the topology check `N10-PIN` cannot make on its own facts, sited where the finding exists. The dollars-only observation belongs to `N12-INFEROWN` and is not restated here |

#### N12 formulation × facts × surface

| Formulation | Facts present | Facts absent | What may be surfaced (authority named) | Qualify or defer |
| --- | --- | --- | --- | --- |
| **1. Literal § 6049(a)(2)** | Onward payment/credit/distribution to `demo.owner.pat` (amount as stated in the scenario; if ≥ `$10`, the threshold fact is present **as a payment fact only**) | **"As a nominee" / belonging / allocable amount.** No ordinary ownership statement | Attributed to **IRC § 6049(a)(2)**: the first conjunct is unestablished, so (a)(2) is not met on these facts. Do not surface an (a)(2) return as required | **Defer** whether the same transfer is independently (a)(1). Do not close that unknown by reasoning |
| **2. IRS filing instructions** | A 1099-INT was received by the taxpayer; a payment to another person occurred | "Amounts that actually belong to another person" (E11); "received interest as a nominee" (E3). Trade-or-business payer status is **not** in the scenario | Do **not** surface the nominee/middleman filing instruction as applicable: its belonging/nominee-receipt terms are unestablished. **Formulation 2's closed identity is 1099GI "Nominee/middleman returns" (E11) plus the Schedule B TIP (E3) — see §7.4. The 1099-INT filer instructions (E10) are not part of it**, and are noted here only as a separate form-instruction source whose own disjuncts (trade-or-business payer, or nominee/middleman status) are likewise unestablished on these facts | Qualify/defer. Ask for the missing ordinary ownership fact rather than inferring it. Do not treat E10 as silently proving (a)(1) |
| **3. 26 CFR 1.6049-4** | A payment to another person | Actually-owned portion; collecting-on-behalf-of; intermediary role as established facts. Ranking unknown | Do **not** surface the actually-owned-portion sentence as met. Whether "makes payment of interest for … another person" applies to an onward transfer without established ownership is the same unverified (a)(1)-adjacent question | **Defer.** Do not infer middleman status from payment alone |

---

## 9. Late-authority trace (adversarial-closure artifact 3)

`PROJECT_PLANNING.md` `## Track 0 Adversarial Closure Gate` artifact 3 requires every aggregate declaration to run:

```text
attest → close → compute → add member → reclose → recompute
```

At every transition, name which prior facts, findings, closures, and publications become unusable and why. "A declaration that remains current after the authority it summarizes changes is a `FAIL`."

The charter instantiates that sequence for this milestone as: **attest, compute, then correct the report (N6a/N6b) or the allocation (N7), then recompute.** Currency is **run-local re-derivation**, not act-log displacement. Charter closed item 8: do **not** claim ADR-0010 displacement; do not select a publication-schema repair; do not require act-log persistence of derived findings.

ADR-0010 Decision 5: a derived value "is not *corrected* in place — it is *re-derived*." Decision 6: "Displacement propagation only; re-derivation is out of scope." Those sentences describe persisted `derived-publication` envelopes this milestone does **not** claim. Production does not call `append_publications` (T0-A §3.3; P3-D1). This trace observes: a new run against **current** kernel findings produces new `RunResult` publications; the previous run's derived numbers are unused because they are not re-derived from current inputs.

**Aggregate declarations in play** (from T0-A §4, not reinvented): box-1 family closure; legacy nominee family closure (closed empty except N8); the run-local derived nominee-distribution reduction (aggregate of the current supportable allocation set against the attached report).

### 9.1 Shared starting sequence

Synthetic workspace, N2 numbers, payment present as in N2 but **not** on the reduction's pin set (**`N2-PAYGATE`** — the payment finding exists on these facts, which is what makes the pin observation discriminative here; `N10-PIN` cannot be checked on N10's own facts, where no payment finding exists).

| Step | What happens | What is current | What becomes unusable |
| --- | --- | --- | --- |
| **Attest** | Box-1 `$1,200` on `demo.1099int.statement-a`; ordinary allocation `$450` to `demo.owner.pat`; separate payment `$450` to Pat; other line-2b families empty | Kernel findings only. No derived reduction yet | Nothing derived exists to stale |
| **Close** | Current-literal-true closures on box-1, legacy nominee (empty), ABP (empty), and the other six line-2b families, each on its current family-horizon | Closures authorize those families' subtotals, including zeros. They do **not** attest "the taxpayer owns `$1,200`" and do **not** manufacture an allocation-absence declaration (T0-A §4) | A closure naming a stale horizon is a hard projection error (ADR-0017, T0-A table). None is stale yet |
| **Compute** | Run-local: supportable reduction `$450`, remainder `$750`. Line 2b subtracts the nominee subtractand once it is published. Attachment **not required** (`1200` ≯ `1500`) | Run-local derived reduction `$450` / share `$750`, pinned to the **current** allocation finding id and the **current** report finding id | Prior non-existence of a reduction is not a claim; it simply ends |

Schedule B: no nominee row (not required). Dividend-absent `BLOCK_ABSENT` would hide a row if one existed; it would not stale these closures or the line-2b arithmetic.

### 9.2 Add member → reclose → recompute (generic artifact-3 limb)

Two member-additions, because two aggregates can change membership.

**Limb A — add a second allocation (derived-reduction aggregate).** After §9.1, attest `$150` belonging to `demo.owner.kim` against the **same** report (N4's second owner), with Kim's own payment fact. Membership of the allocation **set** grows. Box-1 membership is unchanged, so the box-1 closure does **not** stale from this add.

| Step | What happens | What becomes unusable | FAIL if |
| --- | --- | --- | --- |
| Add member | Kim `$150` current | The run-local `$450` reduction / `$750` remainder from §9.1 Compute. That publication summarized a one-owner set | The `$450`/`$750` run-local publication is treated as still current |
| Reclose | No box-1 reclose required. Do not invent a canonical allocation-family closure (T0-A: not committed, not invented) | — | Inventing a closure for the deferred representation |
| Recompute | Aggregate reduction `$600`, remainder `$600`, still supportable against `$1,200` | — | Publishing `$450` or choosing to drop Kim or Pat (N5 allocation policy, not applicable — `$600 ≤ $1,200`) |

T0-F2: Kim's add must not rewrite Pat's current `$450` statement (N4-COLLAPSE / N7-REWRITE-OTHER).

**Limb B — add a second box-1 report (family-closure aggregate).** From §9.1 (before Limb A, to keep numbers simple), add `demo.1099int.statement-b` `$800` (N11a), **without** attaching an allocation to B.

| Step | What happens | What becomes unusable | FAIL if |
| --- | --- | --- | --- |
| Add member | New box-1 member. ADR-0023: member-transition adding a member **advances the family-horizon** | The §9.1 box-1 source-closure, which named the prior horizon. T0-A table: "Member-transition adding or removing a box-1 member advances the horizon and stale-closes this attestation" | The old box-1 closure remains current after the add |
| Reclose | Attest source-closure true on the **new** horizon | — | Computing line 2b / `b1-subtotal` against the stale closure |
| Recompute | `b1-subtotal = 2000`; A's reduction still `$450` / remainder `$750`; B reduction `$0` / remainder `$800`; `interest.positive-total = 2000` now **requires** Schedule B (interest limb of T0-F6) | The §9.1 judgment that the attachment was not required. A's `$450` reduction is **not** invalidated by B's existence (N11a-LEAK would be the lie) | Collapsing A+B; leaking `$450` onto B; treating the old "attachment not required" as still true |

### 9.3 Correct the report (N6a / N6b) → recompute

Same-identity amount correction is **not** a member add. Box-1 membership is unchanged, so the box-1 closure's horizon does **not** stale merely because the amount moved (T0-A: N6a invalidates the prior **amount finding**, not by itself the family closure). ADR-0015 Decision 4: same fact, superseded finding.

**N6a.** `$1,200` → `$1,000`; allocation `$450` still supportable.

| Transition | Unusable | Current after recompute | FAIL if |
| --- | --- | --- | --- |
| Correct report | Prior box-1 finding `$1,200` (superseded). Run-local remainder `$750` and any explanation tree built on the `$1,200` pin | Reduction `$450`, remainder `$550`, same report identity | Stale `$750`; new statement instance; ADR-0010 displacement claim |
| Recompute | — | New run-local publications pinned to the **current** `$1,000` finding id | Reusing the previous `RunResult` |

**N6b.** `$1,200` → `$400`; allocation `$450` now unsupportable.

| Transition | Unusable | Current after recompute | FAIL if |
| --- | --- | --- | --- |
| Correct report | Prior `$1,200` finding; run-local reduction `$450` and remainder `$750` | Supportability fails; composing claims retracted; dependent result **blocks**; never `-$50` | Stale `$450`; negative remainder; unreduced `$400` published as settled (N5-GROSS) |
| Recompute | — | Blocked dependent nominee result / line 2b | A second run that still publishes `$450` |

The allocation **statement** `$450` is not rewritten by the report correction. Supportability failure makes the **derived** reduction unusable; it does not change the ordinary statement (T0-A §4 ordinary-allocation row).

### 9.4 Correct the allocation (N7) → recompute

| Transition | Unusable | Current after recompute | FAIL if |
| --- | --- | --- | --- |
| Correct allocation `$450` → `$400` | Prior allocation finding `$450`; run-local reduction `$450` / remainder `$750` | Replacement reduction `$400`, share `$800`. Prior consequences non-current | Stale `$450`/`$750`; rewriting a second owner's current statement (N7-REWRITE-OTHER) |
| Recompute | — | New run-local publications pinned to the **current** `$400` allocation finding id | ADR-0010 displacement claim; payment-pin displacement of the reduction (**`N2-PAYGATE`**, not `N10-PIN`) — this is an **allocation-correction** sequence in which payment did not change, so it falsifies a shared payment pin only in that direction; a later-payment-without-belonging-change sequence is not instantiated anywhere in this checkpoint |

If Kim `$150` is also current, Pat's correction must leave Kim's statement current. A declaration that "the allocated-away set is `$450`" remaining current after Pat's amount changed is a **FAIL**.

### 9.5 Artifact 3 disposition

**PASS.** The paper trace names, at each transition, the prior run-local publications and (for Limb B) the prior box-1 closure that become unusable, and why. No declaration is left current after the authority it summarizes changes. Mechanism: **run-local re-derivation from current kernel findings**, not ADR-0010 act-log displacement.

---

## 10. Claim-reuse proof (adversarial-closure artifact 4)

`PROJECT_PLANNING.md` artifact 4: a reused claim passes only when Track 0 demonstrates all three **independently**:

1. the same real-world proposition;
2. the same identity and lifecycle; and
3. the same declared authority scope and explanation.

"A matching storage shape, a downstream annotation, or an apparently narrow title cannot redefine or broaden the source declaration."

### 10.1 N8 — same dollars are not the same proposition (T0-F4)

Two current `$450` figures in one workspace, describing the same circumstance as N8 states.

| Test | Legacy `tax.us.2025.scheduleb.adjustment.nominee.amount` `$450` | Ordinary-fact-derived `$450` reduction | Same? |
| --- | --- | --- | --- |
| **Proposition** | A nonnegative preclassified nominee-adjustment amount for one logical Schedule B adjustment instance. Establishes that a fact type can carry that number. **Does not** establish actual-owner identity, report association, allocation basis, or why the amount belongs elsewhere (T0-A §4; P2 E18) | Attributed ordinary statement that `$450` of `demo.1099int.statement-a` is `demo.owner.pat`'s, after N9b routing, used as bounded evidence for a supported Schedule B determination. **Does not** establish belonging (claim boundary) | **No.** Same dollars, different propositions |
| **Identity and lifecycle** | `identity_keys`: tax-year `"2025"` + `tax.us.scheduleb-adjustment-instance`. Free same-identity correction. Family membership of `tax.us.2025.scheduleb.adjustment.nominee`. No owner key, no statement key | Canonical identity **not selected** (R-A/R-B deferred). Whatever it is, it is evaluated against a named report and a named owner (N11, N4). Invalidated by allocation correction (N7) or by supportability against **that** report (N5, N6b, N11b) | **No.** Tax-year + adjustment-instance is not report+owner. Matching `$450` cannot rekey one into the other (ADR-0072 Decision 2 is an accrued-interest amount-equality **collision trigger**, not a transferred identity; T0-A: analogy, not inherited mechanism) |
| **Authority scope and explanation** | Scope: that adjustment instance in 2025. Explanation/label: Schedule B v4/v5 `collect_members` "Nominee Distribution" tied to `scheduleb-nominee-subtotal`. Closure authorizes **that subtotal only** | Scope: the allocation as currently asserted (one owner, amount, attached report at evaluation). Explanation must identify the assertion act, payer report, rule, and authority (plan N2). Reader-facing consumers currently omit **who** (N2-ATTR / T0-F1) | **No.** Legacy explanation cannot name Pat, the report, or the asserting actor, because those fields do not exist on the type |

**Reuse verdict: FAIL the three tests — therefore the claims must not be reused as one.** Publishing one fused `$450`, or subtracting twice, is N8-DOUBLE / N8-CONVERT / N8-REUSE. Required operational result remains one subtraction or an explicit migration/refusal: `$450` / `$750`, never `$900` / `$300`.

### 10.2 N9b — the same gating "yes" is not the same circumstance

| Test | N2 after routing: "yes, `$450` of this 1099-INT is `demo.owner.pat`'s; I received/held it for them" | N9b: "yes, some of this belongs to someone else" **and** the elicited circumstance is a bond purchase reimbursing the seller for pre-acquisition accrual | Same? |
| --- | --- | --- | --- |
| **Proposition** | Interest received or held for another owner; bounded evidence for Schedule B "Nominee Distribution" | Buyer reimbursed the seller for accrued interest the form will report to the buyer; companion consequence is basis plus current-year adjustment, taxable to the **seller** (P2 E5/E14, reused) | **No.** Who the other person is, whether acquisition is the distinguishing event, who is taxed, and the companion consequence all differ (T0-A §2 table) |
| **Identity and lifecycle** | Ordinary allocation statement (identity not selected) attached, at evaluation, to a report | `tax.us.obligation-acquisition-circumstance` via the accrued mapper; pairing to a report (ADR-0068); pairing-scoped rules (ADR-0071) | **No.** Closed mapper schema has `accrued_interest_paid_to_seller`, not a nominee owner/amount (`additionalProperties: false`) |
| **Authority scope and explanation** | Schedule B belonging instruction (plan A1); reporting formulations evaluated separately | Accrued-interest form instruction and Pub 550 (explanatory) for the buyer/seller split; ADR-0070/0071 for supportability and dual consequences **behind a shared supportability gate** — which is **not** nominee independent gating (T0-F3) | **No.** N9b must produce **no** nominee reduction. Label, if any, is "Accrued Interest" on v4's legacy row, not "Nominee Distribution" |

**Reuse verdict: FAIL the three tests.** The gating "yes" is an interaction event, not a claim. Reusing N2's nominee claim from N9b's "yes" is N9b-YES / N9b-CAPTURE.

### 10.3 Artifact 4 disposition

**PASS** as a proof: N8's two `$450`s and N9b's gating "yes" versus N2 **do not** satisfy the three reuse tests. They are not reusable as the same claim. No other reuse of a contributed ordinary statement, payer report, payment fact, or legacy nominee amount as a different proposition is licensed by matching dollars, a shared "yes", a downstream annotation, or a title.

---

## 11. T0-B findings

No new T0-F identifier. T0-A's T0-F1–T0-F6 constrained the traces and are discharged as named kills, not redesigned.

| T0-A finding | How T0-B used it |
| --- | --- |
| T0-F1 | Named kill **N2-ATTR** (also N4-ATTR, N7-ATTR, N10-ATTR). No explanation-extension design |
| T0-F2 | Discriminator kills **N4-COLLAPSE**, **N7-REWRITE-OTHER**. No shape selected |
| T0-F3 | Independent-gating kills **N10-SUPPRESS**, **N12-INFEROWN**, **N12-BELONG**, and the pin-topology checks **N2-PAYGATE** and **N12-SHARED**, plus the N10/N12 formulation tables. `N10-PIN` is retained as a *named non-observation* on N10's facts, with `N2-PAYGATE` carrying the pin contract |
| T0-F4 | N8 kills and artifact 4 §10.1 |
| T0-F5 | §7.3; **N9b-TIE**, **N11b-TIE**. Tie-out not attributed to nominee |
| T0-F6 | §7.3; every case's Schedule B surface; **N11a-ROW** |

Paper did not hit a technical-capability question that requires a spike.

---

## 12. Explicit unknowns (carried; not reopened)

T0-A's unknowns 1–9 remain. T0-B adds none that paper was supposed to close.

Still not selected, combined, or ranked: the three reporting formulations. Still deferred: R-A vs R-B; per-owner shape after T0-F2; explanation-extension shape; N12's possible other § 6049 route; successor/coexistence mechanism for N8 (T0-C). Still neighboring, not repaired here: T0-F5 itemization limitation.

---

## 13. Questions returned rather than answered

None at T0-B. Owner cardinality remains a named decision for T0-C (T0-F2), not a spike. Formulation relationship remains unreconciled by design.

Adversarial-closure artifacts 3 and 4: **PASS** (run-local late-authority; N8/N9b fail reuse as required). Artifacts 5–6 are T0-C.



T0-B COMPLETE

---

# T0-C — synthesis

| | |
| --- | --- |
| Seat | Builder, Track 0 checkpoint T0-C |
| Source ref | `HEAD` at pickup = `f4369ba9322dfdfa23b50f8512340490823dde8a` |
| Plan blob (authoritative pin) | the milestone plan |
| Branch | `milestone/nominee-interest-ownership-translation` |
| Evidence rung | PAPER. No prototype code, tests, experiments, or spikes. Quotes are from committed artifacts. Running an existing test would be a labelled OBSERVATION; none was required. |
| Established input | T0-A and T0-B in this file, including the T0-B repairs absorbed from the independent review. Dispositions, traces, formulation tables, and artifacts 1–4 are not reopened. |
| Writable path | this file only |

**Closed, not reopened:** P2's tax map; the three reporting formulations (never selected, combined, or ranked); P1-D1; R-A vs R-B (deferred — no rivals, no selection by preference; no accepted seam is claimed to govern the representation); attribution placement on the act; the claim boundary (nothing may "establish belonging"); N10/N12 non-inference; the durable-publication carrier gap (run-local `RunResult` only; no ADR-0010 act-log displacement claim).

**Contract-copy conditions (from the T0-B review, copied as load-bearing observations, not as the repaired ones):**

- **`N2-PAYGATE` together with `N12-SHARED` is the pin-topology contract** for independent gating. Pin roles named below are **`input`/`choice`** (ADR-0010 Decision 4) — the roles that make shared pins displace.
- **`N10-PIN` is a named non-observation.** This checkpoint writes **no contract clause and no later-test obligation from it**, because on N10's facts no payment finding exists and committed pin construction cannot pin an absence (`packages/derivation/runner.py` lines 365–372: "Absence is recorded in the disposition's missing list; it has no finding identity to pin. Present refs retain their ordinary pins"; `if source is None: continue`).
- **`N12-INFEROWN` and `N12-BELONG` carry the N12 inference contract.**
- **§7.4 defines formulation 2** — the 1099GI nominee/middleman paragraph plus the Schedule B TIP. **Not** N12's E10 clause; the 1099-INT filer instructions are a separate source.

**No successor producer of an externally bound symbol is proposed.** Artifact 6 is therefore **N-A**. A later unit that names a producer of `tax.us.2025.interest.scheduleb-nominee-subtotal` or `tax.us.2025.interest.taxable-total` (or any other symbol a consumer outside the derivation graph binds or joins on) **must produce artifact 6 under a fresh charter before any execution.**

---

## 14. Synthesis of the transfer dispositions

T0-A §6 disposed each seam of the plan transfer table (`docs/phases/tax-concept-derivation/milestones/nominee-interest-ownership-translation.md` `## Evidence and experiment architecture`, the milestone plan). T0-B applied those dispositions as traces and kills. This checkpoint consolidates them into what a production successor would have to contain. It does not re-derive them.

### 14.1 P-T1 — per seam

| Seam | Disposition (T0-A, not reopened) | What a production successor would have to contain |
| --- | --- | --- |
| Canonical object-valued ordinary fact + field-ref / owner cardinality | **New decision.** Accrued interest is one circumstance / one object-valued fact (`obligation-acquisition-circumstance`; ADR-0067 field-ref of `accrued_interest_paid_to_seller`). That "one current fact" shape does not transfer to arbitrary owner cardinality. Distinct from deferred R-A/R-B. | **The product constraint, not a selected storage shape.** Each owner's current allocation statement must be independently correctable: correcting `demo.owner.pat`'s amount must not rewrite `demo.owner.kim`'s current finding id, value, owner identity, or asserting act (`N4-COLLAPSE`, `N7-REWRITE-OTHER`). A single current fact holding the whole allocated-away set is **nonconforming**. Remaining representations that satisfy that constraint are **not selected** here — N1a–N12 do not discriminate them, and selecting among them by architectural preference is the same class of error the plan forbids for R-A/R-B. ADR-0067's field-ref *reading* pattern remains available if a later object-valued allocation fact is selected; that is not this seam's discriminator. ADR-0068 Decision 6 (multiple acquisitions on one report) is acquisition-specific text and is **not** claimed as contract transfer of the nominee representation. |
| Report association | **Bounded extension.** An allocation is evaluated against **one named report's current amount**. Representation (whether the allocation's own identity includes the report, or a separate pairing names it) stays deferred. | Report-scoped evaluation and remainder: N11a reduction `$450` / remainder `$750` stay on report A, report B remainder `$800`, same-payer identity must not collapse the reports (`N11a-LEAK`, `N11a-COLLAPSE`). N11b: `$450` attached to A (`$300`) is unsupportable on A and must not borrow B (`$800`) (`N11b-MERGE`, `N11b-BORROW`). N6a: recompute against the current amount of the **same** report identity (`N6a-REKEY` is the lie). Supportability is per-report, not pooled. No N1a–N12 case discriminates R-A from R-B (P3-F1, closed). |
| Supportability | **Transfer unchanged.** Inherit ADR-0070 Decisions 8–10. P-T1b: inherit; no deviation returned. | See §14.3. Production copies the posture, not a new nominee allocation policy. |
| Rule-owned consequences | **Bounded extension.** Independently gated consequences with independent explanation (independent pin sets). ADR-0071 Decision 2's **shared** supportability gate is the accrued precedent and **does not transfer**. | See §14.2. Two (or more) rule artifacts, each with its own gate and its own `input`/`choice` pins. Shared-gate dual publication is the kill (`N2-PAYGATE`, `N12-SHARED`, `N10-SUPPRESS`). |
| Ordinary-input mapping | **Bounded extension.** Circumstance routing **before** any nominee allocation is captured; N9b routed to the existing accrued translation; never a tax-label question. | The T0-A §2 routing box as a product property, not interface copy: elicit enough ordinary context after an affirmative gating answer to route nominee / accrued / other-or-uncertain; never ask the user for "nominee distribution," "accrued interest," a Schedule B line, or a tax result. Do **not** overload `packages/tax/obligation_acquisition_mapping.py` (`ORDINARY_ANSWERS_SCHEMA` is `additionalProperties: false` and has `accrued_interest_paid_to_seller`, not a nominee owner/amount; `N9b-MAPPER`). P1-D1: an explicit "no" is transient; durable state converges with N1a (`N1b-DURABLE`). N9a remains a separate document-correction route (`N9a-NOM`). Bounded Branch B reused: no ordinary-language producer of the legacy nominee amount in the searched production tree; production intake is new work, not a mapper edit. |
| Legacy coexistence | **Bounded extension.** No-silent-conversion **posture** transfers. ADR-0072's accrued-specific retirement, same-amount collision trigger, and migration-adoption **do not** already migrate nominee. | See §16. This checkpoint does **not** name a successor producer. Production that later does must satisfy the N8 account and produce artifact 6 under a fresh charter. |

No seam is **not needed**. Every seam in the plan table is load-bearing for at least one of N1a–N12.

### 14.2 P-T1a — independently gated consequences

**Disposition (T0-A, not reopened): yes.** Separately supported consequences require independently gated rules and independent explanation. Shared-gate dual publication does not transfer.

Quoted ADR-0071 Decision 2 (`docs/adr/0071-rule-owned-current-year-and-basis-consequences.md`): "Two separate pairing-scoped rule artifacts, not one rule publishing two findings. … Each applies the same per-pairing dispatch pattern on its own, **gated on the supportability verdict passing for the same pairing finding**." Decision 6: "Correction displacement follows from **shared pins**, with no new machinery. Both findings pin the same upstream dependencies … A correction to the acquisition or the pairing displaces both consequences directly, one hop."

That shared gate and those shared pins are the accrued precedent. Nominee interest is the opposite arrangement:

| Consequence | Gate | `input`/`choice` pins (ADR-0010 Decision 4) | Must not pin |
| --- | --- | --- | --- |
| Belonging-supported Schedule B reduction | Current supportable allocation set against the attached report; ADR-0070 supportability | Allocation finding id; attached report finding id; supportability verdict; the producing rule | The payment/credit/setting-apart finding. Putting it on the reduction's `input`/`choice` pins is `N2-PAYGATE` (payment present, so the join is discriminative) |
| Authority-indexed reporting evaluation, per formulation | That formulation's own terms | The facts **that formulation's own terms read**. Formulation 1 necessarily reads a payment/credit fact and pins it as `input`/`choice`. A **regulation-attributed** statement pins payment, credit, setting-apart, collection, or intermediary facts **if and only if that statement relies on them**; one limited to the actually-owned-portion language does not invent or pin payment. No blanket formulation-wide claim is made | A belonging-supported reduction must not appear as a dependency of a reporting evaluation in a way that lets correcting allocation invent a normalized obligation, or that lets correcting payment suppress the reduction |

**Pin-topology contract, copied as required:**

1. **`N2-PAYGATE`.** A conforming reduction's `input`/`choice` pins name the allocation finding and the attached report, not the payment finding. Observation (T0-B N2; T0-B review Attack 1): join `pin.id` to the kernel finding the scenario asserted as payment; identity is the finding id, not matching dollars. `InputFinding.role` is `"input"` or `"choice"` (`packages/derivation/runner.py` lines 52–59). ADR-0010 Decision 4 (`docs/adr/0010-derived-finding-projection-and-currency.md`): "For each derived finding, each pin with role `input` or `choice` that names a finding id yields a derivation edge `pinned_finding → derived_finding`." Parameter/operation-semantics/adoption/governance pins are provenance, never displacement edges. A shared-gate copy that still publishes `$450` is caught by that join.
2. **`N12-SHARED`.** N12 has a payment finding, so pin membership is checkable. Whatever the reduction's disposition, the payment finding id must **not** appear among the reduction's `input`/`choice` pins, and no published reduction may take the payment finding as a dependency pin. This is the topology check `N10-PIN` cannot make on N10's own facts, sited where the finding exists.
3. **`N10-PIN` is a named non-observation.** No contract clause. No later test of the form "N10: reduction pins must not include a payment finding id" — that observation is vacuously true for a conforming run **and** for a shared-gate that declared payment as a dependency and then omitted the pin (T0-B review T0B-R1). Absence of payment is caught by **`N10-SUPPRESS`** (reduction `$0` or dependent result blocked **for want of payment**), not by pin-id membership.

**N12 inference contract, copied as required (dollars and belonging, not pins):**

- **`N12-INFEROWN`:** reduction ≠ `$0` (a `$450` or any nominee reduction inferred from the payment).
- **`N12-BELONG`:** an allocation statement or belonging finding appears with no ownership assertion.

**Expressibility (T0-A T0-F3, paper-sufficient, not reopened).** ADR-0024 Decision 1 (guarded rules, `choose`/`all`, inapplicable dispositions) plus ADR-0071 Decision 2's *two-rule* shape (one finding per rule id) plus Decision 5 (independent succession). The two-rule *shape* transfers; the shared supportability *gate* and the shared-pin *displacement* of both consequences from payment do not. No executable spike is returned.

**Reporting evaluations are not a second subtractand and not a normalized obligation.** A product finding that "the taxpayer has a 6049 obligation" is `N2-NORM` / `N4-NORM` / `N10-NORM` / `N12-NORM`. See §14.4.

### 14.3 P-T1b — ADR-0070 supportability posture

**Disposition (T0-A, not reopened): inherit.** No product difference was named that would make Decisions 8–10 inapplicable. T0-B applied the posture; it did not re-decide it.

Quoted ADR-0070 (`docs/adr/0070-accrued-amount-supportability-rule.md`):

- Decision 8: "No allocation policy, at either tier. This decision detects and excludes an over-claimed individual pairing or report-group; it does not decide how much of a report an acquisition, or a group of acquisitions, is 'really' entitled to."
- Decision 9: an aggregate block "retracts the individual claims that composed it — it does not leave them published alongside the block."
- Decision 10: the dependent subtotal "blocks entirely rather than excluding the failed group and publishing the remainder as a settled, differently-scoped number."

Nominee mapping, already traced:

| ADR-0070 | Nominee production successor |
| --- | --- |
| Decision 8 | Over-allocation (`N5` `$1,250` against `$1,200`; `N6b` `$450` against `$400`; `N11b` `$450` against attached `$300`) contributes **no** reduction. The product must not drop one owner's claim to make the report fit (`N5-SUBSET`). |
| Decision 9 | Composing claims retracted; not left `published` alongside the block (`N5-STALE`). |
| Decision 10 | Dependent nominee result / line 2b **blocks**. Never remainder `-$50` (`N5-NEG`, `N6b-NEG`). Never a characterized unreduced share as ordinarily computed (`N5-GROSS`, `N6b-GROSS`, `N11b-GROSS`). N11b: report B's *report remainder* stays `$800` (no leakage / no borrowed support); that is **not** a licence to publish line 2b while A's set is unsupportable. |

A production successor that admitted a still-supportable subset, published a negative remainder, or presented unreduced gross as settled would fail these kills. No deviation is returned to the owner.

### 14.4 Reporting as a complete bounded product contract

The three formulations remain authority-indexed and unreconciled. T0-C **does not** select, combine, or rank them, and **does not** treat the unreconciled relationship as forcing a partial milestone result.

**Formulation identity, copied from §7.4 (plan `### A2`, the milestone plan), not from N12's E10 clause:**

| # | Formulation | Authority |
| --- | --- | --- |
| 1 | Literal IRC § 6049(a)(2): receive as a nominee **and** make payments aggregating `$10` or more with respect to the interest so received | statute |
| 2 | 2025 General Instructions for Certain Information Returns, "Nominee/middleman returns"; and the Schedule B TIP | form instruction |
| 3 | 26 CFR 1.6049-4: payor includes collector/middleman; middleman includes a nominee who pays, collects, or acts as intermediary; a person is a middleman as to any portion actually owned by another | regulation |

Formulation 2's operative text is P2 E11 and E3. **The 1099-INT filer instructions (P2 E10) are a separate source.** They are not formulation 2. A contract or later test that treats E10 as formulation 2 repeats T0B-R3.

**Required product behavior (already the T0-B method; now the contract):**

1. Evaluate each formulation on its own terms.
2. Record which scenario facts are present or absent for that authority.
3. Surface only the instruction or sentence that authority expressly supports, with the authority named.
4. Otherwise qualify or defer. Applicability itself remains unresolved.
5. Do **not** suppress formulation 2's attributed guidance because formulation 1's payment conjunct is unestablished (`N10-TIPDROP` is the kill). Do not rewrite the TIP as the statute.
6. Do **not** infer formulation 1's missing conjunct from belonging (N10) or infer belonging from payment (N12: `N12-INFEROWN`, `N12-BELONG`).
7. Do **not** close N12's preserved unknown — whether the onward transfer independently falls within another § 6049 route (e.g. (a)(1)) — by reasoning (`N12-A1`).
8. Per-owner reporting evaluation stays separable (`N4-NORM` / `N4-COLLAPSE` if folded into one aggregate `$450` table).

T0-A unknown 6 asked whether implementation would appear to require a unified reporting predicate. **It does not.** An implementation that emits one "6049 required / must file" finding is the named lie (`N2-NORM` and siblings). Separately attributed guidance, qualification, refusal, or deferral is the complete bounded product contract for this seam. The owner is not asked to determine unresolved law.

This checkpoint does not implement Forms 1096 or 1099-INT filing (charter non-goal).

### 14.5 Attribution exposure (T0-F1) as a production obligation, not a remaining semantic decision

T0-A §3.6: attribution is **recoverable** from the assertion act (`actor`, `at`, `committed_against` on `act.v1`) and **not available** to any of the three current explanation consumers. Exposing it **requires a bounded explanation extension**. T0-B named the reader-facing kill (`N2-ATTR`, also `N4-ATTR`, `N7-ATTR`, `N10-ATTR`). This checkpoint does **not** design the extension, does not relocate attribution into the proposition (placement stays closed), and does not reopen durable publication.

**Contract clause.** A reader shown a derived nominee determination must be able to see **who supported the ordinary statement it rests on**. Current `ExplanationNode` (`packages/derivation/explanation.py` lines 23–31), presentation `citationSites` (`packages/derivation/presentation_projection.py` lines 217–218), and `walk_npe` (lines 256–269) already fail that observation. A production successor that publishes a nominee determination without that exposure fails `N2-ATTR`. The extension's shape is a later charter; the required product property is specified here.

### 14.6 Concise nominee-interest addition to the fluid domain model

Working stratum only; not a schema. Durable publication into `docs/domain-models/taxable-interest-translation.md` is a Foreman/curation act. The current domain model names nominee allocation as something "the application cannot yet determine or translate" (`docs/domain-models/taxable-interest-translation.md` lines 75–81). Track 0's addition:

**The life circumstance.** A payer reports interest in the taxpayer's name. Some or all of that reported interest is another non-spouse person's. That is not a bond purchase reimbursing a seller for pre-acquisition accrual (N9b), and it is not an erroneous form amount (N9a). The product classifies from ordinary context; the user is not asked for a tax label.

**What the document contributes.** The 1099-INT box-1 report is documentary evidence of what the payer reported. It does not say who economically owns any portion.

**What the person contributes.** After circumstance routing: who the other person is, and how much of **that named report** is theirs. Separately, where an attributed statement actually reads it — **necessarily** for literal § 6049(a)(2), and for a regulation-attributed statement only where that statement relies on it: whether the taxpayer paid, credited, or set the interest apart. Silence is not a denial. An explicit "no" is transient.

**What translation the application performs.** It never accepts a preclassified "Nominee Distribution" as ordinary input. It preserves the payer report; it treats the ordinary allocation as bounded evidence for a *supported* Schedule B determination, never as a proven beneficial-ownership finding; it evaluates each reporting formulation on that formulation's own terms; it does not infer belonging from payment or payment from belonging.

**What reaches the return, at this rung.** The committed legacy nominee subtractand still reaches line 2b and the Schedule B nominee row when a legacy amount is current. A canonical ordinary-fact-derived reduction is a **different proposition** (artifact 4) and is not, at this rung, a second producer of that subtractand. See §16.

---

## 15. Neighboring-capability dependency diff (adversarial-closure artifact 5)

`PROJECT_PLANNING.md` `## Track 0 Adversarial Closure Gate` artifact 5: list the prerequisites of each neighboring capability **before and after** the design, including the return state in which the new feature has **no activity**. Every **new feature-specific prerequisite** imposed on an existing neighbor triggers a blast-radius review and must be justified by the neighbor's own meaning, not by implementation convenience.

This design **does not propose a successor producer** of an externally bound symbol. "After" is therefore the paper contract in §§14–16 applied against **committed** consumers, not a new rule graph. No new feature-specific prerequisite is imposed on any neighbor. Inherited shared-attachment and itemization constraints are recorded; they are not nominee-imposed gates.

### 15.1 Accrued-interest intake

| | |
| --- | --- |
| **Before** | Ordinary answers matching `ORDINARY_ANSWERS_SCHEMA` in `packages/tax/obligation_acquisition_mapping.py` (closed; `additionalProperties: false`; field `accrued_interest_paid_to_seller`). Circumstance type `tax.us.obligation-acquisition-circumstance`. ADR-0068 pairing to a report. ADR-0070 per-item and aggregate supportability. ADR-0071 two pairing-scoped rules **gated on the same supportability verdict**, sharing `input`/`choice` pins (Decision 6). ADR-0072 legacy accrued coexistence / retirement for new obligations. |
| **After** | **Unchanged.** Nominee does not add a fact, closure, confirmation, or gate to accrued intake. N9b **routes to** this neighbor as destination; it does not modify the mapper, the pairing, or the shared supportability gate. Overloading the mapper with nominee fields is `N9b-MAPPER` and is forbidden. |
| **No-activity return state** | N1a / N1b: no nominee allocation recorded. Accrued intake, pairing, and pairing-scoped consequences compute exactly as they do today. Closed-empty box-1 is a report-family state, not an accrued-intake prerequisite. |
| **New feature-specific prerequisite on this neighbor?** | **None.** Circumstance routing before nominee capture is a prerequisite of **nominee intake**, not of accrued intake. Accrued's own meaning (buyer reimbursed seller for pre-acquisition accrual; companion consequence is basis plus current-year adjustment, taxable to the seller — P2 Part D, reused) already distinguishes N9b; nominee does not re-justify it. |

Blast-radius review: **not triggered.**

### 15.2 Form 1040 line 2b (`tax.us.2025.interest.taxable-total`)

Walked from `packages/content/tax/2025/rule.form1040-line2b.v6.json`: `publishes` `tax.us.2025.interest.taxable-total`; `value` is `subtract` of the seven-family add minus `scheduleb-nominee-subtotal` + `scheduleb-abp-adjustment-subtotal` + `current-year-adjustment-subtotal` (lines 61–82); `when` `require_closed` on nine source_sets including `tax.us.2025.scheduleb.adjustment.nominee` (lines 85–96); `requires` includes `tax.us.2025.interest.scheduleb-nominee-subtotal` and `tax.us.2025.interest.current-year-adjustment-subtotal` (lines 42–52). Notes: v6 "cannot double-subtract regardless of any lingering legacy [accrued] finding"; nominee is still a subtractand.

| | |
| --- | --- |
| **Before** | Nine `require_closed` families (T0-A §5.1); three subtractands including the **legacy** nominee subtotal; pairing-scoped current-year-adjustment subtotal with **no** pairing source family and **no** `require_closed` for it; comparison guard refuses a negative taxable-interest result. |
| **After** | **Unchanged subtractands, unchanged closures.** This checkpoint does not add a canonical ordinary-fact-derived subtractand to line 2b. Independent gating and report-scoped supportability constrain a *future* producer; they do not change v6's inputs today. A canonical reduction that also reached line 2b while a live legacy amount described the same circumstance would be `N8-DOUBLE` — forbidden by §16, not implemented here. |
| **No-activity return state** | N1a: no allocation recorded; legacy nominee family closed empty (authorized zero). Line 2b is the seven-family add minus zeros. Unanswered ownership question is a **non-claim** (T0-A §4); it does not block line 2b and does not manufacture an absence declaration. Missing required closures still block line 2b on **those families' existing** `require_closed` — justified by the existing composition, not by a new nominee gate (T0-A §5.4–5.5). |
| **New feature-specific prerequisite on this neighbor?** | **None.** Supportability-block of the dependent nominee result under inherited Decision 10 is a property of the *nominee* dependent result, using the same dependency-absence mechanism Decision 10 already names. It is not a new line-2b `require_closed`. |

Blast-radius review: **not triggered.** If a later unit publishes a new producer of `tax.us.2025.interest.taxable-total` or replaces `scheduleb-nominee-subtotal` as a v6 subtractand, that **is** a successor producer of an externally bound symbol: artifact 6 and a fresh charter become mandatory, and this row is reopened.

### 15.3 Schedule B attachment

Walked from `packages/content/tax/2025/rule.attachment.schedule-b.v5.json`: `.requirement` is `comparison: "strictly_greater_than"` on `tax.us.2025.interest.positive-total` and `tax.us.2025.dividends.ordinary-total` against `tax.us.2025.parameter.schedule-b-threshold` (`"values": 1500`); v4 is identical on that object (T0-B §7.3). `itemizations[0].adjustment_rows[0]` is `kind: "nominee_distribution"`, label `"Nominee Distribution"`, `collect_members` on family `tax.us.2025.scheduleb.adjustment.nominee`, `subtotal_symbol` `tax.us.2025.interest.scheduleb-nominee-subtotal` (lines 55–71). Atomic block: `packages/derivation/runner.py` `attempt_attachment` lines 997–1002 return `"blocked"` (`BLOCK_ABSENT`) **before** the threshold is read if any required subtotal is missing; lines 1028–1036 record `disposition: "inapplicable"` **before** itemization or tie-out if no subtotal strictly exceeds the threshold.

| | |
| --- | --- |
| **Before** | Required only if a named subtotal **strictly exceeds** `$1,500`; atomic (any missing required subtotal blocks the **whole** attachment, Part I included); nominee row exists only as a collect of **legacy** members; pairing-scoped current-year-adjustment subtotal is subtracted at line 2b by **both** v5 and v6 and itemized by **neither** v4 nor v5 (T0-F5). |
| **After** | **Unchanged requirement, unchanged atomicity, unchanged nominee collect.** A paper-canonical reduction without a legacy member still has **no committed Schedule B row** even when the attachment is required (T0-B §7.3). Traces must not assume the attachment exists or is required (`N11a-ROW`). |
| **No-activity return state** | `$1,200`-only interest: `interest.positive-total = 1200` ≯ `1500` → attachment **not required**; no nominee row. Dividend-absent: whole attachment **blocked**; still no nominee row; line 2b still computes (T0-F6). |
| **New feature-specific prerequisite on this neighbor?** | **None.** |

**Inherited limitation (T0-F5), not a nominee defect.** `rule.form1040-line2b` v5 and v6 both subtract `tax.us.2025.interest.current-year-adjustment-subtotal`. Neither `rule.attachment.schedule-b` v4 nor v5 carries an adjustment row tying out to that symbol: v4's rows are `nominee_distribution`, `accrued_interest`, `abp_adjustment`; v5's are `nominee_distribution`, `abp_adjustment`. `ITEMIZATION_TIE_OUT_VIOLATION` (`packages/derivation/runner.py` constant line 163; raised near lines 1224–1232, hard-failing the attachment only) fires **only** when the attachment is required and execution reaches the tie-out check. A nominee row joining that attachment **inherits** the constraint: if a nonzero pairing-scoped current-year adjustment is present and Schedule B is required, the attachment can fail tie-out **even when the nominee figure is correct**. That failure is the missing pairing-scoped row, not `nominee_distribution` (`N9b-TIE`, `N11b-TIE`). **Do not attribute it to nominee interest. Do not repair it here.** It is outside this milestone's boundary.

Blast-radius review: **not triggered** for a new nominee-imposed prerequisite. T0-F5 is documented as an inherited neighboring limitation the shared attachment already has.

### 15.4 Standing workspace authorization (ADR-0069)

Quoted plan `## Contracts and boundaries` (the milestone plan): "The current standing workspace authorization remains the operational universe convention. The milestone does not ask for per-family “done” declarations or infer incompleteness from absence of an allocation."

Quoted ADR-0069 Decision 6 (`docs/adr/0069-standing-workspace-authorization.md`): "Ordinary source-family membership changes never touch this mechanism. Member-transition and assertion acts are ignored by the fold entirely — this is the property that makes the authorization 'standing' rather than expiring on every ordinary edit." Decision 1: the authorization "shares no chain, horizon, or lifecycle with per-family closure." Decision 8: absence of any authorization act is `AUTHORIZATION_ABSENT`, never silently current.

| | |
| --- | --- |
| **Before** | Standing grant keyed on workspace, taxpayer/subject, tax year, and re-authorization boundary digest; ordinary assertions and member-transitions do not expire it; no per-family "done"; unexplained allocation-absence is not incompleteness. |
| **After** | **Unchanged.** Nominee translation does not add a per-family confirmation, a "done" declaration, or an authorization-boundary name. "No allocation recorded" remains a non-claim state (T0-A §4): no user author, does not assert taxpayer ownership, ends when an affirmative allocation becomes current. It is **not** an absence declaration and **not** an authorization event. |
| **No-activity return state** | N1a: unanswered ownership question. Authorization currentness is whatever ADR-0069 already resolves; nominee silence neither grants, ends, nor expires it. |
| **New feature-specific prerequisite on this neighbor?** | **None.** Imposing per-family confirmation or inferring incompleteness from absence of an allocation would reopen a closed plan boundary. |

Blast-radius review: **not triggered.**

### 15.5 Dividend dependency (T0-F6)

T0-A §5.7 / T0-F6, not reopened. `tax.us.2025.f1099div.1a` authorizes `tax.us.2025.dividends.1a-subtotal` via `rule.f1099div-1a-subtotal`, feeding `rule.form1040-line3b`. The Schedule B requirement reads `tax.us.2025.dividends.ordinary-total` alongside `interest.positive-total`.

| | |
| --- | --- |
| **Before** | Dividend family state already decides whether the **shared** Schedule B attachment is required (subtotal strictly > `$1,500`) or blocked entirely (`BLOCK_ABSENT` if `ordinary-total` is missing). Line 3b blocks when 1a closure is missing. Line 2b is **not** gated on the dividend subtotal. |
| **After** | **Unchanged dividend rules and closures.** Nominee does not read dividend facts and does not add a `require_closed` on `f1099div.1a`. Direction remains **one-way**: dividend state can decide whether the nominee row's **surface** exists at all; it never changes the nominee figure or line 2b. |
| **No-activity return state** | Closed-empty 1a with current true closure: `ordinary-total` present and zero; attachment not blocked by absence; requirement then rests on interest alone. Missing 1a closure: whole Schedule B blocked; nominee row unpublished; line 2b still computes. |
| **New feature-specific prerequisite on this neighbor?** | **None.** The dependency is the neighbor's existing shared-attachment contract, not a nominee-imposed gate. Justified by ADR-0036 attachment atomicity and the committed requirement object, not by implementation convenience. |

Blast-radius review: **not triggered.**

### 15.6 Artifact 5 disposition

**PASS.** Prerequisites of accrued intake, line 2b, Schedule B, standing authorization, and the dividend family are listed before and after. The no-activity state is named for each. **No new feature-specific prerequisite is imposed on any existing neighbor**, so no blast-radius review is triggered. T0-F5 is recorded as an inherited neighboring limitation, not as a nominee defect and not as a new nominee gate. This PASS would fail if the design added a nominee `require_closed` to line 2b, made Schedule B required from nominee activity below the `$1,500` threshold, expired standing authorization on an unanswered ownership question, overloaded the accrued mapper, or gated line 2b on `dividends.ordinary-total`.

---

## 16. N8 compatibility account

Paper. **No concrete successor producer is proposed.** ADR-0072 is an accrued-specific analogy only: it does not govern or migrate nominee.

### 16.1 Same dollars, different proposition

Artifact 4 §10.1 (PASS, not reopened) already proved the three reuse tests independently **No**. The operational statement this account needs:

- Legacy `tax.us.2025.scheduleb.adjustment.nominee.amount` `$450` is a nonnegative **preclassified adjustment amount** for one logical Schedule B adjustment instance. Identity keys: tax-year `"2025"` + `tax.us.scheduleb-adjustment-instance` (`packages/content/tax/2025/scheduleb-adjustment.nominee.bundle.json` `fact_types[0]`). `value_schema` `{minimum: 0, type: number}`; `supersession.policy: "free"`. **Does not** establish actual-owner identity, report association, allocation basis, or why the amount belongs elsewhere (T0-A §4; P2 E18).
- Ordinary-fact-derived `$450` is an **attributed ordinary statement** that `$450` of `demo.1099int.statement-a` is `demo.owner.pat`'s, after N9b routing, used as bounded evidence for a supported Schedule B determination. **Does not** establish belonging (claim boundary, closed).

Matching `$450` cannot rekey one into the other. Publishing one fused proposition is `N8-CONVERT` / `N8-REUSE`. Subtracting both is `N8-DOUBLE` (line 2b reduced by `$900`; share `$300`). Required operational result remains **one subtraction or an explicit migration/refusal**: reduction `$450`, share `$750`.

### 16.2 Preventing double subtraction

Line 2b v6 already subtracts `tax.us.2025.interest.scheduleb-nominee-subtotal` (`rule.form1040-line2b.v6.json` lines 74–81). That subtotal is collected from the **legacy** family (`rule.scheduleb-adjustment.nominee-subtotal.json`; T0-A §5.3). A second ordinary-fact-derived subtractand that also reached line 2b would double-count (T0-B N8).

**At this rung, double subtraction is prevented by not introducing a second producer.** The committed producer of `scheduleb-nominee-subtotal` remains the legacy collect. A canonical ordinary-fact-derived reduction is a different proposition and **must not** also subtract at line 2b. N8's `$450` / `$750` result, when both describe the same circumstance and only the legacy amount is a line-2b subtractand, is the one committed subtraction.

This is a **compatibility constraint on any later producer**, not a claim that canonical translation already reaches line 2b. T0-B §7.3: "A paper-canonical reduction without a legacy member has **no committed Schedule B row** even when the attachment is required." N2 without a legacy member currently reduces line 2b only once a canonical **or** legacy subtractand is current. Closing that gap **is** proposing a successor producer, which this checkpoint does not do.

### 16.3 No silent conversion

Quoted ADR-0072 Decision 1 (`docs/adr/0072-legacy-pairing-scoped-interest-coexistence.md`): "The legacy accrued-interest input surface is retired for new obligations; **the legacy fact type is never edited, deleted, or reinterpreted.**" Nominee is not named. The posture that transfers (T0-A P-T1 legacy seam): do not edit, delete, or reinterpret `tax.us.2025.scheduleb.adjustment.nominee.amount`; do not upgrade it into an ownership claim it never contained.

What does **not** transfer:

- Decision 1's *retirement of the legacy input surface for new obligations* — Branch B means there is no production ordinary producer to retire; attested legacy facts still exist (tests inject them).
- Decision 2's same-amount collision trigger — analogy only, because the legacy nominee type also lacks owner/report identity; **not** an inherited mechanism.
- Decision 4's `rule.form1040-line2b.v6` migration-adoption path — v6 already exists for **accrued** single-subtractand succession; it still **consumes** the nominee subtotal. It is not a nominee migration.
- Decision 4's nonzero-predecessor block / genuine-zero migration rule — accrued-specific; owner-held representation-transfer adjudication on that ADR remains owner-held **for accrued**, and is not opened here for nominee.

`N8-CONVERT` is the kill: treating the legacy amount as if it named `demo.owner.pat` or `demo.1099int.statement-a`, or as formulation-1/2/3 evidence.

### 16.4 Surfaces a successor producer would touch (T0-A named; P2 Part C reused)

Plan `### Compatibility surfaces for N8 (Gate P2)` and P2 review "Compatibility and migration surfaces a production successor would touch." A later production successor that **replaces or coexists with** the legacy nominee amount would touch, at minimum:

- the fact type `tax.us.2025.scheduleb.adjustment.nominee.amount` — **published history, never edited in place**;
- its source family, closure mapping, subtotal rule, and citation `tax.us.2025.citation.scheduleb-adjustment.nominee`;
- the line-2b subtractand `scheduleb-nominee-subtotal` and the `require_closed` guard on the nominee family — present in v6 **and** in historical v4/v5;
- the Schedule B attachment nominee row, in v5 and v4 (`rule.attachment.schedule-b.v5.json` `itemizations[0].adjustment_rows[0]`; v4 still has that row plus `accrued_interest`);
- the adjustment-slot tables in `packages/derivation/package_validation.py`: `_V3_ADJUSTMENT_BINDINGS["nominee_distribution"]` (lines 211–215); `_V11_ADJUSTMENT_SLOTS` and `_V6_ADJUSTMENT_SLOTS` both still bind `("tax.us.2025.scheduleb.adjustment.nominee", "tax.us.2025.interest.scheduleb-nominee-subtotal")` (lines 217–228) — comment at lines 223–225: "nominee and abp-adjustment are unaffected" by the accrued v6 slot drop;
- the core-calculations package admissions of those artifacts.

**Double subtraction is a live risk independent of Branch B.** No ordinary-language producer was found in P2's enumerated searched committed production areas, but attested legacy facts can still be present.

When — and only when — a later unit names a concrete producer of `tax.us.2025.interest.scheduleb-nominee-subtotal` or of `tax.us.2025.interest.taxable-total`, it must choose a coexistence mechanism that satisfies `$450` once / never `$900`/`$300`, without silent conversion, and it **must** produce artifact 6 with real-consumer execution under a **fresh charter**. That choice is not made here, because making it *is* proposing the successor. ADR-0072's collision-on-amount, migration-adoption, and retirement-for-new-obligations are **available analogies**, not transferred contracts.

---

## 17. Integration-surface artifact (adversarial-closure artifact 6)

**N-A.**

This checkpoint does **not** propose a successor producer of an externally bound symbol. No new rule id, fact type, package member, or published-symbol binding is named for `tax.us.2025.interest.scheduleb-nominee-subtotal`, `tax.us.2025.interest.taxable-total`, or any other symbol a consumer outside the derivation graph binds or joins on. The committed producer of the nominee subtractand remains the legacy family collect. The paper contract in §§14–16 specifies product behavior a later producer would have to satisfy; it is not itself that producer.

`PROJECT_PLANNING.md` artifact 6 is required **whenever** Track 0 plans a producer or a successor producer of an externally bound symbol, including "one synthetic end-to-end model for every materially distinct disposition path, **exercised through the real consumer**. A model that is argued rather than built is not evidence." The paper rung cannot exercise a real consumer. The charter therefore makes artifact 6 mandatory **and** requires a **fresh charter before any execution** if a successor is proposed. Because none is proposed, N-A is the only honest grade.

**A later contract or production unit that publishes a new producer of either bound symbol cannot inherit this N-A.** It must produce artifact 6 under a fresh charter, with real-consumer execution, before it may be called ready.

---

## 18. Adversarial-closure declaration

Track 0's six artifacts, graded **PASS/FAIL only** for 1–5; artifact 6 may be **N-A**. No qualifier such as "pending" is a disposition.

| # | Artifact | Grade | Evidence that would fail if the design were wrong |
| --- | --- | --- | --- |
| 1 | Authority-lifecycle table | **PASS** | T0-A §4 table, `PROJECT_PLANNING.md` columns. Covers the payer report, box-1 closure, ordinary allocation statement, payment/credit fact, legacy nominee amount and closure, run-local derived reduction, authority-indexed reporting evaluation, and pairing-scoped current-year-adjustment neighbor. "No allocation recorded" is explicitly a **non-claim**, not a manufactured absence declaration. **Would fail if:** a tax-year key were treated as authority scope (box-1 identity is payer + statement + tax year — `f1099int.bundle.json` `fact_types[0]` `identity_keys`; two same-payer reports are distinct, N11); if "no allocation recorded" were written as a user denial or closed-empty ownership universe (N1a-SILENCE / T0-A §4); if the payment fact were given as a dependency of the belonging-supported reduction (N10/N12 non-inference; §14.2); if the legacy amount's meaning were written as owner/report/basis (artifact 4 proposition test). |
| 2 | Empty/nonempty authority matrix | **PASS** | T0-A §5. Qualifying families enumerated from committed consumers first (nine line-2b `require_closed` families, `f1099div.1a` via the shared attachment, committed accrued-interest family as N9b/coexistence neighbor). All four required states applied. Canonical allocation family **not invented**. Legacy nominee family exercised explicitly (§5.3), including nonempty **ineligible as ordinary allocation evidence**. Dividend atomic-attachment and `$1,500` strict threshold walked from JSON/code (§5.7, T0-B §7.3). **Would fail if:** closed-empty box-1 were treated as global "no allocation recorded" while the independent legacy nominee family could still have members (§5.2); if missing 1a closure still published Part I (atomic `BLOCK_ABSENT` at `runner.py` 997–1002); if nonempty-ineligible were inherited from a convenient unbuilt filter (dividend §5.7: `collect`s every admitted member); if a closure/eligibility contract were invented for the deferred canonical representation. |
| 3 | Late-authority counterexample | **PASS** | T0-B §9. Sequence `attest → close → compute → add member → reclose → recompute`, plus the charter's correction limbs (N6a/N6b, N7). FAIL columns at each transition. Limb A: run-local `$450`/`$750` unusable after Kim `$150` is added; reclose is a stated no-op because no canonical allocation family is committed. Limb B: old box-1 closure unusable after a second member (ADR-0017 / T0-A table: member-transition advances the horizon). Currency is **run-local re-derivation**, not ADR-0010 act-log displacement. Pin-set check in §9.1 is **`N2-PAYGATE`** on N2 facts, not `N10-PIN`. **Would fail if:** a summarizing declaration remained current after the authority it summarizes changed; if an ADR-0010 displacement claim were the currency mechanism (`N6a-DISP`, `N7-DISP`). |
| 4 | Claim-reuse proof | **PASS** | T0-B §10. Three tests independently **No** for N8's two `$450`s (same dollars, different proposition) and for N9b's gating "yes" versus N2's nominee proposition. **Would fail if:** matching dollars rekeyed the legacy amount into an ordinary allocation (`N8-REUSE` / `N8-CONVERT`); if N9b's "yes" were reused as N2's claim (`N9b-YES` / `N9b-CAPTURE`). |
| 5 | Neighboring-capability dependency diff | **PASS** | This checkpoint §15. Before/after/no-activity named for accrued intake, line 2b, Schedule B, standing authorization, and the dividend dependency. No new feature-specific prerequisite imposed. T0-F5 recorded as inherited limitation. **Would fail if:** the design added a nominee-specific `require_closed` on line 2b, required Schedule B from nominee activity at or below `$1,500`, expired ADR-0069 on an unanswered ownership question, overloaded `obligation_acquisition_mapping.py`, gated line 2b on `dividends.ordinary-total`, or attributed `ITEMIZATION_TIE_OUT_VIOLATION` to nominee interest. |
| 6 | Integration-surface artifact | **N-A** | §17. No successor producer of an externally bound symbol is proposed. **Would be FAIL, not N-A, if this checkpoint had named such a producer and then argued the consumer bindings without real-consumer execution.** |

**Known limitations affecting correctness: OWNER DISPOSITION RECORDED — T0-F5
deferred behind a hard production gate (2026-09-05).**

`PROJECT_PLANNING.md` allows exactly two values here — "none, or owner
disposition required" — and this row is **not** "none". The required disposition
has now been given.

**T0-F5 is a known neighboring correctness limitation.** When the shared
Schedule B attachment is **required** and a **nonzero** pairing-scoped
current-year adjustment is present, the attachment's Part I tie-out fails with
`ITEMIZATION_TIE_OUT_VIOLATION`: line 2b (v5 and v6 alike) subtracts
`tax.us.2025.interest.current-year-adjustment-subtotal`, and neither Schedule B
v4 nor v5 carries an adjustment row tying out to it. A nominee row joining that
attachment is published on a surface that can fail in that state.

The limitation is **inherited, not caused by nominee interest**, and it does not
affect the specified nominee arithmetic, the line 2b figure, the
independent-gating contract, or the reporting method. **That is a bound on its
scope, not a disposition of it.** This checkpoint does **not** self-dispose it as
outside the milestone: whether it is deferred or repaired here is the owner's
call, and **Track 0 closure awaits that disposition.**

Artifact 5 remains **PASS** on its own evidence: the diff discovered the
dependency, named the exact failing state, and bounded it — which is what that
artifact is graded on. A PASS there is not a claim that the limitation is absent.

### The owner disposition (recorded 2026-09-05)

**Option (a): T0-F5 is deferred behind a hard production gate.** The Schedule B
repair is **not** brought into this milestone.

**The gate, as an enforceable condition** (recorded in the plan under
`## Track 0 adversarial closure`): **no production or integration unit may be
accepted as complete for a state combining required Schedule B presentation with
a nonzero pairing-scoped current-year adjustment until T0-F5 is repaired.**

This does **not** prevent preparatory contract or production work **outside that
affected intersection**. T0-F5 remains a real, unrepaired neighboring
correctness limitation: deferral is not a finding that it is absent, repaired,
harmless, or attributable to nominee interest.

No production charter is ready while a later unit proposes a successor producer without artifact 6. That is a named future gate (§17), not a failed row here.

---

## 19. The result: decision-ready contract proposal

**This checkpoint returns a decision-ready contract proposal.** The owner's
T0-F5 disposition has since been recorded (§18: deferred behind a hard production
gate), so nothing is outstanding. The contract's *semantic* content is complete: no
consequential owner decision remains **about the nominee design itself**, and the
result is **not** an honestly bounded partial.

### T0-C review provenance

Every gate and checkpoint in this milestone was independently reviewed before
its successor began, and each review's durable findings were **absorbed into
this record and the milestone plan** — which is where they now live. The working
review records themselves were removed at publication curation, per the
project's curation rule that interim review reports are not publication
deliverables.

Two review provenances are worth stating precisely, so a later reader does not
over- or under-read the scrutiny applied:

- **P1, P2, P3, and T0-B** were reviewed by dispatched independent reviewers.
- **T0-A and T0-C** were reviewed by the **owner**. T0-C's review ran across two
  rounds and produced the adversarial-closure correction (the declaration read
  "none" while describing a limitation, and self-disposed it), the removal of the
  blanket payment/credit dependency claim, and the collapse of a duplicated
  paragraph in N10. No dispatched independent review of T0-A or T0-C occurred.

**The owner's T0-F5 disposition has been recorded** (§18): deferred behind a
hard production gate, with the Schedule B repair kept out of this milestone. That
limitation is real and unrepaired; deferral disposes of it, it does not dissolve
it. With the disposition given and T0-C independently reviewed, **Track 0 may
close.**

### 19.1 Why this is not a partial result

The charter forbids predeclaring a partial. Two tests:

**Test 1 — can every required product behavior be specified without unsupported legal normalization?** Yes. The reporting required-result for N2, N4, N10, N11a, and N12 is already specified as separately attributed evaluation, qualification, or deferral (§14.4; T0-B §7.4). The unreconciled relationship among the three formulations is **preserved**, not resolved. Preserving it is success condition 2 of the plan (`## Success and stop conditions`, the milestone plan): success "does **not** require deciding whether the legal predicates ultimately coincide." A unified "6049 obligation" finding would be unsupported legal normalization; this contract **forbids** it (`N2-NORM` and siblings). N12's possible other § 6049 route remains a preserved unknown with a specified product behavior: do not close it by reasoning (`N12-A1`).

**Test 2 — does another consequential decision remain unresolved?** Candidates, each closed:

| Candidate | Why it is not an unresolved consequential owner decision |
| --- | --- |
| R-A vs R-B | Already deferred by the plan. No N1a–N12 discriminator. Reopening trigger remains a consumer with materially different product behavior. Not selected by preference. No accepted seam is claimed to govern the representation. |
| T0-F2 owner cardinality | The **product behavior** is specified: independently correctable per-owner current statements; combined-fact is nonconforming (`N4-COLLAPSE`, `N7-REWRITE-OTHER`). Remaining representations that satisfy that constraint are not discriminated by N1a–N12. Selecting among them here would be architectural preference — the same class of error the plan forbids for R-A/R-B. Production may pick any conforming shape. The owner is not asked to pick one. |
| Independent gating | Specified (§14.2). Pin-topology contract is `N2-PAYGATE` + `N12-SHARED` with `input`/`choice` roles. N12 inference contract is `N12-INFEROWN` + `N12-BELONG`. `N10-PIN` is a named non-observation from which no clause is written. Paper-expressible; no spike. |
| ADR-0070 supportability | Inherited. No deviation returned. |
| Attribution exposure (T0-F1) | Required reader-facing property specified (`N2-ATTR`). Extension not designed — charter forbade designing it. That is a later-charter implementation obligation, not an open semantic question. Placement on the act stays closed. |
| N8 coexistence mechanism | Required operational behavior specified: one subtraction or explicit migration/refusal; never `$900`/`$300`; never silent conversion. A **concrete successor producer is not proposed**, so the mechanism that would implement a second producer is not yet required, and artifact 6 is N-A. Choosing retirement / collision / migration-adoption **would be** proposing the successor; it is therefore deferred to the unit that names the producer, under a fresh charter. That is a named future gate, not a missing product behavior. |
| Unified reporting predicate (T0-A unknown 6) | **Closed.** Implementation must not require one. Separately attributed guidance is the complete bounded product contract. |
| Durable publication | Orthogonal; run-local `RunResult` only. Not a requirement of this milestone. |

The contract unit in the plan remains **conditional** ("Charter only if Track 0 selects a contract with no consequential owner decision"). This proposal is that contract. Instantiating schemas, ADRs, or a producer is **not** this checkpoint and **must not** proceed from this paper record alone when the instantiation would bind an external symbol (§17).

### 19.2 Contract clauses a production successor must satisfy

Lifted from §§14–16. These are the decision-ready clauses; they are not an ADR text and not a schema.

1. **Preserve the payer report.** Remainder is arithmetic, not an ownership finding. Full allocation leaves share `$0` **with provenance** (`N3-DROP`, `N3-ZERO`). Silence is not an assertion (`N1a-SILENCE`). Explicit "no" is transient (`N1b-DURABLE`).
2. **Route circumstance before capture.** Nominee / accrued (N9b) / other-or-uncertain. Never a tax-label question. Do not overload the accrued mapper. N9a is document correction, not nominee.
3. **Claim boundary.** The ordinary allocation is bounded evidence for a supported Schedule B determination. Nothing establishes belonging (`N2-BELONG`).
4. **Report-scoped evaluation.** One named report's current amount. No leakage, collapse, merge, or borrowed support (N11a, N11b). Same-identity amount correction recomputes; it does not rekey the statement (N6a).
5. **Owner cardinality.** Independently correctable per-owner current statements. Combined-fact is nonconforming. Remaining conforming shapes, and R-A vs R-B, stay deferred.
6. **Supportability inherits ADR-0070 Decisions 8–10.** No allocation policy; retract composing claims; dependent result blocks; never negative remainder; never gross as settled.
7. **Independent gates.** Reduction not gated on payment (`N10-SUPPRESS`). Payment does not infer a reduction (`N12-INFEROWN`, `N12-BELONG`). Pin-topology: `N2-PAYGATE` + `N12-SHARED`; roles `input`/`choice` (ADR-0010 Decision 4). **No clause from `N10-PIN`.**
8. **Reporting.** Three formulations, §7.4 identity (formulation 2 = 1099GI nominee/middleman + Schedule B TIP; **not** E10). Separately attributed; qualify or defer; never select, combine, or rank; never suppress formulation 2 because formulation 1's conjunct is unestablished (`N10-TIPDROP`). Do not close N12's other-§-6049 unknown by reasoning (`N12-A1`).
9. **Attribution.** Recoverable from the assertion act; must be exposable to a reader (`N2-ATTR`). Do not relocate it into the finding. Do not claim ADR-0010 act-log displacement; observe run-local `RunResult` provenance.
10. **Legacy coexistence.** Same dollars are not the same proposition. No silent conversion. No second line-2b subtractand at this rung. Surfaces in §16.4 are the blast list for a later producer. ADR-0072 does not migrate nominee. Artifact 6 + fresh charter before any successor execution.
11. **Neighbors.** No new feature-specific prerequisite on accrued intake, line 2b, Schedule B, standing authorization, or dividends. T0-F5 inherited; not attributed to nominee. T0-F6 one-way; traces must not assume the attachment exists or is required. Standing authorization is not per-family "done" and is not expired by an unanswered ownership question.

### 19.3 Explicit unknowns (carried; none are owner-blocking)

1. R-A vs R-B — deferred; reopening trigger unchanged.
2. Remaining multi-owner shapes that satisfy clause 5 — deferred on the same terms.
3. Relationship among the three reporting formulations — unreconciled by design; product behavior specified without resolving it.
4. Whether N12's onward transfer independently falls within another § 6049 route — preserved unknown; `N12-A1`.
5. Explanation-extension shape — required property specified; shape not designed.
6. *(closed)* Whether implementation requires a unified reporting predicate — **no**.
7. Production intake outside P2's searched tree — out of scope.
8. How T0-F5 is repaired — outside this milestone.
9. Concrete successor producer and its coexistence mechanism — not proposed; artifact 6 N-A until a fresh charter names one.

### 19.4 Questions returned rather than answered

None at T0-C. Paper did not hit a technical-capability question that requires a spike. No formulation was selected. No rival representation was designed. No successor producer was named.

T0-C COMPLETE
