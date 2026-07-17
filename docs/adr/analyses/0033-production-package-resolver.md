# Plain-Language Analysis — Production Package Resolver

Companion to [ADR-0033](../0033-production-package-resolver.md). This document
explains the accepted decision; the ADR is the normative record.

## What changes

The system will gain a safe way to load tax-rule packages from the owner's live
workspace instead of relying only on committed demo fixtures.

The proposed rule is a chain of trust:

1. The user has one current recorded adoption of a particular rule package.
2. That adoption pins a particular published release.
3. The system verifies the release bytes, then the registry bytes that release
   attests.
4. It verifies the chosen package and every member file against that registry.
5. It creates an executable graph only from those verified, explicitly pinned
   members.
6. It refuses to run unless package validation is completely clean.

## Why it is needed

The existing fixture loader works with committed synthetic files. A real
workspace cannot assume nearby files are trustworthy: a package could be
changed, an extra file could sit beside it, a caller could name a stale package,
or even the registry used to verify files could be replaced.

Without this change, a real result could depend on rule content whose identity
and authority the system cannot fully explain.

## What this protects

- A local catalog or path cannot decide which rules are authoritative.
- A stale, automated, or caller-selected adoption cannot override the user's
  current recorded adoption.
- Extra co-located files stay inert rather than quietly becoming executable.
- Checksum mismatches, ambiguous same-key files, missing members, and validation
  failures stop the run instead of producing a partial result.

The current core package has eight validation issues. The proposed production
loader must refuse it until those issues are repaired; it must not add an
exception list just to make the package run.

## What it enables

This is a prerequisite for the first real-return slice: the owner can eventually
run adopted tax rules over facts in the live workspace while preserving a clear
answer to “which exact rules produced this result?”

## What it does not do

It does not implement the production loader yet, accept real data into the
repository, repair the eight package issues, or prove the live-workspace wall and
marshal-only run entrypoint. Those are separately owned implementation
conditions in later milestone tracks.
