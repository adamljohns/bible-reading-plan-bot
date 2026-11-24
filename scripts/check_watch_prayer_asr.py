#!/usr/bin/env python3
"""PJG-0825-PEACE1 — ASR gate vs JSON prayer sentences.

Refuse R2 if any published prayer sentence (or named close) is missing from
the exact generated prayer segment, or if a prayer heading leaks into it.

Staff proof only. Principal ear remains CLOSE.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

WHISPER = os.environ.get("WHISPER_CLI", "/opt/homebrew/bin/whisper-cli")
MODEL = os.environ.get(
    "WHISPER_MODEL",
    os.path.expanduser("~/.openclaw/whisper_models/ggml-small.en.bin"),
)
# PJG-AUD-0530-2026-10-18: small.en false-failed a clearly spoken father prayer on three
# bakes in a row (10-17 21:30 + 10-18 05:3x x2) — it never transcribed "By the power of
# Your Holy Spirit" after the opener pause, while large-v3 heard every sentence. A watch
# that fails on small.en gets one large-v3 second opinion before the gate refuses R2.
SECOND_MODEL = os.environ.get(
    "WHISPER_SECOND_MODEL",
    os.path.expanduser("~/.openclaw/whisper_models/ggml-large-v3.bin"),
)
WATCHES = ("wisdom", "husband", "father", "citizen", "peace")
PRAYER_AUDIT_DIR = Path(os.path.expanduser(
    os.environ.get("WATCH_PRAYER_AUDIT_DIR", "/tmp/pj-watch-prayer-asr")
))
# Per-day JSON keys are wisdom/first/second/third/peace.
# MP3 stems are wisdom/husband/father/citizen/peace.
JSON_KEY = {
    "wisdom": "wisdom",
    "husband": "first",
    "father": "second",
    "citizen": "third",
    "peace": "peace",
}
NAMED = (
    "grant us the grace",
    "in the name of jesus christ",
    "through jesus christ our lord",
    "when a man",
    "hold maria",
)
# Whole-watch MP3s always speak Personal Application / Reflection before the
# prayer. Those are not stray. Heading leak in the prayer region is.
STRAY = (
    "prayer from the",
)


def sentences(prayer: str) -> list[str]:
    body = re.sub(r"^🙏?\s*Prayer\b[^\n]*\n?", "", prayer.strip(), flags=re.I)
    parts = re.split(r"(?<=[.!?])\s+", body)
    out = []
    for p in parts:
        p = re.sub(r"\s+", " ", p).strip()
        if not p:
            continue
        # Amen / In the name… are closes, not standalone required sentences.
        if out and (
            re.fullmatch(r"Amen\.??", p, re.I)
            or re.match(r"In the name of Jesus", p, re.I)
        ):
            out[-1] = out[-1].rstrip() + " " + p
            continue
        out.append(p)
    return out


def extract_prayer(text: str) -> str:
    lines = text.splitlines()
    buf, st = [], "before"
    hdr = re.compile(r"^🙏?\s*Prayer\b", re.I)
    charge = re.compile(r"^(⚓|🛡️|🔑|🕊️?)?\s*(Helm Command|Watch Charge|The Charge|Rudder Steer|Wisdom Key|Wise Takeaway|Key to Wisdom|Word to the Wise|Wisdom to Carry|Prompt for Peace|Peaceful Focus|Evening Reminder|Rest in This|Peace to Carry)\b", re.I)
    amen = re.compile(r"\bAmen\.?\s*$", re.I)
    for line in lines:
        if st == "before" and hdr.match(line.strip()):
            st = "prayer"
            continue
        if st == "prayer" and charge.match(line.strip()):
            break
        if st == "prayer":
            buf.append(line)
            if amen.search(line.strip()):
                break
    return "\n".join(buf).strip()


def asr_one(mp3: Path, tail_sec: int, model: str = "") -> str:
    """Transcribe the last tail_sec seconds; tail_sec <= 0 means the whole file."""
    tmp = Path(tempfile.mkdtemp(prefix="pjg-asr-"))
    wav = tmp / "prayer.wav"
    cut = [] if tail_sec <= 0 else ["-sseof", f"-{int(tail_sec)}"]
    subprocess.run(
        ["/opt/homebrew/bin/ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
         *cut, "-i", str(mp3),
         "-ac", "1", "-ar", "16000", str(wav)],
        check=True,
    )
    out_prefix = tmp / "asr"
    r = subprocess.run(
        [WHISPER, "-m", model or MODEL, "-f", str(wav), "-otxt", "-of", str(out_prefix),
         "-l", "en", "-nt"],
        capture_output=True, text=True,
    )
    txt = Path(str(out_prefix) + ".txt")
    if not txt.is_file():
        raise SystemExit(f"ASR-GATE: whisper produced no text rc={r.returncode} {(r.stderr or r.stdout)[-400:]}")
    return txt.read_text(errors="replace")


# PJG-0915-AUD16: a whisper pass sometimes returns a stub — 945 chars for 150s of
# speech, where the identical command run by hand transcribed the lot. The gate
# could not tell "the audio does not say this" from "the transcription failed",
# so a degenerate pass silently became a missing-sentence verdict and refused a
# correct bake. Roughly 8 chars/second is well under real speech (~15-18) and
# comfortably above an empty result.
MIN_CHARS_PER_SEC = 8.0


def asr_window(mp3: Path, tail_sec: int, dur: float) -> str:
    """asr_one with a retry when the pass returns an implausibly short transcript."""
    span = dur if tail_sec <= 0 else min(float(tail_sec), dur)
    out = asr_one(mp3, tail_sec)
    if span > 20 and len(out.strip()) < MIN_CHARS_PER_SEC * span:
        second = asr_one(mp3, tail_sec)
        if len(second.strip()) > len(out.strip()):
            return second
    return out


def duration_sec(mp3: Path) -> float:
    try:
        r = subprocess.run(
            ["/opt/homebrew/bin/ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(mp3)],
            capture_output=True, text=True, check=True,
        )
        return float((r.stdout or "0").strip() or 0)
    except Exception:
        return 0.0


def asr(mp3: Path, tail_sec: int = 90) -> str:
    if not Path(WHISPER).is_file():
        raise SystemExit(f"ASR-GATE: missing whisper-cli at {WHISPER}")
    if not Path(MODEL).is_file():
        raise SystemExit(f"ASR-GATE: missing model at {MODEL}")
    # Input is the exact prayer-only segment emitted by generate-watch-audio.py.
    # Multiple windows still protect against a degenerate Whisper pass, but no
    # narration or history can satisfy a dropped prayer sentence.
    parts = []
    # PJG-0907-PRAY2: extra 150s window so VoiceStudio Amen is not a 09-05 false-fail.
    # Keep tails plus a whole-segment pass. They all operate only on the prayer
    # artifact, so repeated wording elsewhere in the watch is irrelevant.
    dur = duration_sec(mp3)
    # PJG-0915-AUD16: 130 added on measurement, not taste. On 2026-09-16 citizen
    # (321s) the 130s tail transcribed 1532 chars and contained the prayer while
    # the LONGER 150s tail returned only 952 and did not, and the whole-file pass
    # transcribed the opening and never reached it. whisper degrades on long
    # input, so more seconds can mean fewer words. 130 is the window that
    # actually hears the Citizen prayer on a long-history day.
    for sec in (45, 75, 110, 130, 150, 0):
        parts.append(asr_window(mp3, sec, dur))
    joined = "\n".join(parts)
    # If EVERY pass came back degenerate the transcription failed; say so rather
    # than reporting the prayer as missing and refusing a bake that may be fine.
    if dur > 60 and len(joined.strip()) < MIN_CHARS_PER_SEC * min(dur, 150.0):
        raise SystemExit(
            "ASR-GATE: transcription degenerate for %s (%d chars for %.0fs) — "
            "not a missing-prayer verdict" % (mp3.name, len(joined.strip()), dur)
        )
    return joined


def norm(s: str) -> str:
    s = s.lower()
    s = s.replace("ah-men", "amen").replace("ah men", "amen")
    # PJG-0915-AUD16: drop apostrophes entirely. whisper writes the spoken form
    # "in jesus name"; the text says "In Jesus' name". Keeping the apostrophe
    # made "jesus'" and "jesus" different tokens, so a perfectly audible close
    # read as missing. The 2026-09-16 wisdom prayer failed this gate on nothing
    # but a possessive mark. Apostrophes carry no ASR signal.
    s = s.replace("'", "").replace("’", "")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def tokens(s: str) -> list[str]:
    return [t for t in norm(s).split() if t not in {"the", "a", "an", "and", "of", "to", "in"}]


def present(needle: str, hay: str) -> bool:
    n = tokens(needle)
    if len(n) < 3:
        return norm(needle) in hay
    # Prayer-region proof: first 5 content tokens must appear in order
    # inside a 20-token window. The old 6-in-8 window false-failed audible
    # sentences after F5 overlap / whisper insertions (PJG-0826-AUD1).
    h = hay.split()
    need = n[:5]
    span = max(12, len(need) + 12)
    for i in range(0, max(1, len(h) - len(need) + 1)):
        window = h[i:i + span]
        wi = 0
        ok = True
        for t in need:
            rest = window[wi:]
            if t not in rest:
                ok = False
                break
            wi = wi + rest.index(t) + 1
        if ok:
            return True
    return False


def asr_second_opinion(mp3: Path) -> str:
    """large-v3 over a 130s tail plus the whole file. Slower, so only run on a fail."""
    return "\n".join(asr_one(mp3, sec, SECOND_MODEL) for sec in (130, 0))


# PJG-1120-PEACE-IN: 2026-11-20 Evening Peace shipped a clipped extra "In" spoken
# between two prayer sentences ("...to the Cross. In  Strengthen me..."). Every
# sentence was present, so the presence check passed, and a whole-segment whisper
# pass smooths a lone syllable away. So find it by sound first: a short voiced
# burst (<= 0.6s) with quiet on both sides, mid-prayer. Transcribe a short window
# from that burst; if what it says does not occur in the published prayer, it is
# a stray word and the take fails. Mid-word pauses that happen to isolate a real
# word ("Lord," "Amen") read back as prayer text and pass.
def _frames_db(wav: Path, hop: float = 0.02) -> list[float]:
    import math
    import struct
    import wave
    with wave.open(str(wav)) as w:
        sr = w.getframerate()
        data = w.readframes(w.getnframes())
    samples = struct.unpack("<%dh" % (len(data) // 2), data)
    step = max(1, int(hop * sr))
    out = []
    for i in range(0, len(samples), step):
        chunk = samples[i:i + step]
        rms = math.sqrt(sum(x * x for x in chunk) / len(chunk)) if chunk else 0
        out.append(20 * math.log10(rms / 32768) if rms > 0 else -120.0)
    return out


def junction_strays(prayer_audio: Path, prayer_text: str, model: str = "") -> list[str]:
    hop = 0.02
    tmp = Path(tempfile.mkdtemp(prefix="pjg-junc-"))
    wav = tmp / "p16.wav"
    subprocess.run(["/opt/homebrew/bin/ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-i", str(prayer_audio), "-ac", "1", "-ar", "16000", str(wav)], check=True)
    db = _frames_db(wav, hop)
    if not db:
        return []
    peak = max(db)
    loud = [d > peak - 22 for d in db]      # speech frames, relative to this take
    quiet = [d < peak - 28 for d in db]     # room tone between phrases
    runs, i = [], 0
    while i < len(loud):
        if loud[i]:
            j = i
            while j < len(loud) and loud[j]:
                j += 1
            runs.append((i, j))
            i = j
        else:
            i += 1
    # merge runs split by < 60 ms dips (one word, not two)
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] <= 3:
            merged[-1] = (merged[-1][0], r[1])
        else:
            merged.append(r)
    ptxt = " " + norm(prayer_text) + " "
    out = []
    for n, (st, en) in enumerate(merged[1:-1], start=1):
        dur = (en - st) * hop
        if dur > 0.6:
            continue
        before = merged[n - 1][1]
        after = merged[n + 1][0]
        if (st - before) * hop < 0.25 or (after - en) * hop < 0.25:
            continue
        if not all(quiet[before:st]) and not all(quiet[en:after]):
            continue
        t0 = max(0.0, st * hop - 0.05)
        seg = tmp / f"w{n}.wav"
        subprocess.run(["/opt/homebrew/bin/ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                        "-ss", f"{t0:.2f}", "-t", "3.0", "-i", str(wav), str(seg)], check=True)
        r = subprocess.run([WHISPER, "-m", model or MODEL, "-f", str(seg), "-l", "en", "-nt"],
                           capture_output=True, text=True)
        heard = norm(r.stdout).split()
        if len(heard) < 2:
            continue
        probe = " " + " ".join(heard[:3]) + " "
        if probe in ptxt or (" " + " ".join(heard[:2]) + " ") in ptxt:
            continue
        # tolerate whisper splitting a long word: does the window, minus its first
        # token, start a stretch of the prayer?
        rest = " " + " ".join(heard[1:4]) + " "
        if rest in ptxt or (" " + " ".join(heard[1:3]) + " ") in ptxt:
            out.append(f"stray {heard[0]!r} spoken at {t0:.1f}s before {' '.join(heard[1:5])!r}")
    return out

# PJG-1124-AUD-IN: the junction check above missed every stray "In," of 11-21..12-01
# (11-24 citizen "raised me up in Christ. In, forgive me..."; 11-26/11-28 father;
# 11-29 citizen). It needs dead-quiet room tone on one side of the burst, and these
# takes sit a few dB above peak-28 between sentences, so the burst was skipped before
# whisper ever heard it. The same pass let 11-25 wisdom say "rather than as the path
# of wisdom" twice. So also align a word-level transcript of the exact prayer take
# against the published prayer: any run of heard words the prayer lacks (or a
# replacement that adds 2+ words) is an inserted word and the take fails. Whisper
# spelling variants (Saviour/savior) are replacements of equal length and pass.
_TS = re.compile(r"\[(\d+):(\d+):(\d+\.\d+) --> [^\]]+\]\s*(.*)")


def aligned_insertions(prayer_audio: Path, prayer_text: str, model: str = "") -> list[str]:
    import difflib
    tmp = Path(tempfile.mkdtemp(prefix="pjg-ins-"))
    wav = tmp / "p16.wav"
    subprocess.run(["/opt/homebrew/bin/ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-i", str(prayer_audio), "-ac", "1", "-ar", "16000", str(wav)], check=True)
    r = subprocess.run([WHISPER, "-m", model or MODEL, "-f", str(wav), "-l", "en",
                        "-ml", "1", "-sow"], capture_output=True, text=True)
    heard = []
    for line in r.stdout.splitlines():
        m = _TS.match(line.strip())
        if not m:
            continue
        for w in m.group(4).split():
            nw = norm(w).replace(" ", "")
            if nw:
                t = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
                heard.append((t, w, nw))
    auth = [x for x in (norm(w).replace(" ", "") for w in prayer_text.split()) if x]
    if not heard or not auth:
        return []
    sm = difflib.SequenceMatcher(None, [h[2] for h in heard], auth, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        extra = (tag == "delete") or (tag == "replace" and (i2 - i1) > (j2 - j1) + 1)
        if not extra:
            continue
        said = " ".join(h[1] for h in heard[i1:i2])
        after = " ".join(auth[max(0, j1 - 3):j1])
        out.append(f"inserted {said!r} at {heard[i1][0]:.1f}s after {after!r}")
    return out


def check_watch(day: str, key: str, json_path: Path, mp3: Path, transcribe=None) -> list[str]:
    fails = []
    data = json.loads(json_path.read_text())
    jkey = JSON_KEY.get(key, key)
    watch = (data.get("watches") or {}).get(jkey) or {}
    text = watch.get("text") or ""
    prayer = extract_prayer(text)
    if not prayer:
        fails.append(f"{key}: no published prayer block (json {jkey})")
        return fails
    sents = sentences(prayer)
    if not sents:
        fails.append(f"{key}: prayer sentences empty")
        return fails
    if not mp3.is_file():
        fails.append(f"{key}: missing {mp3}")
        return fails
    prayer_audio = PRAYER_AUDIT_DIR / f"{day}-{key}-prayer.wav"
    if not prayer_audio.is_file():
        fails.append(
            f"{key}: missing exact prayer ASR artifact {prayer_audio}; "
            "refuse whole-watch fallback"
        )
        return fails
    raw = (transcribe or asr)(prayer_audio)
    hay = norm(raw)
    # The prayer's own address is the listen-script opener. Prayers no longer all
    # open "Father," (Principal 2026-11-07: vary Dear Lord / Heavenly Father /
    # God on High / Father God), so take it from the published text.
    opener = norm(re.split(r"[,.!]", sents[0], maxsplit=1)[0]).strip() or "father"
    father_i = hay.rfind(opener)
    if father_i < 0 and opener.split():
        father_i = hay.rfind(opener.split()[-1])
    if father_i < 0:
        fails.append(f"{key}: ASR never said the prayer's opening {opener!r}")
    else:
        prefix = hay[:father_i]
        for s in STRAY:
            if s in prefix:
                fails.append(f"{key}: stray narration before {opener!r} ({s!r})")
    second = transcribe is asr_second_opinion
    if os.environ.get("PRAYER_JUNCTION_GATE", "1") != "0":
        for f in junction_strays(prayer_audio, prayer, SECOND_MODEL if second else ""):
            fails.append(f"{key}: {f}")
    if os.environ.get("PRAYER_INSERT_GATE", "1") != "0":
        for f in aligned_insertions(prayer_audio, prayer, SECOND_MODEL if second else ""):
            fails.append(f"{key}: {f}")
    for sent in sents:
        if not present(sent, hay):
            fails.append(f"{key}: missing sentence {sent[:80]!r}")
    joined = " ".join(sents).lower()
    for named in NAMED:
        if named in joined and named not in hay and not present(named, hay):
            fails.append(f"{key}: named clause missing {named!r}")
    return fails


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: check_watch_prayer_asr.py YYYY-MM-DD [repo]", file=sys.stderr)
        return 2
    day = argv[1]
    root = Path(argv[2]) if len(argv) > 2 else Path.cwd()
    js = root / "docs" / "assets" / "readings" / f"{day}.json"
    if not js.is_file():
        print(f"ASR-GATE: missing {js}", file=sys.stderr)
        return 2
    fails = []
    for key in WATCHES:
        mp3 = root / "docs" / "assets" / "audio" / "readings" / f"{day}-{key}.mp3"
        got = check_watch(day, key, js, mp3)
        if got and Path(SECOND_MODEL).is_file() and mp3.is_file():
            print(f"ASR-GATE {key}: small.en fail ({len(got)}) — large-v3 second opinion", flush=True)
            got = check_watch(day, key, js, mp3, transcribe=asr_second_opinion)
            if not got:
                print(f"ASR-GATE {key}: PASS on large-v3 second opinion", flush=True)
        fails.extend(got)
    if fails:
        print("ASR-GATE FAIL", day)
        for f in fails:
            print(" -", f)
        return 12
    print("ASR-GATE PASS", day)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
