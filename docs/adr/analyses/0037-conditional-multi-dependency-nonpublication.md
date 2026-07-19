# Plain-Language Analysis — Conditional Multi-Dependency Non-Publication

Companion to [ADR-0037](../0037-conditional-multi-dependency-nonpublication.md).
The ADR is the normative record; this document explains the accepted decision.

## What changes

Rules will be able to say that a group of facts is required only when a stated
condition is true. If two facts are missing, the product can name both instead
of finding one, stopping, and revealing the other only after another run.

When the condition is false, those facts are not demanded. A return with no
qualified dividends therefore keeps its ordinary-tax result without answering
unrelated capital-gain questions.

## Why it is needed

D2 needs two declarations when qualified dividends are present. The current
evaluator stops at the first absent fact. The proposed shape keeps the whole
required-fact set in the declared rule, where it can be inspected and
explained.

## What it protects

- A runner or UI cannot quietly decide which facts are required.
- Any fact used to allow publication is recorded as an input, so correcting it
  displaces the result normally.
- Inactive conditions do not create false blocks.
- Missing lists contain only facts that are actually absent.

## What it enables

D2 gains an honest one-walk explanation when both capital-gain declarations
are absent. Future conditional-completeness rules reuse the same declared
language rather than inventing form-specific exceptions.

## What it does not do

It does not implement the schema or evaluator behavior, change tax arithmetic,
or accept personal data. Those steps remain separate.
