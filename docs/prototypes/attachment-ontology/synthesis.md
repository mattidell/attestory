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

1. **Completeness is presence-semantics, encoding pinned (revised after
   confirmation round 1).** Part III answers are **categorical declared
   facts** on the existing taxpayer-assertion pattern — value domain
   `{yes, no}`, never boolean — and completeness is: *every required answer
   exists as a current finding*, evaluated unconditionally per answer
   (presence, not truthiness; a `no` is a present answer). Branch content
   requirements read the *value* only after presence holds: a `yes` on
   foreign-account adds 7b country to the required set and names the
   FinCEN-114 obligation (never produces it); a `yes` on foreign-trust
   likewise. No evaluation order can mask an answer, because presence of
   each required fact is checked independently before any value is read.
   Every answer finding is pinned unconditionally, whatever its value.
2. **Supersession posture:** the attachment's pins include every Part III
   answer and every row-source fact; a superseded pinned fact makes the
   attachment non-current exactly as any derived finding (ADR-0010
   currency). A late-contributed answer supersedes the *blocked* disposition
   through the normal re-run, never edits it.
3. **Row pinning via `collect_members`** — a **named new mechanism**
   (production condition, Track 1/2): the itemization rule collects the
   member findings of the same closed family, at the same horizon, that the
   line's subtotal collected; each row pins its member finding id.
4. **Tie-out as a NEW named invariant (revised after confirmation round
   1 — no committed-vocabulary claim).** The declared relation — the
   itemization's row-sum equals its line's published value, same closed
   family, same horizon — is enforced by a **new mechanism** this ADR
   names and Tracks 1–2 build: a derivation-time check with its own new
   error code (working name `ITEMIZATION_TIE_OUT_VIOLATION`), added to the
   record and walk vocabularies by schema version, whose violation hard-
   fails the attachment derivation (never publishes a divergent form,
   never blocks the line). Confirmation round 1 established that no
   committed path expresses this; it is therefore an explicit production
   condition, stated as unbuilt contract text, with both divergence
   directions (stale row set, stale line) named as its kill-tests.

5. **Error-vocabulary reconciliation (carried, not resolved here).** A real
   pre-existing discrepancy exists on `main`: the runner *emits*
   `SOURCE_SET_UNCLOSED` while the committed record/walk enums permit
   `SOURCE_SET_OPEN` (adversary A6; confirmed against source in
   confirmation round 1). This synthesis takes no position on which name
   wins; the ADR carries it as a named production condition — reconcile
   emit and record layers by versioned schema change — and the foreman has
   flagged a standalone repair track as an owner option, since the defect
   predates and exceeds this milestone.

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
   whole. The presence check must not over-trigger.
2. Each answer absent individually → blocks, naming exactly that fact.
3. Not-required is an atomic disposition — resolves G1 without a state
   field; ADR-0012 atomicity holds.
4. Tie-out divergence both directions (stale row vs stale line) → hard
   error, committed-consistent semantics.
5. Supersession both ways (late answer; superseded answer under a current
   attachment) → currency behaves per ADR-0010.
6. Generalization: the synthesized citizen expresses the Schedule D stub
   with zero Schedule-B-specific surface.
