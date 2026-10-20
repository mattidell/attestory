# Candidate C: Adopted Subtotal and Selection Pattern for Combined Entry (P7)

Audience: Builder, Reviewer, Foreman.\
Evidence: Design analysis and executed live coordinator probe (`test_candidate_c_probe.py`) grounded in adopted `rule.sli-worksheet.v5.json`, `rule.sli-worksheet-line1-subtotal.json`, ADR-0016, ADR-0077 Parts 3–4, and the P5 diagnostic.

---

## 1. Context and Selected Scope

This report evaluates Candidate C, which resolves the multi-statement Schedule 1 combined entry using the exact adopted pattern from the Student Loan Interest (SLI) deduction (`rule.sli-worksheet-line1-subtotal.json` and `rule.sli-worksheet.v5.json`).

- **Policy 1 (Owner-Selected):** Every current statement in the closed family must be a qualifying `supported-loss` before the combined Schedule 1 entry publishes. A return with mixed outcomes, unmodeled circumstances, or unanswered/unknown facts blocks. A closed-empty family produces zero; an unclosed family blocks.
- **Diagnostic Reasons (Stipulated):** The per-statement reason producer uses the stipulated diagnostic categories established in P5 (`yes` $\to$ `supported-loss`, `cannot-tell` $\to$ `cost-basis-unknown`, withdrawn $\to$ `DEPENDENCY_ABSENT`). These isolate producer states and test engine coverage and scheduling behavior; they do not constitute validated tax determinations.
- **Zero-New-Schema Pattern:** Candidate C requires **zero new schemas** and **zero engine modifications**. It uses the existing `rule-artifact.v14` (or `v13`) schema, which already implements `exclusive_presence` selection with `reads_subject_results`. It retains the owner's expressly chosen two-path pattern—one live path and one inert path naming an unwritten fact type—avoiding the schema-successor costs of the one-path proposal in Candidate B.
- **No Imported Rounding:** Current Form 1099-K sales top-entry uses raw `add(collect)` without rounding. Candidate C does not import SLI worksheet whole-dollar rounding: the raw subtotal performs plain `add(collect)`, preserving exact fractional dollar-and-cent amounts (e.g., cents in Box 1a) so no new rounding alters a single-statement amount or multi-statement sum.
- **Scope Boundary:** This probe verifies engine coordination, scheduling, aggregation, and pin provenance on disposable content. It does not test the saved reader, form generation, or complete tax determinations.

---

## 2. Concrete Declaration Shapes

The adopted SLI architecture separates two distinct obligations:
1. **Raw aggregation subtotal (ADR-0016 collect authority):** An ordinary rule performs the collect over the closed family, publishing a single scalar subtotal symbol authorized by the family declaration and admitted by the closure mapping.
2. **Top-entry presence selection (ADR-0077 Parts 3–4):** A selection rule requires that scalar subtotal as a conventional input, declares same-run per-subject reads over statement reasons, verifies whole-family coverage, and chooses between the live combined entry, the owner-chosen inert second path, and the closed-empty zero default.

### A. Raw Box 1a Subtotal Rule

Mirrors `rule.sli-worksheet-line1-subtotal.json` and `rule.f1099g-1-subtotal.json`, but without SLI rounding. It is an ordinary computation rule with unconditional `when: true` (under ADR-0014 Decision 8 and ADR-0016, a nonempty collect requires no separate closure justification of its own; closure is enforced downstream by the family mapping and top-entry gates). `requires` and `pins` are empty because the rule reads no external parameters or scalar inputs.

```json
{
  "schema": "rule-artifact.v14",
  "id": "tax.us.2025.rule.f1099k-box1a-subtotal",
  "version": "v1",
  "scope": {
    "tax_year": 2025,
    "jurisdiction": "US-federal",
    "family": "individual-income-tax"
  },
  "role": "computation",
  "requires": [],
  "pins": [],
  "when": true,
  "value": {
    "op": "add",
    "args": [
      {
        "op": "collect",
        "source_set": "tax.us.2025.f1099k",
        "name": "tax.us.2025.f1099k.box1a-gross-amount"
      }
    ]
  },
  "publishes": "tax.us.2025.f1099k.box1a-subtotal",
  "blocked": {
    "code": "DEPENDENCY_INVALID",
    "missing": []
  },
  "citations": [],
  "notes": "Publishes the raw, unrounded sum of the Form 1099-K Box 1a family under ADR-0016 collect authority. Preserves exact fractional amounts without rounding."
}
```

