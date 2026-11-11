"""Private in-process copies of milestone evidence harnesses.

Each owning test module gets its own copy of a harness, keyed by the
resolved path. Nested bare imports (``import probe``, ``import_module("probe")``)
resolve to that owner's copy. ``packages.*`` and ``tests.*`` stay shared.

A harness that assigns an attribute of a ``packages`` module, or of a class
defined on one, is snapshotted. The previous value is put back when that
owner is finished. A child module importlib binds onto its parent is shared
process state and is left in place. Copies stay for the life of the owner so
a module whose tests are split across a worker still shares one harness.
"""

from __future__ import annotations

import importlib.util
import sys
from contextvars import ContextVar
from dataclasses import dataclass, field
from pathlib import Path
from types import FrameType, ModuleType
from typing import Any

_owner: ContextVar[str | None] = ContextVar("evidence_harness_owner", default=None)
_applying: ContextVar[bool] = ContextVar("evidence_harness_applying", default=False)
_MISSING = object()

# (id(obj), attr) -> value last written by that owner
_WriteKey = tuple[int, str]


@dataclass
class _OwnerState:
    by_path: dict[str, ModuleType] = field(default_factory=dict)
    by_name: dict[str, ModuleType] = field(default_factory=dict)
    written: dict[_WriteKey, object] = field(default_factory=dict)


_owners: dict[str, _OwnerState] = {}
_baseline: dict[_WriteKey, tuple[bool, object]] = {}
_watched: dict[int, object] = {}
_armed_modules: set[int] = set()
_armed_classes: set[int] = set()
_class_watchers: dict[type, type] = {}
# The interpreter's module dict, kept after sys.modules is replaced.
# C code looks a module up there after import returns.
_interpreter_modules: dict[str, Any] | None = None


def current_owner() -> str | None:
    """The test module whose harness copies and engine writes are active."""
    return _owner.get()


def restores_engine_write(target: str) -> bool:
    """True when a packages write of this shape is snapshotted and restored.

    Covered: assignment to an attribute of a packages module, and assignment
    to an attribute of a class defined on a packages module. Not covered: a
    subscript store or an in-place method call. Those cannot be put back by
    restoring the binding.
    """
    if not target or "[]" in target or target.endswith("()"):
        return False
    return "." in target


def activate(owner: str) -> None:
    """Make ``owner`` current and show the engine attributes it has written."""
    _ensure_overlay()
    previous = _owner.get()
    if previous == owner:
        _publish(owner)
        return
    if previous is not None:
        _unpublish(previous)
    _adopt_outside_writes(_owners.get(previous) if previous is not None else None)
    _owner.set(owner)
    _ensure_owner(owner)
    _show(owner)
    _publish(owner)


def release(owner: str) -> None:
    """Park ``owner`` without forgetting its copies or its engine writes.

    The engine shows the baseline again. A later ``activate`` of the same
    owner puts that owner's writes back. Used when a worker switches from
    one test module to another and may switch back.
    """
    if _owner.get() != owner:
        return
    _unpublish(owner)
    _adopt_outside_writes(_owners.get(owner))
    _owner.set(None)
    _show(None)


def finish(owner: str) -> None:
    """Restore engine attributes ``owner`` wrote and drop its private copies."""
    state = _owners.pop(owner, None)
    if _owner.get() == owner:
        _adopt_outside_writes(state)
        _owner.set(None)
    if state is not None:
        _drop_modules(state)
    _show(_owner.get())


def finish_all() -> None:
    """Restore every parked owner. Session teardown."""
    owners = list(_owners)
    for owner in owners:
        finish(owner)
    _owner.set(None)
    _show(None)


