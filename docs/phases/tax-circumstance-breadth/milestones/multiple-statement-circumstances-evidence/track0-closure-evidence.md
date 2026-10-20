# Track 0 Closure Evidence — Multiple Form 1099-K Statements

Audience: Foreman.
Purpose: Track 0 adversarial closure evidence.
Gate: `PROJECT_PLANNING.md` "Track 0 Adversarial Closure Gate"
Probe: `test_track0_closure_probe.py` (executed live coordinator test suite in this directory)

This evidence artifact supplies the measured facts and table shapes required for Track 0 adversarial closure of the multiple Form 1099-K connected sale capability, following ADR 0079 and the connected sale design (`connected-sale-design.md`).

---

## 1. Authority-Lifecycle Table

This table enumerates every contributed fact, reused declaration, aggregate declaration, and absence authority on which the multiple-statement Form 1099-K capability relies.

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| :--- | :--- | :--- | :--- | :--- |
| `tax.us.2025.f1099k.box1a-gross-amount` | Amount reported in Box 1a of Form 1099-K furnished to taxpayer for tax year 2025 | Statement subject `(payer, statement, tax-year)` | Documentary submission / evidence | Statement correction, statement removal, act log rewind |
| `tax.us.2025.f1099k.box4-federal-withholding` | Federal income tax withheld reported in Box 4 of Form 1099-K | Statement subject `(payer, statement, tax-year)` | Documentary submission / evidence | Statement correction, statement removal |
| Circumstance answers (15 questions: `covers-only-single-item`, `purchase-cost`, etc.) | Taxpayer-attested circumstance answer for personal item sale on statement | Statement subject `(payer, statement, tax-year)` | Taxpayer attestation / submission | Answer correction, answer withdrawal, statement removal |
| Predecessor closure authority (v1) | All 2025 Form 1099-K statements recorded up to horizon under v1 single-statement contract | Family horizon chain v1 for `(subject, tax-year)` | Attested closure on v1 horizon | Subsequent member addition on v1, or family handover to v2 |
| Successor closure authority (v2) | All 2025 Form 1099-K statements recorded up to horizon under v2 multi-statement sum contract | Family horizon chain v2 for `(subject, tax-year)` | Attested closure on v2 horizon | Subsequent member addition or member removal on v2 |
| `tax.us.2025.f1099k.box1a-subtotal` | Raw unrounded sum of present Form 1099-K Box 1a member facts under ADR-0016 collect authority | Current member set of family v2 | Present Box 1a member findings | Any member addition, removal, or member Box 1a correction |
| `tax.us.2025.schedule1.top-entry` | Combined eligible personal item sale loss amount entered at the top of 2025 Schedule 1 | Closed family v2 and all member statement subjects | Family closure v2, raw subtotal v1, per-statement reason findings | Family horizon advancement (new/removed member), answer withdrawal, statement correction, or non-loss reason |
| `tax.us.2025.rule.attachment.schedule-1` (disposition) | Itemized attachment schedule supporting Schedule 1 personal item sale loss | Closed family v2 and all member statement subjects | Family closure v2, raw subtotal v1, member statements | Family unclosed, member addition/removal, top-entry blocked |
| `tax.us.2025.rule.f1099k-unresolved` (disposition) | Status flag indicating whether any Form 1099-K statement requires further review | Family v2 statements | Member statements, per-statement reason findings | Statement answer changes, reason changes |

---

## 2. Empty/Nonempty Authority Matrix

This matrix exercises the six materially distinct family states for Form 1099-K (v2) and their downstream impact on Schedule 1 top entry, and the Schedule 1 attachment; Form 1040 income and tax do not read the entry.

