# Track 1 Harness-Core Review — Lifecycle and Failure Integrity

Status: **NOT READY**
Date completed: 2026-07-25
Role: independent High / high technical-adversary Reviewer
Charter:
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-24-presentation-economy-t1-harness-core-review.md`

Owner/foreman disposition, 2026-07-25: the finding stands. The owner declined
a repair cycle and closed the economy milestone after its accepted Track 0
foundation. The reviewed Track 1 implementation was not merged; its repair and
delta-review charters were retired unexecuted. This disposition does not turn
`NOT READY` into acceptance.

## Review object

The Reviewer resolved
`track/presentation-economy-t1-harness-core` once at dispatch. The
artifact-quality object is the Track 1 implementation commit named
`implement Track 1 instrumented harness core and fail-closed lifecycle`
relative to `main`, limited to `tools/presentation_harness/**` and the Track 1
additions to `docs/presentation-economy/README.md`. Foreman continuity commits
are outside the reviewed object.

The Reviewer completed the chartered reads, verified that Chrome was
available, used only synthetic local inputs, and reported no capsule stop
condition. The owner halted the first turn before the written record was
assembled, then accepted the independently measured blocker set as sufficient
to complete the gate with `NOT READY`. The same Reviewer supplied this bounded
evidence handoff without further tools or repository changes.

## Verdict

**NOT READY.** Six blocking behaviors violate the approved Track 1 contract.
Any one is sufficient to block the track:

1. fresh targets do not prevent cross-tuple origin-storage leakage;
2. malformed pre-load injection can become a false pass;
3. signals during Chrome launch leave temporary profiles behind;
4. the CLI accepts a traversing manifest path and emits invalid provenance;
5. check parameters and an empty matrix are not strictly validated; and
6. infrastructure stderr echoes rejected input.

The smallest repair is the focused Track 1 harness repair chartered at
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-25-presentation-economy-t1-harness-core-repair.md`.
No Track 2 work may begin.

## Blocking findings

### F1 — Cross-tuple browser state leaks

An ignored synthetic page wrote one `localStorage` key in the first of two
matrix tuples and required the second tuple to observe no prior value. Running
the harness over that two-tuple manifest exited `1`: the first tuple passed and
the second failed `criterion-unmet`.

`tools/presentation_harness/lib/executor.mjs` creates a fresh target at lines
51–56 and closes it at lines 83–90, but every target remains in the same
browser profile and origin-storage context. A fresh target is therefore not
the state-isolation boundary claimed by the Track 1 contract.

**Required repair:** isolate origin storage per matrix tuple while preserving
one Chrome process, and add real cookie and `localStorage` leakage regressions.

### F2 — Malformed injection becomes a false pass

A tamper case containing syntactically invalid JavaScript was accepted by the
manifest and registered through
`Page.addScriptToEvaluateOnNewDocument`. The otherwise passing criterion
reported `pass`, reason `null`, and process exit `0`.

`manifest.mjs` lines 154–166 accept any string as injection source.
`executor.mjs` lines 141–150 treat successful CDP registration as successful
injection and do not prove that the script parsed or executed.

**Required repair:** reject syntactically invalid injection before Chrome
launch and add an execution acknowledgement that turns a non-executed
injection into `injection-failed`, never a pass.

### F3 — Launch-time signals leak temporary profiles

In separate invocations, the Reviewer waited until the Chrome child appeared
and then sent `SIGINT` or `SIGTERM`. Both harness processes exited `2`, but the
Chrome child was still present at the immediate check and one new temporary
profile remained after each invocation. The two exact synthetic profiles were
removed after measurement.

`run.mjs` installs signal handlers at lines 92–106, but cleanup can dispose
Chrome only after `launchChrome()` returns and assigns `chromeHandle` at line
110. `chrome.mjs` creates the profile and child at lines 75–100 before it
returns an owned disposal handle at lines 148–157. A signal in that ownership
gap exits without profile cleanup.

**Required repair:** make Chrome launch cancellation-safe and transfer cleanup
ownership as soon as the child/profile exist. Regress both launch-time and
post-launch `SIGINT`/`SIGTERM`.

### F4 — Manifest traversal bypasses CLI confinement

The CLI accepted a repository-neighbor traversal spelling that resolved back
to the committed smoke manifest. It completed normally with exit `1`, retained
the traversal spelling in report `manifest_name` and observation `provenance`,
and the Track 0 observation validator rejected that provenance as not
repository-relative.

`run.mjs` lines 60–69 reject only absolute paths and directly join the
un-normalized argument to the repository root. Lines 113 and 120 then publish
the original spelling.

**Required repair:** canonically confine the manifest argument before reading
it, reject traversal and symlink escape, and emit only its normalized
repository-relative form.

### F5 — Manifest strictness is incomplete

Independent in-memory mutations showed that the validator accepted:

- a missing required check parameter;
- an unknown check parameter;
- a selector with the wrong type;
- a negative keyboard tab count; and
- an empty top-level matrix.

The accepted empty matrix produced zero cases, `passed: true`, and exit `0`.
`manifest.mjs` line 150 only requires `params` to be an object, and lines
169–228 allow the top-level matrix itself to be empty.

**Required repair:** validate exact parameter keys, types, and ranges for every
named check; require the non-empty selections needed for a trustworthy run;
and prove an empty matrix cannot pass.

### F6 — Infrastructure stderr echoes rejected input

Supplying a synthetic unknown CLI argument exited `2` with reason
`manifest-invalid`, but stderr repeated the rejected argument verbatim.
`run.mjs` line 33 embeds raw input in the exception and lines 42–45 serialize
the message.

**Required repair:** external infrastructure output must use closed reason
codes and fixed redacted messages. Audit every error path for rejected values,
paths, ports, browser details, and stack content.

## Passing and advisory evidence

The completed measurements also established:

- unknown keys/version, duplicate and dangling ids, candidate/fixture path
  traversal, absolute and remote candidate paths, non-synthetic fixtures, and
  invalid timeouts are rejected before Chrome;
- exit `0`, criterion-failure exit `1`, and infrastructure exit `2` were all
  independently exercised;
- a real non-loopback request was intercepted and produced
  `non-loopback-request-blocked` with exit `2`;
- the committed smoke continued through later tuples after a criterion
  failure;
- keyboard checks use real `Input.dispatchKeyEvent`, and contrast uses browser
  computed style and luminance recomputation;
- two committed-smoke runs were byte-identical and matched the golden;
- the normal smoke observation recorded one browser, three sessions, six
  cases, direct duration, and explicit missing foreman/cache measures, and was
  valid against the Track 0 observation shape; and
- the two raw NUL bytes in `manifest.mjs` are tuple delimiters only. They hide
  no executable content, but they make ordinary Git source diff classify the
  file as binary. This remains a bounded advisory, not a Track 1 blocker.

## Verification completed

| Command or measurement | Result |
| --- | --- |
| `node --test tools/presentation_harness/tests/*.test.mjs` | 27/27 pass |
| committed real-Chrome smoke | expected exit `1`; 4 pass / 2 criterion fail |
| full Python unittest | 590 tests, OK |
| mypy | success, 117 source files |
| governance lint | conformant |
| envelope scan over `main..HEAD` | clean |
| `git diff --check main..HEAD` | clean |
| two-run smoke determinism | byte-identical; exact golden match |

The worktree did not contain its own `.venv`; the Reviewer ran the same
repository virtual environment from the primary checkout while retaining the
Track 1 worktree as its working directory. This is an environment note, not a
test substitution.

## Reviewer execution economy

Tokens were not exposed and remain unknown. The Reviewer reported:

| Measure | Directly reported value |
| --- | ---: |
| model-response turns | 42 |
| total tool calls | 41 |
| repository/governance/context reads | 11 |
| implementation/source inspections | 6 |
| required test/harness calls | 7 |
| Chrome/adversarial/environment probes | 14 |
| status/coordination calls | 1 |
| write calls | 2 |
| harness invocations | 12 |
| Chrome launches | 11 |
| completed fresh targets | at least 18 |
| completed criterion results | 30 |
| directly timed command execution | 160.068 seconds |
| foreman-observed dispatch-to-interruption | 751 seconds |

Browser work was command-line batched CDP automation, never interactive use of
a signed-in browser. Nine completed Chrome runs accounted for the observed
targets/cases; two additional launches were interrupted during launch and
their target counts remain unknown.

Three governing/context reads individually returned roughly 10.9k–11.7k
tokens and were truncated by the tool. Implementation reads were generally
4k–6.5k tokens. The committed smoke output was about 1.5k tokens. These
measurements support separating a mechanical measurement runner from the
judgment-only reviewer surface; they do not support an exact total-token or
monetary-cost claim.

## Measurements transferred to the repair delta review

The blocker evidence is sufficient for `NOT READY`, but the following original
measurements were not completed before interruption and must be included in
the post-repair delta review:

- explicit live enumeration of exactly one Chrome main process and its target
  list;
- explicit before/after cleanup measurement for normal and infrastructure
  error exits, in addition to both signal paths;
- an exhaustive scan of every stdout/stderr field class for content leakage;
  and
- public whole-dataset validation of a captured observation using a compatible
  committed workload, rather than only the Track 0 observation validator
  function.

No repair, push, PR, merge, or Track 2 work occurred during review.