def load(path: Path | str, name: str, *, owner: str | None = None) -> ModuleType:
    """Return ``owner``'s private copy of the evidence file at ``path``.

    The same owner and resolved path always return the same module object.
    Nested evidence imports while the body runs bind to that owner. With
    ``owner`` omitted, the calling test module owns the copy.
    """
    _ensure_overlay()
    _arm_existing_packages()
    # The pytest hook already names the running module. Prefer that over the
    # stack so a test file loaded by path, under some other name, does not
    # become a second owner. Import-time loads run before the hook and still
    # take the stack.
    chosen = owner if owner is not None else _owner.get()
    if chosen is None:
        chosen = _calling_test_module()
    if chosen is None:
        raise RuntimeError("evidence loader has no owning test module")
    if _owner.get() != chosen:
        activate(chosen)
    resolved = str(Path(path).resolve())
    if not _path_is_evidence(resolved):
        raise ValueError("evidence loader only loads an evidence harness")
    state = _ensure_owner(chosen)
    cached = state.by_path.get(resolved)
    if cached is not None:
        state.by_name[name] = cached
        sys.modules[name] = cached
        return cached
    spec = importlib.util.spec_from_file_location(name, resolved)
    if spec is None or spec.loader is None:
        raise ImportError("cannot load evidence harness")
    module = importlib.util.module_from_spec(spec)
    state.by_path[resolved] = module
    state.by_name[name] = module
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        if state.by_path.get(resolved) is module:
            state.by_path.pop(resolved, None)
        if state.by_name.get(name) is module:
            state.by_name.pop(name, None)
        if sys.modules.get(name) is module:
            del sys.modules[name]
        raise
    loaded_from = getattr(module, "__file__", None)
    if isinstance(loaded_from, str):
        state.by_path[str(Path(loaded_from).resolve())] = module
    return module


class _WatchedModule(ModuleType):
    def __setattr__(self, name: str, value: object) -> None:
        _record(self, name, value)
        super().__setattr__(name, value)
        if isinstance(value, type):
            _arm_class(value)


class _Modules(dict[str, ModuleType]):
    """``sys.modules`` view that hides another owner's evidence copies.

    Import uses ``get``, ``in``, subscription, and ``pop``. ``pop`` on a
    dict subclass does not call ``__delitem__``, so it is overridden too.
    Evidence modules live in the owner map and in this dict; ``packages.*``
    and ``tests.*`` stay shared in this dict only.

    Replacing ``sys.modules`` does not replace the interpreter's module
    dict. Shared modules are mirrored there so a C import can see them.
    """

    def get(self, key: str, default: Any = None) -> Any:
        found = self._lookup(key)
        if found is _MISSING:
            return default
        return found

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str):
            return False
        return self._lookup(key) is not _MISSING

    def __getitem__(self, key: str) -> ModuleType:
        found = self._lookup(key)
        if found is _MISSING:
            raise KeyError(key)
        return found  # type: ignore[no-any-return]

    def __setitem__(self, key: str, value: ModuleType) -> None:
        owner_name = _owner.get()
        if owner_name is not None and _is_evidence_module(value):
            state = _ensure_owner(owner_name)
            state.by_name[key] = value
            loaded_from = getattr(value, "__file__", None)
            if isinstance(loaded_from, str):
                state.by_path.setdefault(str(Path(loaded_from).resolve()), value)
        dict.__setitem__(self, key, value)
        if _is_packages_module(value):
            _arm_module(value)
        _mirror_shared(key, value)

    def __delitem__(self, key: str) -> None:
        self._forget(key)
        current = dict.get(self, key, _MISSING)
        dict.__delitem__(self, key)
        _drop_shared(key, current)

    def pop(self, key: str, *args: Any) -> Any:
        visible = self._lookup(key)
        self._forget(key)
        try:
            stored: Any = dict.pop(self, key)
        except KeyError:
            stored = _MISSING
        if stored is not _MISSING:
            _drop_shared(key, stored)
        if visible is not _MISSING:
            return visible
        if stored is not _MISSING:
            return stored
        if args:
            return args[0]
        raise KeyError(key)

    def _lookup(self, key: str) -> Any:
        owner_name = _owner.get()
        state = _owners.get(owner_name) if owner_name is not None else None
        if state is not None and key in state.by_name:
            return state.by_name[key]
        if not dict.__contains__(self, key):
            return _MISSING
        module = dict.__getitem__(self, key)
        if owner_name is not None and _is_evidence_module(module):
            return _MISSING
        return module

    def _forget(self, key: str) -> None:
        owner_name = _owner.get()
        if owner_name is None:
            return
        state = _owners.get(owner_name)
        if state is None:
            return
        module = state.by_name.pop(key, None)
        if module is None:
            return
        loaded_from = getattr(module, "__file__", None)
        if isinstance(loaded_from, str):
            resolved = str(Path(loaded_from).resolve())
            if state.by_path.get(resolved) is module:
                state.by_path.pop(resolved, None)


