# Round 2 Expressiveness and Implementation-Results Review

Date: 2026-07-12. Seat: expressiveness/implementation results, Medium tier.
Scope: SC-P1 only. I ran and inspected both repair suites before reading either
repair examination. I did not read same-round peer outputs or commit bodies.

## Result

**Pass with coverage qualifications.** Both authority shapes reproducibly
enforce current-literal-`true` admission, preserve the admitting finding pin,
and prevent a bare caller family from publishing an empty-source zero. The
committed tests settle the charter's principal SC-P1 distinctions. They do not,
however, explicitly test a Layer-1 aggregate whose computed value is zero or
wrong fact/scope matching, and repair2 slightly overstates its literal replay of
every repair1 negative.

## Independent reproduction

- `repair1`: `python3 -m unittest -v test_resolver.py` — 15 tests, all pass.
- `repair2`: `python3 -m unittest -v test_end_to_end.py` — 11 tests, all pass.
- Independent probe, both shapes: a wrong closure fact type, a wrong required
  identity, and simultaneous current true+false matches all block; present
  member values `5` and `-5` publish computed zero with input pins and no
  closure-authority pin.

## Charter fixture-to-result map

| Fixture / distinction | Repair1 resolver | Repair2 publication |
|---|---|---|
| one current literal `true` | admits; exact id retained | zero publishes; exact id+version pinned |
| current `false` | blocks | blocks |
| absent closure | blocks | blocks |
| old true displaced by current false | blocks | blocks |
| old true displaced by current true | admits new; pins new | zero pins new, not old |
| truthy non-boolean | `1`, `"true"`, `"yes"` block | `1`, `"true"` block |
| two current matching findings | ambiguous; blocks | blocks |
| duplicate A mappings / B adopted rules | blocks | blocks |
| caller bare-family injection | no augmenting carrier seam | faithful path blocks; union mutant publishes |
| presence-only mutant | false fixture kills it per shape | false reaches illegitimate publication per shape |
| currency-blind / truthy mutants | displaced / `1` fixtures kill them | not required as separate rung-3 mutants |
| present members | outside resolver | aggregate 34; closure not consulted |

Every required repair1 fixture has an executed resolver result. Repair2 carries
the charter-required false, absent, displaced, ambiguous, truthy, duplicate,
injection, exact-pin, and present-member cases through publication for both
shapes. Its committed suite omits only one redundant repair1 truthy value
(`"yes"`), not the truthy/non-literal distinction itself.

## Hard distinctions

- **Closure-backed zero vs computed zero vs blocked:** committed tests establish
  closure-backed zero and blocked outcomes; they establish positive Layer-1
  aggregation but not computed zero. My probe supplies the missing observation:
  `5 + -5` publishes zero without a closure pin, distinct from an empty-source
  zero carrying the closure pin.
- **True vs false vs absent vs superseded:** directly and symmetrically tested
  for A and B. Re-attested current true is separately distinguished from the
  displaced predecessor. Mixed current true+false was not named but my probe
  confirms it blocks as ambiguity.
- **Fact vs finding vs source instance:** the implementation separates declared
  closure fact type/identity from finding id/version and pins the latter. My
  wrong-fact and wrong-identity probes block. The committed fixture identity is
  only synthetic tax year and member rows carry finding ids rather than source-
  instance identities, so the suite does not demonstrate cross-subject or
  cross-source-instance isolation. That is a fixture-strength gap, not a
  reproduced affirmative-only failure, and should remain a production contract
  condition rather than expanding this SC-P1 round into SC-P2/SC-P3.

## Examination verification and honesty audit

`examination-repair1.md` matches the executable evidence and discloses all
observed mutant negatives. Its rung-2 residual—the real path might retain a
caller writer—is honestly stated and is exactly what repair2 measures.

`examination-repair2.md` also matches the principal results, declared copy
deviations, mutant divergences, and production-only residuals. One sentence is
too broad: “Every repair1 negative blocks through publication” is not literal,
because repair2 omits repair1's `"yes"` truthy fixture and does not replay each
structural resolver-only assertion. This does not falsify the semantic claim:
two other non-literal truthy values block, and caller construction is tested at
the `Env` boundary. No failed run or adverse mutant result is concealed.

## Recommendation

Accept the round-2 executable evidence as settling SC-P1 affirmative-only
behavior equally for both surviving shapes, subject to the examinations'
production integration conditions. Record computed-zero and richer wrong-scope
fixtures as follow-up test cases; do not use these gaps to choose between the
authority shapes or to reopen SC-P2/SC-P3.
