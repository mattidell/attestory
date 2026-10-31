# P0: trace the gambling-loss refusal and design Schedule A line 16

Milestone: `gambling-losses` (plan `docs/phases/engine-breadth/milestones/gambling-losses.md`).
Source ref: `38c375c3`, branch `milestone/gambling-losses-2025`, core v66 / release v64 /
registry v64. Evidence here: `probe.py` and `probe-output.json` (live, `live_coordinate_run`).
Content, rules, packages, schemas, engine and tests are unchanged by P0.

Primary sources are the ignored local files under `temp/tax-on-taxable-income/sources/`;
`i1040gi` is `i1040gi-2025.txt`, `publ119` is `publ119-21.txt`.

## Summary

- Today a Form W-2G filer whose Schedule A gambling answer is "no" is refused in the
  winnings subtotal, so the whole return stops at Schedule 1 line 8b and everything below
  it, standard deduction or not. The Schedule A attachment is refused separately when it is
  required.
- Line 16 can be added with content successors only. The deduction choice (line 12e) reads
  the new line through a successor of its own rule; no engine, kernel or schema change is
  needed. The closed operation vocabulary has no `min`, but `choose` with a comparison
  expresses it (the line 8a rule uses the same `choose` shape for its limit test).
- One thing the plan did not name: the existing declaration
  `schedule-a-boundary.no-gambling-other-declared` means "no gambling losses **and** no other
  line 16 deduction". A "no" cannot say which, so v67 needs a narrower declaration and a
  losses family; the old fact is left inert.
- Two decisions need the owner (D1 adoption cost, D2 the hand-entered itemized total); see the
  end. Neither is a stop condition. None of the three charter stop conditions is met.

## 1. Law

What the local sources support, and what they do not.

