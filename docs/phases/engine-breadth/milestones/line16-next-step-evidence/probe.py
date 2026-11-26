"""Stage 1 inventory: what the saved page says on a required Schedule D with no sale.

Run from the repository root (or from a scratch copy, for a scratch core):
  python3 docs/phases/engine-breadth/milestones/line16-next-step-evidence/probe.py \
      [--core v108] [--out probe-v108.json] [--workers N]

Every list is synthetic demo acts run once through the real live_coordinate_run
and presentation projection (tools.recorded_replay.saved_output), the same path
the full-surface replay uses. The act lists start from the line16-names P0
lists (line16-names-evidence/probe.py): the four recorded targets, the
single/joint/separate required neighbours, the personal-loss case
(exception1_personal_loss_8949), the Exception 1-holds control and a recorded
sale. Added here: all fifteen ways Exception 1 can fail on the single return,
and two unanswered controls.

For each list the output records, per blocked page field, the text the saved
page draws (renderLine of packages/presentation/pages/citation-walk.v1.html,
re-implemented here for its blocked branch: banner, "Why:" items with a
linked question drawn as its link text, or else the code heading, field
explanation, code sentence and remedy), the question cards
(renderQuestionGroups: question, affected lines and status text), which
questions are named, the filer's recorded answer to each Exception 1 question,
and whether any drawn text states that answer. It also records every page
field's disposition and value so a scratch core can be compared number for
number. This is a text re-implementation of the page's drawing code for these
two parts, not a browser draw.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import recorded_replay as rr  # noqa: E402

P = "tax.us.2025."
EXC = [P + "exception1.only-box2a-capital-gains", P + "exception1.no-capital-losses",
       P + "exception1.no-qof-deferral", P + "exception1.no-boxes-2b-2c-2d"]
FORM8949 = P + "schedule-d-boundary.no-form8949-sources"
SHORT = {EXC[0]: "C1 only-box2a", EXC[1]: "C2 no-capital-losses", EXC[2]: "C3 no-qof-deferral",
         EXC[3]: "C4 no-boxes-2b-2c-2d", FORM8949: "no-form8949-sources"}
PAGE = REPO / "packages/presentation/pages/citation-walk.v1.html"
STATUS_TEXT = {"current": "An answer is recorded here.", "stale": "Needs reconfirmation.",
               "unanswered": "Needs an answer."}
LINK_TEXT = "See the question and affected lines above"
ANSWER_STATEMENT = re.compile(r"\b(?:you answered|your answer(?: is|:))\s+(yes|no)\b", re.IGNORECASE)


def _names_probe() -> Any:
    name = "l16ns_line16_names_probe"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, HERE.parent / "line16-names-evidence" / "probe.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def cases() -> list[tuple[str, list[dict[str, Any]]]]:
    """The probe's act lists, keyed; every value is a synthetic demo list."""
    base = dict(_names_probe().lists())
    h = rr._get_harness()
    out: list[tuple[str, list[dict[str, Any]]]] = []
    required = base["status/single/required"]
    for mask in range(1, 16):
        acts = copy.deepcopy(required)
        for bit, fact in enumerate(EXC):
            acts = h.say(acts, fact, "no" if mask & (1 << bit) else "yes", "l16ns-" + fact.rsplit(".", 1)[1])
        out.append((f"fails/single/{mask:02d}", acts))
    for key in ("recorded/m_2a_only_exc1_only2a_no", "recorded/m_empty_exc1_nolosses_no",
                "recorded/m_empty_exc1_only2a_no", "recorded/t4_s1_removed",
                "status/married_filing_jointly/required", "status/married_filing_separately/required"):
        out.append((key, copy.deepcopy(base[key])))
    out.append(("personal-loss/exception1_personal_loss_8949",
                copy.deepcopy(base["exception1-no/exception1_personal_loss_8949"])))
    out.append(("control/exception1-holds", copy.deepcopy(base["status/single/exception-yes"])))
    out.append(("control/sale-recorded", copy.deepcopy(base["neighbour/recorded-sale"])))
    out.append(("control/c1-unanswered", h.renumber(h.strip(copy.deepcopy(required), EXC[0]))))
    out.append(("control/form8949-unanswered", h.renumber(h.strip(copy.deepcopy(required), FORM8949))))
    return out


