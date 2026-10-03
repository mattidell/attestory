# Track 1a-4 — one worksheet declaration

Disposable candidate. `rule-artifact.v13` is unbuilt. This file states the declaration. The probe runs it. No package validation of v13 is claimed.

Part 3 puts one `reads_subject_results` object on the rule and forbids that symbol in `requires`. Part 4 says the names a path references equal that path's `requires`, and that path pins are `assertion` / `v1`. A path that collects a derived per-subject result cannot satisfy both. The declaration below is the composition this unit will run.

## Item 1. Candidate declaration

The worksheet is return-level. It has `selection` and no top-level `value`. Top-level `when` is true. Top-level `requires` and `pins` are empty.

The old path is the production nonempty worksheet branch. Each of the five answer collects is a per-subject status result. The new path is that same branch with those five collects replaced by one collect of `demo.tax.track0d.statement-conclusion`. The default holds the closed-empty branch: a closed family with no box 1 publishes 0. A nonempty family with neither path active blocks.

A derived per-subject result is pinned as role `input`, version `v2`, origin `derived`, id the derived finding id. That pin is not an `assertion` / `v1` input. It is not a declared path pin. The publication adds it when the selected path reads the entry.

### Assumptions the probe will test

1. Old-path presence is `source_nonempty` of any of the five answer fact types (`member_fact_types`). The v9 activity object names one member. Five answers need the list. The probe treats the path as active when any listed member has a current source.
2. New-path presence is `source_nonempty` of `tax.us.2025.sli.statement-inclusion-relationship`. The predicate is current sources of that fact type. No `source_family` is declared: this probe has no adopted family for the inclusion. "No links" means that source is absent, including when the conclusion rule never published.
3. `reads_subject_results` is a list on the path that reads those results, and on the default only when the default reads any. This default reads none. The symbols in the list are excluded from that path's `requires` and from its declared pins.
4. Names inside a `conditional_dependency_set`'s members are not path `requires`. A `count` of box 1 on the closed family is not a `requires` entry. Other `ref` names in the selected path's value are that path's `requires`.
5. `filing_status` is a choice pin, version `v1`, with no origin. Every other declared path pin is role `input`, version `v1`, origin `assertion`. The pin ids equal the path's `requires`, in the same order.
6. The default's `missing_subjects` block names the current box-1 fact ids, sorted, under `DEPENDENCY_INVALID`. Closed-empty takes the `then` branch and publishes 0. Nonempty with neither path does not publish 0.
7. Each status publisher emits the answer value when the joined row is present, and blocks when the count of that answer on the subject is 0. The old path's collect expects `yes`. A block entry is a result. The declared read refuses it. The new path's collect expects `plain-case-supported`.
8. Origin `derived` is not in the published derived-finding pin enum (`assertion`, `declared_default`). The probe records the pin anyway. That schema gap is not a reason to relabel the pin `assertion` / `v1`.

### Scheduling choice

Presence is decided from current sources before any path's `requires` are consulted. Both paths active: the worksheet is eligible at once, waits for neither path's publishers, evaluates no path value, and blocks with missing `old-and-new-sli-inputs-both-present`. One path active: the worksheet waits only for that path's ordinary `requires` symbols and for every publisher of that path's `reads_subject_results` symbols to be in `resolved`. It does not wait for the unsuffixed symbol to appear in `symbols`. The other path's publishers do not gate it. No path active: the default is eligible and does not wait for any per-statement publisher.

### Pin choice

Declared path pins are the contract set above. They are not the finding ids on the publication. The publication pins the findings the expression read. A derived entry adds the `derived_entry_pin` below. A subject with no result is named in `missing` and gets no invented pin. Each entry keeps the pins its own per-subject publication or block already recorded. Conflict pins the current source findings that made each path active (role `input`, version `v1`, origin `assertion`), plus the rule, adoption, and governance pins. Parameter reads stay parameter pins and are not `requires`.

