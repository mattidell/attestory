"""Track 1: generate core v109, registry v107 and release v107 from published v108.

Run from the repository root, with a new directory outside the repository:
  python3 docs/phases/engine-breadth/milestones/line16-next-step-evidence/track1_build.py <new-dir> [--publish]

The change set is scratch_build.changes() (P0): schema artifact-package.v45,
the four answer-explanation.v1 citizens added as members and entrypoints, and
answer-explanation.v1 added to the admitted schemas. The four citizen files
are already in packages/content (they are the P0 scratch files, byte for
byte). tools.package_successor validates and writes the three generated
files to <new-dir>; --publish then copies them into packages/, refusing to
overwrite anything. Writes track1-build.json here.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from tools.package_successor import generate_to_directory  # noqa: E402

_spec = importlib.util.spec_from_file_location("l16ns_scratch_build", HERE / "scratch_build.py")
assert _spec is not None and _spec.loader is not None
sb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sb)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scratch")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    scratch = Path(args.scratch).resolve()
    assert REPO not in scratch.parents and not scratch.exists()
    scratch.mkdir(parents=True)
    content, releases = REPO / sb.CONTENT, REPO / sb.RELEASES
    (scratch / "changes.json").write_text(json.dumps(sb.changes(), indent=2) + "\n", encoding="utf-8")
    report = generate_to_directory(content / f"package.core-calculations.{sb.FROM['core']}.json",
                                   content / f"published-packages.{sb.FROM['registry']}.json",
                                   releases / f"{sb.STEM}.{sb.FROM['release']}.json",
                                   content, scratch / "changes.json", scratch / "generated")
    targets = {"package.json": content / f"package.core-calculations.{sb.TO['core']}.json",
               "registry.json": content / f"published-packages.{sb.TO['registry']}.json",
               "release.json": releases / f"{sb.STEM}.{sb.TO['release']}.json"}
    digests = {dst.name: hashlib.sha256((scratch / "generated" / src).read_bytes()).hexdigest()
               for src, dst in targets.items()}
    p0 = json.loads((HERE / "scratch-build.json").read_text(encoding="utf-8"))["generated_sha256"]
    citizens = {}
    for slug in sb.SLUGS:
        name = f"answer-explanation.exception1-{slug}-no.v1.json"
        citizens[name] = hashlib.sha256((content / name).read_bytes()).hexdigest()
    record = {"from": sb.FROM, "to": sb.TO, "changes": sb.changes(), "status": "valid",
              "validation": "tools.package_successor.generate_to_directory validated package, registry and release",
              "generated_sha256": digests, "same_as_p0_scratch": digests == p0, "citizen_sha256": citizens,
              "generation": {k: v for k, v in report.items() if isinstance(v, (str, int, bool))}}
    if args.publish:
        for src, dst in targets.items():
            assert not dst.exists(), dst.name
            shutil.copyfile(scratch / "generated" / src, dst)
        record["published"] = sorted(dst.name for dst in targets.values())
    text = json.dumps(record, indent=2) + "\n"
    for root in ("Users", "private", "tmp", "var"):
        assert "/" + root + "/" not in text, "local path in record"
    (HERE / "track1-build.json").write_text(text, encoding="utf-8")
    print(json.dumps({k: v for k, v in record.items() if k != "changes"}, indent=2))


if __name__ == "__main__":
    main()
