"""Inventory evidence-harness loads and the module state they share.

Prints every test module that loads a Python file by path or imports an
evidence harness, which harnesses that load reaches, and where a harness or
test assigns another module's attribute or a shared global (``sys.modules``
and module-level caches).

Static only: it does not import the harnesses. Paths in the report are
repo-relative. A name that does not resolve is listed under unresolved loads
instead of being guessed.

    python3 docs/phases/engine-breadth/milestones/live-harness-isolation-evidence/inventory.py
    python3 docs/phases/engine-breadth/milestones/live-harness-isolation-evidence/inventory.py \\
        --json docs/phases/engine-breadth/milestones/live-harness-isolation-evidence/inventory.json
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator

LIVE_TOKENS = (
    "live_coordinate_run",
    "live_workspace",
    "LiveWorkspace",
    "subprocess",
)
CACHE_DECORATORS = frozenset({"lru_cache", "cache", "cached_property"})
MUTATING_METHODS = frozenset({
    "add", "append", "clear", "discard", "extend", "insert", "pop", "remove",
    "setdefault", "update",
})
SKIP_FILE = "docs/phases/engine-breadth/milestones/live-harness-isolation-evidence/inventory.py"
_CACHE_NAME = re.compile(r"cache|memo", re.IGNORECASE)
_CONST_CACHE: dict[str, dict[str, "Val"]] = {}
_CONST_VISITING: set[str] = set()


@dataclass(frozen=True)
class Val:
    """A name's static value. ``rel`` is repo-relative; empty means the repo root."""

    kind: str
    rel: str | None = None
    text: str | None = None
    origin: str | None = None
    modname: str | None = None
    param_index: int | None = None

    @property
    def foreign(self) -> bool:
        return self.kind in {"module", "alias"} or (
            self.kind == "imported" and self.origin == "packages"
        )


@dataclass
class Load:
    file: str
    line: int
    path: str | None
    module_name: str | None
    mechanism: str
    when: str
    under_main: bool
    evidence: bool
    isolated: bool
    snippet: str


@dataclass
class Write:
    file: str
    line: int
    target: str
    scope: str
    origin: str
    engine: bool
    engine_reason: str
    in_finally: bool
    in_with: bool
    snippet: str


@dataclass
class Cache:
    file: str
    line: int
    name: str
    kind: str


@dataclass
class SysModules:
    file: str
    line: int
    op: str
    key: str | None
    snippet: str


@dataclass
class Unresolved:
    file: str
    line: int
    mechanism: str
    snippet: str


@dataclass
class FileFacts:
    source: str
    lane: str
    loads: list[Load] = field(default_factory=list)
    writes: list[Write] = field(default_factory=list)
    caches: list[Cache] = field(default_factory=list)
    sys_modules: list[SysModules] = field(default_factory=list)
    unresolved: list[Unresolved] = field(default_factory=list)
    imports_tax_loader: bool = False


@dataclass
class Template:
    name_index: int | None = None
    path_index: int | None = None
    name_val: Val | None = None
    path_val: Val | None = None
    mechanism: str = "spec_from_file_location"


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pytest.ini").is_file() and (parent / "packages").is_dir():
            return parent
    raise SystemExit("could not find the repository root from this file")


def rel_of(repo: Path, path: Path) -> str:
    return path.resolve().relative_to(repo).as_posix()


def is_evidence(rel: str | None) -> bool:
    if not rel:
        return False
    return any(part.endswith("-evidence") for part in rel.split("/"))


def origin_of(rel: str | None) -> str:
    if not rel:
        return "other"
    if rel.startswith("packages/") or rel == "packages":
        return "packages"
    if is_evidence(rel):
        return "evidence"
    if rel.startswith("tests/") or rel == "tests":
        return "tests"
    if rel.startswith("tools/") or rel == "tools":
        return "tools"
    return "other"


def sibling_module(rel: str, name: str) -> str | None:
    """A same-directory ``name.py``, for a bare import that never inserted a path.

    Running a file as a script puts its directory on ``sys.path``. The inventory
    starts from the repo root, so that import would otherwise not resolve.
    """
    if not name.isidentifier() or "." in name:
        return None
    parent = Path(rel).parent.as_posix()
    if parent == ".":
        parent = ""
    return join_rel(parent, name + ".py")


def join_rel(base: str, part: str) -> str | None:
    if part.startswith("/"):
        return None
    parts = [piece for piece in base.split("/") if piece] if base else []
    for piece in part.split("/"):
        if piece in ("", "."):
            continue
        if piece == "..":
            if not parts:
                return None
            parts.pop()
        else:
            parts.append(piece)
    return "/".join(parts)


def snippet(source: str, node: ast.AST) -> str:
    text = ast.get_source_segment(source, node) or ""
    text = " ".join(text.split())
    if len(text) > 180:
        text = text[:177] + "..."
    return text


def call_attr(node: ast.Call) -> str | None:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def is_evidence_loader_load(node: ast.Call) -> bool:
    """True for ``evidence_loader.load(...)``, the per-owner harness loader."""
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "load"
        and isinstance(func.value, ast.Name)
        and func.value.id == "evidence_loader"
    )


def decorator_name(node: ast.AST) -> str | None:
    inner = node.func if isinstance(node, ast.Call) else node
    if isinstance(inner, ast.Name):
        return inner.id
    if isinstance(inner, ast.Attribute):
        return inner.attr
    return None


def lane_of(source: str) -> str:
    if any(token in source for token in LIVE_TOKENS) or "pytest.mark.live" in source:
        return "live"
    return "fast"


def is_main_guard(test: ast.AST) -> bool:
    if not isinstance(test, ast.Compare) or len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq):
        return False
    left, right = test.left, test.comparators[0]
    pair = (left, right)
    for name_node, const_node in (pair, (right, left)):
        if (
            isinstance(name_node, ast.Name)
            and name_node.id == "__name__"
            and isinstance(const_node, ast.Constant)
            and const_node.value == "__main__"
        ):
            return True
    return False


def describe_target(node: ast.AST) -> tuple[str, str] | None:
    attrs: list[str] = []
    subs = 0
    cur = node
    while True:
        if isinstance(cur, ast.Attribute):
            attrs.append(cur.attr)
            cur = cur.value
        elif isinstance(cur, ast.Subscript):
            subs += 1
            cur = cur.value
        else:
            break
    if not isinstance(cur, ast.Name):
        return None
    attrs.reverse()
    dotted = cur.id
    for attr in attrs:
        dotted += "." + attr
    if subs:
        dotted += "[]" * subs
    return cur.id, dotted


def store_nodes(target: ast.AST) -> Iterator[ast.AST]:
    if isinstance(target, (ast.Tuple, ast.List)):
        for elt in target.elts:
            yield from store_nodes(elt)
        return
    if isinstance(target, ast.Starred):
        yield from store_nodes(target.value)
        return
    yield target


