"""Track 1: the published single-producer SSA no-activity contract.

Promotes the reopened Track 0 prototype's ten obligations, nine matrix rows
and six mutation kill-tests onto the **real** published surface: ``rule.ss-
benefits-worksheet`` v2 under ``rule-artifact.v4``, the sole producer of
``tax.us.2025.social-security.line6b``, admitted by ``package.core-
calculations`` v30 / ``published-packages`` v25 / release v23 / the
``adopt-core-v30-current`` fixture. See
``docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md``
(``## Amended Track 1 charter``) for the contract and
``tools/generate_ssa_no_activity_content.py`` for the generator that produced
these citizens.

The candidate under measurement:

* one successor rule, ``tax.us.2025.rule.ss-benefits-worksheet`` v2, the
  **sole** producer of ``tax.us.2025.social-security.line6b`` (the
  presentation join is untouched);
* unconditional ``requires``: line 6a, ``rounding.convention``,
  ``no-rrb-or-foreign-social-benefit``, ``filing_status``, and the seven
  numeric worksheet inputs;
* an ADR-0037 ``conditional_dependency_set`` over the 22 worksheet-only
  declarations, active only when ``count(box5) > 0``;
* an unconditional ``require_closed`` over the SSA-1099 benefits family;
* a value-level ``choose`` selecting canonical ``0`` or the unchanged v1
  worksheet expression.

Closure is required on both routes because line 6b must not publish until the
current SSA-1099 source family is confirmed complete — not because of any
limitation of ``count``.  ``test_the_closure_relation_is_carried_by_count_not_
by_require_closed`` measures that the relation travels via ``count``, not
``require_closed``; it is not the semantic justification.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import package_instance_checksum
from packages.derivation.production_resolver import PublicationSurface
from packages.tax.loader import TAX_CONTENT_DIR
from tests.test_form1099g_box1_schedule1_line7 import (
    _act,
    _attested,
    _disposition,
    _published_numeric,
)
from tests.test_ssa1099_benefits_line6_track2 import (
    BOX3,
    BOX4,
    BOX5,
    BOX6,
    CLOSURE,
    FAMILY,
    KIND,
    LUMP,
    RECIPIENT,
    SCOPE_KEY,
    SCOPE_TOKENS,
    _renumber,
    _run as ratified_run,
    _ssa_acts,
)
from tools.generate_ssa_no_activity_content import _bytes, _citizen_checksum, build_release

ROOT = Path(__file__).resolve().parent.parent
CONTENT = TAX_CONTENT_DIR
FIXTURES = ROOT / "packages" / "sample_data" / "ssa1099_benefits_line6"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2025"}

WORKSHEET_RULE = "tax.us.2025.rule.ss-benefits-worksheet"
WORKSHEET_FILE = "rule.ss-benefits-worksheet.v2.json"
WORKSHEET_VERSION = "v2"
PACKAGE_FILE = "package.core-calculations.v30.json"
REGISTRY_FILE = "published-packages.v25.json"
RELEASE_FILE = "demo.release.2025.v23.json"
ADOPTION_FILE = "adopt-core-v30-current.json"
LINE6B = "tax.us.2025.social-security.line6b"
NO_RRB_TOKEN = "no-rrb-or-foreign-social-benefit"
NO_RRB = f"tax.us.2025.ss-benefits-scope.{NO_RRB_TOKEN}"
WORKSHEET_ONLY_TOKENS = tuple(t for t in SCOPE_TOKENS if t != NO_RRB_TOKEN)
CLOSURE_MAPPING = "tax.us.2025.closure-mapping.ssa1099-benefits"
CLOSURE_FINDING = "demo.ssa.closure"
RETAINED_FINDING = f"demo.ssa.scope.{NO_RRB_TOKEN}"

# The seven numeric worksheet inputs plus line 6a: the symbols whose published
# findings a nonempty line-6b result must pin.
WORKSHEET_DEPENDENCY_SYMBOLS = (
    "tax.us.2025.wages.total-w2-box1",
    "tax.us.2025.interest.taxable-total",
    "tax.us.2025.dividends.ordinary-total",
    "tax.us.2025.ira.distributions.line4b",
    "tax.us.2025.capital-gains.line7a-total",
    "tax.us.2025.income.additional-income",
    "tax.us.2025.tax-exempt-interest.line2a-total",
    "tax.us.2025.social-security.line6a",
)

# The eight no-default line2a-scope declarations rule.form1040-line2a.v3
# requires to publish tax-exempt-interest.line2a-total.
LINE2A_SCOPE_TOKENS = (
    "no-f1099int-tax-exempt",
    "no-f1099oid-tax-exempt",
    "no-unreported-tax-exempt",
    "no-premium-adjustment",
    "no-child-income-election",
    "no-amt-form-6251",
    "no-credit-using-tax-exempt",
    "no-deduction-using-tax-exempt",
)
LINE2A_TOTAL = "tax.us.2025.tax-exempt-interest.line2a-total"


def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))


def _load_current_adoption() -> dict[str, object]:
    return cast(
        dict[str, object],
        json.loads((FIXTURES / "adoptions" / ADOPTION_FILE).read_text("utf-8")),
    )


def _real_surface() -> PublicationSurface:
    """The real published v30 chain, read directly from the repo tree."""
    return PublicationSurface(
        FIXTURES / "publication_surface" / "releases",
        CONTENT / REGISTRY_FILE,
        CONTENT,
    )


def _asserts_fact_type(act: dict[str, Any], fact_type_ids: set[str]) -> bool:
    payload = cast(dict[str, Any], act.get("payload", {}))
    finding = cast(dict[str, Any], payload.get("finding", {}))
    fact_id = str(finding.get("fact_id", ""))
    return any(fact_id.startswith(f"{t}|") for t in fact_type_ids)


def build_acts(
    *,
    drop_tokens: tuple[str, ...] = (),
    drop_fact_types: tuple[str, ...] = (),
    extra: list[dict[str, object]] | None = None,
    **kwargs: Any,
) -> list[dict[str, object]]:
    """Production-shaped acts adopting the published v30 package.

    ``drop_tokens`` removes an ``ss-benefits-scope`` declaration's assertion
    act outright — the only way to measure "genuinely absent" rather than
    "answered no". ``drop_fact_types`` does the same for any other
    fully-qualified fact type id (e.g. the ``line2a-scope`` family, which
    lives outside the ``ss-benefits-scope`` vocabulary).
    """
    acts = _ssa_acts(**kwargs)
    acts.pop()  # the v28 fixture adoption
    drop_ids = set(drop_fact_types)
    if drop_tokens:
        drop_ids |= {f"tax.us.2025.ss-benefits-scope.{t}" for t in drop_tokens}
    if drop_ids:
        acts = [a for a in acts if not _asserts_fact_type(cast(dict[str, Any], a), drop_ids)]
    for act in extra or []:
        acts.append(act)
    adoption = _load_current_adoption()
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return _renumber(acts)


def execute(
    acts: list[dict[str, object]], run_id: str, *, surface: PublicationSurface | None = None
) -> tuple[dict[str, Any], dict[str, Any] | None, str | None]:
    subject_surface = surface or _real_surface()
    with TemporaryDirectory() as tmp:
        result = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=subject_surface,
            output_name="out.json",
        )
        if result.refusal is not None:
            return {}, None, str(result.refusal)
        assert result.output_path is not None and result.presentation_path is not None
        return (
            json.loads(result.output_path.read_text("utf-8")),
            json.loads(result.presentation_path.read_text("utf-8")),
            None,
        )


_RUNS: dict[str, tuple[dict[str, Any], dict[str, Any] | None, str | None]] = {}


def run_case(name: str, **kwargs: Any) -> tuple[dict[str, Any], dict[str, Any] | None, str | None]:
    """Execute one matrix row once per process; every obligation shares it."""
    if name not in _RUNS:
        _RUNS[name] = execute(build_acts(**kwargs), f"track1.{name}")
    return _RUNS[name]


def worksheet_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        row
        for row in report.get("dispositions", [])
        if row.get("artifact_id") == WORKSHEET_RULE
    ]


def line6b_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    """Every disposition row the presentation join would see for line 6b.

    ``presentation_projection`` groups by the producing rule's published
    symbol, so a second producer — published, conflict-loser, false-guard or
    blocked — shows up here as a second row.  Counting these is the direct
    measurement of the one-disposition-row invariant.
    """
    return [
        row
        for row in report.get("dispositions", [])
        if row.get("symbol") == LINE6B or row.get("artifact_id") == WORKSHEET_RULE
    ]


def pin_ids(row: dict[str, Any], role: str | None = None) -> set[str]:
    return {p["id"] for p in row.get("pins", []) if role is None or p["role"] == role}


def published_finding(report: dict[str, Any], symbol: str) -> str | None:
    for row in report.get("dispositions", []):
        if row.get("symbol") == symbol and row.get("disposition") == "published":
            return cast(str, row["finding_id"])
    return None


# --- mutation surface (kill-tests only) --------------------------------------


class MutantSurface:
    """A private copy of the real v30 chain with a mutated worksheet rule.

    Never touches the repo tree.  Re-seals the package registry entry, the
    release digest and the adoption checksums so a mutation is measured
    through the same resolver-authenticity gate the unmutated candidate
    passes, exactly as ``package_validation``/``production_resolver`` require.
    """

    def __init__(self, root: Path) -> None:
        self.root = root
        self.members = root / "members"
        self.releases = root / "releases"
        self.members.mkdir(parents=True)
        self.releases.mkdir(parents=True)
        for source in CONTENT.glob("*.json"):
            shutil.copyfile(source, self.members / source.name)
        release_source = FIXTURES / "publication_surface" / "releases" / RELEASE_FILE
        shutil.copyfile(release_source, self.releases / RELEASE_FILE)
        self.adoption = _load_current_adoption()
        self.surface = PublicationSurface(self.releases, self.members / REGISTRY_FILE, self.members)

    def rule(self) -> dict[str, Any]:
        return cast(dict[str, Any], json.loads((self.members / WORKSHEET_FILE).read_text("utf-8")))

    def mutate_rule(self, mutated: dict[str, Any]) -> None:
        (self.members / WORKSHEET_FILE).write_bytes(_bytes(mutated))
        package = json.loads((self.members / PACKAGE_FILE).read_text("utf-8"))
        package["package_checksum"] = package_instance_checksum(package)
        (self.members / PACKAGE_FILE).write_bytes(_bytes(package))

        registry = json.loads((self.members / REGISTRY_FILE).read_text("utf-8"))
        for entry in registry["citizens"]:
            if entry["id"] == WORKSHEET_RULE and entry["version"] == mutated["version"]:
                entry["checksum"] = _citizen_checksum(mutated)
        for entry in registry["packages"]:
            if entry["id"] == package["id"] and entry["version"] == package["version"]:
                entry["checksum"] = package["package_checksum"]
        registry_bytes = _bytes(registry)
        (self.members / REGISTRY_FILE).write_bytes(registry_bytes)

        release_bytes = _bytes(build_release(registry_bytes))
        (self.releases / RELEASE_FILE).write_bytes(release_bytes)

        payload = cast(dict[str, Any], self.adoption["payload"])
        payload["package"]["checksum"] = package["package_checksum"]
        payload["release"]["checksum"] = hashlib.sha256(release_bytes).hexdigest()


def build_mutant_acts(
    subject: MutantSurface, *, drop_tokens: tuple[str, ...] = (), **kwargs: Any
) -> list[dict[str, object]]:
    acts = _ssa_acts(**kwargs)
    acts.pop()
    if drop_tokens:
        drop_ids = {f"tax.us.2025.ss-benefits-scope.{t}" for t in drop_tokens}
        acts = [a for a in acts if not _asserts_fact_type(cast(dict[str, Any], a), drop_ids)]
    adoption = json.loads(json.dumps(subject.adoption))
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return _renumber(acts)


# --- matrix rows --------------------------------------------------------
#
# Each entry is (row label, run name, kwargs).  Obligation 9 walks all of them;
# the per-obligation tests reuse the same cached runs.
CLOSED_EMPTY: dict[str, Any] = dict(benefits=[], ira_amounts=[], wages=15000, close=True)
CLOSED_NONEMPTY: dict[str, Any] = dict(
    benefits=[(12000.0, 0.0, 12000.0)], ira_amounts=[], wages=90000, close=True
)

MATRIX: tuple[tuple[str, str, dict[str, Any]], ...] = (
    ("1 closed empty, R=yes, 22 absent", "closed-empty-declarations-absent",
     dict(drop_tokens=WORKSHEET_ONLY_TOKENS, **CLOSED_EMPTY)),
    ("1b closed empty, all 23 present", "closed-empty-declarations-present", dict(CLOSED_EMPTY)),
    ("2 unclosed empty", "unclosed-empty",
     dict(drop_tokens=WORKSHEET_ONLY_TOKENS, benefits=[], ira_amounts=[], wages=15000, close=False)),
    ("3 unclosed nonempty", "unclosed-nonempty",
     dict(benefits=[(12000.0, 0.0, 12000.0)], ira_amounts=[], wages=90000, close=False)),
    ("4 closed nonempty", "closed-nonempty", dict(CLOSED_NONEMPTY)),
    ("5 closed nonempty, 4 declarations absent", "closed-nonempty-declarations-absent",
     dict(drop_tokens=("no-form-2555", "no-form-4563", "no-sch1-line13-hsa", "no-lump-sum-election"),
          **CLOSED_NONEMPTY)),
    ("6 R=no, closed empty", "closed-empty-retained-no",
     dict(drop_tokens=WORKSHEET_ONLY_TOKENS, scope={NO_RRB_TOKEN: "no"}, **CLOSED_EMPTY)),
    ("6b R=no, closed nonempty", "closed-nonempty-retained-no",
     dict(scope={NO_RRB_TOKEN: "no"}, **CLOSED_NONEMPTY)),
    ("9 R absent, closed empty", "closed-empty-retained-absent",
     dict(drop_tokens=SCOPE_TOKENS, **CLOSED_EMPTY)),
)


class TestObligation1And2ClosedEmptyZero(unittest.TestCase):
    """Obligations 1 and 2: the closed-empty zero and exactly what backs it."""

    def test_closed_empty_publishes_zero_with_declarations_genuinely_absent(self) -> None:
        acts = build_acts(drop_tokens=WORKSHEET_ONLY_TOKENS, **CLOSED_EMPTY)
        asserted = {
            str(cast(dict[str, Any], cast(dict[str, Any], a.get("payload", {})).get("finding", {})).get("fact_id", ""))
            for a in acts
        }
        for token in WORKSHEET_ONLY_TOKENS:
            fact_type = f"tax.us.2025.ss-benefits-scope.{token}"
            self.assertFalse(
                any(fact_id.startswith(f"{fact_type}|") for fact_id in asserted),
                f"{token} was still asserted; the run would not measure absence",
            )
        report, model, refusal = run_case(
            "closed-empty-declarations-absent", drop_tokens=WORKSHEET_ONLY_TOKENS, **CLOSED_EMPTY
        )
        self.assertIsNone(refusal)
        assert model is not None
        rows = worksheet_rows(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "published")
        self.assertEqual(_published_numeric(model, "line-6b"), 0)
        self.assertEqual(_disposition(model, "line-6b"), "computed_zero")

    def test_the_zero_pins_closure_family_mapping_adoption_citations_and_R_only(self) -> None:
        report, _model, _refusal = run_case(
            "closed-empty-declarations-absent", drop_tokens=WORKSHEET_ONLY_TOKENS, **CLOSED_EMPTY
        )
        row = worksheet_rows(report)[0]
        self.assertEqual(pin_ids(row, "input"), {CLOSURE_FINDING, RETAINED_FINDING})
        self.assertEqual(pin_ids(row, "package"), {CLOSURE_MAPPING, FAMILY})
        self.assertEqual(
            pin_ids(row, "citation"),
            {
                "tax.us.2025.citation.form1040.ss-benefits-worksheet",
                "tax.us.2025.citation.form1040.line-6b",
            },
        )
        self.assertEqual(pin_ids(row, "adoption"), {"tax.us.2025.package.core-calculations"})
        for token in WORKSHEET_ONLY_TOKENS:
            self.assertNotIn(f"demo.ssa.scope.{token}", pin_ids(row))


class TestObligation3NonemptyValue(unittest.TestCase):
    """Obligation 3: the nonempty value is the ratified route's, computed."""

    CASES: tuple[tuple[str, dict[str, Any]], ...] = (
        ("high-wage", dict(benefits=[(12000.0, 0.0, 12000.0)], ira_amounts=[], wages=90000)),
        ("below-threshold", dict(benefits=[(10000.0, 0.0, 10000.0)], ira_amounts=[], wages=10000)),
        ("interest", dict(benefits=[(30000.0, 0.0, 30000.0)], ira_amounts=[], wages=40000,
                          interest=1234.56)),
        ("ira-and-tax-exempt", dict(benefits=[(18000.0, 0.0, 18000.0)], ira_amounts=[5000.0],
                                    wages=25000, tax_exempt=3000.0)),
        ("mfs-lived-apart", dict(benefits=[(20000.0, 0.0, 20000.0)], ira_amounts=[], wages=30000,
                                 filing_status="married_filing_separately",
                                 mfs_lived_apart="yes")),
        ("two-statements", dict(benefits=[(9000.0, 0.0, 9000.0), (7000.0, 0.0, 7000.0)],
                                ira_amounts=[], wages=55000, ordinary_dividends=2000.0)),
        ("eighty-five-cap", dict(benefits=[(40000.0, 0.0, 40000.0)], ira_amounts=[], wages=200000)),
    )

    def test_candidate_value_equals_ratified_route_value(self) -> None:
        """Both routes are *run*; neither expression is inspected."""
        for label, case in self.CASES:
            with self.subTest(label):
                _report, model, refusal = execute(
                    build_acts(close=True, **case), f"track1.value.{label}"
                )
                self.assertIsNone(refusal)
                assert model is not None
                _ratified_report, ratified_model = ratified_run(
                    _renumber(_ssa_acts(close=True, **case)), run_id=f"ratified.value.{label}"
                )
                candidate_value = _published_numeric(model, "line-6b")
                ratified_value = _published_numeric(ratified_model, "line-6b")
                self.assertEqual(repr(candidate_value), repr(ratified_value))
                self.assertEqual(
                    _disposition(model, "line-6b"), _disposition(ratified_model, "line-6b")
                )


