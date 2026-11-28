"""Text shared by the saved-page projector and its observer."""

import re
from unicodedata import category, normalize

# Unicode Default_Ignorable_Code_Point. Python's unicodedata exposes general
# categories only. The page uses the corresponding Unicode property escape.
_DEFAULT_IGNORABLE = re.compile(
    "[\u00ad\u034f\u061c\u115f-\u1160\u17b4-\u17b5\u180b-\u180f"
    "\u200b-\u200f\u202a-\u202e\u2060-\u206f\u3164\ufe00-\ufe0f"
    "\ufeff\uffa0\ufff0-\ufff8\U0001bca0-\U0001bca3\U0001d173-\U0001d17a"
    "\U000e0000-\U000e0fff]"
)


def sale_label_key(label: object) -> str:
    """Normalize visible sale labels for comparison, returning empty for blank labels."""
    if not isinstance(label, str):
        return ""
    visible = "".join(char for char in _DEFAULT_IGNORABLE.sub("", label) if category(char) != "Cf")
    canonical = normalize("NFC", visible)
    if not any(not char.isspace() and category(char)[0] not in {"M", "C"} for char in canonical):
        return ""
    return " ".join(canonical.casefold().split())


def has_sale_label_text(label: object) -> bool:
    return bool(sale_label_key(label))