def _code_copy() -> dict[str, dict[str, str]]:
    """BLOCKED_CODE_COPY line entries, read from the page itself."""
    text = PAGE.read_text(encoding="utf-8")
    block = text.split("const BLOCKED_CODE_COPY = Object.freeze({", 1)[1].split("\n});", 1)[0]
    found: dict[str, dict[str, str]] = {}
    for code, body in re.findall(r"\n  ([A-Z0-9_]+): \{(.*?)\n  \}", block, re.S):
        found[code] = dict(re.findall(r'(\w+): "((?:[^"\\]|\\.)*)"', body))
    return found


def recorded_answers(acts: list[dict[str, Any]]) -> dict[str, Any]:
    current: dict[str, Any] = {}
    for act in acts:
        finding = (act.get("payload") or {}).get("finding") or {}
        fact_type = str(finding.get("fact_id", "")).split("|", 1)[0]
        if fact_type in SHORT:
            current[SHORT[fact_type]] = finding.get("value")
    return {name: current.get(name) for name in SHORT.values()}


def draw_blocked(section: dict[str, Any], groups: dict[str, dict[str, Any]], copy_by_code: dict[str, dict[str, str]]) -> list[str]:
    """The text renderLine draws for a blocked field (its blocked branch)."""
    field, resolved = section.get("field") or {}, section.get("resolved") or {}
    reasons = resolved.get("reasons") or []
    linked: dict[int, list[str]] = {}
    for ref in resolved.get("questionRefs") or []:
        for index in ref.get("reasonIndices") or []:
            assert reasons[index]["sentence"] == groups[ref["groupId"]]["question"]
            linked.setdefault(index, []).append(ref["groupId"])
    lines = ["This line has no result."]
    items = []
    for index, reason in enumerate(reasons):
        if index in linked:
            items.append("; ".join(LINK_TEXT for _ in linked[index]))
            continue
        label = reason.get("statementLabel") or {}
        name = reason.get("memberLabel") or ", ".join(
            part for part in (label.get("statement"), label.get("lender")) if isinstance(part, str) and part)
        items.append((name + ": " if name else "") + reason["sentence"])
    codes = list(resolved.get("activeCodes") or [])
    if items:
        return lines + ["Why:"] + ["- " + item for item in items]
    copies = [copy_by_code[code] for code in codes]
    lines += list(dict.fromkeys(c["lineHeading"] for c in copies))
    lines.append(((field.get("dispositions") or {}).get("blocked") or {}).get("explain", ""))
    sentences = list(dict.fromkeys(c["sentence"] for c in copies))
    if sentences:
        lines.append(" ".join(sentences))
    remedies = list(dict.fromkeys(c["lineRemedy"] for c in copies)) or ["Review the saved records for this line."]
    return lines + ["What to do: " + " ".join(remedies)]


def draw_cards(model: dict[str, Any]) -> list[dict[str, Any]]:
    """The question cards renderQuestionGroups draws, with each card's producer."""
    affected: dict[str, set[str]] = {}
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        for ref in (section.get("resolved") or {}).get("questionRefs") or []:
            for scope in ref["scopes"]:
                label = (field.get("label") or section["id"]) + (
                    " (Line " + str(field["line"]) + ")" if field.get("line") is not None else "")
                affected.setdefault(ref["groupId"], set()).add(label + " — " + STATUS_TEXT[scope["status"]])
    cards = []
    for group in model.get("questionGroups") or []:
        cards.append({"question": group["question"], "target": group["answerTarget"]["factTypeId"],
                      "producers": [p["id"] + "@" + p["version"] for p in group["producers"]],
                      "affected": sorted(affected.get(group["id"], ()))})
    return cards


