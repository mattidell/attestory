# Retrospective — Mortgage Interest and What the Loan Paid For

## What differed from the plan

The plan expected a design, then four production tracks, on the adopted
line 8a rule. That rule never read box 2: it collected principal from a
family of box 1 amounts, so the comparison saw zero and an over-limit loan
deducted the whole interest. No test supplied an over-limit principal. The
owner directed a separate content repair, core calculations v43.

Grandfathering needed a date comparison the rule language lacked. The owner
chose a narrow `date_compare` operator, ADR 0078, rather than withholding
the determined zero. Its left side admits any expression. The ADR says so.
Narrowing it would be a new schema version.

The owner's review of the revised design rejected a boundary the draft did
not support. A personal-expense zero still published for a grandfathered
loan, a refinance, and a two-property statement. Uncertainty was treated as
unsupported coverage. Determined zeros used the blocked field. No unit
obtained the person's answers.

Independent production review then returned revise. Three "can't tell"
answers were told as outside coverage, zero descriptions omitted part of
their basis, and saved tokens hid the offered answer. The v45 successor
names those conditions and still blocks the amount. The repair review
accepted that semantic result, not a publication verdict.

## What it cost

Design ran P0 through P7. P3's review found the live v42 defect. The
owner's own reviews found timing defaults that could reach a zero, dropped
date-validation checks and a year-0000 acceptance in the date unit. P4, P5
and P6 each returned corrections, including fixtures that did not store the
cases they described. P7 made third-party and partial
payment an exclusion. Production was four tracks, that review, and one
successor repair. The red check was four typing errors in two new test helpers.

## Follow-ups

- No browser observation of the mortgage page was obtained.
- Allocation, multiple statements, mixed use, refinancing, and the mortgage
  credit stay excluded.
- The configured standard deduction is not the verified 2025 amount.
- The correction session still resolves an older registry and does not carry
  this route.
- One ownership sentence still uses personal shorthand for a filing-unit
  question. The input and the saved label do not.
- The phase still needs a contrasting tax area. None is selected.

## What should change in the next plan

Characterize an adopted limit with an over-limit principal. A comparison
that only sees zero cannot fail. Give every "can't tell" its own reason
beside the yes and the no, and show the answer the person chose rather than
the stored token. Check that a fixture stores the filing status and the use
its description names.
