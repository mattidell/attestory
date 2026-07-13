# Triage: Conditional Selectors Round 2

Date: 2026-07-13
Foreman: Codex Foreman

This document records the triage of findings from Round 2 reviews of the `conditional-selectors` prototype, in accordance with Gate 5 of the prototype process.

## Findings Classification

### 1. Decision-Blocking Findings (Must be resolved in final evaluation and ADR drafts)

* **CS2-A1 (MFS/QSS Spousal Case Grouping Logic Leak):** **Decision-Blocking (Payload level).**
  - *Description:* Grouping MFS and QSS under Case 2 (spousal deductions) exposes them to spousal additional choose blocks.
  - *Resolution:* In the final evaluation analysis and ADR payload examples, MFS and QSS must be moved to Case 1 (non-spousal), leaving Case 2 strictly for MFJ. Since Case 1 looks up the base and additional rates dynamically using the `filing_status` key, this automatically applies the correct base and rate.
* **CS2-A3 (Safety Bypass via `"default": null`):** **Decision-Blocking (Payload level).**
  - *Description:* Providing `"default": null` overrides the runner's built-in `SELECTOR_NO_MATCH_ERROR` safety check.
  - *Resolution:* Remove `"default": null` from standard deduction selector examples to ensure unsupported statuses fail fast.

### 2. Production Conditions (To be addressed during production implementation)

* **CS2-A2 (Missing Status Brackets in Parameter File):** **Production Condition.**
  - *Description:* The tax brackets parameter file only defines brackets for single and MFJ status.
  - *Resolution:* Complete bracket structures for MFS, HoH, and QSS will be defined during production implementation.
* **CS2-A4 (Sorting comparisons with `null`):** **Production Condition.**
  - *Description:* Runner sorting verification needs to explicitly handle `null` value comparison when checking progressive brackets.
  - *Resolution:* Handled in runner implementation.

---

## Foreman Recommendation

The core architecture of Shape B (including the `selector-artifact.v1` schema, V0 absence pinning for dynamic optional displacement, and mutually exclusive guard checks) has successfully converged and is ratified by both reviewers.

No further prototype iteration is needed. The minor payload-level bugs (case grouping, removing default null) will be corrected directly in the final **Evaluation Analysis** and drafted **ADRs**. We proceed to finalize the topic.
