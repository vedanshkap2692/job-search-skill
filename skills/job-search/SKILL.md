---
name: job-search
description: Find open roles that fit the user, check they're still open, save the full JD and score fit. Also fills in details for job links the user pastes and roles from job-alert emails. Use on a schedule, when the user asks for jobs, or when they share a link.
---

# Job search

The goal is a steady flow of open, well-matched roles in the ledger, each with enough detail to decide on and tailor for. The user's targets and filters are in `me/profile.md`.

## Each run

1. **Know what's there.** Read the ledger's job URLs, and company + title + location, so nothing is added twice.
2. **Search broadly, and differently each run.** Rotate titles × locations × sources so runs don't keep finding the same jobs. Sources are in [playbooks/job-sources.md](../../playbooks/job-sources.md); ask the user which sites matter in their market. Use the browser for LinkedIn and sites that need it, and web search or public job-board feeds for the rest.
3. **Open each posting and check it's open:**
   - no "no longer accepting applications", no 404, no redirect to the careers page;
   - posted within about 30 days (prefer the last 14).

   Skip anything you can't confirm.
4. **Read the real posting, not the repost.** A LinkedIn or aggregator listing is often a repost that drops or changes the experience range, pay and location that the company's own ATS posting states. Before scoring fit or applying, follow the apply link to the underlying posting (Greenhouse, Lever, Workday, the staffing firm's own form) and take the requirements from there. Reposts have advertised "1–2 years" for roles whose ATS page says "3–7 years".
5. **Save the full JD** to `data/jds/<company>-<role>.md`, as fetched, not summarised. Tailoring works from this. Note the fit reasoning and any apply-channel details at the bottom.
6. **Add it to the ledger:** company, title, URL, location, mode, family, experience asked, pay (only if stated), source, posted, fit, `fit_why`, must-haves (up to six, short) and `jd_path`. Status "new".
7. **Log** what was added: counts by family, and the two or three best to act on first.

How many per run is up to the user. A good default is 10–20 new roles per run when the market has them.

## Shortlisting

A job moves from "new" to "shortlisted" when it's picked to apply to. That's the user's pick by default: show the best new roles and ask. If `me/permissions.md` hands shortlisting over (say, fits of 4 and above), shortlist those yourself as you add them. [apply](../apply/SKILL.md) and [outreach](../outreach/SKILL.md) work from the shortlist.

## Fit, 1 to 5

Judged against the role family, using `me/profile.md` and `me/master_resume.md`:
- **5:** title, level and core skills match well;
- **4:** a good match, with a gap or two;
- **3:** a reasonable stretch;
- **2 and below:** in scope but weak.

`fit_why` is one line: what the role centres on, what in their background maps to it, and the main gap ("Centres on LLM evaluation; maps to their document-AI work; gap: no Spark").

## Filters

Defaults, which the user can change under "Filters" in `me/profile.md`. Apply them to what the underlying posting says, not the repost. Treat the user's filter lines as hard rules once written: a run that "just this once" stretches them wastes a tailored resume on a role that will bounce at the first screen.
- **Seniority:**
  - asks up to about a year more than they have: in scope;
  - asks one to two years more: a stretch (apply, but no outreach);
  - asks more than that, or a much more senior title: skip.

  Some users set a hard line instead ("minimum ask ≤ N years, no stretches"); then follow it exactly. "N+" with no upper bound passes a "≤ N" line; "N.5+" does not.
- **Pay:** skip roles whose stated range tops out below their floor (the "Lowest acceptable pay" under Filters). Most postings state none; then judge by company and level — only a *stated* range below the floor is a skip.
- **Availability:** a posting that demands "immediate joiners only" is a likely skip when the user has a notice period; flag it rather than silently applying.
- **Their exclusions and deal-breakers:** role types, industries, companies (always including their current employer), locations.
- **Keep the weaker fits:** log every in-scope role, with a lower score rather than dropping it, unless the user prefers a tight list. When many jobs are waiting unreviewed, add only strong fits until the backlog comes down.

Log every skip with its reason in `data/log.md`, so the user can widen a filter that's costing them roles.

## Links the user pastes

Fill in the same fields. If the page needs a login or shows only a summary, open it in the browser, or find the same posting on a public page (the company's own careers site). If nothing works, add it with what you have and say so.

## Job-alert emails

[inbox](../inbox/SKILL.md) hands over roles from alert emails. Check each is open and fits before adding it.

## Housekeeping

Every few days, re-check jobs that have sat at "new" for more than about ten days. Mark closed ones "closed", with the date. Touch only jobs still at "new". Roles that were parked for a missing apply channel ("no working form today") are worth rechecking weekly.

## Tell the user

A short list per run: company, role, location, fit. Lead with the best few and say why.
