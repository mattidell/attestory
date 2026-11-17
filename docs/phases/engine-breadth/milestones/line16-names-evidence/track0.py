"""Track 0 live adversarial evidence, on the unchanged P0 narrow successor.

Run: python3 track0.py <item> <scratch-core.json> [item-specific arguments]
No production content is written. Every sibling is loaded by explicit path
under a unique name. Saved sentences are the full page-model text.
"""
from __future__ import annotations
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
import json
import multiprocessing
import os
from pathlib import Path
import sys
import tempfile
import time
from html.parser import HTMLParser
import shutil

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


p0 = module("l16_t0_p0", HERE / "probe.py")
P = p0.P
BOUNDARY = "schedule-d-boundary.no-form8949-sources"
STATUSES = ("single", "married_filing_jointly", "married_filing_separately")
TARGETS = ("recorded/m_2a_only_exc1_only2a_no", "recorded/m_empty_exc1_nolosses_no",
           "recorded/m_empty_exc1_only2a_no", "recorded/t4_s1_removed") + tuple("status/" + s + "/required" for s in STATUSES)


def exact(a, b):
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def context(core_json):
    common = p0.load(p0.BNQ / "common.py", "t0_common")
    h = common.harness()
    core = common.scratch(Path(core_json)) if core_json else h.Core("v94", "v92", "v92")
    return common, h, core


def page_view(core, outcome):
    assert outcome.refusal is None, str(outcome.refusal)
    common, _, _ = context(None)
    publishes = common.rule_publishes(core)
    report = json.loads(outcome.output_path.read_text())
    model = json.loads(outcome.presentation_path.read_text())
    rows = [{"artifact": p0.short(r.get("artifact_id")),
             "symbol": p0.short(r.get("symbol") or publishes.get(r.get("artifact_id"))),
             "disposition": r.get("disposition"), "code": r.get("code"),
             "missing": [p0.short(n) for n in r.get("missing") or []]} for r in report["dispositions"]]
    fields = {}
    for section in model["sections"]:
        field, resolved = section.get("field") or {}, section.get("resolved") or {}
        own = [r for r in rows if r["symbol"] == p0.short(field.get("binds_symbol"))]
        assert len(own) <= 1
        disposition = resolved.get("disposition")
        instruction = (field.get("dispositions") or {}).get("published_value" if disposition == "published_categorical" else disposition) or {}
        fields[p0.short(field.get("id"))] = {
            "disposition": disposition, "value": resolved.get("value"),
            "reasons": resolved.get("reasons") or [], "row": own[0] if own else None,
            "render": instruction.get("render"), "explain": instruction.get("explain"),
        }
    return {"fields": fields, "rows": rows,
            "publications": {p0.short(p.finding.get("symbol")): p.finding.get("value") for p in outcome.publications or ()}}


def live(core_json, acts, run_id, *, page_path=None, inspect_currency=False):
    _, h, core = context(core_json)
    surface = core.surface()
    with h.loader_entries(core):
        finished = h._handover(h._finish(copy.deepcopy(acts), package_path=core.package_path,
            package_version=core.version, release_path=core.release_path,
            release_version=core.release_version, note=run_id), surface=surface, reconfirm=True)
        with tempfile.TemporaryDirectory() as tmp:
            capability = h.WorkspaceCapability(Path(tmp) / "L")
            outcome = h.live_coordinate_run(capability, repo_root=REPO, authoritative_acts=finished,
                workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": h.YEAR},
                scope_user=h.ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
                governance_pins=[], surface=surface, output_name="out.json")
            result = page_view(core, outcome)
            if inspect_currency:
                from packages.kernel.currency import compute_currency
                from packages.kernel.findings import project
                from packages.derivation import live as coordinator
                schemas = coordinator.DerivationSchemas()
                coordinator.install_domain_companion_presence(schemas.registry)
                coordinator.install_domain_companion_equalities(schemas.registry)
                coordinator.install_domain_declaration_signal_contradictions(schemas.registry)
                registry = coordinator.companion_registry_for_package(schemas.registry, (P + "package.core-calculations", core.version))
                state = project(tuple(finished), registry)
                current = compute_currency(state)
                result["answer_currency"] = [
                    {"id": ident, "value": f["value"], "current": ident in current.current_finding_ids,
                     "displacement": [{"kind": r.kind, "by": r.by} for r in current.reasons.get(ident, ())]}
                    for ident, f in state.findings.items() if f["fact_id"].startswith(P + BOUNDARY + "|")]
                result["publication_pin_ids"] = sorted({pin["id"] for pub in outcome.publications or () for pin in pub.finding["pins"]})
                result["run_current"] = outcome.current
            if page_path is not None:
                from packages.derivation.live_session import _render_page
                page_path.parent.mkdir(parents=True, exist_ok=True)
                page_path.write_bytes(_render_page(REPO, capability, outcome.presentation_path))
            return result


