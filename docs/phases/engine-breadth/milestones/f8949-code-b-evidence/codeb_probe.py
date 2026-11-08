"""What core v80 does with a Form 1099-B sale whose reported basis is wrong (code B).

P0 evidence for docs/phases/engine-breadth/milestones/f8949-code-b.md.
Synthetic demo.* findings on the harness wage return. Reads production
content (package core-calculations v80, registry v78, release v78). Reuses
the f8949-boxes-cf evidence harness (track0, and through it cf_prototype and
cf_probe), loaded under a unique module name, exactly as tests/test_no1099b_sales_v80.py does. Writes
codeb-probe-output.json beside this file. Does not edit packages/.

    python3 docs/phases/engine-breadth/milestones/f8949-code-b-evidence/codeb_probe.py [case ...]

Core v80 has no family for a sale with code B. A filer with a covered sale
whose broker basis is wrong can put it in one of four places, and each is
measured: the line 1a/8a direct families with the broker's basis or the
corrected basis, the box A/D code W families, or the box B/E families. A
box B/E sale with code B (basis shown but not reported, and wrong) is
measured on the box B/E families with the correct basis.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
CF_EVIDENCE = HERE.parent / "f8949-boxes-cf-evidence"
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(CF_EVIDENCE))
OUT = HERE / "codeb-probe-output.json"
Acts = list[dict[str, Any]]


def load(name: str, path: Path) -> Any:
    """Load an evidence module under a unique name (f8949-boxes-cf retrospective)."""
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# track0 imports cf_prototype (and through it cf_probe and the noncovered-sales
# helpers); tests/test_no1099b_sales_v80.py loads it under this same name.
track0: Any = load("f8949_boxes_cf_track0", CF_EVIDENCE / "track0.py")
cfp = track0.cfp
cp = cfp.cp
probe, proto = cp.probe, cp.proto
P = cfp.P

from tests.helpers import current_core_returns as ccr  # noqa: E402

WATCH_LINES = ("1a", "1b", "2", "3", "7", "8a", "8b", "9", "10", "15", "16", "21")
cp.WATCH = tuple(P + f"schedule-d.line-{n}" for n in WATCH_LINES) + tuple(
    P + f"form1040.line-{n}" for n in ("7a", "15", "16"))
cp.TEXT_LINES = tuple(P + f"schedule-d.line-{n}" for n in ("1b", "2", "8b", "9"))
# The rows that say why a line blocks: (disposition, code, missing).
WHY_ROWS = tuple(P + "rule." + name for name in (
    "schedule-d-line1a-gain", "schedule-d-line1b", "schedule-d-line2", "schedule-d-line8a-gain",
    "schedule-d-line8b", "schedule-d-line9", "selected-preferential-base", "form1040-line7a",
    "attachment.f8949", "attachment.schedule-d",
))


def pin_v80() -> None:
    """The published v80 and the published vocabularies, as the v80 test pins them."""
    cp.pin_v79()
    cp.install_v79_noncovered()
    cfp.pin("v80")
    content = cp.probe.CONTENT
    for key, name in (
        ("st", "f8949-no1099b-st.bundle.json"),
        ("lt", "f8949-no1099b-lt.bundle.json"),
        ("boundary", "schedule-d-boundary-form8949-in-class.bundle.json"),
        ("nc_check", "f1099b-noncovered-amounts-check.bundle.json"),
    ):
        cfp.BUNDLES[key] = json.loads((content / name).read_text(encoding="utf-8"))


# ---- sale builders on the v80 families ------------------------------------


def direct(acts: Acts, term: str, proceeds: float, basis: float, tag: str) -> Acts:
    """A sale on the line 1a (st) or 8a (lt) direct-report families: box A/D, no Form 8949."""
    sale = probe.txn(proceeds=proceeds, basis=basis, long_term="yes" if term == "lt" else "no",
                     reported="yes", covered="yes")
    acts = probe.record(acts, P + f"f1099b.covered-{term}", sale, tag)
    acts = probe.record(acts, P + f"f1099b.covered-{term}-proceeds", proceeds, tag + "p")
    return probe.record(acts, P + f"f1099b.covered-{term}-basis", basis, tag + "b")


def wash(acts: Acts, term: str, proceeds: float, basis: float, adjustment: float, tag: str) -> Acts:
    """A sale on the box A (st) or D (lt) code W families: lines 1b and 8b."""
    sale = probe.txn(proceeds=proceeds, basis=basis, long_term="yes" if term == "lt" else "no",
                     wash=adjustment, reported="yes", covered="yes")
    acts = probe.record(acts, P + f"f1099b.covered-w-{term}", sale, tag + "o")
    acts = probe.record(acts, P + f"f1099b.covered-w-{term}-proceeds", proceeds, tag + "p")
    acts = probe.record(acts, P + f"f1099b.covered-w-{term}-basis", basis, tag + "b")
    return probe.record(acts, P + f"f1099b.covered-w-{term}-adjustment", adjustment, tag + "a")


def noncovered(term: str, proceeds: float, basis: float, tag: str) -> Callable[[Acts], None]:
    """A sale on the box B (st) or E (lt) families with the filer's basis."""
    return lambda acts: cp.on_be(acts, term, proceeds, basis, tag)


