"""Print the test code the v70 entry-seed generator reaches.

Run from the repository root:

    python3 docs/phases/engine-breadth/milestones/seed-generator-independence-evidence/trace_reach.py

The generator is imported and run in this process. The trace records test
and evidence-harness functions that execute, the module-level constants
their bytecode loads (including a branch this run did not take), and the
other test modules that import the same helpers. Output paths are
repository-relative. Values that look like filesystem paths are omitted.
"""

from __future__ import annotations

import ast
import dis
import hashlib
import importlib
import json
import sys
import traceback
from collections import defaultdict
from pathlib import Path
from types import CodeType, ModuleType
from typing import Any

REPO = Path(__file__).resolve().parents[5]
EVIDENCE = Path(__file__).resolve().parent
TRACE_PATH = EVIDENCE / "trace.json"
GENERATOR = "tools/generate_entry_loop_v70_fixture.py"
THIS_FILE = Path(__file__).resolve()
_LOAD_OPS = frozenset(
    {"LOAD_GLOBAL", "LOAD_NAME", "LOAD_FROM_DICT_OR_GLOBALS"}
)
_SKIP_NAMES = frozenset(
    {
        "None",
        "True",
        "False",
        "annotations",
    }
)


_REPO_PREFIX = str(REPO) + "/"
_REL_CACHE: dict[str, str | None] = {}


def _rel(filename: str) -> str | None:
    if filename in _REL_CACHE:
        return _REL_CACHE[filename]
    if not filename or filename.startswith("<") or not filename.endswith(".py"):
        _REL_CACHE[filename] = None
        return None
    if filename.startswith(_REPO_PREFIX):
        rel = filename[len(_REPO_PREFIX) :]
        _REL_CACHE[filename] = rel
        return rel
    try:
        rel = Path(filename).resolve().relative_to(REPO).as_posix()
    except ValueError:
        rel = None
    _REL_CACHE[filename] = rel
    return rel


def _kind(rel: str | None) -> str | None:
    if rel is None or rel.endswith("trace_reach.py"):
        return None
    if rel == GENERATOR:
        return "generator"
    if rel.startswith("tests/"):
        return "test"
    if rel.startswith("docs/"):
        return "harness"
    return None


def _module_name(rel: str) -> str:
    if rel.startswith("tests/") and rel.endswith(".py"):
        return rel[: -len(".py")].replace("/", ".")
    return rel


def _unsafe(text: str) -> bool:
    norm = text.replace("\\", "/")
    if norm.startswith("/") or norm.startswith("~"):
        return True
    parts = [part for part in norm.split("/") if part]
    return any(part in {"Users", "tmp", "private", "var", "folders"} for part in parts)


def _safe_repr(value: object) -> str | None:
    if isinstance(value, Path) or callable(value) or isinstance(value, ModuleType):
        return None
    if isinstance(value, type):
        return None
    if isinstance(value, str):
        if _unsafe(value):
            return None
        shown = repr(value)
        return shown if len(shown) <= 180 else None
    if isinstance(value, (int, float, bool)) or value is None:
        return repr(value)
    if isinstance(value, (tuple, list)):
        if len(value) > 24:
            return None
        parts: list[str] = []
        for item in value:
            shown = _safe_repr(item)
            if shown is None:
                return None
            parts.append(shown)
        return ("(" if isinstance(value, tuple) else "[") + ", ".join(parts) + (
            ")" if isinstance(value, tuple) else "]"
        )
    if isinstance(value, dict):
        if len(value) > 16:
            return None
        try:
            encoded = json.dumps(value, sort_keys=True, default=str)
        except (TypeError, ValueError):
            return None
        if _unsafe(encoded) or len(encoded) > 180:
            return None
        return encoded
    return None


class _Frame:
    def __init__(self, rel: str, qualname: str, kind: str | None) -> None:
        self.rel = rel
        self.qualname = qualname
        self.kind = kind

    @property
    def label(self) -> str:
        return f"{self.rel}:{self.qualname}"