def worker(args):
    core_json, shard = args
    result = []
    for key, acts in shard:
        result.append((key, live(core_json, acts, "demo.l16.t0." + key.replace("/", "."))))
    p0.evidence_loader.finish_all()
    return result


def parallel(core_json, cases):
    p0.evidence_loader.finish_all()
    workers = max(1, (os.cpu_count() or 2) - 1)
    started = time.monotonic()
    with multiprocessing.get_context("spawn").Pool(workers) as pool:
        found = dict(pair for part in pool.map(worker, [(core_json, cases[i::workers]) for i in range(workers) if cases[i::workers]]) for pair in part)
    return found, round(time.monotonic() - started, 3)


def write(name, body):
    p0.write("track0-" + name + ".json", body)


def packed(cases):
    return p0.pack_cases({key: p0.compact(value) for key, value in cases.items()})


def line16(result):
    return result["fields"]["form1040.line-16"]


def signature(field):
    return {key: field[key] for key in ("disposition", "value", "row")}


def assess_names(rows):
    """The target fixture notes explicitly call their negative Exception 1
    answers false. All families are empty; the status neighbours reproduce
    that world. A no-Form-8949 'no' is a different world, not a true correction.
    """
    truths = dict(zip(p0.FOUR + p0.EXC, ("no", "no", "yes", "yes", "yes", "yes", "yes", "yes")))
    fails = []
    for row in rows:
        truthful = truths[row["name"]]
        row["truthful_answers"] = [truthful]
        row["truthful_moves"] = [v for v in row["moves_block_answers"] if v == truthful]
        row["verdict"] = "PASS" if row["truthful_moves"] else "FAIL"
        row["truth_basis"] = "Synthetic empty/box-2a-only world; the sale-audit M-case notes call the negative Exception 1 answer false; T4 removed its sole sale; the status neighbours explicitly have no sale."
        if row["verdict"] == "FAIL":
            fails.append({"target": row["target"], "name": row["name"],
                "proposed_fix": "Remove this name from line 16's declaration in this state; its truthful answer does not move or unblock line 16. Keep truthful multi-answer progress as a separate foreman decision."})
    return fails


