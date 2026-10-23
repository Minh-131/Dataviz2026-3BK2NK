"""Interactive Plotly charts with shared visual styling."""
import pandas as pd
import plotly.express as px

from src.flags import flag_url
import plotly.graph_objects as go

NAVY = "#26322D"
TEAL = "#537D64"
CORAL = "#AD4834"
MUTED = "#6E776E"
PALETTE = ["#537D64", "#AD4834", "#836E96", "#BA9350", "#456A85", "#899C56", "#AD7582"]

# Updated once per Streamlit rerun, before any chart is constructed.
_DARK_MODE = False


def set_chart_theme(dark_mode: bool) -> None:
    """Keep Plotly axes, hover tooltips, legends and maps in sync with the UI."""
    global _DARK_MODE
    _DARK_MODE = bool(dark_mode)


def theme_color(light: str, dark: str) -> str:
    return dark if _DARK_MODE else light


def active_palette() -> list[str]:
    """Use higher-contrast colors in dark mode without changing chart meaning."""
    return (["#98C2A4", "#F3A78E", "#CAB6EA", "#F2D086", "#95B5D4", "#B9CB8C", "#E7B2BF"]
            if _DARK_MODE else PALETTE)


def series_color(color: str) -> str:
    """Translate the three primary light-mode plot colors to dark equivalents."""
    if not _DARK_MODE:
        return color
    return {TEAL: "#98C2A4", CORAL: "#F3A78E", "#7C69B0": "#CAB6EA"}.get(color, color)



def finish(fig, height=365, showlegend=True):
    text = theme_color(NAVY, "#F5F1E6")
    muted = theme_color(MUTED, "#B5C2B9")
    axis = theme_color("#D8D6CD", "#546660")
    grid = theme_color("#ECE7DE", "#344843")
    surface = theme_color("#FFFDF8", "#1C3332")
    fig.update_layout(
        height=height,
        margin=dict(l=56, r=14, t=38, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", color=text, size=12),
        xaxis=dict(showgrid=False, linecolor=axis, tickfont=dict(color=muted), title_font=dict(color=text), automargin=True),
        yaxis=dict(gridcolor=grid, zeroline=False, tickfont=dict(color=muted), title_font=dict(color=text), automargin=True),
        legend=dict(orientation="h", y=-0.18, x=0, title_text="", font=dict(color=text)),
        showlegend=showlegend,
        hoverlabel=dict(bgcolor=surface, font_color=text, bordercolor=axis),
        coloraxis_colorbar=dict(tickfont=dict(color=muted), title_font=dict(color=text)),
    )
    return fig


def history_line(frame: pd.DataFrame, metric: str, label: str, suffix: str = "", color: str = TEAL,
                 notes: dict | None = None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=frame.year, y=frame[metric], mode="lines+markers", name=label,
        line=dict(color=series_color(color), width=3.5), marker=dict(size=8),
        hovertemplate=f"%{{x}}<br><b>%{{y:,.2f}}{suffix}</b><extra></extra>",
    ))
    fig.update_xaxes(dtick=1)
    fig.update_yaxes(title_text=label, ticksuffix=suffix)
    for x, text in (notes or {}).items():
        point = frame.loc[frame.year.eq(x), metric]
        if len(point):
            fig.add_annotation(x=x, y=float(point.iloc[0]), text=text, showarrow=True, ax=0, ay=-34,
                               font=dict(size=11, color=theme_color(NAVY, "#F5F1E6")),
                               arrowcolor=theme_color(MUTED, "#B5C2B9"))
    return finish(fig, showlegend=False)


def ranked_change(frame: pd.DataFrame, value: str, title: str):
    data = frame.sort_values(value)
    colors = [series_color(TEAL if val < 0 else CORAL) for val in data[value]]
    fig = go.Figure(go.Bar(
        y=data.country, x=data[value], orientation="h", marker_color=colors,
        customdata=data[["country"]],
        hovertemplate="%{y}<br>Change: %{x:+,.1f}<extra></extra>",
    ))
    fig.add_vline(x=0, line_color=theme_color("#A4B1BC", "#7D94A9"), line_width=1)
    fig.update_xaxes(title_text=title, zeroline=True)
    fig.update_yaxes(title_text="")
    return finish(fig, height=max(340, 50 * len(data) + 95), showlegend=False)


def group_history(frame: pd.DataFrame, metric: str, title: str, selections: list[str], highlight: str | None = None):
    selected = frame.loc[frame.country.isin(selections)]
    fig = px.line(
        selected, x="year", y=metric, color="country", markers=True,
        color_discrete_sequence=active_palette(),
        labels={"year": "Year", metric: title, "country": "Group"},
        hover_data={"year": True, metric: ":,.2f"},
    )
    fig.update_traces(line_width=3, marker_size=7)
    if highlight in selections:
        for trace in fig.data:
            if trace.name == highlight:
                trace.update(line_width=5.5, marker_size=9)
            else:
                trace.update(opacity=0.55)
    fig.update_xaxes(dtick=1)
    return finish(fig, height=425)


