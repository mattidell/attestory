# H1 Repair 1 Charter — Scan-Before-Descriptor Release

Role: **Incumbent repair builder** (High tier). The owner authorized repair
builder dispatch at the foreman's discretion on 2026-07-22. This is the one
repair pass permitted by Gate 4. Work only on branch
`prototypes/guarded-transport-h1/repair1`, based on
`exhibits/guarded-transport-h1/it1`.

## Delta scope

Repair only the incumbent's guard-owned descriptor-release topology. Do not
revive or inspect the rejected rival, change the threat model, add a hosted
service or operating-system identity boundary, change production code, or
modify the plan, seat, process log, ADRs, phase documents, existing reviews,
or another topic. A need for any excluded boundary is a **separate-decision**
conclusion, not permission to add it.

## Required artifacts

Produce only:

1. `docs/archive/2026-08-02-milestone-artifacts/prototypes/guarded-transport/repair1/design.md` — delta design and
   exact credential-discovery inventory.
2. `docs/archive/2026-08-02-milestone-artifacts/prototypes/guarded-transport/repair1/examination-repair1.md` —
   command-backed results for every invariant below, H2/H3 paper record, and
   a proposition-by-proposition conclusion.
3. Disposable probe code only under `prototypes/guarded-transport/repair1/`.

The probe uses only fresh temporary repositories, a constructed marker, local
dummy transport, and a runtime-created non-secret token. It must never contact
a network remote or owner credential store, or commit a personal path,
credential, remote URL, or workspace detail.

## Required invariants

All are mandatory. A failure stops the repair; do not patch around it.

1. **Exact scan before capability release.** The guard must derive the exact
   ref update that its actual local `git push` will attempt, run the same
   outgoing-envelope scanner semantics over it, and receive a clean result
   before it creates, writes, or passes the token descriptor to any Git child.
   `envelope_scan.py --verify` is installation evidence only and does not
   satisfy this invariant. The constructed-marker case must show no descriptor
   creation and no transport invocation.
2. **Complete authoritative-path probe.** A fresh execution must complete:
   clean guarded `git push`; raw `git push`; raw `git push --no-verify`;
   constructed-marker refusal; guard-byte tamper; and missing-install refusal.
   Every raw refusal must be the same descriptor-absent reason, independent of
   any hook. Flush or otherwise make the local transport protocol reliable;
   no timeout or downstream helper-only test qualifies.
3. **Declared same-UID boundary.** Test all stated discovery routes from a
   sibling same-UID process: environment, credential helper, askpass,
   system/global/local config/includes, direct transport, any persistent
   store, and any descriptor path exposed by the fixture. State precisely what
   ordinary sibling-process access is tested and what privileged inspection is
   outside the declared non-malicious process threat. If the topology cannot
   make that boundary honestly without a new OS/identity/hosted boundary,
   report `separate-decision` and stop.
4. **H2/H3 completion at paper level.** Name the selected owner-attested
   server-side backstop and state that no local test proves it. Define an
   implementable E18.1 topology/capability canary and E18.2 seeded-marker
   battery whose assertions include **no credential descriptor exists in the
   Git child before the envelope scan succeeds**. The future Track 2 battery
   may be deferred, but its contract may not be vague.

## Stop and handoff

Commit only the permitted repair artifacts on your branch. Do not push, merge,
rebase, create or move tags, or dispatch/review. Report the commit, every
invariant's result, and whether H1-P1/P2, H2-P1, and H3-P1 are settled,
blocked, deferred, or a separate decision. If any invariant fails, preserve
the failure evidence rather than attempting another repair.
