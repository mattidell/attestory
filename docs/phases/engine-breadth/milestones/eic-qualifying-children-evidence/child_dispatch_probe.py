"""P0 probe: can per-child tests be evaluated per child on the live path?

Investigation only. Builds a throwaway publication surface in a temporary
directory (synthetic citizens, a package, a registry, a release) and runs
synthetic children, named ``demo-child-N``, through the real coordinator,
``packages.derivation.live.live_coordinate_run``. Nothing is written under the
repository, and no published content, fixture or test is touched. Run from the
repository root:

    python3 docs/phases/engine-breadth/milestones/eic-qualifying-children-evidence/child_dispatch_probe.py

Three rule shapes are compared over the same recorded children.

``chain``
    One per-child rule per test, each with the test's own answer as its
    subject, then one per-child combining rule that requires the per-test
    results, then a return-level rule that reads the per-child results.
``flat``
    The Form 1098 shape: one per-child rule whose ``requires`` lists every
    other per-child answer as an ordinary input.
``joined``
    The combined-answer alternative: one per-child answer as the subject and
    the per-child SSN answer as the one ``joined`` type.

The probe prints what each shape publishes or blocks for each case.
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
CHILD_KIND = "probe.eic-child"
P = "probe.eic."
SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}

REL = P + "child.relationship"
AGE = P + "child.age"
RES = P + "child.residency"
JOINT = P + "child.joint-return"
SSN = P + "child.ssn"
OTHER = P + "child.another-may-claim"
COMBINED = P + "child.meets-relationship-age-residency-joint-return"
ANSWER_TYPES = (REL, AGE, RES, JOINT, SSN, OTHER, COMBINED)
CLOSURE = P + "child-roster.source-closure"
INERT = P + "child.inert-path-unwritten"
FAMILY = P + "child-roster"
CLOSURE_MAPPING = P + "closure-mapping.child-roster"
BUNDLE = P + "child.vocabulary"
RULE_PREFIX = P + "rule."


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
        "label": "Synthetic per-child vocabulary",
        "fact_types": [*(_fact_type(t) for t in ANSWER_TYPES), closure, inert],
    }


def _family() -> dict[str, Any]:
    return {
        "schema": "source-family.v1",
        "id": FAMILY,
        "version": "v1",
        "scope": dict(SCOPE),
        "title": "Synthetic child roster",
        "member_predicate": {"fact_type": REL},
        "authorizes_subtotal": P + "child-count",
        "closure_claim": "Every qualifying-child candidate is recorded as a roster item.",
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
        "member_fact_type": _pin(REL),
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


def _is_one(name: str) -> dict[str, Any]:
    return {"op": "compare", "cmp": "eq", "left": {"op": "ref", "name": name}, "right": 1}


def _symbol(short: str) -> str:
    return P + "child." + short


def _all_met(names: list[str]) -> dict[str, Any]:
    """Short-circuits: a later result is never read once an earlier one is 0."""
    return {"op": "all", "args": [_is_one(name) for name in names]}


def _sum_met(names: list[str]) -> dict[str, Any]:
    """Reads every result, so every required result is also a pinned read."""
    return {
        "op": "compare", "cmp": "eq", "right": len(names),
        "left": {"op": "add", "args": [{"op": "ref", "name": n} for n in names]},
    }


def _other_claim_guard(other_ref: str, then_expr: Any) -> dict[str, Any]:
    """A yes to ``another-may-claim`` refuses; it never counts and is never 0."""
    return {
        "op": "choose",
        "when": _yes(other_ref),
        "then": {"op": "block", "code": "DEPENDENCY_INVALID"},
        "else": then_expr,
    }


def _count_rule(shape: str, subject_type: str) -> dict[str, Any]:
    """Return-level count of one shape's per-child results (ADR 0077 selection)."""
    read = _symbol("counts-" + shape)
    return _rule(
        f"{RULE_PREFIX}qualifying-child-count-{shape}",
        schema="rule-artifact.v14",
        when=True,
        selection={
            "mode": "exclusive_presence",
            "conflict": "refuse",
            "paths": [
                {
                    "id": "children",
                    "activity": {"kind": "source_nonempty", "member_fact_types": [_pin(REL)]},
                    "reads_subject_results": [{"symbol": read, "subject": _pin(subject_type)}],
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
                "value": {"op": "count", "name": REL, "source_set": FAMILY},
            },
            "refusal": {
                "code": "DEPENDENCY_INVALID",
                "missing": ["probe-eic-child-roster-inert-path-conflict"],
                "pins": [],
            },
        },
        publishes=_symbol("count-" + shape),
    )


def _rules(variant: str) -> list[dict[str, Any]]:
    """``full`` carries every shape; ``flat-alone`` carries only the flat shape,
    so no answer type is the subject or joined type of any other rule."""
    rules: list[dict[str, Any]] = []
    if variant == "full":
        test_symbols = {}
        for answer, short in ((REL, "relationship"), (AGE, "age"), (RES, "residency"),
                              (JOINT, "joint-return"), (SSN, "ssn")):
            test_symbols[answer] = _symbol(short + "-met")
            rules.append(_rule(
                f"{RULE_PREFIX}{short}-met",
                subject=_pin(answer),
                when=True,
                value=_met(answer),
                publishes=test_symbols[answer],
            ))
        # chain: the combining rule's subject is the relationship answer; every
        # other per-test result joins to it by the shared (child, tax-year) keys.
        other_met = _symbol("other-claimant-clear")
        rules.append(_rule(
            f"{RULE_PREFIX}other-claimant-clear",
            subject=_pin(OTHER),
            when=True,
            value=_other_claim_guard(OTHER, 1),
            publishes=other_met,
        ))
        chain_inputs = [test_symbols[t] for t in (REL, AGE, RES, JOINT, SSN)] + [other_met]
        rules.append(_rule(
            f"{RULE_PREFIX}child-counts-chain",
            subject=_pin(REL),
            requires=chain_inputs,
            when=True,
            value={"op": "choose", "when": _sum_met(chain_inputs), "then": 1, "else": 0},
            publishes=_symbol("counts-chain"),
        ))
        rules.append(_rule(
            f"{RULE_PREFIX}child-counts-chain-all",
            subject=_pin(REL),
            requires=chain_inputs,
            when=True,
            value={"op": "choose", "when": _all_met(chain_inputs), "then": 1, "else": 0},
            publishes=_symbol("counts-chain-all"),
        ))
        # joined: combined answer as subject, the SSN answer as the one joined type.
        rules.append(_rule(
            f"{RULE_PREFIX}child-counts-joined",
            subject=_pin(COMBINED),
            joined=_pin(SSN),
            direction="joined_contains_subject",
            requires=[SSN],
            when=True,
            value={
                "op": "choose",
                "when": {"op": "all", "args": [_yes(COMBINED), _yes(SSN)]},
                "then": 1,
                "else": 0,
            },
            publishes=_symbol("counts-joined"),
        ))
        # the literal count-over-a-source-family reading, for contrast
        rules.append(_rule(
            f"{RULE_PREFIX}child-rows-counted",
            when=True,
            value={"op": "count", "name": REL, "source_set": FAMILY},
            publishes=_symbol("rows-counted"),
        ))
        rules.append(_count_rule("chain", REL))
        rules.append(_count_rule("chain-all", REL))
        rules.append(_count_rule("joined", COMBINED))
    # flat: the Form 1098 shape, every other answer an ordinary required input.
    flat_inputs = [AGE, RES, JOINT, SSN]
    rules.append(_rule(
        f"{RULE_PREFIX}child-counts-flat",
        subject=_pin(REL),
        requires=flat_inputs,
        when=True,
        value={
            "op": "choose",
            "when": {"op": "all", "args": [_yes(REL), *(_yes(a) for a in flat_inputs)]},
            "then": 1,
            "else": 0,
        },
        publishes=_symbol("counts-flat"),
    ))
    rules.append(_count_rule("flat", REL))
    return rules


def _citizens(variant: str) -> list[tuple[dict[str, Any], str]]:
    """Every citizen body with its package-member role."""
    members: list[tuple[dict[str, Any], str]] = [
        (_bundle(), "fact-type-bundle"),
        (_family(), "source-family"),
        (_closure_mapping(), "source-closure-mapping"),
    ]
    members.extend((rule, "computation") for rule in _rules(variant))
    return members


def build_surface(root: Path, variant: str = "full") -> tuple[PublicationSurface, dict[str, Any], dict[str, Any]]:
    base = json.loads(
        (REPO / "packages/content/tax/2025/package.core-calculations.v53.json").read_text("utf-8")
    )
    member_dir = root / "members"
    member_dir.mkdir()
    citizens = _citizens(variant)
    registry_citizens = []
    members = []
    for body, role in citizens:
        (member_dir / f"{body['id']}.{body['version']}.json").write_text(
            json.dumps(body, sort_keys=True), encoding="utf-8")
        registry_citizens.append({
            "id": body["id"], "version": body["version"], "checksum": citizen_checksum(body)})
        members.append({
            "id": body["id"], "version": body["version"], "schema": body["schema"], "role": role})
    package: dict[str, Any] = {
        "schema": base["schema"],
        "id": "probe.package.eic-children",
        "version": "v1",
        "scope": dict(base["scope"]),
        "admitted_schemas": list(base["admitted_schemas"]),
        "composition_obligations": [],
        "conflict_semantics": [],
        "entrypoints": [
            {"id": m["id"], "version": m["version"]}
            for m in members
            if m["role"] in ("source-family", "source-closure-mapping", "fact-type-bundle")
            or "qualifying-child-count" in m["id"] or "rows-counted" in m["id"]
        ],
        "input_bindings": [],
        "members": members,
    }
    package["package_checksum"] = package_instance_checksum(package)
    (member_dir / "package.json").write_text(json.dumps(package, sort_keys=True), encoding="utf-8")
    registry = {
        "citizens": registry_citizens,
        "packages": [{
            "id": package["id"], "version": package["version"],
            "checksum": package["package_checksum"]}],
    }
    registry_path = root / "registry.json"
    registry_path.write_text(json.dumps(registry, sort_keys=True), encoding="utf-8")
    release = {
        "id": "probe.release.eic-children",
        "version": "v1",
        "schema": "release-registry.v1",
        "package_registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest(),
    }
    release_dir = root / "releases"
    release_dir.mkdir()
    release_path = release_dir / "probe.release.eic-children.v1.json"
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


def build_acts(
    children: dict[str, dict[str, str]],
    package: dict[str, Any],
    release: dict[str, Any],
    *,
    closed: bool = True,
) -> list[dict[str, Any]]:
    """``children`` maps a synthetic child label to its answers (type -> value)."""
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
                    f"demo.probe.rel.{child}", child_fact_id(REL, child), answers[REL]),
            },
            "successor": {"id": successor, "predecessor": horizon},
        })
        horizon = successor
        for fact_type, value in answers.items():
            if fact_type == REL:
                continue
            add("assertion", {"finding": _finding(
                f"demo.probe.{fact_type.rsplit('.', 1)[-1]}.{child}",
                child_fact_id(fact_type, child), value)})
    if closed:
        add("assertion", {"finding": _finding(
            "demo.probe.closure",
            f"{CLOSURE}|family-horizon={horizon},tax-year={YEAR}", True)})
    adoption = _act(len(acts), "package-adoption", {
        "package": {
            "id": package["id"], "version": package["version"],
            "checksum": package["package_checksum"]},
        "release": {
            "id": release["id"], "version": release["version"], "checksum": release["checksum"]},
        "revision": len(acts) + 1,
        "scope": {"jurisdiction": "us", "year": YEAR},
        "audit": {"note": "synthetic probe adoption; non-authoritative"},
    })
    acts.append(adoption)
    return acts


