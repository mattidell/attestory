"""Copy the v70 seed's reached helpers into a non-test package.

Reads ``trace.json`` and the helper sources. Writes
``move/seed_helpers/``. Copies only the top-level functions the trace marks
as helper calls, the assignments those functions need, and the imports that
bind those names. Test-module imports are rewritten to ``seed_helpers``.
Two functions are replaced so the copy does not load a test file:

- ``_probe`` imports the copied probe module instead of the evidence loader.
- ``_sdd`` imports the copied senior-deduction module instead of loading a
  test file by path.

Names a copied function mentions but this seed never calls stay unresolved.
Using one of them would raise ``NameError``. That is the untaken-branch
limit of this prototype.
"""

from __future__ import annotations

import ast
import builtins
import json
from pathlib import Path
from typing import Any


def _text_has_machine_path(text: str) -> bool:
    norm = text.replace("\\", "/")
    if norm.startswith("/") or norm.startswith("~"):
        return True
    parts = [part for part in norm.split("/") if part]
    return any(part in _PATH_PARTS for part in parts)


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "packages" / "kernel" / "__init__.py").is_file() and (
            parent / "tests"
        ).is_dir():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _repo_root()
EVIDENCE = Path(__file__).resolve().parent
TRACE_PATH = EVIDENCE / "trace.json"
PACKAGE = EVIDENCE / "move" / "seed_helpers"
BUILTIN_NAMES = set(dir(builtins))
_PATH_PARTS = {"Users", "tmp", "private", "var", "folders"}

PROBE_REL = (
    "docs/phases/engine-breadth/milestones/tax-on-taxable-income-evidence/probe.py"
)
TOTI_REL = "tests/test_tax_on_taxable_income_track1.py"
REFUND_REL = "tests/test_refund_or_amount_owed_track1.py"

REPLACEMENTS = {
    (TOTI_REL, "_probe"): '''def _probe() -> Any:
    import seed_helpers.probe as probe_module
    return probe_module
''',
    (REFUND_REL, "_sdd"): '''def _sdd() -> Any:
    import seed_helpers.test_senior_and_dependent_deductions_track1 as module
    return module
''',
}

# The refund finisher calls this on the probe module. The probe's own
# copied functions never mention the name, so the import has to be forced.
FORCE_NAMES = {PROBE_REL: ["_load_fixture_adoption"]}


def _args(node: ast.AST) -> set[str]:
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        return set()
    args = node.args
    names = {arg.arg for arg in (*args.posonlyargs, *args.args, *args.kwonlyargs)}
    if args.vararg:
        names.add(args.vararg.arg)
    if args.kwarg:
        names.add(args.kwarg.arg)
    return names


def free_names(node: ast.AST) -> set[str]:
    """Names a statement loads from the module, ignoring nested locals."""

    loads: set[str] = set()
    stores: set[str] = set()
    defined: set[str] = set()
    arguments: set[str] = set()
    declared_global: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            if isinstance(child.ctx, ast.Load):
                loads.add(child.id)
            else:
                stores.add(child.id)
        elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined.add(child.name)
            if child is not node:
                arguments.update(_args(child))
        elif isinstance(child, ast.Lambda):
            arguments.update(_args(child))
        elif isinstance(child, ast.Global):
            declared_global.update(child.names)
        elif isinstance(child, ast.ExceptHandler) and child.name:
            stores.add(child.name)
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        arguments.update(_args(node))
        defined.discard(getattr(node, "name", ""))
    free = (loads - stores - defined - arguments - BUILTIN_NAMES) | (
        declared_global & loads
    )
    return {name for name in free if not (name.startswith("__") and name.endswith("__"))}


def _is_root_assign(node: ast.AST, segment: str) -> bool:
    if not isinstance(node, ast.Assign) or len(node.targets) != 1:
        return False
    target = node.targets[0]
    if not isinstance(target, ast.Name) or target.id not in {"ROOT", "REPO"}:
        return False
    return "Path(__file__)" in segment and ".resolve()" in segment