def names(core_json):
    base = dict(p0.lists())
    _, h, _ = context(core_json)
    cases = []
    for target in TARGETS:
        for name in p0.FOUR + p0.EXC:
            for value in ("yes", "no"):
                cases.append((target + "/" + name + "/" + value,
                    h.say(copy.deepcopy(base[target]), P + name, value, "demo-l16-t0-one-" + name)))
    found, wall = parallel(core_json, cases)
    saved = {key: p0.expand(value) for key, value in p0.read_cases(HERE / "candidate.json").items()}
    rows, fails = [], []
    for target in TARGETS:
        original = line16(saved[target])
        assert original["row"]["missing"] == p0.FOUR + p0.EXC
        for name in p0.FOUR + p0.EXC:
            alternatives = {value: line16(found[target + "/" + name + "/" + value]) for value in ("yes", "no")}
            moves = [value for value, field in alternatives.items() if not exact(signature(field), signature(original))]
            verdict = "PASS" if moves else "FAIL"
            row = {"target": target, "name": name, "verdict": verdict, "moves_block_answers": moves,
                   "results": alternatives,
                   "truth_limit": "An answer that changes circumstances is truthful only if those circumstances actually hold; a live act list does not establish them."}
            rows.append(row)
            if not moves:
                fails.append({"target": target, "name": name,
                    "proposed_fix": "Remove this name from line 16's declared block in this state; neither yes nor no is a way forward under the charter's one-answer criterion."})
    no_movement_fails = len(fails)
    fails = assess_names(rows)
    write("names", {"item": 1, "verdict": "FAIL" if fails else "PASS", "runs": len(found),
        "wall_time_s": wall, "fail_count": len(fails), "failed_names": dict(Counter(row["name"] for row in fails)),
        "no_movement_pairs": no_movement_fails,
        "truthfulness_note": "A no-movement FAIL is conclusive even before assessing truth. Movement alone is not proof that a counterfactual answer is truthful.",
        "rows": rows, "fails": fails})
    print(json.dumps({"item": 1, "runs": len(found), "wall_time_s": wall, "fails": len(fails),
                      "failed_names": dict(Counter(row["name"] for row in fails))}, indent=2))


def boundary_lists():
    base = dict(p0.lists())
    _, h, _ = context(None)
    cases = []
    for status in STATUSES:
        for state in ("fully-required", "fully-exempt", "partly", "unanswered"):
            acts = copy.deepcopy(base["status/" + status + "/required"])
            for name in p0.EXC:
                acts = h.strip(acts, P + name)
            values = {name: "yes" for name in p0.EXC} if state.startswith("fully") else {}
            if state in ("fully-required", "partly"):
                values[p0.EXC[0]] = "no"
            for name, value in values.items():
                acts = h.say(acts, P + name, value, "t0-exception-" + name)
            for answer in ("yes", "no", "unanswered"):
                changed = h.strip(copy.deepcopy(acts), P + BOUNDARY)
                if answer != "unanswered": changed = h.say(changed, P + BOUNDARY, answer, "t0-boundary")
                cases.append(("boundary/" + status + "/" + state + "/" + answer, h.renumber(changed)))
    return cases


def boundaries(core_json):
    cases = boundary_lists()
    found, wall = parallel(core_json, cases)
    rows, fails = {}, []
    for key, result in sorted(found.items()):
        blocked = {name: field for name, field in result["fields"].items() if field["disposition"] == "blocked"}
        silent = [name for name, field in blocked.items() if not field["reasons"]]
        rows[key] = {"blocked_fields": len(blocked), "fields_without_reason_sentence": silent,
                     "watched": {name: result["fields"][name] for name in sorted(p0.WATCH)}}
        for name in silent:
            fails.append({"case": key, "field": name,
                "proposed_fix": "Determine the missing explanation root. If line 16's declared names cannot supply a truthful actionable sentence, stop for the foreman; do not edit the projection or page."})
    write("boundary", {"item": 2, "verdict": "FAIL" if fails else "PASS", "runs": len(found),
        "wall_time_s": wall, "rows": rows, "fails": fails,
        "sentence_scope": "All page reason sentences saved, without punctuation filtering. Semantic actionability assessment is in track0-closure.md.",
        **packed(found)})
    print(json.dumps({"item": 2, "runs": len(found), "wall_time_s": wall, "silent_fields": len(fails)}, indent=2))


