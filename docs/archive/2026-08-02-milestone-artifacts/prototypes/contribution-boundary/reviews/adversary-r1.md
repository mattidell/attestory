# Adversary Review R1 — D2 Contribution Boundary

Seat: Adversary (High). Branch `decision/d2-contribution`. Evidence ceiling Rung 2. All
markers synthetic. Probes were inline, read-only; no file written, no git write, repo
unchanged. Reviewed both builds, `plan.md`, both builder charters, governance Articles
7/10/12/14, ADR-0023/0010/0017/0031, and committed `packages/kernel/` +
`packages/derivation/` (runner, marshal, projection, the `runners/derive.py` scenario
adapter). No governance-reviewer output was read.

## Attack 1 — Runs-consume-facts bypass (the crux)

Scenario: I constructed a live `RunContext` **directly** (not via the fixture adapter):
`inputs=[InputFinding('rounding.convention','half_up','GHOST-rounding','input')]`,
`sources=[SourceFact('demo.w2.box1','7770000','GHOST-w2-in-no-record')]`, one committed
wages rule. `run()` **published** `demo.form1040.line1a = 7770000`, its input pins being
`GHOST-rounding` and `GHOST-w2-in-no-record` — finding ids that exist in no act log and no
record. This is the incumbent's Case-6 `777` reproduced at the runner itself, one layer
below `derive.py`.

Root cause: `RunContext.inputs: list[InputFinding]` and `sources: list[SourceFact]` are
**value-bearing slots with caller-supplied `finding_id`** (`runner.py` L49-91). `marshal.py`
marshals only *closure authority* (closure findings + horizons); there is **no committed
marshaller from record state into `inputs`/`sources`**. The only committed constructor of a
run-shaped `RunContext` is the scenario adapter `_context` (`derive.py` L138), which does
`InputFinding(**i)` straight from JSON with zero currency check.

Contract read: the incumbent is **honest** — it closes only the *request* (`run-request.v1`,
paper-only, not committed) and explicitly says "the proposed live marshaller — not that
fixture adapter — must establish that the supplied id is current," naming
adapter-unreachability and a marshal-only entrypoint as production. It never claims the
committed type is closed. The rival **overclaims**: §2.4 wall 2 asserts the context is
"finding-shaped by type … enforced by the shape of the type, not by a check inside it." Probe
result: the *narrow* claim holds (a `raw_inputs=` kwarg is a `TypeError`), but `inputs`/
`sources` are the raw path and accept invented value+id — the type does **not** enforce the
invariant. The rival's own §2.4 last paragraph and §5 concede the soft spot, so its real
position collapses onto the incumbent's; only the wall-2 framing is false.

Verdict: **not decision-blocking** as a contract choice, *conditioned* on the ADR recording,
at MUST level, that (a) `run-request.v1 ≠ RunContext`: closing the request does not close the
evaluator's input type; (b) a marshal-only `RunContext` constructor plus a live-entrypoint
reachability kill-test (direct `derive.py`/hand-assembled `InputFinding` unreachable) is
required; and (c) the rival's "structural by type" claim is struck. The invariant is settled
structurally on the *request* and on the *declaration/edge* side (Attack 2), but is presently
**policy, not structure, at the runtime input** — Gate 6 demands structural. Adopt the
incumbent's framing. Flag, not a kill.

## Attack 2 — Declaration-side leak (rule names a contribution)

Committed derivation edges are walked **only** from pins with role `input`/`choice`
(`projection.py` `_DEPENDENCY_ROLES`). Both designs keep contribution provenance **out of
`pins`** (rival: a plain `finding.v2` field excluded from `pins`; incumbent: a separate
provenance object). A rule's `requires` are symbols over fact types; a contribution is no
symbol and cannot be `ref`/`collect`-ed. No contribution value is reachable through
derivation. **Rejected — not blocking.** Caveat: the E14.2 static check that would reject a
*malformed* rule declaring a contribution dependency does **not** exist committed (grep of
`package_validation.py` finds no kind-vetting); both name it production. Runtime is safe by
construction today; the static guard is deferred.

## Attack 3 — D1 interlock (irreversible)

Drive a synthetic value into a tracked/pushable artifact via a contribution. ADR-0031
Decision 2 is **fail-closed**: missing/unknown/unclassified proof is a deterministic
`NEVER_CROSSES` with no undecided default. So even an unregistered `contribution` /
`contribution-record` kind cannot cross. A live run mounts the repo read-only and writes only
to out-of-repo `L`; both designs add nothing to the commit/push envelope. Probes: scratch
workspaces resolved outside the worktree; `git status` unchanged. No crossing path found.
**Rejected — not blocking.** Caveat: D2 installs no new wall; non-crossing rests entirely on
ADR-0031's production capability wall (Tracks 1/3), correctly consumed not re-proven. The
fail-closed default makes this robust even if the new kinds' sensitivity is never registered.

## Attack 4 — Force an entry order (anti-wizard)

Independent W-2 vs 1099-INT batches: canon orders internally, facts and horizon chains are
disjoint, currency is record-derived — both builds probed equal read-models under opposite
orders. **Rejected.** However: a *correction* contribution B of fact X is admissible only
after the asserting contribution A. Committed `SC-R1` (`findings.py` L216) rejects a plain
assertion of a not-yet-current member, so B-then-A fails while A-then-B succeeds. This is
legitimate **data dependency**, not a UI sequence over independent batches, and matches the
plan's "correction is a *later* contribution." **Not blocking** — but the ADR should scope
"any order" to *independent facts*; it is not unconditional across a fact and its own
correction.

## Attack 5 — Break correction-by-supersession

Attempts: resurrect a stale finding, orphan a dependent, advance the family horizon, or force
an edit. Committed `SC-R2` (`findings.py`) routes same-member corrections to the assertion
path, so the horizon does **not** advance and closure authority survives (ADR-0023 §18.2,
probed; W-2 horizon stayed `-h1`). `marshal.py` marshals **only current** findings, so a
corrected-away closure finding reads as *absent* → the family blocks (fail-safe), never
resurrects. Dependent derived findings displace along committed derivation edges; their
replacement is a re-run (out of scope), not an orphan — the edge stays intact. No
edit/withdrawal mechanism is introduced; history only accumulates (Article 7). Could not
resurrect, orphan, advance the horizon, or force an edit. **Clean bill — not blocking.**

## Verdict at Rung 2

- **D2-P1 survives** as a candidate contract, with **one mandatory, MUST-level production
  condition**: the runs-consume-facts invariant is settled on the closed request and on the
  declaration/edge side, but is **not yet structural at the evaluator's input type** — the
  committed runner published `7770000` pinned to a ghost id (Attack 1). The ADR must mandate a
  marshal-only `RunContext` constructor + entrypoint-unreachability kill-test and must not
  adopt the rival's falsified "structural by type" claim. With that named, no *unclosed*
  decision-blocking hole remains; prefer the incumbent's honest framing.
- **D2-P2 survives** at Rung 2. Any-order (scoped to independent facts) and
  correction-by-supersession are enforced by committed ADR-0023 machinery; no wizard, no
  resurrection, no horizon advance, no hand-edit. No production condition beyond registration.

No decision-blocking bypass. The single reproduced bypass (Attack 1) is the named,
production-fenced fixture/raw-constructor path, not an authorization the ratified contract
grants a live run — provided the RunContext-closure condition is recorded as MUST.
