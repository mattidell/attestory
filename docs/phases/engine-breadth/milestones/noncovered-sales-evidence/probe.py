"""What core v78 does with a sale whose basis was not reported.

Synthetic demo.* findings on the wage return. Reads production content.
Writes the JSON summary beside this file. Does not edit packages/.
"""

from __future__ import annotations

import copy
import json
import re
import sys
import traceback
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.facts import fact_id_for
from tests.helpers import current_core_returns as ccr
from tests.test_collect_closure import _adopt
from tests.test_form_1099_k_income import _handover
from tests.test_form_1099_withholding import YEAR, _add, _close, _introduce
from tests.test_refund_or_amount_owed_track1 import _attested, _finish
from tests.test_withholding_closure import _strip_closure

EVIDENCE = Path(__file__).resolve().parent
CONTENT = ccr.CONTENT
PACKAGE = "package.core-calculations.v78.json"
PACKAGE_VERSION = "v78"
REGISTRY = "published-packages.v76.json"
RELEASE_DIR = ccr.RELEASE_DIR
RELEASE = "demo.release.sli-worksheet-integration.2025.v76.json"
RELEASE_VERSION = "v76"
NO_8949 = "tax.us.2025.schedule-d-boundary.no-form8949-sources"
NO_OTHER = "tax.us.2025.schedule-d-boundary.no-other-form8949-adjustments"
KEEP = (
    "schedule-d.line",
    "form1040.line-7",
    "form1040.line-15",
    "form1040.line-16",
    "preferential",
    "qdcg",
    "capital-gain",
    "taxable",
    "attachment.f8949",
    "attachment.schedule-d",
)


def scrub(text: str) -> str:
    text = text.replace(str(ccr.ROOT), ".")
    text = re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", text)
    return text


def load_indexes() -> tuple[dict[tuple[str, str], dict[str, Any]], dict[str, dict[str, Any]]]:
    families: dict[tuple[str, str], dict[str, Any]] = {}
    fact_types: dict[str, dict[str, Any]] = {}
    for path in CONTENT.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if not isinstance(body, dict):
            continue
        schema = str(body.get("schema", ""))
        if schema.startswith("source-family") and "id" in body and "version" in body:
            families[(str(body["id"]), str(body["version"]))] = body
        if schema == "bundle.v2":
            for fact_type in body.get("fact_types") or []:
                if isinstance(fact_type, dict) and "id" in fact_type:
                    fact_types[str(fact_type["id"])] = fact_type
    return families, fact_types


FAMILIES, FACT_TYPES = load_indexes()


def family_version(acts: list[dict[str, Any]], family_id: str) -> str:
    for act in acts:
        payload = act.get("payload")
        if act.get("kind") != "horizon-genesis" or not isinstance(payload, dict):
            continue
        family = payload.get("family")
        if isinstance(family, dict) and family.get("id") == family_id:
            return str(family["version"])
    raise AssertionError(f"no horizon for {family_id}")


def horizons(acts: list[dict[str, Any]], family_id: str) -> list[str]:
    found: list[str] = []
    for act in acts:
        payload = act.get("payload")
        if not isinstance(payload, dict):
            continue
        family = payload.get("family")
        if not isinstance(family, dict) or family.get("id") != family_id:
            continue
        if act.get("kind") == "horizon-genesis":
            found.append(str(payload["horizon_id"]))
        elif act.get("kind") == "member-transition":
            found.append(str(payload["successor"]["id"]))
    return found


