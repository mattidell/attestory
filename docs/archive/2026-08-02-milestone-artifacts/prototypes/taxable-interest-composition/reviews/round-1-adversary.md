# Round 1 — Adversary Review: Taxable-Interest Composition

Date: 2026-07-14  
Seat: Adversary reviewer (Medium). Owner-launched external context.  
Evidence: Rung 2 paper attacks only (read-only probes outside the repo allowed; none required to ground these findings).  
Independence: Governance reviewer output and any draft ADR-0026 **not read**. Prior TIC reviews do not exist.

**Subjects.** Incumbent `it1/design.md` (3-slot U_2b^v1 = {B1, B3, NF}, package-level composition binding, V1–V8) and clean-room rival `it2/design.md` (4-slot universe = {B1, B3, taxable_oid, unreported}, composition pin + slot bijection + `require_closed`). Both claim TIC-P1 and TIC-P2 settled at static level.

**Method.** Each attack states input state → expected correct result → where each design fails or survives. A construction that breaks one design and not the other is preferred evidence. Classification: **decision-blocking** / **production condition** / **non-blocking**. No repairs.

---

## Finding index

| Id | Title | Designs | Class |
|---|---|---|---|
| TIC-A1 | Omitted-source under-report: taxable OID vs incumbent U_2b^v1 | it1 (primary); it2 contrast | **decision-blocking** |
| TIC-A2 | Rival residual slot: relabel vs absorb (OID peers, K-1, adjustments) | it2 (primary); it1 contrast | **decision-blocking** |
| TIC-A3 | Present-source open-family zero/value (hidden open input) | it1 fails; it2 resists | **decision-blocking** |
| TIC-A4 | Narrow substitution residual paths | both (mostly resist); it1 soft edges | production condition / non-blocking |
| TIC-A5 | Late member on present-source path: zero/value not displaced | it1 fails; it2 resists via direct closure pins | **decision-blocking** |
| TIC-A6 | Lifecycle edges: assert-without-transition, removal, reclassification | both residual | production condition |
| TIC-A7 | Binding integrity: package pairing vs required composition pin | it1 weaker; it2 stronger | **decision-blocking** (it1) / production condition (it2) |

---

## TIC-A1 — Omitted-source under-report (taxable OID) — incumbent

**Class:** decision-blocking (TIC-P1 boundary).  
**Applies to:** it1 primarily; it2 named for contrast.

### Attack

Form 1040 line 2b is **total taxable interest**. The Form 1040 instructions and Schedule B instructions name Form 1099-INT **and** Form 1099-OID as sources of taxable interest (tax-exempt OID and 1099-INT box 8 go to line 2a). That is the legal line-2b universe, not a self-scoped content slice.

**In-scope source omitted by incumbent U_2b^v1:** taxable original-issue discount / periodic interest reportable on Form 1099-OID (or substitute), not a 1099-INT box-1 or box-3 statement item and not authored as `tax.us.2025.interest.non-form`.

**Synthetic filer F-OID:**

| Item | Amount | Family membership under it1 |
|---|---|---|
| Bank 1099-INT box 1 | $200 | B1 member |
| No box 3 amounts | — | B3 closed empty (literal-true on current horizon) |
| No informal loans / non-form cash interest | — | NF closed empty (literal-true) |
| Broker 1099-OID taxable OID (box 1 / periodic) | $350 | **No constituent fact type** — not B1, not B3, not NF fact type |

**Expected (honest line 2b):** $550 published only when OID is in the composition universe and closed/aggregated; coverage must not call taxable-interest composition complete while OID is unrepresented.

**it1 observed (paper contract):**

1. B1 subtotal = $200 (present-source).  
2. B3 subtotal = $0 (closure-backed).  
3. NF subtotal = $0 (closure-backed).  
4. Line-2b rule refs all three → publishes **$200**.  
5. Composition rollup V8: all three constituents CLOSED → composition coverage **CLOSED**, claim text = `required_universe.claim`.

That claim carefully hedges: it “does not assert completeness of source families outside the constituent list.” But the composition still **`publishes` the line-2b symbol** and binds a form-field citizen for Form 1040 line 2b. The hedge makes the *coverage sentence* defensible while the *form line* is understated by $350. That is ADR-0016 decision 5’s harm in a new costume: a narrow (here, three-family) surface standing behind a broader legal result.

