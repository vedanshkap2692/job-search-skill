---
name: dashboard
description: Build, refresh or redesign the dashboard that shows the needs-you queue, the pipeline and what the agent did. Use during onboarding, at the end of every run, or when the user wants a different view.
---

# Dashboard

One page that answers two questions: what needs me, and what did the agent do?

## The default

`python3 ui/build.py` reads the ledger, fills `ui/template.html` with it and writes `ui/dashboard.html`. That's a single page that opens straight from disk, with no server. Re-run it at the end of every run, and after any session that changes the ledger.

- **Left: sittings.** The needs-you queue grouped into short batches (interviews and tests, replies, drafts to check, questions, sign-ins), each with a time estimate. Opening one shows its items one at a time: the draft, a link, a copy button, and "done". Keys: J and K to move, D for done, Esc to go back.
- **Right:** deadlines coming up, pipeline counts (found, applied, replied, interviews, offers), and the agent log, which shows each run's summary and any warnings.
- **Below:** the jobs table, with status filters and search.

"Done" marks live only in that browser; a page opened from disk can't write to the ledger. When the user says they've handled something, or you see it handled (the reply is in the thread, the application confirmed), set `done_at` on the item and rebuild.

The page escapes everything it shows and links only to `http(s)` addresses, because titles and messages come from the web. Keep it that way in any redesign.

## Changing it

The user can ask for any change at any time. Edit `ui/template.html`, and `ui/build.py` if the page needs more data. If they keep their records in another format, adapt `build.py` to read it.

When they're not sure what they want, describe these in a sentence each, and build the one they pick:
- **Sittings** (the default): the day's work as a few short batches, handled one item at a time.
- **Switchboard:** dense panels on one screen, keyboard-driven. The agent's log reads as a list of what it ran, and each application opens like a pull request, with the resume's changes against the base, the form answers and the people contacted.
- **Signal:** the market view. Search a skill to see how many JDs ask for it, whether their resume claims it, and which jobs want it. Gaps become things to study.
- **Pocket:** phone-first cards, one at a time: done, later, or hand back to the agent.

Mixing them is fine, for example Sittings with a Signal tab.

## On the phone

How they reach it away from the laptop depends on the platform: a private published page (some agents can publish one), remote control of the agent, or syncing the file to their phone. The page holds personal data, so never publish it anywhere public.
