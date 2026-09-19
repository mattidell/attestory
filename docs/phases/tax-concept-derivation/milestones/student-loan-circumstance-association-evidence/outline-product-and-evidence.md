# Outline — product and evidence

Work sequence item 1 of
[the milestone plan](../student-loan-circumstance-association.md). This is an
outline for review, not a design and not a specification. Every claim below
about existing software is **evidence level `read`**: it comes from reading
committed source at `b4f601f6`, not from executing anything. Section 9 says
which claims must be raised to `run` before they can carry a build.

## 1. What we are trying to do, in ordinary words

A lender sends a form that says: *this borrower paid us $2,000 of student loan
interest last year.* A person can say true things about their schooling: *in
the autumn term I was taking two evening classes and was not enrolled in any
degree or certificate program.*

Neither statement is useful alone. The tax treatment of that $2,000 depends on
what the borrowing was **for** — and the form never says. To apply the person's
answer to the lender's number, the application has to know that the schooling
the person described is the schooling that the borrowed money paid for.

Today the application does not know that, and cannot find it out. The previous
milestone proved a calculation method works, but it was **handed** the
connection: its test simply declared that the one statement in the workspace
and the one schooling answer in the workspace belonged together. This milestone
is about obtaining that connection honestly, keeping it, getting it back later,
and using it.

## 2. The interaction

The person is shown a statement they have already entered — a named lender, a
statement reference, a tax year, an amount. They are asked, in substance:

> Was all of this interest on one loan? And what schooling did that loan pay
> for?

They answer with circumstances, never with a conclusion. They do not say "I was
an eligible student" and they are not asked whether their school's credential
was legally recognized. They say which period of schooling the money was for,
and what they were doing in it.

They may also be unable to answer — the loan paid for two terms, or they do not
know how the lender combined several loans into one number. **That is a
legitimate outcome**, and the application must be able to end up knowing that
it does not know.

## 3. The four things being related, and why they are not the same thing

The work is difficult mostly because these are routinely confused:

| | What it is | How it is identified today |
| --- | --- | --- |
| **The report** | A lender's document about a year | `lender` + `statement` + `tax-year` |
| **The borrowing** | The actual loan the money came from | **Not represented at all** |
| **The period** | A span of schooling | A period fact's own stable id |
| **The person's circumstance** | What they were doing in that period | A period-keyed fact |

The report and the borrowing are the pair most often collapsed, and collapsing
them is not a modelling shortcut — it is a factual error. Form 1098-E box 1 is
**one number aggregating every loan that lender serviced**, with no per-loan
identifier. So a statement is not a loan, and matching a statement never
establishes which borrowing an amount concerns.

This is not a new insight in this repository. The nominee vertical met the
identical problem on Form 1099-INT and wrote it down
(`packages/tax/identity_association.py`, module docstring): a statement match
proves "only *which report* the acquisition's interest was reported through —
never, by itself, that a specific obligation is the one that report's amount
concerns." Student loan interest is the same shape.

## 4. How the relationship can be wrong while every value is right

These are the failures worth designing against. In each, no individual number
or rule is incorrect.

1. **Silent adoption of a coincidence.** One statement, one schooling answer,
   so they are treated as a pair. This is the prior milestone's stipulation,
   and it is the failure most likely to be reintroduced by accident, because
   cardinality-one makes it invisible.
2. **Leakage across subjects.** Two statements, two different circumstances;
   the wrong circumstance reaches the wrong amount, or one answer is silently
   applied to both.
3. **A relationship that outlives its support.** The period it names is
   corrected, retracted, or replaced, but the connection still resolves and
   still looks sufficient.
4. **Invisible omission.** A statement with no relationship is never visited,
   so it produces neither an answer nor a refusal. Nothing is wrong on screen;
   something is simply missing. This is the hardest to test for, because the
   defect is an absence.

## 5. What prior work established — and it is more than expected

Tracing the producer and consumer paths found adopted production machinery for
most of the *recording* half of this milestone, on a structurally identical
problem:

- **Recording ordinary answers.** `packages/tax/nominee_allocation_recording.py`
  admits ordinary answers through the real contribution boundary, mints opaque
  workspace ids for people rather than deriving them from typed names, carries
  retraction in a separate helper, and owns its own durable act-log
  persistence. Its finding carries the answer with `basis: "attested"`; the
  enclosing act carries who said it and when. It publishes no rule.
- **Recovering them.** `nominee_allocation_recovery.py` rebuilds from the
  committed act log **only**, exposes current findings at an identity tuple
  with attribution, and distinguishes a retraction by another actor from the
  original speaker recanting.
