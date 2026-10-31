"""Track 1: line 25b waits for every withholding family's closure on core v61.

Runs go through ``live_coordinate_run`` on the committed packages (core v60 and
v61). On v60 a recorded Form 1099-INT, -DIV, -R, -G box 4 or SSA-1099 box 6
amount counts on line 25b whether or not its family is closed; v61 blocks line
25b ``SOURCE_SET_UNCLOSED`` instead, and the lines behind it wait. A return
whose withholding is complete publishes on v61 exactly the values it does on
v60. Synthetic ``demo.*`` data only.
"""

from __future__ import annotations

import copy
import json
import unittest
from typing import Any, cast

from packages.derivation.production_resolver import PublicationSurface
from packages.tax.loader import domain_package_companion_declarations
from tests.test_form_1099_k_income import (
    PACKAGE_V60,
    RELEASE_V58,
    SURFACE_V60,
    _handover,
    _run_finished,
    _values,
)
from tests.test_form_1099_withholding import (
    CONTENT,
    DIV_B4_FAMILY,
    G_B4_CLOSURE,
    G_B4_FAMILY,
    INT_B4_FAMILY,
    IRA_B4_FAMILY,
    RELEASE_DIR,
    SSA_B6_CLOSURE,
    SSA_B6_FAMILY,
    YEAR,
    _base,
    _dividends,
    _interest,
    _retirements,
    _social_security,
    _social_security_withholding,
    _unemployment,
    _unemployment_withholding,
)
from tests.test_refund_or_amount_owed_track1 import _act, _attested, _finish

PACKAGE_V61 = CONTENT / "package.core-calculations.v61.json"
RELEASE_V59 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v59.json"
SURFACE_V61 = PublicationSurface(RELEASE_DIR, CONTENT / "published-packages.v59.json", CONTENT)

L24 = "tax.us.2025.tax.line24-total-tax"
L25A = "tax.us.2025.payments.line25a"
L25B = "tax.us.2025.payments.line25b"
L25D = "tax.us.2025.payments.line25d"
L33 = "tax.us.2025.payments.line33"
L35A = "tax.us.2025.payments.line35a-refunded"
L37 = "tax.us.2025.payments.line37-amount-owed"
BEHIND = (L25D, L33, L35A, L37)

# family key -> (family id, closure fact, source set the guard reads, statement income)
FAMILIES: dict[str, tuple[str, str, str]] = {
    "int": (INT_B4_FAMILY, "tax.us.2025.f1099int.b4.source-closure", "tax.us.2025.f1099int.b4"),
    "div": (DIV_B4_FAMILY, "tax.us.2025.f1099div.b4.source-closure", "tax.us.2025.f1099div.b4"),
    "ira": (IRA_B4_FAMILY, "tax.us.2025.f1099r.box4.source-closure", "tax.us.2025.f1099r.box4"),
    "g": (G_B4_FAMILY, G_B4_CLOSURE, "tax.us.2025.f1099g.b4"),
    "ssa": (SSA_B6_FAMILY, SSA_B6_CLOSURE, "tax.us.2025.ssa1099.b6"),
}
AMOUNTS = {"g": (600.0, 400.0), "ssa": (800.0, 500.0), "int": (50.0, 30.0), "div": (40.0, 20.0), "ira": (1200.0, 800.0)}
ALL = set(FAMILIES)


# --- running -------------------------------------------------------------------


