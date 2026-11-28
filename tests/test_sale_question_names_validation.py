"""Runtime shape checks for display-only sale reasons."""

from typing import Any

import pytest

from packages.derivation.presentation_projection import PresentationModelError, _validate_resolved


@pytest.mark.parametrize("extra", [
    {"saleLabel": ""}, {"saleLabel": "\ufeff"}, {"saleLabel": "\u034f"}, {"saleLabel": "\u0301"}, {"saleLabel": "\u115f"}, {"saleLabel": "\u2003\u200b"}, {"saleLabel": " \t"}, {"saleLabel": 123}, {"saleLabel": None},
    {"saleLabel": "demo name", "factId": "demo.fact"},
    {"saleLabel": "demo name", "memberLabel": "demo member"},
    {"saleLabel": "demo name", "statementLabel": {"statement": "demo statement", "taxYear": "2025"}},
])
def test_invalid_sale_reason_shape_is_rejected(extra: dict[str, Any]) -> None:
    resolved = {
        "disposition": "blocked", "activeCodes": [], "act": None,
        "reasons": [{"sentence": "Demo question?", **extra}],
    }
    with pytest.raises(PresentationModelError, match="saleLabel"):
        _validate_resolved(resolved, "$.resolved")


def test_sale_label_cannot_appear_on_an_inapplicable_line() -> None:
    resolved = {
        "disposition": "guard_inapplicable", "act": None,
        "reasons": [{"sentence": "Demo question?", "saleLabel": "demo name"}],
    }
    with pytest.raises(PresentationModelError, match="reasons"):
        _validate_resolved(resolved, "$.resolved")
