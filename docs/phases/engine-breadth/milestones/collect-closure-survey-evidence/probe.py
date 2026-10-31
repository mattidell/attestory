"""P0 probe -- one recorded member, closure unanswered, on core v61 (evidence only).

For each source set the survey lists, this builds a complete return (the
withholding-closure milestone's base, run on the committed core v61 / registry
v59 / release v59), records one member of that source family by a
member-transition, and runs three returns through ``live_coordinate_run``:

* base       -- the complete return, family closed empty (or never asked);
* answered   -- one member, the family's closure attested true at its horizon;
* unanswered -- the same member, the family's closure left unanswered.

A bound form field (a ``binds_symbol`` of a form-field member) is a *gap* line
when the answered return moves it away from the base and the unanswered return
publishes the same moved value: a partial sum reached a published line without
the closure the filer was never asked for. It is *held* when the unanswered
return does not publish it.

Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/collect-closure-survey-evidence/probe.py [source-set ...]

With no argument it runs every source set in ``survey-output.json`` plus the
guarded controls. Synthetic ``demo.*`` ids only. Writes ``probe-output.json``
beside itself (no absolute path). Nothing here edits repository content.
"""

from __future__ import annotations

import glob
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from packages.kernel.facts import fact_id_for  # noqa: E402
from tests.test_form_1099_withholding import (  # noqa: E402
    YEAR,
    _add,
    _assert,
    _base,
    _retirements,
    _social_security,
    _close,
    _introduce,
    _social_security_withholding,
    _transition,
    _unemployment_withholding,
)
from tests.test_other_dependents_credit_track1 import (  # noqa: E402
    _complete,
    build,
    ctc_child,
    odc_child,
    relative,
)
from tests.test_form_1099_withholding import NO_OTHER_DEPENDENT, _w2_withholding  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _act, _attested, _load  # noqa: E402
import copy  # noqa: E402

from tests.test_form_1099_k_income import _handover, _run_finished  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _finish  # noqa: E402
from tests.test_withholding_closure import (  # noqa: E402
    PACKAGE_V61,
    RELEASE_V59,
    SURFACE_V61,
    _horizons,
    _strip_closure,
)


def _run_on(acts: list[dict[str, object]], run_id: str, core: str, *, reconfirm: bool = True) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """``tests.test_withholding_closure._run_on`` for core v61, with the Social Security
    handover's reconfirmation optional: the harness otherwise attests the Social Security
    closure itself after every handover, which would hide an unanswered one."""
    assert core == "v61"
    finished = _finish(copy.deepcopy(acts), package_path=PACKAGE_V61, package_version="v61",
                       release_path=RELEASE_V59, release_version="v59", note=run_id)
    finished = _handover(finished, surface=SURFACE_V61, reconfirm=reconfirm)
    return _run_finished(finished, run_id, SURFACE_V61)

HERE = Path(__file__).resolve().parent
OUT_PATH = HERE / "probe-output.json"
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
_PATH = re.compile(r"(?:/Users|/private|/tmp|/var|/opt)[^\s'\"\\]*")

# Guarded entries the survey did not mark unguarded, run as controls.
CONTROLS = (
    "tax.us.2025.f1099int.b4", "tax.us.2025.f1099div.b4", "tax.us.2025.f1099r.box4",
    "tax.us.2025.f1099g.b4", "tax.us.2025.ssa1099.b6", "tax.us.2025.f1099div.12",
    "tax.us.2025.f1099div.1b", "tax.us.2025.f1098",
)


BUNDLE_OF: dict[str, Any] = {}


def _load_package() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], set[str]]:
    pkg = json.loads((CONTENT / "package.core-calculations.v61.json").read_text())
    idx: dict[tuple[str, str], dict[str, Any]] = {}
    for f in glob.glob(str(CONTENT / "*.json")):
        try:
            j = json.loads(Path(f).read_text())
        except ValueError:
            continue
        if isinstance(j, dict) and "id" in j and "version" in j:
            idx[(j["id"], j["version"])] = j
    mem = [idx[(m["id"], m["version"])] for m in pkg["members"]]
    fams = {m["id"]: m for m in mem if m.get("schema", "").startswith("source-family")}
    maps = {m["family"]["id"]: m for m in mem if m.get("schema", "").startswith("source-closure-mapping")}
    ft: dict[str, Any] = {}
    for m in pkg["members"]:
        if m["role"] == "fact-type-bundle":
            bundle = idx[(m["id"], m["version"])]
            for t in bundle["fact_types"]:
                ft[t["id"]] = t
                BUNDLE_OF[t["id"]] = bundle
    fields = {m["binds_symbol"] for m in mem if m.get("schema", "").startswith("form-field")}
    return fams, maps, ft, idx, fields


