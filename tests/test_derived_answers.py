"""Core v74: two scope answers the record already proves (derived-answers Track 1).

Form 1098 and the Form 1116 cap are derived. The box 8 answer and the other-dependent
answer were held: an answered return with that family left open publishes on v73 and
blocks on the successor. Every case goes through ``live_coordinate_run``. Synthetic
``demo.*`` data only.
"""

from __future__ import annotations

import copy
import hashlib
import json
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.tax.loader import domain_package_companion_declarations
from tests import test_input_questions as miq
from tests import test_other_dependents_credit_track1 as odc
from tests import test_w2g_gambling as w2g
from tests.helpers import current_core_returns as ccr
from tests.test_form_1099_k_income import _handover
from tests.test_form_1099_withholding import YEAR, _social_security_withholding, _unemployment_withholding
from tests.test_refund_or_amount_owed_track1 import _act, _attested, _finish
from tests.test_refund_or_amount_owed_track1 import _load as _release_load

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ccr.CONTENT
RELEASE_DIR = ccr.RELEASE_DIR
P = ccr.P
CORE = P + "package.core-calculations"
CORES = {
    "v73": ("package.core-calculations.v73.json", "v73",
            "demo.release.sli-worksheet-integration.2025.v71.json", "v71", "published-packages.v71.json"),
    "v74": ("package.core-calculations.v74.json", "v74",
            "demo.release.sli-worksheet-integration.2025.v72.json", "v72", "published-packages.v72.json"),
}
SCOPE = P + "f1098-scope.no-mortgage-statement"
INT = P + "line2a-scope.no-f1099int-tax-exempt"
OD = P + "ctc.no-other-dependent"
F1116 = P + "direct-ftc-scope.no-form-1116-required"
OID = P + "line2a-scope.no-f1099oid-tax-exempt"
CG_DIST = P + "capital-gain-distributions"
EXC = (
    P + "exception1.only-box2a-capital-gains",
    P + "exception1.no-capital-losses",
    P + "exception1.no-qof-deferral",
    P + "exception1.no-boxes-2b-2c-2d",
)
M1 = "Did you receive a Form 1098"
FTC = "any other reason you must file Form 1116"
L2A = "tax-exempt interest on a Form 1099-INT"
CTC = "besides the children you counted"
OID_Q = "Form 1099-OID"
EXC_Q = "box 2b, 2c or 2d"
LINE12E = P + "deductions.line-12e"
LINE8A = P + "schedule-a.line8a"
CREDIT = P + "schedule3.line1-direct-ftc"
LINE2A = P + "tax-exempt-interest.line2a-total"
LINE6 = P + "ctc.sch8812.line-6"


class Run:
    def __init__(self, pubs: dict[str, dict[str, Any]], dispositions: list[dict[str, Any]], model: dict[str, Any]) -> None:
        self.pubs, self.dispositions, self.model = pubs, dispositions, model


def _set(acts: list[dict[str, object]], fact: str, value: object) -> list[dict[str, object]]:
    out = copy.deepcopy(acts)
    w2g._set_answer(out, fact, value)
    return out


def _return(joint: bool = False) -> list[dict[str, object]]:
    return w2g._w2g_return([], joint=joint)


def _odc(answer: str | None) -> list[dict[str, object]]:
    answers: dict[str, str] = {}
    if answer is not None:
        answers[OD] = answer
    child = "demo-child-odc"
    acts = odc.build(wages=50000.0, children={child: odc.odc_child()}, return_answers=answers)
    acts.append(_act(len(acts), "bundle-adoption", {"bundle": _release_load("dtb-questions.bundle.json")}))
    for question, value in ccr._TIE_BREAKER_ANSWERS.items():
        fid = f"{P}dtb.child.{question}|child={child},tax-year=2025"
        acts.append(_act(len(acts), "assertion", {"finding": _attested(f"demo.t1.dtb.{question}.{child}", fid, value)}))
    if answer is None:
        acts = miq.drop(acts, OD)
    acts = odc._complete(acts)
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    w2g._w2g(acts, [])
    return acts


