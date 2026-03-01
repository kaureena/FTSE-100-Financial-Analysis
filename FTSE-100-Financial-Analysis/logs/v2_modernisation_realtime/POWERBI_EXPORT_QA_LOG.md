# Power BI Export QA Log (V2)

## Purpose
The Power BI export pack exists to provide recruiter-friendly, “BI-native” visuals:
- donut/pie for composition (sectors/weights)
- gauge/speedometer for health and SLA
- compact dense layout with neon accents

## QA checklist
- [x] Exports are 4K (3840×2160)
- [x] Theme applied (UK Neon Terminal)
- [x] Titles/subtitles follow typography hierarchy
- [x] Footer shows London time + run_id + “Not financial advice”
- [x] Donut/pie charts have labels + legend (no ambiguous slices)
- [x] Gauges have threshold markers (OK/WARN/ALERT)
- [x] No red/green-only encoding

## Known limitations
- Export pack is image-only in this repo (PBIX not included by default).
- Measures are documented in `bi_powerbi/measures/` (main repo).

## Evidence paths
- `v2_modernisation_realtime/bi_powerbi/exports/*`
- `assets/branding/powerbi_theme_uk_neon_terminal.json`
