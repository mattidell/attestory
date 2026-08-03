"""Launch the synthetic W-2 entry-loop evaluation.

This runner composes the existing Track 1 runtime, adopted surface build, and
loopback server.  It owns no entry or serving behavior of its own.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Event
from typing import Any, Mapping, Sequence

from packages.derivation.entry_loop import (
    ENTRY_FIXTURE,
    EntryLoopServer,
    EntrySnapshot,
    SyntheticW2EntryRuntime,
    build_entry_surface,
)
from packages.derivation.live_workspace import WorkspaceCapability


REPO = Path(__file__).resolve().parents[3]
EVIDENCE_PACK = Path(
    "docs/phases/legible-entry/entry-loop-synthetic-evidence-pack.md"
)


def _evaluation_fixture(repo_root: Path) -> dict[str, Any]:
    body = json.loads(
        (repo_root / ENTRY_FIXTURE / "evaluation-w2.json").read_text("utf-8")
    )
    if not isinstance(body, dict):
        raise ValueError("evaluation fixture must be an object")
    return body


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _starting_state_fingerprint(
    snapshot: EntrySnapshot,
    dist: Path,
    evaluation: Mapping[str, Any],
) -> str:
    visible_state = json.loads(json.dumps(snapshot.payload))
    if not isinstance(visible_state, dict):
        raise ValueError("entry snapshot must be an object")
    visible_state.pop("contributions", None)

    digest = hashlib.sha256()
    digest.update(_canonical({"evaluation": evaluation, "state": visible_state}))
    for path in sorted(candidate for candidate in dist.rglob("*") if candidate.is_file()):
        relative = path.relative_to(dist).as_posix().encode("utf-8")
        contents = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(contents).to_bytes(8, "big"))
        digest.update(contents)
    return digest.hexdigest()


def _print_instructions(
    *,
    url: str,
    fingerprint: str,
    evaluation: Mapping[str, Any],
) -> None:
    entries = evaluation["entries"]
    if not isinstance(entries, dict):
        raise ValueError("evaluation entries must be an object")
    initial = entries["initial"]
    correction = entries["correction"]
    if not isinstance(initial, dict) or not isinstance(correction, dict):
        raise ValueError("evaluation figures must be objects")

    print("Synthetic W-2 entry evaluation")
    print(f"URL: {url}")
    print(f"Evidence pack: {EVIDENCE_PACK.as_posix()}")
    print(f"W-2 Box 1 figure to enter: {initial['box1']}")
    print(f"W-2 Box 1 corrected figure: {correction['box1']}")
    print(f"Starting-state fingerprint: sha256:{fingerprint}")
    print("Stop: press Ctrl-C in this terminal.")
    print("Clean restart: stop this command, then run the same command again.")
    sys.stdout.flush()


def main(_argv: Sequence[str] | None = None) -> int:
    try:
        evaluation = _evaluation_fixture(REPO)
        with TemporaryDirectory(prefix="demo-entry-evaluation-") as temporary:
            capability = WorkspaceCapability(Path(temporary) / "L")
            runtime = SyntheticW2EntryRuntime(capability, repo_root=REPO)
            dist = build_entry_surface(capability, repo_root=REPO)
            fingerprint = _starting_state_fingerprint(
                runtime.snapshot(),
                dist,
                evaluation,
            )
            with EntryLoopServer(runtime, dist) as server:
                _print_instructions(
                    url=server.url,
                    fingerprint=fingerprint,
                    evaluation=evaluation,
                )
                Event().wait()
    except KeyboardInterrupt:
        print("\nStopped. Run the command again for a clean starting state.")
        return 130
    except Exception:
        print("Evaluation launch failed.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
