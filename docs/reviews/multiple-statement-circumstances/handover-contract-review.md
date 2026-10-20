# Review — family-handover contract proposal

Audience: Foreman.

- Reviewer, same lineage. HEAD `cf66fce71c1213d4c5cdb122cf80f547a452f62f` on `milestone/multiple-statement-circumstances-consolidation`. Orientation role: reviewer. No probes.
- Object: `family-handover-contract-proposal.md` plus the increment feedback and Increment 4 Foreman check. Candidate `34ca5860` and sale Track 0 stay unaccepted. This is not an owner choice.

## Verdict

**REPAIR REQUIRED.** The supported shape is right: one current predecessor, successor chain absent, retirement remembered by chain key, fresh closure afterwards, both-current logs contained without a hidden retirement. The owner should not decide on this text until the wrong requirements below are corrected in one paper pass.

## Wrong requirements

1. **The cascade citation is the wrong root.** `packages/kernel/currency.py:170` is `_migration_supersessions`, a migration root. Handover displacement is `superseded_entity_ids` added at `currency.py:225`, along individuation edges built at `currency.py:156-168`, then derived findings at `projection.py:66-75`. `facts.py:228` is the entity set. `facts.py:240` is `fact_id_for`, not why a statement survives. A box 1a fact stays because its keys are payer, statement, and tax-year (`f1099k.bundle.v3.json:13-30`). The closure fact is the one keyed on `kernel.family-horizon` (`f1099k.bundle.v3.json:81-90`).

2. **Handover does not authorize an empty subtotal.** Section 7 says a wash-sale handover authorizes empty subtotals. The fold drops the old closure and does not write a new one. Section 1.5 and case 4 already require a fresh true closure and a rerun. That sentence has to match them.

3. **The clause table is not the set the proposal uses.** Decisions 1 and 3 are quoted accurately, and Decision 3 stays unchanged. Decision 5 should be **unchanged**: superseding the horizon entity already feeds `currency.py:225`. Calling it a supplement invites an ADR edit the fold does not need. Decisions 6 and 7 are relied on (roots accumulate; a displaced closure stays displaced; a new true closure and an explicit rerun) and are absent. ADR-0077 Part 5's new-write boundary is `ActLog.append` (`docs/adr/0077-shared-key-count-basis-same-run-read-and-presence-selection.md:345-350`); replay never runs that step. The table's "exact quote" joins separate sentences, and the second-genesis rule is a new write-time check in that shape, not a change to Part 5's source-dependent refusal. Part 5 stays unchanged. The published genesis and horizon descriptions stay unchanged; the cross-version predecessor is the Decision 1 supplement, and it is schema-valid because `family-horizon.v1` allows a string predecessor while `act-horizon-genesis.v1` has none.

4. **The sale writers are not the three named.** `f1099k_statement_recording.py` has `record_f1099k_statement_durably` (genesis at 443-453), `record_f1099k_no_statements_durably` (genesis at 716-726), and `record_f1099k_statement_answers_durably` (802), which does not open a horizon. There is no removal writer. Section 1.6's "removing a statement" is not a path. `family.f1099k.json:1-16` is the only 1099-K declaration; its claim does not authorize a multi-payer sum. Section 5's future-successor requirements match the v1 predicate and the bundle keys. Do not describe a v2 declaration as present.

5. **Containment is not the old raise, and it is not a pending-upgrade reader.** Before `34ca5860`, any second chain for a family id raised. This branch admits another version (`marshal.py:307-322`) and still raises when the adopted version has more than one scope (`marshal.py:316-319`). Refusing authority when more than one version is current for the same family id and scope is the right Finding 1 rule, and it correctly leaves the saved zero current with no forward path. "Restores baseline" and the test's `coverage: unclosed` are a different failure from that raise. Say which one. Owner decision 5's pending-upgrade indicator is a reader change this unit excluded. The untouched standing is already stated: v1 closure and zero stay current, and the new package does not calculate.

## Unfinished mechanisms