def assess_boundaries():
    path = HERE / "track0-boundary.json"
    saved = json.loads(path.read_text())
    cases = {key: p0.expand(value) for key, value in p0.read_cases(path).items()}
    law = json.loads((HERE / "law.json").read_text())
    sentences = {row["name"]: row["sentence"] for row in law["questions"]}
    mfs = "If you are married filing separately, did you live apart from your spouse for all of 2025?"
    known = set(sentences.values()) | {mfs}
    rows, fails = {}, []
    for key, result in cases.items():
        _, status, state, answer = key.split("/")
        actionable = set()
        if state == "unanswered": actionable.update(sentences[n] for n in p0.EXC)
        if state == "partly": actionable.update(sentences[n] for n in p0.EXC[1:])
        if answer == "unanswered": actionable.add(sentences[BOUNDARY])
        if answer == "no": actionable.add(sentences[p0.FOUR[3]])
        if state == "fully-required" and answer == "yes": actionable.add(sentences[p0.EXC[0]])
        if status == "married_filing_separately": actionable.add(mfs)
        fields = {}
        for name, field in result["fields"].items():
            if field["disposition"] != "blocked": continue
            words = [reason["sentence"] for reason in field["reasons"]]
            usable = [sentence for sentence in words if sentence in actionable]
            untrue = [sentence for sentence in words if sentence not in known or sentence == mfs and status != "married_filing_separately"]
            passed = bool(usable) and not untrue
            fields[name] = {"verdict": "PASS" if passed else "FAIL", "actionable_sentences": usable, "untrue_or_unassessed_sentences": untrue}
            if not passed:
                fails.append({"case": key, "field": name,
                    "proposed_fix": "Route to an existing truthful open answer through line 16's declaration if possible. If this field's own producer prevents that, stop for the foreman rather than changing another producer or projection."})
        rows[key] = fields
    saved["actionability"] = rows
    saved["semantic_fails"] = fails
    saved["semantic_standard"] = "At least one sentence identifies an unanswered criterion, the missing Form 8949 boundary, the unanswered adjustment boundary after no, a corrective only-box-2a answer on the deliberately mistaken empty required return, or the applicable unanswered MFS lived-apart fact. This is the field-level Decision 3 check; item 1 separately tests every individual name."
    saved["verdict"] = "FAIL" if fails or saved["fails"] else "PASS"
    write("boundary", saved)
    print(json.dumps({"item": 2, "blocked_fields_assessed": sum(len(f) for f in rows.values()), "semantic_fails": len(fails)}, indent=2))


def append_answer(acts, name, value, tag):
    _, h, _ = context(None)
    # A real correction: keep the predecessor finding in history, append a new
    # assertion of the same fact, then let kernel currency displace the old one.
    old = next(a["payload"]["finding"] for a in reversed(acts)
               if (a.get("payload") or {}).get("finding", {}).get("fact_id", "").startswith(P + name + "|"))
    h._add(acts, "assertion", {"finding": h._attested("demo.l16.t0." + tag, old["fact_id"], value)})
    return h.renumber(acts)


