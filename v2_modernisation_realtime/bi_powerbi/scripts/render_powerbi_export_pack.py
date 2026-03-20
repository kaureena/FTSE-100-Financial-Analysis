"""render_powerbi_export_pack.py

Creates the Power BI-style 4K export evidence pack under:
- v2_modernisation_realtime/bi_powerbi/exports/

This is **portfolio tooling** to keep the evidence pack reproducible.

Usage (from repo root):
    python v2_modernisation_realtime/bi_powerbi/scripts/render_powerbi_export_pack.py

Notes:
- Reads from the V2 semantic marts: v2_modernisation_realtime/data/mart/*.csv
- Reads the FTSE100 universe snapshot: data/reference/ftse100_constituents_universe_snapshot.csv

"""

from __future__ import annotations

import os
from pathlib import Path
from io import BytesIO
import math

import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


REPO_ROOT = Path(__file__).resolve().parents[3]
MART_DIR = REPO_ROOT / "v2_modernisation_realtime" / "data" / "mart"
UNIVERSE_PATH = REPO_ROOT / "data" / "reference" / "ftse100_constituents_universe_snapshot.csv"
EXPORT_DIR = REPO_ROOT / "v2_modernisation_realtime" / "bi_powerbi" / "exports"

FONT_REG = fm.findfont("DejaVu Sans")
FONT_BOLD = fm.findfont("DejaVu Sans:bold")


def hex_to_rgb(hex_color: str):
    hex_color = hex_color.strip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def linear_gradient(size, top_color, bottom_color, horizontal=False):
    w, h = size
    top = np.array(hex_to_rgb(top_color), dtype=np.float32)
    bottom = np.array(hex_to_rgb(bottom_color), dtype=np.float32)
    if horizontal:
        grad = np.linspace(0, 1, w, dtype=np.float32).reshape(1, w, 1)
        arr = top + (bottom - top) * grad
        arr = np.repeat(arr, h, axis=0)
    else:
        grad = np.linspace(0, 1, h, dtype=np.float32).reshape(h, 1, 1)
        arr = top + (bottom - top) * grad
        arr = np.repeat(arr, w, axis=1)
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGB")


def mpl_fig_to_pil(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=200, transparent=True, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGBA")


def render_line_chart(x, y, title=None, subtitle=None, highlight_last=True):
    fig = plt.figure(figsize=(6, 3), dpi=200)
    ax = fig.add_axes([0.08, 0.18, 0.9, 0.75])
    ax.set_facecolor((0, 0, 0, 0))
    fig.patch.set_alpha(0)
    ax.plot(x, y, linewidth=2.2, color="#00E5FF")
    if highlight_last:
        ax.scatter([x[-1]], [y[-1]], s=35, color="#FBBF24", zorder=5)
    ax.grid(True, alpha=0.15, color="#94A3B8")
    ax.tick_params(colors="#C7D2FE", labelsize=8)
    for spine in ax.spines.values():
        spine.set_visible(False)
    if title:
        ax.set_title(title, color="#E5E7EB", fontsize=10, loc="left", pad=8, fontweight="bold")
    if subtitle:
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, color="#94A3B8", fontsize=8, va="bottom")
    return mpl_fig_to_pil(fig)


def render_donut_chart(labels, values, title=None):
    fig = plt.figure(figsize=(3.5, 3.5), dpi=200)
    ax = fig.add_axes([0.05, 0.05, 0.9, 0.9])
    ax.set_facecolor((0, 0, 0, 0))
    fig.patch.set_alpha(0)
    palette = ["#00E5FF", "#22C55E", "#A78BFA", "#FBBF24", "#FB7185", "#60A5FA", "#34D399", "#F472B6", "#F97316", "#94A3B8"]
    colors = [palette[i % len(palette)] for i in range(len(labels))]
    wedges, _ = ax.pie(values, labels=None, startangle=90, colors=colors, wedgeprops=dict(width=0.38, edgecolor=(0, 0, 0, 0)))
    ax.add_artist(plt.Circle((0, 0), 0.62, color=(0, 0, 0, 0)))
    ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=7, frameon=False, labelcolor="#C7D2FE")
    if title:
        ax.set_title(title, color="#E5E7EB", fontsize=10, fontweight="bold", loc="left")
    return mpl_fig_to_pil(fig)