def after(fn: Callable[[Acts], Acts]) -> Callable[[Acts], Acts]:
    """A sales callback that renumbers first (the v80 harness opens families in place)."""
    return lambda acts: fn(ccr._renumbered(acts))


# Answer sets. ``honest`` is how a filer with a code B sale answers the v80
# boundary questions: a Form 8949 is needed (no-form8949-sources no), there
# is an adjustment code other than W (Path B no), and neither in-class
# proposition holds (both mention only wash-sale adjustments).
HONEST = {"q1": "no", "q2": "no", "form8949": "no", "path_b": "no", "old_ic": "no", "new_ic": "no"}
# The filer follows the Form 1099-B and Exception 1: no Form 8949.
NO_8949 = {"q1": "no", "q2": "no"}
# The filer puts the sale on box B or E and says the v79 in-class answer holds.
ON_BE = {"q1": "yes", "q2": "no", "form8949": "no", "path_b": "no", "old_ic": "yes"}


def ret(sales: Callable[[Acts], Any] | None, answers: dict[str, str]) -> Callable[[], Acts]:
    return lambda: cfp.v80_return(sales=sales, **answers)


def cases() -> dict[str, Callable[[], Acts]]:
    a_high_broker = after(lambda a: direct(a, "st", 10000.0, 7000.0, "ahb"))
    a_high_fixed = after(lambda a: direct(a, "st", 10000.0, 4000.0, "ahf"))
    d_low_broker = after(lambda a: direct(a, "lt", 6000.0, 2000.0, "dlb"))
    d_low_fixed = after(lambda a: direct(a, "lt", 6000.0, 3000.0, "dlf"))
    a_loss_broker = after(lambda a: direct(a, "st", 5000.0, 3000.0, "alb"))
    a_loss_fixed = after(lambda a: direct(a, "st", 5000.0, 9000.0, "alf"))
    return {
        "wage": ret(None, {"q1": "no", "q2": "no"}),
        # Box A, broker basis too high: 10000 proceeds, 7000 shown, 4000 correct.
        "a_high_direct_broker_honest": ret(a_high_broker, HONEST),
        "a_high_direct_broker_no8949": ret(a_high_broker, NO_8949),
        "a_high_direct_fixed_no8949": ret(a_high_fixed, NO_8949),
        "a_high_direct_fixed_honest": ret(a_high_fixed, HONEST),
        "a_high_on_w_broker": ret(after(lambda a: wash(a, "st", 10000.0, 7000.0, 3000.0, "ahw")), HONEST),
        "a_high_on_b_fixed": ret(noncovered("st", 10000.0, 4000.0, "ahn"), ON_BE),
        # Box D, broker basis too low: 6000 proceeds, 2000 shown, 3000 correct.
        "d_low_direct_broker_honest": ret(d_low_broker, HONEST),
        "d_low_direct_broker_no8949": ret(d_low_broker, NO_8949),
        "d_low_direct_fixed_no8949": ret(d_low_fixed, NO_8949),
        "d_low_on_e_fixed": ret(noncovered("lt", 6000.0, 3000.0, "dln"), ON_BE),
        # Box A, the correction turns a gain into a loss: 5000, 3000 shown, 9000 correct.
        "a_loss_direct_broker_no8949": ret(a_loss_broker, NO_8949),
        "a_loss_direct_fixed_no8949": ret(a_loss_fixed, NO_8949),
        "a_loss_on_b_fixed": ret(noncovered("st", 5000.0, 9000.0, "aln"), ON_BE),
        # Box A, B and W on one row: 4000, 4500 shown, 6000 correct, 1000 disallowed.
        "a_bw_on_w_broker": ret(after(lambda a: wash(a, "st", 4000.0, 4500.0, 1000.0, "abwb")), HONEST),
        "a_bw_on_w_fixed": ret(after(lambda a: wash(a, "st", 4000.0, 6000.0, 1000.0, "abwf")), HONEST),
        # The same, with Path B answered yes (false: code B is an adjustment other than W).
        "a_bw_on_w_fixed_path_b_yes": ret(after(lambda a: wash(a, "st", 4000.0, 6000.0, 1000.0, "abwy")),
                                          {"q1": "no", "q2": "no", "form8949": "no", "path_b": "yes"}),
        # Box B, basis shown but not reported, and wrong: 3000, 2500 shown, 1000 correct.
        "b_code_b_on_b": ret(noncovered("st", 3000.0, 1000.0, "bcb"), ON_BE),
        # Box E, the same: 6000, 5000 shown, 2000 correct.
        "e_code_b_on_e": ret(noncovered("lt", 6000.0, 2000.0, "ecb"), ON_BE),
    }


