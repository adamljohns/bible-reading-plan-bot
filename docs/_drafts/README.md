# docs/_drafts/

Unapproved outward-facing content lives here until Adam says APPROVE.

`docs/robots.txt` already carries `Disallow: /_drafts/`, and
`bin/approval_gate.py` skips this directory entirely — a page here is hidden by
construction, not by remembering to add a meta tag.

Workflow: write here → Adam APPROVEs → log the line in `/APPROVALS.md` → move
the file to its real home → `python3 bin/approval_gate.py --audit` to confirm
the site is clean.

This README is the only file that should ever be committed empty.