def _acts(kind: str) -> list[dict[str, object]]:
    if kind == "base":
        return _return()
    if kind == "m1-silent":
        return miq.drop(_return(), SCOPE)
    if kind == "m1-proved":
        return miq.drop(ccr.add_mortgage_itemizer(_return(), 40000.0), SCOPE)
    if kind == "m1-open":
        return miq.drop(ccr.add_mortgage_itemizer(_return(), 40000.0), SCOPE, P + "f1098.source-closure")
    if kind == "m1-agreed":
        return ccr.add_mortgage_itemizer(_return(), 40000.0)
    if kind == "m1-contradict":
        return _set(ccr.add_mortgage_itemizer(_return(), 40000.0), SCOPE, True)
    if kind == "m1-joint":
        return miq.drop(ccr.add_mortgage_itemizer(_return(joint=True), 40000.0), SCOPE)
    if kind == "ftc-30":
        return miq.drop(ccr.add_foreign_tax_1099div(_return(), [30.0]), F1116)
    if kind == "ftc-400":
        return miq.drop(ccr.add_foreign_tax_1099div(_return(), [400.0]), F1116)
    if kind == "ftc-30-yes":
        return ccr.add_foreign_tax_1099div(_return(), [30.0])
    if kind == "ftc-400-yes":
        return ccr.add_foreign_tax_1099div(_return(), [400.0])
    if kind == "ftc-joint-500":
        return miq.drop(ccr.add_foreign_tax_1099div(_return(joint=True), [500.0]), F1116)
    if kind == "ftc-joint-700":
        return miq.drop(ccr.add_foreign_tax_1099div(_return(joint=True), [700.0]), F1116)
    if kind == "ftc-joint-700-yes":
        return ccr.add_foreign_tax_1099div(_return(joint=True), [700.0])
    if kind == "l2a-proved":
        return miq.drop(ccr.add_tax_exempt_interest_1099int(_return(), [125.0]), INT)
    if kind == "ctc-proved":
        return _odc(None)
    if kind == "ctc-contradict":
        return _odc("yes")
    if kind == "oid-silent":
        return miq.drop(_return(), OID)
    if kind == "oid-box1":
        return miq.drop(ccr._record_members(_return(), P + "f1099oid.b1", [75.0], tag="oid1"), OID)
    if kind == "exc-silent":
        return miq.drop(_return(), *EXC)
    if kind == "exc-box2a":
        return miq.drop(ccr._record_members(_set(_return(), CG_DIST, "yes"), P + "f1099div.2a", [40.0], tag="b2a"), *EXC)
    raise KeyError(kind)


_CACHE: dict[tuple[str, str], Run] = {}


def go(kind: str, core: str) -> Run:
    key = (kind, core)
    if key not in _CACHE:
        package, version, release, rel_version, registry = CORES[core]
        surface = PublicationSurface(RELEASE_DIR, CONTENT / registry, CONTENT)
        finished = _handover(
            _finish(copy.deepcopy(_acts(kind)), package_path=CONTENT / package, package_version=version,
                    release_path=RELEASE_DIR / release, release_version=rel_version,
                    note=f"demo.t1.{kind}.{core}"),
            surface=surface, reconfirm=True)
        with TemporaryDirectory() as tmp:
            outcome = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"), repo_root=ROOT, authoritative_acts=finished,
                workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": YEAR},
                scope_user=ccr.USER, request={"schema": "run-request.v1"}, run_id=f"demo.t1.{kind}.{core}",
                governance_pins=[], surface=surface, output_name="out.json")
            assert outcome.refusal is None, outcome.refusal
            assert outcome.output_path is not None and outcome.presentation_path is not None
            pubs = {str(item.finding["symbol"]): item.finding for item in outcome.publications or ()}
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
        _CACHE[key] = Run(pubs, list(report.get("dispositions", [])), model)
    return _CACHE[key]


def _asks(run: Run, fragment: str) -> list[str]:
    blocked = miq.blocked(run.model)
    return sorted(
        line for line, reasons in blocked.items()
        if reasons and any(fragment in sentence for sentence in reasons)
    )


def _money(run: Run) -> dict[str, object]:
    out: dict[str, object] = {}
    for symbol, finding in run.pubs.items():
        raw = finding.get("value")
        if isinstance(raw, bool):
            out[symbol] = raw
        elif isinstance(raw, (int, float, str)):
            try:
                out[symbol] = Decimal(str(raw))
            except Exception:
                out[symbol] = raw
        else:
            out[symbol] = json.dumps(raw, sort_keys=True)
    return out


def _dec(run: Run, symbol: str) -> Decimal | None:
    finding = run.pubs.get(symbol)
    if finding is None:
        return None
    return Decimal(str(finding["value"]))


