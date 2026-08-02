# ADR 0009 — Derived-Finding Shape and the Reserved Authority Boundary

- Status: accepted (ratified 2026-07-11; amended pre-ratification — authority positively located in the attribution chain per the recorded instrument framing)
- Tier: 3
- Date: 2026-07-11

## Context

Derivation Machinery Track 4 (the saturation runner) must publish derived
findings through the ADR-0007 `derived-publication-act`. Building the runner
forced a contract question that the Track 1 schemas left implicit and that no
prior ADR resolves:

**What is the shape and authority of a derived finding?**

The kernel `finding.v1` requires `basis ∈ {documentary, attested, elective}`.
All three are *human* authorities — a document stood behind the answer, a
person attested it, or a person elected it. A machine-derived value has none
of these. Assigning one (e.g. `attested`) to a computed number would
misrepresent authority: it would claim a human stood behind a figure the
runner produced. Inventing a fourth basis value (`derived`) would *construct*
the doctrine of derived-finding authority.

That doctrine is a **reserved ontology entry** — T1 derived-finding authority
construction — flagged unbuilt in three places:

- `AGENTS.md` guardrail: "Do not build on reserved or deferred ontology
  entries (T1 derived-finding authority construction ...). If a milestone
  appears to need one, stop and surface the resolution as a Tier 3 decision
  instead of improvising doctrine."
- Project memory: reserved ontology entries (T1 derived-finding authority)
  are open work; milestones must not build on them.
- ADR-0007 decision 6: the publication-act shape "must remain compatible with
  any future T1 resolution" — i.e. it must not pre-decide the authority.

Track 1's `act-derived-publication.v1` provisionally references `finding.v1`
for its carried finding. That reference is the artifact of the unresolved
question, not a settled choice — surfacing it here is the point.

What the reservation does *not* cover matters as much as what it does. The
governance set already answers where a derived finding's authority comes
from, as defined doctrine, not open work: the user is the author of both
finding kinds — "one directly, one through instruments — the way the results
in a spreadsheet belong to the person who built the sheet" (Ontology §2,
findings); machinery publications "are acts of the user, performed through
the instruments the user took up," and "the machinery is never the author of
anything" (Ontology §2, act); "every derived finding traces through its run
to an adoption act, and through the adoption act to the user" (Ontology §2,
adoption). ADR-0007 decision 2 ratified the mechanical form of this framing:
the publication act is attributed to the adopting actor through the adopted
instrument. T1 reserves the *fuller account* of what this authorship amounts
to — its language is "the instrument framing is recorded; a fuller account is
open work" — not the framing itself.

## Evidence

Per ADR-0005 this is not a placeholder decision: the two ratified prototype
exhibits are the evidence. Both `exhibits/rule-language/it1` and
`exhibits/rule-language/it2` modeled a derived finding as a **distinct citizen
with no human basis** — shape `{finding_id, symbol, value, version, pins}`
(round-2 legibility recovery §E confirmed the `derived-finding` def carries a
`symbol`, a `value`, and lineage `pins`, and *no* basis field). The committee
ratified the language contract (ADR-0006) over corpora that used exactly this
shape; the human-authority `basis` never appeared on a derived output in
either exhibit.

## Decision (proposed)

1. **A derived finding is its own citizen kind, `derived-finding.v1`, and its
   authority is carried by its attribution chain, not by a basis field.**
   Shape: `{schema, id, symbol, value, version, pins}`. `basis` is the
   kernel's vocabulary for the grounds of a *human* determination — a document
   stood behind it, a person attested it, a person elected it. A derived
   finding's ground is mechanical and fully pinned: pins → publication act →
   adoption act → user. That chain *is* the recorded instrument framing
   (Context above) — the user's authorship, reachable through the record,
   exactly as the Ontology defines it. Nothing about the value's standing is
   left unexpressed by omitting `basis`; a basis field on a derived finding
   would be either a misrepresentation (borrowing a human ground) or an
   improvised T1 construction (inventing a machine one).
2. **`act-derived-publication.v1` carries a `derived-finding.v1`, not a
   `finding.v1`.** The Track 1 publication-act schema is amended on the
   milestone branch to reference the new kind. (The schema is unmerged and
   not yet adopted, so this is in-milestone settling, per the retrospective
   lesson "schema wording settled before publication," not a published-schema
   mutation.)
3. **The kernel `finding.v1` is unchanged.** Its optional `pins` field remains
   the human-finding derivation-edge shim; derived *outputs* do not travel as
   `finding.v1`. This keeps human findings and machine findings in distinct
   citizen families, which the "form-field/fact-type citizen families" work
   (First Tax Slice, §5.6) can build on without retrofitting authority.

## What T1 still reserves

This ADR consumes the recorded instrument framing and nothing further. Open
under T1, untouched by this shape: what instrument-authorship amounts to at
the filing boundary (where workspace acts meet legal acts); whether and how a
derived finding may serve as the *basis* of a subsequent human act (e.g., an
attestation that cites a computed value); and multi-party authority over
adopted instruments. A future T1 resolution may add standing/authority
doctrine as a view over derived findings; it will not need to reshape the
citizen, because the chain it would interpret is already mandatory in the
shape.

## Consequences

- Track 4 can proceed: the runner publishes `derived-finding.v1` citizens via
  `derived-publication-act`, pins their lineage, and records the run — none of
  it asserting human authority for a machine value.
- ADR-0007 decision 6 is honored, not contradicted: a later T1 doctrine can
  define how derived findings acquire standing/authority as a *view*, without
  changing this shape.
- ADR-0007's note that "the finding schema's `pins` shim gains its intended
  consumer" is refined: the *consumer of derivation lineage* is
  `derived-finding.v1`; `finding.v1.pins` stays available for human findings
  that cite derivation edges, but is not the derived-output carrier.
- Currency/displacement (kernel `currency.py`) will need to fold
  `derived-finding.v1` into the derivation-edge graph in a later track; this
  ADR does not change that module, it scopes what it will consume.

## Alternatives considered

- **Reuse `finding.v1` with a basis value.** Rejected: either misrepresents
  authority (reusing `attested`/`documentary`/`elective`) or constructs the
  reserved T1 doctrine (adding `derived`). Directly violates the AGENTS
  guardrail.
- **Resolve T1 derived-finding authority now.** Out of scope: T1 is a Tier 3
  ontology decision in its own right; the runner does not need authority
  doctrine, only a non-misrepresenting output shape. Deferring authority while
  shipping a compatible shape is the smaller, reversible step.

## Links

- Forces: `docs/archive/2026-08-02-milestone-artifacts/phases/foundation/milestones/derivation-machinery.md` Track 4;
  `docs/archive/2026-08-02-milestone-artifacts/prototypes/rule-language/reviews/round-2-legibility.md` §E (derived
  finding recovered as symbol/value/pins, no basis).
- Companions: ADR-0006 (rule language), ADR-0007 (publication act — decision 6
  reserved-entry guardrail), ADR-0008 (record placement).
- Reserved entry: T1 derived-finding authority (unbuilt; `AGENTS.md`).
