"""P0 probe: can the child tax credit's per-child tests share one roster?

Investigation only. Builds a throwaway publication surface in a temporary
directory (synthetic fact types, a package, a registry, a release) and runs
synthetic children, named ``demo-child-N``, through the real coordinator,
``packages.derivation.live.live_coordinate_run``. Nothing is written under the
repository, and no published content, fixture or test is touched. Run from the
repository root:

    python3 docs/phases/engine-breadth/milestones/child-tax-credit-evidence/ctc_child_probe.py

Five modes bind the vocabulary differently (``MODES``): ``private`` (a synthetic
family); ``same-family`` (the credit's closure mapping on the earned income
family itself, refused by the engine as a second authorized subtotal);
``separate-family`` and ``separate-own-member`` (a credit family over the earned
income child kind, with the committed earned income family and closure mapping
loaded beside it); ``separate-alone`` (the credit family without the earned
income files). The separate modes need the credit's own closure fact type: a
shared closure fact type makes the credit count unclosed.

The shape: the child roster carries the shared answers (relationship, joint
return, SSN, another may claim) and the credit-only answers (under 17,
lived with you, support, citizenship, claimed as your dependent). Per child, a
rule counts the child for the credit when claimed as a dependent and every test
is met; a claimed child that fails any test blocks (it would be a credit for
other dependents, outside the slice); an unclaimed child is not counted and
never blocks. A return-level rule counts the per-child results over the closed
roster, as ``child_dispatch_probe.py`` does for the earned income credit.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.derivation.package_validation import (  # noqa: E402
    citizen_checksum,
    package_instance_checksum,
)
from packages.derivation.production_resolver import PublicationSurface  # noqa: E402
from packages.kernel.facts import fact_id_for  # noqa: E402

USER = "demo.user.filer-1"
YEAR = "2025"
SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}
CHILD_KIND = P = REL = JOINT = SSN = OTHER = U17 = RES = SUP = CIT = CLAIM = ""
TESTS: tuple[str, ...] = ()
ANSWER_TYPES: tuple[str, ...] = ()
CLOSURE = INERT = FAMILY = CLOSURE_MAPPING = BUNDLE = RULE_PREFIX = ""
SHARED = False
MEMBER = ""


def configure(mode: str) -> None:
    """Bind the vocabulary.

    ``private``: a synthetic child kind and family. ``same-family``: the credit's
    mapping over the earned income roster family itself. ``separate-family``: a
    credit family over the earned income child kind, with the committed earned
    income family and closure mapping loaded beside it."""
    global CHILD_KIND, P, REL, JOINT, SSN, OTHER, U17, RES, SUP, CIT, CLAIM
    global TESTS, ANSWER_TYPES, CLOSURE, INERT, FAMILY, CLOSURE_MAPPING, BUNDLE, RULE_PREFIX, SHARED, MEMBER
    SHARED = mode
    if mode != "private":
        CHILD_KIND = "tax.us.eic-child"
        P = "tax.us.2025.ctc."
        REL = "tax.us.2025.eic.child.relationship"
        JOINT = "tax.us.2025.eic.child.joint-return"
        SSN = "tax.us.2025.eic.child.ssn"
        OTHER = "tax.us.2025.eic.child.another-may-claim"
        CLOSURE_MAPPING = "tax.us.2025.closure-mapping.ctc-child-roster"
        BUNDLE = "tax.us.2025.ctc.child.vocabulary"
        INERT = P + "child.inert-path-unwritten"
        if mode == "separate-own-member":
            FAMILY = "tax.us.2025.ctc.child-roster"
            CLOSURE = "tax.us.2025.ctc.child-roster.source-closure"
        elif mode == "same-family":
            FAMILY = "tax.us.2025.eic.child-roster"
            CLOSURE = "tax.us.2025.eic.child-roster.source-closure"
        else:
            FAMILY = "tax.us.2025.ctc.child-roster"
            CLOSURE = "tax.us.2025.ctc.child-roster.source-closure"
    else:
        CHILD_KIND = "probe.ctc-child"
        P = "probe.ctc."
        REL = P + "child.relationship"
        JOINT = P + "child.joint-return"
        SSN = P + "child.ssn"
        OTHER = P + "child.another-may-claim"
        CLOSURE = P + "child-roster.source-closure"
        FAMILY = P + "child-roster"
        CLOSURE_MAPPING = P + "closure-mapping.child-roster"
        BUNDLE = P + "child.vocabulary"
        INERT = P + "child.inert-path-unwritten"
    MEMBER = P + "child.claimed-as-dependent" if mode == "separate-own-member" else REL
    U17 = P + "child.under-17"
    RES = P + "child.lived-with-you"
    SUP = P + "child.no-over-half-support"
    CIT = P + "child.citizen-or-resident"
    CLAIM = P + "child.claimed-as-dependent"
    TESTS = (JOINT, SSN, OTHER, U17, RES, SUP, CIT)
    ANSWER_TYPES = (REL, *TESTS, CLAIM)
    RULE_PREFIX = P + "rule."


configure("private")


def _pin(item_id: str, version: str = "v1") -> dict[str, str]:
    return {"id": item_id, "version": version}


def _fact_type(fact_id: str) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": f"Synthetic per-child answer {fact_id}",
        "nature": "determinable",
        "identity_keys": [
            {"name": "child", "kind": "entity", "entity_kind": CHILD_KIND},
            {"name": "tax-year", "kind": "literal", "values": [YEAR]},
        ],
        "value_schema": {"type": "string", "enum": ["yes", "no"]},
        "supersession": {"policy": "free"},
    }


def _bundle() -> dict[str, Any]:
    closure = {
        "schema": "fact-type.v2",
        "id": CLOSURE,
        "version": "v1",
        "title": "Closure of the synthetic child roster",
        "nature": "determinable",
        "identity_keys": [
            {"name": "family-horizon", "kind": "entity", "entity_kind": "kernel.family-horizon"},
            {"name": "tax-year", "kind": "literal", "values": [YEAR]},
        ],
        "value_schema": {"type": "boolean"},
        "supersession": {"policy": "free"},
    }
    inert = {
        "schema": "fact-type.v2",
        "id": INERT,
        "version": "v1",
        "title": "Internal marker used only to complete an inert rule path",
        "nature": "determinable",
        "identity_keys": [{"name": "marker", "kind": "literal", "values": ["unused"]}],
        "value_schema": {"type": "string", "enum": ["unused"]},
        "supersession": {"policy": "free"},
    }
    return {
        "schema": "bundle.v2",
        "id": BUNDLE,
        "version": "v1",
        "label": "Synthetic child tax credit vocabulary",
        "fact_types": [*(_fact_type(t) for t in ANSWER_TYPES), closure, inert, *_loaded_closures()],
    }


def _loaded_closures() -> list[dict[str, Any]]:
    """With the earned income family loaded, its closure fact type must be too."""
    if SHARED not in ("separate-family", "separate-own-member"):
        return []
    eic = json.loads((REPO / "packages/content/tax/2025/eic-child-roster.bundle.json").read_text("utf-8"))
    return [ft for ft in eic["fact_types"] if ft["id"] == "tax.us.2025.eic.child-roster.source-closure"]


def _family() -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": FAMILY,
        "version": "v1",
        "scope": dict(SCOPE),
        "title": "Synthetic child roster",
        "member_predicate": {"fact_type": MEMBER},
        "authorizes_subtotal": P + "child-count",
        "closure_claim": "Every child who could be a dependent is recorded as a roster item.",
    }


def _closure_mapping() -> dict[str, Any]:
    return {
        "schema": "source-closure-mapping.v2",
        "id": CLOSURE_MAPPING,
        "version": "v1",
        "admission": {"condition": "current-literal-true"},
        "admits_symbol": P + "child-count",
        "closure_fact_type": _pin(CLOSURE),
        "closure_horizon_key": "family-horizon",
        "family": _pin(FAMILY),
        "member_fact_type": _pin(MEMBER),
    }


def _rule(rule_id: str, schema: str = "rule-artifact.v14", **fields: Any) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema": schema,
        "id": rule_id,
        "version": "v1",
        "scope": dict(SCOPE),
        "role": "computation",
        "requires": [],
        "pins": [],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
    }
    body.update(fields)
    return body


def _yes(fact_id: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare",
        "cmp": "eq",
        "left": {"op": "ref", "name": fact_id},
        "right": {"op": "category_literal", "fact_type": _pin(fact_id), "value": "yes"},
    }


def _met(fact_id: str) -> dict[str, Any]:
    return {"op": "choose", "when": _yes(fact_id), "then": 1, "else": 0}


def _is(name: str, value: int) -> dict[str, Any]:
    return {"op": "compare", "cmp": "eq", "left": {"op": "ref", "name": name}, "right": value}


def _short(symbol: str) -> str:
    return symbol.replace(P, "").replace(",tax-year=2025", "").replace("child=", "")


def _rules() -> list[dict[str, Any]]:
    rules: list[dict[str, Any]] = []
    met_symbols: dict[str, str] = {}
    for answer, short in ((JOINT, "joint-return"), (SSN, "ssn"), (U17, "under-17"),
                          (RES, "lived-with-you"), (SUP, "no-support"), (CIT, "citizen"),
                          (CLAIM, "claimed")):
        met_symbols[answer] = P + "child." + short + "-met"
        rules.append(_rule(
            RULE_PREFIX + short + "-met",
            subject=_pin(answer),
            when=True,
            value=_met(answer),
            publishes=met_symbols[answer],
        ))
    other_clear = P + "child.other-claimant-clear"
    rules.append(_rule(
        RULE_PREFIX + "other-claimant-clear",
        subject=_pin(OTHER),
        when=True,
        value={"op": "choose", "when": _yes(OTHER),
               "then": {"op": "block", "code": "DEPENDENCY_INVALID"}, "else": 1},
        publishes=other_clear,
    ))
    tests = [met_symbols[t] for t in (JOINT, SSN, U17, RES, SUP, CIT)] + [other_clear]
    claimed = met_symbols[CLAIM]
    all_met = {"op": "compare", "cmp": "eq", "right": len(tests),
               "left": {"op": "add", "args": [{"op": "ref", "name": n} for n in tests]}}
    # Unclaimed: 0 and never blocks. Claimed: 1 when every test is met, else a block
    # (a claimed child who fails a test is a credit-for-other-dependents case).
    rules.append(_rule(
        RULE_PREFIX + "ctc-child-counts",
        subject=_pin(REL),
        requires=[claimed, *tests],
        when=True,
        value={
            "op": "choose",
            "when": _is(claimed, 0),
            "then": 0,
            "else": {"op": "choose", "when": all_met, "then": 1,
                     "else": {"op": "block", "code": "DEPENDENCY_INVALID"}},
        },
        publishes=P + "child.ctc-counts",
    ))
    rules.append(_rule(
        RULE_PREFIX + "ctc-child-inert-count",
        subject=_pin(REL),
        requires=[],
        when=True,
        value={"op": "count", "name": MEMBER, "source_set": FAMILY},
        publishes=P + "child.rows-counted",
    ))
    rules.append(_count_rule())
    return rules


def _count_rule() -> dict[str, Any]:
    read = P + "child.ctc-counts"
    return _rule(
        RULE_PREFIX + "ctc-child-count",
        schema="rule-artifact.v14",
        when=True,
        selection={
            "mode": "exclusive_presence",
            "conflict": "refuse",
            "paths": [
                {
                    "id": "children",
                    "activity": {"kind": "source_nonempty", "member_fact_types": [_pin(MEMBER)]},
                    "reads_subject_results": [{"symbol": read, "subject": _pin(REL)}],
                    "requires": [],
                    "pins": [],
                    "when": {"op": "require_closed", "source_set": FAMILY},
                    "value": {"op": "add", "args": [
                        {"op": "collect", "name": read, "source_set": FAMILY}]},
                },
                {
                    "id": "inert",
                    "activity": {"kind": "source_nonempty", "member_fact_types": [_pin(INERT)]},
                    "reads_subject_results": [],
                    "requires": [],
                    "pins": [],
                    "when": True,
                    "value": {"op": "block", "code": "DEPENDENCY_ABSENT"},
                },
            ],
            "default": {
                "id": "neither",
                "reads_subject_results": [],
                "requires": [],
                "pins": [],
                "when": True,
                "value": {"op": "count", "name": MEMBER, "source_set": FAMILY},
            },
            "refusal": {
                "code": "DEPENDENCY_INVALID",
                "missing": ["probe-ctc-child-roster-inert-path-conflict"],
                "pins": [],
            },
        },
        publishes=P + "child-count",
    )


def _citizens() -> list[tuple[dict[str, Any], str]]:
    members: list[tuple[dict[str, Any], str]] = [
        (_bundle(), "fact-type-bundle"),
        (_family(), "source-family"),
        (_closure_mapping(), "source-closure-mapping"),
    ]
    members.extend((rule, "computation") for rule in _rules())
    if SHARED in ("separate-family", "separate-own-member"):
        # The committed earned income family and closure mapping, loaded beside the
        # credit's own family over the same child kind and relationship answer.
        eic_dir = REPO / "packages/content/tax/2025"
        members.append((json.loads((eic_dir / "family.eic-child-roster.json").read_text("utf-8")), "source-family"))
        members.append((json.loads((eic_dir / "closure-mapping.eic-child-roster.json").read_text("utf-8")), "source-closure-mapping"))
    if SHARED == "same-family":
        eic_dir = REPO / "packages/content/tax/2025"
        members.append((json.loads((eic_dir / "closure-mapping.eic-child-roster.json").read_text("utf-8")), "source-closure-mapping"))
    return members


def build_surface(root: Path) -> tuple[PublicationSurface, dict[str, Any], dict[str, Any]]:
    base = json.loads(
        (REPO / "packages/content/tax/2025/package.core-calculations.v54.json").read_text("utf-8"))
    member_dir = root / "members"
    member_dir.mkdir()
    registry_citizens = []
    members = []
    for body, role in _citizens():
        (member_dir / f"{body['id']}.{body['version']}.json").write_text(
            json.dumps(body, sort_keys=True), encoding="utf-8")
        registry_citizens.append({
            "id": body["id"], "version": body["version"], "checksum": citizen_checksum(body)})
        members.append({
            "id": body["id"], "version": body["version"], "schema": body["schema"], "role": role})
    package: dict[str, Any] = {
        "schema": base["schema"],
        "id": "probe.package.ctc-children",
        "version": "v1",
        "scope": dict(base["scope"]),
        "admitted_schemas": list(base["admitted_schemas"]),
        "composition_obligations": [],
        "conflict_semantics": [],
        "entrypoints": [
            {"id": m["id"], "version": m["version"]}
            for m in members
            if m["role"] in ("source-family", "source-closure-mapping", "fact-type-bundle")
            or m["id"].endswith("ctc-child-count") or m["id"].endswith("rows-counted")
            or m["id"].endswith("ctc-child-inert-count")
        ],
        "input_bindings": [],
        "members": members,
    }
    package["package_checksum"] = package_instance_checksum(package)
    (member_dir / "package.json").write_text(json.dumps(package, sort_keys=True), encoding="utf-8")
    registry_path = root / "registry.json"
    registry_path.write_text(json.dumps({
        "citizens": registry_citizens,
        "packages": [{"id": package["id"], "version": package["version"],
                      "checksum": package["package_checksum"]}],
    }, sort_keys=True), encoding="utf-8")
    release = {
        "id": "probe.release.ctc-children",
        "version": "v1",
        "schema": "release-registry.v1",
        "package_registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest(),
    }
    release_dir = root / "releases"
    release_dir.mkdir()
    release_path = release_dir / "probe.release.ctc-children.v1.json"
    release_path.write_text(json.dumps(release, sort_keys=True), encoding="utf-8")
    release["checksum"] = hashlib.sha256(release_path.read_bytes()).hexdigest()
    return PublicationSurface(release_dir, registry_path, member_dir), package, release


def _act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "act.v1",
        "act_id": f"demo.probe.act.{index:03d}",
        "kind": kind,
        "actor": USER,
        "at": f"2026-10-24T00:{index // 60:02d}:{index % 60:02d}Z",
        "committed_against": index,
        "payload": payload,
    }


def _finding(finding_id: str, fact_id: str, value: Any) -> dict[str, Any]:
    return {
        "schema": "finding.v2", "id": finding_id, "fact_id": fact_id,
        "value": value, "basis": "attested", "evidence_ids": [],
    }


def child_fact_id(fact_type: str, child: str) -> str:
    return fact_id_for(fact_type, (("child", child), ("tax-year", YEAR)))


def build_acts(children: dict[str, dict[str, str]], package: dict[str, Any],
               release: dict[str, Any], *, closed: bool = True) -> list[dict[str, Any]]:
    acts: list[dict[str, Any]] = []

    def add(kind: str, payload: dict[str, Any]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _bundle()})
    for child in children:
        add("entity-introduced", {"entity": {
            "schema": "entity.v1", "id": child, "kind": CHILD_KIND, "label": "Synthetic child"}})
    scope_key = {"tax-year": YEAR, "subject": "demo.primary"}
    add("horizon-genesis", {
        "family": _pin(FAMILY), "scope": scope_key, "horizon_id": "demo.probe.h0"})
    horizon = "demo.probe.h0"
    for index, (child, answers) in enumerate(children.items()):
        successor = f"demo.probe.h{index + 1}"
        add("member-transition", {
            "family": _pin(FAMILY),
            "scope": scope_key,
            "member": {
                "action": "assert",
                "finding": _finding(
                    f"demo.probe.rel.{child}", child_fact_id(MEMBER, child), answers[MEMBER]),
            },
            "successor": {"id": successor, "predecessor": horizon},
        })
        horizon = successor
        for fact_type, value in answers.items():
            if fact_type == MEMBER:
                continue
            add("assertion", {"finding": _finding(
                f"demo.probe.{fact_type.rsplit('.', 1)[-1]}.{child}",
                child_fact_id(fact_type, child), value)})
    if closed:
        add("assertion", {"finding": _finding(
            "demo.probe.closure",
            f"{CLOSURE}|family-horizon={horizon},tax-year={YEAR}", True)})
    acts.append(_act(len(acts), "package-adoption", {
        "package": {"id": package["id"], "version": package["version"],
                    "checksum": package["package_checksum"]},
        "release": {"id": release["id"], "version": release["version"],
                    "checksum": release["checksum"]},
        "revision": len(acts) + 1,
        "scope": {"jurisdiction": "us", "year": YEAR},
        "audit": {"note": "synthetic probe adoption; non-authoritative"},
    }))
    return acts


def run_case(surface: PublicationSurface, acts: list[dict[str, Any]], label: str,
             *, trace: bool = False) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=REPO,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=f"demo-probe-{label}",
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            return {"refusal": outcome.refusal.reason, "detail": outcome.refusal.detail,
                    "issues": [dict(i) for i in outcome.refusal.issues][:8]}
        published: dict[str, str] = {}
        by_id: dict[str, dict[str, Any]] = {}
        for pub in outcome.publications or ():
            published[str(pub.finding["symbol"])] = str(pub.finding["value"])
            by_id[str(pub.finding["id"])] = pub.finding
        blocked: list[dict[str, Any]] = []
        if outcome.output_path is not None:
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            for row in report.get("dispositions", []):
                if row.get("disposition") == "blocked":
                    blocked.append({k: row.get(k) for k in (
                        "artifact_id", "code", "missing", "subject_fact_id")})
        result: dict[str, Any] = {"published": published, "blocked": blocked}
        if trace:
            result["by_id"] = by_id
        return result


def trace_tree(result: dict[str, Any], symbol: str, indent: int = 2) -> list[str]:
    by_id = result["by_id"]
    root = next((f for f in by_id.values() if f["symbol"] == symbol), None)
    if root is None:
        return [" " * indent + f"{_short(symbol)}: not published"]
    lines = [" " * indent + f"{_short(root['symbol'])} = {root['value']}"]
    for pin in root["pins"]:
        if pin.get("role") != "input":
            continue
        child = by_id.get(pin["id"])
        if child is None:
            lines.append(" " * (indent + 2) + f"[input {pin['id'].replace('demo.probe.', '')}"
                         f" origin={pin.get('origin')}]")
        else:
            lines.extend(trace_tree(result, child["symbol"], indent + 2))
    return lines


def passing(**overrides: str) -> dict[str, str]:
    answers = {t: "yes" for t in (REL, JOINT, SSN, U17, RES, SUP, CIT, CLAIM)}
    answers[OTHER] = "no"
    answers.update(overrides)
    return answers


def build_cases() -> dict[str, tuple[dict[str, dict[str, str]], bool]]:
    """Built per mode, so the answer keys follow the bound vocabulary."""
    return {
        "two-claimed-children-pass": (
            {"demo-child-1": passing(), "demo-child-2": passing()}, True),
        "child-2-aged-17-claimed (ODC: blocks)": (
            {"demo-child-1": passing(), "demo-child-2": passing(**{U17: "no"})}, True),
        "child-2-no-ssn-claimed (ODC: blocks)": (
            {"demo-child-1": passing(), "demo-child-2": passing(**{SSN: "no"})}, True),
        "child-2-not-claimed-lives-elsewhere": (
            {"demo-child-1": passing(),
             "demo-child-2": passing(**{CLAIM: "no", RES: "no"})}, True),
        "child-2-residency-unanswered": (
            {"demo-child-1": passing(),
             "demo-child-2": {k: v for k, v in passing().items() if k != RES}}, True),
        "child-2-citizenship-unanswered": (
            {"demo-child-1": passing(),
             "demo-child-2": {k: v for k, v in passing().items() if k != CIT}}, True),
        "child-2-not-claimed-age-unanswered": (
            {"demo-child-1": passing(),
             "demo-child-2": {k: v for k, v in passing(**{CLAIM: "no"}).items() if k != U17}}, True),
        "roster-not-closed": ({"demo-child-1": passing()}, False),
        "no-children-closed-empty": ({}, True),
    }


def summarize(result: dict[str, Any]) -> str:
    if "refusal" in result:
        return f"  REFUSED {result['refusal']}: {result['detail']} {result['issues']}"
    published = result["published"]
    count = {s: v for s, v in published.items() if s.endswith(P + "child-count")}
    per_child = {_short(s).split("ctc-counts|")[-1]: v
                 for s, v in sorted(published.items()) if "child.ctc-counts|" in s}
    blocked = sorted({(b["artifact_id"].rsplit(".", 1)[-1], b["code"])
                      for b in result["blocked"] if "ctc-child" in b["artifact_id"]
                      or "claimed" in b["artifact_id"]})
    return "\n".join([
        f"  count       {list(count.values()) or 'not published'}",
        f"  per-child   {per_child}",
        f"  blocked     {blocked}",
    ])


def run_mode(mode: str) -> None:
    configure(mode)
    cases = build_cases()
    print(f"##### mode: {mode}")
    with tempfile.TemporaryDirectory() as tmp:
        try:
            surface, package, release = build_surface(Path(tmp))
        except Exception as exc:  # the surface itself may be refused by the registry
            print(f"  SURFACE REFUSED {type(exc).__name__}: {exc}")
            return
        for case_label, (children, closed) in cases.items():
            acts = build_acts(children, package, release, closed=closed)
            print(f"== {case_label}")
            try:
                print(summarize(run_case(surface, copy.deepcopy(acts), case_label)))
            except Exception as exc:
                print(f"  RUN REFUSED {type(exc).__name__}: {exc}")
        if mode == "private":
            children, closed = cases["two-claimed-children-pass"]
            acts = build_acts(children, package, release, closed=closed)
            result = run_case(surface, copy.deepcopy(acts), "trace", trace=True)
            print("== pin closure under the return count, two-claimed-children-pass")
            print("\n".join(trace_tree(result, P + "child-count")))


MODES = ("private", "same-family", "separate-family", "separate-alone", "separate-own-member")


def main() -> int:
    for mode in MODES:
        run_mode(mode)
    configure("private")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
