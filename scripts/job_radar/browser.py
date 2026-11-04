"""Playwright sources: public career pages whose job API only answers inside a browser session.

Used for Eightfold "PCSX" portals (for example Microsoft, Qualcomm, PayPal). Their search API
returns 403 "Not authorized for PCSX" to plain HTTP, but the public careers page calls it
from the browser. We open the public page headless, then call the same endpoint the page
calls, from inside the page. No login, no form filling, a handful of requests per company.

Sites behind a bot challenge (e.g. a Cloudflare "Just a moment..." page)
are deliberately NOT handled: getting past a challenge is circumvention, not reading.
"""
from __future__ import annotations

import datetime as dt
import json
import urllib.parse

from fetchers import DEFAULT_QUERIES, Posting, html_to_text

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")


class Browser:
    def __init__(self):
        from playwright.sync_api import sync_playwright  # imported lazily: only needed here
        self._pw = sync_playwright().start()
        self._b = self._pw.chromium.launch()
        self._ctx = self._b.new_context(user_agent=UA)

    def close(self):
        self._b.close()
        self._pw.stop()

    def _fetch_in_page(self, page, path):
        txt = page.evaluate("async (u) => { const r = await fetch(u); return r.status + '\\n' + await r.text(); }", path)
        status, _, body = txt.partition("\n")
        if status != "200":
            raise RuntimeError(f"HTTP {status} for {path}")
        j = json.loads(body)
        return j.get("data", j)

    def eightfold(self, name, base, domain, queries=None, location="", max_pages=3):
        """base like https://apply.careers.microsoft.com ; domain like microsoft.com ;
        location: optional place the portal filters on, e.g. "India" or "United States"."""
        page = self._ctx.new_page()
        try:
            loc_q = f"?location={urllib.parse.quote(location)}" if location else ""
            page.goto(f"{base}/careers{loc_q}", wait_until="networkidle", timeout=60000)
            seen, out = set(), []
            for q in queries or DEFAULT_QUERIES:
                for start in range(0, 10 * max_pages, 10):
                    params = {"domain": domain, "query": q, "start": start, "sort_by": "timestamp"}
                    if location:
                        params["location"] = location
                    qs = urllib.parse.urlencode(params)
                    d = self._fetch_in_page(page, f"/api/pcsx/search?{qs}")
                    pos = d.get("positions", [])
                    for x in pos:
                        if x["id"] in seen:
                            continue
                        seen.add(x["id"])
                        ts = x.get("postedTs") or x.get("creationTs")
                        out.append(Posting(
                            company=name, title=(x.get("name") or "").strip(),
                            location=" | ".join(x.get("locations") or x.get("standardizedLocations") or []),
                            url=base + (x.get("positionUrl") or f"/careers/job/{x['id']}"), ats="eightfold",
                            posted=dt.datetime.fromtimestamp(ts, dt.timezone.utc).date().isoformat() if ts else None,
                            remote=(x.get("workLocationOption") == "remote"),
                            extra={"pcsx_id": x["id"], "domain": domain, "page_key": base},
                        ))
                    if len(pos) < 10:
                        break
            return out
        finally:
            page.close()

    def eightfold_details(self, postings):
        """Fill descriptions for the postings that survived the cheap filters, one page per portal."""
        by_base = {}
        for p in postings:
            by_base.setdefault(p.extra["page_key"], []).append(p)
        for base, ps in by_base.items():
            page = self._ctx.new_page()
            try:
                page.goto(f"{base}/careers", wait_until="networkidle", timeout=60000)
                for p in ps:
                    try:
                        d = self._fetch_in_page(page, f"/api/pcsx/position_details?position_id={p.extra['pcsx_id']}"
                                                      f"&domain={p.extra['domain']}&hl=en")
                        p.description = html_to_text(d.get("jobDescription"))
                        if d.get("publicUrl"):
                            p.url = d["publicUrl"]
                    except Exception as e:  # keep going; posting is reported as "JD not read"
                        p.extra["detail_error"] = str(e)[:120]
            finally:
                page.close()
