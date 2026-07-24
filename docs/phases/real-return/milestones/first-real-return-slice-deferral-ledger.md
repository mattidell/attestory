# First Real Return Slice — Deferral Ledger

Audience: Shared (status); Product (planning input)

Written 2026-07-18 as the Track 5 completion record. Every deferral this
milestone created or re-affirmed, so that nothing is silently closed. Each
entry names its origin, why it was deferred, and what reactivates it. This
ledger *records*; retiring an entry is future milestone work (an entry is
retired by naming this ledger in the retiring track's review).

## Boundary and infrastructure

1. **Live-run authority separation and guarded publication transport** —
   ADR-0031's "remote credentials reachable only through the guarded push
   path" is **not implemented**. Origin: named residual of Track 4b (its
   charter re-deferred it explicitly rather than claiming it). Accepted
   ADR-0044 clarified on 2026-07-23 that this entry contains two concerns:
   mechanical Developer/Supply ↔ Live-Run Data separation is the missing
   privacy enforcement that holds the data-boundary row at L3, while guarded
   transport / credential confinement is separate Developer/Supply →
   Publication hardening and cannot raise that row by itself. Today the
   envelope gates scan commit/push content, but credentials are not confined
   to the guarded path and the live domains are not mechanically separated.
   ADR-0044 selects no mechanism, schedule, or priority between future
   milestones.
2. **Operator-level bypass is detected, not impossible** — `git commit
   --no-verify` or hook deletion still works; the per-clone byte-verification
   makes the bypass fail the next gate battery rather than preventing it.
   Origin: Track 4b named residual. Server-side prevention (e.g. GitHub push
   protection) is a standalone owner decision. Reactivate: owner decision or
   the hardening milestone.
3. **GitHub remote stays private** — standalone owner decision to change
   (recorded at Track 3). Not a defect; recorded so the default is visible.

## Review carries (named by track reviews, not yet built)

4. **Split-registry / bad-checksum corpus fixtures** — Track 1 D3 re-review
   F3 (non-blocking, optional hardening): the schema constraints bind (the
   reviewer verified them live) but the committed corpus has no
   split-registry positive example and no bad-checksum or empty-split-map
   negative, so they are not regression-pinned. Reactivate: next track that
   touches `release-registry.v1` or the resolver corpus.
5. **Failed-batch record shape unasserted** — Track 2 review F3
   (non-blocking): `apply_contribution_batch` best-effort-validates its
   `failed` terminal record inside a swallowed exception, and no golden
   exercises the failure path, so a malformed failed record would pass
   silently. Reactivate: next track that touches the contribution
   applicator; the named hardening is a failed-record shape assertion.
6. **Marshaller binding-route simplification** — Track 2 review F4 (quality,
   not defect): `marshal_run_context` carries more binding routes than the
   invariant needs (explicit bindings, source-name collection, a legacy demo
   path); every route reads exclusively from `current_findings`, so the
   off-record property holds. Reactivate: next track that touches the
   marshaller. (Track 2 F1, by contrast, was *discharged* — Track 3's
   evaluator fence closed it; recorded here so its absence is not read as
   silence. Track 2 F2's name-based reflection helper carries the same
   review's suggestion to assert the positive parameter-set invariant if
   kept.)

## Contract deferrals (named in ADRs)

7. **Further positive interest sources** — K-1 box 5 interest and market
   discount are outside the line-2b composition's declared universe
   (ADR-0026). The composition blocks honestly rather than under-claiming.
   Reactivate: an interest-breadth milestone.
8. **Subtractive-adjustment mechanism** — nominee, accrued, and premium
   adjustments to interest (ADR-0026). Same posture as 7.
9. **ADR-0028 historical-v1 migration** — historical v1 content remains on
   the residual floor rather than migrated under the manifest contract.
   Reactivate: hardening milestone or first content-migration need.

## Product-surface shims (standing, restated for completeness)

10. **Free supersession policy** — any actor supersedes any finding without
    restriction; a real correction-authority policy is undesigned.
11. **E8.1 UI coverage / human presentation surface** — presentation is
    form-field disposition content; citation *display* formatting is a
    deferred rendering contract. Reactivate: the presentation frontier
    (maturity-matrix frontier 2).

## Explicitly not deferrals

- **RG-1's eight core-package issues** were repaired in Track 4 per
  ADR-0033's MUST (never allowlisted) — discharged, not deferred.
- **The disposition report as review evidence** was not deferred but
  *corrected away* (2026-07-16, Ontology §8): it stays in quarantine by
  contract, permanently.
