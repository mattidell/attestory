"""Scratch core v87: question citizens say what their rules read.

Evidence for docs/phases/engine-breadth/milestones/question-wording.md.
Charter: docs/reviews/question-wording/charter-p0.md.

Copies published core v86 and replaces only question text: the two wash-sale
adjustment closure questions, the Exception 1 only-box-2a question, the
student-loan dependent question, the titles of their two facts (exception1
and sli-scope bundle successors), and the four age and blindness titles in the
vocabulary bundle (Decisions 1-4). No rule, schema, selection, or recording surface changes.
The scratch tree stays outside the repository.

    python3 prototype.py <scratch-directory-outside-the-repo>

If the bundle successor is refused, the build is repeated without the age
and blindness titles and the summary says so.
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
FROM = {"package": "v86", "registry": "v84", "release": "v84"}
TO = {"package": "v87", "registry": "v85", "release": "v85"}

WASH = (
    "Have you recorded the wash-sale loss adjustment amount of every covered {term} sale "
    "with a wash-sale loss adjustment (a loss disallowed because you bought the same "
    "investment within 30 days before or after the sale) on every Form 1099-B you or "
    "your spouse received for 2025?"
)
# Review F1 (Decision 7): only a sale that must be reported on Form 8949 or
# Schedule D defeats Exception 1.
ONLY_BOX2A = (
    "Is it true that you had no capital gains in 2025 other than capital gain "
    "distributions in box 2a of Form 1099-DIV, and that you had no sale in 2025 of "
    "stock, bonds, funds or other property that you must report on Form 8949 or "
    "Schedule D (even one with no gain or loss)? Sales inside an IRA or 401(k) do not "
    "count, and neither does a loss on a personal item unless you received a Form "
    "1099-K or 1099-S for it."
)
SLI = (
    "Is someone else claiming you (or your spouse, on a joint return) as a dependent "
    "on their 2025 return?"
)
AGE = (
    "Taxpayer was born before January 2, 1961. A person reaches age 65 on the "
    "day before the 65th birthday. A taxpayer who was born before January 2, 1961 "
    "but died in 2025 before reaching age 65 is not included."
)
SPOUSE_AGE = (
    "Spouse was born before January 2, 1961. A person reaches age 65 on the "
    "day before the 65th birthday. A spouse who was born before January 2, 1961 "
    "but died in 2025 before reaching age 65 is not included."
)
BLIND = (
    "Taxpayer was totally blind as of December 31, 2025, or as of December 31, "
    "2025 could not see better than 20/200 in the better eye with glasses or "
    "contact lenses, or had a field of vision of 20 degrees or less, as a "
    "statement certified by an eye doctor says."
)
SPOUSE_BLIND = (
    "Spouse was totally blind as of December 31, 2025, or as of December 31, "
    "2025 could not see better than 20/200 in the better eye with glasses or "
    "contact lenses, or had a field of vision of 20 degrees or less, as a "
    "statement certified by an eye doctor says."
)
# Decision 2: the only-box-2a fact's title says what the v3 question asks.
EXC1_TITLE = (
    "Exception 1 component C1 (ADR-0050): whether the return's only capital gains are Form "
    "1099-DIV box-2a capital-gain distributions and the filer had no 2025 sale of stock, bonds, "
    "funds or other property that must be reported on Form 8949 or Schedule D, including one with "
    "no gain or loss; sales inside an IRA or 401(k) do not count, and neither does a loss on "
    "personal-use property unless a Form 1099-K or 1099-S was received for it (Form 1040 instructions, "
    "line 7a: \"If you sold a capital asset ... you must complete and attach Form 8949 and Schedule "
    "D\"; Schedule D instructions, Capital Assets Held for Personal Use: \"Loss from the sale or "
    "exchange of a capital asset held for personal use isn't deductible. But if you had a loss ... for "
    "which you received a Form 1099-S, you must report the transaction on Form 8949 ... Also, if you "
    "had a loss from the sale or exchange of personal property for which you received a Form 1099-K, "
    "you must report the transaction on Form 8949 or on Schedule 1 (Form 1040)\"). "
    "Contributed categorical assertion, domain {yes, no}, no default, presence-before-value, free "
    "supersession. Distinct from the checked schedule-d-required.conclusion."
)
# Decision 3: the student-loan dependency fact names the spouse on a joint return.
SLI_TITLE = (
    "Student Loan Interest Deduction eligibility component (legal zero, not a block): neither the "
    "filer nor, on a joint return, the filer's spouse is claimed as a dependent on another "
    "taxpayer's 2025 return (Form 1040 instructions, Schedule 1 line 21: \"You, or your spouse if "
    "filing jointly, aren't claimed as a dependent on someone else's ... 2025 tax return\"; Pub. "
    "970 p.33). An actual claim, not whether someone could claim. Filer-level. Contributed "
    "categorical assertion, domain {yes, no}, no default. yes asserts neither is claimed and the "
    "route proceeds; no asserts the filer or, on a joint return, the spouse IS claimed -- the law's "
    "own definite $0 for this return, not missing information and not a block."
)
TITLES = {
    P + "taxpayer-over-65": AGE,
    P + "taxpayer-blind": BLIND,
    P + "spouse-over-65": SPOUSE_AGE,
    P + "spouse-blind": SPOUSE_BLIND,
}


def _load(name: str) -> dict[str, Any]:
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def _wash(name: str, term: str) -> dict[str, Any]:
    """The adjustment closure question, worded like its basis and proceeds siblings."""
    body = _load(name)
    if f"of every covered {term} sale on every" not in str(body["closure_question"]):
        raise SystemExit(f"{name} does not have the expected sale phrase")
    sibling = _load(name.replace("-adjustment.", "-basis."))
    if f"of every covered {term} sale with a wash-sale loss adjustment (" not in str(sibling["closure_question"]):
        raise SystemExit(f"{name}: the basis sibling no longer has the limiting phrase")
    body["closure_question"] = WASH.format(term=term)
    body["version"] = "v4"
    return body


def _only_box2a() -> dict[str, Any]:
    body = _load("input-question.exception1-only-box2a-capital-gains.v2.json")
    body["question"] = ONLY_BOX2A
    body["version"] = "v3"
    return body


def _sli() -> dict[str, Any]:
    body = _load("input-question.sli-scope-not-claimed-as-dependent.v1.json")
    body["question"] = SLI
    body["version"] = "v2"
    return body


def _bundle() -> dict[str, Any]:
    body = _load("core_calculations.bundle.v2.json")
    seen = set()
    for fact in body["fact_types"]:
        title = TITLES.get(fact["id"])
        if title is None:
            continue
        fact["title"] = title
        seen.add(fact["id"])
    if seen != set(TITLES):
        raise SystemExit("vocabulary bundle is missing an age or blindness fact")
    body["version"] = "v3"
    return body


def _retitle(name: str, fact_id: str, title: str, version: str) -> dict[str, Any]:
    """A bundle successor that changes one fact type's title and nothing else."""
    body = _load(name)
    hits = [fact for fact in body["fact_types"] if fact["id"] == fact_id]
    if len(hits) != 1:
        raise SystemExit(f"{name} does not declare {fact_id} once")
    hits[0]["title"] = title
    body["version"] = version
    return body


