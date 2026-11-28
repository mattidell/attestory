"""Failing controls for the replay, the scratch anchor, and the trusted walk."""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from unittest.mock import patch

from probe import CORE, HERE, PROMPT, baseline_prompts, declarations, digest, prompt_positions, summary_json
from replay import compare, require_outcomes, successor, synthetic
import scratch
from packages.derivation import live
from tools import recorded_replay as rr


def rejects(checked, name, action, error):
    try:
        action()
    except ValueError as exc:
        if str(exc) != error:
            raise
        checked.append(name)
        return
    raise ValueError(f"control accepted: {name}")


def require_additions(summary, expected):
    for cohort, pinned in expected.items():
        if any(summary[cohort][field] != value for field, value in pinned.items()):
            raise ValueError("pinned count, ordered links or error details differ")


def census_controls():
    rows = [
        {"key": "demo.save", "baseline_outcome": "success", "candidate_outcome": "success"},
        {"key": "demo.error", "baseline_outcome": "error", "candidate_outcome": "error"},
    ]
    pinned = {"success": 1, "error": 1}
    import hashlib

    errors = hashlib.sha256(b'["demo.error"]').hexdigest()
    require_outcomes(rows, pinned, errors)
    checked = []
    failed = {"outcome": "error", "error": "DemoSetupError", "message": "demo setup issue"}
    compare(failed, failed, None)
    rejects(checked, "shared_error_replaces_save", lambda: require_outcomes(
        [dict(row, baseline_outcome="error", candidate_outcome="error") for row in rows], pinned, errors,
    ), "outcome census differs")
    swapped = [dict(row, key=other["key"]) for row, other in zip(rows, reversed(rows), strict=True)]
    rejects(checked, "error_identity_swapped_at_same_count", lambda: require_outcomes(
        swapped, pinned, errors,
    ), "error set differs")
    for field, value in (("error", "DemoOtherError"), ("message", "demo changed error details")):
        changed = {**failed, field: value}
        rejects(checked, f"mismatched_failure_{field}", lambda: compare(failed, changed, None), "failure changed")
    refused = {"outcome": "refused", "error": "refusal", "message": "demo refusal"}
    compare(refused, refused, None)
    rejects(checked, "mismatched_refusal_details", lambda: compare(
        refused, dict(refused, message="demo changed refusal"), None,
    ), "failure changed")

    pins = {"changed_lists": 2, "ordered_links_sha256": "demo.order", "failure_details_sha256": "demo.errors"}
    summary = {"demo": pins}
    require_additions(summary, summary)
    for field in pins:
        rejects(checked, f"wrong_{field}", lambda: require_additions(
            {"demo": {**pins, field: "demo.different"}}, summary,
        ), "pinned count, ordered links or error details differ")
    return checked


def saved_pair(key, acts, core):
    base, candidate = scratch.projectors()
    observed = {}

    def project(**kwargs):
        observed["args"] = kwargs
        observed["before"] = base.build_presentation_model(**kwargs)
        return candidate.build_presentation_model(**kwargs)

    with patch.object(live, "build_presentation_model", project):
        result = rr.saved_output(core, acts, "demo.links.check." + digest(key)[:20])
    if result["outcome"] != "success":
        raise ValueError(f"{key}: expected a saved demo page, got {result.get('error')}: {result.get('message')}")
    before = {**result, "model": observed["before"]}
    return before, result, observed["args"]


def resolved_at(model, section_id):
    return next(s["resolved"] for s in model["sections"] if s["id"] == section_id)


