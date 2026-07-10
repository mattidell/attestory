# Institutions of Settlement

Status: exploratory, not binding.

## The Four Archetypes

When people imagine governing disputes, they usually reach for one of four
institutional shapes, often without noticing they are choosing:

- The legislature (pre-settlement): write the rules before the disputes
  arrive. Constitutions, principles documents, coding standards, schemas.
  Strength: silent disputes settle correctly without anyone appearing.
  Weakness: you must predict the disputes, and wrong predictions fossilize.
- The watchdog (automated enforcement): a standing mechanism that inspects
  every change and objects to violations. Fitness functions, linters, CI
  gates, schema validation. Strength: tireless, incorruptible, instant.
  Weakness: can only enforce what can be formalized, and formalization
  always loses information.
- The committee (deliberation): multiple reviewers reason together toward a
  settlement. Design reviews, multi-agent review panels, RFC processes.
  Strength: surfaces considerations no single reviewer holds. Weakness:
  expensive, slow, and prone to both groupthink and its opposite,
  compromise-shaped incoherence.
- The judge (adjudication): a designated authority decides the instant case.
  Human review gates, the tech lead, the maintainer. Strength: handles
  novelty and context; produces reasoned decisions that can become
  precedent. Weakness: a bottleneck with moods.

No real system uses one shape. The design problem is the portfolio: which
dispute classes go to which institution, at what cost, with what appeal
path.

## Rules Versus Standards

Legal theory has a distinction that maps onto software governance almost
embarrassingly well. A rule is settled ex ante: "no vehicle over 3,000 kg on
the bridge." Cheap to apply, predictable, and inevitably over- and
under-inclusive — it blocks the harmless 3,001 kg vehicle and admits the
harmful 2,999 kg one. A standard is settled ex post: "no vehicles that
endanger the bridge." Perfectly fitted to each case, expensive every time,
and unpredictable in advance. Louis Kaplow's classic analysis frames the
choice economically: rules cost more to make and less to apply; standards
the reverse. High-frequency conduct wants rules; rare, contextual conduct
wants standards.

The software translation: a fitness function is a rule; a principle is a
standard. "The production-edge graph must be acyclic" is a rule — mechanical,
instant, slightly dumb. "Prefer traceability over convenience" is a standard
— it needs a judge, human or agent, applying it to facts. The economics
carry over directly: mechanize the dispute classes that recur identically;
adjudicate the ones that vary. And the conversion is dynamic — a standard
that keeps producing the same judgment in the same shape of case is a rule
waiting to be extracted. That pipeline is the subject of document 05.

## Primary and Secondary Rules

H. L. A. Hart's *The Concept of Law* distinguishes primary rules (rules
about conduct: do not mutate canon) from secondary rules (rules about rules:
how rules are made, changed, recognized as valid, and applied). Hart's claim
is that what separates a legal *system* from a mere pile of customs is the
secondary rules — the rule of change, the rule of adjudication, and above
all the rule of recognition: the ultimate criterion by which anyone knows
what counts as law here.

Most software projects have only primary rules — style guides, conventions —
and improvise the secondary ones every time a primary rule needs changing.
The projects that feel governed rather than merely opinionated are the ones
with explicit secondary rules: how a principle gets amended, who confirms a
plan is complete, what makes a decision binding (a status field on an ADR is
a rule of recognition in miniature). It is worth auditing any project you
care about for its secondary rules; their absence is invisible until the
first constitutional crisis, which usually arrives disguised as a heated
code review.

## Graduated Response

Elinor Ostrom's field studies of long-lived commons institutions found,
among other design principles, graduated sanctions: first violations meet
mild responses, escalation is reserved for repetition. The software
translation is a severity ladder for enforcement — advisory warnings before
blocking checks before human escalation — and it matters because uniform
maximum severity teaches contributors (and agents) to route around the
enforcement layer entirely rather than negotiate with it. A check that
always blocks is a wall; a check that warns, then blocks, then escalates is
a conversation. Ostrom's deeper lesson generalizes: institutions survive
when the governed participate in changing the rules, monitoring is done by
parties accountable to the governed, and conflict resolution is cheap and
local. Any resemblance to a solo developer governing a fleet of agents is
worth chewing on slowly.

## The Agent Inflection

One historical note worth holding: for human organizations, all four
institutions are expensive, so most engineering culture optimizes for
lightweight convention and tolerated drift. Language-model agents change the
cost structure asymmetrically. Pre-settlement becomes dramatically cheaper —
agents actually read the constitution, every time, verbatim. Watchdogs are
unchanged. Committees become cheap but correlated — five agents deliberating
share training priors in a way five humans do not. Judging remains the
scarce resource, because it consumes the one input agents cannot yet supply
for you: your judgment. Institutional designs that were bad economics for
human teams may be excellent economics for agent fleets, and vice versa.
Most received wisdom about process weight predates this inflection and
should be re-derived rather than inherited.
