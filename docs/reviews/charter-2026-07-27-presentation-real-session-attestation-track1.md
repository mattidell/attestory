# Charter — Track 1: session runbook and non-descriptive failure vocabulary

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/real-return/milestones/presentation-real-session-attestation.md`
- Base: `main` @ `ec6972b0490cb73c0d2ee99b24c411cc43d25ec1`. Verify the SHA before starting.

## Context Capsule

- Source ref and resolved launch commit: `main` @ `ec6972b0490cb73c0d2ee99b24c411cc43d25ec1`
- Exact object or commit range: new file `docs/runbooks/presentation-real-session.md`; any bounded scriptability repair in `packages/derivation/live_session.py` and its test module
- Role: Builder
- Scope and evidence-rung ceiling: documentation artifact plus an optional, justified, minimal code change. No new capability, no new surface, no boundary mechanism.
- Stop conditions: any need to touch `tools/presentation_harness/lib/server.mjs` or either evaluation manifest; any need to observe machine configuration; any need for a real workspace; any need to widen the vocabulary to express a value or disposition
- Full reads before acting: this charter; the milestone plan; `docs/adr/0047-live-viewing-environment.md`; `docs/adr/0031-real-data-residency-boundary.md`; `packages/derivation/live_session.py`; `docs/reviews/2026-07-27-presentation-live-session-path-track3-rehearsal.md`; `AGENTS.md` ("Data Safety Rules")

## Goal

Produce the two artifacts the owner's session sitting needs, in one file:
`docs/runbooks/presentation-real-session.md`.

A new `docs/runbooks/` directory is correct here because this artifact
**outlives the milestone** — every future real viewing session uses it. Do not
file it under the milestone. Keep both artifacts in one file: the owner reads
them in a single sitting and two files would drift.

## Artifact 1 — the session runbook

The exact sequence for one sitting, written for the owner to follow start to
finish without improvising. It must cover:

1. **The three preflight answers** — what each one is, and that each comes from
   the owner's own trust domain. Make unmistakable that the project observes
   nothing about the machine: `PreflightProbes` is an injected input, by
   ratified design (ADR-0047 amendment 1), not an unimplemented feature.
2. **Pointing the capability at the real residency** without the locator
   entering any recorded surface. See the open question below — this is the one
   part of the runbook you must not answer silently.
3. **Running the session**, and what each refusal reason code means if one
   comes back. Reason codes are stable and path-free by ADR-0047's locator
   confinement decision; the runbook must not teach the owner to go looking for
   a path in a message that deliberately lacks one.
4. **Obligations during the session** — ADR-0047 preconditions 3 and 4, which
   are owner knowledge rather than mechanism. State the clipboard rule where the
   owner will read it *before* looking, not in a footnote: **no copy at all
   while clipboard-history retention is in force**, because a retained copy
   leaves the residency with no subsequent paste. Also no paste outside the
   residency, no print to a networked or external destination, no retained
   screenshot.
5. **Teardown**, and how to confirm it completed.

## Artifact 2 — the non-descriptive failure vocabulary

The bounded set of statements the owner may make about a session that failed.

This exists because ADR-0047 precondition 5 forbids values, identifiers,
dispositions, and screenshots from chat, reviews, PRs, and the repository — so
**a defect seen during the real session is, by default, unactionable.** The
vocabulary is the only legal channel from a failed real session back to a
repair. Treat it as a data-safety artifact, not as documentation.

The governing line is **mechanical, never evaluative**:

- Legal: "the page did not load", "a section failed to render", "a citation
  link resolved to nothing", "the browser exited before I could look",
  "teardown did not complete", "a refusal came back with reason code X".
- Illegal: anything naming a value, an identifier, a disposition, a count that
  implies one, a comparison against an expectation, or a judgement that
  something was wrong rather than absent.

The boundary is genuinely hard in places — "a section rendered empty" is
mechanical, while "a section rendered empty that should not have" is a
disposition claim wearing mechanical clothes. Draw that line explicitly and give
the owner the reasoning, not just the list, so the vocabulary degrades safely
when a real failure does not match any entry. State what the owner should do
when nothing in the vocabulary fits: report that fact itself, which is legal,
rather than improvising a description.

## Open question you must answer with a recommendation, not a silent choice

The runbook tells the owner how to point the capability at the real residency.
The obvious form — typing the path as an argument — puts the locator in shell
history and in the process table, the latter readable by exactly the
Developer/Supply domain ADR-0044 says is not separated. This is the same hazard
that killed the `tmutil isexcluded` probe in the previous milestone.

Evaluate whether the runbook should instead direct the owner to supply the
locator by a means that avoids both — for example reading it from a file the
runbook never echoes, or an environment variable set outside history expansion —
and whether any of those actually close the hazard or merely move it.

**Recommend, with reasoning, including the option of accepting the exposure as a
named residual.** Do not implement a mechanism for this without saying so
plainly in your hand-off; if the honest answer is that all available options are
imperfect, say that, as the previous milestone did when it chose not to build
the probe.

## Bounded scriptability repair

In scope only if the sitting is materially harder without it. If
`open_presentation_session` already runs as one call, write the runbook and
change no code. Any change must be minimal and justified by the sitting itself,
not by general tidiness.

## Hard constraints

- **No confinement code, sandbox profile, wrapper, `sandbox-exec` invocation, or
  probe implementation.** Class C confinement and Class D precondition
  observation are owner-held outside the supply chain. `PreflightProbes` stays
  an injected input.
- **`tools/presentation_harness/lib/server.mjs` and both evaluation manifests
  are byte-unchanged.** If a clean implementation appears to require touching
  them, stop and report.
- **No real workspace.** Synthetic inputs and temporary workspaces only. You are
  not performing or rehearsing a session; that is Tracks 2 and 3, and both are
  owner-operated.
- **No headed browser launch.** No agent launches a headed process in this
  milestone.
- **No locator, path fragment, canonicalized form, derived identifier, or
  absolute local path** in any file, commit message, or hand-off.
- **No new presentation surfaces**, tax rules, form fields, citations,
  schedules, domains, published schemas, or citizens.

## Verification

```text
python3 -m unittest tests.test_presentation_live_session
python3 -m unittest tests.test_presentation_live_viewing_vehicle
python3 -m unittest tests.test_presentation_l2_integration
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk-production-shaped.v1.json
python3 tools/envelope_scan.py --range main..HEAD
git diff --check
```

Both evaluation manifests are an unchanged regression floor. If you changed no
code, run them anyway — a docs-only track that skips verification cannot prove
it changed no behavior.

## Hand-off

Report: what the runbook covers, your recommendation and reasoning on the
locator-supply question, whether you changed any code and why, and anything the
vocabulary could not cleanly express. Name what you are unsure of rather than
resolving it silently — the review gate for this track is adversarial, and a
reviewer will attempt to smuggle a disposition through the vocabulary.
