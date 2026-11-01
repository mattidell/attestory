# Retrospective — Schedule A Shows Gambling Losses (2025)

## Result

- **A filed Schedule A matches the itemized total on core v70.** Line 16
  shows gambling losses as recorded, the amount counted (up to winnings) and
  the amount not counted; a losses-only itemizer's attachment publishes.
- **Attachments gained two capabilities,** a part that applies only when
  its line or family has something, and a tie-out to a limited line
  (`attachment-rule.v12`). Every other attachment is unchanged.

## What the evidence changed

- **Guard by schema, prove by equality.** Every new runner path is guarded
  by the v12 name, and the other four attachments were checked by publishing
  the same payload on v69 and v70; the review found the one path that was not
  guarded.
- **Each schema successor needs its package schema.** As with the closure
  questions, `artifact-package` had to take a successor to admit the new
  member schema. Two milestones in a row met this at build time.

## Process

- One builder for P0, Track 1 and a repair; one review. This closed the last
  of the three owner-approved engine changes.

## Follow-ups

- The package schema's closed member-schema enum makes every new citizen
  schema a two-schema change; a looser admission rule would remove that.