```json
{
  "worksheet": {
    "schema": "rule-artifact.v13",
    "id": "demo.rule.track1a4.worksheet",
    "version": "v1",
    "scope": {
      "family": "individual-income-tax",
      "jurisdiction": "US-federal",
      "tax_year": 2025
    },
    "role": "computation",
    "citations": [
      {
        "id": "tax.us.2025.citation.form1040.sli-worksheet",
        "version": "v1"
      },
      {
        "id": "tax.us.2025.citation.schedule1.line-21",
        "version": "v1"
      }
    ],
    "publishes": "tax.us.2025.schedule1.line21-sli-deduction",
    "when": true,
    "requires": [],
    "pins": [],
    "selection": {
      "mode": "exclusive_presence",
      "conflict": "refuse",
      "paths": [
        {
          "id": "old",
          "activity": {
            "kind": "source_nonempty",
            "source_family": {
              "id": "tax.us.2025.f1098e.1",
              "version": "v1"
            },
            "member_fact_types": [
              {
                "id": "tax.us.2025.f1098e.no-related-person-interest",
                "version": "v1"
              },
              {
                "id": "tax.us.2025.f1098e.no-non-qualified-loan-component",
                "version": "v1"
              },
              {
                "id": "tax.us.2025.f1098e.no-qualified-employer-plan-interest",
                "version": "v1"
              },
              {
                "id": "tax.us.2025.f1098e.no-employer-educational-assistance-interest",
                "version": "v1"
              },
              {
                "id": "tax.us.2025.f1098e.no-qtp-earnings-used",
                "version": "v1"
              }
            ]
          },
          "reads_subject_results": [
            {
              "symbol": "demo.tax.track1a4.status.no-related-person-interest",
              "subject": {
                "id": "tax.us.2025.f1098e.box1-student-loan-interest",
                "version": "v1"
              }
            },
            {
              "symbol": "demo.tax.track1a4.status.no-non-qualified-loan-component",
              "subject": {
                "id": "tax.us.2025.f1098e.box1-student-loan-interest",
                "version": "v1"
              }
            },
            {
              "symbol": "demo.tax.track1a4.status.no-qualified-employer-plan-interest",
              "subject": {
                "id": "tax.us.2025.f1098e.box1-student-loan-interest",
                "version": "v1"
              }
            },
            {
              "symbol": "demo.tax.track1a4.status.no-employer-educational-assistance-interest",
              "subject": {
                "id": "tax.us.2025.f1098e.box1-student-loan-interest",
                "version": "v1"
              }
            },
            {
              "symbol": "demo.tax.track1a4.status.no-qtp-earnings-used",
              "subject": {
                "id": "tax.us.2025.f1098e.box1-student-loan-interest",
                "version": "v1"
              }
            }
          ],
          "requires": [
            "filing_status",
            "rounding.convention",
            "tax.us.2025.income.total-income",
            "tax.us.2025.schedule1-adjustments-scope.no-line11-educator",
            "tax.us.2025.schedule1-adjustments-scope.no-line12-business-expenses",
            "tax.us.2025.schedule1-adjustments-scope.no-line13-hsa",
            "tax.us.2025.schedule1-adjustments-scope.no-line14-moving",
            "tax.us.2025.schedule1-adjustments-scope.no-line15-deductible-se",
            "tax.us.2025.schedule1-adjustments-scope.no-line16-se-retirement",
            "tax.us.2025.schedule1-adjustments-scope.no-line17-se-health",
            "tax.us.2025.schedule1-adjustments-scope.no-line18-penalty",
            "tax.us.2025.schedule1-adjustments-scope.no-line19-alimony-paid",
            "tax.us.2025.schedule1-adjustments-scope.no-line20-ira-deduction",
            "tax.us.2025.schedule1-adjustments-scope.no-line23-archer-msa",
            "tax.us.2025.schedule1-adjustments-scope.no-line25-other-adjustments",
            "tax.us.2025.sli-scope.legally-obligated-for-interest",
            "tax.us.2025.sli-scope.no-form-2555",
            "tax.us.2025.sli-scope.no-form-4563",
            "tax.us.2025.sli-scope.no-puerto-rico-or-samoa-income",
            "tax.us.2025.sli-scope.not-claimed-as-dependent",
            "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal"
          ],
          "pins": [
            {
              "role": "choice",
              "id": "filing_status",
              "version": "v1"
            },
            {
              "role": "input",
              "id": "rounding.convention",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.income.total-income",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line11-educator",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line12-business-expenses",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line13-hsa",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line14-moving",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line15-deductible-se",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line16-se-retirement",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line17-se-health",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line18-penalty",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line19-alimony-paid",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line20-ira-deduction",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line23-archer-msa",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line25-other-adjustments",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.sli-scope.legally-obligated-for-interest",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.sli-scope.no-form-2555",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.sli-scope.no-form-4563",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.sli-scope.no-puerto-rico-or-samoa-income",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.sli-scope.not-claimed-as-dependent",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal",
              "version": "v1",
              "origin": "assertion"
            }
          ],
          "when": true,
          "value": {
            "mode": {
              "name": "rounding.convention",
              "op": "ref"
            },
            "op": "round",
            "value": {
              "else": {
                "else": {
                  "else": {
                    "else": {
                      "left": {
                        "left": {
                          "name": "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal",
                          "op": "ref"
                        },
                        "op": "subtract",
                        "right": {
                          "args": [
                            {
                              "left": {
                                "name": "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal",
                                "op": "ref"
                              },
                              "op": "subtract",
                              "right": {
                                "op": "parameter",
                                "parameter_id": "tax.us.2025.parameter.sli-interest-cap"
                              }
                            },
                            0
                          ],
                          "op": "max"
                        }
                      },
                      "op": "subtract",
                      "right": {
                        "left": {
                          "left": {
                            "name": "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal",
                            "op": "ref"
                          },
                          "op": "subtract",
                          "right": {
                            "args": [
                              {
                                "left": {
                                  "name": "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal",
                                  "op": "ref"
                                },
                                "op": "subtract",
                                "right": {
                                  "op": "parameter",
                                  "parameter_id": "tax.us.2025.parameter.sli-interest-cap"
                                }
                              },
                              0
                            ],
                            "op": "max"
                          }
                        },
                        "op": "multiply",
                        "right": {
                          "left": {
                            "left": {
                              "args": [
                                {
                                  "left": {
                                    "left": {
                                      "name": "tax.us.2025.income.total-income",
                                      "op": "ref"
                                    },
                                    "op": "subtract",
                                    "right": 0
                                  },
                                  "op": "subtract",
                                  "right": {
                                    "key": {
                                      "name": "filing_status",
                                      "op": "ref"
                                    },
                                    "op": "parameter",
                                    "parameter_id": "tax.us.2025.parameter.sli-magi-threshold"
                                  }
                                },
                                0
                              ],
                              "op": "max"
                            },
                            "min_decimal_places": 3,
                            "op": "divide",
                            "right": {
                              "key": {
                                "name": "filing_status",
                                "op": "ref"
                              },
                              "op": "parameter",
                              "parameter_id": "tax.us.2025.parameter.sli-magi-phase-range"
                            },
                            "rounding": "half_up"
                          },
                          "op": "subtract",
                          "right": {
                            "args": [
                              {
                                "left": {
                                  "left": {
                                    "args": [
                                      {
                                        "left": {
                                          "left": {
                                            "name": "tax.us.2025.income.total-income",
                                            "op": "ref"
                                          },
                                          "op": "subtract",
                                          "right": 0
                                        },
                                        "op": "subtract",
                                        "right": {
                                          "key": {
                                            "name": "filing_status",
                                            "op": "ref"
                                          },
                                          "op": "parameter",
                                          "parameter_id": "tax.us.2025.parameter.sli-magi-threshold"
                                        }
                                      },
                                      0
                                    ],
                                    "op": "max"
                                  },
                                  "min_decimal_places": 3,
                                  "op": "divide",
                                  "right": {
                                    "key": {
                                      "name": "filing_status",
                                      "op": "ref"
                                    },
                                    "op": "parameter",
                                    "parameter_id": "tax.us.2025.parameter.sli-magi-phase-range"
                                  },
                                  "rounding": "half_up"
                                },
                                "op": "subtract",
                                "right": 1
                              },
                              0
                            ],
                            "op": "max"
                          }
                        }
                      }
                    },
                    "op": "choose",
                    "then": 0,
                    "when": {
                      "args": [
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.sli-scope.not-claimed-as-dependent",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.sli-scope.not-claimed-as-dependent",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "no"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.sli-scope.legally-obligated-for-interest",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.sli-scope.legally-obligated-for-interest",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "no"
                          }
                        }
                      ],
                      "op": "any"
                    }
                  },
                  "op": "choose",
                  "then": {
                    "code": "SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE",
                    "op": "block"
                  },
                  "when": {
                    "op": "not",
                    "value": {
                      "args": [
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line11-educator",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line11-educator",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line12-business-expenses",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line12-business-expenses",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line13-hsa",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line13-hsa",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line14-moving",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line14-moving",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line15-deductible-se",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line15-deductible-se",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line16-se-retirement",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line16-se-retirement",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line17-se-health",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line17-se-health",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line18-penalty",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line18-penalty",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line19-alimony-paid",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line19-alimony-paid",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line20-ira-deduction",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line20-ira-deduction",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line23-archer-msa",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line23-archer-msa",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line25-other-adjustments",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line25-other-adjustments",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        }
                      ],
                      "op": "all"
                    }
                  }
                },
                "op": "choose",
                "then": {
                  "code": "SLI_UNIVERSAL_COMPONENT_VIOLATION",
                  "op": "block"
                },
                "when": {
                  "op": "not",
                  "value": {
                    "args": [
                      {
                        "cmp": "eq",
                        "left": {
                          "name": "tax.us.2025.sli-scope.no-form-2555",
                          "op": "ref"
                        },
                        "op": "categorical_compare",
                        "right": {
                          "fact_type": {
                            "id": "tax.us.2025.sli-scope.no-form-2555",
                            "version": "v1"
                          },
                          "op": "category_literal",
                          "value": "yes"
                        }
                      },
                      {
                        "cmp": "eq",
                        "left": {
                          "name": "tax.us.2025.sli-scope.no-form-4563",
                          "op": "ref"
                        },
                        "op": "categorical_compare",
                        "right": {
                          "fact_type": {
                            "id": "tax.us.2025.sli-scope.no-form-4563",
                            "version": "v1"
                          },
                          "op": "category_literal",
                          "value": "yes"
                        }
                      },
                      {
                        "cmp": "eq",
                        "left": {
                          "name": "tax.us.2025.sli-scope.no-puerto-rico-or-samoa-income",
                          "op": "ref"
                        },
                        "op": "categorical_compare",
                        "right": {
                          "fact_type": {
                            "id": "tax.us.2025.sli-scope.no-puerto-rico-or-samoa-income",
                            "version": "v1"
                          },
                          "op": "category_literal",
                          "value": "yes"
                        }
                      },
                      {
                        "op": "collect_categorical_all_equal",
                        "name": "demo.tax.track1a4.status.no-related-person-interest",
                        "value": {
                          "op": "category_literal",
                          "fact_type": {
                            "id": "demo.tax.track1a4.status.no-related-person-interest",
                            "version": "v1"
                          },
                          "value": "yes"
                        }
                      },
                      {
                        "op": "collect_categorical_all_equal",
                        "name": "demo.tax.track1a4.status.no-qualified-employer-plan-interest",
                        "value": {
                          "op": "category_literal",
                          "fact_type": {
                            "id": "demo.tax.track1a4.status.no-qualified-employer-plan-interest",
                            "version": "v1"
                          },
                          "value": "yes"
                        }
                      },
                      {
                        "op": "collect_categorical_all_equal",
                        "name": "demo.tax.track1a4.status.no-non-qualified-loan-component",
                        "value": {
                          "op": "category_literal",
                          "fact_type": {
                            "id": "demo.tax.track1a4.status.no-non-qualified-loan-component",
                            "version": "v1"
                          },
                          "value": "yes"
                        }
                      },
                      {
                        "op": "collect_categorical_all_equal",
                        "name": "demo.tax.track1a4.status.no-employer-educational-assistance-interest",
                        "value": {
                          "op": "category_literal",
                          "fact_type": {
                            "id": "demo.tax.track1a4.status.no-employer-educational-assistance-interest",
                            "version": "v1"
                          },
                          "value": "yes"
                        }
                      },
                      {
                        "op": "collect_categorical_all_equal",
                        "name": "demo.tax.track1a4.status.no-qtp-earnings-used",
                        "value": {
                          "op": "category_literal",
                          "fact_type": {
                            "id": "demo.tax.track1a4.status.no-qtp-earnings-used",
                            "version": "v1"
                          },
                          "value": "yes"
                        }
                      }
                    ],
                    "op": "all"
                  }
                }
              },
              "op": "choose",
              "then": {
                "code": "SLI_MFS_INELIGIBLE",
                "op": "block"
              },
              "when": {
                "cmp": "eq",
                "left": {
                  "name": "filing_status",
                  "op": "ref"
                },
                "op": "categorical_compare",
                "right": {
                  "fact_type": {
                    "id": "tax.us.2025.filing-status",
                    "version": "v1"
                  },
                  "op": "category_literal",
                  "value": "married_filing_separately"
                }
              }
            }
          }
        },
        {
          "id": "new",
          "activity": {
            "kind": "source_nonempty",
            "member_fact_type": {
              "id": "tax.us.2025.sli.statement-inclusion-relationship",
              "version": "v1"
            }
          },
          "reads_subject_results": [
            {
              "symbol": "demo.tax.track0d.statement-conclusion",
              "subject": {
                "id": "tax.us.2025.f1098e.box1-student-loan-interest",
                "version": "v1"
              }
            }
          ],
          "requires": [
            "filing_status",
            "rounding.convention",
            "tax.us.2025.income.total-income",
            "tax.us.2025.schedule1-adjustments-scope.no-line11-educator",
            "tax.us.2025.schedule1-adjustments-scope.no-line12-business-expenses",
            "tax.us.2025.schedule1-adjustments-scope.no-line13-hsa",
            "tax.us.2025.schedule1-adjustments-scope.no-line14-moving",
            "tax.us.2025.schedule1-adjustments-scope.no-line15-deductible-se",
            "tax.us.2025.schedule1-adjustments-scope.no-line16-se-retirement",
            "tax.us.2025.schedule1-adjustments-scope.no-line17-se-health",
            "tax.us.2025.schedule1-adjustments-scope.no-line18-penalty",
            "tax.us.2025.schedule1-adjustments-scope.no-line19-alimony-paid",
            "tax.us.2025.schedule1-adjustments-scope.no-line20-ira-deduction",
            "tax.us.2025.schedule1-adjustments-scope.no-line23-archer-msa",
            "tax.us.2025.schedule1-adjustments-scope.no-line25-other-adjustments",
            "tax.us.2025.sli-scope.legally-obligated-for-interest",
            "tax.us.2025.sli-scope.no-form-2555",
            "tax.us.2025.sli-scope.no-form-4563",
            "tax.us.2025.sli-scope.no-puerto-rico-or-samoa-income",
            "tax.us.2025.sli-scope.not-claimed-as-dependent",
            "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal"
          ],
          "pins": [
            {
              "role": "choice",
              "id": "filing_status",
              "version": "v1"
            },
            {
              "role": "input",
              "id": "rounding.convention",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.income.total-income",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line11-educator",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line12-business-expenses",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line13-hsa",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line14-moving",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line15-deductible-se",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line16-se-retirement",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line17-se-health",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line18-penalty",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line19-alimony-paid",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line20-ira-deduction",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line23-archer-msa",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.schedule1-adjustments-scope.no-line25-other-adjustments",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.sli-scope.legally-obligated-for-interest",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.sli-scope.no-form-2555",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.sli-scope.no-form-4563",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.sli-scope.no-puerto-rico-or-samoa-income",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.sli-scope.not-claimed-as-dependent",
              "version": "v1",
              "origin": "assertion"
            },
            {
              "role": "input",
              "id": "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal",
              "version": "v1",
              "origin": "assertion"
            }
          ],
          "when": true,
          "value": {
            "mode": {
              "name": "rounding.convention",
              "op": "ref"
            },
            "op": "round",
            "value": {
              "else": {
                "else": {
                  "else": {
                    "else": {
                      "left": {
                        "left": {
                          "name": "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal",
                          "op": "ref"
                        },
                        "op": "subtract",
                        "right": {
                          "args": [
                            {
                              "left": {
                                "name": "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal",
                                "op": "ref"
                              },
                              "op": "subtract",
                              "right": {
                                "op": "parameter",
                                "parameter_id": "tax.us.2025.parameter.sli-interest-cap"
                              }
                            },
                            0
                          ],
                          "op": "max"
                        }
                      },
                      "op": "subtract",
                      "right": {
                        "left": {
                          "left": {
                            "name": "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal",
                            "op": "ref"
                          },
                          "op": "subtract",
                          "right": {
                            "args": [
                              {
                                "left": {
                                  "name": "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal",
                                  "op": "ref"
                                },
                                "op": "subtract",
                                "right": {
                                  "op": "parameter",
                                  "parameter_id": "tax.us.2025.parameter.sli-interest-cap"
                                }
                              },
                              0
                            ],
                            "op": "max"
                          }
                        },
                        "op": "multiply",
                        "right": {
                          "left": {
                            "left": {
                              "args": [
                                {
                                  "left": {
                                    "left": {
                                      "name": "tax.us.2025.income.total-income",
                                      "op": "ref"
                                    },
                                    "op": "subtract",
                                    "right": 0
                                  },
                                  "op": "subtract",
                                  "right": {
                                    "key": {
                                      "name": "filing_status",
                                      "op": "ref"
                                    },
                                    "op": "parameter",
                                    "parameter_id": "tax.us.2025.parameter.sli-magi-threshold"
                                  }
                                },
                                0
                              ],
                              "op": "max"
                            },
                            "min_decimal_places": 3,
                            "op": "divide",
                            "right": {
                              "key": {
                                "name": "filing_status",
                                "op": "ref"
                              },
                              "op": "parameter",
                              "parameter_id": "tax.us.2025.parameter.sli-magi-phase-range"
                            },
                            "rounding": "half_up"
                          },
                          "op": "subtract",
                          "right": {
                            "args": [
                              {
                                "left": {
                                  "left": {
                                    "args": [
                                      {
                                        "left": {
                                          "left": {
                                            "name": "tax.us.2025.income.total-income",
                                            "op": "ref"
                                          },
                                          "op": "subtract",
                                          "right": 0
                                        },
                                        "op": "subtract",
                                        "right": {
                                          "key": {
                                            "name": "filing_status",
                                            "op": "ref"
                                          },
                                          "op": "parameter",
                                          "parameter_id": "tax.us.2025.parameter.sli-magi-threshold"
                                        }
                                      },
                                      0
                                    ],
                                    "op": "max"
                                  },
                                  "min_decimal_places": 3,
                                  "op": "divide",
                                  "right": {
                                    "key": {
                                      "name": "filing_status",
                                      "op": "ref"
                                    },
                                    "op": "parameter",
                                    "parameter_id": "tax.us.2025.parameter.sli-magi-phase-range"
                                  },
                                  "rounding": "half_up"
                                },
                                "op": "subtract",
                                "right": 1
                              },
                              0
                            ],
                            "op": "max"
                          }
                        }
                      }
                    },
                    "op": "choose",
                    "then": 0,
                    "when": {
                      "args": [
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.sli-scope.not-claimed-as-dependent",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.sli-scope.not-claimed-as-dependent",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "no"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.sli-scope.legally-obligated-for-interest",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.sli-scope.legally-obligated-for-interest",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "no"
                          }
                        }
                      ],
                      "op": "any"
                    }
                  },
                  "op": "choose",
                  "then": {
                    "code": "SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE",
                    "op": "block"
                  },
                  "when": {
                    "op": "not",
                    "value": {
                      "args": [
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line11-educator",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line11-educator",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line12-business-expenses",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line12-business-expenses",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line13-hsa",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line13-hsa",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line14-moving",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line14-moving",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line15-deductible-se",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line15-deductible-se",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line16-se-retirement",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line16-se-retirement",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line17-se-health",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line17-se-health",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line18-penalty",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line18-penalty",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line19-alimony-paid",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line19-alimony-paid",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line20-ira-deduction",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line20-ira-deduction",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line23-archer-msa",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line23-archer-msa",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        },
                        {
                          "cmp": "eq",
                          "left": {
                            "name": "tax.us.2025.schedule1-adjustments-scope.no-line25-other-adjustments",
                            "op": "ref"
                          },
                          "op": "categorical_compare",
                          "right": {
                            "fact_type": {
                              "id": "tax.us.2025.schedule1-adjustments-scope.no-line25-other-adjustments",
                              "version": "v1"
                            },
                            "op": "category_literal",
                            "value": "yes"
                          }
                        }
                      ],
                      "op": "all"
                    }
                  }
                },
                "op": "choose",
                "then": {
                  "code": "SLI_UNIVERSAL_COMPONENT_VIOLATION",
                  "op": "block"
                },
                "when": {
                  "op": "not",
                  "value": {
                    "args": [
                      {
                        "cmp": "eq",
                        "left": {
                          "name": "tax.us.2025.sli-scope.no-form-2555",
                          "op": "ref"
                        },
                        "op": "categorical_compare",
                        "right": {
                          "fact_type": {
                            "id": "tax.us.2025.sli-scope.no-form-2555",
                            "version": "v1"
                          },
                          "op": "category_literal",
                          "value": "yes"
                        }
                      },
                      {
                        "cmp": "eq",
                        "left": {
                          "name": "tax.us.2025.sli-scope.no-form-4563",
                          "op": "ref"
                        },
                        "op": "categorical_compare",
                        "right": {
                          "fact_type": {
                            "id": "tax.us.2025.sli-scope.no-form-4563",
                            "version": "v1"
                          },
                          "op": "category_literal",
                          "value": "yes"
                        }
                      },
                      {
                        "cmp": "eq",
                        "left": {
                          "name": "tax.us.2025.sli-scope.no-puerto-rico-or-samoa-income",
                          "op": "ref"
                        },
                        "op": "categorical_compare",
                        "right": {
                          "fact_type": {
                            "id": "tax.us.2025.sli-scope.no-puerto-rico-or-samoa-income",
                            "version": "v1"
                          },
                          "op": "category_literal",
                          "value": "yes"
                        }
                      },
                      {
                        "op": "collect_categorical_all_equal",
                        "name": "demo.tax.track0d.statement-conclusion",
                        "value": {
                          "op": "category_literal",
                          "fact_type": {
                            "id": "demo.tax.track0d.statement-conclusion",
                            "version": "v1"
                          },
                          "value": "plain-case-supported"
                        }
                      }
                    ],
                    "op": "all"
                  }
                }
              },
              "op": "choose",
              "then": {
                "code": "SLI_MFS_INELIGIBLE",
                "op": "block"
              },
              "when": {
                "cmp": "eq",
                "left": {
                  "name": "filing_status",
                  "op": "ref"
                },
                "op": "categorical_compare",
                "right": {
                  "fact_type": {
                    "id": "tax.us.2025.filing-status",
                    "version": "v1"
                  },
                  "op": "category_literal",
                  "value": "married_filing_separately"
                }
              }
            }
          }
        }
      ],
      "default": {
        "id": "neither",
        "reads_subject_results": [],
        "requires": [],
        "pins": [],
        "when": true,
        "value": {
          "op": "choose",
          "when": {
            "op": "compare",
            "cmp": "eq",
            "left": {
              "op": "count",
              "name": "tax.us.2025.f1098e.box1-student-loan-interest",
              "source_set": "tax.us.2025.f1098e.1"
            },
            "right": 0
          },
          "then": 0,
          "else": {
            "op": "block",
            "code": "DEPENDENCY_INVALID",
            "missing_subjects": {
              "id": "tax.us.2025.f1098e.box1-student-loan-interest",
              "version": "v1"
            }
          }
        }
      },
      "refusal": {
        "code": "DEPENDENCY_INVALID",
        "missing": [
          "old-and-new-sli-inputs-both-present"
        ],
        "pins": []
      }
    }
  },
  "same_run_status_publishers": [
    {
      "schema": "rule-artifact.v12",
      "id": "demo.rule.track1a4.status.no-related-person-interest",
      "version": "v1",
      "scope": {
        "tax_year": 2025,
        "jurisdiction": "us",
        "family": "demo-student-loan"
      },
      "subject": {
        "id": "tax.us.2025.f1098e.box1-student-loan-interest",
        "version": "v1"
      },
      "joined": {
        "id": "tax.us.2025.f1098e.no-related-person-interest",
        "version": "v1"
      },
      "direction": "joined_contains_subject",
      "role": "computation",
      "requires": [
        "tax.us.2025.f1098e.no-related-person-interest"
      ],
      "pins": [],
      "when": true,
      "publishes": "demo.tax.track1a4.status.no-related-person-interest",
      "blocked": {
        "code": "DEPENDENCY_INVALID",
        "missing": []
      },
      "value": {
        "op": "choose",
        "when": {
          "op": "compare",
          "cmp": "eq",
          "left": {
            "op": "link_count",
            "links": "tax.us.2025.f1098e.no-related-person-interest"
          },
          "right": 0
        },
        "then": {
          "op": "block",
          "code": "DEPENDENCY_INVALID"
        },
        "else": {
          "op": "ref",
          "name": "tax.us.2025.f1098e.no-related-person-interest"
        }
      }
    },
    {
      "schema": "rule-artifact.v12",
      "id": "demo.rule.track1a4.status.no-non-qualified-loan-component",
      "version": "v1",
      "scope": {
        "tax_year": 2025,
        "jurisdiction": "us",
        "family": "demo-student-loan"
      },
      "subject": {
        "id": "tax.us.2025.f1098e.box1-student-loan-interest",
        "version": "v1"
      },
      "joined": {
        "id": "tax.us.2025.f1098e.no-non-qualified-loan-component",
        "version": "v1"
      },
      "direction": "joined_contains_subject",
      "role": "computation",
      "requires": [
        "tax.us.2025.f1098e.no-non-qualified-loan-component"
      ],
      "pins": [],
      "when": true,
      "publishes": "demo.tax.track1a4.status.no-non-qualified-loan-component",
      "blocked": {
        "code": "DEPENDENCY_INVALID",
        "missing": []
      },
      "value": {
        "op": "choose",
        "when": {
          "op": "compare",
          "cmp": "eq",
          "left": {
            "op": "link_count",
            "links": "tax.us.2025.f1098e.no-non-qualified-loan-component"
          },
          "right": 0
        },
        "then": {
          "op": "block",
          "code": "DEPENDENCY_INVALID"
        },
        "else": {
          "op": "ref",
          "name": "tax.us.2025.f1098e.no-non-qualified-loan-component"
        }
      }
    },
    {
      "schema": "rule-artifact.v12",
      "id": "demo.rule.track1a4.status.no-qualified-employer-plan-interest",
      "version": "v1",
      "scope": {
        "tax_year": 2025,
        "jurisdiction": "us",
        "family": "demo-student-loan"
      },
      "subject": {
        "id": "tax.us.2025.f1098e.box1-student-loan-interest",
        "version": "v1"
      },
      "joined": {
        "id": "tax.us.2025.f1098e.no-qualified-employer-plan-interest",
        "version": "v1"
      },
      "direction": "joined_contains_subject",
      "role": "computation",
      "requires": [
        "tax.us.2025.f1098e.no-qualified-employer-plan-interest"
      ],
      "pins": [],
      "when": true,
      "publishes": "demo.tax.track1a4.status.no-qualified-employer-plan-interest",
      "blocked": {
        "code": "DEPENDENCY_INVALID",
        "missing": []
      },
      "value": {
        "op": "choose",
        "when": {
          "op": "compare",
          "cmp": "eq",
          "left": {
            "op": "link_count",
            "links": "tax.us.2025.f1098e.no-qualified-employer-plan-interest"
          },
          "right": 0
        },
        "then": {
          "op": "block",
          "code": "DEPENDENCY_INVALID"
        },
        "else": {
          "op": "ref",
          "name": "tax.us.2025.f1098e.no-qualified-employer-plan-interest"
        }
      }
    },
    {
      "schema": "rule-artifact.v12",
      "id": "demo.rule.track1a4.status.no-employer-educational-assistance-interest",
      "version": "v1",
      "scope": {
        "tax_year": 2025,
        "jurisdiction": "us",
        "family": "demo-student-loan"
      },
      "subject": {
        "id": "tax.us.2025.f1098e.box1-student-loan-interest",
        "version": "v1"
      },
      "joined": {
        "id": "tax.us.2025.f1098e.no-employer-educational-assistance-interest",
        "version": "v1"
      },
      "direction": "joined_contains_subject",
      "role": "computation",
      "requires": [
        "tax.us.2025.f1098e.no-employer-educational-assistance-interest"
      ],
      "pins": [],
      "when": true,
      "publishes": "demo.tax.track1a4.status.no-employer-educational-assistance-interest",
      "blocked": {
        "code": "DEPENDENCY_INVALID",
        "missing": []
      },
      "value": {
        "op": "choose",
        "when": {
          "op": "compare",
          "cmp": "eq",
          "left": {
            "op": "link_count",
            "links": "tax.us.2025.f1098e.no-employer-educational-assistance-interest"
          },
          "right": 0
        },
        "then": {
          "op": "block",
          "code": "DEPENDENCY_INVALID"
        },
        "else": {
          "op": "ref",
          "name": "tax.us.2025.f1098e.no-employer-educational-assistance-interest"
        }
      }
    },
    {
      "schema": "rule-artifact.v12",
      "id": "demo.rule.track1a4.status.no-qtp-earnings-used",
      "version": "v1",
      "scope": {
        "tax_year": 2025,
        "jurisdiction": "us",
        "family": "demo-student-loan"
      },
      "subject": {
        "id": "tax.us.2025.f1098e.box1-student-loan-interest",
        "version": "v1"
      },
      "joined": {
        "id": "tax.us.2025.f1098e.no-qtp-earnings-used",
        "version": "v1"
      },
      "direction": "joined_contains_subject",
      "role": "computation",
      "requires": [
        "tax.us.2025.f1098e.no-qtp-earnings-used"
      ],
      "pins": [],
      "when": true,
      "publishes": "demo.tax.track1a4.status.no-qtp-earnings-used",
      "blocked": {
        "code": "DEPENDENCY_INVALID",
        "missing": []
      },
      "value": {
        "op": "choose",
        "when": {
          "op": "compare",
          "cmp": "eq",
          "left": {
            "op": "link_count",
            "links": "tax.us.2025.f1098e.no-qtp-earnings-used"
          },
          "right": 0
        },
        "then": {
          "op": "block",
          "code": "DEPENDENCY_INVALID"
        },
        "else": {
          "op": "ref",
          "name": "tax.us.2025.f1098e.no-qtp-earnings-used"
        }
      }
    }
  ],
  "new_path_publisher": {
    "id": "demo.rule.track0d.statement-conclusion",
    "publishes": "demo.tax.track0d.statement-conclusion",
    "subject": {
      "id": "tax.us.2025.f1098e.box1-student-loan-interest",
      "version": "v1"
    },
    "note": "The accepted Track 0d statement rule. It stays in the same run. Its value is not restated here."
  },
  "derived_entry_pin": {
    "role": "input",
    "id": "the derived finding id of the entry that was read",
    "version": "v2",
    "origin": "derived"
  }
}
```

