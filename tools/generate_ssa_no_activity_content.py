"""Generate the SSA no-activity applicability repair content set (Milestone 1).

**Single producer.** A two-producer split was drafted and withdrawn before any
version of it was committed to the ratified line: `tax.us.2025.social-
security.line6b` is form-field-bound, and `presentation_projection._one_row`
admits exactly one disposition row per form-field-bound symbol, while two
producers always yield two rows in every reachable state (see the milestone
plan's "Track 1 stop report" and "Reopened Track 0 prototype evidence"). The
shipped design is one successor rule that is the sole producer of the symbol:

``rule.ss-benefits-worksheet`` ``v2`` under ``rule-artifact.v4``:

* **unconditional** ``requires`` — ``social-security.line6a``,
  ``rounding.convention``, ``no-rrb-or-foreign-social-benefit``,
  ``filing_status`` and the seven numeric worksheet inputs.  The other 22
  ``ss-benefits-scope`` declarations leave ``requires`` entirely.

  The seven numeric inputs stay because `requires` is the only sequencing gate
  the scheduler consults and they are *derived* symbols; see
  ``build_single_producer``'s comment on the point and the milestone plan's
  reopened Track 0 evidence.  Requiring them unconditionally
  costs a wageless return almost nothing: each is itself an unconditional
  total rule publishing zero over an empty closed family, and six of the
  seven are already required unconditionally by ``rule.form1040-line9`` to
  reach total income.  The seventh, ``tax-exempt-interest.line2a-total``, is
  not: line 2a is informational, not part of total income, and line9 does not
  require it.  Requiring it here does pull in ``rule.form1040-line2a``'s
  eight ``line2a-scope.*`` declarations for a return that would otherwise
  skip them, but that cost is pre-existing, not introduced by this rule:
  worksheet ``v1`` already required ``tax-exempt-interest.line2a-total``
  among its 33 ``requires``.

  ``filing_status`` is unconditional rather than conditional for a contract
  reason, not a convenience one: ADR-0038 production condition 1, enforced by
  ``package_validation`` check 10a, forbids a ``conditional_dependency_set``
  member whose fact type the same rule also names in a ``category_literal``
  unless that fact type declares the ``{yes, no}`` domain.  This rule's MFS
  branch names ``tax.us.2025.filing-status`` in a ``category_literal`` and that
  fact type's domain is the five filing statuses, so ``filing_status`` cannot
  legally be a conditional member.  It is also not one of "the worksheet's
  remaining numeric inputs" the settlement moves.
* **unconditional guard** — ``require_closed`` on the current SSA-1099 family
  (both routes), and ``no-rrb-or-foreign-social-benefit == "yes"`` (both
  routes: it supplies the source-universe authority the narrow family closure
  disclaims).
* **conditional dependency set** (ADR-0037) — the other **22** declarations,
  activated only when ``count(box5-net-benefits) > 0``, so a nonempty route
  missing several of them reports the complete missing list in one walk, and a
  closed-empty route neither reads nor pins any of them.  No vocabulary
  successor is needed: check 10a recognizes ``{"type": "string", "enum":
  ["yes", "no"]}`` (the ``ss-benefits-scope`` fact types' actual, unchanged
  spelling) as the same closed domain as ``{"enum": ["yes", "no"]}``, so these
  22 declarations stay at their base ``v1``.
* **conditional guard branch** — ``any[count == 0, all[22 conjuncts, MFS set]]``
  short-circuits on the closed-empty route, so the 22 categorical conjuncts and
  the MFS living-arrangement conditional set are evaluated only when nonempty.
* **value** — ``choose(count == 0 -> 0, else -> the v1 worksheet expression
  byte-identical)``. ``choose`` is lazy in the committed evaluator, so the
  closed-empty route never reads an income symbol, a parameter, or ``round``.

No existing citizen bytes are rewritten in place: ``rule.ss-benefits-
worksheet.json`` (v1) remains untouched on disk and simply stops being a
package member, mirroring this corpus's established successor-version
precedent (``rule.form1040-line15`` v1 -> v2 at v29). The schema moves
``rule-artifact.v3`` -> ``v4`` because ``count`` is not in the v3 grammar;
v4 is v3's grammar plus ``count``/``block`` and retains
``conditional_dependency_set``.

Publication generation: ``package.core-calculations`` v30 (the lowest free
version after the ratified line's v29), ``published-packages`` v25, release
v23, ``adopt-core-v30-current``, admitting worksheet v2. All are the lowest
versions free on the ratified line at the time this milestone built them.
``ss-benefits-scope`` stays at its base v1 throughout - no vocabulary
successor is a member of this package.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
FIXTURES = ROOT / "packages" / "sample_data" / "ssa1099_benefits_line6"

SSA_FAMILY = "tax.us.2025.ssa1099.benefits"
BOX5 = "tax.us.2025.ssa1099.box5-net-benefits"
LINE6B = "tax.us.2025.social-security.line6b"
NO_RRB = "tax.us.2025.ss-benefits-scope.no-rrb-or-foreign-social-benefit"
SCOPE_PREFIX = "tax.us.2025.ss-benefits-scope."
LINE6A = "tax.us.2025.social-security.line6a"
# Unconditional on every publication path, scope declarations aside.
UNCONDITIONAL_NON_SCOPE = (LINE6A, "rounding.convention", "filing_status")

WORKSHEET_FILE = "rule.ss-benefits-worksheet.json"
SUCCESSOR_FILE = "rule.ss-benefits-worksheet.v2.json"

BASE_PACKAGE_FILE = "package.core-calculations.v29.json"
PACKAGE_FILE = "package.core-calculations.v30.json"
BASE_REGISTRY_FILE = "published-packages.v24.json"
REGISTRY_FILE = "published-packages.v25.json"
RELEASE_FILE = "demo.release.2025.v23.json"
ADOPTION_FILE = "adopt-core-v30-current.json"


def _bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _load(name: str) -> dict[str, Any]:
    value = json.loads((CONTENT / name).read_text("utf-8"))
    assert isinstance(value, dict)
    return value


def _checksum(value: dict[str, Any]) -> str:
    body = {key: item for key, item in value.items() if key != "package_checksum"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _citizen_checksum(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _count_expr() -> dict[str, Any]:
    """count(box5-net-benefits) over the SSA-1099 benefits family.

    Every discriminating occurrence - the conditional dependency set's
    condition, the guard's empty branch and the value's branch - is built from
    this one helper, so the family id, the member fact type and the counted
    source set cannot drift apart between them.
    """
    return {"op": "count", "name": BOX5, "source_set": SSA_FAMILY}


def _is_empty() -> dict[str, Any]:
    return {"op": "compare", "cmp": "eq", "left": _count_expr(), "right": 0}


def _is_nonempty() -> dict[str, Any]:
    return {"op": "compare", "cmp": "gt", "left": _count_expr(), "right": 0}


def _conjunct_symbol(node: dict[str, Any]) -> str | None:
    """The declaration a v1 `when` categorical conjunct tests, if any."""
    if node.get("op") != "categorical_compare":
        return None
    left = node.get("left")
    if isinstance(left, dict) and left.get("op") == "ref":
        return str(left["name"])
    return None


def build_single_producer() -> dict[str, Any]:
    """rule.ss-benefits-worksheet v2 - the sole producer of line 6b."""
    rule = _load(WORKSHEET_FILE)
    assert rule["schema"] == "rule-artifact.v3"
    assert rule["version"] == "v1"
    assert rule["publishes"] == LINE6B

    v1_when_args = list(rule["when"]["args"])
    assert rule["when"]["op"] == "all"

    declaration_conjuncts = [
        node for node in v1_when_args if _conjunct_symbol(node) is not None
    ]
    other_nodes = [node for node in v1_when_args if _conjunct_symbol(node) is None]
    assert len(declaration_conjuncts) == 23, len(declaration_conjuncts)
    # The one node that is not a declaration conjunct is v1's MFS
    # living-arrangement conditional dependency set.
    assert len(other_nodes) == 1 and other_nodes[0]["op"] == "conditional_dependency_set"
    mfs_node = other_nodes[0]

    retained = [
        node for node in declaration_conjuncts if _conjunct_symbol(node) == NO_RRB
    ]
    worksheet_only = [
        node for node in declaration_conjuncts if _conjunct_symbol(node) != NO_RRB
    ]
    assert len(retained) == 1 and len(worksheet_only) == 22

    # `requires` keeps only what is unconditional for *every* publication path
    # this rule has: the closed-empty zero's own authority (line 6a, the
    # retained source-universe declaration, the rounding convention) plus
    # filing_status, which ADR-0038 production condition 1 forbids as a
    # conditional member (see the module docstring).  The 22 worksheet-only
    # declarations leave `requires` and become ADR-0037 conditional members.
    #
    # The seven numeric worksheet inputs stay in `requires`. Moving them into
    # the conditional set does not work on committed scheduler semantics:
    # `requires` is the only sequencing gate `_Run.is_eligible` consults, and
    # `_record_blocked` resolves a rule permanently, so a rule whose derived
    # dependency is read only inside `when` fires the first pass it is
    # eligible - before the rules that publish that dependency have run -
    # and is then blocked for the rest of the run. ADR-0037 conditional
    # members are safe for *asserted input* facts (present from revision
    # zero) such as the 22 declarations, and unsafe for *derived* symbols.
    # Measured directly on the published citizen by
    # `test_conditionalizing_the_numeric_inputs_breaks_the_nonempty_route`.
    unconditional_numeric = [
        symbol
        for symbol in rule["requires"]
        if not symbol.startswith(SCOPE_PREFIX) and symbol not in UNCONDITIONAL_NON_SCOPE
    ]
    assert len(unconditional_numeric) == 7, unconditional_numeric
    conditional_numeric: list[str] = []
    unconditional_requires = [
        symbol
        for symbol in rule["requires"]
        if symbol in UNCONDITIONAL_NON_SCOPE
        or symbol == NO_RRB
        or symbol in unconditional_numeric
    ]
    conditional_members = [
        _conjunct_symbol(node) for node in worksheet_only
    ] + conditional_numeric
    assert len(conditional_members) == 22 + len(conditional_numeric)

    rule["schema"] = "rule-artifact.v4"
    rule["version"] = "v2"
    rule["requires"] = unconditional_requires
    rule["blocked"] = {
        "code": "DEPENDENCY_ABSENT",
        "missing": list(unconditional_requires),
    }
    rule["when"] = {
        "op": "all",
        "args": [
            # 1. Closure of the current SSA family, on both routes. Ordered
            #    first so an unclosed family blocks SOURCE_SET_UNCLOSED having
            #    genuinely consulted closure state, before any declaration is
            #    read.
            {"op": "require_closed", "source_set": SSA_FAMILY},
            # 2. ADR-0037: activate and completely report the 22 worksheet-only
            #    declarations and the seven numeric worksheet inputs, and only
            #    when the family is nonempty. Ordered ahead of the categorical
            #    conjuncts so a nonempty route missing several of them names
            #    every one in a single walk instead of stopping at the first.
            {
                "op": "conditional_dependency_set",
                "condition": _is_nonempty(),
                "members": [{"op": "ref", "name": name} for name in conditional_members],
            },
            # 3. The retained source-universe declaration, on both routes.
            retained[0],
            # 4. The worksheet-only scope test, active only when nonempty.
            #    `any` short-circuits on the first true argument, so on the
            #    closed-empty route the 22 conjuncts and the MFS conditional
            #    set are never evaluated and therefore never pinned.
            {
                "op": "any",
                "args": [
                    _is_empty(),
                    {"op": "all", "args": [*worksheet_only, mfs_node]},
                ],
            },
        ],
    }
    rule["value"] = {
        "op": "choose",
        "when": _is_empty(),
        "then": 0,
        "else": rule["value"],
    }
    rule["notes"] = (
        rule["notes"]
        + " One rule, one producer, two declared routes. Form 1040 line 6b must not"
        " publish until the current SSA-1099 source family has been confirmed complete:"
        " the worksheet computes the taxable portion of the benefits actually recorded,"
        " so a return whose benefit set is not yet closed has no line 6b answer to give,"
        " empty or otherwise. That is why require_closed is unconditional here. Once the"
        " family is closed the two routes are decided by count over the family's own"
        " member fact type. On the count == 0 route the authority for the published zero"
        " is the closure attestation taken together with zero current members - never"
        " mere emptiness - plus no-rrb-or-foreign-social-benefit, the return's only"
        " committed statement that Form 1040 line 6's universe and this narrow statement"
        " family coincide; without it a zero here would substitute a narrow family's"
        " closure for a broader line's authority. The zero-member component has no"
        " finding of its own and is carried by the absence of any member pin together"
        " with the pinned version of this rule, whose value branch demands count == 0."
        " The other 22 scope declarations are worksheet-internal: at line 6a = 0 the"
        " worksheet's own value reduces to zero for every filing status and every income"
        " vector, so they cannot change the answer and must not gate it. Those 22 symbols,"
        " and only those 22, are therefore an ADR-0037 conditional dependency set"
        " conditioned on count > 0, which both activates them and reports all of them at"
        " once when the nonempty route is short of several. The seven numeric worksheet"
        " inputs are NOT in that set and stay unconditional, which is a sequencing"
        " requirement rather than a claim that the empty route reads them: on the"
        " count == 0 route choose never evaluates the worksheet expression, so wages,"
        " taxable interest, ordinary dividends, IRA distributions, capital gains,"
        " additional income and tax-exempt interest are indeed neither read nor pinned."
        " But requires is the engine's only sequencing gate - eligibility consults it"
        " alone, conditional-set membership is invisible to it, and a blocked rule"
        " resolves permanently - so moving them behind the condition would make this rule"
        " eligible before the rules publishing those symbols have run, permanently"
        " blocking the nonempty route on DEPENDENCY_ABSENT. Requiring them"
        " unconditionally costs a wageless return almost nothing: each of the seven is"
        " itself an unconditional total rule that publishes zero over an empty closed"
        " family, and six of the seven are already required unconditionally by"
        " rule.form1040-line9 to reach total income. The seventh,"
        " tax-exempt-interest.line2a-total, is not: line 2a is informational, not part"
        " of total income, and line9 does not require it. Requiring it here does pull in"
        " rule.form1040-line2a's eight line2a-scope.* declarations for a return that"
        " would otherwise skip them - measured: dropping those eight facts from a"
        " closed-empty run blocks this rule on DEPENDENCY_ABSENT naming"
        " tax-exempt-interest.line2a-total. That cost is pre-existing, not introduced by"
        " this rule: v1 of this worksheet already required tax-exempt-interest.line2a-"
        "total among its 33 requires, so no return that could previously reach a"
        " published line 6b answer is newly burdened here."
        " filing_status stays unconditional: ADR-0038"
        " production condition 1 forbids a conditional member whose fact type this same"
        " rule names in a category_literal unless that fact type declares the {yes, no}"
        " domain, and tax.us.2025.filing-status declares the five filing statuses."
        " On the count > 0 route the value expression, the"
        " pin table, the citations and the 22 conjuncts plus the MFS living-arrangement"
        " set are exactly v1's, so the published worksheet value is unchanged; its"
        " provenance additionally pins the closure mapping, the family declaration and"
        " the current closure finding. This is a decision about what this worksheet"
        " means, scoped to this route; it is not a change to collect semantics and not a"
        " statement that any other nonempty family requires closure. The schema moves"
        " rule-artifact.v3 -> v4 because count is not in the v3 grammar; v4 is v3's"
        " grammar plus count/block and retains conditional_dependency_set."
    )
    return rule


def _member_pin(citizen: dict[str, Any]) -> dict[str, Any]:
    schema = citizen["schema"]
    assert schema.startswith("rule-artifact."), schema
    return {
        "id": citizen["id"],
        "role": citizen["role"],
        "schema": schema,
        "version": citizen["version"],
    }


_NEW_MEMBER_FILES = (SUCCESSOR_FILE,)


def build_package(citizens: dict[str, dict[str, Any]]) -> dict[str, Any]:
    package = _load(BASE_PACKAGE_FILE)
    package["schema"] = "artifact-package.v22"
    package["version"] = "v30"

    # Swap in only the worksheet successor. The ss-benefits-scope vocabulary
    # stays at its base v1: package_validation check 10a now recognizes v1's
    # {"type": "string", "enum": ["yes", "no"]} spelling as the same closed
    # domain as {"enum": ["yes", "no"]}, so no vocabulary successor - and no
    # version mismatch between the worksheet's v1 category_literal pins and
    # the package's selected fact surface - is needed.
    members = [
        dict(member)
        for member in package["members"]
        if member["id"] != "tax.us.2025.rule.ss-benefits-worksheet"
    ]
    members.append(_member_pin(citizens[SUCCESSOR_FILE]))
    package["members"] = sorted(members, key=lambda m: (m["id"], m["version"]))

    entrypoints = [
        dict(entry)
        for entry in package["entrypoints"]
        if entry["id"] != "tax.us.2025.rule.ss-benefits-worksheet"
    ]
    entrypoints.append({"id": "tax.us.2025.rule.ss-benefits-worksheet", "version": "v2"})
    package["entrypoints"] = [
        {"id": eid, "version": ver}
        for eid, ver in sorted({(e["id"], e["version"]) for e in entrypoints})
    ]

    # line 6b keeps exactly one producer, so no conflict_semantics entry is
    # added: there is no conflict to name and no presentation join to widen.
    package["package_checksum"] = _checksum(package)
    return package


def build_registry(package: dict[str, Any], citizens: dict[str, dict[str, Any]]) -> dict[str, Any]:
    registry = _load(BASE_REGISTRY_FILE)
    citizen_entries = [dict(entry) for entry in registry["citizens"]]
    for name in _NEW_MEMBER_FILES:
        citizen = citizens[name]
        key = (citizen["id"], citizen["version"])
        citizen_entries = [e for e in citizen_entries if (e["id"], e["version"]) != key]
        citizen_entries.append(
            {
                "id": citizen["id"],
                "version": citizen["version"],
                "checksum": _citizen_checksum(citizen),
            }
        )
    registry["citizens"] = sorted(citizen_entries, key=lambda e: (e["id"], e["version"]))

    package_entries = [dict(entry) for entry in registry["packages"]]
    package_entries.append(
        {
            "id": package["id"],
            "version": package["version"],
            "checksum": package["package_checksum"],
        }
    )
    registry["packages"] = sorted(package_entries, key=lambda e: (e["id"], e["version"]))
    return registry


def build_release(registry_bytes: bytes) -> dict[str, Any]:
    return {
        "schema": "release-registry.v1",
        "id": "demo.release.2025",
        "version": "v23",
        "package_registry_sha256": hashlib.sha256(registry_bytes).hexdigest(),
    }


def build_adoption(
    package: dict[str, Any], registry: dict[str, Any], release: dict[str, Any], release_bytes: bytes
) -> dict[str, Any]:
    package_entry = next(
        e
        for e in registry["packages"]
        if e["id"] == package["id"] and e["version"] == package["version"]
    )
    return {
        "schema": "act.v1",
        "act_id": "demo.act.adopt.core.v30",
        "kind": "package-adoption",
        "actor": "demo.user.filer-1",
        "at": "2026-08-10T12:00:00Z",
        "committed_against": 0,
        "payload": {
            "package": {
                "id": package["id"],
                "version": package["version"],
                "checksum": package_entry["checksum"],
            },
            "release": {
                "id": release["id"],
                "version": release["version"],
                "checksum": hashlib.sha256(release_bytes).hexdigest(),
            },
            "scope": {"jurisdiction": "us", "year": "2025"},
            "revision": 30,
            "audit": {
                "note": "synthetic SSA no-activity applicability adoption; non-authoritative"
            },
        },
    }


def render_all(
    content_dir: Path | None = None,
    fixtures_dir: Path | None = None,
) -> dict[Path, bytes]:
    content = CONTENT if content_dir is None else content_dir
    fixtures = FIXTURES if fixtures_dir is None else fixtures_dir
    citizens = {
        SUCCESSOR_FILE: build_single_producer(),
    }
    package = build_package(citizens)
    registry = build_registry(package, citizens)

    out: dict[Path, bytes] = {
        content / name: _bytes(citizen) for name, citizen in citizens.items()
    }
    out[content / PACKAGE_FILE] = _bytes(package)
    out[content / REGISTRY_FILE] = _bytes(registry)

    registry_bytes = out[content / REGISTRY_FILE]
    release = build_release(registry_bytes)
    release_bytes = _bytes(release)
    adoption = build_adoption(package, registry, release, release_bytes)

    out[fixtures / "publication_surface" / "releases" / RELEASE_FILE] = release_bytes
    out[fixtures / "adoptions" / ADOPTION_FILE] = _bytes(adoption)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--content-dir",
        type=Path,
        default=None,
        help="render the content citizens into this directory instead of the repo tree",
    )
    parser.add_argument(
        "--fixtures-dir",
        type=Path,
        default=None,
        help="render the release/adoption fixtures into this directory instead of the repo tree",
    )
    args = parser.parse_args()
    for path, body in render_all(args.content_dir, args.fixtures_dir).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)


if __name__ == "__main__":
    main()
