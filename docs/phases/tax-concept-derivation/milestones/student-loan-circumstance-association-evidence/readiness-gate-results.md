# Readiness gate results

Executed evidence for the two checks named in
[the charter](charter-readiness-gate-checks.md) and in
[outline section 9](outline-product-and-evidence.md#9-the-smallest-evidence-that-would-settle-this).
Test module:
[`tests/test_sli_circumstance_association_readiness.py`](../../../../../tests/test_sli_circumstance_association_readiness.py).
Both checks ran against
`packages/derivation/pairing_dispatch.py`'s adopted generic primitive; no
production file was modified.

This document is evidence, not a design. It selects no representation and
adopts nothing. The circumstance shape used in check 1 — one finding whose
value is an object with named properties, read with ADR-0067's `field`
selector — is provisional (outline U1), used only because check 1 needs *a*
shape to run.

## Check 1 — dereference

Disposable pairing: left = a synthetic Form 1098-E box-1 source
(`demo.tax.f1098e.box1-student-loan-interest`, identity keys `lender` +
`statement` + `tax-year`, mirroring the real box-1 fact type's own keys and
value shape — a bare nonnegative number), right = a synthetic
schooling-circumstance source (`demo.tax.schooling-circumstance`) whose value
is `{"qualified_fraction": <number>}`. One declared rule expression —
`multiply(ref(box1), ref(circumstance, field=qualified_fraction))` — dispatched
pairing-scoped through `evaluate_pairing_scoped_rule`, against a disposable
pairing-local `Environment` rebuilt in the test module (two symbols, empty
sources, empty closed sets — the shape
`packages/tax/pairing_consequences.py::_pairing_local_environment` is
documented to build, not imported from it).

**Observation 1 — the value read.** The publication's value depends on both
sides. With `qualified_fraction = 1.0` the published value is `"2000.00"`
(the full left-side box-1 amount); with `qualified_fraction = 0.5` it is
`"1000.00"`. Changing only the right side's named property changes the
published value. The primitive genuinely carries a relationship between a
report amount and a named property of an associated circumstance, not merely
a pass-through of one side.

**Observation 2 — the pins.** The publication pins the exact finding ids
`f.pairing` (the pairing finding), `f.box1` (the left/box-1 finding), and
`f.circumstance` (the right/circumstance finding) — asserted by id, not by
count.

**Observation 3 — loss of the target.** With the circumstance source absent,
the same dispatch yields exactly one blocked row with code
`DEPENDENCY_ABSENT`, whose `missing` names the circumstance's own fact id.
This disposition **comes for free**: it is produced by
`evaluate_pairing_scoped_rule`'s own left/right resolution before
`evaluate_one` is ever invoked (proved in the test by an `evaluate_one` that
raises if called). No rule-author effort is required to get "a surviving
reference is not sufficient support" — the generic primitive already refuses
to publish when the named side cannot be resolved.

**Observation 4 — the prior consumer cannot enter this scope.** Two
expressions were dispatched pairing-scoped in the disposable environment:
`require_closed` on a source-set name, and `count` on the same. Both blocked.
**The code observed for both is `SOURCE_SET_UNCLOSED`, not `DEPENDENCY_ABSENT`
or any other code.** This falls directly out of the environment shape: the
pairing-local environment's `closed_sets` is the empty frozenset, and both
`require_closed` and `count` gate on `source_set in env.closed_sets` before
they read anything else in `env.sources`. The prior milestone's candidate
rule (`require_closed` + `count(box1) == 1`) cannot be evaluated as written
inside pairing scope; it must be restructured, exactly as outline section
6(a) states from a `read`-level reading of the source. This check confirms it
by execution.

## Check 2 — omission

**Expected disposition, recorded before execution:** two Form 1098-E box-1
statements at distinct identities (`S-1`, `S-2`) in one run; `S-1` paired to
one schooling circumstance, `S-2` unassociated. One publication for `S-1`'s
pairing. For `S-2`: no row of any kind — neither a publication nor a blocked
row.

**Observation 5 — exactly one publication, and it is the associated one.**
`result.publications` has length 1; its pins include `f.box1.associated` and
`f.pairing`, and do not include `f.box1.unassociated`.

**Observation 6 — no blocked row names the unassociated statement.**
`result.blocked` is the empty tuple. (Stronger than "no blocked row names
`S-2`'s fact id": there is no blocked row at all, because the dispatcher
iterates *pairing* findings — `S-2` is never a pairing's named side, so it is
never visited in either direction.)

**Observation 7 — the unassociated statement's source is genuinely
present.** Before dispatch, the test asserts two `demo.tax.f1098e...` sources
exist in `ctx.sources` and that `S-2`'s fact id is one of them. The silence
observed is the dispatcher's iteration behaviour, not a missing fixture.

**The observation matched the recorded expectation exactly.** No blocked row
appeared for the unassociated statement; there is nothing to escalate as a
material finding. This confirms outline section 6(b): the dispatcher's
iteration source (`[s for s in sources if s.name == pairing_type]`) is
silent about any statement with no pairing finding, which is failure 4
("invisible omission") from outline section 4, executed rather than read.
U2 (what accounts for a statement with no relationship) remains open and
unresolved by this check — the check only confirms that nothing today closes
it, which is the gate outline section 10 asks for.

## What this raises from `read` to `run`, and what it does not

**Raised to `run`:**
- Outline section 5/6(a): the adopted per-pairing primitive can carry a
  report/circumstance relationship, genuinely dependent on both sides
  (check 1, observations 1–2).
- Outline section 6(a)'s specific claim that the prior milestone's rule
  cannot be lifted into pairing scope because `require_closed`/`count` fail
  there: confirmed by execution, with the exact code (`SOURCE_SET_UNCLOSED`)
  recorded (check 1, observation 4).
- The "surviving reference is not sufficient support" behaviour
  (`DEPENDENCY_ABSENT` naming the lost side) is confirmed to already exist in
  the adopted primitive with no additional rule-author work (check 1,
  observation 3).
- Outline section 6(b): a statement with no relationship produces neither a
  publication nor a blocked row — U2 is confirmed to be a live, unclosed gap
  rather than a suspicion (check 2, observations 5–7).

**Not raised, and explicitly out of scope for these checks:**
- **U1 is not settled.** Check 1 shows a structured circumstance value *can*
  be read pairing-scoped; it does not show that one structured finding is the
  right correction granularity for a person to revise, or what the person
  should be asked. That is an owner decision (outline section 7, U1).
- **U2 is not designed, only observed.** This document names the gap and
  confirms it is silent today. It proposes no completeness mechanism, no
  closed-family rule, no refusal-carrying record — any of outline section
  7's U2 options remains open.
- **No representation is adopted.** The synthetic fact types, the
  `qualified_fraction` property, and the pairing-local `Environment`
  reconstruction used here are disposable test fixtures, not a proposal.
  Nothing in the production package changed.
- **No tax conclusion.** Neither check establishes eligibility, a favorable
  or unfavorable determination, or that a production consumer route exists.
  Check 1's arithmetic (`multiply`) is illustrative dependence-proving only,
  not a claim about how a deduction should actually be computed.
- **U3 and U4 are untouched.** Neither check exercises a borrowing entity, a
  multi-statement/multi-period case, or the generalise-vs-sibling question
  for `pairing_consequences`'s hardcoded environment. The pairing type,
  identities, and cardinality used here are the simplest single-pairing case
  in each direction.
- **No claim about production `pairing_consequences.py`.** That file was
  read only, per the charter's boundary, and is unmodified. The disposable
  environment built in the test module is a re-derivation of its documented
  shape for the purpose of exercising the generic primitive, not evidence
  about that module's own behaviour or any generalisation of it (U4 remains
  open).

## Verification

- `git diff --check` — clean.
- `python3 tools/governance_lint.py` — passed.
- `python3 tools/envelope_scan.py --staged` — passed.
- `python3 -m mypy` (repo-wide) — passed, no issues.
- `python3 -m pytest -n auto` (repo-wide) — all tests passed, including the
  six new in `tests/test_sli_circumstance_association_readiness.py`.