class Analyzer:
    def __init__(self, repo: Path, rel: str, source: str) -> None:
        self.repo = repo
        self.rel = rel
        self.source = source
        self.tree = ast.parse(source)
        self.facts = FileFacts(source=source, lane=lane_of(source))
        self.env: dict[str, Val] = {}
        self.path_dirs: list[str] = [""]
        self.scope = "<module>"
        self.under_main = False
        self.in_finally = False
        self.in_with = False
        self.when = "import"
        self.recording = True
        self.templates: dict[str, Template] = {}
        self._file_val = Val(kind="path", rel=rel, origin=origin_of(rel))
        self._dir_val = Val(
            kind="path",
            rel=str(Path(rel).parent.as_posix()) if Path(rel).parent.as_posix() != "." else "",
            origin=origin_of(rel),
        )

    def run(self) -> FileFacts:
        self.templates = self._templates(self.tree.body)
        saved_env = self.env
        self.env = {"__file__": self._file_val}
        self.path_dirs = [""]
        self._bind_module_constants(self.tree.body)
        constants = dict(self.env)
        self.env = saved_env
        self.env = dict(constants)
        self.path_dirs = [""]
        self.when = "import"
        self.scope = "<module>"
        self._walk_module(self.tree.body)
        final = dict(self.env)
        final_path = list(self.path_dirs)
        self._walk_functions(self.tree.body, final, final_path, "<module>")
        return self.facts

    def _templates(self, body: list[ast.stmt]) -> dict[str, Template]:
        found: dict[str, Template] = {}

        def visit(stmts: list[ast.stmt]) -> None:
            for stmt in stmts:
                if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    found[stmt.name] = self._template_for(stmt)
                    visit(stmt.body)
                elif isinstance(stmt, ast.ClassDef):
                    visit(stmt.body)
                elif isinstance(stmt, (ast.If, ast.For, ast.While, ast.With)):
                    visit(list(stmt.body))
                    visit(list(getattr(stmt, "orelse", [])))
                elif isinstance(stmt, ast.Try):
                    visit(list(stmt.body))
                    visit(list(stmt.finalbody))
                    visit(list(stmt.orelse))

        visit(body)
        return found

    def _template_for(self, fn: ast.FunctionDef | ast.AsyncFunctionDef) -> Template:
        params = [arg.arg for arg in fn.args.args]
        template = Template()
        chosen: ast.Call | None = None
        for call in self._direct_calls(fn.body):
            if call_attr(call) == "spec_from_file_location":
                chosen = call
                template.mechanism = "spec_from_file_location"
                break
        if chosen is None:
            for call in self._direct_calls(fn.body):
                if is_evidence_loader_load(call):
                    chosen = call
                    template.mechanism = "loader"
                    break
        if chosen is None:
            return template
        if template.mechanism == "loader":
            name_val = self._positional(chosen, 1, "name")
            path_val = self._positional(chosen, 0, "path")
        else:
            name_val = self._positional(chosen, 0, "name")
            path_val = self._positional(chosen, 1, "location")
        if isinstance(name_val, ast.Name) and name_val.id in params:
            template.name_index = params.index(name_val.id)
        if isinstance(path_val, ast.Name) and path_val.id in params:
            template.path_index = params.index(path_val.id)
        return template

    def _direct_calls(self, body: list[ast.stmt]) -> Iterator[ast.Call]:
        for stmt in body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            yield from self._calls_outside_nested(stmt)

    def _calls_outside_nested(self, node: ast.AST) -> Iterator[ast.Call]:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            return
        if isinstance(node, ast.Call):
            yield node
        for child in ast.iter_child_nodes(node):
            yield from self._calls_outside_nested(child)

    def _positional(self, call: ast.Call, index: int, keyword: str) -> ast.AST | None:
        for kw in call.keywords:
            if kw.arg == keyword:
                return kw.value
        if index < len(call.args):
            return call.args[index]
        return None

    def _bind_module_constants(self, body: list[ast.stmt]) -> None:
        for stmt in body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if isinstance(stmt, ast.ClassDef):
                continue
            if isinstance(stmt, ast.Assign):
                value = self._eval(stmt.value)
                for target in stmt.targets:
                    self._bind_target(target, value)
            elif isinstance(stmt, ast.AnnAssign) and stmt.value is not None and stmt.target:
                self._bind_target(stmt.target, self._eval(stmt.value))
            elif isinstance(stmt, ast.If):
                self._bind_module_constants(list(stmt.body))
                self._bind_module_constants(list(stmt.orelse))
            elif isinstance(stmt, ast.Try):
                self._bind_module_constants(list(stmt.body))
                self._bind_module_constants(list(stmt.finalbody))

    def _bind_constants(self, body: list[ast.stmt]) -> None:
        """Bind module-level path and string constants, following imports.

        Used while resolving a constant imported from another module. Load and
        write recording is off for that pass.
        """
        for stmt in body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            if isinstance(stmt, (ast.Import, ast.ImportFrom)):
                self._note_import(stmt)
            elif isinstance(stmt, ast.Assign):
                value = self._eval(stmt.value)
                for target in stmt.targets:
                    self._bind_target(target, value)
            elif isinstance(stmt, ast.AnnAssign) and stmt.value is not None and stmt.target:
                self._bind_target(stmt.target, self._eval(stmt.value))
            elif isinstance(stmt, ast.If):
                self._bind_constants(list(stmt.body))
                self._bind_constants(list(stmt.orelse))
            elif isinstance(stmt, ast.Try):
                self._bind_constants(list(stmt.body))
                self._bind_constants(list(stmt.finalbody))

    def _walk_module(self, body: list[ast.stmt]) -> None:
        for stmt in body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            self._walk_stmt(stmt)

    def _walk_functions(
        self,
        body: list[ast.stmt],
        env: dict[str, Val],
        path_dirs: list[str],
        scope: str,
    ) -> None:
        for stmt in body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._analyze_function(stmt, env, path_dirs, scope)
            elif isinstance(stmt, ast.ClassDef):
                self._walk_functions(list(stmt.body), env, path_dirs, scope)
            elif isinstance(stmt, ast.If):
                self._walk_functions(list(stmt.body), env, path_dirs, scope)
                self._walk_functions(list(stmt.orelse), env, path_dirs, scope)
            elif isinstance(stmt, ast.Try):
                self._walk_functions(list(stmt.body), env, path_dirs, scope)
                self._walk_functions(list(stmt.finalbody), env, path_dirs, scope)

    def _analyze_function(
        self,
        fn: ast.FunctionDef | ast.AsyncFunctionDef,
        env: dict[str, Val],
        path_dirs: list[str],
        scope: str,
    ) -> None:
        saved = (self.env, self.path_dirs, self.scope, self.when, self.under_main)
        self.env = dict(env)
        params = [arg.arg for arg in fn.args.args]
        for index, name in enumerate(params):
            self.env[name] = Val(kind="param", text=name, param_index=index)
        self.path_dirs = list(path_dirs)
        self.scope = f"{scope}.{fn.name}" if scope != "<module>" else fn.name
        self.when = "call"
        self._note_decorators(fn)
        self._walk_stmt_list(list(fn.body))
        self.env, self.path_dirs, self.scope, self.when, self.under_main = saved

    def _walk_stmt_list(self, body: list[ast.stmt]) -> None:
        for stmt in body:
            self._walk_stmt(stmt)

    def _walk_stmt(self, stmt: ast.stmt) -> None:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return
        if isinstance(stmt, ast.ClassDef):
            saved = self.env
            self.env = dict(saved)
            self._walk_stmt_list(list(stmt.body))
            self.env = saved
            return
        if isinstance(stmt, ast.Assign):
            self._visit_expr(stmt.value)
            value = self._eval(stmt.value)
            for target in stmt.targets:
                described = list(store_nodes(target))
                self._bind_target(target, value)
                for node in described:
                    self._note_store(node)
            return
        if isinstance(stmt, ast.AnnAssign):
            if stmt.value is not None:
                self._visit_expr(stmt.value)
                self._bind_target(stmt.target, self._eval(stmt.value))
            self._note_store(stmt.target)
            return
        if isinstance(stmt, ast.AugAssign):
            self._visit_expr(stmt.value)
            self._note_store(stmt.target)
            return
        if isinstance(stmt, ast.If):
            self._visit_expr(stmt.test)
            saved_main = self.under_main
            if is_main_guard(stmt.test):
                self.under_main = True
            self._walk_stmt_list(list(stmt.body))
            self.under_main = saved_main
            self._walk_stmt_list(list(stmt.orelse))
            return
        if isinstance(stmt, ast.For):
            self._visit_expr(stmt.iter)
            self._walk_stmt_list(list(stmt.body))
            self._walk_stmt_list(list(stmt.orelse))
            return
        if isinstance(stmt, ast.While):
            self._visit_expr(stmt.test)
            self._walk_stmt_list(list(stmt.body))
            return
        if isinstance(stmt, ast.With):
            for item in stmt.items:
                self._visit_expr(item.context_expr)
            saved = self.in_with
            self.in_with = True
            self._walk_stmt_list(list(stmt.body))
            self.in_with = saved
            return
        if isinstance(stmt, ast.Try):
            self._walk_stmt_list(list(stmt.body))
            saved = self.in_finally
            self.in_finally = True
            self._walk_stmt_list(list(stmt.finalbody))
            self.in_finally = saved
            self._walk_stmt_list(list(stmt.orelse))
            return
        if isinstance(stmt, (ast.Import, ast.ImportFrom)):
            self._note_import(stmt)
            return
        if isinstance(stmt, ast.Expr):
            self._visit_expr(stmt.value)
            return
        if isinstance(stmt, ast.Delete):
            for target in stmt.targets:
                self._note_sys_modules_target(target, "delete")
            return
        for child in ast.iter_child_nodes(stmt):
            if isinstance(child, ast.expr):
                self._visit_expr(child)

    def _visit_expr(self, node: ast.AST) -> None:
        if isinstance(node, ast.Call):
            for arg in node.args:
                self._visit_expr(arg)
            for kw in node.keywords:
                self._visit_expr(kw.value)
            self._note_call(node)
            return
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            return
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.expr):
                self._visit_expr(child)

    def _note_decorators(self, fn: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        for dec in fn.decorator_list:
            name = decorator_name(dec)
            if name in CACHE_DECORATORS:
                self.facts.caches.append(Cache(self.rel, fn.lineno, fn.name, name))

    def _note_call(self, call: ast.Call) -> None:
        attr = call_attr(call)
        if is_evidence_loader_load(call):
            self._note_loader(call)
        elif attr == "spec_from_file_location":
            self._note_spec(call)
        elif attr == "import_module":
            self._note_import_module(call)
        elif attr == "run_path":
            self._note_run_path(call)
        elif attr in {"exec", "compile"} and isinstance(call.func, ast.Name):
            self._note_exec(call)
        elif attr == "insert":
            self._note_path_insert(call)
        elif attr == "append" and self._is_sys_path(call.func):
            self._note_path_append(call)
        elif isinstance(call.func, ast.Name) and call.func.id in self.templates:
            self._note_template_call(call.func.id, call)
        elif attr == "setattr":
            self._note_setattr(call)
        elif attr in MUTATING_METHODS and isinstance(call.func, ast.Attribute):
            self._note_store(call.func.value, method=attr)
        if self._is_sys_modules(getattr(call.func, "value", None)) and attr == "get":
            key = self._eval(call.args[0]) if call.args else Val(kind="unknown")
            self.facts.sys_modules.append(SysModules(
                self.rel, call.lineno, "reuse",
                key.text if key.kind == "str" else None,
                snippet(self.source, call),
            ))

    def _note_spec(self, call: ast.Call) -> None:
        if isinstance(call.func, ast.Name) and call.func.id in self.templates:
            return
        name_node = self._positional(call, 0, "name")
        path_node = self._positional(call, 1, "location")
        if isinstance(path_node, ast.Name) and self.env.get(path_node.id, Val(kind="unknown")).kind == "param":
            return
        if isinstance(name_node, ast.Name) and self.env.get(name_node.id, Val(kind="unknown")).kind == "param":
            name_val = Val(kind="unknown", text=name_node.id)
        else:
            name_val = self._eval(name_node) if name_node is not None else Val(kind="unknown")
        path_val = self._eval(path_node) if path_node is not None else Val(kind="unknown")
        self._emit_load(call, "spec_from_file_location", path_val, name_val, isolated=False)

    def _note_loader(self, call: ast.Call) -> None:
        name_node = self._positional(call, 1, "name")
        path_node = self._positional(call, 0, "path")
        if self._is_param(path_node) or self._is_param(name_node):
            return
        name_val = self._eval(name_node) if name_node is not None else Val(kind="unknown")
        path_val = self._eval(path_node) if path_node is not None else Val(kind="unknown")
        self._emit_load(call, "loader", path_val, name_val, isolated=False)

    def _is_param(self, node: ast.AST | None) -> bool:
        return (
            isinstance(node, ast.Name)
            and self.env.get(node.id, Val(kind="unknown")).kind == "param"
        )

    def _note_template_call(self, func_name: str, call: ast.Call) -> None:
        template = self.templates[func_name]
        if template.path_index is None and template.name_index is None:
            return
        name_val = self._template_arg(call, template.name_index, "name")
        path_val = self._template_arg(call, template.path_index, "location")
        if path_val is None and name_val is None:
            return
        self._emit_load(
            call, template.mechanism,
            path_val or Val(kind="unknown"),
            name_val or Val(kind="unknown"),
            isolated=False,
        )

    def _template_arg(self, call: ast.Call, index: int | None, keyword: str) -> Val | None:
        if index is None:
            return None
        node = self._positional(call, index, keyword)
        if node is None:
            return Val(kind="unknown")
        return self._eval(node)

    def _note_import_module(self, call: ast.Call) -> None:
        node = self._positional(call, 0, "name")
        if node is None:
            return
        val = self._eval(node)
        if val.kind != "str" or not val.text:
            self.facts.unresolved.append(Unresolved(
                self.rel, call.lineno, "import_module", snippet(self.source, call),
            ))
            return
        path = self._resolve_dotted(val.text)
        if path is None:
            sibling = sibling_module(self.rel, val.text)
            if sibling and (self.repo / sibling).is_file():
                path = sibling
        if path is None:
            return
        if is_evidence(path):
            self._emit_load(
                call, "import_module",
                Val(kind="path", rel=path, origin=origin_of(path)),
                Val(kind="str", text=val.text),
                isolated=False,
            )
        self._bind_import_result(call, val.text, path)

    def _note_run_path(self, call: ast.Call) -> None:
        node = self._positional(call, 0, "path")
        if node is None:
            return
        self._emit_load(call, "run_path", self._eval(node), Val(kind="unknown"), isolated=False)

    def _note_exec(self, call: ast.Call) -> None:
        """``exec`` or ``compile`` of a file's text is a load by path.

        Recognised source shapes: ``<path>.read_text()``, ``<path>.read_bytes()``
        and ``open(<path>).read()``. Source the inventory cannot trace to a
        file is not a load.
        """
        source = self._positional(call, 0, "source")
        if not isinstance(source, ast.Call) or not isinstance(source.func, ast.Attribute):
            return
        holder = source.func.value
        if source.func.attr in {"read_text", "read_bytes"}:
            path_node: ast.AST = holder
        elif (
            source.func.attr == "read"
            and isinstance(holder, ast.Call)
            and call_attr(holder) == "open"
            and holder.args
        ):
            path_node = holder.args[0]
        else:
            return
        path_val = self._eval(path_node)
        if path_val.kind not in {"path", "str"}:
            return
        self._emit_load(call, call_attr(call) or "exec", path_val, Val(kind="unknown"), isolated=False)

    def _note_import(self, stmt: ast.Import | ast.ImportFrom) -> None:
        if isinstance(stmt, ast.Import):
            for alias in stmt.names:
                path = self._resolve_dotted(alias.name)
                bound = alias.asname or alias.name.split(".")[0]
                if path is None:
                    if alias.name == "subprocess":
                        self.env[bound] = Val(kind="module", origin="stdlib", modname="subprocess", text="subprocess")
                        continue
                    sibling = sibling_module(self.rel, alias.name)
                    if sibling and (self.repo / sibling).is_file():
                        path = sibling
                    else:
                        continue
                self._bind_resolved_import(bound, alias.name, path)
                if is_evidence(path):
                    self._emit_load(
                        stmt, "import",
                        Val(kind="path", rel=path, origin=origin_of(path)),
                        Val(kind="str", text=alias.name),
                        isolated=False,
                    )
            return
        module = stmt.module or ""
        path = self._resolve_dotted(module) if module else None
        if module == "packages.tax.loader" or module.startswith("packages.tax.loader"):
            self.facts.imports_tax_loader = True
        if path is not None and is_evidence(path):
            self._emit_load(
                stmt, "import",
                Val(kind="path", rel=path, origin=origin_of(path)),
                Val(kind="str", text=module),
                isolated=False,
            )
        constants = module_constants(self.repo, py_file(self.repo, path)) if path is not None else {}
        for alias in stmt.names:
            bound = alias.asname or alias.name
            if alias.name == "*":
                continue
            exported = constants.get(alias.name)
            if exported is not None and exported.kind in {"path", "str", "int"}:
                self.env[bound] = exported
                continue
            if path is not None and self._is_package_dir(path) and alias.name != "*":
                child = join_rel(path, alias.name + ".py")
                if child and (self.repo / child).is_file():
                    self._bind_resolved_import(bound, f"{module}.{alias.name}", child)
                    continue
                child_init = join_rel(path, alias.name + "/__init__.py")
                if child_init and (self.repo / child_init).is_file():
                    self._bind_resolved_import(bound, f"{module}.{alias.name}", str(Path(child_init).parent.as_posix()))
                    continue
            if path is not None:
                self.env[bound] = Val(
                    kind="imported", rel=path, origin=origin_of(path),
                    modname=module, text=alias.name,
                )

    def _bind_import_result(self, call: ast.Call, modname: str, path: str) -> None:
        # The caller binds the result when the call is an assignment value.
        # Record the module on a synthetic name only when import_module is the
        # whole value; assignment binding happens in _walk_stmt via _eval.
        del call, modname, path

    def _bind_resolved_import(self, bound: str, modname: str, path: str) -> None:
        origin = origin_of(path)
        self.env[bound] = Val(kind="module", rel=path, origin=origin, modname=modname)
        if modname == "packages.tax.loader" or modname.startswith("packages.tax.loader"):
            self.facts.imports_tax_loader = True

    def _note_path_insert(self, call: ast.Call) -> None:
        if not self._is_sys_path(call.func) or not call.args:
            return
        index = self._eval(call.args[0]) if len(call.args) > 1 else Val(kind="str", text="0")
        path_node = call.args[1] if len(call.args) > 1 else call.args[0]
        # insert(index, path) is the usual shape. insert(path) is not valid.
        if len(call.args) < 2:
            return
        val = self._eval(path_node)
        if val.kind != "path" or val.rel is None:
            return
        position = 0 if index.kind == "str" and index.text in {None, "0"} else len(self.path_dirs)
        if index.kind == "int":
            position = index.param_index or 0
        if val.rel in self.path_dirs:
            return
        self.path_dirs.insert(position if position <= len(self.path_dirs) else len(self.path_dirs), val.rel)

    def _note_path_append(self, call: ast.Call) -> None:
        if not call.args:
            return
        val = self._eval(call.args[0])
        if val.kind == "path" and val.rel is not None and val.rel not in self.path_dirs:
            self.path_dirs.append(val.rel)

    def _note_setattr(self, call: ast.Call) -> None:
        if not call.args:
            return
        root = self._eval(call.args[0])
        if not root.foreign and root.origin != "packages":
            return
        attr = self._eval(call.args[1]) if len(call.args) > 1 else Val(kind="unknown")
        label = attr.text if attr.kind == "str" and attr.text else "<?>"
        target = f"{root.text or root.modname or 'module'}.{label}"
        self._record_write(call, target, root)

    def _note_store(self, node: ast.AST, method: str | None = None) -> None:
        # A bare name binding is the local, not a write to the module it holds.
        if isinstance(node, ast.Name):
            return
        if isinstance(node, ast.Subscript) and self._is_sys_modules(node.value):
            self._note_sys_modules_target(node, "assign")
            return
        described = describe_target(node)
        if described is None:
            return
        root_name, dotted = described
        if method:
            dotted = f"{dotted}.{method}()"
        if root_name in {"self", "cls"}:
            return
        root = self.env.get(root_name)
        if root is None or not root.foreign:
            return
        self._record_write(node, dotted, root)

    def _note_sys_modules_target(self, node: ast.AST, op: str) -> None:
        if not isinstance(node, ast.Subscript) or not self._is_sys_modules(node.value):
            return
        key = self._eval(node.slice)
        self.facts.sys_modules.append(SysModules(
            self.rel, getattr(node, "lineno", 0), op,
            key.text if key.kind == "str" else None,
            snippet(self.source, node),
        ))

    def _record_write(self, node: ast.AST, target: str, root: Val) -> None:
        engine, reason = self._engine(target, root)
        self.facts.writes.append(Write(
            file=self.rel,
            line=getattr(node, "lineno", 0),
            target=target,
            scope=self.scope,
            origin=root.origin or "other",
            engine=engine,
            engine_reason=reason,
            in_finally=self.in_finally,
            in_with=self.in_with,
            snippet=snippet(self.source, node),
        ))

    def _engine(self, target: str, root: Val) -> tuple[bool, str]:
        if root.origin == "packages":
            return True, "packages-import"
        parts = target.split(".")
        if "loader" in parts and (self.facts.imports_tax_loader or root.origin == "evidence"):
            return True, "loader-attribute"
        return False, ""

    def _emit_load(
        self,
        node: ast.AST,
        mechanism: str,
        path_val: Val,
        name_val: Val,
        *,
        isolated: bool,
    ) -> None:
        if not self.recording:
            return
        path = path_val.rel if path_val.kind == "path" else None
        if path_val.kind == "str" and path_val.text and path_val.text.endswith(".py"):
            path = path_val.text.lstrip("./") if not path_val.text.startswith("/") else None
        module_name = name_val.text if name_val.kind == "str" else name_val.modname
        if path is None and module_name is None:
            self.facts.unresolved.append(Unresolved(
                self.rel, getattr(node, "lineno", 0), mechanism, snippet(self.source, node),
            ))
            return
        if path is not None and path.startswith("/"):
            self.facts.unresolved.append(Unresolved(
                self.rel, getattr(node, "lineno", 0), mechanism, "<absolute>",
            ))
            return
        evidence = is_evidence(path)
        load = Load(
            file=self.rel,
            line=getattr(node, "lineno", 0),
            path=path,
            module_name=module_name,
            mechanism=mechanism,
            when=self.when,
            under_main=self.under_main,
            evidence=evidence,
            isolated=isolated,
            snippet=snippet(self.source, node),
        )
        self.facts.loads.append(load)
        if path and path.endswith(".py"):
            self._maybe_bind_call_result(node, path, module_name)

    def _maybe_bind_call_result(self, node: ast.AST, path: str, module_name: str | None) -> None:
        # Binding of the assignment target is handled by _eval of the call
        # when the call itself is the assignment value. Nested calls stay unbound.
        del node, path, module_name

    def _eval(self, node: ast.AST | None) -> Val:
        if node is None:
            return Val(kind="unknown")
        if isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return Val(kind="str", text=node.value)
            if isinstance(node.value, int) and not isinstance(node.value, bool):
                return Val(kind="int", param_index=node.value, text=str(node.value))
            return Val(kind="unknown")
        if isinstance(node, ast.Name):
            if node.id == "__file__":
                return self._file_val
            found = self.env.get(node.id)
            return found if found is not None else Val(kind="unknown", text=node.id)
        if isinstance(node, ast.JoinedStr):
            parts: list[str] = []
            for value in node.values:
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    parts.append(value.value)
                else:
                    return Val(kind="unknown", text=snippet(self.source, node))
            return Val(kind="str", text="".join(parts))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            left = self._eval(node.left)
            right = self._eval(node.right)
            if left.kind == "path" and left.rel is not None and right.kind == "str" and right.text is not None:
                joined = join_rel(left.rel, right.text)
                if joined is None:
                    return Val(kind="unknown", text=snippet(self.source, node))
                return Val(kind="path", rel=joined, origin=origin_of(joined))
            return Val(kind="unknown", text=snippet(self.source, node))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left = self._eval(node.left)
            right = self._eval(node.right)
            if left.kind == "str" and right.kind == "str" and left.text is not None and right.text is not None:
                return Val(kind="str", text=left.text + right.text)
            return Val(kind="unknown", text=snippet(self.source, node))
        if isinstance(node, ast.Attribute):
            base = self._eval(node.value)
            if base.kind == "path" and base.rel is not None:
                if node.attr == "parent":
                    parent = str(Path(base.rel).parent.as_posix()) if base.rel else ""
                    if parent == ".":
                        parent = ""
                    return Val(kind="path", rel=parent, origin=origin_of(parent))
                if node.attr == "name" and base.rel:
                    return Val(kind="str", text=Path(base.rel).name)
                if node.attr == "stem" and base.rel:
                    return Val(kind="str", text=Path(base.rel).stem)
            if base.kind in {"module", "alias"} and node.attr:
                return Val(
                    kind="alias", rel=base.rel, origin=base.origin, modname=base.modname,
                    text=f"{base.text or base.modname or 'module'}.{node.attr}",
                )
            return Val(kind="unknown", text=snippet(self.source, node))
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute):
            if node.value.attr == "parents":
                base = self._eval(node.value.value)
                index = self._eval(node.slice)
                if base.kind == "path" and base.rel is not None and index.kind == "int" and index.param_index is not None:
                    parts = [part for part in base.rel.split("/") if part]
                    drop = index.param_index + 1
                    if drop > len(parts):
                        return Val(kind="path", rel="", origin="other")
                    kept = "/".join(parts[:-drop])
                    return Val(kind="path", rel=kept, origin=origin_of(kept))
        if isinstance(node, ast.Call):
            return self._eval_call(node)
        return Val(kind="unknown", text=snippet(self.source, node))

    def _eval_call(self, call: ast.Call) -> Val:
        attr = call_attr(call)
        if attr == "str" and len(call.args) == 1 and not isinstance(call.func, ast.Attribute):
            return self._eval(call.args[0])
        if attr in {"resolve", "absolute"} and isinstance(call.func, ast.Attribute):
            return self._eval(call.func.value)
        if isinstance(call.func, ast.Name) and call.func.id == "Path":
            return self._eval_path_ctor(call)
        if attr == "Path" and call.args:
            return self._eval_path_ctor(call)
        if attr in {"spec_from_file_location", "import_module"} or is_evidence_loader_load(call) or (
            isinstance(call.func, ast.Name) and call.func.id in self.templates
        ):
            path, modname = self._load_identity(call, attr or "")
            if path:
                return Val(kind="module", rel=path, origin=origin_of(path), modname=modname, text=modname)
        return Val(kind="unknown", text=snippet(self.source, call))

    def _eval_path_ctor(self, call: ast.Call) -> Val:
        if not call.args:
            return Val(kind="unknown")
        arg = call.args[0]
        if isinstance(arg, ast.Name) and arg.id == "__file__":
            return self._file_val
        val = self._eval(arg)
        if val.kind == "path":
            return val
        if val.kind == "str" and val.text is not None and not val.text.startswith("/"):
            rel = val.text
            return Val(kind="path", rel=rel, origin=origin_of(rel))
        return Val(kind="unknown", text=snippet(self.source, call))

    def _load_identity(self, call: ast.Call, attr: str) -> tuple[str | None, str | None]:
        if isinstance(call.func, ast.Name) and call.func.id in self.templates:
            template = self.templates[call.func.id]
            path_val = self._template_arg(call, template.path_index, "location")
            name_val = self._template_arg(call, template.name_index, "name")
        elif is_evidence_loader_load(call):
            path_val = self._eval(self._positional(call, 0, "path"))
            name_val = self._eval(self._positional(call, 1, "name"))
        elif attr == "import_module":
            name_val = self._eval(self._positional(call, 0, "name"))
            if name_val.kind == "str" and name_val.text:
                return self._resolve_dotted(name_val.text), name_val.text
            return None, None
        else:
            path_val = self._eval(self._positional(call, 1, "location"))
            name_val = self._eval(self._positional(call, 0, "name"))
        path = path_val.rel if path_val and path_val.kind == "path" else None
        modname = name_val.text if name_val and name_val.kind == "str" else None
        return path, modname

    def _bind_target(self, target: ast.AST, value: Val) -> None:
        nodes = list(store_nodes(target))
        if len(nodes) == 1 and isinstance(nodes[0], ast.Name):
            self._bind_name(nodes[0].id, value)
            return
        if isinstance(target, (ast.Tuple, ast.List)) and isinstance(getattr(target, "elts", None), list):
            if all(isinstance(elt, ast.Name) for elt in target.elts) and value.kind in {"module", "alias"}:
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        self.env[elt.id] = Val(
                            kind="alias", rel=value.rel, origin=value.origin,
                            modname=value.modname, text=f"{value.text or value.modname}.{elt.id}",
                        )

    def _bind_name(self, name: str, value: Val) -> None:
        if value.kind == "unknown":
            return
        if value.kind == "str" and name.isupper():
            self.env[name] = value
            return
        if value.kind in {"path", "module", "alias", "imported", "str", "int"}:
            self.env[name] = value
            if value.kind == "module" and value.modname and "packages.tax.loader" in (value.modname or ""):
                self.facts.imports_tax_loader = True

    def _resolve_dotted(self, dotted: str) -> str | None:
        parts = dotted.split(".")
        for directory in self.path_dirs:
            base = directory
            for part in parts:
                base = join_rel(base, part) or ""
            file_rel = base + ".py"
            init_rel = join_rel(base, "__init__.py")
            if (self.repo / file_rel).is_file():
                return file_rel
            if init_rel and (self.repo / init_rel).is_file():
                return base
        return None

    def _is_package_dir(self, path: str) -> bool:
        return (self.repo / path / "__init__.py").is_file() or (self.repo / path).is_dir()

    def _is_sys_path(self, node: ast.AST) -> bool:
        return (
            isinstance(node, ast.Attribute)
            and node.attr in {"insert", "append"}
            and isinstance(node.value, ast.Attribute)
            and node.value.attr == "path"
            and isinstance(node.value.value, ast.Name)
            and node.value.value.id == "sys"
        )

    def _is_sys_modules(self, node: ast.AST | None) -> bool:
        return (
            isinstance(node, ast.Attribute)
            and node.attr == "modules"
            and isinstance(node.value, ast.Name)
            and node.value.id == "sys"
        )

    def _note_subprocess(self, call: ast.Call) -> None:
        func = call.func
        if not (
            isinstance(func, ast.Attribute)
            and isinstance(func.value, ast.Name)
            and func.value.id == "subprocess"
            and func.attr in {"run", "Popen", "check_call", "check_output", "call"}
        ):
            return
        if not call.args or not isinstance(call.args[0], (ast.List, ast.Tuple)):
            return
        for elt in call.args[0].elts:
            val = self._eval(elt)
            path = val.rel if val.kind == "path" else None
            if val.kind == "str" and val.text and val.text.endswith(".py") and not val.text.startswith("/"):
                path = val.text
            if path and path.endswith(".py") and (self.repo / path).is_file():
                self._emit_load(call, "subprocess", Val(kind="path", rel=path), Val(kind="unknown"), isolated=True)


