"""Track 0 adversarial closure runs for sales with no Form 1099-B (boxes C and F).

Evidence for track0-closure.md. Builds the scratch core v80 of
cf_prototype.py (with Decision 3 and the Track 0 repairs) in each worker
process, and runs every case through live_coordinate_run. Nothing under
packages/ is written. Writes track0-output.json beside this file.

    python3 docs/phases/engine-breadth/milestones/f8949-boxes-cf-evidence/track0.py [workers]

Two designs are built. ``final`` is cf_prototype.REPAIRS as committed.
``decided`` is Decisions 1-3 with no Track 0 repair; it runs only the cases
that show the counterexample a repair fixes.
"""

from __future__ import annotations

import atexit
import copy
import json
import shutil
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import cf_prototype as cfp  # noqa: E402

cp = cfp.cp
probe, proto, p0b = cp.probe, cp.proto, cp.p0b
P = cfp.P
OUT = HERE / "track0-output.json"
Acts = list[dict[str, Any]]
FIELDS = tuple(P + name for name in (
    "schedule-d.line-2", "schedule-d.line-3", "schedule-d.line-7", "schedule-d.line-9", "schedule-d.line-10",
    "schedule-d.line-15", "schedule-d.line-16", "schedule-d.line-21", "form1040.line-7a",
))
WATCHED = ("schedule-d", "line7a", "preferential", "attachment.f8949", "f8949.no1099b", "f1099b.noncovered")


# ---- case builders --------------------------------------------------------

V79CLS = {"q1": "yes", "q2": "no", "form8949": "no", "path_b": "no", "old_ic": "yes"}
CLS = {"q1": "no", "q2": "yes", "form8949": "no", "path_b": "no", "new_ic": "yes"}


def ret(fn: Callable[[Acts], Any] | None = None, **kw: Any) -> Callable[[], Acts]:
    return lambda: cfp.v80_return(sales=fn, **kw)


def shared_transaction(acts: Acts) -> None:
    """Two box B sales on different statements that reuse one transaction entity.

    The first has every amount. The second has proceeds only. Pairing on the
    transaction key alone would let the first sale's basis row cover the second.
    """
    cp.on_be(acts, "st", 3000.0, 1000.0, "shr1")
    fam = proto._family_id("st", None)
    value = {"proceeds": 2000.0, "basis": 5000.0, "basis_reported_to_irs": "no", "long_term": "no",
             "wash_disallowed": 0}
    for family_id, val in ((fam, value), (proto._family_id("st", "proceeds"), 2000.0)):
        record_shared(acts, family_id, val, "shr2", transaction="demo.ns.shr1.transaction")


def record_shared(acts: Acts, family_id: str, value: object, tag: str, *, transaction: str) -> None:
    from packages.kernel.facts import fact_id_for
    from tests.test_refund_or_amount_owed_track1 import _attested

    fact = proto.BUILT["facts"][proto.BUILT["member_of"][family_id]]
    declared = []
    for key in fact["identity_keys"]:
        if key["kind"] != "entity":
            declared.append((key["name"], key["values"][0]))
            continue
        entity = transaction if key["name"] == "transaction" else f"demo.ns.{tag}.{key['name']}"
        if not proto._known_entity(acts, entity):
            probe._introduce(acts, entity, key["entity_kind"])
        declared.append((key["name"], entity))
    head = probe.horizons(acts, family_id)[-1]
    slug = family_id.removeprefix(P + "f1099b.")
    probe._add(acts, "member-transition", {
        "family": {"id": family_id, "version": "v1"},
        "scope": {"tax-year": probe.YEAR, "subject": "demo.primary"},
        "member": {"action": "assert", "finding": _attested(
            f"demo.ns.{tag}.{slug}.member", fact_id_for(fact["id"], tuple(declared)), value)},
        "successor": {"id": f"demo.ns.{tag}.{slug}.h1", "predecessor": head},
    })


def orphan_basis(acts: Acts) -> None:
    """A full box B sale, and a basis row on another identity with no sale object (ADR-0082 presence pair)."""
    cp.on_be(acts, "st", 3000.0, 1000.0, "orp1")
    proto._record(acts, proto._family_id("st", "basis"), 4000.0, "orp2")


