"""Adversarial closure for blocks that declare the names they wait on.

The scratch core is built by prototype.py outside the repository.  Every
behavior row below is one synthetic ``live_coordinate_run`` on published v87
and on that scratch successor.

    python3 track0.py authority <scratch-core.json>
    python3 track0.py matrix <scratch-core.json>
    python3 track0.py late <scratch-core.json>
    python3 track0.py reuse <scratch-core.json>
    python3 track0.py neighbour
    python3 track0.py surface
    python3 track0.py trace <scratch-core.json>
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import common  # noqa: E402
import probe  # noqa: E402
import prototype  # noqa: E402

P = common.P
h = common.harness()
Acts = common.Acts

NO_8949 = P + "schedule-d-boundary.no-form8949-sources"
PATH_B = P + "schedule-d-boundary.no-other-form8949-adjustments"

BUILDERS: dict[str, Callable[[], Acts]] = {
    case_id: build for case_id, (_group, build, _note) in probe.CASES.items()
    if _group != "internal-subtotal"
}

HAND: dict[str, dict[str, Any]] = {
    "sd_yes_nothing": {"schedule-d.line-2": -6000, "schedule-d.line-7": -6000,
                         "schedule-d.line-21": 3000},
    "sd_8949_no_unadmitted": {"schedule-d.line-3": -6000, "schedule-d.line-7": -6000,
                                "schedule-d.line-21": 3000},
    "sd_sale_beside_8949_yes": {"schedule-d.line-3": -6000},
    "sd_amounts_disagree": {"schedule-d.line-3": -6000},
    "sd_path_b_unanswered": {"schedule-d.line-3": -6000, "schedule-d.line-21": 3000},
    "codeb_yes_nothing": {"schedule-d.line-1b": 6000},
    "codeb_sale_beside_8949_yes": {"schedule-d.line-1b": 6000},
    "codeb_amounts_disagree": {"schedule-d.line-1b": 6000},
    "wash_adjustment_open": {"schedule-d.line-1b": -5000},
}


def run(core: Any, acts: Acts, run_id: str, *, scratch: bool) -> dict[str, Any]:
    if scratch:
        with prototype.block_missing_runtime():
            result = common.run(core, acts, run_id, schemas=prototype.PrototypeSchemas())
    else:
        result = common.run(core, acts, run_id)
    return probe.public(result)


def run_full(core: Any, acts: Acts, run_id: str, *, scratch: bool) -> dict[str, Any]:
    if scratch:
        with prototype.block_missing_runtime():
            return common.run(core, acts, run_id, schemas=prototype.PrototypeSchemas())
    return common.run(core, acts, run_id)


def both(core_path: Path, acts: Acts, tag: str) -> dict[str, Any]:
    return {
        "v87": run(common.v87(), acts, f"demo.bnq.t0.v87.{tag}", scratch=False),
        "scratch": run(common.scratch(core_path), acts, f"demo.bnq.t0.scratch.{tag}", scratch=True),
    }


def answer(acts: Acts, fact: str, value: Any, tag: str, core_path: Path) -> Acts:
    return h.say(acts, fact, value, tag, common.scratch(core_path).content)


def add_sale(acts: Acts, kind: str, term: str, tag: str, *, rows: dict[str, float | None] | None = None) -> Acts:
    if kind == "codeb":
        acts = h.sale(acts, kind, term, proceeds=10000, basis=7000, corrected=4000,
                      tag=tag, rows=rows)
        acts = probe.answered(acts, q3="yes", form8949="no", path_b="no", ic81="yes",
                              exc1_only_2a="no")
        return probe.statement_answers(acts)
    acts = h.sale(acts, kind, term, proceeds=2000, basis=8000, tag=tag, rows=rows)
    key = "q1" if kind == "noncovered" else "q2"
    in_class = "ic79" if kind == "noncovered" else "ic80"
    acts = probe.answered(acts, **{key: "yes", "form8949": "no", "path_b": "no",
                                      in_class: "yes", "exc1_only_2a": "no", "exc1_no_losses": "no"})
    return probe.statement_answers(acts) if kind == "noncovered" else acts


def close_family(acts: Acts, family: str, tag: str) -> Acts:
    acts = h.strip(acts, family + ".source-closure")
    h._close(acts, family + ".source-closure", h.horizons(acts, family)[-1], f"demo.bnq.t0.{tag}.close")
    return h.renumber(acts)


def correct_member(acts: Acts, fact_fragment: str, value: Any, tag: str) -> Acts:
    fact_id = None
    for act in acts:
        payload = act.get("payload") or {}
        member = payload.get("member") if isinstance(payload, dict) else None
        finding = member.get("finding") if isinstance(member, dict) else None
        if isinstance(finding, dict) and fact_fragment in str(finding.get("fact_id")):
            fact_id = str(finding["fact_id"])
    if fact_id is None:
        raise KeyError(fact_fragment)
    out = copy.deepcopy(acts)
    h._add(out, "assertion", {"finding": h._attested(f"demo.bnq.t0.{tag}", fact_id, value)})
    return h.renumber(out)


def statement_box4_zero(acts: Acts) -> Acts:
    out = copy.deepcopy(acts)
    h.adopt(out, "f1099b-box4.bundle.json")
    statements = [str(act["payload"]["entity"]["id"]) for act in out
                  if act.get("kind") == "entity-introduced"
                  and act["payload"]["entity"].get("kind") == "tax.us.f1099b-statement"]
    for statement in dict.fromkeys(statements):
        fact_id = h.fact_id_for(P + "f1099b.statement-box4-withholding",
                                (("statement", statement), ("tax-year", h.YEAR)))
        h._add(out, "assertion", {"finding": h._attested(
            f"demo.bnq.t0.box4-zero.{statement}", fact_id, 0)})
    return h.renumber(out)


def statement_reported_no(acts: Acts, statement: str, tag: str) -> Acts:
    out = copy.deepcopy(acts)
    for slug in ("statement-box4-withholding-reported", "statement-box7-loss-not-allowed"):
        fact_id = h.fact_id_for(P + "f1099b." + slug,
                                (("statement", statement), ("tax-year", h.YEAR)))
        h._add(out, "assertion", {"finding": h._attested(
            f"demo.bnq.t0.{tag}.{slug}", fact_id, "no")})
    return h.renumber(out)


def resolved(case_id: str, core_path: Path) -> Acts:
    acts = BUILDERS[case_id]()
    if case_id == "sd_yes_nothing":
        return statement_box4_zero(add_sale(acts, "noncovered", "st", "resolved-sd-yes"))
    if case_id == "sd_8949_no_unadmitted":
        return add_sale(acts, "no1099b", "st", "resolved-sd-unadmitted")
    if case_id in {"sd_sale_beside_8949_yes", "codeb_sale_beside_8949_yes"}:
        acts = answer(acts, NO_8949, "no", case_id + "-no8949", core_path)
        return statement_box4_zero(acts)
    if case_id == "sd_amounts_disagree":
        return correct_member(acts, "f8949.no1099b-st-txn.basis|", 8000, "correct-basis")
    if case_id == "sd_path_b_unanswered":
        return answer(acts, PATH_B, "no", "path-b-truthful-no", core_path)
    if case_id == "codeb_yes_nothing":
        return statement_box4_zero(add_sale(acts, "codeb", "st", "resolved-codeb-yes"))
    if case_id == "codeb_amounts_disagree":
        return statement_box4_zero(correct_member(
            acts, "f1099b.code-b-st-txn.adjustment|", 3000, "correct-adjustment"))
    if case_id == "exception1_personal_loss_8949":
        return answer(acts, PATH_B, "no", "personal-loss-path-b", core_path)
    if case_id == "wash_adjustment_open":
        return statement_box4_zero(close_family(
            acts, P + "f1099b.covered-w-st-adjustment", "wash-resolved"))
    raise KeyError(case_id)


def hand_failures(result: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    failures = []
    for field, wanted in expected.items():
        got = (result.get("lines") or {}).get(field)
        if got != wanted:
            failures.append(f"{field}: hand {wanted!r}, live {got!r}")
    return failures


def iter_blocks(value: Any, path: str = "") -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if value.get("op") == "block" and value.get("missing"):
            found.append({"path": path or "/", "code": value["code"], "missing": value["missing"]})
        for key, child in value.items():
            found.extend(iter_blocks(child, path + "/" + key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(iter_blocks(child, path + f"/{index}"))
    return found


def member_body(core: Any, member: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    slug = str(member["id"]).removeprefix(P + "rule.")
    for name in (f"rule.{slug}.{member['version']}.json", f"rule.{slug}.json"):
        path = core.content / name
        if path.exists():
            body = json.loads(path.read_text(encoding="utf-8"))
            if body.get("version") == member["version"]:
                return name, body
    raise KeyError(member["id"])


def resolver_catalog(core: Any) -> dict[str, dict[str, Any]]:
    package = json.loads(core.package_path.read_text(encoding="utf-8"))
    found: dict[str, dict[str, Any]] = {}
    for member in package["members"]:
        role = member.get("role")
        if role not in {"input-question", "source-closure-mapping"}:
            continue
        stem = str(member["id"]).removeprefix(P)
        candidates = [f"{stem}.{member['version']}.json", f"{stem}.json"]
        for name in candidates:
            path = core.content / name
            if not path.exists():
                continue
            body = json.loads(path.read_text(encoding="utf-8"))
            if body.get("version") != member["version"]:
                continue
            if role == "input-question":
                found[str(body["fact_type"]["id"])] = {
                    "kind": role, "citizen": str(body["id"]), "question": body["question"]}
            else:
                names = [body.get("family"), body.get("closure_fact_type"), body.get("fact_type")]
                for item in names:
                    key = item.get("id") if isinstance(item, dict) else item
                    if key:
                        found[str(key)] = {"kind": role, "citizen": str(body["id"]),
                                           "question": body.get("question") or body.get("closure_question")}
            break
    return found


def declarations(core: Any) -> list[dict[str, Any]]:
    package = json.loads(core.package_path.read_text(encoding="utf-8"))
    old_package = json.loads(common.v87().package_path.read_text(encoding="utf-8"))
    old_versions = {member["id"]: member["version"] for member in old_package["members"]}
    rows = []
    for member in package["members"]:
        if (member.get("role") != "computation"
                or old_versions.get(member["id"]) == member["version"]):
            continue
        name, body = member_body(core, member)
        for block in iter_blocks(body):
            rows.append({"rule": str(member["id"]), "version": member["version"], "file": name, **block})
    return rows


def long_term_authority_cases() -> dict[str, Acts]:
    no1099 = h.sale(h.opened(), "no1099b", "lt", proceeds=2000, basis=8000,
                    tag="authority-lt-no1099", rows={"basis": 2000})
    no1099 = probe.answered(no1099, q2="yes", form8949="no", path_b="no", ic80="yes",
                                exc1_only_2a="no", exc1_no_losses="no")
    codeb = h.sale(h.opened(), "codeb", "lt", proceeds=10000, basis=7000, corrected=4000,
                   tag="authority-lt-codeb", rows={"adjustment": 2000})
    codeb = probe.statement_answers(probe.answered(
        codeb, q3="yes", form8949="no", path_b="no", ic81="yes", exc1_only_2a="no"))
    wash = h.sale(h.opened(), "w", "lt", proceeds=2000, basis=8000, wash=1000,
                  tag="authority-lt-wash")
    wash = probe.statement_answers(probe.answered(
        wash, form8949="no", path_b="yes", exc1_only_2a="no", exc1_no_losses="no"))
    wash = h.strip(wash, P + "f1099b.covered-w-lt-adjustment.source-closure")
    return {"lt_no1099_basis_disagrees": no1099, "lt_codeb_adjustment_disagrees": codeb,
            "lt_wash_adjustment_open": wash}


def authority(core_path: Path) -> None:
    core = common.scratch(core_path)
    decls = declarations(core)
    catalog = resolver_catalog(core)
    existing = HERE / "track0-authority.json"
    if existing.exists():
        cases = json.loads(existing.read_text(encoding="utf-8"))["cases"]
        refresh = {"sd_yes_nothing", "sd_amounts_disagree", "codeb_yes_nothing",
                   "codeb_sale_beside_8949_yes", "codeb_amounts_disagree", "wash_adjustment_open"}
        for row in cases:
            if row["id"] not in refresh:
                continue
            after = both(core_path, resolved(row["id"], core_path), "authority." + row["id"] + ".answered-fixed")
            failures = hand_failures(after["scratch"], HAND.get(row["id"], {}))
            row.update({"answered": after, "hand_failures": failures,
                        "answered_computes_or_names_next_question": not failures or bool(
                            after["scratch"].get("questions"))})
    else:
        cases = []
        for case_id in BUILDERS:
            unresolved = both(core_path, BUILDERS[case_id](), "authority." + case_id + ".unanswered")
            after = both(core_path, resolved(case_id, core_path), "authority." + case_id + ".answered")
            failures = hand_failures(after["scratch"], HAND.get(case_id, {}))
            alternate_named = bool(after["scratch"].get("questions"))
            cases.append({"id": case_id, "unanswered": unresolved, "answered": after,
                          "hand": HAND.get(case_id), "hand_failures": failures,
                          "answered_computes_or_names_next_question": not failures or alternate_named})
    extra_cases = [{"id": case_id, "runs": both(core_path, acts, "authority." + case_id)}
                   for case_id, acts in long_term_authority_cases().items()]
    names = sorted({str(name) for row in decls for name in row["missing"]})
    life = []
    all_questions = ({q for row in cases for phase in ("unanswered", "answered")
                      for q in row[phase]["scratch"].get("questions", [])}
                     | {q for row in extra_cases for q in row["runs"]["scratch"].get("questions", [])})
    for name in names:
        resolver = catalog.get(name)
        life.append({"name": name, "declared_by": [
            {"rule": row["rule"], "version": row["version"], "path": row["path"], "code": row["code"]}
            for row in decls if name in row["missing"]],
            "resolver": resolver,
            "resolver_shown_in_live_case": bool(resolver and resolver.get("question") in all_questions)})
    checks = {
        "eleven_successor_rules": len({row["rule"] for row in decls}) == 11,
        "every_declared_name_has_resolver": all(row["resolver"] for row in life),
        "every_resolver_seen_live": all(row["resolver_shown_in_live_case"] for row in life),
        "all_ten_unanswered_cases_show_question": all(row["unanswered"]["scratch"].get("questions") for row in cases),
        "answered_cases_compute_or_name_next_question": all(row["answered_computes_or_names_next_question"] for row in cases),
    }
    common.write("track0-authority.json", {
        "cores": {"published": "core v87", "scratch": "unchanged successor built by prototype.py"},
        "declaration_count": len(decls), "declared_name_count": len(life),
        "declarations": decls, "authority_lifecycle": life, "cases": cases,
        "long_term_authority_cases": extra_cases,
        "checks": checks, "verdict": "PASS" if all(checks.values()) else "FAIL",
    })
    print(json.dumps(checks, indent=2))


def matrix(core_path: Path) -> None:
    rows = []
    for case_id in BUILDERS:
        phases = {
            "unanswered": both(core_path, BUILDERS[case_id](), "matrix-repair." + case_id + ".unanswered"),
            "truthful_answer": both(core_path, resolved(case_id, core_path),
                                     "matrix-repair." + case_id + ".answered"),
        }
        zero_question_terminal = [phase for phase, pair in phases.items()
                                  if pair["scratch"].get("blocked") and not pair["scratch"].get("questions")]
        failures = hand_failures(phases["truthful_answer"]["scratch"], HAND.get(case_id, {}))
        rows.append({"id": case_id, "phases": phases, "hand": HAND.get(case_id),
                     "hand_failures": failures, "zero_question_terminal": zero_question_terminal,
                     "pass": not zero_question_terminal and (not failures or bool(
                         phases["truthful_answer"]["scratch"].get("questions")))})
    checks = {"ten_cases": len(rows) == 10,
              "twenty_scratch_states": sum(len(row["phases"]) for row in rows) == 20,
              "no_zero_question_terminal": all(not row["zero_question_terminal"] for row in rows),
              "all_cases_pass": all(row["pass"] for row in rows)}
    common.write("track0-matrix.json", {"cases": rows, "checks": checks,
                                         "verdict": "PASS" if all(checks.values()) else "FAIL"})
    print(json.dumps(checks, indent=2))


def late(core_path: Path) -> None:
    traces: list[dict[str, Any]] = []

    start = probe.empty(form8949="yes", path_b="yes")
    added = h.sale(start, "no1099b", "st", proceeds=2000, basis=8000,
                   tag="late-form8949-sale")
    added = probe.answered(added, q2="yes", form8949="yes", path_b="no", ic80="yes",
                           exc1_only_2a="no", exc1_no_losses="no")
    corrected = answer(added, NO_8949, "no", "late-form8949-no", core_path)
    traces.append({"id": "sale_after_form8949_yes", "steps": [
        {"id": "form8949_yes", "runs": both(core_path, start, "late.sale.0")},
        {"id": "sale_added_old_yes", "runs": both(core_path, added, "late.sale.1")},
        {"id": "truthful_no", "runs": both(core_path, corrected, "late.sale.2")},
    ]})

    start = probe.sale("no1099b", rows={"basis": 2000})
    corrected = correct_member(start, "f8949.no1099b-st-txn.basis|", 8000, "late-correct-basis")
    traces.append({"id": "amount_corrected", "steps": [
        {"id": "disagrees", "runs": both(core_path, start, "late.amount.0")},
        {"id": "corrected", "runs": both(core_path, corrected, "late.amount.1")},
    ]})

    start = probe.sale("w", form8949="no", path_b="yes")
    family = P + "f1099b.covered-w-st-adjustment"
    added = h.sale(copy.deepcopy(start), "w", "st", proceeds=500, basis=700, wash=200,
                   tag="late-wash-sale")
    added = statement_reported_no(added, "demo.sfa.late-wash-sale.statement", "late-wash")
    added = h.strip(added, family + ".source-closure")
    reclosed = statement_box4_zero(close_family(copy.deepcopy(added), family, "late-wash"))
    traces.append({"id": "wash_adjustment_after_close", "steps": [
        {"id": "closed", "runs": both(core_path, start, "late.wash.0")},
        {"id": "adjustment_added_open", "runs": both(core_path, added, "late.wash.1")},
        {"id": "reclosed", "runs": both(core_path, reclosed, "late.wash.2")},
    ]})

    for trace in traces:
        trace["pass"] = all(step["runs"]["scratch"].get("outcome") == "success" for step in trace["steps"])
    checks = {"three_traces": len(traces) == 3, "all_steps_live": all(row["pass"] for row in traces),
              "open_steps_name_question": bool(traces[0]["steps"][1]["runs"]["scratch"].get("questions"))
                  and bool(traces[1]["steps"][0]["runs"]["scratch"].get("questions"))
                  and bool(traces[2]["steps"][1]["runs"]["scratch"].get("questions")),
              "resolved_steps_reach_hand_values":
                  traces[0]["steps"][2]["runs"]["scratch"].get("lines", {}).get("schedule-d.line-3") == -6000
                  and traces[1]["steps"][1]["runs"]["scratch"].get("lines", {}).get("schedule-d.line-3") == -6000
                  and traces[2]["steps"][2]["runs"]["scratch"].get("lines", {}).get("schedule-d.line-1b") == -5000}
    common.write("track0-late.json", {"traces": traces, "checks": checks,
                                       "verdict": "PASS" if all(checks.values()) else "FAIL"})
    print(json.dumps(checks, indent=2))


def strip_missing(value: Any) -> Any:
    clean = copy.deepcopy(value)
    if isinstance(clean, dict):
        if clean.get("op") == "block":
            clean.pop("missing", None)
        for key, child in list(clean.items()):
            clean[key] = strip_missing(child)
    elif isinstance(clean, list):
        clean = [strip_missing(child) for child in clean]
    return clean


def changed_paths(old: Any, new: Any, prefix: str = "") -> list[str]:
    if old == new:
        return []
    if isinstance(old, dict) and isinstance(new, dict):
        out = []
        for key in sorted(set(old) | set(new)):
            out.extend(changed_paths(old.get(key), new.get(key), prefix + "/" + key))
        return out
    if isinstance(old, list) and isinstance(new, list) and len(old) == len(new):
        out = []
        for index, (a, b) in enumerate(zip(old, new)):
            out.extend(changed_paths(a, b, prefix + f"/{index}"))
        return out
    return [prefix or "/"]


def normalized_successor(body: dict[str, Any], predecessor_version: str) -> dict[str, Any]:
    clean = strip_missing(body)
    clean["version"] = predecessor_version
    if "rule.f1099b.covered-w-" in str(clean.get("id")) and str(clean.get("id")).endswith("txn.admission-check"):
        path = clean["selection"]["paths"][0]
        closure = next(item for item in path.get("requires", []) if str(item).endswith("adjustment.closure-check"))
        path["requires"] = [item for item in path.get("requires", []) if item != closure]
        path["pins"] = [pin for pin in path.get("pins", []) if pin.get("id") != closure]
        path["value"] = path["value"]["then"]
    if str(clean.get("id")) == P + "rule.form1040-line16":
        clean["when"] = clean["when"]["when"]
    return clean


def reuse(core_path: Path) -> None:
    old = common.v87()
    new = common.scratch(core_path)
    old_package = json.loads(old.package_path.read_text(encoding="utf-8"))
    new_package = json.loads(new.package_path.read_text(encoding="utf-8"))
    old_members = {m["id"]: m for m in old_package["members"]}
    rows = []
    for member in new_package["members"]:
        if member.get("role") != "computation" or member["id"] not in old_members:
            continue
        prior = old_members[member["id"]]
        if prior["version"] == member["version"]:
            continue
        _old_name, old_body = member_body(old, prior)
        _new_name, new_body = member_body(new, member)
        diffs = changed_paths(old_body, normalized_successor(new_body, prior["version"]))
        rows.append({"id": member["id"], "predecessor": prior["version"], "successor": member["version"],
                     "differences_after_authorized_normalization": diffs,
                     "predecessor_equivalent_after_normalization": not diffs,
                     "wash_closure_precheck_normalized": "covered-w-" in str(member["id"])})
    matrix_rows = json.loads((HERE / "track0-matrix.json").read_text(encoding="utf-8"))["cases"]
    sample_runs = [{"id": row["id"], **row["phases"]["unanswered"]} for row in matrix_rows]
    def numeric_lines(result: dict[str, Any]) -> dict[str, int | float]:
        return {name: value for name, value in (result.get("lines") or {}).items()
                if isinstance(value, (int, float)) and not isinstance(value, bool)}

    strict = all(row["predecessor_equivalent_after_normalization"] for row in rows)
    checks = {"eleven_successors": len(rows) == 11,
              "declared_names_add_no_read_pin_dependency_or_answer_change": strict,
              "two_wash_prechecks_separately_normalized": sum(
                  bool(row["wash_closure_precheck_normalized"]) for row in rows) == 2,
              "line16_dead_end_guard_separately_normalized": sum(
                  row["id"] == P + "rule.form1040-line16" for row in rows) == 1,
              "ten_live_inputs_on_both_cores": len(sample_runs) == 10,
              "numeric_values_unchanged": all(
                  numeric_lines(row["v87"]) == numeric_lines(row["scratch"])
                  for row in sample_runs)}
    common.write("track0-reuse.json", {"successors": rows, "live_cases": sample_runs, "checks": checks,
                                        "verdict": "PASS" if all(checks.values()) else "FAIL",
                                        "note": "Wash admission adds a closure-check read; line 16 adds a named block only where the predecessor guard was inapplicable."})
    print(json.dumps(checks, indent=2))


def neighbour() -> None:
    source = json.loads((HERE / "rerun-repair-output.json").read_text(encoding="utf-8"))
    checks = {"all_775_classified": source["distinct_lists"] == 775 and len(source["classes"]) == 775,
              "no_numbers_changed": source["counts"].get("numbers_changed", 0) == 0,
              "no_new_question_on_computed": source["new_question_on_computed_count"] == 0,
              "compares_v87_to_one_scratch_successor": source["cores"] == "published core v87 and one scratch successor after v87"}
    common.write("track0-neighbour.json", {
        "source": "rerun-repair-output.json (published v87 and repaired scratch successor)",
        "distinct_lists": source["distinct_lists"], "live_runs": source["live_runs"],
        "new_shards": source["shards"], "reused_p0_shards": 0,
        "four_shard_cap": source["shards"] <= 4,
        "wall_time_seconds": source["wall_time_seconds"], "counts": source["counts"],
        "counts_by_set": source["counts_by_set"],
        "new_question_on_computed_count": source["new_question_on_computed_count"],
        "classes": source["classes"], "changes": source["changes"], "checks": checks,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
    })
    print(json.dumps(checks, indent=2))


def surface() -> None:
    matrix_body = json.loads((HERE / "track0-matrix.json").read_text(encoding="utf-8"))
    catalogs = [resolver_catalog(common.v87())]
    question_sentences = {str(row.get("question")) for catalog in catalogs
                          for row in catalog.values() if row.get("question")}
    authority_body = json.loads((HERE / "track0-authority.json").read_text(encoding="utf-8"))
    question_sentences |= {str(row["resolver"]["question"])
                           for row in authority_body["authority_lifecycle"] if row.get("resolver")}
    rows = []
    for case in matrix_body["cases"]:
        for phase, pair in case["phases"].items():
            scratch = pair["scratch"]
            blocked = scratch.get("blocked") or []
            shown = sorted({reason for group in blocked for reason in group.get("reasons", [])
                            if reason in question_sentences})
            silent = [field for group in blocked
                      if not any(reason in question_sentences for reason in group.get("reasons", []))
                      for field in group.get("fields", [])]
            reasonless = [field for group in blocked if not group.get("reasons")
                          for field in group.get("fields", [])]
            rows.append({"id": case["id"] + "." + phase, "question_sentences_shown": shown,
                         "blocked_field_count": sum(len(group.get("fields", [])) for group in blocked),
                         "blocked_fields_without_question": silent,
                         "blocked_fields_without_reason": reasonless, "pass": not silent})
    checks = {"twenty_case_states": len(rows) == 20,
              "every_blocked_case_shows_exact_question_sentences": all(
                  not row["blocked_field_count"] or row["question_sentences_shown"] for row in rows),
              "every_reason_sentence_that_is_a_question_uses_a_declared_citizen": all(
                  sentence in question_sentences for row in rows for sentence in row["question_sentences_shown"]),
              "every_blocked_field_names_question": all(row["pass"] for row in rows)}
    common.write("track0-surface.json", {"cases": rows, "checks": checks,
                                         "verdict": "PASS" if all(checks.values()) else "FAIL"})
    print(json.dumps(checks, indent=2))


def source_citation(core: Any, artifact: str, missing: str, code: str | None = None) -> str:
    package = json.loads(core.package_path.read_text(encoding="utf-8"))
    full_id = P + "rule." + artifact
    member = next((row for row in package["members"] if row.get("id") == full_id), None)
    if member is None:
        return "packages/content/tax/2025/<synthesized>:1"
    name, _body = member_body(core, member)
    path = core.content / name
    needles = [missing, P + missing]
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines, 1):
        if any(f'"{needle}"' in line for needle in needles):
            return f"packages/content/tax/2025/{name}:{index}"
    if code:
        for index, line in enumerate(lines, 1):
            if f'"code": "{code}"' in line:
                return f"packages/content/tax/2025/{name}:{index}"
    return f"packages/content/tax/2025/{name}:1"


def unexplainable_roots(result: dict[str, Any], row: dict[str, Any], question_names: set[str],
                        core: Any, seen: frozenset[str] = frozenset()) -> list[dict[str, Any]]:
    by_symbol: dict[str, list[dict[str, Any]]] = {}
    for blocked in result.get("all_blocked") or []:
        if blocked.get("symbol"):
            by_symbol.setdefault(str(blocked["symbol"]), []).append(blocked)
    missing = [str(name) for name in row.get("missing") or []]
    if not missing:
        return [{"rule": row.get("artifact"), "code": row.get("code"), "missing": [],
                 "unexplainable_name": None, "why": "expression or fallback block has empty missing",
                 "source": source_citation(core, str(row.get("artifact")), "", str(row.get("code"))) }]
    roots: list[dict[str, Any]] = []
    for name in missing:
        if name in seen or name in question_names:
            continue
        children = [child for child in by_symbol.get(name, []) if child.get("code")]
        if not children:
            producers = [{key: producer.get(key) for key in ("artifact", "disposition", "code", "missing")}
                         for producer in result.get("all_dispositions") or []
                         if producer.get("symbol") == name]
            roots.append({"rule": row.get("artifact"), "code": row.get("code"),
                          "missing": missing, "unexplainable_name": name,
                          "why": "missing name has no question citizen and no blocked producer",
                          "nonblocked_producers": producers,
                          "source": source_citation(core, str(row.get("artifact")), name,
                                                    str(row.get("code")))})
            continue
        child_roots = [root for child in children
                       for root in unexplainable_roots(result, child, question_names, core, seen | {name})]
        roots.extend(child_roots)
    unique = {json.dumps(root, sort_keys=True): root for root in roots}
    return list(unique.values())


def trace(core_path: Path) -> None:
    cores = {"v87": common.v87(), "scratch": common.scratch(core_path)}
    acts = probe.personal_loss_8949()
    results = {
        "v87": run_full(cores["v87"], acts, "demo.bnq.t0b.trace.v87", scratch=False),
        "scratch": run_full(cores["scratch"], acts, "demo.bnq.t0b.trace.scratch", scratch=True),
    }
    question_names = {
        name: {common.short(key) for key in resolver_catalog(core)}
        for name, core in cores.items()
    }
    failed_surface = json.loads((HERE / "track0-surface.json").read_text(encoding="utf-8"))
    fields = next(row["blocked_fields_without_question"] for row in failed_surface["cases"]
                  if row["id"] == "exception1_personal_loss_8949.unanswered")
    rows = []
    for field in fields:
        entry: dict[str, Any] = {"field": field}
        for name, core in cores.items():
            direct = results[name]["blocked"][field]
            roots = unexplainable_roots(results[name], direct, question_names[name], core)
            entry[name] = {
                "rule": direct["artifact"], "code": direct["code"], "missing": direct["missing"],
                "source": source_citation(core, direct["artifact"],
                                          str((direct.get("missing") or [""])[0]), str(direct["code"])),
                "reasons": direct["reasons"], "unexplainable_roots": roots,
                "why_no_reason": ("all-roots projection suppresses the field because at least one reachable "
                                  "root has an unexplainable missing name" if roots else "not reproduced"),
            }
        entry["reasonless_on_v87"] = not entry["v87"]["reasons"]
        def root_keys(name: str) -> set[tuple[str, str, str, str]]:
            return {(str(root["rule"]), str(root["code"]), json.dumps(root["missing"], sort_keys=True),
                     str(root["unexplainable_name"])) for root in entry[name]["unexplainable_roots"]}
        entry["scratch_roots_also_on_v87"] = root_keys("scratch") <= root_keys("v87")
        rows.append(entry)
    checks = {
        "fifteen_fields": len(rows) == 15,
        "all_reasonless_on_v87": all(row["reasonless_on_v87"] for row in rows),
        "all_reasonless_on_scratch": all(not row["scratch"]["reasons"] for row in rows),
        "every_field_reaches_unexplainable_root": all(row["scratch"]["unexplainable_roots"] for row in rows),
        "scratch_roots_also_on_v87": all(row["scratch_roots_also_on_v87"] for row in rows),
    }
    common.write("track0-roots.json", {
        "case": "exception1_personal_loss_8949.unanswered",
        "projection": {"all_roots": "packages/derivation/presentation_projection.py:578",
                       "reason_suppression": "packages/derivation/presentation_projection.py:624"},
        "live_runs": results, "fields": rows, "checks": checks,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
    })
    print(json.dumps(checks, indent=2))


def repair() -> None:
    build = json.loads((HERE / "prototype-build.json").read_text(encoding="utf-8"))
    output = json.loads((HERE / "prototype-output.json").read_text(encoding="utf-8"))
    roots = json.loads((HERE / "track0-roots.json").read_text(encoding="utf-8"))
    authority = json.loads((HERE / "track0-authority.json").read_text(encoding="utf-8"))
    tables = {name: json.loads((HERE / f"track0-{name}.json").read_text(encoding="utf-8"))
              for name in ("matrix", "surface", "reuse", "neighbour")}
    target = output["cases"]["exception1_personal_loss_8949"]
    root_rules = sorted({root["rule"] for field in roots["fields"]
                         for root in field["scratch"]["unexplainable_roots"]})
    line16 = next(row for row in authority["declarations"]
                  if row["rule"] == P + "rule.form1040-line16")
    payload = {
        "root": {
            "unexplainable_rules": root_rules,
            "missing_name_without_question_citizen": "tax.total-tax",
            "producer": "form1040-line16",
            "predecessor_disposition": "inapplicable",
        },
        "repair": {
            "rule": "rule.form1040-line16",
            "predecessor": "v7",
            "successor": "v8",
            "mechanism": "the false guard branch blocks and declares existing boundary-question names",
            "missing": line16["missing"],
            "presentation_change": False,
            "kernel_change": False,
            "numeric_values_changed": False,
        },
        "prototype": {
            "rule_successors": build["rule_successors"],
            "target_questions": target["questions"],
            "target_silent_blocked": target["silent_blocked"],
            "target_line16_disposition": target["lines"]["form1040.line-16"],
        },
        "tables": {name: {"verdict": body["verdict"], "checks": body["checks"]}
                   for name, body in tables.items()},
        "verdict": "PASS" if (not target["silent_blocked"]
                                and all(body["verdict"] == "PASS" for body in tables.values())) else "FAIL",
    }
    common.write("track0-repair.json", payload)
    print(json.dumps({"verdict": payload["verdict"], "tables": {
        name: body["verdict"] for name, body in tables.items()}}, indent=2))


def main() -> None:
    if len(sys.argv) == 3 and sys.argv[1] in {"authority", "matrix", "late", "reuse", "trace"}:
        globals()[sys.argv[1]](Path(sys.argv[2]).resolve())
    elif len(sys.argv) == 2 and sys.argv[1] in {"neighbour", "surface", "repair"}:
        globals()[sys.argv[1]]()
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
