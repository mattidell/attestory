"""Track 1: line 20 without foreign-tax questions, and withholding on lines
25a-25d, proved through the real coordinator on core-calculations v52.

Reuses the senior-and-dependent-deductions Track 1 test's own act-log
builder (``_senior_acts``, via its dynamic loader for the tax-on-taxable-
income P0 probe) for the income-chain cases, and a standalone minimal act
log (bundle-adoption + horizon-genesis + member-transition/assertion +
closure, no income chain at all) for the withholding-only cases, since
lines 25a-25d require nothing but their own source families and
``rounding.convention``. Pattern: ``tests/test_senior_and_dependent_
deductions_track1.py``; ``tests/test_frrs_t4_w2_live_integration.py`` for
the standalone act-log shape.
"""

from __future__ import annotations

import copy
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
from packages.derivation.production_resolver import PublicationSurface

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
RELEASE_DIR = (
    ROOT
    / "packages"
    / "sample_data"
    / "student_loan_worksheet_integration"
    / "publication_surface"
    / "releases"
)
PACKAGE_V52 = CONTENT / "package.core-calculations.v52.json"
PACKAGE_V51 = CONTENT / "package.core-calculations.v51.json"
REGISTRY_V50 = CONTENT / "published-packages.v50.json"
REGISTRY_V49 = CONTENT / "published-packages.v49.json"
RELEASE_V50 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v50.json"
RELEASE_V49 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v49.json"
SURFACE_V52 = PublicationSurface(RELEASE_DIR, REGISTRY_V50, CONTENT)
SURFACE_V51 = PublicationSurface(RELEASE_DIR, REGISTRY_V49, CONTENT)

USER = "demo.user.filer-1"
SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

LINE22 = "tax.us.2025.tax.after-nonrefundable-credits"
LINE20 = "tax.us.2025.credits.form1040-line20"
SCH3_L1 = "tax.us.2025.schedule3.line1-direct-ftc"
ELECTION = "tax.us.2025.direct-ftc.election"
LINE25A = "tax.us.2025.payments.line25a"
LINE25B = "tax.us.2025.payments.line25b"
LINE25C = "tax.us.2025.payments.line25c"
LINE25D = "tax.us.2025.payments.line25d"

SCOPE_TOKENS = (
    "all-foreign-income-passive",
    "all-foreign-income-on-1099div",
    "no-f1099int-foreign-tax",
    "no-k1-k3-foreign-tax",
    "no-other-foreign-tax-source",
    "tax-type-creditable",
    "legal-liability-and-paid",
    "no-refund-rebate-subsidy",
    "no-excluded-income-association",
    "holding-period-16-day-met",
    "no-short-sale-obligation",
    "country-recognized-non-terrorism",
    "no-carryback-carryforward",
    "no-schedule-a-deduction-election",
    "no-form-1116-required",
    "no-sch3-line2",
    "no-sch3-line3",
    "no-sch3-line4",
    "no-sch3-line5",
    "no-sch3-line6",
    "no-line17-schedule2-additional",
    "no-line19-ctc-odc",
    "no-schedule2-regular-tax-add",
    "no-form-4972-on-line16",
)

_SDD_TRACK1_PATH = ROOT / "tests" / "test_senior_and_dependent_deductions_track1.py"
_SDD = None


def _sdd() -> Any:
    global _SDD
    if _SDD is None:
        spec = importlib.util.spec_from_file_location("roao_t1_sdd", _SDD_TRACK1_PATH)
        if spec is None or spec.loader is None:
            raise RuntimeError("could not load senior-and-dependent-deductions Track 1 helpers")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _SDD = module
    return _SDD


def _toti_probe() -> Any:
    return _sdd().toti._probe()


def _act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    probe = _toti_probe()
    return cast(dict[str, object], probe._act(index, kind, payload))


