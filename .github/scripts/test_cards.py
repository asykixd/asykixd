import unittest

from cards import hero, newest, parse_release
from tui import THEMES


class ReleaseTest(unittest.TestCase):
    def test_parse_release_keeps_tag_and_date(self):
        data = {"tag_name": "v1.2.0", "published_at": "2026-10-08T22:16:52Z", "prerelease": False}
        self.assertEqual(parse_release(data), ("v1.2.0", "2026-10-08"))

    def test_newest_picks_latest_publish_date(self):
        rel = {"evelin": ("v1.1.9", "2026-10-08"), "uroboros": ("v1.0.0", "2026-10-04")}
        self.assertEqual(newest(rel), ("evelin", ("v1.1.9", "2026-10-08")))

    def test_hero_shows_fetched_release(self):
        rel = {"evelin": ("v2.0.0", "2027-01-02"), "uroboros": ("v1.3.0", "2026-12-01")}
        svg = hero(THEMES["dark"], rel)
        self.assertIn("v2.0.0", svg)
        self.assertIn("2027-01-02", svg)
        self.assertIn("2 released", svg)


if __name__ == "__main__":
    unittest.main()