class _Reach:
    def __init__(self) -> None:
        self.stack: list[_Frame] = []
        self.calls: dict[tuple[str, str], dict[str, Any]] = {}
        self.loads: dict[tuple[str, str], dict[str, Any]] = {}
        self.imports: dict[str, set[str]] = defaultdict(set)
        self._codes: dict[tuple[str, str], CodeType] = {}
        self._globals: dict[int, dict[str, Any]] = {}

    def caller(self) -> _Frame | None:
        return self.stack[-1] if self.stack else None

    def _building_seed(self) -> bool:
        return any(
            frame.rel == GENERATOR
            and frame.qualname in {"seed_acts", "_complete_core_return", "render_fixture_files"}
            for frame in self.stack
        )

    def note_import(self, name: str, reason: str) -> None:
        if name == "tests" or name.startswith("tests."):
            self.imports[name].add(reason)

    def on_start(
        self,
        code: CodeType,
        _offset: int,
        captured_globals: dict[str, Any] | None,
    ) -> None:
        rel = _rel(code.co_filename)
        kind = _kind(rel)
        caller = self.caller()
        if rel is not None and kind in {"test", "harness"}:
            if captured_globals is not None:
                self._globals[id(code)] = captured_globals
            key = (rel, code.co_qualname)
            row = self.calls.get(key)
            if row is None:
                chain = [frame.label for frame in self.stack[-8:]]
                row = {
                    "rel": rel,
                    "module": _module_name(rel),
                    "qualname": code.co_qualname,
                    "kind": kind,
                    "count": 0,
                    "seed_count": 0,
                    "callers": [],
                    "seed_callers": [],
                    "chain": chain,
                    "seed_chain": [],
                    "during_seed": False,
                }
                self.calls[key] = row
            row["count"] += 1
            self._codes[key] = code
            during_seed = self._building_seed()
            if during_seed:
                row["during_seed"] = True
                row["seed_count"] += 1
                if not row["seed_chain"]:
                    row["seed_chain"] = [frame.label for frame in self.stack[-8:]]
            if caller is not None and caller.label not in row["callers"]:
                if len(row["callers"]) < 12:
                    row["callers"].append(caller.label)
            if during_seed and caller is not None and caller.label not in row["seed_callers"]:
                if len(row["seed_callers"]) < 12:
                    row["seed_callers"].append(caller.label)
        if rel is not None:
            self.stack.append(_Frame(rel, code.co_qualname, kind))

    def on_pop(self, code: CodeType, *_args: object) -> None:
        if not self.stack:
            return
        rel = _rel(code.co_filename)
        if rel is None:
            return
        top = self.stack[-1]
        expected = rel
        if top.rel == expected and top.qualname == code.co_qualname:
            self.stack.pop()
            return
        for index in range(len(self.stack) - 1, -1, -1):
            frame = self.stack[index]
            if frame.rel == expected and frame.qualname == code.co_qualname:
                del self.stack[index:]
                return

    def collect_constant_loads(self) -> None:
        """Record module globals each executed function's bytecode loads."""

        seen: set[int] = set()

        def scan(code: CodeType, rel: str, globals_: dict[str, Any] | None) -> None:
            if id(code) in seen:
                return
            seen.add(id(code))
            found = self._globals.get(id(code), globals_)
            for instr in dis.get_instructions(code):
                if instr.opname not in _LOAD_OPS or not isinstance(instr.argval, str):
                    continue
                name = instr.argval
                if name in _SKIP_NAMES or name.startswith("__") or found is None:
                    continue
                if name not in found:
                    continue
                value = found[name]
                if callable(value) or isinstance(value, (ModuleType, type, Path)):
                    continue
                self._note_load(code, rel, name, value=value)
            for const in code.co_consts:
                if isinstance(const, CodeType):
                    scan(const, rel, found)

        for (rel, qualname), code in self._codes.items():
            if qualname == "<module>":
                continue
            scan(code, rel, self._globals.get(id(code)))
        if self._codes and not self.loads:
            raise RuntimeError("executed functions loaded no module constants")

    def _note_load(
        self,
        code: CodeType,
        rel: str,
        name: str,
        *,
        value: object = None,
        imported_from: str | None = None,
    ) -> None:
        if name.startswith("__"):
            return
        shown = _safe_repr(value)
        key = (rel, name)
        row = self.loads.get(key)
        if row is None:
            row = {
                "rel": rel,
                "module": _module_name(rel),
                "name": name,
                "repr": shown,
                "loaders": [],
                "imported_from": imported_from,
            }
            self.loads[key] = row
        elif row["repr"] is None and shown is not None:
            row["repr"] = shown
        if imported_from and not row.get("imported_from"):
            row["imported_from"] = imported_from
        loader = f"{rel}:{code.co_qualname}"
        if loader not in row["loaders"] and len(row["loaders"]) < 16:
            row["loaders"].append(loader)


