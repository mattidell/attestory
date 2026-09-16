"""P1 Path L fixture — Student Loan Interest Bounded Method Transfer.

The gate's first executable step, chartered at
``docs/phases/tax-concept-derivation/milestones/
student-loan-interest-bounded-method-transfer-evidence/
p1-bounded-executable-comparison.md`` § 2.

**What this establishes.** That a *complete disposable artifact set* — a new
fact-type bundle and a new rule — can be sealed into a disposable
package/registry/release, resolved through the real coordinator, and actually
**executed**, with the seven-step chain observed rather than assumed.

**What it does not establish.** Nothing about the selected product route, and
nothing about any artifact having a production route. Every result here is a
**live run through a disposable package**, never current production behavior.
Nothing is adopted into the real ``package.core-calculations``: the member,
registry and release bytes live only in a per-test temporary directory.

All identities are synthetic ``demo.*``.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.package_validation import package_instance_checksum
from packages.derivation.production_resolver import (
    PublicationSurface,
    resolve_production_package,
)
from tools.generate_ssa_no_activity_content import _bytes, _citizen_checksum

from tests.test_f1098e_student_loan_interest_agi_track6 import (
    SCOPE,
    USER,
    Statement,
    _f1098e_acts,
    _renumber,
)

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
TRACK6 = ROOT / "packages" / "sample_data" / "f1098e_student_loan_interest_track6"
REGISTRY_FILE = "published-packages.v28.json"
RELEASE_FILE = "demo.release.2025.v26.json"
PACKAGE_FILE = "package.core-calculations.v33.json"

MECH_INPUT_ID = "demo.p1.mech.categorical-input"
BUNDLE_ID = "demo.p1.vocabulary"
MECH_RULE_ID = "demo.p1.mech.rule.branching-value"
MECH_SYMBOL = "demo.p1.mech.branching-value"
MECH_DOWNSTREAM_RULE_ID = "demo.p1.mech.rule.consumer"
MECH_DOWNSTREAM_SYMBOL = "demo.p1.mech.consumer-value"
MECH_FINDING_ID = "demo.p1.mech.finding.input"
MECH_ADVERSE_VALUE = 0
MECH_OTHER_VALUE = 7
BOX1 = 1200.0

# MECHANISM-ONLY vocabulary. These names carry NO tax meaning. This bundle exists
# to prove the disposable-graph mechanism, not to model the selected ordinary
# proposition -- its identity is tax-year only, which cannot carry a
# student/academic-period proposition (P0 § 2.1), so it deliberately makes no
# such claim. The candidate's own vocabulary is defined further below.
BUNDLE: dict[str, Any] = {
    "schema": "bundle.v2",
    "id": BUNDLE_ID,
    "version": "v1",
    "label": "Disposable P1 vocabulary: credential-program enrollment",
    "fact_types": [
        {
            "schema": "fact-type.v2",
            "id": MECH_INPUT_ID,
            "version": "v1",
            "title": "Mechanism-only categorical input (no tax meaning)",
            "nature": "determinable",
            "identity_keys": [
                {"name": "tax-year", "kind": "literal", "values": ["2025"]}
            ],
            "value_schema": {"enum": ["token-a", "token-b"]},
            "supersession": {"policy": "free"},
        }
    ],
}

# MECHANISM ONLY -- not the frozen tax intermediate. This rule reads one
# categorical input and publishes one of two arbitrary numeric tokens. It does
# not read the Form 1098-E box-1 amount, does not bound statement cardinality,
# does not identify an academic period, and does not read X1-X3. It therefore
# demonstrates exactly one thing: a current categorical input can control a
# derived numeric publication, which a second rule can consume, on a disposable
# resolved graph.
RULE: dict[str, Any] = {
    "schema": "rule-artifact.v2",
    "id": MECH_RULE_ID,
    "version": "v1",
    "scope": {
        "tax_year": 2025,
        "jurisdiction": "US-federal",
        "family": "individual-income-tax",
    },
    "role": "computation",
    "requires": [MECH_INPUT_ID],
    "pins": [
        {"role": "input", "id": MECH_INPUT_ID, "version": "v1", "origin": "assertion"}
    ],
    "when": True,
    "value": {
        "op": "choose",
        "when": {
            "op": "categorical_compare",
            "cmp": "eq",
            "left": {"op": "ref", "name": MECH_INPUT_ID},
            "right": {
                "op": "category_literal",
                "fact_type": {"id": MECH_INPUT_ID, "version": "v1"},
                "value": "token-a",
            },
        },
        "then": MECH_ADVERSE_VALUE,
        "else": MECH_OTHER_VALUE,
    },
    "publishes": MECH_SYMBOL,
    "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [MECH_INPUT_ID]},
    "notes": (
        "MECHANISM ONLY. A categorical input controlling a derived numeric "
        "publication. The values are arbitrary tokens and are NOT supported tax "
        "determinations. Synthetic; never adopted."
    ),
}

# A downstream consumer, so the mechanism chain reaches a *dependent* result
# rather than stopping at the first publication. Reads the upstream symbol.
DOWNSTREAM_RULE: dict[str, Any] = {
    "schema": "rule-artifact.v2",
    "id": MECH_DOWNSTREAM_RULE_ID,
    "version": "v1",
    "scope": {
        "tax_year": 2025,
        "jurisdiction": "US-federal",
        "family": "individual-income-tax",
    },
    "role": "computation",
    "requires": [MECH_SYMBOL],
    # `origin: assertion` is the corpus convention for a pinned upstream symbol
    # even when it is derived (cf. rule.schedule1-line26 pinning line21). The
    # field is a declaration shape, not a provenance claim.
    "pins": [{"role": "input", "id": MECH_SYMBOL, "version": "v1", "origin": "assertion"}],
    "when": True,
    "value": {"op": "ref", "name": MECH_SYMBOL},
    "publishes": MECH_DOWNSTREAM_SYMBOL,
    "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [MECH_SYMBOL]},
    "notes": "MECHANISM ONLY. Reads the upstream symbol. Never adopted.",
}


# ---------------------------------------------------------------------------
# Candidate B -- the actual bounded single-statement tax route.
#
# Unlike the mechanism artifacts above, this chain: bounds statement cardinality
# to exactly one; reads the *closure-authorized* Form 1098-E box-1 subtotal
# rather than a fixture constant; carries the ordinary proposition at
# student/academic-period identity; reads X1-X3 on the favorable route; and
# publishes a separate derived consequence a downstream rule consumes.
#
# It does NOT read tax.us.2025.f1098e.no-non-qualified-loan-component -- the
# incumbent compressed witness that already collapses student status into a
# user-supplied legal conclusion. Using it would leave the user asserting the
# conclusion this route claims to replace.
# ---------------------------------------------------------------------------

PERIOD_ENTITY_KIND = "demo.p1.academic-period"
PERIOD_ID = "demo.p1.period.fall-2024"

CAND_BUNDLE_ID = "demo.p1.candidate.vocabulary"
ENROLLMENT_ID = "demo.p1.candidate.credential-program-enrollment"
X1_ID = "demo.p1.candidate.credential-recognized"       # X1, local premise
X2_ID = "demo.p1.candidate.institution-eligible"        # X2, local premise
X3_ID = "demo.p1.candidate.half-time-met"               # X3, local premise
CAND_RULE_ID = "demo.p1.candidate.rule.supported-interest"
CAND_SYMBOL = "demo.p1.candidate.eligible-student-supported-interest"
CAND_DOWN_RULE_ID = "demo.p1.candidate.rule.bounded-line1"
CAND_DOWN_SYMBOL = "demo.p1.candidate.bounded-line1"

SUBTOTAL_SYMBOL = "tax.us.2025.sli-worksheet.line1-total-interest-paid-subtotal"
BOX1_FACT_TYPE = "tax.us.2025.f1098e.box1-student-loan-interest"
F1098E_FAMILY = "tax.us.2025.f1098e.1"
COMPRESSED_WITNESS = "tax.us.2025.f1098e.no-non-qualified-loan-component"
# Pins carry *finding* ids (demo.f1098e.no-non-qualified-loan-component.0), not
# fact-type ids, so a matcher keyed on the fact-type id would silently pass even
# when the witness IS pinned. Match the discriminating substring instead --
# verified against the incumbent, whose worksheet row does trip it.
COMPRESSED_WITNESS_TOKEN = "no-non-qualified-loan-component"

ENROLL_FINDING_ID = "demo.p1.candidate.finding.enrollment"

# The authority chain the adverse inference actually uses. citation.v1's own
# contract is that resolution is "structural/adoption-only and does not claim
# external legal verification" (ADR-0029) -- so a citation pin proves the
# executed rule preserved its declared authority, and nothing about legal
# correctness or which historical edition of the HEA text was incorporated.
CITATIONS: list[dict[str, Any]] = [
    {
        "schema": "citation.v1",
        "id": "demo.p1.candidate.citation.irc-221-d-1-C",
        "version": "v1",
        "authority": {"family": "us-code", "title": "26", "section": "221(d)(1)(C)"},
    },
    {
        "schema": "citation.v1",
        "id": "demo.p1.candidate.citation.irc-221-d-3",
        "version": "v1",
        "authority": {"family": "us-code", "title": "26", "section": "221(d)(3)"},
    },
    {
        "schema": "citation.v1",
        "id": "demo.p1.candidate.citation.irc-25A-b-3-A",
        "version": "v1",
        "authority": {"family": "us-code", "title": "26", "section": "25A(b)(3)(A)"},
    },
    {
        # HEA s484(a)(1) as codified.
        "schema": "citation.v1",
        "id": "demo.p1.candidate.citation.hea-484-a-1",
        "version": "v1",
        "authority": {"family": "us-code", "title": "20", "section": "1091(a)(1)"},
    },
]
CITATION_IDS = [c["id"] for c in CITATIONS]

# ---------------------------------------------------------------------------
# The negative control: the WRONG product input.
#
# The filer supplies the legal conclusion directly. The engine does not reject
# this mechanically -- it drives the arithmetic perfectly well. That is the
# point: it is a responsibility-boundary failure, not a mechanical one.
# ---------------------------------------------------------------------------
NEGCTL_BUNDLE_ID = "demo.p1.negctl.vocabulary"
NEGCTL_CONCLUSION_ID = "demo.p1.negctl.eligible-student-conclusion"
NEGCTL_RULE_ID = "demo.p1.negctl.rule.shortcut"
NEGCTL_SYMBOL = "demo.p1.negctl.supported-interest"
NEGCTL_FINDING_ID = "demo.p1.negctl.finding.conclusion"

NEGCTL_BUNDLE: dict[str, Any] = {
    "schema": "bundle.v2",
    "id": NEGCTL_BUNDLE_ID,
    "version": "v1",
    "label": "Negative control vocabulary: a user-authored legal conclusion",
    "fact_types": [
        {
            "schema": "fact-type.v2",
            "id": NEGCTL_CONCLUSION_ID,
            "version": "v1",
            "title": "THE WRONG INPUT: the filer asserts eligible-student status",
            "nature": "determinable",
            "identity_keys": [
                {"name": "tax-year", "kind": "literal", "values": ["2025"]}
            ],
            "value_schema": {"enum": ["yes", "no"]},
            "supersession": {"policy": "free"},
        }
    ],
}

NEGCTL_RULE: dict[str, Any] = {
    "schema": "rule-artifact.v6",
    "id": NEGCTL_RULE_ID,
    "version": "v1",
    "scope": {
        "tax_year": 2025,
        "jurisdiction": "US-federal",
        "family": "individual-income-tax",
    },
    "role": "computation",
    "requires": [NEGCTL_CONCLUSION_ID, SUBTOTAL_SYMBOL],
    "pins": [
        {
            "role": "input",
            "id": NEGCTL_CONCLUSION_ID,
            "version": "v1",
            "origin": "assertion",
        },
        {"role": "input", "id": SUBTOTAL_SYMBOL, "version": "v1", "origin": "assertion"},
    ],
    "when": True,
    "value": {
        "op": "choose",
        "when": {
            "op": "categorical_compare",
            "cmp": "eq",
            "left": {"op": "ref", "name": NEGCTL_CONCLUSION_ID},
            "right": {
                "op": "category_literal",
                "fact_type": {"id": NEGCTL_CONCLUSION_ID, "version": "v1"},
                "value": "yes",
            },
        },
        "then": {"op": "ref", "name": SUBTOTAL_SYMBOL},
        "else": 0,
    },
    # No citations: there is no inference to license. The filer supplied the
    # conclusion, so the rule appeals to no authority at all.
    "publishes": NEGCTL_SYMBOL,
    "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [NEGCTL_CONCLUSION_ID]},
    "notes": (
        "NEGATIVE CONTROL. Reads a user-authored legal conclusion directly. "
        "Arithmetically fine, product-wise wrong. Never adopted."
    ),
}


def _period_keyed(fact_type: str) -> list[dict[str, Any]]:
    """Student/academic-period identity. Tax year is deliberately NOT a key:
    P0 § 2.1 holds that the tax year and the academic period are different
    objects, and a tax-year-only fact would collapse distinct terms."""
    return [{"name": "period", "kind": "entity", "entity_kind": PERIOD_ENTITY_KIND}]


def _cat(fact_id: str, title: str, values: list[str]) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": title,
        "nature": "determinable",
        "identity_keys": _period_keyed(fact_id),
        "value_schema": {"enum": values},
        "supersession": {"policy": "free"},
    }


CAND_BUNDLE: dict[str, Any] = {
    "schema": "bundle.v2",
    "id": CAND_BUNDLE_ID,
    "version": "v1",
    "label": "Disposable Candidate B vocabulary",
    "fact_types": [
        _cat(
            ENROLLMENT_ID,
            "Was the student enrolled in or accepted into a credential program "
            "during this academic period?",
            ["credential-program", "individual-classes-only"],
        ),
        _cat(X1_ID, "X1 local premise: credential recognised", ["yes", "no"]),
        _cat(X2_ID, "X2 local premise: institution eligible", ["yes", "no"]),
        _cat(X3_ID, "X3 local premise: half-time threshold met", ["yes", "no"]),
    ],
}


def _is(fact_id: str, value: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare",
        "cmp": "eq",
        "left": {"op": "ref", "name": fact_id},
        "right": {
            "op": "category_literal",
            "fact_type": {"id": fact_id, "version": "v1"},
            "value": value,
        },
    }


CAND_RULE: dict[str, Any] = {
    "schema": "rule-artifact.v6",
    "id": CAND_RULE_ID,
    "version": "v1",
    "scope": {
        "tax_year": 2025,
        "jurisdiction": "US-federal",
        "family": "individual-income-tax",
    },
    "role": "computation",
    # X1-X3 are deliberately NOT unconditional requires: an unconditional
    # `requires` blocks the rule on *every* branch, which would defeat the
    # adverse short-circuit P0 § 2.4 depends on. They are gathered by a
    # conditional_dependency_set on the favorable branch only.
    "requires": [ENROLLMENT_ID, SUBTOTAL_SYMBOL],
    "pins": [
        {"role": "input", "id": ENROLLMENT_ID, "version": "v1", "origin": "assertion"},
        {"role": "input", "id": X1_ID, "version": "v1", "origin": "assertion"},
        {"role": "input", "id": X2_ID, "version": "v1", "origin": "assertion"},
        {"role": "input", "id": X3_ID, "version": "v1", "origin": "assertion"},
        {
            "role": "input",
            "id": SUBTOTAL_SYMBOL,
            "version": "v1",
            "origin": "assertion",
        },
    ],
    # The exactly-one-current-statement bound, enforced by the rule itself.
    "when": {
        "op": "all",
        "args": [
            {"op": "require_closed", "source_set": F1098E_FAMILY},
            {
                "op": "compare",
                "cmp": "eq",
                "left": {
                    "op": "count",
                    "name": BOX1_FACT_TYPE,
                    "source_set": F1098E_FAMILY,
                },
                "right": 1,
            },
            # Gather X1-X3 only when the favorable branch will need them.
            {
                "op": "conditional_dependency_set",
                "condition": _is(ENROLLMENT_ID, "credential-program"),
                "members": [
                    {"op": "ref", "name": X1_ID},
                    {"op": "ref", "name": X2_ID},
                    {"op": "ref", "name": X3_ID},
                ],
            },
        ],
    },
    "value": {
        "op": "choose",
        # Adverse short-circuits: a failed conjunct fails the whole test, so no
        # X1-X3 support is needed (P0 § 2.4).
        "when": _is(ENROLLMENT_ID, "individual-classes-only"),
        "then": 0,
        "else": {
            "op": "choose",
            "when": {
                "op": "all",
                "args": [_is(X1_ID, "yes"), _is(X2_ID, "yes"), _is(X3_ID, "yes")],
            },
            # The reported amount, via the family's closure-authorized subtotal.
            # ADR-0016 bars collecting the mapped family here (this rule
            # publishes a different symbol), so the subtotal is the corpus-correct
            # read of the document amount.
            "then": {"op": "ref", "name": SUBTOTAL_SYMBOL},
            # A *present but negative* premise is adverse evidence, not a missing
            # dependency. The conjunct is established false, so the supported
            # amount as to s221(d)(1)(C) is determinately zero. Absence is a
            # different state and is handled by the conditional_dependency_set
            # guard in `when`, which blocks DEPENDENCY_ABSENT.
            "else": 0,
        },
    },
    "citations": [{"id": cid, "version": "v1"} for cid in CITATION_IDS],
    "publishes": CAND_SYMBOL,
    "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [ENROLLMENT_ID]},
    "notes": (
        "Candidate B. Statement-scoped supported interest as to s221(d)(1)(C) "
        "only, for the bounded single-loan single-period case. NOT a general "
        "eligible-student determination. Does not read the incumbent compressed "
        "witness. Synthetic; never adopted."
    ),
}

CAND_DOWN_RULE: dict[str, Any] = {
    "schema": "rule-artifact.v6",
    "id": CAND_DOWN_RULE_ID,
    "version": "v1",
    "scope": {
        "tax_year": 2025,
        "jurisdiction": "US-federal",
        "family": "individual-income-tax",
    },
    "role": "computation",
    "requires": [CAND_SYMBOL],
    "pins": [
        {"role": "input", "id": CAND_SYMBOL, "version": "v1", "origin": "assertion"}
    ],
    "when": True,
    "value": {"op": "ref", "name": CAND_SYMBOL},
    "publishes": CAND_DOWN_SYMBOL,
    "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [CAND_SYMBOL]},
    "notes": (
        "Candidate B downstream: a bounded line-1 analogue reading the derived "
        "consequence by symbol, never the ordinary answer. Never adopted."
    ),
}


class DisposableSurface:
    """A private copy of the real v33 chain carrying two *new* members.

    Never touches the repo tree. Re-seals the package instance checksum, the
    registry citizen and package entries, the release digest, and the adoption
    checksums, so the new members are admitted through the same
    resolver-authenticity gate the unmodified chain passes.
    """

    def __init__(self, root: Path) -> None:
        self.members = root / "members"
        self.releases = root / "releases"
        self.members.mkdir(parents=True)
        self.releases.mkdir(parents=True)
        for source in CONTENT.glob("*.json"):
            shutil.copyfile(source, self.members / source.name)
        shutil.copyfile(
            TRACK6 / "publication_surface" / "releases" / RELEASE_FILE,
            self.releases / RELEASE_FILE,
        )
        self.adoption = json.loads(
            (TRACK6 / "adoptions" / "adopt-core-v33-current.json").read_text("utf-8")
        )
        self._seal()
        self.surface = PublicationSurface(
            self.releases, self.members / REGISTRY_FILE, self.members
        )

    def _seal(self) -> None:
        (self.members / f"{BUNDLE_ID}.json").write_bytes(_bytes(BUNDLE))
        (self.members / f"{MECH_RULE_ID}.json").write_bytes(_bytes(RULE))
        (self.members / f"{MECH_DOWNSTREAM_RULE_ID}.json").write_bytes(_bytes(DOWNSTREAM_RULE))
        (self.members / f"{CAND_BUNDLE_ID}.json").write_bytes(_bytes(CAND_BUNDLE))
        (self.members / f"{CAND_RULE_ID}.json").write_bytes(_bytes(CAND_RULE))
        (self.members / f"{CAND_DOWN_RULE_ID}.json").write_bytes(_bytes(CAND_DOWN_RULE))
        for citation in CITATIONS:
            (self.members / f"{citation['id']}.json").write_bytes(_bytes(citation))
        (self.members / f"{NEGCTL_BUNDLE_ID}.json").write_bytes(_bytes(NEGCTL_BUNDLE))
        (self.members / f"{NEGCTL_RULE_ID}.json").write_bytes(_bytes(NEGCTL_RULE))

        package = json.loads((self.members / PACKAGE_FILE).read_text("utf-8"))
        package["members"].append(
            {
                "id": BUNDLE_ID,
                "role": "fact-type-bundle",
                "schema": "bundle.v2",
                "version": "v1",
            }
        )
        package["members"].append(
            {
                "id": MECH_RULE_ID,
                "role": "computation",
                "schema": "rule-artifact.v2",
                "version": "v1",
            }
        )
        # MEMBER_UNREACHABLE otherwise: a member must be reachable from package
        # entrypoints or form fields.
        package["members"].append(
            {
                "id": MECH_DOWNSTREAM_RULE_ID,
                "role": "computation",
                "schema": "rule-artifact.v2",
                "version": "v1",
            }
        )
        package["entrypoints"].append({"id": BUNDLE_ID, "version": "v1"})
        package["entrypoints"].append({"id": MECH_RULE_ID, "version": "v1"})
        package["entrypoints"].append({"id": MECH_DOWNSTREAM_RULE_ID, "version": "v1"})
        for member_id, role, schema in (
            [(CAND_BUNDLE_ID, "fact-type-bundle", "bundle.v2")]
            + [(cid, "citation", "citation.v1") for cid in CITATION_IDS]
            + [
                (CAND_RULE_ID, "computation", "rule-artifact.v6"),
                (CAND_DOWN_RULE_ID, "computation", "rule-artifact.v6"),
                (NEGCTL_BUNDLE_ID, "fact-type-bundle", "bundle.v2"),
                (NEGCTL_RULE_ID, "computation", "rule-artifact.v6"),
            ]
        ):
            package["members"].append(
                {"id": member_id, "role": role, "schema": schema, "version": "v1"}
            )
            package["entrypoints"].append({"id": member_id, "version": "v1"})
        package["package_checksum"] = package_instance_checksum(package)
        (self.members / PACKAGE_FILE).write_bytes(_bytes(package))

        registry = json.loads((self.members / REGISTRY_FILE).read_text("utf-8"))
        registry["citizens"].append(
            {"id": BUNDLE_ID, "version": "v1", "checksum": _citizen_checksum(BUNDLE)}
        )
        registry["citizens"].append(
            {"id": MECH_RULE_ID, "version": "v1", "checksum": _citizen_checksum(RULE)}
        )
        registry["citizens"].append(
            {
                "id": MECH_DOWNSTREAM_RULE_ID,
                "version": "v1",
                "checksum": _citizen_checksum(DOWNSTREAM_RULE),
            }
        )
        for body in [
            CAND_BUNDLE,
            CAND_RULE,
            CAND_DOWN_RULE,
            NEGCTL_BUNDLE,
            NEGCTL_RULE,
        ] + CITATIONS:
            registry["citizens"].append(
                {
                    "id": body["id"],
                    "version": "v1",
                    "checksum": _citizen_checksum(body),
                }
            )
        for entry in registry["packages"]:
            if (
                entry["id"] == package["id"]
                and entry["version"] == package["version"]
            ):
                entry["checksum"] = package["package_checksum"]
        registry_bytes = _bytes(registry)
        (self.members / REGISTRY_FILE).write_bytes(registry_bytes)

        # Patch the existing release body. `build_release` hardcodes
        # demo.release.2025 v23 and would not match this v26 fixture.
        release = json.loads((self.releases / RELEASE_FILE).read_text("utf-8"))
        release["package_registry_sha256"] = hashlib.sha256(registry_bytes).hexdigest()
        release_bytes = _bytes(release)
        (self.releases / RELEASE_FILE).write_bytes(release_bytes)

        payload = cast(dict[str, Any], self.adoption["payload"])
        payload["package"]["checksum"] = package["package_checksum"]
        payload["release"]["checksum"] = hashlib.sha256(release_bytes).hexdigest()


def _attested(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "attested",
        "evidence_ids": [],
    }


def _acts(subject: DisposableSurface, ordinary: str | None) -> list[dict[str, object]]:
    """One synthetic statement, the incumbent inputs, and the ordinary fact."""
    acts = _f1098e_acts(
        statements=[Statement(lender="demo.lender.a", stmt="demo.stmt.a", box1=1200.0)],
        close=True,
        wages=50000,
    )
    acts.pop()  # drop the track-6 adoption; this run uses the sealed one
    # Package membership admits the bundle to the *resolved graph*; a
    # bundle-adoption act admits its fact types to the *kernel vocabulary*.
    # Both are required -- a finding on an unadopted fact type is rejected at
    # kernel admission before any run begins.
    acts.append(
        {
            "schema": "act.v1",
            "act_id": "demo.p1.act.bundle",
            "actor": USER,
            "at": "2026-09-15T11:00:00Z",
            "committed_against": len(acts),
            "kind": "bundle-adoption",
            "payload": {"bundle": BUNDLE},
        }
    )
    if ordinary is not None:
        acts.append(
            {
                "schema": "act.v1",
                "act_id": "demo.p1.act.ordinary",
                "actor": USER,
                "at": "2026-09-15T12:00:00Z",
                "committed_against": len(acts),
                "kind": "assertion",
                "payload": {
                    "finding": _attested(
                        MECH_FINDING_ID,
                        f"{MECH_INPUT_ID}|tax-year=2025",
                        ordinary,
                    )
                },
            }
        )
    adoption = json.loads(json.dumps(subject.adoption))
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return _renumber(acts)


def _candidate_acts(
    subject: DisposableSurface,
    *,
    enrollment: str | None,
    premises: bool = True,
    box1: float = BOX1,
    x1: str | None = "yes",
    x2: str | None = "yes",
    x3: str | None = "yes",
    statements: int = 1,
    lifecycle: list[dict[str, object]] | None = None,
    legal_conclusion: str | None = None,
) -> list[dict[str, object]]:
    """One synthetic statement plus the candidate's own inputs.

    `premises` False omits X1-X3 entirely; setting one of `x1`/`x2`/`x3` to None
    omits just that one, so *partial* presence is expressible. Their values make a
    *present but negative* premise distinguishable from an absent one. `statements` admits more than one Form 1098-E to exercise the
    cardinality bound.
    """
    members = [
        Statement(lender="demo.lender.a", stmt="demo.stmt.a", box1=box1),
        Statement(lender="demo.lender.b", stmt="demo.stmt.b", box1=300.0),
    ][:statements]
    acts = _f1098e_acts(
        statements=members,
        close=True,
        wages=50000,
    )
    acts.pop()
    acts.append(
        {
            "schema": "act.v1",
            "act_id": "demo.p1.cand.act.entity",
            "actor": USER,
            "at": "2026-09-15T10:00:00Z",
            "committed_against": len(acts),
            "kind": "entity-introduced",
            "payload": {
                "entity": {
                    "schema": "entity.v1",
                    "id": PERIOD_ID,
                    "kind": PERIOD_ENTITY_KIND,
                    "label": "Synthetic academic period",
                }
            },
        }
    )
    acts.append(
        {
            "schema": "act.v1",
            "act_id": "demo.p1.cand.act.bundle",
            "actor": USER,
            "at": "2026-09-15T11:00:00Z",
            "committed_against": len(acts),
            "kind": "bundle-adoption",
            "payload": {"bundle": CAND_BUNDLE},
        }
    )
    facts: list[tuple[str, str, str]] = []
    if enrollment is not None:
        facts.append((ENROLL_FINDING_ID, ENROLLMENT_ID, enrollment))
    if premises:
        # A premise set to None is omitted entirely, so *partial* presence is
        # expressible and distinguishable from a present-but-negative value.
        facts += [
            (f"demo.p1.cand.finding.{name}", type_id, value)
            for name, type_id, value in (
                ("x1", X1_ID, x1),
                ("x2", X2_ID, x2),
                ("x3", X3_ID, x3),
            )
            if value is not None
        ]
    for index, (finding_id, type_id, value) in enumerate(facts):
        acts.append(
            {
                "schema": "act.v1",
                "act_id": f"demo.p1.cand.act.fact.{index}",
                "actor": USER,
                "at": "2026-09-15T12:00:00Z",
                "committed_against": len(acts),
                "kind": "assertion",
                "payload": {
                    "finding": _attested(
                        finding_id, f"{type_id}|period={PERIOD_ID}", value
                    )
                },
            }
        )
    if legal_conclusion is not None:
        acts.append(
            {
                "schema": "act.v1",
                "act_id": "demo.p1.negctl.act.bundle",
                "actor": USER,
                "at": "2026-09-15T11:30:00Z",
                "committed_against": len(acts),
                "kind": "bundle-adoption",
                "payload": {"bundle": NEGCTL_BUNDLE},
            }
        )
        acts.append(
            {
                "schema": "act.v1",
                "act_id": "demo.p1.negctl.act.conclusion",
                "actor": USER,
                "at": "2026-09-15T12:30:00Z",
                "committed_against": len(acts),
                "kind": "assertion",
                "payload": {
                    "finding": _attested(
                        NEGCTL_FINDING_ID,
                        f"{NEGCTL_CONCLUSION_ID}|tax-year=2025",
                        legal_conclusion,
                    )
                },
            }
        )
    for offset, extra in enumerate(lifecycle or ()):
        item = dict(extra)
        item.setdefault("schema", "act.v1")
        item.setdefault("actor", USER)
        item.setdefault("at", "2026-09-15T13:00:00Z")
        item.setdefault("act_id", f"demo.p1.cand.act.life.{offset}")
        item["committed_against"] = len(acts)
        acts.append(item)
    adoption = json.loads(json.dumps(subject.adoption))
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return _renumber(acts)


def _execute(subject: DisposableSurface, acts: list[dict[str, object]]) -> dict[str, Any]:
    with TemporaryDirectory() as workspace:
        result = live_coordinate_run(
            WorkspaceCapability(Path(workspace) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id="demo.p1.run.candidate",
            governance_pins=[],
            surface=subject.surface,
            output_name="out.json",
        )
        assert result.refusal is None, f"live refusal: {result.refusal}"
        assert result.output_path is not None
        report = cast(
            dict[str, Any], json.loads(Path(result.output_path).read_text("utf-8"))
        )
        report["_run_values"] = {
            pub.finding["symbol"]: pub.finding["value"]
            for pub in (result.publications or ())
            if "symbol" in pub.finding
        }
        return report


def _run(subject: DisposableSurface, ordinary: str | None) -> dict[str, Any]:
    acts = _acts(subject, ordinary)
    with TemporaryDirectory() as workspace:
        result = live_coordinate_run(
            WorkspaceCapability(Path(workspace) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope=SCOPE,
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id="demo.p1.run.path-l",
            governance_pins=[],
            surface=subject.surface,
            output_name="out.json",
        )
        assert result.refusal is None, f"live refusal: {result.refusal}"
        assert result.output_path is not None
        report = cast(
            dict[str, Any], json.loads(Path(result.output_path).read_text("utf-8"))
        )
        # `run`-level evidence. The durable disposition row carries no `value`
        # (derivation-record.v9), so branch values are observed here and are
        # never claimed as durable.
        values = {
            pub.finding["symbol"]: pub.finding["value"]
            for pub in (result.publications or ())
            if "symbol" in pub.finding
        }
        report["_run_values"] = values
        return report


def _rule_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        row
        for row in report.get("dispositions", [])
        if row.get("artifact_id") == MECH_RULE_ID or row.get("symbol") == MECH_SYMBOL
    ]


def _rows(report: dict[str, Any], rule_id: str, symbol: str) -> list[dict[str, Any]]:
    return [
        row
        for row in report.get("dispositions", [])
        if row.get("artifact_id") == rule_id or row.get("symbol") == symbol
    ]


class PathLUpstreamChain(unittest.TestCase):
    """Path-L feasibility for a complete disposable artifact set.

    Scope: that new members resolve, are admitted to the kernel vocabulary,
    marshal, are read, are pinned, publish, and reach one dependent consumer.
    This is a **feasibility** result about the disposable-graph mechanism. It is
    **not** evidence for the product design or for method transfer.
    """

    def test_members_resolve_by_exact_id_and_version(self) -> None:
        with TemporaryDirectory() as tmp:
            subject = DisposableSurface(Path(tmp))
            resolved = resolve_production_package(
                [subject.adoption],
                run_scope=SCOPE,
                scope_user=USER,
                workspace_revision=33,
                surface=subject.surface,
            )
            self.assertTrue(
                hasattr(resolved, "resolved_members"), f"resolution refused: {resolved}"
            )
            pairs = {
                (member["id"], member.get("version"))
                for member in resolved.resolved_members  # type: ignore[union-attr]
            }
            for member_id in (BUNDLE_ID, MECH_RULE_ID, MECH_DOWNSTREAM_RULE_ID):
                self.assertIn((member_id, "v1"), pairs)


class NeutralHarness(unittest.TestCase):
    """H0 / H1 / H2 -- the **neutral mechanical harness**, not a tax experiment.

    Arbitrary `demo.p1.mech.*` tokens on one identical disposable graph. This
    class proves only that the engine can execute the *shape*: a current
    categorical input controls a derived numeric publication, which a second
    rule consumes. Its inputs are not the selected ordinary fact and its values
    are not tax consequences.

    It satisfies **no** falsification condition -- not FC1, not L1-L6, not FC9.
    Candidate B's cases C0-C7 carry all of those.
    """

    _tmp: "TemporaryDirectory[str]"
    h0: dict[str, Any]
    h1: dict[str, Any]
    h2: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = TemporaryDirectory()
        subject = DisposableSurface(Path(cls._tmp.name))
        cls.h0 = _run(subject, None)
        cls.h1 = _run(subject, "token-a")
        cls.h2 = _run(subject, "token-b")

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_h0_absent_input_blocks(self) -> None:
        """An absent input blocks. No tax meaning attaches to this."""
        rows = _rows(self.h0, MECH_RULE_ID, MECH_SYMBOL)
        self.assertEqual(len(rows), 1, rows)
        self.assertEqual(rows[0]["disposition"], "blocked")
        self.assertEqual(rows[0]["code"], "DEPENDENCY_ABSENT")
        self.assertIn(MECH_INPUT_ID, rows[0].get("missing", []))
        self.assertNotIn(MECH_SYMBOL, self.h0["_run_values"])

    def test_h1_token_a_yields_the_first_value(self) -> None:
        """`run`-level value evidence: the durable row carries no `value`.

        An arbitrary token, not a tax determination.
        """
        rows = _rows(self.h1, MECH_RULE_ID, MECH_SYMBOL)
        self.assertEqual(len(rows), 1, rows)
        self.assertEqual(rows[0]["disposition"], "published")
        self.assertEqual(rows[0]["artifact_id"], MECH_RULE_ID)
        self.assertIn(MECH_FINDING_ID, {p["id"] for p in rows[0].get("pins", [])})
        self.assertEqual(float(self.h1["_run_values"][MECH_SYMBOL]), float(MECH_ADVERSE_VALUE))

    def test_h2_token_b_yields_the_second_value(self) -> None:
        rows = _rows(self.h2, MECH_RULE_ID, MECH_SYMBOL)
        self.assertEqual(len(rows), 1, rows)
        self.assertEqual(rows[0]["disposition"], "published")
        self.assertIn(MECH_FINDING_ID, {p["id"] for p in rows[0].get("pins", [])})
        self.assertEqual(float(self.h2["_run_values"][MECH_SYMBOL]), float(MECH_OTHER_VALUE))

    def test_h1_versus_h2_single_variable_changes_the_derived_value(self) -> None:
        """The one varied input is the only difference -- mechanically."""
        self.assertNotEqual(
            float(self.h1["_run_values"][MECH_SYMBOL]),
            float(self.h2["_run_values"][MECH_SYMBOL]),
        )

    def test_downstream_consumer_depends_on_the_intermediate(self) -> None:
        """The dependent result follows the intermediate, in both directions."""
        for report, expected in ((self.h1, float(MECH_ADVERSE_VALUE)), (self.h2, float(MECH_OTHER_VALUE))):
            rows = _rows(report, MECH_DOWNSTREAM_RULE_ID, MECH_DOWNSTREAM_SYMBOL)
            self.assertEqual(len(rows), 1, rows)
            self.assertEqual(rows[0]["disposition"], "published")
            self.assertEqual(float(report["_run_values"][MECH_DOWNSTREAM_SYMBOL]), expected)

    def test_downstream_blocks_when_the_intermediate_blocks(self) -> None:
        rows = _rows(self.h0, MECH_DOWNSTREAM_RULE_ID, MECH_DOWNSTREAM_SYMBOL)
        self.assertEqual(len(rows), 1, rows)
        self.assertEqual(rows[0]["disposition"], "blocked")


class CandidateBRoute(unittest.TestCase):
    """The actual bounded single-statement tax route.

    C0 absent enrollment; C1 adverse; C2 favorable with X1-X3 present; C3
    favorable-token with X1-X3 **absent**. X1-X3 are identical in C1 and C2, so
    C1 vs C2 varies only the ordinary answer.
    """

    _tmp: "TemporaryDirectory[str]"
    c0: dict[str, Any]
    c1: dict[str, Any]
    c2: dict[str, Any]
    c3: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = TemporaryDirectory()
        s = DisposableSurface(Path(cls._tmp.name))
        cls.c0 = _execute(s, _candidate_acts(s, enrollment=None))
        cls.c1 = _execute(s, _candidate_acts(s, enrollment="individual-classes-only"))
        cls.c2 = _execute(s, _candidate_acts(s, enrollment="credential-program"))
        cls.c3 = _execute(
            s, _candidate_acts(s, enrollment="credential-program", premises=False)
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def _row(self, report: dict[str, Any], rule_id: str, symbol: str) -> dict[str, Any]:
        rows = _rows(report, rule_id, symbol)
        self.assertEqual(len(rows), 1, rows)
        return rows[0]

    def test_c0_absent_enrollment_blocks(self) -> None:
        row = self._row(self.c0, CAND_RULE_ID, CAND_SYMBOL)
        self.assertEqual(row["disposition"], "blocked")
        self.assertNotIn(CAND_SYMBOL, self.c0["_run_values"])

    def test_c1_adverse_yields_zero_supported_interest(self) -> None:
        row = self._row(self.c1, CAND_RULE_ID, CAND_SYMBOL)
        self.assertEqual(row["disposition"], "published")
        self.assertEqual(float(self.c1["_run_values"][CAND_SYMBOL]), 0.0)

    def test_c2_favorable_yields_the_reported_amount_not_a_constant(self) -> None:
        """The published amount equals the *document's* reported box-1 total,
        reached through the family's closure-authorized subtotal."""
        row = self._row(self.c2, CAND_RULE_ID, CAND_SYMBOL)
        self.assertEqual(row["disposition"], "published")
        self.assertEqual(float(self.c2["_run_values"][CAND_SYMBOL]), BOX1)
        self.assertEqual(float(self.c2["_run_values"][SUBTOTAL_SYMBOL]), BOX1)

    def test_c3_favorable_with_premises_absent_is_unknown_not_adverse(self) -> None:
        """Absence is unknown, and blocks inside the rule's own dependency guard.

        X1-X3 are gathered by the `conditional_dependency_set` in `when`, so a
        favorable answer with any of them **absent** blocks `DEPENDENCY_ABSENT`.
        This case shows the favorable branch gathers all its required premises.
        It does **not** test the truth-value conjunction -- the explicit `"no"`
        cases do that, and they publish zero.
        """
        row = self._row(self.c3, CAND_RULE_ID, CAND_SYMBOL)
        self.assertEqual(row["disposition"], "blocked")
        self.assertNotIn(CAND_SYMBOL, self.c3["_run_values"])

    def test_c1_versus_c2_varies_only_the_ordinary_answer(self) -> None:
        self.assertNotEqual(
            float(self.c1["_run_values"][CAND_SYMBOL]),
            float(self.c2["_run_values"][CAND_SYMBOL]),
        )

    def test_rule_pins_the_enrollment_finding_and_the_actual_box1_finding(self) -> None:
        """Provenance reaches the document, not a fixture constant.

        The rule reads the closure-authorized subtotal, and the run's pin chain
        carries through to the box-1 member finding itself plus the family's
        closure authority.
        """
        pins = {p["id"] for p in self._row(self.c2, CAND_RULE_ID, CAND_SYMBOL)["pins"]}
        self.assertIn(ENROLL_FINDING_ID, pins)
        self.assertIn("demo.f1098e.box1.0", pins)
        self.assertIn(F1098E_FAMILY, pins)
        for premise in ("x1", "x2", "x3"):
            self.assertIn(f"demo.p1.cand.finding.{premise}", pins)

    def test_downstream_pins_the_derived_intermediate_not_the_ordinary_fact(self) -> None:
        """L4: the consumer depends on the derived consequence, not the answer."""
        intermediate = self._row(self.c2, CAND_RULE_ID, CAND_SYMBOL)
        down = self._row(self.c2, CAND_DOWN_RULE_ID, CAND_DOWN_SYMBOL)
        self.assertEqual(down["disposition"], "published")
        pins = {p["id"] for p in down["pins"]}
        self.assertIn(intermediate["finding_id"], pins)
        self.assertNotIn(ENROLL_FINDING_ID, pins)
        self.assertEqual(float(self.c2["_run_values"][CAND_DOWN_SYMBOL]), BOX1)

    def test_published_amount_follows_the_reported_amount(self) -> None:
        """The decisive test that the value is *derived from* the document.

        The suite's pin assertions are *subsets* over specific ids, and a
        subset can survive removal of a numerical dependency: this rule's
        `when` guard reads the enrollment fact, the box-1 family and the
        favorable premises whatever the value expression does. (The complete
        pin set does change under that mutation -- 15 pins become 14, losing
        the derived-subtotal finding -- but no assertion inspects the whole
        set.) Varying the reported amount is what discriminates arithmetic
        dependence.
        """
        with TemporaryDirectory() as tmp:
            subject = DisposableSurface(Path(tmp))
            other = _execute(
                subject,
                _candidate_acts(subject, enrollment="credential-program", box1=850.0),
            )
        self.assertEqual(float(other["_run_values"][CAND_SYMBOL]), 850.0)
        self.assertEqual(float(other["_run_values"][CAND_DOWN_SYMBOL]), 850.0)
        self.assertNotEqual(float(other["_run_values"][CAND_SYMBOL]), BOX1)

    def test_adverse_needs_no_x1_x3_support(self) -> None:
        """P0 § 2.4's asymmetry, as *implemented*.

        X1-X3 are gathered by a conditional_dependency_set on the favorable
        branch only. An unconditional `requires` would block every branch and
        silently defeat the asymmetry -- which is what an earlier version of
        this rule did.
        """
        with TemporaryDirectory() as tmp:
            subject = DisposableSurface(Path(tmp))
            report = _execute(
                subject,
                _candidate_acts(
                    subject, enrollment="individual-classes-only", premises=False
                ),
            )
        row = self._row(report, CAND_RULE_ID, CAND_SYMBOL)
        self.assertEqual(row["disposition"], "published")
        self.assertEqual(float(report["_run_values"][CAND_SYMBOL]), 0.0)

    def test_a_negative_premise_is_supported_adverse_evidence_not_unknown(self) -> None:
        """Presence and truth are separate dimensions.

        A current, accepted premise establishing that a conjunct is **false** is
        adverse evidence: the supported amount as to § 221(d)(1)(C) is
        determinately **zero**. That is a different product state from "the
        application cannot determine the consequence", which is C3's absence
        case. Each premise is tested separately, and the negative finding that
        supports the result is pinned.
        """
        premise_cases: tuple[tuple[str, dict[str, Any], str], ...] = (
            ("X1", {"x1": "no"}, "demo.p1.cand.finding.x1"),
            ("X2", {"x2": "no"}, "demo.p1.cand.finding.x2"),
            ("X3", {"x3": "no"}, "demo.p1.cand.finding.x3"),
        )
        for label, kwargs, finding_id in premise_cases:
            with self.subTest(premise=label):
                with TemporaryDirectory() as tmp:
                    subject = DisposableSurface(Path(tmp))
                    report = _execute(
                        subject,
                        _candidate_acts(
                            subject, enrollment="credential-program", **kwargs
                        ),
                    )
                row = self._row(report, CAND_RULE_ID, CAND_SYMBOL)
                self.assertEqual(row["disposition"], "published")
                self.assertEqual(float(report["_run_values"][CAND_SYMBOL]), 0.0)
                self.assertIn(finding_id, {p["id"] for p in row["pins"]})

    def test_partial_premise_presence_is_unknown_not_negative(self) -> None:
        """Two premises present and satisfied, one absent, is still unknown.

        The gather is all-or-nothing for the favorable branch: a determinate
        zero requires a premise that is *present and false*, not merely a
        missing one, however many of its siblings are supplied.
        """
        absence_cases: tuple[tuple[str, dict[str, Any], str], ...] = (
            ("x1 absent", {"x1": None}, X1_ID),
            ("x3 absent", {"x3": None}, X3_ID),
        )
        for label, kwargs, missing_id in absence_cases:
            with self.subTest(case=label):
                with TemporaryDirectory() as tmp:
                    subject = DisposableSurface(Path(tmp))
                    report = _execute(
                        subject,
                        _candidate_acts(
                            subject, enrollment="credential-program", **kwargs
                        ),
                    )
                row = self._row(report, CAND_RULE_ID, CAND_SYMBOL)
                self.assertEqual(row["disposition"], "blocked")
                self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
                self.assertIn(missing_id, row.get("missing", []))
                self.assertNotIn(CAND_SYMBOL, report["_run_values"])

    def test_both_absences_together_block_on_the_ordinary_fact(self) -> None:
        """Track 0 T3: enrollment absent *and* premises absent.

        Blocks naming only the enrollment type -- the outer guard gates X1-X3
        evaluation before their absence matters. No combination reads favorable.
        """
        with TemporaryDirectory() as tmp:
            subject = DisposableSurface(Path(tmp))
            report = _execute(
                subject, _candidate_acts(subject, enrollment=None, premises=False)
            )
        row = self._row(report, CAND_RULE_ID, CAND_SYMBOL)
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertEqual(row.get("missing"), [ENROLLMENT_ID])
        self.assertNotIn(CAND_SYMBOL, report["_run_values"])

    def test_two_statements_with_a_retraction_still_fall_outside(self) -> None:
        """Track 0 T5: the cardinality bound is not evaded by a retraction."""
        with TemporaryDirectory() as tmp:
            subject = DisposableSurface(Path(tmp))
            report = _execute(
                subject,
                _candidate_acts(
                    subject,
                    enrollment="credential-program",
                    statements=2,
                    lifecycle=[
                        {
                            "kind": "finding-retracted",
                            "payload": {"finding_id": ENROLL_FINDING_ID},
                        }
                    ],
                ),
            )
        row = self._row(report, CAND_RULE_ID, CAND_SYMBOL)
        self.assertEqual(row["disposition"], "inapplicable")
        self.assertIs(row["guard_result"], False)
        self.assertNotIn(CAND_SYMBOL, report["_run_values"])

    def test_two_statements_fall_outside_the_bounded_class(self) -> None:
        """The cardinality bound, exercised rather than declared."""
        with TemporaryDirectory() as tmp:
            subject = DisposableSurface(Path(tmp))
            report = _execute(
                subject,
                _candidate_acts(
                    subject, enrollment="credential-program", statements=2
                ),
            )
        row = self._row(report, CAND_RULE_ID, CAND_SYMBOL)
        # The exact selected behavior, not merely "anything but success".
        self.assertEqual(row["disposition"], "inapplicable")
        self.assertIs(row["guard_result"], False)
        self.assertNotIn(CAND_SYMBOL, report["_run_values"])
        # The dependent result blocks because the intermediate is absent.
        down = self._row(report, CAND_DOWN_RULE_ID, CAND_DOWN_SYMBOL)
        self.assertEqual(down["disposition"], "blocked")
        self.assertIn(CAND_SYMBOL, down.get("missing", []))
        self.assertNotIn(CAND_DOWN_SYMBOL, report["_run_values"])

    def test_route_never_reads_the_incumbent_compressed_witness(self) -> None:
        """The user must not still be asserting the conclusion this replaces."""
        for report in (self.c1, self.c2):
            for rule_id, symbol in (
                (CAND_RULE_ID, CAND_SYMBOL),
                (CAND_DOWN_RULE_ID, CAND_DOWN_SYMBOL),
            ):
                pins = {p["id"] for p in self._row(report, rule_id, symbol)["pins"]}
                self.assertFalse(
                    any(COMPRESSED_WITNESS_TOKEN in pin for pin in pins),
                    f"{rule_id} pins the compressed witness: {sorted(pins)}",
                )
        self.assertNotIn(COMPRESSED_WITNESS, json.dumps(CAND_RULE))
        self.assertNotIn(COMPRESSED_WITNESS, json.dumps(CAND_DOWN_RULE))


