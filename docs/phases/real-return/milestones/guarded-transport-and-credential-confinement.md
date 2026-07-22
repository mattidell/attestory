# Milestone: Guarded Transport and Credential Confinement

Status: **active — Track 0 H1 stopped pending owner disposition**
(2026-07-22). The owner approved the milestone and authorized the prototype
builders/reviewers; both rival evidence and the one permitted repair pass have
been completed. No H1 contract is ratified and no production implementation
may begin. Third milestone of the Real Return phase; operates under ADR-0030
per-ADR / per-track merges and ADR-0034 owner-approved dispatch. This is the
phase's first **hardening (L3→L4)** milestone: it discharges a named production
condition rather than adding a new tax domain.

## Decision summary (tiered)

- **Tier 3 (owner, prototype-backed): H1 — the credential-confinement model.**
  The heart of the milestone. ADR-0031 already ratified the *requirement* —
  "remote credentials reachable only through the guarded push path, so raw
  `git push`/`--no-verify` cannot bypass the gate" (Adversary A3) — as a
  production condition, not yet discharged. Today `tools/envelope_scan.py`
  scans commit/push *content* through byte-verified hooks, but the remote
  credential is available to any `git push`, and `--no-verify` skips the
  pre-push hook entirely (detected on the next gate battery, never prevented —
  ledger entry 2). H1 decides the architecture that inverts this: **the
  credential becomes the gate.** Product-visible (it changes how the owner
  pushes) and boundary-critical; genuinely new ground → Tier 3 with rival
  evidence per ADR-0013. This decision earns its own implementation-decision
  ADR (the *how*; ADR-0031 already ratified the *why*, the ADR-0038 pattern of
  discharging a named condition with a ratified shape).
- **Tier 2 (default + veto, prototype-backed): H2 — prevention vs. residual
  detection, and the server-side backstop.** How far toward *prevention* the
  milestone goes and where it consciously accepts residual detection. ADR-0031
  already **rejected** "CI-detection + remote purge-and-rotate" as load-bearing
  (§C.8: publication cannot be un-published), so the design must lead with
  prevention. This topic decides the server-side control (GitHub push
  protection / secret scanning, branch protection; the remote is already
  private — First Real Return Slice ledger entry 3) and draws the explicit
  line between **in-repo-provable confinement** and **owner-attested server
  controls**. Gate 0 may find this needs no separate prototype beyond H1's;
  that finding is recorded, not assumed.
- **Tier 2 (default + veto): H3 — the adversarial audit surface.** ADR-0031's
  named E18.1 canary (topology/capability audit: the credential is not
  reachable except through the guarded path) and E18.2 seeded-marker kill-test
  suite over the enumerated bypass surfaces. This is the *decisive evidence
  form* for a security milestone — it may be design-then-implement rather than
  a rival prototype.
- **Tier 1 (log only):** installer extension (the confinement shim installed
  per-clone alongside the existing envelope hooks, the
  `tools/install_envelope_hooks.py` precedent); live-run harness use of the
  guarded path; matrix/phase-state/retrospective content.

## Threat model (names the adversary — read before Scope)

The boundary this milestone hardens is against **(a) accidental residency
crossings** and **(b) an Adversary A3 who bypasses the content gate** — a
local process, script, or mistaken command that attempts to push without
going through the guard. It is **not** against a malicious owner: the owner
holds the real facts and the ultimate credentials by definition, and no local
control can prevent a determined holder of secrets from exfiltrating their own
data. Confinement that pretends otherwise is theater. The milestone's job is
to make the *only reachable path to the remote* the gated one, so that both
the honest-mistake case and the bypass-tool case fail closed. This scope
statement is load-bearing; without it the milestone is unbounded.

## Objective

Confine the remote credential and transport so that a byte can only cross the
repository→remote boundary through the gated path: raw `git push` and
`git push --no-verify` fail closed (no reachable credential) rather than being
detected after the fact. The data-boundary matrix row rises **L3→L4** and the
deferral ledger's highest-priority entry is retired. The owner performs a real
run over the guarded path; the repository continues to provably carry zero
personal data.

## Why this milestone

Drafted for owner selection over a human presentation surface and further
breadth (the two other live matrix frontiers). The product now runs the owner's
**real tax data** through an
**unconfined** transport, and that exposure compounds with every real run.
Guarded transport is the single named deferral the record repeatedly calls
highest-priority and the only thing holding the data-boundary row (and thus
the whole matrix) below L4. Structurally it is a *lighter* milestone than the
last two: ADR-0031 already ratified the requirement, so only the *how* is
open. The standing phase test — "does the product now do something for its
user it could not before?" — is answered here in a specific sense: it makes
the existing real-data capability **safe to rely on repeatedly**, which is the
precondition for the owner using it as an actual tool rather than a supervised
demonstration.