# ---- run and summarize ---------------------------------------------------


CF_SUMMARIZE = cp.summarize


def summary(outcome: Any) -> dict[str, Any]:
    """cf_probe's summary plus the (disposition, code, missing) of each line's row."""
    result: dict[str, Any] = CF_SUMMARIZE(outcome)
    if outcome.refusal is not None:
        return result
    report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
    model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    # Every question in page order, untruncated (cf_probe cuts sentences at 240 characters).
    questions: list[str] = []
    for section in model.get("sections") or []:
        for reason in (section.get("resolved") or {}).get("reasons") or []:
            sentence = str(reason.get("sentence") or "").strip() if isinstance(reason, dict) else ""
            if sentence.endswith("?") and sentence not in questions:
                questions.append(sentence)
    result["questions"] = questions
    result["rows"] = {
        str(row.get("artifact_id", "")).removeprefix(P + "rule."): [
            row.get("disposition"), row.get("code"), [str(m).removeprefix(P) for m in row.get("missing") or []][:6]]
        for row in report.get("dispositions") or []
        if str(row.get("artifact_id", "")) in WHY_ROWS
    }
    return result


cp.summarize = summary  # cf_probe.run_case reads its module global


def execute(build: Callable[[], Acts], run_id: str) -> dict[str, Any]:
    started = time.monotonic()
    try:
        result = cp.run_case(build(), run_id)
    except Exception as exc:  # noqa: BLE001 — record the failure instead of hiding it
        result = {"error": type(exc).__name__, "message": probe.scrub(str(exc))[:600],
                  "trace": probe.scrub(traceback.format_exc())[-500:]}
    result["seconds"] = round(time.monotonic() - started, 1)
    return result


def keep(result: dict[str, Any]) -> dict[str, Any]:
    names = ("error", "message", "stop_reason", "presentation_valid", "lines", "symbols", "attachments",
             "rows", "blocked", "questions", "f8949_parts")
    out = {k: result.get(k) for k in names if result.get(k) not in (None, [], {})}
    if "blocked" in out:
        out["blocked"] = out["blocked"][:12]
    return out


def main() -> None:
    pin_v80()
    selected = set(sys.argv[1:])
    results: dict[str, Any] = {"package": "core-calculations v80", "registry": "v78", "release": "v78", "cases": {}}
    for name, build in cases().items():
        if selected and name not in selected:
            continue
        result = execute(build, f"demo.codeb.p0.{name}")
        results["cases"][name] = keep(result)
        lines = result.get("lines") or {}
        print(name, result.get("error") or result.get("stop_reason"),
              [lines.get(k) for k in ("form1040.line-15", "form1040.line-16")],
              result.get("attachments"), result.get("seconds"), flush=True)
    if selected and OUT.exists():
        merged = json.loads(OUT.read_text(encoding="utf-8"))
        merged["cases"].update(results["cases"])
        results = merged
    OUT.write_text(probe.scrub(json.dumps(results, indent=1, sort_keys=True)) + "\n", encoding="utf-8")
    print(f"wrote {OUT.name}", flush=True)


if __name__ == "__main__":
    main()
