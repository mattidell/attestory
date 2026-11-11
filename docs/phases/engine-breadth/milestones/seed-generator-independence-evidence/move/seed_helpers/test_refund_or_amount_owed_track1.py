"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

from seed_helpers.repo_root import repo_root

import copy
import hashlib
import json
from pathlib import Path
from typing import Any
from typing import cast

ROOT = repo_root()

CONTENT = ROOT / "packages" / "content" / "tax" / "2025"

USER = "demo.user.filer-1"

SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

def _sdd() -> Any:
    import seed_helpers.test_senior_and_dependent_deductions_track1 as module
    return module

def _toti_probe() -> Any:
    return _sdd().toti._probe()

def _act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    probe = _toti_probe()
    return cast(dict[str, object], probe._act(index, kind, payload))

def _attested(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    probe = _toti_probe()
    return cast(dict[str, object], probe._attested(finding_id, fact_id, value))

def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))

def _finish(
    acts: list[dict[str, object]],
    *,
    package_path: Path,
    package_version: str,
    release_path: Path,
    release_version: str,
    note: str,
) -> list[dict[str, object]]:
    pkg = json.loads(package_path.read_text(encoding="utf-8"))
    rel_csum = hashlib.sha256(release_path.read_bytes()).hexdigest()
    built = copy.deepcopy(acts)
    adoption = copy.deepcopy(_toti_probe()._load_fixture_adoption())
    adoption["act_id"] = f"demo.roaot1.adopt.{len(built):03d}"
    payload = adoption["payload"]
    assert isinstance(payload, dict)
    payload["package"] = {
        "id": "tax.us.2025.package.core-calculations",
        "version": package_version,
        "checksum": pkg["package_checksum"],
    }
    payload["release"] = {
        "id": "demo.release.sli-worksheet-integration.2025",
        "version": release_version,
        "checksum": rel_csum,
    }
    payload["audit"] = {"note": note}
    built.append(adoption)
    for index, row in enumerate(built):
        row["committed_against"] = index
        row["actor"] = USER
    return built

def _close_empty(acts: list[dict[str, object]], *, family: str, version: str, closure_fact: str, horizon: str) -> None:
    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("horizon-genesis", {"family": {"id": family, "version": version}, "scope": SCOPE_KEY, "horizon_id": horizon})
    add("assertion", {"finding": _attested(f"demo.roaot1.closure.{horizon}", f"{closure_fact}|family-horizon={horizon},tax-year=2025", True)})

_BOX4_FAMILIES = {
    "w2-box2": (("w2.bundle.v3.json", "w2-box2.bundle.json"), "", "", ""),
    "f1099int-b4": ("f1099int-box4.bundle.json", "tax.us.2025.f1099int.b4", "v1", "tax.us.2025.f1099int.b4.source-closure"),
    "f1099div-b4": ("f1099div-box4.bundle.json", "tax.us.2025.f1099div.b4", "v1", "tax.us.2025.f1099div.b4.source-closure"),
    "f1099r-b4": ("f1099r-ira.bundle.v3.json", "tax.us.2025.f1099r.box4", "v1", "tax.us.2025.f1099r.box4.source-closure"),
    # Form 1099-K box 4 is a Track 1 stop-condition finding, not built (see
    # rule.form1040-line25b.json's own notes): it stays recorded and summed
    # nowhere, same as P0 found it. Line 25b therefore sums three document
    # subtotals, not four.
}

def _close_other_box4_families(acts: list[dict[str, object]], *, skip: set[str]) -> None:
    """Adopts and closes-empty every box-2/box-4 withholding family except
    the ones named in ``skip``, so line 25b (which requires all four 1099
    document subtotals) and line 25d resolve in a standalone test that only
    populates one document. ``w2-box2`` closes both the box-1 and box-2
    W-2 families empty together (0 == 0), since line 25a v2 requires their
    counts to match."""

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    for key, (bundle_names, family, version, closure_fact) in _BOX4_FAMILIES.items():
        if key in skip:
            continue
        names = bundle_names if isinstance(bundle_names, tuple) else (bundle_names,)
        for name in names:
            add("bundle-adoption", {"bundle": _load(name)})
        if key == "w2-box2":
            _close_w2_box1_and_box2(acts, horizon_suffix=str(len(acts)))
        else:
            _close_empty(acts, family=family, version=version, closure_fact=closure_fact, horizon=f"demo.roaot1.{key}.{len(acts)}")
