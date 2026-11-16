"""Build a question-only scratch successor from published core v91.

Run: python3 <this-file> <scratch-directory-outside-the-repository>
The scratch v92 designation reserves no production version.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from tools.package_successor import generate_to_directory

P = "tax.us.2025."
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
STEM = "demo.release.sli-worksheet-integration.2025"

# Prompts retain each fact's current scope. They do not turn an unsupported
# circumstance into a supported worksheet input. See law.json for the audit.
QUESTIONS = {
    "ss-benefits-scope.no-unsupported-line1-entries":
        "For 2025, do you have any Form 1040 line 1 income other than wages reported in box 1 of your Forms W-2?",
    "ss-benefits-scope.no-pension-annuity-line5b":
        "Do you have taxable pension or annuity income to report on Form 1040, line 5b, for 2025?",
    "ss-benefits-scope.no-traditional-ira-deduction":
        "Do you have a traditional IRA contribution deduction to figure with your Social Security benefits because you or your spouse were covered by a retirement plan at work or through self-employment in 2025?",
    "ss-benefits-scope.no-form-2555":
        "Are you filing Form 2555 for 2025?",
    "ss-benefits-scope.no-form-4563":
        "Are you filing Form 4563 for 2025?",
    "ss-benefits-scope.no-form-8815":
        "Are you filing Form 8815 for 2025?",
    "ss-benefits-scope.no-excluded-adoption-benefits":
        "Are you excluding employer-provided adoption benefits from your income for 2025?",
    "ss-benefits-scope.no-puerto-rico-or-samoa-income":
        "Were you a bona fide resident of Puerto Rico or American Samoa with income from there in 2025?",
    "schedule1-adjustments-scope.no-line24z-writein":
        "Do you have a Schedule 1 line 24z write-in adjustment that must be figured before completing the Social Security Benefits Worksheet for 2025?",
    "mfs-lived-apart-all-year":
        "If you are married filing separately, did you live apart from your spouse for all of 2025?",
}


def artifacts() -> list[tuple[str, dict]]:
    result = []
    for slug, question in QUESTIONS.items():
        name = "input-question." + slug.replace(".", "-") + ".v1.json"
        result.append((name, {
            "schema": "input-question.v1", "id": P + name.removesuffix(".v1.json"),
            "version": "v1", "fact_type": {"id": P + slug, "version": "v1"},
            "question": question,
        }))
    return result


def build(scratch: Path) -> dict:
    scratch.mkdir(parents=True, exist_ok=False)
    content, releases = scratch / "content", scratch / "releases"
    shutil.copytree(CONTENT, content)
    shutil.copytree(RELEASES, releases)
    members = []
    package = json.loads((content / "package.core-calculations.v91.json").read_text())
    ids = {m["id"] for m in package["members"]}
    for name, body in artifacts():
        assert body["id"] not in ids
        (content / name).write_text(json.dumps(body, indent=2) + "\n")
        members.append({"op": "add", "new": {
            "id": body["id"], "version": "v1", "schema": "input-question.v1", "role": "input-question"}})
    changes = {"package_version": "v92", "release_version": "v90", "members": members,
               "entrypoints": [{"op": "add", "value": {"id": m["new"]["id"], "version": "v1"}} for m in members],
               "registry_sort": "id_version", "registry_new_key_order": ["checksum", "id", "version"]}
    change_file = scratch / "changes.json"
    change_file.write_text(json.dumps(changes, indent=2) + "\n")
    result = generate_to_directory(
        content / "package.core-calculations.v91.json", content / "published-packages.v89.json",
        releases / f"{STEM}.v89.json", content, change_file, scratch / "out")
    for src, dst in (
        ("package.json", content / "package.core-calculations.v92.json"),
        ("registry.json", content / "published-packages.v90.json"),
        ("release.json", releases / f"{STEM}.v90.json"),
    ):
        shutil.copyfile(scratch / "out" / src, dst)
    core = {"version": "v92", "registry": "v90", "release_version": "v90",
            "content": str(content), "releases": str(releases), "loader_from": "v91"}
    (scratch / "core.json").write_text(json.dumps(core, indent=2) + "\n")
    return {"baseline": {"core": "v91", "registry": "v89", "release": "v89"},
            "scratch": {"core": "v92", "registry": "v90", "release": "v90"},
            "members_added": [m["new"] for m in members],
            "questions": QUESTIONS, "rule_changes": [],
            "inherited_inconsistencies": [list(r) for r in result.get("inherited_inconsistencies", [])]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scratch", type=Path)
    args = parser.parse_args()
    scratch = args.scratch.resolve()
    if scratch == REPO or REPO in scratch.parents:
        raise SystemExit("scratch must be outside the repository")
    spec = importlib.util.spec_from_file_location("l6b_proto_probe", HERE / "probe.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    result = build(scratch)
    module.write_json(HERE / "prototype-build.json", result)
    print("Built scratch successor: ten input-question citizens; zero rule changes")


if __name__ == "__main__":
    main()
