"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

import seed_helpers.test_w2g_gambling as w2g

def base_return() -> list[dict[str, object]]:
    """A complete return on the latest core with no statement of any family.

    Single filer, wages 50,000 and 4,500 withheld on one W-2, standard deduction, no
    dependents; every closure and absence answer the latest core asks is given, so a run
    publishes the bottom line (Form 1040 line 34) with no blocked rule.
    Asserts: ``test_base_return_publishes_with_nothing_blocked``.
    """
    return w2g._w2g_return([])
