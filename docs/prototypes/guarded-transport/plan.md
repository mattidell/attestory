# Prototype Plan: Guarded Transport and Credential Confinement (H1)

Audience: Agents

Status: **approved by owner 2026-07-22.** Track 0 of the Guarded Transport and
Credential Confinement milestone. The parent milestone and this separate plan
are approved; the owner also authorized the plan's builder dispatches on
2026-07-22. It operates under ADR-0030 per-decision merges and ADR-0034
per-dispatch approval.

Topic: **How the remote credential and the outgoing transport are confined so
that the guarded path is the only credentialed route.** The required property
comes from ADR-0031; this topic decides the shape that can prove it without
placing a real credential, remote, or quarantined-workspace detail in the
repository.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing |
| --- | --- | --- |
| H1-P1 | Credential-confinement topology: which component alone may obtain or release a remote credential, and how the authoritative guarded-push entrypoint invokes the existing envelope scan before it can invoke transport. | Primary, Tier 3 |
| H1-P2 | Raw Git posture: the clone has no independently reachable credential path, so `git push` and `git push --no-verify` fail closed rather than bypassing a hook. | Tightly dependent secondary, Tier 3 |
| H2-P1 | Prevention versus residual detection: the named server-side backstop and the written boundary between synthetic in-repo proof and owner-attested remote configuration. | Dependent Tier 2; Gate 2 may settle it at paper level |
| H3-P1 | Audit surface: the E18.1 capability/topology canary and E18.2 seeded-marker kill-test contract, including the complete bypass-surface inventory. | Tier 2 implementation contract; Gate 2 may settle it at paper level |

Out of scope: tax content, the out-of-repo residency rule itself, a hosted
service, malicious-owner exfiltration, real credentials, real remotes, and
server controls beyond the selected backstop. H2/H3 must not enlarge H1; a
finding that requires a new server or identity boundary becomes a separate
decision.

## Gate 1 — Eligibility

| Proposition | Blast radius | Migration cost | Residual paper uncertainty | Cannot test cheaply | Total | Outcome |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| H1-P1/P2 | 2 | 2 | 2 | 2 | 8 | Prototype-eligible; the real Git credential-discovery path must be tested, not inferred from a wrapper diagram. |
| H2-P1 | 2 | 1 | 1 | 1 | 5 | Paper spike plus owner-attestation boundary; share H1's evidence only where it bears on the line. |
| H3-P1 | 2 | 1 | 1 | 1 | 5 | Paper spike; implementation acceptance is the later kill-test battery, not a prototype production build. |

## Gate 2 — Paper evidence

Both clean-room builders must answer the same synthetic cases. A `demo-token`
or local test endpoint is a non-secret test double only; neither a real
credential nor an owner remote may appear in a fixture, command transcript,
or artifact.

1. **Clean guarded push.** Starting from an installed clone with no raw Git
   credential configuration, show the sole supported command invoking the
   byte-verified envelope battery and only then receiving a `demo-token` for a
   local transport fixture. Name each credential discovery mechanism that is
   absent or neutralized.
2. **Raw-push refusal.** Run `git push` directly against the same local
   fixture. It must fail because no credential is reachable, not because a
   pre-push hook happened to run. Repeat with `git push --no-verify`; the
   failure reason must be unchanged.
3. **Seeded-marker refusal.** Put a constructed synthetic residency marker in
   the outgoing commit envelope. The guarded entrypoint refuses before any
   credential release or transport invocation. The test distinguishes a
   scanner refusal from a remote-side rejection.
4. **Credential-read refusal.** From a process outside the guarded entrypoint,
   attempt each declared discovery route (environment, configured credential
   helper, askpass, config include, and wrapper-private store). It cannot
   obtain the `demo-token`; an unknown or unenumerated route is a failure of
   the topology inventory, not an assumed-safe omission.
5. **Tamper and lifecycle trace.** Install → verify byte identity → guarded
   clean push → alter a guard-owned byte or remove the confinement install →
   guarded push fails closed until repaired. State whether a newly cloned
   repository has a safe default before installation and how the standard
   verification floor makes absence visible.

For every case, provide a producer → authority → consumer → failure map. If
paper identifies one topology that meets all five cases and the local Git
probe falsifies no discovery path, stop; do not climb to a real remote.

## Gate 3 — Evidence depth per question

