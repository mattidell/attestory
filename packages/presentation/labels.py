"""Text shared by the saved-page projector and its observer."""

from unicodedata import category


def has_sale_label_text(label: object) -> bool:
    """Whether a label contains a character besides whitespace or format controls."""
    return isinstance(label, str) and any(
        not char.isspace() and category(char) != "Cf" for char in label
    )
