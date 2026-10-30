"""Track 1: an unresolved Form 1099-K blocks Schedule 1 line 10 on core v60.

Runs go through ``live_coordinate_run`` on the committed packages. A return
with no Form 1099-K, and a return whose Form 1099-K is a supported loss,
keep the values core v59 publishes. An unresolved statement blocks line 10,
and the lines that read additional income do not publish, line 33 among them
(it reads line 32, which reads AGI). Only line 25b does not read that income,
so it keeps the value the same acts publish on v59. A family not confirmed
complete blocks line 10 the same way.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

import unittest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.facts import fact_id_for
from packages.tax.loader import (
    domain_package_companion_declarations,
    load_f1099k_bundle,
    load_f1099k_circumstances_bundle,
)
from tests.test_f1099k_personal_item_sale_track1 import (
    BOX1A,
    BOX4,
    CIRCUMSTANCE_FACTS,
    Q1,
    Q3,
    Q4,
    Q5,
    Q7,
    Q8_PRICE,
    Q8_SHIP,
    Q9_FEES,
    Q9_SELLER_SHIP,
    Q10_TAX,
    Q10_REFUND,
    Q11_BUYER_SHIP,
    Q12_COST,
    Q12_GATE,
    Q13,
)
from tests.test_form_1099_withholding import (
    CONTENT,
    RELEASE_DIR,
    ROOT,
    SCOPE_KEY,
    USER,
    YEAR,
    PACKAGE_V59,
    RELEASE_V57,
    SURFACE_V59,
    _social_security_return,
    _unemployment_return,
)
from tests.test_refund_or_amount_owed_track1 import _act, _attested, _finish

PACKAGE_V60 = CONTENT / "package.core-calculations.v60.json"
RELEASE_V58 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v58.json"
SURFACE_V60 = PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v58.json", CONTENT)
ADOPTION_V60 = ROOT / "packages/sample_data/form_1099_k_income/adoptions/adopt-core-v60-current.json"

_CORE = "tax.us.2025.package.core-calculations"
_FAMILY = "tax.us.2025.f1099k"
_CLOSURE = _FAMILY + ".source-closure"
_PAYER = "demo.platform.a"
_STMT = "demo.stmt.a"
_BOX1A_AMOUNT = 880.0

_LINE10 = "tax.us.2025.schedule1.line10-additional-income"
_LINE8 = "tax.us.2025.income.additional-income"
_LINE9 = "tax.us.2025.income.total-income"
_LINE11 = "tax.us.2025.income.agi"
_LINE15 = "tax.us.2025.income.taxable-income"
_LINE16 = "tax.us.2025.tax.total-tax"
_LINE24 = "tax.us.2025.tax.line24-total-tax"
_LINE25B = "tax.us.2025.payments.line25b"
_LINE33 = "tax.us.2025.payments.line33"
_LINE34 = "tax.us.2025.payments.line34-overpaid"
_LINE35A = "tax.us.2025.payments.line35a-refunded"
_LINE37 = "tax.us.2025.payments.line37-amount-owed"
_UNRESOLVED = "tax.us.2025.f1099k.unresolved"
_TOP = "tax.us.2025.schedule1.top-entry"

_RULE_UNRESOLVED = "tax.us.2025.rule.f1099k-unresolved"
_RULE_TOP = "tax.us.2025.rule.schedule1-top-entry"
_RULE_ATTACHMENT = "tax.us.2025.rule.attachment.schedule-1"
_RULE_LINE10 = "tax.us.2025.rule.schedule1-line10"
_RULE_LINE8 = "tax.us.2025.rule.form1040-line8"
_RULE_LINE9 = "tax.us.2025.rule.form1040-line9"
_RULE_LINE11 = "tax.us.2025.rule.form1040-line11"
_RULE_LINE15 = "tax.us.2025.rule.form1040-line15"
_RULE_LINE16 = "tax.us.2025.rule.form1040-line16"
_RULE_LINE24 = "tax.us.2025.rule.form1040-line24"
_RULE_LINE34 = "tax.us.2025.rule.form1040-line34"
_RULE_LINE35A = "tax.us.2025.rule.form1040-line35a"
_RULE_LINE37 = "tax.us.2025.rule.form1040-line37"

# Lines that read additional income, directly or through the lines above them.
_STOPPED = (_LINE8, _LINE9, _LINE11, _LINE15, _LINE16, _LINE24, _LINE33, _LINE34, _LINE35A, _LINE37)
# On immutable core v59 these still publish while the 1099-K is unresolved.
_GAP_LINES = (_LINE10, _LINE8, _LINE9, _LINE11, _LINE15, _LINE16, _LINE24, _LINE25B, _LINE33, _LINE34, _LINE35A, _LINE37)


def _handover(
    finished: list[dict[str, object]], *, surface: PublicationSurface, reconfirm: bool
) -> list[dict[str, object]]:
    """Hands the Social Security chain over against ``surface``.

    The v59 helper pins its own surface. A v60 adoption is not in that registry,
    so the successor run resolves the family version on the surface that publishes it.
    """
    from packages.derivation.loader import DerivationSchemas
    from packages.tax.loader import (
        install_domain_companion_equalities,
        install_domain_companion_presence,
        install_domain_declaration_signal_contradictions,
    )
    from packages.tax.ssa_family_handover import ssa_family_version_for_acts, stage_ssa_family_handover

    registry = DerivationSchemas().registry
    install_domain_companion_presence(registry)
    install_domain_companion_equalities(registry)
    install_domain_declaration_signal_contradictions(registry)
    version = ssa_family_version_for_acts(finished, actor=USER, surface=surface)
    act, _unused = stage_ssa_family_handover(
        finished, registry, actor=USER, at="2026-10-28T12:00:00Z", family_version=version
    )
    out = copy.deepcopy(finished) + [act]
    if reconfirm:
        horizon = act["payload"]["successor"]["horizon_id"]
        closure = _act(
            len(out),
            "assertion",
            {"finding": _attested(
                "demo.fk.ssa.reconfirm",
                f"tax.us.2025.ssa1099.source-closure|family-horizon={horizon},tax-year={YEAR}",
                True,
            )},
        )
        closure["actor"] = USER
        out.append(closure)
    return out


def _run_on(acts: list[dict[str, object]], run_id: str, core: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if core == "v60":
        package, version, release, rel_version, surface = (
            PACKAGE_V60, "v60", RELEASE_V58, "v58", SURFACE_V60,
        )
    elif core == "v59":
        package, version, release, rel_version, surface = (
            PACKAGE_V59, "v59", RELEASE_V57, "v57", SURFACE_V59,
        )
    else:
        raise AssertionError(core)
    finished = _finish(
        copy.deepcopy(acts),
        package_path=package,
        package_version=version,
        release_path=release,
        release_version=rel_version,
        note=run_id,
    )
    finished = _handover(finished, surface=surface, reconfirm=True)
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            raise AssertionError(f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
        pubs = {str(item.finding["symbol"]): item.finding for item in outcome.publications or ()}
        blocked: list[dict[str, Any]] = []
        if outcome.output_path is not None:
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            blocked = [row for row in report.get("dispositions", []) if row.get("disposition") == "blocked"]
    return pubs, blocked


def _values(pubs: dict[str, Any]) -> dict[str, Any]:
    return {symbol: finding["value"] for symbol, finding in pubs.items()}


def _blocks(blocked: list[dict[str, Any]]) -> list[tuple[str, str, tuple[str, ...]]]:
    return sorted(
        (str(row["artifact_id"]), str(row["code"]), tuple(str(item) for item in row["missing"]))
        for row in blocked
    )


def _run_finished(
    finished: list[dict[str, object]], run_id: str, surface: PublicationSurface
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Runs a log that already carries its adoption and Social Security handover."""
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            raise AssertionError(f"{run_id} refused: {outcome.refusal.reason} {outcome.refusal.detail}")
        pubs = {str(item.finding["symbol"]): item.finding for item in outcome.publications or ()}
        blocked: list[dict[str, Any]] = []
        if outcome.output_path is not None:
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            blocked = [row for row in report.get("dispositions", []) if row.get("disposition") == "blocked"]
    return pubs, blocked


