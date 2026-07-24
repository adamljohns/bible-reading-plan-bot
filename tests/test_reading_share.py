#!/usr/bin/env python3
"""Regression tests for explicit sharing controls on generated daily readings."""
import importlib.util
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GENERATOR = REPO / "scripts" / "build_reading_page_from_md.py"

spec = importlib.util.spec_from_file_location("reading_page", GENERATOR)
assert spec is not None and spec.loader is not None
reading_page = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reading_page)


class DailyReadingShareTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = (REPO / "data" / "readings" / "2026-07-24.md").read_text()
        body = re.sub(r"<!--.*?-->", "", source, flags=re.S)
        version = reading_page.parse_reading_version(source)
        cls.html = reading_page.render_page("2026-07-24", body, version=version)

    def test_all_view_has_explicit_share_control(self):
        first_watch = self.html.index('<section class="watch')
        all_button = self.html.index('data-share-hash="all"')
        self.assertLess(all_button, first_watch)
        self.assertIn("Share all of today’s readings", self.html)

    def test_each_watch_has_its_own_share_control(self):
        for slug in ("wisdom", "husband", "father", "citizen", "peace"):
            section = re.search(
                rf'<section class="watch watch-{slug}".*?</section>',
                self.html,
                flags=re.S,
            )
            self.assertIsNotNone(section, slug)
            assert section is not None
            self.assertIn(f'data-share-hash="{slug}"', section.group(0))
            self.assertIn("Share this reading", section.group(0))

    def test_share_handler_uses_native_share_with_clipboard_fallback(self):
        self.assertIn("navigator.share", self.html)
        self.assertIn("navigator.clipboard.writeText", self.html)
        self.assertIn("shareUrl.search = ''", self.html)
        self.assertIn("shareUrl.hash = '#' + slug", self.html)
        self.assertIn("textArea.setSelectionRange", self.html)
        self.assertIn("history.replaceState", self.html)

    def test_share_controls_are_accessible_buttons(self):
        buttons = re.findall(r'<button\b[^>]*class="share-reading[^>]*>', self.html)
        self.assertEqual(6, len(buttons))
        for button in buttons:
            self.assertIn('type="button"', button)
            self.assertIn('aria-label="', button)
        statuses = re.findall(r'<span\b[^>]*class="share-status"[^>]*>', self.html)
        self.assertEqual(6, len(statuses))
        for status in statuses:
            self.assertIn('role="status"', status)
            self.assertIn('aria-live="polite"', status)

    def test_every_published_2026_reading_has_six_share_controls(self):
        pages = sorted((REPO / "docs" / "readings").glob("2026-??-??.html"))
        self.assertEqual(365, len(pages))
        missing = []
        for page in pages:
            count = page.read_text().count('class="share-reading')
            if count != 6:
                missing.append(f"{page.name}: {count}")
        self.assertEqual([], missing, "published pages without six share controls")


if __name__ == "__main__":
    unittest.main()
