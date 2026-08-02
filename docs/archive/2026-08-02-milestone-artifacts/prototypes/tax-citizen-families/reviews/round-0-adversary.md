# Round 0 Adversarial Review

- Reviewer: adversary
- Date: 2026-07-11
- Subject: `charter-it1.md` sufficiency before builder dispatch
- Instrument: six declared attacks from `roles/reviewer-adversary.md`

I read the charter and the official IRS material named below. I did not read
same-round peer review output or commit-message bodies before submitting this
review. This is a review of the fixture charter, not an approval of a future
candidate design.

## Attacks

### A1 — Missing fixture: 1099-INT has more than one federal meaning

**Attack.** Use a 1099-INT with box 1 interest, box 2 early-withdrawal penalty,
box 3 U.S. Savings Bond/Treasury interest, or box 8 tax-exempt interest. Ask
whether the source fact type and the line 2b bridge can reject an incorrect
box-to-line mapping. A nominee statement is another live case: the full
reported amount and the amount belonging to another owner cannot both be the
taxpayer's line 2b income.

**Outcome.** **Failed attack against the charter: the charter does not exercise
these cases.** F2 requires one synthetic 1099-INT taxable-interest instance and
requires source-box meaning to differ from form-line meaning, but it does not
name the box or require a counterexample. F8 names citations for 1099-INT but
does not make the edge semantics executable. The 2025 IRS Form 1099-INT
instructions and Publication 550 distinguish these fields and state that the
box 2 penalty is deducted separately while box 1 interest remains included.

