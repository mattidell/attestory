# Round 3 Adversary Review — Source Completeness

Date: 2026-07-12  
Seat: adversary, Medium tier / medium effort  
Evidence rung: focused shape-A construction boundary

## Method and observations

I read the round-3 charter, repair3 implementation and examination, the prior
adversary finding/triage, and the official Form 1099-INT and Schedule B/1040
instructions. I did not read either same-round peer review. I ran
`python3 -m unittest -v test_authority`: 11/11 pass. I separately executed
the attacks below against the callable evaluator surface.

The ordinary `AuthorizedMembership` cases do close the round-2 public-dataclass
attack. However, `run_rule_with_carrier` does not require an
`AuthorizedMembership` instance (Python annotations are not runtime checks).
`validate_membership` reads only `mapping_id`, `mapping_version`, and
`authorities`; the subsequent copied evaluator reads the same untyped object’s
`closed_families` and `pin_for`. A duck carrier can validate as empty/fresh,
then supply a closed family and fabricated pin to evaluation. This is an
evaluator-accepted caller authority, not merely the explicitly labelled
`run_rule_trusting` mutant.

## Attacks: attack → outcome → exhibit

1. **False/unknown closure trap — succeeds.** With no findings and the declared
   mapping, I supplied a duck carrier with `authorities=()`, matching fresh
   `resolve_A` output, but `closed_families={FAM}` and `pin_for(FAM)` returning
   fabricated `invented@v9`. `run_rule_with_carrier` published `0` and the
   fabricated closure/mapping pins. Thus an *absent* closure yields zero through
   the purported validated entry. **Exhibit:** local reproduction command
   below; `repair3/authorized_eval.py:63-79,95-100`; `repair2/prototype_eval.py:72-86,101-116`.

2. **Caller-set smuggle — succeeds.** The duck carrier’s `closed_families` is
   exactly a caller-supplied set under a different attribute name. Validation
   never observes it, while layer 2 unions no further data and accepts it as
   authoritative. This recreates the round-2 defect despite the carrier’s
   declared provenance. **Exhibit:** same reproduction; compare
   `validate_membership` with `Env.closed_families`.

3. **Identity trap — not reproduced at this narrow boundary.** Two payer or
   account rows sharing the member name aggregate; neither payer nor account is
   used as a fact identity here. The official form contains payer, recipient,
   and an optional payer-assigned account number, so this prototype cannot
   establish that a production fact model distinguishes two accounts; it also
   does not accidentally use those fields as a key. **Exhibit:**
   `repair3/test_authority.py:55-60`; Form 1099-INT, Copy B/account-number and
   recipient instructions. This remains SC-P2, not proof of safety.

4. **Rekeying/correction trap — not reproduced, but unmodeled.** Closure
   identity is tax-year only and no evidence or fact identity exists in repair3;
   a corrected input cannot rekey a question in this code. That avoids a
   demonstrated Article-1 violation but is insufficient evidence about a real
   correction/evidence-replacement path. **Exhibit:** `repair3/test_authority.py:18-29`; `repair1/resolver.py:22-35`.

5. **Family-boundary trap — not reproduced by the resolver; semantic boundary
   remains open.** Shape A faithfully treats its mapping family string as the
   boundary, without defining its members. IRS Form 1099-INT distinguishes box
   1 interest from box 3 Treasury interest and box 8 tax-exempt interest;
   Schedule B says taxable interest includes several sources and requires payer
   amounts. Repair3 has no test that its `sf-demo-interest-2097` is neither
   over- nor under-inclusive. This is deferred SC-P3, so I do not count it as a
   new construction-boundary failure. **Exhibit:** Form 1099-INT recipient
   instructions boxes 1, 3, 8; 2025 Schedule B instructions, Part I line 1.

6. **Stale-pin trap — succeeds.** The same accepted duck carrier can return a
   stale or wholly invented `ClosureAuthority` from `pin_for` after validation.
   My absent-finding reproduction pinned `invented@v9`; with a real current
   finding, substituting `fake-pin@v666` likewise published that pin. The
   stale-first/current-second test covers only genuine dataclass carriers, not
   the evaluator’s accepted duck surface. **Exhibit:** `authorized_eval.py:95-100`; `prototype_eval.py:82-86,108-110`.

7. **Evolution trap — resists for this construction layer.** Adding a future
   1099-INT member/box requires a mapping version/family decision, not a change
   to closure-finding identity (year remains the question’s identity). Mapping
   provenance causes a carrier for the old mapping to fail against a new
   mapping. The tax meaning of the new member is nevertheless SC-P3 work.
   **Exhibit:** `authorized_eval.py:63-79`; mapping-mismatch test;
   Form 1099-INT’s separately reported boxes.

### Reproduction (synthetic)

```
run_rule_with_carrier(rule, {}, Trojan(), mapping, [])
=> 0; closure-authority invented@v9; mapping-citizen invented-map@v9
```

`Trojan.authorities` was `()`, its mapping provenance matched `mapping`, its
`closed_families` returned the rule family, and its `pin_for` returned the
shown fabricated authority. Therefore the fresh resolver result was also empty
and validation returned normally before publication.

## Dissent and recommendation

I dissent from the examination’s sufficiency call. Repair3 validates a record
of authority but does not bind the subsequently consumed authority interface to
that record. The public `run_rule_with_carrier` path still permits caller-made
empty-source zero and fabricated/stale pins; the explicit `run_rule_trusting`
mutant is a second, independent public bypass. The central construction
question is consequently not closed at the executable boundary.

Repair requires a carrier type/runtime validation that is the sole object given
to `Env` (or reconstruct `AuthorizedMembership` from the fresh resolver output
after validation), and the unsafe mutant must be inaccessible outside its test
fixture. Retain the passed literal-true, duplicate-dataclass, and mapping
provenance cases, then add this duck-carrier regression before any ADR call.
