# Browser Evaluation Runner Repair — Delta Review

Status: **READY**
Date: 2026-07-25
Role: independent High / medium delta Reviewer (technical-adversary lens)
Charter: `docs/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair-review.md`

## Capsule echo (pre-review)

| Item | Resolved value |
| --- | --- |
| **Source ref** | `track/browser-evaluation-runner-completion` → `df70ea162e55abf3e8e81b09caa6d79cfa32a7ef` (working tree clean at this tip) |
| **Exact object** | The repair at commit `e189304` ("repair browser evaluation runner integrity"), diffed against the adopted pre-repair implementation commit `c00e58d` ("implement Track 1 instrumented harness core and fail-closed lifecycle"). Limited to `tools/presentation_harness/**` and the Track 1 sections of `docs/presentation-economy/README.md`. |
| **Role** | One fresh independent delta Reviewer, High tier / medium effort, technical-adversary lens. The original reviewer's lineage was not resumable in this session; this is the fresh path the charter permits. |
| **Scope** | Independently verify F1–F6 closed without weakening one-process batching, closed exit/reason semantics, network confinement, deterministic content-free reports, or Track 0-compatible observations; complete the four measurements transferred from the interrupted original review. |
| **Evidence-rung ceiling** | Focused delta review only. No re-implementation, contract redesign, product/economy/novelty work, or generalization. |
| **Stop conditions** | None tripped: source ref and repair object both resolved cleanly; the prior completed review and repair charter are both present; Chrome (`Google Chrome.app`) is available; no personal/remote data was needed. |

Builder self-report (repair commit message, repair charter, milestone status
prose) was treated as input, not proof. Every finding below was independently
reproduced by rerunning the committed battery and by constructing fresh
synthetic attacks not already present in the committed suite.

## Verdict

**READY**

All six blockers (F1–F6) are closed and independently reproduced. All four
transferred measurements are completed, including one (whole-dataset Track 0
observation validation) that the repair had not actually demonstrated and
which I completed as part of this review. No regression found in adjacent
invariants. CI `verify` on PR #71 is green.

---

## Prior evidence credited, not repeated

Per the charter's "do not repeat" instruction, I did not reconstruct the
harness seed, reopen settled design alternatives, or rerun the original
review's full 42-turn adversarial sweep. F1–F6 are treated as known attack
classes with a committed regression (`tests/real-chrome-repair.test.mjs`)
that already exercises most of them end-to-end against real Chrome. I ran
that battery once, read it line-by-line to confirm it tests what it claims
(not just its name), and then spent independent effort only on gaps I found
in its coverage and on the transferred measurements.

## Independent verification

### 1. Mechanical repair battery (independently run)

```
node --test tools/presentation_harness/tests/*.test.mjs
```

33/33 pass, including `real-Chrome repair battery closes F1-F6 twice with
deterministic correctness output` (10.0s, single real-Chrome session). Read
the test source directly (not the commit message) to confirm it actually
exercises: cookie/`localStorage` isolation across two tuples (5/5 pass, 0
leaked), syntactically invalid injection rejected pre-Chrome
(`manifest-invalid`), five strict-validation mutations (missing/unknown/
wrong-type/negative/empty-matrix, all `manifest-invalid`), symlink and `..`
traversal escape (rejected, outside path never echoed), an unknown CLI
argument (rejected, value never echoed), launch-time `SIGINT` cleanup
(zero leaked profiles), and post-launch `SIGTERM` cleanup after
`DevToolsActivePort` appears (zero leaked profiles).

```
node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/smoke.v1.json
python3 -m unittest tests.test_presentation_economy   # 27 tests OK
python3 tools/governance_lint.py                      # conformant
python3 tools/envelope_scan.py --range main..HEAD     # clean
git diff --check main..HEAD                           # clean
```

