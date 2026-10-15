---
name: seo-aeo-playbook
description: Diagnose organic search and AI-answer visibility, research buyer problems and competing pages, audit indexing signals, plan useful content and earned references, and measure changes with source-backed evidence. Use for SEO/AEO/GEO strategy, search visibility reviews, competitor backlink research, content backlogs, SEO Roast research, or turning search observations into a prioritized publishing and distribution workflow. Includes read-only site and backlink checks, completeness-aware source analysis, and local transcript imports.
---

# SEO and AI Search Playbook

Work from a reader's problem to a useful page, then to discovery, trust and a business outcome. Diagnose the limiting step before producing more content. Treat search results as observations, not access to a ranking algorithm.

## Start with the actual task

1. Read the project's current strategy, approved product facts, content inventory, query panel and recent decisions. Preserve existing permissions, teammate ownership and evidence rules. Ask only for missing facts that affect the work; continue independent research.
2. Establish the audience, business outcome, site/domain variants, target market, available accounts and requested scope. Read-only investigation and drafts do not imply permission to publish, contact people, buy links or change accounts.
3. Reuse prior evidence with its original date. Check for an existing run or draft before repeating it. Record inaccessible surfaces as unavailable, never as zero results.
4. Load only the relevant topic files below. Start with **diagnosis** for a strategy refresh, **technical** for an indexing complaint, or **backlinks** for reputation work.

When the user requests a complete corpus review, inventory the whole corpus and track each source. Do not substitute a sample without agreement. Report reviewed, unread and unavailable counts, and keep the research marked incomplete while requested sources remain unread.

## Topic map

| Task | Read | Produce |
| --- | --- | --- |
| Find the limiting step | [Diagnosis and priorities](references/diagnosis.md) | Evidence table and one next action |
| Find problems before a product search | [Reader intent and query panels](references/intent-research.md) | Clustered panel, page inventory, research questions |
| Inspect indexing, migrations or performance | [Technical discoverability](references/technical.md) | Exact URLs, findings, scope and verification |
| Draft or improve an article | [Content and product proof](references/content.md) | Brief, usable asset, supported copy, matched next step |
| Measure Google and agent visibility | [Search sampling](references/search-measurement.md) | Raw evidence and comparable observations |
| Find relevant independent references | [Backlinks and distribution](references/backlinks.md) | Qualified source-page register and approved next actions |
| Run an ongoing program | [Workflow and evaluation](references/workflow.md) | Dated review, update queue, outcome measures |
| Add transcripts or inspect audit claims | [Research sources](references/research-sources.md) | Provenance, coverage and timestamped notes |
| Run bundled tools | [Scripts and formats](references/tooling.md) | Reproducible local JSON reports |

## Use the evidence hierarchy

- **Observed:** exact page, status, screenshot, result card, account report or demonstrated behavior with date and scope.
- **Documented:** a current primary source describes the feature or requirement; this is not your own product test.
- **Hypothesis:** a proposed explanation or content opportunity, with the observation that would support or weaken it.
- **Outcome:** a verified release, indexed URL, live reference or attributed conversion. A submission, draft or pitch is not an outcome.

The [source index](references/sources/index.md) includes 28 SEO Roast audit notes and [primary platform guidance](references/sources/primary-guidance.md). Audit examples describe the recording date. Their claims about ranking causes are not controlled experiments. Consult current primary documentation when a recommendation depends on changing platform rules.

**Current research coverage: 28 of 50 cataloged transcripts reviewed; 22 remain incomplete (one preview-only, 21 unread).** The comprehensive review is incomplete. See the [coverage register](references/sources/coverage.csv); the source notes support provisional guidance, not a claim to have analyzed the entire library.

## Complete a useful work cycle

1. **Measure first.** Capture the agreed neutral samples or state the precise blocker. Keep branded exploration separate from neutral measurement.
2. **Diagnose.** Separate discovery, crawling, indexing, relevant retrieval, trust and conversion. Do not infer a broken deployment from a browser-navigation error.
3. **Choose.** Inspect existing pages and actual competing source pages. Prefer improving an existing answer when a new page would repeat its reader job.
4. **Make something useful.** Pair the answer with a worked example, decision tool, demonstration or documented original evidence. Identify a relevant distribution opportunity.
5. **Verify.** Check facts, links, publication state and rendering as appropriate. A technical pass cannot certify search indexing or claim ranking gains.
6. **Report.** State what changed, what remains uncertain, the one highest-value next step, and when/how to reassess it. Preserve the underlying evidence privately.

## Tools

The scripts use Python 3.10+ and the standard library. They require no paid SEO account. Run from this skill directory; use `--help` for each command.

```bash
python3 scripts/audit_site.py --site https://example.com --sitemap https://example.com/sitemap.xml --out local/site-audit.json
python3 scripts/source_overlap.py --input local/observations.jsonl --out local/source-overlap.json
python3 scripts/check_backlinks.py --input assets/backlink-candidates.csv --out local/backlinks.json
python3 scripts/import_transcript.py --help
python3 -m unittest discover -s scripts/tests -v
```

The tools make bounded anonymous GET requests or process local files. They do not query Google, impersonate Googlebot, request indexing, send outreach or publish content. Use documented browser controls or an authorized data provider for search/account data. Read its actual parameters, pricing, freshness and coverage; keep provider estimates separate from first-party measurements.

## Evidence and transcripts

Keep raw responses, account exports, screenshots, transcripts and generated reports in the ignored `local/` directory or an explicit private evidence location. Do not commit credentials or private prospect records. The repository contains original research notes and source links, **not full third-party transcripts or video files**.

The importer accepts locally supplied JSON, SRT, VTT or text exports for which the user has appropriate rights. It preserves the source file, timestamps, a hash and completeness declaration in one folder per recording. See [research sources](references/research-sources.md) for the supported refresh process and current SEO Roast access limits. Do not silently substitute a short preview for a complete transcript.

## Keep conclusions honest

- A page accessible to us is not necessarily indexed; an indexing request is not indexing.
- An AI citation, brand mention and recommendation are different observations. Mention order is not a quality ranking.
- A backlink-tool score is not Google's score. Relevant independent pages matter more to this investigation than a raw link count.
- An answer outside the blog feed still needs useful public content and sensible discovery paths if intended for search.
- Do not manufacture product superiority, reviews, statistics, customer permission or unavailable integrations to fill a comparison table.
- Apply the host project's cadence and editorial rules. This skill does not impose a daily article quota or create an automation on its own.