def summarize(saved: dict[str, Any], answers: dict[str, Any]) -> dict[str, Any]:
    if saved["outcome"] != "success":
        return {"outcome": saved["outcome"], "error": saved.get("error"),
                "message": re.sub(r"/(?:Users|private|tmp|var)/\S+", "<path>", str(saved.get("message")))[:400]}
    model, report = saved["model"], saved["report"]
    groups = {group["id"]: group for group in model.get("questionGroups") or []}
    copy_by_code = _code_copy()
    values: dict[str, Any] = {}
    drawn: dict[str, list[str]] = {}
    named: dict[str, list[str]] = {}
    for section in model.get("sections") or []:
        resolved = section.get("resolved") or {}
        values[section["id"]] = [resolved.get("disposition"), resolved.get("value"), resolved.get("activeCodes")]
        if resolved.get("disposition") == "blocked":
            drawn[section["id"]] = draw_blocked(section, groups, copy_by_code)
            named[section["id"]] = sorted(groups[ref["groupId"]]["answerTarget"]["factTypeId"].removeprefix(P)
                                          for ref in resolved.get("questionRefs") or [])
    field_groups: dict[str, dict[str, Any]] = {}
    for section_id, text in drawn.items():
        key = json.dumps([text, named[section_id]])
        field_groups.setdefault(key, {"fields": [], "named_questions": named[section_id], "text": text})["fields"].append(section_id)
    cards = draw_cards(model)
    all_text = [line for text in drawn.values() for line in text] + [
        part for card in cards for part in [card["question"], *card["affected"]]]
    stated = sorted({match.lower() for line in all_text for match in ANSWER_STATEMENT.findall(line)})
    rows = {}
    for row in report.get("dispositions") or []:
        artifact = str(row.get("artifact_id", "")).removeprefix(P + "rule.")
        if artifact in ("form1040-line16", "selected-preferential-base", "schedule-d-required.conclusion"):
            rows[artifact] = {"disposition": row.get("disposition"), "code": row.get("code"),
                              "missing": [str(name).removeprefix(P) for name in row.get("missing") or []]}
    return {
        "outcome": "success",
        "recorded_answers": answers,
        "rows": rows,
        "line16": {"drawn": drawn.get("line-16"), "named_questions": named.get("line-16"),
                   "value": values.get("line-16")},
        "blocked_fields": len(drawn),
        "blocked_field_groups": sorted(field_groups.values(), key=lambda g: g["fields"]),
        "question_cards": cards,
        "answer_words_stated_on_page": stated,
        "values": values,
    }


class ProbeRun:
    """Picklable per-list function: one saved output per core, summarized."""

    def __call__(self, key: str, acts: list[dict[str, Any]], cores: Any) -> dict[str, Any]:
        cores = cores if isinstance(cores, (list, tuple)) else (cores,)
        answers = recorded_answers(acts)
        run_id = "demo.l16ns." + re.sub(r"[^a-z0-9]+", ".", key.lower()).strip(".")
        return {"cores": [summarize(rr.saved_output(core, acts, run_id), answers) for core in cores]}


def run(core_specs: list[str], workers: int | None) -> dict[str, Any]:
    lists = cases()
    cores = tuple(rr.resolve_core(spec) for spec in core_specs)
    results = rr.replay(lists, cores, ProbeRun(), workers=workers)
    return {"format": "line16-next-step-probe.v1",
            "cores": [rr.core_fingerprint(core) for core in cores],
            "lists": len(results),
            "cases": {key: value for key, value in sorted(results.items())}}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", default="v108")
    parser.add_argument("--out", default=None)
    parser.add_argument("--workers", type=int, default=None)
    args = parser.parse_args()
    body = run([args.core], args.workers)
    text = json.dumps(body, indent=1, ensure_ascii=False) + "\n"
    rr._check_no_local_paths(text, "probe output")
    if args.out:
        (HERE / args.out).write_text(text, encoding="utf-8")
    print(json.dumps({"lists": body["lists"], "cores": [c["version"] for c in body["cores"]]}))


if __name__ == "__main__":
    main()
