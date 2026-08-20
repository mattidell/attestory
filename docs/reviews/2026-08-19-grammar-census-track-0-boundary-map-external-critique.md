# Source verification of the external critique of the Track 0 boundary map
Foreman, 2026-08-19. Checks run against commit 990888c2.

| # | Critique claim (source-dependent, grok could not check) | Verified result |
|---|---|---|
| Q1 | Are TERM_OPS/PREDICATE_OPS in the attachment-rule schema, or Python only? | **Python only.** Not in any attachment-rule schema. |
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

## What the checks also rescue

- Surface 5's mini-language is correctly adjacent, but for the wrong stated
  reason. The map says "structurally distinct vocabulary" (grok: identity
  hygiene, not a principle). Q1 supplies a principled reason that matches
  surface 6's test: no schema-typed citizen.
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
