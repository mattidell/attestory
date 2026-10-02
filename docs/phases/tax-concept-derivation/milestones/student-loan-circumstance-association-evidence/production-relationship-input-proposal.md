# Production relationship inputs — selected meaning and bounded interaction

Status: **relationship meaning and identification threshold selected by the
owner on 2026-09-29; interaction is a bounded candidate**. A definite
relationship is recorded when the person can identify what they are
connecting. If they cannot distinguish the intended borrowing, schooling
situation or statement, their uncertainty is preserved without choosing for
them. An unknown interest amount does not make a known relationship uncertain.
This is ordinary identification, not documentary proof, an account-number
requirement or a legal determination. The candidate interaction below does not
select final wording or layout, a published schema, production identifiers,
interest allocation, tax treatment or ADR 0076 Part 3.

## Starting point

The existing plan already separates a borrowing that can persist across
statements, a schooling situation independent of any borrowing, and the
connection between them. It also separates a statement's inclusion of a
borrowing from how much of the statement's interest that borrowing accounts for.
An inclusion with unknown portion is a real state, not a whole-statement claim.
A person is asked for ordinary circumstances and connections, not whether a
loan qualifies for a deduction. They may stop or say they cannot tell. A
correction to one assertion must not rewrite another, though calculations that
actually depend on it must be reconsidered. These are the A1, A2 and A5
starting decisions; this proposal does not reopen them.

Track 12 showed that an account containing references does not itself assert
either relationship. Track 13 showed that *separately affirmative* synthetic
financing and named-statement claims can be contributed, corrected, withdrawn,
consumed and reopened with their own support. Its exact fixture fact IDs and
four-part SCHOOL key made the experiment executable; they are not selected
production input fields or person-facing identifiers.

## Recommended interaction

Give the person recognizable cards for what they have already described. In
**one review step**, show the two distinct statements the application can
record: what this borrowing paid for, and which statement includes its
interest. The person may affirm either, both, or neither and save once. If
they already said both clearly in one ordinary account, show both clauses for
one confirmation; do not make them repeat the account or pass two screens.
Each clause can be affirmed, denied, marked “I cannot tell,” or left unanswered
without forcing the same response for the other clause. Each can be corrected
or withdrawn independently later. The application
assigns stable internal addresses to the subjects and claims. It never treats
a matching lender, amount, date, account fragment, label or document order as
confirmation. A person need not know a loan's issuer, legal classification or
account number to distinguish the borrowing they mean.

| Person sees | Person affirms | Application records |
| --- | --- | --- |
| A borrowing they named, with their own label and any *optional* recognition clues they supplied; a schooling situation they described by period, school and course of study | “Some money from **this borrowing** paid for **these studies**.” | One affirmative financing claim about the two selected, current subjects, with its own answer evidence and correction history. This does **not** say the borrowing was used only for school, which expenses qualify, or how much was borrowed. |
| A particular saved 1098-E, shown with tax year, issuer as printed and box-1 amount, plus enough document context to distinguish two similar statements; their chosen borrowing | “**This statement includes interest on this borrowing.**” | A different affirmative claim about that one statement and borrowing, with its own evidence and history. It says “includes,” even when other borrowings may also be on the statement. It does **not** supply a portion or a whole-statement assertion. |
| An optional later scope or allocation question, only when that work is commissioned | No answer is requested by this bounded recorder. | No amount or whole-statement claim is inferred from either confirmation. The reported box-1 total remains the statement's own fact. A later amount claim would need separate meaning, evidence and lifecycle. Unknown amount does **not** unsettle either definite relationship. |

The existing whole-statement route that needs no borrowing remains available in
the milestone model. This proposal does not replace it with a placeholder loan
or implement it in this recorder.

### How someone recognizes a borrowing

The application first lets the person distinguish borrowings in their own
terms: for example, “the loan I took for autumn 2024” and “the later loan for
spring 2025.” If they know a lender, approximate date, servicer, or account
fragment, those may be shown as **clues**, with their source, to help recognition.
The application does not require them, infer that a servicer name is the lender,
or use a clue as the borrowing's identity. A servicer transfer can put one
borrowing on two statements; equal labels can describe different borrowings.
The person confirms when two references concern the same borrowing. That is
their account of continuity, not proof of the borrowing's legal classification.

The schooling choice shows the person's current description, such as
“Riverside College — BSc — autumn 2024,” rather than an engine fact ID. If two
courses at Riverside were taken in the same autumn, both remain selectable and
the application asks which was paid for. The description and its evidence stay
separate from the financing assertion: changing a course-load answer can
change a downstream conclusion without claiming that the borrowing changed.

If the person cannot distinguish two borrowings, two schooling situations, or
two similar statements well enough to name the intended pair, they can say so.
Keep their account, available clues and the unresolved connection; create **no
affirmative relationship claim for either candidate**. Do not choose the first
row, match equal values, merge possible duplicate loans, or turn uncertainty
into “no.” A known statement inclusion with unknown *amount* remains different
from not knowing whether that borrowing is included at all.

## Concrete examples

The labels and amounts below are synthetic examples of what might be displayed,
not required input fields or proposed database keys.

### A. Two confirmations, no allocation

The person has named “Autumn study borrowing” and described “Riverside College,
BSc, autumn 2024.” With “2025 Form 1098-E, Cedar Servicing, box 1 $1,200”
available beside it, one review might read:

> **Autumn study borrowing**
> - Some of this borrowing paid for **Riverside BSc, autumn 2024**. **Yes**
> - The **2025 Cedar 1098-E** includes interest on this borrowing. **Yes**
> - How much of its $1,200 is from this borrowing: **not asked here**.
>
> **Save these connections**

