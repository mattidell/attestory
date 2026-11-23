"""P0 census of page-owned visible strings across all 775 recorded lists.

Runs every recorded act list from tools/recorded_replay.py on published core
v100 (registry v98, release v98) through live_coordinate_run and
live_session._render_page, then evaluates every rendering condition of
packages/presentation/pages/citation-walk.v1.html on each saved presentation
model to count how many recorded lists show each string kind.

Usage:
    python3 census.py <outside-repo-scratch-dir> [--core v100] [--workers N] [--limit N]

The resumable part file and any rendered HTML pages stay outside the repository.
Committed output is written to census.json beside this script (synthetic demo.*
data only; no absolute or local paths).
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
import time
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from packages.derivation.live_session import _render_page
from tools import recorded_replay as rr

KNOWN_DISPOSITIONS = frozenset(
    ("published_value", "computed_zero", "closure_backed_zero", "published_categorical")
)
NUMERIC_DISPOSITIONS = frozenset(("published_value", "computed_zero", "closure_backed_zero"))
ATTACHMENT_KNOWN_CODES = frozenset(
    ("DEPENDENCY_ABSENT", "ITEMIZATION_TIE_OUT_VIOLATION", "COMPLETENESS_VALUE_VIOLATION")
)
ATTACHMENT_EXPLAIN = {
    "published": "This attachment is required and complete.",
    "blocked": "This attachment is required, but is incomplete: a required condition is missing or violated.",
    "guard_inapplicable": "This attachment is not required for this return.",
}
QUESTION_STATUS = {
    "current": "A response is recorded for this scope.",
    "stale": "This scope needs reconfirmation.",
    "unanswered": "This scope needs an answer.",
}
NUMERIC_STR_RE = re.compile(r"^-?\d+(?:\.\d+)?$")
LOCAL_PATH_RE = re.compile(r"/(?:Users|private|tmp|var|opt)/")


class _PageError(Exception):
    def __init__(self, reason_code: str) -> None:
        super().__init__(reason_code)
        self.reason_code = reason_code


def _is_finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _fmt_num(value: Any) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def _check_explanation_node(node: Any) -> None:
    if (
        not isinstance(node, dict)
        or not isinstance(node.get("id"), str)
        or node.get("kind") not in ("derived", "input", "reference")
        or not isinstance(node.get("edges"), list)
    ):
        raise _PageError("malformed-shared-explanation")
    if node["kind"] != "derived" and node["edges"]:
        raise _PageError("malformed-shared-explanation")
    if node["kind"] == "reference" and (
        node.get("symbol") is not None
        or node.get("value") is not None
        or node.get("produced_by") is not None
    ):
        raise _PageError("malformed-shared-explanation")


def _check_explanation_edge(edge: Any, graph: dict[str, Any]) -> None:
    if not isinstance(edge, dict) or not isinstance(edge.get("pin"), dict):
        raise _PageError("malformed-shared-explanation")
    target = (graph.get("nodes") or {}).get(edge.get("target"))
    pin = edge["pin"]
    if (
        not isinstance(pin.get("role"), str)
        or not isinstance(target, dict)
        or pin.get("id") != target.get("id")
        or (pin["role"] not in ("input", "choice") and target.get("kind") != "reference")
        or (target.get("kind") != "derived" and pin.get("version") != target.get("version"))
    ):
        raise _PageError("malformed-shared-explanation")


def _validate_shared_section(model: dict[str, Any], section: dict[str, Any]) -> dict[str, Any] | None:
    schema = model.get("schema")
    if schema == "presentation-model.v1":
        return None
    if schema not in ("presentation-model.v2", "presentation-model.v3"):
        raise _PageError("malformed-shared-explanation")
    graph = model.get("explanationGraph")
    section_root = (model.get("sectionRoots") or {}).get(section.get("id"))
    if (
        not isinstance(graph, dict)
        or graph.get("schema") != "explanation-graph.v1"
        or graph.get("run_id") != model.get("runId")
        or not isinstance(graph.get("roots"), list)
        or not isinstance(graph.get("nodes"), dict)
        or not isinstance(section_root, dict)
    ):
        raise _PageError("malformed-shared-explanation")
    if section_root.get("kind") == "disposition":
        disp = (section.get("resolved") or {}).get("disposition")
        if disp in NUMERIC_DISPOSITIONS or disp == "published_categorical":
            raise _PageError("malformed-shared-explanation")
        table = model.get("dispositionNodes") or {}
        seen: set[str] = set()
        active: set[str] = set()
        g_seen: set[str] = set()
        g_active: set[str] = set()

        def check_finding(key: str) -> None:
            if key in g_active:
                raise _PageError("malformed-shared-explanation")
            if key in g_seen:
                return
            node = graph["nodes"].get(key)
            _check_explanation_node(node)
            g_active.add(key)
            for edge in node["edges"]:
                _check_explanation_edge(edge, graph)
                check_finding(edge["target"])
            g_active.remove(key)
            g_seen.add(key)

        def check_disp(key: str) -> None:
            if key in active:
                raise _PageError("malformed-shared-explanation")
            if key in seen:
                return
            node = table.get(key)
            if (
                not isinstance(node, dict)
                or node.get("symbol") != key
                or not isinstance(node.get("records"), list)
                or not isinstance(node.get("children"), list)
            ):
                raise _PageError("malformed-shared-explanation")
            if node.get("findingRoot"):
                check_finding(node["findingRoot"])
            active.add(key)
            for child in node["children"]:
                check_disp(child)
            active.remove(key)
            seen.add(key)

        root_key = section_root.get("root")
        if not isinstance(root_key, str):
            raise _PageError("malformed-shared-explanation")
        check_disp(root_key)
        root_node = table[root_key]
        expected = "inapplicable" if disp == "guard_inapplicable" else disp
        if (
            root_node["symbol"] != (section.get("field") or {}).get("binds_symbol")
            or not root_node["records"]
            or any(r.get("disposition") != expected for r in root_node["records"])
        ):
            raise _PageError("malformed-shared-explanation")
        return {"graph": graph, "disposition": root_key}

    if section_root.get("kind") != "published" or not isinstance(section_root.get("root"), int):
        raise _PageError("malformed-shared-explanation")
    idx = section_root["root"]
    if idx < 0 or idx >= len(graph["roots"]) or not isinstance(graph["roots"][idx], dict):
        raise _PageError("malformed-shared-explanation")
    root = graph["roots"][idx]
    colors: dict[str, int] = {}

    def validate(key: str) -> None:
        if colors.get(key) == 1:
            raise _PageError("malformed-shared-explanation")
        if colors.get(key) == 2:
            return
        node = graph["nodes"].get(key)
        _check_explanation_node(node)
        colors[key] = 1
        for edge in node["edges"]:
            _check_explanation_edge(edge, graph)
            validate(edge["target"])
        colors[key] = 2

    validate(root["target"])
    act = (section.get("resolved") or {}).get("act")
    finding = act.get("finding") if isinstance(act, dict) else None
    node = graph["nodes"][root["target"]]
    if (
        not isinstance(finding, dict)
        or act.get("run_id") != model.get("runId")
        or node["kind"] != "derived"
        or node["id"] != finding.get("id")
        or node.get("version") != finding.get("version")
        or node.get("symbol") != finding.get("symbol")
        or node.get("value") != finding.get("value")
        or not isinstance(finding.get("pins"), list)
    ):
        raise _PageError("malformed-shared-explanation")
    return {"graph": graph, "root": root}


def classify_model_strings(model: dict[str, Any]) -> dict[str, Any]:
    """Evaluate every string kind rendered by citation-walk.v1.html on one saved model."""
    examples: dict[str, str] = {}
    extra: dict[str, set[str]] = {
        "line_blocked_codes": set(),
        "attach_blocked_codes": set(),
        "trace_edge_roles": set(),
        "trace_root_roles": set(),
        "trace_disp_values": set(),
        "error_codes": set(),
        "optional_blocks": set(),
        "schemas": set(),
    }

    def mark(kind: str, sample: str) -> None:
        if kind not in examples:
            examples[kind] = sample[:240]

    extra["schemas"].add(str(model.get("schema") or ""))
    for blk in (
        "line21Explanation",
        "mortgageInterestExplanation",
        "mortgageBorrowingExplanation",
        "diagnostics",
        "citationGroups",
        "attachments",
        "questionGroups",
    ):
        val = model.get(blk)
        if val is not None and (not isinstance(val, list) or len(val) > 0):
            extra["optional_blocks"].add(blk)

    # Static shell strings (always rendered)
    mark("shell.title", "Form 1040 — Citation Walk")
    mark("shell.skip_link", "Skip to main content")
    mark("shell.heading", "Form 1040 — Citation Walk")
    mark(
        "shell.subtitle",
        "Every figure below is projected from a cited source fact. Nothing on this page is computed here.",
    )

    # Build citation registry exactly as citation-walk.v1.html:210-233
    sites_by_pin: dict[str, list[dict[str, Any]]] = {}
    all_sites: list[dict[str, Any]] = []
    for section in model.get("sections") or []:
        for site in section.get("citationSites") or []:
            all_sites.append(site)
        disp = (section.get("resolved") or {}).get("disposition")
        citation = (section.get("field") or {}).get("citation")
        if disp in KNOWN_DISPOSITIONS and isinstance(citation, dict) and citation.get("id") and citation.get("version"):
            all_sites.append(
                {
                    "siteId": f"{section['id']}-field-citation",
                    "pinId": citation["id"],
                    "pinVersion": citation["version"],
                    "context": (section.get("field") or {}).get("label") or section["id"],
                }
            )
    for group in model.get("citationGroups") or []:
        for part in group.get("parts") or []:
            for site in part.get("citationSites") or []:
                all_sites.append(site)
    for site in all_sites:
        key = f"{site['pinId']}@{site['pinVersion']}"
        sites_by_pin.setdefault(key, []).append(site)

    pin_labels = model.get("pinLabels") or {}

    def record_citation(site_id: str, pin_id: str, pin_version: str) -> None:
        key = f"{pin_id}@{pin_version}"
        label = pin_labels.get(pin_id)
        if label:
            mark("citation.button_labeled", str(label))
        else:
            mark("citation.button_fallback_id", key)
        mark("citation.detail.pin_id_label", f"Pin id: {pin_id}")
        mark("citation.detail.pin_version_label", f"Pin version: {pin_version}")
        mark("citation.detail.aria_label", f"Citation detail for {pin_id}")
        siblings = [s for s in sites_by_pin.get(key, []) if s["siteId"] != site_id]
        if siblings:
            mark("citation.detail.backlink", f"also cited in {siblings[0]['context']}")

    # Question groups panel (renderQuestionGroups)
    try:
        if model.get("schema") == "presentation-model.v3":
            qgroups = model.get("questionGroups")
            if not isinstance(qgroups, list):
                raise _PageError("malformed-question-groups")
            sections_by_group: dict[str, list[tuple[dict[str, Any], str]]] = {}
            for section in model.get("sections") or []:
                refs = (section.get("resolved") or {}).get("questionRefs")
                if refs is None:
                    continue
                if not isinstance(refs, list):
                    raise _PageError("malformed-question-groups")
                for ref in refs:
                    if not isinstance(ref, dict) or not isinstance(ref.get("scopes"), list):
                        raise _PageError("malformed-question-groups")
                    rows = sections_by_group.setdefault(ref["groupId"], [])
                    for scope in ref["scopes"]:
                        if not isinstance(scope, dict) or not isinstance(scope.get("status"), str):
                            raise _PageError("malformed-question-groups")
                        rows.append((section, scope["status"]))
            if qgroups:
                mark("qgroups.heading", "Questions for blocked lines")
                seen_ids: set[str] = set()
                for group in qgroups:
                    gid = group.get("id")
                    if not isinstance(gid, str) or not gid or gid in seen_ids or not isinstance(group.get("question"), str) or not group["question"]:
                        raise _PageError("malformed-question-groups")
                    seen_ids.add(gid)
                    slabel = (group.get("answerTarget") or {}).get("statementLabel")
                    if slabel:
                        parts = [slabel.get(k) for k in ("statement", "lender", "taxYear") if isinstance(slabel.get(k), str) and slabel.get(k)]
                        if not parts:
                            raise _PageError("malformed-question-groups")
                        mark("qgroups.target_prefix", "For " + ", ".join(parts))
                    rows = sections_by_group.get(gid) or []
                    if not rows:
                        raise _PageError("malformed-question-groups")
                    for sec, status in rows:
                        if status not in QUESTION_STATUS:
                            raise _PageError("malformed-question-groups")
                        field = sec.get("field") or {}
                        lbl = (field.get("label") if isinstance(field.get("label"), str) else sec["id"]) + (
                            f" (Line {field['line']})" if field.get("line") is not None else ""
                        )
                        mark("qgroups.affected_line_suffix", f"{lbl} — {QUESTION_STATUS[status]}")
                        mark(f"qgroups.status.{status}", QUESTION_STATUS[status])
                if len(seen_ids) != len(sections_by_group):
                    raise _PageError("malformed-question-groups")
    except _PageError as exc:
        extra["error_codes"].add(exc.reason_code)
        mark(f"err.{exc.reason_code}", exc.reason_code)

    def qrefs_for_reasons(resolved: dict[str, Any]) -> dict[int, list[dict[str, Any]]]:
        if model.get("schema") != "presentation-model.v3":
            return {}
        refs = resolved.get("questionRefs")
        if refs is None:
            return {}
        if resolved.get("disposition") != "blocked" or not isinstance(refs, list):
            raise _PageError("malformed-question-groups")
        groups = {g["id"]: g for g in (model.get("questionGroups") or []) if isinstance(g, dict) and "id" in g}
        by_reason: dict[int, list[dict[str, Any]]] = {}
        reasons = resolved.get("reasons") or []
        for ref in refs:
            group = groups.get(ref.get("groupId")) if isinstance(ref, dict) else None
            if not group or not isinstance(ref.get("reasonIndices"), list) or not isinstance(ref.get("scopes"), list) or not ref["scopes"]:
                raise _PageError("malformed-question-groups")
            for idx in ref["reasonIndices"]:
                if not isinstance(idx, int) or idx < 0 or idx >= len(reasons) or reasons[idx].get("sentence") != group["question"]:
                    raise _PageError("malformed-question-groups")
                by_reason.setdefault(idx, []).append(group)
        return by_reason

    def walk_shared(shared: dict[str, Any]) -> None:
        mark("trace.summary", "Trace recorded support")
        graph = shared["graph"]
        visited: set[str] = set()

        def show_node(key: str, role: str) -> None:
            node = graph["nodes"][key]
            if key in visited:
                mark("trace.node.reuse_button", f"{role}: reused {node.get('symbol') or node['id']}")
                return
            visited.add(key)
            val = node.get("value")
            numeric = node["kind"] == "input" and (
                _is_finite_number(val) or (isinstance(val, str) and bool(NUMERIC_STR_RE.match(val)))
            )
            caption = f"{role}: {node.get('symbol') or node['id']}" + (f" = {_fmt_num(val)}" if numeric else "")
            mark("trace.node.caption", caption)
            if numeric:
                mark("trace.node.caption_numeric_input", caption)
            if node.get("produced_by") and isinstance(node["produced_by"].get("id"), str):
                mark("trace.node.producer", " — " + node["produced_by"]["id"])
            for edge in node["edges"]:
                pin = edge["pin"]
                extra["trace_edge_roles"].add(str(pin["role"]))
                mark("trace.node.edge_button", f"Show {pin['role']} {pin['id']}")
                show_node(edge["target"], pin["role"])

        disp_visited: set[str] = set()

        def show_disp(key: str) -> None:
            node = model["dispositionNodes"][key]
            if key in disp_visited:
                mark("trace.disp.reuse_button", f"Reused {node['symbol']}")
                return
            disp_visited.add(key)
            if node["records"]:
                dval = str(node["records"][0]["disposition"])
                extra["trace_disp_values"].add(dval)
                mark("trace.disp.caption", f"{node['symbol']}: {dval}")
            else:
                mark("trace.disp.no_records_caption", f"{node['symbol']}: no recorded disposition")
            if node.get("findingRoot"):
                mark("trace.disp.predecessor_button", "Show recorded predecessor")
                show_node(node["findingRoot"], "input")
            for ref in node["children"]:
                mark("trace.disp.dependency_button", f"Show dependency {ref}")
                show_disp(ref)

        if "disposition" in shared:
            show_disp(shared["disposition"])
        else:
            extra["trace_root_roles"].add(str(shared["root"]["role"]))
            show_node(shared["root"]["target"], shared["root"]["role"])

    def walk_line21(section: dict[str, Any], block: dict[str, Any]) -> None:
        mark("line21.heading", "Statements on this line")
        for row in block.get("rows") or []:
            slabel = row.get("statementLabel") or {}
            parts = [slabel.get(k) for k in ("statement", "lender", "taxYear") if isinstance(slabel.get(k), str) and slabel.get(k)]
            if not parts:
                mark("line21.statement_fallback", "Statement")
            for loan in row.get("loans") or []:
                mark("line21.loan_prefix", f"loan: {loan}")
            if row.get("amount") is not None:
                if row.get("account"):
                    mark("line21.amount.with_account", f"Form 1098-E box 1: {_fmt_num(row['amount'])}")
                else:
                    mark("line21.amount.without_account", f"{_fmt_num(row['amount'])} reported")
            status = row.get("status") or {}
            if status.get("kind") == "named-by-reason" and status.get("reasonIndices"):
                mark("line21.reason_link", "See the reason above")
            account = row.get("account")
            basis = row.get("basis")
            if account:
                mark("line21.account.summary", "What this form accounts for")
                mark("line21.account.group_headings", "What the person said / What the calculation used / What it assumed / Recorded, not used")
                older = (account.get("said") or {}).get("olderAnswer") or {}
                if older.get("currency") == "absent":
                    mark("line21.account.older_absent", "Older answer about this form's box 1: absent. No older answer was recorded.")
                elif older:
                    mark("line21.account.older_present", f"Older answer about this form's box 1: {older.get('value')}. Currency: {older.get('currency')}.")
                for item in (account.get("said") or {}).get("current") or []:
                    prop = (item["proposition"] + " ") if item.get("proposition") else ""
                    mark("line21.account.said_current", f"Current. {prop}Recorded answer: {item.get('response')}.")
                for item in (account.get("said") or {}).get("history") or []:
                    prop = (item["proposition"] + " ") if item.get("proposition") else ""
                    mark("line21.account.said_history", f"History, not current. {prop}Recorded answer: {item.get('response')}.")
                used = account.get("used") or {}
                mark("line21.account.used_sentence", str(used.get("kind") or ""))
                mark("line21.account.combined_class", f"Combined class: {used.get('combined')}.")
                if used.get("kind") == "nothing":
                    mark("line21.account.assumed_nothing", "Nothing favorable is assumed. The reason is named above.")
                elif basis:
                    for sent in basis.get("leftWithPerson") or []:
                        mark("line21.account.left_with_you_prefix", f"Left with you: {sent}")
                if not (account.get("recordedNotUsed") or []):
                    mark("line21.account.recorded_none", "None.")
            elif basis:
                mark("line21.basis.summary", "What this statement's loan link rests on")
                mark("line21.basis.group_headings", "What you told us / What the application took as given / Conditions left with you")
                for ans in basis.get("answers") or []:
                    if ans.get("proposition"):
                        mark("line21.basis.answer_with_prop", f"{ans['proposition']} Recorded answer: {ans['response']}.")
                    else:
                        mark("line21.basis.answer_no_prop", f"Recorded answer: {ans['response']}. Question wording was not saved with this answer.")
        working = block.get("working")
        if working:
            mark("line21.working.summary", "How the amount was worked out")
            mark("line21.working.interest_reported", f"Interest reported (worksheet line 1): {_fmt_num(working.get('lineOneSubtotal'))}")
            if working.get("totalIncome") is not None:
                mark("line21.working.income_used", f"Income the worksheet used: {_fmt_num(working.get('totalIncome'))}")
            params = working.get("parameters") or []
            for p in params:
                mark("line21.working.limit_row", f"Limit {p.get('label') or p.get('title') or p.get('id')}: {p.get('value')}")
            mark("line21.working.deduction", f"Deduction: {_fmt_num(working.get('value'))}")
            if params:
                mark("line21.working.limits_caveat", "This page does not say which of these limits changed the amount.")
        mark(
            "line21.run_footer",
            f"This explanation describes run {block.get('runId')}, which read workspace revision {block.get('workspaceRevision')}. Later changes to the workspace are not reflected here.",
        )
        cit_count = len(section.get("citationSites") or []) + (
            1 if (section.get("resolved") or {}).get("disposition") in NUMERIC_DISPOSITIONS else 0
        )
        if cit_count > 0:
            mark("line21.citations.summary", f"All records this line depends on ({cit_count})")

    # Sections
    for section in model.get("sections") or []:
        try:
            shared = _validate_shared_section(model, section)
            field = section.get("field") or {}
            resolved = section.get("resolved") or {}
            disp = resolved.get("disposition")
            is_line21 = section.get("id") == "line-sch1-21"
            has_line21_block = is_line21 and model.get("line21Explanation") is not None
            inst_key = "published_value" if disp == "published_categorical" else disp
            dispositions = field.get("dispositions") or {}
            if inst_key not in dispositions:
                raise _PageError("unrecognized-disposition")
            instruction = dispositions[inst_key]
            if not instruction:
                raise _PageError("missing-instruction")

            mark("line.heading_line_suffix", f"{field.get('label')} (Line {field.get('line')})")
            mark(f"line.badge.{disp}", str(disp).replace("_", " "))

            if disp in NUMERIC_DISPOSITIONS:
                val = resolved.get("value")
                if not _is_finite_number(val):
                    raise _PageError("invalid-numeric-value")
                citation = field.get("citation")
                if not isinstance(citation, dict) or not citation.get("id") or not citation.get("version"):
                    raise _PageError("missing-field-citation")
                for site in section.get("citationSites") or []:
                    record_citation(site["siteId"], site["pinId"], site["pinVersion"])
                record_citation(f"{section['id']}-field-citation", citation["id"], citation["version"])
                if has_line21_block:
                    walk_line21(section, model["line21Explanation"])
            elif disp == "published_categorical":
                render_tok = instruction.get("render")
                if render_tok not in ("checked", "not_checked"):
                    raise _PageError("missing-instruction")
                shown = "checked" if render_tok == "checked" else "not checked"
                mark(f"line.categorical.{render_tok}", shown)
                citation = field.get("citation")
                if not isinstance(citation, dict) or not citation.get("id") or not citation.get("version"):
                    raise _PageError("missing-field-citation")
                record_citation(f"{section['id']}-field-citation", citation["id"], citation["version"])
            elif disp == "blocked":
                codes = resolved.get("activeCodes") if isinstance(resolved.get("activeCodes"), list) else []
                known_codes = set(instruction.get("codes") or [])
                shown_codes = [c for c in codes if c in known_codes]
                reasons = resolved.get("reasons") if isinstance(resolved.get("reasons"), list) else []
                qrefs = qrefs_for_reasons(resolved)
                for idx, reason in enumerate(reasons):
                    if not isinstance(reason, dict) or not isinstance(reason.get("sentence"), str) or not reason["sentence"]:
                        raise _PageError("unknown-error")
                    if idx in qrefs:
                        mark("line.blocked.question_group_link", "See the question and affected lines above")
                        if len(qrefs[idx]) > 1:
                            mark("line.blocked.question_group_link_multi", "; ")
                    else:
                        slabel = reason.get("statementLabel") or {}
                        parts = [slabel.get(k) for k in ("statement", "lender") if isinstance(slabel.get(k), str) and slabel.get(k)]
                        if parts:
                            mark("line.blocked.reason_statement_prefix", ", ".join(parts) + ": " + reason["sentence"])
                mark("line.blocked.banner_heading", "No value published — cannot compute.")
                if not (is_line21 and reasons):
                    mark("line.blocked.missing_codes_label", "Missing dependency code(s): ")
                    if shown_codes:
                        for c in shown_codes:
                            extra["line_blocked_codes"].add(str(c))
                        mark("line.blocked.missing_codes_value", ", ".join(shown_codes))
                    else:
                        mark("line.blocked.missing_codes_unspecified", "(unspecified)")
                if reasons:
                    mark("line.blocked.why_label", "Why: ")
                else:
                    mark("line.blocked.remedy", "Remedy: contribute the missing dependency to unblock this line.")
                if has_line21_block:
                    walk_line21(section, model["line21Explanation"])
            elif disp == "guard_inapplicable":
                mark("line.guard_inapplicable.value", "Not applicable.")
            else:
                raise _PageError("unrecognized-disposition")

            if shared is not None:
                walk_shared(shared)
        except _PageError as exc:
            extra["error_codes"].add(exc.reason_code)
            mark(f"err.{exc.reason_code}", exc.reason_code)

    # Attachments
    for att in model.get("attachments") or []:
        try:
            resolved = att.get("resolved") or {}
            disp = resolved.get("disposition")
            if disp not in ATTACHMENT_EXPLAIN:
                raise _PageError("unrecognized-disposition")
            mark(f"attach.badge.{disp}", str(disp).replace("_", " "))
            mark(f"attach.explain.{disp}", ATTACHMENT_EXPLAIN[disp])
            if disp == "blocked":
                codes = resolved.get("activeCodes") if isinstance(resolved.get("activeCodes"), list) else []
                for c in codes:
                    if c not in ATTACHMENT_KNOWN_CODES:
                        raise _PageError("unrecognized-attachment-code")
                mark("attach.blocked.banner_heading", "Not shown — required and incomplete.")
                mark("attach.blocked.codes_label", "Missing or violated condition code(s): ")
                if codes:
                    for c in codes:
                        extra["attach_blocked_codes"].add(str(c))
                    mark("attach.blocked.codes_value", ", ".join(codes))
                else:
                    mark("attach.blocked.codes_unspecified", "(unspecified)")
                mark(
                    "attach.blocked.remedy",
                    "Remedy: contribute or correct the missing or violated condition to complete this attachment.",
                )
            elif disp == "guard_inapplicable":
                mark("attach.guard_inapplicable.value", "Not required.")
        except _PageError as exc:
            extra["error_codes"].add(exc.reason_code)
            mark(f"err.{exc.reason_code}", exc.reason_code)

    # Citation groups
    for group in model.get("citationGroups") or []:
        for part in group.get("parts") or []:
            for site in part.get("citationSites") or []:
                record_citation(site["siteId"], site["pinId"], site["pinVersion"])

    # Diagnostics
    sections_by_id = {s.get("id"): s for s in (model.get("sections") or []) if isinstance(s, dict)}
    for diag in model.get("diagnostics") or []:
        healthy = True
        for sid in diag.get("inputs") or []:
            sec = sections_by_id.get(sid)
            if not sec:
                healthy = False
                break
            res = sec.get("resolved") or {}
            if res.get("disposition") not in NUMERIC_DISPOSITIONS or not _is_finite_number(res.get("value")):
                healthy = False
                break
        if not healthy:
            mark("diag.suppressed", "Not shown — computed from a blocked or inapplicable input.")

    # Optional mortgage/line21 blocks (check presence; recorded corpus rarely produces them)
    if model.get("mortgageInterestExplanation") is not None:
        mark("mort_int.heading", "Form 1098 mortgage interest account")
    if model.get("mortgageBorrowingExplanation") is not None:
        mark("mort_borr.heading", "Connected mortgage borrowing")

    return {
        "kinds": sorted(examples),
        "examples": examples,
        "extra": {k: sorted(v) for k, v in extra.items()},
    }


def per_list(key: str, acts: list[dict[str, Any]], core: Any) -> dict[str, Any]:
    """Run one recorded list through live_coordinate_run + _render_page and classify strings."""
    resolved = rr.resolve_core(core)
    harness = rr._get_harness()
    slug = hashlib.sha256(key.encode("utf-8")).hexdigest()[:20]
    run_id = "demo.ppw." + slug
    try:
        with harness.loader_entries(resolved):
            finished = harness._finish(
                acts,
                package_path=resolved.package_path,
                package_version=resolved.version,
                release_path=resolved.release_path,
                release_version=resolved.release_version,
                note=run_id,
            )
            finished = harness._handover(finished, surface=resolved.surface(), reconfirm=True)
            with tempfile.TemporaryDirectory() as tmp:
                cap = harness.WorkspaceCapability(Path(tmp) / "L")
                outcome = harness.live_coordinate_run(
                    cap,
                    repo_root=REPO,
                    authoritative_acts=finished,
                    workspace_revision=len(finished),
                    run_scope={"jurisdiction": "us", "year": harness.YEAR},
                    scope_user=harness.ccr.USER,
                    request={"schema": "run-request.v1"},
                    run_id=run_id,
                    governance_pins=[],
                    surface=resolved.surface(),
                    output_name="out.json",
                )
                if outcome.refusal is not None:
                    return {"outcome": "refused", "error": "refusal", "message": str(outcome.refusal.reason)}
                assert outcome.presentation_path is not None
                page_bytes = _render_page(REPO, cap, outcome.presentation_path)
                model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
                info = classify_model_strings(model)
                save_dir = os.environ.get("PPW_SAVE_HTML_DIR")
                if save_dir and key in (os.environ.get("PPW_SAVE_KEYS") or "").split(","):
                    (Path(save_dir) / f"{slug}.html").write_bytes(page_bytes)
                    (Path(save_dir) / f"{slug}.model.json").write_text(
                        json.dumps(model, sort_keys=True), encoding="utf-8"
                    )
                return {
                    "outcome": "success",
                    "page_bytes": len(page_bytes),
                    "section_count": len(model.get("sections") or []),
                    "attachment_count": len(model.get("attachments") or []),
                    **info,
                }
    except Exception as exc:
        clean = re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", str(exc))[:400]
        return {"outcome": "error", "error": type(exc).__name__, "message": clean}


def _write_clean_json(path: Path, payload: dict[str, Any]) -> None:
    text = json.dumps(payload, indent=2) + "\n"
    if LOCAL_PATH_RE.search(text):
        raise ValueError(f"Refusing to write local path into {path}")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="P0 page-plain-words census across the 775 recorded lists.")
    parser.add_argument("scratch", type=Path, help="Outside-repo directory for resumable part file")
    parser.add_argument("--core", default="v100", help="Published core version (default: v100)")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--limit", type=int, default=None, help="Optional limit for smoke testing")
    parser.add_argument("--out", type=Path, default=HERE / "census.json")
    args = parser.parse_args()

    scratch = args.scratch.resolve()
    if scratch == REPO or REPO in scratch.parents:
        raise SystemExit("scratch directory must be outside the repository")
    scratch.mkdir(parents=True, exist_ok=True)

    lists = rr.recorded_lists()
    total_recorded = len(lists)
    if args.limit is not None:
        lists = lists[: args.limit]
    core = rr.resolve_core(args.core)
    workers = args.workers or max(1, (os.cpu_count() or 2) - 1)
    part_path = scratch / ("census-part-smoke.json" if args.limit is not None else "census-part.json")

    started = time.monotonic()
    results = rr.replay(lists, core, per_list, workers=workers, part=part_path)
    wall = round(time.monotonic() - started, 3)

    outcomes = Counter(r["outcome"] for r in results.values())
    errors = Counter(r.get("error") for r in results.values() if r["outcome"] != "success")
    kind_counts: Counter[str] = Counter()
    kind_examples: dict[str, str] = {}
    kind_first_list: dict[str, str] = {}
    extra_counts: dict[str, Counter[str]] = {}

    for key, row in sorted(results.items()):
        if row["outcome"] != "success":
            continue
        for kind in row["kinds"]:
            kind_counts[kind] += 1
            if kind not in kind_examples:
                kind_examples[kind] = row["examples"][kind]
                kind_first_list[kind] = key
        for bucket, values in row["extra"].items():
            c = extra_counts.setdefault(bucket, Counter())
            for val in values:
                c[val] += 1

    summary = {
        "format": "page-plain-words-p0-census.v1",
        "source": {
            "core": core.version,
            "registry": core.registry,
            "release": core.release_version,
            "page": "packages/presentation/pages/citation-walk.v1.html",
        },
        "recorded_lists_total": total_recorded,
        "lists_attempted": len(results),
        "lists_rendered": outcomes.get("success", 0),
        "outcomes": dict(sorted(outcomes.items())),
        "non_success_errors": dict(sorted(errors.items())),
        "workers": workers,
        "wall_time_s": wall,
        "string_kind_counts": {
            k: {
                "lists": kind_counts[k],
                "example": kind_examples[k],
                "sample_list": kind_first_list[k],
            }
            for k in sorted(kind_counts)
        },
        "observed_details": {
            bucket: dict(sorted(counter.items())) for bucket, counter in sorted(extra_counts.items())
        },
    }

    if args.limit is None:
        _write_clean_json(args.out, summary)
    print(
        json.dumps(
            {
                "lists_attempted": summary["lists_attempted"],
                "lists_rendered": summary["lists_rendered"],
                "outcomes": summary["outcomes"],
                "non_success_errors": summary["non_success_errors"],
                "wall_time_s": wall,
                "distinct_kinds_observed": len(kind_counts),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