class ProvenanceAndLifecycle(unittest.TestCase):
    """L1, L3, L5 and M5 for Candidate B."""

    ENROLL_FACT = f"{ENROLLMENT_ID}|period={PERIOD_ID}"

    def _run_with(self, **kwargs: Any) -> tuple[dict[str, Any], list[dict[str, object]]]:
        with TemporaryDirectory() as tmp:
            subject = DisposableSurface(Path(tmp))
            acts = _candidate_acts(subject, **kwargs)
            return _execute(subject, acts), acts

    def _row(self, report: dict[str, Any]) -> dict[str, Any]:
        rows = _rows(report, CAND_RULE_ID, CAND_SYMBOL)
        self.assertEqual(len(rows), 1, rows)
        return rows[0]

    def test_l1_actor_to_current_finding_to_marshalled_input(self) -> None:
        """Two linked observations; the run object carries no actor.

        `InputFinding`/`SourceFact` have no actor field, so authorship is read
        from the `act.v1` envelope and then linked forward by `finding_id`.
        """
        report, acts = self._run_with(enrollment="individual-classes-only")
        assertion = [
            act
            for act in acts
            if act.get("kind") == "assertion"
            and cast(dict[str, Any], act["payload"])["finding"]["id"]
            == ENROLL_FINDING_ID
        ]
        self.assertEqual(len(assertion), 1, "one enrollment assertion act")
        # (i) the envelope names the actor.
        self.assertEqual(assertion[0]["actor"], USER)
        # (ii) that act's finding is the one the rule consumed.
        finding = cast(dict[str, Any], assertion[0]["payload"])["finding"]
        self.assertEqual(finding["fact_id"], self.ENROLL_FACT)
        self.assertIn(
            finding["id"], {p["id"] for p in self._row(report)["pins"]}
        )

    def test_l3_the_declared_authority_chain_is_preserved_in_provenance(self) -> None:
        """Citation-role pins for the chain the adverse inference actually uses.

        This proves only that the executed rule **preserved its declared
        authority**. `citation.v1`'s own contract is that resolution is
        "structural/adoption-only and does not claim external legal
        verification" (ADR-0029), so it proves nothing about legal correctness
        and nothing about which historical edition of the HEA text was
        incorporated. The human semantic review owns the inference itself.
        """
        row = self._row(self._run_with(enrollment="individual-classes-only")[0])
        self.assertEqual(row["artifact_id"], CAND_RULE_ID)
        cited = {p["id"] for p in row["pins"] if p.get("role") == "citation"}
        self.assertEqual(cited, set(CITATION_IDS))
        self.assertIn(
            "tax.us.2025.package.core-calculations", {p["id"] for p in row["pins"]}
        )

    def test_l5_the_box1_source_finding_itself_is_preserved(self) -> None:
        """Compared at the layer L5 names: the **source** finding, not a subtotal.

        The derived subtotal publication is a downstream control, not the
        original report. What must be preserved is the admitted Form 1098-E
        box-1 source finding: its finding id, fact id, value and statement
        identity, identical across both branches, and pinned by both results.
        """

        def box1_source(acts: list[dict[str, object]]) -> dict[str, Any]:
            found = [
                cast(dict[str, Any], cast(dict[str, Any], act["payload"])["finding"])
                for act in acts
                if act.get("kind") == "assertion"
                and BOX1_FACT_TYPE
                in str(
                    cast(dict[str, Any], cast(dict[str, Any], act["payload"]).get("finding", {})).get(
                        "fact_id", ""
                    )
                )
            ]
            assert len(found) == 1, found
            return found[0]

        adverse, adverse_acts = self._run_with(enrollment="individual-classes-only")
        favorable, favorable_acts = self._run_with(enrollment="credential-program")

        a_src, f_src = box1_source(adverse_acts), box1_source(favorable_acts)
        # Identity, value and statement identity all unchanged.
        self.assertEqual(a_src["id"], f_src["id"])
        self.assertEqual(a_src["fact_id"], f_src["fact_id"])
        self.assertEqual(float(a_src["value"]), float(f_src["value"]))
        self.assertIn("statement=demo.stmt.a", a_src["fact_id"])
        self.assertIn("lender=demo.lender.a", a_src["fact_id"])

        # Both executed results pin that same source finding.
        for report in (adverse, favorable):
            self.assertIn(
                a_src["id"], {p["id"] for p in self._row(report)["pins"]}
            )

        # Downstream control: the derived subtotal also matches...
        self.assertEqual(
            float(adverse["_run_values"][SUBTOTAL_SYMBOL]),
            float(favorable["_run_values"][SUBTOTAL_SYMBOL]),
        )
        # ...while the consequence differs, so preservation is not inertness.
        self.assertNotEqual(
            float(adverse["_run_values"][CAND_SYMBOL]),
            float(favorable["_run_values"][CAND_SYMBOL]),
        )

    def test_m5_correction_at_the_same_fact_id_changes_the_consequence(self) -> None:
        """A correction is a new assertion at the same `fact_id`."""
        report, _ = self._run_with(
            enrollment="credential-program",
            lifecycle=[
                {
                    "kind": "assertion",
                    "payload": {
                        "finding": _attested(
                            "demo.p1.cand.finding.enrollment.corrected",
                            self.ENROLL_FACT,
                            "individual-classes-only",
                        )
                    },
                }
            ],
        )
        row = self._row(report)
        self.assertEqual(row["disposition"], "published")
        # The corrected answer governs: zero, not the reported amount.
        self.assertEqual(float(report["_run_values"][CAND_SYMBOL]), 0.0)
        pins = {p["id"] for p in row["pins"]}
        self.assertIn("demo.p1.cand.finding.enrollment.corrected", pins)
        self.assertNotIn(ENROLL_FINDING_ID, pins)

    def test_m5_retraction_leaves_the_consequence_unknown(self) -> None:
        """Retraction ends current support and asserts no opposite claim."""
        report, _ = self._run_with(
            enrollment="credential-program",
            lifecycle=[
                {
                    "kind": "finding-retracted",
                    "payload": {"finding_id": ENROLL_FINDING_ID},
                }
            ],
        )
        row = self._row(report)
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "DEPENDENCY_ABSENT")
        self.assertIn(ENROLLMENT_ID, row.get("missing", []))
        self.assertNotIn(CAND_SYMBOL, report["_run_values"])

    def test_m5_reassertion_after_retraction_is_a_new_finding(self) -> None:
        """A later answer is a new event, never a revival of the retracted one."""
        report, _ = self._run_with(
            enrollment="credential-program",
            lifecycle=[
                {
                    "kind": "finding-retracted",
                    "payload": {"finding_id": ENROLL_FINDING_ID},
                },
                {
                    "kind": "assertion",
                    "payload": {
                        "finding": _attested(
                            "demo.p1.cand.finding.enrollment.reasserted",
                            self.ENROLL_FACT,
                            "individual-classes-only",
                        )
                    },
                },
            ],
        )
        row = self._row(report)
        self.assertEqual(row["disposition"], "published")
        self.assertEqual(float(report["_run_values"][CAND_SYMBOL]), 0.0)
        pins = {p["id"] for p in row["pins"]}
        self.assertIn("demo.p1.cand.finding.enrollment.reasserted", pins)
        self.assertNotIn(ENROLL_FINDING_ID, pins)


