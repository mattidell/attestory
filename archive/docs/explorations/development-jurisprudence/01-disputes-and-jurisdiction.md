# Disputes and Jurisdiction

Status: exploratory, not binding.

## What a Dispute Is

A dispute is a moment where two locally defensible conventions demand
incompatible continuations of the system. Neither side is a mistake. "The UI
needs simpler data than raw artifacts" is true and reasonable; "the artifacts
are the product" is also true and reasonable; a read-model layer satisfies
one by violating the other. The dispute is not an error to prevent — it is
the normal byproduct of a system growing.

This definition has a corollary that shapes everything downstream: disputes
originate in change, and only in change. A frozen codebase has no disputes.
Every incoming requirement, refactor, or agent implementation choice is a
potential collision between something new and something settled. The rate of
disputes is proportional to velocity, which means any governance design that
slows velocity to reduce disputes is treating the symptom by killing the
patient.

## A Taxonomy of Origins

Disputes arrive from a small number of directions, and knowing the direction
helps route the settlement:

- Evolution disputes: a new requirement meets existing structure, and the
  question is which existing structure bends. The most common kind.
- Boundary disputes: two subsystems with coherent internal conventions meet
  at a seam, and the seam must obey one, the other, or a treaty.
- World-model disputes: reality is ambiguous and the representation must
  choose. Is a corrected document a new fact or a revision of an old one?
  Is a jurisdiction a property or a list? These are ontology arguments
  wearing implementation clothes.
- Interface disputes: what the system knows versus what the user sees, and
  who controls the framing. Wizard-versus-workspace is one of these.
- Convenience disputes: the daily micro-collisions between an invariant and
  the easier path. "It would be simpler to just write the value here."
  Individually trivial; in aggregate, they are the primary erosion force.

## The Silent Majority

Almost no disputes present as arguments. They are settled implicitly, in the
moment, by whoever writes the code — each one a tiny trial that nobody knew
was in session. This matters doubly under agent delegation: an agent settles
silent disputes faster than any human, with great fluency, and with a strong
prior toward prevailing industry convention, because that is what it has
seen most. Unwritten jurisdiction therefore has a predictable outcome: the
default party wins, and the default party is the industry mean. Drift is not
a failure of diligence; it is the equilibrium state of ungoverned silent
disputes.

Thomas Schelling's notion of focal points is useful here: coordination
without communication succeeds when one option is salient to all parties.
Written principles are salience engineering — they make your preferred
settlement the obvious one, so silent disputes settle your way without
anyone convening a court.

## What Jurisdiction Means

Jurisdiction is the pre-assignment of dispute classes to authorities: this
kind of collision is settled by that mechanism. The authorities available in
a development context form a rough ladder:

1. Canon artifacts — the dispute is settled by looking something up. If the
   schema says the shape, the shape is settled.
2. Mechanical checks — the dispute is settled by a machine applying a rule.
   Nobody argues with a failing acyclicity check; they fix the cycle or
   petition to change the check.
3. Standards applied in review — a human or agent judges the case against a
   written principle. Slower, context-sensitive, fallible, adaptable.
4. Judgment — a designated person decides, because the dispute is novel or
   the stakes exceed every written authority.

A healthy system pushes each dispute class as far down this ladder as it can
go without distorting outcomes — and no further. The failure modes at both
ends are familiar: everything-is-judgment produces a bottleneck judge and
inconsistent case law; everything-is-mechanical produces a bureaucracy of
checks that encode yesterday's disputes and obstruct tomorrow's.

The design question for any given project is not "should we govern changes"
— silence governs them already. It is "which dispute classes deserve
promotion from silent settlement to assigned jurisdiction, and to which
rung." That question is taken up in the next document.
