# Gmail Newsletter to NotebookLM

This skill lets Codex read Gmail messages labeled `Newsletter` or `News`, create a NotebookLM notebook from the selected emails, and start an audio overview.

The setup below is for humans. Once the tools are installed and authenticated, the agent should rely on `SKILL.md`.

## Prerequisites

- A Google account with Gmail and NotebookLM access.
- Gmail labels named `Newsletter` and/or `News`, or messages that can be found by newsletter/news search terms.
- `jq` for inspecting JSON output.
- `uv` if you want the recommended NotebookLM CLI install command.

## Install Google Workspace CLI

Install `gws` using one of the upstream-supported methods:

```bash
brew install googleworkspace-cli
```

or:

```bash
npm install -g @googleworkspace/cli
```

You can also download a prebuilt binary from:
https://github.com/googleworkspace/cli/releases

Verify:

```bash
gws --help
gws gmail --help
```

## Authenticate Gmail

For a first-time local setup, run:

```bash
gws auth setup
gws auth login --scopes gmail
```

`gws auth setup` uses Google Cloud project configuration. If it cannot complete automatically, follow the manual OAuth setup in the `gws` README and create a Desktop OAuth client.

Smoke test:

```bash
gws gmail users getProfile --params '{"userId":"me"}'
gws gmail +triage --query '{label:Newsletter label:News} is:unread' --max 5 --format json | jq
```

If your labels have spaces or different names, update the prompt you give Codex. Gmail search labels are case-insensitive but label names must match your mailbox.

## Install NotebookLM CLI

Install the NotebookLM CLI:

```bash
uv tool install "notebooklm-py[browser]"
```

Install the Playwright Chromium browser used by the login flow:

```bash
uvx playwright install chromium
```

Verify:

```bash
notebooklm --help
```

## Authenticate NotebookLM

Use the login flow that matches your environment:

```bash
notebooklm login
```

For organizations that require Microsoft Edge for SSO:

```bash
notebooklm login --browser msedge
```

To reuse cookies from an already logged-in Chrome profile:

```bash
notebooklm login --browser-cookies chrome
```

Verify:

```bash
notebooklm auth inspect
notebooklm create "NotebookLM CLI Smoke Test"
```

If the smoke-test notebook is created successfully, you can delete it in NotebookLM.

## Prepare Gmail

This skill works best when newsletters are labeled before Codex runs.

Common options:

- Create Gmail filters that apply `Newsletter` to recurring editorial emails.
- Apply `News` to news digests you want included.
- Leave messages unread if you want the default "all unread newsletter/news emails" behavior.
- Use a date range when you want a bounded digest, for example `June 1, 2026 through June 15, 2026`.

## Example Prompts

Unread fallback:

```text
Use the Gmail Newsletter to NotebookLM skill to create an audio overview from all unread Gmail messages labeled Newsletter or News.
```

Date range:

```text
Use the Gmail Newsletter to NotebookLM skill for Gmail Newsletter or News emails from June 1, 2026 through June 15, 2026. Title the notebook "June News Digest" and generate the audio overview.
```

Custom audio direction:

```text
Create a NotebookLM audio overview from unread newsletter emails. Make the audio focus on market trends, AI product updates, and anything that changes my priorities this week.
```

## Privacy Notes

The workflow exports selected email bodies into temporary Markdown files before uploading them as NotebookLM sources. Codex should summarize the message count, date span, query, and notebook title before upload unless your prompt already clearly authorizes the upload.

The skill is read-only for Gmail. It should not mark messages read, archive, delete, label, or move messages unless you separately ask and confirm.

## Troubleshooting

If `gws` is missing:

```bash
brew install googleworkspace-cli
```

If Gmail auth fails with an access-blocked error, make sure your Google account is added as a test user on the OAuth consent screen for the Google Cloud project used by `gws`.

If Gmail returns no messages, test the query directly in Gmail search, then retry with the exact label names or ask Codex to fall back to:

```text
(newsletter OR news) after:YYYY/MM/DD before:YYYY/MM/DD
```

If NotebookLM login opens the wrong account, inspect available accounts and rerun login with the appropriate profile/account flags:

```bash
notebooklm auth inspect
notebooklm login --browser-cookies 'chrome::Profile 1'
```

If `notebooklm login` says `playwright install` is required but your shell says `playwright: command not found`, run Playwright through `uvx`:

```bash
uvx playwright install chromium
```

Then retry:

```bash
notebooklm login
```

If NotebookLM rejects a source, ask Codex to shorten the email export, remove clipped boilerplate, convert HTML to plain text, or split a large digest into separate source files.

## References

- Google Workspace CLI: https://github.com/googleworkspace/cli
- Gmail CLI skill: https://github.com/googleworkspace/cli/blob/main/skills/gws-gmail/SKILL.md
- NotebookLM: https://notebooklm.google
