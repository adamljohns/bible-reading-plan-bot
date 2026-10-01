import sys
import unittest
from datetime import date
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from generate_reading_local import enforce_watch_opening


class WatchOpeningTest(unittest.TestCase):
    def test_relational_openings_preserve_passage_specific_continuation(self):
        cases = {
            "first": (
                "🕖 0700 First Watch — The Husband's Post",
                "Brother, consider Paul's voyage.",
                "Brother, stand your post",
            ),
            "second": (
                "🕚 1100 Second Watch — The Father's Charge",
                "The covenant promise steadies the house.",
                "Brother, take up the charge",
            ),
            "third": (
                "🕒 1500 Third Watch — The Citizen's Stand",
                "Brother, Rome's magistrate fears the verdict.",
                "Brother, stand firm",
            ),
        }
        for key, (header, original, prefix) in cases.items():
            with self.subTest(key=key):
                text = f"{header}\n\n{original}\n\n📖 Scripture — Test 1:1\n"
                repaired = enforce_watch_opening(text, key, date(2026, 10, 2))
                continuation = original.removeprefix("Brother, ")
                self.assertIn(f"{prefix}: {continuation}", repaired)
                self.assertIn("📖 Scripture — Test 1:1", repaired)

    def test_effective_date_does_not_touch_october_first(self):
        text = "🕖 0700 First Watch — The Husband's Post\n\nBrother, original opening.\n"
        self.assertEqual(
            text,
            enforce_watch_opening(text, "first", date(2026, 10, 1)),
        )

    def test_stand_firm_without_colon_is_not_mistaken_for_canonical_opening(self):
        text = "🕒 1500 Third Watch — The Citizen's Stand\n\nBrother, stand firm in Christ.\n"
        repaired = enforce_watch_opening(text, "third", date(2026, 10, 2))
        self.assertIn("Brother, stand firm: stand firm in Christ.", repaired)

    def test_repair_is_idempotent(self):
        text = "🕒 1500 Third Watch — The Citizen's Stand\n\nBrother, stand firm: Keep faith in prison.\n"
        self.assertEqual(
            text,
            enforce_watch_opening(text, "third", date(2026, 10, 2)),
        )


if __name__ == "__main__":
    unittest.main()
