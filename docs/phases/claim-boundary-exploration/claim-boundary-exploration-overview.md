# Claim Boundary Exploration Phase — Overview

Audience: Product (scope and exit criteria are Shared)

Status: **active.** Adopted by the owner on 2026-08-19. The opening milestone is
planned; no exploratory account or implementation work has begun.

## Purpose

The engine can compute a wide set of bounded 2025 federal return classes and
can connect published values to findings, rules, citations, acts, and runs. The
next product question is not another tax-content row. It is whether those
connections can help a casual but invested user understand what the system is
saying, why it is saying it, where that statement stops, and what the user can
reasonably do because of it.

This phase begins with exploration rather than a settled product contract. It
starts from ordinary, high-level user questions, follows their compressed
meaning through the tax, legal, financial, computational, and epistemic layers
that matter, and reduces what it learns into narrower product questions that
could actually be acted upon.

The working phrase *claim boundary* names the object of inquiry: the boundary
of what a system response gives a reasonable user reason to believe or do. It
is an analytical aid for this phase, not new governance vocabulary and not a
term the product must show to users.

## Standing test

> Can a casual but invested user ask a plain, high-level question and receive a
> useful plain answer whose deeper layers reveal why the system says it, what it
> rests on, where it stops, and what the user may do next—without first learning
> the project's private vocabulary?

The standing test measures communication utility only after the inquiry has
preserved the relevant tax, legal, financial, computational, and epistemic
distinctions. A simple answer that erases a material distinction does not pass.

## Starting point

Engine Breadth closed after repeatedly proving a vertical computation shape.
The project now has substantial declared tax content, closed source families,
versioned rule artifacts, immutable records, explanation walks, and a human
presentation model. It also has two conspicuous user gaps: fact entry still
requires hand-edited JSON, and the product cannot file a return.

The existing system is strongest at answering a technical question: which
findings and artifacts produced this value? It has not yet shown that it can
answer the user's broader questions in ordinary language, or that every
inference invited by its presentation stays inside the support available to
the system.

The governance set already defines `claim` for workspace authority. This phase
does not replace or amend that definition. It investigates a related product
question: which beliefs and actions the system's words, values, omissions,
states, and affordances invite in a reasonable user.

## Scope

- Begin each inquiry with a concrete question a casual user might actually ask.
- Use an obviously synthetic engine scenario whose material contracts are
  verified against a named comparison package, so the inquiry can trace real
  project artifacts without using personal information. No committed artifact
  designates a "current" package; an inquiry must name the package version it
  compared against rather than asserting currency.
- Write the shortest useful plain answer before decomposing it into deeper
  explanation layers.
- Trace the answer through relevant facts, findings, computations, citations,
  mappings, product conventions, limitations, and available actions.
- Examine both explicit statements and implications created by labels,
  omissions, sequencing, and enabled or disabled actions.
- Give an explorer leeway to follow a discovered angle when it can materially
  change the answer, explanation, action, limitation, evaluation, or future
  product requirement.
- Retain only actionable considerations: an item must identify a plausible
  product, explanation, engine, evaluation, limitation, or bounded-research
  consequence.
- Compare multiple domain readings before measuring the final answer's utility
  to a nonexpert user.
- Use adversarial model-agent accounts as exploratory evidence, never as
  professional attestation.

## Non-goals

- No exhaustive map of language, epistemology, tax law, or legal semantics.
- No dictionary of project-specific meanings for ordinary words.
- No requirement to display terms such as `claim`, `integrity`, `complete`,
  `provenance`, or `epistemology` to users.
- No production UI, entry, filing, transmission, schema, rule-language, or
  engine implementation merely because an inquiry identifies a possible need.
- No ADR or governance revision during exploratory work. A consequential
  decision discovered here becomes a candidate for later decision-bearing
  work.
- No claim that model agents are CPAs, tax professionals, lawyers, or users.
- No resumption of the closed Engine Breadth coverage frontier or its filed
  hardening plan without a separate owner selection.
- No personal facts, documents, values, outputs, workspace details, or
  descriptive real-run evidence.

## Exploration discipline