class NegativeControlWrongInput(unittest.TestCase):
    """The user-authored legal conclusion: an FC6 failure, not a crash.

    The engine does **not** reject this mechanically, and that is the finding.
    A numerically correct shortcut is still the wrong responsibility boundary.
    """

    def test_a_user_supplied_legal_conclusion_drives_the_arithmetic(self) -> None:
        with TemporaryDirectory() as tmp:
            subject = DisposableSurface(Path(tmp))
            report = _execute(
                subject,
                _candidate_acts(
                    subject, enrollment="credential-program", legal_conclusion="yes"
                ),
            )
        rows = _rows(report, NEGCTL_RULE_ID, NEGCTL_SYMBOL)
        self.assertEqual(len(rows), 1, rows)
        row = rows[0]
        # It works. That is the problem.
        self.assertEqual(row["disposition"], "published")
        self.assertEqual(float(report["_run_values"][NEGCTL_SYMBOL]), BOX1)
        # The downstream result pins the filer's own legal conclusion...
        self.assertIn(NEGCTL_FINDING_ID, {p["id"] for p in row["pins"]})
        # ...and no authority is appealed to, because no inference was made.
        self.assertEqual(
            set(), {p["id"] for p in row["pins"] if p.get("role") == "citation"}
        )

    def test_contrast_candidate_b_owns_the_inference(self) -> None:
        """FC6 distinguishes the two: who supplies the tax conclusion."""
        with TemporaryDirectory() as tmp:
            subject = DisposableSurface(Path(tmp))
            report = _execute(
                subject,
                _candidate_acts(
                    subject, enrollment="credential-program", legal_conclusion="yes"
                ),
            )
        shortcut = _rows(report, NEGCTL_RULE_ID, NEGCTL_SYMBOL)[0]
        candidate = _rows(report, CAND_RULE_ID, CAND_SYMBOL)[0]
        # Same published amount by two routes...
        self.assertEqual(
            float(report["_run_values"][NEGCTL_SYMBOL]),
            float(report["_run_values"][CAND_SYMBOL]),
        )
        # ...but only the candidate cites authority for the inference...
        self.assertEqual(
            set(CITATION_IDS),
            {p["id"] for p in candidate["pins"] if p.get("role") == "citation"},
        )
        self.assertEqual(
            set(), {p["id"] for p in shortcut["pins"] if p.get("role") == "citation"}
        )
        # ...and only the shortcut pins a filer-authored legal conclusion.
        self.assertIn(NEGCTL_FINDING_ID, {p["id"] for p in shortcut["pins"]})
        self.assertNotIn(NEGCTL_FINDING_ID, {p["id"] for p in candidate["pins"]})