def py_file(repo: Path, path: str) -> str:
    if path.endswith(".py"):
        return path
    init = join_rel(path, "__init__.py")
    if init and (repo / init).is_file():
        return init
    return path


def module_constants(repo: Path, rel: str) -> dict[str, Val]:
    """Path, string, and int constants defined at module level in ``rel``."""
    cached = _CONST_CACHE.get(rel)
    if cached is not None:
        return cached
    if rel in _CONST_VISITING or not rel.endswith(".py") or not (repo / rel).is_file():
        return {}
    _CONST_VISITING.add(rel)
    try:
        try:
            source = (repo / rel).read_text(encoding="utf-8")
            analyzer = Analyzer(repo, rel, source)
        except (OSError, UnicodeError, SyntaxError):
            _CONST_CACHE[rel] = {}
            return {}
        analyzer.recording = False
        analyzer.env = {"__file__": analyzer._file_val}
        analyzer.path_dirs = [""]
        analyzer._bind_constants(analyzer.tree.body)
        result = {
            name: value
            for name, value in analyzer.env.items()
            if name != "__file__" and value.kind in {"path", "str", "int"}
        }
        _CONST_CACHE[rel] = result
        return result
    finally:
        _CONST_VISITING.discard(rel)


def _attach_subprocess(analyzer: Analyzer) -> None:
    """Subprocess script paths are isolated loads. Walk them after the main pass."""
    parents: dict[int, ast.AST] = {}
    for parent in ast.walk(analyzer.tree):
        for child in ast.iter_child_nodes(parent):
            parents[id(child)] = parent

    def enclosing_when(node: ast.AST) -> str:
        current: ast.AST | None = node
        while current is not None:
            if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return "call"
            current = parents.get(id(current))
        return "import"

    saved = analyzer.when
    for node in ast.walk(analyzer.tree):
        if isinstance(node, ast.Call):
            # The env at the end of the module walk can resolve module-level paths.
            analyzer.when = enclosing_when(node)
            analyzer._note_subprocess(node)
    analyzer.when = saved


