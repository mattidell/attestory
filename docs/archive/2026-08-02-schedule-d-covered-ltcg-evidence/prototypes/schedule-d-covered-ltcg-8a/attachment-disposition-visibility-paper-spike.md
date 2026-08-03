# Paper Spike — Attachment Disposition Visibility

Audience: Owner, Foreman.

Date: 2026-08-02. Builder-run, Rung 1 paper only, per
`docs/reviews/charter-2026-08-02-attachment-disposition-visibility-decision.md`.
No committee review — Gate 1 totals 5 (paper-spike-plus-ADR-draft rung),
matching the ADR-0055 and CA-05/CA-06 precedent already used twice on this
milestone, and lower-uncertainty than ADR-0055 was: the shape to mirror
(`_resolve_field_row`'s blocked disposition) already exists and is proven in
production, not newly invented.

## Why this exists

Track 3 (`ef921d4`) landed a charter-stop finding: `_resolve_attachment` in
`packages/derivation/presentation_projection.py` returns `None` for both the
`inapplicable` (not-required) and `blocked` (required-and-incomplete)
attachment dispositions. Only `published` (required-and-complete) ever
produces a `citationGroups` entry, and `citation-walk.v1.html` only ever
iterates `MODEL.citationGroups`. A blocked or not-required Schedule D
attachment is therefore completely invisible on the rendered page: no
signal it exists, is required, or is blocked, and — for a `blocked`
attachment — no missing/violated reason shown at all, even though the
`derivation-record.v4`/`npe-walk.v3` ledger (ADR-0055) already carries the
exact missing/violated codes needed to render it honestly.

This is a pre-existing gap, not introduced by Schedule D: Schedule B's
attachment (`attachment-rule.v2`) has always used the same `_resolve_attachment`
function, but every committed Schedule B golden apparently only ever
exercises the `published` path, so the gap never surfaced until Schedule D's
own goldens (Track 2/3) hit the `blocked`/`inapplicable` states for the
first time on this milestone.

## Producer → authority → consumer → failure map

- **Producer.** `_Run.attempt_attachment` in `packages/derivation/runner.py`
  (ADR-0036/0053/0055) already records the full disposition ledger for an
  attachment citizen: `published` (required-and-complete, with itemization
  pins), `blocked` with an exact code (`DEPENDENCY_ABSENT`,
  `ITEMIZATION_TIE_OUT_VIOLATION`, or `COMPLETENESS_VALUE_VIOLATION`) and a
  `missing` list naming every absent or violated answer, and `inapplicable`
  with `guard_result: false` (not-required).
- **Authority.** `build_presentation_model` in `presentation_projection.py`
  reads that same disposition ledger via `_resolve_attachment`. Its
  three-way branch (`if row["disposition"] == "inapplicable": ... return
  None` / `if row["disposition"] == "blocked": return None` / the published
  path builds `{id, title, parts}`) discards the ledger's own missing/
  violated information for two of the three states before it ever reaches
  the model.
- **Consumer.** `citation-walk.v1.html`'s render loop:
  `for (const group of MODEL.citationGroups || []) { ... renderCitationGroup
  ... }`. Since `_resolve_attachment` already returned `None` for the
  blocked/not-required cases, `build_presentation_model`'s own list
  comprehension (`if group is not None: citation_groups.append(group)`)
  never adds them — the renderer's loop simply has nothing to iterate for
  that attachment. Contrast `renderLine`, the field-row equivalent: its
  `blocked` branch renders a `role="alert"` banner naming
  `resolved.activeCodes`, filtered against the field's own declared
  `dispositions.blocked.codes` — the shape and rendering path this gap
  needs, already built and proven for every numeric/categorical field.
- **Failure.** A required-and-incomplete or not-required Schedule D
  attachment renders **nothing** — not a redacted placeholder, not a
  generic "unavailable" banner, not even a page-error signal. This is
  strictly worse than a bug that shows a wrong value: it is silent omission
  of a citizen ADR-0036 Decision 1 defines as one that "publishes a
  walkable inapplicability disposition... never silence," now violating
  ADR-0046 Requirement 2 ("a blocked line shows what fact is missing and
  the remedy, never a value") for the one citizen whose entire purpose is
  that honest account.

## Two positive instances (paper, unaffected baseline)

**P1 — published attachment renders correctly today.** Schedule D eligible
and complete (Track 3's `eligible` golden): `_resolve_attachment` returns
`{id, title, parts}`, `citationGroups` carries it, `citation-walk.v1.html`
renders the itemization parts with working citations. Confirmed by Track
3's coordinator/harness evidence (`ef921d4`); this paper spike changes
nothing about this path.

**P2 — Schedule B's own published attachment, unaffected.** The existing
`attachment-rule.v2` (Schedule B) published case uses the identical
`_resolve_attachment` published branch; nothing in this spike's proposed
shape touches that branch's existing behavior.

## Two negatives (paper, the gap)

**N1 — not-required attachment renders nothing.** Eligible family
closed-empty (Track 3's `not-required` golden): `row["disposition"] ==
"inapplicable"`, `guard_result` is `False` → `_resolve_attachment` returns
`None` → no `citationGroups` entry → the page shows no Schedule D section
at all. Arguably lower-severity than N2 (there is no missing fact to name
for "not required"), but still a silent omission a real filer might
reasonably expect a confirming "Schedule D: not required" signal for,
rather than the form simply never being mentioned.

**N2 — required-and-incomplete attachment renders nothing, including the
new ADR-0055 violation.** Eligible family closed-nonempty with a violated
or missing boundary declaration (Track 3's `violated-declaration` /
`missing-declaration` goldens, exercising `COMPLETENESS_VALUE_VIOLATION`
and `DEPENDENCY_ABSENT` respectively): `row["disposition"] == "blocked"` →
`_resolve_attachment` returns `None` → no `citationGroups` entry. The
numeric lines (`line-7a`, `line-8a-h`, etc.) still correctly redact via
their own independent `selected-preferential-base` completeness check
(Track 2/ADR-0055), so no wrong number reaches the page — but the
attachment's own walkable account of *why* Schedule D itself is incomplete,
including the exact violated declaration and its value, is entirely
absent. This is the highest-severity instance: ADR-0055 built the exact
information this render needs and it currently cannot reach the page at
all.

## Shape evaluation

**Option A — extend the existing `citationGroups` entry with a disposition
field.** Every entry gains `{"disposition": "published"|"blocked"|
"guard_inapplicable", ...}`, mirroring `_resolve_field_row`'s shape
directly onto the existing key. Rejected: this changes the *meaning* of
every existing `citationGroups` entry, past and future — today, membership
in `citationGroups` already implies "published, has itemization parts,"
an invariant an unknown number of existing goldens and any future consumer
may rely on implicitly. Making that implication explicit-but-conditional
(`disposition` must be checked before assuming `.parts` exists) forces
every existing read site, including the ones this milestone did not touch,
to gain a branch it did not previously need — the opposite of "least new
surface," and the more disruptive of the two options for goldens the
charter explicitly protects (Track 3's own regression proof against v1/v6/v8).

**Option B — a new top-level model key for attachment status, disposition-tagged,
parallel to `sections` (recommended).** Add `attachments: [...]` to
`presentation-model.v1`, one entry per attachment citizen regardless of
disposition: `{"id": attachment id, "title": attachment title, "resolved":
{"disposition": "published"|"blocked"|"guard_inapplicable", "activeCodes":
[...], "act": null}}`, mirroring `_resolve_field_row`'s already-proven
shape exactly, including the same `disposition`/`activeCodes`/`act` field
names so the renderer can reuse (not duplicate) `renderLine`'s blocked/
guard_inapplicable branches with minimal adaptation. `citationGroups`
stays byte-identical in meaning and shape — it continues to hold *only*
published attachments' itemization detail, exactly as today, so every
existing consumer, golden, and harness manifest is unaffected by
construction, not by discipline. The renderer gains one new top-level loop
(`for (const attachment of MODEL.attachments || [])`), parallel to the
existing `sections`/`citationGroups` loops, each wrapped in the same
`renderSafely` blast-containment call every other unit already uses — no
new DOM mechanism, no new accessibility pattern, the identical `role=
"alert"` banner and `section-error` fallback fields already use.

**Which state maps to which shape.** A `published` attachment appears in
*both* `attachments` (status: published) *and* `citationGroups` (its
itemization detail) — no information loss, no shape ambiguity, and a
renderer that only understands the old `citationGroups` loop still shows
the published case correctly (forward-compatible degradation, not a
breaking change for any consumer that has not yet adopted the new key). A
`blocked` or `guard_inapplicable` attachment appears *only* in
`attachments`, since there is no itemization detail to show (the tie-out
rows never resolved).

## Recommendation

Option B. It is paper-distinguishable from Option A without a full
prototype round: Option A forces a shape-meaning change onto every existing
`citationGroups` consumer and every already-committed golden; Option B adds
a wholly new, independently-readable key that changes nothing about the
existing one. This directly satisfies the charter's own framing ("state
which better preserves ADR-0046's existing guarantees... with the least new
surface") and Gate 1's residual-uncertainty axis (scored 1, not higher) is
resolved: no paper surprise, no full prototype needed.

Recorded as proposed ADR-0056, an additive successor to ADR-0046 (whose
Requirements/Foreclosures text is not edited in place) and additive to the
`presentation-model.v1` internal shape and `presentation_projection.py` /
`citation-walk.v1.html` — status **proposed**, pending owner ratification
and a subsequent implementation charter (matching the ADR-0055 precedent).
