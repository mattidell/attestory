"""P0 probe: can the credit for other dependents share the child roster?

Investigation only. Builds a throwaway publication surface in a temporary
directory (synthetic fact types, three source families, a package, a registry,
a release) and runs synthetic dependents, named ``demo-child-N`` and
``demo-dependent-N``, through the real coordinator,
``packages.derivation.live.live_coordinate_run``. Nothing is written under the
repository, and no published content, fixture or test is touched. Run:

    python3 docs/phases/engine-breadth/milestones/other-dependents-credit-evidence/odc_probe.py

The model under test (evidence file, section 3). Each dependent is a claimed row on
one family; a fact belongs to one family, so each family has its own member fact.

- ``ctc``: the child tax credit family over the child kind. Member: the child tax
  credit box (``child.claimed``). A box-yes child must pass every CTC test (under
  17, SSN valid for employment, and the others), else it blocks.
- ``odc-child``: a second family over the same child kind. Member: the credit for
  other dependents box (``child.odc-box``). A box-yes child must fail the CTC age or
  SSN test and have an SSN, ITIN or ATIN issued by the due date (``child.tin``).
- ``odc-relative``: a family over a new entity kind for other dependents who are
  not children. Member: its ODC box (``dependent.claimed``). Every relative test must
  pass, else it blocks.
- ``spouse-gate``: a return-level rule with no subject, as ``rule.ctc-spouse-gate``.
  With any counted dependent the taxpayer SSN or ITIN is required; on a joint return
  the spouse's SSN or ITIN is too. These conditional reads bind run-wide.

The per-child TIN is asked for every child. A per-subject rule reads only symbols named
in ``requires`` (``packages/derivation/live.py``, per-subject discovery), so a per-child
answer read only under a condition on another child answer is not expressible
without an engine change. The probe shows the cost: a CTC child without a TIN answer
blocks (case A4b).

Each case prints the three subtotals, the spouse gate, and every block with the
missing answer.
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
P = "probe.odc."
KIND_C = "probe.odc-child"
KIND_R = "probe.odc-relative"
CTC_FAMILY = "probe.ctc.child-roster"
ODC_FAMILY = "probe.odc.child-roster"
REL_FAMILY = "probe.odc.relative-roster"

# Child answers (kind KIND_C). Shared answers are the existing credit and EIC facts
# in the real content; this probe gives them synthetic ids of the same shape.
C = {k: P + "child." + k for k in (
    "relationship", "joint-return", "another-may-claim", "citizen", "lived-with-you",
    "no-support", "under-17", "ssn", "claimed", "odc-box", "tin")}
# Dependent answers (kind KIND_R). New facts for other dependents who are not children.
R = {k: P + "dependent." + k for k in (
    "claimed", "relationship", "not-qualifying-child", "gross-income", "support",
    "tin", "citizen", "not-married")}
FS = P + "filing-status"
SPOUSE = P + "spouse-tin"
TAXPAYER = P + "taxpayer-tin"
CLOSURE = {
    CTC_FAMILY: "probe.ctc.child-roster.source-closure",
    ODC_FAMILY: P + "odc-child-roster.source-closure",
    REL_FAMILY: P + "odc-relative-roster.source-closure",
}
COUNT = {CTC_FAMILY: "probe.ctc.child-count", ODC_FAMILY: P + "odc-child-count",
         REL_FAMILY: P + "odc-relative-count"}
INERT = {"ctc": "probe.ctc.child.inert", "odc": P + "child.inert",
         "rel": P + "dependent.inert"}
# A fact belongs to one family (the kernel checks membership across all findings),
# so each family has its own member fact: the child tax credit box (claimed) for the
# child family, and the credit-for-other-dependents box (odc-box) for the other-dependent
# family over the same child kind. The relative family uses the relative's ODC box.
CHILD_CLAIM_MEMBER = C["claimed"]
ODC_CHILD_MEMBER = C["odc-box"]
REL_MEMBER = R["claimed"]


def _pin(item_id: str, version: str = "v1") -> dict[str, str]:
    return {"id": item_id, "version": version}


def _yes(fact: str) -> dict[str, Any]:
    return {"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": fact},
            "right": {"op": "category_literal", "fact_type": _pin(fact), "value": "yes"}}


def _no(fact: str) -> dict[str, Any]:
    return {"op": "categorical_compare", "cmp": "eq", "left": {"op": "ref", "name": fact},
            "right": {"op": "category_literal", "fact_type": _pin(fact), "value": "no"}}


def _met(fact: str) -> dict[str, Any]:
    return {"op": "choose", "when": _yes(fact), "then": 1, "else": 0}


def _sum_eq(items: list[dict[str, Any]], n: int) -> dict[str, Any]:
    return {"op": "compare", "cmp": "eq", "left": {"op": "add", "args": items}, "right": n}


def _block(code: str = "DEPENDENCY_INVALID") -> dict[str, Any]:
    return {"op": "block", "code": code}


def _fact_type(fact_id: str, kind: str | None, enum: list[str]) -> dict[str, Any]:
    keys: list[dict[str, Any]] = []
    if kind == "child":
        keys.append({"name": "child", "kind": "entity", "entity_kind": KIND_C})
    elif kind == "dependent":
        keys.append({"name": "dependent", "kind": "entity", "entity_kind": KIND_R})
    keys.append({"name": "tax-year", "kind": "literal", "values": [YEAR]})
    return {"schema": "fact-type.v2", "id": fact_id, "version": "v1",
            "title": f"Synthetic answer {fact_id}", "nature": "determinable",
            "identity_keys": keys, "value_schema": {"type": "string", "enum": enum},
            "supersession": {"policy": "free"}}


def _closure_fact(closure_id: str) -> dict[str, Any]:
    return {"schema": "fact-type.v2", "id": closure_id, "version": "v1",
            "title": f"Closure of {closure_id}", "nature": "determinable",
            "identity_keys": [{"name": "family-horizon", "kind": "entity",
                               "entity_kind": "kernel.family-horizon"},
                              {"name": "tax-year", "kind": "literal", "values": [YEAR]}],
            "value_schema": {"type": "boolean"}, "supersession": {"policy": "free"}}


def _inert_fact(inert_id: str) -> dict[str, Any]:
    return {"schema": "fact-type.v2", "id": inert_id, "version": "v1",
            "title": "Internal marker used only to complete an inert rule path",
            "nature": "determinable",
            "identity_keys": [{"name": "marker", "kind": "literal", "values": ["unused"]}],
            "value_schema": {"type": "string", "enum": ["unused"]},
            "supersession": {"policy": "free"}}


def _bundle() -> dict[str, Any]:
    yn = ["yes", "no"]
    fts = [_fact_type(v, "child", yn) for v in C.values()]
    fts += [_fact_type(v, "dependent", yn) for v in R.values()]
    fts += [_fact_type(FS, None, ["single", "mfj", "hoh"]), _fact_type(SPOUSE, None, yn),
            _fact_type(TAXPAYER, None, yn)]
    fts += [_closure_fact(v) for v in CLOSURE.values()]
    fts += [_inert_fact(v) for v in INERT.values()]
    return {"schema": "bundle.v2", "id": P + "vocabulary", "version": "v1",
            "label": "Synthetic other-dependent credit vocabulary", "fact_types": fts}


def _family(fid: str, member: str, subtotal: str, scope_kind: str) -> dict[str, Any]:
    return {"schema": "source-family.v1", "id": fid, "version": "v1", "scope": dict(SCOPE),
            "title": f"Synthetic {scope_kind} roster", "member_predicate": {"fact_type": member},
            "authorizes_subtotal": subtotal,
            "closure_claim": f"Every {scope_kind} is recorded as a roster item."}


def _mapping(mid: str, fid: str, member: str, subtotal: str) -> dict[str, Any]:
    return {"schema": "source-closure-mapping.v2", "id": mid, "version": "v1",
            "admission": {"condition": "current-literal-true"}, "admits_symbol": subtotal,
            "closure_fact_type": _pin(CLOSURE[fid]), "closure_horizon_key": "family-horizon",
            "family": _pin(fid), "member_fact_type": _pin(member)}


def _rule(rule_id: str, *, requires: list[str], subject: str, value: Any,
          publishes: str, schema: str = "rule-artifact.v14",
          conditional: tuple[str, ...] = ()) -> dict[str, Any]:
    """``conditional`` names assertion inputs read only under a conditional set. They
    are pinned (as production rules pin them) so the marshaller supplies them."""
    return {"schema": schema, "id": rule_id, "version": "v1", "scope": dict(SCOPE),
            "role": "computation", "requires": requires,
            "pins": [{"id": c, "origin": "assertion", "role": "input", "version": "v1"}
                     for c in conditional],
            "subject": _pin(subject), "when": True, "value": value,
            "publishes": publishes, "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []}}


def _other_tests_ok() -> dict[str, Any]:
    """Joint return, lived with you, no own support, citizen or resident, and not
    claimed by another (tie-breaker). Shared by both child families."""
    return _sum_eq([_met(C["joint-return"]), _met(C["lived-with-you"]),
                    _met(C["no-support"]), _met(C["citizen"]),
                    {"op": "choose", "when": _yes(C["another-may-claim"]), "then": 0,
                     "else": 1}], 5)


def _ages_ok() -> dict[str, Any]:
    """Under 17 at the end of 2025 and an SSN valid for employment: the child tax credit."""
    return _sum_eq([_met(C["under-17"]), _met(C["ssn"])], 2)


# Every roster child answers every child test, the TIN answer included. The TIN is read
# only where the SSN is no, but the subject-dispatch emits only symbols named in
# `requires`, so a conditional per-child read is not expressible (evidence file, section 3).
CHILD_TESTS = [C[k] for k in ("claimed", "odc-box", "joint-return", "lived-with-you",
                              "no-support", "citizen", "another-may-claim", "under-17", "ssn",
                              "tin")]


def _ctc_child_rule() -> dict[str, Any]:
    """Subject: the child tax credit box. Box yes must pass every CTC test, else block."""
    both_boxes = {"op": "all", "args": [_yes(C["claimed"]), _yes(C["odc-box"])]}
    value = {"op": "choose", "when": _no(C["claimed"]), "then": 0, "else": {
        "op": "choose", "when": both_boxes, "then": _block(),
        "else": {"op": "choose", "when": {"op": "all", "args": [_other_tests_ok(), _ages_ok()]},
                 "then": 1, "else": _block()}}}
    return _rule(P + "rule.ctc-child-counts", requires=CHILD_TESTS, subject=C["claimed"],
                 value=value, publishes=P + "child.ctc-counts")


def _odc_child_rule() -> dict[str, Any]:
    """Subject: the credit-for-other-dependents box. Box yes must fail the CTC age or SSN
    test, pass the rest, and have an SSN, ITIN or ATIN issued by the due date (the TIN
    answer counts when SSN is no; an SSN satisfies the identification test by itself)."""
    tin_or_ssn = {"op": "choose", "when": _yes(C["ssn"]), "then": 1, "else": {
        "op": "choose", "when": _yes(C["tin"]), "then": 1, "else": _block()}}
    value = {"op": "choose", "when": _no(C["odc-box"]), "then": 0, "else": {
        "op": "choose", "when": _yes(C["claimed"]), "then": _block(), "else": {
            "op": "choose", "when": _other_tests_ok(), "then": {
                "op": "choose", "when": _ages_ok(), "then": _block(), "else": tin_or_ssn},
            "else": _block()}}}
    return _rule(P + "rule.odc-child-counts", requires=CHILD_TESTS, subject=C["odc-box"],
                 value=value, publishes=P + "child.odc-counts")


def _rel_rule() -> dict[str, Any]:
    tests = [R[k] for k in ("relationship", "not-qualifying-child", "gross-income",
                            "support", "tin", "citizen", "not-married")]
    value = {"op": "choose", "when": _no(R["claimed"]), "then": 0, "else": {
        "op": "choose", "when": _sum_eq([_met(t) for t in tests], 7), "then": 1,
        "else": _block()}}
    return _rule(P + "rule.relative-counts", requires=[R["claimed"], *tests],
                 subject=R["claimed"], value=value, publishes=P + "dependent.counts")


def _count_rule(name: str, family: str, member: str, read: str, subject: str,
                inert: str) -> dict[str, Any]:
    """Counts the per-subject results over a closed family (as the CTC probe does)."""
    return {
        "schema": "rule-artifact.v14", "id": P + "rule." + name, "version": "v1",
        "scope": dict(SCOPE), "role": "computation", "requires": [], "pins": [],
        "when": True, "publishes": COUNT[family],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "selection": {
            "mode": "exclusive_presence", "conflict": "refuse",
            "paths": [
                {"id": "members",
                 "activity": {"kind": "source_nonempty", "member_fact_types": [_pin(member)]},
                 "reads_subject_results": [{"symbol": read, "subject": _pin(subject)}],
                 "requires": [], "pins": [],
                 "when": {"op": "require_closed", "source_set": family},
                 "value": {"op": "add", "args": [
                     {"op": "collect", "name": read, "source_set": family}]}},
                {"id": "inert",
                 "activity": {"kind": "source_nonempty", "member_fact_types": [_pin(inert)]},
                 "reads_subject_results": [], "requires": [], "pins": [], "when": True,
                 "value": {"op": "block", "code": "DEPENDENCY_ABSENT"}},
            ],
            "default": {"id": "neither", "reads_subject_results": [], "requires": [],
                        "pins": [], "when": True,
                        "value": {"op": "count", "name": member, "source_set": family}},
            "refusal": {"code": "DEPENDENCY_INVALID",
                        "missing": [f"probe-{name}-inert-path-conflict"], "pins": []},
        },
    }


def _spouse_gate() -> dict[str, Any]:
    """Return level, subject-free (as rule.ctc-spouse-gate). With any counted dependent the
    taxpayer SSN or ITIN is required; on a joint return the spouse's is too."""
    total = {"op": "add", "args": [{"op": "ref", "name": COUNT[CTC_FAMILY]},
                                   {"op": "ref", "name": COUNT[ODC_FAMILY]},
                                   {"op": "ref", "name": COUNT[REL_FAMILY]}]}
    any_dependent = {"op": "compare", "cmp": "gt", "left": total, "right": 0}
    joint = {"op": "categorical_compare", "cmp": "eq",
             "left": {"op": "ref", "name": FS},
             "right": {"op": "category_literal", "fact_type": _pin(FS), "value": "mfj"}}
    spouse_check = {"op": "choose", "when": {"op": "all", "args": [{
        "op": "conditional_dependency_set", "condition": any_dependent,
        "members": [{"op": "ref", "name": SPOUSE}]}]}, "then": 1, "else": _block()}
    taxpayer_check = {"op": "choose", "when": {"op": "all", "args": [{
        "op": "conditional_dependency_set", "condition": any_dependent,
        "members": [{"op": "ref", "name": TAXPAYER}]}]}, "then": {
        "op": "choose", "when": joint, "then": spouse_check, "else": 1}, "else": 1}
    value = taxpayer_check
    rule = _rule(P + "rule.spouse-gate", requires=[FS, COUNT[CTC_FAMILY], COUNT[ODC_FAMILY],
                                                  COUNT[REL_FAMILY]],
                 subject=FS, value=value, publishes=P + "spouse-gate",
                 conditional=(SPOUSE, TAXPAYER))
    del rule["subject"]
    return rule