| Family state | Universe / absence authority | Eligibility or applicability | Expected feature result (Top Entry) | Expected neighboring result (Attachment) | Measured probe test |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Closed empty** | Complete absence authority recorded (`record_f1099k_no_statements_durably`, v2) | Inapplicable (zero statements) | Published `$0.00` (default path: `count == 0`) | Attachment: inapplicable (`test_case4`). Form 1040 income and tax do not read the entry. | `test_case4_closed_empty_v2` |
| **Closed empty (missing authority)** | Required absence authority missing (unclosed empty family) | Any | Blocked (`SOURCE_SET_UNCLOSED`, code `BLOCK_CLOSURE`, missing `tax.us.2025.f1099k`) | Attachment: blocked (`BLOCK_CLOSURE`). Downstream return totals block along dependency. | `test_case5b_unclosed_empty_family` |
| **Nonempty, eligible** | Complete closure authority on current horizon; all statements eligible (`supported-loss`) | Positive | Computed and published (sum of Box 1a: `$1,340.00`) | Attachment: published with 2 row items tying out to `$1,340.00`. Form 1040 income and tax do not read the entry. | `test_case1_two_supported_losses_sum_published` |
| **Nonempty, ineligible (published non-loss)** | Complete closure authority; 1 supported loss beside 1 published non-loss (`cost-basis-unknown`) | Negative | Blocked (`DEPENDENCY_ABSENT`, top entry not published) | Attachment: blocked. Unresolved rule: blocked. Sibling statements keep independent review status. | `test_case2_one_supported_loss_beside_published_non_loss` |
| **Nonempty, ineligible (excluded use)** | Complete closure authority; 1 supported loss beside 1 excluded statement (`prior-depreciable-use-excluded`) | Negative | Blocked (`DEPENDENCY_ABSENT`, top entry not published) | Attachment: blocked. Sibling statements keep independent review status. | `test_case6_gain_or_excluded_statement_beside_supported_loss` |
| **Nonempty, unclosed** | Statements present, but closure authority missing for current horizon | Positive answers present | Blocked (`SOURCE_SET_UNCLOSED`, code `BLOCK_CLOSURE`, missing `tax.us.2025.f1099k`) | Attachment: blocked (`BLOCK_CLOSURE`). Downstream return totals block along dependency. | `test_case5a_unclosed_with_statements` |
| **Nonempty, blocked subject** | Complete closure authority; one subject's reason calculation blocks | Blocked subject | Blocked (`DEPENDENCY_INVALID`, naming subject's Box 1a fact ID) | Attachment: blocked. Candidate C selection contract catches blocked entry via `reads_subject_results`. | `test_case3_blocked_subject` |

---

## 3. Late-Authority Counterexample (Paper Trace)

The paper trace executes:
```text
attest → close → compute → add member → reclose → recompute
```
Measured in `test_case7_late_member_trace` over real coordinator execution and currency projection, recording the exact observed identifiers:

1. **Step 1: Attest Statement A**
   - Statement A recorded: payer `demo.platform.alpha`, ref `demo.statement.bicycle`, Box 1a `$880.00`.
   - Box 1a finding: `f1099k.b1a.finding.f1099k.statement.c7.sub.a` on fact `tax.us.2025.f1099k.box1a-gross-amount|payer=demo.platform.alpha,statement=stmt.demo.platform.alpha.2025.demo.statement.bicycle,tax-year=2025`.
   - Answers saved via `save_f1099k_statement_review`. Family is unclosed on horizon `demo.f1099k.h36`.
2. **Step 2: Close Family (Horizon `demo.f1099k.h36`)**
   - Closure finding attested: `f1099k.closure.finding.close.0` on fact `tax.us.2025.f1099k.source-closure|family-horizon=demo.f1099k.h36,tax-year=2025`.
   - `compute_currency` verifies: Box 1a finding and `close.0` are both in `current_finding_ids`.
3. **Step 3: Compute (Run 1)**
   - Run 1 completes without refusal.
   - Schedule 1 top entry publishes `$880.00`, pinning `f1099k.closure.finding.close.0` and Statement A reason finding (`supported-loss`).
   - Attachment publishes itemization for part `sch1-top-entry-f1099k` with `$880.00` tie-out.
4. **Step 4: Add Member Statement B (Unclosed)**
   - Statement B recorded: payer `demo.platform.beta`, ref `demo.statement.camera`, Box 1a `$460.00` (`close_family=False`).
   - Member transition advances the family horizon chain from `demo.f1099k.h36` to `demo.f1099k.h37`.
   - **Invalidation observation:**
     - Prior closure finding `f1099k.closure.finding.close.0` is **immediately displaced** (in `displaced_finding_ids`, removed from `current_finding_ids`).
     - Prior Run 1 top entry publication is obsolete because its pinned closure `close.0` is non-current.
     - An intermediate run at this point refuses publication: top entry blocks with code `BLOCK_CLOSURE` (`SOURCE_SET_UNCLOSED`), missing `tax.us.2025.f1099k`.
