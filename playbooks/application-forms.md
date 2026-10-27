# Application forms

Field notes on applicant tracking systems. Add what you learn.

## Everywhere
- Check every field after setting it. Autofill from the resume often gets names, dates and locations wrong.
- Numbers only in numeric fields ("25", not "25 LPA" or "$25k"). A field that rejects decimals gets the number rounded **down**.
- After uploading the resume, check that the attached file is this job's resume, not an older one.
- Long textareas reflow the page: a radio or dropdown you set later can land on the wrong option when the layout shifted mid-click. After filling any long answer, re-verify every radio and dropdown below it, by reading the page or zooming a screenshot — not from memory.
- Tick required terms, privacy and accuracy boxes only. Leave marketing, newsletter, SMS-consent and job-alert opt-ins unticked. Voluntary demographic (EEO) sections stay blank or "prefer not to say" unless the user says otherwise.
- Decline any "save your profile / create an account / 1-click apply next time" offer unless the user wants it.
- Submitted means you saw the confirmation page or message.

## Workday
- Dropdowns open with a real click. Then click the option inside `[role=listbox] [role=option]` (a script click on the option works). Typing and pressing Enter sometimes picks the wrong value, so check it.
- Most Workday sites want an account, which is the user's job. Some offer a guest application ("Apply manually" or similar). Look before calling it a login blocker, and decline any offer to create an account afterwards.

## Greenhouse
- Plain boards (boards.greenhouse.io): setting text fields directly usually works.
- **Embedded in a company site:** some companies wrap the Greenhouse form in a cross-origin iframe on their own domain, and boards.greenhouse.io redirects back to the wrapper. File inputs inside the iframe are unreachable. Fix: read the iframe's src from the wrapper page (`document.querySelectorAll('iframe')` → `job-boards.greenhouse.io/embed/job_app?for=<co>&token=<id>&validityToken=...`) and navigate to it top-level; the full form, file inputs included, is then scriptable. Scrape the iframe src **before** starting to fill — navigating away mid-form wipes everything.
- "School" dropdowns often lack newer institutes. Pick "Other" rather than a similarly named wrong school.
- Combobox keyboard selection (Down/Down/Enter) can overshoot and pick the wrong country code; click the option by coordinates and zoom to verify the chip afterwards.

## Ashby (jobs.ashbyhq.com)
- Programmatic value-setting on the Email field and Yes/No toggle buttons does NOT register in Ashby's React state even when the value displays — submit then fails with "Missing entry for required field". Click into the field and type with real keystrokes; click the toggles with real clicks.
- The Yes/No toggles DESELECT when clicked a second time — after any re-click, screenshot to confirm the state before submitting.
- Plain text fields and textareas set programmatically were accepted fine; it's specifically email + toggles that need real input.
- Two upload zones can look identical: the top one is "Autofill from resume" (a parser), the lower one labeled Resume* is the real attachment. Upload to the labeled one; skip the parser and fill fields yourself.
- "How did you learn about us" dropdowns have fixed options; "Company Website" fits applications made from their own Ashby board.
- Some text-looking fields are NUMBER inputs (spinner arrows at the right edge, often salary fields). They mangle text ("12.5 LPA" → "12.5e") and arrow keys INCREMENT the value while focused — a keyboard scroll can silently change the number. Type digits only, click a neutral area to blur, and re-screenshot the field right before submit.
- Some companies cap applications per candidate (for example two in 60 days); check the ledger for recent applications there first.

## Rippling (ats.rippling.com)
- No account needed. The single CV drop zone is also the parser ("The CV will be parsed to fill in the application details") — upload, wait for the success toast, then verify every autofilled field.
- Salary fields that look like text can be numeric-only: anything with letters shows "Invalid input". Plain numbers pass. The error can linger until the field blurs — click a neutral area before judging.
- Likert question rows (Strong No / No / Yes / Strong Yes) are real-click buttons; verify with aria-pressed before submit.
- Pronouns and SMS-consent are optional; leave pronouns blank, decline SMS.

## LinkedIn Easy Apply
- Pre-fills "years of experience with X" questions from answers saved on past applications. These can be stale or overstated — re-check every prefilled number against `me/master_resume.md` before clicking Next.
- The email dropdown only offers addresses verified on the LinkedIn account. If the user's application email isn't among them, use the one they chose for LinkedIn (profile), and flag adding the right address to the account.
- The resume list preselects the newest upload; still scroll the list to confirm the selection is on today's file.
- "Follow <company> to stay up to date" on the review step is pre-ticked — untick it (marketing opt-in rule).
- Treat Easy Apply as the weaker channel: when the same role is on the company's own portal, prefer that or do both per `me/permissions.md`.

## BambooHR
- Long single-page forms with essay questions: the radio-shift problem above bites hard here. Fill all textareas first, then set and verify every radio in a second pass.
- Ends at a reCAPTCHA before Submit: fill and verify everything, leave the tab open, queue the user for the CAPTCHA + Submit click.

## Staffing-agency forms (HuntingCube and similar)
- Often no login needed even when the posting sits behind a job board.
- CTC/salary fields may reject decimals; round down to an integer.
- Decline "Save & 1-Click Apply" profile offers; tick only the required T&C box.

## Naukri (and similar profile-based boards)
- One-click "Apply" submits the **profile resume**, not a file you choose — check what's on the profile and how old it is before using it. Updating the profile resume is an account change: ask the user first.
- Recruiter screening questions appear in a chat box right after Apply; answer them from the profile, on the user's standard experience basis.
- "Apply on company site" buttons redirect out — handle those as normal external forms.
- Search-URL filter parameters tend to get stripped; set experience and freshness filters through the UI instead.

## amazon.jobs
- Needs real typing.

## Lever, Phenom, Freshteam, Oracle
- Setting text fields directly usually works. Oracle-based pages scroll inside a container: find the element and scroll it into view rather than scrolling the page.

## Upload buttons with no file input
Some forms (LinkedIn Easy Apply, SmartRecruiters) show only an "Upload" button. One trick that worked with a Chrome automation extension: patch `HTMLInputElement.prototype.click` so the hidden file input gets attached to the page instead of opening the native file picker, click the button, then upload into the captured input and restore the patch. With other tools, use their own file-upload method. Never trigger the native OS file dialog — it blocks the automation.

## Background tabs
Forms in a background tab may not react until the tab is brought forward or screenshotted. Timers (`setTimeout`) in page scripts can hang there, so don't wait on them.
