# Charter: Track 0 rerun of noncovered sales over the P0b contract

Role: Builder. Source HEAD on milestone/noncovered-sales-2025.
Plan: docs/phases/engine-breadth/milestones/noncovered-sales.md (Decisions
1–9, "Track 0 adversarial closure", "P0b result"). Evidence:
noncovered-sales-evidence/track0-closure.md, track0.py, p0b.py,
p0b-engine-design.md. Gate: `PROJECT_PLANNING.md`, "Track 0 Adversarial
Closure Gate". Do not read governance.

## Scope

1. **Apply Decisions 8 and 9 to the scratch stand-in** (p0b.py; no edits
   under packages/):
   - A current "yes" on the shared noncovered answer stops admitting a
     family once a member is added to that family after the answer, the
     same way a per-family closure is stripped today. Re-answering admits
     it again. A "no" beside any member still admits nothing for that
     family.
   - A current covered sale member with `basis_reported_to_irs` no blocks
     with a dedicated code (name it, e.g. `BASIS_NOT_REPORTED_ON_COVERED`)
     and an explanation telling the filer to record the sale as a
     noncovered sale. Install and measure it on all five covered sale
     objects (covered short-term, covered long-term, covered long-term
     gain-only, both covered wash-sale objects). Show what the page shows.
2. **Rerun all six Track 0 artifacts** over the P0b design, writing a
   new section "Rerun over the P0b contract" in track0-closure.md (keep
   the first run as history). Each row PASS or FAIL with built evidence;
   no row passes beside a standing counterexample: each is fixed or
   refused by an answer, and the row says which. Include at least:
   one-no on every v78 live return tests/helpers/current_core_returns.py
   can build; late sale after "no"; late sale after "yes" (stale, then
   re-answered); "yes" then "no" with a member; the five covered-flag
   cases; flag corrected yes→no and no→yes; the loss and wash line 7a
   cases (−3000 / 3515; −2000 / 3635); boundary no with and without a
   member; the Schedule D attachment row on covered_both_boundaries_no
   (published with a null value — fix or explain).
3. Fill the plan's "Track 0 rerun" subsection with the six rows and the
   closing declaration, or the FAIL summary.

Stop and report if any row needs a kernel edit or a contract beyond
Decision 7.

## Deliverables

Updated track0-closure.md, the scratch module and its JSON digest, the
plan subsection. No production, test, schema or content edits.

## Rules

Synthetic demo.* only; no absolute paths in committed files. Commit
incrementally with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
retry every 10 s up to 5 min if held); never --no-verify; never bare git
stash. Foreground commands only; no pgrep or sleep waiters. No push or
spawn. Do not edit packages/kernel/. Commit after each scope item.