## Item 2. Scheduling

The rule id is `demo.rule.track1a4.worksheet`. It is not line 2b, and it does not use the v9 authorization gate.

Eligibility, in order:

1. Read current sources. Old is active when any of the five answer fact types has a source. New is active when the inclusion fact type has a source. This step does not read `requires`, `symbols`, or `resolved`.
2. Two active paths: eligible now. Top-level `requires` are empty, so nothing is waited on. Block `DEPENDENCY_INVALID`, missing `["old-and-new-sli-inputs-both-present"]`. Do not evaluate either path or the default.
3. One active path: eligible when every name in that path's `requires` is present as a symbol, and every rule that publishes a symbol in that path's `reads_subject_results` is in `resolved`. If the package has no publisher for a declared symbol, do not wait on it. Do not add the declared symbol to `requires`. Do not wait for the inactive path's publishers.
4. No active path: evaluate the default. Its `requires` are empty. Do not wait for the status publishers or the statement-conclusion publisher.

An inactive path's per-statement rules may still run in the same saturation. Their block or publication does not decide this rule's eligibility.

## Item 3. Collection access

One rule covers both paths. After the wait in item 2, a `collect`, `count`, or `collect_categorical_all_equal` whose `name` is a symbol in the selected path's `reads_subject_results` reads the current box-1 subjects and nothing else. For each current subject fact id the entry is the publication `symbol|fact_id`, or the block with that keyed symbol. One of those is one result. Zero or two is `DEPENDENCY_INVALID`, and `missing` is those subject fact ids, sorted. A block entry is a result: the operator blocks `DEPENDENCY_INVALID` and `missing` is the blocked subjects' fact ids, sorted. It does not skip the block and it does not treat the block as an empty or favorable value.

