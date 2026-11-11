"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

import json
from typing import Any
from typing import cast
from packages.tax.loader import TAX_CONTENT_DIR

CONTENT = TAX_CONTENT_DIR

SLI_SCOPE_UNIVERSAL_TOKENS = (
    "no-form-2555",
    "no-form-4563",
    "no-puerto-rico-or-samoa-income",
)

SLI_SCOPE_LEGAL_ZERO_TOKENS = (
    "not-claimed-as-dependent",
    "legally-obligated-for-interest",
)

SCHED1_LINE_TOKENS = (
    "no-line11-educator", "no-line12-business-expenses", "no-line13-hsa",
    "no-line14-moving", "no-line15-deductible-se", "no-line16-se-retirement",
    "no-line17-se-health", "no-line18-penalty", "no-line19-alimony-paid",
    "no-line20-ira-deduction", "no-line23-archer-msa", "no-line25-other-adjustments",
)

def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))