def _finish_on(acts: list[dict[str, object]], run_id: str, core: str) -> list[dict[str, object]]:
    if core == "v60":
        package, version, release, rel_version, surface = (
            PACKAGE_V60, "v60", RELEASE_V58, "v58", SURFACE_V60,
        )
    elif core == "v59":
        package, version, release, rel_version, surface = (
            PACKAGE_V59, "v59", RELEASE_V57, "v57", SURFACE_V59,
        )
    else:
        raise AssertionError(core)
    finished = _finish(
        copy.deepcopy(acts),
        package_path=package,
        package_version=version,
        release_path=release,
        release_version=rel_version,
        note=run_id,
    )
    return _handover(finished, surface=surface, reconfirm=True)


def _append_v60(finished: list[dict[str, object]]) -> list[dict[str, object]]:
    """Adopts core v60 onto a log that already adopted v59. The later revision wins."""
    adoption = cast(dict[str, object], json.loads(ADOPTION_V60.read_text(encoding="utf-8")))
    adoption = copy.deepcopy(adoption)
    adoption["act_id"] = f"demo.fk.adopt.core.v60.{len(finished):03d}"
    adoption["actor"] = USER
    adoption["committed_against"] = len(finished)
    out = copy.deepcopy(finished)
    out.append(adoption)
    return out


