# Search and AI visibility measurement

## Preserve the observation contract

Record exact query, timestamp, panel version, method version, language, requested country, actual browser/account context, displayed location, device, personalization label, surface and sampled depth. A signed-in browser with nonpersonalized parameters is not incognito or a national ranking. A provider's location setting is not necessarily the user's observed location.

For Google browser samples, request the agreed query unchanged, with explicit language/country/personalization settings when supported. Count primary organic web-result cards in displayed order. Exclude ads, AI citations, People Also Ask, related searches and embedded carousel items. Keep sitelinks with their parent. Preserve duplicate cards and pagination offsets. A top-20 contract is incomplete if only 13 cards can be inspected.

Track current domains, legacy domains, third-party mentions and unrelated namesakes separately. Record sponsored appearances without clicking the company's ads. Save raw titles and actual URLs, not only a final rank.

## Keep answer surfaces distinct

For an inline AI Overview, record presence and expand through ordinary controls. Capture answer text, citations and observable provider order. Distinguish recommendation, mention and citation. A missing Overview is `no-overview`, not evidence of a brand failing to appear in an answer. AI Mode is a separate surface and cannot substitute for an absent Overview.

For authorized agent samples, use a fresh isolated context, exact neutral prompt, no target-brand hints and current web sources. Record model/settings when known, every issued search phrase, raw retrieval URLs/order and verbatim answer. Do not selectively rerun a weak result. A tool's returned order is retrieval order; agent output is not measured consumer ChatGPT Search behavior. An installed connector or prior brand conversation contaminates a neutral selection experiment.

Google says ordinary SEO remains applicable to its AI features; no special AI schema or text file is required. A supporting page must be indexed and eligible for a snippet. Inclusion is not guaranteed. Google's AI-feature traffic is reported within Search Console's Web search data. [Primary guidance](https://developers.google.com/search/docs/appearance/ai-features).

## Analyze comparable samples

Group by panel version, method/context, surface, intent cluster and depth. Report completed, incomplete, blocked and no-answer counts. Absence denominators use complete eligible observations only. Preserve positive sightings in incomplete samples as partial evidence without treating them as comparable prevalence.

Calculate rolling frequency only over a stated time window and actual completed sample count. A rotation changes query composition; compare the same query set or report stratified clusters. Do not blend a new 72-question panel with an earlier six-query panel as one trend. Position changes should refer to the same surface and counting method; “not found within 20” is not position 21.

Use `source_overlap.py` for grouping URL/domain appearances. It deliberately does not compute a universal visibility score or scrape results. Normalize input using [the documented schema](tooling.md). Duplicate sample IDs are errors; duplicated sources count once per observation in overlap statistics while remaining in raw evidence.

## Learn from recurring sources

Inspect recurring pages across completed samples. Classify audience and source type manually, then determine what contribution might earn relevant attention. Source overlap identifies review candidates, not causality or Google's hidden algorithm. Keep neutral evidence collection ahead of topic selection and brand-specific experiments.
