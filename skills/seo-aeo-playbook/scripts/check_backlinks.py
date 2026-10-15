#!/usr/bin/env python3
"""Verify exact target anchors on supplied source pages, without sending outreach."""

import argparse
import csv
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit
from web_checks import (
    Client,
    Page,
    clean_url,
    is_html,
    now,
    response_metadata,
    save_json,
)


def inspect(response, target_url):
    data = {
        "fetch": response_metadata(response),
        "target_url": clean_url(target_url),
        "google_indexed": None,
        "matches": [],
    }
    if (
        response.get("error")
        or response.get("truncated")
        or response["status"] != 200
        or not is_html(response)
    ):
        data["link_status"] = "unavailable"
        return data
    page = Page(response["body"], response["url"]).report()
    data["matches"] = [
        link for link in page["links"] if link["url"] == data["target_url"]
    ]
    data["source_robots_meta"] = page["robots_meta"]
    data["link_status"] = (
        "present_in_raw_html" if data["matches"] else "not_found_in_raw_html"
    )
    data["needs_manual_review"] = (
        "Verify surrounding context, independence, rendered links, redirect destinations and search indexing separately."
    )
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="CSV with source_url and target_url")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-pages", type=int, default=10)
    ap.add_argument("--allow-host", action="append", default=[])
    args = ap.parse_args()
    if not 1 <= args.max_pages <= 100:
        ap.error("Use 1–100 pages")
    try:
        with Path(args.input).open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        pairs, seen = [], set()
        for row in rows:
            pair = (clean_url(row["source_url"]), clean_url(row["target_url"]))
            if pair not in seen:
                pairs.append(pair)
                seen.add(pair)
        selected_urls = list(dict.fromkeys(p[0] for p in pairs))[: args.max_pages]
        client = Client(
            [urlsplit(url).netloc for url in selected_urls] + args.allow_host,
            max_requests=args.max_pages * 8,
        )
        responses = {url: client.get(url) for url in selected_urls}
        results = [
            {"source_url": source, **inspect(responses[source], target)}
            for source, target in pairs
            if source in responses
        ]
        save_json(
            args.out,
            {
                "observed_at": now(),
                "results": results,
                "uninspected_pairs": len(pairs) - len(results),
                "requests": client.requests,
                "limits": "Exact URLs excluding fragments; no query stripping, www folding or destination requests. Raw HTML only; no indexing claim.",
            },
        )
        print(
            json.dumps(
                {
                    "report": args.out,
                    "pairs_checked": len(results),
                    "requests": client.requests,
                }
            )
        )
    except (ValueError, KeyError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
