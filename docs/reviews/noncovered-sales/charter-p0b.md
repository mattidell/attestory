# Charter: P0b of noncovered sales — the engine and recording change

Role: Builder. Source HEAD on milestone/noncovered-sales-2025.
Plan: docs/phases/engine-breadth/milestones/noncovered-sales.md (read it
whole, especially Decisions and "Track 0 adversarial closure"). Evidence
to build on: noncovered-sales-evidence/track0-closure.md,
track0-output.json, track0.py, prototype.py and prototype-rules/. Do not
read governance.

Owner, 2026-11-06, on the Track 0 FAIL: change the engine and recording
surface first, then rerun Track 0 and build v79. This unit designs that
change and proves it on scratch. It does not land production code.

## Scope

1. **One answer closes several families.** Today admission takes exactly
   one current true closure finding per family horizon, and a shared
   horizon id is `HorizonModelError` (`one_finding`, `eight_findings`,
   `duplicate_horizon`). Find where this is decided (closure-mapping
   admission in packages/derivation and packages/tax, the
   `source-closure-mapping` schemas, marshalling of the closure fact
   type). Design the smallest change that lets one filer answer ("Did you
   sell any securities whose basis was not reported to the IRS?" = no)
   close all eight noncovered families empty, and lets a later yes plus a
   recorded sale reopen exactly the families that sale belongs to.
   Compare at least: (a) a new closure-mapping schema version naming
   several families for one question; (b) a derived per-family closure
   from one recorded answer through the existing derived-answers path
   (PR #255); (c) the existing pattern every earlier breadth milestone
   used (one closure answer per family, asked together in round one, as
   W-2G and gambling losses did). For (c), say what the filer actually
   sees and whether it already meets the owner's intent; the owner chose
   one question, so (c) is a comparison, not the answer.
2. **Covered-family flag.** A covered sale whose `basis_reported_to_irs`
   becomes no (`covered_flag_no_path_a`, `covered_flag_corrected_to_no`)
   still publishes line 8a. Design the fix: a covered-family successor
   with the ADR-0079 family handover (precedent:
   packages/tax/ssa_family_handover.py and the Form 1099-K handover), or
   a refusal that needs no handover. Say which v78 workspaces it touches.
3. **Scalar identity exclusivity.** Say whether Track 0 needs it once the
   constraints sit on the sale object (design change 1), or whether it can
   be dropped from Decision 6. If needed, the smallest change.
4. **Prove it.** Apply the chosen change in a scratch copy only (a scratch
   module or monkeypatch under the evidence directory; no edits under
   packages/). Rerun `track0.py` cases on it. Show `wage_unclosed`,
   foreign tax, exempt interest and student loan with one answer instead
   of eight, `one_finding`, the late-member reopen, and the covered-flag
   cases. Measure every other v78 live return the existing current-core
   harness (tests/helpers/current_core_returns.py) can build.
5. **Contract.** Name each schema version, ADR (new or superseding), and
   loader switch the production change needs, and whether any of it falls
   under packages/kernel/. Kernel edits are off-limits (PR #258 owns the
   kernel): if the change needs the kernel, stop and report the smallest
   kernel change.

## Deliverables

noncovered-sales-evidence/p0b-engine-design.md: the cause with code
references, the options compared, the chosen change, the scratch proof
with a cases table, the contract list, and a one-paragraph
recommendation. The scratch module and its JSON output. Fill the plan's
"P0b result" section with a short summary that links the evidence. No
production, test, schema or content edits.

## Rules

Synthetic demo.* only; no absolute paths in committed files. Commit
incrementally with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
retry every 10 s up to 5 min if held); never --no-verify; never bare git
stash. Foreground commands only; no pgrep or sleep waiters. No push or
spawn. Do not edit packages/kernel/. Commit after each scope item.
