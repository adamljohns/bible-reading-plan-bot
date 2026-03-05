# Bible Reading Plan Bot 📖

**MOOP's Daily Bible Reading Plan Generator**

A standalone bot that generates daily Bible readings in the Five-Watch format with blended translation style.

## Format
- **Morning Wisdom (0600)** — Proverbs, Psalms, or thematic wisdom passages
- **1st Watch - Husband's Post (0700)** — Sequential OT reading with H.A.P.P.Y. reflection
- **2nd Watch - Father's Charge (1100)** — Sequential OT reading with F.U.L.F.I.L.L.E.D. reflection
- **3rd Watch - Citizen's Stand (1500)** — Sequential OT reading with R.E.S.O.L.U.T.E. reflection
- **Evening Peace (2100)** — Psalms with multi-perspective evening reflection

## Translation Style
Blended: NKJV weight + ESV precision + NASB accuracy + CSB clarity + NLT warmth
With [bracketed amplifications] where translations diverge.

## Usage
```bash
python3 plan.py today        # Show today's readings
python3 plan.py "March 5"    # Show specific date
python3 plan.py generate     # Generate readings for current month
```

## Built by MiniMoop for MOOP (Adam Johns)
Part of the OpenClaw automation ecosystem.
