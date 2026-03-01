# UK Market Context (Repo Theme Notes)

This project is intentionally framed as a **UK Master’s project**.

---

## Trading session conventions used
- **Timezone:** Europe/London  
- **Session window (core):** 08:00–16:30 London time  
- **Index context:** FTSE 100 (“Footsie”) as a UK large-cap benchmark

Where it shows up:
- Timestamp parsing and labelling for dashboards
- Intraday “terminal” pages (market pulse, volatility regimes)
- Event overlays (macro releases + earnings stubs)

---

## Constituents universe realism
The repo includes a **frozen FTSE100 constituents universe snapshot** with:
- Tickers (e.g., `SHEL.L`, `AZN.L`)
- Sector and ICB-style classification
- Index weights (as-of date + source attribution)

File:
- `data/reference/ftse100_constituents_universe_snapshot.csv`

Why we freeze it:
- Index membership changes frequently; the snapshot ensures reproducibility.
- For “live” production, the loader would be connected to an official index vendor feed.

---

## Calendar & events realism (stub)
V2 introduces an events overlay concept:
- **Macro releases calendar** (e.g., CPI, BoE decisions) — stub
- **Earnings dates** for constituents — stub

Output:
- `v2_modernisation_realtime/data/mart/events_overlay.*`

How to extend:
- Replace stub CSV with live provider API.
- Add an “event impact window” (pre/post) for volatility attribution.

---

## Disclaimer
This repository is for analytics / reporting / modelling demonstration only.
It is **not** trading software and is **not financial advice**.

