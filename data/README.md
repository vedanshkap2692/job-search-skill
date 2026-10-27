# data/

The agent's records. Nothing here needs editing by hand.

- `ledger.db`: jobs, people, messages, the needs-you queue, runs and a little state between runs. The tables are in [schema.sql](schema.sql). Onboarding creates the file.
- `log.md`: what happened, newest day first. Every session and scheduled run adds to it.
- `jds/`: the full text of each job description, one markdown file per job.

Everything here except this file and `schema.sql` is gitignored.
