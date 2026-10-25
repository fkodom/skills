"""Shared bounded, anonymous HTTP and HTML inspection; standard library only."""

import json
import re
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from urllib.robotparser import RobotFileParser

USER_AGENT = "SeoPlaybookAudit/1.0"


def now():
    return datetime.now(timezone.utc).isoformat()


def clean_url(value):
    p = urlsplit(value.strip())
    if (
        p.scheme.lower() not in {"http", "https"}
        or not p.hostname
        or p.username
        or p.password
    ):
        raise ValueError("Expected an HTTP(S) URL without embedded credentials")
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path or "/", p.query, ""))


def save_json(path, data):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Client:
    def __init__(
        self, hosts, max_requests=60, delay=0.3, timeout=15, max_bytes=2_000_000
    ):
        self.hosts = {h.lower() for h in hosts}
        self.max_requests, self.delay, self.timeout, self.max_bytes = (
            max_requests,
            delay,
            timeout,
            max_bytes,
        )
        self.requests = 0
        self.last_request = 0.0
        self.robots = {}
        self.stopped = set()
        self.opener = build_opener(NoRedirect())

    def _one(self, url):
        result = {
            "url": url,
            "observed_at": now(),
            "status": None,
            "error": None,
            "headers": {},
        }
        host = urlsplit(url).netloc.lower()
        if host not in self.hosts:
            result["error"] = "out_of_scope_host"
            return result
        if host in self.stopped:
            result["error"] = "host_stopped_after_auth_or_rate_limit"
            return result
        if self.requests >= self.max_requests:
            result["error"] = "request_budget_exhausted"
            return result
        time.sleep(max(0, self.delay - (time.monotonic() - self.last_request)))
        self.last_request = time.monotonic()
        self.requests += 1
        start = time.monotonic()
        try:
            try:
                response = self.opener.open(
                    Request(
                        url,
                        headers={
                            "User-Agent": USER_AGENT,
                            "Accept-Encoding": "identity",
                        },
                    ),
                    timeout=self.timeout,
                )
            except HTTPError as exc:
                response = exc
            with response:
                result["status"] = response.code
                result["headers"] = {
                    k.lower(): response.headers.get_all(k)
                    for k in (
                        "Content-Type",
                        "Location",
                        "X-Robots-Tag",
                        "Link",
                        "Retry-After",
                    )
                    if response.headers.get_all(k)
                }
                raw = response.read(self.max_bytes + 1)
                result["truncated"] = len(raw) > self.max_bytes
                charset = response.headers.get_content_charset() or "utf-8"
                try:
                    result["body"] = raw[: self.max_bytes].decode(
                        charset, errors="replace"
                    )
                except LookupError:
                    result["body"] = raw[: self.max_bytes].decode(
                        "utf-8", errors="replace"
                    )
                if response.code in {401, 403, 429}:
                    self.stopped.add(host)
        except (URLError, OSError, ValueError) as exc:
            result["error"] = type(exc).__name__ + ": " + str(exc)
        result["elapsed_ms"] = round((time.monotonic() - start) * 1000)
        return result

    def policy(self, url):
        p = urlsplit(url)
        origin = f"{p.scheme}://{p.netloc}"
        if origin not in self.robots:
            response = self.get(origin + "/robots.txt", respect_robots=False)
            parser = RobotFileParser()
            usable = not response.get("error") and not response.get("truncated")
            if usable and response["status"] == 200:
                lines = response.get("body", "").splitlines()
                parser.parse(lines)
                # stdlib does not implement Google's wildcard/longest-match semantics.
                unsupported = any(
                    re.match(r"\s*(allow|disallow)\s*:", line, re.I)
                    and re.search(r"[*$]", line.split("#", 1)[0].split(":", 1)[1])
                    for line in lines
                )
                state = "unsupported_rules" if unsupported else "parsed"
                wait = parser.crawl_delay(USER_AGENT)
                rate = parser.request_rate(USER_AGENT)
                self.delay = max(
                    self.delay,
                    wait or 0,
                    rate.seconds / rate.requests if rate and rate.requests else 0,
                )
            elif usable and response["status"] in {404, 410}:
                parser.parse([])
                state = "not_present"
            else:
                state = "unavailable"
            self.robots[origin] = (state, parser, response)
        return self.robots[origin]

    def get(self, url, respect_robots=True):
        current = clean_url(url)
        hops = []
        for _ in range(6):
            if urlsplit(current).netloc not in self.hosts:
                return {
                    "url": current,
                    "requested_url": url,
                    "status": None,
                    "error": "out_of_scope_host",
                    "redirects": hops,
                    "headers": {},
                }
            if respect_robots:
                state, parser, _response = self.policy(current)
                if state in {
                    "unavailable",
                    "unsupported_rules",
                } or not parser.can_fetch(USER_AGENT, current):
                    error = (
                        "robots_" + state
                        if state in {"unavailable", "unsupported_rules"}
                        else "robots_disallowed"
                    )
                    return {
                        "url": current,
                        "requested_url": url,
                        "status": None,
                        "error": error,
                        "redirects": hops,
                        "headers": {},
                    }
            result = self._one(current)
            result.update(requested_url=url, redirects=list(hops))
            if result["status"] not in {301, 302, 303, 307, 308} or result.get("error"):
                return result
            location = result["headers"].get("location", [None])[0]
            if not location:
                result["error"] = "redirect_without_location"
                return result
            hops.append(
                {"url": current, "status": result["status"], "location": location}
            )
            try:
                current = clean_url(urljoin(current, location))
            except ValueError:
                result["error"] = "invalid_redirect"
                return result
        result["error"] = "redirect_limit"
        return result