def model_controls(before, after, wanted):
    changed = bool(wanted)
    checked = []

    def trial(name, mutate, error):
        broken = deepcopy(after)
        mutate(broken)
        rejects(checked, name, lambda: compare(before, broken, wanted), error)

    ordered = "ordered prompt positions or destinations differ"
    if changed:
        (section_id, index), refs = next(iter(wanted.items()))

        def reason(result):
            return resolved_at(result["model"], section_id)["reasons"][index]

        trial("removed_link", lambda result: reason(result).pop(PROMPT), ordered)
        trial("retargeted_link", lambda result: reason(result).update({PROMPT: "question-prompt-demo-other"}), ordered)

        def move(result):
            model = result["model"]
            first = next(iter(wanted))
            second = next(pos for pos, targets in wanted.items() if targets != wanted[first])
            reasons = [resolved_at(model, s)["reasons"][i] for s, i in (first, second)]
            reasons[0][PROMPT], reasons[1][PROMPT] = reasons[1][PROMPT], reasons[0][PROMPT]

        if len({repr(refs) for refs in wanted.values()}) > 1:
            trial("swapped_links_between_reasons", move, ordered)

        def added_on_existing(result):
            for section in result["model"]["sections"]:
                resolved = section["resolved"]
                linked = scratch.linked_positions(resolved)
                if linked:
                    resolved["reasons"][min(linked)][PROMPT] = "question-prompt-demo-unexpected"
                    return
            raise AssertionError("control needs a typed answer link")

        if any(scratch.linked_positions(s["resolved"]) for s in after["model"]["sections"]):
            trial("extra_link_on_typed_question", added_on_existing, ordered)
        trial("changed_reason_wording", lambda result: reason(result).update(sentence="demo changed question"),
              "saved model differs beyond prompt links")
        trial("changed_block_code", lambda result: resolved_at(result["model"], section_id)["activeCodes"].append(
            "DEPENDENCY_INVALID",
        ), "saved model differs beyond prompt links")
    else:
        def add_to_clean(result):
            section = next(s for s in result["model"]["sections"] if s["resolved"].get("reasons"))
            section["resolved"]["reasons"][0][PROMPT] = "question-prompt-demo-unexpected"

        trial("extra_link_on_unchanged_list", add_to_clean, ordered)
        trial("changed_unchanged_model", lambda result: result["model"].update(demo_control=True),
              "saved model differs beyond prompt links")
    suffix = "changed" if changed else "unchanged"
    trial(f"changed_report_on_{suffix}_list", lambda result: result["report"].update(demo_control=True),
          "report changed")
    trial(f"changed_outcome_on_{suffix}_list", lambda result: result.update(outcome="error"), "outcome changed")
    return checked


DOM_INSPECTION = """
  const sections = {};
  const targets = {};
  let errors = 0;
  let controls = 0;
  walkElements(mainEl, (node) => {
    if (node.classList.contains("section-error")) errors += 1;
    if (node.id.startsWith("question-prompt-")) {
      const title = node.children.find((child) => child.tagName === "H3");
      (targets[node.id] ||= []).push(collectVisibleText(title).join(""));
      walkElements(node, (child) => {
        if (["INPUT", "BUTTON", "SELECT", "TEXTAREA", "FORM"].includes(child.tagName)) controls += 1;
      });
    }
  });
  for (const section of byId.get("sections-root").children) {
    const items = [];
    walkElements(section, (node) => {
      if (!node.classList.contains("blocked-reasons")) return;
      for (const list of node.children.filter((child) => child.tagName === "UL")) {
        for (const item of list.children.filter((child) => child.tagName === "LI")) {
          const hrefs = [];
          walkElements(item, (child) => {
            if (child.tagName === "A") hrefs.push(child.getAttribute("href"));
          });
          items.push({text: collectVisibleText(item).join(""), hrefs});
        }
      }
    });
    sections[section.id] = items;
  }
  return {sections, targets, errors, controls};
"""


def dom_observer(directory):
    helper = HERE.parent / "page-plain-words-evidence/check_page_dom.mjs"
    path = directory / "observe.mjs"
    path.write_text(scratch.replace_once(
        helper.read_text(encoding="utf-8"),
        '  if (process.env.PPW_CHECK_BLOCKED_REASONS === "1") {',
        '  if (process.env.RQL_DOM === "1") {\n' + DOM_INSPECTION +
        '  }\n  if (process.env.PPW_CHECK_BLOCKED_REASONS === "1") {',
    ), encoding="utf-8")
    return path


def observe_dom(helper, page, model):
    page_file = helper.with_name("page.html")
    page_file.write_text(page, encoding="utf-8")
    output = subprocess.run(
        ["node", str(helper), str(page_file)], check=True, text=True, capture_output=True, timeout=30,
        input=json.dumps({"key": "demo", "model": model}) + "\n", env={**os.environ, "RQL_DOM": "1"},
    )
    return json.loads(output.stdout)["demo"]