class MultiSubjectObservations(unittest.TestCase):
    """M6 and M7 -- observations, with the incumbent and candidate kept apart."""

    LINE21 = "tax.us.2025.schedule1.line21-sli-deduction"

    def _incumbent(self, divergent: bool) -> dict[str, Any] | None:
        from tests.test_f1098e_student_loan_interest_agi_track6 import execute

        a = Statement(lender="demo.lender.a", stmt="demo.stmt.a", box1=BOX1)
        b = Statement(lender="demo.lender.b", stmt="demo.stmt.b", box1=300.0)
        if divergent:
            b.witnesses["no-non-qualified-loan-component"] = "no"
        report, _, refusal = execute(
            _f1098e_acts(statements=[a, b], close=True, wages=50000),
            f"demo.p1.m6.{'divergent' if divergent else 'agreeing'}",
        )
        self.assertIsNone(refusal, refusal)
        rows = [
            row
            for row in report.get("dispositions", [])
            if row.get("artifact_id") == "tax.us.2025.rule.sli-worksheet"
        ]
        return rows[0] if rows else None

    def test_m6_incumbent_agreeing_witnesses_publish(self) -> None:
        row = self._incumbent(divergent=False)
        assert row is not None
        self.assertEqual(row["disposition"], "published")

    def test_m6_incumbent_divergent_witnesses_block_the_whole_route(self) -> None:
        """O3, not O1.

        `collect_categorical_all_equal` is a genuine universal test: a single
        `"no"` on one statement blocks the entire deduction. The incumbent does
        **not** read one arbitrary statement's witness and does **not** copy one
        answer across both -- so no wrong number is published. It also does not
        differentiate: the qualifying statement loses its deduction too.
        """
        row = self._incumbent(divergent=True)
        assert row is not None
        self.assertEqual(row["disposition"], "blocked")
        self.assertEqual(row["code"], "SLI_UNIVERSAL_COMPONENT_VIOLATION")

    def test_m6_candidate_places_two_statements_outside_its_class(self) -> None:
        """Recorded separately from the incumbent baseline.

        Candidate B narrows currently supported behavior -- the incumbent
        publishes for two agreeing statements, the candidate does not -- and it
        does not differentiate them either.
        """
        with TemporaryDirectory() as tmp:
            subject = DisposableSurface(Path(tmp))
            report = _execute(
                subject,
                _candidate_acts(
                    subject, enrollment="credential-program", statements=2
                ),
            )
        rows = _rows(report, CAND_RULE_ID, CAND_SYMBOL)
        self.assertEqual(rows[0]["disposition"], "inapplicable")
        self.assertIs(rows[0]["guard_result"], False)

    def test_m7_divergent_loan_circumstances_are_unrepresentable(self) -> None:
        """O5 -- inability to represent. Evidence level `read`, NOT `run`.

        This test executes no multi-loan scenario, because none can be
        constructed honestly at this boundary; fabricating an invalid fixture
        to call it execution would prove nothing. It inspects the production
        Form 1098-E fact type and the candidate's period-keyed fact directly
        and establishes that the current vocabulary has no loan identity, no
        per-loan box-1 allocation, and no statement-to-loan relationship.

        Ceiling: this does **not** prove that no bounded specialized mechanism
        could be designed, and does **not** establish that Evaluation Context
        is required.
        """
        # The ordinary fact is keyed on a period -- not a loan.
        self.assertEqual(
            {key["name"] for key in _period_keyed(ENROLLMENT_ID)}, {"period"}
        )
        # Box 1 is keyed on lender + statement + tax-year, and its value is a
        # single number: there is no loan dimension and no allocation.
        bundle = json.loads((CONTENT / "f1098e.bundle.json").read_text("utf-8"))
        box1 = next(
            fact
            for fact in bundle["fact_types"]
            if fact["id"] == BOX1_FACT_TYPE
        )
        self.assertEqual(
            {key["name"] for key in box1["identity_keys"]},
            {"lender", "statement", "tax-year"},
        )
        self.assertEqual(box1["value_schema"]["type"], "number")


