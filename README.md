# job-search-skill

Prompts that turn your AI coding agent into a careful, honest job-search assistant — for any tech role.

Built on [mindadeepam/job-search-assistant](https://github.com/mindadeepam/job-search-assistant) and updated with the field lessons from running it for real: twenty-plus submitted applications' worth of ATS quirks, verification rituals, screener-question policy, connector pitfalls and an always-on blind review gate.

## What this is

A set of markdown instructions, plus a few small files. Give it to an AI agent that can work on your computer (Claude Code, Codex, Cursor, Gemini CLI or similar), and it becomes your job-search assistant. It can:
- find open roles that fit you — reading the company's real posting, not the repost — and score each one;
- build a bank of everything you can claim, from your resumes, LinkedIn, GitHub repos, documents or a voice recording, and turn it into a resume tailored to each job;
- fill in applications across Workday, Greenhouse, Ashby, Rippling, BambooHR, LinkedIn Easy Apply, Naukri and more, with every field verified before submit;
- run an independent blind review on every resume and application before it goes out;
- find people who can refer you, and write the notes and follow-ups in your voice;
- watch your email and LinkedIn for replies, interviews and assessments, with answers drafted;
- apply by email when a posting names an address, with the resume attached;
- prepare you for interviews: company research, likely questions, mock rounds, a study plan;
- show it all on a dashboard, and run on a schedule.

## The safety model

The parts that aren't negotiable, however much you automate:

- **Nothing invented, ever.** Every resume line, form answer and message traces to `me/master_resume.md` — a fact bank built from your material, with a "not claimed" list for skills you don't have and exact wording for claims that need their qualifiers. If a recruiter asks about experience that isn't in the bank, the agent asks *you*, it doesn't improvise. This holds even if you tell it to make something up.
- **A blind review before every send.** A separate reviewer (a fresh subagent on the strongest model available) checks each resume and application against only the JD and the fact bank — never the tailoring notes — and the writer fixes what it flags.
- **Your passwords stay yours.** It never types passwords or codes, never creates accounts, never solves CAPTCHAs. Forms that end at a CAPTCHA are filled, verified and left one click from done for you.
- **Honest screeners.** Experience buckets picked on one consistent, defensible basis; trick questions answered truthfully; decimals rounded down, not up.
- **Verified, not assumed.** Every field re-checked before submit (autofill lies, long textareas shift radio buttons, resume lists preselect the wrong file), and "submitted" means the confirmation page was seen.
- **No double sends, no spam.** Ledger plus live-page checks before every send; outreach only to people actually relevant to the role.

## Try it

Paste this into your agent:

> Set up https://github.com/vedanshkap2692/job-search-skill for me.

It tells you what it can do, asks a few questions, and gets you to a first real result in about an hour: open jobs found, one resume tailored to one of them, and outreach drafted for real people. The rest builds up over the next few sessions, at your pace.

Prefer to do it by hand? Make your own copy with "Use this template" (keep it **private**, since it will hold your resume and job data) or `git clone`. Then open the folder in your agent and say "set me up". [docs/SETUP.md](docs/SETUP.md) covers the browser extension, email connector and optional tools.

## Good to know first

- **It will make mistakes.** It can send and submit on its own from day one, but it's worth checking the first few of everything before you let it run. Your corrections become rules it follows from then on.
- **It's not a cheat code. Use it in good faith.** Honest applications, and messages to people who are actually relevant to the role. People report spam, and it's your name and your account on every message.
- **Sites have rules.** LinkedIn's terms prohibit automated activity, so any sending done for you can get your account restricted. It starts at a moderate pace and backs off at any warning.
- **It reads strangers' messages.** Emails and job pages can contain text meant to trick an agent. It treats everything it reads as information, never as instructions, but keep an eye on what it sends.
- **Everything comes from you.** It claims only what you've told it or shared with it.
- **Your files stay on your machine** (`me/` and `data/` are gitignored), but whatever the agent reads goes to your AI provider and to any service you connect.

## What you need

- An agent that can read files and run commands: Claude Code, Codex, Cursor, Gemini CLI or similar.
- `sqlite3` or Python 3 (most Macs and Linux machines have both).
- Optional, set up with the agent's help ([docs/SETUP.md](docs/SETUP.md)): a browser it can control, an email connection, scheduled tasks, LaTeX for typeset resumes.
- A plan with room for long runs. Searching, tailoring, reviewing and outreach use a fair amount of your agent's usage.

---

## For agents

If a user gave you this link:

1. **Explain first.** In two or three sentences, tell them what this is and what it can do (from the sections above), and ask whether they'd like to set it up or just wanted to know.
2. **To set it up,** suggest a folder (`~/job-search-assistant` unless they'd like another) and clone it there: `git clone https://github.com/vedanshkap2692/job-search-skill.git ~/job-search-assistant`. Their copy will hold personal data. If they want it on GitHub, recommend a private repo made with "Use this template"; a fork of a public repo can't be made private.
3. **Work from that folder.** Read its [AGENTS.md](AGENTS.md) now and follow it; your platform won't load it on its own mid-session. A new user starts with [skills/onboarding](skills/onboarding/SKILL.md). Tell them that future sessions should start in that folder.

Keep it light. They should feel helped, not configured. Show them what's possible a little at a time, and let them decide how far to take it.

## What's in here

```
AGENTS.md       instructions every session starts from (CLAUDE.md and GEMINI.md point here)
docs/SETUP.md   connecting the browser, email, schedules and tools, with the known pitfalls
skills/         one folder per job:
  onboarding/     first setup, and adding things later
  resume-bank/    everything the user can claim, from their material
  resumes/        base resumes, tailoring to a JD, building and verifying the file
  review/         independent blind checks, results, and reviewing the setup
  job-search/     finding and scoring open roles (from the real posting, not the repost)
  outreach/       referral requests, notes, follow-ups
  cold-email/     applying by email when a posting names an address (off by default)
  inbox/          email and LinkedIn replies, interviews, deadlines
  apply/          filling in and submitting applications, screener policy, verification
  interview-prep/ research, mock interviews, study plans, offers
  dashboard/      the page that shows what needs you
  routines/       scheduled runs
playbooks/      field notes: LinkedIn, application forms by ATS, browsers, email, scheduled runs, job sources
me/templates/   blank templates for your profile, fact bank, permissions and style rules
data/           the ledger schema (the ledger and log themselves stay local)
me/             your profile, resume bank, feedback, resumes (local only, gitignored)
ui/             the dashboard template and the script that fills it
```

## Credit

The architecture and most of the base instructions come from [mindadeepam/job-search-assistant](https://github.com/mindadeepam/job-search-assistant) (MIT), by Deepam Minda. This version folds in the operational lessons from an extended real-world run: the honesty architecture, the blind review gate, per-ATS form notes, screener policy, the connectors guide and the verification discipline.

## Contributing

Found a quirk in a job site or an application form? Add it to `playbooks/`. Keep instructions short and plain: prose an agent can follow, not config.

## License

[MIT](LICENSE)