class Module:
    def __init__(self, rel: str, text: str, copy_fns: set[str]) -> None:
        self.rel = rel
        self.stem = Path(rel).stem
        self.lines = text.splitlines()
        self.tree = ast.parse(text)
        self.copy_fns = set(copy_fns)
        self.binders: dict[str, tuple[Any, ...]] = {}
        self.functions: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = {}
        for node in self.tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.functions[node.name] = node
                self.binders[node.name] = ("func", node)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.binders[target.id] = ("assign", node)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                self.binders[node.target.id] = ("assign", node)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    self.binders[alias.asname or alias.name.split(".")[0]] = (
                        "import",
                        node,
                        alias,
                    )
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name == "*":
                        continue
                    self.binders[alias.asname or alias.name] = ("import", node, alias)
        self.needed: set[str] = set(FORCE_NAMES.get(rel, []))
        self.include_assign: set[int] = set()
        self.include_alias: set[tuple[int, str]] = set()
        self.inlines: list[str] = []
        self.satisfied: set[str] = set(self.copy_fns)
        self.unresolved: set[str] = set()
        for name in self.copy_fns:
            source = self._function_tree(name)
            self.needed.update(free_names(source))

    def segment(self, node: ast.AST) -> str:
        if not hasattr(node, "lineno"):
            return ""
        return "\n".join(self.lines[node.lineno - 1 : node.end_lineno])

    def _function_tree(self, name: str) -> ast.AST:
        replacement = REPLACEMENTS.get((self.rel, name))
        if replacement is not None:
            return ast.parse(replacement).body[0]
        return self.functions[name]


def _dotted(rel: str) -> str:
    return ".".join(Path(rel).with_suffix("").parts)


def _classify(node: ast.AST, alias: ast.alias, dotted: dict[str, str]) -> tuple[Any, ...]:
    if isinstance(node, ast.Import):
        if alias.name in dotted:
            return ("seed-module", dotted[alias.name], alias.asname)
        return ("plain-import", alias.name, alias.asname)
    if not isinstance(node, ast.ImportFrom):
        raise RuntimeError("not an import")
    if node.level:
        return ("relative", node.module or "", alias.name, alias.asname)
    module = node.module or ""
    if module in dotted:
        return ("seed-name", dotted[module], alias.name, alias.asname)
    full = f"{module}.{alias.name}" if module else alias.name
    if full in dotted:
        return ("seed-module", dotted[full], alias.asname)
    return ("plain-from", module, alias.name, alias.asname)


def _emit_alias(kind: tuple[Any, ...]) -> str:
    tag = kind[0]
    if tag == "seed-module":
        stem, asname = kind[1], kind[2]
        if asname and asname != stem:
            return f"import seed_helpers.{stem} as {asname}"
        return f"import seed_helpers.{stem} as {stem}"
    if tag == "plain-import":
        name, asname = kind[1], kind[2]
        if asname:
            return f"import {name} as {asname}"
        return f"import {name}"
    if tag == "seed-name":
        stem, original, asname = kind[1], kind[2], kind[3]
        if asname:
            return f"from seed_helpers.{stem} import {original} as {asname}"
        return f"from seed_helpers.{stem} import {original}"
    if tag == "plain-from":
        module, original, asname = kind[1], kind[2], kind[3]
        binding = f"{original} as {asname}" if asname else original
        return f"from {module} import {binding}"
    raise RuntimeError(f"cannot emit import kind {tag}")


def _resolve(modules: dict[str, Module], dotted: dict[str, str]) -> None:
    pending_exports: dict[str, set[str]] = {rel: set() for rel in modules}
    for _ in range(40):
        changed = False
        for rel, module in modules.items():
            for name in list(module.needed):
                if name in module.satisfied or name in module.unresolved:
                    continue
                binder = module.binders.get(name)
                if binder is None:
                    module.unresolved.add(name)
                    changed = True
                    continue
                kind = binder[0]
                if kind == "func":
                    if name in module.copy_fns:
                        module.satisfied.add(name)
                        changed = True
                    else:
                        module.unresolved.add(name)
                        changed = True
                elif kind == "assign":
                    node = binder[1]
                    if id(node) not in module.include_assign:
                        module.include_assign.add(id(node))
                        segment = module.segment(node)
                        if not _is_root_assign(node, segment):
                            module.needed.update(free_names(node))
                        changed = True
                    if name not in module.satisfied:
                        module.satisfied.add(name)
                        changed = True
                elif kind == "import":
                    node, alias = binder[1], binder[2]
                    classified = _classify(node, alias, dotted)
                    if classified[0] == "seed-name":
                        provider = classified[1]
                        original = classified[2]
                        provider_rel = next(
                            item.rel for item in modules.values() if item.stem == provider
                        )
                        if original not in pending_exports[provider_rel]:
                            pending_exports[provider_rel].add(original)
                            modules[provider_rel].needed.add(original)
                            changed = True
                            continue
                        provider_module = modules[provider_rel]
                        if original in provider_module.unresolved:
                            module.unresolved.add(name)
                            changed = True
                            continue
                        if original not in provider_module.satisfied:
                            continue
                    elif classified[0] == "relative":
                        module.unresolved.add(name)
                        changed = True
                        continue
                    elif _imports_unmoved_test(classified):
                        inlined = _inline_literal(name, classified)
                        if inlined is None:
                            module.unresolved.add(name)
                            changed = True
                            continue
                        if inlined not in module.inlines:
                            module.inlines.append(inlined)
                            changed = True
                        if name not in module.satisfied:
                            module.satisfied.add(name)
                            changed = True
                        continue
                    key = (id(node), alias.name)
                    if key not in module.include_alias:
                        module.include_alias.add(key)
                        changed = True
                    if name not in module.satisfied:
                        module.satisfied.add(name)
                        changed = True
        if not changed:
            break
    else:
        raise RuntimeError("helper copy did not settle")


