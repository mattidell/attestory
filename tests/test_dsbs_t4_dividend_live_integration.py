"""Track 4 deliverables 1 and 3: the missing dividend live-integration
precedent, structurally mirroring
``tests/test_frrs_t4_w2_live_integration.py`` (same synthetic-only
discipline, same temp-workspace/capability pattern, same ``demo.*`` actor
namespace) — entering exclusively through ``live_coordinate_run`` from an
authoritative act log (never a ``RunContext`` shortcut), per the Track
0a/2/3 review-chain discipline.

The package under test is ``tax.us.2025.package.core-calculations`` v6
(tools/generate_dsbs_t3_content.py), adopted via
``packages/sample_data/frrs_t3/adoptions/adopt-core-v6-current.json`` at
scope year 2055 — the same package and scope Track 3's QDCG goldens
(tests/test_dsbs_t3_line16_coordinator.py) already exercise. Two prior
tracks proved the Schedule B attachment (tests/test_dsbs_t2_schedule_b.py,
v5) and the QDCG worksheet successor (tests/test_dsbs_t3_line16_coordinator.
py, v6) each *separately*; neither composes them with W-2 + 1099-INT +
1099-DIV facts and the Part III / declared-absence declarations together in
one authoritative act log under the actual v6 pin. That composition is this
file's entire job.

Deliverable 1 (confirming goldens, not new content): ``ClosureAndLineNine
Confirmation`` below re-derives, specifically under the v6 pin, that the
1099-DIV closure mappings honestly close and that line-9 v2 absorbs 3b into
total income. The closure-admission mechanism's general shape — literal-
current-true is the only empty-set authority; false/absent/displaced/
truthy-non-boolean/duplicate all fail closed — is already proven directly
against ``resolve_closure_admissions`` by
tests/test_frrs_t4_w2_live_integration.py::W2Closure over the w2 mapping;
the dividend closure mappings are structurally identical in shape (charter
"Scope reconciliation" item 1: ``source-closure-mapping.v2`` schema,
``family-horizon``-keyed, literal-true-only admission locus), so that proof
already covers the mechanism generically. What is not yet proven is that
the two committed dividend mappings actually exercise that mechanism
correctly when driven live, and that v6 (not v4, where
tests/test_dsbs_t2_coordinator.py first proved line-9 v2's dividend
absorption) still pins the identical behavior — that is what this class
adds.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
T3 = REPO / "packages" / "sample_data" / "frrs_t3"
USER = "demo.user.filer-1"
SCOPE = {"jurisdiction": "us", "year": "2055"}

LINE_3A_RULE = "tax.us.2025.rule.form1040-line3a"
LINE_3B_RULE = "tax.us.2025.rule.form1040-line3b"
LINE_9_RULE = "tax.us.2025.rule.form1040-line9"
LINE_16_RULE = "tax.us.2025.rule.form1040-line16"
SUBTOTAL_1A_RULE = "tax.us.2025.rule.f1099div-1a-subtotal"
SUBTOTAL_1B_RULE = "tax.us.2025.rule.f1099div-1b-subtotal"
ATTACHMENT_RULE = "tax.us.2025.rule.attachment.schedule-b"
ATTACHMENT_SYMBOL = "tax.us.2025.scheduleb.disposition"
FOREIGN_ACCOUNT_SYMBOL = "tax.us.2025.scheduleb.foreign-account"
FOREIGN_TRUST_SYMBOL = "tax.us.2025.scheduleb.foreign-trust"
COUNTRY_SYMBOL = "tax.us.2025.scheduleb.7b-country"
CG_DIST_SYMBOL = "tax.us.2025.capital-gain-distributions"
SCHED_D_SYMBOL = "tax.us.2025.schedule-d-required"


def _act(name: str) -> dict[str, object]:
    return cast(dict[str, object], json.loads((T3 / "adoptions" / name).read_text("utf-8")))


def _surface() -> PublicationSurface:
    return PublicationSurface(T3 / "publication_surface" / "releases", CONTENT / "published-packages.json", CONTENT)


def _live_act(index: int, kind: str, payload: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.dsbs.t4.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-07-20T02:00:{index:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _attested_finding(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    return {"schema": "finding.v1", "id": finding_id, "fact_id": fact_id, "value": value, "basis": "attested", "evidence_ids": []}


def _v6_dividend_acts(
    *,
    wages: float | None = 90000,
    box1a: float | None = 600,
    box1b: float | None = None,
    close_1a: bool = True,
    close_1b: bool = True,
    foreign_account: str | None = "no",
    foreign_trust: str | None = "no",
    country: str | None = None,
    cg_dist: str | None = "no",
    sched_d: str | None = "no",
) -> list[dict[str, object]]:
    """A complete synthetic v6 live record: W-2 + 1099-INT (closure-backed
    zero throughout, never a member) + 1099-DIV + every declaration
    Schedule B / the QDCG worksheet can consume, so one run can be checked
    against both simultaneously — the composition neither
    tests/test_dsbs_t2_schedule_b.py (v5, no QDCG) nor
    tests/test_dsbs_t3_line16_coordinator.py (v6, no Schedule B attachment)
    exercises.
    """
    acts: list[dict[str, object]] = []

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_live_act(len(acts), kind, payload))

    for name in (
        "w2.bundle.v3.json",
        "f1099int.bundle.json",
        "interest_composition.bundle.json",
        "core_calculations.bundle.v2.json",
        "f1099div.bundle.json",
        "scheduleb.bundle.json",
        "qdcg.bundle.json",
    ):
        add("bundle-adoption", {"bundle": json.loads((CONTENT / name).read_text())})

    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.dsbs.t4.employer", "kind": "tax.us.employer", "label": "Synthetic employer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.dsbs.t4.w2", "kind": "tax.us.w2-slip", "label": "Synthetic W-2 slip"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.dsbs.t4.payer", "kind": "tax.us.dividend-payer", "label": "Synthetic dividend payer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.dsbs.t4.stmt", "kind": "tax.us.1099div-statement", "label": "Synthetic 1099-DIV statement"}})

    scope = {"tax-year": "2025", "subject": "demo.primary"}
    families = (
        ("tax.us.2025.w2", "v2", "demo.dsbs.t4.w2.h0"),
        ("tax.us.2025.f1099int.b1", "v1", "demo.dsbs.t4.int-b1.h0"),
        ("tax.us.2025.f1099int.b3", "v1", "demo.dsbs.t4.int-b3.h0"),
        ("tax.us.2025.f1099oid.b1", "v1", "demo.dsbs.t4.oid-b1.h0"),
        ("tax.us.2025.non-form-interest", "v1", "demo.dsbs.t4.nonform.h0"),
        ("tax.us.2025.f1099div.1a", "v1", "demo.dsbs.t4.div1a.h0"),
        ("tax.us.2025.f1099div.1b", "v1", "demo.dsbs.t4.div1b.h0"),
    )
    for family_id, version, horizon_id in families:
        add("horizon-genesis", {"family": {"id": family_id, "version": version}, "scope": scope, "horizon_id": horizon_id})

    w2_horizon = "demo.dsbs.t4.w2.h0"
    if wages is not None:
        add("member-transition", {
            "family": {"id": "tax.us.2025.w2", "version": "v2"},
            "scope": scope,
            "member": {"action": "assert", "finding": {
                "schema": "finding.v2", "id": "demo.dsbs.t4.finding.wages",
                "fact_id": "tax.us.2025.w2.box1-wages|employer=demo.dsbs.t4.employer,w2-slip=demo.dsbs.t4.w2,tax-year=2025",
                "value": wages, "basis": "attested", "evidence_ids": [],
            }},
            "successor": {"id": "demo.dsbs.t4.w2.h1", "predecessor": w2_horizon},
        })
        w2_horizon = "demo.dsbs.t4.w2.h1"

    def _dividend_member(fact_type: str, family_id: str, family_version: str, predecessor: str, successor: str, value: float, finding_id: str) -> None:
        add("member-transition", {
            "family": {"id": family_id, "version": family_version},
            "scope": scope,
            "member": {"action": "assert", "finding": {
                "schema": "finding.v2", "id": finding_id,
                "fact_id": f"{fact_type}|payer=demo.dsbs.t4.payer,statement=demo.dsbs.t4.stmt,tax-year=2025",
                "value": value, "basis": "attested", "evidence_ids": [],
            }},
            "successor": {"id": successor, "predecessor": predecessor},
        })

    div1a_horizon = "demo.dsbs.t4.div1a.h0"
    if box1a is not None:
        _dividend_member(
            "tax.us.2025.f1099div.box1a-ordinary", "tax.us.2025.f1099div.1a", "v1",
            div1a_horizon, "demo.dsbs.t4.div1a.h1", box1a, "demo.dsbs.t4.finding.box1a",
        )
        div1a_horizon = "demo.dsbs.t4.div1a.h1"
    div1b_horizon = "demo.dsbs.t4.div1b.h0"
    if box1b is not None:
        _dividend_member(
            "tax.us.2025.f1099div.box1b-qualified", "tax.us.2025.f1099div.1b", "v1",
            div1b_horizon, "demo.dsbs.t4.div1b.h1", box1b, "demo.dsbs.t4.finding.box1b",
        )
        div1b_horizon = "demo.dsbs.t4.div1b.h1"

    add("assertion", {"finding": _attested_finding("demo.dsbs.t4.finding.rounding", "rounding.convention|tax-year=2025", "half_up")})
    add("assertion", {"finding": _attested_finding("demo.dsbs.t4.finding.status", "tax.us.2025.filing-status|tax-year=2025", "single")})

    if foreign_account is not None:
        add("assertion", {"finding": _attested_finding("demo.dsbs.t4.finding.foreign-account", f"{FOREIGN_ACCOUNT_SYMBOL}|tax-year=2025", foreign_account)})
    if foreign_trust is not None:
        add("assertion", {"finding": _attested_finding("demo.dsbs.t4.finding.foreign-trust", f"{FOREIGN_TRUST_SYMBOL}|tax-year=2025", foreign_trust)})
    if country is not None:
        add("assertion", {"finding": _attested_finding("demo.dsbs.t4.finding.country", f"{COUNTRY_SYMBOL}|tax-year=2025", country)})
    if cg_dist is not None:
        add("assertion", {"finding": _attested_finding("demo.dsbs.t4.finding.cg-dist", f"{CG_DIST_SYMBOL}|tax-year=2025", cg_dist)})
    if sched_d is not None:
        add("assertion", {"finding": _attested_finding("demo.dsbs.t4.finding.sched-d", f"{SCHED_D_SYMBOL}|tax-year=2025", sched_d)})

    closures = [
        ("demo.dsbs.t4.closure.w2", "tax.us.2025.w2.source-closure", w2_horizon),
        ("demo.dsbs.t4.closure.int-b1", "tax.us.2025.f1099int.b1.source-closure", "demo.dsbs.t4.int-b1.h0"),
        ("demo.dsbs.t4.closure.int-b3", "tax.us.2025.f1099int.b3.source-closure", "demo.dsbs.t4.int-b3.h0"),
        ("demo.dsbs.t4.closure.oid-b1", "tax.us.2025.f1099oid.b1.source-closure", "demo.dsbs.t4.oid-b1.h0"),
        ("demo.dsbs.t4.closure.nonform", "tax.us.2025.non-form-interest.source-closure", "demo.dsbs.t4.nonform.h0"),
    ]
    if close_1a:
        closures.append(("demo.dsbs.t4.closure.div1a", "tax.us.2025.f1099div.1a.source-closure", div1a_horizon))
    if close_1b:
        closures.append(("demo.dsbs.t4.closure.div1b", "tax.us.2025.f1099div.1b.source-closure", div1b_horizon))
    for finding_id, fact_type, horizon_id in closures:
        add("assertion", {"finding": _attested_finding(finding_id, f"{fact_type}|family-horizon={horizon_id},tax-year=2025", True)})

    adoption = _act("adopt-core-v6-current.json")
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts


def _run(acts: list[dict[str, object]], run_id: str) -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        result = live_coordinate_run(
            WorkspaceCapability(root / "L"), repo_root=REPO, authoritative_acts=acts,
            workspace_revision=len(acts), run_scope=SCOPE, scope_user=USER,
            request={"schema": "run-request.v1"}, run_id=run_id, governance_pins=[],
            surface=_surface(), output_name="out.json",
        )
        assert result.refusal is None, result.refusal
        assert result.output_path is not None
        return cast(dict[str, Any], json.loads(result.output_path.read_text()))


def _by_artifact(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["artifact_id"]: row for row in report["dispositions"]}


class ClosureAndLineNineConfirmation(unittest.TestCase):
    """Deliverable 1: under the v6 pin specifically, the 1099-DIV closure
    mappings honestly close and line-9 v2 absorbs 3b."""

    def test_closed_empty_both_boxes_publish_honest_zero_pinning_closure(self) -> None:
        report = _run(
            _v6_dividend_acts(box1a=None, box1b=None),
            "demo.dsbs.t4.closure.empty",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE_3A_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE_3B_RULE]["disposition"], "published")
        # A closure-backed zero pins the family closure finding, never a
        # source finding that was never asserted (literal-current-true is
        # the only empty-set authority, ADR-0014/0017).
        pinned_1a = {p["id"] for p in rows[SUBTOTAL_1A_RULE]["pins"]}
        pinned_1b = {p["id"] for p in rows[SUBTOTAL_1B_RULE]["pins"]}
        self.assertIn("demo.dsbs.t4.closure.div1a", pinned_1a)
        self.assertIn("demo.dsbs.t4.closure.div1b", pinned_1b)

    def test_open_family_blocks_only_its_own_line_with_source_set_unclosed(self) -> None:
        # box1a present and closed; box1b's family is left open (no closure
        # asserted) — present-without-closure never silently aggregates
        # into a publication: the subtotal itself sums whatever box1b
        # findings are current regardless of closure (its own closure gate
        # only governs the honest-empty-zero case), but the composing line
        # 3a rule's own ``require_closed`` on the source family blocks it
        # directly with SOURCE_SET_UNCLOSED — line 3a's box1a sibling is
        # wholly unaffected (per-box closure independence).
        report = _run(
            _v6_dividend_acts(box1a=120, box1b=80, close_1b=False),
            "demo.dsbs.t4.closure.open",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE_3B_RULE]["disposition"], "published")
        self.assertEqual(rows[SUBTOTAL_1B_RULE]["disposition"], "published")
        self.assertEqual(rows[LINE_3A_RULE]["disposition"], "blocked")
        self.assertEqual(rows[LINE_3A_RULE]["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(rows[LINE_3A_RULE]["missing"], ["tax.us.2025.f1099div.1b"])

    def test_line9_v2_pins_ordinary_dividends_into_total_income_under_v6(self) -> None:
        report = _run(
            _v6_dividend_acts(box1a=120, box1b=80),
            "demo.dsbs.t4.line9",
        )
        rows = _by_artifact(report)
        self.assertEqual(rows[LINE_9_RULE]["disposition"], "published")
        pinned = {p["id"] for p in rows[LINE_9_RULE]["pins"]}
        self.assertIn(rows[LINE_3B_RULE]["finding_id"], pinned)


class ScheduleBRequiredWithQdcgWorksheet(unittest.TestCase):
    """Deliverable 3, existing branch: dividends over the Schedule B
    threshold with a positive qualified box — the attachment publishes
    (required) and line 16 publishes through the QDCG worksheet path, both
    from the one authoritative act log, both declared-absence declarations
    resolved."""

    def test_schedule_b_publishes_required_and_line16_publishes_worksheet(self) -> None:
        report = _run(
            _v6_dividend_acts(
                box1a=2000, box1b=600,
                foreign_account="no", foreign_trust="no",
                cg_dist="no", sched_d="no",
            ),
            "demo.dsbs.t4.required",
        )
        rows = _by_artifact(report)
        attachment = rows[ATTACHMENT_RULE]
        self.assertEqual(attachment["disposition"], "published")
        self.assertEqual(attachment["symbol"], ATTACHMENT_SYMBOL)
        attachment_pins = {p["id"] for p in attachment["pins"]}
        self.assertIn("demo.dsbs.t4.finding.box1a", attachment_pins)
        self.assertIn("demo.dsbs.t4.finding.foreign-account", attachment_pins)
        self.assertIn("demo.dsbs.t4.finding.foreign-trust", attachment_pins)

        line16 = rows[LINE_16_RULE]
        self.assertEqual(line16["disposition"], "published")
        line16_pins = {p["id"] for p in line16["pins"]}
        self.assertIn("demo.dsbs.t4.finding.cg-dist", line16_pins)
        self.assertIn("demo.dsbs.t4.finding.sched-d", line16_pins)
        self.assertIn(rows[LINE_3A_RULE]["finding_id"], line16_pins)


class ScheduleBNotRequiredWithQdcgWorksheet(unittest.TestCase):
    """Deliverable 3, not-existing branch: dividends at/under the
    threshold — the attachment is inapplicable (not required, walkable
    non-publication naming the threshold/citation) while line 16 still
    resolves cleanly through the ordinary (non-worksheet) path since no
    qualified dividends were ever recorded, and never reaches around the
    attachment (the Track 2 AttachmentCannotPropagateToALine invariant,
    re-confirmed live here rather than merely by content grep)."""

    def test_schedule_b_inapplicable_and_line16_publishes_ordinary_path(self) -> None:
        report = _run(
            _v6_dividend_acts(
                box1a=None, box1b=None,
                foreign_account="no", foreign_trust="no",
                cg_dist=None, sched_d=None,
            ),
            "demo.dsbs.t4.not-required",
        )
        rows = _by_artifact(report)
        attachment = rows[ATTACHMENT_RULE]
        self.assertEqual(attachment["disposition"], "inapplicable")
        self.assertEqual(attachment["guard_result"], False)
        pin_ids = {p["id"] for p in attachment["pins"]}
        self.assertIn("tax.us.2025.parameter.schedule-b-threshold", pin_ids)
        self.assertIn("tax.us.2025.citation.schedule-b", pin_ids)

        line16 = rows[LINE_16_RULE]
        self.assertEqual(line16["disposition"], "published")
        # No qualified dividends were recorded, so the worksheet's own
        # declared-absence declarations are never read, named, or pinned —
        # and, since the attachment is inapplicable rather than open, its
        # symbol (the same string the Track 2 content-grep golden checks
        # for) is absent from line 16's pins too.
        line16_pin_ids = {p["id"] for p in line16["pins"]}
        self.assertNotIn(CG_DIST_SYMBOL, line16_pin_ids)
        self.assertNotIn(SCHED_D_SYMBOL, line16_pin_ids)
        self.assertNotIn(ATTACHMENT_SYMBOL, line16_pin_ids)


if __name__ == "__main__":
    unittest.main()
