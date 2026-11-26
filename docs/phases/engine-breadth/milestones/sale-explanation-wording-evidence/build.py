"""Scratch core v107 from published v106: the sale explanations and questions read plainly.

Run: python3 build.py <new-directory-outside-repository> [--variant all|one]

Variant all replaces the 30 family-block-explanation citizens and the 8 sale
wash-sale adjustment input questions with v2 successors carrying the
sentences in wording.json. Variant one is the safety check: one explanation
(covered-w-st CODE_W_ON_GAIN) and one question (covered-w-st adjustment).
No fact type, rule, family or requirement changes. Successors are closed over
{"id", "version"} pins (none pin an explanation or an input question today,
so the closure is the declared set). Each successor differs from its
predecessor only by the declared prose and its root version; undoing exactly
those recovers every predecessor byte. The package, registry and release
are validated by tools.package_successor. Nothing in packages/ is edited.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from tools.package_successor import SuccessorError, generate_to_directory  # noqa: E402

STEM = "demo.release.sli-worksheet-integration.2025"
ONE = {"tax.us.2025.family-block-explanation.f1099b-covered-w-st.code-w-on-gain",
       "tax.us.2025.input-question.f1099b-covered-w-st-adjustment"}


def literal_replace(raw: str, old: str, new: str) -> str:
    before, after = json.dumps(old, ensure_ascii=False), json.dumps(new, ensure_ascii=False)
    assert raw.count(before) == 1, "ambiguous or absent prose literal"
    return raw.replace(before, after, 1)


def pinned(node, targets, found):
    if isinstance(node, dict):
        if (node.get("id"), node.get("version")) in targets:
            found.append((node["id"], node["version"]))
        for value in node.values():
            pinned(value, targets, found)
    elif isinstance(node, list):
        for value in node:
            pinned(value, targets, found)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scratch")
    parser.add_argument("--variant", choices=("all", "one"), default="all")
    args = parser.parse_args()
    scratch = Path(args.scratch).resolve()
    assert REPO not in scratch.parents and not scratch.exists()
    source = REPO / "packages/content/tax/2025"
    releases = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
    content, rel = scratch / "content", scratch / "releases"
    shutil.copytree(source, content)
    shutil.copytree(releases, rel)
    manifest = [r for r in json.loads((HERE / "wording.json").read_text())["replacements"]
                if args.variant == "all" or r["id"] in ONE]
    package = json.loads((source / "package.core-calculations.v106.json").read_text())
    pins = {m["id"]: m for m in package["members"]}
    files, existing = {}, {}
    for path in source.glob("*.json"):
        body = json.loads(path.read_text())
        if isinstance(body, dict) and re.fullmatch(r"v\d+", str(body.get("version"))):
            files[(body.get("id"), body["version"])] = path
            existing.setdefault(body.get("id"), set()).add(int(body["version"][1:]))
    member_bodies = {mid: json.loads(files[(mid, m["version"])].read_text()) for mid, m in pins.items()
                     if (mid, m["version"]) in files}
    changed = {r["id"] for r in manifest}
    levels = [sorted(changed)]
    while True:
        targets = {(i, pins[i]["version"]) for i in changed}
        new = set()
        for mid, body in member_bodies.items():
            if mid in changed:
                continue
            found: list = []
            for key, value in body.items():
                if key != "id":
                    pinned(value, targets, found)
            if found:
                new.add(mid)
        if not new:
            break
        levels.append(sorted(new))
        changed |= new
    next_version = {i: "v" + str(max(existing[i]) + 1) for i in changed}
    members, entries, successors = [], [], []
    for cid in sorted(changed):
        old_version = pins[cid]["version"]
        old_path = files[(cid, old_version)]
        raw = old_raw = old_path.read_text()
        prose = [r for r in manifest if r["id"] == cid]
        for row in prose:
            raw = literal_replace(raw, row["old"], row["new"])
        pin_count = 0
        for target in sorted(changed - {cid}):
            pattern = re.compile(r'("id": "' + re.escape(target) + r'",\s*"version": ")' + re.escape(pins[target]["version"]) + '"')
            raw, n = pattern.subn(lambda m: m[1] + next_version[target] + '"', raw)
            pin_count += n
        raw, count = re.subn(r'(?m)^(  "version": ")' + re.escape(old_version) + r'("[,]?)$',
                             lambda m: m[1] + next_version[cid] + m[2], raw)
        assert count == 1, cid
        back = re.sub(r'(?m)^(  "version": ")' + re.escape(next_version[cid]) + r'("[,]?)$',
                      lambda m: m[1] + old_version + m[2], raw)
        for target in sorted(changed - {cid}):
            back = re.sub(r'("id": "' + re.escape(target) + r'",\s*"version": ")' + re.escape(next_version[target]) + '"',
                          lambda m: m[1] + pins[target]["version"] + '"', back)
        for row in prose:
            back = literal_replace(back, row["new"], row["old"])
        assert back == old_raw, cid
        next_name = re.sub(r"(?:\.v\d+)?\.json$", "." + next_version[cid] + ".json", old_path.name)
        assert not (content / next_name).exists(), next_name
        (content / next_name).write_text(raw)
        members.append({"op": "replace", "old": pins[cid], "new": {**pins[cid], "version": next_version[cid]}})
        if any(e == {"id": cid, "version": old_version} for e in package["entrypoints"]):
            entries.append({"op": "replace", "old": {"id": cid, "version": old_version},
                            "new": {"id": cid, "version": next_version[cid]}})
        successors.append({"id": cid, "schema": pins[cid].get("schema"), "old_version": old_version,
                           "new_version": next_version[cid], "predecessor": str(old_path.relative_to(REPO)),
                           "successor_filename": next_name,
                           "reason": "wording" if prose else "pins a replaced citizen",
                           "changed_properties": [r["property"] for r in prose], "rewritten_pins": pin_count,
                           "successor_sha256": hashlib.sha256(raw.encode()).hexdigest(), "byte_undo_proof": True})
    changes = {"package_version": "v107", "release_version": "v105", "members": members,
               "entrypoints": entries}
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n")
    output = {"variant": args.variant, "from": {"core": "v106", "registry": "v104", "release": "v104"},
              "to": {"core": "v107", "registry": "v105", "release": "v105"},
              "wording_citizens": len({r["id"] for r in manifest}), "cascade_levels": [len(level) for level in levels],
              "citizens": len(successors), "member_replacements": len(members),
              "entrypoint_replacements": len(entries), "successors": successors}
    out_path = HERE / f"build-{args.variant}.json"
    try:
        report = generate_to_directory(content / "package.core-calculations.v106.json",
                                       content / "published-packages.v104.json", rel / (STEM + ".v104.json"),
                                       content, scratch / "changes.json", scratch / "generated")
    except SuccessorError as exc:
        output.update({"status": "rejected", "failure": re.sub(r"/(?:Users|private|tmp|var)/\S+", "<path>", str(exc))[:2000]})
        out_path.write_text(json.dumps(output, indent=2) + "\n")
        raise SystemExit(output["failure"])
    for src, dst in (("package.json", content / "package.core-calculations.v107.json"),
                     ("registry.json", content / "published-packages.v105.json"),
                     ("release.json", rel / (STEM + ".v105.json"))):
        shutil.copyfile(scratch / "generated" / src, dst)
    (scratch / "core.json").write_text(json.dumps({"version": "v107", "registry": "v105", "release_version": "v105",
                                                   "content": str(content), "releases": str(rel), "loader_from": "v106"},
                                                  indent=2) + "\n")
    output.update({"status": "valid", "validation": "generate_to_directory passed package, registry and release validation",
                   "generation": {k: v for k, v in report.items() if isinstance(v, (str, int, bool))}
                   if isinstance(report, dict) else str(report)})
    out_path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k != "successors"}, indent=2))


if __name__ == "__main__":
    main()
