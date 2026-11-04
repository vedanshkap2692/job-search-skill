#!/usr/bin/env python3
"""Job radar: scan public ATS feeds for roles that pass the user's filters.

    .venv/bin/python radar.py                 # full run (HTTP feeds + Playwright portals)
    .venv/bin/python radar.py --no-browser    # HTTP feeds only, no Playwright
    .venv/bin/python radar.py --verify        # check every slug in companies.yaml still returns jobs
    .venv/bin/python radar.py --only greenhouse,lever --days 30
    .venv/bin/python radar.py --config path/to/filters.yaml

Filters come from me/radar.yaml (falls back to filters.example.yaml). Reads data/ledger.db
read-only to skip jobs already tracked. Never writes to the ledger, never applies, never logs
in. Output: data/radar/radar-<date>.md and .csv (+ a .jsonl audit of every title match and
why it was kept or dropped).
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import datetime as dt
import json
import re
import sqlite3
import sys
import time
from collections import Counter
from pathlib import Path

import yaml

import fetchers as F
import filters as R

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
LEDGER = REPO / "data" / "ledger.db"
OUTDIR = REPO / "data" / "radar"
USER_CONFIG = REPO / "me" / "radar.yaml"
EXAMPLE_CONFIG = HERE / "filters.example.yaml"

HTTP_KINDS = ["greenhouse", "lever", "ashby", "smartrecruiters", "workable", "rippling", "workday", "amazon"]
BROWSER_KINDS = ["eightfold"]


# ------------------------------------------------------------------ inputs
def load_filters(path=None):
    p = Path(path) if path else (USER_CONFIG if USER_CONFIG.exists() else EXAMPLE_CONFIG)
    return p, yaml.safe_load(p.read_text()) or {}


def load_companies(path, fcfg):
    cfg = yaml.safe_load(Path(path).read_text())
    queries = fcfg.get("search_queries") or None
    jobs = []  # (kind, display name, callable)
    for kind in ("greenhouse", "lever", "ashby", "workable", "rippling"):
        for c in cfg.get(kind) or []:
            fn = getattr(F, kind)
            jobs.append((kind, c["name"], lambda fn=fn, c=c: fn(c["slug"], c["name"])))
    sr_country = fcfg.get("smartrecruiters_country") or ""
    for c in cfg.get("smartrecruiters") or []:
        jobs.append(("smartrecruiters", c["name"], lambda c=c: F.smartrecruiters(c["slug"], c["name"], sr_country)))
    wd_loc = fcfg.get("workday_location") or ""
    for c in cfg.get("workday") or []:
        jobs.append(("workday", c["name"], lambda c=c: F.workday(c["host"], c["tenant"], c["site"], c["name"],
                                                                 queries, wd_loc)))
    if cfg.get("amazon"):
        am_country = fcfg.get("amazon_country") or ""
        jobs.append(("amazon", "Amazon", lambda: F.amazon("Amazon", queries, am_country)))
    browser_jobs = [("eightfold", c["name"], c) for c in cfg.get("eightfold") or []]
    return jobs, browser_jobs


def _norm_url(u):
    u = (u or "").strip().lower().split("?")[0].split("#")[0].rstrip("/")
    u = re.sub(r"^https?://(www\.)?", "", u)
    u = re.sub(r"/[a-z]{2}-[a-z]{2}(?=/)", "", u)  # workday /en-US/ locale segment
    return u.replace("boards.greenhouse.io", "job-boards.greenhouse.io").replace("/apply", "")


def _job_id(u):
    """Last URL path segment, used as a second dedupe key (same req, different URL shape)."""
    seg = _norm_url(u).split("/")[-1]
    return seg if len(seg) >= 6 else None


def _norm_text(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def _norm_company(s):
    s = _norm_text(s)
    return re.sub(r"\b(inc|pvt|private|ltd|limited|llc|corp|technologies|technology|labs|software|ai|careers)\b", "", s).strip()


def load_ledger():
    if not LEDGER.exists():
        return set(), set(), set()
    con = sqlite3.connect(f"file:{LEDGER}?mode=ro", uri=True)
    try:
        rows = con.execute("select url, company, title, apply_url from jobs").fetchall()
    finally:
        con.close()
    urls = {_norm_url(r[0]) for r in rows} | {_norm_url(r[3]) for r in rows if r[3]}
    pairs = {(_norm_company(r[1]), _norm_text(r[2])) for r in rows}
    ids = {i for r in rows for i in (_job_id(r[0]), _job_id(r[3] or "")) if i}
    return urls, pairs, ids


# ------------------------------------------------------------------ pipeline
def run_fetch(jobs, workers=8):
    postings, stats, errors = [], {}, []
    with cf.ThreadPoolExecutor(workers) as ex:
        futs = {ex.submit(fn): (kind, name) for kind, name, fn in jobs}
        for fut in cf.as_completed(futs):
            kind, name = futs[fut]
            try:
                ps = fut.result()
                postings.extend(ps)
                stats[(kind, name)] = len(ps)
            except Exception as e:
                errors.append(f"{kind}/{name}: {str(e)[:120]}")
                stats[(kind, name)] = None
    return postings, stats, errors


def needs_detail(p):
    return not p.description and ("detail" in p.extra or "pcsx_id" in p.extra)


def fill_details(postings, workers=6):
    todo = [p for p in postings if needs_detail(p) and "detail" in p.extra]
    detail_fn = {"smartrecruiters": F.smartrecruiters_detail, "workday": F.workday_detail, "rippling": F.rippling_detail}

    def one(p):
        try:
            detail_fn[p.ats](p)
        except Exception as e:
            p.extra["detail_error"] = str(e)[:120]
    with cf.ThreadPoolExecutor(workers) as ex:
        list(ex.map(one, todo))


def classify(postings, rules, days, ledger_urls, ledger_pairs, ledger_ids, browser=None):
    """Two passes: cheap filters (title, location, date) first, then JD-based ones after detail fetch."""
    audit, drops = [], Counter()
    stage1 = []
    seen = set()
    for p in postings:
        key = _norm_url(p.url)
        if key in seen:
            continue
        seen.add(key)
        if rules.company_excluded(p.company):
            drops["excluded employer"] += 1
            continue
        fam = rules.title_family(p.title)
        if not fam:
            drops["title"] += 1
            continue
        loc = rules.location_status(p)
        if not loc:
            drops["location"] += 1
            continue
        age = R.age_days(p.posted)
        if age is not None and age > days:
            drops[f"older than {days}d"] += 1
            audit.append(_audit(p, fam, "drop", f"stale ({age}d)"))
            continue
        stage1.append((p, fam, loc))

    # lazy JD fetch only for survivors
    fill_details([p for p, _, _ in stage1])
    if browser:
        efs = [p for p, _, _ in stage1 if p.ats == "eightfold" and not p.description]
        if efs:
            browser.eightfold_details(efs)

    keeps = []
    for p, fam, loc in stage1:
        age = R.age_days(p.posted)  # detail fetch may have added a date
        if age is not None and age > days:
            drops[f"older than {days}d"] += 1
            audit.append(_audit(p, fam, "drop", f"stale ({age}d)"))
            continue
        if loc == "remote-check" and not rules.remote_ok_for_user(p):
            drops["remote, not for your location"] += 1
            continue
        if not rules.location_status(p):  # the detail fetch may have changed the location
            drops["location"] += 1
            continue
        text = (p.description or "") + "\n" + (p.requirements or "")
        if fam.startswith("check:"):
            ok, name = rules.jd_check_passes(fam, text)
            if not ok:
                drops[f"{name}: too few JD terms"] += 1
                continue
            fam = name
        exp = rules.parse_experience(p.description, p.requirements)
        if not p.description and not p.requirements:
            exp["quote"] = "JD not read (" + p.extra.get("detail_error", "no description in feed") + ")"
        if rules.too_senior(exp):
            drops[f"experience min > {rules.max_years:g}y"] += 1
            audit.append(_audit(p, fam, "drop", f"exp min {exp['min']:g}: {exp['quote'][:140]}"))
            continue
        in_ledger = (_norm_url(p.url) in ledger_urls or _job_id(p.url) in ledger_ids
                     or (_norm_company(p.company), _norm_text(p.title)) in ledger_pairs)
        if in_ledger:
            drops["already in ledger"] += 1
            audit.append(_audit(p, fam, "drop", "in ledger"))
            continue
        hint, score = rules.fit_hint(p, fam, exp)
        keeps.append({"company": p.company, "title": p.title, "location": _short_loc(p.location, rules),
                      "experience": exp["quote"], "exp_min": exp["min"], "posted": p.posted or "",
                      "url": p.url, "ats": p.ats, "fit_hint": hint, "_score": score})
        audit.append(_audit(p, fam, "keep", exp["quote"][:160]))
    keeps.sort(key=lambda k: (-k["_score"], k["posted"] == "", k["company"]))
    return keeps, drops, audit


def _short_loc(s, rules):
    parts = [x.strip() for x in re.split(r"\s*\|\s*", s or "") if x.strip()]
    if rules.loc_rx or rules.code_rx:
        parts = [x for x in parts if rules.location_status(F.Posting("", "", x, "", "")) == "match"] or parts
    out = " | ".join(dict.fromkeys(parts))
    return out[:90]


def _audit(p, fam, decision, why):
    return {"company": p.company, "title": p.title, "location": p.location[:120], "posted": p.posted,
            "url": p.url, "ats": p.ats, "family": fam, "decision": decision, "why": why}


# ------------------------------------------------------------------ outputs
def write_outputs(keeps, drops, audit, stats, errors, days, started, n_postings, cfg_path, rules):
    OUTDIR.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    cols = ["company", "title", "location", "experience", "posted", "url", "ats", "fit_hint"]
    csv_path = OUTDIR / f"radar-{today}.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(keeps)
    with (OUTDIR / f"radar-{today}.audit.jsonl").open("w") as f:
        for a in audit:
            f.write(json.dumps(a) + "\n")

    ok = sum(1 for v in stats.values() if v)
    empty = sorted(f"{k}/{n}" for (k, n), v in stats.items() if v == 0)
    by_ats = Counter(k for (k, _), v in stats.items() if v)
    md = [f"# Job radar, {today}", "",
          f"Scanned {ok} company feeds ({', '.join(f'{k} {v}' for k, v in sorted(by_ats.items()))}), "
          f"{n_postings} postings in total, in {time.time() - started:.0f}s.",
          f"Filters from `{_rel(cfg_path)}`: families {', '.join(n for n, _ in rules.families) or 'none'}"
          f"{'; JD-checked ' + ', '.join(n for n, _, _ in rules.jd_check) if rules.jd_check else ''}; "
          f"{'stated experience minimum at most ' + format(rules.max_years, 'g') + ' years, or none' if rules.max_years is not None else 'no experience filter'}; "
          f"posted within {days} days when dated; not already in data/ledger.db.", "",
          f"**{len(keeps)} keeps.** Experience is quoted from the JD by a regex parser: open the posting and "
          f"confirm before applying. \"not stated\" means no years were found, which the filter keeps.", "",
          "| # | Company | Title | Location | Experience (quoted) | Posted | ATS | Fit hint | URL |",
          "|---|---|---|---|---|---|---|---|---|"]
    for i, k in enumerate(keeps, 1):
        cells = [str(i), k["company"], k["title"], k["location"], k["experience"][:140], k["posted"] or "n/a",
                 k["ats"], k["fit_hint"], k["url"]]
        md.append("| " + " | ".join(c.replace("|", "/").replace("\n", " ") for c in cells) + " |")
    md += ["", "## Dropped, by reason", ""] + [f"- {r}: {n}" for r, n in drops.most_common()]
    if errors:
        md += ["", "## Feeds that failed this run", ""] + [f"- {e}" for e in sorted(errors)]
    if empty:
        md += ["", "## Feeds that returned zero postings", "", ", ".join(empty)]
    md += ["", f"Audit trail of every in-scope title (kept or dropped, with the reason): "
               f"`data/radar/radar-{today}.audit.jsonl`"]
    md_path = OUTDIR / f"radar-{today}.md"
    md_path.write_text("\n".join(md) + "\n")
    return md_path, csv_path


def _rel(p):
    try:
        return str(Path(p).resolve().relative_to(REPO))
    except ValueError:
        return str(p)


# ------------------------------------------------------------------ verify
def verify(jobs, browser_jobs, use_browser, rules, fcfg):
    print(f"Checking {len(jobs) + len(browser_jobs)} feeds...")
    postings, stats, errors = run_fetch(jobs)
    local = Counter()
    for p in postings:
        if rules.location_status(p) == "match":
            local[p.company] += 1
    for (kind, name), n in sorted(stats.items()):
        flag = "DEAD" if not n else ""
        print(f"{kind:16} {name:32} {str(n):>5} postings  {local.get(name, 0):>4} in your locations  {flag}")
    if use_browser and browser_jobs:
        from browser import Browser
        b = Browser()
        try:
            for _, name, c in browser_jobs:
                try:
                    ps = b.eightfold(name, c["base"], c["domain"], queries=(fcfg.get("search_queries") or ["engineer"])[:1],
                                     location=fcfg.get("eightfold_location") or "", max_pages=1)
                    print(f"{'eightfold':16} {name:32} {len(ps):>5} postings (1 query)")
                except Exception as e:
                    print(f"{'eightfold':16} {name:32}  DEAD  {str(e)[:80]}")
        finally:
            b.close()
    for e in errors:
        print("ERROR", e)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--companies", default=str(HERE / "companies.yaml"))
    ap.add_argument("--config", help="filter config (default: me/radar.yaml, else filters.example.yaml)")
    ap.add_argument("--days", type=int, help="freshness window when a posted date exists (default: from config)")
    ap.add_argument("--only", help="comma list of ATS kinds, e.g. greenhouse,lever,eightfold")
    ap.add_argument("--no-browser", action="store_true", help="skip Playwright sources")
    ap.add_argument("--verify", action="store_true", help="check each slug returns jobs, then exit")
    a = ap.parse_args()

    cfg_path, fcfg = load_filters(a.config)
    rules = R.Rules(fcfg)
    days = a.days or rules.days
    print(f"Filters: {_rel(cfg_path)}", file=sys.stderr)
    jobs, browser_jobs = load_companies(a.companies, fcfg)
    if a.only:
        only = set(a.only.split(","))
        jobs = [j for j in jobs if j[0] in only]
        browser_jobs = [j for j in browser_jobs if j[0] in only]
    if a.no_browser:
        browser_jobs = []
    if a.verify:
        verify(jobs, browser_jobs, not a.no_browser, rules, fcfg)
        return

    started = time.time()
    print(f"Fetching {len(jobs)} HTTP feeds...", file=sys.stderr)
    postings, stats, errors = run_fetch(jobs)
    browser = None
    try:
        if browser_jobs:
            from browser import Browser
            print(f"Opening {len(browser_jobs)} browser portals with Playwright...", file=sys.stderr)
            browser = Browser()
            for kind, name, c in browser_jobs:
                try:
                    ps = browser.eightfold(name, c["base"], c["domain"], queries=fcfg.get("search_queries") or None,
                                           location=fcfg.get("eightfold_location") or "")
                    postings.extend(ps)
                    stats[(kind, name)] = len(ps)
                except Exception as e:
                    errors.append(f"{kind}/{name}: {str(e)[:120]}")
                    stats[(kind, name)] = None
        print(f"{len(postings)} postings fetched; filtering...", file=sys.stderr)
        urls, pairs, ids = load_ledger()
        keeps, drops, audit = classify(postings, rules, days, urls, pairs, ids, browser)
    finally:
        if browser:
            browser.close()
    md, csvp = write_outputs(keeps, drops, audit, stats, errors, days, started, len(postings), cfg_path, rules)
    print(f"{len(keeps)} keeps -> {md.relative_to(REPO)} and {csvp.relative_to(REPO)}")


if __name__ == "__main__":
    main()
