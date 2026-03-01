# DAX Measures (Template)

These measures are provided as **templates** so the Power BI build is consistent and professional.

> Tables below assume you import marts from `v2_modernisation_realtime/data/mart/` (or via DuckDB).

---

## Market overview
```DAX
Last Close :=
VAR lastTs =
    MAX ( 'market_overview'[timestamp_london] )
RETURN
    CALCULATE ( MAX ( 'market_overview'[close] ), 'market_overview'[timestamp_london] = lastTs )
```

```DAX
Session Return % :=
VAR firstTs =
    CALCULATE ( MIN ( 'market_overview'[timestamp_london] ), ALL ( 'market_overview' ) )
VAR lastTs =
    CALCULATE ( MAX ( 'market_overview'[timestamp_london] ), ALL ( 'market_overview' ) )
VAR firstClose =
    CALCULATE ( MAX ( 'market_overview'[close] ), 'market_overview'[timestamp_london] = firstTs )
VAR lastClose =
    CALCULATE ( MAX ( 'market_overview'[close] ), 'market_overview'[timestamp_london] = lastTs )
RETURN
    DIVIDE ( lastClose - firstClose, firstClose )
```

---

## Sector weights / breadth
```DAX
Sector Weight % :=
DIVIDE (
    SUM ( 'constituents_universe'[index_weight] ),
    CALCULATE ( SUM ( 'constituents_universe'[index_weight] ), ALL ( 'constituents_universe' ) )
)
```

```DAX
Breadth % (sectors positive) :=
VAR pos =
    CALCULATE ( COUNTROWS ( FILTER ( 'sector_rotation', 'sector_rotation'[sector_return] > 0 ) ), ALL ( 'sector_rotation' ) )
VAR allS =
    CALCULATE ( COUNTROWS ( 'sector_rotation' ), ALL ( 'sector_rotation' ) )
RETURN
    DIVIDE ( pos, allS )
```

---

## Risk
```DAX
Max Drawdown % :=
MIN ( 'drawdown_risk'[drawdown_pct] )
```

```DAX
VaR 95 % :=
MIN ( 'drawdown_risk'[var_95] )
```

---

## Ops / SLA
```DAX
SLA Pass % :=
VAR total = COUNTROWS ( 'pipeline_health' )
VAR breaches =
    CALCULATE ( COUNTROWS ( FILTER ( 'pipeline_health', 'pipeline_health'[sla_breach_flag] = TRUE () ) ) )
RETURN
    1 - DIVIDE ( breaches, total )
```

```DAX
Latency p95 (ms) :=
MAX ( 'latency_sla'[p95_ms] )
```

---

## Monitoring (model)
```DAX
Latest RMSE :=
VAR lastTs = MAX ( 'forecasting_metrics'[timestamp] )
RETURN
    CALCULATE ( MAX ( 'forecasting_metrics'[rmse] ), 'forecasting_metrics'[timestamp] = lastTs )
```

```DAX
Drift Score (proxy) :=
VAR ms = ABS ( MAX ( 'model_monitoring'[mean_shift] ) )
VAR ss = ABS ( MAX ( 'model_monitoring'[std_shift] ) )
RETURN
    MIN ( 100, (ms * 10000) + (ss * 8000) )
```

---

## Notes
- These measures are intentionally simple and are meant for **portfolio reproducibility**.
- For production: add dimensional modelling, proper date tables, and RLS if needed.