def _rules() -> list[dict[str, Any]]:
    return [
        _ctc_child_rule(), _odc_child_rule(), _rel_rule(),
        _count_rule("ctc-child-count", CTC_FAMILY, CHILD_CLAIM_MEMBER,
                    P + "child.ctc-counts", C["claimed"], INERT["ctc"]),
        _count_rule("odc-child-count", ODC_FAMILY, ODC_CHILD_MEMBER,
                    P + "child.odc-counts", C["odc-box"], INERT["odc"]),
        _count_rule("odc-relative-count", REL_FAMILY, REL_MEMBER,
                    P + "dependent.counts", R["claimed"], INERT["rel"]),
        _spouse_gate(),
    ]


def _entrypoint_ids() -> list[str]:
    return [P + "vocabulary", CTC_FAMILY, ODC_FAMILY, REL_FAMILY,
            P + "rule.ctc-child-count", P + "rule.odc-child-count",
            P + "rule.odc-relative-count", P + "rule.spouse-gate"]


def build_surface(root: Path) -> tuple[PublicationSurface, dict[str, Any], dict[str, Any]]:
    base = json.loads((REPO / "packages/content/tax/2025/package.core-calculations.v55.json")
                      .read_text("utf-8"))
    member_dir = root / "members"
    member_dir.mkdir()
    bodies: list[tuple[dict[str, Any], str]] = [
        (_bundle(), "fact-type-bundle"),
        (_family(CTC_FAMILY, CHILD_CLAIM_MEMBER, COUNT[CTC_FAMILY], "child"), "source-family"),
        (_family(ODC_FAMILY, ODC_CHILD_MEMBER, COUNT[ODC_FAMILY], "child"), "source-family"),
        (_family(REL_FAMILY, REL_MEMBER, COUNT[REL_FAMILY], "dependent"), "source-family"),
        (_mapping(P + "closure-mapping.ctc-child", CTC_FAMILY, CHILD_CLAIM_MEMBER,
                  COUNT[CTC_FAMILY]), "source-closure-mapping"),
        (_mapping(P + "closure-mapping.odc-child", ODC_FAMILY, ODC_CHILD_MEMBER,
                  COUNT[ODC_FAMILY]), "source-closure-mapping"),
        (_mapping(P + "closure-mapping.odc-relative", REL_FAMILY, REL_MEMBER,
                  COUNT[REL_FAMILY]), "source-closure-mapping"),
    ]
    bodies += [(rule, "computation") for rule in _rules()]
    registry_citizens: list[dict[str, Any]] = []
    members: list[dict[str, Any]] = []
    for body, role in bodies:
        (member_dir / f"{body['id']}.{body['version']}.json").write_text(
            json.dumps(body, sort_keys=True), encoding="utf-8")
        registry_citizens.append({"id": body["id"], "version": body["version"],
                                  "checksum": citizen_checksum(body)})
        members.append({"id": body["id"], "version": body["version"],
                        "schema": body["schema"], "role": role})
    package: dict[str, Any] = {
        "schema": base["schema"], "id": "probe.package.odc", "version": "v1",
        "scope": dict(base["scope"]), "admitted_schemas": list(base["admitted_schemas"]),
        "composition_obligations": [], "conflict_semantics": [],
        "entrypoints": [{"id": i, "version": "v1"} for i in _entrypoint_ids()],
        "input_bindings": [],
        "members": members,
    }
    package["package_checksum"] = package_instance_checksum(package)
    (member_dir / "package.json").write_text(json.dumps(package, sort_keys=True), encoding="utf-8")
    registry_path = root / "registry.json"
    registry_path.write_text(json.dumps({"citizens": registry_citizens, "packages": [
        {"id": package["id"], "version": package["version"],
         "checksum": package["package_checksum"]}]}, sort_keys=True), encoding="utf-8")
    release = {"id": "probe.release.odc", "version": "v1", "schema": "release-registry.v1",
               "package_registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest()}
    release_dir = root / "releases"
    release_dir.mkdir()
    release_path = release_dir / "probe.release.odc.v1.json"
    release_path.write_text(json.dumps(release, sort_keys=True), encoding="utf-8")
    release["checksum"] = hashlib.sha256(release_path.read_bytes()).hexdigest()
    return PublicationSurface(release_dir, registry_path, member_dir), package, release


def _act(index: int, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"schema": "act.v1", "act_id": f"demo.probe.act.{index:03d}", "kind": kind,
            "actor": USER, "at": f"2026-10-25T00:{index // 60:02d}:{index % 60:02d}Z",
            "committed_against": index, "payload": payload}


def _finding(finding_id: str, fact_id: str, value: Any) -> dict[str, Any]:
    return {"schema": "finding.v2", "id": finding_id, "fact_id": fact_id, "value": value,
            "basis": "attested", "evidence_ids": []}


def _fid(fact: str, entity: tuple[str, str] | None) -> str:
    if entity is None:
        return fact_id_for(fact, (("tax-year", YEAR),))
    return fact_id_for(fact, ((entity[0], entity[1]), ("tax-year", YEAR)))


def build_acts(children: dict[str, dict[str, str]], dependents: dict[str, dict[str, str]],
               package: dict[str, Any], release: dict[str, Any], *, return_facts: dict[str, str],
               closed: dict[str, bool]) -> list[dict[str, Any]]:
    """``closed`` maps family id to whether its closure is asserted."""
    acts: list[dict[str, Any]] = []

    def add(kind: str, payload: dict[str, Any]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _bundle()})
    # Return-level answers come right after the vocabulary, as production asserts them.
    for fact, value in return_facts.items():
        add("assertion", {"finding": _finding(f"demo.probe.ret.{fact.rsplit('.', 1)[-1]}",
                                              f"{fact}|tax-year={YEAR}", value)})
    for child in children:
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": child,
                                             "kind": KIND_C, "label": "Synthetic child"}})
    for dep in dependents:
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": dep,
                                             "kind": KIND_R, "label": "Synthetic dependent"}})
    scope_key = {"tax-year": YEAR, "subject": "demo.primary"}
    horizons: dict[str, str] = {}
    for fam, members, member_fact, name in (
            (CTC_FAMILY, children, CHILD_CLAIM_MEMBER, "child"),
            (ODC_FAMILY, children, ODC_CHILD_MEMBER, "child"),
            (REL_FAMILY, dependents, REL_MEMBER, "dependent")):
        tag = {CTC_FAMILY: "ctc", ODC_FAMILY: "odc", REL_FAMILY: "rel"}[fam]
        head = f"demo.probe.{tag}.h0"
        add("horizon-genesis", {"family": _pin(fam), "scope": scope_key, "horizon_id": head})
        for index, (ent, answers) in enumerate(members.items()):
            succ = f"demo.probe.{tag}.h{index + 1}"
            add("member-transition", {"family": _pin(fam), "scope": scope_key, "member": {
                "action": "assert", "finding": _finding(
                    f"demo.probe.member.{tag}.{ent}", _fid(member_fact, (name, ent)),
                    answers[member_fact])}, "successor": {"id": succ, "predecessor": head}})
            head = succ
        horizons[fam] = head
    for ent, answers in children.items():
        for fact, value in answers.items():
            if fact in (CHILD_CLAIM_MEMBER, ODC_CHILD_MEMBER):
                continue
            add("assertion", {"finding": _finding(
                f"demo.probe.a.{fact.rsplit('.', 1)[-1]}.{ent}", _fid(fact, ("child", ent)), value)})
    for ent, answers in dependents.items():
        for fact, value in answers.items():
            if fact == REL_MEMBER:
                continue
            add("assertion", {"finding": _finding(
                f"demo.probe.a.{fact.rsplit('.', 1)[-1]}.{ent}", _fid(fact, ("dependent", ent)), value)})
    for fam, do in closed.items():
        if do:
            add("assertion", {"finding": _finding(
                f"demo.probe.closure.{fam}",
                f"{CLOSURE[fam]}|family-horizon={horizons[fam]},tax-year={YEAR}", True)})
    acts.append(_act(len(acts), "package-adoption", {
        "package": {"id": package["id"], "version": package["version"],
                    "checksum": package["package_checksum"]},
        "release": {"id": release["id"], "version": release["version"],
                    "checksum": release["checksum"]},
        "revision": len(acts) + 1, "scope": {"jurisdiction": "us", "year": YEAR},
        "audit": {"note": "synthetic probe adoption; non-authoritative"}}))
    return acts


