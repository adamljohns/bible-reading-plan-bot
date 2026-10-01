import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from reading_audio import (
    resolve_audio_asset,
    validate_advertised_page,
    validate_audio_render,
)
from scripts import build_reading_page_from_md


class ReadingAudioContractTest(unittest.TestCase):
    def test_current_relational_names_win_with_legacy_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            audio_dir = Path(tmp)
            for current_slug, legacy_slug in (
                ("first", "husband"),
                ("second", "father"),
                ("third", "citizen"),
            ):
                legacy = audio_dir / f"2026-10-01-{legacy_slug}.mp3"
                current = audio_dir / f"2026-10-01-{current_slug}.mp3"
                legacy.touch()
                self.assertEqual(
                    resolve_audio_asset(audio_dir, "2026-10-01", current_slug), legacy
                )
                current.touch()
                self.assertEqual(
                    resolve_audio_asset(audio_dir, "2026-10-01", current_slug), current
                )

    def test_five_advertised_assets_cannot_render_fewer_players(self):
        with tempfile.TemporaryDirectory() as tmp:
            audio_dir = Path(tmp)
            date = "2026-10-01"
            watches = ["wisdom", "first", "second", "third", "peace"]
            for watch in watches:
                (audio_dir / f"{date}-{watch}.mp3").touch()

            with self.assertRaisesRegex(RuntimeError, "5 existing watch assets"):
                validate_audio_render(audio_dir, date, watches, "<html></html>")

            html = '<audio class="watch-audio"></audio>' * 5
            validate_audio_render(audio_dir, date, watches, html)

    def test_build_refuses_to_write_when_five_assets_render_zero_players(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            date = "2026-10-01"
            data_dir = repo / "data/readings"
            out_dir = repo / "docs/readings"
            audio_dir = repo / "docs/assets/audio/readings"
            data_dir.mkdir(parents=True)
            audio_dir.mkdir(parents=True)
            (data_dir / f"{date}.md").write_text("reading")
            for watch in ("wisdom", "first", "second", "third", "peace"):
                (audio_dir / f"{date}-{watch}.mp3").touch()

            with (
                patch.object(build_reading_page_from_md, "REPO", repo),
                patch.object(build_reading_page_from_md, "DATA_DIR", data_dir),
                patch.object(build_reading_page_from_md, "OUT_DIR", out_dir),
                patch.object(
                    build_reading_page_from_md,
                    "render_page",
                    return_value="<html></html>",
                ),
                self.assertRaisesRegex(RuntimeError, "5 existing watch assets"),
            ):
                build_reading_page_from_md.build_one(date)

            self.assertFalse((out_dir / f"{date}.html").exists())

    def test_ship_gate_ties_json_flags_urls_and_html_players_together(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            date = "2026-10-01"
            json_dir = repo / "docs/assets/readings"
            page_dir = repo / "docs/readings"
            json_dir.mkdir(parents=True)
            page_dir.mkdir(parents=True)
            slugs = ("wisdom", "first", "second", "third", "peace")
            watches = {
                slug: {
                    "has_audio": True,
                    "audio_url": (
                        f"https://usmcmin.org/assets/audio/readings/{date}-{slug}.mp3"
                    ),
                }
                for slug in slugs
            }
            (json_dir / f"{date}.json").write_text(json.dumps({"watches": watches}))
            page = "".join(
                f'<audio class="watch-audio"><source src="../assets/audio/readings/'
                f'{date}-{slug}.mp3"></audio>'
                for slug in slugs
            )
            (page_dir / f"{date}.html").write_text(page)
            self.assertEqual(validate_advertised_page(repo, date), 5)

            (page_dir / f"{date}.html").write_text("<html></html>")
            with self.assertRaisesRegex(RuntimeError, "5 advertised, 0 players"):
                validate_advertised_page(repo, date)


if __name__ == "__main__":
    unittest.main()