| Claim | Local support | Status |
| --- | --- | --- |
| Gambling winnings are income on Schedule 1 line 8b; losses go to Schedule A line 16 | i1040gi l.6564-6571: "Gambling. Enter gambling winnings not attributable to a trade or business ... For details on gambling losses, see the instructions for Schedule A, line 16." | Supported |
| Schedule A is how itemized deductions are figured; the choice is the larger of standard and itemized | i1040gi l.2221-2222 ("To figure your itemized deductions, fill in Schedule A"), l.2223-2225 ("you take the larger of your standard deduction or itemized deductions") | Supported |
| 2025 single standard deduction is 15,750 | i1040gi l.224-228 ("For 2025 ... $15,750-Single or Married filing separately"), f1040 l.96 (and the engine's own parameter) | Supported |
| Losses are limited to winnings | **Not in the local sources.** The Schedule A instructions are not present (only the Form 1040 instructions, Schedule 1-A, Schedule 8, Schedule SE, Pub. 596, the W-2 instructions, Rev. Proc. 2024-40 and P.L. 119-21). `publ119` restates the rule for later years only (below) | Plan statement; needs the Schedule A instructions for a cite |
| 100 percent of losses (not 90) applies to 2025 | `publ119` sec. 70114 (l.5392-5408) replaces section 165(d) with "90 percent of the amount of such losses ... allowed only to the extent of the gains from such transactions", effective "taxable years beginning after December 31, 2025". 2025 is outside that, so the 90 percent does not apply to 2025. The prior 100 percent text of 165(d) is not in the local sources | Supported by exclusion; the 100 percent figure itself is the plan's |
| A standard-deduction filer reports losses nowhere | **Not in the local sources.** What is supported is the structure: the only destination named for losses is Schedule A line 16 (l.6570-6571), and Schedule A exists only for itemizers (l.2221). No line of any local source gives a standard-deduction filer a place to report them | Inferred from structure; confirm in the Schedule A instructions |
| Wagering expenses (travel and the like) count as losses for 2025 | **Not in the local sources** for 2025. `publ119` l.5404-5406 states the "includes any deduction otherwise allowable ... incurred in carrying on any wagering transaction" rule, but only for years after 2025 | Open. The losses fact should be worded as "losses from wagering transactions" and say plainly that expenses are not asked for here (D3) |

Missing for a proper cite: Schedule A instructions line 16 (2025), and the section 165(d)
text for 2025. The first Track 1 step should add them to `temp/` or the cite stays a plan
statement.

## 2. Today (reproduced, core v66)

`probe.py` runs ten returns through `live_coordinate_run` on v66: five shapes, each with the
Schedule A gambling answer "yes" (control) and "no" (the filer has losses). Base: single,
wages 50,000, 4,500 withheld; W-2G box 1 = 6,000, box 4 = 1,440 where a W-2G is recorded.
An itemizer is built two ways: Path B (a Form 1098 statement of 20,000 interest with the
circumstance answers, `f1098-scope.no-mortgage-statement` = false) and Path A (no Form 1098
statement, raw `deductions.itemized` assertion of 20,000).

| Return | Answer | Result | Refused by |
| --- | --- | --- | --- |
| W-2G, standard deduction | yes | bottom line, refund 1,345 | |
| W-2G, standard deduction | **no** | no AGI, taxable income, tax or refund | `rule.w2g-b1-subtotal` is **held** (not applicable): it reads the declaration inside its `when` and publishes only when it is "yes". Then `rule.schedule1-line8b` blocks `DEPENDENCY_ABSENT` on `gambling.b1-winnings-subtotal`, and Schedule 1 line 10, `rule.attachment.schedule-1`, line 8, AGI and everything below block in turn. Line 12e (15,750) and `schedule-a.total` (0) still publish; Schedule A is not required |
| W-2G, Path B itemizer | yes | bottom line, refund 1,855, Schedule A required (excess over standard 4,250) | |
| W-2G, Path B itemizer | **no** | no AGI or below. Same chain as above **plus** `rule.attachment.schedule-a` blocks `COMPLETENESS_VALUE_VIOLATION` (`no-gambling-other-declared=no`). Line 12e = 20,000 still publishes | The same held winnings subtotal; the attachment is a second, independent refusal |
| W-2G, Path A itemizer (assertion 20,000) | yes | bottom line, refund 1,855; line 12e 20,000; **Schedule A is never required** (`schedule-a.total` = 0) | |
| W-2G, Path A itemizer | **no** | the same winnings-subtotal chain | `rule.w2g-b1-subtotal` held |
| no W-2G, standard | no | unchanged from "yes": refund 625 | nothing: the declaration is not read with no W-2G |
| no W-2G, Path B itemizer | no | bottom line published (refund 1,135), but `rule.attachment.schedule-a` blocks `COMPLETENESS_VALUE_VIOLATION` | the attachment alone |

Reading it:

1. **The refusal is by answer, not by arithmetic.** The held rule and its blocked chain are the
   whole of it for a standard-deduction filer. The reason a standard filer is refused today is
   that the winnings subtotal asks the question at all; losses change nothing on that return.
2. **A second, independent refusal sits in the Schedule A attachment's completeness.** It fires
   whenever Schedule A is required and the answer is "no", with or without a W-2G. The
   successor attachment must stop requiring "yes" for gambling or the itemizer stays refused
   after the subtotal is freed.
3. **Path A itemizers never produce a Schedule A.** The attachment compares `schedule-a.total`
   (line 8a only, 0 when there is no Form 1098) with the standard deduction, so a hand-entered
   itemized total of 20,000 never makes Schedule A required. This is already true in v66, not
   something the milestone introduces, but line 16 interacts with it (D2).
4. The probe builds the first committed v66 itemizer with a populated Schedule A (Path B needs
   the Form 1098 circumstance answers; the older Form 1098 harnesses sit on pre-v59 bases).

## 3. Design

### The losses facts, family and closure

New bundle `tax.us.2025.gambling-losses.vocabulary` v1:

- `tax.us.2025.gambling.loss` (nature determinable, free supersession): one loss entry,
  nonnegative number. Identity: one entity key `loss` (new entity kind
  `tax.us.gambling-loss-entry`) and the tax-year literal. Title: losses from wagering
  transactions for 2025 as the filer would total them for one entry; not winnings, not a
  professional gambler's business losses, and not wagering expenses (D3).
- `tax.us.2025.gambling.losses.source-closure`: boolean, family horizon plus tax year, the
  same shape as `tax.us.2025.w2g.b1.source-closure`.
- `tax.us.2025.schedule-a-boundary.no-other-line16-declared`: yes/no, tax year. "I have no
  Schedule A line 16 deduction other than gambling losses." Successor of the narrower meaning
  (see "Existing workspaces").

Family `tax.us.2025.gambling.losses` (source-family.v1) and closure mapping
`tax.us.2025.closure-mapping.gambling-losses` (source-closure-mapping.v2, condition
`current-literal-true`) admit `tax.us.2025.gambling.losses-subtotal`. The closure claim says it
covers gambling losses only: nothing about winnings, wagering expenses, or other line 16
deductions. Confirmed complete like every other family: closed-empty authorizes 0; an
unconfirmed or stale closure blocks `SOURCE_SET_UNCLOSED`, never a partial sum.

`rule.gambling-losses-subtotal` v1 (schema rule-artifact.v4): `when` `require_closed`
on the family; value the sum of the family's members **with cents** (the itemization-cents
stance: the subtotal does not round; the line that reads it rounds once).

