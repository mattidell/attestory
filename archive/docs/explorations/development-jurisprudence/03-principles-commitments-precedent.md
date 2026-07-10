# Principles, Commitments, Precedent

Status: exploratory, not binding.

## The Ladder

Governance concepts arrange themselves into a ladder by generality and by
what it takes to change them:

1. Ontology — what the domain fundamentally is. Changes only when your
   understanding of the domain changes. ("This product manages justified
   beliefs, not answers.")
2. Principles — standing orientations derived from the ontology. Directional,
   always-on, amended rarely and deliberately. ("Every value explains
   itself.")
3. Commitments — specific, dated decisions that apply principles to cases.
   Recorded, immutable, revocable only by supersession. (An ADR.)
4. Mechanisms — instruments that enforce settled matters. Fitness functions,
   schemas, checks, templates. Changed freely, because they are downstream
   of everything above.
5. Precedent — the accumulated corpus of commitments, which guides the
   application of principles to future cases even where no mechanism exists.

The ladder is a dependency graph: each layer should be explainable by appeal
to the layer above. A mechanism nobody can trace to a commitment is a zombie
rule. A commitment that cites no principle is ad hoc — sometimes correctly
so, but the absence of citation is information. A principle that derives
from no ontology is an aesthetic preference wearing a uniform.

## Principle Versus Commitment

The distinction the ladder makes precise:

A principle is timeless in aspiration, directional in content, and settles
*classes* of disputes. It has no date, no author of record, no specific
case. Its test is foreclosure: a principle that never makes you do the more
expensive thing is a platitude. Principles are standards in the
rules-versus-standards sense — they require application, and application
requires judgment.

A commitment is a dated act. It settles an *instance*: this design, this
boundary, this trade-off, decided on this day for these reasons. Its test is
consequences-with-negatives: a commitment recorded without its costs is
advocacy, not a record. Commitments are where principles touch ground — the
case law to the principles' constitution.

The relationship runs both ways. Downward, principles constrain commitments:
a commitment that violates a principle needs either reversal or an explicit
exception, and repeated principled exceptions are amendment pressure on the
principle itself. Upward, commitments give principles their meaning:
"schema is canon" is four words until you have watched it kill a read-model
layer and force a payload split; after those commitments, the principle has
a jurisprudence. A principle with no commitments applying it is untested
law — you do not actually know what it means yet, and neither does anyone
reading it.

## Why Precedent Is Different in Kind

Precedent is not merely storage. Edward Levi's account of legal reasoning
describes it as reasoning by example: a judge does not deduce from rules but
moves analogically from decided cases to the instant one, and the rule
emerges from the run of cases rather than preceding it. This is a remarkably
good description of how experienced engineers actually make design
decisions — and an almost literal description of how language-model agents
work.

Which surfaces the strangest fact in this whole territory: for a human
organization, precedent influences behavior indirectly — someone must
remember the old decision, find the document, choose to follow it. For an
agent, precedent placed in context *directly conditions generation*. The ADR
corpus is not documentation of the decision process; under agent
development, it is an executable component of it. Common law was always a
technology for making past judgment bear on present cases; agents make it a
literal one. It is hard to overstate how unusual this is: development
jurisprudence is the rare domain where writing philosophy down changes the
machine's behavior without any further engineering.

## A Note on Values

One rung sometimes proposed above ontology: values — what matters to the
maker independent of any domain. Auditability mattered to this project's
author before the belief-structure ontology existed to house it; the
ontology was, in part, chosen because it served the value. Values explain
why *this* ontology and not another equally coherent one. They resist
documentation more than any other rung, and attempts to formalize them tend
to produce mission-statement mush. The practical compromise most systems
land on: let values live in the story register — narrated, not specified —
and let the ontology be their first formal shadow.