def _run_on(acts: list[dict[str, object]], run_id: str, core: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if core == "v60":
        package, version, release, rel_version, surface = PACKAGE_V60, "v60", RELEASE_V58, "v58", SURFACE_V60
    elif core == "v61":
        package, version, release, rel_version, surface = PACKAGE_V61, "v61", RELEASE_V59, "v59", SURFACE_V61
    else:
        raise AssertionError(core)
    finished = _finish(
        copy.deepcopy(acts), package_path=package, package_version=version,
        release_path=release, release_version=rel_version, note=run_id,
    )
    finished = _handover(finished, surface=surface, reconfirm=True)
    return _run_finished(finished, run_id, surface)


class Result:
    def __init__(self, pubs: dict[str, Any], blocked: list[dict[str, Any]]) -> None:
        self.pubs, self.blocked = pubs, blocked
        self.values = _values(pubs)

    def value(self, symbol: str) -> float:
        return float(self.values[symbol])

    def root(self, token: str) -> dict[str, Any]:
        rows = [r for r in self.blocked if str(r["artifact_id"]).endswith("rule." + token)]
        assert len(rows) == 1, (token, self.blocked)
        return rows[0]

    def roots(self) -> list[tuple[str, str, tuple[str, ...]]]:
        return sorted(
            (str(r["artifact_id"]), str(r["code"]), tuple(str(m) for m in r["missing"]))
            for r in self.blocked if r["code"] != "DEPENDENCY_ABSENT"
        )


def _pair(acts: list[dict[str, object]], token: str) -> tuple[Result, Result]:
    return (
        Result(*_run_on(acts, f"demo.wc.{token}.v60", "v60")),
        Result(*_run_on(acts, f"demo.wc.{token}.v61", "v61")),
    )


# --- closure manipulation (as the P0 probe) --------------------------------------


def _payload(act: dict[str, object]) -> dict[str, Any]:
    return cast(dict[str, Any], act["payload"])


def _horizons(acts: list[dict[str, object]], family_id: str) -> list[str]:
    out: list[str] = []
    for act in acts:
        p = _payload(act)
        if act["kind"] == "horizon-genesis" and p["family"]["id"] == family_id:
            out.append(str(p["horizon_id"]))
        elif act["kind"] == "member-transition" and p["family"]["id"] == family_id:
            out.append(str(p["successor"]["id"]))
    return out


def _strip_closure(acts: list[dict[str, object]], closure_type: str) -> list[dict[str, object]]:
    kept = []
    for act in acts:
        finding = _payload(act).get("finding")
        if isinstance(finding, dict) and str(finding.get("fact_id", "")).startswith(closure_type + "|"):
            continue
        kept.append(act)
    return kept


def _set_closure(acts: list[dict[str, object]], key: str, mode: str) -> list[dict[str, object]]:
    """mode: none (unanswered) | head (true at the current horizon) | first (true at the
    horizon after the first member, so any later member leaves it stale)."""
    family_id, closure_type, _ = FAMILIES[key]
    out = _strip_closure(acts, closure_type)
    horizons = _horizons(out, family_id)
    if mode == "none":
        return out
    horizon = horizons[-1] if mode == "head" else horizons[1]
    closure = _act(len(out), "assertion", {
        "finding": _attested(f"demo.wc.closure.{key}.{mode}", f"{closure_type}|family-horizon={horizon},tax-year={YEAR}", True),
    })
    if mode == "head":
        out.append(closure)
        return out
    for index, act in enumerate(out):
        p = _payload(act)
        if act["kind"] == "member-transition" and p["family"]["id"] == family_id and str(p["successor"]["id"]) == horizon:
            out.insert(index + 1, closure)
            return out
    raise AssertionError("first-member horizon not found")


# --- returns -------------------------------------------------------------------


def _family_return(key: str, n: int, amounts: list[float | None], mode: str) -> list[dict[str, object]]:
    """``n`` statements of one family, box 4/6 amounts as given, that family's closure per
    ``mode``, every other withholding family closed empty."""
    acts = _base(wages=50000.0, w2_withheld=4500.0)
    if key == "g":
        _unemployment(acts, [6000.0, 4000.0][:n], authority=None)
        _unemployment_withholding(acts, amounts, close=False)
        _social_security_withholding(acts, [])
    elif key == "ssa":
        _social_security(acts, [12000.0, 8000.0][:n], witness=None)
        _unemployment_withholding(acts, [])
        _social_security_withholding(acts, amounts, close=False)
    else:
        income = [10000.0, 5000.0][:n] if key == "ira" else [500.0, 300.0][:n]
        {"int": _interest, "div": _dividends, "ira": _retirements}[key](acts, list(zip(income, amounts)))
        _unemployment_withholding(acts, [])
        _social_security_withholding(acts, [])
    return _set_closure(acts, key, mode)


def _all_families(*, closed: set[str], joint: bool = False) -> list[dict[str, object]]:
    acts = _base(wages=80000.0 if joint else 50000.0, w2_withheld=7000.0 if joint else 4500.0, joint=joint)
    _unemployment(acts, [5000.0, 4000.0], authority=None)
    _unemployment_withholding(acts, [500.0, 400.0], close=False)
    _social_security(acts, [12000.0, 8000.0], witness=None)
    _social_security_withholding(acts, [800.0, 500.0], close=False)
    _interest(acts, [(500.0, 50.0), (300.0, 30.0)])
    _dividends(acts, [(400.0, 40.0), (200.0, 20.0)])
    _retirements(acts, [(10000.0, 1200.0), (5000.0, 800.0)])
    for key in FAMILIES:
        acts = _set_closure(acts, key, "head" if key in closed else "none")
    return acts


def _no_withholding() -> list[dict[str, object]]:
    acts = _base(wages=50000.0, w2_withheld=4500.0)
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    return acts


def _assert_blocked_at_25b(test: unittest.TestCase, result: Result, source_set: str) -> None:
    row = result.root("form1040-line25b")
    test.assertEqual(row["code"], "SOURCE_SET_UNCLOSED")
    test.assertEqual(list(row["missing"]), [source_set])
    for symbol in (L25B, *BEHIND):
        test.assertNotIn(symbol, result.values, symbol)
    for symbol in (L24, L25A):
        test.assertIn(symbol, result.values, symbol)
    blocked_ids = {str(r["artifact_id"]) for r in result.blocked}
    for token in ("form1040-line25d", "form1040-line33"):
        test.assertTrue(any(b.endswith("rule." + token) for b in blocked_ids), token)


# --- tests ---------------------------------------------------------------------


class UnclosedFamilyBlocksLine25b(unittest.TestCase):
    def _check(self, key: str, cause: str, amounts: list[float | None], n: int, mode: str, v60_25b: float) -> None:
        a, b = AMOUNTS[key]
        acts = _family_return(key, n, amounts, mode)
        v60, v61 = _pair(acts, f"{key}.{cause}")
        # v60 pinned: the recorded amount counts while the family is unclosed.
        self.assertEqual(v60.value(L25B), v60_25b)
        self.assertEqual(v60.blocked, [])
        _assert_blocked_at_25b(self, v61, FAMILIES[key][2])
        # Answering the closure publishes line 25b with every recorded amount.
        answered = _family_return(key, n, amounts, "head")
        _, done = _pair(answered, f"{key}.{cause}.answered")
        self.assertEqual(done.value(L25B), a + b if n == 2 and amounts[-1] is not None else a)
        self.assertEqual(done.blocked, [])
        for symbol in BEHIND:
            self.assertIn(symbol, done.values)

    def _family(self, key: str) -> None:
        a, b = AMOUNTS[key]
        self._check(key, "unanswered", [a], 1, "none", a)
        self._check(key, "stale", [a, b], 2, "first", a + b)

    def test_1099int(self) -> None:
        self._family("int")

    def test_1099div(self) -> None:
        self._family("div")

    def test_1099r(self) -> None:
        self._family("ira")

    def test_1099g(self) -> None:
        self._family("g")

    def test_ssa1099(self) -> None:
        self._family("ssa")


class TwoFamiliesUnanswered(unittest.TestCase):
    def test_names_the_first_then_the_second(self) -> None:
        both = _all_families(closed=ALL - {"int", "g"})
        v60, v61 = _pair(both, "two.both")
        self.assertEqual(v60.value(L25B), 4340)
        _assert_blocked_at_25b(self, v61, FAMILIES["int"][2])
        _, second = _pair(_all_families(closed=ALL - {"g"}), "two.second")
        _assert_blocked_at_25b(self, second, FAMILIES["g"][2])
        _, none = _pair(_all_families(closed=ALL), "two.none")
        self.assertEqual(none.value(L25B), 4340)
        self.assertEqual(none.blocked, [])

    def test_names_each_family_in_guard_order(self) -> None:
        # The v3 guard lists INT, DIV, 1099-R, G, SSA; the block names the
        # first still open, so closing them in turn walks the whole order.
        order = ["int", "div", "ira", "g", "ssa"]
        for index, key in enumerate(order):
            acts = _all_families(closed=set(order[:index]))
            result = Result(*_run_on(acts, f"demo.wc.order.{key}.v61", "v61"))
            with self.subTest(open_first=key):
                _assert_blocked_at_25b(self, result, FAMILIES[key][2])

    def test_joint_return_with_one_family_unanswered(self) -> None:
        v60, v61 = _pair(_all_families(closed=ALL - {"g"}, joint=True), "joint.g")
        self.assertIn(L25B, v60.values)
        _assert_blocked_at_25b(self, v61, FAMILIES["g"][2])


class CompleteWithholdingIsUnchanged(unittest.TestCase):
    def _same(self, acts: list[dict[str, object]], token: str) -> tuple[Result, Result]:
        v60, v61 = _pair(acts, token)
        self.assertEqual(v61.values, v60.values)
        self.assertEqual(v61.roots(), v60.roots())
        return v60, v61

    def test_every_family_complete(self) -> None:
        _, v61 = self._same(_all_families(closed=ALL), "complete.single")
        self.assertEqual(v61.value(L25B), 4340)
        self.assertEqual(v61.blocked, [])

    def test_every_family_complete_joint(self) -> None:
        self._same(_all_families(closed=ALL, joint=True), "complete.joint")

    def test_closed_empty(self) -> None:
        _, v61 = self._same(_no_withholding(), "closed-empty")
        self.assertEqual(v61.value(L25B), 0)

    def test_closed_over_a_statement_with_no_box_4_answer(self) -> None:
        _, v61 = self._same(_family_return("g", 1, [None], "head"), "g.blank")
        self.assertEqual(v61.value(L25B), 0)


class W2BoxTwoIsUnchanged(unittest.TestCase):
    """Form W-2 box 2 already blocks on its own closure; v61 neither adds nor removes that."""

    def test_unanswered_box_2_closure_blocks_line_25a_on_both(self) -> None:
        acts = _strip_closure(_no_withholding(), "tax.us.2025.w2-box2.source-closure")
        v60, v61 = _pair(acts, "w2.unanswered")
        self.assertNotIn(L25A, v60.values)
        self.assertNotIn(L25A, v61.values)
        row = v61.root("form1040-line25a")
        self.assertEqual(row["code"], "SOURCE_SET_UNCLOSED")
        self.assertEqual(list(row["missing"]), ["tax.us.2025.w2-box2"])
        self.assertEqual(v61.roots(), v60.roots())

    def test_answered_box_2_is_identical(self) -> None:
        v60, v61 = _pair(_no_withholding(), "w2.answered")
        self.assertEqual(v61.value(L25A), 4500)
        self.assertEqual(v61.values, v60.values)


class RegistryDiff(unittest.TestCase):
    def test_v59_registry_only_adds_entries_to_v58(self) -> None:
        old = json.loads((CONTENT / "published-packages.v58.json").read_text(encoding="utf-8"))
        new = json.loads((CONTENT / "published-packages.v59.json").read_text(encoding="utf-8"))
        for section in ("citizens", "packages"):
            before = {(e["id"], e["version"]): e["checksum"] for e in old[section]}
            after = {(e["id"], e["version"]): e["checksum"] for e in new[section]}
            self.assertEqual(len(before), len(old[section]))
            self.assertEqual({k: after[k] for k in before}, before)
        added_citizens = {(e["id"], e["version"]) for e in new["citizens"]} - {(e["id"], e["version"]) for e in old["citizens"]}
        added_packages = {(e["id"], e["version"]) for e in new["packages"]} - {(e["id"], e["version"]) for e in old["packages"]}
        self.assertEqual(added_citizens, {("tax.us.2025.rule.form1040-line25b", "v3")})
        self.assertEqual(added_packages, {("tax.us.2025.package.core-calculations", "v61")})

    def test_v61_differs_from_v60_only_in_the_line_25b_member(self) -> None:
        old = json.loads(PACKAGE_V60.read_text(encoding="utf-8"))
        new = json.loads(PACKAGE_V61.read_text(encoding="utf-8"))

        def strip(doc: dict[str, Any]) -> dict[str, Any]:
            doc = copy.deepcopy(doc)
            doc.pop("package_checksum", None)
            doc.pop("version", None)
            doc["members"] = [m for m in doc["members"] if m["id"] != "tax.us.2025.rule.form1040-line25b"]
            return doc

        self.assertEqual(strip(new), strip(old))
        pins = {m["id"]: m["version"] for m in new["members"]}
        self.assertEqual(pins["tax.us.2025.rule.form1040-line25b"], "v3")

    def test_v61_shares_the_v60_withholding_declaration(self) -> None:
        core = "tax.us.2025.package.core-calculations"
        declarations = domain_package_companion_declarations()
        self.assertIs(declarations[(core, "v61")], declarations[(core, "v60")])


if __name__ == "__main__":
    unittest.main()