def render_gauge(value, vmin=0, vmax=100, title=None, subtitle=None):
    fig = plt.figure(figsize=(3.8, 2.4), dpi=200)
    ax = fig.add_axes([0.05, 0.05, 0.9, 0.85])
    ax.set_facecolor((0, 0, 0, 0))
    fig.patch.set_alpha(0)
    ax.axis("off")
    angles = np.linspace(-np.pi, 0, 4)
    seg_colors = ["#22C55E", "#FBBF24", "#FB7185"]
    for i in range(3):
        theta1, theta2 = angles[i], angles[i + 1]
        ax.add_patch(matplotlib.patches.Wedge((0, 0), 1.0, np.degrees(theta1), np.degrees(theta2), width=0.25, facecolor=seg_colors[i], alpha=0.85))
    frac = (value - vmin) / (vmax - vmin)
    frac = min(max(frac, 0), 1)
    theta = -np.pi + frac * np.pi
    ax.plot([0, 0.78 * np.cos(theta)], [0, 0.78 * np.sin(theta)], color="#E5E7EB", linewidth=2.6)
    ax.add_patch(matplotlib.patches.Circle((0, 0), 0.04, color="#E5E7EB"))
    ax.text(-1.02, -0.05, f"{vmin}", color="#94A3B8", fontsize=8, ha="left")
    ax.text(1.02, -0.05, f"{vmax}", color="#94A3B8", fontsize=8, ha="right")
    ax.text(0, -0.30, f"{value:.0f}", color="#E5E7EB", fontsize=16, fontweight="bold", ha="center")
    if title:
        ax.text(-1.0, 0.55, title, color="#E5E7EB", fontsize=10, fontweight="bold", ha="left")
    if subtitle:
        ax.text(-1.0, 0.40, subtitle, color="#94A3B8", fontsize=8, ha="left")
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-0.55, 1.05)
    return mpl_fig_to_pil(fig)


def draw_panel(base_img, rect, fill="#0B1324", border="#1F2A44", radius=18, shadow=True):
    x0, y0, x1, y1 = rect
    panel_layer = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(panel_layer)
    if shadow:
        shadow_layer = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
        ds = ImageDraw.Draw(shadow_layer)
        ds.rounded_rectangle([x0 + 8, y0 + 10, x1 + 8, y1 + 10], radius=radius, fill=(0, 0, 0, 160))
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(12))
        base_img.alpha_composite(shadow_layer)
    d.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=hex_to_rgb(fill) + (255,), outline=hex_to_rgb(border) + (255,), width=2)
    base_img.alpha_composite(panel_layer)


def add_accent_strip(base_img, rect, color="#00E5FF", height=10, radius=18):
    x0, y0, x1, y1 = rect
    strip_layer = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(strip_layer)
    d.rounded_rectangle([x0, y0, x1, y0 + height], radius=radius, fill=hex_to_rgb(color) + (230,))
    blurred = strip_layer.filter(ImageFilter.GaussianBlur(6))
    base_img.alpha_composite(blurred)
    base_img.alpha_composite(strip_layer)


def add_glow_rectangle(base_img, rect, glow_color="#00E5FF", glow_radius=18, glow_alpha=160, border_width=3):
    x0, y0, x1, y1 = rect
    glow_layer = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow_layer)
    rgb = hex_to_rgb(glow_color)
    for w in range(border_width, border_width + 3):
        draw.rectangle([x0 - w, y0 - w, x1 + w, y1 + w], outline=rgb + (glow_alpha,), width=w)
    blurred = glow_layer.filter(ImageFilter.GaussianBlur(radius=glow_radius))
    base_img.alpha_composite(blurred)
    draw2 = ImageDraw.Draw(base_img)
    draw2.rectangle([x0, y0, x1, y1], outline=rgb + (220,), width=2)


def paste_center(base_img, chart_img, rect, margin=10):
    x0, y0, x1, y1 = rect
    w = x1 - x0 - 2 * margin
    h = y1 - y0 - 2 * margin
    img = chart_img.copy().resize((w, h), resample=Image.LANCZOS)
    base_img.alpha_composite(img, (x0 + margin, y0 + margin))