**NF residual contradiction (internal).** The paper NF `closure_claim` says every taxable interest amount that is **not** a B1 or B3 statement-item member is recorded. Taxable OID satisfies that English residual. Yet §2.2 defers OID to a later composition version and the NF `member_predicate` is only `tax.us.2025.interest.non-form`. Either:

- OID is in NF’s claim → NF closed empty while $350 OID exists is a **false closure** the design invites by mismatching claim text to fact type; or  
- OID is outside NF → the residual claim is false and U_2b^v1 is not coextensive with line 2b.

Both readings under-report F-OID while the composition reports complete. “Versioned content surface” does not license publishing **Form 1040 line 2b** from a known-strict subset.

**it2 contrast:** taxable_oid is an explicit fourth slot. F-OID with B1=$200, B3/unreported closed empty, OID=$350 closed/present → line 2b can be $550 only if the OID family exists. Omitted-OID package fails slot bijection. **it2 resists this particular under-report; it1 does not.**

### Verdict contribution

it1 TIC-P1 **cannot** be accepted as “coextensive with Form 1040 line 2b” while OID is deferred. At best it is coextensive with a **self-declared slice** mislabeled as line 2b.

---

## TIC-A2 — Rival `unreported_taxable_interest`: absorb or relabel?

**Class:** decision-blocking (TIC-P1 completeness claim).  
**Applies to:** it2 primarily; it1 NF is the same residual pattern with a different name.

### Attack

it2’s four slots are B1, B3, taxable_oid, and `unreported_taxable_interest` (“taxable interest not in either reported class” / not in the reported form classes). The design asserts a disjoint exhaustive slot set for line 2b, then correctly lists unresolved authority: market discount, premium, nominee, accrued-interest adjustment taxonomy are not adopted. The question for the adversary is whether the fourth slot **genuinely absorbs** those in-scope effects or **relabels the residual gap**.

#### A2.1 Positive residual amounts (may fit unreported if authored)

| Source | In line 2b? | Absorbed by `unreported`? |
|---|---|---|
| Taxable interest never issued a 1099 (informal loan) | Yes | **Yes**, by construction — this is the residual’s core job |
| Schedule K-1 interest (partnership/S-corp) with no 1099-INT/OID | Yes (taxable interest) | **Only if** production predicates include K-1 interest fact types. Paper slot name does not pin K-1. Without that, K-1 is another omitted source under a CLOSED unreported family that only knows “non-form cash interest.” |
| Market discount treated as interest (e.g. IRC §1276 inclusion) not printed on 1099-INT/OID for the year | Often ordinary income reported as interest | **Same:** absorbed only by future predicate text, not by the slot label |

**Synthetic filer F-K1:** B1=$0 closed empty, B3 closed empty, OID closed empty, K-1 box interest $80, unreported closed empty with predicate authored only for informal non-form interest (as today’s NF pattern).

- **Expected:** $80 on line 2b, or block until K-1 is a member of some slot.  
- **it2 paper:** unreported CLOSED empty → line 2b **$0** and universe can be called complete under a narrow unreported predicate. The fourth slot **relabels** “everything else” without forcing K-1 (or market-discount) membership. Completeness is authorial, not structural.

#### A2.2 Adjustments that are not positive residual slots (unreported cannot absorb)

These change **arithmetic** of line 2b; they are not “another positive source family” to sum.

| Adjustment | Direction | Why `unreported` fails |
|---|---|---|
| **Nominee interest** included in box 1, distributed to the true owner | Must **reduce** taxable interest | Amount is **in B1**, not “unreported.” Summing B1 without nominee subtraction **over-reports**. Unreported does not subtract. |
| **Accrued interest paid at purchase** (buyer) | Reduces interest income | Again an adjustment against reported interest, not a fourth positive slot. |
| Bond **premium amortization** on taxable bonds | Reduces interest | Same. |

**Synthetic filer F-NOM:** One 1099-INT box 1 = $1,000 of which $400 is nominee interest for another person (filer issues nominee 1099s). True line 2b interest from that statement = $600 (plus any other slots).

