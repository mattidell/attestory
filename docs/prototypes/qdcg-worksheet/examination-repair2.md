# Examination: Repair 2 — QDCG Missing-Declaration Walk (D2)

Rung 1 paper only. Self-examination of `repair2/design.md`, per
`charter-repair2.md`. Not an independent review; does not release any
confirmation seat. No probe, production edit, or claim that a D2 worksheet
production condition is live at HEAD. All examples synthetic `demo-*`.

## D2-P1 — declared absence and present-`"yes"` outcome — settled at Rung 1, unchanged

The two ADR-0032/ADR-0036 assertion types, their `{yes, no}` domain, no
default, and presence-before-value are untouched by the guard substitution
(design §5). The present-`"yes"` outcome is re-derived, not merely asserted:
`conditional_dependency_set` succeeds on presence alone (returns `True` once
both refs read without error), so a `"yes"` value never triggers the node's
`EvalBlocked` path — it falls through to an ordinary `categorical_compare`
that evaluates to boolean `False`, giving the committed
`inapplicable`/`guard_result:false` disposition Repair 1 established (design
§3). Absence and present-wrong-value are different evaluator code paths with
different exception behavior, traced through committed `evaluator.py`/
`runner.py` line numbers, not asserted.

## D2-P2 — successor posture, reduction, missing-declaration walk — now fully settled at Rung 1

This is the finding Repair 2 exists to close. The design cites the committed
`conditional_dependency_set` handling (`evaluator.py` 204-223) to show, from
actual HEAD code rather than the ADR-0037 paper text, that a true condition
with two absent members accumulates both names into one `EvalBlocked` before
raising, and traces that exception through `runner.py`'s guard `try` and
`explanation.py`'s NPE union to a one-row, two-name walk (design §1). It
re-derives the single-absent case symmetrically, so the walk names exactly
the true absent set in every combination, never fewer, never an implied
zero — closing measurement 3's exact fail mode.

The reduction property (design §2) is grounded correctly per the charter's
own bar: it cites the node's *own* false-condition contract
(`evaluator.py` line 211-212, `if not bool(evaluate(condition,...)): return
True`) as the reason `Q=0` never reads the declarations, and the guard is
restructured (node first, unconditional, inside the outer `all`) specifically
so that citation is literal rather than incidental to a separate short-
circuit elsewhere in the expression. This is a genuine improvement over
Repair 1's structure, where the same outcome existed but depended on the
`any`'s operand order.

**D2-P2 is fully settled at Rung 1**: single successor posture,
qualified-zero reduction, present-`"yes"` disposition, and the
two-declaration missing walk are now all re-derived against one consistent
guard expression, cited to committed HEAD source at every claim. What is
**not** settled — the design says so directly — is that none of this is live
production content: no `rule-artifact.v3` line-16 rule, package pin, or
coordinator golden exists for the D2 worksheet itself. Only the generic
`conditional_dependency_set` substrate is committed; the worksheet's *use* of
it remains a Rung-1 paper design, as Repair 1's portions still are.

## D2-P3 — bidirectional contradiction and universe boundary — settled at Rung 1, unchanged

Untouched by construction: the guard substitution is inside the
qualified-positive presence/value check and shares no surface with the
pre-mutation admission-locus interlock. The design states this (design §5).

## Honest gap and one collateral finding

The design reports, rather than works around, one required correction: the
line-16 successor must be authored under `rule-artifact.v3`, not `.v2`
(ADR-0037 decision 1 restricts the new node to the new schema version), so
Repair 1's "v1→v2" package pin is now "v1→v3." Scoped to D2-P2's own
successor-identity claim, not D2-P1's fact types or D2-P3's interlock — but
real and load-bearing, worth a future confirmation check.

## Outcome

| Proposition | Repair 2 outcome |
|---|---|
| D2-P1 | Settled at Rung 1 (unchanged, re-derived) |
| D2-P2 | **Settled at Rung 1** — successor posture, reduction, and two-declaration walk all cited to committed HEAD source |
| D2-P3 | Settled at Rung 1 (unchanged) |

Per the charter, the next step, if the owner agrees D2-P2 is settled, is a
fresh narrowly-scoped confirmation pass re-measuring only what Repair 2
changed — not evaluation analysis or ADR drafting, which this charter does
not authorize.
