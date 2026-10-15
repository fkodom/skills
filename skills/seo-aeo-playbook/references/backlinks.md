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

## Review competitor link exports

Before qualifying prospects, review competitor exports with [the link-review worksheet](../assets/competitor-link-review.csv). Record provider, capture date, root-domain or page scope, filters, row limit and completeness. An overlap between several competitors is a useful lead, not proof that a publisher will accept us. A truncated export cannot establish that a link is missing. Group repeated source URLs and domains without erasing their individual destinations.

## Identify why the link exists

Inspect the source and destination before turning an export row into outreach:

| Observed mechanism | What to establish |
| --- | --- |
| Editorial citation | Which reader question the linked resource answers |
| Vendor profile or resource list | Eligibility, accuracy and who controls the description |
| Partner, affiliate or sponsored reference | The actual relationship and required disclosure/qualification |
| Public product output or attribution | Public-sharing intent, permission and the useful destination |
| API, script or embedded resource | Whether a reader-facing anchor exists at all |

[Rallly](sources/rallly.md) illustrates public outputs; [Sheet2API](sources/sheet2api.md) exposes the risk of mistaking API references for editorial opportunities. A technical reference alone proves neither a current customer relationship nor an endorsement. Google generally extracts crawlable links from anchors with an `href`; inspect rendered content when necessary. [Google link guidance](https://developers.google.com/search/docs/crawling-indexing/links-crawlable).

Do not make private product records public to generate links. Do not insert hidden or keyword-rich widget links or require unqualified ranking links in exchange for a service. [Google's link-spam examples](https://developers.google.com/search/docs/essentials/spam-policies#link-spam).

## Qualify the next action

Start from `assets/backlink-candidates.csv`. Track source URL, target URL, topic/reader question, contribution, source category, contact route, owner, approval status, lifecycle status, last action and next action. Keep private messages and personal contact exports outside public repositories.

Suggested lifecycle: `candidate → qualified → prepared → approved → sent → replied → live_verified`, with `held`, `declined` and `bounced` alternatives. These are distinct facts; never count sent pitches as earned references. Dedupe at both page and organization level before outreach, and check teammate ownership and prior threads.

## Offer something worth citing

A useful pitch explains why this audience benefits and offers one concrete asset: an original worked example, a technically accurate diagram, a fair test procedure, a factual correction or a customer-approved case study. Disclose affiliation and allow editorial judgment. Do not require praise, an exact anchor or a followed link.

For competitor-backlink outreach, prefer a useful addition to an existing relevant article, comparison or resource list. Name the exact URL and section, ask directly to be considered for inclusion, and supply a short factual addition plus one supporting demo or resource. Ask what the editor needs to evaluate it and whether the process involves fees or partner terms. A ready-to-use addition reduces the work required of the publisher; a vague offer to contribute a future article does not make the same request.

Confirm that the page is suitable for multiple providers or for the proposed example. A dedicated review of a competitor is research context, not automatically an insertion opportunity. Distinguish measured page visibility from a page merely found in a backlink export. Propose a new article, podcast or webinar when there is a specific reader benefit, an invitation or explicit user preference; explain why the extra work is justified instead of making it the default.

Describe the specific missing step, example or evidence the destination supplies. “Our article is longer” is not a reader benefit. Inspect links to the competing guide itself, not just domain totals, as illustrated by [SparkSocial](sources/sparksocial.md) and [Liftosaur](sources/liftosaur.md). [Popp World](sources/poppworld.md) also shows why a supplier relationship may not be reproducible through an editorial pitch.

Drafting is not permission to send. Use existing user authorization where it covers the recipient, channel, identity and message scope. Ask only when the necessary authorization is missing. Do not create new batches or recurring follow-ups just because the research produces candidates.

Avoid purchasing ranking credit, excessive exchanges, paid unqualified links, indiscriminate directory submissions and spam comments. Paid sponsorships require appropriate link qualification and a business rationale independent of a ranking guarantee. [Google spam policies](https://developers.google.com/search/docs/essentials/spam-policies#link-spam) and [link attributes](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links).

## Verify the real placement

Fetch the public source URL and inspect the actual anchor, destination, surrounding context and rel values. Check publication date where available, redirect behavior and whether the company is actually described accurately. A footer, login destination, mention without a link or client-rendered widget should not be silently recorded as an independent editorial reference.

`check_backlinks.py` reports exact target anchors in fetched HTML. A blocked/non-HTML/failed response is unavailable, not absent. An absent raw-HTML anchor needs rendered verification before a final conclusion. Google indexing remains unknown unless separately evidenced; the script cannot certify indexing or link equity.

## Evaluate outcomes

Treat reputation building as an ongoing program with bounded individual conversations. When recurring work is authorized, use the project's cadence to check replies, keep promises, qualify new source pages and maintain live references. Track the latest inbound/outbound message, next action and date, follow-up count, approval scope, owner and any stop reason. A daily check does not justify a daily email.

As a starting cadence for an unanswered cold pitch, propose one concise follow-up after 7–10 business days, subject to the user's send permissions and the publisher's stated timeline. Then park the conversation unless the recipient responds or there is a substantive new reason to reconnect. Respect declines, opt-outs, delivery failures and teammate ownership; do not switch channels to restart the same pitch. Review paused opportunities when there is new evidence, rather than recycling the original request indefinitely.

Track useful replies, verified live references, referral visits and genuine attributed actions separately. Review source quality, accurate entity description and reader fit before expanding volume. Proprietary DR/DA metrics may help compare candidates within one tool; they are not Google's scoring system and should not drive the plan alone. [Ahrefs DR definition](https://ahrefs.com/seo/glossary/domain-rating).