def late(core_json):
    base = dict(p0.lists())
    _, h, _ = context(core_json)
    initial = copy.deepcopy(base["status/single/required"])
    yes = append_answer(initial, BOUNDARY, "yes", "late-yes")
    no = append_answer(copy.deepcopy(yes), BOUNDARY, "no", "late-no")
    withdrawn = copy.deepcopy(no)
    h._add(withdrawn, "finding-retracted", {"finding_id": "demo.l16.t0.late-no"})
    withdrawn = h.renumber(withdrawn)
    sold = h.sale(copy.deepcopy(yes), "no1099b", "st", proceeds=2000, basis=8000, tag="l16-t0-late-sale")
    sold = append_answer(sold, BOUNDARY, "no", "sale-boundary-no")
    sold = append_answer(sold, p0.FOUR[1], "yes", "sale-q2-yes")
    # These were not answered in the no-Form-8949 branch. Supply new existing
    # boundary answers without deleting any prior current or historical finding.
    for key, value in (("path_b", "no"), ("ic80", "yes"), ("exc1_no_losses", "no")):
        name = h.ANSWER_FACT[key]
        prior = [a for a in sold if (a.get("payload") or {}).get("finding", {}).get("fact_id", "").startswith(name + "|")]
        if prior: sold = append_answer(sold, name.removeprefix(P), value, "sale-" + key)
        else: sold = h.say(sold, name, value, "sale-" + key)
    stages = [("yes-eight", yes), ("corrected-no-four", no), ("withdrawn-boundary", withdrawn), ("sale-after-eight", sold)]
    started = time.monotonic()
    runs = {key: live(core_json, acts, "demo.l16.t0.late." + key, inspect_currency=True) for key, acts in stages}
    checks = {
        "yes_names_eight": line16(runs["yes-eight"])["row"]["missing"] == p0.FOUR + p0.EXC,
        "correction_names_four": line16(runs["corrected-no-four"])["row"]["missing"] == p0.FOUR,
        "correction_displaces_yes": any(r["id"] == "demo.l16.t0.late-yes" and not r["current"] and r["displacement"] for r in runs["corrected-no-four"]["answer_currency"]),
        "withdrawal_has_no_current_boundary": not any(r["current"] for r in runs["withdrawn-boundary"]["answer_currency"]),
        "withdrawal_asks_boundary": [r["sentence"] for r in line16(runs["withdrawn-boundary"])["reasons"]] == ["Is it true that you had no transaction or adjustment to report on Form 8949?"],
        "sale_publishes_line16": line16(runs["sale-after-eight"])["value"] == 3515,
        "sale_uses_current_no": any(r["id"] == "demo.l16.t0.sale-boundary-no" and r["current"] for r in runs["sale-after-eight"]["answer_currency"]) and "demo.l16.t0.sale-boundary-no" in runs["sale-after-eight"]["publication_pin_ids"],
        "no_displaced_boundary_in_any_stage_pins": all(not set(value["publication_pin_ids"]) & {r["id"] for r in value["answer_currency"] if not r["current"]} for value in runs.values()),
    }
    write("late", {"item": 3, "verdict": "PASS" if all(checks.values()) else "FAIL", "checks": checks,
        "wall_time_s": round(time.monotonic() - started, 3),
        "stages": {key: {"line16": line16(value), "answer_currency": value["answer_currency"],
                          "publication_pin_ids": value["publication_pin_ids"], "run_current": value["run_current"]} for key, value in runs.items()},
        **packed(runs)})
    print(json.dumps({"item": 3, "checks": checks}, indent=2))


def neighbours(core_json):
    base = dict(p0.lists())
    _, h, _ = context(core_json)
    cases = [(key, acts) for key, acts in base.items() if key.startswith(("schedule-d-refused/", "code-b-refused/", "exception1-no/", "wash-admission/"))]
    cases += [("no-schedule-d/" + status, base["status/" + status + "/exception-yes"]) for status in STATUSES]
    box2a = copy.deepcopy(base[TARGETS[0]])
    for name in p0.EXC: box2a = h.say(box2a, P + name, "yes", "t0-box2a-" + name)
    cases.append(("schedule-d-not-required/box2a", box2a))
    cases.append(("sale/short-term", base["neighbour/recorded-sale"]))
    sold = h.sale(copy.deepcopy(base["status/single/exception-yes"]), "no1099b", "lt", proceeds=10000, basis=4000, tag="l16-t0-long")
    sold = h.answer(sold, q2="yes", form8949="no", path_b="no", ic80="yes", exc1_only_2a="no")
    cases.append(("sale/long-term", sold))
    before, wall_a = parallel(None, cases)
    after, wall_b = parallel(core_json, cases)
    rows, fails = {}, []
    for key, _ in cases:
        a, b = before[key]["fields"], after[key]["fields"]
        changes = {name: {"v94": a.get(name), "v95": b.get(name)} for name in set(a) | set(b)
                   if not exact(a.get(name), b.get(name))}
        rows[key] = {"verdict": "FAIL" if changes else "PASS", "fields": len(a),
                     "line16_value": a["form1040.line-16"]["value"], "differences": changes}
        if changes: fails.append({"case": key, "proposed_fix": "Keep all fields of this neighbour identical; narrow the line 16 naming declaration."})
    write("neighbours", {"item": 4, "verdict": "FAIL" if fails else "PASS", "cases": len(cases),
        "runs": len(cases) * 2, "wall_time_s": wall_a + wall_b, "rows": rows, "fails": fails,
        "before": packed(before), "after": packed(after)})
    print(json.dumps({"item": 4, "cases": len(cases), "fails": len(fails)}, indent=2))


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ignored = 0
        self.parts = []
        self.alerts = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"): self.ignored += 1
        if "section-error" in dict(attrs).get("class", "").split(): self.alerts += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"): self.ignored -= 1

    def handle_data(self, data):
        if not self.ignored: self.parts.append(data)

    def text(self):
        return " ".join(" ".join(self.parts).split())


