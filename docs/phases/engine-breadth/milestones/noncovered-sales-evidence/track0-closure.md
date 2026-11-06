# Track 0 adversarial closure — sales whose basis was not reported

Scratch evidence for `PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate",
over Decisions 2–6 in
`docs/phases/engine-breadth/milestones/noncovered-sales.md`. No production,
test, or content edits. Synthetic `demo.*` findings only.

Source ref: `bb766465641abe3fb367a527701a5ca7393fb488` on
`milestone/noncovered-sales-2025`.

The scratch package is core v79 / release v77 (40 members, `source-family.v2`
on the new families, `inherited_inconsistencies` empty). Runs are
`live_coordinate_run`. The digest is `track0-output.json`, produced by
`track0.py`. P0's `probe.py` and `prototype.py` are the runners. Every
saturated case below has `presentation_valid` true and no duplicate form-field
id. `validate_presentation_model` is the presentation probe.

**Result: FAIL. Track 1 does not start.** One answer cannot close the eight
new families. A return that does not use the feature still needs eight new
closure findings before it computes. No content-only change fixes that.

## Authority-lifecycle table

**FAIL.** The table is the authority the scratch package actually uses. The
one question in Decision 3 is not among the facts that admit a family.

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| Filer-supplied basis, proceeds, and the sale object (`tax.us.2025.f1099b.noncovered-{st,lt}` and the proceeds, basis, and adjustment companions) | Box B or E amounts, plus the wash-sale disallowance on the object | One broker, statement, and transaction, tax year 2025, on that family's current horizon | The family's own member finding | A later ordinary assertion on the same fact id replaces the value and leaves the horizon in place. A second member-transition of the same fact id is rejected (`same-member correction belongs on the ordinary assertion path`). Removing the member, or failing to reclose after adding one, makes the prior subtotal unusable. |
| `basis_reported_to_irs` on a new-family object | `yes` is refused (`BASIS_WAS_REPORTED`). `no` is the member the family accepts | The sale object only. Scalar proceeds, basis, and adjustment are numbers and carry no flag | Object member-validation | Superseding the object. A scalar that disagreed with the object was not given its own constraint; the subtotal reaches the object so a refused object blocks the amount. |
| Eight closure facts, one per new family (`…source-closure`) | "The set of members on this horizon is complete." Value must be boolean true | That family's current horizon. Identity is `family-horizon` plus tax year 2025 | The mapping's closure fact type and the adopted family version | A false value, a missing finding, a finding on a superseded horizon, or two current findings for the same horizon. Any of those leaves the family unclosed and blocks, and does not publish zero. |
| Decision 3's one question, probed as `tax.us.2025.f1099b.noncovered-sold.source-closure` | "Did you sell any securities whose basis was not reported to the IRS?" A `no` was supposed to close all eight families empty | One finding, one horizon | Eight mappings sharing that fact type | It does not admit. See the runs below. This fact is not in the package that the other rows ran. |
| `basis_reported_to_irs` on a covered family (v78 families, still adopted at v1 / covered-w at v2) | The flag on a covered sale | That covered object's horizon | The covered family as adopted. No `BASIS_WAS_REPORTED` constraint on covered-st or covered-lt v1 | An ordinary assertion can change the flag. The lines do not read it. Replacing covered-st with a v2 of the same meaning, without a handover, makes the existing v1 closure miss the adopted version. |
| `tax.us.2025.schedule-d-boundary.no-form8949-sources` and `tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments` | The ADR-0061 pair. Both `no` means the return is outside the Form 8949 class | Tax year 2025. Free supersession. One current answer each | Unchanged fact types | A later assertion. The scratch gates read them; they do not redefine them. |
| `tax.us.2025.schedule-d-boundary.noncovered-in-class` | Whether the work beyond covered sales and code W is only boxes B and E | Tax year 2025. Free supersession | The new fact in `schedule-d-boundary-noncovered.bundle.json` | A later assertion. `no` blocks a recorded noncovered amount. It does not close the families. |
| Code W on the new object (`wash_disallowed`) | Column (g) on boxes B and E, same mechanics as boxes A and D | The sale object | `CODE_W_ON_GAIN` and `ADJUSTMENT_EXCEEDS_LOSS` | A disallowance on a gain, or a disallowance larger than the sale's own loss, fails member-validation. The subtotal and Form 8949 then block. |

Admission (`packages/derivation/source_authority.py`, `resolve_closure_admissions`) keeps a family only when exactly one marshalled record has that mapping's closure fact type, the family's current horizon, and boolean true. Marshalling (`packages/derivation/marshal.py`, `marshal_closure_authority`) appends every current finding of a mapping's fact type once per mapping. Eight mappings of one fact type therefore append each finding eight times, and the exactly-one test fails.

Measured on the shared-fact package (`modes.one_question`):

- `one_finding`. One true finding, keyed to the short-term object's horizon. Six scalar subtotals are `SOURCE_SET_UNCLOSED`. Lines 2, 9, 7, 15, 16, 21, and 7a block. Form 1040 blocks.
- `eight_findings`. Eight true findings, one per family horizon, same fact type. The same six scalar subtotals are `SOURCE_SET_UNCLOSED`. Form 1040 blocks.
- `duplicate_horizon`. All eight families genesis with `demo.ns.oq.shared.h0`. `HorizonModelError: horizon id already recorded`.

A `no` would also fail admission: a false value is a non-admission. Closing empty is a true finding on a family that has no members, which is eight true findings of eight fact types (`wage_closed_empty`), not one `no`.

## Empty/nonempty authority matrix

**FAIL.** Closed-empty with eight true closures computes. A boundary `no` blocks a recorded noncovered sale. Two counterexamples to this row's bar still stand: one question does not close the empty families, and a covered sale with `basis_reported_to_irs` no still publishes line 8a. Scalar identity exclusivity is not installed; a number member that carries it is `MEMBER_VALUE_MALFORMED`, which is an engine change, so that half of Decision 6 stays out.

| Family state | Universe / absence authority | Eligibility | Feature result | Neighbor result |
| --- | --- | --- | --- | --- |
| Eight new families closed empty (`wage_closed_empty`) | Eight true closure findings, one per family | No sale | Lines 2 and 9 `closure_backed_zero` 0. Line 7a `computed_zero` 0. Taxable 34250, tax 3875. Both attachments `guard_inapplicable` | Same dollars as v78 `wage` |
| Eight new families closed empty, boundary `no` (`wage_boundary_no`) | Same closures, `noncovered-in-class` no | No sale | Same dollars and dispositions as `wage_closed_empty` | Wage return still computes |
| Families not closed (`wage_unclosed`) | The eight closure findings absent | No sale | Both objects and all six scalar families `SOURCE_SET_UNCLOSED`. Lines 2, 9, 7, 15, 16, 21, and 7a block. Form 1040 blocks. Form 8949 blocks | The wage return does not compute. This is the new prerequisite |
| One shared question, or eight findings of that one fact type | Decision 3 | No sale | Scalar subtotals stay `SOURCE_SET_UNCLOSED`. Form 1040 blocks | Does not restore the wage return |
| Nonempty, boundary `yes` (`lt_gain`, `st_loss`, `wash`, `mixed`, `net_zero`) | Per-family closures true, boundary yes | In class | Line 9 gain 4000 (taxable 38250, tax 3875). Line 2 loss −6000, line 21 3000, line 7a −3000, taxable 31250, tax 3515. Wash line 9 −2000, line 7a −2000, taxable 32250, tax 3635. Net-zero line 9 `computed_zero`, Form 8949 published. Mixed line 1a 1000 and line 9 4000, line 7a 5000, taxable 39250, tax 3995 | Schedule D and line 7a follow the amounts |
| Nonempty, boundary `no` (`boundary_no_gain`) | Closures true, boundary no | Refused by the answer | Line 9, lines 15, 16, and 7a, and Form 8949 block `DEPENDENCY_ABSENT`. Line 8a stays `closure_backed_zero`. The gain is not published | Form 1040 blocks along line 9 |
| Basis omitted (`basis_omitted`) | Object missing `basis` | Not a member | `FindingModelError`: `basis` is required | No partial amount |
| Basis family not reclosed (`basis_unclosed`) | Proceeds closed, basis not | Incomplete | Line 9 and Form 8949 block. Basis subtotal `SOURCE_SET_UNCLOSED` | Line 7a blocks |
| Code W on a gain (`code_w_on_gain`, proceeds 6000, basis 2000, adjustment 500) | Object constraints | Refused by member-validation | `DEPENDENCY_INVALID` missing `CODE_W_ON_GAIN` and `ADJUSTMENT_EXCEEDS_LOSS`. Line 9 and Form 8949 block | No partial Form 8949. Fixed by reaching the object from the subtotal; before that change Form 8949 published box E while line 9 blocked |
| Covered sale, both Form 8949 boundaries `no` (`covered_both_boundaries_no`) | ADR-0061 pair both no | Outside the class | Line 8a blocks. Lines 15, 16, and 7a block. Form 8949 `guard_inapplicable`. The gain is not on those lines. The Schedule D attachment disposition is `published` with value null | Form 1040 blocks along line 8a. Fixed for the named lines 8a, 15, 16, and 7a |
| Covered sale, `basis_reported_to_irs` no, Path A still yes (`covered_flag_no_path_a`, and `covered_flag_corrected_to_no`) | Covered-lt v1 has no flag constraint. The correction is an ordinary assertion of the same fact id | The flag says not reported | Line 8a 4000, lines 15, 16, and 7a 4000, taxable 38250, tax 3875. Form 8949 `guard_inapplicable`. The correction does not move line 8a | Stands. Not fixed |
| Covered-st replaced by v2, no handover (`modes.version_bump`, `wage`) | Adopted family version selects the horizon chain | Existing v1 closure | `rule.closure-check.f1099b-covered-st` is `SOURCE_SET_UNCLOSED`. Line 1a blocks, missing `covered-st.closure-check`. Line 8a stays `closure_backed_zero` | A handover on existing returns would be a recording change. Not installed |

Boxes C and F, adjustment codes other than W, digital assets, and short sales have no families. An empty return with the boundary `no` computes (`wage_boundary_no`). A recorded sale with the boundary `no` blocks (`boundary_no_gain`). That refusal is the answer.

## Late-member lifecycle

**FAIL.** The per-family trace holds. The trace Decision 3 names, close-by-the-one-question-`no`, does not: that question never becomes current authority. The covered-flag correction does not move the published gain.

Paper trace for one long-term noncovered sale, proceeds 6000, basis 2000. The one-question `no` is not a step that runs; the close that does run is the family's own true closure.

| Step | What is current | What becomes unusable | Measured |
| --- | --- | --- | --- |
| Attest the wage return, families not yet closed | Wage findings. No noncovered members | Nothing of the new class is publishable | `wage_unclosed`: lines 2 and 9 block, Form 1040 blocks |
| Close each new family with its own true closure and no members | Eight closure findings | An unclosed read of those families | `wage_closed_empty`: lines 2 and 9 are `closure_backed_zero` 0. Taxable 34250, tax 3875 |
| Compute | Those zeros | A later member makes the zero a stale summary | Same run |
| Add the sale and do not reclose (`late_member_unclosed`) | The new member sits on an unclosed horizon. The old closure was stripped | The prior zero. Line 9 blocks. Form 8949 blocks. Object member-validation is `SOURCE_SET_UNCLOSED` | Saturated. Before the subtotal `require_closed` change, Form 8949 published box E 6000/2000 while line 9 blocked. That partial is fixed |
| Reclose the object, proceeds, and basis (`late_member_reclosed`) | New true closures on the horizons that hold the member | The blocked state | Line 9 4000, lines 15, 16, and 7a 4000, taxable 38250, tax 3875. Form 8949 published |
| Correct `basis_reported_to_irs` on a covered long-term sale from yes to no (`covered_flag_yes`, then `covered_flag_corrected_to_no`) | Ordinary assertion. The horizon and the covered closure stay | The previous object value. The published line does not | Both runs: line 8a 4000. A second member-transition of the same fact id is rejected, so the correction uses the assertion path the kernel names |

The reclose is what makes the new amount publishable. A closure that is left on the pre-member horizon does not stay current, and the old zero is not reused.

## Claim reuse

**PASS.** Two facts are reused. The preferential gate and the covered closure facts are successors or distinct facts, and this row does not call them reused.

Reused: `no-form8949-sources` and `no-other-form8949-adjustments`.

- Same proposition. Both stay the ADR-0061 yes/no boundaries. The scratch gates add `noncovered-in-class` as a further disjunct. They do not rewrite the two questions.
- Same identity and lifecycle. Tax-year literal, free supersession, one current answer. The runs answer them with the same assertion shape as v78.
- Same authority scope. A `yes` still means that boundary holds for the return's tax year. `covered_both_boundaries_no` shows both `no` blocks lines 8a, 15, 16, and 7a. `wage_closed_empty` shows the closed-empty lines still publish zero when the new boundary is not read (the zero arm runs first).

Not reused, and not claimed as reused:

- Covered closure fact types. Each new family has its own `source-closure` id (`prototype-rules/noncovered-{st,lt}*.json`). The shared-fact experiment shows one fact type does not admit eight families.
- The preferential-base gate. `rule.selected-preferential-base.v7.json` is a new version. Its categorical `any` is the two ADR-0061 facts plus `noncovered-in-class`. The gate claim is that successor, not the v6 claim.

No counterexample to those three points on the two reused facts was found.

## Neighboring-capability dependency diff

**FAIL.** Yes. A return that does not use this feature now needs a new answer.

The four v78 returns that were measured are `base_return` (wage), foreign tax 601, exempt interest 50, and student loan 200. No other return in the v78 live set was measured.

On v78, each computes with no noncovered closure. On v79, the same return computes the same dollars only after eight new closure findings, one per new family (`v79_wage` / `wage_closed_empty`, `v79_foreign_tax`, `v79_exempt_interest`, `v79_student_loan`):

| Return | v78 taxable / tax | v79, eight families closed empty | v79, those closures absent |
| --- | --- | --- | --- |
| Wage | 34250 / 3875 | 34250 / 3875 | Form 1040 blocked |
| Foreign tax 601 | 34350 / 3887 | 34350 / 3887 | Not re-run unclosed. The wage return is the no-activity case, and it blocks |
| Exempt interest 50 | 34250 / 3875 | 34250 / 3875 | Same |
| Student loan 200 | 34050 / 3851 | 34050 / 3851 | Same |

`wage_unclosed` is that no-activity return without the eight findings. Lines 2, 9, 7, 15, 16, 21, and 7a block. Form 1040 line 15 and line 16 block. The new requires are real: line 7 v4 and the preferential base v7 and line 7a v6 read lines 2 and 9; those lines `require_closed` on the new families.

Decision 3 said one question would be that prerequisite, and a `no` would close all eight empty. The measured substitute is eight closure findings. That is the requirement the decision forbade.

No design change inside content, short of an engine or schema change, makes one answer close eight families. Marshalling appends a shared fact type once per mapping, so the exactly-one admission never holds. A `no` is not boolean true, so it does not admit. One horizon id cannot be recorded on eight families. Eight fact types are eight answers. Dropping the families off line 7, line 15, and line 7a would leave the no-sales return alone and would also leave the feature uncomputed.

## Integration surface

**PASS.** Each watched symbol has one publisher in the v79 member set (`modes.standard.surface`). Each new form field was probed with `validate_presentation_model`.

| Consumer | Binding | Cardinality | Satisfied |
| --- | --- | --- | --- |
| Schedule D line 2 form field v1 | `rule.schedule-d-line2` v1 publishes `schedule-d.line-2` | Exactly one publisher | Yes. `st_loss` published −6000. `wage_closed_empty` `closure_backed_zero` 0. `wage_unclosed` blocked |
| Schedule D line 9 form field v1 | `rule.schedule-d-line9` v1 publishes `schedule-d.line-9` | Exactly one | Yes. `lt_gain` published 4000. `wash` published −2000. `net_zero` `computed_zero` 0. `wage_closed_empty` `closure_backed_zero` 0. `boundary_no_gain` blocked |
| Schedule D line 7 form field v3 | `rule.schedule-d-line7` v4 | Exactly one | Yes. Reads line 1a and line 2. `st_loss` −6000. `mixed` 1000. Empty `computed_zero` |
| Schedule D line 15 form field v3 | `rule.schedule-d-line15` v6 | Exactly one | Yes. Reads line 8a and line 9. `lt_gain` 4000. `wash` −2000 |
| Schedule D line 16 form field v2 | `rule.schedule-d-line16` v2 | Exactly one | Yes. `st_loss` −6000. `mixed` 5000. `lt_gain` 4000 |
| Schedule D line 21 form field v2 | `rule.schedule-d-line21` v1 | Exactly one | Yes. `st_loss` 3000. `wash` 2000. Empty `computed_zero` |
| Form 1040 line 7a field v1 | Binds `capital-gains.line7a-total`, published only by `rule.form1040-line7a` v6 | Exactly one | Yes. Loss −3000. Wash −2000. Gain 4000 and mixed 5000. Empty `computed_zero` 0. Unclosed and boundary-no blocked |
| Preferential base | `rule.selected-preferential-base` v7, the only publisher. Required by line 7a v6, line 16 v6, and the QDCG worksheet lines | Exactly one | Yes. The tax dollars above are that consumer. The v7 `any` is the two ADR-0061 facts plus `noncovered-in-class`, and the activity checks include lines 2 and 9 |
| Form 8949 attachment v3 | Publishes `form8949.disposition`. Citation v1 binds the same symbol | Exactly one attachment rule | Yes. Published on `lt_gain`, `st_loss`, `wash`, `net_zero`, `mixed`, `late_member_reclosed`. `guard_inapplicable` on closed empty. Blocked on `boundary_no_gain`, `code_w_on_gain`, `late_member_unclosed`, `wage_unclosed` |
| Lines 1a and 8a | Gain symbols published by line 1a v4 and line 8a v5. Form fields bind those gain symbols | Exactly one each | Yes. `mixed` line 1a 1000. `covered_flag_yes` line 8a 4000. `covered_both_boundaries_no` line 8a blocked. Empty `closure_backed_zero` |

Line 7a v6 requires lines 16, 21, the preferential base, line 2, and line 9. Nothing else in the member scan publishes line 2, line 9, or `line7a-total`.

## Design changes

Installed in the scratch package, because a measured counterexample failed without them:

- Sale-object constraints and identity exclusivity live on the object (`source-family.v2`). Scalar families stay numbers. Putting exclusivity on a number member was `MEMBER_VALUE_MALFORMED`.
- Each scalar subtotal's `when` is `require_closed` on that family. On v2 it also `require_closed` the sale object and `accounts_for` that object's members. This is what stopped Form 8949 from publishing `code_w_on_gain` and `late_member_unclosed` while line 9 blocked.
- Lines 2 and 9, the six subtotals, line 1a v4, and line 8a v5 publish zero when the summed amounts are zero, and otherwise publish only when the boundary arm is yes. Both ADR-0061 answers `no` therefore block line 8a instead of publishing it.
- Line 7 v4, line 15 v6, line 7a v6, and preferential base v7 read lines 2 and 9, so a noncovered loss reaches line 7a. Measured: −3000 and tax 3515; wash −2000 and tax 3635.
- Form 8949 v3 adds box B and box E and the two proceeds subtotals. `accounts_for` on the attachment is the predecessor's list.

Not installed, because each one needs an engine, schema, or recording change:

- One closure fact type for eight families.
- A handover from covered-st v1 to a v2 that could carry the flag constraint. Without the handover, the wage return's v1 closure does not admit and line 1a blocks.
- Identity exclusivity on the scalar number families.

## Counterexamples

| Case | Disposition | How |
| --- | --- | --- |
| `code_w_on_gain` published Form 8949 while line 9 blocked | Fixed | The subtotal now requires the sale object's closure, so member-validation's `CODE_W_ON_GAIN` and `ADJUSTMENT_EXCEEDS_LOSS` block Form 8949 |
| `late_member_unclosed` published Form 8949 from an unclosed member | Fixed | `require_closed` on the subtotal. Reclose (`late_member_reclosed`) publishes line 9 = 4000 |
| Covered sale with both Form 8949 boundaries `no` published lines 8a, 15, and 16 | Fixed for those lines | Line 8a v5 blocks. Lines 15, 16, and 7a block. The Schedule D attachment disposition stays `published` with a null value |
| `basis_omitted` | Refused by the object schema | `basis` is required. No amount is computed |
| Boxes C and F, other adjustment codes, digital assets, short sales | Refused by the answer | No families. Boundary `no` with no member computes the wage return. Boundary `no` with a member blocks line 9 and Form 8949 |
| `one_finding`, `eight_findings`, `duplicate_horizon` | Stands | One fact type does not admit eight families. A shared horizon id is rejected. This is why the authority, matrix, late-member, and neighbor rows fail |
| `covered_flag_no_path_a` and `covered_flag_corrected_to_no` | Stands | Line 8a stays 4000 after the flag is no, including after an ordinary assertion that corrects yes to no |
| `version_bump` wage | Stands | Adopting covered-st v2 without a handover leaves `covered-st` `SOURCE_SET_UNCLOSED` and blocks line 1a. The handover is a recording change |
| Scalar identity exclusivity | Stands | Not installed. The engine rejects a number member that carries it |
| `wage_unclosed` | Stands | The no-sales return needs eight new closure findings. One question does not supply them |

## Rerun over the P0b contract

The first run above stays the history of Decisions 2–6. This section is the
rerun after Decisions 7–9. Scratch core v79 / release v77, 41 members.
`live_coordinate_run`. Digest `track0b-output.json`, produced by `p0b.py`
at source ref `0a7fc60f5ab42ed8d568362f1a5c9a750d7394c0`. The extra member is
`attachment.schedule-d.v7`, which replaces v6 in the scratch package only.
Every saturated case has `presentation_valid` true. No production, test,
schema, or content edit. No kernel edit.

The shared fact is `tax.us.2025.f1099b.noncovered-sold.source-closure`.
The question is "Did you sell any securities whose basis was not reported
to the IRS?" The covered-flag token is `BASIS_NOT_REPORTED_ON_COVERED`.
The page sentence is "Record this sale as a noncovered sale. The broker
did not report its basis to the IRS."

**Result: PASS.** One current answer closes the eight families. A later
member strips that family's admission until the filer answers again. A
covered member with `basis_reported_to_irs` no stops publishing the line
that reads it. The nine v78 live returns keep their Form 1040 dollars
under one `no`.

### Authority-lifecycle table

**PASS.** One current answer is the authority. A shared horizon id is
still refused.

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `tax.us.2025.f1099b.noncovered-sold.source-closure` | Did you sell any securities whose basis was not reported? `yes` or `no` | Tax-year identity. One current answer for the eight noncovered families | The eight v3 mappings in the scratch point at this fact. Marshalling records it once | A later `member-transition` on one family strips that family until a later answer. A current `no` beside any current member of that family admits nothing |
| Eight noncovered family closures | Supplied by that one answer in this scratch. Each family still has its own horizon | Per family, for as long as the current answer admits it | The shared answer and the act order of member transitions | The same two events. `one_finding` admits all eight empty. `late_yes_stale` leaves the long-term families unclosed |
| Covered-family closure | The broker reported basis | The covered family that owns the member | `basis_reported_to_irs` on the current member | `no` records `missing: [BASIS_NOT_REPORTED_ON_COVERED]` and the row code `DEPENDENCY_INVALID` |
| `no-form8949-sources`, `no-other-form8949-adjustments` | The two ADR-0061 boundaries | Tax year, as in the first run | Unchanged | An ordinary correction of that answer |

`duplicate_horizon` still raises `HorizonModelError`: `horizon id already
recorded: demo.ns.p0b.shared.h0`. The scratch does not add a horizon. It
records the answer once.

`one_finding` (wage plus one `no`): lines 2 and 9 are `closure_backed_zero`
0, Form 1040 line 15 is 34250, line 16 is 3875. `wage_unclosed` blocks
lines 2, 9, 15, and 16, and each sampled blocked line shows the shared
question once.

### Empty/nonempty authority matrix

**PASS.** Empty with one `no` computes the neighbor. Empty with no answer
blocks. A member after the answer blocks only that member's families until
the filer answers again. A covered flag `no` blocks the line that reads
that family.

| Family state | Universe / absence authority | Eligibility | Feature result | Neighbor result |
| --- | --- | --- | --- | --- |
| Closed empty | One shared `no`, no member | Inapplicable | Lines 1a, 2, 8a, and 9 are `closure_backed_zero` 0 | The nine harness returns keep their v78 line 15 and line 16. See the neighbor table |
| Closed empty | Shared answer absent (`wage_unclosed`) | Any | Lines 2 and 9 blocked. The page shows the shared question | Form 1040 lines 15 and 16 blocked |
| Nonempty, answer current and after the member | Shared `yes` (`lt_gain`, `late_member_reopened`, `late_yes_reanswered`) | Eligible | Line 9 published 4000. Line 7a published 4000. Line 15 is 38250. Line 16 is 3875 | Those dollars include the gain |
| Nonempty, answer stale or `no` | `late_member_unclosed`, `late_yes_stale`, `yes_then_no_with_member`, `boundary_no_with_member` | The long-term families are unclosed | Line 9 blocked. Line 2 stays `closure_backed_zero` 0. The page shows the shared question | Form 1040 lines 15 and 16 blocked. Form 8949 blocked |
| Nonempty, ineligible | Covered member, `basis_reported_to_irs` no | Refused | Line 8a or line 1a blocked. Wash blocks line 8b or line 1b and Form 8949. The page shows the noncovered-sale sentence | Lines 15 and 16 blocked. v78 `covered_flag_no_path_a` still publishes line 8a at 4000 |
| Nonempty, constraint refusal | `code_w_on_gain` | Adjustment code W on a gain | Line 9 blocked. Member-validation `missing` is `CODE_W_ON_GAIN` and `ADJUSTMENT_EXCEEDS_LOSS`. Form 8949 blocked. Sampled page reasons are empty | Lines 15 and 16 blocked |

`boundary_no_without_member`: line 15 is 34250, line 16 is 3875, lines 1a,
2, 8a, and 9 are `closure_backed_zero` 0, and both attachments are
`guard_inapplicable`.

Loss and wash, with the shared `yes` after the member: `st_loss` line 2
is −6000, line 21 is 3000, line 7a is −3000, line 15 is 31250, line 16 is
3515. `wash` line 9 is −2000, line 21 is 2000, line 7a is −2000, line 15
is 32250, line 16 is 3635.

### Late-member lifecycle

**PASS.** Attest and close are the shared answer. Adding a member after
that answer makes the touched families unusable. Answering again publishes.

| Step | Case | What stays usable | What is unusable |
| --- | --- | --- | --- |
| Attest `no`, no member, compute | `boundary_no_without_member`, `one_finding` | The `no` admits every empty family. Lines 2 and 9 are zero. The wage return publishes | Nothing on this return is a noncovered member |
| Attest `no`, then add a long-term sale | `late_member_unclosed` | Line 2 stays 0. Short-term families stay closed | The five long-term families are the only `noncovered_blocked` entries. Line 9, Form 8949, and Form 1040 lines 15 and 16 block. The page shows the question |
| Attest `yes`, compute empty, add the sale | `late_yes_stale` | Line 2 stays 0 | Same long-term block as `late_member_unclosed`. The earlier `yes` does not admit the families that received the member |
| Add the sale, then answer `yes` | `late_member_reopened`, `late_yes_reanswered` | Line 9 is 4000, line 7a is 4000, line 15 is 38250, line 16 is 3875. Form 8949 is `published` | The stale answer is superseded by the later assertion |
| `yes`, then a member, then `no` | `yes_then_no_with_member` | Line 2 stays 0 | Line 9 blocks. A current `no` beside a member admits nothing for that family |

Covered flag corrections use the same current-member rule. `covered_flag_yes`
publishes line 8a at 4000. `covered_flag_corrected_to_no` blocks line 8a
with `missing: [BASIS_NOT_REPORTED_ON_COVERED]`. `covered_flag_corrected_to_yes`
publishes line 8a at 4000 again.

### Claim reuse

**PASS.** The two reused facts are the same two the first run measured.
This rerun does not give them a new proposition, identity, or scope.

- `no-form8949-sources` and `no-other-form8949-adjustments` stay the
  ADR-0061 boundaries: tax-year identity, free supersession, one current
  answer. `boundary_no_without_member` and `boundary_no_with_member` answer
  them with that shape. Both `no` and no member publishes the wage return.
  Both `no` and a noncovered member blocks line 9.
- The preferential-base gate stays the v7 successor from the first run.
  This row does not call v6 reused.
- Covered closure fact types are not the shared fact. The shared fact is
  new. `one_finding` shows one answer, and the eight family closures are
  admissions of that answer.
- Scalar identity exclusivity is not an engine change on the number
  families. Decision 7 dropped it. The sale object keeps its constraints
  (`code_w_on_gain`). The ADR-0082 companion pairs are the production map
  from each scalar fact type to its sale object. This scratch did not
  install those pairs, and no PASS row treats an unmeasured pair as a
  measured fix.

### Neighboring-capability dependency diff

**PASS.** A return with no noncovered sale needs one shared `no`. It does
not need eight closure findings. The new prerequisite is that one answer.
`wage_unclosed` is the same return without it, and Form 1040 blocks.

`tests/helpers/current_core_returns.py` builds these nine. Each v79 row is
one shared `no`. Line 15 and line 16 match v78.

| Return | v78 line 15 / line 16 | v79, one `no` |
| --- | --- | --- |
| Wage | 34250 / 3875 | 34250 / 3875 |
| Foreign tax | 34350 / 3887 | 34350 / 3887 |
| Exempt interest | 34250 / 3875 | 34250 / 3875 |
| Exempt dividend | 34250 / 3875 | 34250 / 3875 |
| Student loan | 34050 / 3851 | 34050 / 3851 |
| Gambling loss | 34250 / 3875 | 34250 / 3875 |
| Mortgage | 34250 / 3875 | 34250 / 3875 |
| Itemized | 34250 / 3875 | 34250 / 3875 |
| Part II-B | 0 / 0, `computed_zero` | 0 / 0, `computed_zero` |

On v79 the one-`no` rows also publish lines 2 and 9 at `closure_backed_zero`
0. v78 leaves those two lines absent (`money.line2` and `money.line9` are
null) because the successor families are not on v78. The patch does not
change v78: `v78/covered_flag_no_path_a` still publishes line 8a at 4000,
line 7a at 4000, line 15 at 38250, and line 16 at 3875.

### Integration surface

**PASS.** The publishers are the ones named in the first run, plus
`attachment.schedule-d.v7` in place of v6. Disposition paths built on this
rerun: published gain, published loss, `computed_zero`, `closure_backed_zero`,
blocked on a missing answer, blocked on a stale answer, blocked on a covered
flag `no`, and blocked on code W. `validate_presentation_model` passed on
every saturated case.

| Consumer | Binding | Cardinality | Satisfied |
| --- | --- | --- | --- |
| Schedule D lines 2 and 9 | `rule.schedule-d-line2` and `rule.schedule-d-line9` | Exactly one publisher each | Yes. `st_loss` line 2 is −6000. `lt_gain` and `wash` publish line 9 at 4000 and −2000. Empty is `closure_backed_zero`. Stale and `no`-with-member block line 9 only |
| Form 1040 line 7a | `rule.form1040-line7a` v6 | Exactly one | Yes. `st_loss` −3000 and tax 3515. `wash` −2000 and tax 3635. `lt_gain` 4000. Empty `computed_zero`. Unclosed, stale, and covered-flag `no` block it |
| Form 1040 lines 15 and 16 | The v78 publishers, reading the Schedule D lines | Exactly one each | Yes. The neighbor table is the no-activity path. The loss, wash, and gain rows are the activity path. Blocked when line 9 or line 8a is blocked |
| Form 8949 attachment | `rule.attachment.f8949` | Exactly one | Yes. `published` on `lt_gain`, `st_loss`, `wash`, `late_member_reopened`, and `late_yes_reanswered`. `guard_inapplicable` on `boundary_no_without_member`. `blocked` on `late_member_unclosed`, `late_yes_stale`, `yes_then_no_with_member`, `boundary_no_with_member`, `code_w_on_gain`, and both wash flag-`no` rows |
| Schedule D attachment | Scratch `attachment.schedule-d.v7`. Its `requirement.subtotals` adds `schedule-d.line-1a-gain` and `schedule-d.line-8a-gain` | Exactly one | Yes. `covered_both_boundaries_no` is `blocked` because `schedule-d.line-8a-gain` is missing. The first run left this attachment `published` with a null value. `covered_flag_yes` and `covered_flag_corrected_to_yes` are `published` with a null value while line 8a is 4000. That null is the non-scalar slot. v78 publishes the same null when line 8a is 4000 |
| Covered flag page | Closure check or wash member-validation | The blocked line carries one explanation | Yes, on the four covered objects this package contains. `covered_flag_no_path_a` and `covered_flag_corrected_to_no`: closure-check `f1099b-covered-lt`, line 8a blocked. `covered_flag_no_st`: closure-check `f1099b-covered-st`, line 1a blocked. `covered_flag_no_w_lt` and `covered_flag_no_w_st`: member-validation artifact id ends in `synthesized`, Form 8949 and the Schedule D attachment blocked, line 8a stays `closure_backed_zero` 0. Each sampled blocked line shows the noncovered-sale sentence. The row `code` is `DEPENDENCY_INVALID`. The dedicated token is the `missing` entry |

`covered-ltcg` has no horizon on the harness return. It is not a member of
core v78 or this successor. Line 8a v4 and v5 read `f1099b.covered-lt`.
The scratch did not add the gain-only family back.

The published derivation-record enum has no `BASIS_NOT_REPORTED_ON_COVERED`
value. This scratch keeps the row `code` at `DEPENDENCY_INVALID` and stores
the token in `missing`. The page sentence is the filer-facing explanation.
No new record schema is published here.

### Design changes in this rerun

Installed in the scratch stand-in only:

- Decision 8. The last assertion of the shared fact is the current answer.
  A later `member-transition` whose family is one of the eight marks that
  family stale. A later answer moves the index past the transition.
  `no` with a current member admits nothing. This reads derivation act
  order inside the scratch's `live_coordinate_run` wrapper.
- Decision 9. A current covered member with `basis_reported_to_irs` no
  drops that family's admission. The blocked row's `missing` entry is
  `BASIS_NOT_REPORTED_ON_COVERED`, the row `code` is `DEPENDENCY_INVALID`,
  and the presentation probe adds the noncovered-sale sentence when that
  token is reachable.
- Schedule D attachment v7 adds the two gain symbols to
  `requirement.subtotals`, so a blocked line 8a blocks the attachment.

### Counterexamples

| Case | Disposition | How |
| --- | --- | --- |
| `one_finding` and `wage_unclosed` | Fixed | One `no` closes the empty families and matches the wage dollars. With no answer, lines 2, 9, 15, and 16 block and the page shows the question |
| Late sale after `no` | Fixed | `late_member_unclosed` blocks line 9 and the five long-term families. Line 2 stays 0 |
| Late sale after `yes`, then re-answered | Fixed | `late_yes_stale` blocks line 9. `late_yes_reanswered` publishes line 9 at 4000 and line 7a at 4000 |
| `yes` then `no` with a member | Fixed | `yes_then_no_with_member` blocks line 9 and shows the question |
| Covered flag `no` on short-term, long-term, and both wash objects | Fixed | Each blocks with `missing: [BASIS_NOT_REPORTED_ON_COVERED]` and shows the noncovered-sale sentence. v78 still publishes line 8a at 4000 |
| Flag corrected `yes` to `no`, and `no` to `yes` | Fixed | `covered_flag_corrected_to_no` blocks line 8a. `covered_flag_corrected_to_yes` publishes line 8a at 4000 |
| `covered-ltcg` | Refused by the answer | The family is not a member of core v78 or this successor, so the return has no horizon and no publisher for it. Line 8a reads `covered-lt`, measured above. The scratch does not revive the family |
| `st_loss` and `wash` line 7a | Fixed | −3000 with tax 3515. Wash −2000 with tax 3635 |
| `boundary_no_without_member` and `boundary_no_with_member` | Fixed | Without a member, 34250 / 3875 and both attachments `guard_inapplicable`. With a member, line 9 and Form 8949 block and the page shows the question |
| Schedule D attachment on `covered_both_boundaries_no` | Fixed | Disposition `blocked`, missing `schedule-d.line-8a-gain`. A published null remains only when line 8a itself publishes (`covered_flag_yes`) |
| `duplicate_horizon` | Refused by the answer | `HorizonModelError` on `demo.ns.p0b.shared.h0`. Shared horizon ids stay illegal. The scratch records one answer and does not share a horizon |
| Scalar identity exclusivity | Refused by the answer | Decision 7 dropped exclusivity on the number families. Object constraints still refuse code W on a gain. Companion pairs were not installed in this scratch |
| `code_w_on_gain` | Fixed | Form 8949 blocked. Member-validation names `CODE_W_ON_GAIN` and `ADJUSTMENT_EXCEEDS_LOSS`. The shared question is not the reason on the page |

