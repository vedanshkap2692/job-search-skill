-- The ledger: every job, person, message and open item, in one SQLite file.
-- Create it with `sqlite3 data/ledger.db < data/schema.sql`, or Python's built-in sqlite3.
-- Agents read and write it. The user never has to.
-- Dates are ISO 8601 text: times in UTC (what datetime('now') gives) or with an offset; bare dates for whole days.
-- Lists are JSON text.

PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS jobs (
  id            INTEGER PRIMARY KEY,
  url           TEXT UNIQUE NOT NULL,   -- direct link to the posting; how duplicates are caught
  company       TEXT NOT NULL,
  title         TEXT NOT NULL,
  location      TEXT,
  mode          TEXT,                   -- onsite | hybrid | remote
  family        TEXT,                   -- one of the user's role families from me/profile.md
  experience    TEXT,                   -- as the posting says it, e.g. "3-5 years"
  pay           TEXT,                   -- only if the posting states it
  source        TEXT,                   -- linkedin, greenhouse, naukri, user, inbox, ...
  posted        TEXT,
  found_at      TEXT NOT NULL DEFAULT (datetime('now')),
  fit           REAL,                   -- 1 to 5
  fit_why       TEXT,                   -- one line: what the role centres on, what matches, the main gap
  must_have     TEXT,                   -- JSON list, for triage only; tailoring reads the full JD
  jd_path       TEXT,                   -- full JD saved as markdown in data/jds/
  status        TEXT NOT NULL DEFAULT 'new',
                -- new (found) -> shortlisted (picked to apply) -> preparing (resume being made)
                -- -> ready (reviewed, can be submitted) -> applied, or needs_user (blocked)
                -- then interviewing | offer | rejected; or closed | skipped at any point
  apply_url     TEXT,
  folder        TEXT,                   -- me/resumes/<company>-<role>/ when the resume was tailored
  resume_path   TEXT,                   -- the file actually sent
  applied_at    TEXT,
  blocker       TEXT,                   -- why it waits on the user: login, captcha, a question
  notes         TEXT,
  updated_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS people (
  id            INTEGER PRIMARY KEY,
  profile_url   TEXT UNIQUE,            -- linkedin.com/in/...; how duplicates are caught
  name          TEXT NOT NULL,
  headline      TEXT,
  company       TEXT,
  relation      TEXT,                   -- connection | alum | ex_colleague | team | manager | recruiter
  job_id        INTEGER REFERENCES jobs(id),  -- the job they were found for
  status        TEXT NOT NULL DEFAULT 'found',
                -- found | invited | connected | messaged | replied | referred | no_reply | skipped
  connected_at  TEXT,
  email         TEXT,                   -- work email only: published, or shown by a tool the user installed
  notes         TEXT,
  updated_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS messages (
  id            INTEGER PRIMARY KEY,
  person_id     INTEGER REFERENCES people(id),
  job_id        INTEGER REFERENCES jobs(id),
  channel       TEXT NOT NULL,          -- linkedin_invite | linkedin_message | inmail | email | other
  direction     TEXT NOT NULL,          -- out | in
  kind          TEXT,                   -- note | message | follow_up | reply | accept
  body          TEXT,
  status        TEXT NOT NULL,          -- drafted | sent | received
  at            TEXT NOT NULL DEFAULT (datetime('now')),
  follow_up_due TEXT
);

-- What the user has to do: the first thing they see.
CREATE TABLE IF NOT EXISTS needs_you (
  id            INTEGER PRIMARY KEY,
  kind          TEXT NOT NULL,
                -- interview | assessment: dates and deadlines
                -- reply: someone wrote back; a draft is in detail
                -- review: drafts or filled forms waiting for the user's OK
                -- question | decision: only the user can answer (offers are decisions)
                -- login: an application stuck at a sign-in
  title         TEXT NOT NULL,
  detail        TEXT,                   -- what to do, plus any draft
  link          TEXT,
  job_id        INTEGER REFERENCES jobs(id),
  person_id     INTEGER REFERENCES people(id),
  due           TEXT,
  created_at    TEXT NOT NULL DEFAULT (datetime('now')),
  done_at       TEXT
);

-- One row per session or scheduled run.
CREATE TABLE IF NOT EXISTS runs (
  id            INTEGER PRIMARY KEY,
  what          TEXT NOT NULL,          -- skill or routine name
  started_at    TEXT NOT NULL DEFAULT (datetime('now')),
  ended_at      TEXT,
  summary       TEXT,                   -- counts and anything notable
  warnings      TEXT                    -- site limits hit, errors, things skipped
);

-- Small bits of state between runs, e.g. last_inbox_check, linkedin_invite_limit_hit_at.
CREATE TABLE IF NOT EXISTS state (
  key           TEXT PRIMARY KEY,
  value         TEXT,
  updated_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS jobs_status ON jobs(status, fit);
CREATE INDEX IF NOT EXISTS jobs_company ON jobs(company);
CREATE INDEX IF NOT EXISTS people_company ON people(company, status);
CREATE INDEX IF NOT EXISTS messages_person ON messages(person_id, at);
CREATE INDEX IF NOT EXISTS needs_you_open ON needs_you(done_at, due);
