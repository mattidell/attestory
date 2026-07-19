# Confirmation R1 — D2 Repair 1

**Seat and boundary.** Fresh independent confirmation reviewer, released by the
owner for this exact charter. I reviewed only Repair 1, its examination, the
Round-1 reviews/triage, named ADR context, and the committed evaluator,
runner, package, projection, explanation, and current line-16 surfaces. I
made no production or schema change, wrote no test, ADR, or evaluation
analysis, and did not assess D1, D3, statutory fidelity, or presentation.
All cited cases are the synthetic `demo-*` paper cases.

## Charter measurements

| # | Result | Concrete evidence |
|---|---|---|
| 1 | **Pass** | Repair 1 specifies one v2 replacement and a package pin from v1 to v2, expressly excluding a second producer and dynamic `conflict_semantics` selection ([design](../repair1/design.md) §§Spine, D2-P2). This accurately differs from HEAD: the current content has the one v1 line-16 producer ([rule.form1040-line16.json](../../../../packages/content/tax/2025/rule.form1040-line16.json) lines 2–24); package validation records output owners from members and only uses `conflict_semantics` for a declared multi-producer conflict ([package_validation.py](../../../../packages/derivation/package_validation.py) lines 347–354, 409–420, 646–652), not as a guard-policy evaluator. The v2 successor is a labelled production condition, not claimed live. |
| 2 | **Pass** | In the synthetic `demo-q-0` case, the proposed first `any` operand reads Q and returns true before the declaration `all`; `choose` then evaluates the ordinary branch ([design](../repair1/design.md) lines 57–79, 102–105). This is supported by the committed evaluator: `any`/`all` use generator short-circuiting and `choose` evaluates exactly its selected branch ([evaluator.py](../../../../packages/derivation/evaluator.py) lines 160–171). Thus neither new declaration is read and the stated value is the unchanged `OrdTax(T)` algebraically. |
| 3 | **Fail** | The `demo-q-600` both-absent case does factually not publish, but it cannot name *both* required declarations. `ref` records a reference and immediately raises `EvalBlocked(BLOCK_ABSENT, [name])` for the first absent symbol ([evaluator.py](../../../../packages/derivation/evaluator.py) lines 108–116); the proposed `all` consequently short-circuits ([design](../repair1/design.md) lines 57–63, 94–100). The runner records that one exception's `missing` list ([runner.py](../../../../packages/derivation/runner.py) lines 336–357, 406–418), and the NPE walk unions only ledger-recorded `missing` values ([explanation.py](../../../../packages/derivation/explanation.py) lines 245–260). `access.refs` would pin both declarations only after a successful `no`/`no` evaluation ([runner.py](../../../../packages/derivation/runner.py) lines 251–290), so it cannot supply the required two-fact missing-declaration walk. |
| 4 | **Pass** | A present synthetic `demo-yes` yields the proposed false guard, not a fictional blocked code. The runner writes `inapplicable` with `guard_result: false` ([runner.py](../../../../packages/derivation/runner.py) lines 336–351); the existing runner test asserts the same outcome ([test_runner.py](../../../../tests/derivation/test_runner.py) lines 106–115), and the NPE test maps it to `guard_inapplicable` ([test_npe_walk.py](../../../../tests/derivation/test_npe_walk.py) lines 107–131). Repair 1 calls this committed disposition and labels any custom blocked vocabulary a versioned production condition ([design](../repair1/design.md) lines 82–92). |
| 5 | **Pass (paper / production condition)** | Repair 1 retains a precise pre-mutation admission-locus interlock for declaration-first, signal-first, and same-batch `demo-*` attempts; it says neither state becomes current in the same-batch case ([design](../repair1/design.md) lines 130–151, 155–166). It limits the proposed bindings to T, Q, filing status, rounding, the two declarations, and parameters/brackets, explicitly excluding box 2a, its signal, and recorded-non-composable content. It does not misstate this as HEAD behavior: the admission interlock and universe guard are explicitly listed as production conditions ([design](../repair1/design.md) lines 180–188). |
| 6 | **Pass** | The design consistently marks absent implementation as production conditions rather than live behavior: fact/binding domain enforcement, sole v2 package adoption, QDCG coordinator goldens, admission temporal kill tests, and the no-reach-around universe check are enumerated ([design](../repair1/design.md) lines 180–188). The authoritative checks are correspondingly proposed at package/admission/coordinator surfaces (including cases 1–7 at lines 155–166), and the optional custom disposition is explicitly conditional rather than claimed. No rule or test is written here. |

## Narrow verdict

**Not confirmed.** Repair 1 resolves the single-successor posture, qualified-zero
reduction, honest present-`yes` disposition, and paper P3 boundary, but not the
decision-blocking requirement that the qualified-positive, both-absent case
produce a walk naming both factual declaration gaps. A bounded follow-up must
address that missing-declaration walk only.
