"""P0 probe — unresolved Form 1099-K (evidence only, no production edit).

Runs the charter's three statements, plus the same return with no Form 1099-K,
through ``live_coordinate_run`` on the committed core v58 and v59 packages.
Tables in ``p0-trace-and-design.md`` are written from this script's JSON.

Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/form-1099-k-income-evidence/probe.py

Synthetic ``demo.*`` ids only. This script writes ``probe-output.json`` beside
itself. No absolute path is written into that file.
"""

from __future__ import annotations

import copy
import json
import re
import sys
import traceback
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.package_validation import (  # noqa: E402
    _iter_selection_dependency_names,
)
from packages.kernel.facts import fact_id_for  # noqa: E402
from packages.tax.loader import (  # noqa: E402
    load_f1099k_bundle,
    load_f1099k_circumstances_bundle,
)
from tests.test_f1099k_personal_item_sale_track1 import (  # noqa: E402
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
from tests.test_form_1099_withholding import (  # noqa: E402
    SCOPE_KEY,
    USER,
    YEAR,
    _act,
    _attested,
    _base,
    _finished,
    _recorded_handover,
    _unemployment,
    _unemployment_return,
)
from tests.test_form_1099_withholding import (  # noqa: E402
    SURFACE_V58,
    SURFACE_V59,
)

HERE = Path(__file__).resolve().parent
OUT_PATH = HERE / "probe-output.json"
CONTENT = REPO / "packages" / "content" / "tax" / "2025"
SAMPLE = REPO / "packages" / "sample_data"

FAMILY_ID = "tax.us.2025.f1099k"
CLOSURE_TYPE = FAMILY_ID + ".source-closure"
PAYER = "demo.platform.a"
STMT = "demo.stmt.a"
BOX1A_AMOUNT = 880.0

_PATH = re.compile(r"(?:/Users|/private|/tmp|/var|/opt)[^\s'\"\\]*")

# Charter rows. The rule id is the disposition key; the symbol is the publication.
ROWS: tuple[tuple[str, str, str], ...] = (
    ("unresolved", "tax.us.2025.rule.f1099k-unresolved", "tax.us.2025.f1099k.unresolved"),
    ("top-entry", "tax.us.2025.rule.schedule1-top-entry", "tax.us.2025.schedule1.top-entry"),
    ("attachment", "tax.us.2025.rule.attachment.schedule-1", "tax.us.2025.schedule1.disposition"),
    ("sch1-line10", "tax.us.2025.rule.schedule1-line10", "tax.us.2025.schedule1.line10-additional-income"),
    ("line8", "tax.us.2025.rule.form1040-line8", "tax.us.2025.income.additional-income"),
    ("line9", "tax.us.2025.rule.form1040-line9", "tax.us.2025.income.total-income"),
    ("line11", "tax.us.2025.rule.form1040-line11", "tax.us.2025.income.agi"),
    ("line15", "tax.us.2025.rule.form1040-line15", "tax.us.2025.income.taxable-income"),
    ("line16", "tax.us.2025.rule.form1040-line16", "tax.us.2025.tax.total-tax"),
    ("line24", "tax.us.2025.rule.form1040-line24", "tax.us.2025.tax.line24-total-tax"),
    ("line25b", "tax.us.2025.rule.form1040-line25b", "tax.us.2025.payments.line25b"),
    ("line33", "tax.us.2025.rule.form1040-line33", "tax.us.2025.payments.line33"),
    ("line34", "tax.us.2025.rule.form1040-line34", "tax.us.2025.payments.line34-overpaid"),
    ("line35a", "tax.us.2025.rule.form1040-line35a", "tax.us.2025.payments.line35a-refunded"),
    ("line37", "tax.us.2025.rule.form1040-line37", "tax.us.2025.payments.line37-amount-owed"),
)
EXTRA_SYMBOLS = (
    "tax.us.2025.schedule1.line7-unemployment",
    "tax.us.2025.f1099k.box1a-subtotal",
    "tax.us.2025.f1099k.statement-loss-reason",
)


def redact(text: str) -> str:
    return _PATH.sub("[path]", text)


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _compact_published(symbol: str, value: Any) -> Any:
    if symbol == "tax.us.2025.schedule1.disposition" and isinstance(value, dict):
        return {"object_keys": sorted(str(k) for k in value)}
    return _jsonable(value)


def _supported_answers() -> dict[str, Any]:
    """The track-1 supported-loss answers (path 5). Box 1a is 880 so they reconcile."""
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
        if isinstance(family, dict) and family.get("id") == FAMILY_ID:
            return payload
    return None


def _splice(acts: list[dict[str, object]], *, box4: float, omit: str | None) -> dict[str, Any]:
    """Record one Form 1099-K on ``acts``.

    Box 1a is the family member, so it is a member-transition. Box 4 and the
    circumstance answers are plain assertions. The closure, if the log already
    has one, is retargeted onto the successor horizon and kept after the
    transition. The base unemployment return does not adopt this family; this
    splice adds the v3 vocabulary the v58 and v59 packages pin.
    """
    built = copy.deepcopy(acts)
    note: dict[str, Any] = {"family_present_before": _genesis(built) is not None}
    counter = [10000]

    def late(kind: str, payload: dict[str, object]) -> dict[str, object]:
        act = _act(counter[0], kind, payload)
        counter[0] += 1
        return act

    inserted: list[dict[str, object]] = []
    vocabulary = load_f1099k_bundle(version="v3")
    circumstances = load_f1099k_circumstances_bundle()
    have = _bundle_ids(built)
    for bundle in (vocabulary, circumstances):
        key = (str(bundle["id"]), str(bundle["version"]))
        if key not in have:
            inserted.append(late("bundle-adoption", {"bundle": bundle}))

    genesis = _genesis(built)
    if genesis is None:
        head = "demo.p0.f1099k.h0"
        inserted.append(late("horizon-genesis", {
            "family": {"id": FAMILY_ID, "version": "v2"},
            "scope": dict(SCOPE_KEY),
            "horizon_id": head,
        }))
        scope = dict(SCOPE_KEY)
        family_version = "v2"
    else:
        head = str(genesis["horizon_id"])
        scope = dict(genesis.get("scope") or SCOPE_KEY)
        family = cast(dict[str, Any], genesis["family"])
        family_version = str(family.get("version"))

    successor = "demo.p0.f1099k.h1"
    keys = (("payer", PAYER), ("statement", STMT))
    inserted.append(late("entity-introduced", {
        "entity": {"schema": "entity.v1", "id": PAYER, "kind": "tax.us.1099k-platform", "label": "Synthetic"},
    }))
    inserted.append(late("entity-introduced", {
        "entity": {"schema": "entity.v1", "id": STMT, "kind": "tax.us.1099k-statement", "label": "Synthetic"},
    }))
    box1a_fact = fact_id_for(BOX1A, keys + (("tax-year", YEAR),))
    inserted.append(late("member-transition", {
        "family": {"id": FAMILY_ID, "version": family_version},
        "scope": scope,
        "member": {"action": "assert", "finding": _attested("demo.p0.f1099k.box1a", box1a_fact, BOX1A_AMOUNT)},
        "successor": {"id": successor, "predecessor": head},
    }))
    box4_fact = fact_id_for(BOX4, keys + (("tax-year", YEAR),))
    inserted.append(late("assertion", {
        "finding": _attested("demo.p0.f1099k.box4", box4_fact, box4),
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
            "finding": _attested(f"demo.p0.f1099k.{short}", fact_id, answers[fact_type]),
        }))

    closure_at: int | None = None
    for index, act in enumerate(built):
        finding = cast(dict[str, Any], act.get("payload") or {}).get("finding")
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(CLOSURE_TYPE + "|"):
            closure_at = index
            finding["fact_id"] = (
                f"{CLOSURE_TYPE}|family-horizon={successor},tax-year={YEAR}"
            )
            break
    if closure_at is None:
        inserted.append(late("assertion", {
            "finding": _attested(
                "demo.p0.f1099k.closure",
                f"{CLOSURE_TYPE}|family-horizon={successor},tax-year={YEAR}",
                True,
            ),
        }))
        built.extend(inserted)
    else:
        built[closure_at:closure_at] = inserted

    note.update({
        "predecessor_horizon": head,
        "successor_horizon": successor,
        "family_version": family_version,
        "scope_keys": sorted(scope),
        "box4": box4,
        "omitted_answer": omit,
        "box1a_fact_id": box1a_fact,
        "asserted_circumstance_count": sum(1 for fact in CIRCUMSTANCE_FACTS if fact in answers),
    })
    return {"acts": built, "splice": note}


def _literal_return() -> list[dict[str, object]]:
    """The reviewer's unemployment return: wages 50000, W-2 box 2 4500, box 4 600."""
    return _unemployment_return(withheld=600.0)


def _v58_admissible_return() -> list[dict[str, object]]:
    """Same wages and unemployment, recorded with the v58 box-4 companion.

    The literal return adopts the v59 box-4 and box-6 families and omits the
    companion core v58 requires. This twin does not.
    """
    acts = _base(wages=50000.0, w2_withheld=4500.0)
    _unemployment(acts, [6000.0], authority=0.0)
    return acts


def _cell(row: dict[str, Any] | None, published: Any) -> str:
    if row is None and published is None:
        return "no disposition"
    if row is None:
        return "published " + json.dumps(published, sort_keys=True)
    kind = str(row.get("disposition"))
    if kind == "published":
        return "published " + json.dumps(published, sort_keys=True)
    if kind == "blocked":
        missing = row.get("missing")
        return f"blocked {row.get('code')} missing={json.dumps(missing, sort_keys=True)}"
    if kind == "inapplicable":
        guard = row.get("guard_result")
        if guard is False:
            return "inapplicable (guard false)"
        return "inapplicable"
    return kind


def _run_one(acts: list[dict[str, object]], run_id: str, core: str) -> dict[str, Any]:
    try:
        finished = _finished(acts, run_id, core=core)
        if core == "v59":
            finished = _recorded_handover(finished, reconfirm=True)
        surface = SURFACE_V59 if core == "v59" else SURFACE_V58
        with TemporaryDirectory() as tmp:
            outcome = live_coordinate_run(
                WorkspaceCapability(Path(tmp) / "L"),
                repo_root=REPO,
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
                return {
                    "status": "refused",
                    "reason": redact(str(outcome.refusal.reason)),
                    "detail": redact(str(outcome.refusal.detail)),
                }
            report: dict[str, Any] = {}
            if outcome.output_path is not None:
                report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            publications = {
                str(item.finding.get("symbol")): item.finding
                for item in (outcome.publications or ())
            }
        return _project(report, publications)
    except Exception as exc:  # a refusal or a projector rejection is evidence
        return {
            "status": "error",
            "error_type": type(exc).__name__,
            "error": redact(f"{type(exc).__name__}: {exc}"),
            "traceback_tail": [redact(line) for line in traceback.format_exc().splitlines()[-8:]],
        }


def _project(report: dict[str, Any], publications: dict[str, Any]) -> dict[str, Any]:
    dispositions = report.get("dispositions")
    rows = dispositions if isinstance(dispositions, list) else []
    by_artifact: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if isinstance(row, dict):
            by_artifact.setdefault(str(row.get("artifact_id")), []).append(row)

    def published_for(symbol: str) -> Any:
        finding = publications.get(symbol)
        if not isinstance(finding, dict) or "value" not in finding:
            return None
        return _compact_published(symbol, finding.get("value"))

    table: list[dict[str, Any]] = []
    for label, artifact, symbol in ROWS:
        matched = by_artifact.get(artifact, [])
        row = matched[-1] if matched else None
        published = published_for(symbol)
        table.append({
            "label": label,
            "artifact_id": artifact,
            "symbol": symbol,
            "disposition_count": len(matched),
            "cell": _cell(row, published),
            "code": None if row is None else row.get("code"),
            "missing": None if row is None else row.get("missing"),
            "disposition": None if row is None else row.get("disposition"),
            "guard_result": None if row is None else row.get("guard_result"),
            "symbol_on_row": None if row is None else row.get("symbol"),
            "published": published,
        })

    extras: list[dict[str, Any]] = []
    for symbol, finding in sorted(publications.items()):
        if not any(symbol == name or symbol.startswith(name + "|") for name in EXTRA_SYMBOLS):
            continue
        if not isinstance(finding, dict):
            continue
        extras.append({
            "symbol": symbol,
            "value": _compact_published(symbol, finding.get("value")),
        })

    loss_rows: list[dict[str, Any]] = []
    for row in by_artifact.get("tax.us.2025.rule.f1099k-statement-loss-reason", []):
        loss_rows.append({
            "disposition": row.get("disposition"),
            "code": row.get("code"),
            "missing": row.get("missing"),
            "guard_result": row.get("guard_result"),
            "symbol": row.get("symbol"),
        })

    roots: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict) or row.get("disposition") != "blocked":
            continue
        if row.get("code") == "DEPENDENCY_ABSENT":
            continue
        roots.append({
            "artifact_id": row.get("artifact_id"),
            "code": row.get("code"),
            "missing": row.get("missing"),
        })

    return {
        "status": "ran",
        "stop_reason": report.get("stop_reason"),
        "table": table,
        "extras": extras,
        "loss_reason_rows": loss_rows,
        "root_blocks": roots,
    }


def _cases(payload: dict[str, Any]) -> list[dict[str, Any]]:
    shapes = (
        ("literal", _literal_return),
        ("v58-admissible", _v58_admissible_return),
    )
    cores = ("v59", "v58")
    statements: tuple[tuple[str, float | None, str | None], ...] = (
        ("none", None, None),
        ("a-supported-box4-0", 0.0, None),
        ("b-supported-box4-150", 150.0, None),
        ("c-unanswered-q5", 0.0, Q5),
    )
    out: list[dict[str, Any]] = []
    for shape_name, builder in shapes:
        for core in cores:
            if shape_name == "v58-admissible" and core == "v59":
                # The admissible twin is the v58 recording. v59 of the literal
                # return is the charter's return.
                continue
            for case_name, box4, omit in statements:
                if shape_name == "v58-admissible" and core == "v58" and case_name == "none":
                    pass
                run_id = f"demo.p0.f1099k.{shape_name}.{core}.{case_name}"
                base = builder()
                splice_note = None
                acts = base
                if box4 is not None:
                    spliced = _splice(base, box4=box4, omit=omit)
                    acts = spliced["acts"]
                    splice_note = spliced["splice"]
                print(f"run {run_id}", flush=True)
                result = _run_one(acts, run_id, core)
                print(f"  {result.get('status')}", flush=True)
                out.append({
                    "run_id": run_id,
                    "shape": shape_name,
                    "core": core,
                    "case": case_name,
                    "splice": splice_note,
                    "result": result,
                })
                payload["cases"] = out
                _dump(payload)
    return out


def _package_pins() -> dict[str, list[dict[str, str]]]:
    wanted = {artifact for _, artifact, _ in ROWS}
    wanted.update({
        "tax.us.2025.rule.f1099k-statement-loss-reason",
        "tax.us.2025.rule.f1099k-box1a-subtotal",
        "tax.us.2025.rule.schedule1-line7",
        "tax.us.2025.rule.form1040-line8",
        "tax.us.2025.f1099k",
        "tax.us.2025.f1099k.vocabulary",
    })
    pins: dict[str, list[dict[str, str]]] = {}
    for version in ("v58", "v59"):
        package = json.loads((CONTENT / f"package.core-calculations.{version}.json").read_text(encoding="utf-8"))
        found = []
        for member in package.get("members", []):
            if isinstance(member, dict) and member.get("id") in wanted:
                found.append({
                    "id": str(member.get("id")),
                    "version": str(member.get("version")),
                    "schema": str(member.get("schema")),
                    "role": str(member.get("role")),
                })
        pins[version] = found
    return pins


def _walk_refs(node: Any, sink: list[str]) -> None:
    if isinstance(node, dict):
        if node.get("op") == "ref" and isinstance(node.get("name"), str):
            sink.append(node["name"])
        for value in node.values():
            _walk_refs(value, sink)
    elif isinstance(node, list):
        for item in node:
            _walk_refs(item, sink)


def _load_member(pin: dict[str, Any]) -> dict[str, Any] | None:
    target_id = pin.get("id")
    target_version = pin.get("version")
    for path in CONTENT.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(body, dict) and body.get("id") == target_id and body.get("version") == target_version:
            return body
    return None


def _trace() -> dict[str, Any]:
    package = json.loads((CONTENT / "package.core-calculations.v59.json").read_text(encoding="utf-8"))
    by_id: dict[str, dict[str, Any]] = {}
    for pin in package.get("members", []):
        if not isinstance(pin, dict):
            continue
        body = _load_member(pin)
        if body is not None:
            by_id[str(pin["id"])] = body

    unresolved = "tax.us.2025.f1099k.unresolved"
    readers: list[dict[str, Any]] = []
    for rule_id, body in sorted(by_id.items()):
        if not str(body.get("schema", "")).startswith("rule-artifact.") and not str(body.get("schema", "")).startswith("attachment-rule."):
            continue
        requires = body.get("requires") if isinstance(body.get("requires"), list) else []
        refs: list[str] = []
        _walk_refs(body.get("when"), refs)
        _walk_refs(body.get("value"), refs)
        selection = body.get("selection")
        if isinstance(selection, dict):
            _walk_refs(selection, refs)
        subtotals = []
        requirement = body.get("requirement")
        if isinstance(requirement, dict):
            subtotals = list(requirement.get("subtotals") or [])
        hit_requires = unresolved in requires
        hit_refs = unresolved in refs
        hit_sub = unresolved in subtotals
        if hit_requires or hit_refs or hit_sub:
            readers.append({
                "id": rule_id,
                "version": body.get("version"),
                "in_requires": hit_requires,
                "in_ref": hit_refs,
                "in_subtotals": hit_sub,
                "publishes": body.get("publishes"),
            })

    line8 = by_id["tax.us.2025.rule.form1040-line8"]
    line10 = by_id["tax.us.2025.rule.schedule1-line10"]
    chain = []
    seen: set[str] = set()

    def follow(symbol: str) -> None:
        if symbol in seen:
            return
        seen.add(symbol)
        publishers = [
            {"id": rule_id, "version": body.get("version"), "schema": body.get("schema"),
             "requires": body.get("requires"), "publishes": body.get("publishes")}
            for rule_id, body in by_id.items()
            if body.get("publishes") == symbol
        ]
        chain.append({"symbol": symbol, "publishers": publishers})
        for pub in publishers:
            for req in pub.get("requires") or []:
                if isinstance(req, str):
                    follow(req)

    follow("tax.us.2025.income.additional-income")

    top = by_id["tax.us.2025.rule.schedule1-top-entry"]
    attachment = by_id["tax.us.2025.rule.attachment.schedule-1"]
    return {
        "line8": {
            "id": line8.get("id"),
            "version": line8.get("version"),
            "schema": line8.get("schema"),
            "requires": line8.get("requires"),
            "value_refs": _refs_of(line8.get("value")),
        },
        "line10": {
            "id": line10.get("id"),
            "version": line10.get("version"),
            "schema": line10.get("schema"),
            "requires": line10.get("requires"),
            "value_refs": _refs_of(line10.get("value")),
            "mentions_unresolved": unresolved in json.dumps(line10),
            "mentions_top_entry": "tax.us.2025.schedule1.top-entry" in json.dumps(line10),
        },
        "top_entry_requires_statements": (
            top.get("selection", {}).get("paths", [{}])[0].get("requires")
        ),
        "top_entry_mentions_unresolved": unresolved in json.dumps(top),
        "attachment_subtotals": (
            attachment.get("requirement", {}).get("subtotals")
            if isinstance(attachment.get("requirement"), dict) else None
        ),
        "attachment_mentions_unresolved": unresolved in json.dumps(attachment),
        "unresolved_rule": {
            "id": by_id["tax.us.2025.rule.f1099k-unresolved"].get("id"),
            "version": by_id["tax.us.2025.rule.f1099k-unresolved"].get("version"),
            "default_when": by_id["tax.us.2025.rule.f1099k-unresolved"].get("selection", {}).get("default", {}).get("when"),
            "default_value": by_id["tax.us.2025.rule.f1099k-unresolved"].get("selection", {}).get("default", {}).get("value"),
            "statement_value_op": (
                by_id["tax.us.2025.rule.f1099k-unresolved"].get("selection", {}).get("paths", [{}])[0].get("value", {}).get("op")
            ),
        },
        "readers_of_unresolved": readers,
        "line8_requires_chain": chain,
    }


def _refs_of(expr: Any) -> list[str]:
    found: list[str] = []
    _walk_refs(expr, found)
    return found


def _dependency_names() -> dict[str, Any]:
    """What the current selector counts as requires for the candidate value."""
    value = {
        "op": "choose",
        "when": {
            "op": "collect_categorical_all_equal",
            "name": "tax.us.2025.f1099k.statement-loss-reason",
            "value": {
                "op": "category_literal",
                "fact_type": {
                    "id": "tax.us.2025.f1099k.statement-loss-reason",
                    "version": "v2",
                },
                "value": "supported-loss",
            },
        },
        "then": {"op": "ref", "name": "tax.us.2025.schedule1.line7-unemployment"},
        "else": {
            "op": "conditional_dependency_set",
            "condition": True,
            "members": [{"op": "ref", "name": "tax.us.2025.f1099k.unresolved"}],
        },
    }
    names = list(_iter_selection_dependency_names(value, {}))
    return {
        "yielded": names,
        "yields_unresolved": "tax.us.2025.f1099k.unresolved" in names,
        "yields_loss_reason": "tax.us.2025.f1099k.statement-loss-reason" in names,
        "yields_line7": "tax.us.2025.schedule1.line7-unemployment" in names,
    }


def _form_fields() -> list[dict[str, Any]]:
    names = (
        "schedule1.line-10.form-field.json",
        "form1040.line-8.form-field.json",
        "f1099k.unresolved.form-field.json",
    )
    out = []
    for name in names:
        body = json.loads((CONTENT / name).read_text(encoding="utf-8"))
        blocked = body.get("blocked") if isinstance(body.get("blocked"), dict) else {}
        out.append({
            "file": name,
            "id": body.get("id"),
            "version": body.get("version"),
            "schema": body.get("schema"),
            "binds": body.get("binds"),
            "blocked_explain": blocked.get("explain") if isinstance(blocked, dict) else None,
        })
    return out


def _goldens() -> list[dict[str, Any]]:
    rows = []
    if not SAMPLE.is_dir():
        return rows
    for path in sorted(SAMPLE.rglob("*.json")):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "f1099k" not in text and "1099-K" not in text and "1099k" not in text:
            continue
        rel = str(path.relative_to(REPO))
        rows.append({
            "path": rel,
            "box1a": "tax.us.2025.f1099k.box1a-gross-amount" in text,
            "unresolved_symbol": "tax.us.2025.f1099k.unresolved" in text,
            "closure": "tax.us.2025.f1099k.source-closure" in text or "demo.probe.f1099k" in text,
            "form_field": "f1099k.unresolved.form-field" in text or "form.f1099k.unresolved" in text,
        })
    return rows


def _dump(payload: dict[str, Any]) -> None:
    OUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    payload: dict[str, Any] = {
        "dependency_names": _dependency_names(),
        "package_pins": _package_pins(),
        "trace": _trace(),
        "form_fields": _form_fields(),
        "goldens": _goldens(),
        "cases": [],
    }
    _dump(payload)
    payload["cases"] = _cases(payload)
    _dump(payload)
    print(f"wrote {OUT_PATH.name} cases={len(payload['cases'])}", flush=True)


if __name__ == "__main__":
    main()
