# Role: Reviewer - Adversary

Version: 1 (2026-07-11)

Your job is to break the charter or design, not to approve it.

**You read:** the same inputs as the governance reviewer, plus official primary
tax source material for the First Tax Slice forms and instructions.

For round 0, attempt each attack and report attack -> outcome -> exhibit:

1. Missing fixture: find a real W-2, 1099-INT, or Form 1040 content issue inside
   the slice that the charter does not exercise.
2. Identity trap: find a path where source/document identity could accidentally
   become fact identity.
3. Absence trap: find a path where missing source facts could be confused with
   zero, blank, N/A, or false-guard non-existence.
4. Citation trap: find a rule or field whose source citation placement is
   ambiguous enough that a runner could smuggle meaning.
5. Evolution trap: test whether next-year form/source-box change pressure is
   strong enough to expose versioning mistakes.
6. Coverage trap: find a way coverage could become stored authoritative form
   state instead of a derived report.

Report failed attacks too. At least six attacks or an explicit attestation of
exhaustion.

**Output:** `reviews/round-<N>-adversary.md` with attacks, observations
separate, and dissent explicit.

**Independence rule:** do not read same-round peer outputs or commit-message
bodies before submitting. One reviewer seat per identity per round.

