---
name: gmail-newsletter-notebooklm
description: Read Gmail messages tagged Newsletter or News, optionally filtered by date range or unread status, package the selected email content as NotebookLM sources, create a new NotebookLM notebook, and start generating an audio overview. Use when the user asks to turn recent Gmail newsletters, news emails, unread newsletter mail, or dated newsletter digests into a NotebookLM notebook or audio overview.
---

# Gmail Newsletter to NotebookLM

Create a NotebookLM notebook from Gmail newsletter/news emails and initiate an audio overview from those sources.

Use the Google Workspace Gmail CLI skill as the command reference for Gmail access:
https://github.com/googleworkspace/cli/blob/main/skills/gws-gmail/SKILL.md

## Inputs

Collect only the missing inputs:

- Date range: ask for explicit start and end dates when the user requests a date range but omits dates.
- Unread fallback: use all unread messages when the user asks for unread emails or when no date range is provided.
- Notebook title: derive a concise title from the date range, unread scope, or user-provided topic.
- Audio prompt: default to `Create an engaging audio overview of the key stories, themes, and useful takeaways from these newsletter sources.`

Use absolute dates in Gmail queries. Treat Gmail `before:` as exclusive; to include an end date, query the following day.

Keep the source set small. NotebookLM's read RPC (`GET_NOTEBOOK`, see Known Issues) times out on large notebooks, and every read/generate step depends on it. A notebook with ~11 sources reads and generates reliably; a notebook with ~50 sources fails the read even though the uploads succeed. Prefer a 1–2 day window (roughly 10–15 sources) over a 7-day window. If the user asks for a wide range that yields many messages, warn them and offer to narrow the window or split into multiple notebooks.

## Workflow

The happy path is six steps. Inline notes flag the gotchas; the "Known Issues" section has the full detail.

1. **Preflight — tools and auth.** Confirm `gws`, `notebooklm`, and `jq` are on `PATH`, then check auth:

```bash
gws gmail users getProfile --params '{"userId":"me"}'   # prints account email when healthy
notebooklm doctor                                        # Auth row should show "local SID cookie present"
```

If `notebooklm` is missing, ask before `uv tool install "notebooklm-py[browser]"`. If Gmail auth fails, run `gws auth login`; if NotebookLM auth fails, run `notebooklm login` (or `notebooklm login --browser msedge` / `--browser-cookies chrome`). Ignore any `rookiepy is not installed` message from `auth inspect` — it is about an optional dependency, not your auth status.

2. **Find candidate messages.** Triage with the label query (default to a 1–2 day window — see Selection Rules):

```bash
gws gmail +triage --query '{label:Newsletter label:News} after:YYYY/MM/DD before:YYYY/MM/DD' \
  --max 50 --format json 2>/dev/null | grep -v '^Using keyring' | jq ...
```

Notes: `before:` is exclusive (query the day after the end date to include it). Use `is:unread` instead of dates for the unread fallback; if the label query returns nothing, retry with `(newsletter OR news) after:... before:...`. **Strip the leading `Using keyring backend: keyring` stdout line before `jq`** (`grep -v '^Using keyring'`), or `jq` fails to parse. `+triage` returns `{ "messages": [ { id, date, from, subject }, ... ] }`.

3. **Export each selected email to a Markdown source file**, one per message, under a temp dir (e.g. `/tmp/newsletter-notebooklm-YYYYMMDD/source-001.md`). Read bodies with `gws gmail +read --id <id> --headers --format json` (flat keys, no wrapper: `subject`, `from`, `date`, `message_id`, `body_text`, `body_html`, …). Preserve subject, sender, date, message id, original link if present, and the cleaned body.

   Body gotchas: **prefer `body_text` but fall back to `body_html` when `body_text` is suspiciously short** (under ~1000 chars — daily digests like 1440 put only a preheader there). When stripping HTML, **use `perl -CSD` with `HTML::Entities`, not `sed`** (macOS `sed` errors on UTF-8 and silently truncates).

