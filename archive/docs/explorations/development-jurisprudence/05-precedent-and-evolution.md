# Precedent and Evolution

Status: exploratory, not binding.

## The Common-Law Loop

The healthiest relationship between judgments and rules is a pipeline that
common-law systems discovered empirically:

1. A dispute arises that no rule covers. A judge settles it and records the
   reasoning — a commitment, an ADR.
2. The settlement becomes precedent: future similar cases are argued by
   analogy to it, cheaply, without re-deriving the reasoning.
3. When the same dispute shape recurs enough times with the same outcome,
   the precedent line is codified into a rule — a statute, a fitness
   function — and enforcement becomes mechanical.
4. The rule occasionally misfires on cases the precedent line never
   imagined; the misfires go back to a judge; the cycle continues.

So the direct answer to "do precedents evolve fitness functions" is yes —
that is the intended metabolism. Fitness functions are case law that
hardened. A check that walks a provenance chain exists because some
judgment once settled that unexplained values are defects; the check is
that judgment, compiled. The pipeline runs backward too: a fitness function
that produces false positives is precedent under strain, and the pressure
should flow back up — refine the rule, or demote it to a standard and
return its dispute class to a judge.

Two disciplines keep the loop honest. Codification should require
recurrence — one judgment is a data point, not a doctrine; extracting a rule
from a single case overfits to its accidents. And every rule should carry
provenance to the commitments that justified it, because a rule that has
lost its citations cannot be re-litigated cheaply, and un-relitigatable
rules are how bureaucracies fossilize.

## Failure Modes of Accumulated Law

- Rule accretion: each incident adds a check, no incident removes one, and
  after some years the check suite encodes a paranoid history nobody
  remembers. Legalism is the cultural symptom: contributors optimizing for
  check-passage rather than for the values the checks once served.
- Zombie rules: enforcement whose provenance is lost. Nobody knows why the
  rule exists, so nobody dares remove it, so it survives precisely because
  it is unaccountable — the opposite of how survival should work.
- Precedent overfitting: yesterday's disputes were about yesterday's
  system. A precedent corpus is a biased sample of the disputes an earlier
  architecture generated; consulting it uncritically for a changed
  architecture imports the bias. Courts handle this with distinguishing —
  "the cited case differs materially" — which requires judges willing to
  distinguish rather than pattern-match.
- Selective codification: the disputes that get rules are the mechanizable
  ones, so over time the mechanical layer governs formality while the
  substantive questions — the ones that resist formalization — remain in
  the silent-settlement regime. The check suite becomes rigorous about
  trivia. Worth auditing: are your most-enforced rules about your
  most-important values?

## Drift as the Null Hypothesis

Absent the loop, systems do not stay where they were put. Lehman's laws of
software evolution observed this half a century ago: a system that is used
must be continually changed, and under continual change its complexity and
its distance from any original design intent increase unless work is
actively spent resisting. In jurisprudential terms: silent disputes settle
toward the path of least resistance, and the path of least resistance is
prevailing convention, so an ungoverned system drifts monotonically toward
the industry mean. The common-law loop is a negative feedback mechanism —
judgments detect drift, rules arrest the detected cases, and the corpus
ratchets settlements so they stay settled. Governance, on this view, is not
about control; it is about giving a system a restoring force toward its own
intentions.

## Precedent as Executable, Again

The agent inflection sharpens all of this. For human teams, step 2 of the
loop — precedent guiding future cases — depends on memory, search, and
willingness. For agent development, precedent placed in context conditions
the next generation of code directly: the corpus is not consulted, it is
*ingested*. This has an underappreciated consequence: curation of the
precedent corpus becomes a first-order engineering activity. What earlier
eras managed with seniority and oral tradition — deciding which old cases
still matter — becomes, literally, context management. The questions of
which commitments an agent sees, in what order, at what level of summary,
are jurisprudence questions and prompt-engineering questions
simultaneously, and there is no meaningful boundary between them.