def parse_file(repo: Path, rel: str) -> FileFacts | None:
    path = repo / rel
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    try:
        analyzer = Analyzer(repo, rel, source)
        facts = analyzer.run()
    except SyntaxError:
        return None
    _attach_subprocess(analyzer)
    _note_module_caches(analyzer)
    return facts


def _note_module_caches(analyzer: Analyzer) -> None:
    for stmt in analyzer.tree.body:
        if not isinstance(stmt, ast.Assign) or len(stmt.targets) != 1:
            continue
        target = stmt.targets[0]
        if not isinstance(target, ast.Name) or not _CACHE_NAME.search(target.id):
            continue
        value = stmt.value
        interesting = isinstance(value, (ast.Dict, ast.List, ast.Set)) or (
            isinstance(value, ast.Call) and call_attr(value) in {"dict", "list", "set"}
        )
        if interesting:
            analyzer.facts.caches.append(Cache(analyzer.rel, stmt.lineno, target.id, "module-container"))


def seed_files(repo: Path) -> list[str]:
    found: list[str] = []
    for path in (repo / "tests").rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        found.append(rel_of(repo, path))
    for path in (repo / "docs" / "phases").rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        rel = rel_of(repo, path)
        if rel == SKIP_FILE:
            continue
        if any(part.endswith("-evidence") for part in path.parts):
            found.append(rel)
    return sorted(set(found))


