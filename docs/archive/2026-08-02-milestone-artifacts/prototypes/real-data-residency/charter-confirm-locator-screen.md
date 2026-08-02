# Charter: Scoped Confirmation Pass — Locator Screen (ADR-0031 Decision 5)

Date: 2026-07-16. Single reviewer seat (Medium tier), independent context.
Mandated by ADR-0013 (2026-07-15 amendment): ADR-0031 Decision 5 is a
foreman-authored fix closing an adversary **under-inclusion** finding (a fixed
prefix denylist under-catches a novel absolute root). The confirmation pass must
exercise the **opposite direction — over-inclusion** — before Decision 5 is
ratifiable text.

- **Seat:** confirmation reviewer, Medium tier.
- **Mandate:** determine whether ADR-0031 Decision 5's **provenance/allow-list
  locator screen** (permit only a declared synthetic-path grammar; deny all other
  absolute/private-locator forms) **over-fires** on legitimate `MAY_CROSS`
  content. Do not re-litigate the under-inclusion finding (already settled);
  test the reverse.

## Read

`docs/adr/0031-real-data-residency-boundary.md` (esp. Decisions 2, 4, 5, 6, 7),
`reviews/adversary-r1.md` (Attack 2), `reviews/governance-r1.md` (Measure 6),
both builds' locator sections, and `docs/governance/` (Article 18, Ontology §8).

## Cases to exercise (all synthetic)

Construct legitimate `MAY_CROSS` artifacts that contain an absolute-path or
locator-shaped token and check whether Decision 5 would wrongly reject them:

1. **Contract prose.** A governance/ADR/charter doc that legitimately quotes an
   absolute path in explanation — e.g. this very topic's docs cite `/Volumes/…`,
   `\\host\share`, `/mnt/…` as examples of forms to deny. Does the allow-list
   screen reject the *document that names them*? If so, the screen over-fires on
   its own contract material.
2. **Code/tooling paths.** Source or CI config referencing legitimate absolute
   or build paths (`/usr/bin/…`, a runner workspace path, a container mount).
3. **Synthetic fixture paths.** A fixture or golden that legitimately contains a
   reserved synthetic path from the permitted grammar — must be **accepted**.
4. **Boundary of the grammar.** A path that is neither a known real root nor in
   the reserved synthetic domain — confirm it denies (this is the intended
   behavior, not over-fire) and that the deny is deterministic, not judgment.
5. **Regression on under-inclusion.** Confirm a novel real root (`/Volumes/…`)
   on a fresh clone/CI (no runtime locator) is still **denied** — the fix must
   not have been weakened to avoid over-fire.

## The tension to resolve

If the allow-list denies *any* absolute path outside the synthetic grammar, then
contracts that must *discuss* real path forms (case 1) cannot cross — including
ADR-0031 itself and these very charters. State whether Decision 5 needs a
**declaration privilege** (a bounded exception letting CONTRACT-class docs name
denied forms as quoted examples without carrying a live locator), analogous to
the incumbent's rejected R4b but scoped to quoted non-locator mentions — and
whether such a privilege reopens a leak path. This is the crux: name it.

## Output

Return as your FINAL MESSAGE the complete content of
`reviews/confirm-locator-screen.md` (≤80 lines): each case marked
over-fires / holds, a verdict on whether Decision 5 is ratifiable as written or
needs a named amendment (e.g. a scoped declaration privilege), and — if an
amendment is needed — the minimal precise change. Do not write files or run git
writes; all examples synthetic.
