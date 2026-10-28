# Retrospective — Federal Tax Withheld on Forms 1099 (2025)

## Result

- **Withholding on Forms 1099-G and SSA-1099 reaches the return.** On core
  v59, federal income tax withheld in Form 1099-G box 4 and Form SSA-1099
  box 6 is recorded, collected in its own family and added on Form 1040
  line 25b with Forms 1099-INT, 1099-DIV and 1099-R box 4. Unemployment of
  $6,000 with $600 withheld moves line 25b, total payments and the refund by
  exactly $600; before, the return was refused.
- **Form 1099-K box 4 stays outside the class,** and line 25b's form-field
  text no longer says it is counted. It is not refused at the bottom line:
  see below.
- **One engine change (ADR-0082, accepted):** the companion rules checked
  when a statement is recorded belong to the package being run. Core v58 and
  earlier still refuse nonzero withholding; a log recorded with withholding
  under v59 is refused under v58, never computed without it.
- **An existing return on v59 is asked three things:** that every 1099-G
  box 4 amount is recorded, that every SSA-1099 box 6 amount is recorded,
  and, after its Social Security family is handed over to v2, that every
  SSA-1099 is recorded. Then every v58 line is unchanged.

## What the evidence changed

- **The fix looked like content and was not.** A 1099-G box 1 or SSA-1099
  box 5 must carry a same-statement companion that is absent or zero, and the
  kernel enforced that for every package at once. P0's first pass designed
  new families on top of it and did not stop; the repair showed that
  relaxing the rule turns a v58 return's $508 refund into $92 owed with no
  refusal. The owner chose the engine change.
- **Keeping the question count low would have changed what a filer
  attests.** Track 1 kept the Social Security family at v1 to avoid a
  handover, leaving a closure claim that says box 6 withholding is absent or
  zero on a package that admits it. The owner chose to replace the claim and
  ask the filer to re-confirm.
- **The plan's goal is not met for Form 1099-K.** The final review recorded
  a 1099-K with $150 in box 4 and the refund still published. The repair
  traced it and stopped, as chartered: any Form 1099-K the engine cannot
  resolve is left out of line 8 and total income while lines 24 through 37
  publish, on v58 as on v59. Only the Schedule 1 attachment blocks. A
  box-4-only block on line 25b would have left the dropped income, so it is
  the next milestone rather than a patch here.
- **A recorded amount counts while its family is unclosed.** A filer who
  records one 1099-G's withholding and not another's gets a smaller line 25b
  with no block. Every withholding family already behaves this way; it is
  parked as one engine question, not fixed for two families.

## Process

- P0 and its repair ran on agy Gemini Flash (about 45 minutes and 1M tokens
  each). The first pass missed its own stop condition and its case table was
  eaten by shell expansion. The owner stopped the Flash Track 0 build before
  it committed anything and moved dispatch to Sonnet 5.5 sub-agents: Track 0
  took 20 minutes, Track 2 18 minutes, the first review 9 minutes.
- **A builder worked around a stop condition** (Track 1, the two-closure
  limit) instead of stopping. Charters now say "stop means stop"; the final
  repair met its hard stop and stopped.
- There is no committed generator for a core package, registry and release
  chain; Track 2 rebuilt the v59 checksums by script.

## Follow-ups

- An unresolved Form 1099-K left out of line 8 and total income while the
  bottom line publishes (every package with the 1099-K route).
- A recorded withholding amount counting while its family is unclosed,
  across every withholding family.
- Form 1099-K box 4 (SC-R1), and routing the 1098, 1099-K and nominee
  recorders through the package overlay before any successor declares an
  entry for them (ADR-0082 production condition 2).
- Package-scoped companion declarations in package content rather than a
  loader map, so the package checksum covers them.
- A generator for the core package, registry and release chain.
