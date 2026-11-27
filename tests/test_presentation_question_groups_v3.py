"""Question grouping through the current saved-page path and old readers."""
from __future__ import annotations

import copy
import html
import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, cast

import pytest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_session import _render_page
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.presentation_projection import (
    PresentationModelError,
    _finalize_question_references,
    _question_group_catalog,
    _question_group_id,
    _reasons_beside,
    build_presentation_model,
    project_presentation_v1,
    validate_presentation_model,
)
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.facts import EntityLifecycle, KernelState, fact_id_for
from packages.kernel.findings import FindingState
from packages.kernel.horizons import HORIZON_ENTITY_KIND, HorizonState
from tests import test_noncovered_sales_v79 as sales_v79
from tests.helpers.chrome_startup_slot import browser_startup_slot
from tests.helpers.current_core_returns import state_taxpayer_facts
from tests.test_no1099b_sales_v80 import build_world as build_v80_world
from tests.test_sli_line21_explanation_page import BROWSER
from tests.test_presentation_l2_integration import FIELD as L2_FIELD
from tools.sale_page_observation import _prepare_v89_covered_sale_companions

ROOT = Path(__file__).resolve().parents[1]
QUESTION = "Did you sell any securities whose basis was not reported to the IRS?"
LINE9_FIELD = "tax.us.2025.schedule-d.line-9"
LINE9_EXPLANATION = (
    "Schedule D line 9, column (h), has no value yet. It waits for your answers about sales "
    "whose basis was not reported to the IRS, or for a recorded long-term sale of that kind "
    "to pass its checks."
)
OLD_V2 = ROOT / "packages/sample_data/derivation/explanation_sharing/presentation-model.exact-pins.v2.json"


def _demo_fact_type(fact_type_id: str) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": fact_type_id,
        "version": "v1",
        "nature": "determinable",
        "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
    }


def test_same_worded_input_questions_keep_distinct_answer_targets() -> None:
    first_type = "demo.answer-target.first"
    second_type = "demo.answer-target.second"
    state = FindingState(fact_state=KernelState(fact_types={
        first_type: _demo_fact_type(first_type),
        second_type: _demo_fact_type(second_type),
    }))
    producers = [
        {
            "schema": "input-question.v1",
            "id": "demo.input-question.first",
            "version": "v1",
            "fact_type": {"id": first_type, "version": "v1"},
            "question": QUESTION,
        },
        {
            "schema": "input-question.v1",
            "id": "demo.input-question.second",
            "version": "v1",
            "fact_type": {"id": second_type, "version": "v1"},
            "question": QUESTION,
        },
    ]

    groups, _by_family, _by_fact_type = _question_group_catalog(
        producers, state, current_finding_ids=frozenset(), authoritative_acts=(),
    )

    assert len(groups) == 2
    [first, second] = groups.values()
    assert first["question"] == second["question"] == QUESTION
    assert first["id"] != second["id"]
    assert first["answerTarget"]["factId"] != second["answerTarget"]["factId"]


