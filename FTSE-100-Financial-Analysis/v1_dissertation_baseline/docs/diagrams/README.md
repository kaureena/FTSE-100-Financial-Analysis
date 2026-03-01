# V1 Diagrams (Rendered)

These diagrams exist so that the **V1 dissertation baseline** can be reviewed quickly without running code.

> Diagrams are rendered as 4K PNGs to match the repo’s evidence-pack style.

---

## Included diagrams

1. **V1 Data Pipeline** — `v1_data_pipeline.png`  
   Shows: snapshot → cleaning/DQ → feature store → ARIMA/LSTM → 7-page exports.

2. **V1 Model Lifecycle** — `v1_model_lifecycle.png`  
   Shows: ARIMA lane vs LSTM lane, and where evaluation/comparison happens.

3. **V1 Dashboard Lineage** — `v1_dashboard_lineage.png`  
   Shows: which artefacts feed which dashboard pages.

---

## Mermaid references (repo-wide)

Mermaid source diagrams are under:
- `../../../../docs/mermaid/`

If you want a V1-only mermaid pack, use the mappings in `v1_dashboard_lineage.png` as a starting point.