def scan(repo: Path) -> dict[str, FileFacts]:
    pending = seed_files(repo)
    facts: dict[str, FileFacts] = {}
    while pending:
        rel = pending.pop()
        if rel in facts or rel == SKIP_FILE:
            continue
        parsed = parse_file(repo, rel)
        if parsed is None:
            continue
        facts[rel] = parsed
        for load in parsed.loads:
            if load.isolated or not load.path or not load.path.endswith(".py"):
                continue
            if load.path not in facts and (repo / load.path).is_file():
                pending.append(load.path)
    return facts


def _load_dict(load: Load) -> dict[str, object]:
    return {
        "file": load.file,
        "line": load.line,
        "path": load.path,
        "module_name": load.module_name,
        "mechanism": load.mechanism,
        "when": load.when,
        "under_main": load.under_main,
        "evidence": load.evidence,
        "isolated": load.isolated,
    }


def closure(facts: dict[str, FileFacts], start: str) -> list[dict[str, object]]:
    reached: dict[tuple[str | None, str | None], dict[str, object]] = {}
    queue = [start]
    seen: set[str] = set()
    while queue:
        rel = queue.pop()
        if rel in seen:
            continue
        seen.add(rel)
        file_facts = facts.get(rel)
        if file_facts is None:
            continue
        for load in file_facts.loads:
            if load.isolated or load.under_main or not load.path:
                continue
            key = (load.module_name, load.path)
            when = load.when
            previous = reached.get(key)
            if previous is None or (previous["when"] == "call" and when == "import"):
                reached[key] = {
                    "module_name": load.module_name,
                    "path": load.path,
                    "when": when,
                    "evidence": load.evidence,
                    "via": load.file,
                    "line": load.line,
                    "mechanism": load.mechanism,
                }
            if load.path.endswith(".py") and load.path in facts and load.path not in seen:
                queue.append(load.path)
    return sorted(reached.values(), key=lambda item: (str(item["path"]), str(item["module_name"])))