- **Asserting a relationship.** ADR-0068 and `identity_association.py` publish
  a one-sided pairing as an independent `derived-finding.v2` — not a field on
  either side. Candidates are narrowed by available references, and
  **confirmation is mandatory at every tier**, explicitly because narrowing is
  not evidence of correspondence.
- **Using it per item.** ADR-0070/0071 `packages/derivation/pairing_dispatch.py`
  evaluates a rule once per pairing finding, resolving each side by the
  pairing's own pinned `left_fact_id`/`right_fact_id`, pinning both sides and
  the pairing, publishing at most one finding per pairing, and blocking a
  single pairing with `DEPENDENCY_ABSENT` naming the fact id it could not
  resolve. Its parameters (`pairing_type`, `left_type`, `right_type`) are
  generic.
- **Lifecycle.** ADR-0073 gives correction, retraction with no opposite claim,
  and reassertion at a stable `fact_id`.

Taken together, failure 3 and the "missing target" case are close to *already
handled* by adopted code, and the confirmation-not-inference answer to failure 1
is an adopted decision rather than a new proposal.

## 6. What is newly discovered, and what it changes

**The engine's ability to follow an asserted relationship lives in exactly one
place, and it is not the evaluator.**

`evaluator.py:125` resolves `ref` against a literal name in `env.symbols`; there
is no operator taking a fact id from a value. More strongly, `env.sources` rows
are **bare values carrying no identity** (`rows = env.sources.get(name, [])`),
so a rule expression cannot tell which member a value came from. No composition
of the closed operator set can relate one statement to one circumstance.
`collect_categorical_all_equal`'s own comment records why it had to exist: an
unkeyed `ref` would otherwise force marshalling to pick an arbitrary current
finding. `input_bindings` match by **fact type only**
(`marshal.py:_fact_id_has_type`), never by key.

One operator is worth naming so it is not mistaken for a way around this.
ADR-0074's `bound_sources` reads a group that was *already selected for it*, so
the identity work again happens outside the evaluator; ADR-0074 also forbids
any rule other than the one it names from using it without a new decision. It
is not a general keyed-access mechanism.

`pairing_dispatch.py` states the same boundary from the other side — an
ordinary declared family has "no dereference of a fact id stored inside another
finding's value" — and then performs that dereference itself, outside the
evaluator.

Three consequences follow, and two of them change the plan.

**(a) The prior milestone's tested rule cannot be lifted into pairing scope.**
`pairing_consequences._pairing_local_environment` builds an environment whose
symbols are exactly the two paired values, with **empty sources and empty
closed sets** — deliberately, so an expression cannot read cross-cutting global
state. So inside pairing scope `require_closed`, `count`, `collect`, and
`collect_categorical_all_equal` all block, and only two symbol names exist. The
prior candidate rule refs five names and gates on
`require_closed` + `count(box1) == 1`. That cardinality gate is precisely what
pairing scope *replaces*; it must be deleted, not carried forward. The plan's
step 5 — "feed recovered inputs to the bounded consequence consumer" — therefore
understates the work: the consumer must be **restructured**, and that is a
design task with a product consequence (see decision U1).

**(b) Completeness of iteration is the unsolved part, and nothing flags it as
such.** The dispatcher iterates the pairings a run has
(`[s for s in sources if s.name == pairing_type]`). A statement with no
relationship is never visited — failure 4. Nothing in the recording half fixes
this.

