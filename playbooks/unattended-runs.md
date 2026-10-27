# Scheduled runs with nobody watching

Every platform does this differently. These notes come from Claude Code's desktop scheduled tasks (October 2026); the ideas carry over to others.

## Approval prompts
- Each run is a fresh session in the default permission mode. Approving something inside one run doesn't carry over, and "always allow" saves only that exact command, which a run rarely repeats.
- What triggered prompts, and what worked instead:
  - writing to `/tmp` or outside the project: write in the project or the session's scratch folder;
  - heredocs, long `python -c` one-liners, `sed -i` on scripts, commands with `$(...)` or backticks: write the script to a file and run `python3 <file>`, one simple command per call.
- Put a short block with these rules in every routine prompt.
- A narrow allowlist for the exact commands the routines use beats allowing everything. See AGENTS.md, "Explain, then let them decide". In Claude Code that's the `permissions.allow` list in the project's `.claude/settings.local.json`, with entries like `Bash(sqlite3 data/ledger.db:*)` and `Bash(python3 ui/build.py:*)`, plus the browser and email tools the runs use. Other agents have their own equivalent. Set it up with the user, and show them what's on it.
- Do a test run while the user is there. Every prompt it hits is one to fix before the schedule starts.

## Other lessons
- The scheduler couldn't read a symlinked prompt file. Copy the file instead, and keep the repo copy as the one you edit.
- Cloud runs may have restricted network access (web fetch blocked), and can't reach the logged-in browser on the user's computer.
- Local runs need the computer awake and the agent's app open.
- Use the strongest model available for runs that write in the user's name.