def _attested(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    probe = _toti_probe()
    return cast(dict[str, object], probe._attested(finding_id, fact_id, value))


def _elective(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    probe = _toti_probe()
    return cast(dict[str, object], probe._elective(finding_id, fact_id, value))


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _finish(
    acts: list[dict[str, object]],
    *,
    package_path: Path,
    package_version: str,
    release_path: Path,
    release_version: str,
    note: str,
) -> list[dict[str, object]]:
    pkg = json.loads(package_path.read_text(encoding="utf-8"))
    rel_csum = hashlib.sha256(release_path.read_bytes()).hexdigest()
    built = copy.deepcopy(acts)
    adoption = copy.deepcopy(_toti_probe()._load_fixture_adoption())
    adoption["act_id"] = f"demo.roaot1.adopt.{len(built):03d}"
    payload = adoption["payload"]
    assert isinstance(payload, dict)
    payload["package"] = {
        "id": "tax.us.2025.package.core-calculations",
        "version": package_version,
        "checksum": pkg["package_checksum"],
    }
    payload["release"] = {
        "id": "demo.release.sli-worksheet-integration.2025",
        "version": release_version,
        "checksum": rel_csum,
    }
    payload["audit"] = {"note": note}
    built.append(adoption)
    for index, row in enumerate(built):
        row["committed_against"] = index
        row["actor"] = USER
    return built


def _finish_v52(acts: list[dict[str, object]], note: str) -> list[dict[str, object]]:
    return _finish(
        acts,
        package_path=PACKAGE_V52,
        package_version="v52",
        release_path=RELEASE_V50,
        release_version="v50",
        note=note,
    )


def _finish_v51(acts: list[dict[str, object]], note: str) -> list[dict[str, object]]:
    return _finish(
        acts,
        package_path=PACKAGE_V51,
        package_version="v51",
        release_path=RELEASE_V49,
        release_version="v49",
        note=note,
    )


def _run(
    acts: list[dict[str, object]], run_id: str, surface: PublicationSurface
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
            surface=surface,
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


def _run_v52(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    return _run(acts, run_id, SURFACE_V52)


def _run_v51(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    return _run(acts, run_id, SURFACE_V51)


def _value(pubs: dict[str, dict[str, Any]], symbol: str) -> Decimal:
    finding = pubs.get(symbol)
    if finding is None:
        raise AssertionError(f"missing publication {symbol}")
    return Decimal(str(finding["value"]))


def _missing_names(blocked: list[dict[str, Any]], artifact_token: str) -> list[str]:
    for row in blocked:
        if artifact_token in str(row.get("artifact_id", "")):
            return cast(list[str], row.get("missing", []))
    return []


# --- Income-chain cases (line 20 / line 22) -------------------------------


def _income_acts(*, wages: float = 50000.0) -> list[dict[str, object]]:
    """Single filer, W-2-only, every senior/dependent feature at its
    no-op default -- reuses the senior-and-dependent-deductions Track 1
    builder (itself built on the tax-on-taxable-income P0 probe's
    ``_base_acts``, which closes the Form 1099-DIV box-7 family empty and
    asserts the old blanket election/scope-token set)."""
    return cast(list[dict[str, object]], _sdd()._senior_acts(wages=wages, filing_status="single"))


def _strip_fact(acts: list[dict[str, object]], fact_prefix: str) -> list[dict[str, object]]:
    """Drop every act whose assertion answers a fact id starting with
    ``fact_prefix`` -- used to make a fact genuinely absent rather than
    answered."""
    kept = []
    for act in acts:
        if act.get("kind") == "assertion":
            payload = cast(dict[str, Any], act.get("payload", {}))
            finding = cast(dict[str, Any], payload.get("finding", {}))
            if str(finding.get("fact_id", "")).startswith(fact_prefix):
                continue
        kept.append(act)
    return kept


def _open_box7_with_foreign_tax(
    acts: list[dict[str, object]], *, amount: float, box1a: float, country: str = "FR"
) -> list[dict[str, object]]:
    """Reopens the closed-empty Form 1099-DIV box-7 family the base builder
    leaves in ``acts`` (horizon ``demo.probe.div7.h0``) and inserts one real
    foreign-tax-paid member before re-closing it at a successor horizon,
    mirroring ``tests/test_form1099div_box7_direct_ftc.py``'s own
    ``_b7_acts`` member-transition shape."""
    acts = copy.deepcopy(acts)
    old_closure_prefix = "tax.us.2025.f1099div.7.source-closure|family-horizon=demo.probe.div7.h0,"
    kept: list[dict[str, object]] = []
    for act in acts:
        if act.get("kind") == "assertion":
            payload = cast(dict[str, Any], act.get("payload", {}))
            finding = cast(dict[str, Any], payload.get("finding", {}))
            if str(finding.get("fact_id", "")).startswith(old_closure_prefix):
                continue
        kept.append(act)
    acts = kept

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    payer, stmt = "demo.roaot1.div7.payer", "demo.roaot1.div7.stmt"
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": payer, "kind": "tax.us.dividend-payer", "label": "Synthetic foreign payer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": stmt, "kind": "tax.us.1099div-statement", "label": "Synthetic foreign 1099-DIV"}})
    add("assertion", {"finding": _attested("demo.roaot1.div7.box1a", f"tax.us.2025.f1099div.box1a-ordinary|payer={payer},statement={stmt},tax-year=2025", box1a)})
    add("assertion", {"finding": _attested("demo.roaot1.div7.box8", f"tax.us.2025.f1099div.box8-country-companion|payer={payer},statement={stmt},tax-year=2025", country)})
    add("member-transition", {
        "family": {"id": "tax.us.2025.f1099div.7", "version": "v1"},
        "scope": SCOPE_KEY,
        "member": {"action": "assert", "finding": _attested("demo.roaot1.div7.box7", f"tax.us.2025.f1099div.box7-foreign-tax-paid|payer={payer},statement={stmt},tax-year=2025", amount)},
        "successor": {"id": "demo.roaot1.div7.h1", "predecessor": "demo.probe.div7.h0"},
    })
    add("assertion", {"finding": _attested("demo.roaot1.div7.closure", "tax.us.2025.f1099div.7.source-closure|family-horizon=demo.roaot1.div7.h1,tax-year=2025", True)})
    return acts


class LineTwentyWithoutForeignTax(unittest.TestCase):
    def test_no_foreign_tax_reaches_line22_without_eligibility_answers(self) -> None:
        # Strip the election and every scope-token assertion entirely (not
        # merely answer "no") -- a genuinely unanswered return, box 7 closed
        # empty, must still reach line 22. Excludes the 7 tokens
        # (no-sch3-line2..6, no-line17-schedule2-additional,
        # no-line19-ctc-odc) that rule.schedule3-line8 and
        # rule.form1040-tax-after-credits each require unconditionally on
        # their own, unrelated to this track's fix.
        independently_required = {
            "no-sch3-line2", "no-sch3-line3", "no-sch3-line4", "no-sch3-line5", "no-sch3-line6",
            "no-line17-schedule2-additional", "no-line19-ctc-odc",
        }
        acts = _income_acts(wages=50000.0)
        acts = _strip_fact(acts, ELECTION + "|")
        for token in SCOPE_TOKENS:
            if token in independently_required:
                continue
            acts = _strip_fact(acts, f"tax.us.2025.direct-ftc-scope.{token}|")
        acts = _finish_v52(acts, "no foreign tax: election and scope tokens never asked")
        pubs, blocked = _run_v52(acts, "demo.roaot1.case1")
        self.assertEqual(_value(pubs, LINE22), Decimal("3875"))
        self.assertEqual(_missing_names(blocked, "schedule3-line1-direct-ftc"), [])
        self.assertEqual(_missing_names(blocked, "form1040-tax-after-credits"), [])

    def test_foreign_tax_present_without_election_blocks_naming_it(self) -> None:
        acts = _income_acts(wages=50000.0)
        acts = _open_box7_with_foreign_tax(acts, amount=50.0, box1a=100.0)
        acts = _strip_fact(acts, ELECTION + "|")
        acts = _finish_v52(acts, "foreign tax present, election unanswered")
        _, blocked = _run_v52(acts, "demo.roaot1.case2")
        missing = _missing_names(blocked, "schedule3-line1-direct-ftc")
        self.assertIn(ELECTION, missing)

    def test_foreign_tax_present_with_election_matches_v1_shape(self) -> None:
        acts = _income_acts(wages=50000.0)
        acts = _open_box7_with_foreign_tax(acts, amount=50.0, box1a=100.0)
        acts = _strip_fact(acts, ELECTION + "|")
        acts.append(_act(len(acts), "assertion", {"finding": _elective("demo.roaot1.election.yes", f"{ELECTION}|tax-year=2025", "yes")}))
        acts = _finish_v52(acts, "foreign tax present, election yes, every scope token yes")
        pubs, blocked = _run_v52(acts, "demo.roaot1.case3")
        # box7-subtotal (50) <= total tax -> credit = 50, same min() shape v1 has.
        self.assertEqual(_value(pubs, SCH3_L1), Decimal("50"))
        self.assertEqual(_value(pubs, LINE20), Decimal("50"))
        self.assertEqual(_missing_names(blocked, "schedule3-line1-direct-ftc"), [])

    def test_v51_package_is_unaffected(self) -> None:
        # v1's own election default ("no") is a by-design dead end
        # regardless of this track (P0 Sec. 5); override to "yes" to reach a
        # published line 22 on the unmodified v51 package, exactly as the
        # P0 probe did.
        acts = _income_acts(wages=50000.0)
        acts = _strip_fact(acts, ELECTION + "|")
        acts.append(_act(len(acts), "assertion", {"finding": _elective("demo.roaot1.v51.election", f"{ELECTION}|tax-year=2025", "yes")}))
        acts = _finish_v51(acts, "v51 unchanged by the v52 successor")
        pubs, _ = _run_v51(acts, "demo.roaot1.v51check")
        self.assertEqual(_value(pubs, LINE22), Decimal("3875"))


# --- Withholding cases (lines 25a-25d), standalone (no income chain) ------


def _withholding_base() -> list[dict[str, object]]:
    acts: list[dict[str, object]] = []

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("core_calculations.bundle.v2.json")})
    add("assertion", {"finding": _attested("demo.roaot1.rounding", "rounding.convention|tax-year=2025", "half_up")})
    return acts

def _close_empty(acts: list[dict[str, object]], *, family: str, version: str, closure_fact: str, horizon: str) -> None:
    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("horizon-genesis", {"family": {"id": family, "version": version}, "scope": SCOPE_KEY, "horizon_id": horizon})
    add("assertion", {"finding": _attested(f"demo.roaot1.closure.{horizon}", f"{closure_fact}|family-horizon={horizon},tax-year=2025", True)})


def _add_w2_box2(acts: list[dict[str, object]], *, employer: str, slip: str, amount: float) -> None:
    """Asserts both box 1 (wages) and box 2 (withholding) for one synthetic
    W-2 slip -- line 25a v2 requires the current box-2 count to equal the
    current box-1 count (repair round 1), so a standalone withholding test
    exercising line 25a must keep both counts matched unless it is
    deliberately testing the mismatch itself."""

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("w2.bundle.v3.json")})
    add("bundle-adoption", {"bundle": _load("w2-box2.bundle.json")})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": employer, "kind": "tax.us.employer", "label": "Synthetic employer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": slip, "kind": "tax.us.w2-slip", "label": "Synthetic W-2 slip"}})
    add("assertion", {"finding": _attested(f"demo.roaot1.box1.{slip}", f"tax.us.2025.w2.box1-wages|employer={employer},w2-slip={slip},tax-year=2025", amount)})
    add("assertion", {"finding": _attested(f"demo.roaot1.box2.{slip}", f"tax.us.2025.w2.box2-withholding|employer={employer},w2-slip={slip},tax-year=2025", amount)})


def _close_w2_box1_and_box2(acts: list[dict[str, object]], *, horizon_suffix: str) -> None:
    _close_empty(acts, family="tax.us.2025.w2", version="v2", closure_fact="tax.us.2025.w2.source-closure", horizon=f"demo.roaot1.w2box1.{horizon_suffix}")
    _close_empty(acts, family="tax.us.2025.w2-box2", version="v1", closure_fact="tax.us.2025.w2-box2.source-closure", horizon=f"demo.roaot1.w2box2.{horizon_suffix}")


_BOX4_FAMILIES = {
    "w2-box2": (("w2.bundle.v3.json", "w2-box2.bundle.json"), "", "", ""),
    "f1099int-b4": ("f1099int-box4.bundle.json", "tax.us.2025.f1099int.b4", "v1", "tax.us.2025.f1099int.b4.source-closure"),
    "f1099div-b4": ("f1099div-box4.bundle.json", "tax.us.2025.f1099div.b4", "v1", "tax.us.2025.f1099div.b4.source-closure"),
    "f1099r-b4": ("f1099r-ira.bundle.v3.json", "tax.us.2025.f1099r.box4", "v1", "tax.us.2025.f1099r.box4.source-closure"),
    # Form 1099-K box 4 is a Track 1 stop-condition finding, not built (see
    # rule.form1040-line25b.json's own notes): it stays recorded and summed
    # nowhere, same as P0 found it. Line 25b therefore sums three document
    # subtotals, not four.
}


def _close_other_box4_families(acts: list[dict[str, object]], *, skip: set[str]) -> None:
    """Adopts and closes-empty every box-2/box-4 withholding family except
    the ones named in ``skip``, so line 25b (which requires all four 1099
    document subtotals) and line 25d resolve in a standalone test that only
    populates one document. ``w2-box2`` closes both the box-1 and box-2
    W-2 families empty together (0 == 0), since line 25a v2 requires their
    counts to match."""

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    for key, (bundle_names, family, version, closure_fact) in _BOX4_FAMILIES.items():
        if key in skip:
            continue
        names = bundle_names if isinstance(bundle_names, tuple) else (bundle_names,)
        for name in names:
            add("bundle-adoption", {"bundle": _load(name)})
        if key == "w2-box2":
            _close_w2_box1_and_box2(acts, horizon_suffix=str(len(acts)))
        else:
            _close_empty(acts, family=family, version=version, closure_fact=closure_fact, horizon=f"demo.roaot1.{key}.{len(acts)}")


class WithholdingLines(unittest.TestCase):
    def test_one_w2_box2_feeds_line25a(self) -> None:
        acts = _withholding_base()
        _add_w2_box2(acts, employer="demo.roaot1.w2a.employer", slip="demo.roaot1.w2a.slip", amount=4500.0)
        _close_w2_box1_and_box2(acts, horizon_suffix="one")
        acts = _finish_v52(acts, "one W-2, box 2 withholding feeds line 25a")
        pubs, blocked = _run_v52(acts, "demo.roaot1.w2box2.one")
        self.assertEqual(_value(pubs, LINE25A), Decimal("4500"))
        self.assertEqual(_missing_names(blocked, "form1040-line25a"), [])

    def test_two_w2s_box2_sum_line25a(self) -> None:
        acts = _withholding_base()
        _add_w2_box2(acts, employer="demo.roaot1.w2a.employer", slip="demo.roaot1.w2a.slip", amount=2000.0)
        # Second W-2: new entities only; the bundle is already adopted.
        acts.append(_act(len(acts), "entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.roaot1.w2b.employer", "kind": "tax.us.employer", "label": "Synthetic second employer"}}))
        acts.append(_act(len(acts), "entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.roaot1.w2b.slip", "kind": "tax.us.w2-slip", "label": "Synthetic second W-2 slip"}}))
        acts.append(_act(len(acts), "assertion", {"finding": _attested("demo.roaot1.box1.w2b", "tax.us.2025.w2.box1-wages|employer=demo.roaot1.w2b.employer,w2-slip=demo.roaot1.w2b.slip,tax-year=2025", 1200.0)}))
        acts.append(_act(len(acts), "assertion", {"finding": _attested("demo.roaot1.box2.w2b", "tax.us.2025.w2.box2-withholding|employer=demo.roaot1.w2b.employer,w2-slip=demo.roaot1.w2b.slip,tax-year=2025", 1200.0)}))
        _close_w2_box1_and_box2(acts, horizon_suffix="two")
        acts = _finish_v52(acts, "two W-2s, box 2 withholding summed on line 25a")
        pubs, blocked = _run_v52(acts, "demo.roaot1.w2box2.two")
        self.assertEqual(_value(pubs, LINE25A), Decimal("3200"))
        self.assertEqual(_missing_names(blocked, "form1040-line25a"), [])

    def test_w2_plus_1099int_box4_feeds_25a_25b_25d(self) -> None:
        acts = _withholding_base()
        _add_w2_box2(acts, employer="demo.roaot1.w2c.employer", slip="demo.roaot1.w2c.slip", amount=4500.0)
        _close_w2_box1_and_box2(acts, horizon_suffix="c")

        def add(kind: str, payload: dict[str, object]) -> None:
            acts.append(_act(len(acts), kind, payload))

        add("bundle-adoption", {"bundle": _load("f1099int-box4.bundle.json")})
        payer, stmt = "demo.roaot1.int.payer", "demo.roaot1.int.stmt"
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": payer, "kind": "tax.us.interest-payer", "label": "Synthetic interest payer"}})
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": stmt, "kind": "tax.us.1099int-statement", "label": "Synthetic 1099-INT"}})
        add("assertion", {"finding": _attested("demo.roaot1.int.box4", f"tax.us.2025.f1099int.box4-withholding|payer={payer},statement={stmt},tax-year=2025", 150.0)})
        _close_empty(acts, family="tax.us.2025.f1099int.b4", version="v1", closure_fact="tax.us.2025.f1099int.b4.source-closure", horizon="demo.roaot1.intb4.h0")
        _close_other_box4_families(acts, skip={"w2-box2", "f1099int-b4"})

        acts = _finish_v52(acts, "W-2 box 2 and 1099-INT box 4 reach 25a, 25b, and 25d")
        pubs, blocked = _run_v52(acts, "demo.roaot1.int.one")
        self.assertEqual(_value(pubs, LINE25A), Decimal("4500"))
        self.assertEqual(_value(pubs, LINE25B), Decimal("150"))
        self.assertEqual(_value(pubs, LINE25C), Decimal("0"))
        self.assertEqual(_value(pubs, LINE25D), Decimal("4650"))
        self.assertEqual(_missing_names(blocked, "form1040-line25d"), [])

    def test_1099k_box4_recorded_and_summed_nowhere_is_a_parked_stop_condition(self) -> None:
        """Documents the Track 1 stop condition (rule.form1040-line25b.json's
        own notes): Form 1099-K box 4 is already recorded
        (tax.us.2025.f1099k.box4-federal-withholding) but has no family of
        its own on line 25b. A new source family naming that already-
        published fact type as its member_predicate would retroactively
        require member-transition for every existing plain-assertion use
        of it (packages/kernel/findings.py SC-R1,
        registry.family_member_predicates is loaded from the whole content
        corpus, unscoped by package version), breaking existing tests on
        main; reusing the box-1a family's own closure to publish a second
        subtotal is independently forbidden by ADR-0016. Parked for the
        owner -- not built this track."""
        self.assertNotIn(
            "tax.us.2025.f1099k.box4-withholding-subtotal",
            _load("rule.form1040-line25b.json")["requires"],
        )

    def test_1099div_box4_feeds_line25b(self) -> None:
        acts = _withholding_base()

        def add(kind: str, payload: dict[str, object]) -> None:
            acts.append(_act(len(acts), kind, payload))

        add("bundle-adoption", {"bundle": _load("f1099div-box4.bundle.json")})
        payer, stmt = "demo.roaot1.div.payer", "demo.roaot1.div.stmt"
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": payer, "kind": "tax.us.dividend-payer", "label": "Synthetic dividend payer"}})
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": stmt, "kind": "tax.us.1099div-statement", "label": "Synthetic 1099-DIV"}})
        add("assertion", {"finding": _attested("demo.roaot1.div.box4", f"tax.us.2025.f1099div.box4-withholding|payer={payer},statement={stmt},tax-year=2025", 75.0)})
        _close_empty(acts, family="tax.us.2025.f1099div.b4", version="v1", closure_fact="tax.us.2025.f1099div.b4.source-closure", horizon="demo.roaot1.divb4.h0")
        _close_other_box4_families(acts, skip={"f1099div-b4"})

        acts = _finish_v52(acts, "1099-DIV box 4 feeds line 25b")
        pubs, blocked = _run_v52(acts, "demo.roaot1.div.one")
        self.assertEqual(_value(pubs, LINE25B), Decimal("75"))
        self.assertEqual(_value(pubs, LINE25D), Decimal("75"))
        self.assertEqual(_missing_names(blocked, "form1040-line25d"), [])

    def test_1099r_box4_feeds_line25b(self) -> None:
        acts = _withholding_base()

        def add(kind: str, payload: dict[str, object]) -> None:
            acts.append(_act(len(acts), kind, payload))

        add("bundle-adoption", {"bundle": _load("f1099r-ira.bundle.v3.json")})
        payer, stmt = "demo.roaot1.ira.payer", "demo.roaot1.ira.stmt"
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": payer, "kind": "tax.us.ira-payer", "label": "Synthetic IRA payer"}})
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": stmt, "kind": "tax.us.1099r-statement", "label": "Synthetic 1099-R"}})
        suffix = f"payer={payer},statement={stmt},tax-year=2025"
        add("assertion", {"finding": _attested("demo.roaot1.ira.box2a", f"tax.us.2025.f1099r.ira-box2a-taxable-amount|{suffix}", 500.0)})
        add("assertion", {"finding": _attested("demo.roaot1.ira.checkbox", f"tax.us.2025.f1099r.ira-sep-simple-checkbox|{suffix}", True)})
        add("assertion", {"finding": _attested("demo.roaot1.ira.code", f"tax.us.2025.f1099r.distribution-code|{suffix}", "7")})
        add("assertion", {"finding": _attested("demo.roaot1.ira.box2b", f"tax.us.2025.f1099r.box2b-not-determined|{suffix}", False)})
        add("assertion", {"finding": _attested("demo.roaot1.ira.box1", f"tax.us.2025.f1099r.ira-box1-taxable-distribution|{suffix}", 500.0)})
        add("assertion", {"finding": _attested("demo.roaot1.ira.box4", f"tax.us.2025.f1099r.ira-box4-withholding|{suffix}", 60.0)})
        _close_empty(acts, family="tax.us.2025.f1099r.box4", version="v1", closure_fact="tax.us.2025.f1099r.box4.source-closure", horizon="demo.roaot1.irab4r.h0")
        _close_other_box4_families(acts, skip={"f1099r-b4"})

        acts = _finish_v52(acts, "1099-R box 4 feeds line 25b")
        pubs, blocked = _run_v52(acts, "demo.roaot1.ira.one")
        self.assertEqual(_value(pubs, LINE25B), Decimal("60"))
        self.assertEqual(_missing_names(blocked, "form1040-line25b"), [])

    def test_line25c_is_always_zero(self) -> None:
        acts = _withholding_base()
        acts = _finish_v52(acts, "line 25c has no route and is always zero")
        pubs, blocked = _run_v52(acts, "demo.roaot1.25c")
        self.assertEqual(_value(pubs, LINE25C), Decimal("0"))
        self.assertEqual(_missing_names(blocked, "form1040-line25c"), [])

    def test_one_w2_box1_no_box2_blocks_naming_the_fact(self) -> None:
        """Repair round 1: line 25a v2 requires the current box-2 count to
        equal the current box-1 count. One real W-2 (box 1) with the box-2
        family closed empty (zero box-2 answers) is a count mismatch (1 vs
        0); line 25a blocks DEPENDENCY_ABSENT naming
        tax.us.2025.w2.box2-withholding, never a silent zero."""
        acts = _income_acts(wages=50000.0)

        def add(kind: str, payload: dict[str, object]) -> None:
            acts.append(_act(len(acts), kind, payload))

        add("bundle-adoption", {"bundle": _load("w2-box2.bundle.json")})
        _close_empty(acts, family="tax.us.2025.w2-box2", version="v1", closure_fact="tax.us.2025.w2-box2.source-closure", horizon="demo.roaot1.w2box2missing.h0")
        acts = _finish_v52(acts, "one W-2 (box 1), zero box-2 answers")
        pubs, blocked = _run_v52(acts, "demo.roaot1.missingbox2.one")
        self.assertNotIn(LINE25A, pubs)
        self.assertIn("tax.us.2025.w2.box2-withholding", _missing_names(blocked, "form1040-line25a"))

    def _reopen_w2_with_second_slip(self, acts: list[dict[str, object]], *, amount: float) -> list[dict[str, object]]:
        acts = copy.deepcopy(acts)
        old_closure_prefix = "tax.us.2025.w2.source-closure|family-horizon=demo.cgd.t2.w2.h1,"
        kept: list[dict[str, object]] = []
        for act in acts:
            if act.get("kind") == "assertion":
                payload = cast(dict[str, Any], act.get("payload", {}))
                finding = cast(dict[str, Any], payload.get("finding", {}))
                if str(finding.get("fact_id", "")).startswith(old_closure_prefix):
                    continue
            kept.append(act)
        acts = kept

        def add(kind: str, payload: dict[str, object]) -> None:
            acts.append(_act(len(acts), kind, payload))

        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.roaot1.w2second.employer", "kind": "tax.us.employer", "label": "Synthetic second employer"}})
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.roaot1.w2second.slip", "kind": "tax.us.w2-slip", "label": "Synthetic second W-2 slip"}})
        add("member-transition", {
            "family": {"id": "tax.us.2025.w2", "version": "v2"},
            "scope": SCOPE_KEY,
            "member": {"action": "assert", "finding": _attested("demo.roaot1.w2second.wages", "tax.us.2025.w2.box1-wages|employer=demo.roaot1.w2second.employer,w2-slip=demo.roaot1.w2second.slip,tax-year=2025", amount)},
            "successor": {"id": "demo.roaot1.w2.h2", "predecessor": "demo.cgd.t2.w2.h1"},
        })
        add("assertion", {"finding": _attested("demo.roaot1.w2.reclose", "tax.us.2025.w2.source-closure|family-horizon=demo.roaot1.w2.h2,tax-year=2025", True)})
        return acts

    def test_two_w2s_box2_for_only_one_blocks_naming_the_fact(self) -> None:
        acts = _income_acts(wages=50000.0)
        acts = self._reopen_w2_with_second_slip(acts, amount=20000.0)

        def add(kind: str, payload: dict[str, object]) -> None:
            acts.append(_act(len(acts), kind, payload))

        add("bundle-adoption", {"bundle": _load("w2-box2.bundle.json")})
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.roaot1.w2first.employer", "kind": "tax.us.employer", "label": "Synthetic first employer alias"}})
        add("assertion", {"finding": _attested("demo.roaot1.box2.only1", "tax.us.2025.w2.box2-withholding|employer=demo.cgd.t2.employer,w2-slip=demo.cgd.t2.w2,tax-year=2025", 4500.0)})
        _close_empty(acts, family="tax.us.2025.w2-box2", version="v1", closure_fact="tax.us.2025.w2-box2.source-closure", horizon="demo.roaot1.w2box2only1.h0")
        acts = _finish_v52(acts, "two W-2s, box 2 answered for only one")
        pubs, blocked = _run_v52(acts, "demo.roaot1.missingbox2.two")
        self.assertNotIn(LINE25A, pubs)
        self.assertIn("tax.us.2025.w2.box2-withholding", _missing_names(blocked, "form1040-line25a"))

    def test_box2_answered_zero_computes_zero(self) -> None:
        acts = _income_acts(wages=50000.0)

        def add(kind: str, payload: dict[str, object]) -> None:
            acts.append(_act(len(acts), kind, payload))

        add("bundle-adoption", {"bundle": _load("w2-box2.bundle.json")})
        add("assertion", {"finding": _attested("demo.roaot1.box2.zero", "tax.us.2025.w2.box2-withholding|employer=demo.cgd.t2.employer,w2-slip=demo.cgd.t2.w2,tax-year=2025", 0.0)})
        _close_empty(acts, family="tax.us.2025.w2-box2", version="v1", closure_fact="tax.us.2025.w2-box2.source-closure", horizon="demo.roaot1.w2box2zero.h0")
        acts = _finish_v52(acts, "box 2 answered $0 -- a valid answer, not an absence")
        pubs, blocked = _run_v52(acts, "demo.roaot1.box2zero")
        self.assertEqual(_value(pubs, LINE25A), Decimal("0"))
        self.assertEqual(_missing_names(blocked, "form1040-line25a"), [])


if __name__ == "__main__":
    unittest.main()
