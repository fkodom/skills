#!/usr/bin/env python3
"""Aggregate local search-source observations without inventing absent ranks."""

import argparse
from collections import Counter, defaultdict
from datetime import date, datetime
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit
from web_checks import clean_url, now, save_json

SURFACES = {"google-organic", "google-ai", "agent-retrieval", "agent-answer"}
STATES = {"complete", "incomplete", "blocked", "no-overview", "no-answer"}
GROUP_FIELDS = (
    "panel_version",
    "method_id",
    "context_key",
    "surface",
    "cluster",
    "target_depth",
)


def validate(row):
    for key in (
        "sample_id",
        "observed_at",
        "query_id",
        "query",
        "panel_version",
        "method_id",
        "context_key",
        "cluster",
    ):
        if not isinstance(row.get(key), str) or not row[key].strip():
            raise ValueError(f"Missing or invalid {key}")
    stamp = datetime.fromisoformat(row["observed_at"].replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        raise ValueError("observed_at needs a timezone")
    if row.get("surface") not in SURFACES or row.get("status") not in STATES:
        raise ValueError("Unsupported surface/status")
    if row["status"] == "no-overview" and row["surface"] != "google-ai":
        raise ValueError("no-overview belongs only to google-ai")
    depth = row.get("target_depth")
    if depth is not None and (type(depth) is not int or depth < 1):
        raise ValueError("target_depth must be a positive integer or null")
    if row["surface"] in {"google-organic", "agent-retrieval"} and depth is None:
        raise ValueError("Retrieval observations require target_depth")
    if not isinstance(row.get("results"), list):
        raise ValueError("results must be a list")
    for item in row["results"]:
        clean_url(item["url"])
    if row["status"] in {"blocked", "no-overview", "no-answer"} and row["results"]:
        raise ValueError(
            "Unavailable/no-answer states cannot contain results; use incomplete for partial evidence"
        )
    if row["surface"] == "google-organic":
        positions = [r.get("position") for r in row["results"]]
        if any(type(p) is not int for p in positions) or positions != list(
            range(1, len(positions) + 1)
        ):
            raise ValueError(
                "Organic positions must be sequential; preserve duplicate cards"
            )
    if (
        row["status"] == "complete"
        and depth is not None
        and len(row["results"]) < depth
    ):
        raise ValueError("Complete sample is shallower than target_depth")
    return stamp


def aggregate(rows, since=None, until=None):
    groups, ids = defaultdict(list), set()
    for row in rows:
        stamp = validate(row)
        if row["sample_id"] in ids:
            raise ValueError(f"Duplicate sample_id: {row['sample_id']}")
        ids.add(row["sample_id"])
        # Window uses each explicitly offset timestamp's calendar date, as documented.
        if since and stamp.date() < since or until and stamp.date() > until:
            continue
        groups[tuple(row.get(k) for k in GROUP_FIELDS)].append(row)
    output = []
    for key, observations in sorted(groups.items(), key=lambda pair: str(pair[0])):
        counts = Counter(r["status"] for r in observations)
        urls, hosts, partial = Counter(), Counter(), Counter()
        eligible = counts["complete"]
        for row in observations:
            sampled = (
                row["results"][: row["target_depth"]]
                if row.get("target_depth")
                else row["results"]
            )
            found = {clean_url(item["url"]) for item in sampled}
            if row["status"] == "complete":
                urls.update(found)
                hosts.update({urlsplit(url).hostname for url in found})
            elif row["status"] == "incomplete":
                partial.update(found)

        def ranked(counter):
            return [
                {
                    "value": value,
                    "observations": count,
                    "eligible_observations": eligible,
                    "frequency": count / eligible if eligible else None,
                }
                for value, count in sorted(counter.items(), key=lambda p: (-p[1], p[0]))
            ]

        ordered = sorted(
            observations,
            key=lambda r: datetime.fromisoformat(
                r["observed_at"].replace("Z", "+00:00")
            ),
        )
        output.append(
            {
                **dict(zip(GROUP_FIELDS, key)),
                "status_counts": dict(counts),
                "eligible_observations": eligible,
                "query_sample_counts": dict(
                    Counter(
                        r["query_id"] for r in observations if r["status"] == "complete"
                    )
                ),
                "observed_from": ordered[0]["observed_at"],
                "observed_to": ordered[-1]["observed_at"],
                "urls": ranked(urls),
                "hosts": ranked(hosts),
                "partial_sightings": dict(partial),
            }
        )
    return {
        "generated_at": now(),
        "window": {
            "since": str(since) if since else None,
            "until": str(until) if until else None,
            "date_basis": "calendar date in each supplied timestamp offset",
        },
        "groups": output,
        "limits": [
            "Frequencies describe completed observations, not market share or ranking causality.",
            "Hosts are exact hostnames, not registrable domains; www and subdomains remain separate.",
            "Compare windows only after matching their query composition and measurement contract.",
            "No-overview, no-answer, blocked and incomplete samples are excluded from absence denominators.",
        ],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--since", type=date.fromisoformat)
    ap.add_argument("--until", type=date.fromisoformat)
    args = ap.parse_args()
    try:
        if args.since and args.until and args.since > args.until:
            raise ValueError("since must not be after until")
        rows = [
            json.loads(line)
            for line in Path(args.input).read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        data = aggregate(rows, args.since, args.until)
        save_json(args.out, data)
        print(json.dumps({"report": args.out, "groups": len(data["groups"])}))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