def unrestored_engine_writes(file_facts: FileFacts) -> list[Write]:
    """Engine writes with no finally partner in the same function and target.

    Two assigns and no finally still count. A restore in another function does
    not clear the write.
    """
    groups: dict[tuple[str, str], list[Write]] = defaultdict(list)
    for write in file_facts.writes:
        if write.engine:
            groups[(write.scope, write.target)].append(write)
    found: list[Write] = []
    for group in groups.values():
        if any(item.in_finally for item in group):
            continue
        found.extend(group)
    return found


def build_report(facts: dict[str, FileFacts]) -> dict[str, object]:
    test_files = sorted(rel for rel in facts if rel.startswith("tests/") and rel.endswith(".py"))
    tests: list[dict[str, object]] = []
    reaches_by_test: dict[str, list[dict[str, object]]] = {}
    for rel in test_files:
        file_facts = facts[rel]
        direct = [
            _load_dict(load)
            for load in file_facts.loads
            if not load.under_main and (load.evidence or load.mechanism in {
                "spec_from_file_location", "run_path", "subprocess", "import_module", "import",
                "loader",
            })
        ]
        if not direct and not any(load.evidence for load in file_facts.loads):
            # Keep a test that reaches an evidence harness only through a helper
            # by computing the closure before dropping it.
            pass
        reached = closure(facts, rel)
        file_loads = [item for item in direct if item["path"]]
        imports_evidence = any(bool(item["evidence"]) for item in reached) or any(
            bool(item["evidence"]) for item in file_loads
        )
        loads_by_path = bool(file_loads)
        if not loads_by_path and not imports_evidence:
            continue
        harnesses = [
            {"path": item["path"], "module_name": item["module_name"], "when": item["when"], "via": item["via"]}
            for item in reached
            if item["evidence"]
        ]
        triggers: list[dict[str, object]] = []
        seen_triggers: set[tuple[str, int, str]] = set()
        for harness in harnesses:
            harness_path = harness["path"]
            if not isinstance(harness_path, str):
                continue
            harness_facts = facts.get(harness_path)
            if harness_facts is None:
                continue
            for write in unrestored_engine_writes(harness_facts):
                key = (write.file, write.line, write.target)
                if key in seen_triggers:
                    continue
                seen_triggers.add(key)
                triggers.append({"file": write.file, "line": write.line, "target": write.target})
        if harnesses and triggers:
            isolation = "subprocess"
        elif harnesses:
            isolation = "private"
        elif file_loads and all(bool(item["isolated"]) for item in file_loads):
            isolation = "isolated"
        else:
            isolation = "not_evidence"
        reaches_by_test[rel] = reached
        tests.append({
            "file": rel,
            "lane": file_facts.lane,
            "isolation": isolation,
            "engine_unrestored": triggers,
            "direct_loads": file_loads,
            "harnesses": harnesses,
        })

    by_name: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for rel, reached in reaches_by_test.items():
        seen_keys: set[tuple[object, object]] = set()
        for item in reached:
            modname = item["module_name"]
            path = item["path"]
            if not isinstance(modname, str) or not modname:
                continue
            key = (modname, path)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            if item["evidence"] or item["via"] != rel:
                by_name[modname][str(path)].add(rel)

    shared: list[dict[str, object]] = []
    for modname in sorted(by_name):
        bindings = by_name[modname]
        tests_for_name = sorted({test for paths in bindings.values() for test in paths})
        if len(tests_for_name) < 2 and len(bindings) < 2:
            continue
        shared.append({
            "module_name": modname,
            "collision": len(bindings) > 1,
            "bindings": [
                {"path": path, "tests": sorted(names)}
                for path, names in sorted(bindings.items())
            ],
        })

    parent: dict[str, str] = {}

    def find(name: str) -> str:
        parent.setdefault(name, name)
        if parent[name] != name:
            parent[name] = find(parent[name])
        return parent[name]

    def union(left: str, right: str) -> None:
        a, b = find(left), find(right)
        if a != b:
            parent[b] = a

    for entry in shared:
        members: list[str] = []
        for binding in entry["bindings"]:
            members.extend(binding["tests"])
        members = sorted(set(members))
        for other in members[1:]:
            union(members[0], other)
    groups: dict[str, set[str]] = defaultdict(set)
    for rel in reaches_by_test:
        if rel in parent:
            groups[find(rel)].add(rel)
    clusters = []
    for members in sorted(groups.values(), key=lambda item: sorted(item)[0]):
        names = sorted({
            entry["module_name"]
            for entry in shared
            if any(test in members for binding in entry["bindings"] for test in binding["tests"])
        })
        clusters.append({"tests": sorted(members), "shared_names": names})

    writes = []
    caches = []
    sys_modules = []
    unresolved = []
    for rel in sorted(facts):
        file_facts = facts[rel]
        in_inventory = rel in reaches_by_test or is_evidence(rel) or any(
            load.evidence for load in file_facts.loads
        )
        if not in_inventory:
            continue
        scope_counts: dict[tuple[str, str], int] = defaultdict(int)
        for write in file_facts.writes:
            scope_counts[(write.scope, write.target)] += 1
        for write in file_facts.writes:
            writes.append({
                "file": write.file,
                "line": write.line,
                "target": write.target,
                "scope": write.scope,
                "origin": write.origin,
                "engine": write.engine,
                "engine_reason": write.engine_reason,
                "in_finally": write.in_finally,
                "in_with": write.in_with,
                "assigns_in_scope": scope_counts[(write.scope, write.target)],
            })
        for cache in file_facts.caches:
            caches.append({"file": cache.file, "line": cache.line, "name": cache.name, "kind": cache.kind})
        for item in file_facts.sys_modules:
            sys_modules.append({
                "file": item.file, "line": item.line, "op": item.op, "key": item.key,
            })
        for item in file_facts.unresolved:
            unresolved.append({
                "file": item.file, "line": item.line, "mechanism": item.mechanism, "snippet": item.snippet,
            })
    writes.sort(key=lambda item: (str(item["file"]), int(item["line"]), str(item["target"])))

    evidence_tests = [item for item in tests if item["harnesses"]]
    bare: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for rel, file_facts in facts.items():
        for load in file_facts.loads:
            if load.under_main or load.isolated or not load.module_name or not load.path:
                continue
            if load.mechanism not in {"import", "import_module"}:
                continue
            if not (is_evidence(load.path) or is_evidence(rel)):
                continue
            bare[load.module_name][load.path].add(rel)
    latent = []
    for name in sorted(bare):
        paths = bare[name]
        if len(paths) < 2:
            continue
        latent.append({
            "module_name": name,
            "bindings": [
                {"path": path, "importers": sorted(importers)}
                for path, importers in sorted(paths.items())
            ],
        })
    reached_tests: dict[str, list[str]] = defaultdict(list)
    for test in tests:
        harnesses = test["harnesses"]
        assert isinstance(harnesses, list)
        seen_paths: set[str] = set()
        for harness in harnesses:
            assert isinstance(harness, dict)
            harness_path = harness["path"]
            if isinstance(harness_path, str) and harness_path not in seen_paths:
                seen_paths.add(harness_path)
                reached_tests[harness_path].append(str(test["file"]))
    engine_files = []
    for rel in sorted(facts):
        if not is_evidence(rel):
            continue
        grouped: dict[tuple[int, str], Write] = {}
        for write in unrestored_engine_writes(facts[rel]):
            grouped.setdefault((write.line, write.target), write)
        if not grouped:
            continue
        engine_files.append({
            "file": rel,
            "reached_by": reached_tests.get(rel, []),
            "writes": [
                {"line": write.line, "target": write.target, "scope": write.scope}
                for _, write in sorted(grouped.items())
            ],
        })
    return {
        "limits": [
            "Static. A load whose path is built at runtime stays in unresolved.",
            "Call-time loads are included even when a particular test never calls that function.",
            "Loads under a __main__ guard are listed on the file and are not part of test reachability.",
            "A private spec_from_file_location name does not isolate bare imports that file executes.",
            "A bare import that does not resolve on the modeled sys.path is the sibling file of that name when the sibling exists.",
            "Subprocess loads are isolated and are not followed into the sharing graph.",
            "Imported path, string, and int constants are followed across modules. A cycle is left unresolved.",
            "An engine write is unrestored when no assignment of that same target in the same function is in a finally.",
            "Latent collisions are bare imports of one name that resolve to different files, whether or not a current test reaches both.",
            "isolation=subprocess means a reached harness writes engine state with no finally partner. isolation=private means the harnesses share only harness globals, or restore engine writes.",
        ],
        "summary": {
            "test_modules_loading_by_path": len(tests),
            "test_modules_reaching_evidence": len(evidence_tests),
            "evidence_files_parsed": sum(1 for rel in facts if is_evidence(rel)),
            "shared_module_names": len(shared),
            "module_name_collisions": sum(1 for entry in shared if entry["collision"]),
            "latent_name_collisions": len(latent),
            "cross_module_writes": len(writes),
            "engine_writes": sum(1 for write in writes if write["engine"]),
            "engine_files_unrestored": len(engine_files),
            "module_caches": len(caches),
            "sys_modules_sites": len(sys_modules),
            "unresolved_loads": len(unresolved),
            "clusters": len(clusters),
            "isolation_subprocess": sum(1 for item in tests if item["isolation"] == "subprocess"),
            "isolation_private": sum(1 for item in tests if item["isolation"] == "private"),
            "isolation_isolated": sum(1 for item in tests if item["isolation"] == "isolated"),
            "isolation_not_evidence": sum(1 for item in tests if item["isolation"] == "not_evidence"),
        },
        "tests": tests,
        "shared": shared,
        "latent_collisions": latent,
        "engine_files": engine_files,
        "clusters": clusters,
        "writes": writes,
        "caches": caches,
        "sys_modules": sys_modules,
        "unresolved": unresolved,
    }


