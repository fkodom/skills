# Nomad List

Source: https://seoroast.com/nomadlist — recorded January 31, 2025; reviewed October 15, 2026. Read all 181 available transcript segments through 20:38. No selected-image or full-video review in this pass.

- **3:00–9:00:** Start migration diagnosis with old valuable URLs, their expected replacements and the observed redirect path. Compare historically successful pages with their current versions.
- **9:00–13:00:** Check source HTML, rendered headings and account-dependent views separately. A changed browser experience may not describe the crawler's experience.
- **16:00–20:38:** Investigate crawl-access failures using Search Console and relevant request logs. The audit's spoofed Googlebot user-agent test is a lead, not proof that verified Googlebot is blocked.

Technical correction: the claim around 5:00–6:00 that relative Location headers are invalid conflicts with HTTP semantics. Resolve the header against the request URL and test the destination. See [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-location) and [Google crawler verification](https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests). Neither a missing robots.txt file nor a blocked diagnostic request alone establishes the cause of a traffic loss. The promised recovery is unproven.
