"""P0 probe — senior-and-dependent-deductions (investigation only, no
production edit).

Runs one synthetic single-filer return, aged 65 or older, with W-2 wages
only, through the real coordinator (``live_coordinate_run``) against the
adopted production package (core-calculations v50) and records today's
Form 1040 lines 11, 12e, 13b, 14 and 15 as published symbols. This is a
*real-path observation*, not a design proposal: it shows what the current
content already does with the existing ``taxpayer_over_65`` assertion, which
today's line 13b and line 12e content still cannot read (see
``p0-law-and-path.md``).

Reuses the ``tax-on-taxable-income`` P0 probe's act-log builder and the
Track 1 test's ``_finish_v50`` / ``_age`` helpers (same shape, loaded
dynamically to avoid importing a test module from content code) rather than
re-deriving a v50-shaped act log from scratch.

This script writes its JSON output under ``temp/`` only (git-ignored); the
script itself is committed as the evidence trail's probe. Run from the
repository root:

    python3 docs/phases/engine-breadth/milestones/senior-and-dependent-deductions-evidence/probe.py

All facts are synthetic (``demo.*`` ids). No absolute paths are written to
any committed file.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.production_resolver import PublicationSurface  # noqa: E402

CONTENT = REPO / "packages" / "content" / "tax" / "2025"
RELEASE_DIR = (
    REPO
    / "packages"
    / "sample_data"
    / "student_loan_worksheet_integration"
    / "publication_surface"
    / "releases"
)
PACKAGE_V50 = CONTENT / "package.core-calculations.v50.json"
REGISTRY_V48 = CONTENT / "published-packages.v48.json"
RELEASE_V48 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v48.json"
SURFACE_V50 = PublicationSurface(RELEASE_DIR, REGISTRY_V48, CONTENT)

OUT_DIR = REPO / "temp" / "senior-and-dependent-deductions"

TOTI_PROBE_PATH = (
    REPO
    / "docs"
    / "phases"
    / "engine-breadth"
    / "milestones"
    / "tax-on-taxable-income-evidence"
    / "probe.py"
)

_SYMBOLS = {
    "line-11_agi": "tax.us.2025.income.agi",
    "line-12e_standard-or-itemized": "tax.us.2025.deductions.line-12e",
    "line-13b_schedule-1a": "tax.us.2025.deductions.schedule-1a",
    "line-14_total-deductions": "tax.us.2025.deductions.line-14",
    "line-15_taxable-income": "tax.us.2025.income.taxable-income",
}


def _load_toti_probe() -> Any:
    spec = importlib.util.spec_from_file_location("sdd_p0_toti_probe", TOTI_PROBE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load the tax-on-taxable-income P0 probe helpers")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _finish_v50(toti: Any, acts: list[dict[str, object]], note: str) -> list[dict[str, object]]:
    pkg = json.loads(PACKAGE_V50.read_text(encoding="utf-8"))
    rel_csum = hashlib.sha256(RELEASE_V48.read_bytes()).hexdigest()
    built = copy.deepcopy(acts)
    adoption = copy.deepcopy(toti._load_fixture_adoption())
    adoption["act_id"] = f"demo.sddprobe.adopt.{len(built):03d}"
    payload = adoption["payload"]
    assert isinstance(payload, dict)
    payload["package"] = {
        "id": "tax.us.2025.package.core-calculations",
        "version": "v50",
        "checksum": pkg["package_checksum"],
    }
    payload["release"] = {
        "id": "demo.release.sli-worksheet-integration.2025",
        "version": "v48",
        "checksum": rel_csum,
    }
    payload["audit"] = {"note": note}
    built.append(adoption)
    for index, row in enumerate(built):
        row["committed_against"] = index
        row["actor"] = toti.USER
    return built


def _age_over_65(toti: Any, acts: list[dict[str, object]]) -> list[dict[str, object]]:
    built = copy.deepcopy(acts)
    built.append(
        toti._act(
            len(built),
            "assertion",
            {
                "finding": toti._attested(
                    "demo.sddprobe.taxpayer-over-65",
                    "tax.us.2025.taxpayer-over-65|tax-year=2025",
                    True,
                )
            },
        )
    )
    return built


def _run(toti: Any, acts: list[dict[str, object]], run_id: str) -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=REPO,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=toti.USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=SURFACE_V50,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            return {"refusal": {"reason": outcome.refusal.reason, "detail": outcome.refusal.detail}}
        pubs: dict[str, Any] = {}
        for pub in outcome.publications or ():
            pubs[str(pub.finding["symbol"])] = pub.finding
        blocked: list[dict[str, Any]] = []
        if outcome.output_path is not None:
            report = cast(dict[str, Any], json.loads(outcome.output_path.read_text("utf-8")))
            for row in report.get("dispositions", []):
                if row.get("disposition") == "blocked":
                    blocked.append(row)
        return {"publications": pubs, "blocked": blocked}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    toti = _load_toti_probe()

    # Single filer, aged 65+ (taxpayer_over_65 asserted true), $50,000 of W-2
    # wages only — the smallest real-path observation that exercises today's
    # line 12e / 13b content with the senior-age assertion already on
    # record.
    acts = toti._base_acts(wages=50000.0, filing_status="single")
    acts = _age_over_65(toti, acts)
    acts = _finish_v50(
        toti, acts, "P0 probe: single, 65+, $50,000 W-2 wages only, core-calculations v50"
    )
    result = _run(toti, acts, "demo.sddprobe.case1")

    lines: dict[str, Any] = {}
    if "refusal" in result:
        lines["_refusal"] = result["refusal"]
    else:
        pubs = result["publications"]
        for label, symbol in _SYMBOLS.items():
            finding = pubs.get(symbol)
            if finding is not None:
                lines[label] = {"value": finding.get("value"), "disposition": "published"}
                continue
            blocked_row = next(
                (b for b in result["blocked"] if symbol in str(b.get("artifact_id", ""))),
                None,
            )
            lines[label] = {
                "value": None,
                "disposition": "blocked" if blocked_row is not None else "absent",
                "blocked_detail": blocked_row,
            }

    out = {
        "case": "single, taxpayer_over_65=true, $50,000 W-2 wages only",
        "lines": lines,
        "notes": (
            "Today's tax.us.2025.rule.form1040-line13b requires"
            " tax.us.2025.schedule1a.no-additional-deductions-declared == 'yes'"
            " and otherwise blocks; it never reads taxpayer_over_65 or"
            " computes Schedule 1-A Part V, so line 13b here is either the"
            " mandatory zero (if the absence assertion is answered 'yes', as"
            " this probe's base act log does) or DEPENDENCY_ABSENT/blocked"
            " (if unanswered) — never the $6,000 the 2025 law would allow"
            " for this case. See p0-law-and-path.md Sec. 3-4 for the full"
            " trace and change list."
        ),
    }
    out_path = OUT_DIR / "probe-output.json"
    out_path.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps(out, indent=2, default=str))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
