# Charter — The Entry Loop (synthetic), Track 3 repair review

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Milestone: `docs/phases/legible-entry/milestones/entry-loop-synthetic.md`
- Branch: `milestone/entry-loop-synthetic`
- Under review: `0c9df17` — 10 files, 455 insertions, 49 deletions
- Repair charter: `docs/reviews/charter-2026-07-29-entry-loop-synthetic-track3-repair.md`
- Prior review: `docs/reviews/2026-07-29-entry-loop-synthetic-track3-review.md` (`NOT READY`, F1 and F2 blocking)
- Verdict: `READY` or `NOT READY` **for Track 3 as a whole**, with numbered findings.

This is the milestone's last build gate. After it, the only remaining work is a
narrow focus-indicator repair and the close.

## What has already been established

The full verification reproduced independently at this commit: 722 passed with
3234 subtests, mypy clean on 135 source files, governance lint conformant,
envelope scan clean over `origin/main-ui..HEAD`. Confirm it rather than
re-deriving it, and spend the review elsewhere.

The foreman also checked one thing the builder claimed and it holds: the new F3
derivation test **runs rather than skips** on the machine of record, and it is not
vacuous on its face — it mutates the declaration, rebuilds with the shipped
offline `build.mjs`, serves the compiled output through the real server, drives
Chrome, and asserts both that the mutated text reached the DOM and that the
original text did not. Your job on F3 is the part the foreman did not do: prove it
can actually fail.

## 1. F1 — is the discriminator real, or a tag on an unchanged requirement?

The prior review's finding was that `entry-field.v1` claimed to model any entry
field while requiring a ten-key currency object. The repair introduces a
discriminated union at `$defs.format` keyed by `"kind"`, with one member
`currency_amount_format`, tags `W2_BOX1_FORMAT` with `"kind":
"currency-amount"`, and rewrites the title and description to say this is a
money-field contract.

Measure whether that is a structural fix or a cosmetic one:

- Does `kind` actually **discriminate**? A `oneOf` over variants selected by
  `kind` constrains; an added property alongside the same unconditional
  `required` list does not. Say which this is.
- Would adding a second variant — a date, a bounded choice — now be an
  **addition** rather than a breaking change to existing declarations? That was
  the stated point of the discriminator. Try it on paper.
- Does an unknown `kind` fail closed, at both the schema and the loader?
- Re-run the prior review's own test: take the five fields it tried (1099-INT
  amount, W-2 Box 13 checkbox, employer name/EIN, date, filing-status choice)
  and confirm the schema now **honestly refuses** the four that do not fit,
  rather than admitting them by carrying an irrelevant currency object. Refusal
  is the correct outcome; silent admission is the defect.
- Judge the title and description against what the schema does. The charter
  forbade retaining a generic claim over a currency-only requirement. Is the new
  wording true, and does it say what is *not* covered?
- `correction.kind`: the prior review found the prose calling an enum open while
  JSON Schema closed it. Confirm prose and schema now agree, and that whichever
  was chosen is supported by stated evidence.
- The charter forbade restructuring the shared `source` / `destination` /
  `purpose` / `correction` core on speculation. Confirm it is unchanged.

## 2. F2 — is the schema now the loader's contract?

`_load_w2_box1_field` should now validate against `entry-field.v1` with
`jsonschema` and no longer restate a subset of its rules.

- **Reproduce both of the prior review's constructions.** A declaration omitting
  `id` with `version: "not-a-version"` must now be refused; so must the same
  declaration with an unknown top-level key, and an unrecognised
  `correction.kind`. Confirm each, individually.
- Confirm the hand-rolled presence and type checks are **deleted**, not left
  beside the schema validation. Two validators is the defect this repair exists
  to remove; leaving both would reintroduce it in the same commit that claims to
  fix it.
- The W-2 format-equality constraint is kept but is supposed to be applied
  **separately, after** schema validation, as a runtime constraint rather than a
  schema one. Confirm the ordering, and confirm a schema-valid but different
  currency-amount format is refused for that runtime reason.
- The builder used `is_valid(...)`, which discards the validation error. That is
  probably deliberate and correct for redaction — an error object can carry the
  rejected value. Confirm nothing leaks: no rejected declaration, no rejected
  value, no schema path, in any message, log, response body, or console output.