### Schedule A line 16 (limited to winnings)

`rule.schedule-a-line16` v1 publishes `tax.us.2025.schedule-a.line16`, composition
`tax.us.2025.schedule-a`:

- `when`: `require_closed` on `tax.us.2025.w2g.b1` (it already reads the winnings subtotal), and
  a `conditional_dependency_set` (the v2 winnings-subtotal shape) that adds
  `gambling.losses-subtotal` only when the W-2G box 1 count is not 0. With no W-2G recorded the
  losses family is **not** read.
- value: `choose(count(b1) = 0, 0, choose(losses <= winnings, losses, winnings))`, where winnings
  is `gambling.b1-winnings-subtotal`. That is `min(losses, winnings)` without a new operation;
  `min` is not in the closed vocabulary (`packages/derivation/loader.py` OPERATION_VOCABULARY)
  and is not needed.
- It cannot be negative: both inputs are nonnegative sums.

The limit is the winnings that reach Schedule 1 line 8b, so it is the same number the return
reports as income, and a reader can see both on one explanation. The disallowed part
(`losses-subtotal` minus line 16) is derivable from two published symbols; no field for it is
proposed.

### Successors

| Citizen | From -> to | What changes |
| --- | --- | --- |
| `rule.w2g-b1-subtotal` | v2 -> v3 | Stops reading `no-gambling-other-declared`: `when` is `require_closed` only. Still sums with cents. Nothing else changes |
| `rule.schedule-a-total` | v1 -> v2 | `requires` and adds `schedule-a.line16`: value `line8a + line16`. Same Form 1098 count > 0 guard |
| `rule.schedule-a-total-closed-empty` | v1 -> v2 | value `line16` (was 0). Same count = 0 guard. v1 had no `requires` on purpose; v2 must require `line16`, so the "always immediately eligible" property is lost. Track 1 must show saturation ordering (line 16 has no dependence on the total, so none is expected) |
| `rule.form1040-line12e` | v2 -> v3 | The itemized side adds `schedule-a.line16` on every route (Path B: `line8a + line16`; Path A: see D2). Adds `schedule-a.line16` to `requires` and the `conditional_dependency_set` |
| `rule.attachment.schedule-a` | v2 -> v3 (attachment-rule.v4 grammar) | Adds a second itemization part `line-16-gambling-losses` (single_family over the new family; one row_set; `subtotal_symbol` and `tie_out.line_symbol` both `gambling.losses-subtotal`, the **raw** subtotal: the cap lives in the line 16 rule, the same shape as the Track 4b student-loan fix, `rule.attachment.schedule-1.v4.json` title). Replaces the required `no-gambling-other-declared` = yes check with `no-other-line16-declared` = yes |
| `rule.schedule-a-boundary-no-gambling-other` | v1 removed; `rule.schedule-a-boundary-no-other-line16` v1 added | Same pattern (gates on the declaration; consumed by nothing). The old fact type stays in its published bundle, inert in v67 |

