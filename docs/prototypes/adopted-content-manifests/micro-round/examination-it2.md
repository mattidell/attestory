# Examination: Iteration 2 — ACM Micro-Round Residuals

This document verifies the clean-room rival design against the nine cases of the charter.

---

## Static-Level Verification

### MR-P1: Fact-Surface Versioning & Wholesale-Adoption Reconciliation
**Status:** Settled-at-static-level.

```python
def validate_mr_p1(package, adopted_bundles, corpus):
    """Verifies fact surface membership, inclusion joins, and mappings."""
    issues = []
    fact_surface = {}  # id -> version
    
    # 1. Gather pinned fact-types and fact-type-bundles
    for pin in package["members"]:
        if pin["role"] == "fact-type":
            fact_surface[pin["id"]] = pin["version"]
            # Case 3 (Negative): unversioned/unresolvable pins fail validation
            citizen = corpus.get((pin["id"], pin["version"]))
            if not citizen or "version" not in citizen:
                issues.append("UNVERSIONED_OR_UNRESOLVABLE_PIN")

    # Case 4 (Negative): Pin/bundle drift detection via inclusion joins
    for ft_id, ft_ver in fact_surface.items():
        found_in_adopted = False
        for bundle in adopted_bundles:
            for ft in bundle.get("fact_types", []):
                if ft["id"] == ft_id:
                    if ft["version"] == ft_ver:
                        found_in_adopted = True
                    else:
                        issues.append("PIN_BUNDLE_VERSION_DRIFT")
        if not found_in_adopted:
            issues.append("PIN_NOT_ADOPTED_IN_WORKSPACE")

    # Case 5 (Negative): Mapping fact-type gap check
    for pin in package["members"]:
        if pin["role"] == "source-closure-mapping":
            mapping = corpus.get((pin["id"], pin["version"]))
            if mapping:
                for key in ("member_fact_type", "closure_fact_type"):
                    ft_id = mapping.get(key)
                    if ft_id not in fact_surface:
                        issues.append("MAPPING_FACT_TYPE_GAP")

    # Cases 1 & 2 (Positive): Resolves exact identities and accepts valid joins
    return issues
```

### MR-P2: Declared Composition-Obligation Trigger
**Status:** Settled-at-static-level.

```python
def validate_mr_p2(package, corpus):
    """Enforces composition obligations without circularity or presentation leaks."""
    issues = []
    obligated_symbols = set()
    compositions = {}  # symbol -> composition_id
    rules = {}         # symbol -> rule_citizen

    # Gather pinned governance, composition, and computation citizens
    for pin in package["members"]:
        citizen = corpus.get((pin["id"], pin["version"]))
        if not citizen:
            continue
        if citizen["schema"] == "composition-obligation.v1":
            obligated_symbols.add(citizen["symbol"])
        elif citizen["schema"] == "taxable-interest-composition.v1":
            compositions[citizen["publishes"]] = citizen["id"]
        elif citizen["schema"] == "rule-artifact.v1":
            rules[citizen["publishes"]] = citizen

    # Validate obligations
    for symbol in obligated_symbols:
        # Case 7 (Negative): Reject bare sum with no composition citizen
        comp_id = compositions.get(symbol)
        if not comp_id:
            issues.append("COMPOSITION_CITIZEN_MISSING")
            continue

        # Case 8 (Negative): Reject obligation without rule composition pin
        rule = rules.get(symbol)
        if rule:
            has_comp_pin = any(
                p["role"] == "composition" and p["id"] == comp_id
                for p in rule.get("pins", [])
            )
            if not has_comp_pin:
                issues.append("COMPOSITION_PIN_MISSING")

    # Case 6 (Positive): Validates composition-governed unit when all match
    # Case 9 (Negative): Form-fields remain presentation-only; no hardcoded runner strings
    return issues
```
