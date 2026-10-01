"""Shared daily-reading audio filename compatibility and render gates."""
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


_SLUGS = {
    "wisdom": ("wisdom",),
    "morning_wisdom": ("wisdom",),
    "first": ("first", "husband"),
    "first_watch": ("first", "husband"),
    "husband": ("first", "husband"),
    "second": ("second", "father"),
    "second_watch": ("second", "father"),
    "father": ("second", "father"),
    "third": ("third", "citizen"),
    "third_watch": ("third", "citizen"),
    "citizen": ("third", "citizen"),
    "peace": ("peace",),
    "evening_peace": ("peace",),
}


def resolve_audio_asset(audio_dir: Path, date: str, watch_key: str):
    """Return the first existing asset, preferring current watch-key names."""
    try:
        slugs = _SLUGS[watch_key]
    except KeyError as exc:
        raise ValueError(f"unknown watch key: {watch_key}") from exc
    for slug in slugs:
        path = audio_dir / f"{date}-{slug}.mp3"
        if path.exists():
            return path
    return None


def validate_audio_render(audio_dir: Path, date: str, watch_keys, html: str):
    """Fail closed when existing watch audio is omitted from generated HTML."""
    expected = sum(
        resolve_audio_asset(audio_dir, date, key) is not None
        for key in watch_keys
    )
    rendered = html.count('<audio class="watch-audio"')
    if rendered != expected:
        raise RuntimeError(
            f"audio render gate failed for {date}: {expected} existing watch assets "
            f"but {rendered} audio players rendered"
        )


def validate_advertised_page(repo: Path, date: str, expected_count: int = 5):
    """Refuse a ship when per-day JSON audio flags disagree with page players."""
    payload = json.loads(
        (repo / "docs/assets/readings" / f"{date}.json").read_text()
    )
    html = (repo / "docs/readings" / f"{date}.html").read_text()
    advertised = [
        watch for watch in payload["watches"].values() if watch.get("has_audio")
    ]
    rendered = html.count('<audio class="watch-audio"')
    if len(advertised) != expected_count or rendered != len(advertised):
        raise RuntimeError(
            f"audio ship gate failed for {date}: {len(advertised)} advertised, "
            f"{rendered} players, expected {expected_count}"
        )
    missing = []
    for watch in advertised:
        audio_url = watch.get("audio_url")
        name = Path(urlparse(audio_url).path).name if audio_url else ""
        if not name or name not in html:
            missing.append(name or "<missing audio_url>")
    if missing:
        raise RuntimeError(
            f"audio ship gate failed for {date}: advertised source(s) absent "
            f"from HTML: {', '.join(missing)}"
        )
    return rendered


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "verify-page":
        raise SystemExit("usage: reading_audio.py verify-page YYYY-MM-DD")
    repository = Path(__file__).resolve().parent.parent
    count = validate_advertised_page(repository, sys.argv[2])
    print(f"audio ship gate ok: {sys.argv[2]} ({count} advertised/player sources)")
