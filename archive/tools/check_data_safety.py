#!/usr/bin/env python3

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PATH_PREFIXES = (
    "tax-docs/",
    "prior-returns/",
    "state/",
    "temp/",
    "definitions/facts/",
    "definitions/input/",
    "generated/",
)

FORBIDDEN_FILE_PATTERNS = (
    "*.current.*.json",
    "*Return*.pdf",
    "*Returns*.pdf",
)


def tracked_or_worktree_paths(root: Path = ROOT) -> list[Path]:
    return [
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts
    ]


def find_forbidden_paths(root: Path = ROOT) -> list[str]:
    violations = []
    for path in tracked_or_worktree_paths(root):
        normalized = path.as_posix()
        if any(normalized.startswith(prefix) for prefix in FORBIDDEN_PATH_PREFIXES):
            violations.append(normalized)
            continue
        if any(path.match(pattern) for pattern in FORBIDDEN_FILE_PATTERNS):
            violations.append(normalized)
    return sorted(violations)


def main() -> int:
    violations = find_forbidden_paths()
    if violations:
        print("Personal-data guardrail violations:")
        for violation in violations:
            print(f"- {violation}")
        return 1
    print("No personal-data guardrail violations found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
