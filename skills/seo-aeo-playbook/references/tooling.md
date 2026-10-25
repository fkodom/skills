# Scripts and data contracts

Run commands from this skill directory with Python 3.10+. Runtime uses only the standard library. All outputs are local JSON; the tools do not publish, authenticate, change settings or send messages. Use `local/` for generated files; it is ignored by Git. If choosing another destination, keep private data outside version control.

## Bounded site audit

```bash
python3 scripts/audit_site.py \
  --site https://example.com \
  --url https://example.com/learn/example \
  --sitemap https://example.com/sitemap-index.xml \
  --max-pages 20 --max-requests 60 \
  --out local/site-audit.json
```

- Explicit site host is in scope; add `--allow-host www.example.com` when a verified redirect or sitemap uses that host. No automatic cross-domain crawl.
- Requests are anonymous GETs, with a declared audit user agent, 15-second timeout, 2 MB response limit and default 0.3-second spacing. No credentials or session cookies are read. A 401/403/429 stops further requests to that host. No retry loop or CAPTCHA bypass.
- Robots rules are fetched first and interpreted conservatively using Python's parser. Unavailable or unsupported rules stop page fetching; this is not a Googlebot simulation or a complete robots compliance engine.
- Sitemap traversal follows at most ten XML maps and records up to 5,000 page URLs. Gzip-compressed maps are not supported. Pending, failed or truncated maps make coverage incomplete. Missing membership then stays null, rather than false.
- Site, explicit URLs, then sitemap URLs are inspected in that order, up to the page/request budget. Link targets are inventoried but not recursively fetched. Query parameters and trailing slashes remain distinct.
- Reports include status/redirect metadata, HTML head canonicals, raw HTTP Link headers, title, H1, meta description, robots directives, anchors, media and JSON-LD syntax. Header canonicals and structured-data eligibility require manual interpretation.
- Findings are review prompts, not an SEO score. A missing H1 is not a guaranteed ranking block. Exact production status and intended state matter. `google_indexed` is always null.

`inspection: unavailable` includes HTTP errors, access blocks, non-HTML, network errors and truncated bodies. It does not mean the URL is absent from Google. The report can be successfully written with unavailable observations; inspect its fields rather than treating exit 0 as a clean bill of health.

## Verify supplied backlinks

Use `assets/competitor-link-review.csv` for the manual export review described in [backlinks](backlinks.md). It records acquisition scope and link mechanisms; it is not an outreach list or a backlink-checker input. Copy qualified source/destination pairs into the candidate schema below. Keep completed worksheets private.

Populate a private copy of `assets/backlink-candidates.csv`. Only `source_url` and `target_url` are required for the checker; other columns support human qualification.

```bash
python3 scripts/check_backlinks.py \
  --input local/candidates.csv --max-pages 10 \
  --out local/backlink-check.json
```

Deduplicates identical source/target pairs, fetches each selected source once, and reports anchor text, actual resolved URL and rel tokens. Matching is exact after removing URL fragments and normalizing scheme/host case. It does not equate www/apex, remove query parameters or follow target redirects. Add verified destination variants as separate pairs when needed.

`present_in_raw_html` is positive anchor evidence. `not_found_in_raw_html` still needs rendered-page review. `unavailable` is not absence. The checker neither certifies Google indexing nor calculates link equity or editorial independence.

## Analyze search source overlap

Normalize existing captures into JSONL; retain originals unchanged. `assets/observation.example.jsonl` is explicitly fictional and is only a format demonstration.

Required fields:

| Field | Contract |
| --- | --- |
| `sample_id` | Unique capture ID; duplicate IDs fail validation |
| `observed_at` | ISO timestamp with offset; use the project's timezone consistently |
| `query_id`, `query` | Stable ID and exact phrase |
| `panel_version` | Query panel definition |
| `method_id` | Counting/retrieval protocol version |
| `context_key` | Stable locale/device/account/model configuration key; raw context can be stored in `context` |
| `cluster` | Intent group |
| `surface` | `google-organic`, `google-ai`, `agent-retrieval`, or `agent-answer` |
| `target_depth` | Positive integer for organic/retrieval samples; null allowed for answer surfaces |
| `status` | `complete`, `incomplete`, `blocked`, `no-overview`, or `no-answer` |
| `results` | Ordered objects with HTTP(S) `url`; organic cards also need sequential `position` starting at 1 |

For Google AI use citation URLs, preserving answer/provider order separately in raw evidence. For agent-answer use answer citation URLs, not guessed provider URLs. For retrieval use the actual returned results. This aggregator measures sources, not whether their brands were recommended. Save recommendation/mention/citation labels and observable ordinals alongside the raw answer.

```bash
python3 scripts/source_overlap.py \
  --input local/observations.jsonl \
  --since 2026-10-08 --until 2026-10-14 \
  --out local/overlap-week.json
```

Windows are inclusive using each timestamp's supplied offset calendar date. Groups separate panel, method, context, surface, cluster and depth. URL/host frequency counts one appearance per complete observation; exact duplicate cards remain in the input. Partial sightings are reported separately. Missing Overviews and blocked/incomplete samples do not enter absence denominators. Complete samples shallower than requested depth fail validation.

Hosts are exact hostnames, not registrable domains. Compare windows only with matching query composition; use the per-query sample counts to check. This is not a rank tracker or a claim about national search share.

## Import local transcripts

See [source refreshes](research-sources.md) for authorization and coverage. Accepted formats:

- JSON array, or `{ "segments": [...] }`; each segment has `start`, `text`, optional `end`. Numeric timestamps are **seconds**, not milliseconds. Times may also be `MM:SS` or `HH:MM:SS.mmm` strings. Other API wrappers require an explicit, reviewed local transformation.
- SRT/VTT cue blocks; identifiers and VTT settings are accepted. Cue text is preserved, including tags.
- Markdown with `[m:ss]` or `[h:mm:ss]` lines, including licensed pack exports. Original frontmatter/notices remain in `source.md`.
- Plain text without timing; coverage and recording duration remain unverified.

Never import a login page or rate-limit message as a transcript. The script does not infer provenance or license rights from a file extension. It refuses an existing slug, invalid or reversed times and unsupported JSON shapes. A local declaration of complete coverage does not prove it. Keep the original license with the source.

## Maintenance checks

```bash
python3 -m unittest discover -s scripts/tests -v
python3 scripts/source_overlap.py --input assets/observation.example.jsonl --out local/example-overlap.json
```

Tests use a local fixture server and synthetic transcript/search data; no third-party account or live search is needed. They cover blocked responses, redirects, sitemap depth, canonical/noindex parsing, backlink matching, incomplete denominators, mixed measurement contracts and transcript preservation. Run the host's skill validator too when available.
