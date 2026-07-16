# Confirmation Pass — Locator Screen (ADR-0031 Decision 5)

Seat: scoped confirmation reviewer (Medium), independent context. Mandate
(ADR-0013 2026-07-15): Decision 5 closed an adversary **under-inclusion** finding
(A2 — a fixed 3-prefix denylist under-catches a novel root); this pass tests the
**opposite direction, over-inclusion** — does the provenance/allow-list screen
wrongly reject legitimate `MAY_CROSS` content? All examples synthetic. Read:
ADR-0031 (Decisions 2,4,5,6,7 + Confirmation pass), `adversary-r1.md` A2,
`governance-r1.md` M6, both builds' locator sections, Constitution Art. 18,
Ontology §8/§sensitivity-inheritance.

Decision 5 as written denies "any absolute-path or private-locator form ... unless
it matches a declared permitted synthetic-path grammar." The screen is rule 2 of
it2 §2's ordered classifier and runs **before** the rule-3 `contract`/`code` kind
check — so a declared kind does not exempt it.

## Case 1 — Contract prose quoting a denied form — **OVER-FIRES** (acute)
Verified grep: ADR-0031 Decision 5, `charter-it1.md`, `charter-it2.md`, this
charter, `adversary-r1.md`, and `it1/design.md` each carry bare `/Volumes/…`,
`/mnt/…`, `\\host\share`, `/Users/` tokens **as quoted examples of forms to deny**.
A form-only allow-list cannot separate a *live locator* from a *mention of a
locator form*, so every one of these CONTRACT-class docs classifies
`NEVER_CROSSES` at rule 2. The screen denies **its own contract material** —
ADR-0031 could not itself be committed or pushed under the rule it declares.
Self-defeating; decision-blocking for ratifiability.

## Case 2 — Code/CI/container paths — **OVER-FIRES**
`#!/usr/bin/env python3` shebangs, a CI runner workspace (`/github/workspace`), a
container mount (`/mnt/…`) are public, non-personal `code`-kind paths that must
cross. None is in a reserved *synthetic-demo* grammar, so "deny all absolute forms
outside the synthetic grammar" rejects them. Sharper: `/mnt/…` is
**simultaneously** a legitimate container mount (must cross) and the adversary's
named denied residency form (must deny `/mnt/tax-live/JQP.pdf`). A screen keyed on
**path form alone cannot separate them** — the true discriminator is provenance
(does the token resolve to owner-local `L`?), not the string.

## Case 3 — Synthetic fixture path from the permitted grammar — **HOLDS**
A fixture/golden bearing a reserved synthetic path that is a declared member of the
grammar is the allow-list's positive case: `MAY_CROSS`. No over-fire, provided the
grammar is actually declared (it2 §D1-P2 reserved demo domains). Clean.

## Case 4 — Path outside both real roots and the synthetic domain — **HOLDS**
A novel absolute root that is neither a known real root nor in the reserved
synthetic set denies. Intended behavior, not over-fire, and **deterministic** —
membership in a declared grammar is a pure predicate, no judgment.

## Case 5 — Under-inclusion regression on fresh clone/CI — **HOLDS**
A novel real root `/Volumes/…` on a fresh clone with no runtime locator and no env
is not a grammar member → denied. The screen does not consult the runtime pointer
value, so a fresh clone/CI enforces the identical rule (closes A2). The
under-inclusion fix is **not weakened**.

## The crux
Cases 4–5 hold for exactly the property that makes Cases 1–2 over-fire: "deny every
absolute form outside the synthetic grammar, with no runtime dependence." A pure
**form** allow-list cannot serve the use/mention line (Case 1) or the
public-path/residency-form collision (Case 2); the load-bearing discriminator is
**provenance** (rule 1) + **no-committed-locator** (Decision 4), which Decision 5
restates as a form net and thereby over-broadens.

A *class-scoped* privilege ("any CONTRACT doc may quote any absolute path") reopens
the leak — a real locator rides in disguised as an "example" (the incumbent's
rejected R4b). The safe privilege is **structural**: contracts draw denied-form
illustrations from a **declared, fixed, non-resolvable reserved illustration
domain** that is itself a grammar member; membership is a predicate, so a live
`/Volumes/tax-live/…` — not a member — still denies (Case 5 preserved).

## Verdict — NOT ratifiable as written; needs a named amendment
Decision 5 over-fires on Cases 1 and 2, including on the ADR text that declares it.
Minimal precise change:

1. **Re-scope the screen from "any absolute-path form" to "private-locator /
   owner-local-resolvable form."** Public system/CI/container roots are out of
   scope; the residency threat is a token that could resolve to `L` (Decision 4,
   rule 1) — not every absolute string. (Fixes Case 2.)
2. **Add a bounded declaration privilege:** a `contract`/`code`-kind artifact may
   contain a denied-form token **only if** it is a member of a **declared reserved
   illustration/public-path domain** (fixed, non-resolvable enumeration, part of
   the permitted grammar); any token outside that set still denies, regardless of
   kind. Licenses quoted **forms**, never a resolvable owner-local path. (Fixes
   Case 1 without reopening the R4b leak; Case 5 intact.)
3. **Consequential:** ADR-0031, the D1 charters, and the reviews re-draw their
   `/Volumes/…`/`/mnt/…`/`\\host\share` illustrations from that reserved domain, or
   the gate rejects them.

The amendment does not touch rule 1 (provenance) or Decision 4 (no committed
locator) — those remain the primary walls; the re-scoped screen is defense-in-depth
over them, the only role a form net can safely hold.
