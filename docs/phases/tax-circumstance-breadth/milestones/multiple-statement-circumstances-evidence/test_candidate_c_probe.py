"""Candidate C execution probe: Adopted subtotal and selection pattern check.

Purpose: Candidate C adopted subtotal and selection pattern check.
Measures actual runner scheduling, aggregation, and coverage behavior for multiple
Form 1099-K statements under Candidate C (adopted SLI subtotal and selection pattern):
1. Case 1: Both subjects publish supported-loss (A: 880.0, B: 460.0 -> 1340.0).
   Measures forward scheduling producer-first and exact pins (subtotal pins both Box 1a
   member findings; top-entry pins subtotal finding and both derived reason findings).
2. Case 2: Both subjects publish supported-loss, forward consumer-first.
   Measures that declared reads_subject_results enforces producer wait, preventing Cycle 0 block.
3. Case 3: Both subjects publish supported-loss, reference runner.
   Measures demand-driven traversal via demand_names.
4. Case 4: A publishes supported-loss; B blocks after answer withdrawal.
   Measures that B's blocked determination refuses DEPENDENCY_INVALID naming B's fact ID,
   curing the P5 defect (B's 460.0 is NOT summed into the total).
5. Case 5: A publishes supported-loss; B publishes a named unknown (cost-basis-unknown).
   Measures that top-entry blocks DEPENDENCY_ABSENT without summing.
6. Case 6: Closed-empty family.
   Measures that default path publishes 0 for closed-empty family.
7. Case 7: Missing closure boundaries.
   7a: Statements present, unclosed -> blocks SOURCE_SET_UNCLOSED.
   7b: Empty family, unclosed -> blocks SOURCE_SET_UNCLOSED (never derives 0).
8. Case 8: Fractional value compatibility.
   Measures that unrounded add(collect) preserves exact cents (880.50 + 460.25 -> 1340.75).

Stipulated Producer Note:
The diagnostic reason producer is fault/producer-state instrumentation joining
the existing cost-basis-known answer to emit stipulated categories:
- 'yes' -> supported-loss
- 'cannot-tell' -> cost-basis-unknown
- withdrawn ('not-asked' declared default) -> block DEPENDENCY_ABSENT
These stipulated categories isolate producer states and do not constitute
validated tax advice or production rule logic.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
from typing import Any, cast
import unittest
from unittest.mock import patch

_REPO_ROOT = Path(__file__).resolve().parents[5]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import pytest

from packages.derivation import live
from packages.derivation.evaluator import BLOCK_CLOSURE
from packages.derivation.live import _ResolvedRunMaterial, live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import citizen_checksum, package_instance_checksum
from packages.derivation.production_resolver import PublicationSurface
from packages.derivation.reference_runner import run_reference
from packages.derivation.runner import _Run
from packages.kernel.act_log import ActLog
from packages.kernel.facts import fact_id_for
from packages.tax.f1099k_statement_recording import (
    record_f1099k_no_statements_durably,
    record_f1099k_statement_durably,
    withdraw_f1099k_statement_answer_durably,
)
from packages.tax.f1099k_statement_review import (
    prepare_f1099k_statement_review,
    save_f1099k_statement_review,
)
from packages.tax.loader import tax_registry
from tests.test_f1098_mortgage_interest_line12e_track2 import _load_fixture_adoption
from tests.test_f1099k_personal_item_sale_track1 import (
    CONTENT,
    PACKAGE_PATH,
    REGISTRY_PATH,
    RELEASE_PATH,
    ROOT,
    SCOPE,
    TOP_ENTRY_SYMBOL,
    USER,
    _finish_acts,
    _make_base_acts,
)
from tests.test_f1099k_statement_recording import BASE_ANSWERS, _evidence_ids
from tools.generate_ssa_no_activity_content import _bytes

REASON_RULE_ID = "tax.us.2025.rule.f1099k-statement-loss-reason"
REASON_SYMBOL = "tax.us.2025.f1099k.statement-loss-reason"
TOP_ENTRY_RULE_ID = "tax.us.2025.rule.schedule1-top-entry"
SUBTOTAL_RULE_ID = "tax.us.2025.rule.f1099k-box1a-subtotal"
SUBTOTAL_SYMBOL = "tax.us.2025.f1099k.box1a-subtotal"
BOX1A_SYMBOL = "tax.us.2025.f1099k.box1a-gross-amount"
COST_BASIS_KNOWN_SYMBOL = "tax.us.2025.f1099k.cost-basis-known"
FAMILY_ID = "tax.us.2025.f1099k"
INERT_FACT_TYPE = "tax.us.2025.f1099k.inert-path-unwritten"


def _box1a_fact_id(keys: dict[str, str]) -> str:
    return fact_id_for(BOX1A_SYMBOL, tuple(sorted(keys.items())))


class DisposableCandidateCSurface:
    """Disposable rechecksummed package surface implementing Candidate C."""

    def __init__(self, root: Path) -> None:
        self.members = root / "members"
        self.releases = root / "releases"
        self.members.mkdir(parents=True)
        self.releases.mkdir(parents=True)
        for source in CONTENT.glob("*.json"):
            shutil.copyfile(source, self.members / source.name)
        release_name = RELEASE_PATH.name
        shutil.copyfile(RELEASE_PATH, self.releases / release_name)
        self.adoption = _load_fixture_adoption()
        self._seal(release_name)
        self.surface = PublicationSurface(self.releases, self.members / REGISTRY_PATH.name, self.members)

    def _seal(self, release_name: str) -> None:
        package = json.loads(PACKAGE_PATH.read_text("utf-8"))
        registry = json.loads(REGISTRY_PATH.read_text("utf-8"))

        # 1. Build diagnostic reason producer (stipulated categories)
        diagnostic_producer = {
            "schema": "rule-artifact.v14",
            "id": REASON_RULE_ID,
            "version": "v3",
            "scope": {
                "tax_year": 2025,
                "jurisdiction": "US-federal",
                "family": "individual-income-tax",
            },
            "role": "computation",
            "subject": {
                "id": BOX1A_SYMBOL,
                "version": "v1",
            },
            "requires": [
                BOX1A_SYMBOL,
                COST_BASIS_KNOWN_SYMBOL,
            ],
            "joined": {"id": COST_BASIS_KNOWN_SYMBOL, "version": "v1"},
            "direction": "joined_contains_subject",
            "pins": [],
            "when": True,
            "value": {
                "op": "choose",
                "when": {
                    "op": "categorical_compare",
                    "cmp": "eq",
                    "left": {
                        "op": "ref",
                        "name": COST_BASIS_KNOWN_SYMBOL,
                    },
                    "right": {"op": "category_literal", "fact_type": {"id": COST_BASIS_KNOWN_SYMBOL, "version": "v1"}, "value": "yes"},
                },
                "then": {
                    "op": "category_literal",
                    "fact_type": {
                        "id": REASON_SYMBOL,
                        "version": "v2",
                    },
                    "value": "supported-loss",
                },
                "else": {
                    "op": "choose",
                    "when": {
                        "op": "categorical_compare",
                        "cmp": "eq",
                        "left": {
                            "op": "ref",
                            "name": COST_BASIS_KNOWN_SYMBOL,
                        },
                        "right": {"op": "category_literal", "fact_type": {"id": COST_BASIS_KNOWN_SYMBOL, "version": "v1"}, "value": "cannot-tell"},
                    },
                    "then": {
                        "op": "category_literal",
                        "fact_type": {
                            "id": REASON_SYMBOL,
                            "version": "v2",
                        },
                        "value": "cost-basis-unknown",
                    },
                    "else": {
                        "op": "block",
                        "code": "DEPENDENCY_ABSENT",
                    },
                },
            },
            "publishes": REASON_SYMBOL,
            "blocked": {
                "code": "DEPENDENCY_ABSENT",
                "missing": [
                    COST_BASIS_KNOWN_SYMBOL,
                ],
            },
            "citations": [],
            "notes": "P7 Candidate C diagnostic producer only: stipulated category instrumentation.",
        }
        (self.members / "rule.f1099k-statement-loss-reason.v3.json").write_bytes(_bytes(diagnostic_producer))

        # 2. Build raw Box 1a subtotal rule (plain add(collect), unrounded)
        subtotal_rule = {
            "schema": "rule-artifact.v14",
            "id": SUBTOTAL_RULE_ID,
            "version": "v1",
            "scope": {
                "tax_year": 2025,
                "jurisdiction": "US-federal",
                "family": "individual-income-tax",
            },
            "role": "computation",
            "requires": [],
            "pins": [],
            "when": True,
            "value": {
                "op": "add",
                "args": [
                    {
                        "op": "collect",
                        "source_set": FAMILY_ID,
                        "name": BOX1A_SYMBOL,
                    }
                ],
            },
            "publishes": SUBTOTAL_SYMBOL,
            "blocked": {
                "code": "DEPENDENCY_INVALID",
                "missing": [],
            },
            "citations": [],
            "notes": "Candidate C: Raw unrounded sum of Form 1099-K Box 1a family under ADR-0016 collect authority.",
        }
        (self.members / "rule.f1099k-box1a-subtotal.json").write_bytes(_bytes(subtotal_rule))

        # 3. Build successor top-entry rule (two-path selection, requiring subtotal scalar)
        top_entry = {
            "schema": "rule-artifact.v14",
            "id": TOP_ENTRY_RULE_ID,
            "version": "v2",
            "scope": {
                "tax_year": 2025,
                "jurisdiction": "US-federal",
                "family": "individual-income-tax",
            },
            "role": "computation",
            "requires": [],
            "pins": [],
            "when": True,
            "selection": {
                "mode": "exclusive_presence",
                "conflict": "refuse",
                "paths": [
                    {
                        "id": "statements",
                        "activity": {
                            "kind": "source_nonempty",
                            "source_family": {
                                "id": FAMILY_ID,
                                "version": "v2",
                            },
                            "member_fact_types": [
                                {
                                    "id": BOX1A_SYMBOL,
                                    "version": "v1",
                                }
                            ],
                        },
                        "reads_subject_results": [
                            {
                                "symbol": REASON_SYMBOL,
                                "subject": {
                                    "id": BOX1A_SYMBOL,
                                    "version": "v1",
                                },
                            }
                        ],
                        "requires": [
                            SUBTOTAL_SYMBOL,
                        ],
                        "pins": [
                            {
                                "id": SUBTOTAL_SYMBOL,
                                "role": "input",
                                "version": "v1",
                                "origin": "assertion",
                            }
                        ],
                        "when": {
                            "op": "require_closed",
                            "source_set": FAMILY_ID,
                        },
                        "value": {
                            "op": "choose",
                            "when": {
                                "op": "collect_categorical_all_equal",
                                "name": REASON_SYMBOL,
                                "value": {
                                    "op": "category_literal",
                                    "fact_type": {
                                        "id": REASON_SYMBOL,
                                        "version": "v2",
                                    },
                                    "value": "supported-loss",
                                },
                            },
                            "then": {
                                "op": "ref",
                                "name": SUBTOTAL_SYMBOL,
                            },
                            "else": {
                                "op": "block",
                                "code": "DEPENDENCY_ABSENT",
                            },
                        },
                    },
                    {
                        "id": "inert",
                        "activity": {
                            "kind": "source_nonempty",
                            "member_fact_types": [
                                {
                                    "id": INERT_FACT_TYPE,
                                    "version": "v1",
                                }
                            ],
                        },
                        "reads_subject_results": [],
                        "requires": [],
                        "pins": [],
                        "when": True,
                        "value": {
                            "op": "block",
                            "code": "DEPENDENCY_INVALID",
                        },
                    },
                ],
                "default": {
                    "id": "neither",
                    "reads_subject_results": [],
                    "requires": [],
                    "pins": [],
                    "when": {
                        "op": "require_closed",
                        "source_set": FAMILY_ID,
                    },
                    "value": {
                        "op": "choose",
                        "when": {
                            "op": "compare",
                            "cmp": "eq",
                            "left": {
                                "op": "count",
                                "name": BOX1A_SYMBOL,
                                "source_set": FAMILY_ID,
                            },
                            "right": 0,
                        },
                        "then": 0,
                        "else": {
                            "op": "block",
                            "code": "DEPENDENCY_INVALID",
                        },
                    },
                },
                "refusal": {
                    "code": "DEPENDENCY_INVALID",
                    "missing": [
                        "f1099k-inert-path-conflict",
                    ],
                    "pins": [],
                },
            },
            "publishes": TOP_ENTRY_SYMBOL,
            "blocked": {
                "code": "DEPENDENCY_INVALID",
                "missing": [],
            },
            "citations": [],
            "notes": "Candidate C top entry: Two-path selection requiring raw subtotal and reading subject reasons.",
        }
        (self.members / "rule.schedule1-top-entry.v2.json").write_bytes(_bytes(top_entry))

        # 4. Build successor family v2 authorizing subtotal
        fam = json.loads((CONTENT / "family.f1099k.json").read_text("utf-8"))
        fam["version"] = "v2"
        fam["authorizes_subtotal"] = SUBTOTAL_SYMBOL
        fam["closure_claim"] = (
            "Every personal item sale amount reported in box 1a of a Form 1099-K furnished to the taxpayer "
            "for tax year 2025 is recorded as a statement item as of the keyed horizon. Closed with members "
            "authorizes the sum of current members; closed-empty authorizes subtotal 0."
        )
        (self.members / "family.f1099k.json").write_bytes(_bytes(fam))

        # 5. Build successor closure-mapping v2 admitting subtotal
        mapping = json.loads((CONTENT / "closure-mapping.f1099k.json").read_text("utf-8"))
        mapping["version"] = "v2"
        mapping["family"] = {"id": FAMILY_ID, "version": "v2"}
        mapping["admits_symbol"] = SUBTOTAL_SYMBOL
        (self.members / "closure-mapping.f1099k.json").write_bytes(_bytes(mapping))

        # 6. Update adopted consumers pinning family v1:
        # a) Attachment rule: update family pin to v2 and subtotal_symbol / tie_out to subtotal
        att = json.loads((CONTENT / "rule.attachment.schedule-1.v3.json").read_text("utf-8"))
        for item in att.get("itemizations", []):
            if item.get("authority", {}).get("source_family", {}).get("id") == FAMILY_ID:
                item["authority"]["source_family"]["version"] = "v2"
                for rs in item.get("row_sets", []):
                    rs["rows"]["source_family"]["version"] = "v2"
                    rs["subtotal_symbol"] = SUBTOTAL_SYMBOL
                item["tie_out"]["line_symbol"] = SUBTOTAL_SYMBOL
        (self.members / "rule.attachment.schedule-1.v3.json").write_bytes(_bytes(att))

        # b) Unresolved rule: update path activity source_family pin to v2
        unres = json.loads((CONTENT / "rule.f1099k-unresolved.v2.json").read_text("utf-8"))
        for p in unres.get("selection", {}).get("paths", []):
            if p.get("activity", {}).get("source_family", {}).get("id") == FAMILY_ID:
                p["activity"]["source_family"]["version"] = "v2"
        (self.members / "rule.f1099k-unresolved.v2.json").write_bytes(_bytes(unres))

        # 7. Update package members list: add subtotal rule, update versions
        package["members"].append({
            "id": SUBTOTAL_RULE_ID,
            "role": "computation",
            "schema": "rule-artifact.v14",
            "version": "v1",
        })
        for m in package["members"]:
            if m["id"] == FAMILY_ID:
                m["version"] = "v2"
            elif m["id"] == "tax.us.2025.closure-mapping.f1099k":
                m["version"] = "v2"

        # 8. Update registry citizens and checksums
        checksum_producer = citizen_checksum(diagnostic_producer)
        checksum_subtotal = citizen_checksum(subtotal_rule)
        checksum_top_entry = citizen_checksum(top_entry)
        checksum_fam = citizen_checksum(fam)
        checksum_mapping = citizen_checksum(mapping)
        checksum_att = citizen_checksum(att)
        checksum_unres = citizen_checksum(unres)

        registry["citizens"].append({
            "id": SUBTOTAL_RULE_ID,
            "role": "computation",
            "schema": "rule-artifact.v14",
            "version": "v1",
            "checksum": checksum_subtotal,
        })
        for citizen in registry["citizens"]:
            cid = citizen["id"]
            if cid == REASON_RULE_ID and citizen.get("version") == "v3":
                citizen["checksum"] = checksum_producer
            elif cid == TOP_ENTRY_RULE_ID and citizen.get("version") == "v2":
                citizen["checksum"] = checksum_top_entry
            elif cid == FAMILY_ID and citizen.get("version") == "v1":
                citizen["version"] = "v2"
                citizen["checksum"] = checksum_fam
            elif cid == "tax.us.2025.closure-mapping.f1099k" and citizen.get("version") == "v1":
                citizen["version"] = "v2"
                citizen["checksum"] = checksum_mapping
            elif cid == "tax.us.2025.rule.attachment.schedule-1" and citizen.get("version") == "v3":
                citizen["checksum"] = checksum_att
            elif cid == "tax.us.2025.rule.f1099k-unresolved" and citizen.get("version") == "v2":
                citizen["checksum"] = checksum_unres

        # 9. Seal package and registry
        package["package_checksum"] = package_instance_checksum(package)
        (self.members / PACKAGE_PATH.name).write_bytes(_bytes(package))

        for entry in registry["packages"]:
            if entry["id"] == package["id"] and entry["version"] == package["version"]:
                entry["checksum"] = package["package_checksum"]

        registry_bytes = _bytes(registry)
        (self.members / REGISTRY_PATH.name).write_bytes(registry_bytes)

        # 10. Seal release
        release = json.loads((self.releases / release_name).read_text("utf-8"))
        release["package_registry_sha256"] = hashlib.sha256(registry_bytes).hexdigest()
        release_bytes = _bytes(release)
        (self.releases / release_name).write_bytes(release_bytes)

        # 11. Update adoption act payload
        payload = cast(dict[str, Any], self.adoption["payload"])
        payload["package"]["id"] = package["id"]
        payload["package"]["version"] = package["version"]
        payload["package"]["checksum"] = package["package_checksum"]
        payload["release"]["id"] = release["id"]
        payload["release"]["version"] = release["version"]
        payload["release"]["checksum"] = hashlib.sha256(release_bytes).hexdigest()


def _prepare_adoption(disposable: DisposableCandidateCSurface, log: ActLog, act_id: str) -> dict[str, Any]:
    adoption = copy.deepcopy(disposable.adoption)
    adoption["act_id"] = act_id
    adoption["committed_against"] = log.read().revision
    adoption["actor"] = USER
    adoption["at"] = "2026-10-18T12:25:00Z"
    cast(dict[str, Any], adoption["payload"])["revision"] = 30
    return adoption


def _read_durable_output(outcome: Any) -> dict[str, Any]:
    if outcome.output_path is None:
        raise AssertionError("successful coordinator run did not provide an output path")
    return cast(dict[str, Any], json.loads(outcome.output_path.read_text("utf-8")))


def _reordered_material_context(order: str) -> Any:
    """Wrapper around live._resolved_run_material to control rule attempt sequence."""
    original_material_fn = live._resolved_run_material

    def _wrapped_material(graph: Any) -> _ResolvedRunMaterial:
        mat = original_material_fn(graph)
        rules = list(mat[0])
        reason_rule = next((r for r in rules if r.get("id") == REASON_RULE_ID), None)
        top_rule = next((r for r in rules if r.get("id") == TOP_ENTRY_RULE_ID), None)
        if reason_rule is not None and top_rule is not None:
            rules.remove(reason_rule)
            rules.remove(top_rule)
            if order == "producer_first":
                rules.insert(0, reason_rule)
                rules.insert(1, top_rule)
            elif order == "consumer_first":
                rules.insert(0, top_rule)
                rules.insert(1, reason_rule)
            else:
                raise ValueError(f"Unknown rule order: {order}")
        return _ResolvedRunMaterial(
            rules=rules,
            parameters=mat[1],
            families=mat[2],
            mappings=mat[3],
            fact_types=mat[4],
            bindings=mat[5],
            collect_names=mat[6],
            emission_only_names=list(mat.emission_only_names),
            parameter_index=mat.parameter_index,
        )

    return patch.object(live, "_resolved_run_material", side_effect=_wrapped_material)


class ExecutionObserver:
    """Instruments _Run.attempt to observe when top-entry is attempted relative to producer."""

    def __init__(self) -> None:
        self.attempts: list[dict[str, Any]] = []
        self.top_entry_attempted_after_producer: bool | None = None
        self.top_entry_attempt_outcome: str | None = None

    def __enter__(self) -> ExecutionObserver:
        orig_attempt = _Run.attempt
        observer = self

        def _monitored_attempt(run_self: _Run, rule: dict[str, Any]) -> str:
            rule_id = str(rule.get("id", ""))
            producer_resolved_before = REASON_RULE_ID in run_self.resolved
            outcome = orig_attempt(run_self, rule)
            observer.attempts.append({
                "rule_id": rule_id,
                "producer_resolved_before": producer_resolved_before,
                "outcome": outcome,
            })
            if rule_id == TOP_ENTRY_RULE_ID and observer.top_entry_attempted_after_producer is None:
                observer.top_entry_attempted_after_producer = producer_resolved_before
                observer.top_entry_attempt_outcome = outcome
            return outcome

        self._patcher = patch.object(_Run, "attempt", new=_monitored_attempt)
        self._patcher.start()
        return self

    def __exit__(self, *args: Any) -> None:
        self._patcher.stop()


def _record_two_statements(
    log: ActLog,
    registry: Any,
    *,
    box1a_a: float = 880.0,
    box1a_b: float = 460.0,
    b_cost_basis_known: str = "yes",
    withdraw_b_cost_basis: bool = False,
    close_family_b: bool = True,
) -> tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str], str | None]:
    """Record two statements: A and B.

    Returns (keys_a, keys_b, findings_a, findings_b, withdrawn_finding_id).
    """
    answers_a = {**BASE_ANSWERS, "cost-basis-known": "yes"}
    answers_b = {**BASE_ANSWERS, "cost-basis-known": b_cost_basis_known}

    # Statement A
    report_a = record_f1099k_statement_durably(
        log, registry, payer_id="demo.platform.alpha", statement_ref="demo.statement.bicycle",
        box1a=box1a_a, box4=0.0, submission_id="demo.c.report.0", evidence_id="demo.c.evidence.0",
        actor=USER, at="2026-10-18T12:00:00Z", expected_revision=log.read().revision,
    )
    keys_a = report_a["statement_keys"]
    review_a = prepare_f1099k_statement_review(
        log, registry, review_id="demo.c.review.0", shown_at="2026-10-18T12:00:30Z", statement_keys=keys_a,
    )
    save_f1099k_statement_review(
        log, registry, review_a, answers=answers_a, submission_id="demo.c.answers.0",
        evidence_ids=_evidence_ids(answers_a, "demo.c.answer-evidence.0"),
        actor=USER, at="2026-10-18T12:10:00Z",
    )
    saved_review_a = prepare_f1099k_statement_review(
        log, registry, review_id="demo.c.saved-review.0", shown_at="2026-10-18T12:15:00Z", statement_keys=keys_a,
    )
    findings_a = {k: v["finding_id"] for k, v in saved_review_a["questions"].items()}

    # Statement B
    report_b = record_f1099k_statement_durably(
        log, registry, payer_id="demo.platform.beta", statement_ref="demo.statement.camera",
        box1a=box1a_b, box4=0.0, submission_id="demo.c.report.1", evidence_id="demo.c.evidence.1",
        actor=USER, at="2026-10-18T12:01:00Z", expected_revision=log.read().revision,
        close_family=close_family_b,
    )
    keys_b = report_b["statement_keys"]
    review_b = prepare_f1099k_statement_review(
        log, registry, review_id="demo.c.review.1", shown_at="2026-10-18T12:01:30Z", statement_keys=keys_b,
    )
    save_f1099k_statement_review(
        log, registry, review_b, answers=answers_b, submission_id="demo.c.answers.1",
        evidence_ids=_evidence_ids(answers_b, "demo.c.answer-evidence.1"),
        actor=USER, at="2026-10-18T12:11:00Z",
    )
    saved_review_b = prepare_f1099k_statement_review(
        log, registry, review_id="demo.c.saved-review.1", shown_at="2026-10-18T12:15:01Z", statement_keys=keys_b,
    )
    findings_b = {k: v["finding_id"] for k, v in saved_review_b["questions"].items()}

    withdrawn_finding_id: str | None = None
    if withdraw_b_cost_basis:
        withdrawn_finding_id = findings_b["cost-basis-known"]
        withdraw_f1099k_statement_answer_durably(
            log, registry, current_findings=[withdrawn_finding_id],
            submission_id="demo.c.withdraw.b-cost-basis", actor=USER,
            at="2026-10-18T12:20:00Z", expected_revision=log.read().revision,
        )

    return keys_a, keys_b, findings_a, findings_b, withdrawn_finding_id


@pytest.mark.live(reason="durable multi-statement recording plus coordinator run exceeds the fast-lane budget")
class CandidateCProbe(unittest.TestCase):
    def test_case1_both_supported_forward_producer_first(self) -> None:
        """Case 1: Both subjects publish supported-loss.

        Measures:
        - Top-entry publishes 1340.0.
        - Exact subtotal pin: subtotal pins both Box 1a member transitions (role=input, v1, assertion).
        - Exact top-entry pins: pins subtotal finding (role=input, v1, assertion) and both
          reason findings (role=input, v2, origin=derived).
        - No forced flattening of Box 1a member pins onto top entry.
        """
        with TemporaryDirectory(prefix="demo.c.case1-") as temp:
            workspace = Path(temp) / "workspace"
            registry = tax_registry()
            log = ActLog(workspace, registry)
            log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)
            keys_a, keys_b, _, _, _ = _record_two_statements(log, registry, b_cost_basis_known="yes")

            disposable = DisposableCandidateCSurface(Path(temp) / "surface")
            adoption = _prepare_adoption(disposable, log, "demo.c.adoption.case1")
            log.append(adoption, expected_revision=log.read().revision)

            acts = log.read().acts
            capability = WorkspaceCapability(workspace)

            with _reordered_material_context("producer_first"), ExecutionObserver() as obs:
                run_out = live_coordinate_run(
                    capability, repo_root=ROOT, authoritative_acts=acts, workspace_revision=len(acts),
                    run_scope=SCOPE, scope_user=USER, request={"schema": "run-request.v1"},
                    run_id="demo.c.run.case1.producer-first", governance_pins=[], surface=disposable.surface,
                    output_name="case1-prod-first.json",
                )
            self.assertIsNone(run_out.refusal)
            self.assertTrue(obs.top_entry_attempted_after_producer)
            self.assertEqual(obs.top_entry_attempt_outcome, "published")

            findings = [pub.finding for pub in run_out.publications or ()]

            # 1. Verify subtotal published finding
            subtotal_finding = next((f for f in findings if f.get("symbol") == SUBTOTAL_SYMBOL), None)
            self.assertIsNotNone(subtotal_finding)
            assert subtotal_finding is not None
            self.assertEqual(subtotal_finding["value"], "1340.0")

            # Subtotal pins both Box 1a member transitions (role=input, version=v1, origin=assertion)
            subtotal_pins = subtotal_finding.get("pins", [])
            box1a_acts = [
                act for act in acts
                if act.get("kind") == "member-transition"
                and isinstance(act.get("payload"), dict)
                and isinstance(act["payload"].get("member"), dict)
                and act["payload"]["member"].get("action") == "assert"
                and isinstance(act["payload"]["member"].get("finding"), dict)
                and BOX1A_SYMBOL in act["payload"]["member"]["finding"].get("fact_id", "")
            ]
            self.assertEqual(len(box1a_acts), 2)
            subtotal_pinned_ids = {p["id"] for p in subtotal_pins}
            for b_act in box1a_acts:
                b_fid = b_act["payload"]["member"]["finding"]["id"]
                self.assertIn(b_fid, subtotal_pinned_ids)
                pin = next(p for p in subtotal_pins if p["id"] == b_fid)
                self.assertEqual(pin["role"], "input")
                self.assertEqual(pin["version"], "v1")
                self.assertEqual(pin.get("origin"), "assertion")

            # 2. Verify top entry published finding
            top_finding = next((f for f in findings if f.get("symbol") == TOP_ENTRY_SYMBOL), None)
            self.assertIsNotNone(top_finding)
            assert top_finding is not None
            self.assertEqual(top_finding["value"], "1340.0")

            top_pins = top_finding.get("pins", [])
            top_pinned_ids = {p["id"] for p in top_pins}

            # Top entry pins the subtotal finding (role=input, version=v2, origin=assertion)
            self.assertIn(subtotal_finding["id"], top_pinned_ids)
            sub_pin = next(p for p in top_pins if p["id"] == subtotal_finding["id"])
            self.assertEqual(sub_pin["role"], "input")
            self.assertEqual(sub_pin["version"], "v2")
            self.assertEqual(sub_pin.get("origin"), "assertion")

            # Top entry does NOT duplicate Box 1a member pins (no forced flattening)
            for b_act in box1a_acts:
                b_fid = b_act["payload"]["member"]["finding"]["id"]
                self.assertNotIn(b_fid, top_pinned_ids)

            # Top entry pins both derived reasons (role=input, version=v2, origin=derived)
            reason_pubs = [f for f in findings if f.get("symbol", "").startswith(f"{REASON_SYMBOL}|")]
            self.assertEqual(len(reason_pubs), 2)
            self.assertEqual({r["value"] for r in reason_pubs}, {"supported-loss"})
            for r in reason_pubs:
                self.assertIn(r["id"], top_pinned_ids)
                r_pin = next(p for p in top_pins if p["id"] == r["id"])
                self.assertEqual(r_pin["role"], "input")
                self.assertEqual(r_pin["version"], "v2")
                self.assertEqual(r_pin.get("origin"), "derived")

    def test_case2_both_supported_forward_consumer_first(self) -> None:
        """Case 2: Both supported, forward consumer-first.

        Measures that reads_subject_results enforces producer wait in forward runner:
        the top entry is ineligible until the reason producer resolves.
        Publishes 1340.0 cleanly; no premature Cycle 0 failure.
        """
        with TemporaryDirectory(prefix="demo.c.case2-") as temp:
            workspace = Path(temp) / "workspace"
            registry = tax_registry()
            log = ActLog(workspace, registry)
            log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)
            _record_two_statements(log, registry, b_cost_basis_known="yes")

            disposable = DisposableCandidateCSurface(Path(temp) / "surface")
            adoption = _prepare_adoption(disposable, log, "demo.c.adoption.case2")
            log.append(adoption, expected_revision=log.read().revision)

            acts = log.read().acts
            capability = WorkspaceCapability(workspace)

            with _reordered_material_context("consumer_first"), ExecutionObserver() as obs:
                run_out = live_coordinate_run(
                    capability, repo_root=ROOT, authoritative_acts=acts, workspace_revision=len(acts),
                    run_scope=SCOPE, scope_user=USER, request={"schema": "run-request.v1"},
                    run_id="demo.c.run.case2.consumer-first", governance_pins=[], surface=disposable.surface,
                    output_name="case2-cons-first.json",
                )
            self.assertIsNone(run_out.refusal)
            # Declared reads_subject_results ensured top entry was not attempted until producer resolved!
            self.assertTrue(obs.top_entry_attempted_after_producer)
            self.assertEqual(obs.top_entry_attempt_outcome, "published")

            findings = [pub.finding for pub in run_out.publications or ()]
            top_finding = next((f for f in findings if f.get("symbol") == TOP_ENTRY_SYMBOL), None)
            self.assertIsNotNone(top_finding)
            assert top_finding is not None
            self.assertEqual(top_finding["value"], "1340.0")

    def test_case3_both_supported_reference_runner(self) -> None:
        """Case 3: Both supported, reference runner.

        Measures demand-driven traversal via demand_names.
        """
        with TemporaryDirectory(prefix="demo.c.case3-") as temp:
            workspace = Path(temp) / "workspace"
            registry = tax_registry()
            log = ActLog(workspace, registry)
            log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)
            _record_two_statements(log, registry, b_cost_basis_known="yes")

            disposable = DisposableCandidateCSurface(Path(temp) / "surface")
            adoption = _prepare_adoption(disposable, log, "demo.c.adoption.case3")
            log.append(adoption, expected_revision=log.read().revision)

            acts = log.read().acts
            capability = WorkspaceCapability(workspace)

            with patch("packages.derivation.production_executor._execute", side_effect=run_reference):
                run_ref = live_coordinate_run(
                    capability, repo_root=ROOT, authoritative_acts=acts, workspace_revision=len(acts),
                    run_scope=SCOPE, scope_user=USER, request={"schema": "run-request.v1"},
                    run_id="demo.c.run.case3.reference", governance_pins=[], surface=disposable.surface,
                    output_name="case3-reference.json",
                )
            self.assertIsNone(run_ref.refusal)
            findings_ref = [pub.finding for pub in run_ref.publications or ()]
            top_ref = next((f for f in findings_ref if f.get("symbol") == TOP_ENTRY_SYMBOL), None)
            self.assertIsNotNone(top_ref)
            assert top_ref is not None
            self.assertEqual(top_ref["value"], "1340.0")

    def test_case4_b_withdrawn_blocks_and_names_b(self) -> None:
        """Case 4: A supported, B withdrawn answer.

        Measures that B's blocked determination refuses DEPENDENCY_INVALID naming B's fact ID.
        Verifies that B's 460.0 is NOT summed into the total (P5 defect cured).
        """
        with TemporaryDirectory(prefix="demo.c.case4-") as temp:
            workspace = Path(temp) / "workspace"
            registry = tax_registry()
            log = ActLog(workspace, registry)
            log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)
            keys_a, keys_b, _, _, withdrawn_fid = _record_two_statements(
                log, registry, b_cost_basis_known="yes", withdraw_b_cost_basis=True,
            )
            self.assertIsNotNone(withdrawn_fid)

            disposable = DisposableCandidateCSurface(Path(temp) / "surface")
            adoption = _prepare_adoption(disposable, log, "demo.c.adoption.case4")
            log.append(adoption, expected_revision=log.read().revision)

            acts = log.read().acts
            capability = WorkspaceCapability(workspace)

            with _reordered_material_context("producer_first"), ExecutionObserver() as obs:
                run_out = live_coordinate_run(
                    capability, repo_root=ROOT, authoritative_acts=acts, workspace_revision=len(acts),
                    run_scope=SCOPE, scope_user=USER, request={"schema": "run-request.v1"},
                    run_id="demo.c.run.case4.forward", governance_pins=[], surface=disposable.surface,
                    output_name="case4-forward.json",
                )
            self.assertIsNone(run_out.refusal)
            self.assertTrue(obs.top_entry_attempted_after_producer)
            self.assertEqual(obs.top_entry_attempt_outcome, "blocked")

            findings = [pub.finding for pub in run_out.publications or ()]

            # Top entry must NOT be published
            self.assertFalse(any(f.get("symbol") == TOP_ENTRY_SYMBOL for f in findings))

            # A reason publishes supported-loss
            a_reason = next((f for f in findings if f.get("symbol") == f"{REASON_SYMBOL}|{_box1a_fact_id(keys_a)}"), None)
            self.assertIsNotNone(a_reason)
            assert a_reason is not None
            self.assertEqual(a_reason["value"], "supported-loss")

            # B reason publication is absent from publications
            self.assertFalse(any(f.get("symbol") == f"{REASON_SYMBOL}|{_box1a_fact_id(keys_b)}" for f in findings))

            # Durable output records:
            durable_data = _read_durable_output(run_out)

            # 1. B producer row: artifact_id REASON_RULE_ID, symbol REASON_SYMBOL + "|" + _box1a_fact_id(keys_b), blocked DEPENDENCY_ABSENT
            b_producer_disp = next(
                d for d in durable_data["dispositions"]
                if d.get("artifact_id") == REASON_RULE_ID and d.get("symbol") == f"{REASON_SYMBOL}|{_box1a_fact_id(keys_b)}"
            )
            self.assertEqual(b_producer_disp["disposition"], "blocked")
            self.assertEqual(b_producer_disp["code"], "DEPENDENCY_ABSENT")
            self.assertEqual(b_producer_disp.get("missing", []), [])

            # 2. Top entry: DEPENDENCY_INVALID blocked disposition naming B's Box 1a fact ID
            top_disp = next(d for d in durable_data["dispositions"] if d.get("artifact_id") == TOP_ENTRY_RULE_ID)
            self.assertEqual(top_disp["disposition"], "blocked")
            self.assertEqual(top_disp["code"], "DEPENDENCY_INVALID")
            b_fact_id = _box1a_fact_id(keys_b)
            self.assertIn(b_fact_id, top_disp.get("missing", []))

    def test_case5_b_published_unknown_refuses(self) -> None:
        """Case 5: A supported, B published unknown (cost-basis-unknown).

        Measures that top entry blocks DEPENDENCY_ABSENT without summing.
        """
        with TemporaryDirectory(prefix="demo.c.case5-") as temp:
            workspace = Path(temp) / "workspace"
            registry = tax_registry()
            log = ActLog(workspace, registry)
            log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)
            keys_a, keys_b, _, _, _ = _record_two_statements(log, registry, b_cost_basis_known="cannot-tell")

            disposable = DisposableCandidateCSurface(Path(temp) / "surface")
            adoption = _prepare_adoption(disposable, log, "demo.c.adoption.case5")
            log.append(adoption, expected_revision=log.read().revision)

            acts = log.read().acts
            capability = WorkspaceCapability(workspace)

            with _reordered_material_context("producer_first"), ExecutionObserver() as obs:
                run_out = live_coordinate_run(
                    capability, repo_root=ROOT, authoritative_acts=acts, workspace_revision=len(acts),
                    run_scope=SCOPE, scope_user=USER, request={"schema": "run-request.v1"},
                    run_id="demo.c.run.case5.forward", governance_pins=[], surface=disposable.surface,
                    output_name="case5-forward.json",
                )
            self.assertIsNone(run_out.refusal)
            self.assertTrue(obs.top_entry_attempted_after_producer)
            self.assertEqual(obs.top_entry_attempt_outcome, "blocked")

            findings = [pub.finding for pub in run_out.publications or ()]
            self.assertFalse(any(f.get("symbol") == TOP_ENTRY_SYMBOL for f in findings))

            # Exact keyed A supported and B cost-basis-unknown publications
            a_reason = next((f for f in findings if f.get("symbol") == f"{REASON_SYMBOL}|{_box1a_fact_id(keys_a)}"), None)
            self.assertIsNotNone(a_reason)
            assert a_reason is not None
            self.assertEqual(a_reason["value"], "supported-loss")

            b_reason = next((f for f in findings if f.get("symbol") == f"{REASON_SYMBOL}|{_box1a_fact_id(keys_b)}"), None)
            self.assertIsNotNone(b_reason)
            assert b_reason is not None
            self.assertEqual(b_reason["value"], "cost-basis-unknown")

            durable_data = _read_durable_output(run_out)
            top_disp = next(d for d in durable_data["dispositions"] if d.get("artifact_id") == TOP_ENTRY_RULE_ID)
            self.assertEqual(top_disp["disposition"], "blocked")
            self.assertEqual(top_disp["code"], "DEPENDENCY_ABSENT")

    def test_case6_closed_empty_publishes_zero(self) -> None:
        """Case 6: Closed-empty family.

        Measures that default path evaluates count == 0 and publishes 0.
        """
        with TemporaryDirectory(prefix="demo.c.case6-") as temp:
            workspace = Path(temp) / "workspace"
            registry = tax_registry()
            log = ActLog(workspace, registry)
            log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)
            record_f1099k_no_statements_durably(
                log, registry, submission_id="demo.c.no-statements", evidence_id="demo.c.evidence.none",
                actor=USER, at="2026-10-18T12:00:00Z", expected_revision=log.read().revision,
            )

            disposable = DisposableCandidateCSurface(Path(temp) / "surface")
            adoption = _prepare_adoption(disposable, log, "demo.c.adoption.case6")
            log.append(adoption, expected_revision=log.read().revision)

            acts = log.read().acts
            capability = WorkspaceCapability(workspace)

            run_out = live_coordinate_run(
                capability, repo_root=ROOT, authoritative_acts=acts, workspace_revision=len(acts),
                run_scope=SCOPE, scope_user=USER, request={"schema": "run-request.v1"},
                run_id="demo.c.run.case6.forward", governance_pins=[], surface=disposable.surface,
                output_name="case6-forward.json",
            )
            self.assertIsNone(run_out.refusal)
            findings = [pub.finding for pub in run_out.publications or ()]
            top_finding = next((f for f in findings if f.get("symbol") == TOP_ENTRY_SYMBOL), None)
            self.assertIsNotNone(top_finding)
            assert top_finding is not None
            self.assertEqual(top_finding["value"], "0")

            # Recover closure finding id from current log acts
            closure_acts = [
                act for act in acts
                if act.get("kind") == "assertion"
                and isinstance(act.get("payload"), dict)
                and isinstance(act["payload"].get("finding"), dict)
                and act["payload"]["finding"].get("fact_id", "").startswith(f"{FAMILY_ID}.source-closure|")
            ]
            self.assertEqual(len(closure_acts), 1)
            closure_finding_id = closure_acts[0]["payload"]["finding"]["id"]

            # Assert top_finding pins include actual recorded closure finding id plus package-role family/mapping pins at v2
            top_pins = top_finding.get("pins", [])
            top_pinned_ids = {p["id"] for p in top_pins}
            self.assertIn(closure_finding_id, top_pinned_ids)
            self.assertTrue(any(p.get("role") == "package" and p.get("id") == FAMILY_ID and p.get("version") == "v2" for p in top_pins))
            self.assertTrue(any(p.get("role") == "package" and p.get("id") == "tax.us.2025.closure-mapping.f1099k" and p.get("version") == "v2" for p in top_pins))

            # Durable disposition is published
            durable_data = _read_durable_output(run_out)
            top_disp = next(d for d in durable_data["dispositions"] if d.get("artifact_id") == TOP_ENTRY_RULE_ID)
            self.assertEqual(top_disp["disposition"], "published")

    def test_case7a_missing_closure_with_statements_blocks(self) -> None:
        """Case 7a: Statements present, unclosed.

        Measures that top-entry blocks with public code SOURCE_SET_UNCLOSED.
        """
        with TemporaryDirectory(prefix="demo.c.case7a-") as temp:
            workspace = Path(temp) / "workspace"
            registry = tax_registry()
            log = ActLog(workspace, registry)
            log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)
            _record_two_statements(log, registry, b_cost_basis_known="yes", close_family_b=False)

            disposable = DisposableCandidateCSurface(Path(temp) / "surface")
            adoption = _prepare_adoption(disposable, log, "demo.c.adoption.case7a")
            log.append(adoption, expected_revision=log.read().revision)

            acts = log.read().acts
            capability = WorkspaceCapability(workspace)

            run_out = live_coordinate_run(
                capability, repo_root=ROOT, authoritative_acts=acts, workspace_revision=len(acts),
                run_scope=SCOPE, scope_user=USER, request={"schema": "run-request.v1"},
                run_id="demo.c.run.case7a.forward", governance_pins=[], surface=disposable.surface,
                output_name="case7a-forward.json",
            )
            self.assertIsNone(run_out.refusal)
            findings = [pub.finding for pub in run_out.publications or ()]
            self.assertFalse(any(f.get("symbol") == TOP_ENTRY_SYMBOL for f in findings))

            durable_data = _read_durable_output(run_out)
            top_disp = next(d for d in durable_data["dispositions"] if d.get("artifact_id") == TOP_ENTRY_RULE_ID)
            self.assertEqual(top_disp["disposition"], "blocked")
            self.assertEqual(top_disp["code"], BLOCK_CLOSURE)
            self.assertIn(FAMILY_ID, top_disp.get("missing", []))

    def test_case7b_missing_closure_empty_family_blocks(self) -> None:
        """Case 7b: Empty family, unclosed.

        Measures that default path blocks SOURCE_SET_UNCLOSED; never derives 0 without closure.
        """
        with TemporaryDirectory(prefix="demo.c.case7b-") as temp:
            workspace = Path(temp) / "workspace"
            registry = tax_registry()
            log = ActLog(workspace, registry)
            log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)
            # No statements recorded, AND no source-closure recorded!

            disposable = DisposableCandidateCSurface(Path(temp) / "surface")
            adoption = _prepare_adoption(disposable, log, "demo.c.adoption.case7b")
            log.append(adoption, expected_revision=log.read().revision)

            acts = log.read().acts
            capability = WorkspaceCapability(workspace)

            run_out = live_coordinate_run(
                capability, repo_root=ROOT, authoritative_acts=acts, workspace_revision=len(acts),
                run_scope=SCOPE, scope_user=USER, request={"schema": "run-request.v1"},
                run_id="demo.c.run.case7b.forward", governance_pins=[], surface=disposable.surface,
                output_name="case7b-forward.json",
            )
            self.assertIsNone(run_out.refusal)
            findings = [pub.finding for pub in run_out.publications or ()]
            self.assertFalse(any(f.get("symbol") == TOP_ENTRY_SYMBOL for f in findings))

            durable_data = _read_durable_output(run_out)
            top_disp = next(d for d in durable_data["dispositions"] if d.get("artifact_id") == TOP_ENTRY_RULE_ID)
            self.assertEqual(top_disp["disposition"], "blocked")
            self.assertEqual(top_disp["code"], BLOCK_CLOSURE)
            self.assertIn(FAMILY_ID, top_disp.get("missing", []))

    def test_case8_fractional_value_compatibility(self) -> None:
        """Case 8: Fractional value compatibility.

        Measures that unrounded add(collect) preserves cents (880.50 + 460.25 -> 1340.75).
        """
        with TemporaryDirectory(prefix="demo.c.case8-") as temp:
            workspace = Path(temp) / "workspace"
            registry = tax_registry()
            log = ActLog(workspace, registry)
            log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)
            _record_two_statements(log, registry, box1a_a=880.50, box1a_b=460.25, b_cost_basis_known="yes")

            disposable = DisposableCandidateCSurface(Path(temp) / "surface")
            adoption = _prepare_adoption(disposable, log, "demo.c.adoption.case8")
            log.append(adoption, expected_revision=log.read().revision)

            acts = log.read().acts
            capability = WorkspaceCapability(workspace)

            run_out = live_coordinate_run(
                capability, repo_root=ROOT, authoritative_acts=acts, workspace_revision=len(acts),
                run_scope=SCOPE, scope_user=USER, request={"schema": "run-request.v1"},
                run_id="demo.c.run.case8.forward", governance_pins=[], surface=disposable.surface,
                output_name="case8-forward.json",
            )
            self.assertIsNone(run_out.refusal)
            findings = [pub.finding for pub in run_out.publications or ()]

            subtotal_finding = next((f for f in findings if f.get("symbol") == SUBTOTAL_SYMBOL), None)
            self.assertIsNotNone(subtotal_finding)
            assert subtotal_finding is not None
            self.assertEqual(subtotal_finding["value"], "1340.75")

            top_finding = next((f for f in findings if f.get("symbol") == TOP_ENTRY_SYMBOL), None)
            self.assertIsNotNone(top_finding)
            assert top_finding is not None
            self.assertEqual(top_finding["value"], "1340.75")


if __name__ == "__main__":
    unittest.main()
