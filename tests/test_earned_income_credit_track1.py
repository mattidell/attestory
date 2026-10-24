"""Track 1: 2025 earned income credit for a return with no qualifying child.

Proved through the real coordinator on core-calculations v53. The 0-child
table is the printed-table parameter, checked against the P0 probe for
every band.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

import unittest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import validate_package
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.projection import compute_derivation_currency
from packages.kernel.currency import compute_currency
from packages.kernel.findings import project
from tests.test_refund_or_amount_owed_track1 import (
    CONTENT,
    RELEASE_DIR,
    ROOT,
    USER,
    _act,
    _attested,
    _finish,
    _finish_v52,
    _income_acts,
    _load,
    _run_v52,
    _sdd,
    _value,
)
from tests.test_refund_or_amount_owed_track2 import (
    _add_bottom_line_answers,
    _reopen_interest_with_real_box1,
)

PACKAGE_V53 = CONTENT / "package.core-calculations.v53.json"
REGISTRY_V51 = CONTENT / "published-packages.v51.json"
RELEASE_V51 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v51.json"
SURFACE_V53 = PublicationSurface(RELEASE_DIR, REGISTRY_V51, CONTENT)
ADOPTION = (
    ROOT
    / "packages/sample_data/earned_income_credit/adoptions/adopt-core-v53-current.json"
)
PROBE_PATH = (
    ROOT
    / "docs/phases/engine-breadth/milestones/earned-income-credit-evidence/probe.py"
)
V52_CHECKSUM = "f1ab428e8bdb94c792628c761a8bd572d85447e1fe769382838be79a98a01c6c"

FS = "tax.us.2025.filing-status"
LINE27A = "tax.us.2025.payments.line27a"
LINES2831 = "tax.us.2025.payments.lines28-31"
TOTAL = "tax.us.2025.payments.lines27-31-total"
LINE32 = "tax.us.2025.payments.line32"
INV = "tax.us.2025.eic.investment-income"
L1 = "tax.us.2025.eic.worksheet-a.line-1"
L3 = "tax.us.2025.eic.worksheet-a.line-3"
L6 = "tax.us.2025.eic.worksheet-a.line-6"
EARLY = "tax.us.2025.eic.early-stop"
ELIG = "tax.us.2025.eic.eligibility-result"

QC = "tax.us.2025.eic.no-qualifying-child"
TP_SSN = "tax.us.2025.eic.taxpayer-valid-ssn"
SP_SSN = "tax.us.2025.eic.spouse-valid-ssn"
NRA = "tax.us.2025.eic.not-nonresident-alien"
AGE = "tax.us.2025.eic.age-25-under-65"
HOME = "tax.us.2025.eic.main-home-in-us"
NOT_QC = "tax.us.2025.eic.not-qualifying-child-of-another"
NOT_DEP = "tax.us.2025.eic.not-claimable-as-dependent"
UNSUP = "tax.us.2025.eic.no-unsupported-situations"
L2831_FACT = "tax.us.2025.lines28-31-scope.no-other-refundable-credits"

EIC_FACTS = (QC, UNSUP, TP_SSN, NRA, AGE, HOME, SP_SSN, NOT_QC, NOT_DEP)
EIC_ANSWERS = tuple(
    "tax.us.2025.eic.answer." + fact_id.rsplit(".", 1)[-1] for fact_id in EIC_FACTS
)
PASSING = {fact: "yes" for fact in (*EIC_FACTS, L2831_FACT)}
SINGLE_REMAINING = (UNSUP, TP_SSN, NRA, AGE, HOME, NOT_QC, NOT_DEP)


def _probe() -> Any:
    spec = importlib.util.spec_from_file_location("eic_p0_probe", PROBE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("earned income credit probe is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(
    acts: list[dict[str, object]], run_id: str
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=SURFACE_V53,
            output_name="out.json",
        )
        pubs: dict[str, dict[str, Any]] = {}
        for pub in outcome.publications or ():
            pubs[str(pub.finding["symbol"])] = pub.finding
        blocked: list[dict[str, Any]] = []
        if outcome.output_path is not None:
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            for row in report.get("dispositions", []):
                if row.get("disposition") == "blocked":
                    blocked.append(row)
        return pubs, blocked


def _finish_v53(acts: list[dict[str, object]], note: str) -> list[dict[str, object]]:
    return _finish(
        acts,
        package_path=PACKAGE_V53,
        package_version="v53",
        release_path=RELEASE_V51,
        release_version="v51",
        note=note,
    )


def _finding_id(acts: list[dict[str, object]], fact_id: str) -> str:
    prefix = fact_id + "|"
    for act in acts:
        if act.get("kind") != "assertion":
            continue
        finding = cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("finding", {}))
        if str(finding.get("fact_id", "")).startswith(prefix):
            return str(finding["id"])
    raise AssertionError(f"no assertion for {fact_id}")


def _with_answers(
    acts: list[dict[str, object]], answers: dict[str, str]
) -> list[dict[str, object]]:
    acts = list(acts)
    acts.append(_act(len(acts), "bundle-adoption", {"bundle": _load("eic-questions.bundle.json")}))
    for fact_id, value in answers.items():
        suffix = fact_id.rsplit(".", 1)[-1]
        acts.append(
            _act(
                len(acts),
                "assertion",
                {"finding": _attested(f"demo.eic.{suffix}", f"{fact_id}|tax-year=2025", value)},
            )
        )
    return acts


def _acts(
    *,
    wages: float,
    filing_status: str = "single",
    interest: float | None = None,
    loss: bool = False,
    answers: dict[str, str] | None = None,
) -> list[dict[str, object]]:
    acts = cast(
        list[dict[str, object]],
        _sdd()._senior_acts(wages=wages, filing_status=filing_status),
    )
    if interest is not None:
        acts, _payer, _stmt = _reopen_interest_with_real_box1(acts, amount=interest)
    if loss:
        acts = cast(
            list[dict[str, object]],
            _sdd().toti._probe()._splice_schedule_d_transactions(acts, st=[(1, 3001)], lt=[]),
        )
    if answers is not None:
        acts = _with_answers(acts, answers)
    return acts


def _credit(
    label: str,
    *,
    wages: float,
    filing_status: str = "single",
    interest: float | None = None,
    loss: bool = False,
    answers: dict[str, str] | None = None,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[dict[str, object]]]:
    raw = _acts(
        wages=wages,
        filing_status=filing_status,
        interest=interest,
        loss=loss,
        answers=PASSING if answers is None else answers,
    )
    pubs, blocked = _run(_finish_v53(raw, label), f"demo.eic.t1.{label}")
    return pubs, blocked, raw


def _row(blocked: list[dict[str, Any]], artifact_id: str) -> dict[str, Any]:
    rows = [row for row in blocked if row.get("artifact_id") == artifact_id]
    if len(rows) != 1:
        shown = [
            (row.get("artifact_id"), row.get("code"), row.get("missing"))
            for row in blocked
            if "eic" in str(row.get("artifact_id", "")) or "line27" in str(row.get("artifact_id", "")) or "lines28" in str(row.get("artifact_id", ""))
        ]
        raise AssertionError(f"{artifact_id} blocked rows {len(rows)}; eic blocks {shown}")
    return rows[0]


def _closure(pubs: dict[str, dict[str, Any]], symbol: str) -> set[str]:
    by_id = {finding["id"]: finding for finding in pubs.values()}
    seen: set[str] = set()
    stack = [pubs[symbol]["id"]]
    found: set[str] = set()
    while stack:
        fid = stack.pop()
        if fid in seen:
            continue
        seen.add(fid)
        found.add(fid)
        finding = by_id.get(fid)
        if finding is None:
            continue
        for pin in finding.get("pins", []):
            pin_id = pin.get("id")
            if isinstance(pin_id, str):
                stack.append(pin_id)
    return found


def _assert_zero_names(test: unittest.TestCase, pubs: dict[str, dict[str, Any]], finding_id: str) -> None:
    test.assertEqual(_value(pubs, LINE27A), Decimal("0"))
    test.assertIn(finding_id, _closure(pubs, LINE27A))


def _eic_missing(blocked: list[dict[str, Any]]) -> list[str]:
    names: list[str] = []
    for row in blocked:
        for name in row.get("missing", []):
            if str(name).startswith("tax.us.2025.eic."):
                names.append(str(name))
    return names


class PackageChain(unittest.TestCase):
    def test_v53_validates_and_adoption_pins_the_release(self) -> None:
        corpus: dict[tuple[str, str], dict[str, Any]] = {}
        for path in CONTENT.glob("*.json"):
            value = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(value, dict) and isinstance(value.get("id"), str) and isinstance(value.get("version"), str):
                corpus[(value["id"], value["version"])] = value
        package = json.loads(PACKAGE_V53.read_text(encoding="utf-8"))
        result = validate_package(package, corpus, DerivationSchemas())
        self.assertTrue(result.ok, [issue.code for issue in result.issues])
        registry = json.loads(REGISTRY_V51.read_text(encoding="utf-8"))
        packages = [(row["id"], row["version"]) for row in registry["packages"]]
        self.assertEqual(packages, sorted(packages))
        citizens = [(row["id"], row["version"]) for row in registry["citizens"]]
        self.assertEqual(citizens, sorted(citizens))
        listed = next(
            row for row in registry["packages"]
            if row["id"] == "tax.us.2025.package.core-calculations" and row["version"] == "v53"
        )
        self.assertEqual(listed["checksum"], package["package_checksum"])
        registry_sha = hashlib.sha256(REGISTRY_V51.read_bytes()).hexdigest()
        release = json.loads(RELEASE_V51.read_text(encoding="utf-8"))
        self.assertEqual(release["package_registry_sha256"], registry_sha)
        adoption = json.loads(ADOPTION.read_text(encoding="utf-8"))
        self.assertEqual(adoption["payload"]["package"]["checksum"], package["package_checksum"])
        self.assertEqual(
            adoption["payload"]["release"]["checksum"],
            hashlib.sha256(RELEASE_V51.read_bytes()).hexdigest(),
        )
        v52 = json.loads((CONTENT / "package.core-calculations.v52.json").read_text(encoding="utf-8"))
        self.assertEqual(v52["package_checksum"], V52_CHECKSUM)

    def test_rule_files_stay_under_5kb(self) -> None:
        names = [
            path.name
            for path in CONTENT.glob("rule.eic-*.json")
        ] + [
            "rule.form1040-line27a.json",
            "rule.form1040-lines28-31.json",
            "rule.form1040-lines27-31-total.v2.json",
            "rule.form1040-line32.v2.json",
        ]
        for name in names:
            size = (CONTENT / name).stat().st_size
            self.assertLessEqual(size, 5000, name)

    def test_table_matches_probe_for_every_0_child_band(self) -> None:
        probe = _probe()
        table = _load("parameter.eic-table-2025.json")
        self.assertEqual(table["id"], "tax.us.2025.parameter.eic-table-2025")
        self.assertEqual(set(table["values"]), {"other", "joint"})
        for column, probe_status in (("other", "other"), ("joint", "mfj")):
            completed = int(probe.LIMITS[probe_status][0][3])
            rows = table["values"][column]
            self.assertIsNone(rows[-1]["upper"])
            self.assertEqual(int(rows[-1]["lower"]), completed)
            self.assertEqual(int(rows[-1]["value"]), 0)
            self.assertEqual(probe.table_credit(completed, 0, probe_status), 0)
            cursor = 1
            self.assertEqual(int(rows[0]["lower"]), 1)
            for row in rows[:-1]:
                lower = int(row["lower"])
                upper = int(row["upper"])
                value = int(row["value"])
                self.assertEqual(lower, cursor, column)
                self.assertLess(lower, upper, column)
                self.assertEqual(probe.table_credit(lower, 0, probe_status), value, column)
                self.assertEqual(probe.table_credit(upper - 1, 0, probe_status), value, column)
                cursor = upper
            self.assertEqual(cursor, completed, column)
            starred = rows[-2]
            self.assertEqual(int(starred["lower"]), (completed // 50) * 50, column)
            self.assertEqual(int(starred["upper"]), completed, column)
            self.assertEqual(int(starred["value"]), probe.FOOTNOTES[(probe_status, 0)], column)


class Credit(unittest.TestCase):
    def test_case_rows(self) -> None:
        rows: tuple[tuple[str, dict[str, Any], str], ...] = (
            ("single-5000", {"wages": 5000}, "384"),
            ("single-9000", {"wages": 9000}, "649"),
            ("single-15000", {"wages": 15000}, "312"),
            ("single-19050", {"wages": 19050}, "2"),
            ("single-19100", {"wages": 19100}, "0"),
            ("single-19103", {"wages": 19103}, "0"),
            ("single-5000-interest-2000", {"wages": 5000, "interest": 2000}, "384"),
            ("single-5000-interest-11950", {"wages": 5000, "interest": 11950}, "163"),
            ("single-9000-interest-6000", {"wages": 9000, "interest": 6000}, "312"),
            ("single-9000-loss", {"wages": 9000, "loss": True}, "649"),
            ("joint-8000", {"wages": 8000, "filing_status": "married_filing_jointly"}, "614"),
            ("joint-20000", {"wages": 20000, "filing_status": "married_filing_jointly"}, "473"),
            ("joint-26200", {"wages": 26200, "filing_status": "married_filing_jointly"}, "1"),
            ("joint-26213", {"wages": 26213, "filing_status": "married_filing_jointly"}, "1"),
            ("qss-5000", {"wages": 5000, "filing_status": "qualifying_surviving_spouse"}, "384"),
        )
        for label, kwargs, expected in rows:
            with self.subTest(label=label):
                pubs, blocked, _raw = _credit(label, **kwargs)
                self.assertEqual(_value(pubs, LINE27A), Decimal(expected), _eic_missing(blocked))
                self.assertEqual(_value(pubs, LINES2831), Decimal("0"))
                self.assertEqual(_value(pubs, TOTAL), Decimal(expected))
                self.assertEqual(_value(pubs, LINE32), Decimal(expected))

    def test_credit_path_pins_every_eic_answer(self) -> None:
        pubs, blocked, _raw = _credit("pins", wages=9000)
        self.assertEqual(_value(pubs, LINE27A), Decimal("649"), _eic_missing(blocked))
        closure = _closure(pubs, LINE27A)
        for symbol in EIC_ANSWERS:
            self.assertIn(pubs[symbol]["id"], closure, symbol)

    def test_unsupported_yes_to_no_displaces_line_27a(self) -> None:
        pubs, blocked, raw = _credit("unsupported-before", wages=9000)
        self.assertEqual(_value(pubs, LINE27A), Decimal("649"), _eic_missing(blocked))
        before_id = pubs[LINE27A]["id"]
        answer = "tax.us.2025.eic.answer.no-unsupported-situations"
        self.assertIn(pubs[answer]["id"], _closure(pubs, LINE27A))
        corrected = list(raw)
        corrected.append(
            _act(
                len(corrected),
                "assertion",
                {
                    "finding": _attested(
                        "demo.eic.no-unsupported-situations.correction",
                        f"{UNSUP}|tax-year=2025",
                        "no",
                    )
                },
            )
        )
        after_acts = _finish_v53(corrected, "unsupported yes corrected to no")
        pubs_after, blocked_after = _run(after_acts, "demo.eic.t1.unsupported-after")
        self.assertNotIn(LINE27A, pubs_after)
        row = _row(blocked_after, "tax.us.2025.rule.eic-answer.no-unsupported-situations")
        self.assertEqual(row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(row["missing"], [])
        schemas = DerivationSchemas()
        kernel = compute_currency(
            project(tuple(dict(act) for act in after_acts), schemas.registry)
        )
        self.assertIn("demo.eic.no-unsupported-situations", kernel.displaced_finding_ids)
        self.assertIn(
            "demo.eic.no-unsupported-situations.correction",
            kernel.current_finding_ids,
        )
        derived = {finding["id"]: finding for finding in pubs.values()}
        view = compute_derivation_currency(kernel, derived)
        self.assertIn(before_id, view.displaced_derived_ids)

    def test_completed_amount_asks_only_the_qualifying_child_question(self) -> None:
        for label, kwargs in (
            ("single-19104", {"wages": 19104}),
            ("single-20000", {"wages": 20000}),
            ("joint-26214", {"wages": 26214, "filing_status": "married_filing_jointly"}),
        ):
            with self.subTest(label=label):
                answers = {QC: "yes", L2831_FACT: "yes"}
                pubs, blocked, _raw = _credit(label, answers=answers, **kwargs)
                self.assertEqual(_value(pubs, LINE27A), Decimal("0"), _eic_missing(blocked))
                self.assertEqual(_eic_missing(blocked), [])
                self.assertEqual(_value(pubs, "tax.us.2025.eic.answer.taxpayer-valid-ssn"), Decimal("1"))

    def test_high_income_asks_no_eic_question(self) -> None:
        pubs, blocked, _raw = _credit(
            "wages-70000", wages=70000, answers={L2831_FACT: "yes"}
        )
        _assert_zero_names(self, pubs, pubs[L3]["id"])
        self.assertNotIn(pubs[L1]["id"], _closure(pubs, LINE27A))
        answer = "tax.us.2025.eic.answer.no-unsupported-situations"
        self.assertNotIn(pubs[answer]["id"], _closure(pubs, LINE27A))
        self.assertEqual(_eic_missing(blocked), [])

    def test_box1_ceiling_with_agi_below_requires_the_unsupported_answer(self) -> None:
        answer = "tax.us.2025.eic.answer.no-unsupported-situations"
        # A $3,000 Schedule D loss leaves box 1 at the ceiling and AGI under it.
        pubs, blocked, _raw = _credit(
            "box1-70000-loss-missing",
            wages=70000,
            loss=True,
            answers={L2831_FACT: "yes"},
        )
        self.assertGreaterEqual(_value(pubs, L1), Decimal("68675"))
        self.assertLess(_value(pubs, L3), Decimal("68675"))
        self.assertNotIn(LINE27A, pubs)
        row = _row(blocked, "tax.us.2025.rule.eic-answer.no-unsupported-situations")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(row["missing"], [UNSUP])

        pubs, blocked, raw = _credit(
            "box1-70000-loss-no",
            wages=70000,
            loss=True,
            answers={UNSUP: "no", L2831_FACT: "yes"},
        )
        self.assertNotIn(LINE27A, pubs)
        row = _row(blocked, "tax.us.2025.rule.eic-answer.no-unsupported-situations")
        self.assertEqual(row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(row["missing"], [])
        self.assertIn(_finding_id(raw, UNSUP), {pin["id"] for pin in row["pins"]})

        pubs, blocked, _raw = _credit(
            "box1-70000-loss-yes",
            wages=70000,
            loss=True,
            answers={UNSUP: "yes", L2831_FACT: "yes"},
        )
        self.assertGreaterEqual(_value(pubs, L1), Decimal("68675"))
        self.assertLess(_value(pubs, L3), Decimal("68675"))
        _assert_zero_names(self, pubs, pubs[answer]["id"])
        self.assertIn(pubs[L1]["id"], _closure(pubs, LINE27A))
        self.assertEqual(_value(pubs, "tax.us.2025.eic.answer.taxpayer-valid-ssn"), Decimal("1"))
        self.assertEqual(_eic_missing(blocked), [])

        pubs, blocked, _raw = _credit(
            "box1-20000-loss-missing",
            wages=20000,
            loss=True,
            answers={QC: "yes", L2831_FACT: "yes"},
        )
        self.assertGreaterEqual(_value(pubs, L1), Decimal("19104"))
        self.assertLess(_value(pubs, L1), Decimal("68675"))
        self.assertLess(_value(pubs, L3), Decimal("19104"))
        self.assertNotIn(LINE27A, pubs)
        row = _row(blocked, "tax.us.2025.rule.eic-answer.no-unsupported-situations")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(row["missing"], [UNSUP])

        pubs, blocked, _raw = _credit(
            "box1-20000-loss-yes",
            wages=20000,
            loss=True,
            answers={QC: "yes", UNSUP: "yes", L2831_FACT: "yes"},
        )
        self.assertLess(_value(pubs, L3), Decimal("19104"))
        _assert_zero_names(self, pubs, pubs[answer]["id"])
        self.assertEqual(_value(pubs, "tax.us.2025.eic.answer.taxpayer-valid-ssn"), Decimal("1"))
        self.assertEqual(_eic_missing(blocked), [])

    def test_mfs_and_hoh_box1_column_ceiling_ignores_the_unsupported_answer(self) -> None:
        answer = "tax.us.2025.eic.answer.no-unsupported-situations"
        for status in ("married_filing_separately", "head_of_household"):
            with self.subTest(status=status, unsupported="absent"):
                pubs, blocked, raw = _credit(
                    f"box1-20000-loss-{status}-absent",
                    wages=20000,
                    loss=True,
                    filing_status=status,
                    answers={QC: "yes", L2831_FACT: "yes"},
                )
                self.assertGreaterEqual(_value(pubs, L1), Decimal("19104"))
                self.assertLess(_value(pubs, L3), Decimal("19104"))
                _assert_zero_names(self, pubs, _finding_id(raw, FS))
                self.assertNotIn(pubs[answer]["id"], _closure(pubs, LINE27A))
                self.assertEqual(_eic_missing(blocked), [])
            with self.subTest(status=status, unsupported="no"):
                pubs, blocked, raw = _credit(
                    f"box1-20000-loss-{status}-no",
                    wages=20000,
                    loss=True,
                    filing_status=status,
                    answers={QC: "yes", UNSUP: "no", L2831_FACT: "yes"},
                )
                self.assertEqual(_value(pubs, LINE27A), Decimal("0"), _eic_missing(blocked))
                self.assertNotIn(_finding_id(raw, UNSUP), _closure(pubs, LINE27A))
                self.assertEqual(_eic_missing(blocked), [])

    def test_investment_income_over_the_limit_requires_the_unsupported_answer(self) -> None:
        pubs, blocked, _raw = _credit(
            "interest-11951-yes",
            wages=5000,
            interest=11951,
            answers={UNSUP: "yes", L2831_FACT: "yes"},
        )
        self.assertEqual(_value(pubs, INV), Decimal("11951"))
        _assert_zero_names(self, pubs, pubs[INV]["id"])
        answer = "tax.us.2025.eic.answer.no-unsupported-situations"
        self.assertIn(pubs[answer]["id"], _closure(pubs, LINE27A))
        self.assertEqual(_value(pubs, "tax.us.2025.eic.answer.taxpayer-valid-ssn"), Decimal("1"))
        self.assertEqual(_eic_missing(blocked), [])

        pubs, blocked, raw = _credit(
            "interest-11951-no",
            wages=5000,
            interest=11951,
            answers={UNSUP: "no", L2831_FACT: "yes"},
        )
        self.assertNotIn(LINE27A, pubs)
        row = _row(blocked, "tax.us.2025.rule.eic-answer.no-unsupported-situations")
        self.assertEqual(row["code"], "DEPENDENCY_INVALID")
        self.assertEqual(row["missing"], [])
        self.assertIn(_finding_id(raw, UNSUP), {pin["id"] for pin in row["pins"]})

        pubs, blocked, _raw = _credit(
            "interest-11951-missing",
            wages=5000,
            interest=11951,
            answers={L2831_FACT: "yes"},
        )
        self.assertNotIn(LINE27A, pubs)
        row = _row(blocked, "tax.us.2025.rule.eic-answer.no-unsupported-situations")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(row["missing"], [UNSUP])

    def test_agi_at_the_completed_amount_names_line_3(self) -> None:
        pubs, blocked, _raw = _credit(
            "agi-completed",
            wages=9000,
            interest=11950,
            answers={QC: "yes", L2831_FACT: "yes"},
        )
        _assert_zero_names(self, pubs, pubs[L3]["id"])
        self.assertEqual(_eic_missing(blocked), [])

    def test_mfs_and_hoh_without_a_qualifying_child_are_zero(self) -> None:
        for status in ("married_filing_separately", "head_of_household"):
            with self.subTest(status=status):
                raw = _acts(wages=9000, filing_status=status, answers={QC: "yes", L2831_FACT: "yes"})
                pubs, blocked = _run(_finish_v53(raw, status), f"demo.eic.t1.{status}")
                _assert_zero_names(self, pubs, _finding_id(raw, FS))
                self.assertEqual(_eic_missing(blocked), [])

    def test_failing_answer_publishes_zero_and_names_the_fact(self) -> None:
        cases = (
            ("tp-ssn", "single", 9000, TP_SSN),
            ("nra", "single", 9000, NRA),
            ("age", "single", 9000, AGE),
            ("home", "single", 9000, HOME),
            ("not-qc", "single", 9000, NOT_QC),
            ("not-dep", "single", 9000, NOT_DEP),
            ("spouse-ssn", "married_filing_jointly", 8000, SP_SSN),
        )
        for label, status, wages, fact_id in cases:
            with self.subTest(fact=fact_id):
                answers = dict(PASSING)
                answers[fact_id] = "no"
                raw = _acts(wages=wages, filing_status=status, answers=answers)
                pubs, _blocked = _run(_finish_v53(raw, label), f"demo.eic.t1.fail.{label}")
                gate = "tax.us.2025.eic.answer." + fact_id.rsplit(".", 1)[-1]
                self.assertEqual(_value(pubs, gate), Decimal("0"))
                self.assertIn(_finding_id(raw, fact_id), {pin["id"] for pin in pubs[gate]["pins"]})
                self.assertIn(pubs[gate]["id"], _closure(pubs, LINE27A))
                self.assertEqual(_value(pubs, LINE27A), Decimal("0"))

    def test_qualifying_child_or_unsupported_no_blocks(self) -> None:
        cases = (
            ("qc-single", "single", QC),
            ("qc-mfs", "married_filing_separately", QC),
            ("qc-hoh", "head_of_household", QC),
            ("unsupported", "single", UNSUP),
        )
        for label, status, fact_id in cases:
            with self.subTest(label=label):
                answers = dict(PASSING)
                answers[fact_id] = "no"
                raw = _acts(wages=9000, filing_status=status, answers=answers)
                pubs, blocked = _run(_finish_v53(raw, label), f"demo.eic.t1.block.{label}")
                self.assertNotIn(LINE27A, pubs)
                rule = "tax.us.2025.rule.eic-answer." + fact_id.rsplit(".", 1)[-1]
                row = _row(blocked, rule)
                self.assertEqual(row["code"], "DEPENDENCY_INVALID")
                self.assertEqual(row["missing"], [])
                self.assertIn(_finding_id(raw, fact_id), {pin["id"] for pin in row["pins"]})

    def test_each_required_single_answer_missing_names_that_fact(self) -> None:
        answers = {QC: "yes", SP_SSN: "yes", L2831_FACT: "yes"}
        pubs, blocked, _raw = _credit("single-missing", wages=9000, answers=answers)
        self.assertNotIn(LINE27A, pubs)
        for fact_id in SINGLE_REMAINING:
            rule = "tax.us.2025.rule.eic-answer." + fact_id.rsplit(".", 1)[-1]
            row = _row(blocked, rule)
            self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
            self.assertEqual(row["missing"], [fact_id])
        self.assertEqual(_value(pubs, "tax.us.2025.eic.answer.spouse-valid-ssn"), Decimal("1"))

    def test_joint_requires_the_spouse_ssn_and_not_the_nonjoint_facts(self) -> None:
        answers = dict(PASSING)
        del answers[SP_SSN]
        pubs, blocked, _raw = _credit(
            "joint-missing-spouse",
            wages=8000,
            filing_status="married_filing_jointly",
            answers=answers,
        )
        self.assertNotIn(LINE27A, pubs)
        row = _row(blocked, "tax.us.2025.rule.eic-answer.spouse-valid-ssn")
        self.assertEqual(row["missing"], [SP_SSN])

        answers = dict(PASSING)
        del answers[NOT_QC]
        del answers[NOT_DEP]
        pubs, blocked, _raw = _credit(
            "joint-omits-nonjoint",
            wages=8000,
            filing_status="married_filing_jointly",
            answers=answers,
        )
        self.assertEqual(_value(pubs, LINE27A), Decimal("614"), _eic_missing(blocked))
        self.assertEqual(_value(pubs, "tax.us.2025.eic.answer.not-qualifying-child-of-another"), Decimal("1"))
        self.assertEqual(_value(pubs, "tax.us.2025.eic.answer.not-claimable-as-dependent"), Decimal("1"))

    def test_missing_qualifying_child_answer_names_that_fact(self) -> None:
        answers = {fact: "yes" for fact in (*SINGLE_REMAINING, SP_SSN, L2831_FACT)}
        pubs, blocked, _raw = _credit("missing-qc", wages=9000, answers=answers)
        self.assertNotIn(LINE27A, pubs)
        row = _row(blocked, "tax.us.2025.rule.eic-answer.no-qualifying-child")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(row["missing"], [QC])

    def test_lines_28_through_31_missing_blocks_on_a_credit_return(self) -> None:
        answers = {fact: "yes" for fact in EIC_FACTS}
        pubs, blocked, _raw = _credit("missing-lines-28-31", wages=5000, answers=answers)
        self.assertEqual(_value(pubs, LINE27A), Decimal("384"))
        row = _row(blocked, "tax.us.2025.rule.form1040-lines28-31")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(row["missing"], [L2831_FACT])

    def test_v52_run_is_unchanged(self) -> None:
        acts = _add_bottom_line_answers(_income_acts(wages=50000.0))
        acts = _finish_v52(acts, "v52 has no separate earned income credit")
        pubs, _blocked = _run_v52(acts, "demo.eic.t1.v52")
        self.assertNotIn(LINE27A, pubs)
        self.assertEqual(_value(pubs, TOTAL), Decimal("0"))
        self.assertEqual(_value(pubs, LINE32), Decimal("0"))
        self.assertNotIn(L6, pubs)
