"""The field table and the consumer table of the sale families, read statically from a core.

Evidence for docs/phases/engine-breadth/milestones/sale-family-audit.md (P0).
Reads a package's members from packages/content/tax/2025 (or a scratch copy)
and writes tables-<version>.json beside this file. Imports no evidence module.

    python3 docs/phases/engine-breadth/milestones/sale-family-audit-evidence/tables.py [content-dir] [version]

Field table: for each field of each sale object, the members that read it.
A reader is a rule expression ``ref`` with that field, a family member
constraint over that field, or the engine's covered-flag refusal
(``packages/derivation/source_authority.py``), which reads
``basis_reported_to_irs`` on the four covered objects of the loader's map.

Row table: each amount row (a proceeds, basis or column (g) fact that is a
sale family's member, with no fields of its own) and the sale it must stand
beside. A row is tied to its sale by the package's loader companion
declaration (``packages/tax/loader.py`` presence pairs, ADR-0082): a row
recorded with no sale of its own on the same identity is refused. A row with
no pair is summed on its line whether or not its sale is recorded (review F1).

Consumer table: for each sale family, every consumer symbol that requires,
directly or through other rules, a symbol computed from that family (its
subtotals, count, gain, admission or amounts check), and each attachment
whose requirement reads such a symbol. Reach is transitive through every
``requires``, so it over-approximates where a family's amounts flow: a
family "reaches" a line whose rule only waits on, say, a check or a count
that rests on that family (review N3). It says what can block or change a
consumer, not which Schedule D line a sale is reported on.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Iterator

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
P = "tax.us.2025."
SALE_OBJECTS = tuple(P + name for name in (
    "f1099b.covered-st-txn", "f1099b.covered-lt-txn", "f1099b.covered-w-st-txn", "f1099b.covered-w-lt-txn",
    "f1099b.noncovered-st-txn", "f1099b.noncovered-lt-txn", "f8949.no1099b-st-txn", "f8949.no1099b-lt-txn",
    "f1099b.code-b-st-txn", "f1099b.code-b-lt-txn",
))
# The engine's covered-flag refusal (packages/tax/loader.py COVERED_FLAG_REFUSAL_OBJECTS,
# packages/derivation/source_authority.py) reads basis_reported_to_irs on these objects.
ENGINE_READS = {P + f"f1099b.covered-{k}-txn": ("basis_reported_to_irs",) for k in ("st", "lt", "w-st", "w-lt")}
CONSUMERS = tuple(P + s for s in (
    "schedule-d.line-1a-gain", "schedule-d.line-1b", "schedule-d.line-2", "schedule-d.line-3",
    "schedule-d.line-7", "schedule-d.line-8a-gain", "schedule-d.line-8b", "schedule-d.line-9",
    "schedule-d.line-10", "schedule-d.line-15", "schedule-d.line-16", "schedule-d.line-21",
    "capital-gains.line7a-total", "capital-gains.selected-preferential-base", "payments.line25b",
    "form8949.disposition", "schedule-d.disposition", "form1040.line7b-schedule-d-not-required",
))


def index(content: Path) -> dict[tuple[str, str], dict[str, Any]]:
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for path in content.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and "id" in body and "version" in body:
            out[(str(body["id"]), str(body["version"]))] = body
    return out


def walk(node: Any) -> Iterator[dict[str, Any]]:
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


def short(name: str) -> str:
    return name.removeprefix(P)


def members(content: Path, version: str) -> list[dict[str, Any]]:
    idx = index(content)
    package = json.loads((content / f"package.core-calculations.{version}.json").read_text(encoding="utf-8"))
    return [idx[(m["id"], m["version"])] | {"_role": m["role"]} for m in package["members"]]


def field_table(bodies: list[dict[str, Any]]) -> dict[str, Any]:
    facts: dict[str, dict[str, Any]] = {}
    for body in bodies:
        if body["_role"] == "fact-type-bundle":
            for fact in body["fact_types"]:
                facts[fact["id"]] = fact
    readers: dict[str, dict[str, set[str]]] = {}
    for body in bodies:
        name = f"{short(body['id'])} {body['version']}"
        if str(body.get("schema", "")).startswith("source-family"):
            subject = body["member_predicate"]["fact_type"]
            for constraint in body.get("member_constraints") or []:
                for node in walk(constraint["violated_when"]):
                    if "field" in node:
                        readers.setdefault(subject, {}).setdefault(node["field"], set()).add(
                            f"{name} constraint {constraint['block_code']}")
            continue
        for node in walk(body):
            if node.get("op") == "ref" and "field" in node:
                readers.setdefault(node["name"], {}).setdefault(node["field"], set()).add(name)
    table: dict[str, Any] = {}
    for obj in SALE_OBJECTS:
        props = facts[obj]["value_schema"]["properties"]
        row: dict[str, Any] = {}
        for field_name in props:
            found = sorted(readers.get(obj, {}).get(field_name, set()))
            if field_name in ENGINE_READS.get(obj, ()):
                found.append("engine covered-flag refusal (BASIS_NOT_REPORTED_ON_COVERED)")
            row[field_name] = found or "unread"
        table[short(obj)] = row
    return table


def row_table(bodies: list[dict[str, Any]], presence_pairs: dict[str, Any]) -> dict[str, Any]:
    """Each amount row of a sale object -> the sale its presence pair requires, or "unpaired"."""
    rows = sorted({str(b["member_predicate"]["fact_type"]) for b in bodies
                   if str(b.get("schema", "")).startswith("source-family")
                   and any(str(b["member_predicate"]["fact_type"]).startswith(obj + ".") for obj in SALE_OBJECTS)})
    table: dict[str, Any] = {}
    for row in rows:
        sale = row.rsplit(".", 1)[0]
        paired = presence_pairs.get(row)
        table[short(row)] = short(sale) if paired == sale or (isinstance(paired, list) and sale in paired) else "unpaired"
    return table


def row_audit(rows: dict[str, Any]) -> list[str]:
    return [f"{row} is not tied to its sale: a row with no sale of its own is summed on its line"
            for row, sale in rows.items() if sale == "unpaired"]


def loader_pairs(version: str) -> dict[str, Any]:
    """The presence pairs packages/tax/loader.py declares for core ``version`` (empty when it declares none)."""
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    from packages.tax.loader import domain_package_companion_declarations

    declaration = domain_package_companion_declarations().get((P + "package.core-calculations", version)) or {}
    return dict(declaration.get("presence_pairs") or {})


def produced_by(bodies: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Symbol published (or decided) -> the member that produces it, with what it requires."""
    out: dict[str, dict[str, Any]] = {}
    for body in bodies:
        symbol = body.get("publishes") or (body.get("subject") or {}).get("id") if body["_role"] in (
            "computation", "attachment-rule") else None
        if not symbol:
            continue
        requires = set(body.get("requires") or [])
        requirement = body.get("requirement") or {}
        requires |= set(requirement.get("subtotals") or [])
        for node in walk(body.get("value")):
            if node.get("op") in ("ref", "sum", "count") and isinstance(node.get("name"), str):
                requires.add(node["name"])
            if isinstance(node.get("source_set"), str):
                requires.add("family:" + node["source_set"])
        for node in walk(body.get("when")):
            if isinstance(node.get("source_set"), str):
                requires.add("family:" + node["source_set"])
        out[str(symbol)] = {"member": f"{short(body['id'])} {body['version']}", "requires": requires}
    return out