def c_w_scalar_only(acts: Acts) -> None:
    """A box C gain whose sale object carries no wash amount, with a wash-sale adjustment row of 500."""
    cfp.cf_sale(acts, "st", 6000.0, 2000.0, "cwso", scalars=("proceeds", "basis"))
    cfp.record(acts, "st", "adjustment", 500.0, "cwso")


def c_amounts_disagree(acts: Acts) -> None:
    """The sale object says a 2000/8000 loss with W 1000; the amount rows say 6000/2000 with W 1000."""
    cfp.record(acts, "st", None, {"proceeds": 2000.0, "basis": 8000.0, "long_term": "no", "wash_disallowed": 1000.0},
               "cdis")
    for kind, value in (("proceeds", 6000.0), ("basis", 2000.0), ("adjustment", 1000.0)):
        cfp.record(acts, "st", kind, value, "cdis")


def c_object_wash_no_row(acts: Acts) -> None:
    """A box C loss whose sale object says W 1000 but has no wash-sale adjustment row."""
    cfp.cf_sale(acts, "st", 4000.0, 7000.0, "cowr", adjustment=1000.0, scalars=("proceeds", "basis"))


def b_w_scalar_only(acts: Acts) -> None:
    """The box B version of c_w_scalar_only (inherited from v79)."""
    cp.on_be(acts, "st", 6000.0, 2000.0, "bwso")
    proto._record(acts, proto._family_id("st", "adjustment"), 500.0, "bwso")


def late_yes(reanswer: bool) -> Callable[[], Acts]:
    """q2 yes with a box F sale, then a box C sale (and optionally yes again)."""
    def build() -> Acts:
        acts = cfp.v80_return(sales=lambda a: cfp.cf_sale(a, "lt", 6000.0, 2000.0, "lyf"), **CLS)
        cfp.cf_sale(acts, "st", 2000.0, 8000.0, "lyc")
        if reanswer:
            acts = cfp.say(acts, cfp.Q2, "yes", "lyagain")
        return ccr_renumbered(acts)
    return build


def two_c_one_missing(acts: Acts) -> None:
    cfp.cf_sale(acts, "st", 3000.0, 1000.0, "two1")
    cfp.cf_sale(acts, "st", 2000.0, 5000.0, "two2", scalars=("proceeds",))


def t1(stage: int) -> Callable[[], Acts]:
    """Wage return, new question no, computed; then a box F sale and the answers that follow it."""
    def build() -> Acts:
        acts = cfp.v80_return()
        if stage >= 1:
            cfp.cf_sale(acts, "lt", 6000.0, 2000.0, "t1")
        if stage >= 2:
            acts = cfp.say(acts, cfp.Q2, "yes", "t1q2")
        if stage >= 3:
            acts = probe.answer(ccr_renumbered(acts), cfp.NEW_IC, "yes", "t1ic")
        if stage >= 4:
            acts = probe.boundary(ccr_renumbered(acts), "no", "no")
        return ccr_renumbered(acts)
    return build


def t2(stage: int, old_ic_after: str | None = None) -> Callable[[], Acts]:
    """A v79-style box B return, computed; then a box C sale and the answers that follow it.

    ``old_ic_after`` corrects the v79 in-class answer at the end. It is false once a box C sale exists.
    """
    def build() -> Acts:
        acts = cfp.v80_return(sales=lambda a: cp.on_be(a, "st", 3000.0, 3500.0, "t2b"), **V79CLS)
        if stage >= 1:
            cfp.cf_sale(acts, "st", 2500.0, 1000.0, "t2c")
        if stage >= 2:
            acts = cfp.say(acts, cfp.Q2, "yes", "t2q2")
        if stage >= 3:
            acts = probe.answer(ccr_renumbered(acts), cfp.NEW_IC, "yes", "t2ic")
        if old_ic_after is not None:
            acts = probe.answer(ccr_renumbered(acts), cfp.OLD_IC, old_ic_after, "t2oic")
        return ccr_renumbered(acts)
    return build


def ccr_renumbered(acts: Acts) -> Acts:
    return cfp.ccr._renumbered(acts)