- **Where does the schema come from at load time, and what happens if it is
  missing or corrupt?** The loader now depends on a file on disk that previously
  only a test read. A surface artifact is shipped as opaque verified bytes; say
  whether the schema is reachable in every context the runtime runs in, and
  whether an unreadable schema fails closed rather than silently skipping
  validation. A validator that no-ops when its schema is absent would be worse
  than the hand-rolled checks it replaced.
- `jsonschema>=4.0` is a declared runtime dependency already imported at module
  level by three kernel modules, so its use is expected. Confirm no new
  dependency and no fallback path was added.

## 3. F3 — can the derivation test fail?

It runs and it is non-vacuous on its face. Prove it bites:

- Break the derivation and confirm the test fails. Restore a hardcoded label in
  the copied `EntryPage.svelte` — the exact defect the old string-searching test
  would have missed — and confirm this one catches it.
- Inspect `tests/helpers/entry_loop_field_derivation_client.mjs`. Can it exit `0`
  while asserting nothing — Chrome absent, navigation failed, selector not found,
  page blank? The Python side asserts `returncode == 0` and
  `{"present": True, "absent": True}`; check the helper cannot report that
  without having actually read the DOM.
- Say plainly whether it runs in CI as well as here, and if not, whether F3 is
  closed or merely written. The builder says it is gated the same way
  `CompiledClientIntegration` already is rather than on a separately-skipping
  path; verify that.
- Data safety with a live browser and a temp build: no residency locator in
  launch arguments, profile paths, URLs, build output, or failure text; and a
  failed or timed-out run leaves nothing behind. The prior Chrome test carries a
  known `launchChrome()` orphan-process and `mkdtemp` leak on caller kill —
  recorded, not fixed. Confirm this test does not widen it.

## 4. Regression, seam, and scope

- `w2-box1-format.js` gained a `kind` key. The format declaration is load-bearing
  for the hint a person reads, the validator, and the refusal message, and Track
  2d landed an **anti-drift regression** over exactly that relationship. Confirm
  it still holds and still bites, and that the added key changed no validation
  behaviour. The builder calls it non-behavioural; check rather than accept.
- Confirm the format-equality check accounts for `kind` consistently, so a
  declaration cannot pass equality while disagreeing on the tag.
- F4 was a restriction: the marker-and-regex seam must not have been widened.
  Confirm `_load_w2_box1_field` still uses one marker and one substitution and
  that `kind` travels through the existing path rather than a new one.
- Scope: no criteria-document edit, no accessibility fix, no presentation model,
  no ADR, no maturity movement, no second fact family, no real data, no residency
  locator.
- Four surface metadata files changed for one changed content file. Recompute
  independently: all 943 manifest entries against byte counts and SHA-256, the
  manifest checksum against registry and adoption pin, the release registry
  digest, the adoption release checksum. The byte total moved from 5,083,917 to
  5,083,946; confirm that is accounted for by the `kind` key alone.
- Run the data-safety scan, then read for what a scan cannot see.

## Boundaries

- **Do not fix anything.** Report findings.
- Do not score or re-score any usability criterion. The cell verdict is FAIL and
  stays FAIL.
- Do not amend the criteria document.
- Do not ratify or amend ADR-0049 or ADR-0051; both are the owner's at the close.
- If you conclude the contract should become an ADR, say so as a note to the
  owner, separately from the verdict.
- No maturity claim.

## Verdict

`READY` or `NOT READY` for Track 3 as a whole. Number each finding, say what is
wrong and what would close it, separate blocking from weakening.

A blocking finding here should be a false claim left in the record — a schema
still overclaiming, a validator that can be bypassed, a test that cannot fail —
rather than a shape you would have chosen differently. If F1 and F2 are genuinely
closed, say so and let the milestone move.

Orient with `python3 tools/foreman_context.py --ref HEAD --format markdown` and
`python3 tools/build_orientation_block.py --ref HEAD`. If either refuses, stop and
report it. No `.venv`; use system `python3`. Ratified line `origin/main-ui`.

## Report back

The verdict; each measurement; which of the four non-money fields the schema now
refuses and how; both F2 reproductions and their outcomes; what happened when you
broke the derivation the F3 test guards; what happens if the schema file is
unreadable at load time; and the single thing most likely to be wrong that you
could not prove either way.