def _rows(run: Run, token: str) -> list[dict[str, Any]]:
    return [row for row in run.dispositions if str(row.get("artifact_id", "")).endswith("rule." + token)]


def _load(name: str) -> dict[str, Any]:
    doc: dict[str, Any] = json.loads((CONTENT / name).read_text(encoding="utf-8"))
    return doc


def test_v74_adds_the_two_rules_and_leaves_every_earlier_checksum() -> None:
    old, new = _load("published-packages.v71.json"), _load("published-packages.v72.json")

    def index(doc: dict[str, Any], key: str) -> dict[tuple[str, str], str]:
        return {(row["id"], row["version"]): row["checksum"] for row in doc[key]}

    old_c, new_c = index(old, "citizens"), index(new, "citizens")
    old_p, new_p = index(old, "packages"), index(new, "packages")
    assert old_c.items() <= new_c.items()
    assert old_p.items() <= new_p.items()
    assert set(new_c) - set(old_c) == {(P + "rule.form1040-line12e", "v4"), (P + "rule.schedule3-line1-direct-ftc", "v4")}
    assert set(new_p) - set(old_p) == {(CORE, "v74")}
    release = json.loads((RELEASE_DIR / CORES["v74"][2]).read_text(encoding="utf-8"))
    assert release["version"] == "v72"
    assert release["package_registry_sha256"] == hashlib.sha256((CONTENT / "published-packages.v72.json").read_bytes()).hexdigest()


def test_v74_replaces_only_the_two_members_and_shares_the_companion_declaration() -> None:
    old, new = _load("package.core-calculations.v73.json"), _load("package.core-calculations.v74.json")
    assert old["input_bindings"] == new["input_bindings"]
    assert old["schema"] == new["schema"] == "artifact-package.v39"

    def pins(pkg: dict[str, Any]) -> set[tuple[str, str]]:
        return {(member["id"], member["version"]) for member in pkg["members"]}

    removed, added = pins(old) - pins(new), pins(new) - pins(old)
    assert removed == {(P + "rule.form1040-line12e", "v3"), (P + "rule.schedule3-line1-direct-ftc", "v3")}
    assert added == {(P + "rule.form1040-line12e", "v4"), (P + "rule.schedule3-line1-direct-ftc", "v4")}
    member = next(row for row in new["members"] if row["id"].endswith("schedule3-line1-direct-ftc"))
    assert member["schema"] == "rule-artifact.v3"
    line = next(row for row in new["members"] if row["id"].endswith("form1040-line12e"))
    assert line["schema"] == "rule-artifact.v4" and line["version"] == "v4"
    held = ("form1040-line2a", "v5"), ("odc-dependent-present", "v2"), ("ctc-sch8812-line-6", "v3"), (
        "odc-child-marked-conflict", "v2"), ("odc-relative-marked-conflict", "v2")
    assert not any(row["id"].endswith(name) and row["version"] == version for name, version in held for row in new["members"])
    assert domain_package_companion_declarations()[(CORE, "v74")] == domain_package_companion_declarations()[(CORE, "v73")]
    rule = _load("rule.form1040-line12e.v4.json")
    assert SCOPE not in rule["requires"]
    assert "f1098.box1-mortgage-interest" in json.dumps(rule["value"])
    ftc = _load("rule.schedule3-line1-direct-ftc.v4.json")
    sets = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("op") == "conditional_dependency_set":
                sets.append(F1116 in [item.get("name") for item in node.get("members", [])])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(ftc["when"])
    assert sets == [False]
    assert F1116 in json.dumps(ftc["when"])


def test_a_recorded_form_1098_publishes_without_the_question_at_the_agreed_amounts() -> None:
    proved, agreed = go("m1-proved", "v74"), go("m1-agreed", "v74")
    assert _asks(proved, M1) == []
    assert _dec(proved, LINE12E) == Decimal("40000")
    assert _dec(proved, LINE8A) == Decimal("40000")
    assert _money(proved) == _money(agreed)
    assert _money(agreed) == _money(go("m1-agreed", "v73"))


def test_no_recorded_form_1098_still_asks_the_v73_question() -> None:
    old, new = go("m1-silent", "v73"), go("m1-silent", "v74")
    assert miq.blocked(old.model) == miq.blocked(new.model)
    assert "12e" in _asks(new, M1)