def _rewrite_function(segment: str, dotted: dict[str, str]) -> str:
    """Rewrite test imports that sit inside a copied function."""

    tree = ast.parse(segment)
    lines = segment.splitlines()
    spans: list[tuple[int, int, list[str]]] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        statement = "\n".join(lines[node.lineno - 1 : node.end_lineno])
        if "tests" not in statement:
            continue
        indent = re_indent(lines[node.lineno - 1])
        pieces: list[str] = []
        for alias in node.names:
            kind = _classify(node, alias, dotted)
            if kind[0] == "relative" or _imports_unmoved_test(kind):
                raise RuntimeError("copied helper imports a test module that was not moved")
            pieces.append(indent + _emit_alias(kind))
        spans.append((node.lineno, node.end_lineno or node.lineno, pieces))
    if not spans:
        return segment
    spans.sort()
    rewritten: list[str] = []
    cursor = 1
    for start, end, pieces in spans:
        rewritten.extend(lines[cursor - 1 : start - 1])
        rewritten.extend(pieces)
        cursor = end + 1
    rewritten.extend(lines[cursor - 1 :])
    return "\n".join(rewritten)


def re_indent(line: str) -> str:
    return line[: len(line) - len(line.lstrip())]


def _literal_segment(module_name: str, original: str, seen: set[str] | None = None) -> str | None:
    """Return the source of a string or number constant imported from a test module."""

    seen = set() if seen is None else seen
    if original in seen:
        return None
    seen.add(original)
    path = ROOT / (module_name.replace(".", "/") + ".py")
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == original for target in node.targets):
            continue
        value = node.value
        if isinstance(value, ast.Name):
            return _literal_segment(module_name, value.id, seen)
        segment = ast.get_source_segment(text, value)
        if segment is None or not _is_literal(value):
            return None
        if _text_has_machine_path(segment):
            return None
        return segment
    return None


def _is_literal(node: ast.AST) -> bool:
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        return _is_literal(node.operand)
    if isinstance(node, (ast.Tuple, ast.List)):
        return all(_is_literal(item) for item in node.elts)
    return False


def _inline_literal(local_name: str, kind: tuple[Any, ...]) -> str | None:
    if kind[0] != "plain-from":
        return None
    segment = _literal_segment(str(kind[1]), str(kind[2]))
    if segment is None:
        return None
    return f"{local_name} = {segment}"


def _imports_unmoved_test(kind: tuple[Any, ...]) -> bool:
    if kind[0] == "plain-from":
        return str(kind[1]).startswith("tests")
    if kind[0] == "plain-import":
        return str(kind[1]).startswith("tests")
    return False


