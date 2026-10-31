"""P0 probe -- do the 24 attachment known-gap source sets publish a partial amount on core v62?

For each source set in ``KNOWN_GAP_ATTACHMENTS`` this records one 1,000 member of the family
(by member-transition, the way a filer does, with any same-statement companion a refusal
names) on the committed core v62 / registry v60 / release v60 and runs it through
``live_coordinate_run`` with the collect-closure tests' own helpers:

* unanswered -- the member, the family's closure left unanswered;
* answered   -- the same member, the closure attested true at its horizon (the control:
  what a confirmed-complete family publishes).

Some attachments are only *required* by another source set (Schedule D by 1099-B proceeds,
Form 8949 by wash-sale proceeds, Schedule 1 by unemployment compensation, Schedule B by
interest above the threshold). For those sets the probe runs a second variant, ``with_trigger``,
in which a trigger family is recorded and closed first so the attachment is required, and the
set under test is the only unconfirmed family. Wash-sale variants also answer the Form 8949
Part III boundary question ("no other adjustments") so Form 8949 can publish.

For each of the four attachments it records whether the disposition publishes, the row sets
it itemizes (row sum and subtotal), or the block that stops it.

Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/attachment-closure-evidence/probe.py [source-set ...]

With arguments the named sets are run and merged into ``probe-output.json``. Synthetic
``demo.*`` data only; nothing here edits repository content.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from packages.kernel.facts import fact_id_for  # noqa: E402
from tests.test_collect_closure import (  # noqa: E402
    P,
    Result,
    _adopt,
    _base_return,
    _gap_return,
    _package_index,
    _run,
)
from tests.test_collect_closure_regression import KNOWN_GAP_ATTACHMENTS  # noqa: E402
from tests.test_form_1099_withholding import YEAR, _add, _assert, _close, _introduce  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _attested  # noqa: E402
from tests.test_withholding_closure import _horizons, _strip_closure  # noqa: E402

ATTACHMENTS = {
    "schedule-d": "schedule-d.disposition",
    "form8949": "form8949.disposition",
    "schedule-1": "schedule1.disposition",
    "schedule-b": "scheduleb.disposition",
}
ATTACHMENT_RULES = {P + "rule.attachment." + k for k in ("schedule-d", "f8949", "schedule-1", "schedule-b")}

# set under test -> (trigger family, trigger amount): a closed family that makes the
# attachment required, so the set under test is the only unconfirmed family.
TRIGGERS: dict[str, tuple[str, float]] = {
    "f1099b.covered-lt-basis": ("f1099b.covered-lt-proceeds", 1000.0),
    "f1099b.covered-st-basis": ("f1099b.covered-st-proceeds", 1000.0),
    "f1099b.covered-w-lt-basis": ("f1099b.covered-w-lt-proceeds", 1000.0),
    "f1099b.covered-w-lt-adjustment": ("f1099b.covered-w-lt-proceeds", 1000.0),
    "f1099b.covered-w-st-basis": ("f1099b.covered-w-st-proceeds", 1000.0),
    "f1099b.covered-w-st-adjustment": ("f1099b.covered-w-st-proceeds", 1000.0),
    "f1098e.1": ("f1099g.1", 1000.0),
    "f1099k": ("f1099g.1", 1000.0),
    "scheduleb.adjustment.nominee": ("f1099int.b1", 2000.0),
    "scheduleb.adjustment.abp-adjustment": ("f1099int.b1", 2000.0),
}
WASH = ("f1099b.covered-w-",)
# A base "none" declaration the member would contradict: flipped (the rule reading it).
FLIPS = {P + "f1099int.b8": (P + "line2a-scope.no-f1099int-tax-exempt", "no")}


def _pick(schema: dict[str, Any], amount: Any) -> Any:
    if "const" in schema:
        return schema["const"]
    for branch in schema.get("anyOf", []):
        if "const" in branch and branch["const"] is not None:
            return branch["const"]
    if "enum" in schema:
        return schema["enum"][0]
    return amount if schema.get("type") == "number" else "demo"


def _flip(acts: list[dict[str, object]], family: str) -> None:
    if family not in FLIPS:
        return
    flip_type, flip_value = FLIPS[family]
    for act in acts:
        finding = act["payload"].get("finding") if isinstance(act["payload"], dict) else None  # type: ignore[union-attr]
        if finding and str(finding.get("fact_id", "")).startswith(flip_type + "|"):
            finding["value"] = flip_value


def add_member(acts: list[dict[str, object]], family: str, value: float, *, close: bool, tag: str,
               companions: tuple[tuple[str, tuple[tuple[str, str], ...]], ...] = ()) -> list[dict[str, object]]:
    """``test_collect_closure._add_member`` plus same-statement companions asserted first."""
    families, mappings, fact_types, _ = _package_index()
    fam, mapping = families[family], mappings[family]
    ftype = fact_types[fam["member_predicate"]["fact_type"]]
    out = _strip_closure(acts, mapping["closure_fact_type"]["id"])
    _flip(out, family)
    _adopt(out, ftype["id"])
    _adopt(out, mapping["closure_fact_type"]["id"])
    horizons = _horizons(out, family)
    if not horizons:
        genesis = f"demo.ac.{tag}.g0"
        _add(out, "horizon-genesis", {"family": {"id": family, "version": fam["version"]},
                                      "scope": {"tax-year": YEAR, "subject": "demo.primary"}, "horizon_id": genesis})
        horizons = [genesis]
    declared: list[tuple[str, str]] = []
    for key in ftype["identity_keys"]:
        if key["kind"] == "entity":
            eid = f"demo.ac.{tag}.{key['name']}"
            _introduce(out, eid, key["entity_kind"])
            declared.append((key["name"], eid))
        else:
            declared.append((key["name"], key["values"][0]))
    for n, (ctype, ckeys) in enumerate(companions):
        _assert(out, f"demo.ac.{tag}.companion.{n}", ctype, ckeys, _pick(fact_types[ctype]["value_schema"], value))
    new = f"demo.ac.{tag}.h1"
    _add(out, "member-transition", {
        "family": {"id": family, "version": fam["version"]},
        "scope": {"tax-year": YEAR, "subject": "demo.primary"},
        "member": {"action": "assert", "finding": _attested(f"demo.ac.{tag}.member", fact_id_for(ftype["id"], tuple(declared)), value)},
        "successor": {"id": new, "predecessor": horizons[-1]},
    })
    if close:
        _close(out, mapping["closure_fact_type"]["id"], new, f"demo.ac.{tag}.closure")
    return out


def _boundary_form8949(acts: list[dict[str, object]]) -> None:
    """The Form 8949 Part III answer a wash-sale return needs for Form 8949 to publish."""
    _, _, _, bundles = _package_index()
    ftid = P + "schedule-d-boundary.no-other-form8949-adjustments"
    _adopt(acts, ftid)
    _assert(acts, "demo.ac.boundary.8949", ftid, (), "yes")


def build(family: str, value: float, *, close: bool, trigger: tuple[str, float] | None,
          companions: list[tuple[str, tuple[tuple[str, str], ...]]]) -> list[dict[str, object]]:
    short = family.replace(P, "")
    tag = short.replace(".", "-")
    if trigger is None and not short.startswith(WASH):
        if short in ("f1099r.ira-fully-taxable", "ssa1099.benefits"):
            return _gap_return(family, close=close)
        return add_member(_base_return(), family, value, close=close, tag=tag, companions=tuple(companions))
    acts = _base_return()
    if short.startswith(WASH):
        _boundary_form8949(acts)
    if trigger is not None:
        acts = add_member(acts, trigger[0], trigger[1], close=True, tag="t" + trigger[0].replace(P, "").replace(".", "-"))
    return add_member(acts, family, value, close=close, tag=tag, companions=tuple(companions))


def summarize(result: Result) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name, sym in ATTACHMENTS.items():
        pub = result.pubs.get(P + sym)
        if pub is None:
            out[name] = {"published": False}
            continue
        parts = []
        for part in pub["value"]["itemizations"]:
            for rs in part["row_sets"]:
                if float(rs["row_sum"]) != 0 or float(rs["subtotal"]["value"]) != 0:
                    parts.append({
                        "part": part["part_id"],
                        "source_set": rs["source_family"]["id"].replace(P, ""),
                        "rows": len(rs["rows"]),
                        "row_sum": rs["row_sum"],
                        "subtotal": rs["subtotal"]["value"],
                    })
            for adj in part.get("adjustment_rows", []):
                if float(adj["row_sum"]) != 0:
                    parts.append({"part": part["part_id"], "adjustment": adj["kind"], "rows": len(adj["rows"]),
                                  "row_sum": adj["row_sum"], "subtotal": adj["subtotal"]["value"]})
        out[name] = {"published": True, "nonzero_row_sets": parts}
    out["attachment_blocks"] = sorted(
        (str(r["artifact_id"]).replace(P, ""), r["code"], [str(m).replace(P, "") for m in r["missing"]])
        for r in result.blocked if r["artifact_id"] in ATTACHMENT_RULES
    )
    out["source_set_unclosed_blocks"] = sorted(
        (str(r["artifact_id"]).replace(P, ""), [str(m).replace(P, "") for m in r["missing"]])
        for r in result.blocked if r["code"] == "SOURCE_SET_UNCLOSED"
    )
    out["other_publishes"] = {
        k: result.value(k) for k in ("interest.taxable-total", "income.agi", "schedule-d.line-8a-gain",
                                      "schedule-d.line-1a-gain", "dividends.1a-subtotal", "unemployment.box1-subtotal")
        if result.has(k)
    }
    return out


def variant(family: str, trigger: tuple[str, float] | None, core: str = "v62") -> dict[str, Any]:
    entry: dict[str, Any] = {}
    tag = family.replace(P, "").replace(".", "-")
    for label, closed in (("unanswered", False), ("answered", True)):
        companions: list[tuple[str, tuple[tuple[str, str], ...]]] = []
        for _ in range(6):
            try:
                acts = build(family, 1000.0, close=closed, trigger=trigger, companions=companions)
                reconfirm = closed or family != P + "ssa1099.benefits"
                result = _run(acts, f"demo.ac.{tag}.{label[0]}{'t' if trigger else ''}", core, reconfirm=reconfirm)
                entry[label] = summarize(result)
                entry[label]["values_sha256"] = hashlib.sha256(json.dumps(result.values, sort_keys=True, default=str).encode()).hexdigest()
                entry[label]["values_count"] = len(result.values)
                if companions:
                    entry[label]["companions_added"] = [c[0].replace(P, "") for c in companions]
                break
            except Exception as exc:  # recorded, not hidden
                match = re.search(r"companion presence violated: .*? but (\S+?)\|(\S+) has no current value", str(exc))
                if match:
                    pairs = tuple((kv.split("=")[0], kv.split("=")[1]) for kv in match.group(2).split(",") if not kv.startswith("tax-year="))
                    companions.append((match.group(1), pairs))
                    continue
                entry[label] = {"error": f"{type(exc).__name__}: {str(exc)[:300]}"}
                break
    return entry


def probe(family: str, core: str = "v62") -> dict[str, Any]:
    short = family.replace(P, "")
    out = {"alone": variant(family, None, core)}
    if short in TRIGGERS:
        trig = TRIGGERS[short]
        out["with_trigger"] = {"trigger": trig[0], **variant(family, (P + trig[0], trig[1]), core)}
    return out


def main() -> None:
    target = Path(__file__).with_name("probe-output.json")
    wanted = [P + a if not a.startswith(P) else a for a in sys.argv[1:]] or sorted(KNOWN_GAP_ATTACHMENTS)
    out = json.loads(target.read_text()) if sys.argv[1:] and target.exists() else {"core": "v62", "sets": {}}
    for family in wanted:
        out["sets"][family.replace(P, "")] = probe(family)
        print("done", family, file=sys.stderr)
        target.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