FAMS, MAPS, FT, _IDX, FIELDS = _load_package()


def _downstream() -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    path = HERE / "survey-output.json"
    if path.exists():
        data = json.loads(path.read_text())
        for e in data["inventory"] + data["collects_guarded_at_their_own_site"]:
            out.setdefault(e["source_set"], set()).update(e["bound_fields_downstream_any_path"])
    return out


DOWNSTREAM = _downstream()


def base_return() -> list[dict[str, object]]:
    acts = _base(wages=50000.0, w2_withheld=4500.0)
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    return acts


def _pick(schema: dict[str, Any], amount: Any) -> Any:
    """A value that satisfies a companion fact type's schema (const, then number, string...)."""
    if "const" in schema:
        return schema["const"]
    for branch in schema.get("anyOf", []):
        if "const" in branch and branch["const"] is not None:
            return branch["const"]
    if "enum" in schema:
        return schema["enum"][0]
    kind = schema.get("type")
    if kind == "number":
        return amount
    if kind == "boolean":
        return False
    return "demo"


def _adopt_if_needed(acts: list[dict[str, object]], type_id: str) -> None:
    adopted = {t["id"] for a in acts if a["kind"] == "bundle-adoption" for t in a["payload"]["bundle"]["fact_types"]}  # type: ignore[index]
    if type_id not in adopted and type_id in BUNDLE_OF:
        _add(acts, "bundle-adoption", {"bundle": BUNDLE_OF[type_id]})


# A base declaration ("no tax-exempt interest") the member would otherwise leave contradicting
# the rule that reads it; the answered and unanswered returns both carry the flip.
FLIPS = {"tax.us.2025.f1099int.b8": ("tax.us.2025.line2a-scope.no-f1099int-tax-exempt", "no")}


def add_member(acts: list[dict[str, object]], family: str, value: Any, *, close: bool,
               companions: tuple[tuple[str, tuple[tuple[str, str], ...]], ...] = ()) -> list[dict[str, object]]:
    """Records one member of ``family`` (entities introduced, same-statement companions
    asserted, horizon advanced) and, when ``close``, attests the family closure at the
    resulting horizon; otherwise the family's closure is left unanswered."""
    fam, mapping = FAMS[family], MAPS[family]
    ftype = FT[fam["member_predicate"]["fact_type"]]
    out = _strip_closure(acts, mapping["closure_fact_type"]["id"])
    if family in FLIPS:
        flip_type, flip_value = FLIPS[family]
        for act in out:
            finding = act["payload"].get("finding") if isinstance(act["payload"], dict) else None  # type: ignore[union-attr]
            if finding and str(finding.get("fact_id", "")).startswith(flip_type + "|"):
                finding["value"] = flip_value
    _adopt_if_needed(out, ftype["id"])
    _adopt_if_needed(out, mapping["closure_fact_type"]["id"])
    horizons = _horizons(out, family)
    if not horizons:
        genesis = "demo.p0.cs.g0"
        _add(out, "horizon-genesis", {"family": {"id": family, "version": fam["version"]},
                                      "scope": {"tax-year": YEAR, "subject": "demo.primary"}, "horizon_id": genesis})
        horizons = [genesis]
    keys: list[tuple[str, str]] = []
    declared: list[tuple[str, str]] = []   # identity keys in the fact type's declared order
    for key in ftype["identity_keys"]:
        if key["kind"] == "entity":
            eid = f"demo.p0.cs.{key['name']}"
            _introduce(out, eid, key["entity_kind"])
            keys.append((key["name"], eid))
            declared.append((key["name"], eid))
        else:
            declared.append((key["name"], key["values"][0]))
    for n, (ctype, ckeys) in enumerate(companions):
        _assert(out, f"demo.p0.cs.companion.{n}", ctype, ckeys, _pick(FT[ctype]["value_schema"], value))
    new = "demo.p0.cs.h1"
    # Recorded with the key order the fact type declares (a literal key may come first).
    _add(out, "member-transition", {
        "family": {"id": family, "version": fam["version"]},
        "scope": {"tax-year": YEAR, "subject": "demo.primary"},
        "member": {"action": "assert", "finding": _attested("demo.p0.cs.member", fact_id_for(ftype["id"], tuple(declared)), value)},
        "successor": {"id": new, "predecessor": horizons[-1]},
    })
    if close:
        _close(out, mapping["closure_fact_type"]["id"], new, "demo.p0.cs.closure")
    return out


