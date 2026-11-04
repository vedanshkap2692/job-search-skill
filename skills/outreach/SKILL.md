---
name: outreach
description: Find people who can refer the user or pass their application on, and write connection notes, messages and follow-ups in the user's voice; send them if the user has handed that over. Use after a job is shortlisted or applied to, and for follow-ups.
---

# Outreach

A referral or a word from someone on the team does more than any resume tweak. This skill finds the right two or three people per role, writes to them the way the user would, and follows up once or twice. Use it in good faith: write to people because they're relevant to the role, not because they work there. That's the difference between outreach and spam. Recommend this to the user; how they use it is their call.

## Sending

You can send these yourself. Until the user has handed sending over in `me/permissions.md`, offer to, and recommend they read the first few before you do. Until then, each one goes in the needs-you queue as a draft (kind `review`): the profile link and the text, ready to paste. Once they've handed it over, send at the pace you've learned for their account.

Work from jobs that are shortlisted, ready or applied ([job-search](../job-search/SKILL.md), "Shortlisting"). A referral helps most when it arrives with, or just after, the application.

Before every send:
1. **Pace:** read Pace in `me/permissions.md` and `state.linkedin_invite_limit_hit_at`. During a cool-off, draft instead of sending invitations.
2. **Live page:** "Pending" on the profile means the invitation already went. For an existing connection, read the whole thread.
3. **Ledger:** check for anyone at that company already contacted.
4. Send, then record the person (`people`) and the message (`messages`).

## Who

- **Order:** their existing connections at the company first (read the old thread and mention past contact honestly), then alumni and former colleagues, people on the team, the team's manager, and a recruiter.
- **How many:** two or three per role. On a big team, several people of the same type is fine.
- **Prefer people who are there now:** their current title shows the company.
- **Finding them:** LinkedIn people search in the browser, filtered by current company, plus the user's school for alumni and network degree for existing connections. Otherwise, web search of public profiles (`site:linkedin.com/in "<company>" "<team or title>"`).
- **Never collect** personal phone numbers or personal email addresses.

## Defaults (the user can change any of these)

- **One thread per person.** If two roles fit, mention both in one message rather than starting two conversations. Follow-ups go in the same thread.
- **Don't flood a company.** If several people there have pending invitations and no replies, wait about a week before adding more.
- **Stretch roles** (see [job-search](../job-search/SKILL.md), "Filters"): apply, but don't reach out.
- **Pace:** learned from experience and kept under Pace in `me/permissions.md`; see [playbooks/linkedin.md](../../playbooks/linkedin.md). Spread sends through the day, and cool off at any warning.

## The ask, by person

Keep the ask small: something they can do in 30 seconds.
- **Alum or peer on the team:** ask for a referral directly. "Would you be open to referring me?"
- **Manager or senior leader:** don't ask for a referral or a call. "Could you take a look, or pass it to whoever is hiring?"
- **Recruiter:** give years of experience and when they can join. "Could you check if I'm a fit, or put me forward?" If two roles fit, lead with the better one and ask to be considered for whichever suits.
- **A short call:** only with someone they already know, or when the person offers.

## Shapes

`me/style.md` overrides these.
- **Connection note,** within the site's limit (300 characters on LinkedIn Premium; free accounts get fewer notes, and shorter ones):
  - the role, and "applied" or "applying" (only "applied" if it was);
  - one line on the scope of their work, in the JD's terms;
  - the ask.

  No numbers or tool lists in a note this short. On a free account with no notes left, send the invitation bare and put all of this in the first message after they accept.
- **Message** (to an existing connection, InMail, email): three to five short sentences. The role; two or three areas of expertise in the JD's terms; one or two impact numbers from the bank; the ask.
- **After they accept:** wait about two days. If they haven't written, send two or three sentences:
  - thanks;
  - the role, with the job link (people often accept on their phone without reading the note);
  - one impact point that's new to them;
  - a light ask ("happy to send my resume if that makes it easier to pass along").
- **Follow-up:** after about three days without a reply, one or two sentences with a new angle, in the same thread. Two per person by default (the number in `me/permissions.md` wins). An invitation that's still pending can't be followed up.

## Sound like a person

- Match the other person's length, tone and formality, especially in replies: a one-word "Sure" gets a short, casual answer.
- Vary the wording every time. A batch of near-identical notes reads as automated, to people and to LinkedIn.
- No flattery, no "I hope this finds you well", no stacked claims, no implementation detail, no internal names.
- Mention a shared school or past employer only when it's true.

## Examples

These show the shape; don't copy the wording.
- **Alum, note:** "Hi Sam, fellow <school> alum here. I've applied for the Data Scientist role on your team at <company>. My work spans forecasting, experimentation and NLP for marketplace pricing. Would you be open to referring me?"
- **Manager, note:** "Hi Priya, I'm applying for the ML Engineer role at <company>. Most of my work has been production NLP and document extraction, with the evaluation around it. Could you take a look at my profile, or pass it to whoever is hiring?"
- **After accepting:** "Thanks for connecting, Sam! Here's the posting: <link>. The closest thing I've built to your team's work is a document pipeline that now handles 95% of invoices without manual entry. Happy to send my resume if that helps."

## Email outreach

Cold email reaches people who don't check LinkedIn, and it's worth offering once LinkedIn outreach is working. It's off until the user turns it on; once on, [cold-email](../cold-email/SKILL.md) covers finding postings that name an address and the sending rules. Finding addresses is the hard part: use only work emails that are published (a team page, a talk, a commit) or shown by an email-finder tool the user installs for that. Don't guess addresses: guesses bounce, and bounces get the user's email flagged as spam. (If the user allows derived work emails in `me/permissions.md`, the evidence rules in cold-email apply.) Use the same shapes as messages, one email per person, and follow up at most once or twice in the same thread.

## Records and reporting

- `people`: status goes found → invited → connected → messaged → replied or referred (or no_reply after the last follow-up). Set `connected_at` when they accept.
- `messages`: one row per note, message and follow-up, drafted or sent, with `follow_up_due`.
- Tell the user: who was contacted for which role, what was sent or is waiting as a draft, and any warnings from the site.