def run_case(
    surface: PublicationSurface, acts: list[dict[str, Any]], label: str, *, trace: bool = False
) -> dict[str, Any]:
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
                    "issues": [dict(i) for i in outcome.refusal.issues][:12]}
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


def _short(symbol: str) -> str:
    return symbol.replace(P, "").replace(",tax-year=2025", "").replace("child=", "")


def trace_tree(result: dict[str, Any], symbol: str, indent: int = 2) -> list[str]:
    """The pin closure under one published symbol, the way an explanation walks it."""
    by_id = result["by_id"]
    root = next((f for f in by_id.values() if f["symbol"] == symbol), None)
    if root is None:
        return [" " * indent + f"{symbol}: not published"]
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
    answers = {t: "yes" for t in (REL, AGE, RES, JOINT, SSN)}
    answers[OTHER] = "no"
    answers.update(overrides)
    core = all(answers.get(t) == "yes" for t in (REL, AGE, RES, JOINT))
    answers.setdefault(COMBINED, "yes" if core else "no")
    if COMBINED not in overrides:
        answers[COMBINED] = "yes" if core else "no"
    return answers


CASES: dict[str, tuple[dict[str, dict[str, str]], bool]] = {
    "two-children-both-pass": (
        {"demo-child-1": passing(), "demo-child-2": passing()}, True),
    "child-2-fails-age": (
        {"demo-child-1": passing(), "demo-child-2": passing(**{AGE: "no"})}, True),
    "child-2-no-ssn": (
        {"demo-child-1": passing(), "demo-child-2": passing(**{SSN: "no"})}, True),
    "child-2-other-may-claim": (
        {"demo-child-1": passing(), "demo-child-2": passing(**{OTHER: "yes"})}, True),
    "child-2-residency-unanswered": (
        {"demo-child-1": passing(),
         "demo-child-2": {k: v for k, v in passing().items() if k != RES}}, True),
    "roster-not-closed": ({"demo-child-1": passing()}, False),
    "no-children-closed-empty": ({}, True),
}


