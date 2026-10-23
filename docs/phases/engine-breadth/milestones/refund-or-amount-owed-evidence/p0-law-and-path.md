# P0 — the 2025 law for lines 22-38 and the real input path

Sources (downloaded, ignored, under `temp/tax-on-taxable-income/sources/`):
`f1040-2025` (2025 Form 1040, downloaded this P0), `i1040gi-2025` (2025 Form
1040 instructions). Line numbers below cite the `.txt` line unless noted as
a page. The 2025 General Instructions for Forms W-2 and W-3 (`iw2w3-2025`,
downloaded this P0) was not needed: the Form 1040 instructions' own line
25a text already states box 2's meaning directly (Sec. 1 below), so no
Form W-2/W-3 citation was required.

## 1. Line table: Form 1040 (2025) lines 22-38

| Line | What it does | Feeds from | Condition / instruction |
| --- | --- | --- | --- |
| 22 | Line 18 − line 21 (= line16+17 − (line19+20)); "If zero or less, enter -0-" | 16, 17, 20, 19 | `f1040-2025` l.112; already implemented (`rule.form1040-tax-after-credits`, `tax.us.2025.tax.after-nonrefundable-credits`), floors at 0 |
| 23 | "Other taxes, including self-employment tax, from Schedule 2, line 21" | Schedule 2 line 21 | `f1040-2025` l.112; Schedule 2 Part II detail is a non-goal (AMT/SE tax/Add'l Medicare/NIIT declared absent) |
| 24 | "Add lines 22 and 23. This is your total tax" | 22, 23 | `f1040-2025` l.113 |
| 25a | "Federal income tax withheld from: Form(s) W-2" — "Add the amounts shown as federal income tax withheld on your Form(s) W-2. The amount withheld should be shown in box 2 of Form W-2." | W-2 box 2, summed | `f1040-2025` l.115-117; `i1040gi-2025` l.2551-2556 |
| 25b | "Form(s) 1099" — includes federal income tax withheld on 1099-R (box 4), and on any 1099 showing withholding on dividends, taxable/tax-exempt interest, unemployment compensation, social security benefits, or railroad retirement benefits (1099 box 4, SSA-1099 box 6, RRB-1099 box 10) | 1099-R box4, 1099-INT/DIV box4 (if withheld), 1099-G box4, SSA-1099 box6 | `f1040-2025` l.116; `i1040gi-2025` l.2559-2576 |
| 25c | "Other forms" — named explicitly: Form(s) W-2G box 4 federal withholding; attach if withheld | W-2G box4 (not a document this engine reads) | `f1040-2025` l.117; `i1040gi-2025` l.2587-2592 |
| 25d | "Add lines 25a through 25c" | 25a-25c | `f1040-2025` l.118 |
| 26 | "2025 estimated tax payments and amount applied from 2024 return" — a person-entered figure, not derived from a statement | taxpayer entry | `f1040-2025` l.119; `i1040gi-2025` l.2536-2545 |
| 27a | Earned income credit (EIC) | Sch. EIC / worksheet | `f1040-2025` l.123; non-goal, declared absent |
| 27b/27c | Clergy Schedule SE / decline-EIC checkbox | — | `f1040-2025` l.124-125; non-goal |
| 28 | Additional child tax credit (ACTC) from Schedule 8812 | Sch. 8812 | `f1040-2025` l.126-127; non-goal, declared absent |
| 29 | American opportunity credit, Form 8863 line 8 | Form 8863 | `f1040-2025` l.128; non-goal |
| 30 | Refundable adoption credit, Form 8839 line 13 | Form 8839 | `f1040-2025` l.129; non-goal |
| 31 | "Amount from Schedule 3, line 15" (Part II total other payments/refundable credits) | Schedule 3 line 15 | `f1040-2025` l.130; non-goal; **distinct from** the already-adopted Schedule 3 Part I (lines 1-8, direct FTC) — this is a different part of the same form |
| 32 | "Add lines 27a, 28, 29, 30, and 31. These are your total other payments and refundable credits" | 27a, 28, 29, 30, 31 | `f1040-2025` l.131 |
| 33 | "Add lines 25d, 26, and 32. These are your total payments" | 25d, 26, 32 | `f1040-2025` l.132 |
| 34 | "If line 33 is more than line 24, subtract line 24 from line 33. This is the amount you overpaid" | 33, 24 | `f1040-2025` l.133; silent on the equal case (33 == 24): the "more than" test is false, so 34 is simply not entered — no instruction computes a negative or zero line 34. "If line 34 is under $1, we will send a refund only on written request." (`i1040gi-2025` l.4215) |
| 35a | "Amount of line 34 you want refunded to you" | 34, taxpayer choice | `f1040-2025` l.134; a person-entered split of line 34 between 35a (refunded) and 36 (applied) |
| 35b-35d | Routing/account/type for direct deposit | — | `f1040-2025` l.135-137; explicit non-goal (no direct-deposit detail) |
| 36 | "Amount of line 34 you want applied to your 2026 estimated tax" | 34, taxpayer choice | `f1040-2025` l.138; `i1040gi-2025` l.4401: "This election to apply part or all of the amount overpaid to your 2026 estimated tax can't be changed later." Elective, not derived |
| 37 | "Subtract line 33 from line 24. This is the amount you owe" | 33, 24 | `f1040-2025` l.139-140; also silent on the equal case for the same reason as 34 (the form provides no "if zero or less" clause here either, unlike line 22); `i1040gi-2025`: "You don't have to pay if line 37 is under $1" (l.4416-4417, "Amount You Owe" section) |
| 38 | Estimated tax penalty (Form 2210) | — | `f1040-2025` l.141; `i1040gi-2025` l.4510 ff.; explicit non-goal, declared absent |

**Lines 17, 19, 23, 27-32 if not absent.** Line 17 (Schedule 2 line 3,
mirrors line 23's Part II but is Part I — AMT and excess advance premium
tax credit repayment) and line 19 (child tax credit / ODC, Schedule 8812)
are already required absent by the adopted `rule.form1040-tax-after-credits`
(`tax.us.2025.direct-ftc-scope.no-line17-schedule2-additional`,
`...no-line19-ctc-odc`). Line 23 needs **Schedule 2 Part II** (self-employment
tax, additional Medicare tax, NIIT, and the other items the Schedule 2 line
21 instructions name) — a *different* Schedule 2 part from line 17's, so
line 17's existing absence fact cannot be reused for it; it needs its own.
Lines 27-32 each need a refundable-credit-family absence (EIC, ACTC, AOC,
adoption credit, Schedule 3 Part II) — none of these share meaning with any
absence fact that exists today (the existing `no-sch3-line2`...`-line6`
facts are Schedule 3 Part I, lines 2-6, feeding line 20, not Part II line 15
feeding line 31).

**Lines 34-37 mechanics.** A zero balance (line 33 == line 24 exactly) is
simply the case where *neither* line 34 nor line 37 is "more than" its
counterpart — the form leaves both blank/zero by the ordinary meaning of
"If X is more than Y, [compute]; [else nothing stated]," not by an explicit
"-0-" instruction the way line 22 has. Rounding: no line-specific rounding
instruction appears for 22-38 beyond the form-wide optional whole-dollar
convention already adopted elsewhere in this corpus (`rounding.convention`).
The line 36 election is explicit taxpayer choice, irrevocable once made,
splitting line 34 between 35a (refunded) and 36 (applied to 2026); it is not
derived from any other fact.

## 2. Withholding inventory — per source document

| Document | Withholding box | Reaches | Recorded today? | What recording the box takes |
| --- | --- | --- | --- | --- |
| W-2 | box 2 | 25a | **No fact type at all.** Box 1 (`tax.us.2025.w2.box1-wages`, `w2.bundle.v3.json`) is the only W-2 field with a fact type; no `*_recording.py`/`*_review.py` module exists for W-2 at all — box 1 is admitted through plain `assertion`/`bundle-adoption`/`horizon-genesis` acts and aggregated by `rule.wages-line1a.v2` (`{"op":"collect","source_set":"tax.us.2025.w2"}` + `add` + `round`). | New fact type `tax.us.2025.w2.box2-withholding` (same `employer`+`w2-slip`+`tax-year` identity keys as box1), a new source family + closure fact type + closure mapping (box1's family/closure are scoped to box1 specifically — `family.w2.v2.json`'s `member_predicate` names `box1-wages`, so box2 needs its own, not a shared one), and a new rule reusing the identical `collect`+`add`+`round` shape as `rule.wages-line1a.v2`. |
| 1099-INT | box 4 | 25b | **No fact type.** Only box 1 (b1), box 3 (b3), box 8 (tax-exempt, b8), box 10 (b10) exist (`f1099int-*.bundle.json`), aggregated generically the same collect/closure way as W-2 box1. | Same shape as W-2 box2: new fact type, new family/closure, new collect rule. |
| 1099-DIV | box 4 | 25b | **No fact type.** Only box 1a, box 2a, box 7 (foreign tax), box 12 (exempt-interest div) exist. | Same shape. |
| 1099-R | box 4 | 25b | **No fact type.** Only the bounded IRA-fully-taxable route exists (box 1 + box 2a + checkbox + distribution-code companions, enforced in `packages/tax/loader.py`'s `domain_companion_fact_types`); no withholding companion. | New fact type as a same-statement companion on the existing IRA family (mirrors the box-1/box-2a companion pattern `loader.py` already enforces), new rule. |
| 1099-G | box 4 | 25b | **Exists, but bounded to zero/absent only.** `tax.us.2025.f1099g.box4-federal-withholding-authority` — "Only explicit null (absent) or numeric zero is admissible... A nonzero value is a hard admission block and never creates Form 1040 line 25b" (`f1099g-box1.bundle.json`); enforced in `loader.py`'s `domain_companion_value_domains` (`frozenset({None, 0, 0.0})`). | A real nonzero box 4 needs this *authority witness* replaced/widened by an actual amount fact (same shape as W-2 box2) plus a 25b-consuming rule — the current fact cannot represent a real withheld amount at all, by design, today. |
| SSA-1099 | box 6 | 25b | **Exists, same zero/absent-only bound.** `tax.us.2025.ssa1099.box6-withholding` — "bounded class admits only absent/zero" (`ssa1099.bundle.v2.json`); same `loader.py` restriction. | Same as 1099-G: needs its bound lifted plus a 25b-consuming rule. |
| 1099-K | box 4 | 25b (or 25c? — Sec. below) | **Exists with a real numeric value** (`tax.us.2025.f1099k.box4-federal-withholding`, `value_schema: number, minimum 0`, recorded by `packages/tax/f1099k_statement_recording.py`'s `STATEMENT_BOX4`). **Flagged route: a nonzero value is recorded but never reaches any payments line.** Its only consumer, `rule.f1099k-statement-loss-reason` (v2-v4), classifies a nonzero box 4 as the categorical reason `"backup-withholding-unsupported"` — a block reason for the *statement-loss* computation, not a contribution to 25b/25c. The withholding amount itself is admitted and stored; nothing sums it anywhere. | A 25b-(or 25c-)consuming rule that reads the already-recorded `tax.us.2025.f1099k.box4-federal-withholding` fact directly — the fact type itself needs no change, only a new consumer. *Note: the 2025 instructions' line 25a/25b/25c text (Sec. 1) never names Form 1099-K; 1099-K backup withholding would need to be assigned a line by analogy (most likely 25c, "other forms," since it is not the W-2/1099-R/SSA/RRB list 25b enumerates) — a decision for the owner, not resolved by this P0.* |
| Schedule K-1 (Form 1065) | — | — | **Not applicable.** The engine's own K-1 (1065) content (`form1065-k1.bundle.json`) models only box 5 (taxable interest); Schedule K-1 (Form 1065) itself carries no federal-income-tax-withheld box in the form the engine reads (domestic partnerships ordinarily do not withhold on partners) — this is a true absence of the underlying form field, not a recording gap. | None. |

**No route drops a withholding amount silently.** The only document whose
real value goes nowhere today is 1099-K box 4 (above) — and that is an
explicit, named block reason (`backup-withholding-unsupported`), not a
silent loss; the value is on record, just never summed. 1099-G and SSA-1099
are bounded to admit only zero/absent, so a real nonzero value there is
refused at the door, never silently accepted and dropped.

## 3. Input path trace: `tax.us.2025.w2.box1-wages` → what W-2 box 2 needs

Traced on the real coordinator path, core-calculations v51
(`packages/content/tax/2025/package.core-calculations.v51.json`).

1. **Entry/recording.** No dedicated `*_recording.py` module exists for
   W-2 at all (unlike Form 1098 or Form 1099-K). A caller admits box 1 via
   three ordinary `act.v1` kinds in sequence: `bundle-adoption` (the
   `w2.bundle.v3.json` vocabulary — fact types for box1-wages and
   source-closure), `horizon-genesis` (opens the `tax.us.2025.w2` family's
   current membership horizon), and `assertion` (one `finding.v2` per W-2
   slip, `fact_id` keyed by `employer`+`w2-slip`+`tax-year`), closed by one
   more `assertion` asserting the horizon's `source-closure` fact `true`.
   The product-slice entry surface (`packages/derivation/entry_loop.py`)
   wraps exactly this shape behind a synthetic HTTP `contribution` act for
   one demo fixture; it is a UI-adjacent convenience, not a second recording
   path.
2. **Recorded act / resolution.** `apply_act` (`packages/kernel/findings.py`)
   admits the assertion against `act-assertion.v2`/`finding.v2` and projects
   it into `FindingState` — identical machinery for any fact type.
3. **Live material.** `compute_currency` (`packages/kernel/currency.py`)
   determines which findings are current for their identity key;
   `marshal_run_context` (`packages/derivation/marshal.py`) reads them into
   `current_findings`.
4. **Marshalling.** `marshal_run_context`'s bindings loop walks the adopted
   package's `input_bindings`; `tax.us.2025.w2.box1-wages` is **not** bound
   directly as a scalar symbol there — it is read by name inside an
   expression (`collect`), which the runner resolves against the current
   `tax.us.2025.w2` source family's members rather than through a one-symbol
   binding.
5. **Dispatch.** `rule.wages-line1a.v2` (`packages/derivation/runner.py`)
   evaluates `{"op":"round","mode":{"op":"ref","name":"rounding.convention"},
   "value":{"op":"add","args":[{"op":"collect",
   "name":"tax.us.2025.w2.box1-wages","source_set":"tax.us.2025.w2"}]}}` —
   **this is how multiple W-2s are summed today**: every current box1-wages
   finding in the closed `tax.us.2025.w2` family is collected and added,
   then rounded once.

**What W-2 box 2 needs at each step** (same table shape as the
senior-and-dependent-deductions P0's own conclusion, reusable because the
vocabulary is identical): a new `fact-type.v2` (box2-withholding, same
identity keys as box1), a new `source-family.v1` + `source-closure-mapping.v2`
pair scoped to the new fact (box1's own family/closure name box1 by id, not
"any W-2 field," so they cannot be shared), and one new `rule-artifact.v2`
using the exact `collect`+`add`+`round` shape box1 already uses, publishing
to a new symbol feeding line 25a. **No schema successor, no expression
operation, and no engine (Python) change is required** — `collect`,
`source-family.v1`, and `source-closure-mapping.v2` are all already-generic
vocabulary; this is new content only. The one genuine engine-adjacent
question is whether a corrected/second W-2 for the same slip should
supersede box 2 independently of box 1 (both facts share `free` supersession
today on box 1; box 2 would get the same policy by construction, not by any
special-casing).

## 4. Existing absence answers line 22 already requires, and what 23-32 add

| Fact | Scope | Line it protects | Reusable for 23-32? |
| --- | --- | --- | --- |
| `tax.us.2025.direct-ftc-scope.no-line17-schedule2-additional` | Schedule 2 **Part I** (AMT, excess APTC repayment) | 17 (feeds 18→22) | **No** for line 23 — line 23 is Schedule 2 **Part II** (SE tax, additional Medicare, NIIT, etc.), a different part of the same schedule; reusing this fact's "yes" would misstate what is actually absent. Needs its own, e.g. `tax.us.2025.schedule2-partii-scope.no-line21-additional-taxes`. |
| `tax.us.2025.direct-ftc-scope.no-line19-ctc-odc` | Child tax credit / ODC | 19 (feeds 21→22) | Not applicable to 23-32 (already fully consumed at line 19/22; no further reuse needed there). |
| `tax.us.2025.direct-ftc-scope.no-sch3-line2`…`no-sch3-line6` | Schedule 3 **Part I**, lines 2-6 (other nonrefundable credits) | 20 | **No** for line 31 — line 31 is Schedule 3 **Part II**, line 15 (other payments/refundable credits: net premium tax credit, health coverage credit, excess SS tax, etc.), a different part again. Needs its own absence(s). |

**New absences lines 27-32 need, none reusable:** EIC (27a), the clergy/decline-EIC
checkbox path (27b/27c — likely not a true absence but a checkbox the bounded
class leaves unchecked), ACTC (28), American opportunity credit (29),
refundable adoption credit (30), and Schedule 3 Part II total (31) — six
distinct refundable-credit/payment families, each already a named non-goal
("declared absent, never assumed zero"). None shares a fact with any
existing absence; each needs its own, following the same
`no-<thing>-declared`/`{yes,no}` shape the corpus already uses throughout.

## 5. Real-path observation

Probe: `docs/phases/engine-breadth/milestones/refund-or-amount-owed-evidence/probe.py`.
Single filer, $50,000 W-2 wages only, every optional feature (senior
deduction, dependent worksheet, itemizing) left at its default, run through
`live_coordinate_run` on core-calculations v51. One deliberate override was
needed to reach a published line 22 at all: the base builder's
`tax.us.2025.direct-ftc.election` defaults to `"no"`, and that fact's own
title says `"no"` "declines [the direct credit] and blocks it" — by design,
not a defect, but it means *every* return using this builder unmodified
is blocked before line 20/22 regardless of whether it has any foreign tax.
The probe supersedes the election to `"yes"` (free supersession); with a $0
Schedule 3 line-1 box-7 subtotal, electing correctly computes a $0 credit.

| Line | Symbol | Value |
| --- | --- | --- |
| 11 (AGI) | `tax.us.2025.income.agi` | $50,000 |
| 15 (taxable income) | `tax.us.2025.income.taxable-income` | $34,250 |
| 16 (tax) | `tax.us.2025.tax.total-tax` | $3,875 |
| 22 (tax after nonrefundable credits) | `tax.us.2025.tax.after-nonrefundable-credits` | $3,875 |

No disposition was `blocked`. Of the **145** symbols this run publishes,
none names line 23, line 24, any of lines 25a-25d, line 26, lines 27-32, or
lines 33-38 — confirming the milestone's own diagnosis: today's content
stops exactly at line 22. One symbol is worth flagging specifically:
`tax.us.2025.f1099k.box4-federal-withholding` **does** publish ($0, from the
closed-empty 1099-K family in this return), demonstrating directly that even
a recorded, real-valued withholding fact reaches no payments line today —
there is simply no rule anywhere in the adopted package that reads it toward
25a/25b/25c.

## 6. Case table (plan's cases, hand-computed)

All cases hold wages/AGI/taxable-income/line-16-tax at the probe's own
verified base ($50,000 wages, single, tax $3,875) except where a case
explicitly varies income; line 22 = $3,875 throughout (line 17, 19, 20 all
absent/zero, as in the probe). Lines 23, 27-32 are $0 throughout (every
non-goal declared absent). Arithmetic is Form 1040's own addition/subtraction
(Sec. 1); no tax-table recomputation is needed for these new lines.

| Case | 25a/25b/25d | 26 | 33 | 24 | 34 (overpaid) | 37 (owed) | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| W-2 only, withholding **above** tax | 25a=$4,500, 25d=$4,500 | $0 | $4,500 | $3,875 | $625 | — | **Refund** of $625 |
| W-2 only, withholding **below** tax | 25a=$3,000, 25d=$3,000 | $0 | $3,000 | $3,875 | — | $875 | **Owes** $875 |
| W-2 only, withholding **exactly equal** | 25a=$3,875, 25d=$3,875 | $0 | $3,875 | $3,875 | — (33 not "more than" 24) | $0 (33−24=0; "don't have to pay if under $1") | **Neither** |
| Two W-2s (same employer total) | W-2 #1 box2 $2,000 + W-2 #2 box2 $1,200 → 25a=$3,200 (collect+add, Sec. 3), 25d=$3,200 | $0 | $3,200 | $3,875 | — | $675 | Owes $675; demonstrates box2 aggregation identically to box1 |
| W-2 + 1099-INT backup withholding | W-2 box2 $4,500 → 25a=$4,500; 1099-INT box4 $150 → 25b=$150; 25d=$4,650 | $0 | $4,650 | $3,875 (unchanged — a token $1 of interest income's tax effect is immaterial at this scale and out of this P0's job to re-derive precisely) | $775 | — | Refund $775; demonstrates 25a **and** 25b both populated and added at 25d |
| Estimated payments, refund | 25a=$3,000, 25d=$3,000 | $1,200 (estimated payments) | $4,200 | $3,875 | $325 | — | Refund $325; demonstrates line 26 as a direct taxpayer-entered figure, not derived from any statement |
| Refund applied to 2026 | Same as the first row (overpaid $625) | | $4,500 | $3,875 | $625 | — | Taxpayer elects line 36 = $625, line 35a = $0: the same $625 overpayment, split entirely to "applied," never "refunded" — line 34 is unchanged by the election; only its disposition across 35a/36 differs |
| Senior (line 13b) + dependent (line 12e) carried to the bottom line | Uses the senior-and-dependent-deductions milestone's own case 1 ($6,000 line 13b) or dependent case (line 12e capped) as the **line 15/16/22** starting point; 25a/33/34/37 compute exactly as any other case once 22 is known | — | — | — | — | — | — | Confirms this milestone's lines compose cleanly on top of that milestone's content — no special-casing needed at 22-38 for either feature |
| No new question answered | Any withholding/absence fact (23's absence, 25a's box2, 26, 27-32's absences) left unasserted | — | — | — | — | — | **Blocked**, `DEPENDENCY_ABSENT`, naming the missing fact — never a silent $0, matching every existing absence pattern in this corpus (Sec. 4) |
| Existing goldens | — | — | — | — | — | — | Unaffected: every change here is new content (new fact types, new rules, a new package/registry/release version); no published schema, package, parameter, or rule version is edited, so every adopted golden keeps its existing package and result |

## 7. Change list

**New fact types (content only, `fact-type.v2`):**
- `tax.us.2025.w2.box2-withholding` (same identity keys as box1-wages).
- `tax.us.2025.f1099int.box4-withholding`, `tax.us.2025.f1099div.box4-withholding`,
  `tax.us.2025.f1099r.ira-box4-withholding` (companion on the existing IRA
  family).
- Widened/replacement amount facts for `tax.us.2025.f1099g.box4-...` and
  `tax.us.2025.ssa1099.box6-withholding` if those documents are brought into
  scope (today's facts cannot hold a nonzero value at all; see Sec. 2).
- `tax.us.2025.schedule2-partii-scope.no-line21-additional-taxes` (line 23).
- One absence each for 27a (EIC), 28 (ACTC), 29 (AOC), 30 (adoption credit),
  31 (Schedule 3 Part II total) — none reusable from existing facts (Sec. 4).
- An estimated-tax-payments fact for line 26 (elective, taxpayer-entered
  amount, not a statement box).
- A line-36-election fact (amount applied to 2026, paired with 35a).

**New source families + closures:** one pair per new per-document
withholding fact that aggregates across multiple statements (W-2 box2,
1099-INT box4, 1099-DIV box4) — each scoped narrowly to its own fact type,
mirroring box1's own family/closure (they cannot be shared; Sec. 3).

**New rules (one per Form 1040 line, per the charter):** 23, 24, 25a, 25b,
25c, 25d, 26, 27a (absence-gated $0), 28-31 (absence-gated $0 each), 32, 33,
34, 35a, 36, 37. A new consumer rule for the already-recorded
`tax.us.2025.f1099k.box4-federal-withholding` if 1099-K backup withholding
is brought into 25b/25c scope.

**Successors:** one new core-calculations package, one new
`published-packages` registry entry, one new release. No published schema,
adopted package, parameter, or rule version is edited — every item above is
new content and new rule versions only.

**Recommended withholding scope, with cost:**
- **W-2 box 2 (in scope).** Lowest cost: reuses the exact box1 shape
  (fact type, family, closure, `collect`+`add`+`round` rule) with no
  schema/op/engine change. Directly matches the plan's "starting with
  Form W-2 box 2."
- **1099-INT and 1099-DIV box 4 (recommended in scope).** Same low cost as
  W-2 box 2 — one new fact type, family, closure, and rule each, no new
  vocabulary. Both documents are already read for their income boxes, so
  the statement/payer entities already exist; only the withholding field is
  new.
- **1099-R box 4 (recommended in scope, slightly higher cost).** Needs a new
  same-statement companion fact on the existing bounded IRA family (one more
  entry in `loader.py`'s `domain_companion_fact_types`), not a new family —
  moderate cost, same engine-change-free conclusion.
- **1099-K box 4 (recommend deferring to the owner).** The fact and its real
  value already exist; the only new work is a consumer rule, which is cheap
  — but which Form 1040 line (25b or 25c) it belongs on is not settled by
  any source this P0 read (the 2025 instructions never name Form 1099-K
  under lines 25a-25c at all), so this is an owner decision, not a cost
  question.
- **1099-G box 4 and SSA-1099 box 6 (recommend deferring).** Both require
  *removing* an existing admission bound that currently blocks any nonzero
  value outright (not merely adding a rule) — higher cost and a visible
  behavior change to a route this engine already ships, which the charter's
  non-goals ("no edit to any published schema, adopted package, parameter,
  or rule version; only successors") allow as a successor but which the
  owner should see named explicitly before it is built.
- **Schedule K-1 (Form 1065) (out of scope, not a cost question).** No
  federal-withholding box exists on the form the engine reads; there is
  nothing to record.

## Stop conditions checked

None triggered. No source contradicted the plan's scope — the plan's
account of lines 22-38 and the withholding landscape (Section "What we
know") is confirmed in every particular this P0 checked. Recording every
withholding box found needs new *content* only (fact types, source
families/closures, rules, a parameter or two) — no schema successor, no new
expression operation, and no engine (Python) change, for either the W-2 box
2 route or any of the new-fact-type routes in Sec. 2 above (the 1099-G/
SSA-1099 bound-widening cases are a content change to a *fact type's*
admitted domain, not a schema, expression-vocabulary, or engine change,
though they are flagged above as a visible behavior change worth the
owner's attention). The probe reached the real coordinator with no
production-code change, after one superseding elective assertion to work
around a pre-existing, by-design block in the base builder's own default
(Sec. 5) — not a change to any rule, schema, or package.

## Track 1 decisions

Recorded after Track 1's build, per the Foreman's repair-round direction,
so `packages/tax/loader.py` carries only the companion-presence pairs that
were actually added, not a note about a rejected one.

- **1099-R box 4 companion presence, considered and rejected.**
  `packages/tax/loader.py`'s `domain_companion_presence_pairs()` is
  installed globally (`tax_registry()`), with no package-version scoping —
  the companion-presence check runs at admission time, before any package
  is even adopted. Adding box 4 as a required same-statement companion of
  the IRA box-1 fact there would retroactively require box 4 on every
  existing IRA box-1 assertion, breaking 8 tests in
  `tests/test_form1099r_ira_line4b_track2.py` (an existing golden on
  `main`) that assert box 1 without a box-4 answer. Not added; box 4 is
  recorded and aggregated (`tax.us.2025.f1099r.ira-box4-withholding`,
  `rule.f1099r-box4-subtotal`) without presence enforcement — a recorded
  distribution without a box-4 answer is not separately detected.
- **Form 1099-K box 4, parked — two independent causes.** (1) A new source
  family naming the already-published `tax.us.2025.f1099k.box4-federal-
  withholding` as its `member_predicate` retroactively requires
  `member-transition` for every existing plain-assertion use of that fact
  (`packages/kernel/findings.py`'s SC-R1 check reads
  `registry.family_member_predicates`, populated from the whole content
  corpus by `tax_registry()`, unscoped by package version) — breaking 9
  tests in `tests/test_f1099k_statement_removal_increment_c.py` and
  `tests/test_family_handover_recording.py` on `main`. (2) Independently,
  reusing the existing box-1a family's own closure to publish a second
  subtotal symbol is forbidden by ADR-0016 (one family authorizes exactly
  one subtotal). Line 25b sums three document subtotals (1099-INT,
  1099-DIV, 1099-R), not four; Form 1099-K box 4 stays recorded and summed
  nowhere, same as P0 found it.
- **Missing W-2 box 2, repaired.** Line 25a v2 (repair round 1) publishes
  only when the current count of W-2 box-2 statements equals the current
  count of W-2 box-1 statements (`count` op, same shape
  `rule.form1040-line12e` v1 already uses with a `source_set`); a mismatch
  falls through to a `ref` on `tax.us.2025.w2.box2-withholding`, which is
  never a bound scalar symbol, so it raises `DEPENDENCY_ABSENT` naming that
  exact fact — existing vocabulary only (`any`/`compare`/`count`/`ref`), no
  new op. `$0` is a valid, equal-count answer, not an absence. The Foreman
  will park the equivalent repair for 1099-INT, 1099-DIV, and 1099-R.
