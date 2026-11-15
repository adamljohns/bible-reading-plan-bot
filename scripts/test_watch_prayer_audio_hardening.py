#!/usr/bin/env python3
"""Targeted, non-publishing tests for PJG-1114-AUD2 hardening."""
from __future__ import annotations

import importlib.util
import json
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    gen = load("watch_audio_generator", ROOT / "bin/generate-watch-audio.py")
    gate = load("watch_prayer_gate", ROOT / "scripts/check_watch_prayer_asr.py")

    requests = gen.voicestudio_prayer_requests(
        "Father, guide me. Keep me faithful. In Jesus name I pray. Amen."
    )
    assert requests == [
        "Father, guide me.",
        "Keep me faithful.",
        "In Jesus name I pray. Amen.",
    ], requests

    with tempfile.TemporaryDirectory(prefix="pjg1114-test-") as td:
        tmp = Path(td)
        calls = tmp / "calls.jsonl"
        fake = tmp / "fake-voicestudio.py"
        fake.write_text(
            "import argparse,json,os,wave\n"
            "p=argparse.ArgumentParser(); p.add_argument('--text'); p.add_argument('--out'); a=p.parse_args()\n"
            "with open(os.environ['FAKE_VS_LOG'],'a') as f: f.write(json.dumps(a.text)+'\\n')\n"
            "with wave.open(a.out,'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(b'\\0\\0'*4800)\n"
        )
        os.environ["FAKE_VS_LOG"] = str(calls)
        gen.VS_SPEAK = str(fake)
        out = tmp / "prayer.wav"
        assert gen.render_voicestudio_text(
            "Father, guide me. Keep me faithful. In Jesus name I pray. Amen.", str(out)
        )
        assert out.is_file() and out.stat().st_size > 1000
        got_calls = [json.loads(line) for line in calls.read_text().splitlines()]
        assert got_calls == requests, got_calls

        gen.PRAYER_AUDIT_DIR = str(tmp / "audit-copy")
        copied = Path(gen.persist_prayer_audit("2099-01-02", "wisdom", str(out)))
        assert copied.is_file() and copied.stat().st_size > 1000

        audit_dir = tmp / "gate-audit"
        gate.PRAYER_AUDIT_DIR = audit_dir
        js = tmp / "day.json"
        js.write_text(json.dumps({"watches": {"wisdom": {"text": (
            "Prayer\nFather, guide me today. Keep me faithful. Amen.\nWatch Charge\nStand firm."
        )}}}))
        whole = tmp / "whole-watch.mp3"
        whole.write_bytes(b"narration may repeat every prayer word")

        missing = gate.check_watch("2099-01-02", "wisdom", js, whole, transcribe=lambda _: "")
        assert missing and "missing exact prayer ASR artifact" in missing[0], missing

        audit_dir.mkdir()
        exact = audit_dir / "2099-01-02-wisdom-prayer.wav"
        exact.write_bytes(out.read_bytes())
        seen = []
        def transcribe(path):
            seen.append(Path(path))
            return "Father, guide me today. Keep me faithful. Amen."
        assert gate.check_watch("2099-01-02", "wisdom", js, whole, transcribe=transcribe) == []
        assert seen == [exact], seen

    print("PASS sentence requests x3; exact prayer artifact required; whole-watch fallback refused")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
