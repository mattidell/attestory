# Track 10 experimental saved-account contract

## Purpose and boundary

This internal JSON experiment asks whether actual neutral results about a
synthetic student-loan account can be reopened with their support after the
live calculation and workspace have ended. It is not a published citizen
schema, production recorder, tax determination, or adoption of mixed-period
treatment.

## Record shape

`tools/sli_saved_account_evidence.py` writes format
`sli-saved-account-evidence.v1`. The document contains:

- run ID and explicit package ID/version provenance;
- an explicit whole-run scope and, where requested, a selected set of actual
  producer pins/publication IDs; `required_support_publication_ids` records
  selected producer dependencies and `other_run_publication_ids` is a neutral
  complement label, not a claim of independence;
- each actual coordinator publication, including its actual finding value,
  identity rendering, and complete recorded pins;
- the coordinator's recorded dispositions, including unresolved statuses and
  their exact pins;
- a separate `recorded_blocked_dependencies` collection containing the
  coordinator's original blocked disposition rows, including exact artifact,
  symbol/subject when present, code, missing references, and recorded pins;
- the current source findings reached by publication and disposition `input`
  pins, with their
  actual values, evidence IDs, structured fact keys obtained from the reopened
  projection, and the corresponding evidence records;
- a separate `context_only` list for records that are retained to explain an
  account but are not evaluated dependencies;
- optional `experiment_metadata` for application-capability scope, stored apart
  from findings and dispositions (for example, mixed-period treatment marked
  unadopted);
- `unresolved_support` and a derived `complete` flag;
- a current/displaced finding-lineage snapshot from the fresh authoritative
  projection, with its recorded displacement reasons and actual retraction
  acts; this is a captured snapshot, not a currency state recomputed by the
  saver.

No fact identity is reconstructed from a rendered or suffixed symbol. No
conclusion, source dependency, category, classification, or cause is created
by the serializer. Producer type metadata is reported only where recorded by
the publication or coordinator; it is not inferred from a symbol. Unavailable
evaluation metadata remains unavailable.

## Validation and recovery

Capture is given publications and dispositions returned by one successful
`live_coordinate_run`, plus maps built from a fresh projection of reopened
authoritative acts. Every input pin resolves to a current source finding, a
same-run publication, or an explicit unresolved target. Source findings must
have structured fact keys; all evidence IDs must resolve. Unresolved targets are recorded and make the
document incomplete. Reopening checks the format, provenance, unique finding
IDs, structured identities, support evidence, disposition/run consistency,
and consistency between `complete` and unresolved support. Reopen uses only
the bytes in the saved file.

`evaluated_support` is exactly the current source support reached from actual
publication and disposition input pins. `recorded_blocked_dependencies`
preserves coordinator refusal rows and does not synthesize missing input pins.
Those rows do not make `complete` false: `complete` concerns only recorded
input-pin/source/evidence closure, even when a required source is known but
invalid for a consumer. `context_only` is not evidence that a rule consumed a
record. Historical findings appear only in the separate lineage snapshot and
cannot appear as current evaluated support after correction or retraction.

## Known limits

The carrier is an experiment scoped to the current package/run. It does not
validate the tax meaning of a neutral observation, persist an entire workspace,
or establish that a filing capability has been adopted. Package version pins
are provenance references; this file does not embed or revalidate package
citizens. General application adoption and mixed-period tax treatment remain
open.
