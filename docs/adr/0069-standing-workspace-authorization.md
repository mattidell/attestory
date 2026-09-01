# ADR 0069 — Standing Workspace Authorization as an Out-of-Kernel Fold with Rule-Scoped Re-Authorization

- Status: **accepted**
- Tier: 2 — the currentness contract production integration depends on;
  not a product-thesis or governance-meaning decision.
- Date: 2026-08-29

## Context

A run's result needs a currentness signal independent of whether the
underlying tax facts happen to be complete: has the taxpayer standing
authorization for this calculation, at all, and does that authorization
still cover what the calculation actually composes today. The only
existing neighboring mechanism, per-family closure, has no taxpayer/year
identity at all, is not "standing" by construction (it expires on every
source-family membership change), and collapses suspension and withdrawal
into simple absence — none of which serves a genuine standing-
authorization contract.

## Decision

1. **A new citizen, decoupled from per-family closure — not a patch on
   it.** The standing workspace authorization is its own entity, granted
   and ended (suspended/withdrawn) by dedicated acts, keyed on at minimum
   `(workspace, taxpayer/subject, tax_year, re-authorization boundary
   digest)`. It shares no chain, horizon, or lifecycle with per-family
   closure, which remains unchanged and continues to serve its original
   purpose (family-membership completeness, not calculation currentness).
2. **An out-of-kernel act-log fold, following the existing
   `derived-publication` precedent — no kernel-registry edits.** The
   authorization fold ignores every act kind it does not own and reads
   the shared act log without registering new entries in the kernel's own
   act-kind/applier tables.
3. **Unconditional taxpayer/year mismatch classification.** A read
   against the wrong taxpayer or wrong tax year is classified as a
   mismatch — a distinct, named disposition from generic absence — based
   solely on `(subject_id, tax_year)` comparison, with no dependency on
   the boundary digest also matching.
4. **Taxpayer-entity supersession is a displacement root.** The fold
   subscribes directly to the real kernel `entity-superseded` act. A
   grant naming a superseded subject entity is inert (a named disposition,
   `AUTHORIZATION_SUBJECT_SUPERSEDED`), and the successor entity does not
   inherit the grant.
5. **The re-authorization boundary is a rule-scoped dependency-closure
   digest, not a whole-adopted-package digest — and it can never fall
   below the entrypoints the run actually executes and publishes.** The
   boundary hashes only the declarations reachable from the specific
   rule(s) a taxpayer's calculation actually composes, rooted at the
   entrypoints the run genuinely resolves and executes. An unrelated
   topic added elsewhere in the adopted package does not change the
   digest and does not force re-authorization; an edit to a rule inside
   the referenced closure does change the digest and does force it. A
   declared calculation scope (Decision 9) may widen this root by union —
   naming further rules a taxpayer's calculation composes — but can never
   replace or narrow it below what the run actually executes and
   publishes: narrowing the authorization boundary without narrowing
   execution would let a run publish output for a calculation outside its
   declared scope while reporting the authorization as current, which
   this contract must never permit.
6. **Ordinary source-family membership changes never touch this
   mechanism.** Member-transition and assertion acts are ignored by the
   fold entirely — this is the property that makes the authorization
   "standing" rather than expiring on every ordinary edit.
7. **Stale scope stays inert.** A grant superseded by a later grant at
   the same identity, or whose boundary digest has drifted from the
   calculation's current closure, is inert and never silently reused —
   preserved by construction (chain/digest comparison, not a time-based
   or best-effort check).
8. **Absence of any authorization act resolves to explicit, non-current
   standing — fail-closed, never silently current.** Authorization
   resolution always calls the fold's resolution function, including when
   the act log has no authorization acts at all; an empty act log yields
   `current=False`, `authorization_status="AUTHORIZATION_ABSENT"` — a
   status distinct from, and never conflated with, a suspended or
   withdrawn grant. A workspace may still be permitted to calculate on
   absent authorization if a future decision names that provisional mode
   explicitly; absence must never itself supply currentness.
