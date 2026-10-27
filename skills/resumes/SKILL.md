---
name: resumes
description: Make base resumes for each role family, tailor a resume to a specific job description, build the file and check it. Use during onboarding, before any application, or when the user asks for a resume or cover letter.
---

# Resumes

Everything on a resume comes from `me/master_resume.md`. If a JD asks for something the bank doesn't have, it goes on an "ask the user" list, never on the resume. Claims the bank records with exact wording (qualified results, estimates) keep that wording.

## Format

Ask whether they have a layout they like. Keep it if they do; otherwise recommend one and show it. For the first run, when nothing is decided yet, a clean one-column HTML page printed to PDF (with headless Chrome or whatever renders HTML on their machine) is quick and fine.
- **Their own Word or Google Doc:** edit a copy per resume, keep the layout, export to PDF.
- **LaTeX or Typst:** precise and easy to rebuild from one set of bullets. Check what's installed (`tectonic`, `pdflatex`, `typst`).
- **HTML to PDF:** easy to restyle; print it with a headless browser.

Defaults, which the user can change:
- One page unless the role clearly benefits from two. Verify by compiling and checking the page count (`pdfinfo`), never by eyeballing the source.
- Friendly to applicant tracking systems: one column, real text (not images), standard headings (Experience, Education, Skills), and no tables for the main content.
- After building, extract the text and check it reads cleanly and in order, with no odd symbols. Use `pdftotext resume.pdf -` if it's installed, a Python PDF library, or your own PDF reading.
- Render a page preview (`pdftoppm -png`) and look at it: templates accumulate stray braces, ugly line breaks and overflowing lines that the source hides.
- File name: `Firstname_Lastname_<Role>.pdf`. Leave the company name out, since recruiters forward files.

**One set of bullets, many resumes.** Keep bullets in the bank with IDs, and build each resume by choosing and rewriting bullets rather than editing a document from scratch. A small build script that takes a list of bullet IDs and overrides makes tailoring fast and keeps every version consistent. Write one if the format allows.

## Base resumes

One per role family in `me/profile.md`, saved in `me/resumes/base/`.
- **Summary:** two lines naming the family's two or three main asks, in the terms JDs use.
- **Experience:** the projects that matter most for that family, strongest first.
- **Skills line:** the family's common tools first, true ones only.
- Score each with [review](../review/SKILL.md), fix what it finds, and show the user the resume, the score and what changed.

Rebuild them when the bank changes. They're the starting point for tailoring, and what goes out when the user chooses not to tailor (see `me/permissions.md`).

## Bullet defaults

`me/style.md` overrides these.
- One idea per bullet, about two lines.
- Impact first. At most three numbers, one of them the impact.
- At most two or three named tools per bullet; the skills line carries the rest.
- Each technique appears once per resume.
- The JD's word for the same thing. Vary the sentence shapes so it doesn't read as generated.
- A qualified claim keeps its qualifier in every version, including the short one. "Cut errors 40% in the pilot" never becomes "cut errors 40%".

## Tailoring to a JD

Tailoring means picking the right work, describing it in the JD's terms and keeping the impact. It's more than reordering the base resume.

1. **Full JD.** Work from the saved JD in `data/jds/`, never the short must-have list in the ledger. LinkedIn pages often need the browser to get the full text.
2. **List the terms.** Pull most of the JD's terms, not a top ten: must-haves, nice-to-haves, and what it says about how the work is done ("owns models end to end", "ships weekly").
3. **Match each term to a true phrase,** from the bank's JD-term index first, then each project's swap-ins. Terms with nothing behind them are left out. Terms on the bank's "not claimed" list stay out even of the skills line. Anything that might be true but isn't recorded goes on the "ask the user" list.
4. **Coverage table** in `notes.md`. Give every term one row: in a bullet (which one), skills line only, left out (and why), or ask the user. Every must-have they've done belongs in a bullet, because recruiters read bullets, not skills lines.
5. **Choose and rewrite the bullets.** Start from the family's base, swap in the projects the JD calls for, and rewrite most bullets in the JD's words. Use one or two JD terms per bullet, spread across the page, so nothing reads as stuffed. Lead each bullet with the number that matters most to this company. The summary names the JD's two or three main asks.
6. **Skills line:** the JD's tools first, true ones only.
7. **Build and check:** page count, text extraction, a rendered preview, no leftover placeholders.
8. **Independent blind review** ([review](../review/SKILL.md)): the reviewer gets the JD, the bank and the resume, never this tailoring's notes. Fix what it finds and rebuild.
9. **Save** `me/resumes/<company>-<role>/`: the resume, any build file, and `notes.md` (below). Set the job's `folder` and `resume_path` in the ledger, and its status to "ready" once the review has passed.

By default every application gets a tailored resume. If the user would rather send a base resume to lower-fit roles, follow `me/permissions.md`. Reusing a recent tailored resume for a very similar JD is fine — it still gets its own folder, notes and review.

### notes.md
```
# <Company>: <Role>
- Date, link, apply link
- Resume: <file>, from base <family>
- Score: <n>/100 after review

## Coverage
| JD term | Type (must / nice / how) | Where |

## Ask the user
## Review findings, and what was fixed
## Form answers (anything this application asked)
```

## Cover letters and free-text questions

Only when a portal requires one, or the user wants one. Three short paragraphs: why this role, two pieces of evidence from the bank in the JD's terms, and a plain close. Same review as a resume. Save it in the job's folder.

## Tell the user

For each resume, briefly: the score, the top fixes the review made, must-haves left out and why, and the "ask the user" items. Their answers go into the bank.
