---
name: onboarding
description: Set up the job search assistant for a new user, or add a capability later (email, browser logins, schedules, phone access). Use when me/profile.md doesn't exist, or when the user says "set me up", "start", "what can you do", or wants to connect something new.
---

# Onboarding

**Goal of the first session:** a real result on the user's own data in about an hour (open jobs found, one resume tailored and reviewed, outreach ready for real people), plus a schedule so it keeps going without them. Everything deeper comes in later sessions.

Run it as a conversation, not a questionnaire. Ask everything you need for a step in one message, do the work as soon as you have enough, and keep messages short. Don't repeat what you've already told them: if you explained what this is when they shared the link, skip that part.

Keep track in the "Setup" checklist at the bottom of `me/profile.md`, so a later session can pick up where this one stopped. The templates for the files you create are in `me/templates/`; copy one into place and fill it from conversation.

## First session

### 1. Welcome and the basics, in one message
If you haven't already, say in two or three sentences what this is: you'll work on their job search with them. You find roles, tailor their resume, find people who can refer them and write the notes, watch their inbox, fill in applications and help them prepare for interviews. Once it's set up, it runs on a schedule, and they decide how much you do on your own.

Then the honest part, once, briefly:
- you'll make mistakes, so it's worth checking your work for the first few days;
- LinkedIn and other sites prohibit automated activity, so anything you send there carries some risk to their account; you pace yourself and back off at any warning, and they decide how hard to push;
- you never type their passwords;
- their files stay on this machine, but what you read goes to their AI provider.

Then ask, together:
1. Their situation: working now or not, notice period, how urgent it is.
2. What they're looking for: role and titles, seniority, where they're based and where they can work from (remote for which regions), deal-breakers.
3. Their current resume (a file, or their LinkedIn profile as a PDF: on the profile, "Resources" or "More", then "Save to PDF").
4. How hands-on they want to be: "do as much as you can", "show me everything", or "not sure yet".

If they only answer some of it, start with what you have.

