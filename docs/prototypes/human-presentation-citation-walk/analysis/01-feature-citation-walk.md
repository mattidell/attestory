# 01 — Citation Walk Feature: Build & Evaluation

## Feature
Read-only projection surface. Renders computed Form-1040 lines + Schedule B
attachment as a walk: `line → subtotal → per-source disposition → citation pin →
source fact`. Substrate for the process experiment; not a product deliverable.
Input = a frozen synthetic fixture (the "computed output"); surface adds no
authority (may render only what the fixture published).

## Build approach (observed, invariant across 10 builder runs)
| Property | Observation |
|---|---|
| Medium | single self-contained HTML file; no framework; no build step; no deps — chosen by every builder unprompted |
| Data | one `Object.freeze`d `FIXTURE`/`FACTS` object = sole numeric source |
| Render | one render-path-per-citation function; called from every citation site |
| DOM | `createElement`/`textContent`; no `innerHTML` (repo security hook rejected `innerHTML` first-draft in C2–C5, forcing this — strengthened zero-authority) |
| Blocked value | absence-of-key (`value` field omitted), not `null`/`0` — structural, not guarded |

## Evaluation targets by cycle
| Cycle | Target |
|---|---|
| C1 | zero-authority + honest blocking (baseline) |
| C2 | evaluation *method* (isolation, break-test standardization) |
| C3 | fail-loud contract (visible on-page signal + blast containment) |
| C4 | citation identity under reuse + sub-section blast granularity |
| C5 | a11y/legibility + fraction of "needs-an-eye" that is mechanizable |

## Heuristics (individual, with emergence cycle)
- Render only published values; never a fabricated **or derived-from-bad-data** number [C1, C4].
- Blocked line: show what's-missing + remedy, never a value [C1].
- Absence-of-key > null-check for "no value" [C1].
- Single frozen source + single render path [C1–C5].
- `createElement`/`textContent` > `innerHTML` (hook-enforced) [C2–C5].
- Fail-loud = **visible on-page** signal; console-only ≠ loud [C2–C3].
- Redact rejected values from error text (error message is itself a leak channel) [C3–C4].
- Sub-section blast containment: a broken part must not hide correct siblings, nor show a value whose evidence is broken [C4].
- Citation identity under reuse: enforce by freeze-prevent or signature-detect [C4].
- Evaluate by execution + fault injection, not doc-reading [C2–C5].
- A "mechanical" check's trust depends on technique (real CDP key events, not `.focus()`; luminance math) [C5].

## Heuristic classes (taxonomy)
Two axes: **artifact properties** vs **evaluation apparatus**.

Artifact properties:
1. **Honesty invariants** — zero-authority, honest blocking, no fabricated/derived value.
2. **Failure-behavior contract** — fail-loud, visible, blast-contained, redacted.
3. **Structural-enforcement patterns** — single source, single render path, immutability, presence-not-truthiness, build-not-interpolate.
4. **Accessibility/legibility baseline** — contrast, ARIA/semantics, keyboard+focus, affordance cue, reuse legibility.

Evaluation apparatus:
5. **Evaluation methodology** — execution over doc-reading, live fault injection, real-input driving, luminance recompute, standardized break-tests.
6. **Process/isolation hygiene** — per-agent browser isolation, exact-paths, sequential-when-browser-bound, break-tests-in-brief.

## Analysis unique to this milestone (non-repeatable vs repeatable)
- **Settled + mechanized (do not re-derive):** the six citation-walk criteria (classes 1–4) are now enumerated and each is script-checkable → future runs *verify via harness*, not re-reason. Reference implementations exist (`../reference/prototypes/cycle5-{a,b}`), each satisfying all accumulated criteria.
- **Generalizes beyond this surface:** classes 5–6 (methodology, hygiene) apply to any agent-evaluated UI. The isolation recipe and break-test discipline are the reusable output.
- **Avoid repeating:** (a) don't run rival builders on already-settled properties; (b) don't re-hand-roll the check rig (harness seed committed); (c) don't re-discover isolation (recipe committed); (d) don't trust `DESIGN.md` self-claims (execute).
