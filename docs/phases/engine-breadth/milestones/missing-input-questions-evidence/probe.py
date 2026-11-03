"""P0 probe -- what a blocked line shows when a filer-supplied input is missing, on core v71 (evidence only).

Part A withholds, one at a time, every asserted fact type the complete current-core base return
(``tests/helpers/current_core_returns.base_return``) records, and runs each return through
``live_coordinate_run`` on the committed core v71 / registry v69 / release v69. Part B builds the
statement-level cases and withholds, one at a time, every fact type the current-core adders record
(Forms 1099-INT box 8, 1099-DIV boxes 12 and 7, 1098-E, 1098, Schedule 8812 Part II-B, gambling losses).

For every case it records each blocked line's id, its disposition codes, the reasons the saved
presentation attaches (the page shows them, else the field's generic blocked text), and the root
blocked rows (code and ``missing``). Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/missing-input-questions-evidence/probe.py [A|B|C|D|all]

Synthetic ``demo.*`` ids only. Writes ``probe-output.json`` beside itself (no absolute paths); cases
already in it are kept, not rerun (delete the file to rerun all).
"""

from __future__ import annotations

import copy
import json
import re
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any, Callable

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

HERE = Path(__file__).resolve().parent
OUT_PATH = HERE / "probe-output.json"
_PATH = re.compile(r"(?:/Users|/private|/tmp|/var|/opt)[^\s'\"\\]*")
P = "tax.us.2025."


def redact(text: str) -> str:
    return _PATH.sub("[path]", text)


def short(symbol: str) -> str:
    return symbol.replace(P, "")


_PUBLISHES: dict[str, str] | None = None


def publishes() -> dict[str, str]:
    """rule artifact id -> the symbol it publishes, over the v71 package's rule members."""
    global _PUBLISHES
    if _PUBLISHES is None:
        import glob
        content = REPO / "packages/content/tax/2025"
        package = json.loads((content / "package.core-calculations.v71.json").read_text(encoding="utf-8"))
        index: dict[tuple[str, str], dict[str, Any]] = {}
        for name in glob.glob(str(content / "*.json")):
            try:
                body = json.loads(Path(name).read_text(encoding="utf-8"))
            except ValueError:
                continue
            if isinstance(body, dict) and "id" in body and "version" in body:
                index[(body["id"], body["version"])] = body
        _PUBLISHES = {}
        for m in package["members"]:
            body = index[(m["id"], m["version"])]
            if "publishes" in body:
                _PUBLISHES[str(body["id"])] = str(body["publishes"])
    return _PUBLISHES


def leaves_of(row: dict[str, Any], by_symbol: dict[str, list[dict[str, Any]]]) -> list[list[Any]]:
    """The root causes under a blocked row, as the projector's walk sees them: a missing symbol with no
    blocked row of its own is an ``absent`` leaf (a source fact); any other root keeps its code."""
    out: set[tuple[str, tuple[str, ...]]] = set()

    def walk(cur: dict[str, Any], seen: frozenset[str]) -> None:
        missing = [str(m) for m in cur.get("missing") or []]
        if cur["code"] != "DEPENDENCY_ABSENT":
            out.add((str(cur["code"]), tuple(short(m) for m in missing)))
            return
        for m in missing:
            if m in seen:
                continue
            blocked = [r for r in by_symbol.get(m, []) if r.get("disposition") == "blocked"]
            if not blocked:
                out.add(("ABSENT", (short(m),)))
            for b in blocked:
                walk(b, seen | {m})

    walk(row, frozenset())
    return [[c, list(m)] for c, m in sorted(out)]


def summarize_run(r: Any) -> dict[str, Any]:
    pub = publishes()
    by_symbol: dict[str, list[dict[str, Any]]] = {}
    for d in r.dispositions:
        by_symbol.setdefault(str(d.get("symbol") or pub.get(str(d["artifact_id"])) or str(d["artifact_id"]).removesuffix(".synthesized")), []).append(d)
    lines = []
    for s in r.model["sections"]:
        res = s["resolved"]
        if res["disposition"] != "blocked":
            continue
        symbol = s["field"]["binds_symbol"]
        rows = [d for d in by_symbol.get(symbol, []) if d.get("disposition") == "blocked"]
        leaves: set[tuple[str, tuple[str, ...]]] = set()
        for row in rows:
            leaves.update((c, tuple(m)) for c, m in leaves_of(row, by_symbol))
        lines.append({
            "section": s["id"],
            "line": s["field"].get("line"),
            "form": s["field"].get("form", {}).get("form_id"),
            "label": s["field"].get("label"),
            "codes": res.get("activeCodes"),
            "leaves": [[c, list(m)] for c, m in sorted(leaves)],
            "reasons": [x.get("sentence") for x in res.get("reasons", [])] if res.get("reasons") else None,
            # the field's generic blocked text, recorded only when it is not the usual sentence
            "generic": (None if re.fullmatch(r"Form \S+ line \S+ is blocked because an input it needs is missing or not yet closed\.",
                                             s["field"]["dispositions"]["blocked"]["explain"])
                        else s["field"]["dispositions"]["blocked"]["explain"]),
        })
    return {"blocked_lines": lines, "blocked_rows": sum(1 for d in r.dispositions if d.get("disposition") == "blocked")}


