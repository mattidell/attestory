"""Track 8: presentation goldens for the Form 1098-E / Student Loan Interest
Deduction / AGI milestone.

Three genuinely distinct disposition paths, re-run live against the real
production surface Track 6 wired (``package.core-calculations.v33`` /
``published-packages.v28`` / release ``demo.release.2025.v26``), asserting
byte-for-byte match against committed goldens -- the same
``tools.generate_schedule_d_presentation_t3_goldens`` /
``tests.test_schedule_d_presentation_t3`` evidentiary pattern this corpus
already established (see also
``tests.test_capital_gain_distributions_line7a_t3_presentation``'s
``ProductionShapedGoldens`` class).

Proves the presentation layer is deterministic and demoable for this
milestone, not merely "it ran once": regenerating twice in-process is
byte-identical, and the committed goldens on disk match a fresh live run.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any

from packages.derivation.presentation_projection import validate_presentation_model
from tools import generate_f1098e_track8_presentation_goldens as goldens

SECTIONS = ("line-10", "line-11a", "line-11b", "line-sch1-21")


def _sections_by_id(model: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {s["id"]: s for s in model["sections"]}


class ProductionShapedGoldens(unittest.TestCase):
    def test_regeneration_is_deterministic_and_matches_committed_goldens(self) -> None:
        first = goldens.regenerate()
        second = goldens.regenerate()
        self.assertEqual(first, second)
        for name, model in first.items():
            committed = json.loads((goldens.GOLDEN_DIR / f"{name}.presentation-model.v1.json").read_text("utf-8"))
            self.assertEqual(committed, model)
            validate_presentation_model(committed)

    def test_every_model_binds_all_four_form_field_symbols_exactly_once(self) -> None:
        models = goldens.regenerate()
        for name, model in models.items():
            seen = [s["id"] for s in model["sections"]]
            for section_id in SECTIONS:
                self.assertEqual(seen.count(section_id), 1, (name, section_id, seen))


class BelowFloorFullDeduction(unittest.TestCase):
    """Path (b): single statement, full eligibility, MAGI below the phaseout
    floor. Full $2,500-capped deduction publishes; AGI reflects it."""

    def test_full_capped_deduction_flows_through_to_agi(self) -> None:
        models = goldens.regenerate()
        sections = _sections_by_id(models["below-floor"])
        self.assertEqual(sections["line-sch1-21"]["resolved"]["disposition"], "published_value")
        self.assertEqual(sections["line-sch1-21"]["resolved"]["value"], 2500)
        self.assertEqual(sections["line-10"]["resolved"]["value"], 2500)
        self.assertEqual(sections["line-11a"]["resolved"]["disposition"], "published_value")
        self.assertEqual(sections["line-11b"]["resolved"]["value"], sections["line-11a"]["resolved"]["value"])
        attachments = {a["id"]: a for a in models["below-floor"]["attachments"]}
        self.assertEqual(
            attachments["tax.us.2025.rule.attachment.schedule-1"]["resolved"]["disposition"], "published"
        )


class ClosedEmptyComputedZero(unittest.TestCase):
    """Path (a): closed family, zero current members. Line 21 is a
    closure-backed computed zero, never a fabricated positive value."""

    def test_closed_empty_family_is_closure_backed_zero(self) -> None:
        models = goldens.regenerate()
        sections = _sections_by_id(models["closed-empty"])
        self.assertEqual(sections["line-sch1-21"]["resolved"]["disposition"], "closure_backed_zero")
        self.assertEqual(sections["line-sch1-21"]["resolved"]["value"], 0)
        self.assertEqual(sections["line-10"]["resolved"]["value"], 0)
        self.assertEqual(sections["line-11a"]["resolved"]["disposition"], "published_value")


class UniversalComponentViolationBlocks(unittest.TestCase):
    """Path (f): a universal eligibility witness answers "no". The whole
    route blocks with SLI_UNIVERSAL_COMPONENT_VIOLATION, never a silent
    zero and never a silent full-box-1 pass-through."""

    def test_related_person_interest_blocks_line21_and_downstream(self) -> None:
        models = goldens.regenerate()
        sections = _sections_by_id(models["universal-violation"])
        self.assertEqual(sections["line-sch1-21"]["resolved"]["disposition"], "blocked")
        self.assertEqual(sections["line-sch1-21"]["resolved"]["activeCodes"], ["SLI_UNIVERSAL_COMPONENT_VIOLATION"])
        # Downstream lines (10, 11a, 11b) redact rather than fabricate an AGI
        # that omits the disqualified statement's own interest -- their own
        # dependency is absent because line 21/26 never published.
        self.assertEqual(sections["line-10"]["resolved"]["disposition"], "blocked")
        self.assertEqual(sections["line-10"]["resolved"]["activeCodes"], ["DEPENDENCY_ABSENT"])


if __name__ == "__main__":
    unittest.main()
