"""Public, no-login job feeds. Each fetcher returns a list of Posting objects.

Every endpoint here is the same public JSON the company's own careers page uses.
Nothing logs in, nothing posts an application. Keep request volume low.
"""
from __future__ import annotations

import datetime as dt
import html
import re
import time
from dataclasses import dataclass, field

import requests

UA = "job-radar/0.2 (personal job search; low volume)"
TIMEOUT = 25

_session = requests.Session()
_session.headers.update({"User-Agent": UA, "Accept": "application/json"})


@dataclass
class Posting:
    company: str
    title: str
    location: str
    url: str
    ats: str
    posted: str | None = None          # ISO date (YYYY-MM-DD) or None
    description: str | None = None     # plain text, may be filled lazily
    requirements: str | None = None    # "basic qualifications" block when the feed separates it
    remote: bool = False
    extra: dict = field(default_factory=dict)  # fetcher-specific info for lazy detail fetches


def get_json(url, method="GET", retries=2, **kw):
    for attempt in range(retries + 1):
        try:
            r = _session.request(method, url, timeout=TIMEOUT, **kw)
        except requests.RequestException:
            if attempt == retries:
                raise
            time.sleep(2 * (attempt + 1))
            continue
        if r.status_code == 429 and attempt < retries:
            time.sleep(10 * (attempt + 1))
            continue
        r.raise_for_status()
        return r.json()


def html_to_text(s: str | None) -> str:
    if not s:
        return ""
    s = html.unescape(s)  # greenhouse double-escapes
    s = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</div>|</h\d>", "\n", s)
    s = re.sub(r"(?i)<li[^>]*>", "\n• ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t ]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()


def _iso_from_ms(ms):
    if not ms:
        return None
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).date().isoformat()


def _iso_from_str(s):
    if not s:
        return None
    m = re.match(r"(\d{4}-\d{2}-\d{2})", s)
    return m.group(1) if m else None