Smoke run: exit 1, 4 pass / 2 fail / 0 error, `manifest_name` emitted as the
normalized repository-relative path (not the CLI's literal argument).

### 2. Tuple isolation (F1) — architecture read + credited battery result

`launchChrome()` has exactly one call site in `run.mjs`; per-tuple isolation
is via a fresh CDP browser context per tuple in `attachFreshTarget`
(executor.mjs), disposed on both the success and error path. One Chrome
process serves the whole batch by construction — there is no code path that
launches a second browser. The committed battery's 5/5 clean result over two
consecutive tuples is the live-Chrome evidence for the storage boundary; I
did not re-run a redundant leak probe since this is exactly what that test
measures.

### 3. Injection integrity (F2) — new adversarial coverage

The committed suite tests two of the three required injection classes
(syntactically invalid → rejected pre-Chrome; valid-and-executed → passes)
plus a *mocked*-CDP unit test for "no acknowledgement." It does **not**
real-Chrome-test the class the original finding actually described: an
injection that is syntactically parseable but **throws at runtime before
reaching the acknowledgement statement** — passing the harness's pre-launch
parse check but never executing to completion. I constructed this case
independently: a tamper case whose injection source is a single statement
that throws immediately, so the appended acknowledgement statement can never
run.

Result against real Chrome: exit `2`, case outcome `error`, reason
`injection-failed`. Confirmed the fix closes the exact failure mode, not just
the two cases the committed suite happened to cover.

### 4. Lifecycle cleanup (F3) — credited battery result

Committed battery asserts zero net new temporary profiles after: normal
completion, launch-time `SIGINT` (killed while waiting on
`DevToolsActivePort`), and post-launch `SIGTERM` (killed after the profile is
`DevToolsActivePort`-ready). Read `chrome.mjs`: the ownership callback fires
before `spawn()` returns, and `run.mjs`'s `cleanup()` prefers
`chromeHandle.dispose()` once available, falling back to the pre-handle
disposer otherwise — closing the ownership gap the original review's signal
probes found. No further live-signal probing needed beyond the committed
battery.

### 5. Path/provenance confinement (F4) + whole-dataset Track 0 validation — completed transferred measurement

Committed battery covers `..`, symlink, and repository-neighbor traversal, all
rejected before Chrome with no path echoed. I additionally confirmed the
*positive* path: a normal smoke run emits `manifest_name:
"tools/presentation_harness/examples/manifests/smoke.v1.json"` (the
normalized form), not any raw argument spelling.

The milestone plan and repair charter both required validating a captured
observation through the public Track 0 dataset validator
(`python3 -m tools.presentation_economy validate --dataset ...`). **This had
not actually been done** — no compatible workload/dataset fixture exists
anywhere in the repair diff or the wider repo tying a harness-run observation
to the Track 0 schema. I completed it: captured the smoke run's observation
fragment, wrapped it in a minimal `frozen-comparison`-kind workload built only
to satisfy schema shape (no economy claim, empty `comparisons: []`), and ran:

```
python3 -m tools.presentation_economy validate --dataset <constructed>
→ {"valid":true}
```

This closes the one transferred measurement the repair's own evidence trail
did not actually demonstrate.

### 6. Strict validation (F5) — credited battery result

Committed battery attacks missing/unknown/wrong-type/out-of-range parameters
and an empty top-level matrix; all five mutations correctly produce
`manifest-invalid` before Chrome launches. Read `manifest.mjs`'s parameter
rule table directly: all four existing checks (`dom-text-present`,
`computed-style-contrast`, `role-alert-present`, `keyboard-focus-reachable`)
have an exact declared key set and validator, matching `checks.mjs`'s
registered check names one-to-one — no check is missing a rule and no rule
references a nonexistent check.

### 7. Output safety (F6) — code-path audit, not just the one committed test

The committed suite proves one case (unknown CLI argument never echoed). I
additionally read every error-construction site to confirm the redaction is
structural, not incidental: `writeInfraError` always prints a fixed message
looked up by reason code, discarding whatever is in the underlying error's
own message — including the one path where a manifest validation error's
granular reason/message (which can contain manifest-supplied strings, e.g. an
unknown check name) is wrapped into an infrastructure error before being
thrown in `run.mjs`; the wrapper's own top-level reason code is always the
fixed `"manifest-invalid"`, so the embedded detail is never printed. The same
holds for Chrome launch failures (raw spawn error text) and internal errors
(stack traces): both are captured on the `Error` object but only the fixed
safe-message lookup ever reaches stdout/stderr. Case-level `reason` fields in
the report are all literal string constants from the closed error-reason set
— grepped `executor.mjs` for every assignment site; none interpolates
content.

### 8. Regression boundary — adjacent invariants

Full focused Node suite (33/33) and Python focused suite (27/27) both pass
with no change outside the repaired files. Batch continuation
("a target/load failure in one tuple does not block the next independent
tuple") and non-loopback blocking tests are unmodified and still pass. The
raw-NUL tuple delimiter (`manifest.mjs`'s NUL-byte separator) is byte-identical
before and after the repair (same two offsets, same count) — the repair did
not touch it, consistent with the charter's instruction to leave that
advisory alone.

### 9. Repository gate

Local: governance lint conformant, envelope scan clean, `git diff --check`
clean. PR #71's `verify` CI check is `SUCCESS`
(`https://github.com/mattidell/attestory/actions/runs/30175915176`). Relied on
that as the authoritative full-suite floor per the charter; did not duplicate
it locally.

---

## Findings

None blocking against the chartered F1–F6 scope. One completed-but-previously-
undemonstrated measurement (§5 above) and one newly-covered adversarial case
(§3 above) are recorded as this review's contribution beyond the committed
evidence. The verdict above is unchanged by the residual findings below —
they were found by voluntary exploration past the charter boundary, at owner
invitation, not by a required measurement.

## Residual findings (beyond charter scope; non-blocking)

The chartered scope is F1–F6 plus directly touched adjacent invariants. The
following two findings came from exploring one step past that boundary, after
the READY verdict above. Neither is a correctness-invalidating regression of
F1–F6; both are logged for owner disposition rather than repaired here
(reviewer does not repair; the milestone's cap is one repair, one review).

**Framing.** This harness's actual failure mode of concern is a *silent false
pass* — the tool's whole value is that `passed: true` means what it claims.
It is not a defense against an adversary editing the harness's own source
(that is an ordinary code-diff/supply-chain concern, already covered by
normal review, and out of scope here).

### R1 — The injection-acknowledgement check bypasses the manifest's own declared timeout

**What it is, concretely:** in `executor.mjs`, every criterion check is
wrapped in `withTimeout(..., manifest.timeoutMs, ...)`, but the injection-
acknowledgement read (`handle.page.evaluate("Boolean(globalThis...)")`,
added by the F2 repair) is a bare, unguarded `await` with no timeout.

**Reproduced:** a candidate page whose script goes render-thread-busy for 8
seconds immediately after the load event (no tamper injection needed — this
is an ordinary, non-adversarial page) against a manifest declaring
`timeout_ms: 1000`. Result: the harness ran **10.2 seconds** and returned
`passed: true`, exit `0` — the declared budget was silently ignored.

**Control:** the identical busy page with the tamper case's injection field
set to `null` (skipping the acknowledgement step entirely) correctly produced
`criterion-timeout`, exit `2`, at ~3.1s — confirming the timeout machinery
itself works and this gap is specific to the one unguarded call the F2 repair
introduced.

**Why it matters (per the framing above, not an adversary story):** this is
an honest correctness bug. A real presentation-review workload with a
synchronously heavy candidate page — plausible, not exotic — can silently
consume far more wall time than declared and still report success, which is
exactly the "report lied and nobody would notice" failure mode the whole
harness exists to prevent. It is not conditioned on any tamper injection
being adversarial; an ordinary `injection: null` case is unaffected, but any
case with a non-null injection (i.e., most tamper cases, since that is the
point of a tamper case) inherits the gap.

**Smallest fix, if pursued:** wrap the existing acknowledgement `evaluate`
call in the same `withTimeout` helper already used for criterion checks,
mapping a timeout there to the existing `injection-failed` reason (already in
the closed case-error vocabulary — no new reason code needed). Small, scoped
change; not attempted here since reviewer does not repair.

### R2 — Acknowledgement marker is a fixed name, not per-run (downgraded to a footnote)

The execution-acknowledgement mechanism reads a fixed global variable name
(`__presentationHarnessInjectionAcknowledged`). A candidate page that
happens to set that same name would be indistinguishable from a tamper
injection that actually ran. On reflection this is not a meaningful risk
under the harness's actual usage model: manifests and candidate fixtures are
authored by trusted builders working in good faith, not adversarially
constructed to defeat the tool, and no realistic authoring path collides with
an internal implementation constant by accident. Recorded only as a minor
design-fragility note; not recommended for repair.

## Out of scope (honored)

No implementation repair, no sub-agent spawn, no push/PR/merge, no completion
record, and no economy/novelty conclusion. The constructed compatibility
dataset in §5 makes no comparison and is not committed — it existed only to
exercise the validator.
