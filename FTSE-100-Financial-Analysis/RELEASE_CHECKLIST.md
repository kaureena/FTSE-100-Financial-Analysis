# Release Checklist (Pre-handover)

Use this before packaging a release zip.

## A) Content completeness
- [ ] V1: 7 exports present and listed in `docs/dashboards/V1/page_index.md`
- [ ] V2: 22 exports present and listed in `docs/dashboards/V2/page_index.md`
- [ ] Mermaid diagrams render (or pre-rendered PNGs exist)
- [ ] Constituents universe snapshot present (and labelled as demo weights)
- [ ] Events calendar present (and labelled as stub unless integrated)

## B) Quality gates
- [ ] DQ run passes (or failures documented and exports flagged)
- [ ] Export audit passes (resolution = 3840×2160)
- [ ] Run register appended for this release
- [ ] No broken internal links in README / navigation docs

## C) Governance
- [ ] Issue register updated (Open vs Closed)
- [ ] Risk log reviewed (last review within 7 days)
- [ ] Decision log updated for any new architectural decisions
- [ ] Hours tracking updated (weekly rollup + breakdown)

## D) Packaging
- [ ] Zip includes only necessary artefacts (remove caches if needed)
- [ ] Include `HANDOVER_NOTES.md`
- [ ] Include `LICENSE` (if applicable)