def format_report(report: dict[str, object]) -> str:
    summary = report["summary"]
    assert isinstance(summary, dict)
    lines = [
        "Live evidence harness inventory",
        "",
        "Summary",
        f"  test modules that load a file by path: {summary['test_modules_loading_by_path']}",
        f"  test modules that reach an evidence harness: {summary['test_modules_reaching_evidence']}",
        f"  evidence files parsed: {summary['evidence_files_parsed']}",
        f"  shared sys.modules names: {summary['shared_module_names']}",
        f"  names bound to more than one file: {summary['module_name_collisions']}",
        f"  latent bare-import collisions: {summary['latent_name_collisions']}",
        f"  cross-module writes: {summary['cross_module_writes']}",
        "  isolation subprocess, private, isolated, not-evidence: "
        f"{summary['isolation_subprocess']}, {summary['isolation_private']}, "
        f"{summary['isolation_isolated']}, {summary['isolation_not_evidence']}",
        f"  writes that touch engine state: {summary['engine_writes']}",
        f"  evidence files with an unrestored engine write: {summary['engine_files_unrestored']}",
        f"  module caches: {summary['module_caches']}",
        f"  sys.modules sites: {summary['sys_modules_sites']}",
        f"  unresolved loads: {summary['unresolved_loads']}",
        "",
        "Test modules",
    ]
    tests = report["tests"]
    assert isinstance(tests, list)
    for item in tests:
        assert isinstance(item, dict)
        lines.append(f"  {item['file']}  lane={item['lane']}  isolation={item['isolation']}")
        directs = item["direct_loads"]
        assert isinstance(directs, list)
        for load in directs:
            assert isinstance(load, dict)
            name = load["module_name"] or "?"
            isolated = " isolated" if load["isolated"] else ""
            lines.append(
                f"    load {load['path']} as {name} "
                f"({load['mechanism']}:{load['line']} {load['when']}{isolated})"
            )
        harnesses = item["harnesses"]
        assert isinstance(harnesses, list)
        direct_paths = {load["path"] for load in directs if isinstance(load, dict)}
        for harness in harnesses:
            assert isinstance(harness, dict)
            if harness["path"] in direct_paths and harness["via"] == item["file"]:
                continue
            lines.append(
                f"    reaches {harness['path']} as {harness['module_name']} "
                f"via {harness['via']} ({harness['when']})"
            )
    lines.append("")
    lines.append("Isolation class")
    for kind in ("subprocess", "private", "isolated", "not_evidence"):
        chosen = [item["file"] for item in tests if item["isolation"] == kind]
        lines.append(f"  {kind} ({len(chosen)})")
        for name in chosen:
            lines.append(f"    {name}")
    lines.append("")
    lines.append("Shared module names")
    shared = report["shared"]
    assert isinstance(shared, list)
    for entry in shared:
        assert isinstance(entry, dict)
        flag = " collision" if entry["collision"] else ""
        lines.append(f"  {entry['module_name']}{flag}")
        bindings = entry["bindings"]
        assert isinstance(bindings, list)
        for binding in bindings:
            assert isinstance(binding, dict)
            tests_for = ", ".join(binding["tests"])
            lines.append(f"    {binding['path']}: {tests_for}")
    lines.append("")
    lines.append("Latent bare-import collisions")
    latent = report["latent_collisions"]
    assert isinstance(latent, list)
    for entry in latent:
        assert isinstance(entry, dict)
        lines.append(f"  {entry['module_name']}")
        bindings = entry["bindings"]
        assert isinstance(bindings, list)
        for binding in bindings:
            assert isinstance(binding, dict)
            importers = binding["importers"]
            assert isinstance(importers, list)
            lines.append(f"    {binding['path']}")
            for importer in importers:
                lines.append(f"      {importer}")
    lines.append("")
    lines.append("Unrestored engine writes")
    engine_files = report["engine_files"]
    assert isinstance(engine_files, list)
    for entry in engine_files:
        assert isinstance(entry, dict)
        reached = entry["reached_by"]
        assert isinstance(reached, list)
        audience = ", ".join(str(name) for name in reached) if reached else "no current test"
        lines.append(f"  {entry['file']}  ({audience})")
        entry_writes = entry["writes"]
        assert isinstance(entry_writes, list)
        for write in entry_writes:
            assert isinstance(write, dict)
            lines.append(f"    {write['line']} {write['target']} [{write['scope']}]")
    lines.append("")
    lines.append("Engine and cross-module writes")
    writes = report["writes"]
    assert isinstance(writes, list)
    for write in writes:
        assert isinstance(write, dict)
        if not write["engine"] and write["origin"] == "evidence":
            mark = "harness"
        elif write["engine"]:
            mark = f"engine:{write['engine_reason']}"
        else:
            mark = str(write["origin"])
        restore = ""
        if write["in_finally"]:
            restore = " finally"
        elif int(write["assigns_in_scope"]) > 1:
            restore = f" x{write['assigns_in_scope']}"
        lines.append(
            f"  {write['file']}:{write['line']} {write['target']} "
            f"[{write['scope']}] {mark}{restore}"
        )
    lines.append("")
    lines.append("Caches and sys.modules")
    caches = report["caches"]
    assert isinstance(caches, list)
    for cache in caches:
        assert isinstance(cache, dict)
        lines.append(f"  cache {cache['file']}:{cache['line']} {cache['name']} ({cache['kind']})")
    sys_modules = report["sys_modules"]
    assert isinstance(sys_modules, list)
    for item in sys_modules:
        assert isinstance(item, dict)
        lines.append(f"  sys.modules {item['op']} {item['file']}:{item['line']} key={item['key']}")
    unresolved = report["unresolved"]
    assert isinstance(unresolved, list)
    if unresolved:
        lines.append("")
        lines.append("Unresolved loads")
        for item in unresolved:
            assert isinstance(item, dict)
            lines.append(f"  {item['file']}:{item['line']} {item['mechanism']} {item['snippet']}")
    limits = report["limits"]
    assert isinstance(limits, list)
    lines.append("")
    lines.append("Limits")
    for limit in limits:
        lines.append(f"  - {limit}")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        metavar="PATH",
        help="Also write the inventory JSON at this repo-relative path.",
    )
    args = parser.parse_args(argv)
    repo = repo_root()
    report = build_report(scan(repo))
    sys.stdout.write(format_report(report))
    if args.json:
        target = Path(args.json)
        if target.is_absolute():
            raise SystemExit("JSON output path must be repo-relative")
        (repo / target).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