- **Expected:** line 2b reflects $600 from that source (or equivalent Schedule B nominee handling), not $1,000.  
- **it2:** four-slot sum includes full B1 $1,000 if box-1 family is “stated box 1.” Unreported does not correct it. Bijection and `require_closed` still pass. **False completeness + over-report.**  
- **it1:** identical failure mode on B1+B3+NF sum; NF does not subtract nominee either.

So the rival’s OID slot is a real boundary improvement over the incumbent, but the claim that the **4-slot set is exhaustive for total taxable interest** is overstated: `unreported_taxable_interest` is a **named residual bucket**, not a proof of absorption for K-1 / market discount, and it does **not** encode nominee / accrued-interest / premium adjustments at all.

it2’s own “Explicit unresolved authority” section admits production must declare predicates and arithmetic before claiming completeness. That admission is correct — and it means TIC-P1 is **not** settled as coextensive with legal line 2b; it is settled only as a **mechanism** plus a **better partial partition**.

### Verdict contribution

it2 TIC-P1 mechanism: strong. it2 TIC-P1 universe-as-legal-line-2b: **conditionally** only after adjustment/K-1/market-discount predicates are real citizens — not by the word `unreported`.

---

## TIC-A3 — Hidden-open-input: present-source publication without family closure

**Class:** decision-blocking (TIC-P2 honest zero / open-input; also under-report).  
**Applies to:** it1 fails; it2 resists.

### Attack

Committed ADR-0014 decision 5: present-source aggregation **does not consult or pin** closure. Empty collect needs current literal-true closure; non-empty collect does not.

**State S-open-B1:**

1. B1 has one recorded statement item $120; **no** B1 closure finding (family open).  
2. B3 closed empty (true closure on current B3 horizon).  
3. NF closed empty (it1) / unreported + OID closed empty (it2).  
4. Adopted package is the design’s “valid” line-2b package.

**Expected (ADR-0016 dec. 3/5 spirit for a coextensive line):** either line 2b blocked until **every** constituent family — including those with present members — is closed, or coverage and publication both refuse to treat the taxable-interest composition as finished. Publishing $120 while B1 is open hides an open input: a second unrecorded 1099-INT box 1 for $500 would leave line 2b at $120 with no mechanical block.

**it1:**

- Case 2 paper: “Present-source B1 does not consult closure.”  
- Line-2b eligibility = presence of the three **subtotal symbols** only (runner: `requires` ⊆ published symbols).  
- B1 subtotal publishes $120 without closure; B3/NF zeros publish; line 2b publishes **$120**.  
- Composition V8 coverage is OPEN (B1 not CLOSED) — but **publication is not gated on V8**. Coverage and the form line diverge: the dangerous number ships.

**it2:**

- Line rule requires `require_closed` **per slot**, including B1, even when the B1 subtotal is non-empty.  
- Missing B1 closure → `SOURCE_SET_UNCLOSED` / block; no line finding.  
- Coverage names the open slot.  
- **Resists.** This is the cleanest single-mechanism differentiator in the round.

### Related zero form

**S-B1-only-zero (classic dec. 5):** only B1 closed empty; B3/NF (it1) or other slots (it2) unclosed.

- it1: B3/NF subtotals block → line 2b blocked. V5 rejects a rule that refs only B1. **Resists** the pure B1-zero promotion the spike allowed.  
- it2: same, plus explicit `require_closed` on all four. **Resists.**

So it1 defeats **empty** narrow zero, but not **present-source incomplete** publication. The charter’s “hidden-open-input zero” family includes publishing a line-2b **value** while a constituent’s completeness is unread. The present-open case is the live hole.

---

## TIC-A4 — Narrow substitution (ADR-0016 dec. 5)

**Class:** production condition (residual paths); core paths resisted by both.  
**Applies to:** both.

| Vector | it1 | it2 |
|---|---|---|
| Collect B1 family, publish line-2b | Resisted (`audit_collect_authority`) | Resisted (same + composition pin) |
| Ref only b1-subtotal, publish line-2b | Resisted (V5 full constituent refs) | Resisted (bijection + required refs) |
| Mapping admits line-2b for B1 family | Resisted (`validate_mapping_against_family`) | Resisted (slot↔family predicate equality) |
| B1 CLOSED reported as composition complete | Resisted (V8 all-constituent + exact claim) | Resisted (coverage pins universe; narrow closure ≠ complete) |
| Package omits a constituent family | Claimed V1 / package closure | Bijection reject |
| Semantic dead-code refs (all symbols in tree/`requires`, value uses only B1 via constant fold) | **Weak:** V5 is structural ref presence; eligibility still needs all subtotals published, so **runtime** still needs B3/NF zeros — resists practical under-narrowing unless false closures (content fraud) | Same structural limit; `require_closed` still forces all closures |
| Line-2b rule **without** any composition citizen in package | **Soft:** V4 is written as pairing when a composition’s `publishes` matches; if **no** composition member exists, composition audit may no-op and a three-ref sum is again a bare spike sum (see TIC-A7) | **Resists:** rule schema requires `composition:{id,version}` pin |