def existing_builder(family: str, close: bool) -> list[dict[str, object]] | None:
    """Families whose member needs a harness the withholding tests already provide."""
    acts = base_return()
    if family == "tax.us.2025.f1099r.ira-fully-taxable":
        acts = _strip_closure(_strip_closure(acts, MAPS[family]["closure_fact_type"]["id"]), MAPS["tax.us.2025.f1099r.box4"]["closure_fact_type"]["id"])
        _retirements(acts, [(10000.0, None)])
    elif family == "tax.us.2025.ssa1099.benefits":
        _social_security(acts, [12000.0], witness=None)
    else:
        return None
    return acts if close else _strip_closure(acts, MAPS[family]["closure_fact_type"]["id"])


ROSTERS = {
    "tax.us.2025.ctc.child-roster": "child",
    "tax.us.2025.eic.child-roster": "child",
    "tax.us.2025.odc.child-roster": "odc-child",
    "tax.us.2025.odc.relative-roster": "relative",
}


def roster_return(acts: list[dict[str, object]], family: str, value: Any, *, close: bool, n_children: int = 1,
                  with_children: bool = True) -> list[dict[str, object]]:
    """A complete return with one dependent on the roster ``family`` (the child, other-
    dependent child or other-dependent relative the existing harnesses build), the other
    rosters answered, and ``family``'s own closure attested or left unanswered."""
    kind = ROSTERS.get(family, "child")
    kids = {f"demo.p0.cs.kid{i}": ctc_child() if kind == "child" else odc_child() for i in range(n_children)} if kind != "relative" and with_children else {}
    rels = {"demo.p0.cs.relative": relative()} if kind == "relative" else {}
    answers = {NO_OTHER_DEPENDENT: "yes", "tax.us.2025.eic.age-25-under-65": "yes",
               "tax.us.2025.eic.main-home-in-us": "yes"}
    out = _complete(build(wages=50000.0, children=kids, relatives=rels, return_answers=answers))
    if kids:
        # The tie-breaker question every claimed child is asked on core v58 and later.
        out.append(_act(len(out), "bundle-adoption", {"bundle": _load("dtb-questions.bundle.json")}))
        for child in kids:
            out.append(_act(len(out), "assertion", {"finding": _attested(
                f"demo.p0.cs.dtb.{child}", f"tax.us.2025.dtb.child.another-could-claim|child={child},tax-year={YEAR}", "no")}))
    _w2_withholding(out, 4500.0)
    _unemployment_withholding(out, [])
    _social_security_withholding(out, [])
    if not close and family in ROSTERS:
        out = _strip_closure(out, MAPS[family]["closure_fact_type"]["id"])
    return out


def part_ii_b_return(acts: list[dict[str, object]], family: str, value: Any, *, close: bool) -> list[dict[str, object]]:
    """Three qualifying children (Schedule 8812 Part II-B applies) plus one member of the
    W-2 box 4 / box 6 family, which only line 21 of Schedule 8812 reads."""
    return add_member(roster_return(acts, family, value, close=True, n_children=3), family, value, close=close)




def run(acts: list[dict[str, object]], run_id: str, *, reconfirm: bool = True) -> dict[str, Any]:
    """Runs on v61. A member refused for contradicting a base declaration ("no X") has that
    declaration removed and is rerun; the removals are recorded."""
    removed: list[str] = []
    for _ in range(10):
        try:
            pubs, blocked = _run_on(acts, run_id, "v61", reconfirm=reconfirm)
            return {"pubs": pubs, "blocked": blocked, "declarations_removed": removed}
        except Exception as exc:  # a refusal is evidence
            match = re.search(r"contradiction: (\S+) is currently", str(exc))
            if not match:
                return {"error": _PATH.sub("[path]", f"{type(exc).__name__}: {exc}")[:500], "declarations_removed": removed}
            removed.append(match.group(1))
            acts = _strip_closure(acts, match.group(1))
    return {"error": "too many declaration removals", "declarations_removed": removed}


