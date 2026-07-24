# Retrospective — Live-Run System Definition and Trust Domains

Status: **final — ADR-0044 accepted by owner direction 2026-07-23;
publication PR pending owner merge.**

## Milestone

Live-Run System Definition and Trust Domains is a bounded Tier 3 positioning
milestone. Its publication unit is
`review/live-run-system-trust-domains`; the PR and merge commit remain
owner-held until merge.

The milestone distinguishes the application's intended privacy boundary from
the current developer-workstation convenience arrangement. It closes a
decision, not a mechanism.

## Shipped

- ADR-0044 defines Developer/Supply, Publication, Live-Run Data, and Owner
  Authorization as four logical trust domains with explicit authorities,
  permitted crossings, and residuals.
- The current owner-adopted, byte-verified package is the intended
  Publication → Live-Run Data supply crossing.
- Guarded transport is positioned as Developer/Supply → Publication integrity,
  not as the live-data privacy wall.
- The active deferral ledger and maturity-matrix explanation now distinguish
  missing live-run authority enforcement from missing publication-credential
  confinement without changing any maturity cell.
- The plain-language companion states which security problems the project
  handles now, which it does not handle, and what proof a later enforcement
  milestone would need.
- The bounded review returned READY with no blocking finding.

No isolation substrate, credential mechanism, proxy, hosted gate, or delivery
date is selected or scheduled. The data-boundary maturity row remains L3.

## Verification

The review branch passed:

```text
python3 -m unittest
  Ran 562 tests in 128.647s — OK

python3 -m mypy
  Success: no issues found in 108 source files

python3 tools/governance_lint.py
  governance lint: conformant

python3 tools/envelope_scan.py --range main..HEAD
  exit 0, no findings

python3 tools/audit_push_envelope_posture.py
  hooks verified; hooked marker refused; --no-verify bypass reachable;
  credential confinement unestablished

python3 -m unittest tests.test_push_envelope_posture
  Ran 3 tests — OK

git diff --check main..HEAD
  exit 0
```

The closure record reruns the ordinary verification floor before publication.

## Decisions

- **Tier 3:** [ADR-0044](../adr/0044-live-run-system-boundary-and-trust-domains.md)
  is accepted by owner direction. It binds the four-domain security position
  and the proof gate for any later L4 claim.
- No Tier 1 or Tier 2 implementation decision was made.

## Deviations

The owner authorized this milestone to use a direct ADR-and-companion path
instead of a new prototype, evaluation analysis, evidence-synthesis artifact,
or committee. Existing accepted boundary ADRs and the completed Guarded
Transport and push-envelope records supplied the bounded evidence.

An earlier evidence-synthesis branch was rendered obsolete by that amendment
and was not included in this publication unit. The owner directly took the
reviewer seat for the current ADR; after that READY review, the owner directed
the foreman to accept the ADR, close the milestone, and open the publication
PR. No sub-agent was dispatched.

## Data safety

All committed work is documentation based on existing synthetic or
non-descriptive records. No real workspace, credential, remote, locator, value,
run disposition, or personal artifact was consulted or recorded.

## Follow-ups

- Owner merge of the publication PR makes this accepted ADR and closure record
  part of the continuous `main` record.
- Any implementation of authority separation starts only from a separately
  owner-selected milestone. It must select and test one substrate, prove the
  forbidden routes absent, and complete the ADR's real-run verification gate
  before an L4 claim.
- Guarded transport may be revisited separately as publication hardening; it
  does not by itself discharge the live-data boundary.
- Schema-publication controls and builder/reviewer scope controls remain
  tabled.

## Planning lessons

A security-positioning decision can usefully state system authorities, handled
threats, and explicit residuals without prematurely selecting a mechanism.
Keeping positioning separate from implementation avoids turning candidate
technologies into accidental commitments. A local proposed draft followed by a
bounded owner-directed review also gave the owner a clean disposition point
before publication.