**N5-style outcomes:** both designs’ mandatory case 5 vectors are resisted **when** the composition machinery is actually in the package and invoked. it1’s resistance is load-time V5 + existing collect audit; it2 adds pin + `require_closed`. Residual narrow paths are binding/adoption gaps (A7), not missing V5 intent.

---

## TIC-A5 — Late member after present-source line 2b (lifecycle)

**Class:** decision-blocking for it1 TIC-P2; it2 resists.  
**Applies to:** both; differentiates.

### Attack

ADR-0017 decision 5: horizon succession displaces **closure facts/findings keyed on the predecessor horizon**; derivation edges from those closures displace **closure-backed** results.  
ADR-0014 decision 5: present-source subtotals **do not pin** closure.  
ADR-0010: derivation edges only from `input`/`choice` pins; displacement of derived findings requires a pin target to leave current state. Adding a **new** member finding does not supersede prior member findings.

**Trace L-present:**

1. Publish as in Case 2: B1 present $120 (DF_B1 pins MF1 only), B3/NF (it1) or other slots (it2) closed empty, line 2b = $120 (DF_2b).  
2. Late second B1 statement MF2 = $80 via atomic `member-transition` (horizon H_B1_0 → H_B1_1).  
3. No re-attest, no rerun yet (and even after rerun, ask what is **current** without new displacement roots).

**Expected:** DF_2b ($120) must leave current state; line 2b blocked or republished at $200 only after re-closure (if required) + explicit rerun. Filer must not keep a **current** $120 line 2b after MF2 is recorded.

**it1 Phase B** documents displacement only for the **empty-zero** path: CF_B1 → DF_B1_0 → DF_2b_0. In L-present, DF_B1 never pinned CF_B1. Horizon succession displaces any old B1 closure (if one existed from a prior empty phase); it does **not** displace DF_B1 that pins only MF1. MF1 remains current; DF_B1 remains current; DF_2b remains current at **$120** while MF2=$80 sits in the record. **Old coextensive (or multi-source) value is not displaced through the two existing edge kinds.** Case 6’s named trace does not cover this branch; TIC-P2 is only demonstrated for closure-backed zeros.

**it2:** line finding pins **direct** closure findings via `require_closed` (`C-x → D-2b` in the paper edge map). Member-transition advances B1 horizon → predecessor-keyed C-b1 displaced → **D-2b displaced** even if D-b1 was present-source. Until C-b1-1 and rerun, line blocks `SOURCE_SET_UNCLOSED`. **Resists** L-present with existing edges only — and this is exactly why direct closure pins on the line are not cosmetic.

### Empty-zero path (both)

Case 6 empty zero → late member → both designs: individuation on horizon → displace CF → derive-displace subtotal zero → derive-displace line zero. **Both resist** the classic false-zero-stays-current attack **when** the line/subtotals actually pinned those closures. No third edge proposed. Good shared convergence on the empty path.

---

## TIC-A6 — Assert-after-zero, removal, reclassification

**Class:** production condition (shared).  
**Applies to:** both.

### A6.1 Assert member without horizon successor

Admit MF_new for B1 **without** atomic successor horizon (malformed transition).

- ADR-0017 decision 3: missing successor **rejects the entire transition**.  
- Both papers rely on that committed rule; neither re-derives it.  
- **Conditionally resisted** only if production admission enforces atomicity (ADR-0017 consequence; still a contract test obligation, not a paper hole unique to TIC).

### A6.2 Removal after zero

Empty zero → add member (displace zero) → remove member → new empty horizon.