The old path names five status symbols. The favorable value is `yes`. The new path names `demo.tax.track0d.statement-conclusion`. The favorable value is `plain-case-supported`. The default names no subject-result symbol. Its `count` of box 1 is the ordinary closed-family count, not this read.

A collect that is not in the selected path's `reads_subject_results` keeps today's behavior, including the Track 0f item 2 split. This declaration does not use that collect.

## Item 4. Execution

One declaration, both runners, then the line 21 presentation consumer. Worksheet dollars that depend on the declared read are executed with the runtime stand-in operator. The conclusion chain uses the Track 0d shared_key_count stand-in (executed with the runtime stand-in operator). Presentation is presentation only.

### old-only

Runners agree: True.
Forward line 21: published 2500.
Reference line 21: published 2500.
Presentation: disposition published_value, value 2500, codes None.
Presentation text: Schedule 1 line 21 is blocked because eligibility authority is incomplete, an excluded class is present, the filer is married filing separately, or the Form 1098-E box-1 family is unclosed.

Forward pins:

```json
[
  {
    "role": "adoption",
    "id": "demo.package.track0d",
    "version": "v1"
  },
  {
    "role": "choice",
    "id": "f.sli.filing",
    "version": "v1"
  },
  {
    "role": "citation",
    "id": "tax.us.2025.citation.form1040.sli-worksheet",
    "version": "v1"
  },
  {
    "role": "citation",
    "id": "tax.us.2025.citation.schedule1.line-21",
    "version": "v1"
  },
  {
    "role": "computation",
    "id": "demo.rule.track1a4.worksheet",
    "version": "v1"
  },
  {
    "role": "governance",
    "id": "demo.governance.track0d",
    "version": "v1"
  },
  {
    "role": "input",
    "id": "f.sli.component.0",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.1",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.10",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.11",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.12",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.13",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.14",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.15",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.16",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.2",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.3",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.4",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.5",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.6",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.7",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.8",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.9",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.income",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.rounding",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "finding:derived:0246a83c53f1f0fc3fc3818e",
    "version": "v2",
    "origin": "derived"
  },
  {
    "role": "input",
    "id": "finding:derived:2197db7f8610166ad1ad8292",
    "version": "v2",
    "origin": "derived"
  },
  {
    "role": "input",
    "id": "finding:derived:2793ed35b0be32a1e15a7dd4",
    "version": "v2",
    "origin": "derived"
  },
  {
    "role": "input",
    "id": "finding:derived:466851b58671240693eb5f19",
    "version": "v2",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "finding:derived:a85331365efc999db144fb0a",
    "version": "v2",
    "origin": "derived"
  },
  {
    "role": "input",
    "id": "finding:derived:e8c8c3c04d748fca16122096",
    "version": "v2",
    "origin": "derived"
  },
  {
    "role": "operation-semantics",
    "id": "round",
    "version": "v1"
  },
  {
    "role": "parameter",
    "id": "tax.us.2025.parameter.sli-interest-cap",
    "version": "v1"
  },
  {
    "role": "parameter",
    "id": "tax.us.2025.parameter.sli-magi-phase-range",
    "version": "v1"
  },
  {
    "role": "parameter",
    "id": "tax.us.2025.parameter.sli-magi-threshold",
    "version": "v1"
  }
]
```

