# Role Template: Foreman — retired (tombstone)

**Retired 2026-07-20.** This file no longer carries doctrine. Its content has
been consolidated into canonical homes so there is a single source for each
piece; nothing is lost. The path is retained (not deleted) only because closed
pre-2026-07-14 prototypes reference it as the source their `roles/foreman.md`
was specialized from — those historical records stay truthful.

Where the content went:

- **Prototype-foreman doctrine** (role definition, scope-and-economy
  stewardship, the optional clerk, external-builder handoff, log hygiene during
  open rounds, foreman succession) → `PROJECT_PLANNING.md`, *Prototype-Driven
  Decisions*.
- **Economic gates and the Gate-4 Markdown caps** (recalibrated 2026-07-16) →
  **ADR-0013** (the caps are now the "2026-07-16 recalibration" amendment; the
  gates are its Decision).
- **Milestone role seeds** (the seat you actually boot from for milestone work)
  → `docs/roles/` — `foreman.md`, `builder.md`, `reviewer.md`, `clerk.md`
  (advisor: `docs/roles/advisor.md`, ADR-0040).

Why it was retired: sub-agent dispatch (ADR-0034) made per-seat committed role
files redundant, so the practice of copying this template into
`docs/prototypes/<topic>/roles/foreman.md` lapsed after 2026-07-14. Keeping a
live-doctrine copy here duplicated ADR-0013 and `PROJECT_PLANNING.md` and had
already drifted (it was the sole home of the recalibrated caps). Single-sourcing
removes that drift surface.
