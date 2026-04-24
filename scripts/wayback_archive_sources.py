#!/usr/bin/env python3
"""
Phase 2: Batch-archive enrichment_sources URLs for green/red/black churches
via the Wayback Machine's Save Page Now + Availability API.

Strategy:
1. For each URL, first check Availability API (no auth, fast) — if a snapshot
   exists within the last 6 months, use it as-is.
2. Otherwise submit to Save Page Now (anonymous endpoint, rate-limited).
3. Checkpoint progress to a state file every N URLs for resumability.
4. Skip facebook.com / instagram.com (auth-walled, Wayback can't snapshot).

Produces:
- tmp/wayback_snapshots.json  — mapping {original_url: archived_url, ...}
- tmp/wayback_failures.json   — list of URLs that couldn't be archived
- tmp/wayback_progress.log    — human-readable progress log

Usage:
    python3 scripts/wayback_archive_sources.py [--max N] [--resume]
"""

import argparse
import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# macOS system Python has stale CA bundle; bypass for public-archive calls only.
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

CHURCHES = 'docs/data/churches.json'
SNAPSHOTS_FILE = 'tmp/wayback_snapshots.json'
FAILURES_FILE = 'tmp/wayback_failures.json'
LOG_FILE = 'tmp/wayback_progress.log'

AVAILABILITY_API = 'https://archive.org/wayback/available?url={}'
CDX_API = 'http://web.archive.org/cdx/search/cdx?url={}&output=json&limit=-1&filter=statuscode:200'
SAVE_NOW = 'https://web.archive.org/save/{}'
FRESH_WINDOW = timedelta(days=180)  # if existing snapshot is newer than this, reuse
SKIP_DOMAINS = ('facebook.com', 'instagram.com', 'tiktok.com', 'youtube.com/channel')
USER_AGENT = 'Mozilla/5.0 (MOOP Church Directory / Wayback batch archiver; +https://usmcmin.org)'
REQUEST_TIMEOUT = 12  # availability + CDX both fast; fail quickly on laggards
SLEEP_BETWEEN_REQUESTS = 0.3  # light rate limit
BACKOFF_ON_429 = 60


def log(msg):
    ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f'[{ts}] {msg}'
    print(line, flush=True)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')


def load_state():
    snaps = {}
    if os.path.exists(SNAPSHOTS_FILE):
        try:
            snaps = json.load(open(SNAPSHOTS_FILE))
        except Exception:
            snaps = {}
    fails = []
    if os.path.exists(FAILURES_FILE):
        try:
            fails = json.load(open(FAILURES_FILE))
        except Exception:
            fails = []
    return snaps, fails


def save_state(snaps, fails):
    json.dump(snaps, open(SNAPSHOTS_FILE, 'w'), indent=2)
    json.dump(fails, open(FAILURES_FILE, 'w'), indent=2)


def should_skip(url):
    u = url.lower()
    for d in SKIP_DOMAINS:
        if d in u:
            return True
    return False


def check_availability(url):
    """Returns (archived_url, timestamp_dt) if snapshot exists, else (None, None).

    Tries availability API first, falls back to CDX API which handles fuzzy matching.
    """
    # Try availability API first (fast, simple)
    try:
        req = urllib.request.Request(
            AVAILABILITY_API.format(urllib.parse.quote(url, safe=':/?=&')),
            headers={'User-Agent': USER_AGENT},
        )
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT, context=SSL_CTX) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        closest = data.get('archived_snapshots', {}).get('closest', {})
        if closest.get('available'):
            archived_url = closest.get('url')
            ts = closest.get('timestamp')
            if ts and len(ts) >= 8:
                try:
                    dt = datetime.strptime(ts[:14], '%Y%m%d%H%M%S')
                except Exception:
                    dt = datetime.strptime(ts[:8], '%Y%m%d')
                return archived_url, dt
    except Exception as e:
        log(f'  availability check failed: {e}')

    # Fallback: CDX API with fuzzy URL matching
    try:
        # Strip scheme for CDX which is more lenient about protocol differences
        cdx_url = url.replace('https://', '').replace('http://', '')
        req = urllib.request.Request(
            CDX_API.format(urllib.parse.quote(cdx_url, safe=':/?=&')),
            headers={'User-Agent': USER_AGENT},
        )
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT, context=SSL_CTX) as resp:
            rows = json.loads(resp.read().decode('utf-8'))
        # CDX returns [[header], [row1], [row2], ...]; last row is most recent
        if len(rows) > 1:
            last = rows[-1]
            # Columns: urlkey, timestamp, original, mimetype, statuscode, digest, length
            ts, original = last[1], last[2]
            archived_url = f'https://web.archive.org/web/{ts}/{original}'
            try:
                dt = datetime.strptime(ts[:14], '%Y%m%d%H%M%S')
            except Exception:
                dt = datetime.strptime(ts[:8], '%Y%m%d')
            return archived_url, dt
    except Exception as e:
        log(f'  CDX check failed: {e}')
    return None, None


