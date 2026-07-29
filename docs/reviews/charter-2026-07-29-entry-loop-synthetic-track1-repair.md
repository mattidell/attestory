# Charter — The Entry Loop (synthetic), Track 1 repair: F2–F3

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Repairing: `2a00193`
- Against: `docs/reviews/2026-07-29-entry-loop-synthetic-track1-review.md` (`NOT READY`, F1 blocking; F2, F3 weakening)
- F1 is out of scope: the rule it enforced was withdrawn (see below)

## Where the track stands

The loop, the Phase A evidence, the contribution admission path, the surface
artifact route, and the data boundary all came back sound. The reviewer mutated
each of the four dependency tests and confirmed every one fails when the thing
it guards is broken. That is the milestone's central risk, and it held.

Three findings were raised. The blocking one is no longer yours to close; two
gaps in durable coverage are.

## F1 — withdrawn, do not work on it

F1 said the build had not closed, or recorded as open, ADR-0048's requirement
that an entry surface launch with spellcheck's network path affirmatively
closed by a vehicle-level flag. That was a correct reading of the rule in force
at the time.

The owner has since withdrawn the rule. **ADR-0050** supersedes ADR-0048's
entry-vehicle requirements: browser and workstation behaviour are the owner's
trusted environment, not the entry surface's contract. The surface owes
contribution-only entry, validated admission that fails closed, redacted
failure, data-boundary behaviour, and no false claim of isolation — which is
what F2 and F3 are about. ADR-0048's contribution boundary is untouched.

So: no vehicle, no launch flag, no preflight, no spellcheck probe, and no
nonclaim paragraph. Do not rewrite the existing review; it stands as correct
under its own premise, and the reviewer disposes it on recheck.

One small thing does carry over. The `spellcheck="false"` attribute may stay,
but if anything in the source or its comments presents it as a security
control, correct that wording. ADR-0050 forbids presenting a browser setting as
a protection the product does not provide. If nothing does, say so and change
nothing.

## F2 — adversarial coverage for the new typed-input boundary

The suite tests one malformed W-2 amount. The reviewer manually exercised wrong
content type, oversized body, malformed JSON, JSON type confusion, template
tampering, duplicate submission, and out-of-order submission against the
endpoint, and **all of them already fail closed** with redacted responses and no
log advance. So this is not a behaviour fix — it is that none of it is
protected against regression.

Add committed regressions for each class the reviewer exercised. This is the
project's first endpoint that turns typed input into a durable act; the standing
discipline is that known adversarial classes arrive as executable coverage
rather than as a reviewer's one-time observation.

If any class does not in fact fail closed when you test it, that is a new
finding — report it, and say so plainly rather than quietly fixing behaviour
under a coverage charter.

## F3 — exercise the compiled client against the API

The endpoint tests use a placeholder HTML file, and the artifact tests check
built-output markers. Nothing runs the compiled page's own relative `./api/*`
requests against the running server. Source inspection says they are served from
the same capability URL, but that is inference.

Close the gap with a test that drives the real built client against the real
endpoint. Track 2 opens this page for the evaluation; this is the integration
most likely to break at exactly that moment.

This is not usability scoring. Do not score the criteria.

## Boundaries

- F2 and F3 only, plus the one wording check under F1. If you find something
  else, report it.
- No preflight extension, no launch vehicle, no confinement code. ADR-0050
  removed the obligation; do not reintroduce it voluntarily.
- No new criteria, no per-field explanation schema, no matrix movement.
- W-2 only, synthetic only, no residency locator in any surface including new
  test names.
- Do not change the four dependency tests. They passed mutation testing; leave
  them alone.

## Verification

The CI `verify` sequence or a stated subset with each omission justified, the
data-safety scan, and the commit you worked from, in the commit message. The
prior commits on this branch set the standard.

Orient with `python3 tools/build_orientation_block.py --ref HEAD`. No `.venv`;
use system `python3`. Ratified line `origin/main-ui`, derived for you; the merged
PR #109 is the milestone's opening plan PR.

## Report back

Whether any source or comment presented `spellcheck="false"` as a security
control, and what you did about it; which adversarial classes you
covered and whether each still failed closed when you tested it; how the F3 test
drives the real client; and anything you noticed but did not touch.