Status publications: yes, yes, yes, yes, yes. Status blocks: 0. Conclusions: not-supported.

### new-only

Runners agree: True.
Forward line 21: published 2500.
Reference line 21: published 2500.
Presentation: disposition published_value, value 2500, codes None.
Presentation text: Schedule 1 line 21 is blocked because eligibility authority is incomplete, an excluded class is present, the filer is married filing separately, or the Form 1098-E box-1 family is unclosed.

Forward pins:

```json
[
  {
    "role": "adoption",
    "id": "demo.package.track0d",
    "version": "v1"
  },
  {
    "role": "choice",
    "id": "f.sli.filing",
    "version": "v1"
  },
  {
    "role": "citation",
    "id": "tax.us.2025.citation.form1040.sli-worksheet",
    "version": "v1"
  },
  {
    "role": "citation",
    "id": "tax.us.2025.citation.schedule1.line-21",
    "version": "v1"
  },
  {
    "role": "computation",
    "id": "demo.rule.track1a4.worksheet",
    "version": "v1"
  },
  {
    "role": "governance",
    "id": "demo.governance.track0d",
    "version": "v1"
  },
  {
    "role": "input",
    "id": "f.sli.component.0",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.1",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.10",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.11",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.12",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.13",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.14",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.15",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.16",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.2",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.3",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.4",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.5",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.6",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.7",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.8",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.component.9",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.income",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.rounding",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "finding:derived:466851b58671240693eb5f19",
    "version": "v2",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "finding:derived:7740a3282196853457849874",
    "version": "v2",
    "origin": "derived"
  },
  {
    "role": "operation-semantics",
    "id": "round",
    "version": "v1"
  },
  {
    "role": "parameter",
    "id": "tax.us.2025.parameter.sli-interest-cap",
    "version": "v1"
  },
  {
    "role": "parameter",
    "id": "tax.us.2025.parameter.sli-magi-phase-range",
    "version": "v1"
  },
  {
    "role": "parameter",
    "id": "tax.us.2025.parameter.sli-magi-threshold",
    "version": "v1"
  }
]
```

