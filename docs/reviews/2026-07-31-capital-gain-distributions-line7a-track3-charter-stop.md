# Capital-Gain Distributions / Line 7a — Track 3 Charter Stop

Audience: Owner and Foreman.

Status: **STOP — owner disposition required before Track 3 can build.**

## Launch and custody

- Track 2 merged through PR #120 at
  `90f12e607cd4ff61770c14859b2a720763361336`; `verify` run `30592473685`
  completed green.
- Track 3 was created from that exact merge and its charter was bound in
  `9ee0dfba9a94f7c0a69ec971db3e0b3e5f99ffd8`.
- The fresh Track-3 Builder stopped before editing. The worktree remained clean;
  there is no implementation commit, generated golden, browser result, or
  partial product change to adopt or discard.

## Reproduced stop evidence

1. `package.core-calculations.v7.json` resolves the line-7a field, line-7a and
   line-7b rules, and line-7a and line-7b citations, but does not contain the
   published `tax.us.2025.form1040.line-7b` form-field citizen.
2. The v7 package is immutable published history. The separately published
   line-7b field is likewise immutable.
3. The existing line-7b field binds
   `tax.us.2025.schedule-d-required.conclusion`; the line-7b rule publishes
   `tax.us.2025.form1040.line7b-schedule-d-not-required`. The resolved graph
   therefore does not expose one field whose declared symbol joins the atomic
   published/blocked/guard-inapplicable line-7b rule disposition through the
   generic presentation path.
4. A synthetic v7 `live_coordinate_run` succeeds and its presentation artifact
   contains line 7a but no line 7b. This confirms the absence at the charter's
   authoritative entrypoint rather than through a hand-shaped model.

Adding the historical field out of band, loading unadopted content, or branching
on line-7b tax IDs in the projector would violate the Track-3 charter. Editing
v7 or the published field in place would violate immutable-history rules.

## Foreman triage

This is a **production-condition gap** from Track 2:

- ADR-0050 Decision 5 requires line 7a and line 7b as distinct atomic
  form-field dispositions.
- ADR-0050's Production Conditions require line-7a/7b form-field citizens and
  presentation of their atomic dispositions.
- The Track-3 charter correctly treats a missing content/package boundary as a
  stop rather than permission to manufacture presentation authority.

The earlier Track-2 repair allowance has already been consumed. A successor
content/package repair is therefore a scope-and-cap disposition for the owner,
not an automatic charter expansion.

## Owner choices

1. **Targeted prerequisite repair (recommended).** Extend the milestone with
   one post-merge Track-2 completion repair. Preserve all published history;
   add only the versioned line-7b field/package/release/adoption successors
   needed for a resolved graph to expose the atomic line-7b disposition through
   generic symbol joins, with production-shaped synthetic tests. Independently
   review that repair, merge it, then rebind and restart Track 3.
2. **Rescope Track 3 to line 7a only.** Amend the milestone contract and exit
   criteria to defer line 7b. This knowingly leaves ADR-0050's line-7b
   production condition incomplete.
3. **Stop the milestone after Track 2.** Record the line-7b presentation path
   as an unresolved production gap and do not claim the milestone's current
   exit criteria.

No option is selected by this record.
