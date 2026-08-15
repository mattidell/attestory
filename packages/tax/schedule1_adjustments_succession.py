"""Schedule 1 Part II absence succession — T0-1 predecessor and successor ids.

The thirteen predecessor ids are the milestone's predecessor population.
The thirteen successor ids are the Schedule-1-native replacements. This
module is the shared table for package admission, content generation, and
tests. It is not a lattice mechanism and not an individuation map.
"""

from __future__ import annotations

PREDECESSOR_PREFIX = "tax.us.2025.ss-benefits-scope."
SUCCESSOR_PREFIX = "tax.us.2025.schedule1-adjustments-scope."

# T0-1 table, in the charter's numbered order.
PREDECESSOR_TOKENS: tuple[str, ...] = (
    "no-schedule1-line24z-writein",
    "no-sch1-line11-educator",
    "no-sch1-line12-business-expenses",
    "no-sch1-line13-hsa",
    "no-sch1-line14-moving",
    "no-sch1-line15-deductible-se",
    "no-sch1-line16-se-retirement",
    "no-sch1-line17-se-health",
    "no-sch1-line18-penalty",
    "no-sch1-line19-alimony-paid",
    "no-sch1-line20-ira-deduction",
    "no-sch1-line23-archer-msa",
    "no-sch1-line25-other-adjustments",
)

SUCCESSOR_TOKENS: tuple[str, ...] = (
    "no-line24z-writein",
    "no-line11-educator",
    "no-line12-business-expenses",
    "no-line13-hsa",
    "no-line14-moving",
    "no-line15-deductible-se",
    "no-line16-se-retirement",
    "no-line17-se-health",
    "no-line18-penalty",
    "no-line19-alimony-paid",
    "no-line20-ira-deduction",
    "no-line23-archer-msa",
    "no-line25-other-adjustments",
)

SUCCESSOR_TITLES: tuple[str, ...] = (
    "Schedule 1 line 24z write-in adjustment is not present for tax year 2025. Contributed categorical assertion, domain {yes, no}, no default. yes asserts the named class is absent; no asserts it is present.",
    "Schedule 1 line 11 educator expenses adjustment is not present for tax year 2025. Contributed categorical assertion, domain {yes, no}, no default. yes asserts the named class is absent; no asserts it is present.",
    "Schedule 1 line 12 certain business expenses of reservists, performing artists, and fee-basis government officials is not present for tax year 2025. Contributed categorical assertion, domain {yes, no}, no default. yes asserts the named class is absent; no asserts it is present.",
    "Schedule 1 line 13 health savings account deduction is not present for tax year 2025. Contributed categorical assertion, domain {yes, no}, no default. yes asserts the named class is absent; no asserts it is present.",
    "Schedule 1 line 14 moving expenses for members of the Armed Forces is not present for tax year 2025. Contributed categorical assertion, domain {yes, no}, no default. yes asserts the named class is absent; no asserts it is present.",
    "Schedule 1 line 15 deductible part of self-employment tax is not present for tax year 2025. Contributed categorical assertion, domain {yes, no}, no default. yes asserts the named class is absent; no asserts it is present.",
    "Schedule 1 line 16 self-employed SEP, SIMPLE, and qualified plans is not present for tax year 2025. Contributed categorical assertion, domain {yes, no}, no default. yes asserts the named class is absent; no asserts it is present.",
    "Schedule 1 line 17 self-employed health insurance deduction is not present for tax year 2025. Contributed categorical assertion, domain {yes, no}, no default. yes asserts the named class is absent; no asserts it is present.",
    "Schedule 1 line 18 penalty on early withdrawal of savings is not present for tax year 2025. Contributed categorical assertion, domain {yes, no}, no default. yes asserts the named class is absent; no asserts it is present.",
    "Schedule 1 line 19 alimony paid is not present for tax year 2025. Contributed categorical assertion, domain {yes, no}, no default. yes asserts the named class is absent; no asserts it is present.",
    "Schedule 1 line 20 IRA deduction is not present for tax year 2025. Contributed categorical assertion, domain {yes, no}, no default. yes asserts the named class is absent; no asserts it is present.",
    "Schedule 1 line 23 Archer MSA deduction is not present for tax year 2025. Contributed categorical assertion, domain {yes, no}, no default. yes asserts the named class is absent; no asserts it is present.",
    "Schedule 1 line 25 other adjustments is not present for tax year 2025. Contributed categorical assertion, domain {yes, no}, no default. yes asserts the named class is absent; no asserts it is present.",
)

PREDECESSOR_IDS: tuple[str, ...] = tuple(PREDECESSOR_PREFIX + token for token in PREDECESSOR_TOKENS)
SUCCESSOR_IDS: tuple[str, ...] = tuple(SUCCESSOR_PREFIX + token for token in SUCCESSOR_TOKENS)
PAIRS: tuple[tuple[str, str], ...] = tuple(zip(PREDECESSOR_IDS, SUCCESSOR_IDS, strict=True))

MIGRATION_ID = "tax.us.2025.schedule1-adjustments-scope.succession"
MIGRATION_VERSION = "v1"
SUCCESSOR_BUNDLE_ID = "tax.us.2025.schedule1-adjustments-scope.vocabulary"
SUCCESSOR_BUNDLE_VERSION = "v1"

NO_RRB_ID = "tax.us.2025.ss-benefits-scope.no-rrb-or-foreign-social-benefit"

# The other nine ss-benefits-scope members that are not this migration's
# predecessors (T0-1 / T0-2). Including any of them in a predecessor list
# is rejected by package admission for this succession.
NON_SCHEDULE1_SCOPE_IDS: tuple[str, ...] = (
    "tax.us.2025.ss-benefits-scope.no-unsupported-line1-entries",
    "tax.us.2025.ss-benefits-scope.no-pension-annuity-line5b",
    "tax.us.2025.ss-benefits-scope.no-traditional-ira-deduction",
    "tax.us.2025.ss-benefits-scope.no-form-2555",
    "tax.us.2025.ss-benefits-scope.no-form-4563",
    "tax.us.2025.ss-benefits-scope.no-form-8815",
    "tax.us.2025.ss-benefits-scope.no-excluded-adoption-benefits",
    "tax.us.2025.ss-benefits-scope.no-puerto-rico-or-samoa-income",
    "tax.us.2025.ss-benefits-scope.no-lump-sum-election",
    NO_RRB_ID,
)

LINE21_STANDIN_ID = "tax.us.2025.schedule1-adjustments-scope.line21-student-loan-interest-standin"