*Fractional-value compatibility observation:* Form 1099-K Box 1a amounts frequently carry cents (e.g. `$880.50` or `$460.25`). Plain `add(collect)` avoids any truncation or whole-dollar rounding; the tested fractional sum is preserved ($880.50 + $460.25 = $1340.75), but no saved-reader or single-statement equivalence was measured.

### B. Successor Top-Entry Selection Rule

Mirrors `rule.sli-worksheet.v5.json` and `rule.f1099k-unresolved.json`. Uses existing schema `rule-artifact.v14`. It requires the scalar `tax.us.2025.f1099k.box1a-subtotal`, declares `reads_subject_results` for `tax.us.2025.f1099k.statement-loss-reason`, retains the owner-selected inert path, and handles closed-empty zero on default. (In the disposable execution probe, this rule is sealed as `v2` in the temporary test surface; a future production successor would be authored as `v3`).

```json
{
  "schema": "rule-artifact.v14",
  "id": "tax.us.2025.rule.schedule1-top-entry",
  "version": "v3",
  "scope": {
    "tax_year": 2025,
    "jurisdiction": "US-federal",
    "family": "individual-income-tax"
  },
  "role": "computation",
  "requires": [],
  "pins": [],
  "when": true,
  "selection": {
    "mode": "exclusive_presence",
    "conflict": "refuse",
    "paths": [
      {
        "id": "statements",
        "activity": {
          "kind": "source_nonempty",
          "source_family": {
            "id": "tax.us.2025.f1099k",
            "version": "v2"
          },
          "member_fact_types": [
            {
              "id": "tax.us.2025.f1099k.box1a-gross-amount",
              "version": "v1"
            }
          ]
        },
        "reads_subject_results": [
          {
            "symbol": "tax.us.2025.f1099k.statement-loss-reason",
            "subject": {
              "id": "tax.us.2025.f1099k.box1a-gross-amount",
              "version": "v1"
            }
          }
        ],
        "requires": [
          "tax.us.2025.f1099k.box1a-subtotal"
        ],
        "pins": [
          {
            "id": "tax.us.2025.f1099k.box1a-subtotal",
            "role": "input",
            "version": "v1",
            "origin": "assertion"
          }
        ],
        "when": {
          "op": "require_closed",
          "source_set": "tax.us.2025.f1099k"
        },
        "value": {
          "op": "choose",
          "when": {
            "op": "collect_categorical_all_equal",
            "name": "tax.us.2025.f1099k.statement-loss-reason",
            "value": {
              "op": "category_literal",
              "fact_type": {
                "id": "tax.us.2025.f1099k.statement-loss-reason",
                "version": "v2"
              },
              "value": "supported-loss"
            }
          },
          "then": {
            "op": "ref",
            "name": "tax.us.2025.f1099k.box1a-subtotal"
          },
          "else": {
            "op": "block",
            "code": "DEPENDENCY_ABSENT"
          }
        }
      },
      {
        "id": "inert",
        "activity": {
          "kind": "source_nonempty",
          "member_fact_types": [
            {
              "id": "tax.us.2025.f1099k.inert-path-unwritten",
              "version": "v1"
            }
          ]
        },
        "reads_subject_results": [],
        "requires": [],
        "pins": [],
        "when": true,
        "value": {
          "op": "block",
          "code": "DEPENDENCY_INVALID"
        }
      }
    ],
    "default": {
      "id": "neither",
      "reads_subject_results": [],
      "requires": [],
      "pins": [],
      "when": {
        "op": "require_closed",
        "source_set": "tax.us.2025.f1099k"
      },
      "value": {
        "op": "choose",
        "when": {
          "op": "compare",
          "cmp": "eq",
          "left": {
            "op": "count",
            "name": "tax.us.2025.f1099k.box1a-gross-amount",
            "source_set": "tax.us.2025.f1099k"
          },
          "right": 0
        },
        "then": 0,
        "else": {
          "op": "block",
          "code": "DEPENDENCY_INVALID"
        }
      }
    },
    "refusal": {
      "code": "DEPENDENCY_INVALID",
      "missing": [
        "f1099k-inert-path-conflict"
      ],
      "pins": []
    }
  },
  "publishes": "tax.us.2025.schedule1.top-entry",
  "blocked": {
    "code": "DEPENDENCY_INVALID",
    "missing": []
  },
  "citations": [],
  "notes": "Candidate C: Combines Form 1099-K qualifying personal item sales into Schedule 1 top entry using adopted selection and subtotal pattern."
}
```