def track0_cases() -> dict[str, Callable[[], Acts]]:
    b_full = lambda a: cp.on_be(a, "st", 2000.0, 8000.0, "bl")  # noqa: E731
    e_full = lambda a: cp.on_be(a, "lt", 6000.0, 2000.0, "eg")  # noqa: E731
    f_full = lambda a: cfp.cf_sale(a, "lt", 6000.0, 2000.0, "fg")  # noqa: E731
    c_full = lambda a: cfp.cf_sale(a, "st", 2000.0, 8000.0, "cl")  # noqa: E731
    cases: dict[str, Callable[[], Acts]] = {
        # Decision 3 on lines 2 and 9.
        "d3_b_loss": ret(b_full, **V79CLS),
        "d3_b_basis_missing": ret(lambda a: cp.on_be(a, "st", 2000.0, 8000.0, "bnb", scalars=("proceeds",)), **V79CLS),
        "d3_b_proceeds_missing": ret(lambda a: cp.on_be(a, "st", 2000.0, 8000.0, "bnp", scalars=("basis",)), **V79CLS),
        "d3_e_basis_missing": ret(lambda a: cp.on_be(a, "lt", 6000.0, 2000.0, "enb", scalars=("proceeds",)), **V79CLS),
        "d3_e_proceeds_missing": ret(lambda a: cp.on_be(a, "lt", 6000.0, 2000.0, "enp", scalars=("basis",)), **V79CLS),
        "d3_b_code_w_on_gain": ret(lambda a: cp.on_be(a, "st", 6000.0, 2000.0, "bw", adjustment=500.0), **V79CLS),
        "d3_b_shared_transaction": ret(shared_transaction, **V79CLS),
        "d3_c_two_sales_one_missing": ret(two_c_one_missing, **CLS),
        "d3_b_orphan_basis": ret(orphan_basis, **V79CLS),
        "w_c_scalar_only_on_gain": ret(c_w_scalar_only, **CLS),
        "w_c_amounts_disagree": ret(c_amounts_disagree, **CLS),
        "w_c_object_wash_no_row": ret(c_object_wash_no_row, **CLS),
        "w_b_scalar_only_on_gain": ret(b_w_scalar_only, **V79CLS),
        "dup_b_and_c_ic_yes": ret(lambda a: [b_full(a), c_full(a)] and None,
                                  **{**V79CLS, "q2": "yes", "new_ic": "yes"}),
        "dup_b_and_c_ic_no": ret(lambda a: [b_full(a), c_full(a)] and None,
                                 **{**V79CLS, "q2": "yes", "new_ic": "no"}),
        "q2_late_yes_stale": late_yes(False),
        "q2_late_yes_reanswered": late_yes(True),
        # Empty/nonempty matrix. Default Form 8949 answer is the harness "yes" (no Form 8949 sources).
        "m_no_no": ret(),
        "m_no_unanswered": ret(q2=None),
        "m_unanswered_no": ret(q1=None),
        "m_yes_nothing_no": ret(q1="yes"),
        "m_no_yes_nothing": ret(q2="yes"),
        "m_yes_yes_nothing": ret(q1="yes", q2="yes"),
        "m_yes_nothing_no_old_ic_yes": ret(q1="yes", old_ic="yes"),
        "m_no_no_8949no": ret(form8949="no", path_b="no"),
        "m_no_no_8949no_pathb_yes": ret(form8949="no", path_b="yes"),
        "m_no_no_8949no_old_ic_yes": ret(form8949="no", path_b="no", old_ic="yes"),
        "m_no_no_8949no_new_ic_yes": ret(form8949="no", path_b="no", new_ic="yes"),
        "m_yes_nothing_no_8949no_old_ic_yes": ret(q1="yes", form8949="no", path_b="no", old_ic="yes"),
        "m_b_yes_no": ret(b_full, **V79CLS),
        "m_b_old_ic_no": ret(b_full, **{**V79CLS, "old_ic": "no"}),
        "m_b_q1_no_with_member": ret(b_full, **{**V79CLS, "q1": "no"}),
        "m_c_no_yes": ret(c_full, **CLS),
        "m_c_new_ic_no": ret(c_full, **{**CLS, "new_ic": "no"}),
        "m_c_q2_no_with_member": ret(c_full, **{**CLS, "q2": "no"}),
        "m_e_yes_q2_yes_nothing": ret(e_full, **{**V79CLS, "q2": "yes", "new_ic": "yes"}),
        "m_f_q1_yes_nothing": ret(f_full, **{**CLS, "q1": "yes"}),
        "m_bf_yes_yes": ret(lambda a: [b_full(a), f_full(a)] and None, **{**CLS, "q1": "yes"}),
        "m_c_8949_yes_pathb_no": ret(c_full, q1="no", q2="yes", new_ic="yes", path_b="no"),
        "m_c_8949_yes": ret(c_full, q1="no", q2="yes", new_ic="yes"),
        "m_b_8949_yes": ret(b_full, q1="yes", q2="no", old_ic="yes"),
    }
    for n in range(5):
        cases[f"t1_stage{n}"] = t1(n)
    for n in range(4):
        cases[f"t2_stage{n}"] = t2(n)
    cases["t2_stage3_old_ic_no"] = t2(3, "no")
    return cases


