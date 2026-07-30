# Charter — Entry Boundary, Track 1: the retention probe

- Role: **Builder** (`docs/roles/builder.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-boundary.md`
- Branch: `milestone/entry-boundary` (base `main-ui` at `8d41cc2`)
- Evidence ceiling: **observation on synthetic fixtures only.** No claim about
  real data, no claim about what any browser does in general — only what this
  vehicle, on this machine, did in this run.

## What this is for

The next milestone decides whether a browser form is an acceptable place for a
person to type real tax facts. That decision should rest on what a browser
actually does with typed text, not on what we assume it does.

Browsers are built to be helpful about typed text. They can remember form
entries for autofill, keep drafts so a crash doesn't lose work, hold undo
history, send text to a spellcheck service, and learn from dictation. Any of
those could leave a wage figure or an SSN somewhere the product never looks.

Your job is to find out which of them fire, and where the text ends up. You are
not building a form for people to use. You are building a throwaway instrument
that answers a question, then writing down the answer.

## Deliverables

**1. A probe.** Under `tools/entry_probe/`, with a README that says in its first
line that this is a throwaway instrument, not product code. It:

- Launches a browser through the **existing confined invocation vehicle**
  (`tools/presentation_harness/lib/chrome.mjs` and its server), so what you
  observe is the confinement the product actually uses, not a default browser.
- Serves a minimal HTML page with a few text inputs — enough to look like a tax
  form field to the browser's heuristics. Give the inputs realistic `name`,
  `id`, `type`, and `autocomplete` attributes, because autofill and form history
  key off exactly those. A field named `q` will not be treated the way a field
  named `ssn` is.
- Types distinctive synthetic values into them, submits or navigates where that
  is what triggers a channel, and closes the browser.
- Then searches the browser profile directory, and anywhere else the vehicle
  writes, for those values.

**2. A findings note** at
`docs/phases/legible-entry/milestones/entry-boundary-retention-findings.md`.
One row or short section per channel, each stating: did it fire, where exactly
did the text end up (file path relative to the profile, and what kind of store),
and does the existing confinement already contain it — meaning the location is
inside the disposable profile and goes away with it, or it is not.

## Channels to cover

Cover at least these. Add any you discover; say so if one cannot be tested and
why.

1. **Form history / autofill** — does the browser save submitted field values
   for later suggestion, and where.
2. **Session restore and crash recovery** — does an unclean exit leave typed
   text in a recovery store. Test the unclean case deliberately; a clean close
   may say nothing about it.
3. **Undo buffer persistence** — does typed text survive anywhere after the
   field is cleared or the page is navigated away from.
4. **Spellcheck** — is it local or does it contact a service. If a service, that
   is a network egress of typed content and the most serious possible finding.
5. **Anything the browser writes on its own** — logs, crash dumps, metrics,
   prefetch, IndexedDB, LocalStorage created by the page or the browser.

For each, the useful answer is a file path and its contents, not a yes.

## Method notes

- Pick synthetic values that are trivially greppable and obviously fake:
  distinctive tokens that cannot collide with anything else on disk, and that a
  reader will never mistake for real data. Do not use anything resembling a real
  SSN, EIN, or account number, including a plausible-looking fake.
- Search the profile with a recursive binary-safe grep. Some of these stores are
  SQLite or LevelDB; the token may be findable as raw bytes even when the file
  is not text. If you find it in a binary store, say which store.
- Run the probe. Report what happened. If a channel does not fire, that is a
  real and useful finding — record it as observed-not-fired, not as absent.

## Boundaries

- **Synthetic only.** No real workspace, no real residency path, no real fact.
- **No residency locator** — not in the probe, the findings note, a commit
  message, or any output. Not a real path, not a fragment of one, not a derived
  identifier.
- **Do not wire the probe into CI**, the verify sequence, or any existing test
  suite. It is run by hand.
- **Do not touch** the presentation harness itself, any product code under
  `packages/`, any schema, fixture, or golden. If the confined vehicle cannot be
  driven without modifying it, that is a **charter-stop finding** — report it,
  do not change it.
- **Do not decide anything.** You are not writing the ADR, not recommending a
  write path, not stating whether a browser form is acceptable. Track 2 does
  that, and it should be able to reach a different conclusion than the one your
  findings seem to suggest. Report observations; leave the judgment alone.

## Stop conditions

Stop and report rather than proceeding if:

- Driving the confined vehicle requires changing it.
- A channel can only be tested by touching something real.
- You find typed content leaving the machine over the network. Stop
  immediately, record exactly what you saw, and do not continue probing.
- The work starts to require a decision this charter did not authorize.

## Verification

The probe is not covered by the test suite, so `verify` is not the gate here —
the gate is that you ran the probe and are reporting what it did.

Before you finish, confirm and state: `pytest -n auto` is unaffected (you
touched nothing it covers), the fixture-safety scan passes, and no synthetic
token you introduced resembles real personal data.

## Report back

- The exact commands you ran and what they printed.
- The findings note contents.
- Anything you could not test, and why.
- Any charter-stop finding, stated plainly rather than worked around.
