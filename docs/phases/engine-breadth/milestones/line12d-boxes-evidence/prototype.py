"""Scratch core v90: Form 1040 line 12d's four boxes are form fields.

Evidence for docs/phases/engine-breadth/milestones/line12d-boxes.md.
Charter: docs/reviews/line12d-boxes/charter-p0.md.

Builds a scratch core v90 on published v89 in a directory outside the
repository. Does not edit packages/. Each box is the line 6d pair: a rule
that publishes 'checked' when the instructions check it, a sibling that
publishes 'not_checked' when they leave it empty, and two form-field.v3
citizens bound to those symbols. Spouse boxes are inapplicable on every
status other than a joint return, or a separate return whose condition
fact is yes.

    python3 prototype.py <scratch-directory-outside-the-repo>
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.package_successor import generate_to_directory  # noqa: E402

P = "tax.us.2025."
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"
FROM = {"package": "v89", "registry": "v87", "release": "v87"}
TO = {"package": "v90", "registry": "v88", "release": "v88"}
MFJ = "married_filing_jointly"
MFS = "married_filing_separately"
COND = "spouse_separate_condition"
CITATION = P + "citation.form1040.line-12d"

# Four boxes. Spouse boxes follow line 12d: joint, or separate with the
# condition fact yes. Head of household, qualifying surviving spouse and
# single never show them.
BOXES: tuple[dict[str, str], ...] = (
    {
        "key": "you_age",
        "slug": "you-age",
        "symbol": "taxpayer_over_65",
        "fact": P + "taxpayer-over-65",
        "label": "You were born before January 2, 1961",
        "line": "12d-you-born-before-1961",
        "who": "you",
    },
    {
        "key": "you_blind",
        "slug": "you-blind",
        "symbol": "taxpayer_blind",
        "fact": P + "taxpayer-blind",
        "label": "You are blind",
        "line": "12d-you-blind",
        "who": "you",
    },
    {
        "key": "spouse_age",
        "slug": "spouse-age",
        "symbol": "spouse_over_65",
        "fact": P + "spouse-over-65",
        "label": "Spouse was born before January 2, 1961",
        "line": "12d-spouse-born-before-1961",
        "who": "spouse",
    },
    {
        "key": "spouse_blind",
        "slug": "spouse-blind",
        "symbol": "spouse_blind",
        "fact": P + "spouse-blind",
        "label": "Spouse is blind",
        "line": "12d-spouse-blind",
        "who": "spouse",
    },
)


def _ref(name: str) -> dict[str, Any]:
    return {"op": "ref", "name": name}


def _cds(names: list[str], condition: Any = True) -> dict[str, Any]:
    return {
        "op": "conditional_dependency_set",
        "condition": condition,
        "members": [_ref(name) for name in names],
    }


def _status_is(value: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare",
        "cmp": "eq",
        "left": _ref("filing_status"),
        "right": {
            "op": "category_literal",
            "fact_type": {"id": P + "filing-status", "version": "v1"},
            "value": value,
        },
    }


def _pin(fact_id: str) -> dict[str, str]:
    return {"role": "input", "id": fact_id, "version": "v1", "origin": "assertion"}


def _scope() -> dict[str, Any]:
    return {"family": "individual-income-tax", "jurisdiction": "US-federal", "tax_year": 2025}


def spouse_when(symbol: str, *, checked: bool) -> dict[str, Any]:
    """Publish only where the 2025 instructions check a spouse box.

    Joint: read the spouse fact. Separate: read the condition first, then
    the spouse fact only when that condition is yes. Every other status is
    inapplicable without reading a spouse fact.
    """
    bit = _ref(symbol) if checked else {"op": "not", "value": _ref(symbol)}
    joint = {"op": "all", "args": [_cds([symbol]), bit]}
    separate_yes = {
        "op": "choose",
        "when": {"op": "all", "args": [_cds([COND]), _ref(COND)]},
        "then": {"op": "all", "args": [_cds([symbol]), bit]},
        "else": False,
    }
    return {
        "op": "choose",
        "when": _status_is(MFJ),
        "then": joint,
        "else": {
            "op": "choose",
            "when": _status_is(MFS),
            "then": separate_yes,
            "else": False,
        },
    }


def you_when(symbol: str, *, checked: bool) -> dict[str, Any]:
    bit = _ref(symbol) if checked else {"op": "not", "value": _ref(symbol)}
    return {"op": "all", "args": [_cds([symbol]), bit]}


def citation() -> dict[str, Any]:
    return {
        "schema": "citation.v1",
        "id": CITATION,
        "version": "v1",
        "authority": {"family": "irs-instructions", "form_id": "1040", "tax_year": 2025},
    }


def rule(box: dict[str, str], *, checked: bool) -> dict[str, Any]:
    suffix = "" if checked else "-not-checked"
    publishes = P + "form1040.line12d." + box["slug"] + ("" if checked else "-not-checked")
    state = "checked" if checked else "not_checked"
    if box["who"] == "you":
        when = you_when(box["symbol"], checked=checked)
        requires = [box["symbol"]]
        pins = [_pin(box["fact"])]
        missing = [box["symbol"]]
        notes = (
            "Form 1040 line 12d, the You box "
            f"({box['label']}). Publishes {state!r} from the recorded "
            f"{box['symbol']} answer. The 2025 instructions check this box on "
            "every filing status."
        )
    else:
        when = spouse_when(box["symbol"], checked=checked)
        requires = ["filing_status"]
        pins = [_pin(P + "filing-status"), _pin(box["fact"]),
                _pin(P + "standard-deduction.spouse-separate-condition")]
        missing = ["filing_status", COND, box["symbol"]]
        notes = (
            "Form 1040 line 12d, the Spouse box "
            f"({box['label']}). Publishes {state!r} from the recorded "
            f"{box['symbol']} answer only on a joint return, or a separate "
            "return whose spouse_separate_condition is yes. Head of household, "
            "qualifying surviving spouse and single are inapplicable."
        )
    return {
        "schema": "rule-artifact.v3",
        "id": P + "rule.form1040-line12d-" + box["slug"] + suffix,
        "version": "v1",
        "scope": _scope(),
        "role": "computation",
        "requires": requires,
        "pins": pins,
        "when": when,
        "value": state,
        "publishes": publishes,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": missing},
        "citations": [{"id": CITATION, "version": "v1"}],
        "notes": notes,
    }


def field(box: dict[str, str], *, checked: bool) -> dict[str, Any]:
    suffix = "" if checked else "-not-checked"
    publishes = P + "form1040.line12d." + box["slug"] + ("" if checked else "-not-checked")
    state = "checked" if checked else "not_checked"
    line = box["line"] if checked else box["line"] + "-not-checked"
    label = box["label"] if checked else box["label"] + " (not checked)"
    explain = (
        f"Line 12d {box['label']}: the box is {state.replace('_', ' ')}."
    )
    return {
        "schema": "form-field.v3",
        "id": P + "form1040.line-12d-" + box["slug"] + suffix,
        "version": "v1",
        "form": {
            "authority": "IRS",
            "form_id": "1040",
            "tax_year": 2025,
            "jurisdiction": "US-federal",
        },
        "line": line,
        "label": label,
        "description": (
            "Form 1040 line 12d "
            + ("checkbox" if checked else "honest not-checked disposition")
            + f" for {box['label']}."
        ),
        "binds_symbol": publishes,
        "citation": {"id": CITATION, "version": "v1"},
        "dispositions": {
            "published_value": {"render": state, "explain": explain},
            "computed_zero": {
                "render": "",
                "explain": "Not used for the line 12d categorical disposition.",
            },
            "closure_backed_zero": {
                "render": "",
                "explain": "Not used for the line 12d categorical disposition.",
            },
            "blocked": {
                "render": "",
                "explain": "line 12d is blocked because an age or blindness answer is missing",
                "codes": [
                    "DEPENDENCY_ABSENT",
                    "DEPENDENCY_INVALID",
                    "CATEGORICAL_DOMAIN_MISMATCH",
                    "SOURCE_SET_UNCLOSED",
                ],
            },
            "guard_inapplicable": {
                "render": "",
                "explain": (
                    "This line 12d box does not apply to this return, or the box is the other checked/not-checked state."
                    if box["who"] == "spouse"
                    else "This line 12d box is the other checked/not-checked state."
                ),
            },
        },
    }


def artifacts() -> list[tuple[str, dict[str, Any]]]:
    written: list[tuple[str, dict[str, Any]]] = [
        ("citation.form1040.line-12d.json", citation()),
    ]
    for box in BOXES:
        for checked in (True, False):
            body = rule(box, checked=checked)
            written.append((f"rule.form1040-line12d-{box['slug']}"
                            f"{'' if checked else '-not-checked'}.json", body))
            written.append((f"form1040.line-12d-{box['slug']}"
                            f"{'' if checked else '-not-checked'}.form-field.json",
                            field(box, checked=checked)))
    return written


def role_for(schema: str) -> str:
    return {
        "citation.v1": "citation",
        "rule-artifact.v3": "computation",
        "form-field.v3": "form-field",
    }[schema]


def change_list() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    package = json.loads(
        (CONTENT / f"package.core-calculations.{FROM['package']}.json").read_text(
            encoding="utf-8"
        )
    )
    members_now = {member["id"]: member for member in package["members"]}
    members: list[dict[str, Any]] = []
    entrypoints: list[dict[str, Any]] = []
    for _name, body in artifacts():
        new = {
            "id": body["id"],
            "version": body["version"],
            "schema": body["schema"],
            "role": role_for(body["schema"]),
        }
        if body["id"] in members_now:
            raise SystemExit(f"{body['id']} is already a member")
        members.append({"op": "add", "new": new})
        if body["schema"] == "rule-artifact.v3":
            entrypoints.append({"op": "add", "value": {"id": new["id"], "version": new["version"]}})
    changes = {
        "package_version": TO["package"],
        "release_version": TO["release"],
        "members": members,
        "entrypoints": entrypoints,
        "registry_sort": "id_version",
        "registry_new_key_order": ["checksum", "id", "version"],
    }
    return changes, members


def build(scratch: Path) -> dict[str, Any]:
    content = scratch / "content"
    releases = scratch / "releases"
    shutil.copytree(CONTENT, content)
    shutil.copytree(RELEASES, releases)
    for name, body in artifacts():
        (content / name).write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    changes, members = change_list()
    changes_path = scratch / "changes.json"
    changes_path.write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    report = generate_to_directory(
        content / f"package.core-calculations.{FROM['package']}.json",
        content / f"published-packages.{FROM['registry']}.json",
        releases / f"{RELEASE_STEM}.{FROM['release']}.json",
        content,
        changes_path,
        scratch / "out",
    )
    for src, folder, target in (
        ("package.json", content, f"package.core-calculations.{TO['package']}.json"),
        ("registry.json", content, f"published-packages.{TO['registry']}.json"),
        ("release.json", releases, f"{RELEASE_STEM}.{TO['release']}.json"),
    ):
        shutil.copy(scratch / "out" / src, folder / target)
    core = {
        "version": TO["package"],
        "registry": TO["registry"],
        "release_version": TO["release"],
        "content": str(content),
        "releases": str(releases),
        "loader_from": FROM["package"],
    }
    (scratch / "core.json").write_text(json.dumps(core, indent=2) + "\n", encoding="utf-8")
    return {
        "from": FROM,
        "to": TO,
        "package": report["package"]["version"],
        "registry": TO["registry"],
        "release": report["release"]["version"],
        "members_added": [
            [member["new"]["role"], member["new"]["id"].removeprefix(P), member["new"]["version"]]
            for member in members
        ],
        "inherited_inconsistencies": [
            list(row) for row in report.get("inherited_inconsistencies") or ()
        ],
        "boxes": [
            {
                "key": box["key"],
                "checked_field": f"form1040.line-12d-{box['slug']}",
                "not_checked_field": f"form1040.line-12d-{box['slug']}-not-checked",
                "line": box["line"],
                "who": box["who"],
                "symbol": box["symbol"],
            }
            for box in BOXES
        ],
        "design": (
            "Eight form-field.v3 citizens and eight rule-artifact.v3 publishers, "
            "plus citation.form1040.line-12d. Content only: no engine, schema, "
            "projection or renderer change."
        ),
    }


def public_error(exc: BaseException) -> str:
    return re.sub(r"(?:/Users|/private|/tmp|/var)/\S+", "[path]", f"{type(exc).__name__}: {exc}")[:800]


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: prototype.py <scratch-directory-outside-the-repo>")
    scratch = Path(sys.argv[1]).resolve()
    if REPO in scratch.parents or scratch == REPO:
        raise SystemExit("scratch directory must be outside the repository")
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    try:
        summary = build(scratch)
    except Exception as exc:  # noqa: BLE001 - a refused build is the finding
        summary = {"from": FROM, "to": TO, "refused": public_error(exc)}
    text = json.dumps(summary, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"prototype summary contains {needle}")
    (HERE / "prototype-build.json").write_text(text, encoding="utf-8")
    print(json.dumps(
        {k: summary.get(k) for k in ("package", "release", "refused", "design")},
        indent=2,
    ))


if __name__ == "__main__":
    main()
