# Backlinks and distribution

## Start with pages and people

Use actual recurring search/AI source pages, relevant industry resources, genuine product integrations, customer-approved stories and reputable directories. Competitor backlink tools can expand discovery, but their indexes and authority scores have provider-specific coverage. A search result containing a company's name is not proof of a hyperlink.

Qualify the exact source page: audience fit, topical context, maintenance, editorial independence, linked destination and what would improve that page for its reader. Distinguish a vendor-controlled profile, customer reference, publisher article, partner listing, forum post and sitewide footer. A relevant nofollow mention can still send qualified readers; a followed link does not guarantee ranking value.

## Select the right destination

Inspect the destination distribution in a competitor export: homepage, product page, comparison, guide, app/login or customer subdomain. Many referring domains to one home page do not show that a particular guide has strong discovery. Compare relevant pages as well as domains. For each qualified prospect, choose the page that answers its readers' question; do not route every request to the homepage.

The [Tolt audit](sources/tolt.md), especially 12:00–15:00 and 16:00–27:00, makes this concrete: inspect where links land, then read recurring community and publisher pages for the question they serve. Record the **source page → reader question → useful contribution → destination page** for each prospect. This is a research method, not evidence that copying a competitor's links reproduces its rankings.

Keep two discovery opportunities separate:

- **Our own result:** a page on the company's domain appears for the query.
- **A third-party result:** an eligible marketplace listing, publisher article or directory lets that audience discover the company.

A company's mention inside a high-ranking directory is not its own-domain ranking. Inspect the listing's eligibility, accuracy and destination, and record whether it is vendor-controlled or independently written. Correct a renamed company's existing profile rather than creating misleading duplicate identities. [Blitz](sources/blitz-seo-1.md) and [Memo Cards](sources/memo-cards.md).

## Keep a usable register

Start from `assets/backlink-candidates.csv`. Track source URL, target URL, topic/reader question, contribution, source category, contact route, owner, approval status, lifecycle status, last action and next action. Keep private messages and personal contact exports outside public repositories.

Suggested lifecycle: `candidate → qualified → prepared → approved → sent → replied → live_verified`, with `held`, `declined` and `bounced` alternatives. These are distinct facts; never count sent pitches as earned references. Dedupe at both page and organization level before outreach, and check teammate ownership and prior threads.

## Offer something worth citing

A useful pitch explains why this audience benefits and offers one concrete asset: an original worked example, a technically accurate diagram, a fair test procedure, a factual correction or a customer-approved case study. Disclose affiliation and allow editorial judgment. Do not require praise, an exact anchor or a followed link.

Drafting is not permission to send. Use existing user authorization where it covers the recipient, channel, identity and message scope. Ask only when the necessary authorization is missing. Do not create new batches or recurring follow-ups just because the research produces candidates.

Avoid purchasing ranking credit, excessive exchanges, paid unqualified links, indiscriminate directory submissions and spam comments. Paid sponsorships require appropriate link qualification and a business rationale independent of a ranking guarantee. [Google spam policies](https://developers.google.com/search/docs/essentials/spam-policies#link-spam) and [link attributes](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links).

## Verify the real placement

Fetch the public source URL and inspect the actual anchor, destination, surrounding context and rel values. Check publication date where available, redirect behavior and whether the company is actually described accurately. A footer, login destination, mention without a link or client-rendered widget should not be silently recorded as an independent editorial reference.

`check_backlinks.py` reports exact target anchors in fetched HTML. A blocked/non-HTML/failed response is unavailable, not absent. An absent raw-HTML anchor needs rendered verification before a final conclusion. Google indexing remains unknown unless separately evidenced; the script cannot certify indexing or link equity.

## Evaluate outcomes

Track useful replies, verified live references, referral visits and genuine attributed actions separately. Review source quality, accurate entity description and reader fit before expanding volume. Proprietary DR/DA metrics may help compare candidates within one tool; they are not Google's scoring system and should not drive the plan alone. [Ahrefs DR definition](https://ahrefs.com/seo/glossary/domain-rating).