def _install(reach: _Reach) -> tuple[int, Any]:
    tool_id = next(
        candidate
        for candidate in range(1, 6)
        if sys.monitoring.get_tool(candidate) is None
    )
    sys.monitoring.use_tool_id(tool_id, "seed-generator-independence-trace")
    events = sys.monitoring.events

    def _start(code: CodeType, offset: int) -> None:
        captured = None
        if _kind(_rel(code.co_filename)) in {"test", "harness"}:
            captured = sys._getframe(1).f_globals
        reach.on_start(code, offset, captured)

    def _ret(code: CodeType, offset: int, _retval: object) -> None:
        reach.on_pop(code, offset)

    def _unwind(code: CodeType, offset: int, _exc: object) -> None:
        reach.on_pop(code, offset)

    sys.monitoring.register_callback(tool_id, events.PY_START, _start)
    sys.monitoring.register_callback(tool_id, events.PY_RETURN, _ret)
    sys.monitoring.register_callback(tool_id, events.PY_UNWIND, _unwind)
    sys.monitoring.set_events(
        tool_id,
        events.PY_START | events.PY_RETURN | events.PY_UNWIND,
    )

    class _Hook:
        def find_spec(
            self,
            fullname: str,
            path: object = None,
            target: object = None,
        ) -> None:
            if fullname != "tests" and not fullname.startswith("tests."):
                return None
            reason = "imported while the generator runs"
            for frame in reversed(traceback.extract_stack()[:-1]):
                rel = _rel(frame.filename)
                if rel is None or rel.endswith("trace_reach.py"):
                    continue
                reason = f"imported by {rel}:{frame.name}"
                break
            reach.note_import(fullname, reason)
            return None

    hook = _Hook()
    sys.meta_path.insert(0, hook)
    return tool_id, hook


def _source_spans(rels: set[str]) -> dict[tuple[str, str], dict[str, int]]:
    spans: dict[tuple[str, str], dict[str, int]] = {}

    def walk(node: ast.AST, prefix: str, rel: str, *, inside_function: bool) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if inside_function:
                    qual = f"{prefix}.<locals>.{child.name}"
                else:
                    qual = f"{prefix}.{child.name}" if prefix else child.name
                end = child.end_lineno or child.lineno
                spans[(rel, qual)] = {
                    "start": child.lineno,
                    "end": end,
                    "lines": end - child.lineno + 1,
                }
                walk(child, qual, rel, inside_function=True)
            elif isinstance(child, ast.ClassDef):
                qual = f"{prefix}.{child.name}" if prefix else child.name
                walk(child, qual, rel, inside_function=False)

    for rel in sorted(rels):
        path = REPO / rel
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
        except (OSError, SyntaxError):
            continue
        walk(tree, "", rel, inside_function=False)
    return spans


def _binding_sources(rels: set[str]) -> dict[tuple[str, str], str]:
    found: dict[tuple[str, str], str] = {}
    for rel in sorted(rels):
        path = REPO / rel
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
        except (OSError, SyntaxError):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom) or node.module is None:
                continue
            for alias in node.names:
                bound = alias.asname or alias.name
                found[(rel, bound)] = f"from {node.module} import {alias.name}"
    return found


