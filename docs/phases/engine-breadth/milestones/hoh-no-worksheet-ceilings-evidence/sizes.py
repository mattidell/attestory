"""Measure the scratch worksheet successors against the fast size guard.

Run: python3 sizes.py <scratch-content-directory> --out sizes.json

Imports tests/test_content_file_sizes.py and points it at the scratch content
copy, which holds published content plus the two successor files. The guard's
worksheet set is the unversioned line files only, so a v2 filename fails that
equality. Byte sizes are also compared with the worksheet cap (6 KiB) on
their own. Nothing under packages/ or tests/ is edited.
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))

FILES = (
    "rule.qdcg-worksheet.line-6.v2.json",
    "rule.qdcg-worksheet.line-13.v2.json",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("content", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    content = args.content.resolve()
    if not content.is_dir():
        raise SystemExit("content directory is missing")
    sizes = importlib.import_module("tests.test_content_file_sizes")
    sizes.CONTENT = content
    names = {path.name for path in content.glob("rule.qdcg-worksheet.*.json")}
    extra = sorted(names - sizes.WORKSHEET_NAMES)
    missing = sorted(sizes.WORKSHEET_NAMES - names)
    cap = sizes.WORKSHEET_CAP
    measured = {}
    for name in FILES:
        path = content / name
        size = path.stat().st_size
        measured[name] = {"bytes": size, "cap": cap, "within_cap": size <= cap}
    try:
        sizes.test_content_rule_files_stay_within_their_caps()
        guard = "passed"
    except AssertionError as exc:
        guard = str(exc).strip() or "AssertionError"
    body = {
        "guard": "tests.test_content_file_sizes.test_content_rule_files_stay_within_their_caps",
        "result": guard,
        "worksheet_cap": cap,
        "set_extra": extra,
        "set_missing": missing,
        "files": measured,
    }
    text = json.dumps(body, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"sizes output contains {needle}")
    args.out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
