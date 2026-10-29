# Package successor candidates

The tool builds a package, registry and release candidate from a verified predecessor and explicit changes. It validates the predecessor and candidate with the existing package and schema validators. Replacement checks establish a same-identity, newer, structurally compatible member; they do not establish preservation of tax meaning.

Run from the repository root with an existing, trusted output parent and a new output directory name:

```sh
python3 -m tools.package_successor \
  --package packages/content/tax/2025/package.core-calculations.v57.json \
  --registry packages/content/tax/2025/published-packages.v55.json \
  --release packages/sample_data/student_loan_worksheet_integration/publication_surface/releases/demo.release.sli-worksheet-integration.2025.v55.json \
  --corpus packages/content/tax/2025 \
  --changes tests/fixtures/package_successor/v57-to-v58.json \
  --output temp/demo-candidate
```

The tool is proven through core v60 across three frozen chains. For the second reconstruction use `package.core-calculations.v58.json`, `published-packages.v56.json`, the corresponding release v56, and `tests/fixtures/package_successor/v58-to-v59.json`. For the third use `package.core-calculations.v59.json`, `published-packages.v57.json`, release v57, and `tests/fixtures/package_successor/v59-to-v60.json`, producing core v60, registry v58 and release v58. Select a fresh destination for each. Those frozen change sets are inputs; the v58/v59/v60 published files are comparison targets, not inputs. The result directory contains `package.json`, `registry.json` and `release.json`. The JSON report names their package and release identities, the canonical package checksum, raw registry and release byte hashes, and inherited pin/body schema inconsistencies.

A minimal change set for an unchanged successor is:

```json
{"package_version": "v99", "release_version": "v99"}
```

Versions must increase and the target package identity must be absent from the predecessor registry. Optional `schema` selects an already-published package schema. `members` is a list of `add`, `remove`, or `replace` edits with exact `new` and/or `old` pins; an add may specify `before` as an `[id, version]` member anchor, a replacement may use `before` or `at_end`, and either may supply `registry_before`. Different identities require remove/add. `entrypoints`, `bindings`, and `admitted_schemas` accept explicit add/remove edits with `value`, or replace edits with `old` and `new`; omitted lists preserve the predecessor. `binding_sort: "symbol"` sorts bindings. `registry_sort: "id_version"` sorts registry entries; `registry_tail` lists exact citizen identities to keep at the end, and `registry_new_key_order` chooses `id`, `version`, and `checksum` ordering. `release_key_order` controls release object key order. See the three frozen examples for complete syntax.

The inherited mismatch in the historical chain is reported, not silently corrected. It is retained only when the exact predecessor pin remains and its body matches the predecessor registry checksum. Every added or replacement member must match its body's schema. Conflicting corpus bodies for the same id/version are refused.

The existing registry loaders validate every entry in both the predecessor and candidate registries, including entries unused by the selected package. Their path-based interface requires a private, automatically deleted temporary snapshot for each registry. A correct release hash alone does not validate registry entries. Optional ordering and schema fields must use the documented types and supported values; an explicit null, false, or empty string is refused.

The destination must be absent, outside the repository's `packages` tree and outside the corpus and input paths. Its existing parent must have no symlink components; traversal and existing destination symlinks are refused. All inputs are read and validated before output is written, and input bytes are rechecked before installation. Three files are written to a private sibling directory and installed together with the operating system's exclusive directory rename: macOS `renameatx_np(RENAME_EXCL)` or Linux `renameat2(RENAME_NOREPLACE)`. Other platforms or filesystems without that primitive fail closed. The output parent must be a trusted directory on a local filesystem that implements those calls; this is not a defense against an adversary who can rename or replace the parent or staging directory concurrently, nor a guarantee of persistence through power loss. Failed installation removes only the tool's staging files and never overwrites a competing destination.

These are candidates, not a publication or adoption. ADR-0082 requires a successor's own package-scoped companion declaration and live release evidence as separate duties. The tool creates neither; the three files alone are not publication-complete.