def pages(core_json, page_dir):
    helper = module("l16_t0_page_alerts_test", REPO / "tests/test_page_alerts_v92.py")
    assert helper.BROWSER, "headless Chrome is required"
    cases = dict(p0.lists())
    target = cases["recorded/t4_s1_removed"]
    _, h, _ = context(core_json)
    unanswered = h.renumber(h.strip(copy.deepcopy(cases["status/single/required"]), P + BOUNDARY))
    started = time.monotonic()
    rows = {}
    profile_root = helper._new_owned_chrome_tempdir()
    try:
        for key, acts in (("target", target), ("unanswered-boundary", unanswered)):
            page = page_dir / ("demo.l16.t0." + key + ".html")
            live(core_json, acts, "demo.l16.t0.page." + key, page_path=page)
            model = helper._saved_model(page)
            dom = helper._dump(page, profile_root / key)
            (page_dir / ("demo.l16.t0." + key + ".dom.html")).write_text(dom)
            visible = VisibleText()
            visible.feed(dom)
            fields = {}
            for section in model["sections"]:
                field, resolved = section.get("field") or {}, section.get("resolved") or {}
                name = p0.short(field.get("id"))
                if name not in p0.WATCH: continue
                section_dom = helper._section(dom, field["label"])
                drawn = VisibleText()
                drawn.feed(section_dom)
                sentences = [r["sentence"] for r in resolved.get("reasons") or []]
                fields[name] = {"sentences": sentences,
                    "all_sentences_drawn": all(" ".join(text.split()) in drawn.text() for text in sentences),
                    "drawn_sentence_count": sum(" ".join(text.split()) in drawn.text() for text in sentences)}
            alerts = [text for text in helper.SAFE_RENDER if text in visible.text()]
            expected = 8 if key == "target" else 1
            passed = visible.alerts == 0 and not alerts and len(fields) == 5 and all(
                f["all_sentences_drawn"] and f["drawn_sentence_count"] == expected for f in fields.values())
            rows[key] = {"verdict": "PASS" if passed else "FAIL", "page_filename": page.name,
                "page_sha256": hashlib.sha256(page.read_bytes()).hexdigest(),
                "dom_sha256": hashlib.sha256(dom.encode()).hexdigest(),
                "safe_render_alert_elements": visible.alerts, "safe_render_alert_sentences": alerts, "fields": fields,
                "observation": "Questions checked against drawn field text excluding script/style, not merely embedded MODEL text."}
    finally:
        shutil.rmtree(profile_root)
    write("page", {"item": 5, "verdict": "PASS" if all(r["verdict"] == "PASS" for r in rows.values()) else "FAIL",
        "wall_time_s": round(time.monotonic() - started, 3), "rows": rows,
        "retained_pages": "Saved outside Git in the scratch successor's track0-pages directory; operational report identifies it."})
    print(json.dumps({"item": 5, "rows": {key: row["verdict"] for key, row in rows.items()}}, indent=2))