9. **A `calculation-scope-declaration` act supplies Decision 5's
   requested-calculation scope, as an out-of-kernel act-log entry — not a
   kernel-projected fact.** Because `run-request.v1` is deliberately
   closed with no value-bearing members (runs consume facts, not
   run-request parameters), the specific rule(s) a taxpayer's calculation
   composes is expressed as an entry on the shared act log: a
   `calculation-scope-declaration` act, keyed on `(subject_id, tax_year)`,
   naming the composed rule ids, folded by the same out-of-kernel,
   compose-over pattern as the grant/end acts themselves. This act never
   enters the kernel-projected fact model — it is not a `Finding`, is
   never addressable from any rule's `when`/`value` expression, and no
   tax computation can read it; it is a derived-state act-log entry
   consumed by one dedicated, non-kernel fold, the same tier of citizen
   as the grant/end acts this fold already owns. The published nested
   citizen is `workspace-calculation-scope.v1` (wrapped by
   `act-calculation-scope-declaration.v1`): a `remove`/`reclassify`-style
   discriminator is unnecessary here since the act kind itself is
   dedicated; the act-log payload-schema selector reads the nested
   citizen's own declared `schema` field to select the correct payload
   version on append and read, so a genuinely-shaped act enters the
   authoritative log rather than only being consumable by a caller that
   bypasses it.
10. **Resolved authorization status reaches the durable record.** The
    resolved authorization disposition (`current`, `authorization_status`,
    `authorization_grant_id`) is persisted to the durable run output file
    and to the production presentation-model root (an optional
    `authorization` object), so a reader of either durable artifact — not
    only an in-memory caller — can recover the standing authority, its
    status, and which grant it came from.

## Production conditions (owed to production implementation; never allowlisted)

- No production caller yet emits `calculation-scope-declaration` acts;
  until one does, every taxpayer's calculation is rooted in the full
  package entrypoint set (a no-op case of the union rule in Decision 5).
  Which caller is responsible for emitting the declaration, and on what
  cadence, is an open owner decision.
- No production caller narrows *execution* to a declared scope — a
  declaration can only widen the authorization boundary today, never
  narrow it, precisely because narrowing the boundary without narrowing
  execution would let the two diverge. A future caller that actually
  narrows execution to the declared scope is open work.
- Fuller cross-product testing of the `AUTHORIZATION_STALE`/superseded-
  grant disposition against real suspend/withdraw histories, beyond the
  covered subcases.

## Consequences

- Production integration charters against a real, evidence-backed
  currentness mechanism instead of an assumed one.
- A future consumer needing calculation currentness scoped to something
  other than taxpayer/year/rule-composition evaluates whether this same
  out-of-kernel-fold-plus-rule-scoped-closure pattern transfers, rather
  than assuming per-family closure could have been stretched to serve.
- Per-family closure (`horizons.py`, `source_authority.py`) is untouched;
  this decision does not redefine, migrate, or deprecate it.
- A declared calculation scope is, today, never able to narrow what a run
  publishes or narrow the authorization boundary below it; it is a
  widen-only refinement, useful only once a caller emits it, and inert
  otherwise. A future decision that wants a declared scope to genuinely
  narrow the authorization boundary must first narrow production
  execution to that same scope — the two can never diverge.

## Alternatives Considered

- **Kernel-registered act kinds for the authorization citizen.** Rejected:
  more invasive than the codebase's own established pattern for exactly
  this kind of derived, non-kernel state; no case here requires
  kernel-level registration.
- **A boundary-gated mismatch diagnostic** (wrong-taxpayer/wrong-year
  degrading to generic `not_authorized` when boundary digests differ).
  Rejected: this is not a rare edge case but the common one, defeating
  the requirement that wrong-taxpayer/wrong-year be a distinct, named
  disposition.
- **A whole-adopted-package-surface digest as the re-authorization
  boundary.** Rejected: over-triggers on an unrelated package addition
  and under-triggers on an in-scope edit — proven wrong on constructed
  counterexamples by direct digest comparison against the correct,
  rule-scoped answer.
- **Patching per-family closure to also carry taxpayer/year identity.**
  Rejected: per-family closure's chain-succession semantics are
  membership-completeness semantics, not currentness-authorization
  semantics; conflating them would make ordinary family-membership
  changes expire the authorization, the exact defect this decision exists
  to avoid.
- **Describing the scope declaration as a kernel-projected fact.**
  Rejected: it is never addressable from `env.sources` or any rule's
  `when`/`value` expression, and no tax computation reads it — calling it
  a "fact" would overclaim what it structurally is.
