# Presentation — Live Viewing Boundary Track 1 Second Focused Recheck

Status: **READY**
Date: 2026-07-26
Role: independent Reviewer (same Reviewer as the original review and first recheck)
Charter: `docs/reviews/charter-2026-07-26-presentation-live-viewing-boundary-track1-recheck2.md`

## Capsule echo (pre-recheck)

| Item | Resolved value |
| --- | --- |
| **Source ref** | `track/presentation-live-viewing-boundary-track1`, current at `b421938`. Repair commit under recheck: `08eecb6` (prior recheck: `a476c40`; first repair: `52ef7b0`). |
| **Exact object** | One paragraph in the "Threat posture and residuals" section of `docs/adr/0047-live-viewing-environment.md` (`git diff a476c40..08eecb6` touches only this file, one hunk). |
| **Role** | Second focused recheck, owner-authorized exception to the plan's stated one-repair cap, since the prior recheck characterized the residual as a single-line, non-substantive text correction with no open design question. |
| **Scope** | Measurement 5 only, plus anything the one-paragraph diff directly touches. Measurements 1–4 from the original review are not re-derived; the first recheck already passed them. |

## Measurements

| # | Measurement | Result |
| --- | --- | --- |
| 1 | Residual closed: the threat-posture summary counts the silently fatal conditions correctly and states clipboard-history's disposition consistently with the Class D and precondition-disposition sections; no surface retains the two-condition count. | **Pass.** The paragraph now reads: "of the three silently fatal machine conditions, the two the preflight can always decide — backup inclusion and content indexing — are refused unconditionally, and clipboard-history retention is refused where detectable and named as an owner responsibility where it is not." This states three, and correctly splits disposition rather than claiming uniform refusal. `grep -n "two silently fatal\|silently fatal" docs/adr/0047-live-viewing-environment.md` shows the only other occurrence (line 153, Class D) already said "the first three are silently fatal" from the first repair — the two now agree. |
| 2 | No new inconsistency or drift: the reworded paragraph introduces no claim absent from the decision sections it summarizes; the Class C rewording does not imply a substrate is available, endorsed, or scheduled; Presentation stays L2, data boundary stays L3. | **Pass.** "the two the preflight can always decide... refused unconditionally" matches "Decision — precondition disposition" verbatim in substance ("the two conditions the preflight must always be able to decide"). "clipboard-history retention is refused where detectable and named as an owner responsibility where it is not" matches that same section's own clipboard-history paragraph verbatim in substance ("a refusal where detectable and a named owner responsibility where not"). "Class C remains open, no substrate having been selected or evaluated" reuses the exact framing the first repair already established in the Class C section itself ("This class is open because nothing is selected, not because nothing exists"; "no confinement substrate having been selected or evaluated" already appears verbatim in the Explicit residuals list). No new claim is introduced anywhere in the diff. The "Consequences" section (unchanged, not touched by this diff) still holds Presentation at L2 and the data boundary at L3. |

## Data safety

`python3 tools/envelope_scan.py --range main..HEAD` — exit 0, no output. `git diff --check main..HEAD` — exit 0, no output. No residency locator, path fragment, or owner-local identifier in the changed paragraph.

## Non-blocking observation

`docs/phases/real-return/milestones/presentation-live-viewing-boundary.md:141-143` still illustrates the "fourth class... silently fatal" point with content indexing as its sole worked example and does not itself claim a count of two or three, so it is not inconsistent with this repair and is out of this charter's scope (the diff under recheck touches only the ADR). Noting it only so a later reader doesn't need to re-derive that it was considered and found non-blocking.

## Verdict

**READY.** Both required measurements pass on independent verification: the residual identified in the first recheck (`a476c40`, Finding 1) is closed, and the one-paragraph repair introduces no claim beyond what the ADR's own Class C and precondition-disposition sections already establish. Track 1's review-and-repair stage is complete.