def check_dom(old, new, wanted):
    if old["sections"].keys() != new["sections"].keys() or new["errors"] or new["controls"]:
        raise ValueError("DOM sections or display-only requirement differ")
    target_counts = Counter()
    positions = set()
    for section, old_items in old["sections"].items():
        for index, (left, right) in enumerate(zip(old_items, new["sections"][section], strict=True)):
            if left["text"] != right["text"]:
                raise ValueError("DOM reason text or order changed")
            if (section, index) not in wanted:
                if left["hrefs"] != right["hrefs"]:
                    raise ValueError("DOM added a link where no prompt was expected")
                continue
            positions.add((section, index))
            if left["hrefs"] or len(right["hrefs"]) != 1 or not right["hrefs"][0].startswith("#question-prompt-"):
                raise ValueError("DOM prompt is missing its single link")
            target = right["hrefs"][0][1:]
            if new["targets"].get(target) != [right["text"]]:
                raise ValueError("DOM prompt points at the wrong labelled question")
            target_counts[target] += 1
    if positions != set(wanted) or target_counts != Counter({name: 1 for name in new["targets"]}):
        raise ValueError("DOM prompt destinations and positions disagree")
    return len(positions)


def publication_controls(kwargs):
    """Check the inherited sale attribution against actual publication acts."""
    _, candidate = scratch.projectors()
    observed = []
    method = candidate._SaleQuestions.reasons

    def check(walker, traces, questions, other):
        traces = list(traces)
        result = method(walker, traces, questions, other)
        if result and not observed:
            answer, row, _, _ = traces[0]
            artifact = row["artifact_id"]
            fid = next(fid for fid, finding in walker.publications.items()
                       if finding["symbol"].startswith(artifact + "."))
            act_finding = walker.publication_act_findings[fid]
            finding = walker.publications[fid]
            if act_finding != finding:
                raise ValueError("authentic sale finding and publication act disagree")
            for name, change in (
                ("missing_publication_act", {key: value for key, value in walker.publication_act_findings.items() if key != fid}),
                ("publication_act_finding_changed", {**walker.publication_act_findings, fid: {**act_finding, "version": "v3"}}),
            ):
                with patch.object(walker, "publication_act_findings", change):
                    if method(walker, traces, questions, other):
                        raise ValueError(f"inherited attribution accepted {name}")
                observed.append(name)
            with patch.object(walker, "publications", {**walker.publications, fid: {**finding, "version": "v3"}}):
                if method(walker, traces, questions, other):
                    raise ValueError("inherited attribution accepted a changed finding beside the act")
            observed.append("result_finding_changed_beside_act")
        return result

    with patch.object(candidate._SaleQuestions, "reasons", check):
        candidate.build_presentation_model(**kwargs)
    if len(observed) != 3:
        raise ValueError("publication controls did not reach a labelled fixing question")
    return observed


