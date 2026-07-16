# Charter — R2 Member-Citizen Byte Verification

Date: 2026-07-15. Chartered by the principal foreman under the owner-paced
Core Tax Conditions remediation. Parent charter:
`charter-2026-07-15-core-tax-conditions-remediation.md`. Branch:
`milestone/core-tax-conditions` at R1 custody commit `fb568be` (R1's handoff
record is `daf8c12`).

## Purpose

Discharge PMR-2 and ADR-0027's member-immutability production condition:
package adoption must resolve registry-verified member citizen bytes, rather
than trusting a bare `(id, version)` match from an arbitrary corpus. This is a
bounded implementation of accepted ADR-0027 decision 6 / consequence PC3;
it does not reopen membership, projection, schema, or citation contracts.

## Owner-launched execution seat

The owner launches one builder to implement this charter. The foreman retains
branch and commit custody but does not implement or judge the artifact's
quality. The builder may change only the registry/checksum resolution path,
its focused tests, and synthetic fixtures necessary to prove the required
golden.

## Required result

1. Every citizen returned in a package's resolved member graph is verified
   against its published registry bytes before it can be adopted.
2. A synthetic golden mutates a resolved member's bytes while retaining its
   published `(id, version)` and demonstrates rejection at adoption.
3. The implementation must not introduce a second membership authority,
   filesystem-path membership, or a package-embedded duplicate checksum
   authority. The package remains the membership authority; the publication
   registry remains the byte authority.

## Verification and handoff

Before handoff, the builder reports the focused mutation golden command and
result, plus any affected focused tests. The foreman records the result,
checks that the change stays in charter scope, runs `git diff --check`, and
commits the completed R2 unit. Full suite, type, and governance verification
are reserved for R3 after both R1 and R2 are landed.

## Stop conditions

Stop and return to the foreman if the work requires a new citizen identity
rule, new package membership semantics, a registry-format contract change, or
any interpretation beyond ADR-0027 decision 6 / PC3. Such a condition is a
separate decision or amendment, not an R2 implementation choice.
