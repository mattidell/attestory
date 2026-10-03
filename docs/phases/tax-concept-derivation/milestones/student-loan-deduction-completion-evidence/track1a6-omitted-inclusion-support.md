# Track 1a-6 — omitted inclusions reach their statement's support decision

Everything here is **proposed**: ADR 0077 text plus a disposable probe. Nothing under `packages/`, `tests/` or schemas changed. The probe is `temp/track1a6/probe.py` (ignored). It was run as `PYTHONPATH=. python3 temp/track1a6/probe.py` and exited 0.

Labels: **recorder execution** means the start state was built with the real recorder and a real `ActLog`, recovered fresh, and checked with the real `current_claim_applicability`. **Runtime stand-in** means the Track 0d chain (with its `shared_key_count` stand-in) and the Track 1a-4 worksheet scheduler, with this track's connection patched in at runtime. Line 21 presentation is presentation only. It showed the generic sentence in every case.

## The connection

Replay omits an inclusion it cannot establish. In its place, the marshaller supplies a source of a system fact type, `tax.us.2025.sli.statement-inclusion-applicability-unestablished`. That source keeps the inclusion's identity keys and finding id and carries the value `sli.statement-inclusion.applicability-unestablished`. The per-statement conclusion rule requires that type, with default `established`. It publishes `not-supported` whenever a marker is on the statement, and it reads every marker, so each omitted inclusion's finding is pinned. A per-statement echo publishes the marker value beside the conclusion. Part 4's new path names the marker type. The marker is not the person's `tax.us.2025.sli.statement-inclusion-unresolved` and does not carry that fact's value or wording.

## Cases

Both runners agreed in every row.

| Case | Start state (recorder execution) | Treatment (runtime stand-in) | Statement | Line 21 |
| --- | --- | --- | --- | --- |
| Owner's mixed case | A `unresolved-applicability`, B `current`, box 1 1800 | joined as today | `not-supported` (two links) | blocked |
| Owner's mixed case | same | Track 1a-5 omission + A as unresolved | `plain-case-supported` | **published 1800** (the reproduced gap) |
| Owner's mixed case | same | Track 1a-6 marker | `not-supported`, mark `applicability-unestablished`, pins A and the 1800 box 1 | blocked `SLI_UNIVERSAL_COMPONENT_VIOLATION` |
| Sole omitted link | A `unresolved-applicability`, box 1 1800 | joined as today | `plain-case-supported` | published 1800 (the Part 5 gap) |
| Sole omitted link | same | Track 1a-5 | `not-supported`, pins box 1 only | blocked |
| Sole omitted link | same | Track 1a-6 | `not-supported`, mark `applicability-unestablished`, pins A | blocked |
| Two omitted on one statement | A and B `unresolved-applicability` | Track 1a-6 | `not-supported`, pins A and B | blocked |
| Mixed beside an unaffected statement | A unresolved, B current, sibling `current` | Track 1a-5 | both `plain-case-supported` | **published 2500** |
| Mixed beside an unaffected statement | same | Track 1a-6 | sibling `plain-case-supported` / `established`; first `not-supported` | blocked |
| Reviewed route, sole | reviewed amount-only to 1850; A `current` | Track 1a-6 | `plain-case-supported` / `established` | published 1850 |
| Reviewed route, mixed | reviewed amount-only to 1850; A and B `current` | Track 1a-6 | `not-supported` (two loans, owner decision 3) / `established` | blocked |
| Both present | sole omitted link plus five old answers | Track 1a-5 and Track 1a-6 | `not-supported` | blocked `DEPENDENCY_INVALID`, `old-and-new-sli-inputs-both-present` |
| Plain case | A `current`, box 1 1250 | today and Track 1a-6 | `plain-case-supported` | published 1250 |
| Track 1a-4 synthetic cases | not recorder-built | Track 1a-6 | — | old-only 2500, new-only 2500, both blocked on the presence token, closed-empty 0, nonempty-neither blocked on the box fact id |

The reviewed route re-binds A. The deduction returns where A is the statement's only loan. Where B is also current, the statement holds two loans and stays `not-supported` for that reason, with the applicability mark back to `established`. A successful statement gains one declared-default pin for the marker; its value is unchanged.

## ADR

ADR 0077 Part 5's "Replay" section now has steps 3 to 5 (marker, statement decision, presence) and the table above. Part 4's runtime and shape name the marker instead of "counted as an unresolved inclusion". The Consequences section lists the build obligations. Three alternatives are added, and two open questions: a direct pin for the box 1 finding the inclusion was confirmed against, and the marker names. The INDEX row matches. `tools/governance_lint.py`: conformant.
