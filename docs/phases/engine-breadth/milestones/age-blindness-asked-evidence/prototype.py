"""Scratch core v88: age 65 and blindness are asked, and the amounts wait for the answers.

Evidence for docs/phases/engine-breadth/milestones/age-blindness-asked.md.
Charter: docs/reviews/age-blindness-asked/charter-p0.md.

Builds question-wording's scratch core v87 by loading its prototype
(question-wording-evidence/prototype.py, ``build``), then makes core v88 on
top of it in the same scratch tree:

- the four input bindings (taxpayer_over_65, taxpayer_blind, spouse_over_65,
  spouse_blind) change mode from ``optional_default`` to ``required``, so an
  unanswered fact is absent instead of the declared default false;
- four ``input-question`` members, one per fact, are added (and named as
  entry points, as every other input question is);
- ``rule.dependents-worksheet-line-1`` v2 reads the spouse's two facts only on
  a joint or separate return, so a single, head of household or qualifying
  surviving spouse return is not asked about a spouse; an always-active
  ``conditional_dependency_set`` names every missing answer at once;
- ``rule.schedule1a-part-v-line-36b`` v2 reads the spouse's age only on a
  joint return.

Vocabulary bundle v4, built on question-wording's v3, keeps the two spouse
titles as v3 wrote them (Decision 9 drops the separate-return sentence
Decision 3 had added). One new return-level fact carries that condition,
asked only on a separate return. Fact type ids, versions and the unused
``default-false`` on the four age and blindness facts stay (Decision 4).
No schema, expression operation, selection or recording surface changes.
The scratch tree stays outside the repository.

    python3 prototype.py <scratch-directory-outside-the-repo>
"""

from __future__ import annotations

import copy
import importlib.util
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

QW = REPO / "docs/phases/engine-breadth/milestones/question-wording-evidence/prototype.py"
P = "tax.us.2025."
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"
FROM = {"package": "v87", "registry": "v85", "release": "v85"}
TO = {"package": "v88", "registry": "v86", "release": "v86"}

MFJ = "married_filing_jointly"
MFS = "married_filing_separately"

# Decision 9. The chart footnote (law.json, line 12d): the spouse's boxes on a
# separate return count only when the spouse had no income, isn't filing a
# return, and can't be claimed as a dependent. No published fact says that.
COND_SLUG = "standard-deduction.spouse-separate-condition"
COND_SYMBOL = "spouse_separate_condition"
COND_TITLE = (
    "The spouse had no income, isn't filing a return, and can't be claimed as a dependent "
    "on another person's return."
)
# Decision 10. The same three conditions, in the "Is it true that" form the
# Exception 1 questions use.
COND_QUESTION = (
    "Is it true that your spouse had no income, isn't filing a return, and can't be claimed "
    "as a dependent on another person's return?"
)
# Decision 4: optional_default stays on the four fact types; the binding mode decides.
SPOUSE_FACTS = (P + "spouse-over-65", P + "spouse-blind")
QUESTIONS = {
    "taxpayer-over-65": (
        "Were you born before January 2, 1961? A person reaches age 65 on the day before "
        "their 65th birthday, so a birthday of January 1, 1961 counts and January 2, 1961 "
        "does not. If this return is for someone who died in 2025 before reaching age 65, "
        "answer no."
    ),
    "taxpayer-blind": (
        "Were you totally blind on December 31, 2025, or do you have a statement certified "
        "by your eye doctor (ophthalmologist or optometrist) that you can't see better than "
        "20/200 in your better eye with glasses or contact lenses, or that your field of "
        "vision is 20 degrees or less?"
    ),
    "spouse-over-65": (
        "Was your spouse born before January 2, 1961? A person reaches age 65 on the day "
        "before their 65th birthday. If your spouse died in 2025 before reaching age 65, "
        "answer no."
    ),
    "spouse-blind": (
        "Was your spouse totally blind on December 31, 2025, or does your spouse have a "
        "statement certified by an eye doctor (ophthalmologist or optometrist) that they "
        "can't see better than 20/200 in the better eye with glasses or contact lenses, or "
        "that their field of vision is 20 degrees or less?"
    ),
    COND_SLUG: COND_QUESTION,
}
SYMBOLS = {
    "taxpayer-over-65": "taxpayer_over_65",
    "taxpayer-blind": "taxpayer_blind",
    "spouse-over-65": "spouse_over_65",
    "spouse-blind": "spouse_blind",
}


def load_qw() -> Any:
    name = "aba_p0_qw_prototype"
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, QW)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def _ref(name: str) -> dict[str, Any]:
    return {"op": "ref", "name": name}


def _status_is(value: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare", "cmp": "eq", "left": _ref("filing_status"),
        "right": {"op": "category_literal",
                  "fact_type": {"id": P + "filing-status", "version": "v1"}, "value": value},
    }


