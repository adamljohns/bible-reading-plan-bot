# Codex Notes for bible-reading-plan-bot

This repo's operating manual is `CLAUDE.md`. Read it before editing.

Key rules:

- Treat the current dirty working tree as pre-existing fleet/autopilot work.
- Do not run `git reset --hard`, `git checkout -- .`, or broad cleanup commands.
- Do not use `git add -A` or `git add .`; stage explicit files only.
- The main public site deploys from `docs/` through GitHub Pages.
- For church directory work, preserve all schema invariants in `CLAUDE.md`.
- For generated church pages, edit source data and run the documented generators rather than hand-editing generated HTML.
- Production-affecting changes should be reviewed before push.