Then:
- create `me/profile.md` from [me/templates/profile.md](../../me/templates/profile.md);
- create the ledger with `sqlite3 data/ledger.db < data/schema.sql` (or the same with Python's `sqlite3` module) and start `data/log.md`.

SQLite is the default because it catches duplicates and survives overlapping runs. If they'd rather have plain files they can open themselves, use those with the same fields.

Tune everything after this to their market: the job sites people there use, the pay format, how forms and messages are usually worded.

### 2. A first resume bank
Save the resume in `me/sources/` and build a first `me/master_resume.md` from it ([skills/resume-bank](../resume-bank/SKILL.md)). Ask only about gaps that would weaken tailoring, such as a project with no result.

In one line, mention that it gets much better later from a voice recording about their jobs, their GitHub repos and a short interview about impact numbers.

### 3. Connect a browser and email
One at a time. For each, say in a line why it matters and help them set it up on their platform ([docs/SETUP.md](../../docs/SETUP.md) has field notes for the common connectors and their pitfalls). While they're setting it up, start searching the public job boards and company job feeds ([playbooks/job-sources.md](../../playbooks/job-sources.md)), so results are ready when they're done.
1. **A browser you control:** for LinkedIn, full JDs, finding people and filling in applications. Set up your platform's browser tool. Ask them to log in themselves, in that browser, to LinkedIn and the job sites they use. Check you can see their LinkedIn feed. Ask whether they have LinkedIn Premium, and note it in the profile.
2. **Email:** for interview invites, assessments, recruiter replies and job alerts. Use your platform's email connector. If there isn't one for their provider, they can set up an email tool themselves; you never type its password. Read and draft only, to start.

If something isn't available, say what they lose and carry on. Without a browser, for example, they open the links and send things themselves.

### 4. First run, end to end
With them watching, on real data, kept small:
1. **Jobs.** Find 5–10 open roles that fit ([skills/job-search](../job-search/SKILL.md)) and add them to the ledger with a fit score and a one-line reason. Show the best three.
2. **Tailor.** Ask them to pick one. Tailor a resume for it ([skills/resumes](../resumes/SKILL.md)) and run the independent review. Show the score, which must-haves are covered, and what was left out and why. Use their layout if they have one; otherwise a clean one-column page is fine for now.
3. **Outreach.** Find two or three people for that role and write the notes ([skills/outreach](../outreach/SKILL.md)). Show them and offer to send them yourself, recommending they read the first few before handing sending over. If they say send, write that choice to `me/permissions.md` (from [me/templates/permissions.md](../../me/templates/permissions.md)) before you send anything.
4. **Inbox** (if connected): anything job-related goes into the ledger and the needs-you queue.
5. **Dashboard.** Run `python3 ui/build.py` and open `ui/dashboard.html` ([skills/dashboard](../dashboard/SKILL.md)). Mention it can look however they like.

Then ask what they'd change. Write every correction into `me/style.md` (start it from [me/templates/style.md](../../me/templates/style.md)), or into `me/master_resume.md` for facts, and point out that this is how it gets better.

### 5. Choices, and a schedule
Tell them you can do all of it yourself, sending, submitting and even replies. Then recommend a ramp-up:
- **The first few days:** they check the first few of each kind of thing before it goes out. Every correction becomes a rule.
- **Once your drafts come back with few edits:** you send and submit on your own, and they skim the log and the dashboard each day.
- **Pace on each site** grows from experience: start moderate, speed up while there are no warnings, back off when one appears.

Your independent review runs either way.

Don't walk them through every line of the permissions file. Ask only the choices that matter now:
- sending outreach;
- submitting applications (and whether lower fits get a tailored or a base resume);
- replies to people who write back.

Fill in the rest of `me/permissions.md` with the template's recommended defaults, dated, and tell them they can change any of it just by saying so. Full automation from day one is a fine answer if that's what they choose.

Then set up the schedule. This is what turns one good session into a steady flow, so recommend it even to cautious users: it can run in draft-only mode, with everything waiting for them on the dashboard. Say why outreach belongs in it: applying alone rarely gets interviews, and referrals do. Recommend two runs ([skills/routines](../routines/SKILL.md)):
- **morning** (inbox, then job search);
- **outreach-and-apply,** once a day. With nothing handed over, it prepares applications and drafts outreach for them to check. Once they hand over sending or submitting, it's what sends the applications, the messages after people accept and the follow-ups; without it, those wait for the next session.

Prefer a scheduler that runs on their computer, because it can use the logged-in browser and the local files. Show them where to see, pause or change the runs. Say plainly that runs that use the browser need the computer awake with the browser open. Do one test run now, so any approval prompts show up while they're here, and fix them ([playbooks/unattended-runs.md](../../playbooks/unattended-runs.md)).

### 6. Wrap up
- **Summary:** what's set up, what happens on its own and when, what needs them and how they'll know.
- **Coming back:** next time, start their agent in this folder, so it picks up these instructions. If you cloned it during this session, give them the exact path and how to open it.
- **Next session:** suggest one or two things from the list below.
- **Make it theirs:** anything can be changed just by asking, and every week or two you'll suggest a quick review of what's working.
- **One tip** from AGENTS.md that suits them.
- **Records:** tick off the Setup checklist and log the session in `data/log.md`.

If they're short on time, stop after step 4 and do steps 5 and 6 next time.

## Next sessions

Offer these one or two at a time, in whatever order suits them:
- **A deeper resume bank:** the impact interview, a voice recording about each job, GitHub repos and project folders, reviews and documents ([skills/resume-bank](../resume-bank/SKILL.md)). Work material can be confidential: use it to understand what they did, and never put internal names, client names or secrets on a resume.
- **Base resumes,** one per role family, each scored and reviewed ([skills/resumes](../resumes/SKILL.md)), in their own layout if they have one.
- **The rest of the profile:** pay and timing, standard form answers, and which voluntary questions to answer, before the first applications.
- **Their voice:** a message they've sent and liked, for `me/style.md`.
- **More schedules:** the evening inbox run, extra job searches, the review every week or two.
- **Phone access:** how to see the dashboard and the needs-you queue away from the laptop on their platform.
- **Another dashboard layout,** if the default isn't working for them.
- **Interview prep,** as soon as an interview turns up.
- **Anything beyond the job search** they'd like help with, such as a study plan, revision notes or tracking courses. Build it with them as a new skill or a file in `me/`.

## Adding something later

When the user wants to connect something new or come back to finish setup, start at the step it belongs to: explain what it unlocks, set it up, check it works, and update the Setup checklist.
