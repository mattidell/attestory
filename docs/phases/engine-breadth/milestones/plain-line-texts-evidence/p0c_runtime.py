"""Decision 5's one additive validator entry, in memory for evidence only.

The table is local to validate_package. Transform its AST, require that the
only AST delta is the declared v96 entry, and temporarily replace the code
on the existing function object so already-imported aliases see it too.
No source file, historical entry, check or fall-forward expression changes.
"""
from __future__ import annotations
import ast
from contextlib import contextmanager
import copy
import importlib
import inspect
import textwrap

FIELD = "tax.us.2025.form1040.line-2b"


@contextmanager
def injected_graph():
    pv = importlib.import_module("packages.derivation.package_validation")
    function = pv.validate_package
    original = function.__code__
    source, start = inspect.getsourcelines(function)
    tree = ast.parse(textwrap.dedent("".join(source)))
    before = ast.dump(tree, include_attributes=False)
    tables = [n for n in ast.walk(tree) if isinstance(n, ast.AnnAssign)
              and isinstance(n.target, ast.Name) and n.target.id == "_successor_graphs"]
    assert len(tables) == 1 and isinstance(tables[0].value, ast.Dict)
    table = tables[0].value
    keys = [ast.literal_eval(k) for k in table.keys]
    assert "v96" not in keys
    prior = table.values[keys.index("v68")]
    value = ast.literal_eval(prior)
    expected = copy.deepcopy(value)
    assert expected[1][FIELD] == ("form-field.v3", "v6")
    expected[1][FIELD] = ("form-field.v3", "v7")
    table.keys.append(ast.Constant("v96"))
    table.values.append(ast.parse(repr(expected), mode="eval").body)
    injected_value = ast.literal_eval(table.values[-1])
    assert injected_value == expected
    # Undo the one addition and prove the complete function AST unchanged.
    key, entry = table.keys.pop(), table.values.pop()
    assert ast.dump(tree, include_attributes=False) == before
    table.keys.append(key); table.values.append(entry)
    ast.fix_missing_locations(tree)
    ast.increment_lineno(tree, start - 1)
    namespace = dict(vars(pv))
    exec(compile(tree, pv.__file__, "exec"), namespace)
    replacement = namespace[function.__name__]
    assert replacement.__code__.co_freevars == original.co_freevars
    function.__code__ = replacement.__code__
    try:
        yield {"entry": {"v96": expected}, "only_declared_ast_delta": True}
    finally:
        function.__code__ = original
        assert function.__code__ is original
