"""Core v75 names an unconfirmed family's existing closure question.

The runs go through ``live_coordinate_run``. v74 is compared to the P0 survey.
v75 is compared to that same survey where the charter says nothing changes,
and to the sentences the survey recorded where a line gains its question.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

import pytest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.tax.loader import (
    domain_package_companion_declarations,
    unconfirmed_family_names_closure_question,
)
from tests import evidence_loader
from tests.test_form_1099_k_income import _handover
from tests.test_form_1099_withholding import _close
from tests.test_refund_or_amount_owed_track1 import _finish

ROOT = Path(__file__).resolve().parents[1]
CORE = "tax.us.2025.package.core-calculations"
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
RELEASE_DIR = (
    ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
)
_PROBE_PATH = (
    ROOT / "docs/phases/engine-breadth/milestones/closure-question-coverage-evidence/probe.py"
)

# (package file, package version, registry file, release file, release version)
_CORES: dict[str, tuple[str, str, str, str, str]] = {
    "v74": (
        "package.core-calculations.v74.json",
        "v74",
        "published-packages.v72.json",
        "demo.release.sli-worksheet-integration.2025.v72.json",
        "v72",
    ),
    "v75": (
        "package.core-calculations.v75.json",
        "v75",
        "published-packages.v73.json",
        "demo.release.sli-worksheet-integration.2025.v73.json",
        "v73",
    ),
}

# The two families P0 left unnamed, each with and without a member.
_WASH = (
    ("f1099b.covered-w-st", "none"),
    ("f1099b.covered-w-st", "members"),
    ("f1099b.covered-w-lt", "none"),
    ("f1099b.covered-w-lt", "members"),
)

# A sample of the families P0 already showed naming their question on every line.
_SAMPLE = (
    ("f1099int.b1", "none"),
    ("f1099int.b1", "members"),
    ("w2", "none"),
    ("w2", "members"),
    ("f1099b.covered-w-st-basis", "none"),
    ("f1098", "none"),
    # No member: Form 1099-K already names its question, including on the selection lines.
    ("f1099k", "none"),
)

_SELECTION_LINES = ("sch1-10", "sch1-top")


def _probe() -> Any:
    return evidence_loader.load(_PROBE_PATH, "closure_question_coverage_probe")


probe = _probe()
SURVEY = json.loads(probe.OUTPUT.read_text(encoding="utf-8"))


def _load(path: Path) -> dict[str, Any]:
    body: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return body


def _survey_body(summary: dict[str, Any]) -> dict[str, Any]:
    """The survey record without the timing and the probe's setup note.

    ``run_case`` stores ``seconds`` and ``setup``. ``summarize`` does not.
    Both are about the probe run, not the blocked lines.
    """
    return {key: value for key, value in summary.items() if key not in {"seconds", "setup"}}


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return tuple(sorted((str(key), _freeze(item)) for key, item in value.items()))
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _reason_face(reasons: Any) -> tuple[Any, ...] | None:
    if not reasons:
        return None
    return tuple(
        tuple(sorted((str(key), _freeze(item)) for key, item in reason.items()))
        for reason in reasons
    )


def _face(model: dict[str, Any]) -> dict[str, Any]:
    """Line and attachment presentation, without finding ids or the adoption pin."""
    sections = []
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        resolved = section.get("resolved") or {}
        sections.append((
            str(field.get("line") or field.get("id")),
            str(field.get("binds_symbol") or ""),
            resolved.get("disposition"),
            _freeze(resolved.get("value")),
            _reason_face(resolved.get("reasons")),
            tuple(resolved.get("activeCodes") or ()),
        ))
    attachments = []
    for attachment in model.get("attachments") or []:
        resolved = attachment.get("resolved") or {}
        attachments.append((
            attachment.get("id"),
            resolved.get("disposition"),
            tuple(resolved.get("activeCodes") or ()),
        ))
    inputs = tuple(sorted(
        (row.get("factTypeId"), _freeze(row.get("value")))
        for row in model.get("unsupportedSourceFindings") or []
    ))
    return {"sections": sections, "attachments": attachments, "inputs": inputs}


def _published(outcome: Any) -> list[tuple[str, Any]]:
    rows = [
        (str(item.finding["symbol"]), _freeze(item.finding.get("value")))
        for item in outcome.publications or ()
    ]
    return sorted(rows, key=lambda pair: pair[0])


def _run(acts: list[dict[str, Any]], run_id: str, core: str, *, reconfirm: bool = True) -> dict[str, Any]:
    package_name, package_version, registry_name, release_name, release_version = _CORES[core]
    surface = PublicationSurface(RELEASE_DIR, CONTENT / registry_name, CONTENT)
    finished = _handover(
        _finish(
            acts,
            package_path=CONTENT / package_name,
            package_version=package_version,
            release_path=RELEASE_DIR / release_name,
            release_version=release_version,
            note=run_id,
        ),
        surface=surface,
        reconfirm=reconfirm,
    )
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=probe.ROOT,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": probe.YEAR},
            scope_user=probe.ccr.USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            raise AssertionError(f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
        assert outcome.output_path is not None and outcome.presentation_path is not None
        report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
        model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
        return {
            "dispositions": list(report.get("dispositions") or []),
            "model": model,
            "published": _published(outcome),
        }


def _unconfirmed(short: str, variant: str, core: str) -> tuple[dict[str, Any], dict[str, Any]]:
    family_id = probe.P + short
    acts, _note = probe.prepare(family_id, variant)
    _families, mappings, _fact_types, _extra = probe.load_index()
    question = str(mappings[family_id].get("closure_question") or "")
    payload = _run(acts, f"demo.t1.{short.replace('.', '-')}.{variant}.{core}", core)
    return payload, probe.summarize(family_id, question, payload)


def _reasons_for(model: dict[str, Any], line: str) -> list[dict[str, Any]]:
    found: list[list[dict[str, Any]]] = []
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        if str(field.get("line") or field.get("id")) != line:
            continue
        reasons = (section.get("resolved") or {}).get("reasons") or []
        found.append(list(reasons))
    assert len(found) == 1, line
    return found[0]


def _blocked_reasons(model: dict[str, Any]) -> dict[str, Any]:
    found: dict[str, Any] = {}
    for section in model.get("sections") or []:
        resolved = section.get("resolved") or {}
        if resolved.get("disposition") != "blocked":
            continue
        field = section.get("field") or {}
        line = str(field.get("line") or field.get("id"))
        assert line not in found, line
        found[line] = resolved.get("reasons")
    return found


def test_successor_records_only_the_v75_package() -> None:
    """v75 keeps v74's members and companion declaration. The switch is separate."""
    old = _load(CONTENT / "package.core-calculations.v74.json")
    new = _load(CONTENT / "package.core-calculations.v75.json")
    assert {key: value for key, value in old.items() if key not in {"version", "package_checksum"}} == {
        key: value for key, value in new.items() if key not in {"version", "package_checksum"}
    }
    assert new["version"] == "v75"
    assert new["schema"] == "artifact-package.v39"

    reg_old = _load(CONTENT / "published-packages.v72.json")
    reg_new = _load(CONTENT / "published-packages.v73.json")
    assert reg_old["citizens"] == reg_new["citizens"]

    def pins(doc: dict[str, Any]) -> dict[tuple[str, str], str]:
        return {(row["id"], row["version"]): row["checksum"] for row in doc["packages"]}

    old_pins, new_pins = pins(reg_old), pins(reg_new)
    assert set(new_pins) - set(old_pins) == {(CORE, "v75")}
    assert set(old_pins) - set(new_pins) == set()
    assert new_pins[(CORE, "v75")] == new["package_checksum"]
    order = [(row["id"], row["version"]) for row in reg_new["packages"]]
    assert order.index((CORE, "v75")) == order.index((CORE, "v74")) + 1
    assert order.index((CORE, "v8")) == order.index((CORE, "v75")) + 1

    release_path = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v73.json"
    release = _load(release_path)
    registry_path = CONTENT / "published-packages.v73.json"
    assert release["id"] == "demo.release.sli-worksheet-integration.2025"
    assert release["version"] == "v73"
    assert release["schema"] == "release-registry.v1"
    assert release["package_registry_sha256"] == hashlib.sha256(registry_path.read_bytes()).hexdigest()

    declarations = domain_package_companion_declarations()
    assert declarations[(CORE, "v75")] == declarations[(CORE, "v74")]
    assert unconfirmed_family_names_closure_question(CORE, "v75") is True
    assert unconfirmed_family_names_closure_question(CORE, "v76") is True
    assert unconfirmed_family_names_closure_question(CORE, "v74") is False
    assert unconfirmed_family_names_closure_question(CORE, "v1") is False
    assert unconfirmed_family_names_closure_question("tax.us.2025.package.interest-slice", "v75") is False


