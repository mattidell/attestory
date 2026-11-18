"""Scratch core v97 from published v96: the two sale reasons, plus every forced cascade.

Run: python3 srp_build.py <new-directory-outside-repository>

The reasons live in source-family citizens (member_constraints[].meaning).
A new family version is pinned by {"id", "version"} in other citizens, so
every package member that pins a replaced citizen is itself replaced, until
the set is closed. Each successor differs from its predecessor only by the
declared prose, its root version and pinned versions of replaced citizens;
undoing exactly those recovers every predecessor byte. No production
content changes; the generated package, registry and release are validated
by tools.package_successor.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from tools.package_successor import generate_to_directory, SuccessorError

STEM = "demo.release.sli-worksheet-integration.2025"


def literal_replace(raw, old, new):
    before, after = json.dumps(old, ensure_ascii=False), json.dumps(new, ensure_ascii=False)
    assert raw.count(before) == 1, "ambiguous or absent prose literal"
    return raw.replace(before, after, 1)


def pinned(node, targets, found):
    if isinstance(node, dict):
        if (node.get("id"), node.get("version")) in targets: found.append((node["id"], node["version"]))
        for value in node.values(): pinned(value, targets, found)
    elif isinstance(node, list):
        for value in node: pinned(value, targets, found)


def main():
    scratch = Path(sys.argv[1]).resolve()
    assert REPO not in scratch.parents and not scratch.exists()
    source = REPO / "packages/content/tax/2025"
    releases = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
    content, rel = scratch / "content", scratch / "releases"
    shutil.copytree(source, content); shutil.copytree(releases, rel)
    manifest = json.loads((HERE / "wording.json").read_text())["replacements"]
    package = json.loads((source / "package.core-calculations.v96.json").read_text())
    pins = {m["id"]: m for m in package["members"]}
    files, existing = {}, {}
    for path in source.glob("*.json"):
        body = json.loads(path.read_text())
        if isinstance(body, dict) and re.fullmatch(r"v\d+", str(body.get("version"))):
            files[(body.get("id"), body["version"])] = path
            existing.setdefault(body.get("id"), set()).add(int(body["version"][1:]))
    member_bodies = {mid: json.loads(files[(mid, m["version"])].read_text()) for mid, m in pins.items()
                     if (mid, m["version"]) in files}
    # Close the replacement set over version pins.
    changed = {r["id"] for r in manifest}
    levels = [sorted(changed)]
    while True:
        targets = {(i, pins[i]["version"]) for i in changed}
        new = set()
        for mid, body in member_bodies.items():
            if mid in changed: continue
            found = []
            for key, value in body.items():
                if key != "id": pinned(value, targets, found)
            if found: new.add(mid)
        if not new: break
        levels.append(sorted(new)); changed |= new
    next_version = {i: "v" + str(max(existing[i]) + 1) for i in changed}
    members, entries, successors = [], [], []
    for cid in sorted(changed):
        old_version = pins[cid]["version"]
        old_path = files[(cid, old_version)]
        raw = old_raw = old_path.read_text()
        old = json.loads(raw)
        prose = [r for r in manifest if r["id"] == cid]
        for row in prose: raw = literal_replace(raw, row["old"], row["new"])
        # Pinned references to replaced citizens: rewrite each {"id": X, "version": vN} pair.
        pin_count = 0
        for target in sorted(changed - {cid}):
            pattern = re.compile(r'("id": "' + re.escape(target) + r'",\s*"version": ")' + re.escape(pins[target]["version"]) + '"')
            raw, n = pattern.subn(lambda m: m[1] + next_version[target] + '"', raw)
            pin_count += n
        found = []
        for key, value in old.items():
            if key != "id": pinned(value, {(t, pins[t]["version"]) for t in changed - {cid}}, found)
        assert pin_count == len(found), (cid, pin_count, found)
        raw, count = re.subn(r'(?m)^(  "version": ")' + re.escape(old_version) + r'("[,]?)$',
                             lambda m: m[1] + next_version[cid] + m[2], raw)
        assert count == 1
        # Byte-undo proof: reverse root version, pins and prose.
        back = re.sub(r'(?m)^(  "version": ")' + re.escape(next_version[cid]) + r'("[,]?)$', lambda m: m[1] + old_version + m[2], raw)
        for target in sorted(changed - {cid}):
            back = re.sub(r'("id": "' + re.escape(target) + r'",\s*"version": ")' + re.escape(next_version[target]) + '"',
                          lambda m: m[1] + pins[target]["version"] + '"', back)
        for row in prose: back = literal_replace(back, row["new"], row["old"])
        assert back == old_raw, cid
        next_name = re.sub(r"(?:\.v\d+)?\.json$", "." + next_version[cid] + ".json", old_path.name)
        assert not (content / next_name).exists(), next_name
        (content / next_name).write_text(raw)
        new_pin = {**pins[cid], "version": next_version[cid]}
        members.append({"op": "replace", "old": pins[cid], "new": new_pin})
        if any(e == {"id": cid, "version": old_version} for e in package["entrypoints"]):
            entries.append({"op": "replace", "old": {"id": cid, "version": old_version},
                            "new": {"id": cid, "version": next_version[cid]}})
        successors.append({"id": cid, "schema": pins[cid].get("schema"), "old_version": old_version,
            "new_version": next_version[cid], "predecessor": str(old_path.relative_to(REPO)),
            "successor_filename": next_name, "reason": "wording" if prose else "pins a replaced citizen",
            "changed_properties": [r["property"] for r in prose], "rewritten_pins": pin_count,
            "successor_sha256": hashlib.sha256(raw.encode()).hexdigest(), "byte_undo_proof": True})
    changes = {"package_version": "v97", "release_version": "v95", "members": members,
               "entrypoints": entries, "registry_sort": "id_version"}
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n")
    output = {"from": {"core": "v96", "registry": "v94", "release": "v94"},
              "to": {"core": "v97", "registry": "v95", "release": "v95"},
              "wording_citizens": len({r["id"] for r in manifest}), "cascade_levels": [len(l) for l in levels],
              "citizens": len(successors), "member_replacements": len(members),
              "entrypoint_replacements": len(entries), "successors": successors}
    try:
        report = generate_to_directory(content / "package.core-calculations.v96.json",
            content / "published-packages.v94.json", rel / (STEM + ".v94.json"),
            content, scratch / "changes.json", scratch / "generated")
    except SuccessorError as exc:
        output.update({"status": "rejected", "failure": re.sub(r"/(?:Users|private|tmp|var)/\S+", "<path>", str(exc))[:2000]})
        (HERE / "build.json").write_text(json.dumps(output, indent=2) + "\n")
        raise SystemExit(output["failure"])
    for src, dst in (("package.json", content / "package.core-calculations.v97.json"),
                     ("registry.json", content / "published-packages.v95.json"),
                     ("release.json", rel / (STEM + ".v95.json"))):
        shutil.copyfile(scratch / "generated" / src, dst)
    (scratch / "core.json").write_text(json.dumps({"version": "v97", "registry": "v95", "release_version": "v95",
        "content": str(content), "releases": str(rel), "loader_from": "v96"}, indent=2) + "\n")
    output.update({"status": "valid", "validation": "generate_to_directory passed package, registry and release validation",
                   "generation": {k: v for k, v in report.items() if isinstance(v, (str, int, bool))} if isinstance(report, dict) else str(report)})
    (HERE / "build.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k != "successors"}, indent=2))


if __name__ == "__main__": main()
