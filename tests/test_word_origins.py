import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bin"))
from dictionary_origin_schema import validate_origin_fields

class WordOriginsTests(unittest.TestCase):
    def test_optional_schema_preserves_old_records(self):
        self.assertEqual([], validate_origin_fields({"slug": "old-entry"}))

    def test_schema_enums_urls_and_crosslists(self):
        self.assertEqual([], validate_origin_fields({"origin_category": "bible", "origin_label": "disputed", "origin_sources": ["https://example.com/source"], "origin_crosslist": ["military-language"]}))
        errors = validate_origin_fields({"origin_category": "legend", "origin_label": "maybe", "origin_sources": ["not-a-url"], "origin_crosslist": ["unknown-hub"]})
        self.assertEqual(4, len(errors))

    def test_weaponized_requires_visible_corruption_summary(self):
        errors = validate_origin_fields({"origin_category": "weaponized", "corruption_summary": "<em> </em>"})
        self.assertIn("weaponized entries require a non-empty corruption_summary", errors)
        crosslisted = validate_origin_fields({"origin_crosslist": ["weaponized-words"], "corruption_summary": ""})
        self.assertIn("weaponized entries require a non-empty corruption_summary", crosslisted)

    def test_hubs_render_categories_crosslist_and_corruption(self):
        fixture = ROOT / "tests/fixtures/word-origins-valid.json"
        with tempfile.TemporaryDirectory() as output:
            subprocess.run([sys.executable, str(ROOT / "bin/build_word_origin_hubs.py"), "--batch-glob", str(fixture), "--output-dir", output], cwd=ROOT, check=True, capture_output=True, text=True)
            origins = (Path(output) / "word-origins.html").read_text()
            military = (Path(output) / "military-language.html").read_text()
            weaponized = (Path(output) / "weaponized-words.html").read_text()
        for category in ("bible", "civil-war", "eponym", "civic", "americana", "trades"):
            self.assertIn(f'id="{category}"', origins)
        for category in ("marine", "navy", "army", "civil-war"):
            self.assertIn(f'id="{category}"', military)
        self.assertIn("fixture-origin-civil-war.html", origins)
        self.assertIn("fixture-origin-civil-war-military.html", origins)
        self.assertNotIn("fixture-origin-civil-war.html", military)
        self.assertIn("fixture-origin-civil-war-military.html", military)
        self.assertIn("Fixture corruption summary.", weaponized)
        self.assertIn("https://example.com/origins/weaponized", weaponized)

    def _build_with_overlay(self, overlay, output):
        tags = Path(output) / "tags.json"
        tags.write_text(json.dumps(overlay))
        return subprocess.run([sys.executable, str(ROOT / "bin/build_word_origin_hubs.py"), "--batch-glob", str(ROOT / "tests/fixtures/word-origins-valid.json"),
                               "--origin-tags", str(tags), "--output-dir", output], cwd=ROOT, capture_output=True, text=True)

    def test_overlay_tags_legacy_entry_onto_hub(self):
        overlay = {"tolerance": {"origin_category": "weaponized", "origin_label": "attested", "origin_sources": ["https://example.com/tolerance"], "corruption_summary": "Overlay tolerance summary."}}
        with tempfile.TemporaryDirectory() as output:
            result = self._build_with_overlay(overlay, output)
            self.assertEqual(0, result.returncode, result.stderr)
            weaponized = (Path(output) / "weaponized-words.html").read_text()
        self.assertIn('href="tolerance.html"', weaponized)
        self.assertIn("Overlay tolerance summary.", weaponized)

    def test_overlay_rejects_unknown_slug(self):
        with tempfile.TemporaryDirectory() as output:
            result = self._build_with_overlay({"not-a-real-entry": {"origin_category": "civic"}}, output)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("unknown slug", result.stderr)

    def test_overlay_weaponized_legacy_requires_summary(self):
        with tempfile.TemporaryDirectory() as output:
            result = self._build_with_overlay({"woke": {"origin_category": "weaponized"}}, output)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("weaponized entries require a non-empty corruption_summary", result.stderr)

    def test_batch_preflight_rejects_empty_weaponized_summary(self):
        fixture = ROOT / "tests/fixtures/word-origins-invalid-weaponized.json"
        result = subprocess.run(["bash", "bin/batch_pipeline.sh", str(fixture)], cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("weaponized entries require a non-empty corruption_summary", result.stdout + result.stderr)
        self.assertFalse((ROOT / "docs/dictionary/fixture-empty-weaponized.html").exists())

    def test_hub_slugs_are_reserved(self):
        reserved = {line.strip() for line in (ROOT / "data/dictionary-reserved-slugs.txt").read_text().splitlines() if line.strip() and not line.startswith("#")}
        self.assertEqual({"word-origins", "military-language", "weaponized-words"}, reserved)

if __name__ == "__main__":
    unittest.main()
