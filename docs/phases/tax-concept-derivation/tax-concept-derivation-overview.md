# Tax Concept Derivation

## Purpose

This phase establishes the missing semantic layer between facts held in a
workspace and values rendered on a tax return.

The return engine has proved that it can transcribe reported amounts, aggregate
declared families, apply versioned rules, and preserve derivation lineage. The
Taxable Interest Modeling milestone showed why that is not yet a general tax
model: a document reports something; it does not by itself establish what the
law makes of the reported amount. A return line is where a tax concept is
reported; it is not the definition of that concept.

The phase therefore tests this chain as an explicit product capability:

> evidence → reported and ordinary circumstance facts → tax classification →
> derived tax-concept facts → return calculation and form projection →
> explanation

The immediate product value is not a richer disclaimer. It is an engine that
can distinguish what a source says from the tax conclusion drawn from it, ask
for a comprehensible missing circumstance when one matters, and explain both
the conclusion and the rule that produced it.

## Product posture

The application maintains a workspace, generates a simulated return from the
workspace, and helps the user investigate tax questions. It does not borrow a
tax professional's authority and it does not ask the user to supply legal
classifications they cannot reasonably be expected to understand.

The intended division of work is:

- evidence supports reported facts and may suggest ordinary factual questions;
- the user supplies or corrects facts about their own documents and
  circumstances;
- adopted tax content classifies those facts and derives tax concepts;
- the return engine consumes tax-concept results rather than treating source
  document boxes as though they were already tax conclusions; and
- citations and explanations identify how the determination could be checked,
  without pretending that citation itself makes the application authoritative.

The standing workspace convention governs which inputs the calculation treats
as present. This phase does not reopen source-family closure, provisional-run,
scenario, or action-scoped confirmation design. A user confirmation about the
workspace cannot certify that the product's tax model is adequate; model
coverage remains the product's responsibility.

## The bounded opening slice

Taxable interest remains the worked domain because the repository has deep
existing content and the preceding milestone mapped its modeling failures. The
phase does **not** begin by attempting the whole taxable-interest universe.

The opening slice uses one synthetic 2025 Form 1099-INT box-1 item and one
ordinary circumstance: accrued interest paid when the underlying obligation
was purchased. It compares two cases with the same reported amount:

1. no accrued-interest circumstance applies; and
2. a bounded accrued-interest amount applies under the treatment established
   from official sources.

That pair is small but discriminating. It forces the model to preserve a
reported amount while deriving a potentially different includible amount. It
also crosses every intended layer without requiring the phase to model
education exclusions, original issue discount, nominee ownership, bond-premium
elections, joint-return subject identity, or the complete universe of interest
income.

The slice is a test fixture for architecture, not a claim that its categories
exhaust US-federal taxable interest.

## Scope

During this phase the project may:

- define the minimum semantics of a reported fact, an ordinary circumstance
  fact, a tax-classification result, a derived tax concept, and a reporting
  projection;
- establish how subject, jurisdiction, period, quantity, rule version, and
  source authority travel across those layers;
- compare an explicit item-level determination with the current direct
  source-family-to-form-line path;
- create synthetic, executable vertical slices before selecting production
  schemas or citizen shapes;
- establish a versioned coverage account that says which regions of a concept
  a build can decide without redefining the concept to match the build;
- test how a missing material circumstance becomes a bounded question or a
  visible limit rather than a silent classification; and
- project a derived tax-concept value onto a simulated return while preserving
  the distinction between the concept and its form placement.

## Non-goals

This phase does not promise:

- an exhaustive ontology of tax law or complete taxable-interest coverage;
- implementation of every Form 1099-INT, Form 1099-OID, Schedule B, or
  non-document interest category;
- a universal answer to how all tax concepts should be represented;
- a professional opinion, legal determination, filing act, or product claim to
  institutional authority;
- a new user declaration about source-family or tax-concept completeness;
- a hypothetical-scenario system, provisional-return contract, or run graph;
- a production schema or governance amendment merely because a prototype used
  a convenient shape; or
- an interface whose principal function is warning the user that the model is
  incomplete.

Coverage breadth is admitted only when it tests a named architectural question
or implements an already selected contract. Interesting taxable-interest cases
outside the opening slice are adversarial tests and future candidates, not an
automatic backlog for this phase.

## Principles for bounded modeling

### Model the legal concept broadly enough to locate the slice

The project needs enough awareness of the surrounding concept to know what the
slice does and does not establish. It does not need to enumerate the entire
domain before learning from the slice. The concept account may therefore name
regions such as inclusion, exclusion, allocation, timing, election, and
reporting without instantiating every category within them.

### Model only distinctions that change something

A distinction earns representation when it changes a calculation, a question,
a lifecycle result, a return projection, an explanation, a coverage boundary,
or the product's ability to detect that it lacks a necessary fact. Coherence
may require a broader vocabulary than the first fixture exercises, but unused
abstractions do not enter the model merely for elegance.

### Keep concept meaning separate from executable coverage

The tax concept is not defined as the categories currently implemented. The
coverage profile is not a confession that no result may be computed. It is a
versioned account of where the executable model reaches, where it knowingly
stops, and which boundaries it can detect.

### Treat authority as support for the method

Official authority should support the propositions encoded by tax rules. The
application models how a conclusion is reached and how it could be examined;
it does not become the author of the law or inherit the standing of a
professional who applies it.

## Phase exit criteria

The phase is ready to close when:

1. at least one tax-concept value is derived in production from reported and
   ordinary circumstance facts through an adopted tax-classification rule;
2. changing the circumstance can change the classification without rewriting
   what the source reported;
3. at least one return field consumes the derived tax concept through an
   explicit reporting projection rather than directly treating a document box
   or reporting subtotal as the substantive concept;
4. the concept's meaning and the build's executable coverage are recoverable
   as different things from committed artifacts;
5. the derivation identifies subject, period, jurisdiction, quantity, rule
   version, and the facts and authority on which the classification depends;
6. an unsupported adjacent case has a deliberate, testable behavior and cannot
   silently masquerade as covered merely because the rule ran;
7. the approach has been tested against one contrasting tax concept whose
   structure differs materially from interest income; and
8. a fresh reader can recover what the result means, how it was derived, where
   it appears on the simulated return, and what the model does not establish.

Closing the phase does not require complete taxable-interest coverage or a
general-purpose tax ontology.