def consumer_table(bodies: list[dict[str, Any]]) -> dict[str, Any]:
    graph = produced_by(bodies)
    families = sorted(b["id"] for b in bodies if str(b.get("schema", "")).startswith("source-family")
                      and any(s in b["id"] for s in ("f1099b.", "f8949.")) and not b["id"].endswith(("-proceeds", "-basis", "-adjustment")))

    def touches(symbol: str, stem: str, seen: set[str]) -> bool:
        if symbol in seen:
            return False
        seen.add(symbol)
        if symbol.startswith("family:"):
            return symbol.removeprefix("family:").startswith(stem)
        node = graph.get(symbol)
        if node is None:
            return False
        if symbol.startswith(stem + "-") or symbol.startswith(stem + "."):
            return True
        return any(touches(r, stem, seen) for r in node["requires"])

    table: dict[str, Any] = {}
    for family in families:
        stem = family
        reached = [short(c) for c in CONSUMERS if touches(c, stem, set())]
        table[short(family)] = reached
    return table


# ---- the proposed committed audit test -----------------------------------------------
#
# Every field of every sale object is read by a rule (or the engine), or is
# listed here with why it cannot change the return. Every Form 1099-B box the
# records do not carry names the answer that refuses it, and that answer must be
# a fact the package declares. A new field, a removed reader, or a removed
# answer fails the check.

# Keyed by (sale object, field), so a new object's field of the same name is audited (review N1).
_BOX5 = ("Box 5. Form 8949 box A/D versus B/E follows whether basis was reported (box 12, the "
         "basis_reported_to_irs field the engine reads), not box 5 (i8949 lines 378-384).")
NO_EFFECT = {(f"f1099b.{kind}-txn", "covered_security"): _BOX5 for kind in ("covered-st", "covered-lt", "covered-w-st",
                                                                            "covered-w-lt")}
