"""Render the active milestone's temporary initial-briefing follow-up capsule."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.foreman_context import (
    ContextError,
    GitRepository,
    load_document,
    render_context,
    validate_initial_briefing_follow_up,
)


def parse_arguments(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", required=True, help="explicit Git revision to read")
    parser.add_argument("--repo", default=".", help="repository root (default: current directory)")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="skip the automatic `git fetch origin`",
    )
    return parser.parse_args(argv)


def markdown_capsule(capsule: dict[str, Any], source_ref: str) -> str:
    lines = [
        "# Initial briefing follow-up (temporary)",
        "",
        f"- Topic: `{capsule['topic']}`",
        f"- Selected ref: `{source_ref}`",
        f"- Grounding commit: `{capsule['grounding_commit']}`",
        "- Expires: milestone close",
        "",
        "## Guidance",
        "",
    ]
    for note in capsule["notes"]:
        lines.append(f"- {note}")
    lines.extend(["", "## Grounding sources", ""])
    for source in capsule["sources"]:
        lines.append(f"- `{source['path']}` @ `{source['blob']}`")
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
    repository = GitRepository(Path(arguments.repo).resolve())
    if not arguments.no_fetch:
        repository.fetch()
    try:
        context = render_context(repository, arguments.ref)
        state = context["state"]
        if not state["initial_briefing_follow_up"]:
            raise ContextError(
                f"{state['active_plan']} has no active initial briefing follow-up capsule"
            )
        plan = load_document(
            repository, context["source"]["commit"], state["active_plan"]
        )
        capsule = validate_initial_briefing_follow_up(
            repository, plan, state["topic"], context["milestone"]
        )
        if capsule is None:
            raise ContextError("initial briefing follow-up capsule disappeared during validation")
    except ContextError as error:
        print(f"foreman context follow-up: {error}", file=sys.stderr)
        return 2
    if arguments.format == "json":
        print(json.dumps(capsule, indent=2, sort_keys=True))
    else:
        print(markdown_capsule(capsule, arguments.ref), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
