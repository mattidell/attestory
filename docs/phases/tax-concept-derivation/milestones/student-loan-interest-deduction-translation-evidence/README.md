# Student Loan Interest Deduction Translation — retained evidence

Evidence from a milestone that **closed explicitly partial** on 2026-09-14: a
completed bounded investigation with no production path. The closed plan is
[`../student-loan-interest-deduction-translation.md`](../student-loan-interest-deduction-translation.md);
its deferral ledger is authoritative for what a resumed milestone must preserve.

**Nothing here is an accepted contract.** No ADR, schema, content, package
version, or production code came out of this milestone.

| Artifact | Establishes | Evidence level | Who may use it | Must revalidate | Does not authorize |
| --- | --- | --- | --- | --- | --- |
| [`p1-loan-qualification.md`](p1-loan-qualification.md) | The tax boundary of the six § 221(d)(1) loan-qualification constituents | Statute and regulation, read directly | The **resumed student-loan vertical** | Statutory currency, if years pass | Any implementation; it selects nothing |
| [`p1-obligation-and-amounts.md`](p1-obligation-and-amounts.md) | The tax boundary of obligation, the two § 221(e)(1) operations, and § 221(c) dependent status | Statute and regulation, read directly | The **resumed student-loan vertical** | Statutory currency | Any implementation |
| [`p2-source-and-entry.md`](p2-source-and-entry.md) | How Form 1098-E contribution, closure, witness identity, lifecycle, and entry behave | **Observations at the source state examined during this milestone** | Any later work needing to locate consumers or comparison surfaces | **Every specific claim, against current code** | Any conclusion that current behavior still matches |
| [`p2-computation-and-consumers.md`](p2-computation-and-consumers.md) | Worksheet gates and arithmetic, the subtotal authority constraint, Schedule 1 and AGI propagation, the reader surface | **Observations at the source state examined during this milestone** | Same | **Every specific claim, against current code** | Same |
| [`p3-partial-design.md`](p3-partial-design.md) | What a per-statement path would have to do, and why each candidate shape fails | A requirements and design record | Any later work needing the requirements | **Every claim about current machinery**, against the source present when that work begins. Its requirements and rejected shapes are starting hypotheses, not findings | **Not a contract**; not evidence the proposed mechanisms work. Obligations 2a and 2b are undischarged |
| [`../../../../prototypes/sli-eligible-student/`](../../../../prototypes/sli-eligible-student/) | The bounded dispatcher and coverage failure, reproducibly | **Executable.** Real evaluator and real dispatcher, inside a hand-built environment | The **proposed prerequisite milestone** — start here | **Rerun it on that milestone's starting commit** to reproduce the bounded negative result before relying on it | Anything beyond its stated limits: hand-built environment, authored pins, projection over synthetic rows, partial tax expression, conceptual completeness check, unproven pin isolation |

## The result this evidence supports

No committed path currently uses every current Form 1098-E box-1 statement as the
iteration subject, requires exactly one usable statement association, resolves
this case's heterogeneous related facts, fails closed on an unassociated
statement, and preserves statement-isolated dependencies. The actual pairing
dispatcher iterates existing pairing records, so an unpaired box-1 statement is
never visited and produces neither a publication nor a blocked row.

That is the bounded formulation. It is **not** a claim that the engine cannot
generally evaluate per identified item.

**This observation is expected to expire.** It describes the machinery as it
stands. After the prerequisite is implemented the negative result may properly
cease to hold — that is the point of doing the work. A later milestone must not
simply delete it, and must not keep citing it either: it must **replace** it with
a positive executable case proving complete subject accounting, heterogeneous
binding, failure preservation, and subject-specific dependency isolation. Until
such a case exists, the
probe on that milestone's starting commit is the evidence of record.

## Routing

The proposed prerequisite —
[`../PROPOSED-identified-evaluation-context.md`](../PROPOSED-identified-evaluation-context.md) —
routes **first** to the executable probe and its findings, and may use the P2
observations as starting hypotheses. It must not treat the P1 tax analysis as an
engine-contract specification, nor the P3 design as a selected implementation.

The authoritative institutional catalog remains a **separate required blocker**,
sequenced after that prerequisite. Statement-specific explanation remains a
**production condition** for the resumed vertical.
