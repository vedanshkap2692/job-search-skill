---
name: cold-email
description: Find hiring opportunities that name an email address (LinkedIn posts, careers pages, job postings) and send a tailored application or intro email with the resume attached. Off until the user turns it on. Use on scheduled runs once enabled, when the user asks for outreach by email, and whenever a posting names an application email.
---

# Cold email

The goal is interviews. A short, specific email with a tailored resume, sent to the person who is actually hiring, within hours of them posting, beats a week-old portal application. This skill is **off by default**: it starts only when the user has turned it on in `me/permissions.md` (with how much is handed over — drafts, or sending too).

## Finding opportunities and addresses

Work these sources each run, newest first:
1. **LinkedIn posts (not the jobs tab).** Search posts for hiring language, sorted by recent:
   `https://www.linkedin.com/search/results/content/?keywords=<query>&sortBy=%22date_posted%22`
   Rotate queries built from the user's role families and locations: "hiring <role>", "we're hiring <specialty>", "hiring <role> <city>", "looking for <role>". Posts often include the poster's email or say "DM me / email me at …". The poster is usually the hiring manager or founder — the best possible target.
2. **Job postings that name an email** ("send your resume to …"). Treat every JD the ledger collects as a source; grep new JDs for email addresses.
3. **Careers pages / about pages** of high-fit companies already in the ledger: many startups publish careers@/talent@/jobs@ or a founder's work email.
4. **The posting's "job poster" on LinkedIn** — if no email is published, their LinkedIn DM is the fallback channel (that's [outreach](../outreach/SKILL.md), not this skill).

**Email rules (hard):** by default, only PUBLISHED work emails — printed in the post, JD, careers page, or company site. Never scrape personal emails, never use lookup tools the user didn't install. If no usable address exists, hand the lead to outreach for a LinkedIn note instead.

**Derived work emails** are allowed only if the user has turned them on in `me/permissions.md`. Then, for a hiring person (founder, recruiter, the team's lead) at a company worth the effort:
- the company's pattern (first@, first.last@, …) must be evidenced by at least one real published address of a person on the same domain, or the company publishes its own careers@/jobs@ alias (use that alias as is);
- the person must be confirmed at the company now, on their LinkedIn or the company site;
- no paid lookup tools, no SMTP probing or "verify email" services, no personal addresses;
- record the evidence (where the pattern came from, where the person was confirmed) in `people.notes`;
- a bounce marks the address bad: never retry variants of it.

A guessed address with no evidence is still out: guesses bounce, and bounces get the user's mail flagged as spam.

## Qualify before emailing

- The role must pass the normal filters (`me/profile.md`): location, seniority in range, pay floor, not already applied, under the per-company cap.
- Ledger first: add the job (shortlist it if the fit clears the user's bar) and the person (people table, relation 'recruiter' or 'team', email in the email column). Check `messages` so nobody is emailed twice — one thread per person, follow-ups inside it.
- **One company, one email** until someone there replies. Two people at the same company getting near-identical mail on the same day compare notes. The exception is a person plus the company's own careers@ alias on the same email (one send, both in To).

## The email

Subject: `Application: <role> — <user's name>` (or `Re: your post about hiring <role>` for posts).
Body, 90–140 words, plain text, the user's voice (`me/style.md`):
1. One line naming exactly what they posted and where ("your post today about hiring a <role>").
2. Two to three lines of evidence from `me/master_resume.md` chosen for THAT post — lead with the project closest to what they're hiring for. Numbers, no adjectives.
3. If they asked for details (pay, notice, location), answer all of them in a compact list from `me/profile.md` — and only what they asked.
4. Close plainly: available for a call this week; resume attached.

Attach the resume for that role family (tailored via [resumes](../resumes/SKILL.md) for strong fits if time allows; base resume otherwise, per permissions). Sign with the user's phone, application email and LinkedIn URL from the profile.

## Sending

Send only from the user's dedicated application email — never from a current-employer account, whatever is signed in. Mechanics (connector vs. the mail site in the controlled browser, attachments, multi-account pitfalls, scheduled sends) are in [playbooks/email.md](../../playbooks/email.md).

For a batch, schedule the sends for the start of the recipients' working day, a few minutes apart, rather than sending them all at once. Keep the final text of each email in the job's or the batch's notes, so the follow-up can quote what was said.

## Review, always

Before sending, run the independent review ([review](../review/SKILL.md), Outreach checklist): claims traceable to the bank, role named right, length, no stuffing, person not already contacted, wording varied across the batch. Fix findings, then send.

## After sending

- `messages` row: channel 'email', direction 'out', kind 'message', status 'sent' (or 'scheduled', then 'sent' once it has left), `follow_up_due` about +4 days.
- **Check delivery a few hours later.** Bounces arrive late, and they happen even for addresses published on the company's own site. Mark the message and the person 'bounced', tell the user in the log, and find another channel (a different published address, or outreach on LinkedIn) rather than retrying variants.
- Log counts in `data/log.md` and `runs`.
- **Follow-up:** one, after ~4 days of silence, two lines, in the same thread. Never more than one follow-up per person.

## Pace and reputation

- A daily cap, agreed with the user (around 10/day is a sane default), with varied wording — never the same body twice. Recruiters compare notes, and mail providers spam-filter bursts of near-identical mail.
- Review the whole batch independently before any of it goes out, not just each email: the reviewer checks that wording varies across the batch and that no company appears twice.
- Only genuinely relevant roles; one email per person, one thread.
- If anyone replies "not interested" or asks to stop: mark `people.status` 'skipped', never email again.
- Replies land in the tracked inbox — [inbox](../inbox/SKILL.md) routes them; interview-scheduling replies get drafted for the user per permissions.
