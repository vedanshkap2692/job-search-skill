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

**Email rules (hard):** only PUBLISHED work emails — printed in the post, JD, careers page, or company site. Never guess patterns (first.last@company), never scrape personal emails, never use lookup tools the user didn't install. If no published address exists, hand the lead to outreach for a LinkedIn note instead.

## Qualify before emailing

- The role must pass the normal filters (`me/profile.md`): location, seniority in range, pay floor, not already applied, under the per-company cap.
- Ledger first: add the job (shortlist it if the fit clears the user's bar) and the person (people table, relation 'recruiter' or 'team', email in the email column). Check `messages` so nobody is emailed twice — one thread per person, follow-ups inside it.

## The email

Subject: `Application: <role> — <user's name>` (or `Re: your post about hiring <role>` for posts).
Body, 90–140 words, plain text, the user's voice (`me/style.md`):
1. One line naming exactly what they posted and where ("your post today about hiring a <role>").
2. Two to three lines of evidence from `me/master_resume.md` chosen for THAT post — lead with the project closest to what they're hiring for. Numbers, no adjectives.
3. If they asked for details (pay, notice, location), answer all of them in a compact list from `me/profile.md` — and only what they asked.
4. Close plainly: available for a call this week; resume attached.

Attach the resume for that role family (tailored via [resumes](../resumes/SKILL.md) for strong fits if time allows; base resume otherwise, per permissions). Sign with the user's phone, application email and LinkedIn URL from the profile.

## Sending

Send only from the user's dedicated application email — never from a current-employer account, whatever is signed in. Mechanics (connector vs. the mail site in the controlled browser, attachments, multi-account pitfalls) are in [playbooks/email.md](../../playbooks/email.md).

## Review, always

Before sending, run the independent review ([review](../review/SKILL.md), Outreach checklist): claims traceable to the bank, role named right, length, no stuffing, person not already contacted, wording varied across the batch. Fix findings, then send.

## After sending

- `messages` row: channel 'email', direction 'out', kind 'message', status 'sent', `follow_up_due` about +4 days.
- Log counts in `data/log.md` and `runs`.
- **Follow-up:** one, after ~4 days of silence, two lines, in the same thread. Never more than one follow-up per person.

## Pace and reputation

- A daily cap, agreed with the user (around 10/day is a sane default), with varied wording — never the same body twice. Recruiters compare notes, and mail providers spam-filter bursts of near-identical mail.
- Only genuinely relevant roles; one email per person, one thread.
- If anyone replies "not interested" or asks to stop: mark `people.status` 'skipped', never email again.
- Replies land in the tracked inbox — [inbox](../inbox/SKILL.md) routes them; interview-scheduling replies get drafted for the user per permissions.