- Both: supersession roots accumulate (ADR-0017 dec. 6); old DF_2b_0 stays noncurrent; new zero needs new closure + rerun.  
- **Resisted on paper** if horizon successors are always recorded. No resurrection path found that reuses DF_2b_0 as current without violating ADR-0017.

### A6.3 Reclassification across predicates

Member moves from B1 predicate to B3 predicate (or OID ↔ unreported).

- Requires **membership-changing** transitions on **both** families (remove from one, add to the other), each with horizon successors.  
- Both papers say “same atomic transition/successor path” for removal/reclassification but **do not** specify dual-family atomicity or reject single-family half-moves.  
- **Attack:** reclass recorded only as B3 add → B1 still lists the member, B1 closure may be stale-wrong, double-count risk if both subtotals include it.  
- **Shared production condition:** define multi-family reclassification admission before claiming lifecycle completeness.

---

## TIC-A7 — Binding integrity

**Class:** decision-blocking for it1; production condition for it2.  
**Applies to:** both.

### A7.1 Incumbent package-level binding without mandatory composition

it1 prefers package membership pairing (V4–V7); composition pin role is an unresolved minor. Derived-finding pin roles today are closed and do **not** include `composition`.

**Attack package P-bare:**

- Members: B1/B3/NF declarations, mappings, three subtotal rules, line-2b rule with all three refs, form field.  
- **No** `coextensive-composition.v1` citizen.  
- Validation: existing `audit_collect_authority` passes (rule does not collect). Package closure of parameter refs passes.  
- Composition audit: if it only iterates composition members, **no compositions → no V4–V7 failures**.  
- Runtime: three subtotals + line sum publish. Coextensiveness declaration **absent** — spike-shaped bare sum with extra refs.

it1 N1b claims “composition missing → V4 reject.” That holds only if V4 is implemented as **“every rule publishing a composition-claimed symbol must have a composition binder”** or **“line-2b symbol requires a composition member.”** As written in §2.3.3, V4 is **pairing** (`publishes == composition.publishes` ⇒ bound). Absence of any composition leaves the universal quantifier vacuous. **Paper binding does not force the declaration to exist.**

### A7.2 Incumbent: validated package, incomplete universe still “line 2b”

Even with composition present, U_2b^v1 omits OID (TIC-A1). Package can pass V1–V8 and still under-report F-OID. Binding integrity includes **semantic** coextensiveness, not only structural constituent refs. it1 binding can be perfect relative to a non-coextensive universe.

### A7.3 Rival composition pin + `require_closed`

- Rule schema **requires** `composition:{id,version}`; missing pin fails schema.  
- Constituents must bijection universe slots; line’s subtotal refs **and** `require_closed` sets must match.  
- Runner pins composition + universe as package pins; line pins every closure read.

**Attack:** composition pin points at version v1 (4 slots) while a corrupted package swaps in a 3-slot universe citizen under the same id different version — rejected if pin version is checked (paper requires version pin). **Resists** when pin equality is enforced.

**Residual production conditions:** implement `require_closed` only through the single ADR-0014 dispatch (no second closed-set writer); reject alternate runners that evaluate the four refs without executing the four closure ops; golden-test pin sets include all closures even on multi-source non-zero lines.

### A7.4 Conflict_semantics smuggle

Package declares `conflict_semantics` for the line-2b symbol and ships a second narrow rule.

- it1 V3 addresses two **compositions** on same `publishes`, not two rules with declared conflict resolution choosing the narrow producer.  
- Existing package validation allows multiple producers if conflict is declared — resolution policy is not specified to prefer the composition-bound rule.  
- **Shared production condition:** conflict resolution must not elect a non-composition producer for a composition-claimed symbol.

---

## Equal attack matrix (summary)

| Attack | it1 incumbent | it2 rival |
|---|---|---|
| F-OID omitted source under-report | **Fails** — $200 line 2b, composition CLOSED | **Resists** — OID slot + bijection |
| F-K1 / market-discount residual | Fails if NF predicate narrow (same class as A2) | **Fails** if unreported predicate narrow — relabel not absorb |
| F-NOM nominee / accrued-interest adjustment | **Fails** — sum of gross families | **Fails** — unreported does not subtract |
| B1-only empty zero / ref-subset rule | **Resists** (V5 + eligibility) | **Resists** (bijection + require_closed) |
| Present B1 open, other slots closed empty | **Fails** — line publishes | **Resists** — require_closed(B1) |
| Late second B1 after present-source line | **Fails** — DF_2b stays current | **Resists** — direct C→line edges |
| Empty zero late member (Case 6) | **Resists** | **Resists** |
| Package without composition citizen | **Fails** (vacuous V4) | **Resists** (required pin) |
| Reclassification half-move | Production gap | Production gap |