def _supported_answers() -> dict[str, Any]:
    """The track-1 supported-loss answers. Box 1a is 880 so they reconcile."""
    return {
        Q1: "yes",
        Q3: "yes",
        Q4: "personal-use",
        Q5: "yes",
        Q7: "no",
        Q8_PRICE: 800.0,
        Q8_SHIP: "platform-pass-through",
        Q9_FEES: 80.0,
        Q9_SELLER_SHIP: 0.0,
        Q10_TAX: 56.0,
        Q10_REFUND: 0.0,
        Q11_BUYER_SHIP: 24.0,
        Q12_COST: 1000.0,
        Q12_GATE: "yes",
        Q13: "no",
    }


def _bundle_ids(acts: list[dict[str, object]]) -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    for act in acts:
        if act.get("kind") != "bundle-adoption":
            continue
        bundle = cast(dict[str, Any], act["payload"]).get("bundle")
        if isinstance(bundle, dict) and isinstance(bundle.get("id"), str):
            found.add((bundle["id"], str(bundle.get("version"))))
    return found


def _genesis(acts: list[dict[str, object]]) -> dict[str, Any] | None:
    for act in acts:
        if act.get("kind") != "horizon-genesis":
            continue
        payload = cast(dict[str, Any], act["payload"])
        family = payload.get("family")
        if isinstance(family, dict) and family.get("id") == _FAMILY:
            return payload
    return None


def _splice(acts: list[dict[str, object]], *, box4: float, omit: str | None) -> list[dict[str, object]]:
    """Records one Form 1099-K on a copy of ``acts`` and retargets the family closure."""
    return _splice_many(acts, statements=[(box4, omit)])


