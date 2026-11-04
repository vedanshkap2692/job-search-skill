# What the agent may do without asking

The user's choices, in plain words, with dates. They can change anything here just by saying so; update this file when they do and add a line to History. Anything not handed to the agent yet is drafted for the user.

The values in brackets are the recommended defaults for a new user. Onboarding asks only about sending, submitting and replies, and fills in the rest from these.

Whatever is handed over, the Never rules in AGENTS.md still hold (no invented facts, no passwords or CAPTCHAs, no double sends), and the independent review still runs on everything before it goes out.

**Status:** active (or "paused": scheduled runs then stop at the start)

## Applications
- Shortlisting: [the user picks from the list] / the agent picks fits of N and above
- Fill in forms: [yes]
- Submit: [no, leave at the last step for the user] / for fits of N and above / all shortlisted roles
- Resume: [tailored for every application] / tailored for fits of N and above, base resume otherwise
- Applications per company per week: [2] / no limit / N
- Easy Apply / one-click applies: [use them, and also apply on the company's own portal when the same role is open there] / Easy Apply alone is fine / skip Easy Apply when a direct form exists
- Channel order: [the company's own portal first; job boards and one-click applies only when there's no direct form, or as the extra in a double apply] / whichever is quickest
- Volume mode: [off: tailored applications to good fits] / on: apply to every role that passes the hard filters in `me/profile.md`; tailor for fits of N and above, and below that reuse the closest resume that already passed review (the review still runs on the pairing, and nothing is invented)
- Consents and attestations: [the agent ticks required privacy and terms boxes; "information is true" attestations and typed-name signatures are left for the user] / the agent handles those too, but only on forms where every answer came from `me/master_resume.md` and `me/profile.md`. Marketing and talent-community opt-ins stay unticked either way, and CAPTCHAs, one-time codes, passwords and account creation always stay with the user.

## LinkedIn
- Connection requests: [draft only] / send
- Notes on requests: [with a note when the account allows] / always without, then a message once they accept
- Message to someone who accepted: [draft only] / send
- Follow-ups to people who haven't replied: [draft only] / send; [two] per person, or N

## Email
- [drafts only] / send outreach / send replies
- Apply-by-email when a posting names an address: [draft for the user] / always send
- Proactive cold email (skills/cold-email): [off] / on, up to [10] a day, [one] follow-up max, [one] company per email until someone there replies
- Derived work emails: [off: published addresses only] / on, for hiring people at companies worth the effort, when the company's address pattern is evidenced by at least one real published address on the same domain (or the company's own careers@/jobs@ alias), and the person is confirmed at the company. No paid lookup tools, no SMTP probing, no personal emails; evidence goes in `people.notes`; a bounce marks the address bad and variants are never retried.
- Batches: [scheduled for the recipients' morning, a few minutes apart] / sent as soon as reviewed
- From address: only the application email in `me/profile.md`; never a current-employer account

## Replies to people who write back
Recruiters, referrers, hiring managers, interview scheduling, offers and salary questions:
- [drafted for the user] / handled by the agent: all, or which ones (e.g. "confirm interview slots if the calendar is free")

## Pace
Learned from experience. Start moderate, speed up while there are no warnings, back off when one appears. Note what happened on each site:
- (e.g. "<date>: LinkedIn showed an invitation warning after about N in a week; backed off 4 days, now keeping under M")

## Where personal details may go
- [applicant portals for roles on the shortlist; job sites they're logged in to; the email connector]
- Anything else they add:

## History
- <date>: <what changed, and why>