def _mirror_shared(key: str, value: object) -> None:
    real = _interpreter_modules
    if real is None or _is_evidence_module(value):
        return
    real[key] = value


def _drop_shared(key: str, value: object) -> None:
    real = _interpreter_modules
    if real is None or value is _MISSING or _is_evidence_module(value):
        return
    if dict.get(real, key) is value:
        del real[key]


def _ensure_overlay() -> _Modules:
    global _interpreter_modules
    current = sys.modules
    if isinstance(current, _Modules):
        return current
    _interpreter_modules = current
    overlay = _Modules(current)
    sys.modules = overlay
    return overlay


def _ensure_owner(owner: str) -> _OwnerState:
    state = _owners.get(owner)
    if state is None:
        state = _OwnerState()
        _owners[owner] = state
    return state


def _calling_test_module() -> str | None:
    frame: FrameType | None = sys._getframe()
    for _ in range(48):
        if frame is None:
            return None
        frame = frame.f_back
        if frame is None:
            return None
        module_name = frame.f_globals.get("__name__")
        module_file = frame.f_globals.get("__file__")
        if not isinstance(module_name, str) or not isinstance(module_file, str):
            continue
        file_name = Path(module_file).name
        if not file_name.startswith("test_") or not file_name.endswith(".py"):
            continue
        if module_name == "__main__":
            continue
        return module_name
    return None


def _path_is_evidence(filename: str) -> bool:
    return any(part.endswith("-evidence") for part in filename.split("/"))


def _is_evidence_module(module: object) -> bool:
    if not isinstance(module, ModuleType):
        return False
    loaded_from = getattr(module, "__file__", None)
    return isinstance(loaded_from, str) and _path_is_evidence(loaded_from)


def _is_packages_module(module: object) -> bool:
    if not isinstance(module, ModuleType):
        return False
    name = module.__name__
    return name == "packages" or name.startswith("packages.")


def _is_submodule_binding(obj: object, name: str, value: object) -> bool:
    """True when ``value`` is the child module importlib binds onto ``obj``."""
    if not isinstance(obj, ModuleType) or not isinstance(value, ModuleType):
        return False
    parent_name = obj.__name__
    child_name = value.__name__
    if child_name != f"{parent_name}.{name}":
        return False
    return sys.modules.get(child_name) is value


def _is_packages_object(obj: object) -> bool:
    if isinstance(obj, ModuleType):
        return _is_packages_module(obj)
    if isinstance(obj, type):
        module_name = getattr(obj, "__module__", "")
        return module_name == "packages" or (
            isinstance(module_name, str) and module_name.startswith("packages.")
        )
    return False


def _called_from_evidence() -> bool:
    frame: FrameType | None = sys._getframe()
    for _ in range(48):
        if frame is None:
            return False
        frame = frame.f_back
        if frame is None:
            return False
        filename = frame.f_code.co_filename
        if _path_is_evidence(filename):
            return True
    return False


def _arm_existing_packages() -> None:
    for module in list(sys.modules.values()):
        if _is_packages_module(module):
            _arm_module(module)


def _arm_module(module: ModuleType) -> None:
    if not _is_packages_module(module):
        return
    if id(module) in _armed_modules:
        return
    _armed_modules.add(id(module))
    if type(module) is ModuleType:
        try:
            module.__class__ = _WatchedModule
        except (TypeError, AttributeError):
            return
    for value in list(module.__dict__.values()):
        if isinstance(value, type):
            _arm_class(value)


def _arm_class(cls: type) -> None:
    if id(cls) in _armed_classes:
        return
    _armed_classes.add(id(cls))
    if not _is_packages_object(cls):
        return
    meta = type(cls)
    try:
        watcher = _watcher_for(meta)
        cls.__class__ = watcher
    except (TypeError, AttributeError):
        return