def response_metadata(response):
    return {k: v for k, v in response.items() if k != "body"}


class Page(HTMLParser):
    def __init__(self, html, url):
        super().__init__(convert_charrefs=True)
        self.url = url
        self.base = None
        self.titles, self.h1, self.canonicals, self.links = [], [], [], []
        self.meta, self.media, self.jsonld = [], [], []
        self.in_head = False
        self.capture = None
        self.anchor = None
        self.feed(html)

    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if tag == "head":
            self.in_head = True
        if tag == "base" and a.get("href") and self.base is None:
            self.base = urljoin(self.url, a["href"])
        if tag in {"title", "h1"}:
            self.capture = (tag, [])
        if tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self.capture = ("jsonld", [])
        if (
            tag == "link"
            and "canonical" in a.get("rel", "").lower().split()
            and a.get("href")
        ):
            self.canonicals.append({"href": a["href"], "in_head": self.in_head})
        if tag == "meta":
            self.meta.append(a)
        if tag == "a" and a.get("href"):
            self.anchor = {
                "href": a["href"],
                "rel": a.get("rel", "").lower().split(),
                "text": "",
            }
            self.links.append(self.anchor)
        if tag in {"video", "iframe", "img"}:
            self.media.append(
                {
                    "tag": tag,
                    "src": a.get("src"),
                    "alt": a.get("alt"),
                    "title": a.get("title"),
                }
            )

    def handle_data(self, data):
        if self.capture:
            self.capture[1].append(data)
        if self.anchor is not None:
            self.anchor["text"] += data

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
        if tag == "a":
            self.anchor = None
        if self.capture and (
            tag == self.capture[0] or tag == "script" and self.capture[0] == "jsonld"
        ):
            kind, data = self.capture
            raw = "".join(data)
            if kind == "jsonld":
                try:
                    self.jsonld.append({"valid_json": True, "value": json.loads(raw)})
                except ValueError:
                    self.jsonld.append({"valid_json": False})
            else:
                (self.titles if kind == "title" else self.h1).append(
                    " ".join(raw.split())
                )
            self.capture = None

    def resolved(self, href):
        try:
            return clean_url(urljoin(self.base or self.url, href))
        except ValueError:
            return None

    def report(self):
        robots = [
            {"agent": m.get("name", "").lower(), "content": m.get("content", "")}
            for m in self.meta
            if m.get("name", "").lower() in {"robots", "googlebot", "bingbot"}
        ]
        return {
            "titles": self.titles,
            "h1": self.h1,
            "canonicals": [
                {**c, "url": self.resolved(c["href"])} for c in self.canonicals
            ],
            "robots_meta": robots,
            "descriptions": [
                m.get("content", "")
                for m in self.meta
                if m.get("name", "").lower() == "description"
            ],
            "links": [
                {
                    **link,
                    "url": self.resolved(link["href"]),
                    "text": " ".join(link["text"].split()),
                }
                for link in self.links
            ],
            "media": self.media,
            "jsonld": self.jsonld,
        }


def is_html(response):
    return any(
        "text/html" in s.lower() or "application/xhtml+xml" in s.lower()
        for s in response.get("headers", {}).get("content-type", [])
    )


def google_noindex(report, headers):
    values = [
        m["content"]
        for m in report["robots_meta"]
        if m["agent"] in {"robots", "googlebot"}
    ]
    for value in headers.get("x-robots-tag", []):
        # Preserve all raw headers; this check recognizes generic/Googlebot noindex only.
        scope = None
        for token in value.lower().split(","):
            if ":" in token:
                left, right = token.strip().split(":", 1)
                if left not in {
                    "max-snippet",
                    "max-image-preview",
                    "max-video-preview",
                    "unavailable_after",
                }:
                    scope, token = left, right
            if scope in {None, "googlebot"}:
                values.append(token)
    return any(re.search(r"\b(noindex|none)\b", value, re.I) for value in values)