# --- returns -------------------------------------------------------------------------------


def _w2_statement_base() -> list[dict[str, object]]:
    from tests import test_statement_withholding_answer as swa
    return swa._no_withholding()


def _family(key: str, n: int, amounts: list[float | None]) -> list[dict[str, object]]:
    from tests import test_statement_withholding_answer as swa
    return swa.family_return(key, n, amounts)


def _two_w2(box2: float | None) -> list[dict[str, object]]:
    """Two W-2 slips, box 2 answered on the first only (``box2`` None) or on both, W-2 box 2 family closed."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "swa_probe", REPO / "docs/phases/engine-breadth/milestones/statement-withholding-answer-evidence/probe.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["swa_probe"] = mod
    spec.loader.exec_module(mod)
    acts = mod._w2_second_slip(_w2_statement_base(), box2=box2)
    return mod._set_closure_w2(acts, "head")


def _adder(name: str) -> list[dict[str, object]]:
    from tests.helpers import current_core_returns as c
    base = c.base_return
    if name == "int-b8":
        return c.add_tax_exempt_interest_1099int(base(), [40.0])
    if name == "div-b12":
        return c.add_exempt_interest_dividends_1099div(base(), [60.0])
    if name == "div-b7":
        return c.add_foreign_tax_1099div(base(), [30.0])
    if name == "f1098e":
        return c.add_student_loan_interest_1098e(base(), [500.0])
    if name == "f1098":
        return c.add_mortgage_itemizer(base(), 9000.0)
    if name == "part-ii-b":
        return c.part_ii_b_return(box4=300.0, box6=200.0)
    if name == "gambling-losses":
        return c.declare_no_other_line16(c.add_gambling_losses(base(), [400.0]))
    raise KeyError(name)


ADDERS = ("int-b8", "div-b12", "div-b7", "f1098e", "f1098", "part-ii-b", "gambling-losses")
def _drop(acts: list[dict[str, object]], *fact_types: str) -> list[dict[str, object]]:
    from tests.helpers import current_core_returns as c
    kept = [a for a in acts if str(a["payload"].get("finding", {}).get("fact_id", "")).split("|")[0] not in fact_types]
    assert len(kept) < len(acts), fact_types
    return c._renumbered(copy.deepcopy(kept))


def _closure(acts: list[dict[str, object]], key: str, mode: str) -> list[dict[str, object]]:
    from tests.test_withholding_closure import _set_closure
    return _set_closure(acts, key, mode)


def _sli_witness_withheld() -> list[dict[str, object]]:
    from tests.helpers import current_core_returns as c
    acts = c.add_student_loan_interest_1098e(c.base_return(), [500.0])
    return _drop(acts, P + "f1098e.no-related-person-interest", P + "w2.box2-withholding")


STATEMENT_CASES = {
    # lines with two causes: a missing answer and an unconfirmed family
    "mixed.25b-int-box4-missing-div-box4-unconfirmed": lambda: _closure(_family("int", 1, [None]), "div", "none"),
    "mixed.25a-box2-missing-25b-int-box4-unconfirmed": lambda: _drop(_closure(_family("int", 1, [50.0]), "int", "none"), P + "w2.box2-withholding"),
    "mixed.scope-answer-missing-b1-unconfirmed": lambda: _drop(_w2_statement_base(), P + "line2a-scope.no-amt-form-6251", P + "f1099int.b1.source-closure"),
    "mixed.scope-answer-missing-div-1a-unconfirmed": lambda: _drop(_w2_statement_base(), P + "line2a-scope.no-amt-form-6251", P + "f1099div.1a.source-closure"),
    "mixed.box2-missing-and-statement-answer-missing-on-1098e": _sli_witness_withheld,
    # an amount that cannot be recorded at all (the kernel refuses a negative box 4)
    "int.negative-box4": lambda: _family("int", 1, [-5.0]),
    **{f"{k}.one-statement-no-answer": (lambda k=k: _family(k, 1, [None])) for k in ("int", "div", "ira", "g", "ssa")},
    **{f"{k}.two-statements-second-no-answer": (lambda k=k: _family(k, 2, [{"int": 50.0, "div": 40.0, "ira": 1200.0, "g": 600.0, "ssa": 800.0}[k], None]))
       for k in ("int", "div", "ira", "g", "ssa")},
    "w2.two-slips-second-no-box2": lambda: _two_w2(None),
    "w2.two-slips-both-answered": lambda: _two_w2(1200.0),
}


def build(spec: str) -> list[dict[str, object]]:
    """``withhold:<return>:<fact type>`` removes that fact type's assertions from a complete return;
    ``build:<case>`` is a case as built."""
    from tests.helpers import current_core_returns as c
    kind, _, rest = spec.partition(":")
    if kind == "build":
        return STATEMENT_CASES[rest]()
    ret, _, fact_type = rest.partition(":")
    acts = copy.deepcopy(c.base_return() if ret == "base" else _adder(ret))
    kept = [a for a in acts if str(a["payload"].get("finding", {}).get("fact_id", "")).split("|")[0] != fact_type]
    assert len(kept) < len(acts), spec
    return c._renumbered(kept)


def asserted_types(acts: list[dict[str, object]]) -> list[str]:
    seen: list[str] = []
    for a in acts:
        f = a["payload"].get("finding")
        if f and a["kind"] == "assertion":
            t = str(f["fact_id"]).split("|")[0]
            if t not in seen:
                seen.append(t)
    return seen


# core -> (package file, package version, release file, release version, registry file); core vN pairs with
# registry and release v(N-2)
OLDER = {
    f"v{n}": (f"package.core-calculations.v{n}.json", f"v{n}", f"demo.release.sli-worksheet-integration.2025.v{n - 2}.json",
              f"v{n - 2}", f"published-packages.v{n - 2}.json")
    for n in (68, 69, 70)
}
# the cases rendered again on the earlier cores (each answers: what did they show before?)
ON_EARLIER = (
    "withhold:base:tax.us.2025.w2.box2-withholding",
    "withhold:base:tax.us.2025.schedule1-part1-scope.no-sch1-line3-business",
    "build:int.one-statement-no-answer",
    "build:mixed.25a-box2-missing-25b-int-box4-unconfirmed",
    "build:mixed.25b-int-box4-missing-div-box4-unconfirmed",
    "build:mixed.scope-answer-missing-div-1a-unconfirmed",
    "build:mixed.box2-missing-and-statement-answer-missing-on-1098e",
)


def run_case(args: tuple[str, str]) -> dict[str, Any]:
    run_id, spec = args
    from tests import test_statement_withholding_answer as swa
    core = "v71"
    if spec.startswith("core:"):
        _, core, spec = spec.split(":", 2)
        swa.CORES.update(OLDER)
    try:
        return {"run_id": run_id, "spec": spec, "core": core, "status": "ran", **summarize_run(swa.run(build(spec), run_id, core))}
    except Exception as exc:  # a refusal is evidence
        return {"run_id": run_id, "spec": spec, "status": "error", "error": redact(f"{type(exc).__name__}: {exc}")[:600]}


def main() -> None:
    part = sys.argv[1] if len(sys.argv) > 1 else "all"
    done: dict[str, Any] = {}
    if OUT_PATH.exists():
        done = {c["run_id"]: c for c in json.loads(OUT_PATH.read_text(encoding="utf-8"))["cases"]}
    todo: list[tuple[str, str]] = []
    if part in ("A", "all"):
        from tests.helpers import current_core_returns as c
        todo += [(f"demo.p0.mi.A.{t.replace(P, '')}", f"withhold:base:{t}") for t in asserted_types(c.base_return())]
    if part in ("B", "all"):
        from tests.helpers import current_core_returns as c
        base_types = set(asserted_types(c.base_return()))
        todo += [(f"demo.p0.mi.B.{name}", f"build:{name}") for name in STATEMENT_CASES]
        for adder in ADDERS:
            for t in asserted_types(_adder(adder)):
                if t not in base_types:
                    todo.append((f"demo.p0.mi.B.{adder}.{t.replace(P, '')}", f"withhold:{adder}:{t}"))
    if part in ("D", "all"):
        # facts the base return can lose without any line blocking (their route is not active there) are
        # withheld again on each adder's return, where the route is active
        quiet = {str(c["spec"]).split(":")[-1] for c in done.values()
                 if c["run_id"].startswith("demo.p0.mi.A.") and c["status"] == "ran" and not c["blocked_lines"]}
        for adder in ADDERS:
            for t in asserted_types(_adder(adder)):
                if t in quiet:
                    todo.append((f"demo.p0.mi.D.{adder}.{t.replace(P, '')}", f"withhold:{adder}:{t}"))
    if part in ("C", "all"):
        for core in OLDER:
            todo += [(f"demo.p0.mi.C.{core}.{spec.split(':', 2)[-1].replace('tax.us.2025.', '')}", f"core:{core}:{spec}")
                     for spec in ON_EARLIER]
    todo = [t for t in todo if t[0] not in done]
    with ProcessPoolExecutor(max_workers=6) as pool:
        for res in pool.map(run_case, todo):
            done[res["run_id"]] = res
            print(res["run_id"], res["status"], flush=True)
            OUT_PATH.write_text(json.dumps({"core": "v71", "cases": sorted(done.values(), key=lambda c: c["run_id"])}, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
