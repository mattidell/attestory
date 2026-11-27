"""Rebuild the P0 scratch: proposed answer-explanation.v1 and scratch core v109.

Run from the repository root, with a new directory outside the repository:
  python3 docs/phases/engine-breadth/milestones/line16-next-step-evidence/scratch_build.py <new-dir>

1. Finds the P0 plan and scratch evidence in the pre-rebase snapshot and
   exports the plan's tree with `git archive` into <new-dir>/repo.
2. Applies scratch.diff there: the proposed schema answer-explanation.v1,
   artifact-package.v45 (v44 plus that one schema and role), their
   published.json checksums, loader role, capability row, package
   validation and authorization-closure edges, the projection change,
   the v109 loader carry-forward, and four answer-explanation citizens.
3. Exports the P0 evidence scripts into the scratch tree, including the
   versions of probe.py and replay.py used for the scratch comparison.
4. Inside the export, generates and validates package v109, registry v107
   and release v107 from published v108 with tools.package_successor
   (schema artifact-package.v45; four members and entrypoints added; one
   admitted schema added) and installs them in the export's content and
   release directories.
5. Writes scratch-build.json beside the scratch tree with the base commit,
   the diff digest, and the generated files' digests.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SNAPSHOT = "refs/snapshot/2026-11-26-line16-next-step-pre-rebase"
PLAN_SUBJECT = "plan: a required Schedule D with no sale says what to do next"
SCRATCH_SUBJECT = "p0(line16-next-step): scratch answer explanations and full replay"
P = "tax.us.2025."
SLUGS = ("only-box2a-capital-gains", "no-capital-losses", "no-qof-deferral", "no-boxes-2b-2c-2d")
STEM = "demo.release.sli-worksheet-integration.2025"
FROM = {"core": "v108", "registry": "v106", "release": "v106"}
TO = {"core": "v109", "registry": "v107", "release": "v107"}
CONTENT = Path("packages/content/tax/2025")
RELEASES = Path("packages/sample_data/student_loan_worksheet_integration/publication_surface/releases")


def p0_sources() -> tuple[str, str]:
    message = f"The P0 scratch build reproduces only from {SNAPSHOT}."
    try:
        log = subprocess.check_output(
            ["git", "log", "--format=%H%x09%s", SNAPSHOT], cwd=REPO,
            text=True, stderr=subprocess.DEVNULL, timeout=30,
        )
    except subprocess.CalledProcessError:
        raise SystemExit(message) from None
    refs: dict[str, str] = {}
    for line in log.splitlines():
        commit, _, subject = line.partition("\t")
        if subject in (PLAN_SUBJECT, SCRATCH_SUBJECT):
            refs.setdefault(subject, commit)
    if len(refs) != 2:
        raise SystemExit(message)
    return refs[PLAN_SUBJECT], refs[SCRATCH_SUBJECT]


def extract_tree(ref: str, export: Path, *paths: str) -> None:
    archive = subprocess.check_output(["git", "archive", ref, *paths], cwd=REPO, timeout=300)
    subprocess.run(["tar", "-x", "-C", str(export)], input=archive, check=True, timeout=300)


def changes() -> dict:
    members = []
    entries = []
    for slug in SLUGS:
        pin = {"id": f"{P}answer-explanation.exception1-{slug}-no", "version": "v1"}
        members.append({"op": "add", "new": {**pin, "schema": "answer-explanation.v1", "role": "answer-explanation"}})
        entries.append({"op": "add", "value": pin})
    return {"package_version": TO["core"], "release_version": TO["release"], "schema": "artifact-package.v45",
            "members": members, "entrypoints": entries,
            "admitted_schemas": [{"op": "add", "value": "answer-explanation.v1"}]}


def generate(export: Path) -> dict:
    """Runs inside the export (its own code): validate and install v109."""
    sys.path.insert(0, str(export))
    from tools.package_successor import generate_to_directory

    work = export.parent / "generate"
    work.mkdir()
    (work / "changes.json").write_text(json.dumps(changes(), indent=2) + "\n", encoding="utf-8")
    content, releases = export / CONTENT, export / RELEASES
    report = generate_to_directory(content / f"package.core-calculations.{FROM['core']}.json",
                                   content / f"published-packages.{FROM['registry']}.json",
                                   releases / f"{STEM}.{FROM['release']}.json",
                                   content, work / "changes.json", work / "generated")
    installed = {"package.json": content / f"package.core-calculations.{TO['core']}.json",
                 "registry.json": content / f"published-packages.{TO['registry']}.json",
                 "release.json": releases / f"{STEM}.{TO['release']}.json"}
    digests = {}
    for name, target in installed.items():
        assert not target.exists(), target.name
        shutil.copyfile(work / "generated" / name, target)
        digests[target.name] = hashlib.sha256(target.read_bytes()).hexdigest()
    return {"generated_sha256": digests,
            "generation": {k: v for k, v in report.items() if isinstance(v, (str, int, bool))}}


def main() -> None:
    if len(sys.argv) == 3 and sys.argv[1] == "--generate":
        print(json.dumps(generate(Path(sys.argv[2]).resolve())))
        return
    scratch = Path(sys.argv[1]).resolve()
    assert REPO not in scratch.parents and scratch != REPO and not scratch.exists(), "need a new directory outside the repository"
    base, evidence = p0_sources()
    export = scratch / "repo"
    export.mkdir(parents=True)
    extract_tree(base, export)
    diff = (HERE / "scratch.diff").read_bytes()
    subprocess.run(["git", "apply", "--unidiff-zero", "-"], cwd=export, input=diff, check=True, timeout=120)
    evidence_path = HERE.relative_to(REPO)
    extract_tree(evidence, export, str(evidence_path))
    target = export / evidence_path
    out = subprocess.run([sys.executable, str(target / "scratch_build.py"), "--generate", str(export)],
                         cwd=export, check=True, capture_output=True, text=True, timeout=1200)
    generated = json.loads(out.stdout.strip().splitlines()[-1])
    record = {"base": base, "scratch_diff_sha256": hashlib.sha256(diff).hexdigest(), "from": FROM, "to": TO,
              "changes": changes(), "status": "valid",
              "validation": "tools.package_successor.generate_to_directory validated package, registry and release",
              **generated}
    text = json.dumps(record, indent=2) + "\n"
    for root in ("Users", "private", "tmp", "var"):
        assert "/" + root + "/" not in text, "local path in record"
    (scratch / "scratch-build.json").write_text(text, encoding="utf-8")
    core = {"version": TO["core"], "registry": TO["registry"], "release_version": TO["release"]}
    (scratch / "core-v109.json").write_text(json.dumps(core) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in record.items() if k != "changes"}, indent=2))


if __name__ == "__main__":
    main()
