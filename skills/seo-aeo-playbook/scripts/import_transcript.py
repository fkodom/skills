#!/usr/bin/env python3
"""Import a local authorized transcript into a private, immutable source folder."""

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
from web_checks import clean_url, now, save_json


def seconds(value):
    if isinstance(value, bool):
        raise ValueError("Invalid timestamp")
    if isinstance(value, (int, float)):
        result = float(value)
    else:
        parts = str(value).replace(",", ".").split(":")
        if not 1 <= len(parts) <= 3:
            raise ValueError("Invalid timestamp")
        if len(parts) > 1 and (
            any(not p.isdigit() for p in parts[:-1])
            or any(not 0 <= float(p) < 60 for p in parts[1:])
        ):
            raise ValueError("Invalid clock timestamp")
        result = 0.0
        for part in parts:
            result = result * 60 + float(part)
    if result < 0 or result != result or result == float("inf"):
        raise ValueError("Timestamp must be finite and nonnegative")
    return result


def parse_transcript(path):
    text = path.read_text(encoding="utf-8-sig")
    suffix = path.suffix.lower()
    segments = []
    if suffix == ".json":
        data = json.loads(text)
        items = data.get("segments") if isinstance(data, dict) else data
        if not isinstance(items, list):
            raise ValueError(
                "JSON must be an array or {segments: [...]} with start/text and optional end"
            )
        for item in items:
            if not isinstance(item, dict):
                raise ValueError("Each segment must be an object")
            start = seconds(item["start"])
            end = seconds(item["end"]) if item.get("end") is not None else None
            body = item["text"]
            if not isinstance(body, str) or not body.strip():
                raise ValueError("Each segment needs nonempty text")
            segments.append({"start": start, "end": end, "text": body})
    elif suffix in {".srt", ".vtt"}:
        for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n")):
            lines = block.strip().splitlines()
            if not lines or lines[0].startswith(("WEBVTT", "NOTE", "STYLE", "REGION")):
                continue
            index = next((i for i, line in enumerate(lines) if "-->" in line), None)
            if index is None:
                raise ValueError("Subtitle block without cue timing")
            left, right = lines[index].split("-->", 1)
            if not right.strip():
                raise ValueError("Missing cue end")
            body = "\n".join(lines[index + 1 :])
            if not body.strip():
                raise ValueError("Empty subtitle cue")
            segments.append(
                {
                    "start": seconds(left.strip()),
                    "end": seconds(right.strip().split()[0]),
                    "text": body,
                }
            )
    elif suffix in {".md", ".txt"}:
        # Preserve all original text, including frontmatter/license notices, in source.ext.
        matches = list(re.finditer(r"(?m)^\[(\d+(?::\d{2}){1,2}(?:\.\d+)?)\]\s*", text))
        if matches:
            for i, match in enumerate(matches):
                body = text[
                    match.end() : matches[i + 1].start()
                    if i + 1 < len(matches)
                    else len(text)
                ].strip()
                segments.append(
                    {"start": seconds(match.group(1)), "end": None, "text": body}
                )
        elif text.strip():
            segments.append({"start": None, "end": None, "text": text})
    else:
        raise ValueError("Supported formats: JSON, SRT, VTT, MD and TXT")
    if not segments or any(not s["text"].strip() for s in segments):
        raise ValueError("No complete nonempty transcript segments found")
    starts = [s["start"] for s in segments if s["start"] is not None]
    if starts != sorted(starts):
        raise ValueError(
            "Out-of-order starts; inspect the source rather than silently sorting"
        )
    if any(s["end"] is not None and s["end"] < s["start"] for s in segments):
        raise ValueError("A cue ends before it starts")
    return segments


def import_file(
    source,
    root,
    slug,
    title,
    source_url,
    accessed_on,
    coverage,
    rights_note,
    license_file=None,
):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("Use a lowercase hyphenated slug")
    date.fromisoformat(accessed_on)
    source_url = clean_url(source_url)
    if not rights_note.strip():
        raise ValueError("Record the authorization/license basis")
    if coverage not in {"complete", "partial", "unknown"}:
        raise ValueError("Unsupported coverage declaration")
    segments = parse_transcript(source)
    if license_file and not license_file.is_file():
        raise ValueError("License file does not exist")
    target = root / slug
    if target.exists():
        raise ValueError(
            "Destination exists; preserve it and choose a versioned slug for a changed source"
        )
    target.mkdir(parents=True)
    shutil.copy2(source, target / ("source" + source.suffix.lower()))
    if license_file:
        shutil.copy2(license_file, target / ("LICENSE" + license_file.suffix.lower()))
    save_json(target / "segments.json", segments)
    last = max(
        (
            s["end"] if s["end"] is not None else s["start"]
            for s in segments
            if s["start"] is not None
        ),
        default=None,
    )
    record = {
        "title": title,
        "source_url": source_url,
        "accessed_on": accessed_on,
        "imported_at": now(),
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "coverage_declared": coverage,
        "coverage_verified_by_script": False,
        "rights_note": rights_note,
        "segments": len(segments),
        "last_observed_timestamp_seconds": last,
        "timestamp_warning": "Last cue start is not recording duration when end is absent.",
        "source_file": "source" + source.suffix.lower(),
    }
    save_json(target / "provenance.json", record)
    return record


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "local" / "transcripts",
    )
    ap.add_argument("--slug", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--source-url", required=True)
    ap.add_argument("--accessed-on", required=True, help="YYYY-MM-DD")
    ap.add_argument(
        "--coverage", required=True, choices=["complete", "partial", "unknown"]
    )
    ap.add_argument(
        "--rights-note", required=True, help="Local provenance, not a license grant"
    )
    ap.add_argument("--license-file", type=Path)
    args = ap.parse_args()
    try:
        record = import_file(
            args.input,
            args.out_dir,
            args.slug,
            args.title,
            args.source_url,
            args.accessed_on,
            args.coverage,
            args.rights_note,
            args.license_file,
        )
        print(
            json.dumps(
                {
                    "directory": str(args.out_dir / args.slug),
                    "segments": record["segments"],
                    "coverage": record["coverage_declared"],
                }
            )
        )
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