def artifacts(include_bundle: bool) -> list[tuple[str, dict[str, Any]]]:
    rows = [
        ("closure-mapping.f1099b-covered-w-st-adjustment.v4.json", _wash(
            "closure-mapping.f1099b-covered-w-st-adjustment.v3.json", "short-term")),
        ("closure-mapping.f1099b-covered-w-lt-adjustment.v4.json", _wash(
            "closure-mapping.f1099b-covered-w-lt-adjustment.v3.json", "long-term")),
        ("input-question.exception1-only-box2a-capital-gains.v3.json", _only_box2a()),
        ("input-question.sli-scope-not-claimed-as-dependent.v2.json", _sli()),
        ("exception1.bundle.v2.json", _retitle(
            "exception1.bundle.json", P + "exception1.only-box2a-capital-gains", EXC1_TITLE, "v2")),
        ("sli-scope.bundle.v2.json", _retitle(
            "sli-scope.bundle.json", P + "sli-scope.not-claimed-as-dependent", SLI_TITLE, "v2")),
    ]
    if include_bundle:
        rows.append(("core_calculations.bundle.v3.json", _bundle()))
    return rows


def role_for(schema: str) -> str:
    return {
        "source-closure-mapping.v3": "source-closure-mapping",
        "input-question.v1": "input-question",
        "bundle.v2": "fact-type-bundle",
    }[schema]