def create_base_canvas(title, subtitle, as_of_text, run_id_text, page_label=None):
    W, H = 3840, 2160
    bg = linear_gradient((W, H), "#070A12", "#0B1023", horizontal=False).convert("RGBA")
    draw = ImageDraw.Draw(bg)

    header_h = 150
    header = linear_gradient((W, header_h), "#0B1023", "#050812", horizontal=True).convert("RGBA")
    bg.alpha_composite(header, (0, 0))
    draw.line([(0, header_h - 2), (W, header_h - 2)], fill=hex_to_rgb("#00E5FF") + (180,), width=3)

    nav_w = 260
    nav = Image.new("RGBA", (nav_w, H), (8, 12, 22, 255))
    nav_grad = linear_gradient((nav_w, H), "#070A12", "#0B1023", horizontal=False).convert("RGBA")
    nav = Image.alpha_composite(nav, nav_grad)
    bg.alpha_composite(nav, (0, 0))
    draw.line([(nav_w, header_h), (nav_w, H)], fill=hex_to_rgb("#1F2A44") + (255,), width=2)

    title_font = ImageFont.truetype(FONT_BOLD, 46)
    subtitle_font = ImageFont.truetype(FONT_REG, 24)
    meta_font = ImageFont.truetype(FONT_REG, 22)
    nav_font = ImageFont.truetype(FONT_BOLD, 24)
    nav_small = ImageFont.truetype(FONT_REG, 18)

    draw.text((nav_w + 30, 28), title, font=title_font, fill=hex_to_rgb("#E5E7EB") + (255,))
    draw.text((nav_w + 30, 86), subtitle, font=subtitle_font, fill=hex_to_rgb("#94A3B8") + (255,))

    meta = f"As-of: {as_of_text}   •   Run: {run_id_text}"
    draw.text((W - 30 - draw.textlength(meta, font=meta_font), 46), meta, font=meta_font, fill=hex_to_rgb("#C7D2FE") + (255,))

    if page_label:
        draw.text((nav_w + 30, header_h - 38), page_label, font=meta_font, fill=hex_to_rgb("#00E5FF") + (255,))

    nav_items = [
        ("PULSE", "Market overview & movers"),
        ("SECTORS", "Weights & rotation"),
        ("RISK", "Drawdown • VaR • vol"),
        ("FORECAST", "MAE/RMSE • drift"),
        ("OPS", "SLA • latency • DQ"),
        ("GOV", "Catalogues & lineage"),
    ]
    y = header_h + 40
    for it, desc in nav_items:
        draw.text((28, y), it, font=nav_font, fill=hex_to_rgb("#E5E7EB") + (255,))
        draw.text((28, y + 28), desc, font=nav_small, fill=hex_to_rgb("#94A3B8") + (255,))
        y += 110

    footer_font = ImageFont.truetype(FONT_REG, 18)
    footer = "FTSE-100-Financial-Analysis • UK Market Terminal (Portfolio) • Not financial advice"
    draw.text((nav_w + 30, H - 34), footer, font=footer_font, fill=hex_to_rgb("#64748B") + (255,))

    return bg


def draw_kpi_tile(img, rect, label, value, sub=None, accent="#00E5FF"):
    x0, y0, x1, y1 = rect
    draw_panel(img, rect, fill="#0B1324", border="#1F2A44", radius=16, shadow=True)
    add_accent_strip(img, rect, color=accent, height=8, radius=16)
    add_glow_rectangle(img, rect, glow_color=accent, glow_radius=12, glow_alpha=90, border_width=2)

    d = ImageDraw.Draw(img)
    label_font = ImageFont.truetype(FONT_BOLD, 22)
    value_font = ImageFont.truetype(FONT_BOLD, 42)
    sub_font = ImageFont.truetype(FONT_REG, 18)

    d.text((x0 + 22, y0 + 18), label.upper(), font=label_font, fill=hex_to_rgb("#94A3B8") + (255,))
    d.text((x0 + 22, y0 + 58), value, font=value_font, fill=hex_to_rgb("#E5E7EB") + (255,))
    if sub:
        d.text((x0 + 22, y1 - 34), sub, font=sub_font, fill=hex_to_rgb("#C7D2FE") + (255,))


