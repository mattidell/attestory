# Capital-Gain Distributions / Line 7a — Track 4 F1 Repair Recheck

**Verdict: READY**

## Object, posture, and boundary

- Orientation resolved `HEAD` to
  `57629e1699ff7e584055fbf57cb0a49bcb9dd75a`; `git rev-parse HEAD`
  independently matched it.
- Exact repair range:
  `c2e52338cca3ea58e72db1ba6efbd796746047bc..
  c2d6c1a2fe1f63c8904da59ad565767cf561db0a`. It contains one commit,
  whose parent is the repair-charter commit. The recheck-charter/pointer
  commit is the repair tip's direct successor and is excluded from the object.
- This continues the original author-independent Completion Reviewer lineage.
  It is a focused F1 recheck, not a second completion review.
- Evidence was limited to the committed predecessor ledger, original
  completion review, and exact repair diff. All original completion-review
  measurements outside F1 remained credited.
- The one-file ceiling was
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a-deferral-ledger.md`.
  No stop condition fired.

## Measurements

### 1. Exact object and containment — pass

`git rev-list --count` returned `1`, and `git diff --name-only` returned only:

```text
docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a-deferral-ledger.md
```

No implementation, schema, content, package, test, ADR, governance, matrix,
pointer, plan, frontier, roadmap, retrospective, README, or other record is
inside the repair range.

### 2. Exact predecessor obligation and triggers — pass

The new entry explicitly identifies the Dividends and Schedule B deferral
ledger, entry 5. It preserves all four required facts:

1. Schedule B Part I still ties only to the box-1/1099-INT family.
2. The tie-out has not been generalized to a multi-family interest sum.
3. The obligation is untouched and not retired.
4. Reactivation occurs upon either an interest-breadth milestone admitting a
   second 1099-INT family or any milestone that must prove Schedule B Part I
   against more than one family.

The entry carries the predecessor obligation without narrowing or
reinterpreting it.

### 3. Every other ledger entry — pass

The raw diff adds only the new entry and increments the ordinal prefixes of
the four following entries. An independent whole-file comparison removed the
new entry from the repair tip, normalized every numeric list prefix to `N.`,
and compared that result against the similarly normalized repair base. The
comparison was byte-equal with no output.

Every other entry therefore retains its prior substance, classification, and
trigger.

### 4. Scope and safety — pass

The repair does not select or recommend an interest milestone, make an
implementation claim, retire the obligation, or alter any other completion
record. The added prose contains no real/private material, values,
dispositions, refusal reasons, credentials, or locators.

## Verification

```text
git rev-list --count c2e52338cca3ea58e72db1ba6efbd796746047bc..c2d6c1a2fe1f63c8904da59ad565767cf561db0a
# 1

git diff --name-only c2e52338cca3ea58e72db1ba6efbd796746047bc..c2d6c1a2fe1f63c8904da59ad565767cf561db0a
# exactly the one ledger path

git diff --check c2e52338cca3ea58e72db1ba6efbd796746047bc..c2d6c1a2fe1f63c8904da59ad565767cf561db0a
# clean

rg -n "Schedule B Part I|box-1/1099-INT|multi-family" \
  docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a-deferral-ledger.md
# entry 10 contains the obligation and both triggers

python3 tools/governance_lint.py
# governance lint: conformant

python3 tools/envelope_scan.py --range main..HEAD
# clean
```

No full suite, repeated PR/CI measurement, real-data operation, or broader
completion review was performed. F1 is closed, and every credited
completion-review measurement remains intact.
