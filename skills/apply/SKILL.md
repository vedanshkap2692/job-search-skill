---
name: apply
description: Fill in job applications with the right resume and the user's standard answers, and submit them if the user has handed that over. Use when jobs are ready to apply to, on a schedule or on request.
---

# Apply

Filling in even ten applications a day by hand is exhausting. This skill does the form work: it opens each application, fills it in from what the user has told you, attaches the right resume, and submits it, or leaves it one click from done.

## Submitting

You can submit applications yourself. Until the user has handed that over in `me/permissions.md`, offer to, and recommend they check the first few you've filled in before you do. Until then, fill each one up to the last step, leave the tab open for them, and add a needs-you item of kind `review`. Keep that to a handful of open tabs ([playbooks/browser.md](../../playbooks/browser.md)).

Even with submitting handed over, some forms end at a CAPTCHA. You never solve those: fill everything, verify it, leave the tab open at the CAPTCHA, and queue a needs-you item saying it's one click (CAPTCHA + Submit) from done.

## Picking what to apply to

- **Which jobs:** status "ready" first (resume done and reviewed), then "shortlisted" (prepare them below). Jobs at "new" aren't picked to apply to yet; see [job-search](../job-search/SKILL.md), "Shortlisting".
- **Order:** best fit first, then the freshest posting. Portals that rarely need a login (LinkedIn Easy Apply, Greenhouse, Lever, Ashby and similar) before ones that usually do (Workday, Taleo, Oracle).
- **Jump the queue:** jobs where someone has already been contacted, so the referral has an application to point to.
- **Check before preparing:**
  - not already applied: no applied job in the ledger with the same company and title, and no "you've already applied" notice on the portal;
  - still open — on the company's own posting, not just the aggregator's copy;
  - the real requirements: a LinkedIn or aggregator repost often hides the experience range and pay that the underlying ATS posting states. Open the actual apply destination before deciding; more than one "1–2 years" repost has turned out to be "3–7 years" on the company's own page;
  - experience asked and stated pay pass the user's filters in `me/profile.md`;
  - under the per-company limit in `me/permissions.md`, if they set one;
  - the portal's own cap on applications per candidate, if any (check the ledger for recent applications there).
- **Easy Apply and one-click applies** (LinkedIn Easy Apply, job boards' quick-apply) are convenient but opaque: the user never sees what the company receives, and recruiters often weigh them less. When the same role is open on the company's own portal or a direct form, prefer that — or do both, if the user has chosen a double-apply rule in `me/permissions.md`. One-click applies on job boards send the board's **profile resume**, not today's tailored one: check what's on the profile first, and changing it is an account change that needs the user's OK.
- **Volume** is up to the user. Recommend tailored applications to good fits over mass applications to weak ones: recruiters notice the second kind. If they turn on volume mode in `me/permissions.md`, apply to every role that passes the hard filters, reusing a reviewed resume below their tailoring line; the review and the Never rules still hold.
- **Same day for strong fits.** Postings close fast, sometimes within a day or two of appearing. Don't let a strong fit sit in the queue overnight, and recheck it's still open right before submitting.

## Preparing

Set the job to "preparing".
1. **Folder:** every application gets `me/resumes/<company>-<role>/` with a `notes.md`, even when it uses a base resume, so there's one record of what was sent where. Set `jobs.folder`.
2. **Resume:** tailored for this job ([resumes](../resumes/SKILL.md)), or the base resume for its family if `me/permissions.md` says so for this fit level.
3. **Answers:** from `me/profile.md` ("Standard form answers"), the job's `notes.md` and `me/master_resume.md`.
4. **Review:** an independent blind check of the resume and any free-text answers ([review](../review/SKILL.md)). Once it passes, the job is "ready".

## Filling in

- Open the apply page in its own tab. Personal details go only to the kinds of sites listed under "Where personal details may go" in `me/permissions.md`. If the apply link leads somewhere else (an unfamiliar site asking for documents or payment), stop and ask.
- Fill every field from the answers above. Free-text answers are short and plain, in the JD's terms; oddly specific detail reads as AI-written. Numbers only in numeric fields.
- Upload the job's resume, then check it's the file attached and not an older one.
- Check every field after setting it. Autofill and resume parsing often get names, dates and locations wrong; prefilled "saved answers" from past applications can be stale or overstated — re-check every number against `me/master_resume.md`.
- Tick required terms and privacy boxes only. Leave marketing, newsletter, SMS, talent-community and job-alert opt-ins unticked, and "follow this company" boxes too, unless the user wants them. "Information is true" attestations and typed-name signatures follow "Consents and attestations" in `me/permissions.md`: left for the user by default, and even when handed over, only on a form where every answer came from the user's own facts. Leave voluntary demographic (EEO) questions blank or "prefer not to say", per the profile.
- Quirks of specific portals: [playbooks/application-forms.md](../../playbooks/application-forms.md). Add new ones you learn.

## Screener questions

Forms ask about experience, pay and availability in ways the profile doesn't always match word for word. The rules:
- **Experience buckets with no honest option:** pick on a consistent, defensible basis and use the same basis everywhere. A common one: cumulative hands-on time with that skill across jobs, internships and substantial research work — not calendar time since first touching it, and never a bucket above what the resume's own dates can support. Record the basis in `me/profile.md` so every application answers alike.
- **"Years of experience with X":** answer from `me/master_resume.md`, not from what would look good. A skill on the "not claimed" list gets 0 or "no experience", even when the form makes that look disqualifying.
- **Numeric-only pay fields:** digits only, in the form's unit. When a field rejects decimals, round the user's number **down**, never up (understating current pay is safe; overstating is a lie).
- **Notice period:** use the user's standard phrasing from the profile (for example "30 days from written offer confirmation"), shortened honestly when the field is a dropdown.
- **Knowledge or logic screeners** (a statistics question, a "which of these is true" trap): answer honestly from what the user actually knows, even when the honest answer looks worse. These questions are often designed so the flattering answer is the wrong one.
- A required question you can't answer honestly from what you have: stop, queue it for the user (kind `question`), and don't guess.

## Verify before submitting

Mistakes cluster at the end, after a long form has shifted under you:
- **Re-verify every field** by reading the page (or zooming a screenshot) just before submit, not from memory of having set it.
- **Radio buttons and dropdowns after long text:** filling a big textarea can reflow the page so later clicks landed on the wrong option. After any long answer, re-check every radio and dropdown below it.
- **The attachment:** confirm the file name on the page is this job's resume.
- **Counts and units:** pay in the right unit, phone without stray characters, the right city.

## When to stop and hand it to the user

- A login, account creation, one-time code or CAPTCHA.
- A required question you can't answer honestly from what you have.
- A file that won't attach.

Set the job to `needs_user`, write the blocker, and add a needs-you item with the apply link and what's needed: kind `login` for sign-ins, `question` for questions. Group sign-ins by portal so they can clear several in one sitting. Once they've signed in, the session usually stays open in the browser, so check again on the next run before queueing it a second time.

## After submitting

- Confirm that the confirmation page or message appeared. If it didn't, it wasn't submitted — say so.
- Record status "applied", `applied_at` and `resume_path` in the ledger, and the portal in the job's `notes.md`.
- Save any new question and the answer you gave to the job's `notes.md`. Add questions that keep coming up to "Anything else forms keep asking" in `me/profile.md`, so the next form is quicker.
- Close the tab.

## Tell the user

Submitted (company, role, tailored or base), waiting at the last step for them, blocked (grouped by portal), skipped (with the reason).
