from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

# Streamlit + Plotly are optional (install requirements_ui.txt)
try:
    import streamlit as st  # type: ignore
except Exception as e:  # pragma: no cover
    raise SystemExit(
        "Streamlit is not installed. Install UI deps with:\n\n"
        "  pip install -r requirements.txt -r requirements_ui.txt\n\n"
        f"Original error: {e}"
    )

try:
    import plotly.graph_objects as go  # type: ignore
except Exception:  # pragma: no cover
    go = None

REPO_ROOT = Path(__file__).resolve().parents[1]
MART_DIR = REPO_ROOT / "v2_modernisation_realtime" / "data" / "mart"


def _load_table(name: str) -> pd.DataFrame:
    """Load a mart table by name (parquet preferred)."""
    pq = MART_DIR / f"{name}.parquet"
    csv = MART_DIR / f"{name}.csv"
    if pq.exists():
        return pd.read_parquet(pq)
    if csv.exists():
        return pd.read_csv(csv)
    raise FileNotFoundError(f"Missing mart table: {name} (looked for {pq} / {csv})")


@st.cache_data(show_spinner=False)
def load_market_overview() -> pd.DataFrame:
    return _load_table("market_overview")


@st.cache_data(show_spinner=False)
def load_intraday_terminal() -> pd.DataFrame:
    return _load_table("intraday_terminal")


@st.cache_data(show_spinner=False)
def load_sector_rotation() -> pd.DataFrame:
    return _load_table("sector_rotation")


@st.cache_data(show_spinner=False)
def load_pipeline_health() -> pd.DataFrame:
    return _load_table("pipeline_health")


@st.cache_data(show_spinner=False)
def load_latency_sla() -> pd.DataFrame:
    return _load_table("latency_sla")


@st.cache_data(show_spinner=False)
def load_alerts() -> pd.DataFrame:
    return _load_table("alerts_register")


@st.cache_data(show_spinner=False)
def load_events() -> pd.DataFrame:
    return _load_table("events_overlay")


def _terminal_css() -> str:
    return """
<style>
:root {
  --bg: #05060a;
  --panel: #0b1020;
  --text: #e6e6e6;
  --muted: #9aa4b2;
  --neon: #44d2ff;
  --neon2: #b6ff6a;
}

html, body, [class*="css"]  {
  background-color: var(--bg) !important;
  color: var(--text) !important;
}

section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #070a12 0%, #05060a 100%);
  border-right: 1px solid rgba(68, 210, 255, 0.15);
}

div[data-testid="stMetric"] {
  background: rgba(11, 16, 32, 0.85);
  border: 1px solid rgba(68, 210, 255, 0.18);
  border-radius: 12px;
  padding: 12px 14px;
}

h1, h2, h3 {
  text-shadow: 0 0 22px rgba(68, 210, 255, 0.18);
}

a { color: var(--neon) !important; }

</style>
"""