Status publications: . Status blocks: 5. Conclusions: plain-case-supported.

### both

Runners agree: True.
Forward line 21: blocked DEPENDENCY_INVALID missing [old-and-new-sli-inputs-both-present].
Reference line 21: blocked DEPENDENCY_INVALID missing [old-and-new-sli-inputs-both-present].
Presentation: disposition blocked, value None, codes ['DEPENDENCY_INVALID'].
Presentation text: Schedule 1 line 21 is blocked because eligibility authority is incomplete, an excluded class is present, the filer is married filing separately, or the Form 1098-E box-1 family is unclosed.

Forward pins:

```json
[
  {
    "role": "adoption",
    "id": "demo.package.track0d",
    "version": "v1"
  },
  {
    "role": "governance",
    "id": "demo.governance.track0d",
    "version": "v1"
  },
  {
    "role": "input",
    "id": "demo.finding.answer.no-employer-educational-assistance-interest.demo-stmt",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "demo.finding.answer.no-non-qualified-loan-component.demo-stmt",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "demo.finding.answer.no-qtp-earnings-used.demo-stmt",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "demo.finding.answer.no-qualified-employer-plan-interest.demo-stmt",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "demo.finding.answer.no-related-person-interest.demo-stmt",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "demo.finding.inclusion.demo-stmt.demo-loan",
    "version": "v1",
    "origin": "assertion"
  }
]
```

Status publications: yes, yes, yes, yes, yes. Status blocks: 0. Conclusions: plain-case-supported.

### closed-empty

Runners agree: True.
Forward line 21: published 0.
Reference line 21: published 0.
Presentation: disposition computed_zero, value 0, codes None.
Presentation text: Schedule 1 line 21 is blocked because eligibility authority is incomplete, an excluded class is present, the filer is married filing separately, or the Form 1098-E box-1 family is unclosed.

Forward pins:

```json
[
  {
    "role": "adoption",
    "id": "demo.package.track0d",
    "version": "v1"
  },
  {
    "role": "citation",
    "id": "tax.us.2025.citation.form1040.sli-worksheet",
    "version": "v1"
  },
  {
    "role": "citation",
    "id": "tax.us.2025.citation.schedule1.line-21",
    "version": "v1"
  },
  {
    "role": "computation",
    "id": "demo.rule.track1a4.worksheet",
    "version": "v1"
  },
  {
    "role": "governance",
    "id": "demo.governance.track0d",
    "version": "v1"
  },
  {
    "role": "input",
    "id": "f.sli.closure",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "package",
    "id": "tax.us.2025.f1098e.1",
    "version": "v1"
  },
  {
    "role": "package",
    "id": "tax.us.2025.mapping.f1098e.1",
    "version": "v1"
  }
]
```

Status publications: . Status blocks: 0. Conclusions: .

### nonempty-neither

Runners agree: True.
Forward line 21: blocked DEPENDENCY_INVALID missing [tax.us.2025.f1098e.box1-student-loan-interest|lender=demo-lender,statement=demo-stmt,tax-year=2025].
Reference line 21: blocked DEPENDENCY_INVALID missing [tax.us.2025.f1098e.box1-student-loan-interest|lender=demo-lender,statement=demo-stmt,tax-year=2025].
Presentation: disposition blocked, value None, codes ['DEPENDENCY_INVALID'].
Presentation text: Schedule 1 line 21 is blocked because eligibility authority is incomplete, an excluded class is present, the filer is married filing separately, or the Form 1098-E box-1 family is unclosed.

Forward pins:

```json
[
  {
    "role": "adoption",
    "id": "demo.package.track0d",
    "version": "v1"
  },
  {
    "role": "citation",
    "id": "tax.us.2025.citation.form1040.sli-worksheet",
    "version": "v1"
  },
  {
    "role": "citation",
    "id": "tax.us.2025.citation.schedule1.line-21",
    "version": "v1"
  },
  {
    "role": "governance",
    "id": "demo.governance.track0d",
    "version": "v1"
  },
  {
    "role": "input",
    "id": "demo.finding.box.demo-stmt",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "input",
    "id": "f.sli.closure",
    "version": "v1",
    "origin": "assertion"
  },
  {
    "role": "package",
    "id": "tax.us.2025.f1098e.1",
    "version": "v1"
  },
  {
    "role": "package",
    "id": "tax.us.2025.mapping.f1098e.1",
    "version": "v1"
  }
]
```

Status publications: . Status blocks: 5. Conclusions: not-supported.

## Item 5. Replacement text

The Foreman applies this. This run does not edit ADR 0077.

The text below replaces the current Part 3 and Part 4, from the Part 3 heading through the end of "Line 2b stays as it is", and stops before Part 5. Sentences that the run kept are still written out, so the replacement is the whole of those two parts.

What changed, and why:

- `reads_subject_results` is a list on the path, not one object on the rule. The old path names five status symbols. The new path names the statement conclusion. A rule-level wait would have made the new-only case wait on the five status publishers, which blocked in that run, or made the old-only case wait on the conclusion, which published `not-supported` in that run. Neither wait happened. New-only and old-only each published 2500.
- The symbols in that list stay out of `requires` and out of the declared path pins. The dollar cases did not block `DEPENDENCY_ABSENT` on those symbols. Each entry the path read is pinned role `input`, version `v2`, origin `derived`, id the derived finding id. Old-only carried five of those pins. New-only carried one. Both, closed-empty, and nonempty-neither carried none.
- Presence is decided from current sources before path `requires`. Both present blocked at once, missing `old-and-new-sli-inputs-both-present`, and pinned the five answer findings and the inclusion finding. It did not pin the derived status or conclusion findings, which had also been published in that same run.
- The default holds the closed-empty branch, because selection replaces top-level `value`. Closed-empty published 0. Presentation disposition was `computed_zero`. Nonempty with neither blocked `DEPENDENCY_INVALID`. `missing` was the box-1 fact id. No dollar was published.
- Path `requires` are the `ref` names in that path's value. Members of a `conditional_dependency_set`, the box-1 `count` name, and `reads_subject_results` symbols are not entries. Declared pins use those `requires` ids. `filing_status` is role `choice`, version `v1`, with no origin. The other declared pins are role `input`, version `v1`, origin `assertion`. The publication then pins the findings actually read, including parameter pins and the derived entry pins. One label, `assertion` / `v1` for every path pin, cannot say that.
- Old activity names `member_fact_types`, the five answer facts, and is active when any of them has a current source. New activity names the inclusion fact and no source family. The predicate is current sources of the named member. That split is what made old-only, new-only, both, and neither four different line 21 results.
- The five cases did not include a selected path whose subject-result entry was a block. The read still refuses a block entry. What the five cases showed is the favorable collect, the conflict that does not read entries, the default that does not read entries, and inactive-path blocks that do not become the worksheet's result.
- Origin `derived` is not in the published derived-finding pin enum. The probe recorded the pin and did not pass that finding through schema validation. The replacement allows that origin on these pins only. This run does not edit a schema.
- Line 2b, `rule-artifact.v9`, and `artifact-package.v30` stay as they are. This run's rule id is `demo.rule.track1a4.worksheet`. It did not block missing `v9-declarative-binding-unauthorized`.
- The person-visible blocked sentence is the generic line 21 sentence. Both and nonempty-neither presented `blocked`, `activeCodes` `DEPENDENCY_INVALID`, and that sentence. The missing token was not in the presentation text. Old-only and new-only presented `published_value` 2500. Closed-empty presented `computed_zero` 0.

### Replacement for Part 3 and Part 4

## Decision — Part 3. Same-run reading of per-subject results

**A path on a return-level rule declares the per-subject symbols it reads. The worksheet waits for the publishers of those symbols only when that path is the selected path. Both runners then see the same entries: one result for each current subject, and a block counts as that subject's result.** The reader refuses unless each current subject has exactly one result.

Track 0f item 2 is the defect the declared read removes. A return-level rule with no `requires` let the runners disagree about a collect of the conclusion symbol. The same rule with `requires` of that unsuffixed symbol made both runners block `DEPENDENCY_ABSENT`, including when the chain had published `plain-case-supported`. The keyed publication never fills the unsuffixed name.

`packages/derivation/subject_dispatch.py` builds the keyed symbol as `publishes` plus `|` plus the subject fact id. The per-subject block rows use that same symbol.

### Shape

`reads_subject_results` is a list. It is a field of a selection path, and of the default when the default reads any per-subject result. It is not a field of the rule. One object per symbol:

```json
{
  "reads_subject_results": [
    {
      "symbol": "<the per-subject rule's publishes>",
      "subject": {"id": "<subject fact type id>", "version": "vN"}
    }
  ]
}
```

`symbol` is the unsuffixed name the per-subject rule publishes. `subject` is the fact type that rule declares as its subject. The Track 1a-4 worksheet puts five objects on the old path, one for each answer-status symbol, and one object on the new path, for `demo.tax.track0d.statement-conclusion`. The subject on every object is `tax.us.2025.f1098e.box1-student-loan-interest`. The default's list is empty.

Changed from the previous Part 3: the field was one object on the rule, and it named one symbol. One object cannot name the five old-path symbols and the new-path symbol, and a rule-level list would be waited on for every presence outcome.

### Validation

- The rule has no `subject`. A rule with both `subject` and a path or default that carries `reads_subject_results` is rejected.
- Some rule in the package publishes `symbol` and declares `subject` as its subject fact type. The subject's id and version resolve on the package fact surface.
- The declaration does not make the unsuffixed symbol a `requires` entry of the rule or of the path. Putting that symbol in `requires` keeps today's behavior: both runners block `DEPENDENCY_ABSENT`.
- A symbol in `reads_subject_results` is not a declared path pin.

Changed from the previous Part 3: the exclusion from `requires` now covers the path as well as the rule, and the same symbols are excluded from declared path pins. Part 4's equality, below, states the same exclusion.

### Runtime

`runner._execute` and `reference_runner.run_reference` share eligibility and `attempt`. This read uses that shared path.

Presence is decided first, from current sources, by the Part 4 plan. Only then does the selected declaration contribute a wait:

- Conflict: do not wait for any path's publishers.
- Default, when its `reads_subject_results` is empty: do not wait for any per-subject publisher.
- One selected path: the rule becomes eligible when every ordinary `requires` name of that path is in `symbols`, and every rule that publishes a symbol in that path's `reads_subject_results` is in `resolved`. A predecessor that blocked is in `resolved`. If the package has no publisher for a declared symbol, do not wait. The other path's publishers are not a wait.

The rule is not eligible because the unsuffixed symbol is in `symbols`. The Track 1a-4 run is the measure. Old-only published 2500 while the same run's conclusion was `not-supported`. New-only published 2500 while the same run's five status rules were blocked. Both present blocked on the presence token and did not pin those derived findings.

After the wait, both runners expose the same entries for the current rows of the declared subject fact type:

- a publication whose symbol is `symbol|<subject fact id>`, or
- a block whose symbol is that same keyed symbol, when the per-subject rule blocked and published nothing for that subject.

A block is a result. It is not the absence of a result. Publication order may differ. Values, pins, and blocked rows may not.

Inside the selected path, a collect-family operator (`collect`, `count`, or `collect_categorical_all_equal`) whose `name` is one of that path's declared symbols reads exactly these entries, one per current subject, and nothing else. If any entry is a block, that operator refuses with `DEPENDENCY_INVALID` and lists the blocked subjects' fact ids in `missing`, sorted. It never skips the blocked entry, and never reads it as an empty or favorable value. A collect-family operator over `symbol` in a rule without this declaration keeps today's behavior.

An ordinary `requires` test, and a collect that does not go through this declaration, are unchanged. The item 2 split on an undeclared collect remains the behavior of that collect.

Changed from the previous Part 3: eligibility is per selected path, after presence, and conflict and the empty default do not wait. The previous text waited, for the whole rule, until every publisher of the one symbol had resolved.

### Coverage

The reader must be able to refuse unless each current subject has exactly one result. Exactly one means one publication or one block, not both and not neither.

- A subject with no publication and no block is missing. Block `DEPENDENCY_INVALID`. `missing` is those subject fact ids, sorted.
- A subject with two results is missing, same code, same list.
- A subject whose rule blocked and published nothing has one result, the block. The reader's own value then refuses a set that contains a block, or a value other than the one favorable value, with `DEPENDENCY_INVALID` and the missing token that value expression declares.

The old path's favorable value is `yes`. The new path's favorable value is `plain-case-supported`. The Track 1a-4 run measured the favorable side: five `yes` status publications on the old path, and one `plain-case-supported` conclusion on the new path, each producing line 21 `2500` on both runners. It did not measure a selected path whose entry was a block. Inactive-path blocks were present in the new-only run and were not the worksheet's result.

No new operator is required for the refusal itself. This part does not add `SLI_STATEMENT_COVERAGE` to the record enum. The disposition code is `DEPENDENCY_INVALID`. It does not change the worksheet's phase-out or limit arithmetic. The same 2500 cap the production worksheet publishes for one box of 3000 and total income 50000 is what old-only and new-only published.

Changed from the previous Part 3: `missing` names subject fact ids in every sentence. The previous coverage sentence said subject finding ids. The nonempty-neither result in this run named the box fact id `tax.us.2025.f1098e.box1-student-loan-interest|lender=demo-lender,statement=demo-stmt,tax-year=2025`.

### Pins

Each entry carries the pins the per-subject publication or block already recorded. The return-level finding pins each published entry it read: role `input`, id the derived finding id, version `v2`, origin `derived`. It does not copy the entry's inner pins onto itself. It does not invent a pin for a subject that has no result; that subject is named in `missing`.

Origin `derived` is allowed on these pins only. The published derived-finding pin enum remains `assertion` and `declared_default` until a schema version says otherwise. The Track 1a-4 probe recorded origin `derived` and did not submit that finding to the current schema check. Old-only's line 21 finding carried five such pins. New-only's carried one.