The currently authorized rung is **Rung 1 plus one Rung-2 throwaway local Git
probe**. The sole climb question is: *can the chosen confinement shape make
the actual Git transport require a guard-owned test credential while raw Git,
including `--no-verify`, has no alternative discovery route?* The probe uses a
fresh temporary repository, a local dummy transport/askpass fixture, and a
constructed marker. It never contacts a network remote or reads an owner
credential. Rung 3/4 are not authorized: production code and any owner remote
belong after an accepted ADR and in the milestone's implementation/live tracks.

## Gate 4 — Cost caps

- One bounded build round: an incumbent and a **sealed clean-room rival**,
  each resolving all five cases and the one Rung-2 probe.
- At most one owner-authorized repair pass; a repair is delta-scoped to a
  named finding. A foreman-authored repair requires the ADR-0013 confirmation
  pass.
- Two independent reviewers after the build round. Repairs use delta review
  unless the contract surface changes.
- Builder and review documents stop when the declared cases, propositions,
  rung, and measurements are fully reported; no line cap applies.

## Gate 5 — Triage

Decision-blocking: any raw credential route, a `--no-verify` path that can
transport, a guard that releases the token before the envelope passes, an
unnamed credential-discovery mechanism, a test that does not drive actual Git
transport, or a claim that server-side control proves an in-repo property.
Production conditions: installer byte verification, ergonomics, and the final
E18.1/E18.2 battery. Separate decision: any required hosted service, hardware
credential, or remote policy beyond H2. Deferred breadth: malicious-owner
controls and non-Git publication channels. Non-blocking defects are logged and
fixed only within the authorized repair pass.

## Gate 6 — Minimum converged subset

The minimum ratifiable H1 subset is one topology with a named sole credential
holder/releaser, an authoritative guarded Git command, and a complete local
credential-discovery inventory. It must demonstrate: a clean guarded local
push; raw and `--no-verify` refusal due to absent credential; marker refusal
before credential release; and out-of-path credential-read refusal. H2 must
state the owner-attested server backstop and its non-provable boundary; H3 must
name an implementable E18.1/E18.2 battery. Anything less does not discharge
ADR-0031's guarded-transport condition.

## Gate 7 — Production boundary

Only plan, charter, examination, review, process-log, and evaluation documents
merge from this topic. Accepted conclusions become one proposed Tier 3 H1 ADR
(and a Tier 2 H2/H3 ADR only if Gate 0 establishes an independent contract),
reviewed and owner-ratified through ADR-0030. Prototype code remains an
exhibit. Track 1 reimplements the accepted shape; Track 2 implements its
adversarial battery; Track 3 owns the owner-only live attestation and records.

## Gate 8 — Roles

| Role | Tier | Reason |
| --- | --- | --- |
| Prototype foreman | High | Security-boundary scope triage and evidence-ladder enforcement. |
| Incumbent builder | High | Must trace real Git credential discovery without mistaking a hook for confinement. |
| Rival builder | High | Clean-room competing topology over the identical local fixture contract. |
| Governance reviewer | Medium | Measures ADR-0031 and governance conformance, evidence boundaries, and the claimed/provable split. |
| Adversary reviewer | High | Attacks bypasses in Git credential discovery, `--no-verify`, and release ordering. |

Each builder and reviewer remains unassigned until the owner approves the
specific current charter for that role under ADR-0034. The user's 2026-07-22
authorization is recorded as direction to proceed, not substituted for that
required charter-specific checkpoint.

## Review measurements

Governance measures whether every conclusion preserves ADR-0031's directional
capability wall, distinguishes prevention from detection, names the
in-repo-versus-owner-attested line, and uses no real secret or residency data.
Adversary independently attempts the five Gate-2 cases plus a configuration
precedence attack (system/global/local config and environment overrides), a
credential-helper/askpass substitution, a direct transport invocation, and a
guard-byte tamper. A result is pass, fail, or not-run with the command or
static evidence that produced it; an impression is not a review.

## Data safety

All paths, tokens, repository names, markers, and transport endpoints are
constructed synthetic test data. A test must never call an owner remote, read
or write the owner credential store, reveal a workspace location, or include a
literal personal-path marker that the envelope scan would identify. Test
markers are assembled from fragments where necessary, following
`tests/test_envelope_hooks.py`.