def _plot_line(df: pd.DataFrame, x: str, y: str, title: str):
    if go is None:
        st.line_chart(df.set_index(x)[y])
        return
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[x], y=df[y], mode="lines", name=y))
    fig.update_layout(
        title=title,
        template="plotly_dark",
        height=420,
        margin=dict(l=10, r=10, t=55, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)


def _plot_candles(df: pd.DataFrame, title: str):
    if go is None:
        st.info("Plotly not installed — showing close line chart instead.")
        _plot_line(df, x="timestamp_london", y="close", title=title)
        return
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df["timestamp_london"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="FTSE100",
            )
        ]
    )
    fig.update_layout(
        title=title,
        template="plotly_dark",
        height=520,
        margin=dict(l=10, r=10, t=55, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="UK Market Terminal — FTSE 100", page_icon="📈", layout="wide")
    st.markdown(_terminal_css(), unsafe_allow_html=True)

    st.title("UK Market Terminal — FTSE 100")
    st.caption("Portfolio build: V2 marts + DuckDB + neon exports. Data is reproducible and offline-friendly.")

    if not MART_DIR.exists():
        st.error(f"Mart directory not found: {MART_DIR}")
        st.stop()

    page = st.sidebar.radio(
        "Terminal Pages",
        [
            "01 — Pulse Overview",
            "02 — Intraday Terminal",
            "03 — Sector Rotation",
            "04 — Monitoring + Alerts",
            "05 — Events Overlay",
        ],
        index=0,
    )

    # Shared: latest run id from any mart table
    try:
        run_id = str(_load_table("board_pack")["run_id"].iloc[0])
    except Exception:
        run_id = "(unknown)"
    st.sidebar.markdown(f"**Run ID:** `{run_id}`")

    if page.startswith("01"):
        df = load_market_overview()
        df["timestamp_london"] = pd.to_datetime(df["timestamp_london"])
        latest = df.sort_values("timestamp_london").tail(1).iloc[0]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Last", f"{latest['close']:.2f}")
        c2.metric("Δ vs Prev Close", f"{latest['delta_pct']:.2f}%")
        c3.metric("Session High", f"{latest['session_high']:.2f}")
        c4.metric("Session Low", f"{latest['session_low']:.2f}")

        _plot_line(df, x="timestamp_london", y="close", title="FTSE 100 — 5m close")

        st.subheader("Market Overview Table (last 20 rows)")
        st.dataframe(df.sort_values("timestamp_london").tail(20), use_container_width=True)

    elif page.startswith("02"):
        df = load_intraday_terminal()
        df["timestamp_london"] = pd.to_datetime(df["timestamp_london"])
        st.subheader("Intraday Terminal — 1m candles")
        st.caption("Candlestick chart + key indicators (MA20/MA60/RSI/VWAP).")

        # date filter
        start = st.sidebar.date_input("Start date", df["timestamp_london"].min().date())
        end = st.sidebar.date_input("End date", df["timestamp_london"].max().date())
        mask = (df["timestamp_london"].dt.date >= start) & (df["timestamp_london"].dt.date <= end)
        view = df.loc[mask].copy()

        _plot_candles(view, title="FTSE 100 — Intraday 1m")

        st.subheader("Indicator Snapshot")
        st.dataframe(view.tail(30), use_container_width=True)

    elif page.startswith("03"):
        rot = load_sector_rotation()
        rot["date"] = pd.to_datetime(rot["date"])
        latest_date = rot["date"].max()
        latest = rot[rot["date"] == latest_date].sort_values("ret_20d", ascending=False)

        st.subheader(f"Sector Rotation — as of {latest_date.date().isoformat()}")
        st.caption("5d / 20d compounded returns per sector.")

        st.dataframe(latest, use_container_width=True)

        # plot top 10 sectors by 20d return
        top = latest.head(10)
        if go is None:
            st.bar_chart(top.set_index("sector")["ret_20d"])
        else:
            fig = go.Figure(go.Bar(x=top["sector"], y=top["ret_20d"], name="20d return"))
            fig.update_layout(template="plotly_dark", height=420, margin=dict(l=10, r=10, t=55, b=10))
            st.plotly_chart(fig, use_container_width=True)

    elif page.startswith("04"):
        alerts = load_alerts()
        pipe = load_pipeline_health()
        lat = load_latency_sla()

        st.subheader("Active Alerts")
        st.dataframe(alerts, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Pipeline Health (last 14d)")
            st.dataframe(pipe.sort_values("date", ascending=False), use_container_width=True)
        with c2:
            st.subheader("Latency SLA (hourly)")
            st.dataframe(lat.sort_values("hour", ascending=False).head(48), use_container_width=True)

    elif page.startswith("05"):
        ev = load_events()
        st.subheader("Events Overlay (macro + earnings)")
        st.caption("This is an enrichment stub. Replace with a real calendar feed if you have a provider.")

        if "timestamp_london" in ev.columns:
            ev["timestamp_london"] = pd.to_datetime(ev["timestamp_london"], errors="coerce")
            ev = ev.sort_values("timestamp_london")
        st.dataframe(ev.head(100), use_container_width=True)

    else:
        st.info("Page not implemented.")


if __name__ == "__main__":  # pragma: no cover
    main()