def _box(symbol: str) -> dict[str, Any]:
    return {"op": "choose", "when": _ref(symbol), "then": 1, "else": 0}


def question(slug: str) -> dict[str, Any]:
    return {
        "fact_type": {"id": P + slug, "version": "v1"},
        "id": P + "input-question." + slug,
        "question": QUESTIONS[slug],
        "schema": "input-question.v1",
        "version": "v1",
    }


def _ask(names: list[str]) -> dict[str, Any]:
    """A conditional_dependency_set that is always active: every absent name is named together."""
    return {"op": "conditional_dependency_set", "condition": True, "members": [_ref(n) for n in names]}


def line1(content: Path) -> dict[str, Any]:
    """Worksheet line 1 v2. Spouse boxes count on a joint return, and on a separate return only when the condition fact is yes."""
    body = json.loads((content / "rule.dependents-worksheet-line-1.json").read_text(encoding="utf-8"))
    assert body["version"] == "v1"
    taxpayer = ["taxpayer_over_65", "taxpayer_blind"]
    spouse = ["spouse_over_65", "spouse_blind"]
    spouse_boxes = {"op": "add", "args": [_box("spouse_over_65"), _box("spouse_blind")]}
    body["version"] = "v2"
    body["requires"] = ["filing_status"]
    body["value"] = {
        "op": "choose",
        "when": {
            "op": "choose",
            "when": _status_is(MFJ),
            "then": _ask(taxpayer + spouse),
            "else": {
                "op": "choose",
                "when": _status_is(MFS),
                "then": _ask(taxpayer + spouse + [COND_SYMBOL]),
                "else": _ask(taxpayer),
            },
        },
        "then": {
            "op": "add",
            "args": [
                _box("taxpayer_over_65"),
                _box("taxpayer_blind"),
                {
                    "op": "choose",
                    "when": _status_is(MFJ),
                    "then": spouse_boxes,
                    "else": {
                        "op": "choose",
                        "when": _status_is(MFS),
                        "then": {
                            "op": "choose",
                            "when": _ref(COND_SYMBOL),
                            "then": {"op": "add", "args": [_box("spouse_over_65"), _box("spouse_blind")]},
                            "else": 0,
                        },
                        "else": 0,
                    },
                },
            ],
        },
        "else": 0,
    }
    body["notes"] = (
        "Standard Deduction Worksheet for Dependents, line 1, and the box count of the Standard "
        "Deduction Chart for People Who Were Born Before January 2, 1961, or Were Blind "
        "(i1040gi-2025, line 12d and line 12e). v2 successor to v1: the four age and blindness "
        "facts are required inputs with no default, so the count waits until they are answered. "
        "The taxpayer's two boxes are read on every return. The spouse's two count on a married "
        "filing jointly return. On a married filing separately return they count only when "
        "spouse_separate_condition is yes (the chart footnote: the spouse had no income, isn't "
        "filing a return, and can't be claimed as a dependent). That fact is asked only on a "
        "separate return. One always-active conditional_dependency_set per status names every "
        "missing answer together. Head of household (line 12d: don't check any boxes for your "
        "spouse) and qualifying surviving spouse (the chart stops at 2 boxes) count only the "
        "taxpayer's boxes; v1 also counted a spouse on a qualifying surviving spouse return."
    )
    return body


def line36b(content: Path) -> dict[str, Any]:
    """Schedule 1-A line 36b v2: the spouse's age is read, and asked, only on a joint return."""
    body = json.loads((content / "rule.schedule1a-part-v-line-36b.json").read_text(encoding="utf-8"))
    assert body["version"] == "v1"
    inner = body["value"]
    body["version"] = "v2"
    body["requires"] = ["filing_status", P + "schedule1a.line35-per-person-amount"]
    body["value"] = {"op": "choose", "when": _status_is(MFJ), "then": inner, "else": 0}
    body["notes"] = (
        "Schedule 1-A Part V line 36b, v2 successor to v1: line 35 when the return is married "
        "filing jointly, the spouse was born before January 2, 1961 (and did not die in 2025 "
        "before reaching 65), and the spouse has a valid SSN; otherwise 0. spouse_over_65 is a "
        "required input with no default, so it is read, and asked, only on a joint return: the "
        "joint-return test now comes first. Every other return publishes 0 without reading it. "
        "The valid-SSN conditional_dependency_set and the rest of v1's expression are unchanged."
    )
    return body


