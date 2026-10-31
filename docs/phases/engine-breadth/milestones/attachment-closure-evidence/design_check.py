"""P0 design check -- would guarding the subtotal rules make the attachments wait? (scratch candidate)

Builds, in a temporary directory outside the repository, a core v63 candidate from the
committed core v62 / registry v60 / release v60 with ``tools/package_successor.build_successor``:
each named ``...-subtotal`` rule gets a successor whose ``when`` is
``require_closed`` over the source set its ``collect`` reads (the shape of
``rule.f1099div-2a-subtotal`` v2). The candidate is then run on the real coordinator
(``live_coordinate_run``) through the same cases as ``probe.py``. Nothing is written to the
repository except ``design-check-output.json``; the candidate package, registry, release and
rule bodies live in the temporary directory only. The runtime patch below gives the
scratch core v63 the companion declaration v62 shares, as the loader would for a published
v63; it changes no repository file.

    python3 docs/phases/engine-breadth/milestones/attachment-closure-evidence/design_check.py \
        <rule-name> [<rule-name> ...] -- <source-set> [<source-set> ...]

The rule names are the ``rule.<name>`` ids without the ``tax.us.2025.rule.`` prefix; the
source sets are the cases to run on the candidate and to compare with ``probe-output.json``.
With no source set only the change set ``v62-to-v63.json`` is written (the package_successor
change-set shape, as the collect-closure survey's ``v61-to-v62.json``).
"""

from __future__ import annotations

import copy
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

import packages.tax.loader as loader  # noqa: E402
import probe  # noqa: E402
import tests.test_collect_closure as cc  # noqa: E402
from packages.derivation.production_resolver import PublicationSurface  # noqa: E402
from tools.collect_closure_survey import walk  # noqa: E402
from tools.package_successor import build_successor, load_corpus  # noqa: E402

P = cc.P


def build_candidate(rule_names: list[str], tmp: Path) -> dict[str, Any]:
    content = tmp / "content"
    releases = tmp / "releases"
    shutil.copytree(cc.CONTENT, content)
    shutil.copytree(cc.RELEASE_DIR, releases)
    package = json.loads(cc.PACKAGE_V62.read_text())
    registry = (cc.CONTENT / "published-packages.v60.json").read_bytes()
    release = json.loads(cc.RELEASE_V60.read_text())
    corpus, _ = load_corpus(content)
    entry_keys = {(e["id"], e["version"]) for e in package["entrypoints"]}
    members, entrypoints, summary = [], [], []
    for name in rule_names:
        rid = P + "rule." + name
        old_pin = next(m for m in package["members"] if m["id"] == rid)
        body = copy.deepcopy(corpus[(rid, old_pin["version"])])
        source_set = next(n["source_set"] for n in walk(body) if n.get("op") == "collect")
        new_version = "v" + str(int(old_pin["version"][1:]) + 1)
        body["version"] = new_version
        body["when"] = {"op": "require_closed", "source_set": source_set}
        body["notes"] = (body.get("notes", "") + f" Scratch design check: requires {source_set} closed at the current horizon.").strip()
        corpus[(rid, new_version)] = body
        (content / f"rule.{name}.{new_version}.json").write_text(json.dumps(body, indent=2, sort_keys=True) + "\n")
        members.append({"op": "replace", "old": old_pin, "new": dict(old_pin, version=new_version)})
        is_entry = (rid, old_pin["version"]) in entry_keys
        if is_entry:
            entrypoints.append({"op": "replace", "old": {"id": rid, "version": old_pin["version"]},
                                "new": {"id": rid, "version": new_version}})
        summary.append({"rule": name, "from": old_pin["version"], "to": new_version, "schema": old_pin["schema"],
                        "source_set": source_set.replace(P, ""), "entrypoint": is_entry})
    changes = {"package_version": "v63", "release_version": "v61", "members": members, "registry_sort": "id_version",
               "registry_tail": [["tax.us.2025.rule.odc-child.counts", "v2"]],
               "registry_new_key_order": ["checksum", "id", "version"], "entrypoints": entrypoints}
    result = build_successor(package, registry, release, corpus, changes)
    (HERE / "v62-to-v63.json").write_text(json.dumps(changes, indent=2) + "\n")
    package_path = content / "package.core-calculations.v63.json"
    registry_path = content / "published-packages.v61.json"
    release_path = releases / "demo.release.sli-worksheet-integration.2025.v61.json"
    package_path.write_bytes(result.package)
    registry_path.write_bytes(result.registry)
    release_path.write_bytes(result.release)
    cc.CORES["v63"] = (package_path, release_path, "v61", PublicationSurface(releases, registry_path, content))
    original = loader.domain_package_companion_declarations

    def declarations() -> dict[Any, Any]:
        out = original()
        out[(P + "package.core-calculations", "v63")] = out[(P + "package.core-calculations", "v62")]
        return out

    loader.domain_package_companion_declarations = declarations  # type: ignore[assignment]
    return {"successors": summary, "entrypoint_edits": len(entrypoints), "members_replaced": len(members)}


def main() -> None:
    args = sys.argv[1:]
    split = args.index("--")
    rule_names, sets = args[:split], args[split + 1:]
    baseline = json.loads((HERE / "probe-output.json").read_text())["sets"]
    out: dict[str, Any] = {"candidate": None, "sets": {}}
    with tempfile.TemporaryDirectory() as tmp:
        out["candidate"] = build_candidate(rule_names, Path(tmp))
        if not sets:  # change set only
            return
        for short in sets:
            v63 = probe.probe(P + short, "v63")
            comparison: dict[str, Any] = {}
            for variant_name, v in v63.items():
                base = baseline[short][variant_name]
                comparison[variant_name] = {
                    "v62_answered_values_equal": base["answered"].get("values_sha256") == v["answered"].get("values_sha256"),
                    "v63": {k: v[k] for k in ("unanswered", "answered")},
                }
            out["sets"][short] = comparison
            print("done", short, file=sys.stderr)
        v62 = cc._run(cc._complete_return(), "demo.ac.complete.v62", "v62")
        v63 = cc._run(cc._complete_return(), "demo.ac.complete.v63", "v63")
        out["complete_return"] = {
            "blocked_v62": len(v62.blocked), "blocked_v63": len(v63.blocked),
            "values_equal": v62.values == v63.values, "values_count": len(v63.values),
            "schedule_d_published_v63": v63.has("schedule-d.disposition"),
        }
    (HERE / "design-check-output.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