## Scope

1. **Credential confinement (H1).** The ratified confinement architecture: the
   remote credential is reachable only through the guarded push path. Raw
   `git push` has no reachable credential; `--no-verify` cannot skip the guard
   because the guard is not (only) a skippable hook — it is the sole holder of,
   or sole releaser of, the credential. Installed per-clone and byte-verified,
   extending the `tools/install_envelope_hooks.py` model, so a clone without
   the confinement fails the standard verification battery.
2. **The guarded push path (H1).** The single command/path through which a
   legitimate push runs the full envelope battery (`tools/envelope_scan.py`
   over the outgoing content) and only then reaches the remote. Ergonomics are
   a first-class design concern: a guard the owner routinely bypasses for
   convenience is not a guard.
3. **Server-side backstop and the provable line (H2).** The consciously chosen
   server-side control (push protection / secret scanning / branch protection;
   the private remote already recorded), and an explicit written line between
   what is **kill-tested in-repo** and what is an **owner-attested server
   control** — the latter recorded the way "the remote stays private" is
   recorded today, not claimed as a unit test.
4. **The adversarial battery (H3).** Kill-tests over the enumerated bypass
   surfaces (E18.2 seeded-marker): a seeded *synthetic* residency marker in an
   outgoing envelope is blocked through the confinement path; a raw
   `git push --no-verify` fails closed; a credential-read outside the guarded
   path fails. The E18.1 canary: a topology/capability audit asserting the
   credential is not reachable except through the guard.
5. **Live-run integration.** The owner performs a real run and pushes (if any
   push occurs) exclusively over the guarded path; acceptance evidence is the
   non-descriptive attestation, same form as prior milestones.

## Non-goals and deferred boundaries

- **No new tax content.** No new domain, line, schedule, or worksheet. This is
  a boundary-hardening milestone.
- **No human presentation surface** — E8.1 and citation display stay on the
  frontier.
- **No hosted/remote service.** Confining the transport is not building a
  server the owner runs against remotely; the run stays local and
  owner-operated. "Guarded transport" means the *credential path*, not a new
  deployment topology.
- **No reopening of the residency contract.** ADR-0031 stands; this milestone
  *discharges its named production condition*, it does not relitigate the
  boundary.
- **Malicious-owner exfiltration is out of the threat model** (see Threat
  model). Named here so its exclusion is visible, not silent.
- **Server-side prevention beyond the chosen backstop** (e.g. organization
  policy, hardware tokens) is deferred unless H2 finds one load-bearing.

## Contracts

### Existing (build on, do not reopen)

ADR-0031 (real-data residency boundary — the guarded-transport production
condition this milestone discharges; the E18.1/E18.2 audit surfaces it names),
ADR-0032/0033 (contribution boundary, production resolver — the run this
hardens), ADR-0030/0034 (process), and the existing envelope tooling
(`tools/envelope_scan.py`, `tools/install_envelope_hooks.py`,
`tests/test_envelope_hooks.py`) as the installed-and-byte-verified precedent
the confinement shim extends.

### Decided here

