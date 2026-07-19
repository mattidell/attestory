# Examination: Repair 1 — QDCG Line-16 Successor Posture (D2)

Owner-directed foreman completion, 2026-07-18. This supplies the second output
required by `charter-repair1.md` after Repair 1 arrived with its design only.
It is not an independent review and does not release the held confirmation
seat. Rung 1 paper only; no probe, production edit, or claim that a production
condition is live at HEAD. All examples are synthetic `demo-*`.

## D2-P1 — declared absence and present-`yes` outcome — settled at Rung 1

The repair retains two free-supersession ADR-0032 assertion types with the
ADR-0036 categorical `{yes, no}` domain, no default, and presence before
value (`repair1/design.md`, “D2-P1”). They are not unconditional `requires`:
the qualified-zero branch never reads them, while the qualified-positive path
does. That keeps a `no` a present fact and avoids declaration demand where it
has no tax bearing.

For a present `yes`, the sole rule's guard is false and the committed runner
records `inapplicable` / `guard_inapplicable`; the repair no longer claims the
nonexistent `DECLARATION_OUT_OF_SCOPE` blocked code (case 6). This is a
walkable committed outcome, not a claim that a new vocabulary already exists.

## D2-P2 — successor posture, reduction, and missing declarations — unresolved at Rung 1

The repair resolves the two Round-1 posture defects on its main path:

- one v2 successor owns line 16, with no dual producer, dynamic
  `conflict_semantics`, or traversal-order selection claim;
- `Q=0` takes the lazy ordinary branch, reads no declarations, and is
  algebraically the existing `OrdTax(T)` result; and
- `Q>0` reaches the declarations only through evaluated guard access, so a
  successful `no`/`no` worksheet result pins both declarations for
  displacement.

The ladder remains expressible in the committed operation vocabulary: `min`
is composed from `choose`/`compare` (or `subtract`/`max`), and preferential
rates use single-band `bracket_fold` declarations. No authorized probe is
needed for those cited constructions.

However, the repair does **not** yet demonstrate the charter's full missing
declaration case. The guarded `all` short-circuits: with both declarations
absent, the runner may report only the first missing reference. The design
truthfully notes this, but its statement that both declaration symbols are the
contributable gaps is not an executed or structural guarantee that the
non-publication walk names both. Therefore D2-P2 is not settled until the
fresh confirmation measures whether the existing explanation graph can supply
the required two-fact walk, or a bounded repair names a representable route.

## D2-P3 — bidirectional contradiction and universe boundary — settled at Rung 1

The repair preserves admission-locus mutual exclusion between a current
capital-gain-distributions declaration of `no` and
`CAPITAL_GAIN_DISTRIBUTION_RECORDED`: declaration-first, signal-first, and
same-batch candidates reject before mutation (design, “D2-P3”, case 4).
There is no both-current state from which line 16 can publish. The worksheet
binds only taxable income, qualified dividends, filing status, rounding,
declarations, and declared parameters; it has no route to box 2a, its signal,
or recorded-non-composable content (case 7).

The admission interlock and universe guard remain explicit production
conditions, with required temporal and no-reach-around kill tests; this paper
examination does not treat them as implemented.

## Outcome

| Proposition | Repair 1 outcome | Remaining condition |
|---|---|---|
| D2-P1 | Settled at Rung 1 | Confirmation checks the committed present-`yes` walk. |
| D2-P2 | **Unresolved** | Prove or repair the two-declaration missing walk; all other posture defects are repaired on paper. |
| D2-P3 | Settled at Rung 1 | Production admission/universe kill tests remain owed. |

Repair 1 is complete as a two-document artifact, but it is not ready for an
evaluation analysis or ADR. Confirmation R1 remains the next bounded check and
is still inactive pending the owner's separate explicit release.