def _val(pubs: dict[str, Any], symbol: str) -> str | None:
    return str(pubs[symbol]["value"]) if symbol in pubs else None


def _short(symbol: str) -> str:
    return symbol.replace("tax.us.2025.", "")


def _roots(blocked: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"rule": str(r["artifact_id"]).split("rule.")[-1], "code": r["code"], "missing": [_short(str(m)) for m in r.get("missing") or []]}
            for r in blocked if r["code"] != "DEPENDENCY_ABSENT"]


def _build_running(family: str, value: Any, close: bool, builder: Any, run_id: str) -> dict[str, Any]:
    """Builds and runs, adding the same-statement companion a refusal names, until it runs."""
    companions: list[tuple[str, tuple[tuple[str, str], ...]]] = []
    for _ in range(6):
        if builder is add_member:
            special = existing_builder(family, close)
            acts = special if special is not None else add_member(base_return(), family, value, close=close, companions=tuple(companions))
        else:
            acts = builder(base_return(), family, value, close=close)
        # Only the Social Security family's own unanswered closure needs the harness's
        # automatic reconfirmation switched off.
        result = run(acts, run_id, reconfirm=not (not close and family == "tax.us.2025.ssa1099.benefits"))
        match = re.search(r"companion presence violated: .*? but (\S+?)\|(\S+) has no current value", result.get("error", ""))
        if not match:
            result["companions_added"] = [c[0].replace("tax.us.2025.", "") for c in companions]
            return result
        pairs = tuple((kv.split("=")[0], kv.split("=")[1]) for kv in match.group(2).split(",") if not kv.startswith("tax-year="))
        companions.append((match.group(1), pairs))
    return result


def case(family: str, value: Any, base_run: dict[str, Any], builder: Any = add_member) -> dict[str, Any]:
    tag = family.replace("tax.us.2025.", "")
    answered = _build_running(family, value, True, builder, f"demo.p0.cs.{tag}.answered")
    unanswered = _build_running(family, value, False, builder, f"demo.p0.cs.{tag}.unanswered")
    result: dict[str, Any] = {"source_set": family, "member_value": value}
    result["member_value"] = value
    for name, r in (("answered", answered), ("unanswered", unanswered)):
        if "error" in r:
            result[name] = {"error": r["error"], "declarations_removed": r["declarations_removed"]}
    if "error" in answered or "error" in unanswered:
        result["verdict"] = "member not recordable here (see error)"
        return result
    bp = base_run["pubs"]
    # Only bound fields downstream of this source set's subtotal are attributed to it; a
    # harness that adds companions or a second family moves other lines too.
    downstream = DOWNSTREAM.get(family, set(FIELDS))
    moved_all = sorted(s for s in FIELDS if _val(answered["pubs"], s) != _val(bp, s))
    moved = [s for s in moved_all if s in downstream]
    result["moved_lines_not_downstream_of_this_set"] = [_short(s) for s in moved_all if s not in downstream]
    # Only a line the answered return publishes can be compared with the unanswered one.
    comparable = [s for s in moved if _val(answered["pubs"], s) is not None]
    gap = [s for s in comparable if _val(unanswered["pubs"], s) == _val(answered["pubs"], s)]
    held = [s for s in comparable if _val(unanswered["pubs"], s) is None]
    other = [s for s in comparable if s not in gap and s not in held]
    unpublished_when_answered = [s for s in moved if _val(answered["pubs"], s) is None]
    result.update({
        "declarations_removed": answered["declarations_removed"],
        "answered_lines_moved_from_base": [_short(s) for s in moved],
        "unanswered_gap_lines": [_short(s) for s in gap],
        "unanswered_held_lines": [_short(s) for s in held],
        "unanswered_other_lines": [_short(s) for s in other],
        "answered_lines_unpublished": [_short(s) for s in unpublished_when_answered],
        "answered_roots": _roots(answered["blocked"]),
        "unanswered_roots": _roots(unanswered["blocked"]),
        "companions_added": answered.get("companions_added", []),
        "answered_blocked_count": len(answered["blocked"]),
        "unanswered_blocked_count": len(unanswered["blocked"]),
        "sample_gap_values": {_short(s): {"base": _val(bp, s), "answered": _val(answered["pubs"], s), "unanswered": _val(unanswered["pubs"], s)} for s in gap[:6]},
    })
    fam_short = _short(family)

    def closure_roots(r: dict[str, Any]) -> list[dict[str, Any]]:
        return [x for x in _roots(r["blocked"]) if x["code"] == "SOURCE_SET_UNCLOSED" and fam_short in x["missing"]]

    result["closure_block_answered_run"] = closure_roots(answered)
    result["closure_block_unanswered_run"] = closure_roots(unanswered)
    if not comparable:
        if closure_roots(unanswered) and not closure_roots(answered):
            result["verdict"] = ("held (by root block only): the answered return is incomplete for other reasons, "
                                 "but the unanswered closure blocks " + ", ".join(x["rule"] for x in closure_roots(unanswered)))
        elif not closure_roots(unanswered):
            result["verdict"] = ("no closure block fires and no value compared: nothing blocks SOURCE_SET_UNCLOSED on this "
                                 "set although it is unanswered, but the member moves no bound line in this scenario "
                                 "(or the answered return is incomplete for other reasons); see the survey for the static guard")
        else:
            result["verdict"] = "inconclusive: the answered return publishes no moved bound line (see answered_roots)"
    elif gap:
        result["verdict"] = "GAP: unanswered closure publishes the partial sum on bound lines"
    else:
        result["verdict"] = "held: unanswered closure keeps every moved bound line from publishing"
    return result