@pytest.mark.parametrize(("short", "variant"), _WASH)
def test_v74_wash_matches_the_survey(short: str, variant: str) -> None:
    _payload, summary = _unconfirmed(short, variant, "v74")
    assert _survey_body(summary) == _survey_body(SURVEY["results"][short][variant])


@pytest.mark.parametrize(("short", "variant"), _WASH)
def test_v75_wash_names_its_question(short: str, variant: str) -> None:
    family_id = probe.P + short
    _payload, summary = _unconfirmed(short, variant, "v75")
    survey = SURVEY["results"][short][variant]
    assert survey["blocked_line_count"] == 32
    assert summary["blocked_line_count"] == 32
    assert {line["line"] for line in summary["blocked_lines"]} == {
        line["line"] for line in survey["blocked_lines"]
    }
    silent = [line["line"] for line in summary["blocked_lines"] if not line["names_question"]]
    assert silent == []
    assert summary["unnamed"] == []
    assert len(summary["names_on"]) == 32
    synthesized = [
        row for row in summary["direct_blocks"]
        if str(row["artifact_id"]).endswith(".member-validation.synthesized")
    ]
    assert synthesized == [{
        "artifact_id": f"{short}.member-validation.synthesized",
        "code": "SOURCE_SET_UNCLOSED",
        "missing": [short],
    }]
    _families, mappings, _fact_types, _extra = probe.load_index()
    question = str(mappings[family_id]["closure_question"])
    assert question
    assert all(line["names_question"] for line in summary["blocked_lines"])