def change_list(rows: list[tuple[str, dict[str, Any]]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    package = json.loads((CONTENT / f"package.core-calculations.{FROM['package']}.json").read_text(encoding="utf-8"))
    members_now = {member["id"]: member for member in package["members"]}
    entry_keys = {(entry["id"], entry["version"]) for entry in package["entrypoints"]}
    members: list[dict[str, Any]] = []
    entrypoints: list[dict[str, Any]] = []
    for _name, body in rows:
        new = {"id": body["id"], "version": body["version"], "schema": body["schema"], "role": role_for(body["schema"])}
        old = members_now.get(body["id"])
        if old is None:
            raise SystemExit(f"published package has no member {body['id']}")
        members.append({"op": "replace", "old": dict(old), "new": new})
        if (old["id"], old["version"]) in entry_keys:
            entrypoints.append({
                "op": "replace",
                "old": {"id": old["id"], "version": old["version"]},
                "new": {"id": new["id"], "version": new["version"]},
            })
    changes = {
        "package_version": TO["package"],
        "release_version": TO["release"],
        "members": members,
        "entrypoints": entrypoints,
        "registry_sort": "id_version",
        "registry_new_key_order": ["checksum", "id", "version"],
    }
    return changes, members


def build(scratch: Path, include_bundle: bool) -> dict[str, Any]:
    content = scratch / "content"
    releases = scratch / "releases"
    shutil.copytree(CONTENT, content)
    shutil.copytree(RELEASES, releases)
    rows = artifacts(include_bundle)
    for name, body in rows:
        (content / name).write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    changes, members = change_list(rows)
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
    words = {
        "wash_st": rows[0][1]["closure_question"],
        "wash_lt": rows[1][1]["closure_question"],
        "only_box2a": rows[2][1]["question"],
        "sli": rows[3][1]["question"],
    }
    words["fact_titles"] = {
        "exception1.only-box2a-capital-gains": EXC1_TITLE,
        "sli-scope.not-claimed-as-dependent": SLI_TITLE,
    }
    if include_bundle:
        words["titles"] = {
            fact_id.removeprefix(P): title for fact_id, title in TITLES.items()
        }
    return {
        "from": FROM,
        "to": TO,
        "package": report["package"]["version"],
        "registry": TO["registry"],
        "release": report["release"]["version"],
        "members_edited": len(members),
        "replaced": len(members),
        "members": [
            [member["op"], member["new"]["id"].removeprefix(P), member["new"]["version"]]
            for member in members
        ],
        "bundle": "included" if include_bundle else "stopped",
        "inherited_inconsistencies": [list(row) for row in report.get("inherited_inconsistencies") or ()],
        "words": words,
    }


def public_error(exc: BaseException) -> str:
    text = f"{type(exc).__name__}: {exc}"
    text = re.sub(r"(?:/Users|/private|/tmp|/var)/\S+", "[path]", text)
    return text[:500]


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: prototype.py <scratch-directory-outside-the-repo>")
    scratch = Path(sys.argv[1]).resolve()
    if REPO in scratch.parents or scratch == REPO:
        raise SystemExit("scratch directory must be outside the repository")
    cause = ""
    try:
        if scratch.exists():
            shutil.rmtree(scratch)
        scratch.mkdir(parents=True)
        summary = build(scratch, True)
    except Exception as first:
        cause = public_error(first)
        if scratch.exists():
            shutil.rmtree(scratch)
        scratch.mkdir(parents=True)
        try:
            summary = build(scratch, False)
        except Exception as second:
            raise SystemExit(cause + " | without bundle: " + public_error(second)) from second
        summary["bundle"] = "stopped"
        summary["bundle_cause"] = cause
    text = json.dumps(summary, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"prototype summary contains {needle}")
    (HERE / "prototype-build.json").write_text(text, encoding="utf-8")
    print(json.dumps({
        "package": summary["package"],
        "replaced": summary["replaced"],
        "bundle": summary["bundle"],
        "output": "prototype-build.json",
    }, indent=2))


if __name__ == "__main__":
    main()