def country_map(frame: pd.DataFrame, metric: str, label: str):
    """Land without a valid observation stays neutral grey, never ocean blue.

    Choropleth country polygons are plotted only when a value exists; the
    geographic base layer supplies the separate missing-data color.
    """
    df = frame.dropna(subset=[metric, "iso3"]).copy()
    missing = theme_color("#D4D4D0", "#89908D")
    ocean = theme_color("#EAF2F4", "#0C2635")
    border = theme_color("#FFFFFF", "#243A3E")
    fig = px.choropleth(
        df, locations="iso3", color=metric, hover_name="country",
        hover_data={metric: ":,.1f"},
        color_continuous_scale=["#F4E6C7", "#E0BC83", "#B96B4D", "#7D3229"],
        labels={metric: label}, projection="natural earth",
        range_color=(0, 100) if metric == "CoHD_headcount" else None,
    )
    fig.update_traces(marker_line_color=border, marker_line_width=0.35)
    fig.update_geos(
        showframe=False, showcoastlines=True, coastlinecolor=theme_color("#B5B5B0", "#3F5655"),
        showcountries=True, countrycolor=border, countrywidth=.65,
        showland=True, landcolor=missing,
        showocean=True, oceancolor=ocean,
        showlakes=True, lakecolor=ocean,
        bgcolor=ocean,
    )
    fig.update_layout(
        geo=dict(bgcolor=ocean),
        coloraxis_colorbar=dict(title=dict(text=label, side="top"), thickness=15, len=.65),
    )
    return finish(fig, height=515, showlegend=False)


def nutrition_scatter(frame: pd.DataFrame, outcome: str, ylabel: str, label: str | None = None,
                      flag_iso: str | None = None):
    size = frame["population"].fillna(0).clip(lower=0)
    size = size.where(size.gt(0), other=1000000)
    graph = frame.assign(pop_size=size)
    fig = px.scatter(
        graph, x="CoHD_headcount", y=outcome, color="region", size="pop_size",
        size_max=34, opacity=0.8, color_discrete_sequence=active_palette(),
        hover_name="country", hover_data={"pop_size": False, "CoHD_headcount": ":.1f", outcome: ":.1f"},
        labels={"CoHD_headcount": "Share who cannot afford a healthy diet (%)", outcome: ylabel, "region": "Region"},
    )
    fig.update_traces(marker=dict(line=dict(width=0.7, color=theme_color("white", "#1B3043"))))
    fig.update_xaxes(range=[0, 103])
    row = frame[frame.country.eq(label)] if label else frame.iloc[0:0]
    if len(row):
        r = row.iloc[0]
        fig.add_annotation(x=float(r.CoHD_headcount), y=float(r[outcome]), text=f"<b>{label}</b>",
                           showarrow=True, ax=-60, ay=-30, font=dict(size=12, color=series_color(CORAL)),
                           arrowcolor=series_color(CORAL),
                           bgcolor=theme_color("rgba(255,255,255,0.88)", "rgba(21,38,58,0.94)"))
        url = flag_url(flag_iso or "", 80)
        if url:
            ymax = float(frame[outcome].max()) or 1.0
            fig.add_layout_image(source=url, xref="x", yref="y", x=float(r.CoHD_headcount) + 1.6, y=float(r[outcome]),
                                 sizex=5, sizey=ymax * 0.07, xanchor="left", yanchor="middle", sizing="contain", layer="above")
    return finish(fig, height=485)


def compare_countries(frame: pd.DataFrame, metric: str, title: str, selected: list[str], flags: dict | None = None):
    data = frame[frame.country.isin(selected)].dropna(subset=[metric])
    fig = px.line(data, x="year", y=metric, color="country", markers=True,
                  color_discrete_sequence=active_palette(), labels={"year": "Year", metric: title, "country": "Country"})
    fig.update_traces(line_width=3, marker_size=6)
    fig.update_xaxes(dtick=1)
    if flags and len(data):
        span = float(data[metric].max() - data[metric].min()) or 1.0
        last_year = int(data.year.max())
        for name, grp in data.groupby("country"):
            end = grp.sort_values("year").iloc[-1]
            url = flag_url(flags.get(name, ""), 80)
            if url:
                fig.add_layout_image(source=url, xref="x", yref="y", x=float(end.year) + 0.12, y=float(end[metric]),
                                     sizex=0.42, sizey=span * 0.09, xanchor="left", yanchor="middle",
                                     sizing="contain", layer="above")
        fig.update_xaxes(range=[data.year.min() - 0.3, last_year + 0.75])
    return finish(fig, height=440)


def ranks(frame: pd.DataFrame, metric: str, label: str, top_n: int, flags: dict | None = None):
    data = frame.dropna(subset=[metric]).nlargest(top_n, metric).sort_values(metric)
    fig = px.bar(data, x=metric, y="country", orientation="h", color_discrete_sequence=[series_color(CORAL)],
                 labels={metric: label, "country": ""}, hover_data={metric: ":,.1f"})
    fig.update_yaxes(title_text="")
    if flags and len(data):
        top = float(data[metric].max()) or 1.0
        for _, row in data.iterrows():
            url = flag_url(flags.get(row.country, ""), 80)
            if url:
                fig.add_layout_image(source=url, xref="x", yref="y", x=float(row[metric]) + top * 0.012, y=row.country,
                                     sizex=top * 0.06, sizey=0.62, xanchor="left", yanchor="middle",
                                     sizing="contain", layer="above")
        fig.update_xaxes(range=[0, top * 1.1])
    return finish(fig, height=max(340, top_n * 32 + 100), showlegend=False)