---

## Verdicts per proposition per design

### it1 — Incumbent

| Proposition | Verdict | Conditions / reasons |
|---|---|---|
| **TIC-P1** | **Reject** as coextensive Form 1040 line 2b | U_2b^v1 omits taxable OID while publishing the line-2b symbol (TIC-A1). Versioned-surface hedge does not satisfy ADR-0016 dec. 4 coextensiveness with the form line. Declaration **mechanism** (composition citizen + V5) is directionally sound but binds the wrong/incomplete universe and can be omitted under vacuous V4 (TIC-A7). |
| **TIC-P2** | **Reject** as stated | Honest **empty** zero and Case 6 empty lifecycle resist. Present-source open-family publication (TIC-A3) and present-source late-member non-displacement (TIC-A5) leave current line 2b values with open or extended membership. Package binding does not force composition (TIC-A7). |

### it2 — Clean-room rival

| Proposition | Verdict | Conditions / reasons |
|---|---|---|
| **TIC-P1** | **Conditionally accept** (mechanism + OID boundary); **not** full legal completeness | Accept: 4-slot partition including taxable OID; slot bijection; composition pin; coverage pinned to universe; rejects narrow B1 substitution. **Conditions before claiming line-2b coextensiveness:** (1) production predicates for unreported must enumerate residual classes actually in scope (K-1 interest, etc.) or add slots — the name `unreported` alone is a relabel (TIC-A2); (2) nominee / accrued interest / premium **adjustment arithmetic** must be declared — unreported cannot absorb them; (3) no silent drop of adjustment taxonomy (design already warns — enforce as gate). |
| **TIC-P2** | **Conditionally accept** | Accept: all-slot `require_closed` defeats present-open publication (TIC-A3); direct closure pins defeat present-source late-member staleness (TIC-A5); empty-zero lifecycle uses only individuation + derivation. **Conditions:** implement `require_closed` solely via ADR-0014 dispatch; production admission atomicity for member-transition (ADR-0017); dual-family reclassification rules (TIC-A6); pin-set goldens. |

---

## Carry-forward recommendation (advisory)

Owner decides disposition. On the evidence of these attacks:

1. **Do not** carry forward it1’s U_2b^v1 {B1, B3, NF} as the line-2b coextensive universe. Taxable OID is in-scope for the form line; deferral while publishing line 2b is under-report by construction (TIC-A1).  
2. **Do** carry forward it2’s structural shape: versioned universe + composition citizen, **slot bijection** validator, **required composition pin** on the line rule, and generic **`require_closed` per constituent** with line findings pinning those closures. That bundle is what defeats TIC-A3, TIC-A5, and the vacuous-binding hole.  
3. **Do not** treat `unreported_taxable_interest` (or it1’s NF) as proof of completeness. Force explicit predicates (and separate slots where predicates are not residual) for every positive source class the return must include; force **adjustment** rules for nominee / accrued-interest / premium — residual sum slots cannot express them (TIC-A2).  
4. it1’s V5 “ref every constituent subtotal” is necessary but **not sufficient** without (a) a non-vacuous “composition required” binder and (b) per-constituent closure reads on the line.  
5. Shared production conditions (atomic member-transition, reclassification, conflict_semantics) belong in the conforming ADR’s consequences, not as silent assumptions.

**Committee-facing one-liner:** the rival wins the mechanism and the OID boundary; neither design yet owns honest **total** taxable interest; the incumbent’s scoped coextensiveness claim is the round’s sharpest failed attack surface.

---

## Scope / non-findings

- No runner, schema, or horizon edits were made; no design repairs.  
- Governance review not consulted; no ADR-0026 draft read.  
- Exact schema bytes, Schedule B presentation threshold, and reusable all-lines composition abstraction: out of Gate 5 / not used as pass criteria here.  
- Paper only: classifications assume the designs are implemented as written; where committed kernel semantics (ADR-0010/0014/0017) contradict a paper claim, the kernel wins.