def test_projection_links_only_the_exact_missing_statement_target() -> None:
    fact_type_id = "demo.statement-scoped-question"
    first_statement = "demo.statement.first"
    second_statement = "demo.statement.second"
    statement_kind = "demo.statement"
    fact_type = {
        "schema": "fact-type.v2",
        "id": fact_type_id,
        "version": "v1",
        "nature": "determinable",
        "identity_keys": [
            {"name": "statement", "kind": "entity", "entity_kind": statement_kind},
            {"name": "tax-year", "kind": "literal", "values": ["2025"]},
        ],
        "value_schema": {"type": "string"},
    }
    fact_state = KernelState(
        fact_types={fact_type_id: fact_type},
        entities={
            statement_id: EntityLifecycle(
                entity={
                    "schema": "entity.v1",
                    "id": statement_id,
                    "kind": statement_kind,
                    "label": label,
                },
                status="current",
            )
            for statement_id, label in (
                (first_statement, "Demo statement one"),
                (second_statement, "Demo statement two"),
            )
        },
    )
    first_fact_id = fact_id_for(fact_type_id, (("statement", first_statement), ("tax-year", "2025")))
    second_fact_id = fact_id_for(fact_type_id, (("statement", second_statement), ("tax-year", "2025")))
    current_finding_id = "demo.finding.current-statement-answer"
    state = FindingState(
        fact_state=fact_state,
        findings={current_finding_id: {
            "schema": "finding.v1",
            "id": current_finding_id,
            "fact_id": first_fact_id,
            "value": "yes",
            "basis": "attested",
            "evidence_ids": [],
        }},
    )
    field = copy.deepcopy(L2_FIELD)
    field.update(id="demo.field.statement-question", binds_symbol="demo.symbol.statement-question")
    rule = {
        "schema": "rule-artifact.v2",
        "id": "demo.rule.statement-question",
        "publishes": "demo.symbol.statement-question",
    }
    question = {
        "schema": "input-question.v1",
        "id": "demo.input-question.statement-scoped",
        "version": "v1",
        "fact_type": {"id": fact_type_id, "version": "v1"},
        "question": QUESTION,
    }
    model = build_presentation_model(
        run_id="demo.statement-question-target",
        resolved_members=[field, rule, question],
        state=state,
        publications=[],
        dispositions=[{
            "artifact_id": rule["id"],
            "disposition": "blocked",
            "symbol": rule["publishes"],
            "code": "DEPENDENCY_ABSENT",
            "missing": [second_fact_id],
            "pins": [],
        }],
        current_finding_ids=frozenset({current_finding_id}),
    )

    [group] = model["questionGroups"]
    assert group["answerTarget"]["factId"] == second_fact_id
    assert group["answerTarget"]["statementLabel"] == {
        "statement": "Demo statement two",
        "taxYear": "2025",
    }
    section = model["sections"][0]
    [reference] = section["resolved"]["questionRefs"]
    assert reference["groupId"] == group["id"]
    assert reference["scopes"] == [{"kind": "fact", "id": second_fact_id, "status": "unanswered"}]
    assert first_fact_id not in {candidate["answerTarget"]["factId"] for candidate in model["questionGroups"]}

    type_only_model = build_presentation_model(
        run_id="demo.statement-question-type-only",
        resolved_members=[field, rule, question],
        state=state,
        publications=[],
        dispositions=[{
            "artifact_id": rule["id"],
            "disposition": "blocked",
            "symbol": rule["publishes"],
            "code": "DEPENDENCY_ABSENT",
            "missing": ["demo.binding.unscoped-answer"],
            "pins": [],
        }],
        symbol_fact_types={"demo.binding.unscoped-answer": fact_type_id},
        current_finding_ids=frozenset({current_finding_id}),
    )
    type_only_section = type_only_model["sections"][0]
    assert type_only_section["resolved"]["reasons"] == [{"sentence": QUESTION}]
    assert "questionRefs" not in type_only_section["resolved"]
    assert type_only_model["questionGroups"] == []

    single_target_state = FindingState(fact_state=KernelState(
        fact_types={fact_type_id: fact_type},
        entities={second_statement: fact_state.entities[second_statement]},
    ))
    single_target_model = build_presentation_model(
        run_id="demo.statement-question-single-target",
        resolved_members=[field, rule, question],
        state=single_target_state,
        publications=[],
        dispositions=[{
            "artifact_id": rule["id"],
            "disposition": "blocked",
            "symbol": rule["publishes"],
            "code": "DEPENDENCY_ABSENT",
            "missing": ["demo.binding.unscoped-answer"],
            "pins": [],
        }],
        symbol_fact_types={"demo.binding.unscoped-answer": fact_type_id},
        current_finding_ids=frozenset(),
    )
    [single_target_group] = single_target_model["questionGroups"]
    assert single_target_group["answerTarget"]["factId"] == second_fact_id
    assert single_target_group["answerTarget"]["statementLabel"]["statement"] == "Demo statement two"