# Cases whose counterexample a Track 0 repair fixes, run again on the decided design.
DECIDED = ("m_yes_nothing_no", "m_yes_nothing_no_old_ic_yes", "m_yes_yes_nothing", "m_f_q1_yes_nothing", "m_no_no_8949no_old_ic_yes",
           "m_no_no_8949no_new_ic_yes", "d3_b_shared_transaction", "d3_b_basis_missing", "m_no_no", "d3_b_loss",
           "m_c_8949_yes", "m_b_8949_yes", "t1_stage3", "w_c_scalar_only_on_gain", "w_c_amounts_disagree",
           "w_c_object_wash_no_row", "w_b_scalar_only_on_gain", "c_basis_missing", "c_wash", "mixed_abcf")


# ---- worker ---------------------------------------------------------------


STATE: dict[str, Any] = {}


def summarize(outcome: Any) -> dict[str, Any]:
    summary = ORIGINAL_SUMMARIZE(outcome)
    if outcome.refusal is not None:
        return summary
    report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
    rows = []
    for row in report.get("dispositions") or []:
        artifact = str(row.get("artifact_id", ""))
        if any(w in artifact for w in WATCHED):
            rows.append([artifact.removeprefix(P), row.get("version"), row.get("disposition"), row.get("code"),
                         [str(m).removeprefix(P) for m in (row.get("missing") or [])][:4]])
    summary["dispositions"] = sorted(rows)
    model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    sentences: list[str] = []
    fields: dict[str, Any] = {}
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        resolved = section.get("resolved") or {}
        reasons = [probe.scrub(str(r["sentence"])) for r in resolved.get("reasons") or []
                   if isinstance(r, dict) and r.get("sentence")]
        sentences += [s for s in reasons if s not in sentences]
        if field.get("id") in FIELDS:
            explain = ((field.get("dispositions") or {}).get(str(resolved.get("disposition"))) or {}).get("explain")
            fields[str(field["id"]).removeprefix(P)] = {
                "disposition": resolved.get("disposition"), "value": resolved.get("value"),
                "explain": explain, "reasons": reasons}
    summary["questions"] = [s for s in sentences if s.endswith("?")]
    summary["fields"] = fields
    return summary


ORIGINAL_SUMMARIZE = cp.summarize


def init(repairs: list[str]) -> None:
    cfp.REPAIRS.clear()
    cfp.REPAIRS.update(repairs)
    cp.TEXT_LINES = FIELDS
    cp.summarize = summarize
    cp.pin_v79()
    cp.install_v79_noncovered()
    tmp = tempfile.mkdtemp(prefix="cf-t0-")
    atexit.register(shutil.rmtree, tmp, True)
    STATE["build"] = cfp.build(Path(tmp).resolve() / "scratch", write_rules=False)
    STATE["new"] = {**cfp.new_cases(), **track0_cases()}


