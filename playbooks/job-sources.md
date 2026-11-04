# Where to find jobs

## Anywhere
- **LinkedIn Jobs,** with the filters in [linkedin.md](linkedin.md).
- **Company career pages.** Many companies post through an applicant system with a public feed that needs no login:
  - Greenhouse: `https://boards-api.greenhouse.io/v1/boards/<company>/jobs?content=true`
  - Lever: `https://api.lever.co/v0/postings/<company>?mode=json`
  - Ashby: `https://api.ashbyhq.com/posting-api/job-board/<company>`
  - SmartRecruiters: `https://api.smartrecruiters.com/v1/companies/<company>/postings?country=<cc>` (JD per posting at the `ref` URL)
  - Workable: `https://apply.workable.com/api/v1/widget/accounts/<company>?details=true` (rate-limits hard)
  - Rippling: `https://api.rippling.com/platform/api/ats/v1/board/<company>/jobs`
  - Workday: `POST https://<host>/wday/cxs/<tenant>/<site>/jobs` with `{"searchText": "...", "limit": 20, "offset": 0, "appliedFacets": {}}`; host and site come from the careers URL `https://<host>/en-US/<site>`
  - amazon.jobs: `https://www.amazon.jobs/en/search.json?base_query=<q>&country=<ISO-3>`

  The company name is the one in their job-board URL.
- **Job radar:** [scripts/job_radar/](../scripts/job_radar/README.md) scans about 120 of these feeds in one go (plus Eightfold portals via Playwright), applies the user's filters from `me/radar.yaml`, skips what's already in the ledger and writes `data/radar/radar-<date>.md`. A good first step for a scheduled job-search run once it's set up.
- **Finding more company boards:** public multi-ATS dumps (for example the job-board-data project, built from Common Crawl) list thousands of Greenhouse, Lever, Ashby and Workday slugs, refreshed daily. Use them to find companies to add to the radar, not as a job feed: they have no experience field, and being in the dump doesn't prove a job is still open. Check each dataset's license before reusing it.
- **Web search with site filters:** `site:boards.greenhouse.io`, `site:job-boards.greenhouse.io`, `site:jobs.lever.co`, `site:jobs.ashbyhq.com`, `site:myworkdayjobs.com`, plus title and location.
- **Startups:** Wellfound, YC's Work at a Startup, and Hacker News's monthly "Who is hiring?" thread.
- **Remote:** Himalayas (a documented public API, with country and seniority filters), We Work Remotely, Remote OK. The free remote feeds are small and lean US/EU.
- **New-grad lists (US):** community GitHub repos of new-grad and internship postings (SimplifyJobs and similar) are updated daily. They're almost all US roles; filter "India" matches carefully ("Indianapolis").
- **People posting roles:** LinkedIn posts that say "hiring" (search posts, not jobs), alumni groups, community Slacks and Discords.

## By region
- **India:** Naukri, Instahyre, Cutshort, Hirist, foundit, Wellfound's India pages. Hirist states exact minimum and maximum years on each posting, which makes vetting fast. Public Telegram job channels (read at `t.me/s/<channel>`) post fresh roles with links to company portals; quality varies a lot by channel.
- **Elsewhere:** Indeed, Welcome to the Jungle (formerly Otta), Built In, levels.fyi's job pages, and local boards. Ask the user which ones they use.

## What not to automate
- Respect each site's terms and robots.txt. Several boards ban scraping in their terms (Wellfound, for one) or block AI agents in robots.txt (Naukri, foundit). Use those by hand in the user's browser, or through their email alerts.
- Sites that answer scripts with a bot challenge (a Cloudflare "Just a moment…" page, a 403) stay browser-only. Getting past a challenge is circumvention.
- LinkedIn: never scrape. Use its email alerts and normal browsing.
- Aggregators that copy postings (and many lesser-known "AI jobs" sites) are fine for finding leads. Confirm every lead on the company's own portal before scoring or applying.
- Career pages built on JavaScript-only portals (Darwinbox, Keka and similar) have no feed. A page-change monitor (changedetection.io, open source) can watch them if the user wants.

## Is it still open?
- Closed signs: "no longer accepting applications", "position filled", "job expired", a 404, or a redirect to the careers home page.
- Check the posted date. Prefer the last two weeks.
- Postings close fast, and a radar or alert hit can be gone within a day or two. Apply to strong fits the same day you find them, and recheck that a posting is still open just before submitting.

## Duplicates
The same job often shows up on LinkedIn, aggregators and the company site. Treat the same company, title and location as one job, and prefer the company's own apply link.