- Pre-persistence `apply_act` on `append` and `append_batch` is proposed. Today those paths check schema, revision, and the ADR-0077 step only (`act_log.py:206-209` and `262-263`). `read` validates schemas at `act_log.py:170-171` and does not fold. `project` is what raises. The new-write-only second-genesis rule is correctly kept off replay. Post-retirement transition and genesis refusals are safe for old logs only if those acts are never saved, which depends on that write-time fold. The targeted-fold gap for a direct closure `assertion` is stated and is real: existing lattice refusal is `findings.py:644-647` with `facts.py:272`, so `project` fails later and `read` does not.
- The test matrix is unexecuted, as labeled. It names Finding 1, the recorder bypass, and the old-engine `read` boundary. It does not name a historical two-genesis log that stays readable, third-version genesis, chained or reverse handover, a closed-nonempty handover, or the untouched workspace. Finding 1 is specified on the helper log, not through the recorder.

## Owner choices, after the repair

Do not pick these here.

| Choice | Value | Cost | Risk | Limitation |
| --- | --- | --- | --- | --- |
| A. Recorder stages handover in the same save as the first v2 family write. B. A separate upgrade step. | A avoids a v2 genesis beside v1. B keeps v1 writes until the person upgrades. | A couples every family writer to the new act. B blocks v2 writes until that step exists. | A still asks the completeness question again. B leaves stale v1 writers if a caller skips the step. | Neither creates a 1099-K v2 declaration or a removal operation. Answers do not open the horizon. |
| Full fold before every save, or lifecycle kinds only. | Full fold refuses a bad closure assertion before it is durable. Targeted fold matches the acts that move chains. | Full fold projects every save. Targeted fold leaves a direct closure assertion to fail at `project`. | A missed kind makes a saved log unreadable at `project` while `read` still parses. | Replay must not gain the second-genesis rule. |
| Refuse closure authority when two versions are current for one family id and scope. | Stops Finding 1's adopted closure from being admitted. | The synthetic helper must stop appending a second current chain. | Calling this the old raise, or a quiet unclosed family, changes who else can calculate. | The saved zero stays current. There is no supported repair of that log inside handover. |
| Wash-sale fixtures: clean v2 genesis, or an explicit handover in the setup. | Clean genesis avoids a both-current baseline. | Handover-in-setup records a retirement the tests must understand. | Either choice is fixture policy, not a wash-sale migration. | After handover, an empty subtotal still needs its own fresh closure. |

## Next step

Repair those five requirements in the proposal. Then the owner can choose the trigger, the fold scope, the containment failure mode, and the fixture policy. No schema, no ADR draft, and no implementation charter in that pass.

## Repair confirmation

Checked at HEAD `b33a8be31bfab96a856654248776fd0fe3a5ec0c` on `milestone/multiple-statement-circumstances-consolidation`. No probes. The five wrong requirements and the missing tests are resolved. The owner-choice table is an accurate basis for the four decisions. **READY for owner decision.**

The cascade now runs from the superseded-entity set at `facts.py:228` through `currency.py:225` and the individuation edges at `currency.py:156-168`, then derived pins at `projection.py:66-75`. Box 1a stays on payer, statement, and tax-year (`f1099k.bundle.v3.json:13-30`); the horizon-keyed closure is `f1099k.bundle.v3.json:81-90`. Handover authorizes nothing by itself: a fresh true closure and an explicit rerun are still required before empty subtotals publish. Decisions 3, 5, 6, and 7, and ADR-0077 Part 5, are Unchanged. The Part 5 quote is the single sentence at `docs/adr/0077-shared-key-count-basis-same-run-read-and-presence-selection.md:345`. Second-genesis is a new write-time check on that boundary, and the historical two-genesis row keeps it off replay. Published genesis and horizon sentences stay unchanged; the cross-version predecessor remains the Decision 1 supplement. The statement writer (349), the no-statement writer (687), and the answers writer (802) are the real paths; answers open no horizon, and there is no removal writer. `family.f1099k.json:1-16` v1 is the only declaration. Both-current containment refuses closure authority with `SourceAuthorityError("family has multiple active version chains")`, leaves the saved zero current, and has no handover repair. The untouched standing is section 1 and `test_untouched_workspace_standing`.

Section 9 also names third-version genesis, chained handover, reverse handover, and closed-nonempty handover. All of those rows are unexecuted specifications. Section 11 carries the trigger, the fold scope, the containment refusal, and the fixture policy, with the same value, cost, risk, and limitation. The added note that statement recorders already fold staged acts matches `f1099k_statement_recording.py` calling `project` and `apply_act`. Candidate `34ca5860` and sale Track 0 stay unaccepted. This confirmation does not choose for the owner.