Changed from the previous Part 3: the previous pin sentence did not say the role, version, or origin of the pin that points at the derived finding. A derived result is not an `assertion` / `v1` input.

## Decision — Part 4. Presence selection beyond line 2b

**`exclusive_presence` / `refuse` is evaluated for every `rule-artifact.v13` rule that declares it and passes the validation below. The rule id is not an authorization list. Form 1040 line 2b version `v8` keeps the binding it has today.**

Track 0f item 3 cloned the worksheet onto `rule-artifact.v9`. Every presence case blocked `DEPENDENCY_INVALID`, missing `v9-declarative-binding-unauthorized`. The v9 clone stays unauthorized. This part is the v13 behavior. The Track 1a-4 run used rule id `demo.rule.track1a4.worksheet` and did not block on that v9 token.

For that declaration the four presence outcomes, plus the closed-empty outcome the default distinguishes, were:

- Old answers present, inclusion absent: old path, line 21 published 2500. Both runners agreed. Presentation disposition `published_value`.
- Inclusion present, the five answers absent: new path, line 21 published 2500. Both runners agreed. Presentation disposition `published_value`.
- Both present: no path value. Block `DEPENDENCY_INVALID`, missing `old-and-new-sli-inputs-both-present`. Presentation disposition `blocked`, `activeCodes` `["DEPENDENCY_INVALID"]`.
- No box, no answers, no inclusion: default, line 21 published 0. Presentation disposition `computed_zero`.
- A box present, no answers, no inclusion: default, no dollar. Block `DEPENDENCY_INVALID`, missing that box's fact id. Presentation disposition `blocked`, `activeCodes` `["DEPENDENCY_INVALID"]`.

### Shape

`selection` on `rule-artifact.v13` is the v9 selection object, copied forward, with the path fields this part adds. It is an alternative to top-level `value`: a rule has one of them, not both. v13 does not carry v9's `aggregation` object.

- `mode` is `exclusive_presence`. `conflict` is `refuse`. No other mode or conflict is valid.
- `paths` has at least two paths. Each path has an `id`, an `activity`, `reads_subject_results`, `requires`, `pins`, `when`, and `value`. The id matches the v9 pattern. The default object's `id` is `neither`. The default has the same fields.
- Activity is `source_nonempty` or `derived_activity`. `source_nonempty` names a member fact type, or `member_fact_types` when the path is active if any one of several members has a current source. `source_family` is present when the member belongs to an adopted family, and omitted when it does not. The runtime predicate is current sources of the named member, which is the predicate `source_nonempty` already uses. `derived_activity` names a fact type. The Track 1a-4 old path uses `member_fact_types` for the five answer facts and the statement family. The new path uses one member, `tax.us.2025.sli.statement-inclusion-relationship`, and no source family.
- `refusal.code` is `DEPENDENCY_INVALID`. `refusal.missing` is a non-empty list of unique strings.

Changed from the previous Part 4: activity was one `member_fact_type` plus a required source family. One member cannot name the five answers. The inclusion in this run has no adopted family. The path and the default gain `reads_subject_results`.

### Validation

For a v13 rule that declares `selection`:

- The rule has no `subject`. Top-level `when` is true. Top-level `requires` and `pins` are empty.
- Path ids are unique. The default id is `neither` and is not also a path id.
- Each activity's fact type resolves on the package fact surface. This checks resolution. It does not check that the ids are the nominee family or the nominee fact type.
- The names that are `requires` of a path are the `ref` names in that path's `when` and `value`, and any collect-family `name` that is not a symbol in that path's `reads_subject_results` and not the member name of a closed-family `count`. Names that appear only as members of a `conditional_dependency_set` are not `requires`. The default obeys the same rule. The Track 1a-4 default references the box-1 count and has empty `requires`.
- The path's declared pins are one pin per `requires` entry, same ids, same order. Role `choice` keeps version `v1` and has no origin. Every other declared pin is role `input`, version `v1`, origin `assertion`. Parameter ids are not `requires` and are not declared path pins. Symbols in `reads_subject_results` are not declared path pins.
- A path's `when` and `value` may use the ordinary expression operators, including `collect`, `count`, `block`, and `collect_categorical_all_equal`. Line 2b version `v8` keeps its own ban on dynamic dependency nodes inside a path. That ban is not copied here.

There is no list of authorized rule ids.

Changed from the previous Part 4: the previous equality said every name the path references is a `requires` entry, and every path pin is an `assertion` / `v1` input equal to that set. That equality cannot describe a derived per-subject collect, a choice, a parameter, a conditional member, or the closed-family count. The Track 1a-4 paths each declared 21 `requires`. The five status symbols and the conclusion symbol were not among them. `filing_status` was the choice pin. Closed-empty still published 0 with empty path `requires` on the default.

### Runtime

Both schedulers evaluate the declaration inside `attempt`, so they share one plan. The plan kinds are the ones line 2b already returns: `conflict`, `path`, or `default`. Activity is decided from current sources before any path's `requires` are consulted. An inactive path's publishers do not block the selected path.

- **One active path.** Wait as Part 3 says. Evaluate that path's `when`, then its `value`. A false `when` is inapplicable. A block raised by the value is that block. Do not evaluate the other path or the default.
- **No active path.** Evaluate the default the same way. Do not wait for a path's publishers.
- **More than one active path.** Evaluate no path value and do not wait for either path's publishers. Block `DEPENDENCY_INVALID` with the rule's `refusal.missing`. Pin the current source findings that made each active path true.

The Track 1a-4 conflict disposition pinned six findings, role `input`, version `v1`, origin `assertion`: the five answer findings and the inclusion finding, plus adoption and governance. It did not pin a path value.

The default value in that declaration is a `count` of box 1 compared with 0. The `then` branch is 0. The `else` branch blocks `DEPENDENCY_INVALID` and `missing` is the current subject fact ids, sorted. Closed-empty took `then`. Nonempty-neither took `else`.

Changed from the previous Part 4: the previous runtime waited on the selected path's `requires` and treated every named symbol the same way. It had no separate wait for per-subject publishers, and it had no way to avoid waiting on the inactive path. The closed-empty branch was not on the default.

### Pins

The selected path's publication pins what that path's expression read, plus the rule and adoption pins an ordinary publication carries. A derived entry read through `reads_subject_results` is pinned as Part 3 says: role `input`, version `v2`, origin `derived`, id the derived finding id. A ref to an ordinary derived symbol keeps the pin that symbol already has. In this run the line-1 subtotal pin was role `input`, version `v2`, origin `assertion`. Parameter reads are parameter pins. A choice input keeps role `choice`.

A conflict pins the activity evidence and does not pin a path value that was not evaluated. A contract failure before the plan runs blocks `DEPENDENCY_INVALID`. The missing token is the existing one for that failure: `declarative-top-level-contract-invalid`, `selection-path-id-duplicate`, or `selection-path-pin-contract-invalid`. This part does not add a record code for them.

Changed from the previous Part 4: publication pins are not the declared path-pin set. The declared set identifies dependencies by symbol. The publication identifies the findings that were read, and a derived per-subject entry uses origin `derived`.

### Line 2b stays as it is

`tax.us.2025.rule.form1040-line2b` version `v8`, schema `rule-artifact.v9`, keeps its id gate, its path ids `legacy` and `new`, its activity checks, its dynamic-dependency ban, and its refusal token `legacy-and-derived-nominee-both-present`. Its bytes are not edited. `rule-artifact.v9` and `artifact-package.v30` are not edited. A v9 rule that is not that citizen and that carries `selection` still fails package validation with `RULE_SELECTION_UNAUTHORIZED` and, if it is run, still blocks with missing `v9-declarative-binding-unauthorized`. v9 `aggregation` stays authorized only for `tax.us.2025.rule.interest.derived-nominee-subtotal` version `v1`.

The Track 1a-4 worksheet is a disposable v13 declaration, rule id `demo.rule.track1a4.worksheet`. It is not a rewrite of the v9 clone and not a loosening of the v8 checks.

This part does not change the person-visible line 21 sentence. Blocked cases in this run showed that generic sentence and `DEPENDENCY_INVALID`. They did not show the missing token. Published 2500 showed disposition `published_value`. Closed-empty showed `computed_zero`.