def test_an_open_form_1098_family_blocks_the_same_lines_without_the_question_on_v74() -> None:
    old, new = go("m1-open", "v73"), go("m1-open", "v74")
    assert set(miq.blocked(old.model)) == set(miq.blocked(new.model))
    assert "12e" in _asks(old, M1)
    assert _asks(new, M1) == []
    assert _dec(new, LINE12E) is None and _dec(old, LINE12E) is None
    assert _money(old) == _money(new)


def test_a_contradicting_form_1098_answer_publishes_the_statement_on_v74() -> None:
    contradicted = go("m1-contradict", "v74")
    assert _money(contradicted) == _money(go("m1-agreed", "v74"))
    assert not any(row.get("code") == "F1098_SCOPE_CONTRADICTION" for row in contradicted.dispositions)
    v73 = go("m1-contradict", "v73")
    assert any(row.get("code") == "F1098_SCOPE_CONTRADICTION" for row in _rows(v73, "form1040-line12e"))
    assert _dec(v73, LINE12E) is None


def test_a_joint_return_with_one_form_1098_publishes_line_12e() -> None:
    run = go("m1-joint", "v74")
    assert _asks(run, M1) == []
    assert _dec(run, LINE12E) == Decimal("40000")
    assert _dec(run, LINE8A) == Decimal("40000")


def test_the_base_return_publishes_the_v73_amounts() -> None:
    assert _money(go("base", "v74")) == _money(go("base", "v73"))
    assert _dec(go("base", "v74"), LINE12E) == Decimal("15750")


def test_box_7_of_30_still_asks_and_the_answered_return_matches_v73() -> None:
    unanswered = go("ftc-30", "v74")
    assert miq.blocked(unanswered.model) == miq.blocked(go("ftc-30", "v73").model)
    assert _asks(unanswered, FTC)
    assert any(F1116 in row.get("missing", []) for row in _rows(unanswered, "schedule3-line1-direct-ftc"))
    assert _money(go("ftc-30-yes", "v74")) == _money(go("ftc-30-yes", "v73"))
    assert _dec(go("ftc-30-yes", "v74"), CREDIT) == Decimal("30")


def test_box_7_of_400_is_not_asked_and_matches_the_answered_return() -> None:
    proved, answered = go("ftc-400", "v74"), go("ftc-400-yes", "v73")
    assert _asks(proved, FTC) == []
    assert any(row.get("disposition") == "inapplicable" for row in _rows(proved, "schedule3-line1-direct-ftc"))
    assert _dec(proved, CREDIT) is None
    assert _money(proved) == _money(answered)
    assert _money(go("ftc-400-yes", "v74")) == _money(answered)


def test_the_joint_caps_are_500_and_700() -> None:
    under = go("ftc-joint-500", "v74")
    assert miq.blocked(under.model) == miq.blocked(go("ftc-joint-500", "v73").model)
    assert _asks(under, FTC)
    assert _dec(under, LINE12E) == Decimal("31500")
    over = go("ftc-joint-700", "v74")
    assert _asks(over, FTC) == []
    assert any(row.get("disposition") == "inapplicable" for row in _rows(over, "schedule3-line1-direct-ftc"))
    assert _dec(over, CREDIT) is None
    assert _dec(over, LINE12E) == Decimal("31500")
    assert _money(over) == _money(go("ftc-joint-700-yes", "v73"))


def test_the_held_proofs_still_ask_on_v74() -> None:
    for kind, fragment in (("l2a-proved", L2A), ("ctc-proved", CTC)):
        old, new = go(kind, "v73"), go(kind, "v74")
        assert miq.blocked(old.model) == miq.blocked(new.model)
        assert _asks(new, fragment)


def test_v73_keeps_both_contradiction_blocks_and_v74_keeps_the_other_dependent_one() -> None:
    child = go("ctc-contradict", "v73")
    assert any(row.get("code") == "DEPENDENCY_INVALID" for row in _rows(child, "odc-child-marked-conflict"))
    same = go("ctc-contradict", "v74")
    assert miq.blocked(child.model) == miq.blocked(same.model)
    assert any(row.get("code") == "DEPENDENCY_INVALID" for row in _rows(same, "odc-child-marked-conflict"))


def test_oid_and_exception_1_are_unchanged_on_v74() -> None:
    for kind, fragment in (("oid-silent", OID_Q), ("oid-box1", OID_Q), ("exc-silent", EXC_Q), ("exc-box2a", EXC_Q)):
        old, new = go(kind, "v73"), go(kind, "v74")
        assert miq.blocked(old.model) == miq.blocked(new.model)
        assert _asks(new, fragment)
