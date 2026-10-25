import copy
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit_site import audit_page, collect_sitemaps
from check_backlinks import inspect
from import_transcript import import_file, parse_transcript, seconds
from source_overlap import aggregate
from web_checks import Client, Page, clean_url, google_noindex


class FixtureHandler(BaseHTTPRequestHandler):
    counts = {}
    robots_text = "User-agent: *\nDisallow: /private\n"

    def log_message(self, *_args):
        pass

    def do_GET(self):
        type(self).counts[self.path] = type(self).counts.get(self.path, 0) + 1
        origin = f"http://{self.headers['Host']}"
        code, kind, headers = 200, "text/html", {}
        body = "<html><head><title>Example</title></head><body><h1>Hello</h1></body></html>"
        if self.path == "/robots.txt":
            kind, body = "text/plain", self.robots_text
        elif self.path == "/index.xml":
            kind = "application/xml"
            body = f'<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>{origin}/pages.xml</loc></sitemap></sitemapindex>'
        elif self.path == "/pages.xml":
            kind = "application/xml"
            body = f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"><url><loc>{origin}/article</loc><image:image><image:loc>{origin}/picture.png</image:loc></image:image></url><url><loc>{origin}/preview/draft</loc></url></urlset>'
        elif self.path == "/redirect":
            code, headers = 301, {"Location": "/article"}
        elif self.path == "/external":
            code, headers = 302, {"Location": "https://other.invalid/"}
        elif self.path == "/preview/draft":
            headers = {"X-Robots-Tag": "googlebot: noindex, nofollow"}
            body = '<head><title>Draft</title><link rel="canonical" href="/learn/draft"></head><h1>Draft</h1>'
        elif self.path == "/rate":
            code, headers = 429, {"Retry-After": "60"}
        elif self.path == "/missing":
            code = 404
        elif self.path == "/oops":
            code = 503
        elif self.path == "/large":
            body = "x" * 3000
        self.send_response(code)
        self.send_header("Content-Type", kind)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body.encode())


class HttpChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), FixtureHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.host = f"127.0.0.1:{cls.server.server_port}"
        cls.origin = "http://" + cls.host

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()
        cls.server.server_close()

    def setUp(self):
        FixtureHandler.counts = {}
        FixtureHandler.robots_text = "User-agent: *\nDisallow: /private\n"
        self.client = Client([self.host], delay=0)

    def test_nested_sitemap_excludes_image_locs(self):
        maps = collect_sitemaps(self.client, [self.origin + "/index.xml"])
        self.assertTrue(maps["complete"])
        self.assertEqual(
            maps["urls"], [self.origin + "/article", self.origin + "/preview/draft"]
        )

    def test_unfinished_sitemap_does_not_claim_absence(self):
        maps = collect_sitemaps(self.client, [self.origin + "/index.xml"], limit=1)
        self.assertFalse(maps["complete"])
        row = audit_page(self.client, self.origin + "/article", maps)
        self.assertIsNone(row["in_supplied_sitemaps"])

    def test_redirect_and_scope(self):
        row = self.client.get(self.origin + "/redirect")
        self.assertEqual(row["status"], 200)
        self.assertEqual(row["url"], self.origin + "/article")
        self.assertEqual(row["redirects"][0]["status"], 301)
        self.assertEqual(
            self.client.get(self.origin + "/external")["error"], "out_of_scope_host"
        )

    def test_robots_disallow_and_unsupported_rules(self):
        self.assertEqual(
            self.client.get(self.origin + "/private")["error"], "robots_disallowed"
        )
        self.assertNotIn("/private", FixtureHandler.counts)
        FixtureHandler.robots_text = "User-agent: *\nDisallow: /*?private=*\n"
        other = Client([self.host], delay=0)
        self.assertEqual(
            other.get(self.origin + "/article")["error"], "robots_unsupported_rules"
        )

    def test_rate_limit_stops_host(self):
        self.assertEqual(self.client.get(self.origin + "/rate")["status"], 429)
        self.assertEqual(
            self.client.get(self.origin + "/article")["error"],
            "host_stopped_after_auth_or_rate_limit",
        )
        self.assertNotIn("/article", FixtureHandler.counts)

    def test_error_statuses_remain_distinct(self):
        for path, status in [("/missing", 404), ("/oops", 503)]:
            row = self.client.get(self.origin + path)
            self.assertEqual(row["status"], status)
            self.assertEqual(
                inspect(row, "https://example.com")["link_status"], "unavailable"
            )

    def test_budget_and_size_caps(self):
        client = Client([self.host], max_requests=1, delay=0)
        self.assertEqual(
            client.get(self.origin + "/article")["error"], "request_budget_exhausted"
        )
        client = Client([self.host], max_bytes=1000, delay=0)
        row = client.get(self.origin + "/large")
        self.assertTrue(row["truncated"])
        self.assertEqual(
            inspect(row, "https://example.com")["link_status"], "unavailable"
        )

    def test_preview_noindex_and_sitemap_conflict(self):
        maps = collect_sitemaps(self.client, [self.origin + "/pages.xml"])
        row = audit_page(self.client, self.origin + "/preview/draft", maps)
        self.assertTrue(row["google_noindex_observed"])
        self.assertIn("noindex_url_in_sitemap", row["findings"])
        self.assertIn("preview_in_sitemap", row["findings"])
        self.assertIsNone(row["google_indexed"])