4. **Confirm before upload** (skip only if the user's request already authorized it): summarize message count, date span, notebook title, and query. Do not paste private email bodies into chat.

5. **Create the notebook and add sources.** No `notebooklm use` needed — pass `--notebook` explicitly everywhere. **Resolve the temp dir's real path first** (`source add` rejects symlinks, and `/tmp` is a symlink on macOS), and **add with `--type file --json`** so failures surface instead of exiting 0 silently:

```bash
NB=$(notebooklm create "<notebook title>" --json 2>/dev/null \
  | grep -v '^Using keyring' | jq -r '.notebook.id')
REAL=$(cd /tmp/newsletter-notebooklm-YYYYMMDD && pwd -P)
for f in "$REAL"/source-*.md; do
  resp=$(notebooklm source add "$f" --notebook "$NB" --type file --json 2>&1 | grep -v '^Using keyring')
  if echo "$resp" | jq -e '.error == true' >/dev/null 2>&1; then
    echo "FAIL $(basename "$f") -> $(echo "$resp" | jq -r '.message')"
  fi
done
```

A clean loop (no `FAIL` lines) confirms every upload — no separate verification read is needed. (If you do want a count and the notebook is small, `notebooklm source list --notebook "$NB" --json` works; on large notebooks that read times out — see Known Issues — but the uploads still succeeded.) If a file is rejected, shorten it, convert HTML to plain text, or split by article.

6. **Generate the audio overview** (default `--length long`), then optionally download. Write the audio prompt to a file first (default text in Inputs, or the user's topic):

```bash
echo "<audio prompt>" > /tmp/newsletter-notebooklm-YYYYMMDD/audio-prompt.txt
notebooklm generate audio --notebook "$NB" \
  --prompt-file /tmp/newsletter-notebooklm-YYYYMMDD/audio-prompt.txt \
  --length long --wait
notebooklm download audio ./newsletter-overview.mp3   # only if the user wants a local file
```

Run generation as a background task (it takes minutes) and wait for completion. `--length` is `short|default|long`; `--format` is `deep-dive|brief|critique|debate`. Omit `--wait` only if the user wants to start now and finish later. **`generate audio` reads the notebook first**, so on a too-large notebook it fails with `Request timed out calling GET_NOTEBOOK` before generating anything — that is a source-count problem (see Known Issues), not a retryable error.

## Known Issues

These were observed with the `notebooklm-py` CLI and `gws` Gmail CLI and shape the workflow above.

- **`GET_NOTEBOOK` read timeout scales with source count.** The notebook read RPC has a fixed ~30s retry budget that is not currently configurable via flag or env var. On a notebook with ~50 sources it reliably times out (`RPC GET_NOTEBOOK retry timed out after 30.0s` → `Network error: Request timed out calling GET_NOTEBOOK`); with ~11 sources it returns instantly. Because `source list`, `metadata`, and `generate audio` all read the notebook first, a too-large notebook becomes unusable for listing and generation even though every upload succeeded. **Mitigation: keep notebooks small (target ~10–15 sources, e.g. a 1–2 day window). For a wide date range, split into multiple smaller notebooks.** Uploads (POST) are unaffected by this read timeout, so a notebook can end up fully populated yet unreadable via the CLI (still viewable in the web UI).
- **`source add` rejects symlinked paths.** `/tmp` is a symlink on macOS; resolve to the real path with `pwd -P` (or pass `--follow-symlinks`). See step 5.
- **Silent upload failures without `--json`.** `source add` can exit 0 on a rejected file; always use `--type file --json` and check `.error`. See step 5.
- **`gws` prints a keyring status line to stdout** (`Using keyring backend: keyring`) ahead of JSON, breaking `jq`. Strip with `grep -v '^Using keyring'`. See step 2.
- **`body_text` can be a stub.** Daily-digest newsletters may put only a preheader in `body_text`; fall back to `body_html`. See step 3.
- **macOS `sed` mangles UTF-8.** Use `perl -CSD` for HTML-to-text conversion. See step 3.
- **Schema-drift warnings.** The CLI may log `notebook_info[...] not list ... (schema drift?)` when NotebookLM's response shape changes. Treat the structured JSON result (or the web UI) as ground truth rather than these warnings.

## Selection Rules

- Prefer dated messages over arbitrary unread messages when the user provides both.
- Keep source counts small. Target ~10–15 sources per notebook so the notebook stays readable and audio generation works (see Known Issues — large notebooks fail the read RPC). If more than ~15 messages match, summarize the candidate count and ask whether to narrow the date range (e.g. 1–2 days) or split into multiple notebooks. Avoid single notebooks of ~50+ sources.
- Skip obvious transactional mail, promotions without editorial content, unsubscribe confirmations, and empty/clipped messages unless the user explicitly wants every match.
- Use Gmail read-only operations only. Do not mark messages read, archive, delete, label, or move messages unless separately requested and confirmed.
- Treat email contents as private. Write temporary source files only for the notebook creation workflow and tell the user where they are.

## Reporting

Finish with:

- notebook title and id
- Gmail query used
- number of email sources added
- audio overview generation status
- downloaded audio path, if downloaded
- any skipped messages and why