`rule.schedule-a-excess-over-standard`, `rule.schedule-a-line8a`, the standard-deduction rules
and every rule below line 12e are unchanged: they read `schedule-a.total` and `line-12e`.

### How losses enter the standard-or-itemized choice

They must. Line 12e is `max(standard, itemized)`. A filer whose losses (up to winnings) exceed
the standard deduction on their own should itemize; today's route could never see that. So line
12e reads line 16, by successor. This is an ordinary content change (one rule), not an engine
change. It is the case the plan's non-goal carved out ("unless P0 shows the losses must enter
it"). Hand case 2 shows it matters (a 935 refund difference).

A filer on the standard deduction whose losses are small gets exactly their no-loss return
(hand case 1): `max` picks the standard deduction and line 16 is shown but unused. That also
holds for a tie (hand case 7, the existing deterministic tie-to-standard).

### Form fields

None new. Line 8a, the only other populated Schedule A symbol, has no form field; Schedule A is
presented by the attachment's itemization parts. Line 16 is published as a symbol and appears in
the line 12e explanation and in the attachment's itemization part. Adding a Schedule A line field
is a presentation change (the form-field projection joins exactly one disposition row per
field symbol) that the plan does not ask for; Track 1 may add it as an optional extra if the
presentation tests make it cheap.

### The v66 -> v67 change set

Entrypoint replacements follow the rule in the W-2G design: only successors that are entrypoints
on v66 change entrypoints. Checked against `package.core-calculations.v66.json`.

| Op | Citizen | Entrypoint effect |
| --- | --- | --- |
| add | bundle `tax.us.2025.gambling-losses.vocabulary` v1 | none |
| add | source-family `tax.us.2025.gambling.losses` v1 | none |
| add | closure mapping `tax.us.2025.closure-mapping.gambling-losses` v1 | none |
| add | `rule.gambling-losses-subtotal` v1 | none |
| add | `rule.schedule-a-line16` v1 | none (read by 12e and the totals) |
| add | `rule.schedule-a-boundary-no-other-line16` v1 | add entrypoint (as its v1 sibling) |
| remove | `rule.schedule-a-boundary-no-gambling-other` v1 | remove entrypoint |
| replace | `rule.w2g-b1-subtotal` v2 -> v3 | not an entrypoint on v66 |
| replace | `rule.schedule-a-total` v1 -> v2 | replace entrypoint |
| replace | `rule.schedule-a-total-closed-empty` v1 -> v2 | replace entrypoint |
| replace | `rule.form1040-line12e` v2 -> v3 | replace entrypoint |
| replace | `rule.attachment.schedule-a` v2 -> v3 | replace entrypoint |
| fixtures | core v67, registry v65, release v65 (`tools/package_successor.py`), `conflict_semantics` selected producer for `schedule-a.total` stays `rule.schedule-a-total` v2 | |

Thirteen citizens, within the 11-per-track guidance only if the two rules that "add" and the
fixtures are counted as one track; treat it as one atomic track. **It must be one track**:
shipping the winnings successor without the line 12e and total successors would compute an
itemizer's return with losses silently ignored, which is worse than the refusal. An alternative
order (everything but `w2g-b1-subtotal` first, the refusal removed last) is available if the
owner wants two commits; the refusal must be the last step.

Collect-closure survey and its regression expectations (`tools/collect_closure_survey`, the
`KNOWN_GAP_ATTACHMENTS_V63` style lists) gain the new family; Track 1 must confirm.

### Existing workspaces: what they are asked on adoption (v66 -> v67)

