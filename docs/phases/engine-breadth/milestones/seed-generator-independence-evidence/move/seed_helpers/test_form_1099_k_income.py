"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

import copy
from packages.derivation.production_resolver import PublicationSurface
from seed_helpers.test_form_1099_withholding import USER
from seed_helpers.test_form_1099_withholding import YEAR
from seed_helpers.test_refund_or_amount_owed_track1 import _act
from seed_helpers.test_refund_or_amount_owed_track1 import _attested

def _handover(
    finished: list[dict[str, object]], *, surface: PublicationSurface, reconfirm: bool
) -> list[dict[str, object]]:
    """Hands the Social Security chain over against ``surface``.

    The v59 helper pins its own surface. A v60 adoption is not in that registry,
    so the successor run resolves the family version on the surface that publishes it.
    """
    from packages.derivation.loader import DerivationSchemas
    from packages.tax.loader import (
        install_domain_companion_equalities,
        install_domain_companion_presence,
        install_domain_declaration_signal_contradictions,
    )
    from packages.tax.ssa_family_handover import ssa_family_version_for_acts, stage_ssa_family_handover

    registry = DerivationSchemas().registry
    install_domain_companion_presence(registry)
    install_domain_companion_equalities(registry)
    install_domain_declaration_signal_contradictions(registry)
    version = ssa_family_version_for_acts(finished, actor=USER, surface=surface)
    act, _unused = stage_ssa_family_handover(
        finished, registry, actor=USER, at="2026-10-28T12:00:00Z", family_version=version
    )
    out = copy.deepcopy(finished) + [act]
    if reconfirm:
        horizon = act["payload"]["successor"]["horizon_id"]
        closure = _act(
            len(out),
            "assertion",
            {"finding": _attested(
                "demo.fk.ssa.reconfirm",
                f"tax.us.2025.ssa1099.source-closure|family-horizon={horizon},tax-year={YEAR}",
                True,
            )},
        )
        closure["actor"] = USER
        out.append(closure)
    return out