### C. Successor Source Family Declaration

Revises `family.f1099k.json` (version `v2`). Under ADR-0016, the family's `authorizes_subtotal` points directly to the raw collect subtotal symbol, not to the downstream top-entry rule. The closure claim explicitly authorizes the multi-statement sum, mirroring `family.f1098e-1.json`.

```json
{
  "schema": "source-family.v1",
  "id": "tax.us.2025.f1099k",
  "version": "v2",
  "scope": {
    "tax_year": 2025,
    "jurisdiction": "US-federal",
    "family": "individual-income-tax"
  },
  "title": "Form 1099-K box 1a gross payment amount statement items, tax year 2025",
  "authorizes_subtotal": "tax.us.2025.f1099k.box1a-subtotal",
  "member_predicate": {
    "fact_type": "tax.us.2025.f1099k.box1a-gross-amount"
  },
  "closure_claim": "Every personal item sale amount reported in box 1a of a Form 1099-K furnished to the taxpayer for tax year 2025 is recorded as a statement item as of the keyed horizon. Closed with members authorizes the sum of current members; closed-empty authorizes subtotal 0."
}
```

### D. Successor Closure Mapping Declaration

Revises `closure-mapping.f1099k.json` (version `v2`). Admits the raw subtotal symbol rather than the top entry.

```json
{
  "schema": "source-closure-mapping.v2",
  "id": "tax.us.2025.closure-mapping.f1099k",
  "version": "v2",
  "family": {
    "id": "tax.us.2025.f1099k",
    "version": "v2"
  },
  "member_fact_type": {
    "id": "tax.us.2025.f1099k.box1a-gross-amount",
    "version": "v1"
  },
  "closure_fact_type": {
    "id": "tax.us.2025.f1099k.source-closure",
    "version": "v1"
  },
  "closure_horizon_key": "family-horizon",
  "admits_symbol": "tax.us.2025.f1099k.box1a-subtotal",
  "admission": {
    "condition": "current-literal-true"
  }
}
```

---

## 3. Inventory of Changed Citizens and Adopted Consumers

Calling a content-only approach "zero work" is false: it avoids schema and engine changes, but requires strict inspection of content provenance, package validation rules, and all consumers that pin the family:

1. **`tax.us.2025.rule.f1099k-box1a-subtotal` (New citizen `v1`, `rule-artifact.v14`):**
   Collects `box1a-gross-amount` over closed family; publishes scalar subtotal.
2. **`tax.us.2025.rule.schedule1-top-entry` (Disposable test instrumentation `v2`; future production successor `v3`, `rule-artifact.v14`):**
   Two-path selection; requires scalar subtotal; declares `reads_subject_results`.
3. **`tax.us.2025.f1099k` (Successor family `v2`, `source-family.v1`):**
   Updates `authorizes_subtotal` from top-entry to `box1a-subtotal`; updates `closure_claim` to authorize multi-statement sum.
4. **`tax.us.2025.closure-mapping.f1099k` (Successor mapping `v2`, `source-closure-mapping.v2`):**
   Updates `admits_symbol` to `box1a-subtotal`; points at family `v2`.
5. **`tax.us.2025.rule.attachment.schedule-1` (Adopted consumer, needs successor `v4`):**
   Inspects `itemizations` for `sch1-top-entry-f1099k`: authority and row_sets currently pin `tax.us.2025.f1099k` at version `v1`, and set `subtotal_symbol` to `tax.us.2025.schedule1.top-entry`. Under ADR-0016, `package_validation` requires `row_set.subtotal_symbol == family.authorizes_subtotal`. Production adoption requires updating this consumer to pin family `v2` and set `subtotal_symbol` and `tie_out.line_symbol` to `tax.us.2025.f1099k.box1a-subtotal` (mirroring the Track 4b SLI attachment repair).
6. **`tax.us.2025.rule.f1099k-unresolved` (Adopted consumer, needs successor `v3`):**
   Path `statement` activity currently pins `source_family: {"id": "tax.us.2025.f1099k", "version": "v1"}`. Production adoption requires updating the pin to `v2` and reconciling its `count > 1` guard.
7. **`tax.us.2025.f1099k.inert-path-unwritten` (Fact type `v1`, `fact-type.v2`):**
   Already declared in `f1099k.bundle.v3.json`. Requires no new declaration or schema.