class TestObligation4NonemptyProvenance(unittest.TestCase):
    """Obligation 4: the nonempty result pins every active dependency."""

    def test_pins_every_active_worksheet_dependency_and_the_closure_triple(self) -> None:
        report, _model, refusal = run_case("closed-nonempty", **CLOSED_NONEMPTY)
        self.assertIsNone(refusal)
        row = worksheet_rows(report)[0]
        self.assertEqual(row["disposition"], "published")
        pins = pin_ids(row)
        for symbol in WORKSHEET_DEPENDENCY_SYMBOLS:
            finding_id = published_finding(report, symbol)
            self.assertIsNotNone(finding_id, symbol)
            self.assertIn(cast(str, finding_id), pins, symbol)
        for token in SCOPE_TOKENS:
            self.assertIn(f"demo.ssa.scope.{token}", pins, token)
        self.assertLessEqual({CLOSURE_FINDING, FAMILY, CLOSURE_MAPPING}, pins)


class TestObligation5CompleteMissingList(unittest.TestCase):
    """Obligation 5: one walk names every absent conditional member."""

    ABSENT = ("no-form-2555", "no-form-4563", "no-sch1-line13-hsa", "no-lump-sum-election")

    def test_all_absent_conditional_members_are_named_at_once(self) -> None:
        report, model, refusal = run_case(
            "closed-nonempty-declarations-absent", drop_tokens=self.ABSENT, **CLOSED_NONEMPTY
        )
        self.assertIsNone(refusal)
        assert model is not None
        rows = worksheet_rows(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(
            sorted(rows[0]["missing"]),
            sorted(f"tax.us.2025.ss-benefits-scope.{t}" for t in self.ABSENT),
        )


class TestObligation6UnclosedBlocks(unittest.TestCase):
    """Obligation 6: neither unclosed route publishes anything."""

    def test_unclosed_empty_blocks(self) -> None:
        report, model, refusal = run_case(
            "unclosed-empty", drop_tokens=WORKSHEET_ONLY_TOKENS,
            benefits=[], ira_amounts=[], wages=15000, close=False,
        )
        self.assertIsNone(refusal)
        assert model is not None
        rows = worksheet_rows(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(_disposition(model, "line-6b"), "blocked")

    def test_unclosed_nonempty_blocks_on_closure_not_on_a_missing_symbol(self) -> None:
        report, model, refusal = run_case(
            "unclosed-nonempty",
            benefits=[(12000.0, 0.0, 12000.0)], ira_amounts=[], wages=90000, close=False,
        )
        self.assertIsNone(refusal)
        assert model is not None
        rows = worksheet_rows(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(rows[0]["missing"], [FAMILY])
        self.assertEqual(_disposition(model, "line-6b"), "blocked")


class TestObligation7RetainedDeclaration(unittest.TestCase):
    """Obligation 7: a negative or absent R cannot reach the zero branch."""

    def test_R_no_cannot_take_the_zero_branch(self) -> None:
        report, model, refusal = run_case(
            "closed-empty-retained-no", drop_tokens=WORKSHEET_ONLY_TOKENS,
            scope={NO_RRB_TOKEN: "no"}, **CLOSED_EMPTY,
        )
        self.assertIsNone(refusal)
        assert model is not None
        rows = worksheet_rows(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "inapplicable")
        self.assertIs(rows[0]["guard_result"], False)
        self.assertEqual(_disposition(model, "line-6b"), "guard_inapplicable")

    def test_R_no_also_stops_the_nonempty_route(self) -> None:
        report, _model, refusal = run_case(
            "closed-nonempty-retained-no", scope={NO_RRB_TOKEN: "no"}, **CLOSED_NONEMPTY
        )
        self.assertIsNone(refusal)
        rows = worksheet_rows(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "inapplicable")

    def test_R_absent_blocks_naming_only_R(self) -> None:
        """The 22 stay silent: an inactive conditional member is not missing."""
        report, model, refusal = run_case(
            "closed-empty-retained-absent", drop_tokens=SCOPE_TOKENS, **CLOSED_EMPTY
        )
        self.assertIsNone(refusal)
        assert model is not None
        rows = worksheet_rows(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["missing"], [NO_RRB])
        self.assertEqual(_disposition(model, "line-6b"), "blocked")


class TestObligation8LateMemberAndReclosure(unittest.TestCase):
    """Obligation 8: ADR-0017 decision 7 across the candidate's two routes."""

    STATEMENT = "demo.ssa.statement.late"

    def _late_member_acts(self) -> list[dict[str, object]]:
        extra: list[dict[str, object]] = [
            _act(0, "entity-introduced", {
                "entity": {
                    "schema": "entity.v1",
                    "id": self.STATEMENT,
                    "kind": "tax.us.ssa1099-statement",
                    "label": "Late synthetic Form SSA-1099",
                }
            })
        ]
        for fact_type, value, suffix in (
            (BOX3, 4000.0, "box3"),
            (BOX4, 0.0, "box4"),
            (BOX6, 0, "box6"),
            (RECIPIENT, "taxpayer", "recipient"),
            (KIND, "ssa-1099", "kind"),
            (LUMP, False, "lump"),
        ):
            extra.append(_act(0, "assertion", {
                "finding": _attested(
                    f"demo.ssa.finding.{suffix}.late",
                    f"{fact_type}|statement={self.STATEMENT},tax-year=2025",
                    value,
                )
            }))
        extra.append(_act(0, "member-transition", {
            "family": {"id": FAMILY, "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {
                "action": "assert",
                "finding": _attested(
                    "demo.ssa.finding.box5.late",
                    f"{BOX5}|statement={self.STATEMENT},tax-year=2025",
                    4000.0,
                ),
            },
            "successor": {"id": "demo.ssa.h.late", "predecessor": "demo.ssa.h0"},
        }))
        return extra

    def test_late_member_displaces_the_zero_and_reclosure_recomputes(self) -> None:
        base = dict(drop_tokens=WORKSHEET_ONLY_TOKENS, **CLOSED_EMPTY)

        report1, model1, refusal1 = run_case("closed-empty-declarations-absent", **base)
        self.assertIsNone(refusal1)
        assert model1 is not None
        self.assertEqual(worksheet_rows(report1)[0]["disposition"], "published")
        self.assertEqual(_published_numeric(model1, "line-6b"), 0)

        # Step 2: a late member arrives on horizon successor h.late, which
        # displaces the h0 closure finding.  The closure-backed zero is gone
        # and the candidate blocks rather than substituting a stale authority.
        late = self._late_member_acts()
        report2, model2, refusal2 = execute(
            build_acts(extra=late, **base), "track1.late.member"
        )
        self.assertIsNone(refusal2)
        assert model2 is not None
        rows2 = worksheet_rows(report2)
        self.assertEqual(len(rows2), 1)
        self.assertEqual(rows2[0]["disposition"], "blocked")
        self.assertEqual(rows2[0]["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(_disposition(model2, "line-6b"), "blocked")

        # Step 3: reclose on the current horizon.  The family is nonempty now,
        # so the 22 conditional members activate and are genuinely absent —
        # the rule must say so rather than fall back to the zero branch.
        reclosed = list(late)
        reclosed.append(_act(0, "assertion", {
            "finding": _attested(
                "demo.ssa.closure.late",
                f"{CLOSURE}|family-horizon=demo.ssa.h.late,tax-year=2025",
                True,
            )
        }))
        report3, model3, refusal3 = execute(
            build_acts(extra=reclosed, **base), "track1.late.reclosed-absent"
        )
        self.assertIsNone(refusal3)
        assert model3 is not None
        rows3 = worksheet_rows(report3)
        self.assertEqual(len(rows3), 1)
        self.assertEqual(rows3[0]["disposition"], "blocked")
        self.assertEqual(
            sorted(rows3[0]["missing"]),
            sorted(f"tax.us.2025.ss-benefits-scope.{t}" for t in WORKSHEET_ONLY_TOKENS),
        )

        # Step 4: with the declarations answered, reclosure recomputes a real
        # worksheet result on the same lifecycle.  Wages are raised so the
        # recomputation is a nonzero taxable amount rather than a second zero,
        # which would not distinguish "recomputed" from "still the empty zero".
        report4, model4, refusal4 = execute(
            build_acts(extra=reclosed, benefits=[], ira_amounts=[], wages=90000, close=True),
            "track1.late.reclosed-answered",
        )
        self.assertIsNone(refusal4)
        assert model4 is not None
        rows4 = worksheet_rows(report4)
        self.assertEqual(len(rows4), 1)
        self.assertEqual(rows4[0]["disposition"], "published")
        self.assertEqual(_disposition(model4, "line-6b"), "published_value")
        self.assertGreater(_published_numeric(model4, "line-6b"), 0)


class TestObligation9OneRowAndAValidModel(unittest.TestCase):
    """Obligation 9: the non-negotiable one the withdrawn settlement missed."""

    def test_every_matrix_row_yields_one_line6b_row_and_a_valid_model(self) -> None:
        for label, name, kwargs in MATRIX:
            with self.subTest(label):
                report, model, refusal = run_case(name, **kwargs)
                self.assertIsNone(refusal, label)
                self.assertEqual(len(worksheet_rows(report)), 1, label)
                self.assertEqual(len(line6b_rows(report)), 1, label)
                self.assertIsNotNone(model, label)
                assert model is not None
                self.assertEqual(model["schema"], "presentation-model.v1")
                self.assertIsNotNone(_disposition(model, "line-6b"), label)

    def test_the_package_declares_exactly_one_producer_of_line6b(self) -> None:
        package = _load(PACKAGE_FILE)
        self.assertNotIn(
            LINE6B, {c["symbol"] for c in package.get("conflict_semantics", [])}
        )
        producers = [
            member for member in package["members"] if member["id"] == WORKSHEET_RULE
        ]
        self.assertEqual([m["version"] for m in producers], [WORKSHEET_VERSION])


class TestObligation10Mutations(unittest.TestCase):
    """Obligation 10: each load-bearing element is separately killed."""

    def _mutated(self, apply: Any) -> MutantSurface:
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        subject = MutantSurface(Path(tmp.name) / "mutant")
        rule = subject.rule()
        apply(rule)
        subject.mutate_rule(rule)
        return subject

    def _closed_empty(self, subject: MutantSurface, run_id: str) -> tuple[dict[str, Any], str | None]:
        report, _model, refusal = execute(
            build_mutant_acts(subject, drop_tokens=WORKSHEET_ONLY_TOKENS, **CLOSED_EMPTY),
            run_id,
            surface=subject.surface,
        )
        return report, refusal

    def test_mutating_the_family_id_strips_the_zeros_closure_authority(self) -> None:
        """Point the family at another closed family and the zero survives —
        but it is no longer *this* family's zero.  The kill is in provenance,
        not in the number: an unmutated closed-empty zero pins the SSA closure
        finding, the SSA family declaration and the SSA closure mapping, and
        the mutant pins none of them.  Asserting only on the value would have
        passed a mutation that silently re-authorized line 6b from an
        unrelated source family."""
        def apply(rule: dict[str, Any]) -> None:
            body = json.dumps(rule).replace(FAMILY, "tax.us.2025.f1099int.b1")
            rule.clear()
            rule.update(json.loads(body))

        report, refusal = self._closed_empty(self._mutated(apply), "mutant.family")
        self.assertIsNone(refusal)
        pins = pin_ids(worksheet_rows(report)[0])
        self.assertTrue(pins.isdisjoint({CLOSURE_FINDING, FAMILY, CLOSURE_MAPPING}))

    def test_mutating_the_member_predicate_changes_the_nonempty_value(self) -> None:
        """Counting a fact type outside the family makes a real, nonempty
        family look empty: the rule takes the zero branch and publishes 0
        where the ratified route publishes 10200.

        Measured limitation, reported rather than hidden: substituting a
        *same-statement companion* of box 5 — box 3 or box 6 — is **not**
        observable here, because every companion has exactly one finding per
        statement in this corpus and `evaluator.count` does not check its
        `name` against the family's declared member fact type.  This kill test
        therefore holds "counts something in this family", not "counts the
        declared member predicate".
        """
        def apply(rule: dict[str, Any]) -> None:
            body = json.dumps(rule).replace(BOX5, "tax.us.2025.wages.total-w2-box1")
            rule.clear()
            rule.update(json.loads(body))

        subject = self._mutated(apply)
        _report, model, refusal = execute(
            build_mutant_acts(subject, **CLOSED_NONEMPTY), "mutant.predicate", surface=subject.surface
        )
        self.assertIsNone(refusal)
        assert model is not None
        unmutated, unmutated_model, _ = run_case("closed-nonempty", **CLOSED_NONEMPTY)
        assert unmutated_model is not None
        self.assertEqual(_published_numeric(unmutated_model, "line-6b"), 10200)
        self.assertNotEqual(
            _published_numeric(model, "line-6b"),
            _published_numeric(unmutated_model, "line-6b"),
        )

    def test_the_closure_relation_is_carried_by_count_not_by_require_closed(self) -> None:
        """Measured, not assumed: deleting the `require_closed` node alone is
        **not** observable.  `evaluator.count` blocks `SOURCE_SET_UNCLOSED` on
        an unclosed family and records the same closure read, so the closure
        relation survives its own deletion.  The declaration is therefore
        legible rather than load-bearing, and the family kill test above is
        what actually holds the closure relation."""
        def apply(rule: dict[str, Any]) -> None:
            rule["when"]["args"] = [
                arg for arg in rule["when"]["args"] if arg["op"] != "require_closed"
            ]

        subject = self._mutated(apply)
        report, _model, refusal = execute(
            build_mutant_acts(
                subject,
                benefits=[(12000.0, 0.0, 12000.0)], ira_amounts=[], wages=90000, close=False,
            ),
            "mutant.closure",
            surface=subject.surface,
        )
        self.assertIsNone(refusal)
        row = worksheet_rows(report)[0]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "SOURCE_SET_UNCLOSED")

    def test_dropping_the_retained_declaration_lets_R_absent_publish_a_zero(self) -> None:
        def apply(rule: dict[str, Any]) -> None:
            rule["requires"] = [r for r in rule["requires"] if r != NO_RRB]
            rule["when"]["args"] = [
                arg
                for arg in rule["when"]["args"]
                if not (
                    arg["op"] == "categorical_compare"
                    and arg.get("left", {}).get("name") == NO_RRB
                )
            ]

        subject = self._mutated(apply)
        report, _model, refusal = execute(
            build_mutant_acts(subject, drop_tokens=SCOPE_TOKENS, **CLOSED_EMPTY),
            "mutant.retained",
            surface=subject.surface,
        )
        # Unmutated, this state blocks naming R. Mutated it must not.
        if refusal is None:
            row = worksheet_rows(report)[0]
            self.assertNotEqual(
                (row["disposition"], row.get("missing")), ("blocked", [NO_RRB])
            )

    def test_inverting_the_conditional_condition_activates_members_when_empty(self) -> None:
        def apply(rule: dict[str, Any]) -> None:
            for arg in rule["when"]["args"]:
                if arg["op"] == "conditional_dependency_set":
                    arg["condition"]["cmp"] = "gte"

        subject = self._mutated(apply)
        report, refusal = self._closed_empty(subject, "mutant.condition")
        if refusal is None:
            row = worksheet_rows(report)[0]
            self.assertNotEqual(row["disposition"], "published")

    def test_conditionalizing_the_numeric_inputs_breaks_the_nonempty_route(self) -> None:
        """The seven derived numeric inputs must stay in the *unconditional*
        `requires`, and this is the kill test that holds them there on the real
        published citizen.

        `_Run.is_eligible` consults `rule["requires"]` alone; membership in a
        `conditional_dependency_set` is invisible to eligibility sequencing.
        So moving the seven into the conditional set leaves nothing to order
        the worksheet behind the rules that publish them: it becomes eligible
        on the first pass, `_record_blocked` resolves it permanently, and the
        nonempty route can never publish.

        This test measures the mutation against the shipped artifact directly,
        not against a synthetic surface.
        """
        numeric = WORKSHEET_DEPENDENCY_SYMBOLS[:7]

        def apply(rule: dict[str, Any]) -> None:
            rule["requires"] = [r for r in rule["requires"] if r not in numeric]
            for arg in rule["when"]["args"]:
                if arg["op"] == "conditional_dependency_set":
                    arg["members"].extend({"op": "ref", "name": n} for n in numeric)

        subject = self._mutated(apply)
        report, _model, refusal = execute(
            build_mutant_acts(subject, **CLOSED_NONEMPTY),
            "mutant.conditional-numerics",
            surface=subject.surface,
        )
        # Unmutated, this state publishes 10200.  Asserted positively rather
        # than as `if refusal is None`, so the test cannot pass vacuously.
        self.assertIsNone(refusal)
        _unmutated, unmutated_model, _ = run_case("closed-nonempty", **CLOSED_NONEMPTY)
        assert unmutated_model is not None
        self.assertEqual(_published_numeric(unmutated_model, "line-6b"), 10200)

        row = worksheet_rows(report)[0]
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        # Measured: only the inputs still unpublished on the pass the worksheet
        # first became eligible are named — the mistake surfaces as a *race*,
        # not as all seven going missing at once.  That is precisely why it
        # needs a kill test: a partial missing list is easy to misread as an
        # unrelated fixture gap.
        self.assertTrue(set(row["missing"]).issubset(set(numeric)))
        self.assertTrue(set(row["missing"]))

    def test_changing_the_zero_branch_changes_the_published_zero(self) -> None:
        def apply(rule: dict[str, Any]) -> None:
            rule["value"]["then"] = 1

        subject = self._mutated(apply)
        report, refusal = self._closed_empty(subject, "mutant.value")
        self.assertIsNone(refusal)
        row = worksheet_rows(report)[0]
        self.assertEqual(row["disposition"], "published")
        # The candidate's zero is load-bearing: a one-dollar branch is visible.
        _report, model, _refusal = execute(
            build_mutant_acts(subject, drop_tokens=WORKSHEET_ONLY_TOKENS, **CLOSED_EMPTY),
            "mutant.value.model",
            surface=subject.surface,
        )
        assert model is not None
        self.assertEqual(_published_numeric(model, "line-6b"), 1)


class TestUnclosedNonemptyReplacesTheSupersededPrototype(unittest.TestCase):
    """The four-part replacement evidence for the stopped Track 1's never-written
    ``test_member_present_no_closure_publishes``.

    Named for what actually happens on this candidate, not for the withdrawn
    assumption the stopped Track 1's test name carried: a present member with
    no closure does **not** publish anything — closure is unconditional on
    both routes, for the semantic reason that line 6b has no answer to give
    until the current SSA-1099 source family is confirmed complete."""

    def test_part_1_nonempty_unclosed_blocks(self) -> None:
        report, model, refusal = run_case(
            "unclosed-nonempty",
            benefits=[(12000.0, 0.0, 12000.0)], ira_amounts=[], wages=90000, close=False,
        )
        self.assertIsNone(refusal)
        assert model is not None
        rows = worksheet_rows(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(_disposition(model, "line-6b"), "blocked")

    def test_part_2_closed_nonempty_publishes_the_same_value_with_closure_provenance(self) -> None:
        report, model, refusal = run_case("closed-nonempty", **CLOSED_NONEMPTY)
        self.assertIsNone(refusal)
        assert model is not None
        row = worksheet_rows(report)[0]
        self.assertEqual(row["disposition"], "published")
        self.assertEqual(_published_numeric(model, "line-6b"), 10200)
        pins = pin_ids(row)
        self.assertLessEqual({CLOSURE_FINDING, FAMILY, CLOSURE_MAPPING}, pins)

    def test_part_3_a_late_member_invalidates(self) -> None:
        """A member arriving after closure displaces the closure finding onto
        a successor horizon; the previously-published closed-nonempty result
        is no longer reachable and the same lifecycle blocks."""
        acts = build_acts(**CLOSED_NONEMPTY)
        report0, model0, refusal0 = execute(acts, "track1.replacement.part3.base")
        self.assertIsNone(refusal0)
        assert model0 is not None
        self.assertEqual(worksheet_rows(report0)[0]["disposition"], "published")

        late_statement = "demo.ssa.statement.late.part3"
        late: list[dict[str, object]] = [
            _act(0, "entity-introduced", {
                "entity": {
                    "schema": "entity.v1",
                    "id": late_statement,
                    "kind": "tax.us.ssa1099-statement",
                    "label": "Late synthetic Form SSA-1099 (part 3)",
                }
            })
        ]
        for fact_type, value, suffix in (
            (BOX3, 4000.0, "box3"),
            (BOX4, 0.0, "box4"),
            (BOX6, 0, "box6"),
            (RECIPIENT, "taxpayer", "recipient"),
            (KIND, "ssa-1099", "kind"),
            (LUMP, False, "lump"),
        ):
            late.append(_act(0, "assertion", {
                "finding": _attested(
                    f"demo.ssa.finding.{suffix}.late.part3",
                    f"{fact_type}|statement={late_statement},tax-year=2025",
                    value,
                )
            }))
        late.append(_act(0, "member-transition", {
            "family": {"id": FAMILY, "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {
                "action": "assert",
                "finding": _attested(
                    "demo.ssa.finding.box5.late.part3",
                    f"{BOX5}|statement={late_statement},tax-year=2025",
                    4000.0,
                ),
            },
            "successor": {"id": "demo.ssa.h.late.part3", "predecessor": "demo.ssa.h0"},
        }))
        report1, model1, refusal1 = execute(
            build_acts(extra=late, **CLOSED_NONEMPTY), "track1.replacement.part3.late"
        )
        self.assertIsNone(refusal1)
        assert model1 is not None
        rows1 = worksheet_rows(report1)
        self.assertEqual(len(rows1), 1)
        self.assertEqual(rows1[0]["disposition"], "blocked")
        self.assertEqual(rows1[0]["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(_disposition(model1, "line-6b"), "blocked")
        self._late_acts_part3 = late

    def test_part_4_fresh_closure_republishes(self) -> None:
        late_statement = "demo.ssa.statement.late.part4"
        late: list[dict[str, object]] = [
            _act(0, "entity-introduced", {
                "entity": {
                    "schema": "entity.v1",
                    "id": late_statement,
                    "kind": "tax.us.ssa1099-statement",
                    "label": "Late synthetic Form SSA-1099 (part 4)",
                }
            })
        ]
        for fact_type, value, suffix in (
            (BOX3, 4000.0, "box3"),
            (BOX4, 0.0, "box4"),
            (BOX6, 0, "box6"),
            (RECIPIENT, "taxpayer", "recipient"),
            (KIND, "ssa-1099", "kind"),
            (LUMP, False, "lump"),
        ):
            late.append(_act(0, "assertion", {
                "finding": _attested(
                    f"demo.ssa.finding.{suffix}.late.part4",
                    f"{fact_type}|statement={late_statement},tax-year=2025",
                    value,
                )
            }))
        late.append(_act(0, "member-transition", {
            "family": {"id": FAMILY, "version": "v1"},
            "scope": SCOPE_KEY,
            "member": {
                "action": "assert",
                "finding": _attested(
                    "demo.ssa.finding.box5.late.part4",
                    f"{BOX5}|statement={late_statement},tax-year=2025",
                    4000.0,
                ),
            },
            "successor": {"id": "demo.ssa.h.late.part4", "predecessor": "demo.ssa.h0"},
        }))
        late.append(_act(0, "assertion", {
            "finding": _attested(
                "demo.ssa.closure.late.part4",
                f"{CLOSURE}|family-horizon=demo.ssa.h.late.part4,tax-year=2025",
                True,
            )
        }))
        report, model, refusal = execute(
            build_acts(extra=late, ira_amounts=[], wages=90000,
                       benefits=[(12000.0, 0.0, 12000.0), (4000.0, 0.0, 4000.0)], close=True),
            "track1.replacement.part4.reclosed",
        )
        self.assertIsNone(refusal)
        assert model is not None
        rows = worksheet_rows(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "published")
        self.assertEqual(_disposition(model, "line-6b"), "published_value")
        self.assertGreater(_published_numeric(model, "line-6b"), 0)
        pins = pin_ids(rows[0])
        self.assertLessEqual({FAMILY, CLOSURE_MAPPING}, pins)


class TestDependencyCostWitness(unittest.TestCase):
    """Durable witness for the worksheet notes' six-of-seven claim.

    An earlier draft of this rule's notes claimed rule.form1040-line9
    requires all seven of the unconditional numeric worksheet inputs; a
    targeted review (``docs/reviews/2026-08-13-ssa-no-activity-v4-targeted-
    rereview.md``, finding F2) found that claim existed only as prose and
    generator text, not as a committed regression, and required a durable
    witness before it could be trusted. These tests are that witness.
    """

    def test_worksheet_has_exactly_seven_numeric_prerequisites(self) -> None:
        rule = _load(WORKSHEET_FILE)
        non_numeric = {
            NO_RRB,
            "tax.us.2025.social-security.line6a",
            "filing_status",
            "rounding.convention",
        }
        numeric = [r for r in rule["requires"] if r not in non_numeric]
        self.assertEqual(len(numeric), 7)
        self.assertEqual(set(numeric), set(WORKSHEET_DEPENDENCY_SYMBOLS[:7]))

    def test_line9_shares_six_of_seven_and_line2a_total_is_the_sole_exception(self) -> None:
        line9 = _load("rule.form1040-line9.v7.json")
        numeric = set(WORKSHEET_DEPENDENCY_SYMBOLS[:7])
        shared = numeric & set(line9["requires"])
        missing = numeric - set(line9["requires"])
        self.assertEqual(len(shared), 6)
        self.assertEqual(missing, {LINE2A_TOTAL})

    def test_worksheet_v1_already_required_line2a_total(self) -> None:
        v1 = _load("rule.ss-benefits-worksheet.json")
        self.assertEqual(v1["version"], "v1")
        self.assertIn(LINE2A_TOTAL, v1["requires"])
        self.assertEqual(len(v1["requires"]), 33)

    def test_dropping_the_line2a_scope_declarations_blocks_on_line2a_total_only(self) -> None:
        drop_ids = {f"tax.us.2025.line2a-scope.{token}" for token in LINE2A_SCOPE_TOKENS}
        acts = build_acts(drop_fact_types=tuple(drop_ids), **CLOSED_EMPTY)
        report, _model, refusal = execute(acts, "track1.f2-witness.line2a-scope-absent")
        self.assertIsNone(refusal)
        rows = worksheet_rows(report)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(set(rows[0]["missing"]), {LINE2A_TOTAL})


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
