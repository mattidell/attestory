"""P0 for the age fact's title: where it is shown, and what a successor does to a saved answer.

Evidence for docs/phases/engine-breadth/milestones/eic-age-title.md.
Charter: docs/reviews/eic-age-title/charter-p0.md.

Two synthetic demo.* returns on published core v103 (single filer, wages
7,000). One records eic.age-25-under-65 as yes. One leaves it unanswered.
Each runs through live_coordinate_run and the production saved-page
renderer. The return builder is the hoh-eic probe, loaded by path.

With --scratch DIR (a new directory outside the repository), the script
also builds a bundle successor whose only wording change is the title in
wording.json, then loads the v103 answer three ways: the saved v103
adoption on that surface, the same acts re-finished on the successor, and
the same acts plus a re-adoption of the new bundle.

Writes p0.json beside this file. Nothing in packages/ or tests/ is edited.

    python3 docs/phases/engine-breadth/milestones/eic-age-title-evidence/probe.py
    python3 docs/phases/engine-breadth/milestones/eic-age-title-evidence/probe.py --scratch DIR
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import html
import importlib.util
import json
import re
import shutil
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

MILESTONES = REPO / "docs/phases/engine-breadth/milestones"
FACT = "tax.us.2025.eic.age-25-under-65"
BUNDLE_ID = "tax.us.2025.eic-questions.vocabulary"
ANSWER_SYMBOL = "tax.us.2025.eic.answer.age-25-under-65"
LINE = "form1040.line-27a"
TITLE_MARK = (
    "You, or your spouse if you are filing a joint return, were born after "
    "December 31, 1960, and before January 2, 2001. No means the credit is $0."
)
QUESTION_MARK = "Were you, or your spouse if you file a joint return, at least age 25 but under age 65"
FROM = {"core": "v103", "registry": "v101", "release": "v101"}
TO = {"core": "v104", "registry": "v102", "release": "v102"}
STEM = "demo.release.sli-worksheet-integration.2025"


def load(name: str, path: Path) -> Any:
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


hoh = load("eat_p0_hoh_probe", MILESTONES / "hoh-eic-evidence/probe.py")
h = hoh.h

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_session import _render_page  # noqa: E402
from packages.derivation.loader import DerivationSchemas  # noqa: E402
from packages.kernel.currency import compute_currency  # noqa: E402
from packages.kernel.findings import project  # noqa: E402
from packages.tax.loader import (  # noqa: E402
    install_domain_companion_equalities,
    install_domain_companion_presence,
    install_domain_declaration_signal_contradictions,
)
from tools.package_successor import SuccessorError, generate_to_directory  # noqa: E402


def scrub(text: str) -> str:
    text = text.replace(str(REPO), ".")
    return re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", text)


def paths_holding(node: Any, needle: str, prefix: str = "$", limit: int = 24) -> list[str]:
    found: list[str] = []

    def walk(value: Any, at: str) -> None:
        if len(found) >= limit:
            return
        if isinstance(value, str):
            if needle in value:
                found.append(at)
        elif isinstance(value, dict):
            for key, child in value.items():
                walk(child, f"{at}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{at}[{index}]")

    walk(node, prefix)
    return found


def visible_text(page: str) -> str:
    stripped = re.sub(r"<script\b[^>]*>.*?</script>", " ", page, flags=re.I | re.S)
    stripped = re.sub(r"<style\b[^>]*>.*?</style>", " ", stripped, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", stripped)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def excerpt(text: str, mark: str, width: int = 280) -> str | None:
    at = text.find(mark)
    if at < 0:
        return None
    start = max(0, at - 40)
    return text[start:at + width]


def wording() -> str:
    body = json.loads((HERE / "wording.json").read_text(encoding="utf-8"))
    title = body["title"]
    assert isinstance(title, str) and title.startswith("You, or your spouse")
    assert "died in 2025" in title and title.endswith("free supersession.")
    return title


def core_of(version: str, registry: str, release: str, content: Path | None = None,
            releases: Path | None = None, loader_from: str | None = None) -> Any:
    kwargs: dict[str, Any] = {}
    if content is not None:
        kwargs["content"] = content
    if releases is not None:
        kwargs["releases"] = releases
    if loader_from is not None:
        kwargs["loader_from"] = loader_from
    return h.Core(version, registry, release, **kwargs)


def prepare(unanswered: bool) -> list[dict[str, Any]]:
    dropped = (FACT,) if unanswered else ()
    acts = hoh.build("single/none/7000", h.CONTENT, "none", dropped)
    return h.renumber(acts)


def kernel_view(acts: list[dict[str, Any]]) -> dict[str, Any]:
    registry = DerivationSchemas().registry
    install_domain_companion_presence(registry)
    install_domain_companion_equalities(registry)
    install_domain_declaration_signal_contradictions(registry)
    state = project(tuple(acts), registry)
    fact_type = state.fact_state.fact_types.get(FACT)
    currency = compute_currency(state)
    rows = []
    for finding_id, finding in state.findings.items():
        if not str(finding.get("fact_id", "")).startswith(FACT + "|"):
            continue
        rows.append({
            "id": finding_id,
            "schema": finding.get("schema"),
            "fact_id": finding.get("fact_id"),
            "value": finding.get("value"),
            "basis": finding.get("basis"),
            "keys": sorted(finding.keys()),
            "current": finding_id in currency.current_finding_ids,
            "pins_field": "pins" in finding,
        })
    adoptions = []
    for act in acts:
        if act.get("kind") != "bundle-adoption":
            continue
        bundle = (act.get("payload") or {}).get("bundle") or {}
        if bundle.get("id") != BUNDLE_ID:
            continue
        declared = next((item for item in bundle.get("fact_types") or [] if item.get("id") == FACT), None)
        adoptions.append({
            "bundle_version": bundle.get("version"),
            "fact_type_version": None if declared is None else declared.get("version"),
            "title_is_published": None if declared is None else declared.get("title") == TITLE_MARK + " Contributed categorical assertion, domain {yes, no}, no default, presence-before-value, free supersession.",
            "title_is_successor": None if declared is None else declared.get("title") == wording(),
        })
    package = None
    for act in acts:
        if act.get("kind") != "package-adoption":
            continue
        pin = (act.get("payload") or {}).get("package") or {}
        package = {"id": pin.get("id"), "version": pin.get("version")}
    return {
        "fact_type_present": fact_type is not None,
        "fact_type_version": None if fact_type is None else fact_type.get("version"),
        "title_is_published": None if fact_type is None else fact_type.get("title", "").startswith(
            "You, or your spouse if you are filing a joint return, were born after December 31, 1960"
        ) and "died in 2025" not in fact_type.get("title", ""),
        "title_is_successor": None if fact_type is None else fact_type.get("title") == wording(),
        "findings": rows,
        "bundle_adoptions": adoptions,
        "package_adoption": package,
    }


def run_case(core: Any, acts: list[dict[str, Any]], run_id: str, *, finish: bool = True) -> dict[str, Any]:
    surface = core.surface()
    with h.loader_entries(core):
        # A saved log already carries one package adoption. Finishing it again
        # makes two current adoptions, and the handover refuses the tie.
        if finish:
            finished = h._handover(
                h._finish(
                    copy.deepcopy(acts),
                    package_path=core.package_path,
                    package_version=core.version,
                    release_path=core.release_path,
                    release_version=core.release_version,
                    note=run_id,
                ),
                surface=surface,
                reconfirm=True,
            )
        else:
            finished = copy.deepcopy(acts)
        with TemporaryDirectory() as tmp:
            capability = h.WorkspaceCapability(Path(tmp) / "L")
            outcome = live_coordinate_run(
                capability, repo_root=REPO, authoritative_acts=finished,
                workspace_revision=len(finished),
                run_scope={"jurisdiction": "us", "year": h.YEAR}, scope_user=h.ccr.USER,
                request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
                surface=surface, output_name="out.json",
            )
            if outcome.refusal is not None:
                return {
                    "refusal": outcome.refusal.reason,
                    "detail": scrub(str(outcome.refusal.detail))[:400],
                    "kernel": kernel_view(finished),
                }
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
            page = Path(tmp) / "page.html"
            page.write_bytes(_render_page(REPO, capability, outcome.presentation_path))
            page_text = page.read_text(encoding="utf-8")
    shown = visible_text(page_text)
    graph = model.get("explanationGraph") or {}
    groups = model.get("questionGroups") or []
    age_groups = []
    for group in groups:
        question = str(group.get("question") or "")
        target = group.get("answerTarget") or {}
        if FACT in json.dumps(target) or QUESTION_MARK in question or FACT in question:
            age_groups.append({
                "keys": sorted(group.keys()),
                "factTypeId": target.get("factTypeId"),
                "factTypeVersion": target.get("factTypeVersion"),
                "question_is_input_question": question.startswith(QUESTION_MARK),
                "title_in_question": TITLE_MARK in question,
            })
    graph_nodes = []
    for key, node in (graph.get("nodes") or {}).items():
        blob = json.dumps(node)
        if FACT in blob or "age-25-under-65" in blob:
            graph_nodes.append({
                "key_kind": key.split(":", 1)[0],
                "node_keys": sorted(node.keys()),
                "kind": node.get("kind"),
                "symbol": node.get("symbol"),
                "value": node.get("value"),
                "title_present": TITLE_MARK in blob,
            })
    line = None
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        if str(field.get("id") or "").removeprefix("tax.us.2025.") != LINE:
            continue
        resolved = section.get("resolved") or {}
        said = []
        for name in ("questions", "reasons", "blocked_reasons"):
            for item in resolved.get(name) or []:
                sentence = item.get("sentence") if isinstance(item, dict) else item
                if isinstance(sentence, str) and sentence.strip():
                    said.append(sentence)
        line = {
            "disposition": resolved.get("disposition"),
            "value": resolved.get("value"),
            "sentences": said[:4],
        }
    pubs = []
    for item in outcome.publications or ():
        finding = item.finding
        symbol = str(finding.get("symbol") or "")
        if symbol not in {ANSWER_SYMBOL, "tax.us.2025.payments.line27a"}:
            continue
        pins = []
        for pin in finding.get("pins") or []:
            pins.append({
                "role": pin.get("role"),
                "version": pin.get("version"),
                "origin": pin.get("origin"),
                "id_is_fact_type": pin.get("id") == FACT,
                "id_is_rule": str(pin.get("id") or "").startswith("tax.us.2025.rule."),
            })
        pubs.append({
            "symbol": symbol.removeprefix("tax.us.2025."),
            "value": finding.get("value"),
            "schema": finding.get("schema"),
            "version": finding.get("version"),
            "pins": pins,
        })
    surfaces = {
        "page_visible": shown,
        "presentation_model": model,
        "explanation_graph": graph,
        "question_groups": groups,
        "report": report,
    }
    title_hits = {name: paths_holding(value, TITLE_MARK) for name, value in surfaces.items()}
    question_hits = {
        "page_visible": QUESTION_MARK in shown,
        "question_groups": paths_holding(groups, QUESTION_MARK),
        "report": paths_holding(report, QUESTION_MARK),
        "explanation_graph": paths_holding(graph, QUESTION_MARK),
    }
    unsupported = [
        row.get("factTypeId") for row in model.get("unsupportedSourceFindings") or []
        if row.get("factTypeId") == FACT
    ]
    return {
        "stop": report.get("stop_reason"),
        "line_27a": line,
        "age_question_groups": age_groups,
        "graph_nodes": graph_nodes[:12],
        "graph_nodes_for_fact": len(graph_nodes),
        "publications": pubs,
        "title_hits": title_hits,
        "title_on_any_surface": any(title_hits.values()),
        "question_hits": question_hits,
        "page_question_excerpt": excerpt(shown, QUESTION_MARK),
        "page_title_excerpt": excerpt(shown, "were born after December 31, 1960"),
        "unsupported_source_finding": unsupported,
        "calculation_view_present": "calculationView" in model,
        "kernel": kernel_view(finished),
        "finished_acts": finished,
    }


def public_result(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "finished_acts"}


def build_successor(scratch: Path) -> dict[str, Any]:
    assert REPO not in scratch.parents and scratch != REPO and not scratch.exists()
    source = REPO / "packages/content/tax/2025"
    releases = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
    content, rel = scratch / "content", scratch / "releases"
    shutil.copytree(source, content)
    shutil.copytree(releases, rel)
    new_title = wording()
    bundle_path = content / "eic-questions.bundle.json"
    raw = bundle_path.read_text(encoding="utf-8")
    body = json.loads(raw)
    old = next(item["title"] for item in body["fact_types"] if item["id"] == FACT)
    assert old == TITLE_MARK + " Contributed categorical assertion, domain {yes, no}, no default, presence-before-value, free supersession."
    assert raw.count(json.dumps(old, ensure_ascii=False)) == 1
    replaced = raw.replace(json.dumps(old, ensure_ascii=False), json.dumps(new_title, ensure_ascii=False), 1)
    replaced, count = re.subn(
        r'(?m)^(  "version": ")v1(")$',
        lambda match: match.group(1) + "v2" + match.group(2),
        replaced,
    )
    assert count == 1
    back = re.sub(r'(?m)^(  "version": ")v2(")$', lambda match: match.group(1) + "v1" + match.group(2), replaced)
    back = back.replace(json.dumps(new_title, ensure_ascii=False), json.dumps(old, ensure_ascii=False), 1)
    assert back == raw
    next_name = "eic-questions.bundle.v2.json"
    assert not (content / next_name).exists()
    (content / next_name).write_text(replaced, encoding="utf-8")
    package = json.loads((source / f"package.core-calculations.{FROM['core']}.json").read_text(encoding="utf-8"))
    old_pin = next(member for member in package["members"] if member["id"] == BUNDLE_ID)
    assert old_pin["version"] == "v1"
    new_pin = {**old_pin, "version": "v2"}
    members = [{"op": "replace", "old": old_pin, "new": new_pin}]
    entries = []
    if any(item == {"id": BUNDLE_ID, "version": "v1"} for item in package["entrypoints"]):
        entries.append({
            "op": "replace",
            "old": {"id": BUNDLE_ID, "version": "v1"},
            "new": {"id": BUNDLE_ID, "version": "v2"},
        })
    # Any other v103 member that pins this bundle version would have to move with it.
    # Index the corpus once. A per-member rescan of this directory does not finish
    # inside the evidence budget.
    indexed: dict[tuple[str, str], dict[str, Any]] = {}
    for path in sorted(source.glob("*.json")):
        candidate = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(candidate, dict) and isinstance(candidate.get("id"), str) and isinstance(candidate.get("version"), str):
            indexed.setdefault((candidate["id"], candidate["version"]), candidate)
    pinned_by = []
    for member in package["members"]:
        if member["id"] == BUNDLE_ID:
            continue
        file_body = indexed.get((member["id"], member["version"]))
        if file_body is None:
            continue
        if BUNDLE_ID in json.dumps(file_body):
            pinned_by.append(member["id"])
    assert pinned_by == []
    changes = {
        "package_version": TO["core"],
        "release_version": TO["release"],
        "members": members,
        "entrypoints": entries,
        "registry_sort": "id_version",
    }
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    output: dict[str, Any] = {
        "from": FROM,
        "to": TO,
        "bundle": {"id": BUNDLE_ID, "old_version": "v1", "new_version": "v2"},
        "fact_type_version_kept": "v1",
        "other_members_pinning_bundle": pinned_by,
        "entrypoint_replacements": len(entries),
        "byte_undo_proof": True,
        "successor_sha256": hashlib.sha256(replaced.encode("utf-8")).hexdigest(),
    }
    try:
        report = generate_to_directory(
            content / f"package.core-calculations.{FROM['core']}.json",
            content / f"published-packages.{FROM['registry']}.json",
            rel / f"{STEM}.{FROM['release']}.json",
            content,
            scratch / "changes.json",
            scratch / "generated",
        )
    except SuccessorError as exc:
        output.update({"status": "rejected", "failure": scrub(str(exc))[:2000]})
        return output
    for src, dst in (
        ("package.json", content / f"package.core-calculations.{TO['core']}.json"),
        ("registry.json", content / f"published-packages.{TO['registry']}.json"),
        ("release.json", rel / f"{STEM}.{TO['release']}.json"),
    ):
        shutil.copyfile(scratch / "generated" / src, dst)
    (scratch / "core.json").write_text(json.dumps({
        "version": TO["core"], "registry": TO["registry"], "release_version": TO["release"],
        "content": str(content), "releases": str(rel), "loader_from": FROM["core"],
    }, indent=2) + "\n", encoding="utf-8")
    output.update({
        "status": "valid",
        "validation": "generate_to_directory passed package, registry and release validation",
        "generation": {key: value for key, value in report.items() if isinstance(value, (str, int, bool))},
    })
    return output


def opened(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Drop the finish and the Social Security handover so one later finish can run.

    The saved log already holds one package adoption, one family-handover, and
    the reconfirm that handover writes. Leaving those in and finishing again
    either ties two adoptions or finds the family chain already handed over.
    """
    kept = []
    for act in acts:
        if act.get("kind") in {"package-adoption", "family-handover"}:
            continue
        finding = (act.get("payload") or {}).get("finding") or {}
        if finding.get("id") == "demo.fk.ssa.reconfirm":
            continue
        kept.append(act)
    return kept