def _importers(helpers: set[tuple[str, str]]) -> list[dict[str, Any]]:
    by_module: dict[str, set[str]] = defaultdict(set)
    for module, name in helpers:
        by_module[module].add(name)
    rows: list[dict[str, Any]] = []
    roots = [REPO / "tests", REPO / "tools"]
    for root in roots:
        for path in sorted(root.rglob("*.py")):
            rel = path.relative_to(REPO).as_posix()
            if rel.endswith("trace_reach.py"):
                continue
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
            except (OSError, SyntaxError):
                continue
            aliases: dict[str, str] = {}
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module in by_module:
                    names = [
                        alias.name
                        for alias in node.names
                        if alias.name in by_module[node.module] or alias.name == "*"
                    ]
                    if names:
                        rows.append(
                            {
                                "importer": rel,
                                "module": node.module,
                                "names": sorted(set(names)),
                                "lineno": node.lineno,
                            }
                        )
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in by_module:
                            aliases[alias.asname or alias.name] = alias.name
                elif isinstance(node, ast.ImportFrom) and node.module == "tests":
                    for alias in node.names:
                        dotted = f"tests.{alias.name}"
                        if dotted in by_module:
                            aliases[alias.asname or alias.name] = dotted
            if not aliases:
                continue
            used: dict[str, set[str]] = defaultdict(set)
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Attribute)
                    and isinstance(node.value, ast.Name)
                    and node.value.id in aliases
                    and node.attr in by_module[aliases[node.value.id]]
                ):
                    used[aliases[node.value.id]].add(node.attr)
            for module, names in sorted(used.items()):
                rows.append(
                    {
                        "importer": rel,
                        "module": module,
                        "names": sorted(names),
                        "lineno": 0,
                        "via": "attribute",
                    }
                )
    rows.sort(key=lambda row: (row["module"], row["importer"], row["names"]))
    return rows


def _fixture_check(rendered: dict[str, bytes]) -> dict[str, Any]:
    from packages.derivation.entry_loop import CURRENT_CORE_ENTRY_FIXTURE

    root = REPO / CURRENT_CORE_ENTRY_FIXTURE
    files: list[dict[str, Any]] = []
    match = True
    for relative, contents in sorted(rendered.items()):
        committed = root / relative
        same = committed.is_file() and committed.read_bytes() == contents
        match = match and same
        files.append(
            {
                "relative": f"{CURRENT_CORE_ENTRY_FIXTURE.as_posix()}/{relative}",
                "sha256": hashlib.sha256(contents).hexdigest(),
                "bytes": len(contents),
                "matches_committed": same,
            }
        )
    return {"matches_committed_seed": match, "files": files}


def _scan_text(value: object) -> None:
    if isinstance(value, str) and _unsafe(value):
        raise RuntimeError("trace output contained a filesystem path")
    if isinstance(value, dict):
        for item in value.values():
            _scan_text(item)
    elif isinstance(value, list):
        for item in value:
            _scan_text(item)


def _print_group(title: str, rows: list[dict[str, Any]], *, seed: bool) -> None:
    print(f"\n## {title}")
    current = ""
    for row in rows:
        if row["rel"] != current:
            current = row["rel"]
            print(f"\n# {current}")
        callers = ", ".join(row["seed_callers"] if seed else row["callers"]) or "generator entry"
        lines = row.get("lines")
        span = f" lines {row['start']}-{row['end']} ({lines})" if lines else ""
        count = row["seed_count"] if seed else row["count"]
        print(f"- {row['qualname']}{span}  count={count}")
        print(f"  reason: called by {callers}")
        chain = row["seed_chain"] if seed and row.get("seed_chain") else row["chain"]
        if chain:
            print(f"  chain: {' <- '.join(reversed(chain))}")


def _print_constants(title: str, rows: list[dict[str, Any]]) -> None:
    print(f"\n## {title}")
    print("A name is listed when an executed function's bytecode loads it,")
    print("including a branch this run did not take and a nested function.")
    current = ""
    for row in rows:
        if row["rel"] != current:
            current = row["rel"]
            print(f"\n# {current}")
        shown = row["repr"] if row["repr"] is not None else "(value omitted)"
        origin = f"  imported as: {row['imported_from']}" if row.get("imported_from") else ""
        print(f"- {row['name']} = {shown}")
        print(f"  reason: loaded by {', '.join(row['loaders'])}")
        if origin:
            print(origin)


def _called_by_helper(row: dict[str, Any]) -> bool:
    return bool(row["during_seed"]) and any(
        not caller.endswith(":<module>") for caller in row["seed_callers"]
    )