def _splice_many(
    acts: list[dict[str, object]],
    *,
    statements: list[tuple[float, str | None]],
    closed: bool = True,
) -> list[dict[str, object]]:
    """Records Form 1099-K statements on a copy of ``acts`` and retargets the family closure.

    Box 1a is the family member. Box 4 and the circumstance answers are plain
    assertions. Each statement is ``(box 4, circumstance fact type to omit)``.
    With no statements the family stays at its base horizon. ``closed=False``
    drops the family closure, so the filer has not said the statements are
    complete. Act ids sit above the base log's own ids; the timestamp is
    rewritten because the shared act helper only formats a valid clock minute
    for small indexes. The first statement keeps the single-statement ids.
    """
    built = copy.deepcopy(acts)
    counter = [10000]

    def late(kind: str, payload: dict[str, object]) -> dict[str, object]:
        act = _act(counter[0], kind, payload)
        second = counter[0] % 60
        minute = 20 + ((counter[0] // 60) % 30)
        act["at"] = f"2026-10-28T12:{minute:02d}:{second:02d}Z"
        counter[0] += 1
        return act

    inserted: list[dict[str, object]] = []
    have = _bundle_ids(built)
    for bundle in (load_f1099k_bundle(version="v3"), load_f1099k_circumstances_bundle()):
        key = (str(bundle["id"]), str(bundle["version"]))
        if key not in have:
            inserted.append(late("bundle-adoption", {"bundle": cast(object, bundle)}))

    genesis = _genesis(built)
    if genesis is None:
        head = "demo.fk.f1099k.h0"
        inserted.append(late("horizon-genesis", {
            "family": {"id": _FAMILY, "version": "v2"},
            "scope": dict(SCOPE_KEY),
            "horizon_id": head,
        }))
        scope: dict[str, object] = dict(SCOPE_KEY)
        family_version = "v2"
    else:
        head = str(genesis["horizon_id"])
        scope = dict(cast(dict[str, object], genesis.get("scope") or SCOPE_KEY))
        family = cast(dict[str, Any], genesis["family"])
        family_version = str(family.get("version"))

    for index, (box4, omit) in enumerate(statements):
        tag = "" if index == 0 else f".{index}"
        payer = _PAYER if index == 0 else f"demo.platform.{chr(ord('a') + index)}"
        stmt = _STMT if index == 0 else f"demo.stmt.{chr(ord('a') + index)}"
        successor = f"demo.fk.f1099k.h{index + 1}"
        keys = (("payer", payer), ("statement", stmt))
        inserted.append(late("entity-introduced", {
            "entity": {
                "schema": "entity.v1",
                "id": payer,
                "kind": "tax.us.1099k-platform",
                "label": "Synthetic",
            },
        }))
        inserted.append(late("entity-introduced", {
            "entity": {
                "schema": "entity.v1",
                "id": stmt,
                "kind": "tax.us.1099k-statement",
                "label": "Synthetic",
            },
        }))
        box1a_fact = fact_id_for(BOX1A, keys + (("tax-year", YEAR),))
        inserted.append(late("member-transition", {
            "family": {"id": _FAMILY, "version": family_version},
            "scope": scope,
            "member": {
                "action": "assert",
                "finding": _attested(f"demo.fk.f1099k.box1a{tag}", box1a_fact, _BOX1A_AMOUNT),
            },
            "successor": {"id": successor, "predecessor": head},
        }))
        head = successor
        box4_fact = fact_id_for(BOX4, keys + (("tax-year", YEAR),))
        inserted.append(late("assertion", {
            "finding": _attested(f"demo.fk.f1099k.box4{tag}", box4_fact, box4),
        }))
        answers = _supported_answers()
        if omit is not None:
            answers.pop(omit, None)
        for fact_type in CIRCUMSTANCE_FACTS:
            if fact_type not in answers:
                continue
            short = fact_type.rsplit(".", 1)[-1]
            fact_id = fact_id_for(fact_type, keys + (("tax-year", YEAR),))
            inserted.append(late("assertion", {
                "finding": _attested(f"demo.fk.f1099k.{short}{tag}", fact_id, answers[fact_type]),
            }))

    closure_at: int | None = None
    for index, act in enumerate(built):
        finding = cast(dict[str, Any], cast(dict[str, Any], act.get("payload") or {}).get("finding"))
        if finding and str(finding.get("fact_id", "")).startswith(_CLOSURE + "|"):
            closure_at = index
            break
    if closed:
        closure_fact = f"{_CLOSURE}|family-horizon={head},tax-year={YEAR}"
        if closure_at is None:
            inserted.append(late("assertion", {
                "finding": _attested("demo.fk.f1099k.closure", closure_fact, True),
            }))
            built.extend(inserted)
        else:
            cast(dict[str, Any], cast(dict[str, Any], built[closure_at]["payload"])["finding"])["fact_id"] = closure_fact
            built[closure_at:closure_at] = inserted
    elif closure_at is None:
        built.extend(inserted)
    else:
        # The closure assertion is dropped: the family has no confirmation at all.
        del built[closure_at]
        built[closure_at:closure_at] = inserted
    return built


def _row(blocked: list[dict[str, Any]], artifact_id: str) -> dict[str, Any]:
    rows = [row for row in blocked if row.get("artifact_id") == artifact_id]
    if len(rows) != 1:
        seen = sorted(str(row.get("artifact_id")) for row in blocked)
        raise AssertionError(f"{artifact_id} blocked {len(rows)} times; blocked: {seen}")
    return rows[0]


class V60AdmitsTheUnemploymentWithholdingReturn(unittest.TestCase):
    def test_v60_shares_the_v59_withholding_declaration(self) -> None:
        declarations = domain_package_companion_declarations()
        self.assertIs(declarations[(_CORE, "v59")], declarations[(_CORE, "v60")])

    def test_v60_counts_the_track1_unemployment_withholding_return_as_v59_does(self) -> None:
        acts = _unemployment_return(withheld=600.0)
        v59_pubs, v59_blocked = _run_on(acts, "demo.fk.admit.v59", "v59")
        v60_pubs, v60_blocked = _run_on(acts, "demo.fk.admit.v60", "v60")
        self.assertEqual(_values(v60_pubs), _values(v59_pubs))
        self.assertEqual(_blocks(v60_blocked), _blocks(v59_blocked))


class UnresolvedForm1099KBlocksLine10(unittest.TestCase):
    def _assert_line10_blocks_and_25b_keeps_v59(self, *, box4: float, omit: str | None, run_id: str) -> None:
        acts = _splice(_unemployment_return(withheld=600.0), box4=box4, omit=omit)
        v59_pubs, _ = _run_on(acts, run_id + ".v59", "v59")
        v60_pubs, v60_blocked = _run_on(acts, run_id + ".v60", "v60")

        line10 = _row(v60_blocked, _RULE_LINE10)
        self.assertEqual(line10["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(list(line10["missing"]), [_UNRESOLVED])
        self.assertNotIn(_LINE10, v60_pubs)

        # Exact lists where the cause is one link: the 1099-K rules, line 10
        # and line 8. Further down each line names the traced input among
        # its other inputs that the block also stops (line 9 names line 6b,
        # line 15 names line 14, line 16 the qualified-dividends worksheet).
        exact = {
            _RULE_UNRESOLVED: [],
            _RULE_TOP: [],
            _RULE_ATTACHMENT: [_TOP],
            _RULE_LINE8: [_LINE10],
        }
        traced = {
            _RULE_LINE9: _LINE8,
            _RULE_LINE11: _LINE9,
            _RULE_LINE15: _LINE11,
            _RULE_LINE16: _LINE15,
            _RULE_LINE24: "tax.us.2025.tax.after-nonrefundable-credits",
            # Line 33 reads line 32, the refundable credits, which read AGI.
            # P0 expected line 33 to publish; the run blocks it.
            "tax.us.2025.rule.form1040-line33": "tax.us.2025.payments.line32",
            _RULE_LINE34: _LINE24,
            _RULE_LINE35A: _LINE34,
            _RULE_LINE37: _LINE24,
        }
        for artifact_id, missing in exact.items():
            row = _row(v60_blocked, artifact_id)
            self.assertEqual(row["code"], "DEPENDENCY_ABSENT", artifact_id)
            self.assertEqual(list(row["missing"]), missing, artifact_id)
        for artifact_id, symbol in traced.items():
            row = _row(v60_blocked, artifact_id)
            self.assertEqual(row["code"], "DEPENDENCY_ABSENT", artifact_id)
            self.assertIn(symbol, list(row["missing"]), artifact_id)
        for symbol in _STOPPED:
            self.assertNotIn(symbol, v60_pubs, symbol)
        self.assertEqual(v60_pubs[_LINE25B]["value"], v59_pubs[_LINE25B]["value"])

    def test_box4_150_blocks_line10_and_keeps_line_25b(self) -> None:
        self._assert_line10_blocks_and_25b_keeps_v59(box4=150.0, omit=None, run_id="demo.fk.b150")

    def test_an_omitted_circumstance_answer_blocks_the_same_way(self) -> None:
        self._assert_line10_blocks_and_25b_keeps_v59(box4=0.0, omit=Q5, run_id="demo.fk.omit")

    def test_supported_loss_publishes_the_v59_values(self) -> None:
        acts = _splice(_unemployment_return(withheld=600.0), box4=0.0, omit=None)
        v59_pubs, v59_blocked = _run_on(acts, "demo.fk.loss.v59", "v59")
        v60_pubs, v60_blocked = _run_on(acts, "demo.fk.loss.v60", "v60")
        self.assertEqual(_values(v60_pubs), _values(v59_pubs))
        self.assertEqual(_blocks(v60_blocked), _blocks(v59_blocked))

    def test_no_form_1099k_publishes_the_v59_values(self) -> None:
        acts = _unemployment_return(withheld=600.0)
        v59_pubs, v59_blocked = _run_on(acts, "demo.fk.none.v59", "v59")
        v60_pubs, v60_blocked = _run_on(acts, "demo.fk.none.v60", "v60")
        self.assertEqual(_values(v60_pubs), _values(v59_pubs))
        self.assertEqual(_blocks(v60_blocked), _blocks(v59_blocked))

    def test_a_v59_log_adopted_onto_v60_keeps_the_resolved_values(self) -> None:
        acts = _splice(_unemployment_return(withheld=600.0), box4=0.0, omit=None)
        v59_pubs, v59_blocked = _run_on(acts, "demo.fk.adopted.v59", "v59")
        adopted = _append_v60(_finish_on(acts, "demo.fk.adopted.log", "v59"))
        v60_pubs, v60_blocked = _run_finished(adopted, "demo.fk.adopted.v60", SURFACE_V60)
        self.assertEqual(_values(v60_pubs), _values(v59_pubs))
        self.assertEqual(_blocks(v60_blocked), _blocks(v59_blocked))

    def test_v59_still_publishes_downstream_lines_when_the_1099k_is_unresolved(self) -> None:
        # Pre-existing gap. Core v59 is immutable: an unresolved Form 1099-K does
        # not stop the lines that read additional income. v60 is the successor
        # that blocks them. This pins the gap as it is.
        acts = _splice(_unemployment_return(withheld=600.0), box4=150.0, omit=None)
        pubs, _blocked = _run_on(acts, "demo.fk.gap.v59", "v59")
        for symbol in _GAP_LINES:
            self.assertIn(symbol, pubs, symbol)


_LINE32 = "tax.us.2025.payments.line32"
# Schedule 1 line 10 and every line from 8 to 24 and 32 to 37 that waits behind it.
_WAITING = (_LINE10, _LINE32) + _STOPPED


class UnclosedForm1099KFamilyBlocksLine10(unittest.TestCase):
    """The filer has not said whether every Form 1099-K is recorded."""

    def _assert_waits_for_the_closure(self, statements: list[tuple[float, str | None]], run_id: str) -> None:
        acts = _splice_many(_unemployment_return(withheld=600.0), statements=statements, closed=False)
        v59_pubs, _ = _run_on(acts, run_id + ".v59", "v59")
        v60_pubs, v60_blocked = _run_on(acts, run_id + ".v60", "v60")
        line10 = _row(v60_blocked, _RULE_LINE10)
        self.assertEqual(line10["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(list(line10["missing"]), [_FAMILY])
        for symbol in _WAITING:
            self.assertNotIn(symbol, v60_pubs, symbol)
        # Pre-existing gap on immutable v59: line 10 and everything below it publish.
        for symbol in _WAITING:
            self.assertIn(symbol, v59_pubs, symbol)

    def test_no_statement_and_no_closure_waits(self) -> None:
        self._assert_waits_for_the_closure([], "demo.fk.unclosed.none")

    def test_a_supported_statement_without_the_closure_waits(self) -> None:
        self._assert_waits_for_the_closure([(0.0, None)], "demo.fk.unclosed.supported")


class MixedForm1099KStatements(unittest.TestCase):
    def _assert_unresolved_blocks(self, statements: list[tuple[float, str | None]], run_id: str) -> None:
        acts = _splice_many(_unemployment_return(withheld=600.0), statements=statements)
        v60_pubs, v60_blocked = _run_on(acts, run_id + ".v60", "v60")
        line10 = _row(v60_blocked, _RULE_LINE10)
        self.assertEqual(line10["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(list(line10["missing"]), [_UNRESOLVED])
        for symbol in _WAITING:
            self.assertNotIn(symbol, v60_pubs, symbol)

    def test_a_supported_then_an_unresolved_statement_blocks(self) -> None:
        self._assert_unresolved_blocks([(0.0, None), (150.0, None)], "demo.fk.mix.su")

    def test_an_unresolved_then_a_supported_statement_blocks(self) -> None:
        self._assert_unresolved_blocks([(150.0, None), (0.0, None)], "demo.fk.mix.us")

    def test_two_supported_statements_publish_the_v59_values(self) -> None:
        acts = _splice_many(_unemployment_return(withheld=600.0), statements=[(0.0, None), (0.0, None)])
        v59_pubs, v59_blocked = _run_on(acts, "demo.fk.mix.ss.v59", "v59")
        v60_pubs, v60_blocked = _run_on(acts, "demo.fk.mix.ss.v60", "v60")
        self.assertEqual(_values(v60_pubs), _values(v59_pubs))
        self.assertEqual(_blocks(v60_blocked), _blocks(v59_blocked))


class SocialSecurityWithholdingOnV60(unittest.TestCase):
    def test_form_ssa_1099_withholding_equals_v59(self) -> None:
        acts = _social_security_return(withheld=800.0)
        v59_pubs, v59_blocked = _run_on(acts, "demo.fk.ssa.v59", "v59")
        v60_pubs, v60_blocked = _run_on(acts, "demo.fk.ssa.v60", "v60")
        self.assertEqual(_values(v60_pubs), _values(v59_pubs))
        self.assertEqual(_blocks(v60_blocked), _blocks(v59_blocked))
        self.assertEqual(str(v60_pubs[_LINE25B]["value"]), "800")


if __name__ == "__main__":
    unittest.main()
