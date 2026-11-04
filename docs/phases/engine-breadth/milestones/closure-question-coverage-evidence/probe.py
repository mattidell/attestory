"""P0 probe: each core v74 source family left unconfirmed, through live_coordinate_run.

Evidence only. Synthetic demo.* facts. Writes probe-output.json beside this file.
Does not modify package content. No absolute paths in the output.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

_HERE = Path(__file__).resolve().parent
for _candidate in _HERE.parents:
    if (_candidate / "packages" / "derivation" / "live.py").is_file():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.facts import fact_id_for
from packages.tax.loader import (
    domain_companion_equality_pairs,
    domain_companion_presence_pairs,
    domain_companion_value_domains,
    domain_package_companion_declarations,
)
from tests import test_w2g_gambling as w2g
from tests.helpers import current_core_returns as ccr
from tests.test_form_1099_k_income import _handover
from tests.test_form_1099_withholding import SCOPE_KEY, YEAR, _add, _close, _introduce
from tests.test_refund_or_amount_owed_track1 import _act, _attested, _finish

P = "tax.us.2025."
CORE_ID = P + "package.core-calculations"
HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "probe-output.json"


def repo_root() -> Path:
    for candidate in HERE.parents:
        if (candidate / "packages" / "derivation" / "live.py").is_file():
            return candidate
    raise SystemExit("repo root not found")


ROOT = repo_root()
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
RELEASE_DIR = ROOT / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
PACKAGE_NAME = "package.core-calculations.v74.json"
RELEASE_NAME = "demo.release.sli-worksheet-integration.2025.v72.json"
REGISTRY_NAME = "published-packages.v72.json"

# Same-statement facts a recorded member needs so the only new block is the closure.
# Values are the ones the current-core return helpers already use.
EXTRA_COMPANIONS: dict[str, list[tuple[str, object]]] = {
    P + "f1098": [
        (P + "f1098.box2-outstanding-principal", 200000.0),
        (P + "f1098.box3-origination-date", "2020-06-01"),
        (P + "f1098.box4-overpaid-refund", 0.0),
        (P + "f1098.box5-mortgage-insurance", 0.0),
        (P + "f1098.box6-points", 0.0),
        (P + "f1098.box9-number-of-properties", 1.0),
        (P + "f1098.box11-other", 0.0),
        *[(P + "f1098." + name, "yes") for name in (
            "liable-and-paid", "qualified-main-home", "acquisition-debt-use", "no-balance-increase",
            "no-refinance", "single-mortgage-single-home", "not-shared-except-spouse",
            "no-mortgage-interest-credit", "owns-the-home", "lives-there-most-of-the-time",
            "filing-unit-owns-home", "shared-main-home", "home-is-collateral", "owes-the-loan",
            "paid-the-interest", "no-one-else-owes-it", "this-is-the-original-loan",
        )],
        (P + "f1098.what-the-money-paid-for", "bought-the-home"),
        (P + "f1098.mortgage-credit-certificate-received", "not-received"),
    ],
    P + "f1098e.1": [
        (P + "f1098e.box2-checked-authority", False),
        *[(P + "f1098e." + name, "yes") for name in (
            "no-related-person-interest", "no-qualified-employer-plan-interest",
            "no-non-qualified-loan-component", "no-employer-educational-assistance-interest",
            "no-qtp-earnings-used",
        )],
    ],
}
# Answers the base already gives, flipped so a recorded member is not refused and is read.
FLIPS: dict[str, list[tuple[str, object]]] = {
    P + "f1099div.2a": [(P + "capital-gain-distributions", "yes")],
    P + "f1098": [(P + "f1098-scope.no-mortgage-statement", False)],
    P + "f1099div.7": [(P + "direct-ftc.election", "yes")],
}
# Applied on both variants. Without the flip the line never reads the family.
READ_ANSWERS: dict[str, list[tuple[str, object]]] = {
    P + "f1099int.b8": [(P + "line2a-scope.no-f1099int-tax-exempt", "no")],
    P + "odc.child-roster": [(P + "ctc.no-other-dependent", "no")],
    P + "odc.relative-roster": [(P + "ctc.no-other-dependent", "no")],
}
PART_II_B = {P + "w2-box4", P + "w2-box6"}
COMPANION_VALUES: dict[str, object] = {
    P + "ssa1099.box3-benefits-paid": 100,
    P + "ssa1099.box4-repayment": 0,
    P + "f1099div.box8-country-companion": "FR",
    P + "f1099div.box1a-ordinary": 100.0,
    P + "ssa1099.recipient": "taxpayer",
    P + "ssa1099.statement-kind": "ssa-1099",
    P + "ssa1099.lump-sum-election": False,
}
REUSE_ENTITIES: dict[str, dict[str, str]] = {
    P + "w2": {"employer": "demo.cgd.t2.employer", "w2-slip": "demo.cgd.t2.w2"},
    P + "w2-box2": {"employer": "demo.cgd.t2.employer", "w2-slip": "demo.cgd.t2.w2"},
    P + "w2-box4": {"employer": "demo.cgd.t2.employer", "w2-slip": "demo.cgd.t2.w2"},
    P + "w2-box6": {"employer": "demo.cgd.t2.employer", "w2-slip": "demo.cgd.t2.w2"},
}
WASH = {P + "f1099b.covered-w-st", P + "f1099b.covered-w-lt"}
LONG_TERM = {P + "f1099b.covered-lt", P + "f1099b.covered-w-lt"}


def scrub(text: str) -> str:
    text = text.replace(str(ROOT), ".")
    text = re.sub(r"/(?:Users|private|tmp|var)/\S+", "<path>", text)
    return text


def walk(node: Any) -> Any:
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


def load_index() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    package = json.loads((CONTENT / PACKAGE_NAME).read_text(encoding="utf-8"))
    idx: dict[tuple[str, str], dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and "id" in body and "version" in body:
            idx[(body["id"], body["version"])] = body
    members = [idx[(row["id"], row["version"])] for row in package["members"]]
    families = {row["id"]: row for row in members if str(row.get("schema", "")).startswith("source-family")}
    mappings = {
        row["family"]["id"]: row
        for row in members
        if str(row.get("schema", "")).startswith("source-closure-mapping")
    }
    fact_types: dict[str, Any] = {}
    bundles: dict[str, Any] = {}
    for row in members:
        for fact_type in row.get("fact_types") or []:
            fact_types[fact_type["id"]] = fact_type
            bundles[fact_type["id"]] = row
    rules = [row for row in members if isinstance(row.get("publishes"), str) or "when" in row or "value" in row]
    return families, mappings, fact_types, {"bundles": bundles, "rules": rules, "members": members}


def read_ops(family_id: str, rules: list[dict[str, Any]]) -> list[str]:
    found: set[str] = set()
    for rule in rules:
        for node in walk(rule):
            if node.get("source_set") == family_id and node.get("op"):
                found.add(str(node["op"]))
            source_family = node.get("source_family")
            if isinstance(source_family, dict) and source_family.get("id") == family_id:
                found.add("source_family")
            family = node.get("family")
            if isinstance(family, dict) and family.get("id") == family_id and node.get("relationship"):
                found.add("accounts_for:" + str(node["relationship"]))
    return sorted(found)


def short(identifier: str) -> str:
    return identifier.replace(P, "").replace(P + "rule.", "")


def finding_of(act: dict[str, Any]) -> dict[str, Any] | None:
    payload = act.get("payload")
    if not isinstance(payload, dict):
        return None
    if act.get("kind") == "member-transition":
        member = payload.get("member")
        if isinstance(member, dict) and isinstance(member.get("finding"), dict):
            return member["finding"]
        return None
    finding = payload.get("finding")
    return finding if isinstance(finding, dict) else None


def fact_type_of(fact_id: str) -> str:
    return fact_id.split("|", 1)[0]


def has_member(acts: list[dict[str, Any]], fact_type: str) -> bool:
    return any(
        isinstance(finding := finding_of(act), dict) and str(finding.get("fact_id", "")).startswith(fact_type + "|")
        for act in acts
    )


def horizon_version(acts: list[dict[str, Any]], family_id: str) -> str | None:
    for act in acts:
        payload = act.get("payload")
        if act.get("kind") == "horizon-genesis" and isinstance(payload, dict):
            family = payload.get("family")
            if isinstance(family, dict) and family.get("id") == family_id:
                return str(family.get("version"))
    return None


def strip_closure(acts: list[dict[str, Any]], closure_type: str) -> list[dict[str, Any]]:
    kept = []
    prefix = closure_type + "|"
    for act in acts:
        finding = finding_of(act)
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(prefix):
            continue
        kept.append(act)
    return kept


def drop_members(acts: list[dict[str, Any]], family_id: str, fact_type: str) -> list[dict[str, Any]]:
    kept = []
    prefix = fact_type + "|"
    for act in acts:
        payload = act.get("payload")
        if act.get("kind") == "member-transition" and isinstance(payload, dict):
            family = payload.get("family")
            if isinstance(family, dict) and family.get("id") == family_id:
                continue
        finding = finding_of(act)
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(prefix):
            continue
        kept.append(act)
    return kept


def set_answer(acts: list[dict[str, Any]], fact_type: str, value: object) -> None:
    hits = 0
    for act in acts:
        finding = finding_of(act)
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(fact_type + "|"):
            finding["value"] = value
            hits += 1
    if hits != 1:
        raise AssertionError(f"expected one {fact_type} answer, found {hits}")


def adopted(acts: list[dict[str, Any]]) -> set[str]:
    found: set[str] = set()
    for act in acts:
        if act.get("kind") != "bundle-adoption":
            continue
        payload = act.get("payload")
        bundle = payload.get("bundle") if isinstance(payload, dict) else None
        if isinstance(bundle, dict):
            for fact_type in bundle.get("fact_types") or []:
                found.add(str(fact_type["id"]))
    return found


def adopt(acts: list[dict[str, Any]], fact_type: str, bundles: dict[str, Any]) -> None:
    if fact_type in adopted(acts):
        return
    bundle = bundles.get(fact_type)
    if bundle is None:
        raise AssertionError(f"no adopted bundle carries {fact_type}")
    _add(acts, "bundle-adoption", {"bundle": bundle})


def scalar_value(fact_type: dict[str, Any]) -> object:
    schema = fact_type.get("value_schema") or {}
    if "enum" in schema:
        return "yes" if "yes" in schema["enum"] else schema["enum"][0]
    if schema.get("type") == "boolean":
        return True
    if schema.get("type") == "string":
        return "demo"
    return 100


def object_value(schema: dict[str, Any], family_id: str) -> dict[str, Any]:
    props = schema.get("properties") or {}
    required = list(schema.get("required") or [])
    wash = family_id in WASH
    value: dict[str, Any] = {}
    for name in required:
        spec = props.get(name) or {}
        if "enum" in spec:
            if name == "box_1g_wash_sale_adjustment":
                value[name] = "yes" if wash else "no"
            elif name == "long_term":
                value[name] = "yes" if family_id in LONG_TERM else "no"
            elif name in ("covered_security", "basis_reported_to_irs"):
                value[name] = "yes"
            else:
                value[name] = "no" if "no" in spec["enum"] else spec["enum"][0]
        elif spec.get("type") == "number":
            value[name] = 0
        elif spec.get("type") == "boolean":
            value[name] = False
        else:
            value[name] = "demo"
    if "proceeds" in props:
        value["proceeds"] = 100
        value["basis"] = 250 if wash else 40
    if wash:
        value["box_1g_wash_sale_adjustment"] = "yes"
        value["box_1g_wash_sale_disallowed_amount"] = 50
    return value


def member_value(fact_type: dict[str, Any], family_id: str) -> object:
    schema = fact_type.get("value_schema") or {}
    if schema.get("type") == "object":
        return object_value(schema, family_id)
    return scalar_value(fact_type)


def v74_companions(fact_type_id: str) -> dict[str, str | list[str] | None]:
    pairs: dict[str, str | list[str] | None] = dict(domain_companion_presence_pairs())
    domains = dict(domain_companion_value_domains())
    overlay = domain_package_companion_declarations()[(CORE_ID, "v74")]
    for key, value in overlay["presence_pairs"].items():
        if value is None:
            pairs.pop(key, None)
        else:
            pairs[key] = value
    for key, value in overlay["value_domains"].items():
        if value is None:
            domains.pop(key, None)
        else:
            domains[key] = value
    raw = pairs.get(fact_type_id)
    listed = [raw] if isinstance(raw, str) else list(raw or [])
    return {"ids": listed, "domains": domains}  # type: ignore[return-value]


_MISSING = object()


def _same(left: object, right: object) -> bool:
    # False == 0, so domain membership has to be by value and type.
    return left == right and type(left) is type(right)


def companion_value(companion_id: str, domains: dict[str, Any], member: object, member_type: str) -> object:
    if domain_companion_equality_pairs().get(member_type) == companion_id:
        return member
    if companion_id in COMPANION_VALUES:
        return COMPANION_VALUES[companion_id]
    if companion_id in domains:
        values = list(domains[companion_id])
        for prefer in (None, 0, 0.0, False, "yes", "no", "taxpayer"):
            if any(_same(item, prefer) for item in values):
                return prefer
        return sorted(values, key=lambda item: (item is None, str(item)))[0]
    return _MISSING


def keys_for(fact_type: dict[str, Any], entities: dict[str, str]) -> tuple[tuple[str, str], ...]:
    bound: list[tuple[str, str]] = []
    for key in fact_type["identity_keys"]:
        if key["kind"] == "entity":
            entity_id = entities.get(key["name"])
            if entity_id is None:
                raise AssertionError(f"{fact_type['id']} needs entity key {key['name']}")
            bound.append((key["name"], entity_id))
        else:
            bound.append((key["name"], key["values"][0]))
    return tuple(bound)


def introduced(acts: list[dict[str, Any]]) -> set[str]:
    found: set[str] = set()
    for act in acts:
        if act.get("kind") != "entity-introduced":
            continue
        payload = act.get("payload")
        entity = payload.get("entity") if isinstance(payload, dict) else None
        if isinstance(entity, dict):
            found.add(str(entity.get("id")))
    return found


def ensure_entities(acts: list[dict[str, Any]], fact_type: dict[str, Any], tag: str, reuse: dict[str, str]) -> dict[str, str]:
    entities = dict(reuse)
    have = introduced(acts)
    for key in fact_type["identity_keys"]:
        if key["kind"] != "entity":
            continue
        if key["name"] not in entities:
            entities[key["name"]] = f"demo.p0.{tag}.{key['name']}"
        entity_id = entities[key["name"]]
        if entity_id not in have:
            _introduce(acts, entity_id, key["entity_kind"])
            have.add(entity_id)
    return entities


def assert_fact(acts: list[dict[str, Any]], finding_id: str, fact_type: dict[str, Any], entities: dict[str, str], value: object) -> None:
    fact_id = fact_id_for(fact_type["id"], keys_for(fact_type, entities))
    _add(acts, "assertion", {"finding": _attested(finding_id, fact_id, value)})


def add_member(
    acts: list[dict[str, Any]],
    family: dict[str, Any],
    mapping: dict[str, Any],
    fact_types: dict[str, Any],
    bundles: dict[str, Any],
) -> str:
    family_id = family["id"]
    fact_type = fact_types[family["member_predicate"]["fact_type"]]
    version = horizon_version(acts, family_id)
    mapped = str(mapping["family"]["version"])
    if version is None:
        version = mapped
        _add(acts, "horizon-genesis", {
            "family": {"id": family_id, "version": version},
            "scope": dict(SCOPE_KEY),
            "horizon_id": f"demo.p0.{short(family_id).replace('.', '-')}.h0",
        })
    elif version != mapped and family_id != P + "ssa1099.benefits":
        raise AssertionError(f"{family_id} horizon {version} does not match mapping {mapped}")
    tag = short(family_id).replace(".", "-")
    entities = ensure_entities(acts, fact_type, tag, REUSE_ENTITIES.get(family_id, {}))
    adopt(acts, fact_type["id"], bundles)
    value = member_value(fact_type, family_id)
    spec = v74_companions(fact_type["id"])
    companion_ids = list(spec["ids"])
    for companion_id, _companion_value in EXTRA_COMPANIONS.get(family_id, []):
        if companion_id not in companion_ids:
            companion_ids.append(companion_id)
    for index, companion_id in enumerate(companion_ids):
        companion = fact_types.get(companion_id)
        if companion is None:
            raise AssertionError(f"companion {companion_id} is not in the v74 bundles")
        adopt(acts, companion_id, bundles)
        if companion_id in {item[0] for item in EXTRA_COMPANIONS.get(family_id, [])}:
            companion_amount = next(item[1] for item in EXTRA_COMPANIONS[family_id] if item[0] == companion_id)
        else:
            companion_amount = companion_value(companion_id, spec["domains"], value, fact_type["id"])
            if companion_amount is _MISSING:
                companion_amount = scalar_value(companion)
        ensure_entities(acts, companion, tag, entities)
        assert_fact(acts, f"demo.p0.{tag}.companion{index}", companion, entities, companion_amount)
    horizons: list[str] = []
    for act in acts:
        payload = act.get("payload")
        if not isinstance(payload, dict):
            continue
        if act.get("kind") == "horizon-genesis" and payload.get("family", {}).get("id") == family_id:
            horizons.append(str(payload["horizon_id"]))
        elif act.get("kind") == "member-transition" and payload.get("family", {}).get("id") == family_id:
            horizons.append(str(payload["successor"]["id"]))
    if not horizons:
        raise AssertionError(f"no horizon for {family_id}")
    successor = f"demo.p0.{tag}.h1"
    fact_id = fact_id_for(fact_type["id"], keys_for(fact_type, entities))
    _add(acts, "member-transition", {
        "family": {"id": family_id, "version": version},
        "scope": dict(SCOPE_KEY),
        "member": {"action": "assert", "finding": _attested(f"demo.p0.{tag}.member", fact_id, value)},
        "successor": {"id": successor, "predecessor": horizons[-1]},
    })
    return "added one member"


def align_family_version(acts: list[dict[str, Any]], family_id: str, version: str) -> bool:
    changed = False
    for act in acts:
        payload = act.get("payload")
        if not isinstance(payload, dict):
            continue
        family = payload.get("family")
        if act.get("kind") in ("horizon-genesis", "member-transition") and isinstance(family, dict) and family.get("id") == family_id:
            if family.get("version") != version:
                family["version"] = version
                changed = True
    return changed


def latest_horizon(acts: list[dict[str, Any]], family_id: str) -> str:
    horizons: list[str] = []
    for act in acts:
        payload = act.get("payload")
        if not isinstance(payload, dict):
            continue
        if act.get("kind") == "horizon-genesis" and payload.get("family", {}).get("id") == family_id:
            horizons.append(str(payload["horizon_id"]))
        elif act.get("kind") == "member-transition" and payload.get("family", {}).get("id") == family_id:
            horizons.append(str(payload["successor"]["id"]))
    if not horizons:
        raise AssertionError(f"no horizon for {family_id}")
    return horizons[-1]


def ensure_w2g_winning(
    acts: list[dict[str, Any]],
    families: dict[str, Any],
    mappings: dict[str, Any],
    fact_types: dict[str, Any],
    bundles: dict[str, Any],
) -> str:
    """Schedule A line 16 reads gambling losses only when a Form W-2G winning is on record."""
    family_id = P + "w2g.b1"
    fact_type_id = families[family_id]["member_predicate"]["fact_type"]
    if has_member(acts, fact_type_id):
        return ""
    mapping = mappings[family_id]
    closure = mapping["closure_fact_type"]["id"]
    kept = strip_closure(acts, closure)
    acts.clear()
    acts.extend(kept)
    note = add_member(acts, families[family_id], mapping, fact_types, bundles)
    _close(acts, closure, latest_horizon(acts, family_id), "demo.p0.w2g-b1.reclose")
    return "closed one w2g winning (" + note + "); "


def prepare(family_id: str, variant: str) -> tuple[list[dict[str, Any]], str]:
    families, mappings, fact_types, extra = load_index()
    family = families[family_id]
    mapping = mappings[family_id]
    fact_type_id = family["member_predicate"]["fact_type"]
    note = ""
    if family_id in PART_II_B:
        acts = ccr.part_ii_b_return(box4=100.0, box6=100.0)
        note = "part II-B return; "
    else:
        acts = w2g._w2g_return([])
    if family_id == P + "gambling.losses":
        note += ensure_w2g_winning(acts, families, mappings, fact_types, extra["bundles"])
    for fact_type, value in READ_ANSWERS.get(family_id, []):
        set_answer(acts, fact_type, value)
        note += f"set {short(fact_type)} ; "
    mapped = str(mapping["family"]["version"])
    if variant == "members":
        for fact_type, value in FLIPS.get(family_id, []):
            set_answer(acts, fact_type, value)
            note += f"set {short(fact_type)} ; "
        if family_id != P + "ssa1099.benefits" and align_family_version(acts, family_id, mapped):
            note += f"aligned horizon to {mapped}; "
        if has_member(acts, fact_type_id):
            note += "kept the existing member"
        else:
            note += add_member(acts, family, mapping, fact_types, extra["bundles"])
    elif variant == "none":
        acts = drop_members(acts, family_id, fact_type_id)
        note += "removed members" if not has_member(acts, fact_type_id) else "members remained"
        if family_id != P + "ssa1099.benefits" and align_family_version(acts, family_id, mapped):
            note += f"; aligned horizon to {mapped}"
    else:
        raise AssertionError(variant)
    acts = strip_closure(acts, mapping["closure_fact_type"]["id"])
    note += "; removed only that closure"
    return ccr._renumbered(acts), note


def surface() -> PublicationSurface:
    return PublicationSurface(RELEASE_DIR, CONTENT / REGISTRY_NAME, CONTENT)


def execute(acts: list[dict[str, Any]], run_id: str, *, reconfirm: bool = True) -> dict[str, Any]:
    package = CONTENT / PACKAGE_NAME
    release = RELEASE_DIR / RELEASE_NAME
    finished = _handover(
        _finish(
            copy.deepcopy(acts), package_path=package, package_version="v74",
            release_path=release, release_version="v72", note=run_id,
        ),
        surface=surface(), reconfirm=reconfirm,
    )
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"), repo_root=ROOT, authoritative_acts=finished,
            workspace_revision=len(finished), run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=ccr.USER, request={"schema": "run-request.v1"}, run_id=run_id,
            governance_pins=[], surface=surface(), output_name="out.json",
        )
        if outcome.refusal is not None:
            return {"refused": scrub(f"{outcome.refusal.reason} {outcome.refusal.detail}")}
        assert outcome.output_path is not None and outcome.presentation_path is not None
        report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
        model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    return {"dispositions": list(report.get("dispositions") or []), "model": model}


def rules_by_id() -> dict[str, dict[str, Any]]:
    _families, _mappings, _fact_types, extra = load_index()
    found: dict[str, dict[str, Any]] = {}
    for row in extra["members"]:
        if isinstance(row.get("id"), str) and isinstance(row.get("publishes"), str):
            found[row["id"]] = row
    return found


def by_symbol(dispositions: list[dict[str, Any]], rules: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in dispositions:
        symbol = row.get("symbol")
        if symbol is None:
            rule = rules.get(str(row.get("artifact_id")))
            symbol = rule.get("publishes") if rule else None
        if isinstance(symbol, str):
            grouped.setdefault(symbol, []).append(row)
    return grouped


def terminals(row: dict[str, Any], grouped: dict[str, list[dict[str, Any]]]) -> frozenset[tuple[str, str, tuple[str, ...]]]:
    """Unique blocked leaves. One result per artifact, so a shared dependency is stored once."""
    memo: dict[tuple[str, str, tuple[str, ...]], frozenset[tuple[str, str, tuple[str, ...]]]] = {}
    visiting: set[tuple[str, str, tuple[str, ...]]] = set()

    def reach(current: dict[str, Any]) -> frozenset[tuple[str, str, tuple[str, ...]]]:
        artifact = str(current.get("artifact_id") or "")
        code = str(current.get("code") or "")
        missing = tuple(str(item) for item in current.get("missing") or [])
        key = (artifact, code, missing)
        cached = memo.get(key)
        if cached is not None:
            return cached
        if key in visiting:
            return frozenset({key})
        visiting.add(key)
        if code == "SOURCE_SET_UNCLOSED" or not missing:
            found = frozenset({key})
        else:
            children = [
                item
                for symbol in missing
                for item in grouped.get(symbol, [])
                if item.get("disposition") == "blocked"
            ]
            if not children:
                found = frozenset({key})
            else:
                found = frozenset().union(*(reach(child) for child in children))
        visiting.discard(key)
        memo[key] = found
        return found

    if not row.get("code") and not row.get("artifact_id"):
        return frozenset()
    return reach(row)


def concerns(family_id: str, missing: tuple[str, ...] | list[str]) -> bool:
    prefix = family_id + "."
    return any(item == family_id or item.startswith(prefix) for item in missing)


def pack_root(root: tuple[str, str, tuple[str, ...]]) -> dict[str, Any]:
    return {
        "artifact_id": short(root[0]),
        "code": root[1],
        "missing": [short(item) for item in root[2]],
    }


def summarize(family_id: str, question: str, payload: dict[str, Any]) -> dict[str, Any]:
    if "refused" in payload:
        return {
            "refused": payload["refused"], "blocked_lines": [], "names_on": [],
            "family_root_codes": [], "read": False,
        }
    rules = rules_by_id()
    grouped = by_symbol(payload["dispositions"], rules)
    lines = []
    about_roots: set[tuple[str, str, tuple[str, ...]]] = set()
    other_roots: set[tuple[str, str, tuple[str, ...]]] = set()
    names_on: list[str] = []
    unnamed: list[str] = []
    for section in payload["model"].get("sections") or []:
        resolved = section.get("resolved") or {}
        if resolved.get("disposition") != "blocked":
            continue
        field = section.get("field") or {}
        symbol = str(field.get("binds_symbol") or "")
        rows = [row for row in grouped.get(symbol, []) if row.get("disposition") == "blocked"]
        roots: set[tuple[str, str, tuple[str, ...]]] = set()
        for row in rows:
            roots |= terminals(row, grouped)
        reasons = resolved.get("reasons")
        sentences = [str(item.get("sentence")) for item in reasons if isinstance(item, dict)] if reasons else []
        names = bool(question) and question in sentences
        line = str(field.get("line") or field.get("id"))
        about = [root for root in roots if concerns(family_id, root[2])]
        record = {
            "line": line,
            "symbol": short(symbol),
            "code": rows[0].get("code") if len(rows) == 1 else None,
            "missing": [short(str(item)) for item in (rows[0].get("missing") or [])] if len(rows) == 1 else [],
            "names_question": names,
            "root_codes": sorted({root[1] for root in roots}),
            "about_family": bool(about),
        }
        if sentences and not names:
            record["other_reasons"] = sentences
        if about:
            about_roots.update(about)
            if names:
                names_on.append(line)
            else:
                unnamed.append(line)
        else:
            other_roots.update(roots)
        lines.append(record)
    direct = []
    for row in payload["dispositions"]:
        if row.get("disposition") != "blocked":
            continue
        missing = [str(item) for item in row.get("missing") or []]
        if concerns(family_id, missing):
            direct.append({
                "artifact_id": short(str(row.get("artifact_id"))),
                "code": row.get("code"),
                "missing": [short(item) for item in missing],
            })
            about_roots.add((str(row.get("artifact_id") or ""), str(row.get("code") or ""), tuple(missing)))
    about_lines = [line for line in lines if line["about_family"]]
    return {
        "blocked_lines": about_lines,
        "blocked_line_count": len(about_lines),
        "other_blocked_count": len(lines) - len(about_lines),
        "names_on": names_on,
        "unnamed": unnamed,
        "family_root_codes": sorted({root[1] for root in about_roots}),
        "family_roots": [pack_root(root) for root in sorted(about_roots)],
        "other_roots": [pack_root(root) for root in sorted(other_roots)][:12],
        "direct_blocks": direct,
        "read": bool(about_lines or direct),
    }


def run_case(family_id: str, variant: str) -> dict[str, Any]:
    started = time.monotonic()
    try:
        acts, note = prepare(family_id, variant)
        _families, mappings, _fact_types, _extra = load_index()
        question = str(mappings[family_id].get("closure_question") or "")
        payload = execute(
            acts,
            f"demo.p0.{short(family_id).replace('.', '-')}.{variant}",
            reconfirm=family_id != P + "ssa1099.benefits",
        )
        summary = summarize(family_id, question, payload)
        summary["setup"] = note
    except Exception as exc:  # one family must not abort the survey
        summary = {"error": scrub(f"{type(exc).__name__}: {exc}"), "trace": scrub(traceback.format_exc(limit=8))}
    summary["seconds"] = round(time.monotonic() - started, 2)
    return summary


def inventory() -> list[dict[str, Any]]:
    families, mappings, _fact_types, extra = load_index()
    rows = []
    for family_id in sorted(mappings):
        mapping = mappings[family_id]
        family = families.get(family_id)
        question = mapping.get("closure_question")
        kinds = [
            name for name in ("member_constraints", "identity_exclusivity", "itemizations", "completeness")
            if isinstance(family, dict) and family.get(name)
        ]
        rows.append({
            "family": family_id,
            "short": short(family_id),
            "mapping": mapping["id"],
            "mapping_version": mapping["version"],
            "family_version": None if family is None else family.get("version"),
            "member_fact_type": (mapping.get("member_fact_type") or {}).get("id"),
            "closure_fact_type": (mapping.get("closure_fact_type") or {}).get("id"),
            "question": question,
            "question_missing": not (isinstance(question, str) and question.strip()),
            "reads": read_ops(family_id, extra["rules"]),
            "constrained": bool(kinds),
            "constraint_kinds": kinds,
            "declared": family is not None,
        })
    return rows


def run_base() -> dict[str, Any]:
    started = time.monotonic()
    try:
        payload = execute(ccr._renumbered(w2g._w2g_return([])), "demo.p0.base")
        summary = summarize("", "", payload)
    except Exception as exc:
        summary = {"error": scrub(f"{type(exc).__name__}: {exc}")}
    summary["seconds"] = round(time.monotonic() - started, 2)
    return summary


def save(document: dict[str, Any]) -> None:
    OUTPUT.write_text(json.dumps(document, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append", default=[])
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    rows = inventory()
    if args.list:
        for row in rows:
            print(
                f"{row['short']}\t{row['family_version']}\t{','.join(row['reads'])}"
                f"\t{','.join(row['constraint_kinds']) or '-'}\t{row['question_missing']}"
            )
        return
    if args.only:
        wanted = set(args.only)
        rows = [row for row in rows if row["short"] in wanted or row["family"] in wanted]
    document: dict[str, Any] = {
        "core": "v74",
        "package": PACKAGE_NAME,
        "families_checked": [row["short"] for row in rows],
        "inventory": rows,
        "base": {},
        "results": {},
    }
    if args.resume and OUTPUT.is_file():
        previous = json.loads(OUTPUT.read_text(encoding="utf-8"))
        if previous.get("core") == "v74" and isinstance(previous.get("results"), dict):
            document["base"] = previous.get("base") or {}
            document["results"] = previous["results"]
    save(document)
    if not document["base"]:
        document["base"] = run_base()
        save(document)
    print(f"base blocked={document['base'].get('blocked_line_count')} error={document['base'].get('error')} seconds={document['base'].get('seconds')}", flush=True)

    def finished(record: object) -> bool:
        return isinstance(record, dict) and "error" not in record and "family_roots" in record and "seconds" in record

    tasks = [
        (row["family"], variant)
        for row in rows
        for variant in ("none", "members")
        if not finished(document["results"].get(short(row["family"]), {}).get(variant))
    ]
    if args.workers <= 1:
        for family_id, variant in tasks:
            record = run_case(family_id, variant)
            document["results"].setdefault(short(family_id), {})[variant] = record
            save(document)
            print(
                f"{short(family_id)} {variant} read={record.get('read')} lines={record.get('blocked_line_count')} "
                f"unnamed={len(record.get('unnamed') or [])} codes={record.get('family_root_codes')} "
                f"err={record.get('error') or record.get('refused')}",
                flush=True,
            )
        return
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(run_case, family_id, variant): (family_id, variant) for family_id, variant in tasks}
        for future in as_completed(futures):
            family_id, variant = futures[future]
            record = future.result()
            document["results"].setdefault(short(family_id), {})[variant] = record
            save(document)
            print(
                f"{short(family_id)} {variant} read={record.get('read')} lines={record.get('blocked_line_count')} "
                f"unnamed={len(record.get('unnamed') or [])} codes={record.get('family_root_codes')} "
                f"err={record.get('error') or record.get('refused')}",
                flush=True,
            )


if __name__ == "__main__":
    main()