Two precisions. The plan's sequencing (step 4 recording, step 5 consumer) is a
natural build order, not a stated judgement about difficulty, and its case list
already requires the absent-relationship case; the point is that neither marks
this as the harder half, so it is easy to arrive at it late. And this is the
same class of gap the prior milestone's deferral ledger named as E3
("differentiated or bounded multi-statement behaviour — unbuilt production
obligation"), not a diagnosis E3 already made: E3 is broader, and locating the
gap at the dispatcher's iteration source is new here.

**(c) A constraint on the obvious repair.** Accounting for every statement by
collecting over the Form 1098-E family runs into ADR-0016, enforced in
`source_authority.audit_collect_authority`: a rule collecting over a mapped
family must publish exactly that family's authorized subtotal symbol. A new
completeness rule cannot simply collect that family and publish a new symbol.

## 7. Consequential uncertainties

Each is a decision, not a task.

**U1 — What is the person asked, and is their answer one fact or several?**
Pairing scope offers two symbols. ADR-0067's `field` selector can read named
properties off a bound finding's value object. That makes "one circumstance
finding with a structured value" the shape the mechanism favours, against the
prior milestone's several separate premise facts. *Why it matters:* it changes
what the person is asked and what a single correction corrects. *Depends on it:*
the recording payload, the consumer's expression, the correction cases.
*Resolved by:* section 9's first check supplies the mechanical half — that a
structured value can be read pairing-scoped at all. It does **not** settle the
product half: whether one structured finding gives the right correction
granularity is a judgement about what a person should be able to revise alone,
and needs an owner decision rather than a passing test. *When:* before any
producer is chartered.

**U2 — What accounts for a statement with no relationship?** Options: a
separate closed-family rule over statements (constrained by (c)); a
refusal-carrying record produced at the same time as the association; or an
explicit, bounded acceptance that this milestone does not close it. *Why it
matters:* it is the difference between a bounded honest result and a silent
wrong one. *Depends on it:* the exit criterion on multi-record isolation, and
whether Evaluation Context is genuinely reached. *Resolved by:* an executed
two-statement case where one is unassociated, with the expected disposition
stated in advance. *When:* this is the gate for Track 0.

**U3 — Is a separate borrowing entity needed now?** The pairing can name a
period directly and let the composition claim make the loan implicit, as the
earlier paper candidate proposed. That holds only while one statement means one
loan and one period. *Why it matters:* inventing a loan-account system with no
consumer is waste; relabelling a statement as a loan is an error. *Resolved by:* the plan's case list has already partly
constrained this — it requires exercising "two statements concerning one
borrowing" and "one statement covering more than one borrowing or period",
either through a selected representation or through honest unsupported
behaviour. So the open question is narrower than whether to model a borrowing
at all: it is whether refusal is an adequate answer for those two cases.
*When:* before the contract unit.

**U4 — Does the existing pairing seam generalise, or is a sibling needed?**
`pairing_consequences` binds two hardcoded fact-type constants. Reuse means
either generalising that environment or writing a parallel seam. *Why it
matters:* cost and blast radius; touching a seam that serves nominee interest
risks adopted behaviour. *Resolved by:* reading the call path and attempting the
narrow generalisation in a disposable copy first. *When:* at chartering.

**U5 — Reliance.** The owner intends to allow reasonable reliance on evidence
under a standing authorization. If that changes what the producer asserts
without a person's confirmation, it collides with ADR-0068's mandatory
confirmation. *Resolved by:* an owner decision, in ordinary language, only if a
concrete case forces it. *When:* only when forced; not opened here.

## 8. What would make a design unacceptable

Stated before choosing, as the plan requires.

- It infers a relationship from a name, an amount, a count, or a statement
  reference without a person's confirmation.
- A statement with no relationship yields neither a result nor a refusal.
- A relationship keeps applying after the support it names is gone.
- The person is asked for a legal conclusion, or for a fact about their
  institution they would not reasonably know.
- Correctness depends on there being exactly one statement, whether or not the
  code says so.
- The recovered path is exercised with any value the original caller kept in
  memory.
- It builds a general grouping or context mechanism to avoid answering U2.

## 9. The smallest evidence that would settle this

Two executed checks, in this order, before any production charter:

1. **Dereference check.** Build a disposable pairing whose left side is a
   Form 1098-E box-1 source and whose right side is a schooling-circumstance
   source, dispatch one declared rule pairing-scoped, and observe: the value
   the expression read, the pins on the publication, and the blocked code and
   named fact id when the right side is retracted. This raises sections 5 and
   6(a) from `read` to `run`, and either confirms or refutes that the adopted
   primitive carries this relationship at all.
2. **Omission check.** Two statements, one associated and one not. Record the
   expected disposition for the unassociated statement **first**, then execute.
   If the run is silent about it, U2 is a required design decision and not a
   deferral.

Both use synthetic `demo.*` identities with source values intact. Neither needs
a production change. A count of publications alone proves nothing here: the
first check must assert the *value read* and the *pinned finding ids*, and the
second must assert a named disposition for a statement that produced no row.

## 10. Proposed change to the plan

Recommended, on the evidence above:

1. **Reorder.** Make the omission account (U2) the subject of Track 0's gate,
   rather than a case carried through it. Recording and recovery have strong
   adopted precedent; iteration completeness does not.
2. **Restate step 5.** The prior bounded consumer is not reusable as written.
   Name it as a rule to be restructured under pairing scope, and treat its
   cardinality gate as something to remove.
3. **Add the two checks in section 9 as an explicit readiness gate** before
   chartering any producer, so no implementation is chartered on `read`-level
   claims about the dispatcher.
4. **Record U1 as an owner-visible product choice**, because it changes the
   question a person is asked.

Nothing here justifies changing the milestone's boundaries, non-goals, or its
refusal to select an Evaluation Context.
