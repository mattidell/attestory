# Review — Packaging the Surface, Track 2: the ADR

- Reviewer: independent, author-independent review per `docs/roles/reviewer.md`
- Object: `docs/adr/0049-surface-artifact.md` and its `docs/adr/INDEX.md` row,
  diff `d730752..8d8ef76` (branch `milestone/packaging-the-surface`)
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-28-packaging-the-surface-track2.md`
- Verdict: **READY**

## Orientation note

`python3 tools/build_orientation_block.py --ref main --role reviewer` errors
with a topic mismatch (`docs/phase-state.md` on `main` still names
`real-return-phase-close`, from `main`'s HEAD at `b686e9c`, PR #99). `main` has
not merged Legible Entry or this milestone; this branch is many commits ahead
of `main` and carries its own current `docs/phase-state.md` naming this exact
Track 2 charter. The mismatch is a pre-existing property of `main` lagging
open work, not a mismatch in the review object itself — the branch, commit
(`8d8ef76`, verified against `git rev-parse HEAD`), charter path, and diff
range given in the dispatch all agree with what's on disk. Reported per the
role file's instruction to surface a stale pointer rather than silently work
around it; it did not block this review because the object was named
explicitly and independently confirmed against Git.

## What I checked

- Read `packages/derivation/surface_resolver.py`,
  `packages/schemas/derivation/surface-artifact.v1.schema.json`,
  `packages/sample_data/surface_t1/manifest/surface-artifact.entry-page.v1.json`,
  and `tests/test_surface_t1_build_and_open.py` directly, not the ADR's account
  of them.
- Re-ran the determinism check independently rather than trusting the ADR's
  self-report of it: copied `packages/sample_data/surface_t1/content/app` to
  two fresh directories, ran `node build.mjs` in each (Node v25.8.0, this
  machine), diffed the two `dist/` trees. Byte-identical, confirming the
  ADR's claim as stated and at the width stated.
- Ran the CI `verify` quartet directly: `pytest -n auto` (687 passed, includes
  all three of `tests/test_surface_t1_build_and_open.py`'s tests — Node,
  `sandbox-exec`, and Chrome are all present on this machine, and they ran
  and passed, not skipped), `python -m mypy` (clean, 131 files), 
  `python tools/governance_lint.py` (conformant), `python
  tools/envelope_scan.py --range d730752..HEAD` (no findings).
- Diffed `bb751ba..0fd05e7` (Track 1's actual commit range) against
  `production_resolver.py` to confirm the ADR's claim that the only change
  there is the additive `expected_kind` parameter — confirmed, that is the
  entire diff to that file.
- Independently recomputed the measured cost from the manifest JSON rather
  than trusting the prose: `sum(e['bytes'] for e in entries)` over
  `surface-artifact.entry-page.v1.json` gives exactly 941 entries,
  5,065,001 bytes, matching both the ADR body and the INDEX row exactly.
- Confirmed the symlink-following claim (`node_modules/.bin/acorn ->
  ../acorn/bin/acorn`) is a real entry in the fixture tree, not a
  hypothetical.
- Read `docs/adr/0047-live-viewing-environment.md`'s Class D section in full
  to check the ADR's characterization of it (a total classification of
  session-leakage channels) against the source text — accurate; Class D
  enumerates backup, indexing, clipboard-history, sync, and screen-capture,
  all session-time observation questions, nothing about build-time
  toolchain presence.
- Confirmed `production_resolver.py` itself uses `package_instance_checksum`
  / `verify_published_package` for its own package instances, so the ADR's
  "the same primitive `artifact-package.v4` instances are verified by" claim
  is literally true, not just analogous.
- Confirmed the INDEX.md row is well-formed, matches the table's existing
  convention, and its claims (byte counts, the "checked, not assumed"
  framing, the Class D rejection) match the ADR body — it isn't a shorter,
  looser paraphrase that drifts from the document it summarizes.

## The charter's central question: does it decide, or describe?

**Open question 1 (what the build's output rests on) — decided, and decided
correctly.** This is the section that matters most and it's the strongest
part of the document. It states the trust chain precisely ("verified inputs,
plus a command whose own text is itself verified, executed once by whatever
Node is on the machine"), states plainly what that does and does not
establish (provenance, not content identity — "reused" analogy is drawn
correctly, since ADR-0033's existing guarantee is extended to "what produced
this" rather than duplicated), and lands on an explicit, checkable
conclusion: not sufficient, and here is exactly what would make it
sufficient (a pure-function build with no wall-clock/random/locale/hostname
dependence, checked across machines and Node versions, not just this one).
It doesn't paper over the gap with "plausible" reasoning about the compiler
— it says so, and names that it used to do exactly that (the self-reported
revision from a "reading of `build.mjs` and `svelte/compiler`" to a measured
check). That correction is real: I reran the check myself and got the same
byte-identical result. The document does not ask me to take its word for
either the before or the after.

**Open question 2 (Node as a precondition) — decided.** It explicitly
declines to file this under ADR-0047 Class D, gives the actual reason (Class
D is a total classification of session-leakage channels; Node's absence is a
build-time functional precondition, not a leakage channel), and names a new
category rather than either stretching an existing one to fit or leaving the
question unplaced. I checked Class D's text directly — the characterization
holds. It also correctly identifies that the Node-version risk and the
build-output-verification gap are the same open question seen from two
angles, which is a real observation, not restatement dressed up as one: a
cross-machine byte-identity check is definitionally a check across whatever
Node versions those machines run.

**Open question 3 (why the rule package was left alone) — decided.** States
the alternative that was rejected (an opaque-member role added to
`artifact-package.v4`), states the cost of the alternative in one clear
sentence ("everything validates except the parts that don't, permanently, to
save building one resolver once"), and gives the future reader the exact
argument to counter before proposing a merge. I confirmed against Track 1's
actual diff (`bb751ba..0fd05e7`) that the named files
(`package_validation.py`, `loader.py`, `schema_registry.py`,
`artifact-package.v4.schema.json`) are untouched and that
`production_resolver.py`'s only change is the additive parameter — the
"not touched in substance" claim is not an assertion, it's demonstrated by
the diff the ADR points at, and I re-verified that diff myself rather than
trusting the pointer.

All three are decisions with reasoning that survives being checked, not
descriptions of the questions dressed as answers. This is exactly the
failure mode the charter existed to prevent, and it doesn't happen here.

## Determinism claim: stated at its real width

Confirmed independently, twice (once by rerunning the exact procedure
described, once by re-reading the surrounding prose for scope creep). The
document is careful in a way that's checkable, not just asserted: it names
what two same-machine runs actually rule out (timestamps, ordering,
per-run identifiers) versus what they don't touch (cross-machine,
cross-Node-version, cross-platform, over time), and repeats that boundary
in three separate places (the body, the Consequences section, and the
Evidence Limits section) without ever letting the wider claim slip through
unqualified. I found no sentence in the document that states or implies
"the build is deterministic" as a general fact. The Evidence Limits section
in particular is precise to the point of redundancy with the body — that's
a minor cost in length (see below) but not a correctness problem.

## Conclusion survives its own evidence

Yes. "Verified inputs plus one fixed command is not sufficient to claim the
served bytes are reviewed bytes" is exactly what the evidence supports: the
digest chain covers every input and the command text itself, and nothing
digests the output, so a non-deterministic build (on this same machine, in
principle, though the check argues against the common causes) could pass
every check in the chain while serving different bytes. The document doesn't
overstate this into "the build might be compromised" (unsupported, alarmist)
or understate it into "this is basically fine because we checked determinism
once" (the exact conflation the charter warned about). It sits at the width
the evidence earns.

## Accuracy against the code

Checked directly, not accepted from the document's prose:

- `surface_resolver.py`: `resolve_surface_artifact`'s shape, the
  `expected_kind` reuse of `select_current_adoption`, the
  `package_instance_checksum`/`verify_published_package` verification of the
  manifest as a published instance, the flat `{path, sha256, bytes}` entry
  checking, and the `_within` symlink-confinement logic (a target resolving
  outside the root refused, one resolving back inside followed) all match
  the code exactly as described.
- `surface-artifact.v1.schema.json`: shapes only the manifest (`schema`,
  `id`, `version`, `build_command`, `entrypoint_html`, `entries`,
  `package_checksum`), each entry constrained to `{path, sha256, bytes}`
  with a path pattern excluding absolute and parent-relative paths — matches
  the ADR's description exactly, including "the manifest itself is the only
  thing this schema shapes."
- The adoption route (`surface-adoption` kind, `_well_formed_adoption`'s
  `expected_kind` parameter, unchanged `act-package-adoption.v1` payload):
  confirmed against the diff.
- The measured cost (941 / 5,065,001): recomputed independently from the
  manifest and matches exactly, not approximately.

No misdescription found anywhere I checked.

## Weak points carried forward

All three named in the charter are present, in the document's own words, not
softened: the macOS-only, CI-uncovered offline enforcement; the three
underscore-private imports from `production_resolver.py` with an honest
statement of the failure mode if they drift; and the untested TypeScript
toolchain cost. None of these evaporated or got quietly reworded into
something weaker than the original finding. The "untested minority refusal
paths" item is new content beyond what the charter named, but it's accurate
(I did not independently exercise those five refusal codes, since the
charter didn't ask for that and Track 1's review already covers the pattern)
and it's honestly scoped ("not a new gap" — matches an existing pattern in
`production_resolver.py`).

## Length and register

357 lines against 522 (ADR-0047) and 581 (ADR-0048), the two named
analogues — real, substantial compression given this ADR also had to decide
three open questions the analogues didn't carry. I don't think it has
drifted into the defensive, over-qualified register the project is moving
away from: the hedging that exists is concentrated exactly where the
substance requires it (the provenance/reproducibility distinction, stated
carefully because getting it wrong in either direction was the actual risk
named in the charter), and the rest of the document — the container shape,
the adoption route, the alternatives, the weak points, the cost — is stated
plainly without qualification. The one place I'd call a genuine, if minor,
cost: the same-machine/cross-machine boundary is restated close to verbatim
in three places (the body's "what it does not touch," the Consequences
section, and Evidence Limits). That's not wrong, and I'd rather see it
over-restated than have it slip once, but a tighter document could have said
it once with force and referred back to it rather than restating it in full
each time. Not a blocking finding.

## What I could not check

- Cross-machine or cross-Node-version determinism — the ADR itself is
  explicit that this wasn't checked and names it as future work; I have one
  machine and one Node version available, so I could not extend the check
  further than the ADR already does. This is not a gap in the ADR; it's an
  honestly named limit of the evidence, and I confirmed the document does
  not claim more than it checked.
- Anything about the builder's own account of its revision history (the
  self-reported error, the foreman's earlier determinism run) — per role
  posture I did not seek that out and treated only the committed artifact
  and my own reruns as evidence.

## Verdict

**READY.** The ADR decides what the charter required it to decide, at the
width the evidence supports, and every specific factual claim I checked
against the code, the schema, the fixture manifest, and a live rerun of the
determinism experiment held up exactly as stated. The carried weak points
are present and unweakened. Length is a minor, non-blocking observation, not
a defect.
