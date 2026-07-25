# Plain-Language Analysis — Presentation Surface Contract

Companion to [ADR-0046](../0046-presentation-surface-contract.md). The ADR is
the authoritative record.

## What changes

The project now has a ratified rulebook for the page a filer actually reads —
the "citation walk" that shows a Form 1040 line, its subtotal, where each
number came from, and a clickable trail back to the source fact. Until now
this pattern only existed as a synthetic prototype used to study how to build
and evaluate UI with agents; it had no product status. This ADR promotes the
converged rules from that study into a real contract a future implementation
must satisfy.

## Why it is needed

An earlier exploratory milestone spent five build-and-review cycles hammering
on a fake version of this page, deliberately trying to break it (injecting
values on blocked lines, feeding bad data, etc.), to find out what a
trustworthy version of this surface actually requires. That milestone found
consistent answers but was explicitly not allowed to make them official yet —
it was scoped as research, not product decision-making. Those findings would
otherwise sit unused until someone re-derived them from scratch while building
the real thing.

## The rules, in plain terms

- **Show only real numbers.** The page can only display what the underlying
  computation actually produced — never a number the page itself calculates
  or guesses.
- **Be honest about gaps.** If a number is missing because some fact wasn't
  provided, say so and say what's needed — never show a blank, a zero, or a
  fake placeholder.
- **Fail loudly, on the page.** If something breaks, the user must see it
  right there — not just in a developer console nobody's watching.
- **Contain damage.** If one part of the page breaks, it shouldn't take down
  or hide unrelated parts that are fine.
- **Don't let citations get confused with each other** if the same fact is
  cited in more than one place.
- **Be usable**, not just correct: readable contrast, screen-reader landmarks,
  visible keyboard focus.

## The three decisions this ADR had to make

The research left three specific judgment calls unresolved on purpose — they
are product decisions, not engineering findings. The owner made all three:

1. **When an invalid input is rejected, should the error message show the bad
   value?** No — always hide it. A "helpful" error that echoes back what was
   typed can itself leak sensitive data.
2. **Do behind-the-scenes cross-check numbers (like a subtotal shown just to
   verify the math) have to follow the same honesty rules as the main
   numbers?** Yes. A "just a diagnostic" number is still something the user
   sees, so it can't sneak around the blocking rule.
3. **When a line is missing data, should the warning show up only right there
   on that line, or also in a summary banner at the top of the page?** Just on
   the line itself, for now — keeps one place responsible for showing the
   problem instead of two places that could drift out of sync.

## What this does *not* do

This ADR does not build anything. It does not raise the project's maturity
tracking for the Presentation capability — that still requires an actual
implementation, built against real tax data (not the synthetic research
fixture), independently reviewed, and verified the same rigorous way every
other real-data capability in this project has been. This ADR just makes sure
that implementation starts from settled rules instead of re-arguing them.
