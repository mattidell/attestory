"""Core v79 runs the Track 0 rerun cases through the real coordinator.

Each case is the act list the rerun built. v79 is package
core-calculations v79, registry v77, and release v77. The nine current-core
returns are also run on pinned core v78, with no noncovered answer, and their
Form 1040 line 15 and line 16 dollars are the same ones v79 publishes under
one no. Cores through v78 stay off the refusal map in the switch tests.

Drives live_coordinate_run. The live marker is derived from that name.
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/noncovered-sales-evidence"
QUESTION = "Did you sell any securities whose basis was not reported to the IRS?"
REFUSAL = "BASIS_NOT_REPORTED_ON_COVERED"
REFUSAL_SENTENCE = (
    "Record this sale as a noncovered sale. The broker did not report its basis to the IRS."
)
WASH_SENTENCE = "A wash-sale disallowance is recorded on a sale that is not a loss."
# Lines 2 and 9 select closure_backed_zero under a "yes" with no member of that
# term as well as under a "no", and block for an unanswered, stale or
# conflicting answer, a refused in-class boundary, or a failed sale check.
LINE_EXPLAINS = {
    "schedule-d.line-2": {
        "closure_backed_zero": (
            "Schedule D line 2, column (h), is zero. No short-term sale whose basis was not "
            "reported to the IRS is recorded, and your answer about those sales confirms the list is complete."
        ),
        "blocked": (
            "Schedule D line 2, column (h), has no value yet. It waits for your answers about sales "
            "whose basis was not reported to the IRS, or for a recorded short-term sale of that kind "
            "to pass its checks."
        ),
    },
    "schedule-d.line-9": {
        "closure_backed_zero": (
            "Schedule D line 9, column (h), is zero. No long-term sale whose basis was not "
            "reported to the IRS is recorded, and your answer about those sales confirms the list is complete."
        ),
        "blocked": (
            "Schedule D line 9, column (h), has no value yet. It waits for your answers about sales "
            "whose basis was not reported to the IRS, or for a recorded long-term sale of that kind "
            "to pass its checks."
        ),
    },
}
RETIRED_EXPLAINS = ("You said you have no", "waiting for the basis of")
QUESTION_CASES = {
    "boundary_no_with_member",
    "late_member_unclosed",
    "late_yes_stale",
    "wage_unclosed",
    "yes_then_no_with_member",
}
REFUSAL_CASES = {
    "covered_both_boundaries_no",
    "covered_flag_corrected_to_no",
    "covered_flag_no_path_a",
    "covered_flag_no_st",
    "covered_flag_no_w_lt",
    "covered_flag_no_w_st",
}
NINE = (
    "wage",
    "foreign_tax",
    "exempt_interest",
    "exempt_dividend",
    "student_loan",
    "gambling_loss",
    "mortgage",
    "itemized",
    "part_ii_b",
)

EXPECTED = json.loads(r"""
{
  "v79": {
    "boundary_no_with_member": {
      "lines": {
        "form1040.line-15": [
          "blocked",
          null
        ],
        "form1040.line-16": [
          "blocked",
          null
        ],
        "form1040.line-7a": [
          "blocked",
          null
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "blocked",
          null
        ],
        "schedule-d.line-15": [
          "blocked",
          null
        ],
        "schedule-d.line-16": [
          "blocked",
          null
        ],
        "schedule-d.line-21": [
          "blocked",
          null
        ]
      },
      "attachments": {
        "f8949": "blocked",
        "schedule-d": "blocked"
      },
      "error": null
    },
    "boundary_no_without_member": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "code_w_on_gain": {
      "lines": {
        "form1040.line-15": [
          "blocked",
          null
        ],
        "form1040.line-16": [
          "blocked",
          null
        ],
        "form1040.line-7a": [
          "blocked",
          null
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "blocked",
          null
        ],
        "schedule-d.line-15": [
          "blocked",
          null
        ],
        "schedule-d.line-16": [
          "blocked",
          null
        ],
        "schedule-d.line-21": [
          "blocked",
          null
        ]
      },
      "attachments": {
        "f8949": "blocked",
        "schedule-d": "blocked"
      },
      "error": null
    },
    "covered_both_boundaries_no": {
      "lines": {
        "form1040.line-15": [
          "blocked",
          null
        ],
        "form1040.line-16": [
          "blocked",
          null
        ],
        "form1040.line-7a": [
          "blocked",
          null
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "blocked",
          null
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "blocked",
          null
        ],
        "schedule-d.line-16": [
          "blocked",
          null
        ],
        "schedule-d.line-21": [
          "blocked",
          null
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "blocked"
      },
      "error": null
    },
    "covered_flag_corrected_to_no": {
      "lines": {
        "form1040.line-15": [
          "blocked",
          null
        ],
        "form1040.line-16": [
          "blocked",
          null
        ],
        "form1040.line-7a": [
          "blocked",
          null
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "blocked",
          null
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "blocked",
          null
        ],
        "schedule-d.line-16": [
          "blocked",
          null
        ],
        "schedule-d.line-21": [
          "blocked",
          null
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "blocked"
      },
      "error": null
    },
    "covered_flag_corrected_to_yes": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          38250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "published_value",
          4000
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "published_value",
          4000
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "published_value",
          4000
        ],
        "schedule-d.line-16": [
          "published_value",
          4000
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "published"
      },
      "error": null
    },
    "covered_flag_no_path_a": {
      "lines": {
        "form1040.line-15": [
          "blocked",
          null
        ],
        "form1040.line-16": [
          "blocked",
          null
        ],
        "form1040.line-7a": [
          "blocked",
          null
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "blocked",
          null
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "blocked",
          null
        ],
        "schedule-d.line-16": [
          "blocked",
          null
        ],
        "schedule-d.line-21": [
          "blocked",
          null
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "blocked"
      },
      "error": null
    },
    "covered_flag_no_st": {
      "lines": {
        "form1040.line-15": [
          "blocked",
          null
        ],
        "form1040.line-16": [
          "blocked",
          null
        ],
        "form1040.line-7a": [
          "blocked",
          null
        ],
        "schedule-d.line-1a": [
          "blocked",
          null
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "blocked",
          null
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "blocked",
          null
        ],
        "schedule-d.line-21": [
          "blocked",
          null
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "blocked"
      },
      "error": null
    },
    "covered_flag_no_w_lt": {
      "lines": {
        "form1040.line-15": [
          "blocked",
          null
        ],
        "form1040.line-16": [
          "blocked",
          null
        ],
        "form1040.line-7a": [
          "blocked",
          null
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "blocked",
          null
        ],
        "schedule-d.line-16": [
          "blocked",
          null
        ],
        "schedule-d.line-21": [
          "blocked",
          null
        ]
      },
      "attachments": {
        "f8949": "blocked",
        "schedule-d": "blocked"
      },
      "error": null
    },
    "covered_flag_no_w_st": {
      "lines": {
        "form1040.line-15": [
          "blocked",
          null
        ],
        "form1040.line-16": [
          "blocked",
          null
        ],
        "form1040.line-7a": [
          "blocked",
          null
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "blocked",
          null
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "blocked",
          null
        ],
        "schedule-d.line-21": [
          "blocked",
          null
        ]
      },
      "attachments": {
        "f8949": "blocked",
        "schedule-d": "blocked"
      },
      "error": null
    },
    "covered_flag_yes": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          38250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "published_value",
          4000
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "published_value",
          4000
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "published_value",
          4000
        ],
        "schedule-d.line-16": [
          "published_value",
          4000
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "published"
      },
      "error": null
    },
    "duplicate_horizon": {
      "lines": {},
      "attachments": {},
      "error": "HorizonModelError"
    },
    "late_member_reopened": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          38250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "published_value",
          4000
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "published_value",
          4000
        ],
        "schedule-d.line-15": [
          "published_value",
          4000
        ],
        "schedule-d.line-16": [
          "published_value",
          4000
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "published",
        "schedule-d": "published"
      },
      "error": null
    },
    "late_member_unclosed": {
      "lines": {
        "form1040.line-15": [
          "blocked",
          null
        ],
        "form1040.line-16": [
          "blocked",
          null
        ],
        "form1040.line-7a": [
          "blocked",
          null
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "blocked",
          null
        ],
        "schedule-d.line-15": [
          "blocked",
          null
        ],
        "schedule-d.line-16": [
          "blocked",
          null
        ],
        "schedule-d.line-21": [
          "blocked",
          null
        ]
      },
      "attachments": {
        "f8949": "blocked",
        "schedule-d": "blocked"
      },
      "error": null
    },
    "late_yes_reanswered": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          38250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "published_value",
          4000
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "published_value",
          4000
        ],
        "schedule-d.line-15": [
          "published_value",
          4000
        ],
        "schedule-d.line-16": [
          "published_value",
          4000
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "published",
        "schedule-d": "published"
      },
      "error": null
    },
    "late_yes_stale": {
      "lines": {
        "form1040.line-15": [
          "blocked",
          null
        ],
        "form1040.line-16": [
          "blocked",
          null
        ],
        "form1040.line-7a": [
          "blocked",
          null
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "blocked",
          null
        ],
        "schedule-d.line-15": [
          "blocked",
          null
        ],
        "schedule-d.line-16": [
          "blocked",
          null
        ],
        "schedule-d.line-21": [
          "blocked",
          null
        ]
      },
      "attachments": {
        "f8949": "blocked",
        "schedule-d": "blocked"
      },
      "error": null
    },
    "lt_gain": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          38250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "published_value",
          4000
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "published_value",
          4000
        ],
        "schedule-d.line-15": [
          "published_value",
          4000
        ],
        "schedule-d.line-16": [
          "published_value",
          4000
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "published",
        "schedule-d": "published"
      },
      "error": null
    },
    "one_exempt_dividend": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "one_exempt_interest": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "one_finding": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "one_foreign_tax": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34350
        ],
        "form1040.line-16": [
          "published_value",
          3887
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "one_gambling_loss": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "one_itemized": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "one_mortgage": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "one_part_ii_b": {
      "lines": {
        "form1040.line-15": [
          "computed_zero",
          0
        ],
        "form1040.line-16": [
          "computed_zero",
          0
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "one_student_loan": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34050
        ],
        "form1040.line-16": [
          "published_value",
          3851
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "one_wage": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "st_loss": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          31250
        ],
        "form1040.line-16": [
          "published_value",
          3515
        ],
        "form1040.line-7a": [
          "published_value",
          -3000
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "published_value",
          -6000
        ],
        "schedule-d.line-7": [
          "published_value",
          -6000
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "published_value",
          -6000
        ],
        "schedule-d.line-21": [
          "published_value",
          3000
        ]
      },
      "attachments": {
        "f8949": "published",
        "schedule-d": "published"
      },
      "error": null
    },
    "wage_unclosed": {
      "lines": {
        "form1040.line-15": [
          "blocked",
          null
        ],
        "form1040.line-16": [
          "blocked",
          null
        ],
        "form1040.line-7a": [
          "blocked",
          null
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "blocked",
          null
        ],
        "schedule-d.line-7": [
          "blocked",
          null
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "blocked",
          null
        ],
        "schedule-d.line-15": [
          "blocked",
          null
        ],
        "schedule-d.line-16": [
          "blocked",
          null
        ],
        "schedule-d.line-21": [
          "blocked",
          null
        ]
      },
      "attachments": {
        "f8949": "blocked",
        "schedule-d": "blocked"
      },
      "error": null
    },
    "wash": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          32250
        ],
        "form1040.line-16": [
          "published_value",
          3635
        ],
        "form1040.line-7a": [
          "published_value",
          -2000
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "published_value",
          -2000
        ],
        "schedule-d.line-15": [
          "published_value",
          -2000
        ],
        "schedule-d.line-16": [
          "published_value",
          -2000
        ],
        "schedule-d.line-21": [
          "published_value",
          2000
        ]
      },
      "attachments": {
        "f8949": "published",
        "schedule-d": "published"
      },
      "error": null
    },
    "yes_then_no_with_member": {
      "lines": {
        "form1040.line-15": [
          "blocked",
          null
        ],
        "form1040.line-16": [
          "blocked",
          null
        ],
        "form1040.line-7a": [
          "blocked",
          null
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-2": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-9": [
          "blocked",
          null
        ],
        "schedule-d.line-15": [
          "blocked",
          null
        ],
        "schedule-d.line-16": [
          "blocked",
          null
        ],
        "schedule-d.line-21": [
          "blocked",
          null
        ]
      },
      "attachments": {
        "f8949": "blocked",
        "schedule-d": "blocked"
      },
      "error": null
    }
  },
  "v78": {
    "covered_flag_no_path_a": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          38250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "published_value",
          4000
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "published_value",
          4000
        ],
        "schedule-d.line-15": [
          "published_value",
          4000
        ],
        "schedule-d.line-16": [
          "published_value",
          4000
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "published"
      },
      "error": null
    },
    "exempt_dividend": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "exempt_interest": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "foreign_tax": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34350
        ],
        "form1040.line-16": [
          "published_value",
          3887
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "gambling_loss": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "itemized": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "mortgage": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "part_ii_b": {
      "lines": {
        "form1040.line-15": [
          "computed_zero",
          0
        ],
        "form1040.line-16": [
          "computed_zero",
          0
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "student_loan": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34050
        ],
        "form1040.line-16": [
          "published_value",
          3851
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    },
    "wage": {
      "lines": {
        "form1040.line-15": [
          "published_value",
          34250
        ],
        "form1040.line-16": [
          "published_value",
          3875
        ],
        "form1040.line-7a": [
          "computed_zero",
          0
        ],
        "schedule-d.line-1a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-8a": [
          "closure_backed_zero",
          0
        ],
        "schedule-d.line-15": [
          "computed_zero",
          0
        ],
        "schedule-d.line-16": [
          "computed_zero",
          0
        ],
        "schedule-d.line-21": [
          "computed_zero",
          0
        ],
        "schedule-d.line-7": [
          "computed_zero",
          0
        ]
      },
      "attachments": {
        "f8949": "guard_inapplicable",
        "schedule-d": "guard_inapplicable"
      },
      "error": null
    }
  }
}
""")


def _install(world: SimpleNamespace) -> None:
    proto = world.proto
    content = world.probe.CONTENT
    if proto.BUILT.get("families"):
        return
    proto.USE_V2 = True
    bundles = {
        key: json.loads((content / name).read_text(encoding="utf-8"))
        for key, name in (
            ("st", "f1099b-noncovered-st.bundle.json"),
            ("lt", "f1099b-noncovered-lt.bundle.json"),
            ("boundary", "schedule-d-boundary-noncovered.bundle.json"),
        )
    }
    facts = {
        fact["id"]: fact
        for bundle in bundles.values()
        for fact in bundle["fact_types"]
    }
    families = []
    member_of = {}
    for path in sorted(content.glob("family.f1099b-noncovered-*.json")):
        body = json.loads(path.read_text(encoding="utf-8"))
        families.append(body["id"])
        member_of[body["id"]] = body["member_predicate"]["fact_type"]
    proto.BUILT.clear()
    proto.BUILT.update({
        "bundles": bundles,
        "facts": facts,
        "families": families,
        "member_of": member_of,
    })


@pytest.fixture(scope="module")
def world() -> SimpleNamespace:
    sys.path.insert(0, str(EVIDENCE))
    p0b = cast(Any, importlib.import_module("p0b"))
    probe = cast(Any, importlib.import_module("probe"))
    proto = cast(Any, importlib.import_module("prototype"))
    track0 = cast(Any, importlib.import_module("track0"))

    loaded = SimpleNamespace(p0b=p0b, probe=probe, proto=proto, track0=track0)
    _install(loaded)
    cases = p0b._cases()
    cases.pop("_part_ii_b_build_error", None)
    neighbors = p0b._neighbors()
    neighbors.pop("_part_ii_b_build_error", None)
    loaded.cases = cases
    loaded.neighbors = neighbors
    return loaded


def _pin(probe: Any, version: str) -> None:
    if version == "v79":
        probe.PACKAGE = "package.core-calculations.v79.json"
        probe.PACKAGE_VERSION = "v79"
        probe.REGISTRY = "published-packages.v77.json"
        probe.RELEASE = "demo.release.sli-worksheet-integration.2025.v77.json"
        probe.RELEASE_VERSION = "v77"
    else:
        probe.PACKAGE = "package.core-calculations.v78.json"
        probe.PACKAGE_VERSION = "v78"
        probe.REGISTRY = "published-packages.v76.json"
        probe.RELEASE = "demo.release.sli-worksheet-integration.2025.v76.json"
        probe.RELEASE_VERSION = "v76"


def _line_map(result: dict[str, Any]) -> dict[str, list[Any]]:
    found: dict[str, list[Any]] = {}
    for row in result.get("lines") or []:
        citizen = str(row.get("id") or "")
        short = citizen.removeprefix("tax.us.2025.")
        if short in {
            "form1040.line-15", "form1040.line-16", "form1040.line-7a",
            "schedule-d.line-1a", "schedule-d.line-2", "schedule-d.line-7", "schedule-d.line-8a",
            "schedule-d.line-9", "schedule-d.line-15", "schedule-d.line-16",
            "schedule-d.line-21",
        }:
            value = row.get("value")
            if isinstance(value, float) and value.is_integer():
                value = int(value)
            found[short] = [row.get("disposition"), value]
    return found


def _attachments(result: dict[str, Any]) -> dict[str, str]:
    found: dict[str, str] = {}
    for row in result.get("attachments") or []:
        name = str(row.get("id") or "").split(".")[-1]
        if name in {"f8949", "schedule-d"}:
            found[name] = row.get("disposition")
    return found


def _explains(result: dict[str, Any]) -> dict[str, tuple[Any, Any]]:
    found: dict[str, tuple[Any, Any]] = {}
    for row in result.get("lines") or []:
        short = str(row.get("id") or "").removeprefix("tax.us.2025.")
        if short in LINE_EXPLAINS:
            found[short] = (row.get("disposition"), row.get("explain"))
    return found


def _sentences(result: dict[str, Any]) -> list[str]:
    found: list[str] = []
    for row in result.get("lines") or []:
        found.extend(str(reason) for reason in (row.get("reasons") or []))
    return found


@pytest.mark.parametrize("name", sorted(EXPECTED["v79"]))
def test_v79_matches_the_track0_rerun(world: SimpleNamespace, name: str) -> None:
    _pin(world.probe, "v79")
    result = world.track0._execute(world.cases[name], f"demo.ns.t1.v79.{name}")
    expected = EXPECTED["v79"][name]
    if expected["error"] == "HorizonModelError":
        assert result.get("error") == "HorizonModelError"
        assert result.get("horizon_refused") is True
        assert "demo.ns.p0b.shared.h0" in str(result.get("message"))
        return
    assert result.get("error") is None, result.get("message")
    assert result.get("presentation_valid") is True
    assert result.get("stop_reason") == "saturated"
    assert _line_map(result) == expected["lines"]
    assert _attachments(result) == expected["attachments"]
    sentences = _sentences(result)
    if name in QUESTION_CASES:
        assert any(QUESTION in sentence for sentence in sentences)
    if name in REFUSAL_CASES:
        assert any(REFUSAL in (row.get("missing") or []) for row in (result.get("blocked") or []))
        assert any(REFUSAL_SENTENCE in sentence for sentence in sentences)
    if name == "code_w_on_gain":
        assert any(WASH_SENTENCE in sentence for sentence in sentences)
    for field, (disposition, explain) in _explains(result).items():
        assert not any(retired in str(explain) for retired in RETIRED_EXPLAINS), (field, explain)
        if disposition in LINE_EXPLAINS[field]:
            assert explain == LINE_EXPLAINS[field][disposition], (field, disposition)
    if name == "lt_gain":
        # A "yes" with no short-term member: the zero must not claim a denial.
        assert _explains(result)["schedule-d.line-2"][0] == "closure_backed_zero"
    if name in {"lt_gain", "st_loss", "wash"}:
        # A pure box B or box E return attaches Schedule D.
        assert _attachments(result)["schedule-d"] == "published"
    if name == "one_wage":
        # One "no" on a wage return: no Schedule D, as on v78.
        assert _attachments(result)["schedule-d"] == "guard_inapplicable"



@pytest.mark.parametrize("name", list(NINE) + ["covered_flag_no_path_a"])
def test_v78_pinned_returns_keep_their_dollars(world: SimpleNamespace, name: str) -> None:
    from tests.helpers import current_core_returns as ccr

    _pin(world.probe, "v78")
    if name == "covered_flag_no_path_a":
        acts = world.probe.direct(ccr.base_return(), "lt", 6000.0, 2000.0, "v78flag")
    else:
        acts = ccr._renumbered(world.neighbors[name])
    result = world.track0._execute(acts, f"demo.ns.t1.v78.{name}")
    assert result.get("error") is None, result.get("message")
    assert result.get("presentation_valid") is True
    assert _line_map(result) == EXPECTED["v78"][name]["lines"]
    assert _attachments(result) == EXPECTED["v78"][name]["attachments"]
    if name != "covered_flag_no_path_a":
        v79_lines = EXPECTED["v79"]["one_" + name]["lines"]
        for field in ("form1040.line-15", "form1040.line-16"):
            assert _line_map(result)[field] == v79_lines[field]


def test_expectation_table_covers_every_rerun_case() -> None:
    assert set(EXPECTED["v79"]) >= set(QUESTION_CASES) | set(REFUSAL_CASES) | {"code_w_on_gain", "duplicate_horizon"}
    assert len(EXPECTED["v79"]) == 31
    assert len(NINE) == 9
