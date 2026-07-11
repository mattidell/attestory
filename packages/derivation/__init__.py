"""Derivation machinery: schema-authoritative evaluation of rule artifacts.

Per ADRs 0006-0008. Tax meaning lives in versioned rule-artifact citizens
in a closed expression language; the published schemas are the runtime
authority (ADR-0006 decision 3); derived findings enter the record through
derived-publication acts (ADR-0007); every run is bounded by a paired
derivation record (ADR-0008). This package holds the loader/validator,
eligibility model, saturation runner, reference runner, and explanation
walker built on those contracts.
"""