H1 the credential-confinement model — through the ADR-0005/0013 prototype
process with an owner-approved `docs/prototypes/<topic>/plan.md` before first
charter, rival evidence per ADR-0013, per-ADR no-ff merge on ratification.
H2/H3 are ratified as needed (Gate 0 reports whether either needs a prototype
distinct from H1's).

## Data safety

Heightened for this milestone because its subject *is* the boundary. Standing
rules unchanged and in force. **Additional discipline specific to this
milestone:** no real credential, token, or remote secret ever appears in a
fixture, test, charter, review, or golden — confinement is exercised with
synthetic/dummy credentials and *seeded synthetic* residency markers only. The
real credential exists solely in the owner's run environment; its entire
repo-side existence remains the three-fact attestation. A test that needed a
real credential to pass would itself be a boundary violation and is prohibited
by construction.

## Verification

- Full in-repo suite, mypy, governance lint stay green and fully synthetic.
- **Adversarial kill-tests are the decisive evidence** — the security analogue
  of the envelope byte-verification battery. A green happy-path is not
  evidence of confinement; the battery must prove the *bypass* paths fail
  closed: raw `--no-verify` push blocked, credential unreachable outside the
  guard (E18.1 canary), seeded-marker envelope blocked through the confinement
  path (E18.2), over every enumerated surface.
- **Standing charter requirement (promoted, First Real Return Slice),
  translated to this milestone:** every behavior track's charter drives the
  *actual push/transport path the owner uses* and proves the adversary paths
  closed from that surface — not a downstream helper that simulates the guard.
- **Fail-closed by construction** (residency-classifier discipline): a
  confinement bug that blocks a legitimate push is a usability defect to fix;
  one that fails *open* is a data-safety defect and a blocking finding.
- Acceptance evidence for the real run is the owner's non-descriptive
  attestation — ran the slice over the guarded path, dispositions observed in
  quarantine, no artifact crossed the boundary — never which lines published.

## Exit criteria

1. H1 ratified with rival-backed evidence (H2/H3 as Gate 0 directs); per-ADR
   merges on `main`.
2. The confinement mechanism is installed per-clone and byte-verified; raw
   `git push` and `git push --no-verify` cannot reach the remote (fail closed,
   demonstrated by kill-test).
3. The adversarial battery is green: seeded-marker envelope blocked through the
   confinement path (E18.2); credential unreachable outside the guarded path
   (E18.1 canary); every enumerated bypass surface kill-tested.
4. The in-repo-provable / owner-attested line is written down explicitly; any
   server-side control is recorded as an attested owner control, named, not
   claimed as a unit test.
5. The owner has run the real slice over the guarded path; the non-descriptive
   attestation is recorded.
6. The repository contains zero personal data, mechanically checked (unchanged
   standing gate).
7. Maturity matrix data-boundary row raised L3→L4 (with honest footnotes for
   any aspect the milestone did not exercise); phase-state briefing rewritten;
   retrospective written; the First Real Return Slice deferral ledger's entry 1
   (guarded transport) **retired** and entries 2 (operator bypass) and 3
   (private remote) dispositioned by name.

## Tracks

Per ADR-0030, each decision topic and each track is its own short-lived branch
with its own review gate and no-ff merge; dependency order, not a single-branch
plan.

### Track 0 — Contract decision (H1, and H2/H3 as needed)

The H1 prototype with an owner-approved plan before first charter, rival
confinement shapes evaluated on **bypass-resistance** (does raw/`--no-verify`
push fail closed?), **ergonomics** (owner workflow cost — a routinely-bypassed
guard fails), **in-repo testability** (can the confinement be kill-tested
synthetically?), and **reversibility**. Candidate rivals to frame (not to
foreclose): (A) a git credential-helper that releases the token only after the
envelope battery passes; (B) a guarded-push wrapper that is the sole holder of
the credential, with no credential configured for raw `git`; (C) an ephemeral
per-push credential plus a server-side backstop. **Gate-0 economics reported
to the owner before charters** — this milestone's single biggest planning
unknown is the in-repo-provable vs. owner-configured testability split (a
credential helper may not see the outgoing pack; server-side controls are not
unit-testable from `main`), and Gate 0 is where that resolves cheaply. If the
split is unfavorable, the owner may rescope before spending on build.

### Track 1 — Confinement mechanism

The ratified confinement architecture implemented and installed per-clone
alongside the existing envelope hooks (the `tools/install_envelope_hooks.py` /
byte-verification precedent), with the guarded push path as the sole
credentialed route. Charter names its adversarial-surface evidence per the
Verification section. No new tax content.

### Track 2 — Adversarial battery

The E18.1 canary and E18.2 seeded-marker kill-tests over every enumerated
bypass surface, proving the bypass paths fail closed from the authoritative
push surface. Fully synthetic credentials and markers.

### Track 3 — Live integration and completion

The owner's real run over the guarded path, attestation recorded; then matrix
(data-boundary row L3→L4), phase-state rewrite, retrospective, and deferral
ledger update (entry 1 retired, 2/3 dispositioned) — itself reviewed and
merged as a records track.

## Process notes carried from the Dividends and Schedule B Slice retrospective

- **Dispatch git hygiene (promoted lesson, and acutely relevant here):** this
  milestone touches git plumbing directly. Foreman-side git mutations run in a
  dedicated worktree whenever a sub-agent dispatch is in flight, never on the
  primary checkout's `main` — the shared-`.git`-refs race that twice clobbered
  `main` last milestone is a live hazard for a milestone whose *subject* is git
  transport.
- **Harness charters specify by required capability, not artifact name**
  (promoted lesson): Track 1's charter names the confinement *capability* and
  the surfaces it must guard, not a single script filename, to avoid the silent
  builder-correction drift Track 4 hit last milestone.

## Principles touched (foreclosure clause)

- **Honest blocking → honest confinement:** the boundary must *prevent* the
  crossing where it credibly can, and where it can only detect, it says so
  plainly (the in-repo/owner-attested line). No control is claimed stronger
  than it is.
- **Fail-closed:** every confinement path fails closed; a fail-open is a
  blocking data-safety defect, never a usability trade-off.
- **The repository provably carries zero personal data:** unchanged and
  binding; strengthened from *scanned* to *credential-confined* on the
  transport leg.
- **Trace over answer:** a blocked push is walkable — the guard says *why* it
  refused (which surface, which marker class), not an opaque failure.
- Exceptions auto-escalate to Tier 3 per the standing protocol.