def run_case(surface: PublicationSurface, acts: list[dict[str, Any]], label: str) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"), repo_root=REPO, authoritative_acts=acts,
            workspace_revision=len(acts), run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=USER, request={"schema": "run-request.v1"}, run_id=f"demo-probe-{label}",
            governance_pins=[], surface=surface, output_name="out.json")
        if outcome.refusal is not None:
            return {"refusal": outcome.refusal.reason, "detail": outcome.refusal.detail}
        published = {str(p.finding["symbol"]): str(p.finding["value"])
                     for p in outcome.publications or ()}
        blocked: list[tuple[str, str, str]] = []
        if outcome.output_path is not None:
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            for row in report.get("dispositions", []):
                if row.get("disposition") == "blocked":
                    blocked.append((str(row.get("artifact_id", "")).rsplit(".", 1)[-1],
                                    str(row.get("code")),
                                    ",".join(str(m).rsplit(".", 1)[-1] for m in (row.get("missing") or []))))
        return {"published": published, "blocked": sorted(set(blocked))}


def _value(published: dict[str, str], name: str) -> str:
    for symbol, value in published.items():
        if symbol.split("|")[0].endswith(name):
            return value
    return "-"


def summarize(result: dict[str, Any]) -> str:
    if "refusal" in result:
        return f"  REFUSED {result['refusal']}: {result['detail']}"
    pub = result["published"]
    lines = [
        f"  ctc-child-count {_value(pub, COUNT[CTC_FAMILY])}  "
        f"odc-child-count {_value(pub, COUNT[ODC_FAMILY])}  "
        f"odc-relative-count {_value(pub, COUNT[REL_FAMILY])}  "
        f"spouse-gate {_value(pub, P + 'spouse-gate')}"]
    for art, code, missing in result["blocked"]:
        lines.append(f"  blocked {art} {code} missing=[{missing}]")
    return "\n".join(lines)