def summarize(result: dict[str, Any]) -> str:
    if "refusal" in result:
        return f"  REFUSED {result['refusal']}: {result['detail']} {result['issues']}"
    published = result["published"]
    counts = {
        s.rsplit(".", 1)[-1]: v for s, v in sorted(published.items())
        if ".child.count-" in s or ".child.rows-counted" in s
    }
    lines = [f"  counts      {counts}"]
    for shape in ("chain", "chain-all", "flat", "joined"):
        per_child = {
            _short(s).split("counts-" + shape + "|")[-1]: v
            for s, v in sorted(published.items()) if ".child.counts-" + shape + "|" in s
        }
        if per_child:
            lines.append(f"  per-child   {shape:7s} {per_child}")
    blocked = sorted({
        (b["artifact_id"].rsplit(".", 1)[-1], b["code"], (b.get("subject_fact_id") or "")
         .split("child=")[-1][:14]) for b in result["blocked"]
        if "child-counts" in b["artifact_id"] or "qualifying-child-count" in b["artifact_id"]
        or "-met" in b["artifact_id"] or "other-claimant" in b["artifact_id"]
    })
    lines.append(f"  blocked     {blocked}")
    return "\n".join(lines)


def main() -> int:
    for variant in ("full", "flat-alone"):
        print(f"##### variant: {variant}")
        with tempfile.TemporaryDirectory() as tmp:
            surface, package, release = build_surface(Path(tmp), variant)
            for label, (children, closed) in CASES.items():
                acts = build_acts(children, package, release, closed=closed)
                print(f"== {label}")
                print(summarize(run_case(surface, copy.deepcopy(acts), label)))
            if variant == "full":
                children, closed = CASES["child-2-fails-age"]
                acts = build_acts(children, package, release, closed=closed)
                result = run_case(surface, copy.deepcopy(acts), "trace", trace=True)
                for shape in ("chain-all", "chain"):
                    print(f"== pin closure under the {shape} count, child-2-fails-age")
                    print("\n".join(trace_tree(result, _symbol("count-" + shape))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