| Workspace | Asked |
| --- | --- |
| No W-2G, any deduction route | **Nothing new.** Line 16 is 0 without reading the losses family (the conditional dependency), the old `no-gambling-other` answer is ignored. A Schedule A itemizer is additionally asked `no-other-line16-declared` (one yes/no) because the attachment's completeness now reads it instead of the old answer |
| W-2G recorded, old answer "yes" | One closure confirmation of the losses family (closed-empty = "no gambling losses"). Their figures do not change once confirmed. Until then the return stops at line 12e (D1) |
| W-2G recorded, old answer "no" (the refused ones) | Enter the losses (each entry), confirm the family closed, and, if they itemize, answer `no-other-line16-declared` (their old "no" cannot tell losses from other line 16 deductions) |
| W-2G recorded, standard deduction | The same losses closure; no Schedule A is produced and no other question is added |

D1 below decides whether the W-2G/old-"yes" row asks anything.

## 4. Cases (hand-computed)

Single, wages 50,000, 4,500 withheld, 2025 standard deduction 15,750. Tax from the 2025 Tax
Table (rows of 50, midpoint, half up; the same convention the W-2G cases use). W-2G: box 1 W,
box 4 = 24 percent of W. Path B is a Form 1098 with 20,000 interest. All values are what the
v67 design must produce; v66 cannot produce any "with losses" row.

| # | Case | Line 16 | Itemized | Line 12e | Taxable | Tax | Payments | Refund |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Baseline v66: W-2G 6,000, no losses, standard | 0 | 0 | 15,750 | 40,250 | 4,595 | 5,940 | 1,345 |
| 1 | Standard deduction **with** losses 2,000 (W 6,000) | 2,000 | 2,000 | 15,750 | 40,250 | 4,595 | 5,940 | **1,345 (same as 0)** |
| 2 | Standard-deduction filer whose losses reach the itemizing range: W 20,000 (box 4 4,800), losses 20,000, no other itemized deduction | 20,000 | 20,000 | **20,000** | 50,000 | 5,920 | 9,300 | 3,380 (standard would be 54,250 / 6,855 / 2,445) |
| 3 | Itemizer (Path B, 20,000), W 6,000, losses 2,000 (below winnings) | 2,000 | 22,000 | 22,000 | 34,000 | 3,845 | 5,940 | 2,095 (no losses: 36,000 / 4,085 / 1,855) |
| 4 | Itemizer (Path B), W 6,000, losses 9,000 (above winnings) | **6,000** (limited) | 26,000 | 26,000 | 30,000 | 3,365 | 5,940 | 2,575; 3,000 disallowed and shown |
| 5 | Losses with **no winnings recorded** (no W-2G), Path B, losses 2,000 | 0 | 20,000 | 20,000 | 30,000 | 3,365 | 4,500 | 1,135 = v66 value (probe `itemizer_1098_no_w2g_losses-yes`); the losses family is not read |
| 5b | Same, standard deduction | 0 | 0 | 15,750 | 34,250 | 3,875 | 4,500 | 625 = v66 |
| 6 | **Unconfirmed** losses family (W 6,000, losses 2,000 recorded, closure never or stale) | blocks `SOURCE_SET_UNCLOSED` on `gambling.losses` | blocks | blocks | blocks | blocks | 5,940 publishes | blocks. AGI 56,000 still publishes. Not an unfavorable result: an unresolved one |
| 7 | Tie: W 20,000, losses 15,750, no other itemized | 15,750 | 15,750 | 15,750 (standard; the tie favors it) | 54,250 | 6,855 | 9,300 | 2,445; Schedule A not required (excess 0, not strictly greater) |

Notes on the hand values:

- Case 0's figures are the W-2G milestone's case 2 and the probe's `standard_w2g_losses-yes`
  and agree. Cases 3 and 4 use the probe's Path B itemizer (`itemizer_1098_w2g_losses-yes`:
  36,000 / 4,085 / 1,855) as their no-loss control.
