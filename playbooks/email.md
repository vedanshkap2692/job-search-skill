# Email

Field notes on sending application mail. The user's application address lives in `me/profile.md`.

## Which account, every time
- Everything goes from the user's **dedicated application email**. Never from a current-employer account — not for sends, not for drafts, not "just this once".
- Browsers and connectors often have **several accounts signed in** (work, personal, university). Gmail's web UI numbers them (`/mail/u/0/`, `/mail/u/1/`, …) and the default is whatever was signed in first — often the work account. Before composing, verify the active account: open mail with an explicit account (`https://mail.google.com/mail/?authuser=<application-address>`) and check the tab title or avatar shows the right address. The same applies to Google account pickers on forms (a "choose an account" screen before a Google Form or Drive upload): pick the application account, never the employer one.
- A wrong-account send from an employer address is the worst failure this system can make. When in doubt, stop and screenshot.

## Connector vs. browser
- **An email connector** (Gmail/Outlook MCP or similar) is best for reading, searching, drafting and text-only sends — it's what inbox routines use.
- **Attachments** are often better through the mail site in the controlled browser: connectors typically want inline base64, which is error-prone and heavy at resume sizes. Sending via the web UI also leaves the mail in the user's Sent folder as normal.

## Gmail web mechanics (controlled browser)
1. Open compose. Type the recipient, then commit the chip (Tab or Enter) before moving on — clicking Subject too early can land keystrokes in To.
2. Click the Subject field and type; click the body and type. Gmail autosaves ("Draft saved").
3. **Attachment:** don't click the paperclip — it opens the native file dialog, which blocks automation. Find the hidden `input[type=file][name="Filedata"]` in the DOM (tag it via JS with an aria-label if the accessibility tree can't see it) and use your file-upload tool on it. The attachment chip appears at the bottom of the compose window with the file size.
4. Verify recipient, subject, body and attachment in a screenshot, then Send. Confirm the "Message sent" toast before recording 'sent' in the ledger.

## Attaching a file to a Google Form
Forms with a file-upload question require the Drive picker. If the browser's active Google account is wrong, switch accounts first (the form reloads). One workaround when the picker won't take a local file: upload the file to Drive from Gmail ("Add to Drive" on a draft's attachment), then pick it from Drive in the form.

## Hygiene
- One thread per person; follow-ups go in the same thread.
- Subject lines name the role plainly: `Application: <role> — <name>`.
- Plain text, no tracking links, no images.
- Forwarding rules (e.g. a university mailbox forwarding to the main inbox) mean replies can arrive somewhere you don't watch; note in `me/profile.md` which addresses forward where, and flag any address that doesn't forward.