# ---------------------------------------------------------------- Greenhouse
def greenhouse(slug, name):
    j = get_json(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true")
    out = []
    for x in j.get("jobs", []):
        loc = (x.get("location") or {}).get("name") or ""
        offices = ", ".join(o.get("name", "") for o in x.get("offices", []) if o.get("name"))
        out.append(Posting(
            company=name, title=x.get("title", "").strip(), location=" | ".join(filter(None, [loc, offices])),
            url=x.get("absolute_url", ""), ats="greenhouse",
            posted=_iso_from_str(x.get("first_published") or x.get("updated_at")),
            description=html_to_text(x.get("content")),
        ))
    return out


# ---------------------------------------------------------------- Lever
def lever(slug, name):
    j = get_json(f"https://api.lever.co/v0/postings/{slug}?mode=json")
    out = []
    for x in j if isinstance(j, list) else []:
        cats = x.get("categories") or {}
        locs = cats.get("allLocations") or [cats.get("location") or ""]
        parts = [x.get("descriptionPlain") or ""]
        for lst in x.get("lists", []):
            parts.append(lst.get("text", ""))
            parts.append(html_to_text(lst.get("content", "")))
        parts.append(x.get("additionalPlain") or "")
        out.append(Posting(
            company=name, title=x.get("text", "").strip(), location=" | ".join(filter(None, locs)),
            url=x.get("hostedUrl", ""), ats="lever", posted=_iso_from_ms(x.get("createdAt")),
            description="\n".join(parts), remote=(x.get("workplaceType") == "remote"),
        ))
    return out


# ---------------------------------------------------------------- Ashby
def ashby(slug, name):
    j = get_json(f"https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=false")
    out = []
    for x in j.get("jobs", []):
        if x.get("isListed") is False:
            continue
        locs = [x.get("location") or ""] + [s.get("location", "") for s in x.get("secondaryLocations", []) or []]
        country = ((x.get("address") or {}).get("postalAddress") or {}).get("addressCountry") or ""
        out.append(Posting(
            company=name, title=x.get("title", "").strip(),
            location=" | ".join(filter(None, locs + [country])),
            url=x.get("jobUrl", ""), ats="ashby", posted=_iso_from_str(x.get("publishedAt")),
            description=x.get("descriptionPlain") or html_to_text(x.get("descriptionHtml")),
            remote=bool(x.get("isRemote")),
        ))
    return out


# ---------------------------------------------------------------- SmartRecruiters
def smartrecruiters(slug, name, country=""):
    """country: optional ISO-2 code ("in", "us") so the feed filters server-side."""
    out, offset = [], 0
    cq = f"country={country.lower()}&" if country else ""
    while True:
        j = get_json(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings?{cq}limit=100&offset={offset}")
        content = j.get("content", [])
        for x in content:
            loc = x.get("location") or {}
            out.append(Posting(
                company=name, title=x.get("name", "").strip(),
                location=", ".join(filter(None, [loc.get("city"), loc.get("region"), loc.get("country")])),
                url=f"https://jobs.smartrecruiters.com/{slug}/{x.get('id')}", ats="smartrecruiters",
                posted=_iso_from_str(x.get("releasedDate")), remote=bool(loc.get("remote")),
                extra={"detail": x.get("ref")},
            ))
        offset += len(content)
        if not content or offset >= j.get("totalFound", 0) or offset >= 1000:
            break
    return out


def smartrecruiters_detail(p: Posting):
    j = get_json(p.extra["detail"])
    secs = ((j.get("jobAd") or {}).get("sections") or {})
    p.description = "\n".join(html_to_text((secs.get(k) or {}).get("text")) for k in
                              ("jobDescription", "qualifications", "additionalInformation"))
    if j.get("postingUrl"):
        p.url = j["postingUrl"]


# ---------------------------------------------------------------- Workable
def workable(slug, name):
    j = get_json(f"https://apply.workable.com/api/v1/widget/accounts/{slug}?details=true")
    out = []
    for x in j.get("jobs", []):
        locs = x.get("locations") or [{"city": x.get("city"), "country": x.get("country")}]
        loc = " | ".join(", ".join(filter(None, [l.get("city"), l.get("country")])) for l in locs)
        out.append(Posting(
            company=name, title=x.get("title", "").strip(), location=loc, url=x.get("url", ""), ats="workable",
            posted=_iso_from_str(x.get("published_on") or x.get("created_at")),
            description=html_to_text(x.get("description")), remote=bool(x.get("telecommuting")),
        ))
    return out


# ---------------------------------------------------------------- Rippling ATS
def rippling(slug, name):
    j = get_json(f"https://api.rippling.com/platform/api/ats/v1/board/{slug}/jobs")
    out = []
    for x in j if isinstance(j, list) else []:
        out.append(Posting(
            company=name, title=(x.get("name") or "").strip(), location=(x.get("workLocation") or {}).get("label", ""),
            url=x.get("url", ""), ats="rippling",
            extra={"detail": f"https://api.rippling.com/platform/api/ats/v1/board/{slug}/jobs/{x.get('uuid')}"},
        ))
    return out


def rippling_detail(p: Posting):
    j = get_json(p.extra["detail"])
    d = j.get("description") or {}
    p.description = "\n".join(html_to_text(v) for v in d.values() if isinstance(v, str))
    p.posted = _iso_from_str(j.get("createdOn") or j.get("created_at")) or p.posted
    locs = j.get("workLocations") or []
    if locs:
        p.location = " | ".join(l if isinstance(l, str) else l.get("label", "") for l in locs)


# ---------------------------------------------------------------- Workday (CXS)
# Workday and amazon.jobs have no "list everything" feed, so they are searched by keyword.
# The keywords come from search_queries in the filter config.
DEFAULT_QUERIES = ["software engineer", "data scientist", "machine learning"]


def _workday_posted(s):
    """'Posted Today' / 'Posted Yesterday' / 'Posted 3 Days Ago' / 'Posted 30+ Days Ago'."""
    if not s:
        return None
    today = dt.date.today()
    s = s.lower()
    if "today" in s:
        return today.isoformat()
    if "yesterday" in s:
        return (today - dt.timedelta(days=1)).isoformat()
    m = re.search(r"(\d+)\+?\s*days", s)
    if m:
        return (today - dt.timedelta(days=int(m.group(1)))).isoformat()
    return None


def workday(host, tenant, site, name, queries=None, location=""):
    """location: optional words appended to each keyword search, e.g. "India" or "Remote"."""
    base = f"https://{host}/wday/cxs/{tenant}/{site}"
    seen, out = set(), []
    for q in queries or DEFAULT_QUERIES:
        for offset in range(0, 100, 20):
            j = get_json(f"{base}/jobs", method="POST",
                         json={"appliedFacets": {}, "limit": 20, "offset": offset,
                               "searchText": f"{q} {location}".strip()})
            jobs = j.get("jobPostings", [])
            for x in jobs:
                path = x.get("externalPath")
                if not path or path in seen:
                    continue
                seen.add(path)
                out.append(Posting(
                    company=name, title=x.get("title", "").strip(),
                    # the path's 2nd segment is the primary location, e.g. /job/Pune-India/...
                    location=f'{x.get("locationsText") or ""} {path.split("/")[2] if path.count("/") >= 2 else ""}',
                    url=f"https://{host}/en-US/{site}{path}", ats="workday",
                    posted=_workday_posted(x.get("postedOn")), extra={"detail": f"{base}{path}"},
                ))
            if len(jobs) < 20 or offset + 20 >= (j.get("total") or 0):
                break
    return out


def workday_detail(p: Posting):
    j = get_json(p.extra["detail"])
    info = j.get("jobPostingInfo") or {}
    p.description = html_to_text(info.get("jobDescription"))
    locs = [info.get("location") or ""] + (info.get("additionalLocations") or [])
    p.location = " | ".join(filter(None, locs)) or p.location
    p.posted = _iso_from_str(info.get("startDate")) or p.posted
    if info.get("externalUrl"):
        p.url = info["externalUrl"]


# ---------------------------------------------------------------- amazon.jobs
def amazon(name="Amazon", queries=None, country=""):
    """country: optional ISO-3 code ("IND", "USA", "GBR") so the search filters server-side."""
    seen, out = set(), []
    for q in queries or DEFAULT_QUERIES:
        for offset in range(0, 300, 100):
            params = {"base_query": q, "result_limit": 100, "offset": offset, "sort": "recent"}
            if country:
                params["country"] = country.upper()
            j = get_json("https://www.amazon.jobs/en/search.json", params=params)
            jobs = j.get("jobs", [])
            for x in jobs:
                jid = x.get("id_icims") or x.get("id")
                if jid in seen:
                    continue
                seen.add(jid)
                posted = None
                try:
                    posted = dt.datetime.strptime(x.get("posted_date", ""), "%B %d, %Y").date().isoformat()
                except ValueError:
                    pass
                out.append(Posting(
                    company=name, title=x.get("title", "").strip(),
                    location=x.get("normalized_location") or x.get("location", ""),
                    url="https://www.amazon.jobs" + x.get("job_path", ""), ats="amazon", posted=posted,
                    description=html_to_text(x.get("description")) + "\nPreferred qualifications:\n"
                                + html_to_text(x.get("preferred_qualifications")),
                    requirements=html_to_text(x.get("basic_qualifications")),
                    extra={"team": x.get("company_name")},
                ))
            if len(jobs) < 100:
                break
    return out