def test_projection_suppresses_family_link_when_horizon_target_is_ambiguous() -> None:
    family_id = "demo.family.multi-scope"
    closure_type_id = "demo.family.multi-scope-closure"
    first_horizon = "demo.horizon.primary"
    second_horizon = "demo.horizon.secondary"
    first_scope = (("subject", "demo.primary"), ("tax-year", "2025"))
    second_scope = (("subject", "demo.secondary"), ("tax-year", "2025"))
    fact_type = {
        "schema": "fact-type.v2",
        "id": closure_type_id,
        "version": "v1",
        "nature": "determinable",
        "identity_keys": [
            {"name": "family-horizon", "kind": "entity", "entity_kind": HORIZON_ENTITY_KIND},
            {"name": "tax-year", "kind": "literal", "values": ["2025"]},
        ],
        "value_schema": {"type": "boolean"},
    }
    fact_state = KernelState(
        fact_types={closure_type_id: fact_type},
        entities={
            horizon_id: EntityLifecycle(
                entity={"schema": "entity.v1", "id": horizon_id, "kind": HORIZON_ENTITY_KIND},
                status="current",
            )
            for horizon_id in (first_horizon, second_horizon)
        },
    )
    state = FindingState(
        fact_state=fact_state,
        horizon_state=HorizonState(current_by_chain={
            (family_id, "v1", first_scope): first_horizon,
            (family_id, "v1", second_scope): second_horizon,
        }),
    )
    field = copy.deepcopy(L2_FIELD)
    field.update(id="demo.field.multi-scope-family", binds_symbol="demo.symbol.multi-scope-family")
    rule = {
        "schema": "rule-artifact.v2",
        "id": "demo.rule.multi-scope-family",
        "publishes": "demo.symbol.multi-scope-family",
    }
    mapping = {
        "schema": "source-closure-mapping.v4",
        "id": "demo.closure-mapping.multi-scope-family",
        "version": "v1",
        "closure_fact_type": {"id": closure_type_id, "version": "v1"},
        "closure_question": QUESTION,
        "families": [{"family": {"id": family_id, "version": "v1"}}],
    }
    model = build_presentation_model(
        run_id="demo.family-multiple-scope-targets",
        resolved_members=[field, rule, mapping],
        state=state,
        publications=[],
        dispositions=[{
            "artifact_id": rule["id"],
            "disposition": "blocked",
            "symbol": rule["publishes"],
            "code": "SOURCE_SET_UNCLOSED",
            "missing": [family_id],
            "pins": [],
        }],
        current_finding_ids=frozenset(),
    )

    section = model["sections"][0]
    assert section["resolved"]["reasons"] == [{"sentence": QUESTION}]
    assert "questionRefs" not in section["resolved"]
    assert model["questionGroups"] == []


def test_duplicate_selection_sentences_do_not_receive_closure_group_links() -> None:
    selected_reasons = [
        {"sentence": QUESTION, "factId": "demo.answer.first", "statementLabel": {"statement": "First demo statement"}},
        {"sentence": QUESTION, "factId": "demo.answer.second", "statementLabel": {"statement": "Second demo statement"}},
    ]
    merged, closure_indices = _reasons_beside(selected_reasons, [{"sentence": QUESTION}])
    references = [{
        "groupId": "question-demo",
        "question": QUESTION,
        "reasonIndices": closure_indices[QUESTION],
        "scope": {"kind": "fact", "id": "demo.answer.first", "status": "unanswered"},
    }]

    assert merged == selected_reasons
    assert closure_indices[QUESTION] == []
    assert _finalize_question_references(references, merged) == []


