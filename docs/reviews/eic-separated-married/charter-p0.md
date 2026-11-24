# Charter: P0 of the separated-spouse question is asked only of a married filer

Role: Builder. Source HEAD on milestone/eic-separated-married-2025.
Plan: docs/phases/engine-breadth/milestones/eic-separated-married.md (read
it whole). Precedents: eic-no-ssn-child (plan Decisions 3 and 5, review
ENS-R1, evidence probe.py and hand.py), hoh-eic and hoh-qualifying-person
evidence, and the full-surface replay in tools/recorded_replay.py (`full`).
Do not read governance.

## Scope

1. **Sources.** Fetch the 2025 Form 1040 instructions (line 27a) and
   Publication 596 into ignored temp/. Quote, with page and line, Step 3
   questions 3 to 5, the special rule for separated spouses, and any text
   on how "married" is judged for a head of household (for example a
   spouse who lived apart for the last six months is "considered
   unmarried" for head of household but may still be married for the
   credit). Read each section whole.
2. **What the record knows.** On published core v102, which recorded
   answer or fact says whether a head of household filer was married at
   the end of 2025? Cite the fact type, the input question and the rule
   that reads it. Say whether it is always asked of a head of household,
   and whether its meaning matches Step 3 question 3.
3. **Trace.** Synthetic demo.* returns through the real live coordinator:
   head of household married and not married; qualifying child with and
   without a valid SSN; separated (apart or in writing) or not; married
   filing separately. Record what each computes and asks today, what the
   sources say, and the hand credit from the 2025 table.
4. **Content route.** As scratch successors on v102 loaded from published
   content: ask the separated-spouse question only of a married filer.
   Say whether any route changes which answer an unrelated path needs. If
   the record cannot tell, name the smallest new question from the
   instructions and stop.
5. **Replay.** Full-surface replay of the 775 recorded lists, v102 against
   the scratch successor, with expected changes declared. Report
   pass/unexpected and unused expectations.
6. **Size.** Report the byte size of each scratch rule file; the live
   tests cap `rule.eic-*.json` at 5,000 bytes unless listed with a reason
   (`tests/test_earned_income_credit_track1.py`,
   `tests/test_eic_qualifying_children_track1.py`).

## Deliverables

In docs/phases/engine-breadth/milestones/eic-separated-married-evidence/:
p0.md (sources quoted, what the record knows, trace table, route,
replay, decisions for the foreman), the scripts a later test will need,
and small JSON. Fill a "P0 result" section in the plan. No production,
test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed. Fetched sources
  stay in ignored temp/.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn. Do not edit packages/ or
  tests/.
