# Job radar

Scans the public job feeds of about 120 companies in one go and lists the roles that pass your filters:
- the title matches one of your role families (or a broad title whose JD has enough of your terms);
- the location is one of yours, or remote and open to you;
- the experience minimum stated in the JD is within your limit, or none is stated;
- it was posted within your freshness window, when the feed gives a date;
- the employer isn't on your skip list (your current employer, always);
- it isn't already in `data/ledger.db` (the radar reads the ledger and never writes to it).

The radar never logs in, applies, emails or writes to the ledger. It only reads the same public JSON that each company's careers page reads.

## Setup

Needs Python 3.9+. From the repo root:

```sh
cd scripts/job_radar
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m playwright install chromium   # only needed for the Eightfold portals
```

The virtualenv stays in this folder (gitignored); system Python isn't touched. Playwright keeps Chromium in its own shared cache.

## Your filters

Filters live in `me/radar.yaml`, which is yours and gitignored. Start from the example:

```sh
cp scripts/job_radar/filters.example.yaml me/radar.yaml
```

The agent writes it for you from `me/profile.md` (Targets and Filters) during onboarding or the first radar run, and keeps the two in step when the profile changes. If `me/radar.yaml` doesn't exist, the radar uses the example, which searches early-career software, data and ML roles anywhere.

What's in it (every field is explained in [filters.example.yaml](filters.example.yaml)):
- `locations`, `location_codes`, `remote_ok`, `remote_jd_words`, `remote_exclude_words`: where;
- `smartrecruiters_country`, `amazon_country`, `workday_location`, `eightfold_location`: server-side country hints, so those feeds return less;
- `search_queries`: keywords for the feeds that can only be searched (Workday, amazon.jobs, Eightfold);
- `families`, `check_jd`, `jd_terms`, `exclude_titles`: which titles count;
- `exclude_companies`: employers to skip;
- `max_required_years`, `degree`: the experience line ("minimum ask ≤ N years");
- `fit_terms`, `core_terms`, `flags`: the fit hint, built from your fact bank.

## Run it

From `scripts/job_radar`:

```sh
.venv/bin/python radar.py                  # full run, a few minutes
.venv/bin/python radar.py --no-browser     # skip the Playwright portals
.venv/bin/python radar.py --only ashby,lever --days 30
.venv/bin/python radar.py --config path/to/other.yaml
.venv/bin/python radar.py --verify         # check that every company in companies.yaml still returns jobs
```

Output goes to `data/radar/`:
- `radar-<date>.md`: the keeps, ranked by a rough fit hint, then drop counts by reason and any feeds that failed;
- `radar-<date>.csv`: the same keeps, with columns company, title, location, experience, posted, url, ats, fit_hint;
- `radar-<date>.audit.jsonl`: every in-scope title, kept or dropped, with the reason. Use it to check the experience parser, for example to see which roles were dropped as too senior.

Running it again on the same day overwrites that day's files.

## What the agent does with it

The radar finds candidates; it doesn't decide. For each keep worth a look, the agent opens the posting, confirms it's open and that the experience line really passes, saves the JD and adds it to the ledger per [skills/job-search](../../skills/job-search/SKILL.md). Postings at these companies fill fast and some close within days, so apply to strong keeps the same day.

## Sources

| Kind | Endpoint | Notes |
|---|---|---|
| greenhouse | `boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true` | Full JD in the list |
| lever | `api.lever.co/v0/postings/<slug>?mode=json` | Full JD in the list |
| ashby | `api.ashbyhq.com/posting-api/job-board/<slug>` | Full JD in the list |
| smartrecruiters | `api.smartrecruiters.com/v1/companies/<slug>/postings?country=<cc>` | JD fetched per posting, only for title and location matches |
| workable | `apply.workable.com/api/v1/widget/accounts/<slug>?details=true` | Supported; rate-limits hard (429), so keep the list short |
| rippling | `api.rippling.com/platform/api/ats/v1/board/<slug>/jobs` | JD fetched per posting |
| workday | `POST https://<host>/wday/cxs/<tenant>/<site>/jobs` | Keyword searches. JD fetched per match. Some tenants refuse with 422 or fail with 502 now and then. |
| amazon | `www.amazon.jobs/en/search.json` | Only the basic qualifications are parsed for years, so a preferred "5+ years" doesn't drop a role |
| eightfold (Playwright) | `/api/pcsx/search` and `/api/pcsx/position_details`, called from inside the public careers page | Returns 403 to plain HTTP. Playwright opens the page headless and calls the same endpoint the page itself calls. |

Playwright is used only for the Eightfold portals. Sites behind a bot challenge (a Cloudflare "Just a moment…" page and the like) are deliberately skipped: getting past one is circumvention. LinkedIn, job boards that need a login, and anything else behind a login are out of scope.

## Add a company

Find its job-board URL and add one line to `companies.yaml` under the matching kind:

```yaml
greenhouse:
  - {slug: "databricks", name: "Databricks"}          # job-boards.greenhouse.io/databricks
workday:
  - {name: "Visa", host: "visa.wd5.myworkdayjobs.com", tenant: "visa", site: "Visa"}   # https://<host>/en-US/<site>
```

Then run `--verify`. A short slug can belong to an unrelated namesake, so open the board once and check it's the company you mean. Use the same company name as the ledger, so the dedupe can match on company plus title. The list that ships is a starting point: add the companies you'd most like to work at, and drop ones that don't hire where you are.

## How the filters work, and where they go wrong

- **Experience** (`filters.parse_experience`):
  - It finds "1-3 years", "2+ years", "minimum 2 years" and "3 years of experience", including spelled-out numbers.
  - It ignores mentions under a "Preferred / Nice to have" heading, or marked "preferred" or "a plus" inline.
  - The binding minimum is the largest required one.
  - In "Bachelor's + 3 years, or Master's + 1 year", the figure after your degree (`degree`) counts.

  It's a regex, so always open the posting and confirm before applying. "not stated (only in preferred: …)" means the only years found were in the preferred section.
- **Titles**: `exclude_titles` runs first, then `families` in order, then `check_jd`. A `check_jd` title is kept only when the JD has at least `min_jd_hits` matches of `jd_terms`.
- **Fit hint**: the family, then strong/good/weak by how many of your `fit_terms` appear in the JD (core terms count double), then any `flags` and the terms that matched. It's a sorting aid, not a fit score for the ledger.
- **Dedupe**: an exact URL match (ignoring query strings and Workday's `/en-US/`), the same job ID in the URL, or the same company plus title as a ledger row.