def record(acts: list[dict[str, Any]], family_id: str, value: object, tag: str) -> list[dict[str, Any]]:
    """One member of an already-genesis'd family, then close that family again."""
    out = _strip_closure(copy.deepcopy(acts), family_id + ".source-closure")
    version = family_version(out, family_id)
    family = FAMILIES[(family_id, version)]
    fact_type = FACT_TYPES[str(family["member_predicate"]["fact_type"])]
    _adopt(out, fact_type["id"])
    declared: list[tuple[str, str]] = []
    for key in fact_type["identity_keys"]:
        if key["kind"] == "entity":
            entity_id = f"demo.ns.{tag}.{key['name']}"
            if not any(
                act.get("kind") == "entity-introduced"
                and isinstance(act.get("payload"), dict)
                and isinstance(act["payload"].get("entity"), dict)
                and act["payload"]["entity"].get("id") == entity_id
                for act in out
            ):
                _introduce(out, entity_id, key["entity_kind"])
            declared.append((key["name"], entity_id))
        else:
            declared.append((key["name"], key["values"][0]))
    head = horizons(out, family_id)[-1]
    horizon_index = len(horizons(out, family_id))
    successor = f"demo.ns.{tag}.h{horizon_index}"
    _add(out, "member-transition", {
        "family": {"id": family_id, "version": version},
        "scope": {"tax-year": YEAR, "subject": "demo.primary"},
        "member": {
            "action": "assert",
            "finding": _attested(
                f"demo.ns.{tag}.member.h{horizon_index}",
                fact_id_for(fact_type["id"], tuple(declared)),
                value,
            ),
        },
        "successor": {"id": successor, "predecessor": head},
    })
    _close(out, family_id + ".source-closure", successor, f"demo.ns.{tag}.closure")
    return ccr._renumbered(out)


def _identity(acts: list[dict[str, Any]], family_id: str, tag: str) -> tuple[str, tuple[tuple[str, str], ...]]:
    version = family_version(acts, family_id)
    family = FAMILIES[(family_id, version)]
    fact_type = FACT_TYPES[str(family["member_predicate"]["fact_type"])]
    declared: list[tuple[str, str]] = []
    for key in fact_type["identity_keys"]:
        if key["kind"] == "entity":
            declared.append((key["name"], f"demo.ns.{tag}.{key['name']}"))
        else:
            declared.append((key["name"], key["values"][0]))
    return fact_type["id"], tuple(declared)


def correct(acts: list[dict[str, Any]], family_id: str, value: object, tag: str) -> list[dict[str, Any]]:
    """Same-member value correction. A second transition of the same fact is rejected; the ordinary assertion path is the one the kernel names."""
    out = copy.deepcopy(acts)
    fact_type_id, declared = _identity(out, family_id, tag)
    _add(out, "assertion", {
        "finding": _attested(
            f"demo.ns.{tag}.corrected",
            fact_id_for(fact_type_id, declared),
            value,
        ),
    })
    return ccr._renumbered(out)


def answer(acts: list[dict[str, Any]], fact_type: str, value: object, tag: str) -> list[dict[str, Any]]:
    hits = 0
    for act in acts:
        payload = act.get("payload")
        finding = payload.get("finding") if isinstance(payload, dict) else None
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(fact_type + "|"):
            finding["value"] = value
            hits += 1
    if hits == 1:
        return acts
    if hits != 0:
        raise AssertionError(f"{fact_type} answered {hits} times")
    out = copy.deepcopy(acts)
    _adopt(out, fact_type)
    _add(out, "assertion", {
        "finding": _attested(
            f"demo.ns.{tag}",
            fact_id_for(fact_type, (("tax-year", YEAR),)),
            value,
        ),
    })
    return ccr._renumbered(out)


def txn(
    *,
    proceeds: float,
    basis: float | None,
    long_term: str,
    wash: float | None = None,
    reported: str = "no",
    covered: str = "no",
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "proceeds": proceeds,
        "covered_security": covered,
        "basis_reported_to_irs": reported,
        "long_term": long_term,
        "box_1f_market_discount": "no",
        "box_1g_wash_sale_adjustment": "yes" if wash is not None else "no",
        "ordinary_indicated": "no",
        "qof_indicated": "no",
        "taxpayer_side_adjustment": "no",
        "collectibles_or_special_rate": "no",
    }
    if basis is not None:
        value["basis"] = basis
    if wash is not None:
        value["box_1g_wash_sale_disallowed_amount"] = wash
    return value