def _print_trace(report: dict[str, Any]) -> None:
    counts = report["counts"]
    print("v70 entry seed generator reach")
    print(f"generator: {GENERATOR}")
    print(f"committed seed matches this run: {report['fixture']['matches_committed_seed']}")
    print(
        "helper functions called while the seed is built: "
        f"{counts['helper_functions']} "
        f"across {counts['helper_modules']} modules, "
        f"{counts['helper_unique_lines']} lines "
        f"({counts['helper_lines']} counting nested functions again)"
    )
    print(
        "helper constants: "
        f"{counts['helper_constants']} "
        f"in {counts['helper_constant_modules']} modules"
    )
    print(
        "evidence-loader functions also called: "
        f"{counts['loader_functions']} ({counts['loader_lines']} lines)"
    )
    print(
        "module bodies that ran during the seed build: "
        f"{counts['module_body_functions']} "
        "(class statements and import-time helpers, not called by the seed)"
    )
    print(
        "functions that ran only because a module was imported beforehand: "
        f"{counts['import_only_functions']}"
    )
    print(f"test modules imported: {counts['imported_test_modules']}")
    _print_group(
        "Helper functions called while the seed is built",
        [row for row in report["functions"] if row.get("helper_call")],
        seed=True,
    )
    _print_constants(
        "Constants loaded by those helper functions",
        [row for row in report["constants"] if row.get("helper_constant")],
    )
    _print_group(
        "Evidence-loader functions called while the probe is loaded",
        [row for row in report["functions"] if row.get("loader_call")],
        seed=True,
    )
    _print_group(
        "Module bodies that ran during the seed build",
        [row for row in report["functions"] if row.get("module_body_during_seed")],
        seed=True,
    )
    _print_group(
        "Functions executed only because a module was imported beforehand",
        [row for row in report["functions"] if not row["during_seed"]],
        seed=False,
    )
    print("\n## Test modules imported")
    for row in report["imports"]:
        used = "executed" if row["executed_function"] else "imported, no function executed"
        print(f"- {row['module']}  ({used})")
        for reason in row["reasons"]:
            print(f"  reason: {reason}")
    print("\n## Other modules that import the same helpers")
    for row in report["importers"]:
        if row["importer"] == GENERATOR:
            continue
        via = " via attribute" if row.get("via") else ""
        print(
            f"- {row['importer']} imports {', '.join(row['names'])} "
            f"from {row['module']}{via}"
        )