The person can change either “Yes” to “I cannot tell” before saving. One save
may record both affirmations. The interaction need not use these exact controls
or sentences; the two meanings must remain separately inspectable. If the
person affirms only one clause, the application records only that relationship
and preserves the other response or lack of response without guessing.

The application records **financing: yes** for the selected borrowing and
schooling situation, and **statement inclusion: yes** for that borrowing and
that one statement. One submitted answer can support two separately addressable
claim records, each preserving which clause was affirmed. It need not make the
person supply two evidence items or repeat an affirmation. The portion remains
unknown; $1,200 is the form's total, not an allocated amount or deduction.
No tax treatment is selected.

### B. What “cannot tell” preserves

The person has two borrowings labelled “Autumn loan” and “Other loan,” but
cannot recall which paid for the Riverside BSc. They can still describe the
schooling, and the application keeps that description and the unresolved
borrowing choice. Neither possible financing pair receives a “yes” claim. If
they can independently identify that the Cedar statement includes interest on
Autumn loan, its **statement-inclusion** claim may stand; it does not fill in
the missing financing claim.

Conversely, a person may know that Autumn loan paid for Riverside but cannot
tell which of two Cedar statements reports its interest. The financing claim
stands; neither statement receives an invented inclusion claim. “I cannot say”
does not retract an earlier affirmed claim. If the person means to withdraw or
question that earlier claim, the application must record that distinct action.

### C. Correct one connection, keep the other

Initially the person confirms that Autumn study borrowing paid for Riverside
and that the Cedar statement includes interest on it. A second borrowing,
“Campus borrowing,” has its own financing claim for Riverside and a different
statement. Later the person corrects the first account: Autumn study borrowing
actually paid for a separate Metro College course in autumn 2024. The
application retires **only** the prior Autumn–Riverside financing assertion,
records the affirmed Autumn–Metro successor with predecessor history, and
reconsiders results that read it. The Cedar–Autumn statement-inclusion claim
remains what the person said. Campus–Riverside and its statement remain
independently supported. Nothing in the correction decides whether either
statement's interest is deductible.

If instead the person corrects the *schooling description* for Riverside at
the same identified course of study (for example, its course load), the
financing assertions can continue to name that situation; conclusions reading
the corrected schooling fact are reconsidered. If the correction means it was
actually a different course of study, applicability of each connection needs
the person's clarification. The application does not silently retarget it.

### D. Withdraw one assertion

The person says, “Remove what I said about Autumn study borrowing paying for
Riverside; I am no longer asserting it.” The application ends current support
for that financing claim and retains its history. The Cedar statement's
separately affirmed inclusion of Autumn borrowing remains current, as do
Campus borrowing's financing and statement claims. The missing financing
connection is not recorded as an assertion that the loan paid for *no*
schooling. Any result needing that connection is reconsidered from its actual
remaining support; withdrawal alone does not select a tax result.

If the person instead withdraws only the Cedar–Autumn inclusion, Autumn's
schooling-financing claim remains current. There is no supported inclusion for
that statement until one is affirmed. A corrected box-1 amount likewise does
not rewrite either relationship. If a corrected statement changes or leaves
unclear **which borrowings it includes**, the application asks whether the
earlier inclusion still holds; it does not preserve it merely because the
statement can still be found.

## Proposed recording boundary

The later recorder should preserve the person's actual answer, the two
selected current subjects, the description and source context shown when they
answered, and each claim's own attributed clause, standing and predecessor
history. One submitted answer may support both claims, but their propositions
and lifecycles are separate. The storage shape must not force separate screens,
submissions, or repeated affirmations.
Only an explicit “yes” creates an affirmative relationship source. A “no,”
“cannot tell,” skipped question or unresolved choice remains distinguishable
in the supplied account, without manufacturing the opposite relationship.
Negative and uncertain responses are not tax dispositions.

The borrowing is a reusable subject, but this proposal does not require a
lender, account number, terms or balance. The schooling situation is not keyed
by borrowing, and the 1098-E is not a loan. Production internal addresses and
published schema shape should be selected during a later recorder charter from
these meanings and evidence needs. The Track 13 synthetic IDs, exact fact-ID
references and test-local categories are implementation evidence only.

## Selected meaning and next build boundary

**Selected:** a definite financing or statement-inclusion claim rests on the
person's ability to identify the specific things being connected, assisted by
recognizable descriptions rather than documentary proof. Either can be known
while the other is uncertain. An unknown interest amount leaves a known
statement-inclusion claim definite. Keep interest portion as a separate,
deferred claim. The two claims are independently recorded and correctable, not
necessarily affirmed through separate screens or submissions.

**Recommended interaction:** one review with two separately editable clauses,
saved in one action when both are affirmed. This is a candidate shape, not
final wording or layout. Treating an indistinguishable group as one borrowing,
requiring a lender or account number, or automatically matching clues would
materially change the selected behavior and is not commissioned. The next
bounded recorder charter may specify the smallest internal reference and
evidence shape and test correction/withdrawal across both consumers. It must
surface any new material product choice before implementing it. Interest
allocation and ADR 0076 Part 3 remain deferred.

Sources: [A1's ordinary questions](a1-stage2-what-is-posed.md),
[A1's resting and uncertainty distinctions](a1-stage3-resting-and-cannot-say.md),
[A2's applicability rules](a2-change-and-applicability.md),
[A5's borrowing selection](a5-stage1-borrowing-and-storage.md),
[A5's schooling and financing identities](a5-stage2-circumstances-and-keying.md),
[Track 12's reference boundary](track12-account-reference-boundary-report.md),
and [Track 13's executed experiment](track13-explicit-claim-recording-report.md).