8. **Package / Registry Surface (`artifact-package.v36`, `package-registry.v1`):**
   Package v48 uses schema `artifact-package.v36`. Citizens are added/updated in registry v46; checksums are re-sealed; release manifest is updated.

---

## 4. Paper Predictions vs. Executed Measurements

The table below contrasts the paper design predictions with the actual executed measurements from `test_candidate_c_probe.py` across all 9 test runs.

| Case | Scenario & Inputs | Candidate C Predicted Behavior | Measured Execution Result | Measured Disposition & Public Code | Provenance & P5 Defect Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Both Supported (Producer-First)** | Stmt A: $880.00 (`supported-loss`)<br>Stmt B: $460.00 (`supported-loss`)<br>Family closed. | Active path selected. Waits on reason publishers. Subtotal computes $1340.00. `collect_categorical_all_equal` passes. | **Publishes `1340.0`** | `published` | Exact pins verified: subtotal pins both Box 1a assertions (`v1`, `assertion`). Top entry pins subtotal (`v2`, `assertion`) and both reasons (`v2`, `derived`). **No forced flattening** of Box 1a onto top entry. |
| **2. Both Supported (Consumer-First)** | Same inputs, but material order forces top entry attempt before reason producer. | Forward runner checks `_selection_eligible`. Rule is ineligible until reason producer resolves. | **Publishes `1340.0`** | `published` | **Cures P5 Cycle 0 defect.** Execution observer confirmed top entry was NOT attempted until reason producer resolved (`top_entry_attempted_after_producer=True`). |
| **3. Both Supported (Reference Runner)** | Same inputs, executed via `run_reference`. | Demand-driven scheduler resolves read symbols via `demand_names`. | **Publishes `1340.0`** | `published` | Reference runner matched forward runner published numeric value (`1340.0`). (Numeric value equality verified; demand-driven traversal does not guarantee identical pin ordering or full byte/pin equality). |
| **4. B Withdrawn / Blocked** | Stmt A: $880.00 (`supported-loss`)<br>Stmt B: $460.00 (withdrawn answer $\to$ reason blocks `DEPENDENCY_ABSENT`).<br>Family closed. | `_subject_results` identifies B as blocked. Evaluator raises `EvalBlocked(BLOCK_INVALID, [B_fact_id])`. Path blocks. | **No top publication; B reason absent; A reason published `supported-loss`.** | `blocked`, `DEPENDENCY_INVALID` (top entry) / `blocked`, `DEPENDENCY_ABSENT` (B producer). | **Completely cures P5 defect.** B's $460.00 was **not** summed into the return. The missing list explicitly named B's Box 1a fact ID; B producer durably blocked `DEPENDENCY_ABSENT`. |
| **5. B Published Unknown** | Stmt A: $880.00 (`supported-loss`)<br>Stmt B: $460.00 (`cost-basis-unknown`).<br>Family closed. | Both reasons published. `collect_categorical_all_equal` returns `false`. Evaluator takes `else` branch. | **No top publication; A published `supported-loss`, B published `cost-basis-unknown`.** | `blocked`, `DEPENDENCY_ABSENT` (top entry) | Both keyed reasons published; top entry blocked without summing. Unknown preserved as a refusal result, not zero. |
| **6. Closed Empty** | Zero statements recorded.<br>Family closure asserted at horizon. | Neither path active. Default `neither` selected. Gated by `require_closed`. `count == 0` evaluates to `true`. | **Publishes `0`** | `published` | Published finding pins actual recorded closure finding id and package-role family/mapping pins at v2. Clean zero for closed-empty. Durable disposition is `published`. |
| **7a. Missing Closure (Statements Present)** | Stmt A and Stmt B recorded, but family closure unasserted. | Active path selected. Evaluator evaluates `when: require_closed`. Fails because family is not in `env.closed_sets`. | **No publication.** | `blocked`, `SOURCE_SET_UNCLOSED` (public code from `BLOCK_CLOSURE`) naming `tax.us.2025.f1099k`. | Confirms missing closure raises an authoritative block rather than marking rule inapplicable or computing an entry. |
| **7b. Missing Closure (Empty Family)** | Zero statements recorded, and `source-closure` is NOT asserted. | Neither path active. Default `neither` selected. Evaluator evaluates `when: require_closed` on default. Fails. | **No publication.** | `blocked`, `SOURCE_SET_UNCLOSED` naming `tax.us.2025.f1099k`. | Crucial boundary: an unclosed empty family **never** produces zero. |
| **8. Fractional-Value Compatibility** | Stmt A: $880.50 (`supported-loss`)<br>Stmt B: $460.25 (`supported-loss`)<br>Family closed. | Unrounded `add(collect)` evaluates $880.50 + $460.25. | **Publishes `1340.75`** | `published` | Exact cents preserved. Subtotal published `1340.75`; top entry published `1340.75`. Zero rounding distortion. |