def replay(core_json, part_path):
    from tools.recorded_replay import core_fingerprint, resolve_core
    started = time.monotonic()
    part_bytes = part_path.read_bytes()
    saved = json.loads(part_bytes)
    cores = [resolve_core("v94"), resolve_core(Path(core_json))]
    assert saved["_metadata"]["cores"] == [core_fingerprint(core) for core in cores]
    scratch = cores[1]
    # Verify byte identity, not only semantic citizen checksums. All inherited
    # content bytes must still be the published copy used to build P0.
    inherited = list((REPO / "packages/content/tax/2025").iterdir())
    for path in inherited:
        if path.is_file(): assert path.read_bytes() == (scratch.content / path.name).read_bytes(), path.name
    release = json.loads(scratch.release_path.read_text())
    assert hashlib.sha256((scratch.content / "published-packages.v93.json").read_bytes()).hexdigest() == release["package_registry_sha256"]
    builder = module("l16_t0_p0_content_builder", p0.PBR / "prototype.py")
    expected = builder.line16_body()
    named = expected["when"]["else"]["then"]
    expected["when"]["else"]["then"] = {"op": "choose", "when": {
        "op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": builder.NO_8949},
        "right": {"op": "category_literal", "fact_type": {"id": builder.NO_8949, "version": "v1"}, "value": "yes"}},
        "then": named, "else": {"op": "block", "code": "DEPENDENCY_ABSENT", "missing": builder.FOUR}}
    expected["notes"] += " Eight names require the existing no-Form-8949 answer to be yes; known Form 8949 work keeps four."
    rule = scratch.content / "rule.form1040-line16.v9.json"
    assert rule.read_bytes() == (json.dumps(expected, indent=2) + "\n").encode()
    classifier = module("l16_t0_strict_classifier", HERE / "classify.py")
    counts = Counter(classifier.classify_pair(r["pins"]["v94"], r["pins"]["v95"]) for r in saved["results"].values())
    original = json.loads((HERE / "rerun.json").read_text())
    assert len(saved["results"]) == 775 and dict(counts) == original["counts"] and not counts["unexpected"]
    write("replay", {"item": 6, "verdict": "PASS", "mode": "reused", "lists": 775,
        "classification_counts": dict(counts), "part_sha256": hashlib.sha256(part_bytes).hexdigest(),
        "successor_rule_sha256": hashlib.sha256(rule.read_bytes()).hexdigest(),
        "original_replay_wall_time_s": original["wall_time_s"], "new_live_replay_wall_time_s": 0,
        "reuse_validation_wall_time_s": round(time.monotonic() - started, 3),
        "content_identity": "Part fingerprints match; inherited bytes match published content, registry SHA matches release, and successor rule bytes exactly match the committed P0 builder.",
        "classifier_controls": original["classifier_controls"]})
    print(json.dumps({"item": 6, "mode": "reused", "counts": dict(counts)}, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("item")
    parser.add_argument("core")
    parser.add_argument("extra", nargs="*")
    args = parser.parse_args()
    if args.item == "names": names(args.core)
    elif args.item == "boundary":
        boundaries(args.core)
        assess_boundaries()
    elif args.item == "assess-boundary": assess_boundaries()
    elif args.item == "late": late(args.core)
    elif args.item == "neighbours": neighbours(args.core)
    elif args.item == "page": pages(args.core, Path(args.extra[0]) if args.extra else Path(args.core).parent / "track0-pages")
    elif args.item == "replay": replay(args.core, Path(args.extra[0]))
    elif args.item == "assess-names":
        path = HERE / "track0-names.json"
        saved = json.loads(path.read_text())
        saved["no_movement_pairs"] = sum(not r["moves_block_answers"] for r in saved["rows"])
        saved["fails"] = assess_names(saved["rows"])
        saved["fail_count"] = len(saved["fails"])
        saved["failed_names"] = dict(Counter(r["name"] for r in saved["fails"]))
        saved["verdict"] = "FAIL" if saved["fails"] else "PASS"
        write("names", saved)
        print(json.dumps({"truthful_fail_pairs": len(saved["fails"]), "no_movement_pairs": saved["no_movement_pairs"]}))
    else: raise SystemExit("unsupported Track 0 item")


if __name__ == "__main__":
    main()
