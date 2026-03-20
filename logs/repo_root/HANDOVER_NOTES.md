# Handover Notes (to Reena / Reviewer)

## What to review first (10 minutes)
1) `README.md` (repo narrative)
2) `docs/01_PORTFOLIO_WALKTHROUGH.md` (talk track)
3) Dashboard exports:
   - `docs/dashboards/V2/exports/v2_page_01_footsie_pulse_overview.png`
   - `docs/dashboards/V2/exports/v2_page_16_board_pack_one_pager.png`
   - `docs/dashboards/V1/exports/v1_page_06_model_comparison.png`

## How to rebuild quickly (offline)
- Run V1:
  - `python scripts/v1_build_all.py --data-source snapshot`
- Run V2:
  - `python scripts/v2_build_all.py --data-source snapshot`
- Regenerate V2 exports from marts only:
  - `python scripts/v2_export_from_marts.py`

## How to evidence operational maturity
- Run register:
  - `docs/logs/refresh_run_register.csv`
- DQ issue register:
  - `docs/logs/07_dq_issue_register.csv`
- Pipeline monitoring:
  - `v2_modernisation_realtime/monitoring/reports/*`

## Known limitations (be upfront)
- Constituents weights are demo weights, not official.
- Events/news are stub feeds unless integrated.

## Where to update logs
- Use `logs/` folder (this pack provides the standardised templates).