def v79_case(name: str) -> Acts:
    if "v79" not in STATE:
        cases = cfp.v79_cases()
        acts = cp.opened()
        cp.on_be(acts, "st", 2000.0, 8000.0, "b8949y")
        cases["t0_b_loss_8949_yes"] = cp.answered(acts, q1="yes", form8949="yes", other=None, in_class="yes", tag="b8949y")
        cases["t0_q1_yes_nothing"] = p0b._with_answer(cfp.ccr.base_return(), "yes")
        bw = cp.opened()
        b_w_scalar_only(bw)
        cases["t0_b_w_scalar_only_on_gain"] = cp.answered(bw, q1="yes", in_class="yes", tag="bwso")
        cases["t0_8949no_old_ic_yes_q1_no"] = cp.answered(cp.opened(), q1="no", form8949="no", other="no",
                                                          in_class="yes", tag="oicq1no")
        STATE["v79"] = cases
    return STATE["v79"][name]


def run(task: tuple[str, str]) -> tuple[tuple[str, str], dict[str, Any]]:
    kind, name = task
    if kind == "new":
        cfp.pin("v80")
        result = cp.execute(STATE["new"][name], f"demo.cf.t0.{name}")
        return task, {"result": cfp.trim(result) | {"dispositions": result.get("dispositions"),
                                                    "fields": result.get("fields")},
                      "mismatch": cfp.check(name, result)}
    acts = v79_case(name)
    if kind == "c79":
        cfp.pin("v79")
        return task, cp.execute(lambda: acts, f"demo.cf.t0c79.{name}")
    cfp.pin("v80")
    answer = "no" if kind == "c80" else None
    return task, cp.execute(lambda: cfp.with_q2(acts, answer), f"demo.cf.t0{kind}.{name}")


# ---- static integration surface ------------------------------------------


def surface(content: Path) -> dict[str, Any]:
    package = json.loads((content / "package.core-calculations.v80.json").read_text(encoding="utf-8"))
    wanted = {(m["id"], m["version"]) for m in package["members"]}
    bodies: dict[tuple[str, str], dict[str, Any]] = {}
    for path in content.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and (body.get("id"), body.get("version")) in wanted:
            bodies[(body["id"], body["version"])] = body
    symbols = [P + s for s in ("schedule-d.line-2", "schedule-d.line-3", "schedule-d.line-7", "schedule-d.line-9",
                               "schedule-d.line-10", "schedule-d.line-15", "schedule-d.line-16", "schedule-d.line-21",
                               "capital-gains.line7a-total", "capital-gains.selected-preferential-base")]
    symbols += [body["publishes"] for (mid, _v), body in sorted(bodies.items())
                if mid in (P + "rule.attachment.f8949", P + "rule.attachment.schedule-d")]
    out: dict[str, Any] = {"members_resolved": len(bodies), "members_listed": len(wanted)}
    for symbol in symbols:
        publishers, fields, consumers = [], [], []
        for (mid, ver), body in sorted(bodies.items()):
            tag = f"{mid.removeprefix(P)} {ver} ({body.get('schema')})"
            if body.get("publishes") == symbol:
                publishers.append(tag)
            elif body.get("binds_symbol") == symbol:
                fields.append(tag)
            elif cfp.mentions({k: v for k, v in body.items() if k not in ("id", "notes")}, symbol):
                consumers.append(tag)
        out[symbol.removeprefix(P)] = {"publishers": publishers, "form_fields": fields, "consumers": consumers}
    return out


# ---- main -----------------------------------------------------------------


KEEP_ROWS = ("rule.schedule-d-line", "rule.form1040-line7a", "rule.selected-preferential-base", "rule.attachment.")


def compact(payload: dict[str, Any]) -> dict[str, Any]:
    """Drop what ``fields`` and ``dispositions`` already carry, and the subtotal rows."""
    for section in ("v80_cases", "decided_design"):
        for case in payload.get(section, {}).values():
            result = case["result"]
            result.pop("line_text", None)
            result.pop("blocked", None)
            result.pop("seconds", None)
            if result.get("dispositions"):
                result["dispositions"] = [row for row in result["dispositions"]
                                          if row[0].startswith(KEEP_ROWS) or row[0].endswith(".amounts-check")]
    return payload




