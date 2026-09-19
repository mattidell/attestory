# Guidelines for planning and development

## 1. Begin with a plain-language account of the work

The initial plan should explain:

- What we are trying to accomplish.
- Why it matters.
- What circumstances and concepts are involved.
- What relationships the application must understand.
- What makes the work difficult or uncertain.
- What we expect to learn.
- What would count as a successful outcome.

Write for someone who has not yet acquired the project's context. Introduce
specialized terms as their meaning becomes necessary.

## 2. Represent complexity at the level currently understood

A high-level plan should make the important complexity visible. It can identify
interacting rules, uncertain relationships, limitations of existing software,
and competing requirements in ordinary language.

Specificity should grow with understanding. A statement such as “each amount
must remain connected to the circumstances that determine how it is treated”
can establish a clear obligation before the mechanism for maintaining that
connection is known.

## 3. Include the development of the plan within the plan

Plan for successive refinement:

1. Describe the purpose and the important questions.
2. Investigate the relevant concepts and existing behavior.
3. Establish the relationships and distinctions that must be preserved.
4. Explore possible representations and mechanisms.
5. Test consequential assumptions.
6. Select an approach and specify its implementation.
7. Revisit earlier decisions when new evidence changes their basis.

Each stage should produce enough understanding to shape the next stage. Allow
the investigation to change the proposed sequence, scope, and division of work.

## 4. Identify the different things being modeled

Make explicit which aspects of the work require understanding:

- The real-world circumstances.
- The rules applied to those circumstances.
- The information available to the application.
- The representation of that information.
- The application's computations and behavior.
- The meaning communicated to the user.
- The development process and its participants.
- The evidence used to judge the work.

Consider each separately and examine their relationships. Success in one area
may leave questions open in another.

## 5. Express required behavior before choosing its mechanism

Describe what the application must preserve, distinguish, account for, and
communicate.

Then investigate how the software can satisfy those obligations. When proposing
reuse of an existing approach, identify what the earlier work established and
what the new situation requires beyond it.

Keep proposed mechanisms open to revision until their important assumptions
have been examined.

## 6. Make unresolved decisions visible

For each consequential uncertainty, identify:

- What needs to be decided.
- Why the decision matters.
- What depends on it.
- What evidence could help resolve it.
- When it must be resolved.

An unresolved decision can be a legitimate output of an early planning stage.
Give it an explicit place in subsequent work.

## 7. Use gates to establish readiness for dependent work

A gate should answer a practical question: Do we understand enough to take the
next step responsibly?

Define the decisions and evidence needed to answer that question. Distinguish
readiness to investigate, readiness to select an approach, readiness to
implement, and readiness to release.

Review the gates themselves as understanding develops. New evidence may reveal
an obligation that the original plan omitted.

## 8. Investigate boundaries and change

As the plan becomes more concrete, examine:

- Missing, conflicting, duplicate, or incomplete information.
- Multiple items with different circumstances.
- Corrections, replacements, and withdrawals.
- Information lost through aggregation or simplification.
- Cases the proposed mechanism might silently overlook.
- Differences between an unfavorable result and an unresolved result.

Use these cases to discover what the representation and behavior must support.

## 9. Design evidence around the claim being evaluated

State what an investigation or experiment is intended to establish.

Identify which parts use existing software, which are proposed, and which are
supplied manually. Choose cases that could expose a failure in the proposed
approach.

Keep conclusions within the demonstrated scope. Record remaining uncertainty
clearly enough that later work can investigate it.

## 10. Review meaning across the whole path

Follow the meaning of information from its source through its representation,
computation, result, and explanation.

Check that names, quantities, relationships, and claims remain consistent.
Examine what a user or subsequent developer would reasonably understand from
the output.

Include how trustworthy information is obtained and maintained, alongside how
the application consumes it.

## 11. Treat repairs as changes to connected understanding

When a finding changes an assumption, follow its consequences through the plan,
design, experiments, implementation, and handoff material.

Update the current account wherever another participant will encounter it.
Reassess conclusions that depended on the repaired assumption, including
conclusions introduced by the review itself.

## 12. Preserve learning when the direction changes

Investigation may reveal a prerequisite, a separate information problem, or an
implementation cost that changes the appropriate scope.

Record what remains useful, what was disproved, what remains unresolved, and
what future work must establish.

A milestone can produce valuable understanding even when the evidence supports
revising or postponing its proposed implementation.

## Governing principle

The initial plan represents the complexity in language people can understand.
Successive work turns that understanding into decisions, representations, and
executable behavior, with evidence supporting each increase in specificity.
