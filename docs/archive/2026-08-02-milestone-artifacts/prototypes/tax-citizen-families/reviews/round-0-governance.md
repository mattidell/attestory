# Round 0 Governance Review

Reviewer: codex (resume session, 2026-07-11)
Seat: governance fidelity
Scope: `charter-it1.md` only, as required by `reviews/round-0.md`.
Independence: no same-round peer review or same-round commit-message body was
read before this submission.

## Checks

### 1. Article 1 — peerage and no document-child fact identity

**Check -> result -> exhibit:** The charter partially forces the required
distinction. F1 explicitly requires fact identity without making facts
document-children; F2 requires source-box meaning to remain distinct from
form-line meaning; and F10 exercises correction of a source finding through a
derivation cascade. The relevant exhibits are F1, F2, and F10 in
`charter-it1.md`.

The fixture set does not explicitly require the Article 1 detection that
removing or replacing evidence leaves fact and finding identity/content
unchanged while changing only evidentiary standing. A design can satisfy the
literal F1 wording while still accidentally keying a fact on a source citizen.
This is a charter gap, not a prototype result.

**Disposition recommendation:** amend the charter before the builder opens:
add an evidence-removal/re-upload probe to F1 or F2. The probe should use the
same asserted finding before and after evidence replacement/removal and require
stable fact/finding identity and content, with only evidence standing changing.

### 2. Articles 9/10 — canon and declaration

**Check -> result -> exhibit:** The charter requires concrete schemas or
schema amendments, identifies all load-bearing citizen families, and requires
a hand-written positive and negative instance for every new or amended family
(F6, F7, F8, F12; Q1, Q2, and Q7; Evidence Expected). This is good coverage of
the declaration boundary and the payload-instantiation gate.

There is one measurement gap: F12 says that a negative example catches a
meaningful contract error, but does not require a strict validator run showing
that the example is rejected for that reason. Without that requirement, a
written negative example could remain an assertion rather than evidence that
consumers reject undeclared or malformed shape.

**Disposition recommendation:** amend F12/Evidence Expected to require a
machine-checkable validation result for every positive and negative example:
positives validate, negatives fail, and the failure is identified without
repair or coercion. Include at least one negative for an undeclared shape or
wrong schema version.

### 3. Article 11 — legibility and thin execution

**Check -> result -> exhibit:** Satisfied as a charter. F2 requires the
source-box/form-line bridge to be distinguished; F6 requires declared meaning
for the included Form 1040 fields; F7 requires declared rendering-absence
semantics; F8 requires citations for source facts, form lines, parameters, and
rules; F10 requires recoverable derivation edges and explanation paths. Q3,
Q5, and Q8 explicitly ask where these meanings live and whether a reader can
recover them from artifacts. The Evidence Expected section requires schemas,
instances, scenarios, and a validator/evaluator rather than accepting hidden
runner behavior.

The charter does not authorize the prototype to settle broad tax coverage or
form traversal, and its Out Of Scope section keeps those boundaries visible.
That is appropriate for this gate. The official-source requirement is a
build-time evidence obligation, not an undeclared runtime input.

### 4. Article 14 — record and recomputable coverage

**Check -> result -> exhibit:** Satisfied, subject to the explicit evidence
shape being preserved in the build. F5 requires an unclosed source set to
block without publishing a zero. F11 requires current-state coverage to expose
open closure assertions without storing coverage as authoritative form state.
Q9 repeats the prohibition, and the Evidence Expected section places coverage
observations in records or derived reports. These requirements preserve the
distinction between current facts and an observation about them.

The builder should demonstrate the result by recomputing the report from the
synthetic workspace and derivation records rather than introducing a coverage
citizen. That is an implementation measurement implied by F11/Q9, not a
request to add a new ontology entry.

### 5. Reserved-entry safety

**Check -> result -> exhibit:** Satisfied. The charter explicitly excludes
stance/position doctrine in Out Of Scope. F3-F5 concern source-set closure as
ordinary fact content and require basis/pins to be designed; they do not
require a stance or legal-position construction. F10 concerns mechanical
derivation displacement, not authority construction for derived findings. The
charter also excludes filing, which keeps legal effect outside this prototype.

No fixture requires resolving the reserved T1 derived-finding authority
construction or the reserved T2 stance/position entry. Any candidate design
that needs either to make a fixture work should report that as a failure and
stop rather than filling the reservation.

### 6. ADR-0005 evidence gate

**Check -> result -> exhibit:** The charter has the structure required to
generate contract-foundational Tier 2 evidence: a shared fixture set for an
incumbent and rival, explicit questions Q1-Q10, positive and negative
examples, evolution and supersession probes, and an examination note with
paths to exhibits. F1-F12 cover the principal citizen, lifecycle, rendering,
citation, and coverage risks.

It is not yet sufficient to open the builder unchanged because the two gaps in
checks 1 and 2 weaken the falsifiability of the Article 1 and Article 9/10
claims. The round should remain open until the foreman records whether those
amendments are adopted or the owner overrides them. After amendment, the
charter should be capable of producing the prototype evaluation analysis ADR-
0005 requires; the decision remains Tier 2 unless that later analysis
honestly narrows it.

## Observations and dissent

- This review is a charter sufficiency review, not an endorsement of any
  eventual form-field or fact-type design.
- The charter's treatment of rendered absence is appropriately concrete: it
  names computed zero, closure-backed zero, and guard/non-existence as three
  distinct cases. The builder still must prove a fresh reader can recover the
  distinction from artifacts alone.
- No dissent is registered on the governance checks themselves. The two
  recommended amendments are evidence-strengthening conditions before build,
  not competing contract designs.

## Recommendation

**Amend charter, then reopen builder dispatch.** The charter's scope and
question set are otherwise adequate for round 1. The foreman should preserve
the amendments as a disposition decision and keep the rival-builder and
fresh-reader seats closed until the normal process opens them.
