"""Scratch pytest plugin for the gain-break-even P0 census (evidence only; never in tests/).

Wraps packages.derivation.live.live_coordinate_run for one pytest session and
appends, per live run that carries a sale, the sale path, term, column (h),
the core version adopted, the calling test file:line and the outcome, to
$GBE_CENSUS_OUT.<pid>.jsonl. Run (from the repository root):

  GBE_CENSUS_OUT=<scratch>/rec PYTHONPATH=<this directory> \
    python3 -m pytest -p gbe_census_plugin -n 9 -p no:cacheprovider <test files>

then python3 census.py <scratch>/rec to write census.json.
"""
from __future__ import annotations

import functools
import inspect
import json
import os
import re

OUT = os.environ["GBE_CENSUS_OUT"]
FAM = re.compile(r"^tax\.us\.2025\.(f1099b\.(covered|covered-w|noncovered|code-b|covered-ltcg)(-(st|lt))?|f8949\.no1099b-(st|lt))$")


def _f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _col_h(fam, s):
    p, b = _f(s.get("proceeds")), _f(s.get("basis"))
    if "covered-w" in fam:
        return p - b + _f(s.get("box_1g_wash_sale_disallowed_amount"))
    if "code-b" in fam:
        c = s.get("corrected_basis", s.get("basis"))
        return p - _f(c) + _f(s.get("wash_disallowed"))
    if fam.endswith("covered-st") or fam.endswith("covered-lt") or "covered-ltcg" in fam:
        return p - b
    return p - b + _f(s.get("wash_disallowed"))


def _sales(acts):
    found = {}
    for a in acts:
        if a.get("kind") != "member-transition":
            continue
        pl = a.get("payload") or {}
        fam = str((pl.get("family") or {}).get("id"))
        if not FAM.match(fam):
            continue
        m = pl.get("member") or {}
        if m.get("action") == "remove":
            found.pop(str(m.get("fact_id")), None)
        elif m.get("action") == "assert":
            fi = m["finding"]
            v = fi.get("value")
            if isinstance(v, dict):
                found[str(fi["fact_id"])] = (fam.removeprefix("tax.us.2025."), v)
    out = []
    for fam, v in found.values():
        out.append({"family": fam, "h": _col_h(fam, v), "proceeds": _f(v.get("proceeds")), "basis": _f(v.get("basis")),
                    "lt": v.get("long_term")})
    return out


def _version(acts):
    ver = None
    for a in acts:
        pkg = (a.get("payload") or {}).get("package") if isinstance(a.get("payload"), dict) else None
        if isinstance(pkg, dict) and str(pkg.get("id", "")).endswith("core-calculations"):
            ver = pkg.get("version")
    return ver


def _caller():
    frames = []
    for fr in inspect.stack()[2:40]:
        fn = fr.filename
        if "/tests/" in fn or "/docs/" in fn:
            rel = fn.split("/tests/", 1)[-1] if "/tests/" in fn else fn.split("/docs/", 1)[-1]
            prefix = "tests/" if "/tests/" in fn else "docs/"
            frames.append(f"{prefix}{rel}:{fr.lineno}")
    return frames


def pytest_configure(config):
    import packages.derivation.live as live

    original = live.live_coordinate_run
    if getattr(original, "_gbe", False):
        return

    @functools.wraps(original)
    def wrapped(*args, **kwargs):
        acts = kwargs.get("authoritative_acts") or []
        sales = _sales(acts)
        rec = {"test": os.environ.get("PYTEST_CURRENT_TEST", "").split(" (")[0], "caller": _caller(),
               "core": _version(acts), "sales": sales}
        try:
            outcome = original(*args, **kwargs)
        except Exception as exc:
            rec["error"] = type(exc).__name__
            if sales:
                _write(rec)
            raise
        if sales:
            try:
                if outcome.refusal is not None:
                    rec["refusal"] = str(outcome.refusal.reason)
                else:
                    report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
                    rec["stop"] = report.get("stop_reason")
                    pubs = {}
                    for p in outcome.publications or ():
                        s = str(p.finding.get("symbol")).removeprefix("tax.us.2025.")
                        if s.startswith("schedule-d.line-") or s in ("form1040.line-7a", "form1040.line-16"):
                            pubs[s] = p.finding.get("value")
                    rec["pubs"] = pubs
                    rec["blocked"] = sorted({str(r.get("artifact_id")).removeprefix("tax.us.2025.rule.")
                                             for r in report.get("dispositions") or []
                                             if r.get("disposition") == "blocked"
                                             and re.search(r"schedule-d|8949|f1099b|line7a|preferential", str(r.get("artifact_id")))})
            except Exception as exc:  # noqa: BLE001
                rec["observe_error"] = repr(exc)[:200]
            _write(rec)
        return outcome

    wrapped._gbe = True
    live.live_coordinate_run = wrapped


def _write(rec):
    with open(f"{OUT}.{os.getpid()}.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, default=str) + "\n")
