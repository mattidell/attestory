# Federal Field Coverage (2025)

## Summary

- Fields in scope: 7
- Directly populated: 4
- Requires computation: 2
- Missing required source data: 0
- Optional not populated: 1

## irs.2025.f1040

| Field | Status | Value | Source |
| --- | --- | --- | --- |
| `irs.2025.f1040.line1a`<br>Form 1040 line 1a wages | Direct | $82,500.00 | Demo W-2: Acme Robotics, field 1: Wages, tips, other compensation (`w2.box1.wages`) |
| `irs.2025.f1040.line25a`<br>Form 1040 line 25a federal income tax withheld from Forms W-2 | Direct | $11,400.00 | Demo W-2: Acme Robotics, field 2: Federal income tax withheld (`w2.box2.federal_income_tax_withheld`) |
| `irs.2025.f1040.line25b`<br>Form 1040 line 25b federal income tax withheld from Forms 1099 | Optional |  |  |
| `irs.2025.f1040.line2b`<br>Form 1040 line 2b taxable interest | Computed |  |  |

## irs.2025.f1040sb

| Field | Status | Value | Source |
| --- | --- | --- | --- |
| `irs.2025.f1040sb.part_i.interest_payers.payer_name`<br>Schedule B Part I interest payer name | Direct | Example Bank | Demo 1099-INT: Example Bank, field payer: Payer name (`1099_int.payer.name`) |
| `irs.2025.f1040sb.part_i.interest_payers.interest_amount`<br>Schedule B Part I interest amount | Direct | $432.10 | Demo 1099-INT: Example Bank, field 1: Interest income (`1099_int.box1.interest_income`) |
| `irs.2025.f1040sb.line4`<br>Schedule B line 4 total interest | Computed |  |  |