def draw_table(img, rect, headers, rows, col_widths=None, accent="#00E5FF"):
    x0, y0, x1, y1 = rect
    draw_panel(img, rect, fill="#0B1324", border="#1F2A44", radius=16, shadow=True)
    add_accent_strip(img, rect, color=accent, height=8, radius=16)

    d = ImageDraw.Draw(img)
    header_font = ImageFont.truetype(FONT_BOLD, 20)
    cell_font = ImageFont.truetype(FONT_REG, 18)

    ncol = len(headers)
    if col_widths is None:
        total_w = x1 - x0 - 40
        col_widths = [total_w / ncol] * ncol

    cur_x = x0 + 20
    cur_y = y0 + 18
    for h, w in zip(headers, col_widths):
        d.text((cur_x, cur_y), h, font=header_font, fill=hex_to_rgb("#E5E7EB") + (255,))
        cur_x += w

    d.line([(x0 + 18, cur_y + 32), (x1 - 18, cur_y + 32)], fill=hex_to_rgb("#1F2A44") + (255,), width=2)

    row_h = 30
    cur_y = cur_y + 42
    for r in rows:
        cur_x = x0 + 20
        for val, w in zip(r, col_widths):
            d.text((cur_x, cur_y), str(val), font=cell_font, fill=hex_to_rgb("#C7D2FE") + (255,))
            cur_x += w
        cur_y += row_h
        if cur_y > y1 - 30:
            break


def load_inputs():
    market_overview = pd.read_csv(MART_DIR / "market_overview.csv")
    market_overview["timestamp_london"] = pd.to_datetime(market_overview["timestamp_london"])

    drawdown_risk = pd.read_csv(MART_DIR / "drawdown_risk.csv")
    drawdown_risk["date"] = pd.to_datetime(drawdown_risk["date"])

    sector_rotation = pd.read_csv(MART_DIR / "sector_rotation.csv")
    sector_rotation["date"] = pd.to_datetime(sector_rotation["date"])

    top_movers = pd.read_csv(MART_DIR / "top_movers.csv")
    top_movers["date"] = pd.to_datetime(top_movers["date"])

    pipeline_health = pd.read_csv(MART_DIR / "pipeline_health.csv")
    pipeline_health["date"] = pd.to_datetime(pipeline_health["date"])

    latency_sla = pd.read_csv(MART_DIR / "latency_sla.csv")
    latency_sla["hour"] = pd.to_datetime(latency_sla["hour"])

    forecasting_metrics = pd.read_csv(MART_DIR / "forecasting_metrics.csv")
    forecasting_metrics["timestamp"] = pd.to_datetime(forecasting_metrics["timestamp"])

    model_monitoring = pd.read_csv(MART_DIR / "model_monitoring.csv")

    vol_regimes = pd.read_csv(MART_DIR / "volatility_regimes.csv")
    vol_regimes["timestamp_london"] = pd.to_datetime(vol_regimes["timestamp_london"])

    universe = pd.read_csv(UNIVERSE_PATH)
    sector_weights = universe.groupby("sector")["index_weight"].sum().sort_values(ascending=False)

    return {
        "market_overview": market_overview,
        "drawdown_risk": drawdown_risk,
        "sector_rotation": sector_rotation,
        "top_movers": top_movers,
        "pipeline_health": pipeline_health,
        "latency_sla": latency_sla,
        "forecasting_metrics": forecasting_metrics,
        "model_monitoring": model_monitoring,
        "vol_regimes": vol_regimes,
        "sector_weights": sector_weights,
        "universe": universe,
    }


