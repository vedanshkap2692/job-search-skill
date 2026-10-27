---
name: review
description: Independently check anything before it goes out in the user's name (a tailored resume, a batch of outreach, an application), look at results every week or two, and review the setup itself with the user. Use before every send or submit, and on the review schedule.
---

# Review

A second look by someone who didn't write it catches what the writer can't see: a must-have missed, a claim the bank doesn't back, a note that reads as spam. The review runs before **every** submission and send, even when the user has stopped checking things themselves, and even when it feels redundant. It is the system's main defence against the one mistake that matters most here: a claim going out in the user's name that they can't back in an interview.

## How to run a review

The review is **blind**: the reviewer must not see anything written during the tailoring — not the coverage notes, not the reasoning, not earlier drafts. A reviewer who reads the writer's notes inherits the writer's blind spots. The reviewer sees only:
  - the output;
  - the sources: the JD, `me/master_resume.md`, `me/profile.md`;
  - the rules: `me/style.md` and the relevant skill;
  - for outreach, also that company's rows in `people` and `messages`, so it can spot repeats.

- **With subagents:** start a fresh one with a prompt like the one below, on the strongest model available — this is the one place not to economise.
- **Without subagents:** do a separate pass with only those files open, and read the output as if a stranger wrote it.
- The reviewer lists problems; it doesn't rewrite. The writer fixes them, rebuilds, and records what was found and fixed (in the job's `notes.md` for resumes, in `data/log.md` for outreach).
- If a fix changes the resume, the changed version is what goes out — don't fix the file and send the old PDF.

```
Review this <resume / batch of outreach / application> for <company, role>.
Sources: <JD path>, me/master_resume.md, me/profile.md. Rules: me/style.md, skills/<skill>/SKILL.md.
Do not read any notes.md or tailoring notes — judge only what's in front of you.
List every problem with where it is and a suggested fix, most serious first. Check the list for <kind> in skills/review/SKILL.md.
Don't rewrite it. End with a score out of 100 (resumes only).
```

## Resume

- **Unbacked claims:** anything not in the bank. This is pass or fail; fix every one before it goes out.
- **Dropped qualifiers:** a claim that's only true with its qualifier ("shadow rollout", "on staging", "pilot") stated as if it were the unqualified thing. As serious as an unbacked claim.
- **Coverage:** must-haves the user has done that are missing from the bullets, or only in the skills line.
- **Impact:** numbers dropped from bullets that had them; small or unimpressive numbers.
- **Stuffing:** the same JD term repeated, or a technique mentioned twice.
- **Form:** length, layout, text that doesn't extract cleanly, typos, leftover placeholders.
- **Score** out of 100:
  - must-have coverage: 40;
  - evidence and impact: 25;
  - relevance and order: 15;
  - readability and parsing: 10;
  - wording: 10.

  Show the score with the top three fixes. By default, revise anything under about 75 before sending. The user can set their own bar.

## Outreach

- Within the site's length limit; the role named correctly; "applied" only if it really was.
- The right ask for the person's role; nothing claimed that isn't in the bank.
- Reads like a person wrote it: no flattery, no stacked claims, wording varied across the batch, matching the other person's tone in replies.
- Nobody messaged twice; no company flooded; each person is plausibly relevant to the role. Messages sent only because someone works there read as spam.

## Application

- Every field matches the profile and the bank; numbers only in numeric fields.
- The right resume attached — this job's file, not an older one.
- Screener answers honest and on the user's standard basis ([apply](../apply/SKILL.md), "Screener questions"): experience buckets the resume's dates support, skills from the "not claimed" list answered as none, trick questions answered truthfully.
- Required questions answered honestly, or the job queued for the user.
- Only required consents ticked; marketing, SMS and follow-company opt-ins unticked; demographic questions blank.

## Results, every week or two

Pull the numbers from the ledger. For example:
```sql
-- applications and responses by role family
SELECT family, COUNT(*) AS applied,
       SUM(status IN ('interviewing','offer','rejected')) AS heard_back
FROM jobs WHERE applied_at IS NOT NULL GROUP BY family;

-- outreach by type of person
SELECT relation, COUNT(*) AS contacted,
       SUM(connected_at IS NOT NULL) AS accepted,
       SUM(status IN ('replied','referred')) AS replied
FROM people WHERE status NOT IN ('found','skipped') GROUP BY relation;
```
Then report:
- what the numbers say, and what they don't say yet (a few dozen applications is noise; say so plainly);
- at most three or four specific changes, each tied to evidence: a resume angle, an outreach opener, which roles to target or drop.

Recommend; the user decides.

## Setup review, every week or two, or whenever the user asks

A look at the system itself, done with the user:
- What they still do by hand that you could take over, and what you do that they keep correcting.
- Whether the pace, the schedules and the dashboard still suit them.
- Rules in `me/style.md` that contradict each other or are out of date.
- What they want added: a new source, a study plan, tracking something else.

Agree the changes with them, make them (in `me/`, or in their copy of the skills), and log what changed.