@pytest.mark.parametrize(("short", "variant"), _SAMPLE)
def test_sample_family_is_unchanged_on_v75(short: str, variant: str) -> None:
    surveyed = SURVEY["results"][short][variant]
    before, summary_v74 = _unconfirmed(short, variant, "v74")
    after, summary_v75 = _unconfirmed(short, variant, "v75")
    assert _survey_body(summary_v74) == _survey_body(surveyed)
    assert _survey_body(summary_v75) == _survey_body(surveyed)
    assert after["published"] == before["published"]
    assert _face(after["model"]) == _face(before["model"])


def test_f1099k_with_one_member_names_both_sentences() -> None:
    before, summary_v74 = _unconfirmed("f1099k", "members", "v74")
    after, summary_v75 = _unconfirmed("f1099k", "members", "v75")
    surveyed = SURVEY["results"]["f1099k"]["members"]
    assert _survey_body(summary_v74) == _survey_body(surveyed)
    _families, mappings, _fact_types, _extra = probe.load_index()
    question = str(mappings[probe.P + "f1099k"]["closure_question"])
    assert question

    v74_lines = _blocked_reasons(before["model"])
    v75_lines = _blocked_reasons(after["model"])
    assert set(v74_lines) == set(v75_lines)
    for line in _SELECTION_LINES:
        prior = _reasons_for(before["model"], line)
        gained = _reasons_for(after["model"], line)
        prior_sentences = [str(reason["sentence"]) for reason in prior]
        recorded = next(row for row in surveyed["blocked_lines"] if row["line"] == line)
        assert prior_sentences == recorded["other_reasons"]
        assert question not in prior_sentences
        assert [str(reason["sentence"]) for reason in gained] == sorted({*prior_sentences, question})
        for reason in prior:
            assert reason in gained
        for reason in gained:
            if reason["sentence"] == question:
                assert set(reason) == {"sentence"}
    for line, reasons in v74_lines.items():
        if line in _SELECTION_LINES:
            continue
        assert v75_lines[line] == reasons
    assert summary_v75["blocked_line_count"] == summary_v74["blocked_line_count"] == 30
    assert after["published"] == before["published"]