def _condition_fact() -> dict[str, Any]:
    """Same boolean shape as the age facts, including the unused default. The binding is required."""
    return {
        "id": P + COND_SLUG,
        "identity_keys": [{"kind": "literal", "name": "tax-year", "values": ["2025"]}],
        "nature": "determinable",
        "optional_default": {"parameter": {"id": P + "parameter.default-false", "version": "v1"}},
        "schema": "fact-type.v2",
        "supersession": {"policy": "free"},
        "title": COND_TITLE,
        "value_schema": {"type": "boolean"},
        "version": "v1",
    }


def vocabulary_v4(content: Path) -> tuple[dict[str, Any], dict[str, str]]:
    """Bundle v4: v3's fact types, titles unchanged, plus the separate-return condition fact."""
    body = json.loads((content / "core_calculations.bundle.v3.json").read_text(encoding="utf-8"))
    if body.get("version") != "v3" or body.get("id") != P + "core_calculations.vocabulary":
        raise SystemExit("scratch v87 vocabulary bundle is not core_calculations.vocabulary v3")
    titles: dict[str, str] = {}
    insert_at = None
    for index, fact in enumerate(body["fact_types"]):
        if fact.get("id") not in SPOUSE_FACTS:
            continue
        title = str(fact.get("title") or "")
        if "separate return" in title.lower():
            raise SystemExit("v3 spouse title already names a separate return")
        default = fact.get("optional_default")
        parameter = default.get("parameter") if isinstance(default, dict) else None
        if not isinstance(parameter, dict) or parameter.get("id") != P + "parameter.default-false":
            raise SystemExit("spouse fact lost its unused default-false")
        titles[str(fact["id"])] = title
        insert_at = index + 1
    if set(titles) != set(SPOUSE_FACTS) or insert_at is None:
        raise SystemExit("vocabulary bundle v3 is missing a spouse fact")
    if any(fact.get("id") == P + COND_SLUG for fact in body["fact_types"]):
        raise SystemExit("condition fact is already in vocabulary v3")
    body["fact_types"].insert(insert_at, _condition_fact())
    body["version"] = "v4"
    body["label"] = (
        "Filing status, taxpayer and spouse demographics, the separate-return spouse condition, "
        "and itemized deductions fact types for tax year 2025"
    )
    return body, titles


def _clause_flags(text: str) -> dict[str, bool]:
    low = text.lower()
    return {
        "spouse": "spouse" in low,
        "income": "no income" in low or "no gross income" in low,
        "filing": "isn't filing" in low or "is not filing" in low or "not filing a return" in low,
        "dependent": "claimed as a dependent" in low or "can't be claimed" in low or "cannot be claimed" in low,
    }


def find_existing_condition() -> dict[str, Any]:
    """A published fact is reusable only when its own text states the whole condition."""
    exact: list[str] = []
    near: list[str] = []
    published = REPO / "packages/content/tax/2025"
    for path in sorted(published.glob("*.json")):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        texts: list[tuple[Any, Any]] = []
        if isinstance(body, dict):
            if body.get("title"):
                texts.append((body.get("id"), body.get("title")))
            if body.get("question"):
                texts.append((body.get("id"), body.get("question")))
            for fact in body.get("fact_types") or []:
                if isinstance(fact, dict) and fact.get("title"):
                    texts.append((fact.get("id"), fact.get("title")))
        for ident, text in texts:
            flags = _clause_flags(str(text))
            matched = [name for name in ("income", "filing", "dependent") if flags[name]]
            if flags["spouse"] and len(matched) == 3:
                exact.append(str(ident))
            elif flags["spouse"] and len(matched) >= 2:
                near.append(str(ident))
    return {"exact": sorted(set(exact)), "near": sorted(set(near))}


def binding_edits(package: dict[str, Any]) -> list[dict[str, Any]]:
    edits = []
    for slug, symbol in SYMBOLS.items():
        old = next(b for b in package["input_bindings"] if b["symbol"] == symbol)
        assert old["mode"] == "optional_default" and old["fact_type"]["id"] == P + slug
        new = copy.deepcopy(old)
        new["mode"] = "required"
        edits.append({"op": "replace", "old": old, "new": new})
    edits.append({"op": "add", "value": {
        "fact_type": {"id": P + COND_SLUG, "version": "v1"},
        "mode": "required",
        "symbol": COND_SYMBOL,
    }})
    return edits


