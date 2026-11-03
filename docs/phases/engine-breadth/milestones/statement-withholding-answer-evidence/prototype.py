"""P0 prototype -- the proposed core v71 built in a scratch copy, then run (evidence only).

Nothing is written under ``packages/``. The script copies the committed content and release
directories to a temporary directory, adds one new rule artifact (``rule.form1040-line25b`` v4,
``rule-artifact.v4``) there, builds package v71 / registry v69 / release v69 with
``tools/package_successor.py``, and runs every case of ``probe.py`` on v71 through
``live_coordinate_run``. The v70 side of each comparison is ``probe-output.json`` (run
``probe.py`` first). The only repository code touched is one in-process wrapper that gives v71
the same companion declaration v70 has (``packages/tax/loader.py`` needs this entry in Track 1).

    python3 docs/phases/engine-breadth/milestones/statement-withholding-answer-evidence/prototype.py [eq|gte]

``eq`` compares the two counts for equality as Form 1040 line 25a does for Form W-2; ``gte``
requires at least as many answers as statements. Writes ``prototype-output-<cmp>.json``, and the
rule it built to ``prototype-line25b-v4-<cmp>.json``. Synthetic ``demo.*`` data only.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

import probe  # noqa: E402
from packages.tax import loader  # noqa: E402
from tools.package_successor import generate_to_directory  # noqa: E402

P = "tax.us.2025."
# (box 4 / box 6 fact, its family, the statement's income fact, the income family)
FAMILIES = (
    ("f1099int.box4-withholding", "f1099int.b4", "f1099int.box1-interest", "f1099int.b1"),
    ("f1099div.box4-withholding", "f1099div.b4", "f1099div.box1a-ordinary", "f1099div.1a"),
    ("f1099r.ira-box4-withholding", "f1099r.box4", "f1099r.ira-box1-taxable-distribution", "f1099r.ira-fully-taxable"),
    ("f1099g.box4-withholding", "f1099g.b4", "f1099g.box1-unemployment", "f1099g.1"),
    ("ssa1099.box6-voluntary-withholding", "ssa1099.b6", "ssa1099.box5-net-benefits", "ssa1099.benefits"),
)


def make_rule(cmp: str) -> dict[str, Any]:
    rule = json.loads((probe.CONTENT / "rule.form1040-line25b.v3.json").read_text(encoding="utf-8"))
    args = list(rule["when"]["args"])  # the five require_closed of v3, unchanged
    for b4, b4_set, income, income_set in FAMILIES:
        args.append({"op": "any", "args": [
            {"op": "compare", "cmp": cmp,
             "left": {"op": "count", "name": P + b4, "source_set": P + b4_set},
             "right": {"op": "count", "name": P + income, "source_set": P + income_set}},
            # reached only when the counts disagree: the answer is absent, so it blocks naming the box 4 fact
            {"op": "ref", "name": P + b4},
        ]})
    rule["when"] = {"op": "all", "args": args}
    rule["schema"] = "rule-artifact.v4"
    rule["version"] = "v4"
    rule["notes"] = "PROTOTYPE, not a citizen: scratch evidence for statement-withholding-answer P0."
    return rule


def build(cmp: str, scratch: Path) -> None:
    content, releases = scratch / "content", scratch / "releases"
    shutil.copytree(probe.CONTENT, content)
    shutil.copytree(probe.RELEASE_DIR, releases)
    rule = make_rule(cmp)
    text = json.dumps(rule, indent=2, sort_keys=True) + "\n"
    (content / "rule.form1040-line25b.v4.json").write_text(text, encoding="utf-8")
    (HERE / f"prototype-line25b-v4-{cmp}.json").write_text(text, encoding="utf-8")
    changes = {
        "package_version": "v71", "release_version": "v69",
        "members": [{"op": "replace",
                     "old": {"id": P + "rule.form1040-line25b", "role": "computation", "schema": "rule-artifact.v3", "version": "v3"},
                     "new": {"id": P + "rule.form1040-line25b", "role": "computation", "schema": "rule-artifact.v4", "version": "v4"}}],
        "registry_sort": "id_version", "registry_new_key_order": ["checksum", "id", "version"],
    }
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2), encoding="utf-8")
    report = generate_to_directory(
        content / "package.core-calculations.v70.json", content / "published-packages.v68.json",
        releases / "demo.release.sli-worksheet-integration.2025.v68.json", content, scratch / "changes.json", scratch / "out")
    print("successor", report["package"]["version"], "inherited:", report["inherited_inconsistencies"], flush=True)
    for name, (folder, target) in {
        "package.json": ("content", "package.core-calculations.v71.json"),
        "registry.json": ("content", "published-packages.v69.json"),
        "release.json": ("releases", "demo.release.sli-worksheet-integration.2025.v69.json"),
    }.items():
        shutil.copy(scratch / "out" / name, scratch / folder / target)
    probe.CONTENT, probe.RELEASE_DIR = content, releases
    probe.CORES["v71"] = (
        "package.core-calculations.v71.json", "v71",
        "demo.release.sli-worksheet-integration.2025.v69.json", "v69", "published-packages.v69.json")
    original = loader.domain_package_companion_declarations

    def with_v71() -> dict[tuple[str, str], dict[str, Any]]:
        declarations = dict(original())
        declarations[("tax.us.2025.package.core-calculations", "v71")] = declarations[("tax.us.2025.package.core-calculations", "v70")]
        return declarations

    loader.domain_package_companion_declarations = with_v71  # type: ignore[assignment]


def main() -> None:
    """Runs every case on v71 and writes ``prototype-output-<cmp>.json``. Cases already in an
    existing output file are kept, not rerun (delete the file to rerun all)."""
    cmp = sys.argv[1] if len(sys.argv) > 1 else "eq"
    v70 = {c["run_id"]: c for c in json.loads((HERE / "probe-output.json").read_text(encoding="utf-8"))["cases"]}
    out_path = HERE / f"prototype-output-{cmp}.json"
    done: dict[str, Any] = {}
    if out_path.exists():
        done = {c["run_id"]: c for c in json.loads(out_path.read_text(encoding="utf-8"))["cases"]}
    cases: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory() as tmp:
        build(cmp, Path(tmp).resolve() / "s")
        for family, cause, builder in probe.case_table():
            run_id = f"demo.p0.swa.{family}.{cause}"
            if run_id in done:
                cases.append(done[run_id])
                continue
            print("run", run_id, flush=True)
            new = probe.summarize(builder(), run_id + ".v71", "v71")
            old = v70.get(run_id) or probe.summarize(builder(), run_id, "v70")  # a case probe-output.json lacks
            cases.append({"family": family, "cause": cause, "run_id": run_id, "v70_lines": old.get("lines"),
                          "v71": new, "lines_identical_to_v70": old.get("lines") == new.get("lines")})
            out_path.write_text(json.dumps({"cmp": cmp, "cases": cases}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    out_path.write_text(json.dumps({"cmp": cmp, "cases": cases}, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
