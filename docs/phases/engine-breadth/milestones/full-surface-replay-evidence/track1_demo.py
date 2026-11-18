"""Track 1 demonstration: full-surface replay of every recorded list.

Run: python3 track1_demo.py identity|v95v96 <part-file-outside-repo> [--workers N]
  identity  core v96 against core v96 (every list must be identical)
  v95v96    core v95 against core v96 with plain-line-texts' declared changes

The declared changes are read from the plain-line-texts evidence: every
replaced sentence (p0c-wording.json, repair-wording.json, chained where the
repair replaced a sentence the first pass had replaced) and every successor
version (p0c-validation.json, repair-validation.json) plus the package
adoption pin.  Nothing else is expected.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from tools import recorded_replay as rr  # noqa: E402

PLT = HERE.parent / "plain-line-texts-evidence"


def declared_expectations() -> list[rr.Expectation]:
    texts: dict[tuple[str, str], list[str]] = {}
    for name in ("p0c-wording.json", "repair-wording.json"):
        for row in json.loads((PLT / name).read_text())["replacements"]:
            attribute = row["property"]
            old, new = (row["shown"], row["new_shown"]) if attribute == "title" else (row["old"], row["new"])
            slot = texts.get((row["id"], attribute))
            if slot is not None and slot[1] == old:
                slot[1] = new  # the repair replaced a sentence the first pass replaced
            else:
                texts[(row["id"], attribute)] = [old, new]
    out = [rr.text_change(cid, attribute, old, new) for (cid, attribute), (old, new) in sorted(texts.items())]
    versions = {"tax.us.2025.package.core-calculations": ("v95", "v96")}
    for name in ("p0c-validation.json", "repair-validation.json"):
        for row in json.loads((PLT / name).read_text())["successors"]:
            versions[row["id"]] = (row["old_version"], row["new_version"])
    out += [rr.version_change(cid, old, new) for cid, (old, new) in sorted(versions.items())]
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("identity", "v95v96"))
    parser.add_argument("part", type=Path)
    parser.add_argument("--workers", type=int, default=None)
    args = parser.parse_args()
    assert REPO not in args.part.resolve().parents
    cores = ("v96", "v96") if args.mode == "identity" else ("v95", "v96")
    expectations = [] if args.mode == "identity" else declared_expectations()
    lists = rr.recorded_lists()
    assert len(lists) == 775
    from tests import evidence_loader
    owner = evidence_loader.current_owner()
    if owner:
        evidence_loader.release(owner)
    started = time.monotonic()
    summary = rr.run_full(*cores, expectations, workers=args.workers, part=args.part, lists=lists)
    summary["wall_time_s"] = round(time.monotonic() - started, 1)
    summary["expectations_declared"] = len(expectations)
    name = "track1-identity.json" if args.mode == "identity" else "track1-v95-v96.json"
    text = json.dumps(summary, indent=1) + "\n"
    rr._check_no_local_paths(text, name)
    (HERE / name).write_text(text)
    print(json.dumps({k: summary[k] for k in ("lists", "classes", "passing", "failing", "unexpected_differences", "wall_time_s")}, indent=1))


if __name__ == "__main__":
    main()
