#!/usr/bin/env python3
"""Audit a bounded set of public HTML pages; never certifies search indexing."""

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit
from web_checks import (
    Client,
    Page,
    clean_url,
    google_noindex,
    is_html,
    now,
    response_metadata,
    save_json,
)


def collect_sitemaps(client, roots, limit=10, url_limit=5000):
    queue, seen, urls, reports = list(roots), set(), [], []
    complete = True
    while queue and len(seen) < limit:
        url = clean_url(queue.pop(0))
        if url in seen:
            continue
        seen.add(url)
        response = client.get(url)
        row = response_metadata(response)
        reports.append(row)
        if (
            response.get("error")
            or response["status"] != 200
            or response.get("truncated")
        ):
            complete = False
            continue
        try:
            root = ET.fromstring(response.get("body", ""))
            kind = root.tag.rsplit("}", 1)[-1]
            if kind not in {"sitemapindex", "urlset"}:
                raise ValueError("Expected sitemapindex or urlset")
            expected = "sitemap" if kind == "sitemapindex" else "url"
            for item in root:
                if item.tag.rsplit("}", 1)[-1] != expected:
                    continue
                loc = next(
                    (c.text for c in item if c.tag.rsplit("}", 1)[-1] == "loc"), None
                )
                if not loc:
                    raise ValueError("Missing loc")
                target = clean_url(loc)
                if kind == "sitemapindex":
                    if target not in seen and target not in queue:
                        queue.append(target)
                elif len(urls) < url_limit:
                    urls.append(target)
                else:
                    complete = False
                    row["url_limit_reached"] = True
        except (ET.ParseError, ValueError) as exc:
            row["parse_error"] = str(exc)
            complete = False
    return {
        "complete": complete and not queue and bool(roots),
        "reports": reports,
        "urls": list(dict.fromkeys(urls)),
        "pending_sitemaps": queue,
    }


def audit_page(client, url, sitemap):
    response = client.get(url)
    result = response_metadata(response)
    found = clean_url(url) in sitemap["urls"]
    result["in_supplied_sitemaps"] = (
        True if found else False if sitemap["complete"] else None
    )
    result["google_indexed"] = None
    result["findings"] = []
    if (
        response.get("error")
        or response.get("truncated")
        or response["status"] != 200
        or not is_html(response)
    ):
        result["inspection"] = "unavailable"
        return result
    page = Page(response["body"], response["url"])
    result["html"] = page.report()
    result["inspection"] = "raw_html_only"
    facts = result["html"]
    result["google_noindex_observed"] = google_noindex(facts, response["headers"])
    for key, flag in [
        ("titles", "missing_title"),
        ("h1", "missing_h1"),
        ("descriptions", "missing_description"),
    ]:
        if not any(facts[key]):
            result["findings"].append(flag)
    canonicals = [c["url"] for c in facts["canonicals"] if c["in_head"]]
    if not canonicals:
        result["findings"].append("no_html_head_canonical_check_http_link_header")
    elif len(canonicals) > 1:
        result["findings"].append("multiple_html_canonicals")
    elif canonicals[0] != clean_url(response["url"]):
        result["findings"].append("canonical_points_elsewhere_verify_intent")
    if result["google_noindex_observed"] and found:
        result["findings"].append("noindex_url_in_sitemap")
    if "/preview/" in urlsplit(url).path:
        if found:
            result["findings"].append("preview_in_sitemap")
        if not result["google_noindex_observed"]:
            result["findings"].append("preview_missing_observed_noindex")
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--site", required=True)
    ap.add_argument(
        "--url", action="append", default=[], help="Explicit page; repeatable"
    )
    ap.add_argument(
        "--sitemap",
        action="append",
        default=[],
        help="Sitemap or index URL; repeatable",
    )
    ap.add_argument(
        "--allow-host",
        action="append",
        default=[],
        help="Additional exact host[:port] for redirects/sitemaps",
    )
    ap.add_argument("--max-pages", type=int, default=20)
    ap.add_argument("--max-requests", type=int, default=60)
    ap.add_argument("--delay", type=float, default=0.3)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    if (
        not 1 <= args.max_pages <= 100
        or not 1 <= args.max_requests <= 500
        or args.delay < 0
    ):
        ap.error("Use 1–100 pages, 1–500 requests and a nonnegative delay")
    try:
        site = clean_url(args.site)
        client = Client(
            [urlsplit(site).netloc, *args.allow_host], args.max_requests, args.delay
        )
        maps = collect_sitemaps(client, args.sitemap)
        candidates = list(
            dict.fromkeys([site, *map(clean_url, args.url), *maps["urls"]])
        )
        selected = candidates[: args.max_pages]
        pages = [audit_page(client, url, maps) for url in selected]
        data = {
            "observed_at": now(),
            "site": site,
            "scope": "anonymous raw HTML; no JS rendering or indexing certification",
            "requests": client.requests,
            "sitemaps": maps,
            "pages": pages,
            "uninspected_page_count": len(candidates) - len(selected),
            "robots": {
                origin: {"state": state, **response_metadata(response)}
                for origin, (state, _parser, response) in client.robots.items()
            },
        }
        save_json(args.out, data)
        print(
            json.dumps(
                {
                    "report": args.out,
                    "inspected": len(pages),
                    "unavailable": sum(p["inspection"] == "unavailable" for p in pages),
                    "requests": client.requests,
                }
            )
        )
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