class IncumbentVersusCandidate(unittest.TestCase):
    """A vs B -- **behavioral only**. Many variables differ; nothing causal.

    Candidate B's `bounded-line1` is an **analogue** of the worksheet's
    line-1/line-21 path, not the production worksheet itself.
    """

    def test_the_two_routes_name_different_outputs_and_different_support(self) -> None:
        from tests.test_f1098e_student_loan_interest_agi_track6 import execute

        incumbent, _, refusal = execute(
            _f1098e_acts(
                statements=[
                    Statement(lender="demo.lender.a", stmt="demo.stmt.a", box1=BOX1)
                ],
                close=True,
                wages=50000,
            ),
            "demo.p1.avb.incumbent",
        )
        self.assertIsNone(refusal, refusal)
        with TemporaryDirectory() as tmp:
            subject = DisposableSurface(Path(tmp))
            candidate = _execute(
                subject,
                _candidate_acts(subject, enrollment="individual-classes-only"),
            )

        def row_for(report: dict[str, Any], artifact: str) -> dict[str, Any] | None:
            rows = [
                r
                for r in report.get("dispositions", [])
                if r.get("artifact_id") == artifact
            ]
            return rows[0] if rows else None

        worksheet = row_for(incumbent, "tax.us.2025.rule.sli-worksheet")
        assert worksheet is not None
        # The incumbent publishes Schedule 1 line 21 and reads the compressed
        # witness among its support.
        self.assertEqual(worksheet["disposition"], "published")
        self.assertEqual(worksheet["symbol"], "tax.us.2025.schedule1.line21-sli-deduction")
        self.assertTrue(
            any(COMPRESSED_WITNESS_TOKEN in p["id"] for p in worksheet["pins"]),
            "the incumbent's support includes the compressed witness",
        )

        # The candidate publishes its own analogue symbol and does not.
        down = row_for(candidate, CAND_DOWN_RULE_ID)
        assert down is not None
        self.assertEqual(down["symbol"], CAND_DOWN_SYMBOL)
        self.assertNotEqual(down["symbol"], worksheet["symbol"])
        self.assertFalse(
            any(COMPRESSED_WITNESS_TOKEN in p["id"] for p in down["pins"])
        )


class SealIntegrity(unittest.TestCase):
    """What the seal itself guarantees -- nothing more.

    This class deliberately makes no claim about the behavioral suite detecting
    a *correctly resealed* graph that omits the candidate rule. That would need a
    genuine resealed mutation run, which is not implemented here.
    """

    def test_editing_package_bytes_without_resealing_refuses(self) -> None:
        """Checksum integrity only: the adoption pins the sealed package."""
        with TemporaryDirectory() as tmp:
            subject = DisposableSurface(Path(tmp))
            package = json.loads((subject.members / PACKAGE_FILE).read_text("utf-8"))
            package["members"] = [
                m for m in package["members"] if m["id"] != CAND_RULE_ID
            ]
            (subject.members / PACKAGE_FILE).write_bytes(_bytes(package))
            resolved = resolve_production_package(
                [subject.adoption],
                run_scope=SCOPE,
                scope_user=USER,
                workspace_revision=33,
                surface=subject.surface,
            )
            self.assertFalse(hasattr(resolved, "resolved_members"), resolved)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
