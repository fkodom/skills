# Technical discoverability

## Verify the exact URL

Start with a direct GET and a fresh browser navigation to the production URL. Record status, redirect chain, final URL, response time, content type, title, canonical, robots directives and visible content. A tool error, blocked fetch, JavaScript transition or stale preview is not evidence of a production 404. A 200 response with an error page can also be misleading; inspect the body.

Use `audit_site.py` for a bounded anonymous HTML pass. It does not render JavaScript, simulate Googlebot, measure Core Web Vitals, or confirm Google's indexing. Validate findings in the browser and Search Console where available.

## Check publication intent

| Intended state | Expected checks |
| --- | --- |
| Public article | Working canonical URL, useful visible text, appropriate index controls, discovery links, sitemap entry where used |
| Unapproved preview | Explicit noindex, absent from sitemap and public content exports; no accidental links from public feeds |
| Moved page | Direct permanent redirect to the relevant replacement; update internal links and sitemap |
| Duplicate variant | Consistent preferred URL signals; do not request indexing of every alternate |
| Removed content | Intentional removal status and corrected links; avoid redirecting every missing URL to the home page |

Canonical is a signal, not a guarantee of Google's choice. Inspect user-declared and Google-selected canonical, last crawl, fetch result and indexing reason. Keep HTTP/HTTPS, www/apex, trailing slashes, parameters and old domains distinct until verified. A sitemap should list preferred public URLs, not every route the application can generate.

Primary checks: [canonical consolidation](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls), [sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview), [robots meta tags](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag).

## Diagnose a site move

Use [the migration worksheet](../assets/migration-review.csv). Start with old URLs that had useful traffic or references, then map each to its intended replacement. Record the observed chain, final content, canonical and Search Console crawl date. Include legacy help, pricing and app subdomains; a login redirect may hide a formerly public answer. See [Nomad List](sources/nomadlist.md) and [Friends & Fables](sources/fables.md).

For a permanent move, test direct permanent redirects to corresponding replacements, refresh internal links and preferred sitemap URLs, and monitor old and new locations. Use [Google's migration guidance](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes). Do not prescribe another domain move merely because old results remain visible.

Two checks prevent false diagnoses:

- A relative `Location` header is valid HTTP. Resolve it against the request URI and check the resulting chain; do not flag it solely for lacking a hostname. [RFC 9110 section 10.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#name-location).
- A request with a Googlebot user-agent string is not verified Googlebot. Check relevant Search Console evidence and identify crawler requests through published IP ranges or reverse-and-forward DNS verification before attributing a block to Google's crawler. [Google request verification](https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests).

## Separate crawl and index

Robots.txt controls crawling; blocking a URL there is not a reliable substitute for an accessible noindex directive. A successful live inspection establishes current accessibility, not existing inclusion in the index. Request indexing for an important changed URL when authorized, once the page is ready; repeated requests are not a speed strategy. Maintain the sitemap rather than uploading a new copy for every post. [URL Inspection](https://support.google.com/webmasters/answer/9012289) and [recrawl requests](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl).

For “crawled, currently not indexed,” examine duplication, usefulness, preferred canonical, discovery and crawl dates before rewriting infrastructure. Report the exact reason instead of collapsing every exclusion into a technical error.

## Inspect the reader experience

Check mobile layout, main text availability, meaningful headings, real anchor links, images with relevant alternatives and media that actually supports the explanation. JSON-LD must match visible facts; its presence alone does not earn a result feature. Video embedding does not establish video indexing. [Video guidance](https://developers.google.com/search/docs/appearance/video).

Image metadata can supply creator, credit and licensing details and eligibility for specific image features. It does not establish a ranking increase. Keep image-search observations separate from web results and match metadata to the actual asset. [Google image metadata](https://developers.google.com/search/docs/appearance/structured-data/image-license-metadata).

Keep lab diagnostics separate from real-user field measurements. Record device, URL versus origin scope, test date and the field-data window. Compare deploy dates to that window before concluding an old issue remains unfixed. A faster lab run does not demonstrate that a rolling population metric has recovered. [PageSpeed data](https://developers.google.com/speed/docs/insights/v5/about).

Google recommends descriptive, concise titles and intelligible URLs; neither a fixed character count nor an exact-match slug is a ranking requirement. Keep useful live URLs unless a move has a concrete benefit and a migration plan. [Title guidance](https://developers.google.com/search/docs/appearance/title-link) and [URL guidance](https://developers.google.com/search/docs/crawling-indexing/url-structure).

## Close a finding

Each technical issue needs the exact affected URL, observed evidence, intended behavior, change and post-change verification. A green automated report means only that its bounded checks passed. Indexing, rendering, analytics and conversion remain separate questions.
