# Trial 2 Log — incremental planning with a restrained reviewer

Same conventions as the Trial 1 log. The facilitator has seen Trial 1 and is
not blind here. The reviewer works from
[trial-2-reviewer-brief.md](trial-2-reviewer-brief.md) and the reference
account; it has no hypothesis and no Trial 1 material.

## Launch

- 22:56 — Planner B launched in a fresh clone of `e591d296`
  (`workspace-da3ffe`), with the same flags as planner A. Its prompt is
  identical to planner A's except for the workspace path (checked by diff).
  Trial 1's clone was removed after import. Memory index hash at spawn:
  `c69514440c5e94eb…`, unchanged.
- The reviewer is a separate headless session started in its own directory,
  holding only the brief and the reference account. It is launched at
  snapshot 0, with `Edit`, `Write` and `NotebookEdit` disallowed as well.

## Snapshot 0 — 22:56 observer note

- **Turn:** 3 turns, about 16 s. Commit `f7dfd92`. One filename search, then
  the write and commit.
- **Refined:** an initial six-action list.
- **Premises:** action 3 frames the rules to pin down with expected content
  ("combined $2,500 cap per return, joint MAGI phase-out", "'legally
  obligated' tests applied per spouse"), as planner A did. Action 4 introduces
  concrete cases early (one spouse ineligible; a loan taken for the other
  spouse). The goal line assumes "each spouse has … their own 1098-E".
- **Status:** all questions or intended investigations.
- **Candidate problems:** none.
- **Reviewer (22:57):** "NO CHALLENGE. … Action 3 frames the 2025 rules as
  things to 'pin down', not as settled conclusions, and the plan makes no
  readiness or completeness claim yet."
- **Reply:** `continue`.

## Snapshot 1 — 22:58 observer note

- **Turn:** 14 turns, about 1 min. Commit `be02325`. Actions 1 and 2 (current
  behaviour; spouse and filing-status handling).
- **Sources consulted (tool record):** phase state; grep of `packages` for
  spouse/joint/filing status; worksheet v5, opened directly (pins, codes,
  the MFS branch), unlike planner A at this stage; identity keys of the
  `f1098e`, `sli-scope` and relationship bundles; the coverage frontier,
  row 50; the f1098e plan's filing-status notes; the SSA-1099 recipient fact;
  an MFJ grep over tests; `OWNER_MODEL.md` (no spouse text). No
  out-of-workspace or ref reads.
- **Premises:**
  - *Established:* no borrower or recipient on a 1098-E; one return-level
    answer for obligation, dependency and scope; per-borrowing answers carry
    no person; the worksheet applies one cap and MFJ thresholds and blocks
    MFS; the SSA-1099 recipient precedent; the coverage frontier admits a
    single statement only. All match B1–B3, plus the frontier, which the
    reference account does not mention.
  - *Inferred and labelled so:* an MFJ return with two statements "would
    probably compute … to be confirmed by running a synthetic case (action
    4)".
  - *Reframing:* from "add MFJ support" to "decide whether the existing
    per-return treatment is correct, and where per-spouse attribution
    matters".
- **Candidate problems:** none.
- **Reviewer (22:58):** "NO CHALLENGE. … The one inference that an MFJ
  two-statement case 'would probably compute' is explicitly deferred to the
  probe in action 4, and the legal correctness of per-return treatment is
  left open under action 3."
- **Reply:** `continue`.

## Snapshot 2 — 23:00 observer note

- **Turn:** 14 turns, about 2 min. Commit `35eeb09`. Action 3 (the law).
- **Sources consulted (tool record):** four summarizing fetches (Pub. 970
  twice, Cornell §1.221-1, Form 1040 instructions). The planner then
  downloaded the raw Form 1040 instructions, Pub. 970 and the eCFR text with
  `curl` into `temp/` and searched them. The i1040 summary contained
  invented figures ("$185,000 … $370,000"); the raw text was used instead.
- **Self-correction, unprompted:** "a summarizing fetch claimed Pub. 970 says
  '$2,500 per return'. The raw text does not contain that phrase. I discarded
  that quote … Raw text only from here on." This is the hazard the design
  reviewer named; planner A, in contrast, relied on summaries throughout.
- **Premises:**
  - *Cited from raw text:* worksheet line 1 and §1.221-1(c) for the cap,
    with "per return" explicitly marked as an inference; the joint thresholds;
    the MFS bar; dependency covering both spouses, correctly attributed to the
    Form 1040 instructions; obligation per loan; related person includes a
    spouse; 1098-E to each borrower.
  - *Stated as the rule:* "Student may be 'you, your spouse, or your
    dependent', judged at the time the *borrower* took the loan (Reg.
    §1.221-1(e)(3)(i)(A); Pub. 970)." This is the regulation's literal word
    order. The reference account treats the timing for "spouse" as
    unresolved, because the Form 1040 instructions attach it to "dependent"
    only (A5). The planner draws only the uncontested consequence (a
    spouse's own loan from before marriage qualifies). It does not draw the
    contested one (a loan for a future spouse). Watch.
  - "Every per-spouse distinction is in eligibility attribution, not
    arithmetic", qualified by "Not found: any 2025 rule …".
- **Candidate problems:** none.
- **Reviewer (23:01):** "NO CHALLENGE. … The claim that per-spouse
  differences lie in 'attribution, not arithmetic' sits close to its own
  per-loan obligation finding. But the planner left open whether attribution
  affects any computed result, so I'm watching it rather than challenging it
  now."
- **Reply:** `continue`.

## Snapshot 3 — 23:07 observer note

- **Turn:** 13 turns, about 6 min. Commit `82496a8`. Action 4 (probe).
- **Sources consulted (tool record):** scope fact titles; the end-to-end and
  Track 5 tests; the Track 6 `_f1098e_acts` helper; a scratch probe in `temp/`
  (first run failed on the import path and was rerun with `PYTHONPATH=.`);
  a grep for person-facing wording of the scope answers; the Track 6
  presentation sample. No out-of-workspace or ref reads.
- **Premises:**
  - *Observed:* MFJ at 50,000 gives 2,500; MFJ at 180,000 gives 1,668, the same
    figure as the reference probe (B1); MFS is blocked. Qualified: "already
    computes a correct figure **when every answer is truthfully 'yes' for the
    household**".
  - *Risks read from the rule and fact titles:*
    a. The return-level obligation "no" zeroes both spouses' interest, and a
       "yes" can gloss a loan neither spouse owes. Both directions are named,
       matching C3.
    b. The dependency wording says "the filer"; the mitigation that a joint
       filer rarely can be a dependent is labelled "general law and not
       verified in a source here".
    c. Nothing records whose education a loan financed, as for single filers
       (C4).
  - No person-facing question text exists for the scope answers; they are
    shown as pins. Planner A reached the same finding at its snapshot 6.
  - *New option:* "Refuse MFJ until attributed".
- **Snapshot 2 watch (timing for "spouse"):** not drawn on in this snapshot.
- **Candidate problems:** none. The whole-route block on one statement's "no"
  (C6) is not discussed. The planner read the codes at snapshot 1, but no
  completeness claim depends on them yet.
