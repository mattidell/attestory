"""Emit the executed evidence record as markdown.

    python3 -m prototype.reported_interest.run
"""

from __future__ import annotations

from .model import CASES
from .rubric import (
    ACCESS_MODES,
    RUBRIC,
    currentness_probe,
    independent_lifecycle,
    later_year_probe,
    run_shape,
)
from .shapes import SHAPES, project_line_2b

SHAPE_LABELS = {
    "A": "artifact-alone",
    "C": "embedded-composite",
    "E": "relationship-edge",
    "B": "explicit determination",
}


def _outcome(run: object) -> str:
    from .rubric import ShapeRun

    assert isinstance(run, ShapeRun)
    if run.is_blocked:
        assert run.blocked is not None
        missing = (
            f" ({', '.join(m.rsplit('.', 1)[-1] for m in run.blocked.missing)})"
            if run.blocked.missing
            else ""
        )
        return f"blocked: {run.blocked.code}{missing}"
    assert run.item is not None
    return f"line 2b = {project_line_2b(run.store, run.item, run.workspace)}"


def main() -> None:
    print("## Case outcomes\n")
    print("| Case | " + " | ".join(SHAPE_LABELS) + " |")
    print("| --- | " + " | ".join("---" for _ in SHAPE_LABELS) + " |")
    for case, make in CASES.items():
        ws = make()
        cells = [_outcome(run_shape(shape, ws)) for shape in SHAPE_LABELS]
        print(f"| {case} | {' | '.join(cells)} |")

    print("\n## Rubric failures\n")
    any_failure = False
    for case, make in CASES.items():
        ws = make()
        for shape in SHAPE_LABELS:
            run = run_shape(shape, ws)
            for check_name, check in RUBRIC.items():
                passed, detail = check(run)
                if not passed:
                    any_failure = True
                    print(f"- **FAIL {case} / shape {shape} / {check_name}** — {detail}")
    if not any_failure:
        print("- no failures")

    print("\n## Separate-rule provenance\n")
    run = run_shape("A", CASES["TI-B2"]())
    for art in run.artifacts():
        print(f"- {art.kind}: rule={art.provenance.rule_id}.v{art.provenance.rule_version} reads={list(art.provenance.reads)}")

    print("\n## Lifecycle (in_provenance iff displaced)\n")
    for label, (passed, detail) in independent_lifecycle().items():
        if not passed:
            print(f"- FAIL — {label}: {detail}")
    print("- all per-artifact displacement observations match provenance")

    print("\n## Later-year consumer\n")
    probe = later_year_probe()
    for shape in SHAPE_LABELS:
        for access in ACCESS_MODES:
            print(f"- {shape}/{access}: `{probe[f'{shape}/{access}: passed']}`")


if __name__ == "__main__":
    main()