- Case 2 uses Path A (no Form 1098 statement, no itemized assertion): the itemized side is
  the assertion's default 0 plus line 16. Schedule A is required (20,000 > 15,750) and carries
  only line 16; it is complete because the other categories are answered "yes".
- Case 5 is the Schedule A-side invariant: line 16 is 0 whenever no W-2G is recorded, so a
  losses entry without winnings never changes a return. The losses are shown as disallowed
  100 percent in the explanation (if the family is closed) rather than refused.
- Case 6 shows why a W-2G filer on the standard deduction must confirm the losses family: the
  choice cannot be made without it (case 2).

## 5. Stop conditions

1. *The standard-or-itemized choice cannot read the new line without an engine change.* Not
   met. Line 12e v3 reads `schedule-a.line16` by content successor; `min` is expressed by
   `choose`.
2. *The honest class needs Schedule C.* Not met. Non-professional winnings that reach line 8b
   (W-2G) with losses to line 16 is Schedule A only. Professional gamblers and wagering
   expenses stay out (D3).
3. *A v66 return without gambling losses would change.* Not met on figures: every v66 return
   that published a result publishes the same figures. A v66 return that has a W-2G (answer
   "yes") would, under the closure-only design, stop at line 12e until the filer confirms
   "no gambling losses". Whether that counts as a change is D1; the design offers an
   alternative that changes nothing.

## Decisions for the owner

**D1. Adoption cost for existing W-2G returns.** Recommended: **closure only.** Every W-2G
workspace confirms the losses family once (closed-empty), the old answer is ignored in v67,
and the design stays uniform ("confirmed complete like any other family"). Cost: a v66 W-2G
return with answer "yes" is blocked at line 12e on v67 until it answers; figures unchanged
afterward. Alternative: **carry the old "yes" forward** (line 16 is 0 and the losses family is
not read when the old declaration is "yes"; otherwise the family is read). Nothing existing
changes, but "yes" then silently carries two meanings and the rule has an `any(declared = yes,
require_closed(...))` branch that Track 1 must prove (the evaluator short-circuits `any`; the
declaration's absence blocks before the closure is tried).

**D2. The hand-entered itemized total (Path A) with losses.** Line 12e's raw assertion
`tax.us.2025.deductions.itemized` is "Taxpayer asserted itemized deductions for 2025" and
today bypasses Schedule A entirely (section 2, point 3). Adding line 16 to it risks counting losses
twice (a filer who already put them in the total) and leaves a Schedule A that shows line 16
only while line 12e uses assertion plus line 16. Recommended: **on Path A, block by name when
both the assertion is non-zero and line 16 is non-zero** (a named code, in the style of
`F1098_SCOPE_CONTRADICTION`); allow Path A with an unasserted (zero) total, where line 16 is the
whole itemized deduction and Schedule A matches line 12e (case 2). Alternative: always add line
16 and say in the explanation that the asserted total must exclude gambling losses, accepting
the possible double count and the incomplete Schedule A.

**D3. Scope words.** (a) The losses fact is "losses from wagering transactions", not
expenses; the 2025 treatment of wagering expenses is not in the local sources (Law). (b) A
filer with losses but no W-2G winnings is not refused: line 16 is 0 and the return is
unchanged (case 5). If the owner prefers a refusal there (winnings may exist without a W-2G,
which the engine already refuses by answer), say so before Track 1.

## Open items for Track 1 to prove (none is a design change)

- The attachment grammar admits a second itemization part whose tie-out line is the raw
  subtotal and whose family may be unclosed when no W-2G is recorded (a guard or the part is
  skipped). If it cannot be skipped, every Schedule A itemizer must confirm the losses family
  (the same closure ask as D1, for itemizers).
- Saturation ordering for `rule.schedule-a-total-closed-empty` v2 once it has `requires`.
- Line 12e v3 against the other Path A / Path B branches the Form 1098 contradiction tests
  already cover; and cents on line 16 (the 12e figure carries cents today, '20000.0').
- The Schedule A instructions and section 165(d) text added to the local sources.
