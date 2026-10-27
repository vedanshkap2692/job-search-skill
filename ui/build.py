"""Build ui/dashboard.html from the ledger.

Usage: python3 ui/build.py [--db data/ledger.db] [--out ui/dashboard.html]

Reads the ledger, embeds it as JSON in template.html and writes one page that
opens straight from disk. Re-run it after every run. To change the look, edit
template.html; this script only fills in __DATA__.
"""
import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

QUERIES = {
    "needs": """
        SELECT n.id, n.kind, n.title, n.detail, n.link, n.due, n.created_at,
               j.company, j.title AS job_title
        FROM needs_you n LEFT JOIN jobs j ON j.id = n.job_id
        WHERE n.done_at IS NULL
        ORDER BY n.due IS NULL, n.due, n.created_at""",
    "jobs": """
        SELECT id, company, title, location, mode, family, fit, fit_why, status,
               url, apply_url, found_at, applied_at
        FROM jobs ORDER BY found_at DESC""",
    "people": "SELECT status, COUNT(*) AS n FROM people GROUP BY status",
    "messages": """
        SELECT m.id, m.channel, m.direction, m.kind, m.status, m.at, m.body,
               j.company, p.name AS person
        FROM messages m LEFT JOIN jobs j ON j.id = m.job_id
        LEFT JOIN people p ON p.id = m.person_id
        ORDER BY m.at DESC LIMIT 60""",
    "runs": """
        SELECT what, started_at, ended_at, summary, warnings
        FROM runs ORDER BY started_at DESC LIMIT 40""",
}


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--db", type=Path, default=ROOT / "data" / "ledger.db")
    p.add_argument("--out", type=Path, default=ROOT / "ui" / "dashboard.html")
    args = p.parse_args()

    if not args.db.exists():
        sys.exit(f"No ledger at {args.db}. Create it with: sqlite3 {args.db} < data/schema.sql")

    con = sqlite3.connect(args.db)
    con.row_factory = sqlite3.Row
    data = {k: [dict(r) for r in con.execute(q)] for k, q in QUERIES.items()}
    data["generated_at"] = datetime.now().astimezone().isoformat(timespec="minutes")

    # Text from the web could close or comment out the <script> block ("</script>", "<!--").
    # Escaping every "<" keeps the JSON valid and the page intact.
    blob = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    page = (ROOT / "ui" / "template.html").read_text(encoding="utf-8").replace("__DATA__", blob)
    args.out.write_text(page, encoding="utf-8")
    print(f"Wrote {args.out}: {len(data['needs'])} open items, {len(data['jobs'])} jobs, {len(data['runs'])} runs")


if __name__ == "__main__":
    main()
