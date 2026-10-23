"""P0 probe -- refund-or-amount-owed (investigation only, no production edit).

Runs one synthetic single-filer, W-2-only return through the real coordinator
(``live_coordinate_run``) against the adopted production package
(core-calculations v51) and records today's Form 1040 lines 11, 15, 16 and 22
as published symbols, plus every other publication the run produces, so P0
can see exactly where the return stops today (see ``p0-law-and-path.md``
Sec. 5).

Reuses the senior-and-dependent-deductions Track 1 test's own act-log
builder (``_senior_acts``, with every optional feature left at its
no-senior/no-dependent default) and its ``_finish_v51`` / ``_run`` helpers
(same shape as that milestone's own P0 probe) rather than re-deriving a
v51-shaped act log from scratch. That builder itself is built on the
tax-on-taxable-income P0 probe's ``_base_acts``, which already closes every
family needed to reach Form 1040 line 22 (tax after nonrefundable credits),
including the direct-foreign-tax-credit scope absences for Schedule 2
line 17 and the child tax credit (line 19).

This script writes its JSON output under ``temp/`` only (git-ignored); the
script itself is committed as the evidence trail's probe. Run from the
repository root:

    python3 docs/phases/engine-breadth/milestones/refund-or-amount-owed-evidence/probe.py

All facts are synthetic (``demo.*`` ids). No absolute paths are written to
any committed file.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

OUT_DIR = REPO / "temp" / "refund-or-amount-owed"

SDD_TRACK1_PATH = REPO / "tests" / "test_senior_and_dependent_deductions_track1.py"

_SYMBOLS = {
    "line-11_agi": "tax.us.2025.income.agi",
    "line-15_taxable-income": "tax.us.2025.income.taxable-income",
    "line-16_tax": "tax.us.2025.tax.total-tax",
    "line-22_tax-after-nonrefundable-credits": "tax.us.2025.tax.after-nonrefundable-credits",
}


def _load_sdd_track1() -> Any:
    spec = importlib.util.spec_from_file_location("roao_p0_sdd_track1", SDD_TRACK1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load the senior-and-dependent-deductions Track 1 helpers")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _elect_direct_ftc(sdd: Any, acts: list[dict[str, object]]) -> list[dict[str, object]]:
    """``_base_acts`` asserts ``tax.us.2025.direct-ftc.election = "no"``, which
    this fact type's own title (`f1099div-box7.bundle.json`) says "declines
    [the direct credit] and blocks" it -- by design, not a defect. With no
    foreign tax at all (box 7 closed empty, subtotal $0), the return needing
    line 22 published must instead elect "yes" (electing with a $0 box-7
    subtotal correctly computes a $0 credit). This appends a superseding
    elective finding (free supersession) rather than editing the base
    builder, which other tests share unmodified."""
    toti = sdd.toti._probe()
    built = list(acts)
    built.append(
        toti._act(
            len(built),
            "assertion",
            {
                "finding": toti._elective(
                    "demo.roaoprobe.direct-ftc.election",
                    "tax.us.2025.direct-ftc.election|tax-year=2025",
                    "yes",
                )
            },
        )
    )
    return built


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sdd = _load_sdd_track1()

    # Single filer, $50,000 of W-2 wages only; no senior deduction, no
    # dependent worksheet, no itemizing -- the plan's own "W-2 only, single"
    # case, left at every optional feature's default so today's content runs
    # exactly as it would for an ordinary return.
    acts = sdd._senior_acts(wages=50000.0, filing_status="single")
    acts = _elect_direct_ftc(sdd, acts)
    acts = sdd._finish_v51(
        acts, "P0 probe: single, $50,000 W-2 wages only, core-calculations v51"
    )
    pubs, blocked = sdd._run(acts, "demo.roaoprobe.case1")

    lines: dict[str, Any] = {}
    for label, symbol in _SYMBOLS.items():
        finding = pubs.get(symbol)
        if finding is not None:
            lines[label] = {"value": finding.get("value"), "disposition": "published"}
            continue
        blocked_row = next(
            (b for b in blocked if symbol in str(b.get("artifact_id", ""))),
            None,
        )
        lines[label] = {
            "value": None,
            "disposition": "blocked" if blocked_row is not None else "absent",
            "blocked_detail": blocked_row,
        }

    out = {
        "case": "single, $50,000 W-2 wages only, no senior/dependent/itemized features",
        "lines": lines,
        "all_publications": sorted(pubs.keys()),
        "all_blocked": blocked,
        "notes": (
            "The base builder's own direct-ftc.election = 'no' default"
            " blocks line 22 entirely (that fact's title: 'no declines"
            " [the direct credit] and blocks' it, by design, not a"
            " defect) even with zero foreign tax; this probe supersedes"
            " it to 'yes' (a $0 box-7 subtotal then correctly computes a"
            " $0 credit) to reach a published line 22. With that in"
            " place: AGI $50,000, taxable income $34,250, tax (line 16)"
            " $3,875, tax after nonrefundable credits (line 22) $3,875 --"
            " and nothing further. Of the 145 symbols this run publishes,"
            " none names line 23, line 24, any of lines 25a-25d (including"
            " tax.us.2025.f1099k.box4-federal-withholding, which DOES"
            " publish $0 from the closed-empty 1099-K family but reaches"
            " no payments line), line 26, lines 27-32, or lines 33-38."
            " See p0-law-and-path.md Sec. 1-2 for the law and the"
            " per-document withholding inventory, and Sec. 7 for the"
            " change list this leaves for Track 1/2."
        ),
    }
    out_path = OUT_DIR / "probe-output.json"
    out_path.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps(out, indent=2, default=str))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
