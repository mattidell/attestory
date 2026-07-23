# H1 Round 1 Governance Review Charter

Role: **Governance reviewer** (Medium tier). The owner authorized this review
dispatch on 2026-07-22 as part of the approved Track 0 plan. Work only on
branch `prototypes/guarded-transport-h1/review-governance-r1`.

## Object under review

Review these exact sealed exhibits, not their parent branches and not the
owner-excluded similarly named feature work:

- Incumbent: `1255b2732971c11ed0a5b4b012df7a4159c9b105`
  (`docs/prototypes/guarded-transport/it1/{design.md,examination-it1.md}` and
  `prototypes/guarded-transport/h1_it1_probe.py`).
- Rival: `95b232f`
  (`docs/prototypes/guarded-transport/it2/{design.md,examination-it2.md}` and
  `prototypes/guarded-transport/it2/probe.sh`).

Use `git show <commit>:<path>` or isolated temporary checkouts; do not alter
either exhibit. Your output is only
`docs/prototypes/guarded-transport/reviews/round-1-governance.md`.

## Measurements

Report `pass`, `fail`, or `not run` for each, with direct evidence.

1. **ADR-0031 boundary fidelity.** Does each topology distinguish a
   non-malicious accidental/local-process attempt from a malicious credential
   owner, and does it actually make raw Git lack the credential rather than
   merely relying on a skippable hook?
2. **Capability claim.** For each claimed sole-holder/releaser, enumerate the
   credential-discovery routes and decide whether the stated same-UID local
   process can obtain the dummy capability. Do not accept mode bits alone as
   confinement. For inherited descriptors, state precisely what the probe does
   and does not establish.
3. **Authoritative surface.** Verify that every claimed result drives actual
   `git push`; that the guard invokes the envelope check before release; and
   that direct `git push` plus `--no-verify` fail for the same absent-capability
   reason.
4. **Honest proof boundary.** Check H2's owner-attested server-control line
   and H3's proposed E18.1/E18.2 evidence form. Reject any claim that a local
   dummy transport proves a server configuration or real credential boundary.
5. **Data/process conformance.** Confirm dummy-only material, no personal
   paths/secrets/remotes, clean-room separation, correct prototype-versus-
   production boundary, and scope conformance to the plan.

Do not redesign, repair, or adjudicate between alternatives on preference.
Identify decision-blocking findings by proposition and cite the exact failed
measurement. Commit only the review file, do not push or merge, and report the
commit id.