def test_confirmed_base_return_matches_v74() -> None:
    acts = probe.ccr._renumbered(probe.w2g._w2g_return([]))
    before = _run(acts, "demo.t1.base.v74", "v74")
    after = _run(acts, "demo.t1.base.v75", "v75")
    assert _survey_body(probe.summarize("", "", before)) == _survey_body(SURVEY["base"])
    assert _survey_body(probe.summarize("", "", after)) == _survey_body(SURVEY["base"])
    assert before["published"]
    assert after["published"] == before["published"]
    assert _face(after["model"]) == _face(before["model"])
    assert SURVEY["base"]["blocked_line_count"] == 0


_WASH_ST = probe.P + "f1099b.covered-w-st"
_COVERED_ST = probe.P + "f1099b.covered-st"
_WASH_VALIDATION = _WASH_ST + ".member-validation"
_WASH_SYNTHESIZED = _WASH_VALIDATION + ".synthesized"
_WASH_CONSUMERS = (
    "tax.us.2025.rule.attachment.f8949",
    "tax.us.2025.rule.attachment.schedule-d",
    "tax.us.2025.rule.f1099b-covered-w-st-adjustment-subtotal",
    "tax.us.2025.rule.f1099b-covered-w-st-basis-subtotal",
    "tax.us.2025.rule.f1099b-covered-w-st-proceeds-subtotal",
    "tax.us.2025.rule.schedule-d-line1b",
)
_IDENTITY_BLOCK = "tax.us.2025.block.covered-w.identity-key-collision"


def _member_finding(acts: list[dict[str, Any]], family_id: str) -> dict[str, Any]:
    found: list[dict[str, Any]] = []
    for act in acts:
        if act.get("kind") != "member-transition":
            continue
        payload = act.get("payload")
        if not isinstance(payload, dict) or payload.get("family", {}).get("id") != family_id:
            continue
        member = payload.get("member")
        finding = member.get("finding") if isinstance(member, dict) else None
        if isinstance(finding, dict):
            found.append(finding)
    assert len(found) == 1, family_id
    return found[0]


def _bound_entities(fact_id: str) -> dict[str, str]:
    _fact_type, _bar, suffix = fact_id.partition("|")
    entities: dict[str, str] = {}
    for part in suffix.split(","):
        name, value = part.split("=", 1)
        if name != "tax-year":
            entities[name] = value
    return entities


def _reclose(acts: list[dict[str, Any]], family_id: str, mappings: dict[str, Any], finding_id: str) -> None:
    closure = str(mappings[family_id]["closure_fact_type"]["id"])
    acts[:] = probe.strip_closure(acts, closure)
    _close(acts, closure, probe.latest_horizon(acts, family_id), finding_id)


def _closed_wash(*, drop_amount: bool, collide: bool) -> tuple[list[dict[str, Any]], str]:
    """One closed covered short-term wash-sale member, optionally invalid or colliding."""
    acts, _note = probe.prepare(_WASH_ST, "members")
    families, mappings, fact_types, extra = probe.load_index()
    question = str(mappings[_WASH_ST]["closure_question"])
    if drop_amount:
        value = _member_finding(acts, _WASH_ST)["value"]
        assert value["box_1g_wash_sale_adjustment"] == "yes"
        del value["box_1g_wash_sale_disallowed_amount"]
    if collide:
        entities = _bound_entities(str(_member_finding(acts, _WASH_ST)["fact_id"]))
        mapped = str(mappings[_COVERED_ST]["family"]["version"])
        probe.align_family_version(acts, _COVERED_ST, mapped)
        saved = probe.REUSE_ENTITIES.get(_COVERED_ST)
        probe.REUSE_ENTITIES[_COVERED_ST] = entities
        try:
            probe.add_member(acts, families[_COVERED_ST], mappings[_COVERED_ST], fact_types, extra["bundles"])
        finally:
            if saved is None:
                probe.REUSE_ENTITIES.pop(_COVERED_ST, None)
            else:
                probe.REUSE_ENTITIES[_COVERED_ST] = saved
        covered = _bound_entities(str(_member_finding(acts, _COVERED_ST)["fact_id"]))
        assert covered == entities
        _reclose(acts, _COVERED_ST, mappings, "demo.t1.covered-st.reclose")
    _reclose(acts, _WASH_ST, mappings, "demo.t1.wash-st.reclose")
    return acts, question