def save_page_now(url):
    """Returns archived_url on success, else None."""
    try:
        req = urllib.request.Request(
            SAVE_NOW.format(url),
            headers={'User-Agent': USER_AGENT},
            method='GET',  # SPN accepts GET
        )
        with urllib.request.urlopen(req, timeout=90, context=SSL_CTX) as resp:
            # SPN redirects to the snapshot URL
            final_url = resp.geturl()
            if '/web/' in final_url:
                return final_url
            # Or the Content-Location header might hold it
            cl = resp.headers.get('Content-Location')
            if cl and '/web/' in cl:
                return 'https://web.archive.org' + cl
    except urllib.error.HTTPError as e:
        if e.code == 429:
            log(f'  rate limited (429); backoff {BACKOFF_ON_429}s')
            time.sleep(BACKOFF_ON_429)
            return save_page_now(url)  # one retry after backoff
        log(f'  save-now HTTPError {e.code}: {e.reason}')
    except Exception as e:
        log(f'  save-now failed: {e}')
    return None


def archive_url(url, snaps, fails, no_spn=False):
    """Archive a single URL. Updates snaps or fails in place.

    Priority:
    1. Use existing Wayback snapshot if ANY exists (availability API is fast)
    2. Only call Save Page Now if URL has zero archive history (skipped when no_spn=True)
    """
    if url in snaps:
        return 'cached'
    if should_skip(url):
        fails.append({'url': url, 'reason': 'auth-walled skip'})
        return 'skip'

    # Availability API first — grab ANY existing snapshot
    archived, ts = check_availability(url)
    if archived:
        is_fresh = ts and datetime.utcnow() - ts < FRESH_WINDOW
        via = 'availability' if is_fresh else 'availability-older'
        snaps[url] = {
            'archived': archived,
            'via': via,
            'captured': ts.strftime('%Y-%m-%dT%H:%M:%SZ') if ts else None,
        }
        return 'fresh' if is_fresh else 'older'

    # No snapshot exists
    if no_spn:
        fails.append({'url': url, 'reason': 'no-existing-snapshot (SPN skipped)'})
        return 'no-snapshot'

    # Submit Save Page Now (slow, ~60-90s)
    archived_now = save_page_now(url)
    if archived_now:
        snaps[url] = {
            'archived': archived_now,
            'via': 'save-now',
            'captured': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        }
        return 'saved'

    fails.append({'url': url, 'reason': 'no-archive-and-save-now-failed'})
    return 'fail'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max', type=int, default=0, help='stop after N URLs (0=all)')
    parser.add_argument('--resume', action='store_true', help='skip URLs already in snapshots file')
    parser.add_argument('--no-spn', action='store_true', help='availability-only; skip Save Page Now for URLs with no existing snapshot')
    args = parser.parse_args()

    os.makedirs('tmp', exist_ok=True)

    data = json.load(open(CHURCHES))
    churches = data.get('churches') if isinstance(data, dict) else data

    # Gather unique URLs across green/red/black churches
    urls = []
    seen = set()
    for c in churches:
        if c.get('overall_rating') not in ('green', 'red', 'black'):
            continue
        for u in (c.get('enrichment_sources') or []):
            if not isinstance(u, str) or not u.strip():
                continue
            if 'web.archive.org' in u:
                continue
            if u in seen:
                continue
            seen.add(u)
            urls.append(u)

    log(f'Starting Phase 2 batch archive: {len(urls)} unique URLs')

    snaps, fails = load_state()
    if args.resume:
        urls = [u for u in urls if u not in snaps]
        log(f'Resume mode: {len(urls)} URLs remaining')

    if args.max:
        urls = urls[:args.max]
        log(f'Max mode: processing {len(urls)} URLs this run')

    stats = {'fresh': 0, 'older': 0, 'saved': 0, 'skip': 0, 'fail': 0, 'cached': 0, 'no-snapshot': 0}

    for i, url in enumerate(urls):
        result = archive_url(url, snaps, fails, no_spn=args.no_spn)
        stats[result] = stats.get(result, 0) + 1
        log(f'[{i+1}/{len(urls)}] {result:8s}  {url}')

        # Checkpoint every 10
        if (i + 1) % 10 == 0:
            save_state(snaps, fails)
            log(f'  checkpoint: {json.dumps(stats)}')

        # Rate limit (only when we actually hit the network)
        if result in ('saved', 'fresh', 'older'):
            time.sleep(SLEEP_BETWEEN_REQUESTS)

    save_state(snaps, fails)
    log(f'DONE. Final stats: {json.dumps(stats)}')
    log(f'Total snaps: {len(snaps)}  total fails: {len(fails)}')


if __name__ == '__main__':
    main()
