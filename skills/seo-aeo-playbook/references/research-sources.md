# Research sources and transcript refreshes

## What this skill contains

The [source index](sources/index.md) contains original timestamped notes from nine SEO Roast audits reviewed on October 14, 2026. The preceding research read their complete available transcripts, inspected nine selected audit images and one paused PostEverywhere frame near 8:00. It did not watch every video end to end. Full transcript files were not archived or included in this repository.

That was incomplete coverage of the user's request. The catalog inspected on that date listed 50 audits. Track all 50 in [coverage.csv](sources/coverage.csv), leaving the 41 unread entries explicit. A successful import is not a completed reading, and a transcript reading is not a full-video review. Reconcile those coverage dimensions separately before claiming completion.

Keep three source layers separate: the speaker's words, the visual material actually inspected, and our interpretation. A chapter summary may be machine-generated and may overstate the spoken claim. Prefer the exact timestamped evidence when they disagree. Old audit metrics remain historical; never report them as current competitor facts.

## Add complete local transcripts

For user-owned recordings or authorized exports, use the local importer. It does not retrieve website sessions, download videos or purchase material.

```bash
python3 scripts/import_transcript.py \
  --input /private/authorized-export.md \
  --slug example-audit-2026-10-14 \
  --title 'Example audit' \
  --source-url https://example.com/audit \
  --accessed-on 2026-10-14 \
  --coverage complete \
  --rights-note 'User-supplied export authorized for internal analysis' \
  --license-file /private/LICENSE.md
```

Each recording gets its own directory under ignored `local/transcripts/`, containing the unchanged source, normalized segments and provenance. The source preserves notices and frontmatter. `--coverage complete` records the operator's declaration; the tool cannot prove the export includes the entire recording. Compare opening/final cues, stated duration and source UI before making that declaration. Keep gaps and unknown coverage explicit.

## SEO Roast access facts

As checked October 14, 2026, the [transcript terms](https://seoroast.com/terms-of-service#transcripts) distinguish limited website reading from licensed collection. The [transcript pack](https://seoroast.com/transcripts) supplies individual Markdown files for internal analysis and excludes redistribution. Keep supplied files and their license local; public skill notes do not replace or reproduce the pack.

The user identified `GET https://seoroast.com/api/transcripts/posteverywhere` as an authenticated endpoint returning 200. This research did not independently archive that response or establish a stable API contract. A successful authenticated request is not a redistribution license. The signed-in UI later enforced an hourly full-transcript limit. Do not rotate accounts, replay cookies or bypass that limit.

If a future license expressly permits programmatic retrieval, use the documented access method and current schema, stop on 401/403/429, respect the stated limit and keep credentials out of logs. Prefer a provider export when available. No authenticated bulk downloader is bundled here.

## A repeatable research pass

1. Inspect the public audit index and compare source URLs/recording dates with the catalog. Do not repeatedly redownload unchanged material.
2. Obtain an authorized local export or read the available source normally. Record exact coverage and acquisition method. Do not upgrade a 90-second preview to “full transcript.”
3. Hash/import the export if provided. Preserve prior versions rather than overwriting them.
4. Read the relevant sections and inspect the corresponding page/video frame through normal controls. Note what was actually viewed and what was not.
5. Write a short original note: timestamp, observed issue, proposed explanation, useful application, limitation and current primary-source check.
6. Update a topic guide only if the new evidence changes a decision or adds a reusable method. Avoid accumulating the same generic tip in multiple files.
7. Validate local links, script behavior and staged paths. Never stage `local/` or a project's private evidence directory.

## Source-backed, not source-led

Consulting examples are useful for generating hypotheses. They do not establish causal ranking weights, universal conversion lifts or guaranteed AI recommendations. Record the audited URL, tool/provider, root/subdomain scope, date, filters and unit before interpreting a metric. A toolbar showing a large platform's authority cannot be attributed to a vendor mentioned on that platform.