def direct(acts: list[dict[str, Any]], term: str, proceeds: float, basis: float | None, tag: str) -> list[dict[str, Any]]:
    """Put a basis-not-reported sale on the covered direct-report families. That is the only place v78 can hold it."""
    acts = record(acts, f"tax.us.2025.f1099b.covered-{term}", txn(
        proceeds=proceeds, basis=basis, long_term="yes" if term == "lt" else "no",
    ), tag + "o")
    acts = record(acts, f"tax.us.2025.f1099b.covered-{term}-proceeds", proceeds, tag + "p")
    if basis is not None:
        acts = record(acts, f"tax.us.2025.f1099b.covered-{term}-basis", basis, tag + "b")
    return acts


def wash(acts: list[dict[str, Any]], term: str, proceeds: float, basis: float, adjustment: float, tag: str) -> list[dict[str, Any]]:
    acts = record(acts, f"tax.us.2025.f1099b.covered-w-{term}", txn(
        proceeds=proceeds, basis=basis, long_term="yes" if term == "lt" else "no", wash=adjustment,
    ), tag + "o")
    acts = record(acts, f"tax.us.2025.f1099b.covered-w-{term}-proceeds", proceeds, tag + "p")
    acts = record(acts, f"tax.us.2025.f1099b.covered-w-{term}-basis", basis, tag + "b")
    acts = record(acts, f"tax.us.2025.f1099b.covered-w-{term}-adjustment", adjustment, tag + "a")
    return acts


def boundary(acts: list[dict[str, Any]], form8949: str, other: str | None) -> list[dict[str, Any]]:
    acts = answer(acts, NO_8949, form8949, "no8949")
    if other is not None:
        acts = answer(acts, NO_OTHER, other, "noother")
    return acts


def cases() -> dict[str, list[dict[str, Any]]]:
    base = ccr.base_return()
    lt = direct(copy.deepcopy(base), "lt", 6000.0, 2000.0, "lt")
    st = direct(copy.deepcopy(base), "st", 2000.0, 8000.0, "st")
    mixed = direct(direct(copy.deepcopy(base), "st", 5000.0, 4000.0, "mxst"), "lt", 6000.0, 2000.0, "mxlt")
    washed = wash(copy.deepcopy(base), "lt", 4000.0, 7000.0, 1000.0, "w")
    omitted = direct(copy.deepcopy(base), "lt", 6000.0, None, "omit")
    unclosed = _strip_closure(
        record(copy.deepcopy(base), "tax.us.2025.f1099b.covered-lt-proceeds", 6000.0, "openp"),
        "tax.us.2025.f1099b.covered-lt-basis.source-closure",
    )
    return {
        "baseline": base,
        "lt_gain_on_covered_family": lt,
        "lt_gain_boundary_no": boundary(copy.deepcopy(lt), "no", "no"),
        "st_loss_on_covered_family": st,
        "st_loss_boundary_no": boundary(copy.deepcopy(st), "no", "no"),
        "mixed_on_covered_families": mixed,
        "wash_on_covered_w_path_b": boundary(copy.deepcopy(washed), "no", "yes"),
        "wash_boundary_no": boundary(copy.deepcopy(washed), "no", "no"),
        "basis_omitted_on_object": omitted,
        "basis_family_unclosed": ccr._renumbered(unclosed),
    }


def interesting(symbol: str) -> bool:
    return any(piece in symbol for piece in KEEP)