def _watcher_for(meta: type) -> type:
    found = _class_watchers.get(meta)
    if found is not None:
        return found

    class _ClassWatcher(meta):  # type: ignore[misc]
        def __setattr__(cls, name: str, value: object) -> None:
            _record(cls, name, value)
            super().__setattr__(name, value)

    _ClassWatcher.__name__ = "Watched" + meta.__name__
    _class_watchers[meta] = _ClassWatcher
    return _ClassWatcher


def _record(obj: object, name: str, value: object) -> None:
    if _applying.get() or name.startswith("__"):
        return
    if _owner.get() is None or not _called_from_evidence():
        return
    if not _is_packages_object(obj):
        return
    if _is_submodule_binding(obj, name, value):
        return
    owner_name = _owner.get()
    if owner_name is None:
        return
    key = (id(obj), name)
    if key not in _baseline:
        owned, previous = _own_value(obj, name)
        _baseline[key] = (owned, previous)
    _watched[id(obj)] = obj
    _ensure_owner(owner_name).written[key] = value


def _own_value(obj: object, name: str) -> tuple[bool, object]:
    mapping = getattr(obj, "__dict__", None)
    if mapping is not None and name in mapping:
        return True, mapping[name]
    return False, None


def _adopt_outside_writes(state: _OwnerState | None) -> None:
    """Keep a value someone other than the leaving owner's harness set.

    Before the engine switches away from an owner, a watched attribute should
    hold that owner's write, or the baseline where it wrote nothing. A value
    that is neither came from outside the loader's watch (a test's own patch,
    for instance). It becomes the baseline, and the owner forgets its write,
    so no later switch puts the overwritten value back.
    """
    for key, (existed, previous) in list(_baseline.items()):
        obj = _watched.get(key[0])
        if obj is None:
            continue
        if state is not None and key in state.written:
            expected: tuple[bool, object] = (True, state.written[key])
        else:
            expected = (existed, previous)
        live = _own_value(obj, key[1])
        if live[0] == expected[0] and (not live[0] or live[1] is expected[1]):
            continue
        _baseline[key] = live
        if state is not None:
            state.written.pop(key, None)


def _show(owner: str | None) -> None:
    keys: set[_WriteKey] = set(_baseline)
    state = _owners.get(owner) if owner is not None else None
    token = _applying.set(True)
    try:
        for key in keys:
            obj = _watched.get(key[0])
            if obj is None:
                continue
            if state is not None and key in state.written:
                _raw_set(obj, key[1], state.written[key])
                continue
            existed, previous = _baseline[key]
            if existed:
                _raw_set(obj, key[1], previous)
            elif _own_value(obj, key[1])[0]:
                _, current = _own_value(obj, key[1])
                if not _is_submodule_binding(obj, key[1], current):
                    _raw_del(obj, key[1])
    finally:
        _applying.reset(token)


def _raw_set(obj: object, name: str, value: object) -> None:
    if isinstance(obj, ModuleType):
        ModuleType.__setattr__(obj, name, value)
        return
    if isinstance(obj, type):
        type.__setattr__(obj, name, value)
        return
    object.__setattr__(obj, name, value)


def _raw_del(obj: object, name: str) -> None:
    if isinstance(obj, ModuleType):
        ModuleType.__delattr__(obj, name)
        return
    if isinstance(obj, type):
        type.__delattr__(obj, name)
        return
    object.__delattr__(obj, name)


def _publish(owner: str) -> None:
    state = _owners.get(owner)
    modules = sys.modules
    if state is None or not isinstance(modules, _Modules):
        return
    for name, module in state.by_name.items():
        dict.__setitem__(modules, name, module)


def _unpublish(owner: str) -> None:
    state = _owners.get(owner)
    modules = sys.modules
    if state is None or not isinstance(modules, _Modules):
        return
    for name, module in state.by_name.items():
        if dict.get(modules, name) is module:
            dict.__delitem__(modules, name)


def _drop_modules(state: _OwnerState) -> None:
    modules = sys.modules
    if not isinstance(modules, _Modules):
        return
    for name, module in list(state.by_name.items()):
        if dict.get(modules, name) is module:
            dict.__delitem__(modules, name)
    state.by_name.clear()
    state.by_path.clear()
    state.written.clear()