def _blocked(payload: dict[str, Any], artifact_id: str) -> dict[str, Any]:
    rows = [
        row for row in payload["dispositions"]
        if row.get("disposition") == "blocked" and row.get("artifact_id") == artifact_id
    ]
    assert len(rows) == 1, (artifact_id, rows)
    return cast(dict[str, Any], rows[0])


def _assert_validation_failure(payload: dict[str, Any], question: str, missing: set[str]) -> None:
    synthesized = _blocked(payload, _WASH_SYNTHESIZED)
    assert synthesized["code"] == "DEPENDENCY_INVALID"
    assert set(synthesized["missing"]) == missing
    symbol = _WASH_VALIDATION
    for artifact_id in _WASH_CONSUMERS:
        row = _blocked(payload, artifact_id)
        assert row["code"] == "DEPENDENCY_ABSENT"
        assert symbol in row["missing"]
    for section in payload["model"].get("sections") or []:
        resolved = section.get("resolved") or {}
        if resolved.get("disposition") != "blocked":
            continue
        sentences = [str(reason.get("sentence")) for reason in resolved.get("reasons") or []]
        assert question not in sentences


def _both_cores(acts: list[dict[str, Any]], stem: str, question: str, missing: set[str]) -> None:
    before = _run(acts, f"demo.t1.{stem}.v74", "v74")
    after = _run(acts, f"demo.t1.{stem}.v75", "v75")
    _assert_validation_failure(before, question, missing)
    _assert_validation_failure(after, question, missing)
    assert before["published"]
    assert after["published"] == before["published"]
    assert _face(after["model"]) == _face(before["model"])


def test_closed_wash_sale_without_the_disallowed_amount_stays_invalid() -> None:
    """A closed member with the flag set and the amount absent fails validation on both cores."""
    acts, question = _closed_wash(drop_amount=True, collide=False)
    _both_cores(acts, "wash-flag-without-amount", question, {"BOX_1G_FLAG_WITHOUT_AMOUNT"})


def test_closed_wash_sale_identity_collision_stays_invalid() -> None:
    """A closed wash-sale member that shares its identity with a closed covered short-term member."""
    acts, question = _closed_wash(drop_amount=False, collide=True)
    _both_cores(
        acts,
        "wash-identity-collision",
        question,
        {"IDENTITY_EXCLUSIVITY_COLLISION", f"identity_exclusivity:{_IDENTITY_BLOCK}"},
    )


def test_admitted_wash_sale_matches_v74() -> None:
    """A constrained family that is admitted still validates as it does on v74."""
    family_id = probe.P + "f1099b.covered-w-st"
    acts, _note = probe.prepare(family_id, "members")
    _families, mappings, _fact_types, _extra = probe.load_index()
    closure = str(mappings[family_id]["closure_fact_type"]["id"])
    _close(acts, closure, probe.latest_horizon(acts, family_id), "demo.t1.reclose")
    before = _run(acts, "demo.t1.wash-admitted.v74", "v74")
    after = _run(acts, "demo.t1.wash-admitted.v75", "v75")
    assert before["published"]
    assert after["published"] == before["published"]
    assert _face(after["model"]) == _face(before["model"])
    summary = probe.summarize(family_id, str(mappings[family_id]["closure_question"]), after)
    assert all(
        row["code"] != "SOURCE_SET_UNCLOSED"
        for row in summary["direct_blocks"]
        if str(row["artifact_id"]).endswith(".member-validation.synthesized")
    )