def build(scratch: Path) -> dict[str, Any]:
    found = find_existing_condition()
    if found["exact"]:
        raise SystemExit("an existing fact already states the condition: " + ", ".join(found["exact"]))
    qw = load_qw()
    v87 = qw.build(scratch, True)
    if v87["bundle"] != "included" or v87["package"] != FROM["package"]:
        raise SystemExit("question-wording prototype did not build core v87 with its bundle")
    shutil.copy(scratch / "core.json", scratch / "core-v87.json")
    content = scratch / "content"
    releases = scratch / "releases"
    package = json.loads((content / f"package.core-calculations.{FROM['package']}.json").read_text(encoding="utf-8"))
    members_now = {m["id"]: m for m in package["members"]}

    written: list[tuple[str, dict[str, Any]]] = []
    for slug in QUESTIONS:
        written.append((f"input-question.{slug}.v1.json", question(slug)))
    written.append(("rule.dependents-worksheet-line-1.v2.json", line1(content)))
    written.append(("rule.schedule1a-part-v-line-36b.v2.json", line36b(content)))
    bundle, spouse_titles = vocabulary_v4(content)
    written.append(("core_calculations.bundle.v4.json", bundle))
    for name, body in written:
        path = content / name
        if path.exists():
            raise SystemExit(f"{name} already exists")
        path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")

    members: list[dict[str, Any]] = []
    entrypoints: list[dict[str, Any]] = []
    for _name, body in written:
        new = {"id": body["id"], "version": body["version"], "schema": body["schema"]}
        if body["schema"] == "input-question.v1":
            new["role"] = "input-question"
            if body["id"] in members_now:
                raise SystemExit(f"{body['id']} is already a member")
            members.append({"op": "add", "new": new})
            entrypoints.append({"op": "add", "value": {"id": body["id"], "version": body["version"]}})
        else:
            old = members_now[body["id"]]
            new["role"] = old["role"]
            members.append({"op": "replace", "old": dict(old), "new": new})
    changes = {
        "package_version": TO["package"],
        "release_version": TO["release"],
        "members": members,
        "entrypoints": entrypoints,
        "bindings": binding_edits(package),
        "registry_sort": "id_version",
        "registry_new_key_order": ["checksum", "id", "version"],
    }
    changes_path = scratch / "changes-v88.json"
    changes_path.write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    out = scratch / "out-v88"
    report = generate_to_directory(
        content / f"package.core-calculations.{FROM['package']}.json",
        content / f"published-packages.{FROM['registry']}.json",
        releases / f"{RELEASE_STEM}.{FROM['release']}.json",
        content,
        changes_path,
        out,
    )
    for src, folder, target in (
        ("package.json", content, f"package.core-calculations.{TO['package']}.json"),
        ("registry.json", content, f"published-packages.{TO['registry']}.json"),
        ("release.json", releases, f"{RELEASE_STEM}.{TO['release']}.json"),
    ):
        shutil.copy(out / src, folder / target)
    core = {
        "version": TO["package"],
        "registry": TO["registry"],
        "release_version": TO["release"],
        "content": str(content),
        "releases": str(releases),
        "loader_from": "v86",
    }
    (scratch / "core-v88.json").write_text(json.dumps(core, indent=2) + "\n", encoding="utf-8")
    built = json.loads((content / f"package.core-calculations.{TO['package']}.json").read_text(encoding="utf-8"))
    return {
        "from": FROM,
        "to": TO,
        "v87": {"package": v87["package"], "replaced": v87["replaced"], "bundle": v87["bundle"]},
        "package": report["package"]["version"],
        "release": report["release"]["version"],
        "members": [
            [edit["op"], edit["new"]["id"].removeprefix(P), edit["new"]["version"]] for edit in members
        ],
        "entrypoints_added": [edit["value"]["id"].removeprefix(P) for edit in entrypoints],
        "bindings": [
            {"symbol": b["symbol"], "fact_type": b["fact_type"]["id"].removeprefix(P), "mode": b["mode"]}
            for b in built["input_bindings"] if b["symbol"] in set(SYMBOLS.values()) | {COND_SYMBOL}
        ],
        "inherited_inconsistencies": [list(row) for row in report.get("inherited_inconsistencies") or ()],
        "questions": {slug: QUESTIONS[slug] for slug in QUESTIONS},
        "rules": {
            "dependents-worksheet-line-1": {
                "v2_requires": next(body["requires"] for _, body in written if body.get("id", "").endswith("dependents-worksheet-line-1")),
            },
            "schedule1a-part-v-line-36b": {
                "v2_requires": next(body["requires"] for _, body in written if body.get("id", "").endswith("schedule1a-part-v-line-36b")),
            },
        },
        "condition_fact": {
            "reused": False,
            "id": COND_SLUG,
            "symbol": COND_SYMBOL,
            "title": COND_TITLE,
            "question": COND_QUESTION,
            "search_exact": found["exact"],
            "search_near": found["near"],
        },
        "bundle": {
            "id": "core_calculations.vocabulary",
            "from": "v3",
            "version": "v4",
            "spouse_titles": {fact_id.removeprefix(P): title for fact_id, title in spouse_titles.items()},
            "spouse_titles_unchanged": True,
            "optional_default_kept": True,
        },
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
    print(json.dumps({k: summary.get(k) for k in ("package", "release", "refused")}, indent=2))


if __name__ == "__main__":
    main()
