# Men’s Prayer Wall (v0)

- Public hub: `/prayer/`
- Gated wall: `/prayer/wall.html` (`noindex,nofollow`)
- API (Worker): `/api/prayer/*` — data under R2 prefix `prayer-wall/` (not publicly GET-able)

## Secrets (Worker — never commit)
```bash
cd ~/usmcmin-site-worker
wrangler secret put PRAYER_WALL_PIN
wrangler secret put PRAYER_WALL_SESSION_SECRET
wrangler deploy
```

Pending local note (operator only): `~/.openclaw/credentials/prayer-wall-pin-pending.txt`

## Deploy
1. Push `docs/prayer/*` via bible-reading-plan-bot → R2 Action
2. Deploy Worker with prayer API routes + secrets
