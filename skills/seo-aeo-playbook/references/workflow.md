# Workflow and evaluation

## Save one coherent run

Use the project's timezone and a unique dated run ID. Resume unfinished stages instead of selectively resampling or producing duplicate drafts. Read the current plan and recent user decisions first. A convenient structure is:

```text
private-evidence/YYYY-MM-DD/run-id/
  search/       # raw browser/provider captures
  sources/      # fetched pages, screenshots, source metadata
  accounts/     # narrowly scoped GSC/analytics exports
  verification/ # technical and publication checks
strategy/
  query-panel.csv
  observations.jsonl
  backlog.md
  reviews.md
  briefs/
```

Public repositories should contain compact decisions, approved briefs and content, not private exports or bulk source copies. Stage explicit paths and inspect the staged file list before committing. Preserve local evidence when removing historical artifacts from Git.

## Order the recurring work

1. Collect agreed neutral search samples; log unavailable surfaces.
2. Reconcile current published content, drafts and actual release state.
3. Compare only equivalent observations and identify blockers.
4. Review a small rotating sample of primary competing/source pages.
5. Choose the next content or reputation action from evidence.
6. Draft only the authorized work, in the host project's UI and branch conventions.
7. Verify the result and deliver a concise dated report.

Scheduling requires a user request. Use the available scheduler and preserve existing prompts, ownership and notification preferences. This reference suggests a sequence, not an instruction to create or modify automations. A project can keep a small daily benchmark and a broader weekly rotation.

## Keep an improvement queue

Review up to three existing pages in a weekly strategy pass. Use [the improvement worksheet](../assets/page-improvement.csv) to record the observed query, reader job, missing answer, useful asset, owner and review window. Start with a page that already reaches the right audience but leaves a specific question unanswered; do not equate adding length with improving it. [Backpack](sources/backpack-laravel.md). This complements new content rather than creating a second treatment of the same question.

Keep separately tracked streams when useful: educational reference pages, promoted blog articles, product pages, earned-reference opportunities and technical issues. Each has different evidence and approval needs. Do not force one new article in every stream each day.

## Measure the right outcome

Separate release, discovery, indexed state, impressions, relevant visits and genuine conversions. Record Search Console dates, search type, filters and reporting delay. Record analytics property, timezone, landing page, channel/attribution scope and event definition. Missing account access means null fields, not zero traffic.

Compare matching periods and page age. Keep branded/nonbranded queries and paid/organic acquisition distinct where the data supports it. A recent content cohort needs time and comparable exposure; repeated checking does not increase the underlying sample size. A website-wide booking count cannot be inferred from Google Ads alone.

Before an experiment, name the change, expected reader benefit, primary outcome, observation window and competing explanations. Use before/after evidence cautiously: simultaneous content, bids, promotion and indexing changes prevent strong causal attribution.

## Deliver a readable review

Lead with what the evidence permits us to conclude. Include measurement date/context, a compact results table, missing coverage, completed work and one prioritized next step. Link the actual draft/PR/artifact, state what was tested, and avoid claiming that article volume or email sends caused search gains.