---

## 5. Provenance Pin Chain Distinctions

The probe measured and verified the exact distinction between declared metadata and runtime finding pins:

1. **Declared Metadata (`pins` field on rule JSON):**
   - Subtotal rule declares `requires: []` and `pins: []`.
   - Top-entry rule declares `requires: ["tax.us.2025.f1099k.box1a-subtotal"]` and one declared pin for `tax.us.2025.f1099k.box1a-subtotal` (`role: input, version: v1, origin: assertion`).
   - The declared read symbols (`statement-loss-reason`) are explicitly excluded from declared rule/path `requires` and declared `pins` (ADR-0077 Part 3).
2. **Actual Runtime Finding Pins (`pins` array on published Finding):**
   - **Subtotal finding:** Pins each current Box 1a member finding as `role: input, version: v1, origin: assertion`.
   - **Top-entry finding:** Pins the scalar subtotal finding as `role: input, version: v2, origin: assertion`.
   - **No forced flattening:** The individual Box 1a member assertion pins are pinned to the subtotal finding, not duplicated onto the top-entry finding. The top entry pins the closure-authorized subtotal finding.
   - **Reason pins via declared read:** The top-entry finding pins each read per-statement reason finding as `role: input, version: v2, origin: derived` (ADR-0077 Part 3).
3. **Supplied vs. Defaulted vs. Derived Distinctions:**
   - *Supplied inputs:* Taxpayer circumstance answers (e.g., `cost-basis-known: "yes"`), pinned by the reason rule as `role: input, origin: assertion`.
   - *Defaulted inputs:* Withdrawn or unanswered questions falling back to `not-asked` parameter defaults, pinned as `origin: declared_default`.
   - *Derived findings:* Per-statement reasons (`statement-loss-reason`), the aggregate Box 1a subtotal (`box1a-subtotal`), and the top entry (`schedule1.top-entry`).
4. **Tax vs. Diagnostic Distinctions:**
   - The diagnostic reason producer is diagnostic instrumentation isolating producer resolution states (`supported-loss`, `cost-basis-unknown`, and `DEPENDENCY_ABSENT`).
   - The probe asserts structural runner and aggregation correctness under Policy 1, not final tax determinations.

---

## 6. Execution Verification

The probe was executed using the repository's normal verification tools:

- **Targeted Static Analysis:**
  ```sh
  python3 -m mypy docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances-evidence/test_candidate_c_probe.py
  ```
  *Result:* `Success: no issues found in 1 source file`.
- **Focused Execution Probe:**
  ```sh
  pytest docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances-evidence/test_candidate_c_probe.py
  ```
  *Result:* `9 passed in 36.10s`.

All 9 cases executed through the real recorder, package validation, marshalling, and `live_coordinate_run` on unchanged derivation engine code.

---

## 7. Conclusion and Next Step Recommendation

Candidate C succeeded on all 9 measured cases:
- It eliminates the P5 defect where a blocked statement was silently absorbed into the return entry.
- It eliminates the forward scheduling order-dependence (Cycle 0 premature block) by using declared `reads_subject_results`.
- It preserves exact fractional dollar-and-cent amounts with zero new rounding.
- It requires **zero new schemas** and **zero engine modifications**.

**Work Remaining for Production Adoption:**
Candidate C avoids engine and schema extensions, but requires standard content successor authoring for production:
1. Authoring production `rule.f1099k-box1a-subtotal.json`.
2. Authoring production `family.f1099k.v2.json` and `closure-mapping.f1099k.v2.json`.
3. Updating production `rule.schedule1-top-entry` to `v3` selection.
4. Authoring matching successors for dependent family consumers: `rule.attachment.schedule-1.v4.json` (subtotal tie out) and `rule.f1099k-unresolved.v3.json` (reconciling family pin and multi-statement count).
5. Completing the sale circumstance input transport, presentation model projection, and review reloading for multi-statement workspaces.