def build_page_01(ctx):
    mo = ctx["market_overview"].sort_values("timestamp_london")
    mo["date"] = mo["timestamp_london"].dt.date
    last_date = mo["date"].max()
    mo_day = mo[mo["date"] == last_date]
    x = mo_day["timestamp_london"].dt.strftime("%H:%M").tolist()
    y = mo_day["close"].astype(float).tolist()

    dd_latest = ctx["drawdown_risk"].sort_values("date").iloc[-1]
    vol20 = float(dd_latest["rolling_vol_20"])
    var95 = float(dd_latest["var_95"])
    dd = float(dd_latest["drawdown_pct"])
    risk_score = min(100, abs(dd) * 5 + vol20 * 250 + abs(var95) * 2000)

    sw = ctx["sector_weights"]
    top = sw.head(7)
    other = sw.iloc[7:].sum()
    donut_labels = list(top.index) + ["Other"]
    donut_values = list(top.values) + [other]

    movers = ctx["top_movers"]
    latest_movers_date = movers["date"].max()
    movers_latest = movers[movers["date"] == latest_movers_date]
    gainers = movers_latest[movers_latest["direction"] == "gainer"].sort_values("return", ascending=False).head(6)
    losers = movers_latest[movers_latest["direction"] == "loser"].sort_values("return").head(6)
    table_rows = []
    for i in range(6):
        g = gainers.iloc[i] if i < len(gainers) else None
        l = losers.iloc[i] if i < len(losers) else None
        table_rows.append([
            (g["ticker"] if g is not None else ""),
            (f"{g['return']*100:+.2f}%" if g is not None else ""),
            (l["ticker"] if l is not None else ""),
            (f"{l['return']*100:+.2f}%" if l is not None else ""),
        ])

    latest_row = mo.sort_values("timestamp_london").iloc[-1]
    img = create_base_canvas(
        title="FTSE 100 — UK Market Terminal",
        subtitle="Power BI Export Pack • Pulse Overview",
        as_of_text=str(last_date),
        run_id_text=str(latest_row["run_id"]),
        page_label="PBI • Page 01",
    )

    W, H = img.size
    nav_w, header_h, margin = 260, 150, 26
    content_x0 = nav_w + margin
    content_y0 = header_h + margin
    content_x1 = W - margin

    kpi_h = 180
    gap = 18
    tile_w = int((content_x1 - content_x0 - 3 * gap) / 4)
    tiles = []
    for i in range(4):
        x0 = content_x0 + i * (tile_w + gap)
        tiles.append((x0, content_y0, x0 + tile_w, content_y0 + kpi_h))

    close_last = y[-1]
    close_first = y[0]
    ret_pct = (close_last / close_first - 1) * 100
    hi = float(mo_day["high"].max())
    lo = float(mo_day["low"].min())
    freshness_minutes = float(latest_row["freshness_minutes"])

    draw_kpi_tile(img, tiles[0], "Last", f"{close_last:,.2f}", f"Return {ret_pct:+.2f}%", accent="#00E5FF")
    draw_kpi_tile(img, tiles[1], "High / Low", f"{hi:,.2f} / {lo:,.2f}", "Session range", accent="#A78BFA")
    draw_kpi_tile(img, tiles[2], "Vol (20)", f"{vol20*100:.2f}%", "Realised (rolling)", accent="#22C55E")
    draw_kpi_tile(img, tiles[3], "Freshness", f"{freshness_minutes/60:.1f}h", "Data freshness", accent="#FBBF24")

    y_top = content_y0 + kpi_h + 22
    panel1 = (content_x0, y_top, content_x0 + int((content_x1 - content_x0) * 0.62), y_top + 820)
    panel2 = (panel1[2] + 20, y_top, content_x1, y_top + 400)
    panel3 = (panel1[2] + 20, panel2[3] + 20, content_x1, y_top + 820)
    panel4 = (content_x0, panel1[3] + 22, content_x1, H - 70)

    for rect, accent in [(panel1, "#00E5FF"), (panel2, "#A78BFA"), (panel3, "#22C55E"), (panel4, "#FBBF24")]:
        draw_panel(img, rect, fill="#0B1324", border="#1F2A44", radius=18, shadow=True)
        add_accent_strip(img, rect, color=accent, height=10, radius=18)
        add_glow_rectangle(img, rect, glow_color=accent, glow_radius=14, glow_alpha=70, border_width=2)

    paste_center(img, render_line_chart(x, y, title="Intraday Close (5m)", subtitle="London time • points"), panel1, margin=22)
    paste_center(img, render_donut_chart(donut_labels, donut_values, title="Index Weight by Sector"), panel2, margin=18)
    paste_center(img, render_gauge(risk_score, 0, 100, title="Risk Score", subtitle=f"DD {dd:+.2f}% • VaR95 {var95*100:.2f}%"), panel3, margin=18)
    draw_table(img, panel4, headers=["Top Gainers", "Move", "Top Losers", "Move"], rows=table_rows, col_widths=[320, 140, 320, 140], accent="#FBBF24")

    img.convert("RGB").save(EXPORT_DIR / "pbi_page_01_market_overview.png", "PNG")


def main():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    ctx = load_inputs()

    # For brevity, we only rebuild page 01 in this script.
    # The repo ships all 6 pages already under exports/.
    build_page_01(ctx)

    print("✅ Power BI export pack refreshed (page 01).")
    print(f"Output folder: {EXPORT_DIR}")


if __name__ == "__main__":
    main()