def summarize_run(outcome: Any) -> dict[str, Any]:
    if outcome.refusal is not None:
        return {
            "refusal": {"reason": outcome.refusal.reason, "detail": scrub(str(outcome.refusal.detail))[:500]},
            "published": [],
            "blocked": [],
            "lines": [],
        }
    assert outcome.output_path is not None and outcome.presentation_path is not None
    report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
    model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    published = []
    for item in outcome.publications or ():
        symbol = str(item.finding.get("symbol"))
        if interesting(symbol):
            published.append({"symbol": symbol, "value": item.finding.get("value")})
    blocked = []
    for row in report.get("dispositions") or []:
        if row.get("disposition") != "blocked":
            continue
        artifact = str(row.get("artifact_id", ""))
        missing = [str(item) for item in (row.get("missing") or [])]
        blob = artifact + " " + " ".join(missing)
        if not interesting(blob) and "f1099b" not in blob and "8949" not in blob:
            continue
        blocked.append({
            "artifact_id": artifact,
            "code": row.get("code"),
            "missing": missing[:8],
        })
    lines = []
    for section in model.get("sections") or []:
        field = section.get("field") or {}
        citizen = str(field.get("id") or "")
        if not interesting(citizen):
            continue
        resolved = section.get("resolved") or {}
        reasons = []
        for reason in (resolved.get("reasons") or [])[:4]:
            if isinstance(reason, dict) and reason.get("sentence"):
                reasons.append(scrub(str(reason["sentence"]))[:240])
        instruction = (field.get("dispositions") or {}).get(str(resolved.get("disposition"))) or {}
        lines.append({
            "id": citizen,
            "disposition": resolved.get("disposition"),
            "value": resolved.get("value"),
            "reasons": reasons,
            "explain": instruction.get("explain"),
        })
    attachments = []
    for attachment in model.get("attachments") or []:
        name = str(attachment.get("id") or "")
        if "8949" not in name and "schedule-d" not in name:
            continue
        resolved = attachment.get("resolved") or {}
        attachments.append({
            "id": name,
            "disposition": resolved.get("disposition"),
            "value": resolved.get("value"),
        })
    groups = []
    for group in model.get("citationGroups") or []:
        name = str(group.get("id") or "")
        if "8949" not in name and "schedule-d" not in name:
            continue
        parts = []
        for part in group.get("parts") or []:
            heading = str(part.get("heading") or "")
            if "box B" not in heading and "box E" not in heading and "box A" not in heading and "box D" not in heading:
                continue
            parts.append({
                "heading": heading,
                "tieOutText": scrub(str(part.get("tieOutText") or ""))[:160],
                "sites": len(part.get("citationSites") or []),
            })
        if parts:
            groups.append({"id": name, "parts": parts})
    return {
        "refusal": None,
        "stop_reason": report.get("stop_reason"),
        "published": published,
        "blocked": blocked[:40],
        "lines": lines,
        "attachments": attachments,
        "groups": groups,
    }


def run_one(acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    surface = PublicationSurface(RELEASE_DIR, CONTENT / REGISTRY, CONTENT)
    finished = _handover(
        _finish(
            copy.deepcopy(acts),
            package_path=CONTENT / PACKAGE,
            package_version=PACKAGE_VERSION,
            release_path=RELEASE_DIR / RELEASE,
            release_version=RELEASE_VERSION,
            note=run_id,
        ),
        surface=surface,
        reconfirm=True,
    )
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ccr.ROOT,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=ccr.USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        return summarize_run(outcome)


def main() -> None:
    selected = set(sys.argv[1:])
    results: dict[str, Any] = {}
    built = cases()
    for name, acts in built.items():
        if selected and name not in selected:
            continue
        try:
            results[name] = run_one(acts, f"demo.ns.p0.{name}")
        except Exception as exc:  # noqa: BLE001 — the probe records the failure instead of hiding it
            results[name] = {
                "error": type(exc).__name__,
                "message": scrub(str(exc))[:800],
                "trace": scrub(traceback.format_exc())[-1500:],
            }
        print(name, results[name].get("error") or results[name].get("refusal") or "ok", flush=True)
    out = EVIDENCE / "probe-output.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {out.name} ({out.stat().st_size} bytes)", flush=True)


if __name__ == "__main__":
    main()
