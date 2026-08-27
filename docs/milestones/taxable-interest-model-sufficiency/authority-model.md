# Authority and the Coverage-Profile Method

## The problem this document addresses

An application that computes tax results must be able to say *why* each of its
substantive decisions is correct. The naive version of that requirement is
"cite a source." The naive version fails in a specific and expensive way: a
citation attached to a rule tells you that somebody consulted something, but
not **which proposition** the source establishes, **what kind** of authority it
is, or whether the cited source is even the kind of source capable of
establishing that proposition.

> **Do not reduce the solution to "add statute citations."** A statute
> reference bolted onto a rule is not proposition-level provenance, and a
> corpus full of them can still leave every substantive question unsupported.

Authority attaches to **propositions and rule edges**, not to artifacts.

## What must be recorded for each supported proposition

Seven things. All seven, or the proposition is not supported — it is asserted
next to a link.

### 1. The exact proposition or rule edge supported

Not "this rule concerns interest." Rather: *"amounts of this kind are
includible in gross income for this period"*, or *"this amount is reduced by
that amount before the limitation applies"*, or *"this quantity is reported on
that line."*

The unit of support is the edge in the reasoning, not the artifact that
happens to contain it. One rule typically has several edges, and they are
usually supported by different sources of different classes.

### 2. The authority class

Which kind of source this is. The classes are not interchangeable, and the
class determines what the source is *capable* of establishing. See the
hierarchy below.

### 3. Jurisdiction and effective period

Which jurisdiction and regime the source governs, and for what period it is
effective. Tax authority is dated. A correct citation to a superseded provision
supports nothing about the current year, and an undated citation cannot be
checked for that failure.

### 4. A precise locator

Enough to take a reader to the exact text: section and subdivision for a
statute or regulation; form, year, and **line** for a form or instruction;
publication, revision, and section for a publication.

Locator precision is not pedantry. A citation to a whole form or a whole
publication is unfalsifiable — nobody can check whether the cited document says
what the rule claims, so nobody does.

### 5. The role the source plays for that proposition

What the source is *doing*. A source may:

- **define** — establish the concept or the includibility itself
- **interpret** — construe a defined term or resolve an ambiguity
- **qualify** — limit, condition, or carve out
- **override** — displace an otherwise applicable rule
- **operationalise** — specify the mechanics of computing or reporting
- **merely explain** — restate for a lay audience without adding authority

The last of these is the one that causes trouble. Explanatory material is
enormously useful and frequently accurate, and it establishes nothing on its
own. A model whose substantive support consists of explanatory sources has the
appearance of provenance without the substance.

### 6. The relationship to other authority for the same proposition

How this source stands relative to the others: whether it implements a
statute, construes a regulation, restates published guidance, or operationalises
a rule established elsewhere. A source's weight depends on that relationship,
and a set of citations without relationships cannot be evaluated.

### 7. Whether the recorded set is sufficient for the proposition

Whether the sources recorded, taken together, actually establish the
proposition — or whether they establish part of it and the remainder is
assumed. This is the requirement that keeps the other six from becoming
bookkeeping.

A proposition supported by mechanics-only sources, or by explanatory-only
sources, must be recorded as **partially supported**, not as supported.

## The source hierarchy and what each class can support

| Class | Can establish | Cannot establish alone |
| --- | --- | --- |
| Statute | Substantive existence, includibility, exclusion, allocation, timing | Detailed mechanics; the resolution of terms the statute delegates |
| Treasury regulation | Binding construction and mechanics the statute delegates | Anything contrary to the statute |
| Judicial authority | Binding construction within its scope; resolution of contested meaning | General rules beyond its jurisdiction or facts |
| Published administrative guidance | The administration's binding or advisory position, with stated reliance limits | Substantive meaning against statute or regulation |
| Form | What must be reported, where, and in what order | What an amount substantively *means* |
| Form instructions | Reporting mechanics, ordering, thresholds, filing conditions | Substantive tax meaning, though it often correctly restates it |
| Publication | Explanation and worked examples for a lay reader | Substantive meaning; publications are explanatory |

Two statements about this table are the whole point of it, and neither is
obvious.

> **Forms and instructions are legitimate authority for reporting mechanics.
> They are not automatically sufficient authority for substantive tax
> meaning.** Which line an amount goes on, in what order subtractions occur,
> and when a schedule must be attached are exactly what instructions establish.
> Whether an amount is includible in gross income is not.

> **Statutes are foundational but are not necessarily sufficient by
> themselves.** A statute that delegates its mechanics to regulations does not
> support a computation on its own, and a statute whose operative term has been
> construed cannot be applied correctly without that construction.

The practical consequence is that most substantive propositions need at least
two classes, and a corpus consisting entirely of one class is a finding
regardless of which class it is.

## The failure modes this structure detects

- **Mechanics cited for substance.** An instruction line supports where an
  amount is reported; it is cited as establishing that the amount is taxable.
- **Explanation cited for authority.** A publication's clear statement is
  treated as the rule, when it is a restatement of a rule that was never read.
- **Undated authority.** A provision cited without effective period, so a later
  amendment silently invalidates the model.
- **Imprecise locator.** A whole-document citation nobody can verify.
- **Unrelated sources stacked.** Several citations that each support a
  neighbouring proposition and none of which supports the one asserted.
- **Silent delegation.** A statute cited for a computation whose mechanics the
  statute expressly leaves to regulations that were not consulted.
- **Coordination missed.** A provision applied without the coordinating rule
  that reduces or conditions it — a failure that produces a plausible number.

## Method: constructing a coverage profile

The coverage profile defined in
[concept-coverage-and-claims.md](concept-coverage-and-claims.md) is built
against the intensional model, not against the implementation. The order
matters, because building it the other way produces a profile that is complete
by construction and says nothing.

1. **Declare the authority boundary first.** Jurisdiction, regime, period, and
   the classes of source that will be examined. The boundary is part of the
   result: a region outside it is *outside the declared authority boundary*,
   which is a different status from *unsupported*.

2. **Enumerate the concept's universe from authority**, not from the
   application's categories. What the law counts, including everything the
   build cannot handle.

3. **For each region, record the substantive proposition and its authority**
   under the seven requirements above. Regions whose authority is
   mechanics-only or explanation-only are marked partially supported at this
   step, before any implementation question arises.

4. **Identify the facts each region requires** — reported, economic, and
   circumstantial — and specifically which of them **no ordinary document
   discloses**. This is where invisible gaps are found, and it is the step most
   often skipped, because it is the only one that cannot be done by reading the
   code.

5. **Only then compare against the implementation**, and assign a status from
   the closed vocabulary. A region that does not fit an existing status is a
   finding about the vocabulary; inventing a status to make a case fit destroys
   the vocabulary's meaning and is a defect this milestone committed and
   repaired.

6. **Separate the actionable gaps from the residual risk.** The gap list is a
   lower bound. Record what depth of authority examination and what adversarial
   effort produced it, because those two numbers are the only bound on what is
   *not* on the list.

The profile is versioned with the content it describes. It is a claim about a
build, and it expires.