5. **Step 5: Reclose Family (Horizon `demo.f1099k.h37`)**
   - Fresh closure finding attested: `f1099k.closure.finding.close.1` on fact `tax.us.2025.f1099k.source-closure|family-horizon=demo.f1099k.h37,tax-year=2025`.
   - `compute_currency` verifies: `close.1` is in `current_finding_ids`; `close.0` remains displaced. Both statement findings are current.
6. **Step 6: Recompute (Run 2)**
   - Run 2 completes without refusal.
   - Schedule 1 top entry publishes `$1,340.00`, pinning `close.1`, raw subtotal (`$1,340.00`), and both Statement A and Statement B reason findings (`supported-loss`).
   - Attachment publishes itemization with 2 rows and tie-out of `$1,340.00`.

**Trace verdict:** PASS. No prior closure, aggregate finding, or publication persists across member additions.

---

## 4. Claim-Reuse Proof

### A. Non-Reused Claim: Family Closure Authority
- **Finding:** The family closure claim is **not reused** between family version `v1` and successor `v2`.
- **Reason:**
  - `v1` closure claim (`family.f1099k.json` v1): *"Every personal item sale amount reported in box 1a of a Form 1099-K furnished to the taxpayer for tax year 2025 is recorded as a statement item as of the keyed horizon. Closed with exactly one member authorizes that member; closed-empty authorizes 0."*
  - `v2` closure claim (`family.f1099k.json` v2): *"Every personal item sale amount reported in box 1a of a Form 1099-K furnished to the taxpayer for tax year 2025 is recorded as a statement item as of the keyed horizon. Closed with members authorizes the sum of current members; closed-empty authorizes subtotal 0."*
  - Under ADR-0079 and the Single-Source Rule, v1 bound cardinality to at most one statement and authorized a single member directly; v2 authorizes multi-member summation via the raw subtotal symbol. The claim represents a distinct real-world proposition and a distinct derivation authority. The v2 family carries its own version and checksum; v1 is not broadened in place.

### B. Reused Claim: Member Fact Predicate
- **Finding:** The member fact type `tax.us.2025.f1099k.box1a-gross-amount` **is reused** across family versions v1 and v2.
- **Proof of Three Invariants:**
  1. *Same real-world proposition:* The gross payment amount reported in Box 1a of Form 1099-K furnished to the taxpayer by a settlement organization for tax year 2025.
  2. *Same identity and lifecycle:* Sourced by documentary evidence from the payer statement, keyed by `(payer, statement, tax-year)`. Correctable via same-member statement updates; removable via member removal.
  3. *Same declared authority scope and explanation:* Declared as a documentary finding in the fact lattice. Survives the `v1 -> v2` family handover intact without rewriting or re-keying, as proven in `test_case9_upgrade_v1_one_statement_then_v2_statement` (retained statement finding remains current in currency projection and participates in v2 subtotal).

---

## 5. Neighboring-Capability Dependency Diff

This section details the prerequisites of neighboring capabilities before and after the connected sale design:

| Capability / Workspace | Prerequisites Before Design | Prerequisites After Design | Impact / Justification | Measured probe test |
| :--- | :--- | :--- | :--- | :--- |
| **Return with no Form 1099-K activity** | Schedule 1 asks whether a Form 1099-K was received; the answer closes the v1 family empty. | The same question closes the v2 family empty (`record_f1099k_no_statements_durably`). Top entry takes the default path (`count == 0 -> 0`). | No new prerequisite. A workspace whose answer is on v1 answers again under the successor package (no copied closure, ADR 0079). | `test_case4_closed_empty_v2` |
| **Single-statement workspaces on v46–v48** | Package adopted `tax.us.2025.f1099k` at v1. Single statement produced personal item sale deduction up to `$880.00`. | `FAMILY_VERSION` remains `"v1"`. Recorders default to `"v1"`. Workspaces adopted at v46–v48 continue writing v1 chains and closure mapping v1. Exact-version selection in `marshal.py` matches v1 mapping to v1 horizon. | Completely preserved. Zero drift for existing golden returns or single-statement fixtures. | Form 1099-K modules on core calculations v47/v48 in the plan's unit test lane. |
| **Form 1098 Mortgage Interest (Line 12e)** | Uses `tax.us.2025.f1098` family with its own single-statement count stop in `rule.f1098-mortgage-interest-deduction.v3.json`. | Unchanged. Form 1098 family, rules, and count stops remain untouched. | Finding F2: Form 1098 is completely decoupled from Form 1099-K. No changes made to Form 1098 rules. | Form 1098 circumstance modules in the plan's unit test lane. |
| **Form 1040 income and tax** | Do not read `tax.us.2025.schedule1.top-entry`. | Unchanged. | Only the Schedule 1 attachment rule reads the top-entry symbol (content search of `packages/content/tax/2025/rule.*.json`); income and tax are independent of it. | Content search; no probe needed. |

---

## 6. Integration-Surface Artifact

This artifact enumerates every consumer binding of the externally bound top-entry symbol (`tax.us.2025.schedule1.top-entry`) and the itemized attachment (`tax.us.2025.rule.attachment.schedule-1`).

| Consumer | Binding artifact or join | Cardinality it expects | Satisfied by design? | Measured probe test |
| :--- | :--- | :--- | :--- | :--- |
| **Presentation Model: Schedule 1 top-entry field** | Form field section for `tax.us.2025.schedule1.top-entry.form-field` in `packages/derivation/presentation_projection.py` | Exactly one published value or blocked disposition | Yes. Resolves to published integer value (`1340`) or blocked disposition with reason. | `test_case10_presentation_model_schedule1_field_and_explanations` |
| **Presentation Model: Per-Statement Explanations** | `f1099kStatementExplanation` dictionary in presentation projection | One entry per statement subject key | Yes. Contains independent entry for each statement (`stmt.alpha` and `stmt.beta`), each reporting its own Box 1a gross amount (`880.0`, `460.0`) and reason (`supported-loss`). | `test_case10_presentation_model_schedule1_field_and_explanations` |
| **Schedule 1 Attachment: Itemization** | Part `sch1-top-entry-f1099k` in the Schedule 1 attachment rule (`rule.attachment.schedule-1.v4.json` in core calculations v49) | Itemization part sum matching top-entry; row set containing all member statements | Yes. Itemization publishes with 2 rows and part sum `1340.0` tying out to line value `1340.0`. | `test_case1_two_supported_losses_sum_published` |
| **Statement Review UI: Review Preparation** | `prepare_f1099k_statement_review` in `packages/tax/f1099k_statement_review.py` | Snapshot of statement's own Box 1a and answers | Yes. Returns statement's own reported Box 1a (`880.0`, `460.0`) independent of top-entry or siblings. | `test_case10_presentation_model_schedule1_field_and_explanations` |
| **Unresolved Statement Detector** | `tax.us.2025.rule.f1099k-unresolved` | Exactly one disposition (`inapplicable` when all supported-loss; `blocked` otherwise) | Yes. Evaluates to `inapplicable` in Case 1; blocks in Case 2. | `test_case1_two_supported_losses_sum_published`, `test_case2_one_supported_loss_beside_published_non_loss` |

---

## 7. Withdrawn answers

Under the production reason successor every circumstance question has the
`not-asked` default, and the reason rule maps it to a published reason (for
example `cost-basis-unanswered`) rather than blocking. A withdrawn answer
therefore publishes that statement's reason, and the top entry blocks with
`DEPENDENCY_ABSENT` (`test_case3b_withdrawn_answer_under_production_reason_successor`),
as design case 4 expects. A statement whose reason itself blocks makes the top
entry block with `DEPENDENCY_INVALID` naming that statement
(`test_case3_blocked_subject`).

---

## 8. Summary of Measured Probe Results

Probe: `test_track0_closure_probe.py`
Command: `pytest docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances-evidence/test_track0_closure_probe.py`
Result: `12 passed in 69.78s` (100% passing across all 12 test cases).

Every disposition path and gate requirement chartered for Track 0 closure is fully measured and evidenced. Zero rows left unmeasured.
