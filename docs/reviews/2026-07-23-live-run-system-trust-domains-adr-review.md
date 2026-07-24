# Review — Proposed ADR-0044 Live-Run System Boundary and Trust Domains

Role: independent ADR reviewer.

Authorization: direct owner instruction on 2026-07-23 to take the reviewer seat
and review the current ADR. Review basis: the bounded **ADR review shape** in
`docs/phases/real-return/milestones/live-run-trust-domain-definition.md`.

Object: local commit on `adr/live-run-system-trust-domains`, specifically:

- `docs/adr/0044-live-run-system-boundary-and-trust-domains.md`
- `docs/adr/analyses/0044-live-run-system-boundary-and-trust-domains.md`

The same commit's ADR index and phase/handoff/roadmap edits were checked for
status coherence only. They are not separate decision content. No prototype
committee, evidence-synthesis artifact, implementation review, push, PR, or
owner disposition is part of this review.

Verdict: **READY as a local proposed ADR for owner consideration.**

## R1 — Required ADR shape

Result: **pass**.

The ADR contains each of the seven sections required by the active plan:

1. **Context — system versus developer workflow:** “Context — the system is
   not the developer workflow” distinguishes a convenient same-authority
   workstation arrangement from the application's intended privacy boundary.
2. **Four domains:** the decision table defines Developer/Supply, Publication,
   Live-Run Data, and Owner Authorization by assets and authority.
3. **Permitted crossings:** the four numbered crossings cover
   Developer/Supply → Publication, Publication → Live-Run Data, Owner
   Authorization → Live-Run Data, and the no-descriptive-artifact return rule;
   it expressly excludes a direct Developer/Supply → Live-Run Data crossing.
4. **Threat posture and residuals:** the claim is conditional on later
   enforcement against an unprivileged Developer/Supply authority. Owner
   elevation, administrator/root-equivalent control, Live-Run compromise, and
   an owner-adopted malicious release are explicit residuals.
5. **Guarded transport:** it is placed at Developer/Supply → Publication,
   conditional hook protection and reachable `--no-verify` bypass are stated,
   and credential confinement remains `unestablished`.
6. **Future implementation gate:** the ADR selects no substrate, leaves the
   data-boundary row at L3, and names the later implementation and real-run
   verification required for L4.
7. **Links and evidence limits:** direct records are listed and the stopped
   same-UID evidence is expressly limited to its tested shapes.

The ADR is marked `proposed`; the ADR index describes it as inert while under
review. No branch record presents it as accepted.

## R2 — Existing-record support and claim calibration

Result: **pass**.

### Accepted boundary contracts

- ADR-0031 Decision 1 supports the authority distinction between ordinary
  authoring/publication and an explicitly capable live run; Decisions 2 and
  4–7 support fail-closed classification, locator exclusion, independently
  constructed synthetic fixtures, and sensitivity inheritance.
- ADR-0032 Decisions 1, 3, and 6 support contribution as a separate live event,
  runs consuming facts rather than caller values, and contribution artifacts
  remaining within the residency boundary.
- ADR-0033 Decisions 1–3 support current owner adoption and the verified
  release → registry → package/member → hard-validation chain instead of
  working-tree proximity, caller selection, or co-located bytes.

ADR-0044 preserves those contracts and names its two changes to ADR-0031's
architectural framing: the adopted package becomes the intended supply
crossing, and guarded transport becomes publication integrity rather than the
live-data privacy wall. It does not silently edit ADR-0031 in place.

### Guarded Transport evidence

The cited H1 records support the draft's narrow statements:

- `round-1-triage.md` and both Round 1 reviews record that the rival's mode-600
  store was readable by a same-UID process, while the incumbent released its
  descriptor before the authoritative envelope scan and did not complete the
  required actual-Git probe.
- `repair1-triage.md` and both delta reviews record that the one permitted
  repair still lacked a reproducible completed successful actual-Git path.

The ADR does not turn those results into an impossibility theorem. It
explicitly leaves separate identities, containers, VMs, credential stores,
proxies, and hosted controls unselected and unproven.

### Current push-envelope posture

The targeted audit and test reproduced the exact posture the ADR states:

```json
{"credential_confinement": "unestablished", "hooked_marker_refused": true, "hooks_verified": true, "no_verify_bypass_reachable": true}
```

This is used only as synthetic evidence that hooks protect when invoked and
that raw bypass remains reachable. The ADR and companion expressly deny that
the audit inspects or protects an owner credential, remote, or live run.

No cited evidence is upgraded beyond its type.

## R3 — No unplanned enforcement or maturity claim

Result: **pass**.

The ADR defines logical authority boundaries, then states twice that the
current same-UID workflow does not enforce them. It selects no OS user,
container, VM, credential store, proxy, hosted control, or other substrate.
The future-mechanism examples appear only as candidates or deferred
alternatives.

The data-boundary row remains L3. The draft requires a later, separately
planned implementation to prove forbidden routes absent, repeat E18.1/E18.2
checks, prove adopted-package consumption, and complete owner-run verification
before any L4 claim. Guarded transport alone is expressly insufficient for the
live-data privacy claim.

## R4 — Positioning and security limits

Result: **pass**.

The draft is a security-positioning decision rather than an implementation
claim:

- it says what authority separation the application would rely on;
- it says the current developer workflow does not provide that separation;
- it assigns present repository/envelope controls only an L3
  accidental-leakage role;
- it names the threats and residuals the project does not handle; and
- it defers whether and how a mechanical boundary will be implemented.

If accepted, this would be a binding Tier 3 positioning contract, not an
informal essay. While it remains a local `proposed` draft, it is inert. That
status distinction is explicit and coherent with the owner's instruction that
the ADR remain local.

## R5 — Plain-language companion

Result: **pass**.

The companion accurately explains the ADR without adding authority or scope.
It covers:

- the move from developer-workflow convenience to four logical domains;
- the difference between accidental-publication controls and protection from
  malicious same-authority code;
- the adopted-package crossing and non-descriptive return statement;
- guarded transport's publication-integrity role;
- the current same-UID, credential-confinement, owner-elevation, and
  administrator/root limits; and
- the later implementation and L4 gate.

It links the authoritative ADR near the top and says the ADR controls. No
material contradiction or omitted load-bearing limit was found.

## R6 — Status, references, and data safety

Result: **pass**.

All repository-relative paths listed under “Links and evidence limits” exist.
The ADR-to-companion link resolves. The proposed ADR index row is explicitly
inert. Phase state, handoff, and roadmap all describe the draft as proposed,
local-branch work pending review and owner disposition.

The branch contains only documentation. No personal value, live-workspace
locator, credential, remote detail, descriptive live-run artifact, or absolute
owner-local path was found. The record says no such material was consulted.

## Verification

All checks passed locally from the exact review branch:

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
  exit 0; hooks verified, hooked marker refused, --no-verify bypass reachable,
  credential confinement unestablished

python3 -m unittest tests.test_push_envelope_posture
  Ran 3 tests — OK

git diff --check main..HEAD
  exit 0
```

## Findings and limits

No blocking finding.

One non-blocking interpretation note: acceptance would commit the project to
the four-domain security position and its stated future proof gate; it would
not commit the project to implementing any named substrate or to scheduling
that work. The local proposed status keeps that owner decision open.

## Recommendation

The local draft is ready for the owner's substantive disposition. Keep it
local and inert until that decision. If the owner accepts the position, the
status change and any publication/merge action remain separate owner-directed
steps.