def ctc_child(**over: str) -> dict[str, str]:
    """A child for the child tax credit: box yes, every test yes."""
    a = {k: "yes" for k in C.values()}
    a[C["odc-box"]] = "no"
    a[C["another-may-claim"]] = "no"
    a.update(over)
    return a


def odc_child(**over: str) -> dict[str, str]:
    """A child for the other-dependent credit: ODC box yes, fails the age test."""
    a = ctc_child(**{C["claimed"]: "no", C["odc-box"]: "yes", C["under-17"]: "no"})
    a.update(over)
    return a


def odc_child_no_ssn(**over: str) -> dict[str, str]:
    a = odc_child(**{C["ssn"]: "no", C["under-17"]: "yes", C["tin"]: "yes"})
    a.update(over)
    return a


def relative(**over: str) -> dict[str, str]:
    """A relative (other dependent who is not a child) that passes every test."""
    a = {k: "yes" for k in R.values()}
    a.update(over)
    return a


def without(d: dict[str, str], key: str) -> dict[str, str]:
    return {k: v for k, v in d.items() if k != key}


YES = {CTC_FAMILY: True, ODC_FAMILY: True, REL_FAMILY: True}
SINGLE = {FS: "single", TAXPAYER: "yes"}


def cases() -> list[tuple[str, dict[str, Any], dict[str, Any], dict[str, bool], dict[str, str]]]:
    """(label, children, dependents, closure map, return-level facts)."""
    return [
        ("A1 CTC child, single", {"demo-child-1": ctc_child()}, {}, YES, SINGLE),
        ("A2 CTC child + age-17 ODC child, single: CTC 1, ODC 1",
         {"demo-child-1": ctc_child(), "demo-child-2": odc_child()}, {}, YES, SINGLE),
        ("A3 ODC child, no SSN, ITIN yes: ODC 1",
         {"demo-child-1": odc_child_no_ssn(**{C["tin"]: "yes"})}, {}, YES, SINGLE),
        ("A4 ODC child, no SSN, TIN not answered: blocks",
         {"demo-child-1": without(odc_child_no_ssn(), C["tin"])}, {}, YES, SINGLE),
        ("A4b CTC child, TIN not answered: blocks (TIN asked for every child)",
         {"demo-child-1": without(ctc_child(), C["tin"])}, {}, YES, SINGLE),
        ("A5 ODC child, no SSN, TIN no: blocks (no TIN, outside class)",
         {"demo-child-1": odc_child_no_ssn(**{C["tin"]: "no"})}, {}, YES, SINGLE),
        ("A6 CTC box on a child aged 17: blocks (wrong box)",
         {"demo-child-1": ctc_child(**{C["under-17"]: "no"})}, {}, YES, SINGLE),
        ("A7 ODC box on a child who passes every CTC test: blocks",
         {"demo-child-1": odc_child(**{C["under-17"]: "yes"})}, {}, YES, SINGLE),
        ("A8 both boxes yes: blocks",
         {"demo-child-1": ctc_child(**{C["odc-box"]: "yes", C["under-17"]: "no"})},
         {}, YES, SINGLE),
        ("A9 ODC box, lived elsewhere: blocks (outside)",
         {"demo-child-1": odc_child(**{C["lived-with-you"]: "no"})}, {}, YES, SINGLE),
        ("A10 ODC box, age test unanswered: blocks",
         {"demo-child-1": without(odc_child(), C["under-17"])}, {}, YES, SINGLE),
        ("A11 child roster not closed: blocks",
         {"demo-child-1": ctc_child(), "demo-child-2": odc_child()},
         {}, {CTC_FAMILY: False, ODC_FAMILY: False, REL_FAMILY: True}, SINGLE),
        ("A12 closed, no children: 0 and 0", {}, {}, YES, SINGLE),
        ("A13 child with neither box (dependent for other purposes): 0 and 0, no block",
         {"demo-child-1": ctc_child(**{C["claimed"]: "no"})}, {}, YES, SINGLE),
        ("B1 relative passes: relative 1", {}, {"demo-dependent-1": relative()}, YES, SINGLE),
        ("B2 relative gross income at or above limit: blocks",
         {}, {"demo-dependent-1": relative(**{R["gross-income"]: "no"})}, YES, SINGLE),
        ("B3 relative without SSN, ITIN or ATIN: blocks",
         {}, {"demo-dependent-1": relative(**{R["tin"]: "no"})}, YES, SINGLE),
        ("B4 relative roster not closed: blocks", {}, {"demo-dependent-1": relative()},
         {CTC_FAMILY: True, ODC_FAMILY: True, REL_FAMILY: False}, SINGLE),
        ("B5 relative married: blocks (outside)",
         {}, {"demo-dependent-1": relative(**{R["not-married"]: "no"})}, YES, SINGLE),
        ("C1 CTC + age-17 child + relative, joint, spouse TIN yes",
         {"demo-child-1": ctc_child(), "demo-child-2": odc_child()},
         {"demo-dependent-1": relative()}, YES, {FS: "mfj", SPOUSE: "yes", TAXPAYER: "yes"}),
        ("D1 joint, ODC-only child, spouse TIN not answered: blocks",
         {"demo-child-1": odc_child()}, {}, YES, {FS: "mfj", TAXPAYER: "yes"}),
        ("D2 joint, ODC-only child, spouse TIN yes: passes",
         {"demo-child-1": odc_child()}, {}, YES, {FS: "mfj", SPOUSE: "yes", TAXPAYER: "yes"}),
        ("D3 head of household, ODC-only child, no spouse answer: passes",
         {"demo-child-1": odc_child()}, {}, YES, {FS: "hoh", TAXPAYER: "yes"}),
        ("D3b single, ODC-only child, taxpayer TIN not answered: blocks",
         {"demo-child-1": odc_child()}, {}, YES, {FS: "single"}),
        ("D4 joint, CTC child only, spouse TIN not answered: blocks (as v55)",
         {"demo-child-1": ctc_child()}, {}, YES, {FS: "mfj", TAXPAYER: "yes"}),
        ("D5 joint, no dependents, spouse TIN not answered: passes (not read)",
         {}, {}, YES, {FS: "mfj"}),
    ]


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        surface, package, release = build_surface(Path(tmp))
        for label, children, dependents, closed, facts in cases():
            acts = build_acts(children, dependents, package, release, return_facts=facts,
                              closed=closed)
            print(f"== {label}")
            print(summarize(run_case(surface, copy.deepcopy(acts), label[:2])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