The phase uses a wide discovery surface and a narrow commitment surface.
Explorers may reach across domains, but an inquiry remains anchored to its
plain-language question. A thread stays live only while it can answer at least
one of these questions:

1. Could this change what the system should say or show?
2. Could this change what the user may reasonably believe or do?
3. Could this expose a misleading implication or missing limitation?
4. Could this require a different explanation, provenance, engine, or
   evaluation capability?
5. Could this become a bounded future investigation with a concrete product
   consequence?

If none applies, the thread may remain temporary research but does not enter
the phase's actionable consideration register.

Expansion and reduction are separate acts. An exploratory account follows a
promising angle deeply. A later synthesis groups related findings, tests what
would be lost by collapsing them, and promotes only the smallest useful set of
considerations. Contradictory accounts may coexist until a future decision
actually requires their resolution.

## Inquiry shape

Each worked inquiry should leave behind five recoverable layers:

1. **User question** — the exact plain-language question and the situation in
   which a person would ask it.
2. **Plain answer** — the shortest useful response, written without requiring
   project vocabulary.
3. **Progressive explanation** — optional layers for origin, computation,
   relevance, authority, qualifications, uncertainty, and next action.
4. **Claim-boundary trace** — what each material statement or affordance asks
   the user to believe or do, who supplies it, what supports it, what invalidates
   it, and which nearby inference it does not support.
5. **Actionable consequences** — product changes, explanation requirements,
   evaluations, explicit limitations, or bounded later inquiries that could
   follow.

This is a working inquiry format, not a new citizen or product contract. The
phase may revise it when concrete examples expose a better shape.

## Phase outputs

- Worked inquiry documents grounded in synthetic end-to-end examples.
- Adversarial accounts that identify over-inference, missing support, domain
  collisions, and communication failures.
- An actionable consideration register that excludes unconnected topic ideas.
- Cross-inquiry synthesis identifying repeated structures and meaningful
  differences.
- One or more bounded candidate milestones or successor phases stated with an
  object, user value, evidence standard, and non-goals.
- A recorded recommendation about whether semantic explanation requires a
  later grammar census, governance reader's guide, interface prototype, or
  professional-adversary program.

## Principal risks

**Infinite decompression.** Every explanation contains more language that could
itself be explained. An inquiry stops when it reaches actual authority,
recorded system operation, an explicit product judgment, or a qualification
whose further analysis has no plausible action under the admission rule.

**Current-design anchoring.** Beginning with an existing presentation can make
the current artifact shape seem inevitable. Boundary mutations, adversarial
readings, and the required contrasting inquiry test whether the first result is
specific to today's interface or reveals a more durable user need.

**Expert simulation mistaken for evidence of use.** Strong model agents can
reconstruct missing meaning and can imitate professional language. Their
accounts identify questions and counterexamples; they do not establish what a
real user understands or what a professional would attest.

**Actionability applied too early.** A foundational distinction may lack an
immediate implementation. Explorers may retain it temporarily while following
the active question. The actionability threshold governs durable promotion,
not what an explorer is permitted to notice.

**A private explanatory dialect.** The project could make its own framework
internally coherent while becoming harder for a casual reader. Every inquiry
therefore begins and ends in ordinary language; working analytical terms remain
behind the product unless independent evidence shows they help the user.

## Exit criteria

The phase is ready for an owner-held close, continuation, or pivot when:

- at least one plain user question has been traced end to end through a
  synthetic engine example verified against a named comparison package's
  contracts and subjected to adversarial evaluation;
- at least one materially different question has tested whether the first
  inquiry's structure generalizes or was accidental;
- the actionable register distinguishes product consequences from interesting
  but presently unactionable research;
- repeated patterns have been reduced into at least one narrower, testable
  product objective—or the evidence supports stopping without one;
- unresolved reach remains visible without becoming committed implementation
  scope; and
- the owner can select the next work for a stated user reason rather than
  because it is the latest concept discussed.

These criteria do not claim that the semantic, legal, financial, or tax domain
has been exhaustively explored. Exploration is complete enough when it makes a
smaller consequential question tractable.
