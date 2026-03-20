# Dashboard Review Log

Reviewer checklist + notes for the dashboard export packs.

---

## Review checklist (per page)
- [ ] Page title + subtitle present (UK market terminal style).
- [ ] Timestamp uses Europe/London and is visible somewhere on page.
- [ ] Key KPI tiles have units (points, %, ms).
- [ ] Legends readable at 100% zoom (Teams/Zoom screen share).
- [ ] Visual density: no wasted whitespace; panels align to grid.
- [ ] Consistent neon accent strips + glow borders.
- [ ] If the page is V2: sourced from `v2_modernisation_realtime/data/mart/*`.

---

## Latest review notes (2026-02-17)
### V1 pack (`docs/dashboards/V1/exports/`)
- ✅ Candles/volume panel readability at 4K is good.
- ✅ Forecast pages show clear horizon framing (10-minute).
- ⚠️ Consider adding a small “data freshness” badge to V1 pages (optional).

### V2 pack (`docs/dashboards/V2/exports/`)
- ✅ Terminal-style layout consistent across pages.
- ✅ Correlation heatmap remains readable at 4K.
- ⚠️ Some pages could benefit from explicit donut/gauge visuals for executive audiences.

### Power BI export pack (`v2_modernisation_realtime/bi_powerbi/exports/`)
- ✅ Added donut/pie and gauge visuals for executive interpretation.
- ✅ Uses the same UK terminal brand language and 16:9 layout.

---

## Next review iteration ideas
- Add a “screen-reader friendly” alt-text appendix for all exports.
- Add a small “data source attribution” footer on each page.
