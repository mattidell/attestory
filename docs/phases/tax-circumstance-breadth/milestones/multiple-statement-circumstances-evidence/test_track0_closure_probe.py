"""Track 0 disposable closure evidence probe for multiple Form 1099-K statements.

Purpose: Track 0 adversarial closure probe.
Specification: docs/phases/tax-circumstance-breadth/milestones/multiple-statement-circumstances-evidence/connected-sale-design.md
Gate: PROJECT_PLANNING.md "Track 0 Adversarial Closure Gate"

Builds the design's successor content (family tax.us.2025.f1099k v2 on source-family.v1,
its closure mapping, reason successor without the count stop, raw Box 1a subtotal,
Candidate C top-entry selection, attachment and unresolved successors) in memory and a
temporary directory, never under packages/content/, and never adopted or published.

Records through the real Form 1099-K writers (family_version="v2"), the accepted handover,
ActLog, the live coordinator and the presentation projection.

Exercises synthetic end-to-end models for every materially distinct disposition path:
1. Two supported losses (sum published, pins verified);
2. One supported loss beside a published non-loss reason (blocked DEPENDENCY_ABSENT);
3. A blocked subject (reads_subject_results blocked-subject contract; blocks DEPENDENCY_INVALID naming Box 1a fact ID);
3b. Withdrawn answer under production reason successor (yields cost-basis-unanswered, blocks DEPENDENCY_ABSENT; design contradiction observation);
4. Closed-empty on v2 ($0.00 published; attachment inapplicable);
5a. Unclosed with statements (SOURCE_SET_UNCLOSED);
5b. Unclosed empty family (SOURCE_SET_UNCLOSED);
6. Excluded statement beside supported loss (prior-depreciable-use-excluded; blocks DEPENDENCY_ABSENT);
7. Late-member trace (attest -> close -> compute -> add member -> reclose -> recompute);
8. Upgrade v1 closed-empty -> first v2 statement -> fresh v2 closure;
9. Upgrade v1 one statement + closure -> second v2 statement -> fresh v2 closure;
10. Presentation-model probe for Schedule 1 field and per-statement explanation.
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
from packages.derivation.presentation_projection import validate_presentation_model
from packages.kernel.act_log import ActLog
from packages.kernel.currency import compute_currency
from packages.kernel.facts import fact_id_for
from packages.kernel.findings import project
from packages.tax.f1099k_statement_recording import (
    CLOSURE_TYPE,
    DEFAULT_FAMILY_SCOPE,
    FAMILY_ID,
    STATEMENT_BOX1A,
    STATEMENT_BOX4,
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
    USER,
    _finish_acts,
    _make_base_acts,
)
from tests.test_f1099k_statement_recording import BASE_ANSWERS, _evidence_ids
from tools.generate_ssa_no_activity_content import _bytes

REASON_RULE_ID = "tax.us.2025.rule.f1099k-statement-loss-reason"
REASON_SYMBOL = "tax.us.2025.f1099k.statement-loss-reason"
TOP_ENTRY_RULE_ID = "tax.us.2025.rule.schedule1-top-entry"
TOP_ENTRY_SYMBOL = "tax.us.2025.schedule1.top-entry"
SUBTOTAL_RULE_ID = "tax.us.2025.rule.f1099k-box1a-subtotal"
SUBTOTAL_SYMBOL = "tax.us.2025.f1099k.box1a-subtotal"
BOX1A_SYMBOL = "tax.us.2025.f1099k.box1a-gross-amount"
ATTACHMENT_RULE_ID = "tax.us.2025.rule.attachment.schedule-1"
UNRESOLVED_RULE_ID = "tax.us.2025.rule.f1099k-unresolved"

ALL_16_DISCOVERY_IDS: frozenset[str] = frozenset({
    "tax.us.2025.f1099k.box4-federal-withholding",
    "tax.us.2025.f1099k.covers-only-single-item",
    "tax.us.2025.f1099k.acquired-by-purchase",
    "tax.us.2025.f1099k.primary-purpose-at-acquisition",
    "tax.us.2025.f1099k.exclusive-personal-use",
    "tax.us.2025.f1099k.digital-asset-involvement",
    "tax.us.2025.f1099k.agreed-item-price",
    "tax.us.2025.f1099k.shipping-arrangement",
    "tax.us.2025.f1099k.platform-fees",
    "tax.us.2025.f1099k.seller-paid-shipping",
    "tax.us.2025.f1099k.sales-tax-collected-by-platform",
    "tax.us.2025.f1099k.refund-amount",
    "tax.us.2025.f1099k.buyer-paid-shipping",
    "tax.us.2025.f1099k.cost-basis-known",
    "tax.us.2025.f1099k.purchase-cost",
    "tax.us.2025.f1099k.lasting-improvements-or-adjustments",
})

from contextlib import contextmanager


@contextmanager
def instrumented_sale_input_transport():
    """Instrument input transport for personal item sale circumstances across multiple statements."""
    original_fn = live._resolved_run_material

    def _wrapped_material(graph: Any) -> _ResolvedRunMaterial:
        material = original_fn(graph)
        rules, parameters, families, mappings, fact_types, bindings, collect_names = material
        original_emission_only = list(material.emission_only_names)
        box1a_ft = next(
            (ft for ft in fact_types if ft.get("id") == BOX1A_SYMBOL and ft.get("version") == "v1"),
            None,
        )
        assert box1a_ft is not None
        box1a_keys = [k["name"] for k in box1a_ft.get("identity_keys", []) if isinstance(k, dict)]
        discovered: list[str] = []
        modified_rules: list[dict[str, Any]] = []
        for rule in rules:
            rule_copy = copy.deepcopy(rule)
            subject = rule_copy.get("subject")
            if (
                isinstance(subject, dict)
                and subject.get("id") == BOX1A_SYMBOL
                and subject.get("version") == "v1"
            ):
                for req_symbol in rule_copy.get("requires", []):
                    if req_symbol not in ALL_16_DISCOVERY_IDS:
                        continue
                    matching_binding = next(
                        (b for b in bindings if b.get("symbol") == req_symbol), None
                    )
                    if matching_binding is None:
                        continue
                    ft_ref = matching_binding.get("fact_type", {})
                    if not isinstance(ft_ref, dict):
                        continue
                    if ft_ref.get("id") != req_symbol:
                        continue
                    if matching_binding.get("mode") != "optional_default":
                        continue
                    if ft_ref.get("version") != "v1":
                        continue
                    ft_decl = next(
                        (
                            ft
                            for ft in fact_types
                            if ft.get("id") == req_symbol and ft.get("version") == "v1"
                        ),
                        None,
                    )
                    if ft_decl is None:
                        continue
                    decl_keys = [
                        k["name"]
                        for k in ft_decl.get("identity_keys", [])
                        if isinstance(k, dict)
                    ]
                    if decl_keys != box1a_keys:
                        continue
                    if (
                        req_symbol not in collect_names
                        and req_symbol not in original_emission_only
                        and req_symbol not in discovered
                    ):
                        discovered.append(req_symbol)
            modified_rules.append(rule_copy)
        instrumented_emission = list(original_emission_only) + discovered
        return _ResolvedRunMaterial(
            rules=modified_rules,
            parameters=material[1],
            families=material[2],
            mappings=material[3],
            fact_types=material[4],
            bindings=material[5],
            collect_names=material[6],
            emission_only_names=instrumented_emission,
            parameter_index=material.parameter_index,
        )

    with patch.object(live, "_resolved_run_material", side_effect=_wrapped_material):
        yield


class DisposableTrack0Surface:
    """Disposable Track 0 surface constructing the candidate successor content in memory / tmp."""

    def __init__(self, root: Path, *, diagnostic_block: bool = False) -> None:
        self.members = root / "members"
        self.releases = root / "releases"
        self.members.mkdir(parents=True)
        self.releases.mkdir(parents=True)
        for source in CONTENT.glob("*.json"):
            shutil.copyfile(source, self.members / source.name)
        release_name = RELEASE_PATH.name
        shutil.copyfile(RELEASE_PATH, self.releases / release_name)
        self.adoption = _load_fixture_adoption()
        self._seal(release_name, diagnostic_block=diagnostic_block)
        self.surface = PublicationSurface(
            self.releases, self.members / REGISTRY_PATH.name, self.members
        )

    def _seal(self, release_name: str, *, diagnostic_block: bool = False) -> None:
        package = json.loads(PACKAGE_PATH.read_text("utf-8"))
        registry = json.loads(REGISTRY_PATH.read_text("utf-8"))

        # 1. Reason rule successor: remove shared_key_count guard
        reason_rule = json.loads(
            (CONTENT / "rule.f1099k-statement-loss-reason.v3.json").read_text("utf-8")
        )
        if (
            isinstance(reason_rule.get("value"), dict)
            and (reason_rule["value"].get("when") or {}).get("left", {}).get("op")
            == "shared_key_count"
        ):
            reason_rule["value"] = reason_rule["value"]["else"]

        if diagnostic_block:
            # Candidate C diagnostic pattern: when cost-basis-known is withdrawn ("not-asked"),
            # the reason rule blocks DEPENDENCY_ABSENT rather than falling back to categorical reason.
            # This exercises the Candidate C reads_subject_results blocked-subject contract.
            reason_rule["value"] = {
                "op": "choose",
                "when": {
                    "op": "categorical_compare",
                    "cmp": "eq",
                    "left": {
                        "op": "ref",
                        "name": "tax.us.2025.f1099k.cost-basis-known",
                    },
                    "right": {
                        "op": "category_literal",
                        "fact_type": {
                            "id": "tax.us.2025.f1099k.cost-basis-known",
                            "version": "v1",
                        },
                        "value": "not-asked",
                    },
                },
                "then": {
                    "op": "block",
                    "code": "DEPENDENCY_ABSENT",
                },
                "else": reason_rule["value"],
            }

        (self.members / "rule.f1099k-statement-loss-reason.v3.json").write_bytes(
            _bytes(reason_rule)
        )

        # 2. Raw Box 1a subtotal rule (plain unrounded add(collect))
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
            "notes": "Candidate C / Track 0: Raw unrounded sum of Form 1099-K Box 1a family under ADR-0016 collect authority.",
        }
        (self.members / "rule.f1099k-box1a-subtotal.json").write_bytes(_bytes(subtotal_rule))

        # 3. Schedule 1 top entry successor: two-path selection requiring raw subtotal
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
                                    "id": "tax.us.2025.f1099k.inert-path-unwritten",
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

        # 4. Family successor v2
        fam = json.loads((CONTENT / "family.f1099k.json").read_text("utf-8"))
        fam["version"] = "v2"
        fam["authorizes_subtotal"] = SUBTOTAL_SYMBOL
        fam["closure_claim"] = (
            "Every personal item sale amount reported in box 1a of a Form 1099-K furnished to the taxpayer "
            "for tax year 2025 is recorded as a statement item as of the keyed horizon. Closed with members "
            "authorizes the sum of current members; closed-empty authorizes subtotal 0."
        )
        (self.members / "family.f1099k.json").write_bytes(_bytes(fam))

        # 5. Closure-mapping successor v2
        mapping = json.loads((CONTENT / "closure-mapping.f1099k.json").read_text("utf-8"))
        mapping["version"] = "v2"
        mapping["family"] = {"id": FAMILY_ID, "version": "v2"}
        mapping["admits_symbol"] = SUBTOTAL_SYMBOL
        (self.members / "closure-mapping.f1099k.json").write_bytes(_bytes(mapping))

        # 6. Attachment successor v3
        att = json.loads((CONTENT / "rule.attachment.schedule-1.v3.json").read_text("utf-8"))
        for item in att.get("itemizations", []):
            if item.get("authority", {}).get("source_family", {}).get("id") == FAMILY_ID:
                item["authority"]["source_family"]["version"] = "v2"
                for rs in item.get("row_sets", []):
                    rs["rows"]["source_family"]["version"] = "v2"
                    rs["subtotal_symbol"] = SUBTOTAL_SYMBOL
                item["tie_out"]["line_symbol"] = SUBTOTAL_SYMBOL
        (self.members / "rule.attachment.schedule-1.v3.json").write_bytes(_bytes(att))

        # 7. Unresolved successor v2
        unres = json.loads((CONTENT / "rule.f1099k-unresolved.v2.json").read_text("utf-8"))
        for p in unres.get("selection", {}).get("paths", []):
            if p.get("id") == "statement":
                p["activity"]["source_family"]["version"] = "v2"
                p["when"] = {
                    "op": "not",
                    "value": {
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
                }
        (self.members / "rule.f1099k-unresolved.v2.json").write_bytes(_bytes(unres))

        # 8. Package members
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

        checksum_reason = citizen_checksum(reason_rule)
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
                citizen["checksum"] = checksum_reason
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

        package["package_checksum"] = package_instance_checksum(package)
        (self.members / PACKAGE_PATH.name).write_bytes(_bytes(package))

        for entry in registry["packages"]:
            if entry["id"] == package["id"] and entry["version"] == package["version"]:
                entry["checksum"] = package["package_checksum"]

        registry_bytes = _bytes(registry)
        (self.members / REGISTRY_PATH.name).write_bytes(registry_bytes)

        release = json.loads((self.releases / release_name).read_text("utf-8"))
        release["package_registry_sha256"] = hashlib.sha256(registry_bytes).hexdigest()
        release_bytes = _bytes(release)
        (self.releases / release_name).write_bytes(release_bytes)

        payload = cast(dict[str, Any], self.adoption["payload"])
        payload["package"]["id"] = package["id"]
        payload["package"]["version"] = package["version"]
        payload["package"]["checksum"] = package["package_checksum"]
        payload["release"]["id"] = release["id"]
        payload["release"]["version"] = release["version"]
        payload["release"]["checksum"] = hashlib.sha256(release_bytes).hexdigest()


def _prepare_adoption(
    disposable: DisposableTrack0Surface, log: ActLog, act_id: str, revision: int = 50
) -> dict[str, Any]:
    adoption = copy.deepcopy(disposable.adoption)
    adoption["act_id"] = act_id
    adoption["committed_against"] = log.read().revision
    adoption["actor"] = USER
    adoption["at"] = "2026-10-18T12:25:00Z"
    cast(dict[str, Any], adoption["payload"])["revision"] = revision
    return adoption


def _current_f1099k_horizon(state: Any) -> str:
    scope_tuple = tuple(sorted(DEFAULT_FAMILY_SCOPE.items()))
    for (fid, ver, sc), hid in state.horizon_state.current_by_chain.items():
        if fid == FAMILY_ID and sc == scope_tuple:
            return hid
    raise KeyError(f"f1099k horizon not found in current_by_chain for scope {scope_tuple}")


def _attest_closure(
    log: ActLog,
    horizon_id: str,
    *,
    actor: str = USER,
    at: str = "2026-10-18T12:20:00Z",
    suffix: str = "closure",
) -> str:
    rev = log.read().revision
    finding_id = f"f1099k.closure.finding.{suffix}"
    fact_id = f"tax.us.2025.f1099k.source-closure|family-horizon={horizon_id},tax-year=2025"
    finding = {
        "schema": "finding.v1",
        "id": finding_id,
        "fact_id": fact_id,
        "value": True,
        "basis": "attested",
        "evidence_ids": [],
    }
    act = {
        "schema": "act.v1",
        "act_id": f"act.{suffix}",
        "kind": "assertion",
        "actor": actor,
        "at": at,
        "committed_against": rev,
        "payload": {
            "finding": finding,
        },
    }
    log.append(act, expected_revision=rev)
    return finding_id


ANSWERS_B_LOSS = {
    **BASE_ANSWERS,
    "shipping-arrangement": "seller-received-shipping",
    "agreed-item-price": 380.0,
    "sales-tax-collected-by-platform": 20.0,
    "buyer-paid-shipping": 60.0,
    "platform-fees": 15.0,
    "seller-paid-shipping": 15.0,
    "purchase-cost": 800.0,
}


@pytest.mark.live(reason="Live coordinator execution over disposable Track 0 content surface")
class TestTrack0ClosureProbe(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory(prefix="track0-probe-")
        self.addCleanup(self.temp.cleanup)
        self.temp_path = Path(self.temp.name)
        self.registry = tax_registry()

    def test_case1_two_supported_losses_sum_published(self) -> None:
        workspace = self.temp_path / "case1"
        log = ActLog(workspace, self.registry)
        log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)

        rep_a = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.alpha",
            statement_ref="demo.statement.bicycle",
            box1a=880.0,
            box4=0.0,
            submission_id="c1.sub.a",
            evidence_id="c1.ev.a",
            actor=USER,
            at="2026-10-18T12:00:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=False,
        )
        rev_a = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c1.rev.a",
            shown_at="2026-10-18T12:00:30Z",
            statement_keys=rep_a["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_a,
            answers=BASE_ANSWERS,
            submission_id="c1.ans.a",
            evidence_ids=_evidence_ids(BASE_ANSWERS, "c1.ev.ans.a"),
            actor=USER,
            at="2026-10-18T12:05:00Z",
        )

        rep_b = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.beta",
            statement_ref="demo.statement.camera",
            box1a=460.0,
            box4=0.0,
            submission_id="c1.sub.b",
            evidence_id="c1.ev.b",
            actor=USER,
            at="2026-10-18T12:10:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=True,
        )
        rev_b = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c1.rev.b",
            shown_at="2026-10-18T12:10:30Z",
            statement_keys=rep_b["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_b,
            answers=ANSWERS_B_LOSS,
            submission_id="c1.ans.b",
            evidence_ids=_evidence_ids(ANSWERS_B_LOSS, "c1.ev.ans.b"),
            actor=USER,
            at="2026-10-18T12:15:00Z",
        )

        disposable = DisposableTrack0Surface(self.temp_path / "surface1")
        adoption = _prepare_adoption(disposable, log, "adopt.c1")
        log.append(adoption, expected_revision=log.read().revision)

        acts = log.read().acts
        capability = WorkspaceCapability(workspace)
        with instrumented_sale_input_transport():
            run_out = live_coordinate_run(
                capability,
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="c1.run",
                governance_pins=[],
                surface=disposable.surface,
                output_name="c1.json",
            )

        self.assertIsNone(run_out.refusal)
        findings = {pub.finding.get("symbol"): pub.finding for pub in run_out.publications}

        # 1. Raw Box 1a subtotal
        subtotal_f = findings.get(SUBTOTAL_SYMBOL)
        self.assertIsNotNone(subtotal_f)
        assert subtotal_f is not None
        self.assertEqual(subtotal_f["value"], "1340.0")
        subtotal_pin_ids = {p["id"] for p in subtotal_f.get("pins", [])}
        self.assertIn(rep_a["finding_ids"][0], subtotal_pin_ids)
        self.assertIn(rep_b["finding_ids"][0], subtotal_pin_ids)

        # 2. Schedule 1 top entry
        top_f = findings.get(TOP_ENTRY_SYMBOL)
        self.assertIsNotNone(top_f)
        assert top_f is not None
        self.assertEqual(top_f["value"], "1340.0")
        top_pins = top_f.get("pins", [])
        top_pin_ids = {p["id"] for p in top_pins}
        self.assertIn(subtotal_f["id"], top_pin_ids)

        # Reason findings for both statements pinned
        reason_f_a = next(
            f
            for sym, f in findings.items()
            if sym and sym.startswith(REASON_SYMBOL) and "bicycle" in sym
        )
        reason_f_b = next(
            f
            for sym, f in findings.items()
            if sym and sym.startswith(REASON_SYMBOL) and "camera" in sym
        )
        self.assertEqual(reason_f_a["value"], "supported-loss")
        self.assertEqual(reason_f_b["value"], "supported-loss")
        self.assertIn(reason_f_a["id"], top_pin_ids)
        self.assertIn(reason_f_b["id"], top_pin_ids)

        # Closure pinned
        closure_fid = rep_b["finding_ids"][-1]
        self.assertIn(closure_fid, top_pin_ids)

        # 3. Attachment published
        durable = json.loads(run_out.output_path.read_text("utf-8"))
        att_disp = next(
            d for d in durable["dispositions"] if d.get("artifact_id") == ATTACHMENT_RULE_ID
        )
        self.assertEqual(att_disp["disposition"], "published")
        att_f = findings.get("tax.us.2025.schedule1.disposition")
        self.assertIsNotNone(att_f)
        assert att_f is not None
        self.assertTrue(att_f["value"]["required"])
        k_item = next(
            i for i in att_f["value"]["itemizations"] if i["part_id"] == "sch1-top-entry-f1099k"
        )
        self.assertEqual(k_item["part_sum"], "1340.0")
        self.assertEqual(k_item["tie_out"]["line_value"], "1340.0")
        self.assertEqual(len(k_item["row_sets"][0]["rows"]), 2)

        # 4. Unresolved inapplicable
        unres_disp = next(
            d for d in durable["dispositions"] if d.get("artifact_id") == UNRESOLVED_RULE_ID
        )
        self.assertEqual(unres_disp["disposition"], "inapplicable")

    def test_case2_one_supported_loss_beside_published_non_loss(self) -> None:
        workspace = self.temp_path / "case2"
        log = ActLog(workspace, self.registry)
        log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)

        rep_a = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.alpha",
            statement_ref="demo.statement.bicycle",
            box1a=880.0,
            box4=0.0,
            submission_id="c2.sub.a",
            evidence_id="c2.ev.a",
            actor=USER,
            at="2026-10-18T12:00:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=False,
        )
        rev_a = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c2.rev.a",
            shown_at="2026-10-18T12:00:30Z",
            statement_keys=rep_a["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_a,
            answers=BASE_ANSWERS,
            submission_id="c2.ans.a",
            evidence_ids=_evidence_ids(BASE_ANSWERS, "c2.ev.ans.a"),
            actor=USER,
            at="2026-10-18T12:05:00Z",
        )

        answers_b_unknown = {**ANSWERS_B_LOSS, "cost-basis-known": "cannot-tell"}
        rep_b = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.beta",
            statement_ref="demo.statement.camera",
            box1a=460.0,
            box4=0.0,
            submission_id="c2.sub.b",
            evidence_id="c2.ev.b",
            actor=USER,
            at="2026-10-18T12:10:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=True,
        )
        rev_b = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c2.rev.b",
            shown_at="2026-10-18T12:10:30Z",
            statement_keys=rep_b["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_b,
            answers=answers_b_unknown,
            submission_id="c2.ans.b",
            evidence_ids=_evidence_ids(answers_b_unknown, "c2.ev.ans.b"),
            actor=USER,
            at="2026-10-18T12:15:00Z",
        )

        disposable = DisposableTrack0Surface(self.temp_path / "surface2")
        adoption = _prepare_adoption(disposable, log, "adopt.c2")
        log.append(adoption, expected_revision=log.read().revision)

        acts = log.read().acts
        capability = WorkspaceCapability(workspace)
        with instrumented_sale_input_transport():
            run_out = live_coordinate_run(
                capability,
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="c2.run",
                governance_pins=[],
                surface=disposable.surface,
                output_name="c2.json",
            )

        self.assertIsNone(run_out.refusal)
        findings = {pub.finding.get("symbol"): pub.finding for pub in run_out.publications}

        # Statement A is supported-loss; Statement B is cost-basis-unknown
        reason_f_a = next(
            f
            for sym, f in findings.items()
            if sym and sym.startswith(REASON_SYMBOL) and "bicycle" in sym
        )
        reason_f_b = next(
            f
            for sym, f in findings.items()
            if sym and sym.startswith(REASON_SYMBOL) and "camera" in sym
        )
        self.assertEqual(reason_f_a["value"], "supported-loss")
        self.assertEqual(reason_f_b["value"], "cost-basis-unknown")

        # Top entry is NOT published, blocks DEPENDENCY_ABSENT
        self.assertNotIn(TOP_ENTRY_SYMBOL, findings)
        durable = json.loads(run_out.output_path.read_text("utf-8"))
        top_disp = next(
            d for d in durable["dispositions"] if d.get("artifact_id") == TOP_ENTRY_RULE_ID
        )
        self.assertEqual(top_disp["disposition"], "blocked")
        self.assertEqual(top_disp["code"], "DEPENDENCY_ABSENT")

        # Attachment blocks
        att_disp = next(
            d for d in durable["dispositions"] if d.get("artifact_id") == ATTACHMENT_RULE_ID
        )
        self.assertEqual(att_disp["disposition"], "blocked")

        # Unresolved blocks
        unres_disp = next(
            d for d in durable["dispositions"] if d.get("artifact_id") == UNRESOLVED_RULE_ID
        )
        self.assertEqual(unres_disp["disposition"], "blocked")

    def test_case3_blocked_subject(self) -> None:
        """Candidate C selection contract: a subject whose reason blocks causes top-entry to block DEPENDENCY_INVALID citing Box 1a fact ID."""
        workspace = self.temp_path / "case3"
        log = ActLog(workspace, self.registry)
        log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)

        rep_a = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.alpha",
            statement_ref="demo.statement.bicycle",
            box1a=880.0,
            box4=0.0,
            submission_id="c3.sub.a",
            evidence_id="c3.ev.a",
            actor=USER,
            at="2026-10-18T12:00:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=False,
        )
        rev_a = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c3.rev.a",
            shown_at="2026-10-18T12:00:30Z",
            statement_keys=rep_a["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_a,
            answers=BASE_ANSWERS,
            submission_id="c3.ans.a",
            evidence_ids=_evidence_ids(BASE_ANSWERS, "c3.ev.ans.a"),
            actor=USER,
            at="2026-10-18T12:05:00Z",
        )

        rep_b = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.beta",
            statement_ref="demo.statement.camera",
            box1a=460.0,
            box4=0.0,
            submission_id="c3.sub.b",
            evidence_id="c3.ev.b",
            actor=USER,
            at="2026-10-18T12:10:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=True,
        )
        rev_b = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c3.rev.b",
            shown_at="2026-10-18T12:10:30Z",
            statement_keys=rep_b["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_b,
            answers=ANSWERS_B_LOSS,
            submission_id="c3.ans.b",
            evidence_ids=_evidence_ids(ANSWERS_B_LOSS, "c3.ev.ans.b"),
            actor=USER,
            at="2026-10-18T12:15:00Z",
        )
        saved_rev_b = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c3.srev.b",
            shown_at="2026-10-18T12:16:00Z",
            statement_keys=rep_b["statement_keys"],
        )
        cost_basis_finding_id = saved_rev_b["questions"]["cost-basis-known"]["finding_id"]

        withdraw_f1099k_statement_answer_durably(
            log,
            self.registry,
            current_findings=[cost_basis_finding_id],
            submission_id="c3.withdraw.b",
            actor=USER,
            at="2026-10-18T12:20:00Z",
            expected_revision=log.read().revision,
        )

        disposable = DisposableTrack0Surface(self.temp_path / "surface3", diagnostic_block=True)
        adoption = _prepare_adoption(disposable, log, "adopt.c3")
        log.append(adoption, expected_revision=log.read().revision)

        acts = log.read().acts
        capability = WorkspaceCapability(workspace)
        with instrumented_sale_input_transport():
            run_out = live_coordinate_run(
                capability,
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="c3.run",
                governance_pins=[],
                surface=disposable.surface,
                output_name="c3.json",
            )

        self.assertIsNone(run_out.refusal)
        durable = json.loads(run_out.output_path.read_text("utf-8"))
        top_disp = next(
            d for d in durable["dispositions"] if d.get("artifact_id") == TOP_ENTRY_RULE_ID
        )
        self.assertEqual(top_disp["disposition"], "blocked")
        self.assertEqual(top_disp["code"], "DEPENDENCY_INVALID")

        # Cites Statement B's Box 1a fact ID
        b1a_b_fact_id = fact_id_for(
            STATEMENT_BOX1A, tuple(sorted(rep_b["statement_keys"].items()))
        )
        self.assertIn(b1a_b_fact_id, top_disp.get("missing", []))

    def test_case3b_withdrawn_answer_under_production_reason_successor(self) -> None:
        """Observation contradicting design: under the real reason successor, withdrawn answers yield cost-basis-unanswered (blocking DEPENDENCY_ABSENT, not DEPENDENCY_INVALID)."""
        workspace = self.temp_path / "case3b"
        log = ActLog(workspace, self.registry)
        log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)

        rep_a = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.alpha",
            statement_ref="demo.statement.bicycle",
            box1a=880.0,
            box4=0.0,
            submission_id="c3b.sub.a",
            evidence_id="c3b.ev.a",
            actor=USER,
            at="2026-10-18T12:00:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=False,
        )
        rev_a = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c3b.rev.a",
            shown_at="2026-10-18T12:00:30Z",
            statement_keys=rep_a["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_a,
            answers=BASE_ANSWERS,
            submission_id="c3b.ans.a",
            evidence_ids=_evidence_ids(BASE_ANSWERS, "c3b.ev.ans.a"),
            actor=USER,
            at="2026-10-18T12:05:00Z",
        )

        rep_b = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.beta",
            statement_ref="demo.statement.camera",
            box1a=460.0,
            box4=0.0,
            submission_id="c3b.sub.b",
            evidence_id="c3b.ev.b",
            actor=USER,
            at="2026-10-18T12:10:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=True,
        )
        rev_b = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c3b.rev.b",
            shown_at="2026-10-18T12:10:30Z",
            statement_keys=rep_b["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_b,
            answers=ANSWERS_B_LOSS,
            submission_id="c3b.ans.b",
            evidence_ids=_evidence_ids(ANSWERS_B_LOSS, "c3b.ev.ans.b"),
            actor=USER,
            at="2026-10-18T12:15:00Z",
        )
        saved_rev_b = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c3b.srev.b",
            shown_at="2026-10-18T12:16:00Z",
            statement_keys=rep_b["statement_keys"],
        )
        cost_basis_finding_id = saved_rev_b["questions"]["cost-basis-known"]["finding_id"]

        withdraw_f1099k_statement_answer_durably(
            log,
            self.registry,
            current_findings=[cost_basis_finding_id],
            submission_id="c3b.withdraw.b",
            actor=USER,
            at="2026-10-18T12:20:00Z",
            expected_revision=log.read().revision,
        )

        # Standard production reason successor (diagnostic_block=False)
        disposable = DisposableTrack0Surface(self.temp_path / "surface3b", diagnostic_block=False)
        adoption = _prepare_adoption(disposable, log, "adopt.c3b")
        log.append(adoption, expected_revision=log.read().revision)

        acts = log.read().acts
        capability = WorkspaceCapability(workspace)
        with instrumented_sale_input_transport():
            run_out = live_coordinate_run(
                capability,
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="c3b.run",
                governance_pins=[],
                surface=disposable.surface,
                output_name="c3b.json",
            )

        self.assertIsNone(run_out.refusal)
        findings = {pub.finding.get("symbol"): pub.finding for pub in run_out.publications}

        # Statement B reason evaluated to cost-basis-unanswered (a published category, not a block)
        reason_f_b = next(
            f
            for sym, f in findings.items()
            if sym and sym.startswith(REASON_SYMBOL) and "camera" in sym
        )
        self.assertEqual(reason_f_b["value"], "cost-basis-unanswered")

        # Top entry blocks DEPENDENCY_ABSENT via the selection rule's choose else branch
        durable = json.loads(run_out.output_path.read_text("utf-8"))
        top_disp = next(
            d for d in durable["dispositions"] if d.get("artifact_id") == TOP_ENTRY_RULE_ID
        )
        self.assertEqual(top_disp["disposition"], "blocked")
        self.assertEqual(top_disp["code"], "DEPENDENCY_ABSENT")

    def test_case4_closed_empty_v2(self) -> None:
        workspace = self.temp_path / "case4"
        log = ActLog(workspace, self.registry)
        log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)

        record_f1099k_no_statements_durably(
            log,
            self.registry,
            submission_id="c4.sub",
            evidence_id="c4.ev",
            actor=USER,
            at="2026-10-18T12:00:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
        )

        disposable = DisposableTrack0Surface(self.temp_path / "surface4")
        adoption = _prepare_adoption(disposable, log, "adopt.c4")
        log.append(adoption, expected_revision=log.read().revision)

        acts = log.read().acts
        capability = WorkspaceCapability(workspace)
        with instrumented_sale_input_transport():
            run_out = live_coordinate_run(
                capability,
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="c4.run",
                governance_pins=[],
                surface=disposable.surface,
                output_name="c4.json",
            )

        self.assertIsNone(run_out.refusal)
        findings = {pub.finding.get("symbol"): pub.finding for pub in run_out.publications}
        top_f = findings.get(TOP_ENTRY_SYMBOL)
        self.assertIsNotNone(top_f)
        assert top_f is not None
        self.assertEqual(float(top_f["value"]), 0.0)

        durable = json.loads(run_out.output_path.read_text("utf-8"))
        att_disp = next(
            d for d in durable["dispositions"] if d.get("artifact_id") == ATTACHMENT_RULE_ID
        )
        self.assertEqual(att_disp["disposition"], "inapplicable")

    def test_case5a_unclosed_with_statements(self) -> None:
        workspace = self.temp_path / "case5a"
        log = ActLog(workspace, self.registry)
        log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)

        rep_a = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.alpha",
            statement_ref="demo.statement.bicycle",
            box1a=880.0,
            box4=0.0,
            submission_id="c5a.sub.a",
            evidence_id="c5a.ev.a",
            actor=USER,
            at="2026-10-18T12:00:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=False,
        )
        rev_a = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c5a.rev.a",
            shown_at="2026-10-18T12:00:30Z",
            statement_keys=rep_a["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_a,
            answers=BASE_ANSWERS,
            submission_id="c5a.ans.a",
            evidence_ids=_evidence_ids(BASE_ANSWERS, "c5a.ev.ans.a"),
            actor=USER,
            at="2026-10-18T12:05:00Z",
        )

        disposable = DisposableTrack0Surface(self.temp_path / "surface5a")
        adoption = _prepare_adoption(disposable, log, "adopt.c5a")
        log.append(adoption, expected_revision=log.read().revision)

        acts = log.read().acts
        capability = WorkspaceCapability(workspace)
        with instrumented_sale_input_transport():
            run_out = live_coordinate_run(
                capability,
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="c5a.run",
                governance_pins=[],
                surface=disposable.surface,
                output_name="c5a.json",
            )

        self.assertIsNone(run_out.refusal)
        findings = {pub.finding.get("symbol"): pub.finding for pub in run_out.publications}
        self.assertNotIn(TOP_ENTRY_SYMBOL, findings)

        durable = json.loads(run_out.output_path.read_text("utf-8"))
        top_disp = next(
            d for d in durable["dispositions"] if d.get("artifact_id") == TOP_ENTRY_RULE_ID
        )
        self.assertEqual(top_disp["disposition"], "blocked")
        self.assertEqual(top_disp["code"], BLOCK_CLOSURE)
        self.assertIn(FAMILY_ID, top_disp.get("missing", []))

    def test_case5b_unclosed_empty_family(self) -> None:
        workspace = self.temp_path / "case5b"
        log = ActLog(workspace, self.registry)
        log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)

        disposable = DisposableTrack0Surface(self.temp_path / "surface5b")
        adoption = _prepare_adoption(disposable, log, "adopt.c5b")
        log.append(adoption, expected_revision=log.read().revision)

        acts = log.read().acts
        capability = WorkspaceCapability(workspace)
        with instrumented_sale_input_transport():
            run_out = live_coordinate_run(
                capability,
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="c5b.run",
                governance_pins=[],
                surface=disposable.surface,
                output_name="c5b.json",
            )

        self.assertIsNone(run_out.refusal)
        findings = {pub.finding.get("symbol"): pub.finding for pub in run_out.publications}
        self.assertNotIn(TOP_ENTRY_SYMBOL, findings)

        durable = json.loads(run_out.output_path.read_text("utf-8"))
        top_disp = next(
            d for d in durable["dispositions"] if d.get("artifact_id") == TOP_ENTRY_RULE_ID
        )
        self.assertEqual(top_disp["disposition"], "blocked")
        self.assertEqual(top_disp["code"], BLOCK_CLOSURE)
        self.assertIn(FAMILY_ID, top_disp.get("missing", []))

    def test_case6_gain_or_excluded_statement_beside_supported_loss(self) -> None:
        workspace = self.temp_path / "case6"
        log = ActLog(workspace, self.registry)
        log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)

        rep_a = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.alpha",
            statement_ref="demo.statement.bicycle",
            box1a=880.0,
            box4=0.0,
            submission_id="c6.sub.a",
            evidence_id="c6.ev.a",
            actor=USER,
            at="2026-10-18T12:00:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=False,
        )
        rev_a = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c6.rev.a",
            shown_at="2026-10-18T12:00:30Z",
            statement_keys=rep_a["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_a,
            answers=BASE_ANSWERS,
            submission_id="c6.ans.a",
            evidence_ids=_evidence_ids(BASE_ANSWERS, "c6.ev.ans.a"),
            actor=USER,
            at="2026-10-18T12:05:00Z",
        )

        answers_b_excluded = {**ANSWERS_B_LOSS, "exclusive-personal-use": "no"}
        rep_b = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.beta",
            statement_ref="demo.statement.camera",
            box1a=460.0,
            box4=0.0,
            submission_id="c6.sub.b",
            evidence_id="c6.ev.b",
            actor=USER,
            at="2026-10-18T12:10:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=True,
        )
        rev_b = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c6.rev.b",
            shown_at="2026-10-18T12:10:30Z",
            statement_keys=rep_b["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_b,
            answers=answers_b_excluded,
            submission_id="c6.ans.b",
            evidence_ids=_evidence_ids(answers_b_excluded, "c6.ev.ans.b"),
            actor=USER,
            at="2026-10-18T12:15:00Z",
        )

        disposable = DisposableTrack0Surface(self.temp_path / "surface6")
        adoption = _prepare_adoption(disposable, log, "adopt.c6")
        log.append(adoption, expected_revision=log.read().revision)

        acts = log.read().acts
        capability = WorkspaceCapability(workspace)
        with instrumented_sale_input_transport():
            run_out = live_coordinate_run(
                capability,
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="c6.run",
                governance_pins=[],
                surface=disposable.surface,
                output_name="c6.json",
            )

        self.assertIsNone(run_out.refusal)
        findings = {pub.finding.get("symbol"): pub.finding for pub in run_out.publications}

        reason_f_b = next(
            f
            for sym, f in findings.items()
            if sym and sym.startswith(REASON_SYMBOL) and "camera" in sym
        )
        self.assertEqual(reason_f_b["value"], "prior-depreciable-use-excluded")

        self.assertNotIn(TOP_ENTRY_SYMBOL, findings)
        durable = json.loads(run_out.output_path.read_text("utf-8"))
        top_disp = next(
            d for d in durable["dispositions"] if d.get("artifact_id") == TOP_ENTRY_RULE_ID
        )
        self.assertEqual(top_disp["disposition"], "blocked")
        self.assertEqual(top_disp["code"], "DEPENDENCY_ABSENT")

    def test_case7_late_member_trace(self) -> None:
        """Paper trace test: attest -> close -> compute -> add member -> reclose -> recompute."""
        workspace = self.temp_path / "case7"
        log = ActLog(workspace, self.registry)
        log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)

        # Step 1: Attest Statement A
        rep_a = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.alpha",
            statement_ref="demo.statement.bicycle",
            box1a=880.0,
            box4=0.0,
            submission_id="c7.sub.a",
            evidence_id="c7.ev.a",
            actor=USER,
            at="2026-10-18T12:00:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=False,
        )
        rev_a = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c7.rev.a",
            shown_at="2026-10-18T12:00:30Z",
            statement_keys=rep_a["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_a,
            answers=BASE_ANSWERS,
            submission_id="c7.ans.a",
            evidence_ids=_evidence_ids(BASE_ANSWERS, "c7.ev.ans.a"),
            actor=USER,
            at="2026-10-18T12:05:00Z",
        )
        b1a_a_fid = rep_a["finding_ids"][0]

        # Step 2: Close family on current horizon h0
        state0 = project(log.read().acts, self.registry)
        h0 = _current_f1099k_horizon(state0)
        closure_0_fid = _attest_closure(log, h0, suffix="close.0")

        state1 = project(log.read().acts, self.registry)
        cur1 = compute_currency(state1)
        self.assertIn(b1a_a_fid, cur1.current_finding_ids)
        self.assertIn(closure_0_fid, cur1.current_finding_ids)

        # Step 3: Compute Run 1
        disposable = DisposableTrack0Surface(self.temp_path / "surface7")
        adoption = _prepare_adoption(disposable, log, "adopt.c7")
        log.append(adoption, expected_revision=log.read().revision)

        acts1 = log.read().acts
        capability = WorkspaceCapability(workspace)
        with instrumented_sale_input_transport():
            run1 = live_coordinate_run(
                capability,
                repo_root=ROOT,
                authoritative_acts=acts1,
                workspace_revision=len(acts1),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="c7.run1",
                governance_pins=[],
                surface=disposable.surface,
                output_name="c7_1.json",
            )
        self.assertIsNone(run1.refusal)
        top1_f = next(
            pub.finding for pub in run1.publications if pub.finding.get("symbol") == TOP_ENTRY_SYMBOL
        )
        self.assertEqual(float(top1_f["value"]), 880.0)
        self.assertIn(closure_0_fid, {p["id"] for p in top1_f["pins"]})

        # Step 4: Add member Statement B (unclosed)
        rep_b = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.beta",
            statement_ref="demo.statement.camera",
            box1a=460.0,
            box4=0.0,
            submission_id="c7.sub.b",
            evidence_id="c7.ev.b",
            actor=USER,
            at="2026-10-18T12:10:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=False,
        )
        b1a_b_fid = rep_b["finding_ids"][0]
        rev_b = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c7.rev.b",
            shown_at="2026-10-18T12:10:30Z",
            statement_keys=rep_b["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_b,
            answers=ANSWERS_B_LOSS,
            submission_id="c7.ans.b",
            evidence_ids=_evidence_ids(ANSWERS_B_LOSS, "c7.ev.ans.b"),
            actor=USER,
            at="2026-10-18T12:15:00Z",
        )

        state2 = project(log.read().acts, self.registry)
        cur2 = compute_currency(state2)
        # Prior closure_0_fid is displaced!
        self.assertNotIn(closure_0_fid, cur2.current_finding_ids)
        self.assertIn(closure_0_fid, cur2.displaced_finding_ids)
        # Both statement findings are current
        self.assertIn(b1a_a_fid, cur2.current_finding_ids)
        self.assertIn(b1a_b_fid, cur2.current_finding_ids)

        # Pre-reclose run blocks SOURCE_SET_UNCLOSED
        acts2 = log.read().acts
        with instrumented_sale_input_transport():
            run_mid = live_coordinate_run(
                capability,
                repo_root=ROOT,
                authoritative_acts=acts2,
                workspace_revision=len(acts2),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="c7.run_mid",
                governance_pins=[],
                surface=disposable.surface,
                output_name="c7_mid.json",
            )
        self.assertIsNone(run_mid.refusal)
        durable_mid = json.loads(run_mid.output_path.read_text("utf-8"))
        top_disp_mid = next(
            d for d in durable_mid["dispositions"] if d.get("artifact_id") == TOP_ENTRY_RULE_ID
        )
        self.assertEqual(top_disp_mid["disposition"], "blocked")
        self.assertEqual(top_disp_mid["code"], BLOCK_CLOSURE)

        # Step 5: Reclose family on current horizon h1
        h1 = _current_f1099k_horizon(state2)
        closure_1_fid = _attest_closure(log, h1, suffix="close.1")
        state3 = project(log.read().acts, self.registry)
        cur3 = compute_currency(state3)
        self.assertIn(closure_1_fid, cur3.current_finding_ids)
        self.assertIn(closure_0_fid, cur3.displaced_finding_ids)

        # Step 6: Recompute Run 2
        acts3 = log.read().acts
        with instrumented_sale_input_transport():
            run2 = live_coordinate_run(
                capability,
                repo_root=ROOT,
                authoritative_acts=acts3,
                workspace_revision=len(acts3),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="c7.run2",
                governance_pins=[],
                surface=disposable.surface,
                output_name="c7_2.json",
            )
        self.assertIsNone(run2.refusal)
        top2_f = next(
            pub.finding for pub in run2.publications if pub.finding.get("symbol") == TOP_ENTRY_SYMBOL
        )
        self.assertEqual(float(top2_f["value"]), 1340.0)
        self.assertIn(closure_1_fid, {p["id"] for p in top2_f["pins"]})

    def test_case8_upgrade_v1_closed_empty_then_v2_statement(self) -> None:
        workspace = self.temp_path / "case8"
        log = ActLog(workspace, self.registry)
        log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)

        # 1. Closed-empty on v1
        res_empty = record_f1099k_no_statements_durably(
            log,
            self.registry,
            submission_id="c8.sub.empty",
            evidence_id="c8.ev.empty",
            actor=USER,
            at="2026-10-18T12:00:00Z",
            expected_revision=log.read().revision,
            family_version="v1",
        )
        v1_closure_id = res_empty["finding_ids"][0]
        state1 = project(log.read().acts, self.registry)
        cur1 = compute_currency(state1)
        self.assertIn(v1_closure_id, cur1.current_finding_ids)

        # 2. Record first statement on v2 with close_family=False
        rep_a = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.alpha",
            statement_ref="demo.statement.bicycle",
            box1a=880.0,
            box4=0.0,
            submission_id="c8.sub.a",
            evidence_id="c8.ev.a",
            actor=USER,
            at="2026-10-18T12:05:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=False,
        )
        rev_a = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c8.rev.a",
            shown_at="2026-10-18T12:05:30Z",
            statement_keys=rep_a["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_a,
            answers=BASE_ANSWERS,
            submission_id="c8.ans.a",
            evidence_ids=_evidence_ids(BASE_ANSWERS, "c8.ev.ans.a"),
            actor=USER,
            at="2026-10-18T12:06:00Z",
        )

        state2 = project(log.read().acts, self.registry)
        cur2 = compute_currency(state2)
        # v1 chain is retired; v1 closure is displaced
        self.assertIn(v1_closure_id, cur2.displaced_finding_ids)
        self.assertNotIn(v1_closure_id, cur2.current_finding_ids)

        post_h = _current_f1099k_horizon(state2)
        self.assertIn(post_h, state2.horizon_state.horizons)

        # Pre-closure run halts SOURCE_SET_UNCLOSED
        disposable = DisposableTrack0Surface(self.temp_path / "surface8")
        adoption = _prepare_adoption(disposable, log, "adopt.c8")
        log.append(adoption, expected_revision=log.read().revision)

        acts2 = log.read().acts
        capability = WorkspaceCapability(workspace)
        with instrumented_sale_input_transport():
            run_pre = live_coordinate_run(
                capability,
                repo_root=ROOT,
                authoritative_acts=acts2,
                workspace_revision=len(acts2),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="c8.pre",
                governance_pins=[],
                surface=disposable.surface,
                output_name="c8_pre.json",
            )
        self.assertIsNone(run_pre.refusal)
        durable_pre = json.loads(run_pre.output_path.read_text("utf-8"))
        top_disp_pre = next(
            d for d in durable_pre["dispositions"] if d.get("artifact_id") == TOP_ENTRY_RULE_ID
        )
        self.assertEqual(top_disp_pre["disposition"], "blocked")
        self.assertEqual(top_disp_pre["code"], BLOCK_CLOSURE)

        # 3. Attest fresh closure on post-transition horizon
        v2_closure_id = _attest_closure(log, post_h, suffix="close.c8")
        acts3 = log.read().acts
        with instrumented_sale_input_transport():
            run_post = live_coordinate_run(
                capability,
                repo_root=ROOT,
                authoritative_acts=acts3,
                workspace_revision=len(acts3),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="c8.post",
                governance_pins=[],
                surface=disposable.surface,
                output_name="c8_post.json",
            )
        self.assertIsNone(run_post.refusal)
        findings = {pub.finding.get("symbol"): pub.finding for pub in run_post.publications}
        top_f = findings.get(TOP_ENTRY_SYMBOL)
        self.assertIsNotNone(top_f)
        assert top_f is not None
        self.assertEqual(float(top_f["value"]), 880.0)

    def test_case9_upgrade_v1_one_statement_then_v2_statement(self) -> None:
        workspace = self.temp_path / "case9"
        log = ActLog(workspace, self.registry)
        log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)

        # 1. Closed single statement on v1
        rep_a = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.alpha",
            statement_ref="demo.statement.bicycle",
            box1a=880.0,
            box4=0.0,
            submission_id="c9.sub.a",
            evidence_id="c9.ev.a",
            actor=USER,
            at="2026-10-18T12:00:00Z",
            expected_revision=log.read().revision,
            family_version="v1",
            close_family=True,
        )
        rev_a = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c9.rev.a",
            shown_at="2026-10-18T12:00:30Z",
            statement_keys=rep_a["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_a,
            answers=BASE_ANSWERS,
            submission_id="c9.ans.a",
            evidence_ids=_evidence_ids(BASE_ANSWERS, "c9.ev.ans.a"),
            actor=USER,
            at="2026-10-18T12:05:00Z",
        )
        b1a_a_fid = rep_a["finding_ids"][0]
        v1_closure_fid = rep_a["finding_ids"][-1]

        # 2. Add second statement on v2 with close_family=False
        rep_b = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.beta",
            statement_ref="demo.statement.camera",
            box1a=460.0,
            box4=0.0,
            submission_id="c9.sub.b",
            evidence_id="c9.ev.b",
            actor=USER,
            at="2026-10-18T12:10:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=False,
        )
        b1a_b_fid = rep_b["finding_ids"][0]
        rev_b = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c9.rev.b",
            shown_at="2026-10-18T12:10:30Z",
            statement_keys=rep_b["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_b,
            answers=ANSWERS_B_LOSS,
            submission_id="c9.ans.b",
            evidence_ids=_evidence_ids(ANSWERS_B_LOSS, "c9.ev.ans.b"),
            actor=USER,
            at="2026-10-18T12:15:00Z",
        )

        state2 = project(log.read().acts, self.registry)
        cur2 = compute_currency(state2)
        # Retained statement A survives in fact lattice and currency
        self.assertIn(b1a_a_fid, cur2.current_finding_ids)
        self.assertIn(b1a_b_fid, cur2.current_finding_ids)
        # v1 closure is displaced
        self.assertIn(v1_closure_fid, cur2.displaced_finding_ids)

        post_h = _current_f1099k_horizon(state2)
        self.assertIn(post_h, state2.horizon_state.horizons)

        # 3. Attest fresh closure on post-transition horizon
        v2_closure_fid = _attest_closure(log, post_h, suffix="close.c9")

        disposable = DisposableTrack0Surface(self.temp_path / "surface9")
        adoption = _prepare_adoption(disposable, log, "adopt.c9")
        log.append(adoption, expected_revision=log.read().revision)

        acts3 = log.read().acts
        capability = WorkspaceCapability(workspace)
        with instrumented_sale_input_transport():
            run_out = live_coordinate_run(
                capability,
                repo_root=ROOT,
                authoritative_acts=acts3,
                workspace_revision=len(acts3),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="c9.run",
                governance_pins=[],
                surface=disposable.surface,
                output_name="c9.json",
            )
        self.assertIsNone(run_out.refusal)
        findings = {pub.finding.get("symbol"): pub.finding for pub in run_out.publications}
        top_f = findings.get(TOP_ENTRY_SYMBOL)
        self.assertIsNotNone(top_f)
        assert top_f is not None
        self.assertEqual(float(top_f["value"]), 1340.0)

    def test_case10_presentation_model_schedule1_field_and_explanations(self) -> None:
        workspace = self.temp_path / "case10"
        log = ActLog(workspace, self.registry)
        log.append_batch(_finish_acts(_make_base_acts()), expected_revision=0)

        rep_a = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.alpha",
            statement_ref="demo.statement.bicycle",
            box1a=880.0,
            box4=0.0,
            submission_id="c10.sub.a",
            evidence_id="c10.ev.a",
            actor=USER,
            at="2026-10-18T12:00:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=False,
        )
        rev_a = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c10.rev.a",
            shown_at="2026-10-18T12:00:30Z",
            statement_keys=rep_a["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_a,
            answers=BASE_ANSWERS,
            submission_id="c10.ans.a",
            evidence_ids=_evidence_ids(BASE_ANSWERS, "c10.ev.ans.a"),
            actor=USER,
            at="2026-10-18T12:05:00Z",
        )

        rep_b = record_f1099k_statement_durably(
            log,
            self.registry,
            payer_id="demo.platform.beta",
            statement_ref="demo.statement.camera",
            box1a=460.0,
            box4=0.0,
            submission_id="c10.sub.b",
            evidence_id="c10.ev.b",
            actor=USER,
            at="2026-10-18T12:10:00Z",
            expected_revision=log.read().revision,
            family_version="v2",
            close_family=True,
        )
        rev_b = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c10.rev.b",
            shown_at="2026-10-18T12:10:30Z",
            statement_keys=rep_b["statement_keys"],
        )
        save_f1099k_statement_review(
            log,
            self.registry,
            rev_b,
            answers=ANSWERS_B_LOSS,
            submission_id="c10.ans.b",
            evidence_ids=_evidence_ids(ANSWERS_B_LOSS, "c10.ev.ans.b"),
            actor=USER,
            at="2026-10-18T12:15:00Z",
        )

        disposable = DisposableTrack0Surface(self.temp_path / "surface10")
        adoption = _prepare_adoption(disposable, log, "adopt.c10")
        log.append(adoption, expected_revision=log.read().revision)

        acts = log.read().acts
        capability = WorkspaceCapability(workspace)
        with instrumented_sale_input_transport():
            run_out = live_coordinate_run(
                capability,
                repo_root=ROOT,
                authoritative_acts=acts,
                workspace_revision=len(acts),
                run_scope=SCOPE,
                scope_user=USER,
                request={"schema": "run-request.v1"},
                run_id="c10.run",
                governance_pins=[],
                surface=disposable.surface,
                output_name="c10.json",
            )
        self.assertIsNone(run_out.refusal)

        model = json.loads(run_out.presentation_path.read_text("utf-8"))
        validate_presentation_model(model)

        # 1. Schedule 1 top entry form field section
        sch1_section = next(
            s
            for s in model["sections"]
            if (s.get("field") or {}).get("id") == "tax.us.2025.schedule1.top-entry.form-field"
        )
        self.assertEqual(sch1_section["resolved"]["disposition"], "published_value")
        self.assertEqual(sch1_section["resolved"]["value"], 1340)

        # 2. f1099kStatementExplanation per-statement entries
        expl = model["f1099kStatementExplanation"]
        self.assertIn(rep_a["statement_keys"]["statement"], expl)
        self.assertIn(rep_b["statement_keys"]["statement"], expl)

        expl_a = expl[rep_a["statement_keys"]["statement"]]
        expl_b = expl[rep_b["statement_keys"]["statement"]]

        self.assertEqual(expl_a["reason"], "supported-loss")
        self.assertEqual(expl_a["computation"]["expectedBox1aGrossAmount"], 880.0)

        self.assertEqual(expl_b["reason"], "supported-loss")
        self.assertEqual(expl_b["computation"]["expectedBox1aGrossAmount"], 460.0)

        # Own reported box1a from review snapshot
        rev_a_fresh = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c10.rev.a.f",
            shown_at="2026-10-18T12:30:00Z",
            statement_keys=rep_a["statement_keys"],
        )
        rev_b_fresh = prepare_f1099k_statement_review(
            log,
            self.registry,
            review_id="c10.rev.b.f",
            shown_at="2026-10-18T12:30:00Z",
            statement_keys=rep_b["statement_keys"],
        )
        self.assertEqual(rev_a_fresh["statement"]["box1a"], 880.0)
        self.assertEqual(rev_b_fresh["statement"]["box1a"], 460.0)


if __name__ == "__main__":
    unittest.main()
