# Retrospective: Sale Family Audit (2025)

Milestone key: sale-family-audit. Plan:
`docs/phases/engine-breadth/milestones/sale-family-audit.md`.
Closed 2026-11-09.

## What happened

The f8949-code-b retrospective asked for one audit of every sale family
instead of one inherited defect per milestone. P0 tabled every field a
Form 1099-B or Form 8949 sale record carries against the rules that read
it, and reran all 213 v81 returns in two answer modes: the harness's
default answers and the answers a truthful filer gives.

The honest mode found the most serious defect: on v81, no return with a
Form 8949 sale got a tax when the Exception 1 questions were answered
truthfully. Every earlier sale milestone tested with the default answers,
which are false beside a sale. P0 found seven more: zero-net sales
ignored on line 7a and the base, no box C/F count, box 1g and `long_term`
unread, rows not tied to their sale, and boxes 4 and 7 carried by nothing.

Track 0 passed all six rows after three repairs. The decided box 4 and
box 7 answers were one per return and stayed current when a sale from a
new statement arrived, so they became per-statement questions.

The fresh review matched every hand-computed value, and found two more
wrong-return paths: covered and code W rows with no sale of their own
still counted (inherited), and line 7b said Schedule D was not required
beside required attachments (new, exposed by the reworded questions). The
repair fixed both in place on the unmerged v82 and halved the live
module's runs. No engine, schema or recording change was needed.

## What worked

- Running every case in both answer modes. The defect that hid for five
  milestones showed up on the first honest run.
- Committing the audit as a test. It fails 56 times on v81 and passes on
  v82, and the reviewer showed it fails when a field loses its last reader.
- Rerunning v81 harnesses in a subprocess in P0 kept the #264 global leak
  out of the evidence.

## What to change

- A field the reworded question changes needs its readers re-audited too:
  line 7b read the Exception 1 answers, and was outside both the
  projection and the audit tables until the review.
- The audit covered sale records but not amount rows at first; a row with
  no sale is the same class of gap as a field with no reader. Audit both
  sides of every pairing.
- The live module started at about 694 coordinator runs. Assert run
  equivalence once and drop the repeats before the fixture is pinned, not
  after review.
- Evidence-backed live modules should run their harnesses in a subprocess
  or on private copies, as P0 did; CI's worksteal scheduler shares one
  process across modules.

## Follow-ups

Parked in the roadmap: box 4 withholding as a real family, box 7 read
only beside a loss, box 13, statement names in the box 4 and box 7
questions, the question-less Exception 1 refusal, the unasked boundary
answers, the kernel reverse presence check, and harness isolation.
