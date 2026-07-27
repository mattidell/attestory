# Presentation — Live Viewing Boundary Track 1 Repair Recheck

Status: **NOT READY**
Date: 2026-07-26
Role: independent Reviewer (same Reviewer as the original review)
Charter: `docs/reviews/charter-2026-07-26-presentation-live-viewing-boundary-track1-repair-review.md`

## Capsule echo (pre-recheck)

| Item | Resolved value |
| --- | --- |
| **Source ref** | `track/presentation-live-viewing-boundary-track1`, current at `8255528`. Repair commit under recheck: `52ef7b0` (reviewed original: `498c396`; original review: `b1a630a`). |
| **Exact object** | Finding 1, Observation 1, and the invariants the repair's diff touches: `docs/adr/0047-live-viewing-environment.md`, `docs/adr/analyses/0047-live-viewing-environment.md`, `docs/adr/INDEX.md`, `docs/phases/real-return/milestones/presentation-live-viewing-boundary.md`. Measurements 1/3/4/5 from the original review are not re-derived except where this diff reaches them. |
| **Role** | Focused recheck, not a second full review. |
| **Stop conditions** | Repair cap is spent per the charter: a further `NOT READY` returns to the Foreman for owner direction, not another repair. |

## Measurements

| # | Measurement | Result |
| --- | --- | --- |
| 1 | Finding 1 closed: clipboard-history retention classified exactly once, in Class D, with Class A's boundary excluding background retention without new ambiguity about where a deliberate paste belongs. | **Pass.** `docs/adr/0047-live-viewing-environment.md` adds a bounded-act sentence to Class A ("Class A is bounded to the deliberate, one-shot act itself... It does not cover background software that silently retains the act... classifies under Class D") and enumerates clipboard-history retention once, in Class D, alongside backup/indexing as the "third silently fatal" precondition. A deliberate paste (the act itself) stays squarely Class A; only its unsolicited *retention* moves to D — no channel is now claimed by two classes. |
| 2 | Totality preserved: no new unclassified remainder; re-probe for a channel of the same shape (background software silently converting an in-session act into a durable record outside the residency). | **Pass, none found.** Independently re-probed: OS "Recent Items"/file-open history (not applicable — the vehicle opens no external files); Handoff/Continuity screen mirroring (requires the site to declare Handoff support, not applicable to a local/loopback-served page, and is arguably already covered by "third-party synchronization software covering the residency" if it ever became relevant); notification-center previews of copy/paste toasts (no such OS feature exists). None survive as a distinct unclassified channel of Finding 1's shape. |
| 3 | Split disposition is honest, not a loophole: a passing clipboard check must not read as a completeness claim, and the two always-decidable preconditions must retain unconditional refusal. | **Pass.** The ADR states plainly: "Where the preflight can observe it... it refuses... Where it cannot, the owner is responsible... That partial detectability is why clipboard history is listed separately from the two conditions the preflight must always be able to decide." The milestone plan mirrors this: "These two must always be decidable; an indeterminate result is a refusal" for indexing/backup, and for clipboard, "its absence is not a pass claim: the undetectable remainder is a named owner responsibility." No surface conflates the two always-decidable conditions with the partly-decidable one. |
| 4 | Observation 1 addressed without overcorrection: Class C must not imply a substrate is available/endorsed/scheduled; Presentation stays L2, data boundary L3; the narrowed Guarded Transport claim still supports rejecting the vehicle-first shape. | **Pass.** Class C now reads "open because nothing is selected, not because nothing exists," names Seatbelt/`sandbox-exec` as "unevaluated... neither foreclosed nor endorsed," and narrows the load-bearing claim to "a cooperative same-UID mechanism is not a trust boundary, so a flag-configured browser cannot be one" — which is exactly what the Guarded Transport records support and is sufficient on its own to reject the vehicle-first shape; the platform-impossibility claim was never load-bearing for that rejection. Consequences section (unchanged by this diff) still holds Presentation at L2 and the data boundary at L3; no substrate selection language was introduced anywhere in the diff. |
| 5 | Consistency across surfaces: ADR, analysis, milestone plan, and INDEX row agree; no surface retains the superseded four-class wording or the platform-impossibility phrasing. | **Fail — see Finding 1.** One stale cross-reference survives inside the ADR itself. |

## Data safety

`python3 tools/envelope_scan.py --range main..HEAD` — exit 0, no output. `git diff --check main..HEAD` — exit 0, no output. No residency locator, path fragment, or owner-local identifier found in any changed file.

## Finding 1 (recheck) — "Threat posture and residuals" still says two silently fatal conditions, and describes both as flatly "refused"

**File/line:** `docs/adr/0047-live-viewing-environment.md:253` (section "Threat posture and residuals"):

> "the controllable channels are controlled by construction, the two silently
> fatal machine conditions are refused rather than assumed away, the
> irreducible human channels are named as residuals rather than hidden"

The repair correctly updated Class D to name **three** silently-fatal conditions ("the first three are **silently fatal**") and, in "Decision — precondition disposition," gave clipboard-history retention an explicitly **split** treatment ("a refusal where detectable and a named owner responsibility where not"), distinct from indexing and backup's unconditional refusal. This summary sentence, two sections later in the same document, was not updated to match: it still says "two," and it still characterizes all of them as simply "refused rather than assumed away" — which is true of indexing/backup but not of clipboard-history retention, whose undetectable remainder is explicitly *not* refused but instead named an owner-knowledge residual under attestation condition 4.

This is not a re-opening of Finding 1's substance — the classification, the Class D enumeration, and the attestation conditions are all internally correct and consistent with each other, as measurements 1, 3, and 4 above confirm. The residual is narrower: the document's own closing summary of what it claims contradicts what the document says two sections earlier, in the one place a fresh reader would go to check the ADR's exact claimed posture without re-reading the whole decision. Measurement 5 (consistency across surfaces) was written to catch exactly this shape of miss.

**Recommended repair (not prescribed):** change "the two silently fatal machine conditions are refused rather than assumed away" to something that (a) says three, and (b) does not claim clipboard-history retention is simply "refused" — e.g., "the three silently fatal machine conditions are either refused or, where undetectable, named as an owner-knowledge residual rather than assumed away."

## Verdict

**NOT READY.** Four of five measurements pass; the repair correctly closes Finding 1's substance and addresses Observation 1 without overcorrection. Measurement 5 (cross-surface consistency) finds one stale internal cross-reference at `docs/adr/0047-live-viewing-environment.md:253` that undercounts the silently-fatal conditions and overstates clipboard-history's disposition as unconditional refusal. Per the charter, the plan's repair cap is now spent: this returns to the Foreman for owner direction rather than a further repair. The residual is a single-line, non-substantive text correction with no open design question behind it.
