"""Build a scratch core v73 OUTSIDE the repository and prototype the filing-status projection change there.

    python3 scratch_v73.py <scratch-dir>

Copies the committed tree (``git archive HEAD``) into ``<scratch-dir>/repo``, writes one ``input-question.v1``
citizen per fact in groups.py (81 including filing status, each carrying its group's sentence), constructs core
v73 / registry v71 / release v71 with ``tools/package_successor.py`` (the scratch copy), installs them in the
scratch tree, and patches the scratch ``presentation_projection.py`` and ``live.py`` so a root that is a package
input binding symbol (``filing_status``) resolves to its bound fact type before the question lookup.
Nothing in the real repository is touched.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(HERE))
from groups import GROUPS  # noqa: E402


def main():
    scratch = Path(sys.argv[1]).resolve()
    repo = scratch / "repo"
    assert not repo.exists(), "scratch repo already exists"
    repo.mkdir(parents=True)
    arch = subprocess.run(["git", "-C", str(REPO), "archive", "HEAD"], check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(repo)], input=arch, check=True)
    content = repo / "packages/content/tax/2025"
    facts = {}
    for gid, text, members, kind in GROUPS:
        for fact, pol in members:
            facts[fact] = text
    members, entry = [], []
    for fact, text in facts.items():
        slug = fact.replace(".", "-")
        cid = f"tax.us.2025.input-question.{slug}"
        (content / f"input-question.{slug}.v1.json").write_text(json.dumps({
            "fact_type": {"id": f"tax.us.2025.{fact}", "version": "v1"}, "id": cid, "question": text,
            "schema": "input-question.v1", "version": "v1"}, indent=2) + "\n", encoding="utf-8")
        members.append({"op": "add", "new": {"id": cid, "role": "input-question", "schema": "input-question.v1", "version": "v1"}})
        entry.append({"op": "add", "value": {"id": cid, "version": "v1"}})
    changes = {"package_version": "v73", "release_version": "v71", "schema": "artifact-package.v39",
               "members": members, "entrypoints": entry, "registry_sort": "id_version",
               "registry_new_key_order": ["checksum", "id", "version"]}
    (scratch / "v72-to-v73.json").write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    out = scratch / "candidate"
    rel = repo / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
    r = subprocess.run([sys.executable, "tools/package_successor.py",
                        "--package", str(content / "package.core-calculations.v72.json"),
                        "--registry", str(content / "published-packages.v70.json"),
                        "--release", str(rel / "demo.release.sli-worksheet-integration.2025.v70.json"),
                        "--corpus", str(content), "--changes", str(scratch / "v72-to-v73.json"), "--output", str(out)],
                       cwd=repo, capture_output=True, text=True, env={**__import__('os').environ, 'PYTHONPATH': str(repo)})
    print(r.stdout, r.stderr)
    r.check_returncode()
    (content / "package.core-calculations.v73.json").write_bytes((out / "package.json").read_bytes())
    (content / "published-packages.v71.json").write_bytes((out / "registry.json").read_bytes())
    (rel / "demo.release.sli-worksheet-integration.2025.v71.json").write_bytes((out / "release.json").read_bytes())

    # prototype of the smallest filing-status change (scratch copy only)
    pp = repo / "packages/derivation/presentation_projection.py"
    s = pp.read_text(encoding="utf-8")
    s = s.replace("""    by_symbol: Mapping[str, Sequence[Mapping[str, Any]]],
) -> list[dict[str, Any]]:
    \"\"\"The declared question for every cause""", """    by_symbol: Mapping[str, Sequence[Mapping[str, Any]]],
    symbol_fact_types: Mapping[str, str] | None = None,
) -> list[dict[str, Any]]:
    \"\"\"The declared question for every cause""", 1)
    s = s.replace("""                if current.get("code") == "DEPENDENCY_ABSENT" and str(symbol) in input_questions:
                    facts.add(str(symbol))
                    continue""", """                bound = (symbol_fact_types or {}).get(str(symbol), str(symbol))
                if current.get("code") == "DEPENDENCY_ABSENT" and bound in input_questions:
                    facts.add(bound)
                    continue""", 1)
    s = s.replace("""                row, resolved_members=resolved_members, by_symbol=by_symbol,
            )""", """                row, resolved_members=resolved_members, by_symbol=by_symbol,
                symbol_fact_types=symbol_fact_types,
            )""", 1)
    s = s.replace("""    workspace_revision: int | None = None,
) -> dict[str, Any]:
    \"\"\"Build the presentation-model.v1 payload""", """    workspace_revision: int | None = None,
    symbol_fact_types: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    \"\"\"Build the presentation-model.v1 payload""", 1)
    pp.write_text(s, encoding="utf-8")
    lv = repo / "packages/derivation/live.py"
    t = lv.read_text(encoding="utf-8")
    t = t.replace("""            workspace_revision=workspace_revision,
        )
    except PresentationModelError:""", """            workspace_revision=workspace_revision,
            symbol_fact_types={b["symbol"]: b["fact_type"]["id"] for b in resolved.package.get("input_bindings", [])
                               if isinstance(b.get("symbol"), str) and isinstance(b.get("fact_type"), dict)},
        )
    except PresentationModelError:""", 1)
    lv.write_text(t, encoding="utf-8")
    print("scratch ready:", repo)


if __name__ == "__main__":
    main()
