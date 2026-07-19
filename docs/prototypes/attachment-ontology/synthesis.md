# Synthesis — Attachment Ontology (D1), foreman-assembled converged shape

2026-07-19. Assembled from reviewer-checked elements of it1 and it2 per
`evaluation-analysis.md`; owner authorized the confirmation pass. This note
is the artifact under confirmation — it is not ratifiable text until the
pass reports.

## The citizen (it1 state model, G1 resolved)

An **attachment disposition** is a derived finding like any line disposition,
published by a declared attachment rule. Its three states are **atomic
dispositions on the ratified triad** — no embedded state field:

- **Not required** → the requirement rule publishes a
  `guard_inapplicable`-family disposition: atomic, walkable (inputs,
  threshold, citation, per-trigger outcome), never silence.
- **Required and complete** → the attachment rule **publishes** the whole
  form content (rows, subtotals, Part III answers), pinned to every consumed
  fact.
- **Required and incomplete** → the attachment rule **blocks** with the
  standard non-publication walk naming each missing contributable fact.
  Sibling line rules cannot reference the attachment symbol (verified
  against committed runner source), so propagation is impossible by
  construction.

## Semantics carried from it2

1. **Completeness is `all(...)`** over every required Part III answer:
   foreign-account AND foreign-trust must each be answered; a "no" is an
   answer; a "yes" on either adds that branch's required content (7b
   country; 7a names the FinCEN-114 obligation, never produces it). No
   answer masks another.
2. **Supersession posture:** the attachment's pins include every Part III
   answer and every row-source fact; a superseded pinned fact makes the
   attachment non-current exactly as any derived finding (ADR-0010
   currency). A late-contributed answer supersedes the *blocked* disposition
   through the normal re-run, never edits it.
3. **Row pinning via `collect_members`** — a **named new mechanism**
   (production condition, Track 1/2): the itemization rule collects the
   member findings of the same closed family, at the same horizon, that the
   line's subtotal collected; each row pins its member finding id.
4. **Tie-out as declared relation:** row-sum must equal the line's published
   value. Violation is a **hard projection error** using the committed error
   vocabulary (`SOURCE_SET_UNCLOSED` family / projection-error path — it2's
   `DEPENDENCY_INVALID` emission is corrected; exact code selection is
   Track-1 content under the committed vocabulary, confirmation case 4
   checks the semantics, not the string).

## Hardening adopted into ADR text

- Row **shape** is per-schedule content; the generic citizen fixes only:
  rows pin member findings, rows subtotal, subtotal ties to a named line.
  (Both builders' payer+amount row model is Schedule-B content, not
  ontology.)
- The requirement conditional is declared rule content over existing
  subtotals; boundary semantics: strictly greater than the cited threshold
  parameter.

## Confirmation cases (charter binds the reviewer to these six)

1. Over-blocking: required + both answers present ("no"/"no") → publishes
   whole. `all(...)` must not over-trigger.
2. Each answer absent individually → blocks, naming exactly that fact.
3. Not-required is an atomic disposition — resolves G1 without a state
   field; ADR-0012 atomicity holds.
4. Tie-out divergence both directions (stale row vs stale line) → hard
   error, committed-consistent semantics.
5. Supersession both ways (late answer; superseded answer under a current
   attachment) → currency behaves per ADR-0010.
6. Generalization: the synthesized citizen expresses the Schedule D stub
   with zero Schedule-B-specific surface.