def main() -> None:
    if sys.argv[1:] == ["surface"]:  # rebuild and refresh only the static integration surface
        cp.pin_v79()
        cp.install_v79_noncovered()
        with tempfile.TemporaryDirectory() as tmp:
            cfp.build(Path(tmp).resolve() / "scratch", write_rules=False)
            payload = json.loads(OUT.read_text(encoding="utf-8"))
            payload["surface"] = surface(Path(tmp).resolve() / "scratch" / "content")
        OUT.write_text(probe.scrub(json.dumps(payload, indent=1, sort_keys=True, default=str)) + "\n", encoding="utf-8")
        return
    if sys.argv[1:2] == ["only"]:  # run the named v80 cases on the final design and merge them
        init(sorted(cfp.REPAIRS))
        payload = json.loads(OUT.read_text(encoding="utf-8"))
        for token in sys.argv[2:]:  # name (a v80 case) or c79:name (a v79 return on v79)
            kind, _, name = token.rpartition(":")
            if kind:
                payload.setdefault("extra_v79", {})[name] = run((kind, name))[1]
            else:
                payload["v80_cases"][name] = run(("new", name))[1]
        OUT.write_text(probe.scrub(json.dumps(compact(payload), indent=1, sort_keys=True, default=str)) + "\n",
                       encoding="utf-8")
        return
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    cp.pin_v79()
    cp.install_v79_noncovered()
    origin = (probe.CONTENT, probe.RELEASE_DIR)
    with tempfile.TemporaryDirectory() as tmp:
        build = cfp.build(Path(tmp).resolve() / "scratch", write_rules=True)
        static = surface(Path(tmp).resolve() / "scratch" / "content")
    probe.CONTENT, probe.RELEASE_DIR = origin
    cp.pin_v79()
    STATE.clear()
    new_names = list({**cfp.new_cases(), **track0_cases()})
    v79_names = sorted(cfp.v79_cases()) + ["t0_b_loss_8949_yes", "t0_q1_yes_nothing", "t0_8949no_old_ic_yes_q1_no",
                                           "t0_b_w_scalar_only_on_gain"]
    tasks = [("new", n) for n in new_names] + [(k, n) for n in v79_names for k in ("c79", "c80", "u80")]
    results: dict[str, Any] = {}
    with ProcessPoolExecutor(workers, initializer=init, initargs=(sorted(cfp.REPAIRS),)) as pool:
        for (kind, name), result in pool.map(run, tasks):
            results.setdefault(kind, {})[name] = result
            print(kind, name, (result.get("mismatch") if kind == "new" else cfp.form1040(result)), flush=True)
    with ProcessPoolExecutor(min(workers, len(DECIDED)), initializer=init, initargs=([],)) as pool:
        for (_kind, name), result in pool.map(run, [("new", n) for n in DECIDED]):
            results.setdefault("decided", {})[name] = result
            print("decided", name, flush=True)
    carry = {}
    for name in v79_names:
        before, after, untouched = results["c79"][name], results["c80"][name], results["u80"][name]
        carry[name] = {
            "v79": {"form1040": cfp.form1040(before), "attachments": before.get("attachments"),
                    "error": before.get("error")},
            "v80_q2_no_diff": cfp.compare(before, after),
            "v80_q2_no_lines_3_10": {k: (after.get("lines") or {}).get(k)
                                     for k in ("schedule-d.line-3", "schedule-d.line-10")},
            "v80_q2_no_questions": after.get("questions"),
            "v80_q2_unanswered_form1040": cfp.form1040(untouched),
            "v80_q2_unanswered_questions": untouched.get("questions"),
        }
    payload = {"source_ref": "eb02b548", "repairs": sorted(cfp.REPAIRS), "build": build, "surface": static,
               "v80_cases": results["new"], "decided_design": results.get("decided", {}),
               "v79_returns_on_v80": carry}
    OUT.write_text(probe.scrub(json.dumps(compact(payload), indent=1, sort_keys=True, default=str)) + "\n",
                   encoding="utf-8")
    print(f"wrote {OUT.name}", flush=True)


if __name__ == "__main__":
    main()