def adopt_successor(acts: list[dict[str, Any]], content: Path) -> list[dict[str, Any]]:
    body = json.loads((content / "eic-questions.bundle.v2.json").read_text(encoding="utf-8"))
    out = copy.deepcopy(acts)
    h._add(out, "bundle-adoption", {"bundle": body})
    return h.renumber(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch", type=Path)
    parser.add_argument("--out", type=Path, default=HERE / "p0.json")
    args = parser.parse_args()
    started = time.monotonic()
    published = core_of(FROM["core"], FROM["registry"], FROM["release"])
    answered_acts = prepare(False)
    unanswered_acts = prepare(True)
    answered = run_case(published, answered_acts, "demo.eat.age.answered")
    unanswered = run_case(published, unanswered_acts, "demo.eat.age.unanswered")
    body: dict[str, Any] = {
        "core": FROM,
        "return": "demo single filer, wages 7000, no qualifying child, other earned-income-credit answers yes",
        "answered": public_result(answered),
        "unanswered": public_result(unanswered),
        "title_shown_on_v103": bool(answered.get("title_on_any_surface") or unanswered.get("title_on_any_surface")),
    }
    if args.scratch is not None:
        scratch = args.scratch.resolve()
        built = build_successor(scratch)
        body["successor_build"] = built
        if built.get("status") == "valid":
            successor = core_of(
                TO["core"], TO["registry"], TO["release"],
                content=scratch / "content", releases=scratch / "releases", loader_from=FROM["core"],
            )
            saved = answered["finished_acts"]
            # The saved log already pins core v103. Replay it unchanged on the
            # successor surface, which still holds the v103 package file.
            held = run_case(successor, saved, "demo.eat.age.saved-on-successor-surface", finish=False)
            # Open the log, then finish once on the successor package.
            pre = opened(saved)
            refit = run_case(successor, pre, "demo.eat.age.refit-successor")
            readopt = run_case(successor, adopt_successor(pre, scratch / "content"), "demo.eat.age.readopt-bundle")
            body["loads"] = {
                "saved_v103_log_on_successor_surface": public_result(held),
                "acts_refinished_on_successor": public_result(refit),
                "acts_refinished_after_bundle_v2_adoption": public_result(readopt),
            }
    body["wall_time_s"] = round(time.monotonic() - started, 1)
    text = json.dumps(body, indent=1, sort_keys=True) + "\n"
    assert not re.search(r"/(?:Users|private|tmp|var)/", text), "local path in p0.json"
    args.out.write_text(text, encoding="utf-8")
    print(json.dumps({
        "title_shown_on_v103": body["title_shown_on_v103"],
        "answered_line": body["answered"].get("line_27a"),
        "unanswered_line": body["unanswered"].get("line_27a"),
        "successor": body.get("successor_build", {}).get("status"),
        "loads": {
            name: {
                "refusal": row.get("refusal"),
                "line": row.get("line_27a"),
                "kernel_title_published": (row.get("kernel") or {}).get("title_is_published"),
                "kernel_title_successor": (row.get("kernel") or {}).get("title_is_successor"),
                "findings": (row.get("kernel") or {}).get("findings"),
                "package": (row.get("kernel") or {}).get("package_adoption"),
            }
            for name, row in body.get("loads", {}).items()
        },
        "wall_time_s": body["wall_time_s"],
    }, indent=1))


if __name__ == "__main__":
    main()
