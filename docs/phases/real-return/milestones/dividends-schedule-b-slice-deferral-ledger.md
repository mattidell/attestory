# Dividends and Schedule B Slice — Deferral Ledger

Audience: Shared (status); Product (planning input)

Written 2026-07-21 as the Track 5 completion record. Every deferral this
milestone created or re-affirmed, so that nothing is silently closed. Each
entry names its origin, why it was deferred, and what reactivates it. This
ledger *records*; retiring an entry is future milestone work (an entry is
retired by naming this ledger in the retiring track's review). Entries
carried forward from the prior milestone's ledger
(`first-real-return-slice-deferral-ledger.md`) are marked **carried**, with a
disposition note on whether this milestone touched them.

## Boundary and infrastructure (carried)

1. **Guarded transport / credential confinement** — carried, **touched and
   not retired** by Push-Envelope Preflight and Bypass Visibility (PR #45,
   2026-07-22).
   ADR-0031's "remote credentials reachable only through the guarded push
   path" remains not implemented. The rescope's synthetic audit makes that
   absence explicit (`credential_confinement: unestablished`); it does not
   provide a credential wall or alter the L3 row. Still the ledger's
   highest-priority entry; it alone holds the data-boundary row short of L4.
   Reactivate: a separately chartered OS, identity, or hosted-boundary topic.
2. **Operator-level bypass is detected, not impossible** — carried, **touched
   and re-affirmed, not retired** by Push-Envelope Preflight and Bypass
   Visibility (PR #45, 2026-07-22). The new audit drives a synthetic marker
   through actual local Git commands and reports `git push --no-verify` as
   bypass-reachable. That is visibility evidence only: raw transport remains
   possible and the per-clone byte-verification still detects hook deletion or
   tamper only when the audit/gate runs. Reactivate: owner decision or the
   credential-confinement hardening topic.
3. **GitHub remote stays private** — carried, **untouched**. Standalone
   owner decision to change; not a defect.

## New this milestone: declared-universe scope

4. **Dividend boxes 2a, 3, 5, 7, 12 are named honest-block exclusions.**
   Origin: milestone plan (owner-ratified at plan stage) and ADR-0035 (D3) —
   the declared 1099-DIV universe is boxes 1a/1b only; a return with facts
   in the other named boxes blocks honestly rather than silently omitting
   them. Reactivate: a dividend-breadth milestone that widens the declared
   universe.
5. **Schedule B Part I ties to the box-1/1099-INT family only.** Origin:
   Track 2 charter/commit `2a10f60`, documented as a scope-bounded
   simplification — this milestone's fixtures and declared universe never
   populate more than one interest family, so the tie-out target was never
   generalized to a multi-family sum. (This is distinct from the Track 2 F1
   defect, which was a genuine bug in that same tie-out and was repaired
   before merge — see entry 10.) Reactivate: an interest-breadth milestone
   that admits a second 1099-INT family, or any milestone that must prove
   Schedule B Part I against more than one family.

## Review carries (named by track reviews, not yet built)

6. **Split-registry / bad-checksum corpus fixtures** — carried, **untouched**
   this milestone (no DSBS track touched `release-registry.v1` or the
   resolver corpus). Reactivate: next track that touches either.
7. **Failed-batch record shape unasserted** — carried, **untouched** (no
   DSBS track touched the contribution applicator). Reactivate: next track
   that touches `apply_contribution_batch`.
8. **Marshaller binding-route simplification** — carried, **re-affirmed, not
   retired.** DSBS Track 2 (`2a10f60`) added a fourth binding route to
   `packages/derivation/marshal.py` for `attachment-rule.v1`'s own
   requirement/completeness symbol surface, following the same additive
   pattern the original finding described (every route still reads
   exclusively from `current_findings`, so the off-record property the
   finding cared about continues to hold — not independently re-verified by
   a dedicated reviewer this milestone, since no DSBS track charter named
   this file as its object of review). The simplification opportunity named
   in the original finding is now larger, not smaller. Reactivate: next
   track that touches the marshaller.
9. **Scaffold visibility for fresh checkouts** — new, Track 4 review F2
   (non-blocking). `tools/scaffold_live_acts.py` and `workspace-seed/` are
   intentionally untracked (ADR-0031); a fresh clone or fresh worktree never
   carries the owner's in-progress edits to them, so their current content
   (v6 pin, full dividend/Schedule-B/QDCG template set) lives only in the
   owner's working checkout, confirmed present and correct there but not
   independently verifiable by a reviewer without owner-provided access.
   Not a defect — the untracked posture is the ADR-0031 contract working as
   designed — but a standing operational fact worth naming: the owner is the
   sole custodian of these files' current content. Reactivate: if a fresh
   clone ever needs to reproduce a live run and the scaffold content is
   found stale or missing.

## Contract deferrals (named in ADRs, carried)

10. **Further positive interest sources** — carried, **untouched**. K-1 box
    5 interest and market discount remain outside line 2b's declared
    composition (ADR-0026). Reactivate: an interest-breadth milestone.
11. **Subtractive-adjustment mechanism** — carried, **untouched**. Nominee,
    accrued, and premium adjustments to interest (ADR-0026). Same posture as
    10.
12. **ADR-0028 historical-v1 migration** — carried, **untouched** as a
    migration, though this milestone's Track 1 (review F2) newly relied on
    the same "historical, not current" carve-out: the superseded
    `form1040.line-2b.form-field` v1 instance (schema `form-field.v2`)
    stays published as history and is no longer surfaced as current by
    `load_form_fields()`'s version-rank indexing, now alongside the new v2
    instance (schema `form-field.v3`). Confirms the carve-out generalizes;
    does not migrate anything. Reactivate: hardening milestone or first
    content-migration need.

## Product-surface shims (standing, restated for completeness)

13. **Free supersession policy** — carried, **untouched**. Any actor
    supersedes any finding without restriction; a real correction-authority
    policy is undesigned.
14. **E8.1 UI coverage / human presentation surface** — carried,
    **untouched**, and now the maturity matrix's top content frontier
    (frontier reading below): presentation remains form-field disposition
    content, not a human surface a real user reads directly; citation
    *display* formatting is a deferred rendering contract.

## Explicitly not deferrals

- **Track 2's Schedule B Part I tie-out defect (review F1)** was *repaired*,
  not deferred: the original comparison target (line 2b's full four-family
  sum) was a genuine bug for any filer with interest from more than one
  1099-INT source; the fix narrowed it to the correct box-1 subtotal before
  merge, with a regression golden. Distinct from entry 5's scope-bounded
  simplification, which the fix did not (and could not, under the declared
  single-family universe) change.
- **Track 3's F1 and R1 findings** (rule-file substitution-probe breakage;
  a second Check-10-adjacent defect) were both *repaired* before merge, with
  independent delta re-reviews confirming discharge — no residual.
- **Track 1's F2 vocabulary-reconciliation and F3 universe-guard-scoping
  findings** were *informational*, confirming existing behavior as correct
  and intentional, not defects — recorded in the review, not carried here.
- **Track 4's F1 (`BUNDLE_FILES` scope beyond literal charter text)** was a
  correctly-justified scope reconciliation, not a defect — the two
  additional bundles were required for the scaffold to support exactly what
  the charter's own objective named.