def _render(module: Module, dotted: dict[str, str]) -> str:
    out = [
        '"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""',
        "",
        "from __future__ import annotations",
        "",
    ]
    uses_root = any(
        _is_root_assign(node, module.segment(node))
        for node in module.tree.body
        if isinstance(node, ast.Assign) and id(node) in module.include_assign
    )
    if uses_root:
        out.append("from seed_helpers.repo_root import repo_root")
        out.append("")
    emitted_import = False
    emitted_inlines = False
    for node in module.tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.ImportFrom) and node.module == "__future__":
                continue
            pieces = []
            for alias in node.names:
                if (id(node), alias.name) not in module.include_alias:
                    continue
                pieces.append(_emit_alias(_classify(node, alias, dotted)))
            if pieces:
                out.extend(pieces)
                emitted_import = True
        elif isinstance(node, (ast.Assign, ast.AnnAssign)) and id(node) in module.include_assign:
            if emitted_import:
                out.append("")
                emitted_import = False
            if not emitted_inlines and module.inlines:
                out.extend(module.inlines)
                out.append("")
                emitted_inlines = True
            segment = module.segment(node)
            if _is_root_assign(node, segment):
                target = node.targets[0]
                assert isinstance(target, ast.Name)
                out.append(f"{target.id} = repo_root()")
            else:
                out.append(segment)
            out.append("")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in module.copy_fns:
            if emitted_import:
                out.append("")
                emitted_import = False
            replacement = REPLACEMENTS.get((module.rel, node.name))
            body = replacement if replacement else _rewrite_function(module.segment(node), dotted)
            out.append(body.rstrip("\n"))
            out.append("")
    if module.inlines and not emitted_inlines:
        out.extend(module.inlines)
        out.append("")
    text = "\n".join(out).rstrip() + "\n"
    if _text_has_machine_path(text):
        raise RuntimeError(f"{module.rel} copy contains a machine path")
    if "import tests" in text or "from tests" in text:
        raise RuntimeError(f"{module.rel} copy still imports a test module")
    return text


def _importer_counts(trace: dict[str, Any], helper_rels: set[str]) -> dict[str, Any]:
    files = {item["importer"] for item in trace["importers"]}
    files.discard("tools/generate_entry_loop_v70_fixture.py")
    helper_files = files & helper_rels
    others = files - helper_rels
    tests = sorted(path for path in others if path.startswith("tests/"))
    tools = sorted(path for path in others if path.startswith("tools/"))
    rest = sorted(others - set(tests) - set(tools))
    return {
        "helper_modules_that_import_each_other": len(helper_files),
        "other_files": len(others),
        "other_test_modules": len(tests),
        "other_tools": tools,
        "other_non_test_non_tool": rest,
    }


def main() -> None:
    trace = json.loads(TRACE_PATH.read_text(encoding="utf-8"))
    by_rel: dict[str, set[str]] = {}
    spans: dict[tuple[str, str], int] = {}
    for row in trace["functions"]:
        if not row.get("helper_call") or "<locals>" in row["qualname"]:
            continue
        by_rel.setdefault(row["rel"], set()).add(row["qualname"])
        spans[(row["rel"], row["qualname"])] = int(row["lines"])
    modules = {
        rel: Module(rel, (ROOT / rel).read_text(encoding="utf-8"), names)
        for rel, names in sorted(by_rel.items())
    }
    dotted = {_dotted(rel): Path(rel).stem for rel in modules}
    if len(dotted) != len(modules):
        raise RuntimeError("helper module stems are not unique")
    _resolve(modules, dotted)
    PACKAGE.mkdir(parents=True, exist_ok=True)
    (PACKAGE / "__init__.py").write_text(
        '"""Non-test copy of the helpers the v70 entry seed calls."""\n',
        encoding="utf-8",
    )
    (PACKAGE / "repo_root.py").write_text(
        '''"""Find the repository root without embedding a machine path."""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "packages" / "kernel" / "__init__.py").is_file() and (
            parent / "tests"
        ).is_dir():
            return parent
    raise RuntimeError("repository root not found")
''',
        encoding="utf-8",
    )
    function_lines = 0
    emitted_lines = 0
    unresolved: dict[str, list[str]] = {}
    for rel, module in modules.items():
        text = _render(module, dotted)
        (PACKAGE / f"{module.stem}.py").write_text(text, encoding="utf-8")
        ast.parse(text)
        emitted_lines += text.count("\n")
        for name in module.copy_fns:
            function_lines += spans[(rel, name)]
        if module.unresolved:
            unresolved[rel] = sorted(module.unresolved)
    summary = {
        "copied_function_span_lines": function_lines,
        "emitted_module_lines": emitted_lines,
        "helper_modules": len(modules),
        "helper_unique_lines_in_trace": trace["counts"]["helper_unique_lines"],
        "importers": _importer_counts(trace, set(modules)),
        "replaced_functions": ["_probe", "_sdd"],
        "unresolved_names": unresolved,
    }
    text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if _text_has_machine_path(text):
        raise RuntimeError("extract summary contains a machine path")
    (EVIDENCE / "move" / "extract_summary.json").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
