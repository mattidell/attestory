# Browser Evaluation Runner Residual Repair (R1/R2) — Delta Review

Status: **READY**
Date: 2026-07-25
Role: independent High / medium delta Reviewer (same lineage as the F1–F6 delta review; fresh session)
Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-25-browser-evaluation-runner-residual-repair-review.md`

## Capsule echo (pre-review)

| Item | Resolved value |
| --- | --- |
| **Source ref** | `track/browser-evaluation-runner-completion` → `28cb9c858ec93bd990cd4d303c532af6c15648e1` (working tree clean) |
| **Exact object** | Commit `22776b9` ("bound and isolate injection acknowledgements"), relative to the accepted F1–F6 repair commit `e189304`. Limited to `tools/presentation_harness/lib/executor.mjs`, its focused tests, and the corresponding README sentence. |
| **Scope** | Verify only that R1 (acknowledgement bypasses `timeout_ms`) and R2 (fixed, guessable acknowledgement marker) are closed, and that the accepted F1–F6 repair plus directly touched invariants remain intact. |
| **Evidence-rung ceiling** | One focused two-finding recheck. No re-opening of the original F1–F6 sweep, no exploration past R1/R2. |
| **Stop conditions** | None tripped: repair object resolved cleanly, both residuals have committed regressions, Chrome available, no Builder working context consulted. |

Builder self-report treated as input, not proof — both residuals were
independently reproduced with fresh, self-authored attacks (not the committed
test's exact fixtures) before accepting the fix.

## Verdict

**READY**

Both R1 and R2 are closed. The accepted F1–F6 floor is intact (34/34 focused
Node tests, including the two new residual regressions). CI `verify` is green
at the reviewed tip.

---

## Independent verification

### 1. R1 — acknowledgement now bounded by `timeout_ms`

Read the diff (`e189304..22776b9`) directly: the acknowledgement read is now
wrapped in the same `withTimeout` helper already used for criterion checks,
racing against `manifest.timeoutMs` and throwing `TimeoutMarker` on expiry;
the surrounding `catch` still maps any failure — throw, stall, or timeout —
to the existing closed reason `injection-failed`.

Independently reproduced with a **freshly authored** repro (not the committed
test's fixture): a candidate page that goes render-thread-busy for 8 seconds
right after `load`, with an ordinary (non-adversarial) tamper injection
present, `timeout_ms: 1000`. Result: **exit `2`, `injection-failed`, elapsed
~3.0s** — bounded, not the full 8-second busy duration and not a pass. This
is the same class as the original finding, run cold. The committed
`real-Chrome-repair` test asserts an equivalent bound (`elapsedMs < 7000`)
using its own fixture; both converge on the same behavior.

Cleanup: the timeout path still disposes cleanly — the smoke run and the
`.repair-battery-*`/reviewer scratch directories left no orphaned temp
profiles after either reproduction (checked via the repair battery's own
profile-name diffing, which passed at 34/34).

### 2. R2 — marker is now per-tuple and non-guessable

Read `executor.mjs`: the acknowledgement key is now
`` `__presentationHarnessInjectionAcknowledged_${randomUUID()}` ``, generated
fresh per tuple and closed over by that tuple's evaluate expression only —
never the old fixed literal.

Independently reproduced the exact collision attack: a candidate page that
pre-sets the **old, pre-repair fixed name** to `true`, paired with a tamper
injection that throws immediately (never completes). Result: **exit `2`,
`injection-failed`** — the collision no longer succeeds because the harness
is no longer looking for that name. The committed test exercises the
identical attack shape with its own fixture and passes.

### 3. Valid injection still acknowledges and passes

Covered by the credited F1–F6 battery (unchanged in this repair): the
real-Chrome battery's `valid-injection` tamper case still reaches `pass` with
the new per-tuple marker, and the full 34/34 focused suite is green,
confirming the timeout/marker changes did not regress the positive path.

### 4. Marker privacy and determinism

- Grepped stdout/stderr from both of my fresh reproductions above for
  `presentationHarnessInjectionAcknowledged`: **absent** in both streams for
  both R1 and R2 repros.
- Committed battery asserts the same on its own captured stdout/stderr
  (`includes("__presentationHarnessInjectionAcknowledged_")` → `false`).
- Re-ran the smoke manifest and diffed byte-for-byte against
  `examples/reports/smoke-expected.v1.json`: **identical**. The per-tuple
  random marker never entering output means the now-nondeterministic internal
  value has no effect on deterministic public bytes, as required.

### 5. Focused floor (independently run once)

```
node --test tools/presentation_harness/tests/*.test.mjs
```

**34/34 pass** (33 from the accepted F1–F6 floor + 1 new unit test for the
bounded-timeout case; the real-Chrome battery itself grew in place to cover
both residuals rather than adding a second real-Chrome test, so the visible
count only grew by one). Did not recreate the original review rig or repeat
unrelated probes, per charter.

```
node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/smoke.v1.json
python3 -m unittest tests.test_presentation_economy   # 27 tests OK
```

### 6. Repository gate

```
python3 tools/governance_lint.py       # conformant
python3 tools/envelope_scan.py --range main..HEAD   # clean
git diff --check main..HEAD           # clean
```

PR #71's `verify` CI is `SUCCESS` at head `28cb9c8`
(`https://github.com/mattidell/attestory/actions/runs/30178738931`).

---

## Findings

None. Both accepted residuals are closed; no new residual identified within
the chartered R1/R2 boundary. Per charter, I did not explore past this
two-finding gate.

## Out of scope (honored)

No implementation repair, no sub-agent spawn, no push/PR/merge, no completion
record, no re-opening of the F1–F6 sweep, no exploration beyond R1/R2.