def walk_controls():
    """Remove and corrupt the witnesses needed by the new prompt-only route."""
    _, candidate = scratch.projectors()
    key = "demo.scope.answer"
    sentence = "Enter the demo amount."
    question = {"schema": "input-question.v1", "id": "demo.amount-question", "version": "v1",
                "fact_type": {"id": key, "version": "v1"}, "question": sentence}
    family = {
        "schema": "source-closure-mapping.v4", "id": "demo.family-closure", "version": "v1",
        "families": [{"family": {"id": "demo.family", "version": "v1"}}],
        "closure_question": "Have you recorded every demo source?",
    }
    leaf = {"artifact_id": "demo.rule.leaf", "missing": ["demo.input"], "disposition": "blocked",
            "code": "DEPENDENCY_ABSENT"}
    row = {"artifact_id": "demo.rule.line", "missing": ["demo.leaf"], "disposition": "blocked",
           "code": "DEPENDENCY_ABSENT"}
    inputs = {"demo.input": key}

    def prompts(current=row, members=(question,), by_symbol=None, binding=inputs, **changes):
        origins = {}
        if by_symbol is None:
            by_symbol = {"demo.leaf": [leaf]}
        reasons = candidate._closure_question_reasons(
            current, resolved_members=members, by_symbol=by_symbol, symbol_fact_types=binding,
            prompt_origins_out=origins, prompt_indexes=declarations(members), **changes,
        )
        scratch.attach_prompts({"reasons": reasons}, origins, "demo.section")
        return [reason[PROMPT] for reason in reasons if PROMPT in reason]

    if prompts() != ["question-prompt-demo.section-0"]:
        raise ValueError("adopted imperative witness did not link without an answer fact")

    family_row = {**row, "missing": ["demo.family"], "code": "SOURCE_SET_UNCLOSED"}
    if not prompts(family_row, (family,)):
        raise ValueError("adopted grouped closure witness did not link")
    negative = {
        "no_adopted_question": prompts(members=()),
        "wrong_question_target_pin": prompts(members=({**question, "fact_type": {"id": "demo.other"}},)),
        "blank_question": prompts(members=({**question, "question": " "},)),
        "missing_binding_map": prompts(binding={}),
        "missing_blocked_predecessor": prompts(by_symbol={}),
        "predecessor_published": prompts(by_symbol={"demo.leaf": [{**leaf, "disposition": "published"}]}),
        "wrong_leaf_code": prompts(by_symbol={"demo.leaf": [{**leaf, "code": "DEPENDENCY_INVALID"}]}),
        "wrong_missing_symbol": prompts(by_symbol={"demo.leaf": [{**leaf, "missing": ["demo.other"]}]}),
        "missing_leaf_in_mixed_walk": prompts(by_symbol={"demo.leaf": [{**leaf, "missing": []}]}),
        "unknown_second_cause": prompts(by_symbol={"demo.leaf": [{**leaf, "missing": ["demo.input", "demo.other"]}]}),
        "closure_does_not_adopt_family": prompts(family_row, ({**family, "families": []},)),
        "plain_explanation_equals_unwalked_question": prompts(
            {**row, "missing": ["demo.code"]}, constraint_meanings={"demo.code": sentence},
        ),
    }
    if any(negative.values()):
        raise ValueError("a damaged walk still reported a prompt")
    return sorted(negative)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    demo = synthetic()
    results = {"census": census_controls(), "walk": walk_controls(), "live": {}}
    with TemporaryDirectory() as directory:
        directory = Path(directory)
        helper = dom_observer(directory)
        next_core = successor(directory)
        harness = rr._get_harness()
        box4 = harness.sale(harness.opened(), "covered", "st", proceeds=2000, basis=1000,
                            tag="demo.reason-links.box4")
        box4 = harness.answer(box4, **harness.honest({"covered"}, new_questions=True))
        box4 = harness.say(box4, harness.P + "f1099b.no-sale-box4-present", "no", "demo.reason-links.no-sale")
        # The statement reports withholding without an amount. The amount
        # fact identity has not been created by an assertion.
        answer_type = harness.P + "f1099b.statement-box4-withholding-reported"
        bundle = harness.bundle_for(answer_type, rr.resolve_core(CORE).content)
        if answer_type not in harness._adopted(box4):
            harness._add(box4, "bundle-adoption", {"bundle": bundle})
        box4 = harness.strip(box4, answer_type)
        statement = next(act["payload"]["entity"]["id"] for act in box4
                         if act["kind"] == "entity-introduced"
                         and act["payload"]["entity"]["kind"] == "tax.us.f1099b-statement")
        reported = harness.fact_id_for(harness.P + "f1099b.statement-box4-withholding-reported",
                                       (("statement", statement), ("tax-year", harness.YEAR)))
        harness._add(box4, "assertion", {"finding": harness._attested("demo.reason-links.reported", reported, "yes")})
        box4 = harness.renumber(box4)
        for key, acts, core in (
            ("demo.roster.eic", demo["demo.roster.eic"], CORE),
            ("demo.sale.single-sale", demo["demo.sale.single-sale"], CORE),
            ("demo.sale.two-fixes", demo["demo.sale.two-fixes"], CORE),
            ("demo.sale.successor", demo["demo.sale.two-fixes"], next_core),
            ("demo.box4.current", box4, CORE),
            ("demo.box4.older", box4, "v89"),
        ):
            before, after, kwargs = saved_pair(key, acts, core)
            wanted = baseline_prompts(before["model"], kwargs["resolved_members"])
            compare(before, after, wanted)
            page = scratch.scratch_page()
            old = observe_dom(helper, scratch.baseline_source(scratch.PAGE), before["model"])
            new = observe_dom(helper, page, after["model"])
            row = {
                "core": rr.resolve_core(core).version, "rendered_links": check_dom(old, new, wanted),
                "producers": dict(Counter(ref["id"] for refs in wanted.values() for ref in refs)),
            }
            if key in {"demo.roster.eic", "demo.sale.single-sale", "demo.sale.two-fixes"}:
                row["rejected"] = model_controls(before, after, wanted)
            if key in {"demo.sale.two-fixes", "demo.sale.successor"}:
                row.setdefault("rejected", []).extend(publication_controls(kwargs))
            if key == "demo.roster.eic":
                broken = deepcopy(new)
                section, index = next(iter(wanted))
                broken["sections"][section][index]["hrefs"] = ["#question-prompt-demo-wrong"]
                rejects(row["rejected"], "retargeted_rendered_link", lambda: check_dom(old, broken, wanted),
                        "DOM prompt points at the wrong labelled question")
            results["live"][key] = row
            print(key, row["rendered_links"], flush=True)
    args.out.write_text(summary_json(results), encoding="utf-8")


if __name__ == "__main__":
    main()
