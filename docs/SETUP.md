# Setting up the environment

What the assistant needs, how to connect it, and the pitfalls found running this for real. The agent walks the user through all of this ([skills/onboarding](../skills/onboarding/SKILL.md)); this file is the reference it works from. Nothing here is required on day one — each piece unlocks more of the system.

## The agent itself

Any coding agent that can read files and run commands works: Claude Code, Codex, Cursor, Gemini CLI or similar. Claude Code is what this setup was built and tested with:
- Install: `npm install -g @anthropic-ai/claude-code` (or the desktop app, which also has scheduled tasks).
- Start every session in this repo's folder, so the agent picks up `AGENTS.md` (via `CLAUDE.md`).
- A plan with room for long runs helps: searching, tailoring and reviews use real usage.

## A browser the agent can control

Unlocks LinkedIn, full JDs, application forms, and sending in the user's name. With Claude Code that's the **Claude in Chrome** extension; other agents have their own browser tools (Playwright-based tools work too, but lose the user's logged-in sessions).

- **Logins are the user's.** They sign in to LinkedIn, job boards and their mail in that browser themselves. The agent never types passwords, one-time codes or 2FA codes, never creates accounts, and never solves CAPTCHAs — "I'm not a robot" checkboxes included. Anything behind a login or CAPTCHA waits in the needs-you queue, with the tab left open at the blocked step so the user can finish in one click.
- **Site permissions:** extensions like Claude in Chrome gate which sites the agent may act on. Grant the job boards, ATS domains and webmail; leave banking and everything else out.
- **The session is the user's:** never sign out, change account settings, or close tabs the agent didn't open. Tab hygiene and the rest: [playbooks/browser.md](../playbooks/browser.md).
- **Multiple Google accounts** signed into one browser profile are the single biggest hazard — a work account is often the default. Verify the active account before any compose or form: [playbooks/email.md](../playbooks/email.md).

## Email

Unlocks the inbox routine (interview invites, recruiter replies, confirmations, job alerts) and apply-by-email.

- **A connector** (Gmail/Outlook MCP on Claude Code and claude.ai, or the platform's equivalent): best for searching, reading, drafting and text-only sends. Connect it to the user's **personal/application account**, not their work account.
- **Attachments** (resumes) are usually easier through the webmail UI in the controlled browser than through a connector; the mechanics, including the hidden-file-input trick, are in [playbooks/email.md](../playbooks/email.md).
- The user should have **one dedicated application address**. It goes in `me/profile.md`, and it's the only address anything is sent from.

## Schedules

Unlocks morning/evening runs with nobody watching. Use the platform's scheduler (Claude Code desktop has scheduled tasks) or cron/launchd running the agent headless from this folder. Runs that use the browser need the computer awake and the browser open. Approval prompts kill unattended runs — do a test run with the user present and fix every prompt it hits: [playbooks/unattended-runs.md](../playbooks/unattended-runs.md).

## Subagents

Unlocks parallel tailoring and, more importantly, the **blind review** ([skills/review](../skills/review/SKILL.md)): a fresh agent that checks each resume and application against the fact bank without seeing the tailoring notes. Use the strongest model available for reviews and for anything that writes in the user's name; cheaper models are fine for scouting and fetching. Without subagents, the review is a separate pass with only the sources open.

## Command-line tools

All optional; the agent checks what's installed and adapts.

| Tool | For | Without it |
| --- | --- | --- |
| `sqlite3` (or Python's `sqlite3` module) | the ledger | plain files with the same fields |
| `python3` | the dashboard (`ui/build.py`), small scripts | skip the dashboard |
| `tectonic` / `pdflatex` / `typst` | LaTeX/Typst resumes | HTML printed to PDF via headless browser |
| `pdftotext` | checking a resume extracts cleanly for ATS parsers | a Python PDF library |
| `pdfinfo`, `pdftoppm` | verifying page count and rendering a visual preview of each built resume | open the PDF and look |

On a Mac: `brew install poppler tectonic` covers the PDF tools and LaTeX.

## Verifying the setup

Before the first unattended run, check each piece the way the skills will use it:
1. Browser: open LinkedIn — the feed should show the user logged in.
2. Email: search the inbox for a known message; send a test mail to the user themselves from the application address, attachment included.
3. Ledger: `sqlite3 data/ledger.db < data/schema.sql`, then a trivial insert and select.
4. Dashboard: `python3 ui/build.py` and open `ui/dashboard.html`.
5. Resume build: compile a base resume, check page count and text extraction.
6. One real application end to end with the user watching, including the independent review and, if a CAPTCHA appears, the hand-to-user step.

## What stays with the user, always

However much is handed over in `me/permissions.md`:
- passwords, one-time codes, 2FA, account creation;
- CAPTCHAs (the agent fills the form, verifies it, leaves the tab open, and queues the final click);
- payments of any kind;
- offers, salary negotiation and anything else they've kept as draft-only.