# Box 4 and box 7 are asked once per recorded Form 1099-B statement (Track 0
# repairs statement_box4 and statement_box7); the return-level answers P0
# proposed are not declared by the final v82.
REFUSED_BY = {
    "box 4 federal income tax withheld": ["f1099b.statement-box4-withholding-reported"],
    "box 7 loss not allowed": ["f1099b.statement-box7-loss-not-allowed"],
    "box 3 collectibles (box B/E, C/F, code B)": ["schedule-d-boundary.no-lines-18-19-sources"],
    "box 3 QOF (box B/E, C/F, code B)": ["schedule-d-boundary.no-1099da-or-qof"],
    # Review N2: Form 6781 reaches Schedule D lines 4 and 11, which this return does not compute; the unasked
    # boundary answer (Decision 5) refuses it. Box 13 (bartering) is not a sale on Schedule D and is parked.
    "boxes 8 to 11 section 1256 contracts (Form 6781)": ["schedule-d-boundary.no-other-schedule-d-sources"],
    "box 2 ordinary, box 1f market discount, box 6 gross proceeds (codes O, D, E)": [
        "schedule-d-boundary.no-other-form8949-adjustments", "schedule-d-boundary.noncovered-in-class",
        "schedule-d-boundary.form8949-in-class", "schedule-d-boundary.form8949-code-b-in-class"],
}


def read_by_rules(bodies: list[dict[str, Any]]) -> set[str]:
    """Every fact or symbol a rule reads: a ref, count, sum or collect name, or a require_paired witness."""
    out: set[str] = set()
    for body in bodies:
        if body["_role"] not in ("computation", "attachment-rule"):
            continue
        for node in walk(body):
            for key in ("name", "withholding"):
                if isinstance(node.get(key), str):
                    out.add(node[key])
    return out


def audit(bodies: list[dict[str, Any]], fields: dict[str, Any]) -> list[str]:
    declared = {fact["id"] for body in bodies if body["_role"] == "fact-type-bundle" for fact in body["fact_types"]}
    read = read_by_rules(bodies)
    failures = [f"{obj}.{name} is read by no rule and has no reason it cannot change the return"
                for obj, row in fields.items() for name, readers in row.items()
                if readers == "unread" and (obj, name) not in NO_EFFECT]
    failures += [f"{box}: the answer {fact} is not declared" for box, facts in REFUSED_BY.items()
                 for fact in facts if P + fact not in declared]
    failures += [f"{box}: no rule reads the answer {fact}" for box, facts in REFUSED_BY.items()
                 for fact in facts if P + fact in declared and P + fact not in read]
    return failures


# Every sale family's count must make Schedule D activity: both attachments (Form 8949
# except for the line 1a and 8a sales), the three rules that choose the Schedule D
# route, and Form 1040 line 7b ("Schedule D not required", review F2) read it.
COUNTS = {f"f1099b.{k}-{t}-count": k != "covered" for k in ("covered", "covered-w", "noncovered", "code-b")
          for t in ("st", "lt")} | {f"f8949.no1099b-{t}-count": True for t in ("st", "lt")}
ROUTE_READERS = ("tax.total-tax", "capital-gains.line7a-total", "capital-gains.selected-preferential-base",
                 "form1040.line7b-schedule-d-not-required")


def consumer_audit(bodies: list[dict[str, Any]]) -> list[str]:
    graph = produced_by(bodies)
    failures = []
    for symbol, on_8949 in COUNTS.items():
        if P + symbol not in graph:
            failures.append(f"{symbol}: no rule publishes the count")
            continue
        readers = ["schedule-d.disposition", *ROUTE_READERS] + (["form8949.disposition"] if on_8949 else [])
        failures += [f"{symbol} is not read by {reader}" for reader in readers
                     if P + symbol not in graph.get(P + reader, {}).get("requires", set())]
    return failures


def main() -> None:
    content = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "packages/content/tax/2025"
    version = sys.argv[2] if len(sys.argv) > 2 else "v81"
    bodies = members(content, version)
    fields = field_table(bodies)
    rows = row_table(bodies, loader_pairs(version))
    out = {"package": f"core-calculations {version}", "fields": fields, "rows": rows,
           "consumers": consumer_table(bodies),
           "consumers_are": "transitive reach through requires: what can block or change each consumer, not the "
                            "line a sale is reported on",
           "audit_failures": audit(bodies, fields) + row_audit(rows) + consumer_audit(bodies)}
    target = HERE / f"tables-{version}.json"
    target.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out["audit_failures"], indent=1))


if __name__ == "__main__":
    main()
