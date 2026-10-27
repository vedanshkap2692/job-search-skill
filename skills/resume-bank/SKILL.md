---
name: resume-bank
description: Build and grow me/master_resume.md, the single source of everything the user can claim, from their resumes, LinkedIn PDF, voice recordings, repos, documents and conversation. Use during onboarding, when the user shares new material, or when tailoring turns up something to ask them.
---

# Resume bank

`me/master_resume.md` is where every claim comes from. Resumes, form answers, outreach and interview stories use nothing else, so the quality of everything downstream depends on this file. Start it from [me/templates/master_resume.md](../../me/templates/master_resume.md).

Build it in two passes. The first, in onboarding, comes from their current resume and is good enough to tailor with. The second, in a later session, goes deep: recordings, repos, documents and an impact interview. Tell them the second pass is where most of the improvement comes from.

## Sources, and what each is good for

Save everything they hand over in `me/sources/`.

- **Current and old resumes, LinkedIn PDF:** roles, titles, dates, education, the projects they already describe. Old resumes often mention work the current one dropped. The LinkedIn PDF is on their profile, under "Resources" or "More", then "Save to PDF".
- **A recording:** the richest source, because people say things they'd never write. Suggest 10–20 minutes per job, talking freely. Give them prompts to talk through (below). Transcribe it with what's available: a local transcription tool such as Whisper, phone dictation, or your platform's voice mode. Read the whole transcript, not a summary.
- **Repos and project folders:** read the README, the structure, the main modules and the history (`git log --author=<them> --stat` shows what they touched and when). From this you learn the stack, the scale and what they owned. Ask about anything unclear, because code shows what was built, not their part in it or what it achieved.
- **Reviews, promotion write-ups, design docs, decks, launch posts, thank-you messages:** outcomes and numbers that someone else confirmed.
- **Public work:** portfolio, papers, talks, blog posts, open-source contributions.

### Prompts for a recording
For each job:
1. What does the company do, and what did your team own?
2. The three or four things you're proudest of there. For each one:
   - what problem it solved, and for whom;
   - what you built or ran, and what part was yours;
   - the hard decisions and the tradeoffs;
   - what changed afterwards, with any numbers you remember;
   - who used it, and how many.
3. Anything you led, mentored or started.
4. Tools and methods you used often enough to be asked about in an interview.

## The impact interview

Go project by project. Ask what it was for, what changed after it shipped, for whom, and by how much. Push gently for numbers:
- money: revenue, savings, the value of what flows through it;
- time: before and after, per task or end to end;
- share automated or handled without a person;
- growth: users, volume, conversion;
- scale: requests, records, documents, users.

When they don't know an exact figure, ask for a range or a proxy ("roughly how many a day?", "how long did it take before?"). Write down the source of every number: a document, the code or data, or "their estimate". Never round up or inflate. An estimate they can explain in an interview is fine; one they can't, isn't.

If they still have access to the data (a dashboard, a database they can query), offer to help pull the real figure, and record how it was measured.

## What to write

Follow the template's sections:
- **Ground rules:** exact titles and dates per role, education, and their own rules (numbers they don't want used, words they dislike).
- **One section per project or area:**
  - what and why in plain words, for interviews;
  - the numbers table, with source and method;
  - bullets: a full one and a short one, each keeping the impact number;
  - swap-in phrases: true variations to use when a JD asks for something specific;
  - JD terms that are true for it.
- **JD-term index:** common JD asks → the true phrase → the project. It grows with every tailored resume.
- **Not claimed:** tools and skills they haven't used. Add to it whenever they say "no, I haven't done that". Never claim anything on this list, and don't point out its absence.
- **Safe to assume:** the standard practice around their work that needn't be asked about. For a data scientist that's pandas, EDA and model evaluation; for a backend engineer, Git, testing and code review.
- **Summaries and skills lines** for each role family.

## Writing defaults

The user's `me/style.md` overrides any of these.
- Impact first. Every version of a bullet keeps its impact number, including the short one. When space is tight, drop detail before impact.
- Use only numbers that impress an outsider: totals, ratios, big before → after changes. Leave out small counts and per-day rates.
- Business terms, not internal project names or client names. Internal detail lives in "what and why", for interviews.
- One idea per bullet. Vary the sentence shapes.

## Confidential material

Work material can be confidential. Use it to understand what they did; never copy internal names, client names, code or secrets into the bank's bullets. If they're unsure whether something can be shared, leave it out of the bullets and keep it in "what and why".

## Keeping it growing

- Each tailored resume ends with an "ask the user" list. When they answer, add the facts here, with the source.
- After an interview, add any story that landed well, or a number they found.
- Log changes in `data/log.md`.

## Tell the user

After each pass: the projects you have, the strongest numbers, and the weak spots. For example: "two projects have no impact number yet", or "nothing here backs the cloud experience most of your target JDs ask for". Suggest how to close each gap.
