# Explanation sharing: measurements and reader boundaries

The shared explanation graph records each reachable finding or provenance reference once and preserves every role-bearing pin as an edge. New saved presentations retain that graph alongside their existing section and citation fields. Valid historical `presentation-model.v1` files remain readable; their flattened citation sites cannot reconstruct intermediate findings. The named `project_presentation_v1` adapter validates a v2 model before producing its historical view for frozen-golden comparisons. `explain_legacy`, `walk_npe_legacy`, and the CLI's `--legacy-tree` explicitly provide expanded compatibility views.

## Reproduce the baseline and comparison

From the repository root:

```sh
python3 docs/phases/engineering-health/milestones/explanation-sharing-evidence/census.py > /tmp/census.tsv
python3 docs/phases/engineering-health/milestones/explanation-sharing-evidence/census.py --self-test
python3 docs/phases/engineering-health/milestones/explanation-sharing-evidence/census.py --v58
python3 -m docs.phases.engineering-health.milestones.explanation-sharing-evidence.negative_control
```

The first command selects tracked JSON with the `presentation-model.v1` discriminator, so newer successor examples do not change the baseline. It reproduces `census.tsv`, which inventories all 36 committed v1 presentation goldens and nine harness examples, and every saved section root. Those files store zero `ExplanationNode` trees; a zero count means no such tree was stored, not that support was absent. The table records file bytes, root pins and flattened citation sites, with distinct `(id, version)` counts. Root rows report immediate saved pins and sites, not full lineage. File citation counts cover section sites; specialized blocks and citation groups are separate. Total golden bytes were 7,728,275; 15,219 section citation occurrences occupied 1,968,050 bytes in compact JSON. Existing line-local citation sites are retained in v2.

The historical 9,885 tree nodes over 218 findings observation lacks a recorded scenario and counting procedure. It cannot be reproduced exactly or treated as a comparison baseline. The identified v58 parent and grandparent scenarios below use the real coordinator, validate the successor and compare its named v1 projection against the unchanged golden. Compact byte counts use sorted-key UTF-8 JSON without whitespace. The single-root graph counts include producer and provenance pins, so their node and edge counts are not directly comparable with the legacy tree's distinct finding-ID count.

| Core v58 line 27a | Expanded tree nodes | Tree bytes | Shared graph nodes | Graph edges | Graph bytes | Entire v1 file bytes | Entire v2 file bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Parent wins | 8,608 | 1,594,462 | 314 | 526 | 153,718 | 509,132 | 1,062,991 |
| Grandparent loses | 8,684 | 1,607,412 | 318 | 532 | 155,272 | 509,995 | 1,060,091 |

The all-section graph for those runs contains 647 nodes / 1,134 edges / 339,845 compact bytes and 645 / 1,124 / 337,550 respectively. These are separate from the single-line comparison. The complete v2 files are larger because v1 did not save the complete graph and v2 retains the existing line-local citation sites. This is a storage measurement, not a runtime benchmark.

The negative control loads the actual walker from ratified base `bb9e05e98a390ce12631c5d8fd18025af5300cdd`. With memoization enabled, a five-layer reused graph still serializes 31 tree occurrences / 4,139 bytes, while the successor has 5 nodes / 8 edges / 1,446 bytes. At ten layers the old serialization has 1,023 occurrences / 136,571 bytes and the successor has 10 nodes / 18 edges / 2,946 bytes. The graph is built directly; the test does not materialize an expanded tree before graph serialization.

## Meaning and consumers

Each root carries its own role and authorization context. Canonical nodes distinguish derived findings, inputs and bare references, and preserve value, symbol, version and producer. Edges retain complete recorded pin metadata and repeated uses. Graphs are scoped to a run/snapshot; validation checks schema shape, root-to-finding identity and pins, run context, dangling references and cycles. Unknown pins remain explicit references. The saved projection refuses ambiguous published predecessors. Its disposition table records the actual blocked or inapplicable rows and links justified derived predecessors without synthesizing run records.

`consumer-inventory.txt` preserves the reproducible source scans that identified direct walker and NPE callers, CLI reports, projection, saved-model readers and browser routes. The CLI writes one graph across its roots and renders reuse references. NPE retains run-scoped ledger and publication selection, with a v4 graph and explicit v3 adapter. The saved browser opens nodes lazily and reuse controls focus the already-rendered canonical occurrence. The v1 loader does not invent a graph. Schema and runtime checks are complementary: the published shapes constrain structure, while runtime checks resolve references and verify context.

The old SLI durable-reader tests characterized what its flattened saved representation omitted. Their v1 assertions remain against the validated legacy projection. The successor graph intentionally records actual intermediate findings and blocked disposition evidence; rejected or missing identifiers remain failure evidence and are not invented as successful findings. Existing v1 golden bytes and previously published schema bytes remain unchanged.

The evidence is bounded: the v58 graph relation test checks every reachable recorded pin, producer and value on that live path; a saved-file/browser test follows an actual numeric source and reuse link, and malformed references are refused. NPE tests cover blocked, violation and interrupted selection, including a real blocked coordinator record. The layered-diamond test checks graph and leaf-walk growth by node and edge counts rather than timing. This does not establish runtime improvement for unrelated presentation fields.

## Verification status

The provenance-boundary repair addresses two accepted mutations observed before the fix: redirecting a parameter pin to a derived node with the same ID, and adding a fabricated symbol and value to a bare reference. The pre-fix graph validator and actual saved loader accepted both; published and blocked browser traversal also accepted each mutation. Focused regressions now exercise those same boundaries and reject them, while preserving legitimate unknown references and same-ID nodes of different kinds. These checks do not alter the published schemas.

After that repair, `pytest -x` completed the full selection with 3,646 passed and 20 skipped in 631.63 seconds using the configured 10 workers. The focused graph and saved-browser selection passed 20 tests, and `python3 -m mypy` found no issues in 420 source files. Green `verify` on the final curated PR head remains required.

An earlier complete local run reported 3,573 passed, 20 skipped and two failures: both were 60-second headless Chromium subprocess timeouts in line-21 page tests. The exact two cases subsequently passed together in isolation in 80.86 seconds total; one uses a newly generated v2 model and the other a committed v1 golden. Their timeout cause was not established.