**Exhibit.** [2025 Form 1099-INT instructions](https://www.irs.gov/instructions/i1099int)
and [Publication 550 (2025), Investment Income and Expenses](https://www.irs.gov/publications/p550).

**Required disposition.** Add at least one negative or paired fixture: box 1
taxable interest with box 2 penalty, or box 3/8 interest that must not be
silently treated as ordinary box 1 input. If the case is intentionally out of
scope, say so in F2 rather than relying on "taxable interest" as an unstated
filter.

### A2 — Identity trap: source/document identity can still become fact identity

**Attack.** Construct two W-2 documents for the same synthetic employee,
employer, and tax year, with distinct box 1 values. Also construct the IRS
permitted multiple-form case where identifying information is repeated but the
forms carry different reported items. Test whether the facts remain distinct
by declared fact identity and whether replacing or re-uploading a document
changes only evidence standing.

**Outcome.** **Attack succeeds.** F1 has two W-2 source instances and says not
to make facts document-children, but it does not force the candidate to
survive same-entity/same-period documents or a corrected/reissued document.
A design can therefore pass F1 while using an opaque document id as a hidden
fact key, or while collapsing two legitimate values into one. The charter also
does not require the evidence-removal/re-upload peerage probe.

**Exhibit.** `charter-it1.md`, F1 and F10; [2025 General Instructions for Forms
W-2 and W-3](https://www.irs.gov/pub/irs-prior/iw2w3--2025.pdf), section
“Multiple forms.”

**Required disposition.** Add an identity-collision fixture with two same-
employer/same-year forms and a document replacement/removal mutation. Require
the examination to show the fact identity key and to demonstrate that evidence
identity is not in it.

### A3 — Absence trap: zero, missing, invalid, and non-existent remain
underspecified

**Attack.** Run four states for one included output line: (1) a present source
finding whose value is zero, (2) an empty source set with a closure assertion,
(3) no source and no closure assertion, and (4) a present but schema-invalid
source value. Then run a false guard for a mutually exclusive line. Compare
published findings, block codes, rendering metadata, and explanation paths.

**Outcome.** **Attack succeeds.** F3-F5 and F7 cover some of the intended
distinctions, but the charter does not require a present-zero source, an
invalid source, or a rendered/recorded blocked state. It also does not require
the negative result that invalid input cannot be converted to zero or reused
as an unclosed-source block. “Guard/non-existence” is named without requiring
the guard and its inapplicable disposition to be declared in the artifact.

**Exhibit.** `charter-it1.md`, F3-F7 and the Evidence And Decision Gate;
`packages/derivation/evaluator.py` currently distinguishes closure blocking,
but the Track 0 charter must establish the tax-content contract rather than
inherit evaluator behavior.

**Required disposition.** Add the four-state matrix above, or explicitly
bound the invalid-input case to a later track with a reason. Require an
explanation assertion for each state and require no published finding for
unclosed, invalid, and false-guard cases.

### A4 — Citation trap: a citation can be present without being authoritative

**Attack.** Replace a source citation with a broad IRS landing page, the wrong
tax year, or a locator that does not identify the box/line/rule. Then remove or
alter the citation while leaving a hidden runner mapping unchanged. Ask whether
schema validation rejects the instance, whether package closure catches the
wrong source, and whether output bytes remain independent of citation text.

**Outcome.** **Attack succeeds.** F8 says each listed fact/rule “cite[s] their
official source,” but it does not define a citation citizen/shape, required
year and locator, or the boundary between explanatory provenance and executable
meaning. A candidate can satisfy the English requirement with a notes URL while
the runner smuggles box mappings, thresholds, or form relationships in code.
No fixture mutates a citation or proves that citations are non-operative.

**Exhibit.** `charter-it1.md`, F8 and Q5/Q8; [2025 Form 1040](https://www.irs.gov/pub/irs-prior/f1040--2025.pdf),
which distinguishes line 1a, line 2b, line 9, line 11a, line 12e, line 15, and
line 16 rather than treating a form URL as their meaning.

**Required disposition.** Require a fully resolved citation instance with
document identity, tax-year applicability, and a precise locator. Add a
negative mutation that removes the locator or changes the year, and a parity
check showing citation text cannot alter evaluation.

### A5 — Evolution trap: the sketch does not prove version boundaries

**Attack.** Take a 2025 package and apply both kinds of change named by F9:
change a tax-year parameter and change a source-form structure. Verify that
the old published citizen/schema remains immutable, that an old-year artifact
does not consume a new-year box, and that the semantic identity of an
unchanged field is not accidentally regenerated under a new id.

**Outcome.** **Attack succeeds.** F9 asks for one parameter change and one
structural change to be sketched, but it does not require an executable
cross-year instance, rejection of mixed-year package members, or an
immutability check. This is not hypothetical form churn: the IRS 2026 W-2
instructions describe Box 14 being split into Boxes 14a and 14b, while the
2025 Form 1040 has its own dated line layout and standard-deduction values.
The charter's unspecified tax year makes the version boundary harder to audit.

**Exhibit.** `charter-it1.md`, F9; [2026 General Instructions for Forms W-2 and
W-3](https://www.irs.gov/instructions/iw2w3), “Changes to boxes 9 and 14a” and
“Box 14 ... split into box 14a and box 14b”; [2025 Form 1040](https://www.irs.gov/pub/irs-prior/f1040--2025.pdf).

**Required disposition.** Name the tax year in the charter and turn F9 into a
small versioning fixture: one old-year positive, one new-year positive, one
mixed-year negative, and one assertion that old schemas/artifacts are not
mutated.

### A6 — Coverage trap: “can say” is not a recomputation contract

**Attack.** Produce the F11 coverage/gap report, delete its materialized
projection, rebuild it from the act log/read models, and compare bytes. Then
inject a stale “closed” report while leaving the source-set closure act open.
Ask whether the system recomputes current coverage and whether the stale
report can become authoritative form state.

**Outcome.** **Attack succeeds.** F11 says coverage “can say” which closure
assertions remain open and says not to store coverage as authoritative form
state, but it does not require a report schema, source inputs, recomputation
parity, stale-report rejection, or a proof that coverage is not admitted as an
act. Q9 states the right principle but does not make it measurable in the
fixture charter.

**Exhibit.** `charter-it1.md`, F11 and Q9; [Article 14](../../../governance/constitution.md#article-14--record)
requires coverage observed to belong to the record while coverage available
now is computed fresh.

**Required disposition.** Add a rebuild-and-stale-projection test. The expected
result should be byte-identical fresh coverage from current acts, with the
stale projection ignored or rejected and open closure assertions reported as
gaps.

## Failed attacks and observations

- I tried to attack the charter for not deciding whether form fields are
  first-class citizens, rule-output symbols, or generated content. That attack
  **failed**: Q2 explicitly makes this the decision question, and F6/F7/F9
  provide the right pressure points. The omission is not a missing fixture;
  the candidate still needs to answer it with evidence.
- I tried to attack the charter for omitting broad filing-status and Schedule B
  behavior. That attack **failed as a scope objection**: the charter explicitly
  places those matters out of scope, while retaining enough Form 1040 identity
  to test the narrow line bridge. The 1099-INT box distinctions in A1 are
  different because they affect the included line 2b bridge itself.
- F12 is directionally sound: it requires positive and negative examples for
  new or amended families. It does not, however, cure A3-A6 because those are
  behavioral/evolution fixtures, not merely schema examples.

## Dissent and recommendation

I dissent from opening the builder seat on this charter as written. The
questions are well chosen, but six attack surfaces can pass without producing
evidence: A1 through A6 above. Amend the charter before dispatch, at minimum
adding the identity-collision mutation, the four-state absence matrix, the
resolved-citation mutation, the cross-year mixed-package negative, and the
coverage rebuild/stale-projection check. The 1099-INT edge case should either
be added or explicitly excluded with a reason tied to the slice boundary.

The charter is otherwise suitable for a first candidate iteration: it names
the relevant citizen families, has a real rival requirement, and asks the
correct Tier 2-versus-Tier 1 question. This review does not recommend a new
ADR yet; the evidence gate should first produce a candidate and a rival under
the amended fixtures.