@pytest.fixture(scope="module")
def v99_saved_page() -> dict[str, Any]:
    """Capture a synthetic late-sale return through the current coordinator."""
    world = cast(Any, sales_v79.world).__wrapped__()
    track0 = world.track0
    probe = world.probe
    acts = build_v80_world().cfp.with_q2(world.cases["late_member_unclosed"], "no")
    acts = _prepare_v89_covered_sale_companions(acts)
    acts = state_taxpayer_facts(acts, core="v88")

    package_name = "package.core-calculations.v99.json"
    registry_name = "published-packages.v98.json"
    release_name = "demo.release.sli-worksheet-integration.2025.v98.json"
    package_path = probe.CONTENT / package_name
    release_path = probe.RELEASE_DIR / release_name
    registry_path = probe.CONTENT / registry_name
    assert package_path.is_file() and release_path.is_file() and registry_path.is_file()
    surface = PublicationSurface(probe.RELEASE_DIR, registry_path, probe.CONTENT)
    run_id = "demo.track2.question-groups-v99"
    finished = track0._handover(
        track0._finish(
            copy.deepcopy(acts),
            package_path=package_path,
            package_version="v99",
            release_path=release_path,
            release_version="v98",
            note=run_id,
        ),
        surface=surface,
        reconfirm=True,
    )

    with tempfile.TemporaryDirectory(prefix="question-groups-v3-") as tmp:
        capability = WorkspaceCapability(Path(tmp) / "L")
        outcome = live_coordinate_run(
            capability,
            repo_root=ROOT,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=track0.ccr.USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        assert outcome.refusal is None, outcome.refusal
        assert outcome.presentation_path is not None
        assert outcome.output_path is not None
        model = cast(dict[str, Any], json.loads(outcome.presentation_path.read_text("utf-8")))
        report = cast(dict[str, Any], json.loads(outcome.output_path.read_text("utf-8")))
        page = _render_page(ROOT, capability, outcome.presentation_path)
    validate_presentation_model(model)
    return {"model": model, "report": report, "page": page}


def _render_variant(model: dict[str, Any], base: Path, name: str) -> bytes:
    workspace = base / name
    workspace.mkdir(parents=True)
    capability = WorkspaceCapability(workspace)
    path = workspace / "presentation.json"
    path.write_text(json.dumps(model), encoding="utf-8")
    return _render_page(ROOT, capability, path)


def _visible_dom(page: bytes, *, body_script: str, base: Path, name: str) -> dict[str, Any]:
    if BROWSER is None:
        pytest.skip("headless Chrome is unavailable")
    path = base / f"{name}.html"
    path.write_bytes(page.replace(
        b"</body>",
        f"<script>{body_script}</script></body>".encode("utf-8"),
        1,
    ))
    command = [
        str(BROWSER), "--headless", "--disable-gpu", "--no-sandbox",
        f"--user-data-dir={base / ('profile-' + name)}",
        "--virtual-time-budget=2000", "--dump-dom", path.as_uri(),
    ]
    with browser_startup_slot():
        result = subprocess.run(command, capture_output=True, text=True, timeout=60, check=True)
    match = re.search(r'<pre id="track2-visible-check">(.*?)</pre>', result.stdout, re.S)
    assert match is not None, "Chrome did not return the requested visible page state"
    return cast(dict[str, Any], json.loads(html.unescape(match.group(1))))


@pytest.mark.live
def test_saved_v99_page_groups_the_shared_answer_and_keeps_other_reasons(
    v99_saved_page: dict[str, Any], tmp_path: Path,
) -> None:
    model = v99_saved_page["model"]
    assert model["schema"] == "presentation-model.v3"
    groups = model["questionGroups"]
    assert len(groups) == 1
    group = groups[0]
    assert group["question"] == QUESTION
    assert {producer["schema"] for producer in group["producers"]} == {
        "input-question.v1", "source-closure-mapping.v4",
    }
    assert group["answerTarget"]["factId"] == (
        "tax.us.2025.f1099b.noncovered-sold.source-closure|tax-year=2025"
    )

    line9 = next(section for section in model["sections"] if section["field"]["id"] == LINE9_FIELD)
    resolved = line9["resolved"]
    assert resolved["reasons"] == [
        {"sentence": QUESTION},
        {"sentence": LINE9_EXPLANATION},
    ]
    [line9_ref] = resolved["questionRefs"]
    assert line9_ref["groupId"] == group["id"]
    assert line9_ref["reasonIndices"] == [0]
    assert {scope["status"] for scope in line9_ref["scopes"]} == {"stale"}

    amount_rows = [
        row for row in v99_saved_page["report"]["dispositions"]
        if row.get("artifact_id") == "tax.us.2025.rule.f1099b.noncovered-lt-txn.amounts-check"
    ]
    assert len(amount_rows) == 1
    assert amount_rows[0]["disposition"] == "blocked"
    assert amount_rows[0]["code"] == "DEPENDENCY_INVALID"

    browser_data = _visible_dom(
        v99_saved_page["page"],
        body_script=(
            "const cards=[...document.querySelectorAll('#question-groups-root .question-group')];"
            f"const line=document.getElementById({json.dumps(line9['id'])});"
            "const data={cards:cards.map(x=>({id:x.id,question:x.querySelector('h3').innerText,text:x.innerText})),"
            "line9:line.innerText,links:[...line.querySelectorAll('a[href^=\"#question-group-\"]')].map(x=>x.getAttribute('href'))};"
            "const out=document.createElement('pre');out.id='track2-visible-check';out.textContent=JSON.stringify(data);"
            "document.body.appendChild(out);"
        ),
        base=tmp_path,
        name="v99-current",
    )
    assert len(browser_data["cards"]) == 1
    assert browser_data["cards"][0]["question"] == QUESTION
    assert "reconfirmation" in browser_data["cards"][0]["text"]
    assert len(browser_data["links"]) == 1
    assert QUESTION not in browser_data["line9"]
    assert LINE9_EXPLANATION in browser_data["line9"]


@pytest.mark.live
@pytest.mark.parametrize("label", [
    {"memberLabel": "Demo Sam", "memberOrdinal": 2},
    {"statementLabel": {"statement": "Demo statement", "taxYear": "2025"},
     "statementPayerLabel": "Demo Payer"},
])
def test_saved_fact_question_cannot_link_to_equal_text_display_reason(
    v99_saved_page: dict[str, Any], label: dict[str, Any],
) -> None:
    model = copy.deepcopy(v99_saved_page["model"])
    resolved = next(section["resolved"] for section in model["sections"] if section["resolved"].get("questionRefs"))
    reference = resolved["questionRefs"][0]
    original_index = reference["reasonIndices"][0]
    display_index = len(resolved["reasons"])
    resolved["reasons"].append({
        "sentence": resolved["reasons"][original_index]["sentence"],
        **label,
    })
    validate_presentation_model(model)
    reference["reasonIndices"] = [display_index]
    with pytest.raises(PresentationModelError, match="reasonIndices"):
        validate_presentation_model(model)


@pytest.mark.live
def test_grouped_line21_reason_keeps_one_anchor_for_multiple_group_links(
    v99_saved_page: dict[str, Any], tmp_path: Path,
) -> None:
    model = copy.deepcopy(v99_saved_page["model"])
    source_group = model["questionGroups"][0]
    target_type = "demo.answer-target.line21-statement"
    identity_keys = [
        {"name": "statement", "value": "demo.statement.line21"},
        {"name": "tax-year", "value": "2025"},
    ]
    second_fact_id = fact_id_for(
        target_type,
        (("statement", "demo.statement.line21"), ("tax-year", "2025")),
    )
    second_group = {
        "id": _question_group_id(target_type, "v1", identity_keys),
        "question": source_group["question"],
        "answerTarget": {
            "factTypeId": target_type,
            "factTypeVersion": "v1",
            "factId": second_fact_id,
            "identityKeys": identity_keys,
            "statementLabel": {"statement": "Demo line 21 statement", "taxYear": "2025"},
        },
        "producers": [{
            "schema": "input-question.v1",
            "id": "demo.input-question.line21-statement",
            "version": "v1",
        }],
    }
    model["questionGroups"].append(second_group)
    line21 = next(section for section in model["sections"] if section["id"] == "line-sch1-21")
    line21["resolved"] = {
        "disposition": "blocked",
        "activeCodes": ["DEPENDENCY_ABSENT"],
        "act": None,
        "reasons": [{"sentence": source_group["question"]}],
        "questionRefs": [
            {
                "groupId": source_group["id"],
                "reasonIndices": [0],
                "scopes": [{"kind": "fact", "id": source_group["answerTarget"]["factId"], "status": "stale"}],
            },
            {
                "groupId": second_group["id"],
                "reasonIndices": [0],
                "scopes": [{"kind": "fact", "id": second_fact_id, "status": "unanswered"}],
            },
        ],
    }
    line21_symbol = line21["field"]["binds_symbol"]
    model["sectionRoots"][line21["id"]] = {"kind": "disposition", "root": line21_symbol}
    model["dispositionNodes"][line21_symbol] = {
        "symbol": line21_symbol,
        "records": [{"disposition": "blocked", "artifact_id": "demo.rule.line21"}],
        "children": [],
    }
    model["line21Explanation"] = {
        "schema": "line21-explanation.v1",
        "runId": model["runId"],
        "workspaceRevision": 1,
        "rows": [{
            "statementLabel": {"statement": "Demo line 21 statement", "taxYear": "2025"},
            "loans": ["demo loan"],
            "status": {"kind": "named-by-reason", "reasonIndices": [0]},
        }],
    }
    validate_presentation_model(model)
    page = _render_variant(model, tmp_path, "line21-group-anchors")
    visible = _visible_dom(
        page,
        body_script=(
            "const line=document.getElementById('line-sch1-21');"
            "const target=line.querySelector('#line21-reason-0');"
            "const data={anchorCount:line.querySelectorAll('#line21-reason-0').length,"
            "line21Links:[...line.querySelectorAll('.line21-explanation a[href=\"#line21-reason-0\"]')].length,"
            "groupLinks:target ? target.querySelectorAll('a[href^=\"#question-group-\"]').length : 0,"
            "linkTarget:line.querySelector('.line21-explanation a[href=\"#line21-reason-0\"]')?.getAttribute('href')};"
            "const out=document.createElement('pre');out.id='track2-visible-check';out.textContent=JSON.stringify(data);"
            "document.body.appendChild(out);"
        ),
        base=tmp_path,
        name="line21-group-anchors",
    )
    assert visible == {
        "anchorCount": 1,
        "line21Links": 1,
        "groupLinks": 2,
        "linkTarget": "#line21-reason-0",
    }


@pytest.mark.live
def test_equal_text_statement_reasons_remain_visible_without_group_links(
    v99_saved_page: dict[str, Any], tmp_path: Path,
) -> None:
    model = copy.deepcopy(v99_saved_page["model"])
    model["questionGroups"] = []
    line9 = next(section for section in model["sections"] if section["field"]["id"] == LINE9_FIELD)
    for section in model["sections"]:
        section["resolved"].pop("questionRefs", None)
    line9["resolved"]["reasons"] = [
        {
            "sentence": QUESTION,
            "factId": "demo.answer.first",
            "statementLabel": {"statement": "First demo statement"},
        },
        {
            "sentence": QUESTION,
            "statementLabel": {"statement": "Second demo statement", "taxYear": "2025"},
            "statementPayerLabel": "Demo  Payer & Sons",
        },
    ]
    validate_presentation_model(model)
    page = _render_variant(model, tmp_path, "equal-sentence-independent-reasons")
    visible = _visible_dom(
        page,
        body_script=(
            f"const line=document.getElementById({json.dumps(line9['id'])});"
            "const data={reasons:[...line.querySelectorAll('.blocked-reasons li')].map(x=>x.innerText),"
            "groupLinks:line.querySelectorAll('a[href^=\"#question-group-\"]').length,"
            "groupCards:document.querySelectorAll('#question-groups-root .question-group').length};"
            "const out=document.createElement('pre');out.id='track2-visible-check';out.textContent=JSON.stringify(data);"
            "document.body.appendChild(out);"
        ),
        base=tmp_path,
        name="equal-sentence-independent-reasons",
    )
    assert visible["reasons"] == [
        f"First demo statement: {QUESTION}",
        f"Second demo statement, Demo  Payer & Sons: {QUESTION}",
    ]
    assert visible["groupLinks"] == 0
    assert visible["groupCards"] == 0


@pytest.mark.live
def test_saved_reader_keeps_same_worded_distinct_targets_and_old_v2_pages(
    v99_saved_page: dict[str, Any], tmp_path: Path,
) -> None:
    model = copy.deepcopy(v99_saved_page["model"])
    target_type = "demo.answer-target.statement"
    producer = [{
        "schema": "input-question.v1",
        "id": "demo.input-question.independent",
        "version": "v1",
    }]
    groups = []
    for statement_id, label in (
        ("demo.statement.first", "Demo statement one"),
        ("demo.statement.second", "Demo statement two"),
    ):
        identity_keys = [
            {"name": "statement", "value": statement_id},
            {"name": "tax-year", "value": "2025"},
        ]
        target = {
            "factTypeId": target_type,
            "factTypeVersion": "v1",
            "factId": fact_id_for(
                target_type,
                (("statement", statement_id), ("tax-year", "2025")),
            ),
            "identityKeys": identity_keys,
            "statementLabel": {"statement": label, "taxYear": "2025"},
        }
        groups.append({
            "id": _question_group_id(target_type, "v1", identity_keys),
            "question": model["questionGroups"][0]["question"],
            "answerTarget": target,
            "producers": producer,
        })
    model["questionGroups"] = groups
    line9 = next(section for section in model["sections"] if section["field"]["id"] == LINE9_FIELD)
    line9["resolved"]["questionRefs"] = [
        {
            "groupId": group["id"],
            "reasonIndices": [0],
            "scopes": [{
                "kind": "fact",
                "id": group["answerTarget"]["factId"],
                "status": "unanswered",
            }],
        }
        for group in groups
    ]
    for section in model["sections"]:
        if section["id"] != line9["id"]:
            section["resolved"].pop("questionRefs", None)
    validate_presentation_model(model)

    line9 = next(section for section in model["sections"] if section["field"]["id"] == LINE9_FIELD)
    page = _render_variant(model, tmp_path, "same-worded-distinct")
    second_browser_data = _visible_dom(
        page,
        body_script=(
            "const cards=[...document.querySelectorAll('#question-groups-root .question-group')];"
            f"const line=document.getElementById({json.dumps(line9['id'])});"
            "const links=[...line.querySelectorAll('a[href^=\"#question-group-\"]')];"
            "const data={cards:cards.map(x=>({id:x.id,question:x.querySelector('h3').innerText,text:x.innerText})),"
            "links:links.map(x=>x.getAttribute('href'))};"
            "const out=document.createElement('pre');out.id='track2-visible-check';out.textContent=JSON.stringify(data);"
            "document.body.appendChild(out);"
        ),
        base=tmp_path,
        name="same-worded-distinct",
    )
    assert len(second_browser_data["cards"]) == 2
    assert [card["question"] for card in second_browser_data["cards"]] == [QUESTION, QUESTION]
    assert len({card["id"] for card in second_browser_data["cards"]}) == 2
    assert any("Demo statement one" in card["text"] for card in second_browser_data["cards"])
    assert any("Demo statement two" in card["text"] for card in second_browser_data["cards"])
    assert all("demo.statement." not in card["text"] for card in second_browser_data["cards"])
    assert len(set(second_browser_data["links"])) == 2

    legacy = cast(dict[str, Any], json.loads(OLD_V2.read_text(encoding="utf-8")))
    assert legacy["schema"] == "presentation-model.v2"
    validate_presentation_model(legacy)
    legacy_page = _render_variant(legacy, tmp_path, "old-v2")
    legacy_browser_data = _visible_dom(
        legacy_page,
        body_script=(
            "const data={modelSchema:MODEL.schema,cardCount:document.querySelectorAll('#question-groups-root .question-group').length};"
            "const out=document.createElement('pre');out.id='track2-visible-check';out.textContent=JSON.stringify(data);"
            "document.body.appendChild(out);"
        ),
        base=tmp_path,
        name="old-v2",
    )
    assert legacy_browser_data == {"modelSchema": "presentation-model.v2", "cardCount": 0}

    projected = project_presentation_v1(v99_saved_page["model"])
    assert projected["schema"] == "presentation-model.v1"
    assert "questionGroups" not in projected
    assert all("questionRefs" not in section["resolved"] for section in projected["sections"])
    projected_line9 = next(section for section in projected["sections"] if section["field"]["id"] == LINE9_FIELD)
    assert projected_line9["resolved"]["reasons"] == line9["resolved"]["reasons"]
    validate_presentation_model(projected)
