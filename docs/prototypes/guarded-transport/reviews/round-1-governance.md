# H1 Round 1 governance review

Role: Governance reviewer (Medium tier)  
Status: completed 2026-07-22  
Charter: `charter-review-governance-r1.md`

## Scope and method

This review considered only the sealed incumbent exhibit
`1255b2732971c11ed0a5b4b012df7a4159c9b105` and sealed rival exhibit
`95b232f40aac90d81b9237c86b2b598764396d2c`, at the paths named in the
charter. Evidence below is from those exhibits' design, examination, and probe
files, plus the cited ADR-0031 / E18 contract. No parent branch or
owner-excluded similarly named feature work was consulted.

`pass`, `fail`, and `not run` describe the stated measurement, not an
alternative-selection judgment.

## Measurements

| Measurement | Incumbent (`1255b273`) | Rival (`95b232f`) |
| --- | --- | --- |
| 1. ADR-0031 boundary fidelity | **pass** — the ordinary direct `git push` and `git push --no-verify` receive no `GUARD_TOKEN_FD`; the sealed examination records the same descriptor-absent refusal for both. The design also expressly separates that accidental/raw-process case from a malicious credential owner. The unresolved inherited-descriptor question is measured separately below. | **fail** — `it2/design.md` and `examination-it2.md` show a same-UID process reading the mode-600 executor store. That process can reconstruct the released environment and a credentialed invocation, so the executor is not the sole effective releaser. |
| 2. Capability claim | **not run** — the direct-helper probe establishes only that a newly launched helper does not inherit the descriptor. The pipe is deliberately inherited by the guard's Git child; the exhibit does not test whether a stated same-UID peer can acquire that child's descriptor or otherwise obtain the dummy capability. It does establish no persistent mode-bit-protected store. | **fail** — `probe.sh` runs `cat "$state/credential"` as the same UID and prints the explicit failure result. Unix mode 600 is therefore correctly rejected as confinement. |
| 3. Authoritative surface | **fail** — direct raw and `--no-verify` refusal do drive actual Git transport, but the ordering claim fails. `guarded_push()` calls `envelope_scan.py --verify`, then creates/writes the token pipe and passes it to `git push`; `--verify` only verifies hook bytes. The actual outgoing-envelope check is the installed pre-push hook's `envelope_scan.py --push`, which runs after Git has inherited the token descriptor. The receipt count proves the helper did not *consume* the token, not that the guard withheld/released no capability before the envelope passed. | **pass** — `probe.sh` invokes `envelope_scan.py --range` before it reads the synthetic store, writes the release log, or invokes `git push`. Its raw and `--no-verify` cases invoke the actual ext transport and fail for absent release variables, independent of hooks. This does not cure Measurement 2's same-UID store route. |
| 4. Honest proof boundary | **fail** — H2 is honest: it names an owner-attested GitHub backstop and says the no-network probe proves no hosted control. H3 is not yet an adequate E18.1/E18.2 form for this topology: its E18.2 receipt assertion observes transport consumption, while Measurement 3 shows descriptor release already occurred; Track 2 is deferred rather than supplied with a no-release-before-envelope-pass canary. | **fail** — it correctly says its local receive-pack proves neither server prevention nor owner configuration, but it does not name the owner-attested server backstop required by Gate 6. Its H3 text defers a later battery rather than stating an E18.1/E18.2 evidence form that could be implemented against a selected topology. |
| 5. Data/process conformance | **not run** — dummy-only material, constructed markers, local fixtures, and no real remote, credential, personal source, or owner path are evident in the sealed files; their Rung-2/prototype boundary also conforms to the plan. Clean-room separation itself cannot be confirmed from these three sealed files alone. | **not run** — dummy-only material, constructed markers, local fixtures, and the prototype boundary are evident. Clean-room separation itself cannot be confirmed from these three sealed files alone. |

## Decision-blocking findings

1. **H1-P1/P2 incumbent — Measurement 3 failed.** The incumbent releases the
   token capability to the Git child after hook-byte verification but before
   the actual outgoing-envelope scan. This is the plan's explicit Gate-5
   blocker: “a guard that releases the token before the envelope passes.” A
   pre-push hook may prevent the remote helper from consuming the pipe, but it
   cannot turn an already-inherited descriptor into an unreleased capability.

2. **H1-P1/P2 rival — Measurements 1 and 2 failed.** The rival demonstrates a
   same-UID read of its executor-private store. Its own stated result correctly
   blocks the sole-holder/releaser proposition; mode bits are not a distinct
   credential authority.

3. **Gate-6 H2/H3 minimum — Measurement 4 failed for the round as a whole.**
   The incumbent supplies an honest H2 attestation boundary but not an adequate
   no-release E18.2 form; the rival supplies neither the required named
   owner-attested backstop nor a selected E18.1/E18.2 form. Neither result
   claims that the local dummy transport proves remote configuration, which is
   correct, but the required paper evidence remains incomplete.

## Non-blocking evidence boundary

The incumbent's inherited descriptor has a narrower demonstrated claim than
its broad local-process wording: the probe proves absence in ordinary new raw
Git/helper processes, not acquisition resistance against an inspected or
otherwise privileged same-UID peer of the credentialed Git child. This review
does not infer either safety or unsafety beyond that unrun test.

Both exhibits keep real credentials, remotes, residency details, and personal
material out of the repository. Neither local probe is evidence of a real
server configuration or real credential boundary.