class HtmlChecks(unittest.TestCase):
    def test_base_canonical_anchor_and_structured_data(self):
        html = '<head><base href="https://example.com/docs/"><title>A &amp; B</title><link rel="canonical" href="guide"><meta name="robots" content="index,follow"><script type="application/ld+json">{"@type":"Article"}</script></head><h1>Simple <b>guide</b></h1><a href="guide#part" rel="nofollow sponsored">Read <b>this</b></a>'
        row = Page(html, "https://example.com/").report()
        self.assertEqual(row["canonicals"][0]["url"], "https://example.com/docs/guide")
        self.assertEqual(row["links"][0]["text"], "Read this")
        self.assertEqual(row["h1"], ["Simple guide"])
        self.assertEqual(row["titles"], ["A & B"])
        self.assertTrue(row["jsonld"][0]["valid_json"])
        response = {
            "url": "https://example.com/",
            "status": 200,
            "headers": {"content-type": ["text/html"]},
            "body": html,
        }
        result = inspect(response, "https://example.com/docs/guide")
        self.assertEqual(result["link_status"], "present_in_raw_html")
        self.assertEqual(result["matches"][0]["rel"], ["nofollow", "sponsored"])
        self.assertEqual(
            inspect(response, "https://example.com/docs/guide?x=1")["link_status"],
            "not_found_in_raw_html",
        )

    def test_agent_scoped_robots(self):
        report = Page(
            '<meta name="bingbot" content="noindex">', "https://example.com"
        ).report()
        self.assertFalse(
            google_noindex(report, {"x-robots-tag": ["bingbot: noindex, nofollow"]})
        )
        self.assertTrue(
            google_noindex(report, {"x-robots-tag": ["googlebot: noindex"]})
        )

    def test_url_credentials_rejected(self):
        with self.assertRaises(ValueError):
            clean_url("https://user:secret@example.com")


def observation(sample_id="a", status="complete"):
    return {
        "sample_id": sample_id,
        "observed_at": "2026-10-14T09:00:00-05:00",
        "query_id": "q1",
        "query": "example",
        "panel_version": "v1",
        "method_id": "m1",
        "context_key": "c1",
        "cluster": "task",
        "surface": "google-organic",
        "target_depth": 2,
        "status": status,
        "results": [
            {"position": 1, "url": "https://example.com/a"},
            {"position": 2, "url": "https://example.com/a#part"},
        ],
    }


class OverlapChecks(unittest.TestCase):
    def test_incomplete_denominator_and_duplicate_sources(self):
        a, b, c = (
            observation(),
            observation("b", "incomplete"),
            observation("c", "blocked"),
        )
        b["results"] = [{"position": 1, "url": "https://other.example/"}]
        c["results"] = []
        group = aggregate([a, b, c])["groups"][0]
        self.assertEqual(group["eligible_observations"], 1)
        self.assertEqual(group["urls"][0]["observations"], 1)
        self.assertEqual(group["urls"][0]["frequency"], 1.0)
        self.assertEqual(group["partial_sightings"], {"https://other.example/": 1})

    def test_mixed_panels_and_no_overview(self):
        a, b, c = observation(), observation("b"), observation("c", "no-overview")
        b["panel_version"] = "v2"
        c.update(surface="google-ai", target_depth=None, results=[])
        groups = aggregate([a, b, c])["groups"]
        self.assertEqual(len(groups), 3)
        ai = next(g for g in groups if g["surface"] == "google-ai")
        self.assertEqual(ai["eligible_observations"], 0)

    def test_invalid_complete_duplicate_ids_and_window(self):
        a = observation()
        with self.assertRaises(ValueError):
            aggregate([a, copy.deepcopy(a)])
        a["results"] = a["results"][:1]
        with self.assertRaises(ValueError):
            aggregate([a])
        self.assertEqual(aggregate([observation()], date(2026, 10, 15))["groups"], [])


class TranscriptChecks(unittest.TestCase):
    def test_import_preserves_source_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "test.md"
            raw = "---\ntitle: Example\n---\nLicense notice\n[0:00] First.\n[0:02] Second.\n"
            source.write_text(raw)
            record = import_file(
                source,
                root / "out",
                "example",
                "Example",
                "https://example.com/audit",
                "2026-10-14",
                "partial",
                "Synthetic test fixture",
            )
            self.assertEqual(record["segments"], 2)
            self.assertFalse(record["coverage_verified_by_script"])
            self.assertEqual((root / "out/example/source.md").read_text(), raw)
            with self.assertRaises(ValueError):
                import_file(
                    source,
                    root / "out",
                    "example",
                    "Example",
                    "https://example.com/audit",
                    "2026-10-14",
                    "partial",
                    "Synthetic fixture",
                )

    def test_supported_cues_and_bad_times(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            fixtures = {
                "one.srt": "1\n00:00:01,200 --> 00:00:02,500\nExample.\n",
                "two.vtt": "WEBVTT\n\nid-1\n00:01.200 --> 00:02.500 align:start\nExample.\n",
                "three.json": json.dumps(
                    {"segments": [{"start": 1.2, "end": 2.5, "text": "Example."}]}
                ),
            }
            for name, body in fixtures.items():
                source = root / name
                source.write_text(body)
                self.assertEqual(parse_transcript(source)[0]["start"], 1.2)
            bad = root / "bad.json"
            bad.write_text(json.dumps([{"start": 10, "end": 2, "text": "Example."}]))
            with self.assertRaises(ValueError):
                parse_transcript(bad)
        for value in [float("inf"), float("nan"), -1, True, "1:75", "1:-1"]:
            with self.assertRaises(ValueError):
                seconds(value)


if __name__ == "__main__":
    unittest.main()