def main() -> None:
    survey = json.loads((HERE / "survey-output.json").read_text())
    wanted = sys.argv[1:]
    sets: list[str] = []
    for e in survey["inventory"]:
        if e["source_set"] not in sets:
            sets.append(e["source_set"])
    for e in survey["collects_guarded_at_their_own_site"]:
        if e["source_set"] not in sets and e["source_set"] in FAMS:
            sets.append(e["source_set"])   # collects the survey found guarded at their own site
    sets += [c for c in CONTROLS if c not in sets]
    if wanted:
        sets = [s for s in sets if s in wanted or s.replace("tax.us.2025.", "") in wanted]
    base = run(base_return(), "demo.p0.cs.base")
    assert "error" not in base and not base["blocked"], base.get("error")
    cases: list[dict[str, Any]] = []
    prior = {}
    if OUT_PATH.exists() and wanted:
        prior = {c["source_set"]: c for c in json.loads(OUT_PATH.read_text())["cases"]}
    for ss in sets:
        print("case", ss, flush=True)
        fam = FAMS.get(ss)
        if fam is None:
            cases.append({"source_set": ss, "verdict": "source set is not a declared family"})
            continue
        if ss in ("tax.us.2025.w2-box4", "tax.us.2025.w2-box6"):
            pb = run(roster_return(base_return(), ss, 1, close=True, n_children=3), "demo.p0.cs.part2b.base")
            cases.append(case(ss, 1000.0, pb, builder=part_ii_b_return))
            merged = {**prior, **{c["source_set"]: c for c in cases}}
            OUT_PATH.write_text(json.dumps({"core": "v61", "cases": list(merged.values())}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            continue
        if ss in ROSTERS:
            cases.append(case(ss, "yes", base, builder=roster_return))
            merged = {**prior, **{c["source_set"]: c for c in cases}}
            OUT_PATH.write_text(json.dumps({"core": "v61", "cases": list(merged.values())}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            continue
        ftype = FT[fam["member_predicate"]["fact_type"]]
        vtype = ftype["value_schema"].get("type")
        if vtype != "number":
            cases.append({"source_set": ss, "verdict": f"deferred: member value type {vtype}"})
            continue
        cases.append(case(ss, 1000.0, base))
        merged = {**prior, **{c["source_set"]: c for c in cases}}
        OUT_PATH.write_text(json.dumps({"core": "v61", "cases": list(merged.values())}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    merged = {**prior, **{c["source_set"]: c for c in cases}}
    OUT_PATH.write_text(json.dumps({"core": "v61", "cases": list(merged.values())}, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
