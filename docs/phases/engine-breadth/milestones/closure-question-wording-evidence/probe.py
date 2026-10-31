"""P0 probe (closure-question-wording): on the real coordinator (live_coordinate_run, core v66),
make a line block SOURCE_SET_UNCLOSED and read what each surface says.

Case A: one Form 1099-G box 4 withholding member recorded, its closure unanswered -> line 25b blocks
        at the root; lines 25d, 33, 34, 35a, 36, 37 wait behind it.
Case B: one Form 1099-INT box 1 interest member recorded, its closure unanswered -> line 2b blocks
        at the root; the lines behind it wait.

Surfaces read, for every blocked line on the path:
  - the saved presentation model (resolved record, reasons, the field's blocked text);
  - the rendered page, via headless Chrome --dump-dom of the page `live_session._render_page` builds
    from the saved model (skipped, and said so, when no browser is found);
  - the CLI's blocked-surface line (the f-string `runners/derive.py::_human` prints per blocked row,
    applied to the live run's blocked rows: the derive CLI itself only takes a scenario file).

Synthetic demo.* data only. Run from the repo root:

    python3 docs/phases/engine-breadth/milestones/closure-question-wording-evidence/probe.py

Reads committed tests' helpers; changes nothing and writes only probe-output.json beside this file.
"""
from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_session import _render_page  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.presentation_projection import validate_presentation_model  # noqa: E402
from tests import test_collect_closure as cc  # noqa: E402
from tests import test_itemization_cents as ic  # noqa: E402
from tests import test_w2g_gambling as w2g  # noqa: E402
from tests.test_form_1099_k_income import _handover  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import USER, _finish  # noqa: E402
from tests.test_sli_line21_explanation_page import BROWSER  # noqa: E402
from tests.test_withholding_closure import _strip_closure  # noqa: E402

P = "tax.us.2025."
OUT = Path(__file__).with_name("probe-output.json")


def run(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, Any], bytes | None]:
    """Run on core v66 / registry v64 / release v64; a member contradicting a base 'none' declaration
    has that declaration withdrawn first (as a filer does by recording the member)."""
    for _ in range(5):
        try:
            return _run_once(acts, run_id)
        except Exception as exc:
            found = re.search(r"contradiction: (\S+) is currently", str(exc))
            if not found:
                raise
            acts = _strip_closure(acts, found.group(1))
    raise AssertionError("too many declaration withdrawals")


def _run_once(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, Any], dict[str, Any], bytes | None]:
    finished = _finish(
        copy.deepcopy(acts), package_path=ic.PACKAGE_V66, package_version="v66",
        release_path=ic.RELEASE_V64, release_version="v64", note=run_id,
    )
    finished = _handover(finished, surface=ic.SURFACE_V66, reconfirm=True)
    with TemporaryDirectory() as tmp:
        capability = WorkspaceCapability(Path(tmp) / "L")
        outcome = live_coordinate_run(
            capability, repo_root=ic.ROOT, authoritative_acts=finished, workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": "2025"}, scope_user=USER,
            request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
            surface=ic.SURFACE_V66, output_name="out.json",
        )
        assert outcome.refusal is None, outcome.refusal
        assert outcome.presentation_path is not None and outcome.output_path is not None
        model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
        report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
        page = _render_page(ic.ROOT, capability, outcome.presentation_path)
    return model, report, page


class _SectionText(HTMLParser):
    """Visible text of each rendered line wrapper (<div id=SECTION_ID>), one string per section id."""

    def __init__(self, ids: set[str]) -> None:
        super().__init__()
        self.ids = ids
        self.stack: list[str | None] = []
        self.current: list[str] = []
        self.sections: dict[str, list[str]] = {}
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.skip += 1
        raw = dict(attrs).get("id")
        sid = raw if tag == "div" and raw in self.ids else None
        if sid:
            self.current.append(sid)
            self.sections.setdefault(sid, [])
        self.stack.append(sid)

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
        if self.stack:
            if self.stack.pop() is not None and self.current:
                self.current.pop()

    def handle_data(self, data: str) -> None:
        if self.skip or not self.current or not data.strip():
            return
        self.sections[self.current[-1]].append(" ".join(data.split()))


def rendered_text(page: bytes, ids: set[str]) -> dict[str, str] | None:
    if BROWSER is None:
        return None
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "page.html"
        path.write_bytes(page)
        dom = subprocess.run(
            [BROWSER, "--headless", "--disable-gpu", "--no-sandbox", "--dump-dom", path.as_uri()],
            check=True, capture_output=True, text=True, timeout=60,
        ).stdout
    parser = _SectionText(ids)
    parser.feed(dom)
    return {sid: " | ".join(parts) for sid, parts in parser.sections.items()}


def cli_line(row: dict[str, Any]) -> str:
    # The f-string runners/derive.py::_human prints per blocked row.
    return f"  - {row['artifact_id']}: {row['code']} (missing {', '.join(row['missing']) or 'none'})"


