#!/usr/bin/env python3
"""
Run wayback availability+CDX checks against a small queue file (post-round
host-side capture). Updates tmp/wayback_snapshots.json incrementally.

Usage:
    python3 scripts/wayback_archive_queue.py tmp/wayback_r59_queue.json
"""

import json
import os
import sys
import time
import urllib.parse
import urllib.request
import ssl
from datetime import datetime

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

AVAILABILITY = 'https://archive.org/wayback/available?url={}'
CDX = 'http://web.archive.org/cdx/search/cdx?url={}&output=json&limit=-1&filter=statuscode:200'
SAVE_NOW = 'https://web.archive.org/save/{}'
UA = 'Mozilla/5.0 (MOOP Church Directory / Wayback queue archiver)'
SNAPS = 'tmp/wayback_snapshots.json'


def check(url):
    try:
        req = urllib.request.Request(AVAILABILITY.format(urllib.parse.quote(url, safe=':/?=&')),
                                      headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as r:
            d = json.loads(r.read().decode())
        c = d.get('archived_snapshots', {}).get('closest', {})
        if c.get('available'):
            return c.get('url'), c.get('timestamp')
    except Exception:
        pass
    try:
        cdx_url = url.replace('https://', '').replace('http://', '')
        req = urllib.request.Request(CDX.format(urllib.parse.quote(cdx_url, safe=':/?=&')),
                                      headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as r:
            rows = json.loads(r.read().decode())
        if len(rows) > 1:
            ts, original = rows[-1][1], rows[-1][2]
            return f'https://web.archive.org/web/{ts}/{original}', ts
    except Exception:
        pass
    return None, None


def save_now(url):
    """Try Save Page Now (slow, ~60-90s). Returns archived URL or None."""
    try:
        req = urllib.request.Request(SAVE_NOW.format(url), headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r:
            final = r.geturl()
            if '/web/' in final:
                return final
            cl = r.headers.get('Content-Location')
            if cl and '/web/' in cl:
                return 'https://web.archive.org' + cl
    except Exception as e:
        print(f'  save-now failed: {e}', flush=True)
    return None


def main():
    if len(sys.argv) < 2:
        sys.exit('usage: wayback_archive_queue.py <queue.json> [--save-now]')
    queue_file = sys.argv[1]
    do_save = '--save-now' in sys.argv

    queue = json.load(open(queue_file))
    snaps = {}
    if os.path.exists(SNAPS):
        snaps = json.load(open(SNAPS))

    found = 0
    saved_new = 0
    none_found = 0

    for i, url in enumerate(queue):
        if url in snaps:
            continue
        archived, ts = check(url)
        if archived:
            snaps[url] = {'archived': archived, 'via': 'queue-availability', 'captured': ts}
            found += 1
            print(f'[{i+1}/{len(queue)}] FOUND  {url}')
        elif do_save:
            print(f'[{i+1}/{len(queue)}] saving... {url}')
            archived_now = save_now(url)
            if archived_now:
                snaps[url] = {'archived': archived_now, 'via': 'queue-save-now',
                              'captured': datetime.utcnow().strftime('%Y%m%d%H%M%S')}
                saved_new += 1
                print(f'  saved  -> {archived_now}')
            else:
                none_found += 1
                print(f'  no save')
        else:
            none_found += 1
            print(f'[{i+1}/{len(queue)}] none   {url}')
        if (i+1) % 10 == 0:
            json.dump(snaps, open(SNAPS,'w'), indent=2)
        time.sleep(0.4)

    json.dump(snaps, open(SNAPS,'w'), indent=2)
    print(f'\nDone. found={found} saved_new={saved_new} none={none_found}')


if __name__ == '__main__':
    main()
