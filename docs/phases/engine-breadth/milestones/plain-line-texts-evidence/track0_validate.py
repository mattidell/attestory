"""Apply Track 0 adversarial wording fixes, verify byte-undo witnesses, and validate scratch v96.

Run: python3 track0_validate.py <new-scratch-directory-outside-repository>
All runtime content and controls stay outside the repository.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


runtime = load("plt_t0_validation_runtime", HERE / "p0c_runtime.py")
prior = load("plt_t0_byte_helpers", HERE / "p0b_build.py")
from tools.package_successor import generate_to_directory, load_corpus
from packages.derivation.package_validation import (
    validate_package,
    package_instance_checksum,
    load_published_citizen_checksums,
)
from packages.derivation.loader import DerivationSchemas


TRACK0_FIXES: dict[tuple[str, str], tuple[str, str, str]] = {
    (
        "tax.us.2025.form.sch8812.line-6",
        "dispositions.computed_zero.explain",
    ): (
        "The number of other dependents for this credit is zero after your answers and dependent records are checked.",
        "Schedule 8812 line 6 is zero because you confirmed that you have no other dependents for this credit, or no recorded dependent qualifies.",
        "Item 1 failure in P0c: drawn on 699 pages including returns with no dependent records where tax.us.2025.ctc.no-other-dependent is yes; P0c claimed dependent records were checked.",
    ),
    (
        "tax.us.2025.form1040.line-10",
        "dispositions.published_value.explain",
    ): (
        "Your adjustments to income come from Schedule 1 line 26 and are subtracted from total income to get adjusted gross income.",
        "Your adjustments to income come from the completed Schedule 1 line 26 total and are subtracted from line 9 total income on line 11a.",
        "Item 2 failure in P0c: predecessor proved Schedule 1 line 26 completeness and named lines 9 and 11a; P0c dropped completeness and the line references.",
    ),
    (
        "tax.us.2025.form1040.line-25a",
        "dispositions.computed_zero.explain",
    ): (
        "The federal income tax withholding in box 2 of your recorded Forms W-2 totals zero after rounding.",
        "Your Form W-2 federal income tax withholding on line 25a is zero because no Forms W-2 are recorded or the box 2 amounts on the completed Forms W-2 round to zero.",
        "Item 1 and Item 3 failure in P0c: rule.form1040-line25a.v3 pins rounding.convention so closed-empty w2/w2-box2 also selects computed_zero; P0c claimed recorded Forms W-2 exist when none are recorded and dropped completeness.",
    ),
    (
        "tax.us.2025.form1040.line-25b",
        "dispositions.computed_zero.explain",
    ): (
        "The recorded federal income tax withholding from Forms 1099 and SSA-1099 totals zero after rounding.",
        "Your Form 1099 and Form SSA-1099 federal income tax withholding on line 25b is zero because none is recorded or the completed withholding amounts round to zero.",
        "Item 1 and Item 3 failure in P0c: drawn on 61 pages where all six withholding families are closed-empty; P0c claimed recorded withholding from Forms 1099 and SSA-1099 exists and dropped completeness.",
    ),
    (
        "tax.us.2025.form1040.line-25c",
        "dispositions.computed_zero.explain",
    ): (
        "The federal income tax withholding in box 4 of your recorded Forms W-2G totals zero after rounding.",
        "Your other-form federal income tax withholding on line 25c is zero because no Forms W-2G are recorded or the box 4 amounts on the completed Forms W-2G round to zero.",
        "Item 1 and Item 3 failure in P0c: drawn on 699 pages including 695+ pages where w2g.b4 is closed-empty; P0c claimed recorded Forms W-2G exist when none are recorded and dropped completeness.",
    ),
    (
        "tax.us.2025.form1040.line-2a",
        "dispositions.computed_zero.explain",
    ): (
        "You confirmed the tax-exempt interest records are complete, and the combined Form 1099-INT box 8 and Form 1099-DIV box 12 amount is zero after rounding.",
        "Your tax-exempt interest on line 2a is zero because no Form 1099-INT box 8 or Form 1099-DIV box 12 amounts are recorded or their total rounds to zero, with the required tax-exempt interest records and answers complete.",
        "Item 1 and Item 2 failure in P0c: drawn on 697 pages where neither Form 1099-INT box 8 nor Form 1099-DIV box 12 is recorded; P0c implied tax-exempt interest records exist and omitted the required scope answers.",
    ),
    (
        "tax.us.2025.form1040.line-2a",
        "dispositions.published_value.explain",
    ): (
        "Your tax-exempt interest is the combined amount from the completed Form 1099-INT box 8 and Form 1099-DIV box 12 records, with the other required tax-exempt interest answers complete. It is reported on line 2a but is not included in taxable income.",
        "Your tax-exempt interest on line 2a is the rounded total from any recorded Form 1099-INT box 8 and Form 1099-DIV box 12 amounts, with the required tax-exempt interest records and answers complete. It is reported on line 2a but is not included in taxable income.",
        "Item 1 and Item 2 failure in P0c: drawn on carried_one_exempt_dividend where Path A (no-f1099int-tax-exempt=yes) has no Form 1099-INT box 8 records; P0c replaced predecessor 'and/or' with 'completed Form 1099-INT box 8 and Form 1099-DIV box 12 records' and dropped rounding.",
    ),
    (
        "tax.us.2025.form1040.line-2b",
        "dispositions.computed_zero.explain",
    ): (
        "Your taxable interest is zero after the completed interest totals and recorded adjustments are combined and rounded.",
        "Your taxable interest on line 2b is zero because no taxable interest is recorded or the completed interest amounts, after any applicable adjustments, round to zero.",
        "Item 1 failure in P0c: drawn on 692 pages where no interest and no adjustments are recorded; P0c claimed 'recorded adjustments' exist.",
    ),
    (
        "tax.us.2025.form1040.line-2b",
        "dispositions.published_value.explain",
    ): (
        "Your taxable interest on line 2b is the Schedule B Part I total, rounded once to whole dollars.",
        "Your taxable interest on line 2b is the completed taxable interest total (including any Schedule B Part I adjustments), rounded once to whole dollars.",
        "Item 1 and Item 3 failure in P0c: in all 7 recorded lists drawing this text, Schedule B is guard_inapplicable (not required); P0c unconditionally called the value 'the Schedule B Part I total'.",
    ),
    (
        "tax.us.2025.form1040.line-3a",
        "dispositions.computed_zero.explain",
    ): (
        "The qualified dividends in box 1b of your recorded Forms 1099-DIV total zero after rounding, and those records are complete.",
        "Your qualified dividends on line 3a are zero because no Form 1099-DIV box 1b amounts are recorded or their total rounds to zero, and those records are complete.",
        "Item 1 failure in P0c: drawn on 699 pages including 690+ pages where f1099div.1b is closed-empty; P0c claimed 'box 1b of your recorded Forms 1099-DIV' exists when no Form 1099-DIV is recorded.",
    ),
    (
        "tax.us.2025.form1040.line-3b",
        "dispositions.computed_zero.explain",
    ): (
        "The ordinary dividends in box 1a of your recorded Forms 1099-DIV total zero after rounding, and those records are complete.",
        "Your ordinary dividends on line 3b are zero because no Form 1099-DIV box 1a amounts are recorded or their total rounds to zero, and those records are complete.",
        "Item 1 failure in P0c: drawn on 690 pages including 685+ pages where f1099div.1a is closed-empty; P0c claimed 'box 1a of your recorded Forms 1099-DIV' exists when no Form 1099-DIV is recorded.",
    ),
    (
        "tax.us.2025.form1040.line-3b",
        "dispositions.published_value.explain",
    ): (
        "Your ordinary dividends are the total of box 1a on your recorded Forms 1099-DIV.",
        "Your ordinary dividends on line 3b are the completed Form 1099-DIV box 1a total, rounded once to whole dollars.",
        "Item 1, Item 2, and Item 3 failure in P0c: rule.form1040-line3b.v2 requires f1099div.1a closure and rounds the box 1a subtotal to whole dollars; P0c omitted rounding and completeness, diverging from sibling lines 2b and Schedule D line 13.",
    ),
    (
        "tax.us.2025.form1040.line-6b",
        "dispositions.blocked.explain",
    ): (
        "The taxable part of your Social Security benefits cannot be calculated until the benefit records and worksheet information are complete.",
        "The taxable part of your Social Security benefits cannot be calculated because the Social Security benefit records, required income amounts, or worksheet answers are incomplete.",
        "Item 1 and Item 2 failure in P0c: in all 147 recorded lists drawing this text, ssa1099.benefits is already closed-empty and line 6b is blocked on required income symbol line7a-total; P0c replaced predecessor 'or' with 'until the benefit records and worksheet information are complete'.",
    ),
    (
        "tax.us.2025.form1040.line-7a",
        "dispositions.computed_zero.explain",
    ): (
        "Your capital gain or loss is zero after the Schedule D calculation, or after rounding the box 2a capital gain distributions when Schedule D is not required.",
        "Your capital gain or loss on line 7a is zero because no sales, capital loss carryovers, or Form 1099-DIV box 2a capital gain distributions are recorded, or the completed Schedule D or box 2a calculation rounds to zero.",
        "Item 1 and Item 2 failure in P0c: drawn on 80 pages including wage-only returns with no sales and no Form 1099-DIV box 2a distributions; P0c claimed 'rounding the box 2a capital gain distributions' or 'the Schedule D calculation' occurred and dropped completeness.",
    ),
    (
        "tax.us.2025.form1040.line-7b",
        "dispositions.guard_inapplicable.explain",
    ): (
        "The no-Schedule-D box is not checked because you recorded a sale for Form 8949 or Schedule D, or an answer shows that you do not meet the exception for filing without Schedule D.",
        "The Schedule D not required box on line 7b is not checked because you recorded a sale for Form 8949 or Schedule D, or an answer shows that you do not meet the exception for filing without Schedule D.",
        "Item 3 failure in P0c: 2025 Form 1040 and instructions name the line 7b checkbox 'Schedule D not required', not 'no-Schedule-D box'.",
    ),
    (
        "tax.us.2025.form1040.line-8",
        "dispositions.published_value.explain",
    ): (
        "Your additional income comes from Schedule 1 line 10. It is included once in your total income on Form 1040 line 9.",
        "Your additional income comes from the completed Schedule 1 line 10 total. It is included once in your total income on Form 1040 line 9.",
        "Item 2 failure in P0c: predecessor proved Schedule 1 line 10 completeness ('from complete Schedule 1 line 10'); P0c dropped completeness.",
    ),
    (
        "tax.us.2025.form1040.tax-after-credits",
        "dispositions.blocked.explain",
    ): (
        "Tax after credits is waiting for the tax on line 16, credits on line 20, or confirmation that lines 17 and 19 have no amount.",
        "Tax after credits is waiting for the tax on line 16, the credits on lines 19 and 20, or confirmation that line 17 has no amount.",
        "Item 1 failure in P0c: rule.form1040-tax-after-credits.v2 requires the computed line 19 credit (tax.us.2025.ctc.form1040-line19) and notes that v1's line 19 absence is no longer read; P0c falsely claimed line 19 needs confirmation that it has no amount.",
    ),
    (
        "tax.us.2025.schedule-d.line-13",
        "dispositions.computed_zero.explain",
    ): (
        "Your capital gain distributions are zero after the amounts in box 2a of your recorded Forms 1099-DIV are totaled and rounded.",
        "Your capital gain distributions on Schedule D line 13 are zero because no Form 1099-DIV box 2a amounts are recorded or their total rounds to zero, and those records are complete.",
        "Item 1 and Item 3 failure in P0c: drawn on 693 pages including 685+ pages where f1099div.2a is closed-empty; P0c claimed 'box 2a of your recorded Forms 1099-DIV' exists when no Form 1099-DIV is recorded and dropped completeness.",
    ),
    (
        "tax.us.2025.schedule-d.line-13",
        "dispositions.published_value.explain",
    ): (
        "Your capital gain distributions on Schedule D line 13 are the total of Form 1099-DIV box 2a, rounded once to whole dollars.",
        "Your capital gain distributions on Schedule D line 13 are the completed Form 1099-DIV box 2a total, rounded once to whole dollars.",
        "Item 2 and Item 3 failure in P0c: rule.f1099div-2a-subtotal.v3 requires f1099div.2a closure; stating 'completed' preserves closure basis and aligns with sibling lines 2b, 3b, and Schedule 1 line 7.",
    ),
    (
        "tax.us.2025.schedule1.line-10",
        "dispositions.published_value.explain",
    ): (
        "Your additional income on Schedule 1 line 10 is the completed total, including the recorded unemployment compensation and gambling winnings, with the answers about other income complete.",
        "Your additional income on Schedule 1 line 10 is the sum of line 7 (unemployment compensation) and line 8b (gambling winnings), with the required records and answers about other Schedule 1 Part I income complete.",
        "Item 1 failure in P0c: in all 6 recorded lists drawing this text (e.g. reuse_unemp_alone), no gambling winnings are recorded (line 8b is 0); P0c claimed 'including the recorded unemployment compensation and gambling winnings'.",
    ),
    (
        "tax.us.2025.schedule1.line-21",
        "dispositions.closure_backed_zero.explain",
    ): (
        "You confirmed that no student loan interest from Forms 1098-E needs to be included, so this deduction is zero.",
        "Your student loan interest deduction on Schedule 1 line 21 is zero because no Form 1098-E box 1 interest is recorded and those records are complete.",
        "Item 1 and Item 2 failure in P0c: closure_backed_zero on Schedule 1 line 21 is reached only when count(f1098e.box1-student-loan-interest) == 0 and f1098e.1 is closed-empty; P0c conflated closed-empty absence with per-statement inclusion ('needs to be included').",
    ),
    (
        "tax.us.2025.schedule1.line-7",
        "dispositions.published_value.explain",
    ): (
        "Your unemployment compensation on Schedule 1 line 7 is the total of box 1 on the completed Forms 1099-G records.",
        "Your unemployment compensation on Schedule 1 line 7 is the completed Form 1099-G box 1 total, rounded once to whole dollars.",
        "Item 1 and Item 3 failure in P0c: rule.schedule1-line7.v3 rounds unemployment.box1-subtotal to whole dollars; P0c omitted rounding and used inconsistent phrasing ('Forms 1099-G records').",
    ),
}


def main():
    scratch = Path(sys.argv[1]).resolve()
    assert scratch != REPO and REPO not in scratch.parents
    if scratch.exists():
        shutil.rmtree(scratch)
    source = REPO / "packages/content/tax/2025"
    releases_src = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
    content = scratch / "content"
    releases = scratch / "releases"
    shutil.copytree(source, content)
    shutil.copytree(releases_src, releases)

    p0b_manifest = json.loads((HERE / "p0b-wording.json").read_text())["replacements"]
    p0c_doc = json.loads((HERE / "p0c-wording.json").read_text())
    manifest = p0c_doc["replacements"]
    assert len(manifest) == len(p0b_manifest) == 57

    changes_out = []
    for idx, row in enumerate(manifest, 1):
        key = (row["id"], row["property"])
        if key in TRACK0_FIXES:
            p0c_text, new_text, reason = TRACK0_FIXES[key]
            assert row["new_shown"] in (p0c_text, new_text), key
            row["new_shown"] = new_text
            row["new"] = new_text
            changes_out.append({
                "index": idx,
                "id": row["id"],
                "version": row["version"],
                "property": row["property"],
                "old_shown": row["shown"],
                "p0c_shown": p0c_text,
                "track0_shown": new_text,
                "reason": reason,
            })

    assert len(changes_out) == len(TRACK0_FIXES) == 22
    p0c_doc["basis"] = (
        "Track 0 adversarial closure manifest: 57 properties in 50 citizens; "
        "35 P0c replacements retained and 22 refined for closed-empty absence, "
        "Path A/single-source states, Schedule B non-requirement, line 19 credit "
        "dependency, rounding, and 2025 instruction naming. Decisions 1-8."
    )
    manifest_bytes = json.dumps(p0c_doc, indent=2) + "\n"
    assert not re.search(r"/(?:Users|private|tmp|var)/", manifest_bytes)
    (HERE / "p0c-wording.json").write_text(manifest_bytes)
    (HERE / "track0-wording.json").write_text(manifest_bytes)
    (HERE / "track0-wording-changes.json").write_text(
        json.dumps({"changed_count": len(changes_out), "retained_count": 57 - len(changes_out), "changes": changes_out}, indent=2) + "\n"
    )

    package = json.loads((source / "package.core-calculations.v95.json").read_text())
    pins = {m["id"]: m for m in package["members"]}
    existing: dict[str, set[int]] = {}
    for path in source.glob("*.json"):
        body = json.loads(path.read_text())
        if re.fullmatch(r"v\d+", str(body.get("version"))):
            existing.setdefault(body.get("id"), set()).add(int(body["version"][1:]))

    grouped: dict[str, list[dict]] = {}
    for row in manifest:
        grouped.setdefault(row["file"], []).append(row)

    members, entries, successors = [], [], []
    for filename, replacements in sorted(grouped.items()):
        old_path = REPO / filename
        raw = old_raw = old_path.read_text()
        old = json.loads(raw)
        new_version = "v" + str(max(existing[old["id"]]) + 1)
        normalized = copy.deepcopy(old)
        undo = []
        for row in replacements:
            assert prior.property_at(old, row["property"]) == row["old"]
            prior.property_at(normalized, row["property"], row["new"], put=True)
            raw, before, after = prior.literal_replace(raw, row["old"], row["new"])
            undo.append((after, before))
        pattern = re.compile(r'(?m)^(  "version": ")' + re.escape(old["version"]) + r'("[,]?)$')
        raw, count = pattern.subn(lambda m: m[1] + new_version + m[2], raw)
        assert count == 1
        normalized["version"] = new_version
        assert json.loads(raw) == normalized
        recovered = raw
        recovered, count = re.subn(
            r'(?m)^(  "version": ")' + re.escape(new_version) + r'("[,]?)$',
            lambda m: m[1] + old["version"] + m[2],
            recovered,
        )
        assert count == 1
        for after, before in reversed(undo):
            recovered = recovered.replace(after, before, 1)
        assert recovered == old_raw, f"non-prose predecessor bytes changed in {filename}"
        next_name = re.sub(r"(?:\.v\d+)?\.json$", "." + new_version + ".json", old_path.name)
        assert not (content / next_name).exists()
        (content / next_name).write_text(raw)
        old_pin = pins[old["id"]]
        assert old_pin["version"] == old["version"]
        new_pin = {**old_pin, "version": new_version}
        members.append({"op": "replace", "old": old_pin, "new": new_pin})
        if any(e == {"id": old["id"], "version": old["version"]} for e in package["entrypoints"]):
            entries.append({
                "op": "replace",
                "old": {"id": old["id"], "version": old["version"]},
                "new": {"id": old["id"], "version": new_version},
            })
        successors.append({
            "id": old["id"],
            "old_version": old["version"],
            "new_version": new_version,
            "predecessor": filename,
            "successor_filename": next_name,
            "changed_properties": [r["property"] for r in replacements],
            "predecessor_sha256": hashlib.sha256(old_path.read_bytes()).hexdigest(),
            "successor_sha256": hashlib.sha256(raw.encode()).hexdigest(),
            "byte_undo_proof": True,
        })

    assert len(successors) == 50
    changes = {
        "package_version": "v96",
        "release_version": "v94",
        "members": members,
        "entrypoints": entries,
        "registry_sort": "id_version",
    }
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n")

    schemas = DerivationSchemas()
    corpus, _ = load_corpus(content)
    v95 = json.loads((content / "package.core-calculations.v95.json").read_text())
    old_checks = load_published_citizen_checksums(content / "published-packages.v93.json")
    before = validate_package(v95, corpus, schemas, old_checks)
    assert before.ok, before.issues
    stem = "demo.release.sli-worksheet-integration.2025"

    with runtime.injected_graph() as injection:
        report = generate_to_directory(
            content / "package.core-calculations.v95.json",
            content / "published-packages.v93.json",
            releases / (stem + ".v93.json"),
            content,
            scratch / "changes.json",
            scratch / "generated",
        )
        for src, dst in (
            ("package.json", content / "package.core-calculations.v96.json"),
            ("registry.json", content / "published-packages.v94.json"),
            ("release.json", releases / (stem + ".v94.json")),
        ):
            shutil.copyfile(scratch / "generated" / src, dst)
        checks = load_published_citizen_checksums(content / "published-packages.v94.json")
        v96 = json.loads((content / "package.core-calculations.v96.json").read_text())
        valid = validate_package(v96, corpus, schemas, checks)
        assert valid.ok, valid.issues
        controls = {}
        for name, pkg_obj, field_version, expected_ok in (
            ("v96_with_v6_rejected", v96, "v6", False),
            ("v95_with_v7_rejected", v95, "v7", False),
            ("v95_unchanged_under_injection", v95, "v6", True),
        ):
            changed = copy.deepcopy(pkg_obj)
            pin = next(p for p in changed["members"] if p["id"] == runtime.FIELD)
            pin["version"] = field_version
            changed["package_checksum"] = package_instance_checksum(changed)
            result = validate_package(changed, corpus, schemas, checks)
            codes = [i.code for i in result.issues]
            assert result.ok == expected_ok, (name, result.issues)
            if not expected_ok:
                assert codes == ["NOMINEE_RETURN_SUCCESSOR_GRAPH_MIXED"], (name, codes)
            controls[name] = {"passed": True, "ok": result.ok, "codes": codes}

    assert validate_package(v95, corpus, schemas, old_checks).ok
    (scratch / "core.json").write_text(
        json.dumps(
            {
                "version": "v96",
                "registry": "v94",
                "release_version": "v94",
                "content": str(content),
                "releases": str(releases),
                "loader_from": "v95",
            },
            indent=2,
        )
        + "\n"
    )
    output = {
        "status": "pass",
        "source": "published core v95 / registry v93 / release v93",
        "scratch": "core v96 / registry v94 / release v94",
        "injection": injection,
        "controls": controls,
        "v95_before_and_after_injection": "valid",
        "citizens": len(successors),
        "replacements": len(manifest),
        "wording_changes_from_p0c": len(changes_out),
        "byte_undo_proofs": len(successors),
        "generation": report,
        "successors": successors,
    }
    out_text = json.dumps(output, indent=2) + "\n"
    assert not re.search(r"/(?:Users|private|tmp|var)/", out_text)
    (HERE / "p0c-validation.json").write_text(out_text)
    (HERE / "track0-validation.json").write_text(out_text)
    print(json.dumps({k: v for k, v in output.items() if k != "successors"}, indent=2))


if __name__ == "__main__":
    main()