def _published_symbols() -> dict[str, set[str]]:
    """rule id -> symbol(s) it publishes, for the rules core v66 pins (a blocked report row names the rule, not the symbol)."""
    import glob
    corpus = ic.CONTENT
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for f in glob.glob(str(corpus / "*.json")):
        try:
            body = json.loads(Path(f).read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and "id" in body and "version" in body:
            index[(body["id"], body["version"])] = body
    package = json.loads(ic.PACKAGE_V66.read_text(encoding="utf-8"))
    out: dict[str, set[str]] = {}
    for m in package["members"]:
        if m["role"] in ("computation", "field-mapping"):
            rule = index[(m["id"], m["version"])]
            if isinstance(rule.get("publishes"), str):
                out.setdefault(m["id"], set()).add(rule["publishes"])
    return out


def root_trace(blocked: list[dict[str, Any]]) -> dict[str, Any]:
    """Follow each blocked symbol's `missing` through the blocked rows to the rows it bottoms out on, and
    classify them: SOURCE_SET_UNCLOSED rows (closure roots) or anything else. Shows the join the
    projector would make (blocked rows by published symbol; walk `missing`)."""
    published = _published_symbols()
    by_symbol: dict[str, list[dict[str, Any]]] = {}
    unmapped = 0
    for row in blocked:
        symbols = published.get(row["artifact_id"])
        if not symbols:
            unmapped += 1
            continue
        for symbol in symbols:
            by_symbol.setdefault(symbol, []).append(row)

    def roots(symbol: str, seen: tuple[str, ...] = ()) -> set[tuple[str, tuple[str, ...]]]:
        rows = by_symbol.get(symbol)
        if not rows:
            return {("not-blocked-or-absent", (symbol,))}
        found: set[tuple[str, tuple[str, ...]]] = set()
        for row in rows:
            if row["code"] == "SOURCE_SET_UNCLOSED":
                found.add(("closure", tuple(row["missing"])))
                continue
            for missing in row["missing"]:
                if missing not in seen:
                    found |= roots(missing, seen + (symbol,))
        return found

    kinds: dict[str, int] = {}
    families: set[str] = set()
    for symbol in by_symbol:
        found = roots(symbol)
        label = "only-closure-roots" if {k for k, _ in found} == {"closure"} else "other-or-mixed"
        kinds[label] = kinds.get(label, 0) + 1
        families |= {f for k, fs in found if k == "closure" for f in fs}
    return {"blocked_rows": len(blocked), "rows_not_mapped_to_a_symbol": unmapped, "blocked_symbols": len(by_symbol),
            "symbols_by_root_kind": kinds, "closure_families_reached": sorted(families)}


HAND_SUPPLIED = "HAND-SUPPLIED TEST SENTENCE (not from content): Have you recorded every Form 1099-G box 4 amount?"


def design_check(model: dict[str, Any], section_ids: list[str]) -> dict[str, Any]:
    """Design check: put a hand-supplied {sentence} reason on blocked lines of a COPY of the saved model, then
    ask today's unchanged validator and today's unchanged page whether they accept and how they render it.
    This shows presentation-model.v2 and the page need no change to carry a sentence-only reason; the
    sentence here is a test string, not content."""
    edited = copy.deepcopy(model)
    for section in edited["sections"]:
        if section["id"] in section_ids:
            section["resolved"]["reasons"] = [{"sentence": HAND_SUPPLIED}]
    validate_presentation_model(edited)
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "model.json"
        path.write_text(json.dumps(edited), encoding="utf-8")
        page = _render_page(ic.ROOT, WorkspaceCapability(Path(tmp)), path)
    text = rendered_text(page, set(section_ids)) if BROWSER is not None else None
    return {"validator_accepts": True, "rendered_page_text": text}


def read_case(name: str, acts: list[dict[str, object]]) -> dict[str, Any]:
    model, report, page = run(acts, f"demo.cqw.{name}")
    blocked = [r for r in report["dispositions"] if r["disposition"] == "blocked"]
    blocked_symbols = {
        n["symbol"] for n in model["dispositionNodes"].values()
        if n["records"] and n["records"][0]["disposition"] == "blocked"
    }
    text = rendered_text(page, {s["id"] for s in model["sections"]}) if page is not None else None
    lines = []
    for s in model["sections"]:
        if s["resolved"]["disposition"] != "blocked":
            continue
        node = model["dispositionNodes"][s["field"]["binds_symbol"]]
        lines.append({
            "section": s["id"],
            "line": s["field"]["line"],
            "label": s["field"]["label"],
            "saved_resolved": s["resolved"],
            "saved_field_blocked_explain": s["field"]["dispositions"]["blocked"]["explain"],
            "saved_has_reasons_key": "reasons" in s["resolved"],
            "saved_disposition_node_record": {k: v for k, v in node["records"][0].items() if k != "pins"},
            "saved_disposition_node_children": node["children"],
            "rendered_page_text": None if text is None else text.get(s["id"]),
        })
    return {
        "case": name,
        "blocked_rows": [{"artifact_id": r["artifact_id"], "code": r["code"], "missing": r["missing"]} for r in blocked],
        "cli_blocked_lines": [cli_line(r) for r in sorted(blocked, key=lambda r: r["artifact_id"])],
        "root_rows": [r["artifact_id"] for r in blocked if r["code"] == "SOURCE_SET_UNCLOSED"],
        "blocked_sections": lines,
        "model_schema": model["schema"],
        "model_top_level_keys": sorted(model),
        "browser_available": BROWSER is not None,
        "root_trace": root_trace(blocked),
        "design_check_sentence_only_reason": design_check(
            model, ["line-25b", "line-33", "line-37"] if name.startswith("A") else ["line-2b", "line-37"]
        ),
    }


def main() -> None:
    base = w2g._w2g_return([])
    a = cc._add_member(copy.deepcopy(base), P + "f1099g.b4", 600.0, close=False, tag="g4")
    b = cc._add_member(copy.deepcopy(base), P + "f1099int.b1", 800.0, close=False, tag="int1")
    out = {"core": "v66", "cases": [read_case("A-1099g-box4-line25b", a), read_case("B-1099int-box1-line2b", b)]}
    OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    for case in out["cases"]:
        print(case["case"], "roots:", case["root_rows"], "blocked sections:", [s["section"] for s in case["blocked_sections"]])


if __name__ == "__main__":
    main()
