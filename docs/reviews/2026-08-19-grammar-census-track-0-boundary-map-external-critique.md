# Source verification of the external critique of the Track 0 boundary map
Foreman, 2026-08-19. Checks run against commit 990888c2.

| # | Critique claim (source-dependent, grok could not check) | Verified result |
|---|---|---|
| Q1 | Are TERM_OPS/PREDICATE_OPS in the attachment-rule schema, or Python only? | ~~**Python only.** Not in any attachment-rule schema.~~ **WRONG — superseded 2026-08-20, see "Correction to Q1" below.** |
| Q2 | Are blocking codes schema enums, or Python constants only? | **Schema enums** — present in derivation-record.v2..v7, npe-walk.v1..v3, checked-conclusion-binding.v1. |
| Q3 | Are rounding modes in operation-semantics, or only evaluator.py? | **In operation-semantics.v1.schema.json.** |
| Q4 | Do findings.py invariant pairs have any schema? | **No schema anywhere.** |
| Q5 | Is act-package-adoption an act (surface 8) filed under packages (surface 4)? | **Yes** — title "Package adoption act payload". |

## Confirmed contradictions in the map (not arguable — decided by source)

1. **Rounding modes are on both sides of the line.** Surface 6 classes
   rounding-mode dispatch grammar-adjacent on the stated ground that surface
   6's contents are "registry-populated Python dictionaries, not a
   schema-validated citizen." Q3 shows rounding modes ARE in
   operation-semantics.v1 — the very citizen surface 3 classes grammar
   proper. The same construct is classified twice, oppositely, depending on
   which file was read. Grok predicted this exactly.

2. **act-package-adoption is cross-filed.** Q5 confirms it is an act payload,
   i.e. surface 8 (grammar-adjacent), but the map cites it as concrete
   surface for surface 4 (grammar proper).

## Correction to Q1 — added 2026-08-20

**Q1 was the wrong question, and the answer drawn from it was wrong.**

Grok asked whether the vocabulary appears in an `attachment-rule` schema. It
does not — that much was accurately checked. But "not in `attachment-rule`"
was then treated as "not in any schema," and the round-2 Builder found the
schema this reasoning missed: the term and predicate vocabulary is
schema-typed at
`packages/schemas/derivation/source-family.v2.schema.json`, `$defs/term`
(:172) and `$defs/predicate` (:278), reached as
`member_constraints[].violated_when` (:66) and
`identity_exclusivity[].components` (:97). Its sole caller is
`packages/derivation/runner.py:653-707`, reading `self.ctx.family_declarations`
(bound at :637). ADR-0066 decision 1 says where to look, in as many words:
"Structured-member constraints belong to versioned source-family content."

The Foreman verified all of this against source on 2026-08-20 and accepts it.
Surface 5b-i is **grammar proper**, not adjacent.

**Why this matters more than the one wrong row.** Both the external model and
the Foreman's own verification pass reached the same wrong conclusion, from
the same cause: the citizen's name does not advertise what it contains. A
reader looking for an attachment-rule's validation vocabulary has no reason
to open a file called `source-family`. Two independent readers missed it, and
only a third reader working the same ground caught it. That is direct
evidence for the census's method — independent readings reconciled — and it
is a discoverability finding Track 2 should carry.

It is also a caution about the verification pattern used here: checking the
specific claim an external critique makes is not the same as checking the
conclusion being drawn from it. The question was answered correctly and the
inference from it was still false.

## What the checks also rescue

- ~~Surface 5's mini-language is correctly adjacent, for the principled reason
  that it has no schema-typed citizen.~~ **Withdrawn — see "Correction to Q1"
  above. It has one, and it is proper.**
- Surface 2 stands. Q2 confirms blocking codes are schema-carried, as claimed.
- Surface 6(i) stands. Q4 confirms findings.py pairs are unschematised.

## Consequence for the repair

A single consistent test — "is it declared in a schema-typed versioned
citizen?" — reproduces the map's labels almost everywhere and forces exactly
two changes: rounding modes become proper, and surface 8 becomes proper.
That test is decidable and defensible, but grok's axis-6 argument is that it
conflates module statics with clause expressiveness and pre-judges the later
comparison. Hence the repair records ORTHOGONAL AXES alongside the binary
rather than replacing one lossy label with another.

## Standing value beyond this repair

The critique's answer on pre-judgment (its axis 6) is a substantive first
draft of comparison dimensions for Track 3's brief: defeasibility /
rule-yields-to-rule as a paradigm rather than a blocking enum; period and
horizon semantics as a linguistic feature (OpenFisca); peer languages vs one
grammar with satellites (DMN FEEL vs boxed expressions vs tables); embedded
vs standalone (where meaning is allowed to live); object language vs
observational theory (traces as productions); constitutive vs prescriptive
(LegalRuleML). Carry these to Track 3 as candidate dimensions — as an
external model consultation, never as authority.