def main() -> None:
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    reach = _Reach()
    tool_id, hook = _install(reach)
    reach.stack.append(_Frame(TRACE_PATH.parent.name + "/trace_reach.py", "main", None))
    try:
        generator = importlib.import_module("tools.generate_entry_loop_v70_fixture")
        rendered = generator.render_fixture_files()
    finally:
        sys.monitoring.set_events(tool_id, 0)
        if hook in sys.meta_path:
            sys.meta_path.remove(hook)
    reach.collect_constant_loads()

    functions = [
        row
        for row in reach.calls.values()
        if row["qualname"] != "<module>"
    ]
    functions.sort(key=lambda row: (row["rel"], row["qualname"]))
    spans = _source_spans({row["rel"] for row in functions})
    for row in functions:
        span = spans.get((row["rel"], row["qualname"]))
        if span is not None:
            row.update(span)
        elif "<locals>" in row["qualname"]:
            row["lines"] = None

    executed_rels = {row["rel"] for row in reach.calls.values()}
    bindings = _binding_sources(executed_rels)
    constants = []
    for key, row in reach.loads.items():
        if key[0] not in executed_rels:
            continue
        # A load during module import is part of arriving at the module.
        # Keep it when an executed function also loaded it, or when the
        # loader is any code object in a module that executed a function.
        loaders = [
            loader
            for loader in row["loaders"]
            if not loader.endswith(":<module>")
        ]
        if not loaders:
            continue
        copied = dict(row)
        copied["loaders"] = loaders
        binding = bindings.get((row["rel"], row["name"]))
        if binding and not copied.get("imported_from"):
            copied["imported_from"] = binding
        constants.append(copied)
    seed_keys = {
        (row["rel"], row["qualname"])
        for row in functions
        if row["during_seed"]
    }

    def _loader_during_seed(loader: str) -> bool:
        rel, _, qualname = loader.partition(":")
        if (rel, qualname) in seed_keys:
            return True
        parent = qualname.split(".<locals>", 1)[0]
        return (rel, parent) in seed_keys

    for row in functions:
        loader = row["rel"] == "tests/evidence_loader.py"
        helper = _called_by_helper(row) and not loader
        row["helper_call"] = helper
        row["loader_call"] = bool(row["during_seed"]) and loader and _called_by_helper(row)
        row["module_body_during_seed"] = (
            bool(row["during_seed"]) and not helper and not row["loader_call"]
        )
    helper_loader_names = {
        f"{row['rel']}:{row['qualname']}" for row in functions if row.get("helper_call")
    }

    def _loader_is_helper(loader: str) -> bool:
        if loader in helper_loader_names:
            return True
        rel, _, qualname = loader.partition(":")
        parent = qualname.split(".<locals>", 1)[0]
        return f"{rel}:{parent}" in helper_loader_names

    for row in constants:
        row["during_seed"] = any(_loader_during_seed(loader) for loader in row["loaders"])
        row["helper_constant"] = any(_loader_is_helper(loader) for loader in row["loaders"])
    constants.sort(key=lambda row: (row["rel"], row["name"]))

    executed_modules = {row["module"] for row in functions if row["kind"] == "test"}
    seed_functions = [row for row in functions if row["during_seed"]]
    helper_functions = [row for row in functions if row["helper_call"]]
    loader_functions = [row for row in functions if row["loader_call"]]
    module_body_functions = [row for row in functions if row["module_body_during_seed"]]
    helper_keys = {
        (row["module"], row["qualname"].split(".")[-1])
        for row in helper_functions
        if row["kind"] == "test" and "<locals>" not in row["qualname"]
    }
    seed_constants = [row for row in constants if row["during_seed"]]
    imports = [
        {
            "module": name,
            "reasons": sorted(reasons),
            "executed_function": name in executed_modules,
        }
        for name, reasons in sorted(reach.imports.items())
    ]
    known_imports = {row["module"] for row in imports}
    for row in seed_functions:
        if row["kind"] != "test" or row["module"] in known_imports:
            continue
        reason = "loaded by path while the seed is built"
        if row.get("seed_chain"):
            reason = f"loaded by path; called from {row['seed_chain'][-1]}"
        imports.append(
            {
                "module": row["module"],
                "reasons": [reason],
                "executed_function": True,
                "loaded_by_path": True,
            }
        )
        known_imports.add(row["module"])
    imports.sort(key=lambda row: row["module"])
    modules_with_functions = {row["module"] for row in functions if row["kind"] == "test"}
    report = {
        "generator": GENERATOR,
        "fixture": _fixture_check(rendered),
        "counts": {
            "executed_functions": len(functions),
            "executed_modules": len({row["rel"] for row in functions}),
            "executed_lines": sum(row.get("lines") or 0 for row in functions),
            "seed_functions": len(seed_functions),
            "seed_modules": len({row["rel"] for row in seed_functions}),
            "seed_lines": sum(row.get("lines") or 0 for row in seed_functions),
            "import_only_functions": len(functions) - len(seed_functions),
            "constants": len(constants),
            "constant_modules": len({row["rel"] for row in constants}),
            "seed_constants": len(seed_constants),
            "seed_constant_modules": len({row["rel"] for row in seed_constants}),
            "helper_functions": len(helper_functions),
            "helper_modules": len({row["rel"] for row in helper_functions}),
            "helper_lines": sum(row.get("lines") or 0 for row in helper_functions),
            "helper_unique_lines": sum(
                (row.get("lines") or 0)
                for row in helper_functions
                if "<locals>" not in row["qualname"]
            ),
            "helper_constants": sum(1 for row in constants if row.get("helper_constant")),
            "helper_constant_modules": len(
                {row["rel"] for row in constants if row.get("helper_constant")}
            ),
            "loader_functions": len(loader_functions),
            "loader_lines": sum(row.get("lines") or 0 for row in loader_functions),
            "module_body_functions": len(module_body_functions),
            "imported_test_modules": len(imports),
            "test_modules_with_executed_functions": len(modules_with_functions),
        },
        "functions": functions,
        "constants": constants,
        "imports": imports,
        "importers": _importers(helper_keys),
    }
    _scan_text(report)
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    _scan_text(json.loads(text))
    TRACE_PATH.write_text(text, encoding="utf-8")
    _print_trace(report)
    print(f"\nwrote {TRACE_PATH.relative_to(REPO).as_posix()}")
    if not report["fixture"]["matches_committed_seed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
