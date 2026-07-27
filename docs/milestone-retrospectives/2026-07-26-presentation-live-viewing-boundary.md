# Retrospective — Presentation Live Viewing Boundary and Invocation Vehicle

- Merged: PR #88 (plan), PR #89 (Track 1, ADR-0047), PR #90 (Track 2, vehicle)

## What differed from the plan

The milestone's first act was to reject its own obvious shape, before any code
existed. The owner selected the Presentation frontier with a headed viewing
target, which reads as a straightforward instruction to build a contained
browser launcher. It isn't. Chrome's `--disable-background-networking`,
`--disable-sync`, and `--user-data-dir` are cooperative settings inside a
process running under the owner's own authority, and ADR-0044 already settles
that case: naming directories or wrapping commands does not create a trust
boundary. A track chartered to prove otherwise would have built something and
then failed on inspection — the exact shape of the Guarded Transport failure,
where a mode-600 credential store was defeated by a same-UID process.

The owner named that risk explicitly at planning time rather than after. The
plan was reshaped to define the viewing environment first and build second.

The reshaping also surfaced the narrower truth underneath. Mechanical authority
separation is the **L4** gate, not the L3 one. Presentation L3 rests on the same
bar W-2, Interest, and Dividends already cleared with an ordinary Python
process: synthetic battery plus the owner's non-descriptive attestation under an
accidental-leakage posture. So the real question was never containment. It was
**what the owner would be attesting to** for a surface whose purpose is putting
live data in front of a person — a channel ADR-0044 defines domains for
processes and never contemplated.

## What it cost

Two decision-review cycles on Track 1, one build with one findings-only repair
on Track 2, and one records track. Both repairs were applied by the Foreman
directly rather than by a Builder round, on the owner's standing instruction to
fix rather than charter when the fix is small; both were text- or test-only.

The one cap exception the owner authorized was a single-line cross-reference fix
on Track 1's second recheck.

## What the reviews caught

Both findings were claim-discipline errors, and they ran in opposite directions.

**Track 1 — an overclaim in the negative.** I asserted as settled fact that
macOS offers no unprivileged per-process network confinement. Seatbelt
(`sandbox-exec`) is base-system, requires no root, and had simply never been
evaluated here. Claiming something is impossible is still a claim, and this one
had no evidence behind it. Worse, an unexamined impossibility forecloses a
design direction permanently and silently. The correction propagated to the ADR,
its analysis, the ADR index, and the plan's own prose, which had inherited the
same error.

**Track 2 — a missing guard where the caveat looks like dead weight.** The
clipboard-history split disposition was implemented correctly: when a viewing
session is allowed, an owner-responsibility code attaches whether the probe
confirmed absence or couldn't decide, because an enumerable manager scan rules
out only the managers it knows. But the only test covering that branch used the
undecidable and detected inputs. The confirmed-absent case — the one that looks
like good news — had no coverage. A later "simplification" gating the code on
`clipboard is not ABSENT` would have read as correct, passed every test, and
silently reintroduced the completeness claim ADR-0047 was repaired twice to
forbid. The repair added the guard and verified it fails under exactly that
mutation; the Reviewer reproduced the mutation independently rather than
accepting the report.

## What was built

A confined headed invocation vehicle whose profile, cache, downloads, and print
destinations are constructed inside the live workspace from runtime capability
state alone — no `tmpdir()`, no environment fallback, no caller-supplied path —
canonicalized, re-checked after creation to close the mkdir race, and refusing
any pre-existing symlink. Plus a fail-closed preflight where an unreadable,
unknown, or indeterminate probe is a refusal, never a pass.

One design constraint is worth carrying forward: **a knowledge constraint became
an API constraint.** Because the residency locator may not reach chat, a log, or
a PR, the ordinary affordance of a path-confinement check — reporting the
offending path — was unavailable. The fix was not redaction after the fact but
designing the return type so the path never enters a diagnostic. Reason codes
only, enforced by test rather than convention.

## Follow-ups

- **Evaluate Seatbelt (`sandbox-exec`) as a Class C enforcement substrate.**
  Unevaluated, not foreclosed. This belongs to ADR-0044's future implementation
  gate and a data-boundary L4 claim, not to Presentation. Reactivate when the
  owner selects hardening.
- **Presentation L2 → L3** now needs only real operation and the owner's
  non-descriptive attestation under ADR-0047's five honesty preconditions. The
  vehicle gap is closed. This is an owner act, not a build.
- **Phase-state pointer hand-off** drifted three times in this milestone across
  two distinct mechanisms: a Foreman filing a charter without advancing the
  pointer, and a Reviewer resetting `current_role` to `"Foreman"` on hand-back —
  a value `tools/build_orientation_block.py` rejects outright. Addressed in the
  role documentation this milestone.

## What should change in the next plan

When the owner names a target that implies a mechanism, check whether the
mechanism can hold **before** chartering a track to build it, and check it
against the accepted boundary ADRs rather than from scratch. ADR-0044 already
contained the answer here; the work was reading it, not deriving it. That check
cost one planning exchange and saved a build-then-discard cycle.

Second: when a milestone ships working code without lifting a maturity level,
say so in the records loudly and early. The close-out is where "we built the
thing" quietly becomes "we reached the level," and the two are not the same.
