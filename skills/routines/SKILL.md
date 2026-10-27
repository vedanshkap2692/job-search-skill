---
name: routines
description: Set up scheduled runs on the user's platform (morning, outreach-and-apply, evening, job search, review), define what each run does, and pause or change them. Use during onboarding, or when the user wants a schedule added, changed or paused.
---

# Routines

Routines keep the work going while the user does other things. Each one is a fresh agent session, started on a schedule with a short prompt.

## Setting one up

Use whatever scheduler the user's agent has, and explain it in plain words:
- **A local scheduler** is the best fit, because runs can use the logged-in browser and the files in this folder. For example: scheduled tasks in the agent's desktop app (Claude Code's desktop app has them), or cron or launchd running the agent's headless mode from this folder (`claude -p "<prompt>"`, `codex exec "<prompt>"`).
- **Cloud schedules** (some agents offer routines that run on their servers) can't use the browser on the user's computer, and can't see `me/` or `data/` unless those are synced somewhere private. They suit searching and drafting at most.

Then:
- Tell them plainly that runs which use the browser need the computer awake and the browser open.
- **Do a test run** right away, while they're here, so approval prompts and missing tools show up now and not at 8am. Fix what stalls ([playbooks/unattended-runs.md](../../playbooks/unattended-runs.md)).
- Show them where to see, pause and change each run.
- Note in `me/profile.md` (Accounts and tools) which runs exist, when, and where.

## The prompt

Keep it short; the skills hold the detail.
```
You're running the <name> routine for the job search assistant in <path to this folder>.
Read AGENTS.md, then the "<name>" section of skills/routines/SKILL.md, and do it.
Nobody is watching this run: never wait for input. Put anything that needs the user in the needs-you queue.
<the unattended-run rules from playbooks/unattended-runs.md, if this platform needs them>
```

## Every run starts and ends the same way

**Start:**
1. Read `me/permissions.md`. If its Status is "paused", log that and stop.
2. Insert a row in `runs` (what, `started_at`), and keep its id.
3. Read `me/style.md` and the last few days of `data/log.md`.

**End:**
1. Update the `runs` row: `ended_at`, summary (counts), warnings.
2. Add a few lines to `data/log.md` and any new needs-you items.
3. Run `python3 ui/build.py`.
4. Finish with a short message: what needs the user first, then counts.

## The runs

### morning
[inbox](../inbox/SKILL.md), then [job-search](../job-search/SKILL.md). New interviews and replies reach the user before their day starts, and the list of new roles is fresh. Everyone gets this one.

### outreach-and-apply
[apply](../apply/SKILL.md) for shortlisted and ready jobs, then [outreach](../outreach/SKILL.md) for them: new people, messages to people who accepted, and follow-ups that are due. Both follow `me/permissions.md` exactly, so with nothing handed over this run prepares and drafts. Set it up as soon as the user hands over any sending or submitting; it's what sends the post-accept messages and follow-ups.

### evening
[inbox](../inbox/SKILL.md) again, then a short summary of the day: what went out, what came in, what needs them tomorrow.

### job-search
[job-search](../job-search/SKILL.md) on its own, for extra searches when the market is busy.

### review
Every week or two: the results review, then the setup review, from [review](../review/SKILL.md). It ends with suggestions for the user, not changes.

A good start is morning, plus outreach-and-apply once a day if they've handed anything over. Add more as their pace grows; how many and when is their call.

## Nobody is watching

- Never stall on a question: queue it as a needs-you item and carry on with the rest.
- Approval prompts stop unattended runs dead. Avoid the commands that trigger them, or agree a narrow allowlist with the user ([playbooks/unattended-runs.md](../../playbooks/unattended-runs.md)).
- If the browser isn't available, do what doesn't need it, and say what was skipped.
- If a site shows a warning, stop sending on that site for the rest of the run and record it under Pace.

## Pausing and changing

- **Pause:** set Status to "paused" in `me/permissions.md`; that works on any platform. Disable the schedules too if they'd rather not use up runs.
- **Resume:** set Status back to "active".
- **Change:** update the schedule in the scheduler and in `me/profile.md`. Log every change in `data/log.md`.
