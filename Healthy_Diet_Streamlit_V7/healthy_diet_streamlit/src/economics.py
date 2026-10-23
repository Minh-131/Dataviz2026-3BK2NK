"""Optional World Bank food inflation + existing GDP and affordability analyses.

Food inflation source (user-provided Excel): World Bank Global Database of Inflation,
annual sheet 'fcpi_a'. This is food CPI inflation, not the CoAHD price index.
GDP in this project is the existing `gdp_pc_ppp` column. Its WDI definition
and vintage must be verified against NY.GDP.PCAP.PP.KD before final publication.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.charts import CORAL, TEAL, finish, active_palette, series_color, theme_color
from src.statistics import spearman_corr
from src.flags import flag_url

ROOT = Path(__file__).resolve().parents[1]
INFLATION_FILE = ROOT / "data" / "Inflation-data.xlsx"


def cross_section(countries: pd.DataFrame, year: int) -> pd.DataFrame:
    """Only paired observations with valid GDP, unaffordability, and diet cost."""
    subset = countries.loc[countries.year.eq(year)].copy()
    subset = subset.dropna(subset=["gdp_pc_ppp", "CoHD_headcount", "CoHD_PPP"])
    return subset.loc[subset.gdp_pc_ppp.gt(0)].copy()


def gdp_associations(countries: pd.DataFrame, year: int) -> dict:
    d = cross_section(countries, year)
    return {
        "n": len(d),
        "rho_gdp_vs_unafford": spearman_corr(d.gdp_pc_ppp, d.CoHD_headcount) if len(d)>2 else float("nan"),
        "rho_gdp_vs_diet_cost": spearman_corr(d.gdp_pc_ppp, d.CoHD_PPP) if len(d)>2 else float("nan"),
    }


def gdp_affordability_chart(df: pd.DataFrame):
    fig = px.scatter(
        df, x="gdp_pc_ppp", y="CoHD_headcount", color="income_group",
        hover_name="country", log_x=True,
        labels={"gdp_pc_ppp": "GDP per person (PPP, current international $, log scale)",
                "CoHD_headcount": "Share who cannot afford (%)",
                "income_group": "Income group"},
        hover_data={"gdp_pc_ppp": ":,.0f", "CoHD_headcount": ":.1f", "CoHD_PPP": ":.2f"},
        color_discrete_sequence=active_palette(), opacity=0.8,
    )
    fig.update_traces(marker=dict(size=9, line=dict(color=theme_color("white", "#1B3043"), width=0.5)))
    fig.update_yaxes(range=[-3, 103]); fig.update_xaxes(type="log")
    return finish(fig, height=480)


def cost_vs_affordability_chart(df: pd.DataFrame):
    fig = px.scatter(
        df, x="CoHD_PPP", y="CoHD_headcount", color="income_group",
        hover_name="country", opacity=0.8, color_discrete_sequence=active_palette(),
        labels={"CoHD_PPP": "Healthy diet cost (PPP $/person/day)",
                "CoHD_headcount": "Share who cannot afford (%)", "income_group": "Income group"},
        hover_data={"CoHD_PPP": ":.2f", "CoHD_headcount": ":.1f", "gdp_pc_ppp": ":,.0f"},
    )
    fig.update_traces(marker=dict(size=9, line=dict(color=theme_color("white", "#1B3043"), width=0.5)))
    pair = df[df.country.isin(["Nigeria", "Cyprus"])].set_index("country")
    if {"Nigeria", "Cyprus"}.issubset(pair.index):
        price = float(pair.loc["Nigeria", "CoHD_PPP"])
        fig.add_vline(x=price, line_dash="dot", line_width=1.2, line_color=theme_color("#8A8A80", "#9FB0A8"))
        fig.add_annotation(x=price, y=102, yanchor="bottom", showarrow=False, text=f"Same price: {price:.2f} PPP $",
                           font=dict(size=11, color=theme_color("#26322D", "#F5F1E6")))
        for name, ay in (("Nigeria", -26), ("Cyprus", -30)):
            r = pair.loc[name]
            url = flag_url(r.iso3, 80) if "iso3" in pair.columns else None
            if url:
                fig.add_layout_image(source=url, xref="x", yref="y", x=float(r.CoHD_PPP) - 0.06, y=float(r.CoHD_headcount),
                                     sizex=0.26, sizey=7, xanchor="right", yanchor="middle", sizing="contain", layer="above")
            color = series_color(CORAL if name == "Nigeria" else TEAL)
            fig.add_annotation(x=float(r.CoHD_PPP), y=float(r.CoHD_headcount),
                               text=f"<b>{name}</b> {r.CoHD_headcount:.0f}%" if r.CoHD_headcount >= 10 else f"<b>{name}</b> {r.CoHD_headcount:.1f}%", showarrow=True, ax=70, ay=ay,
                               arrowcolor=color, arrowwidth=1.4, font=dict(color=color, size=12),
                               bgcolor=theme_color("rgba(255,255,255,0.92)", "rgba(21,38,58,0.94)"))
    fig.update_yaxes(range=[-3,103])
    return finish(fig, height=470)


def _long_excel_sheet(book, sheet: str, value_col: str) -> pd.DataFrame:
    """Parse the World Bank Global Inflation Database annual wide Excel sheet.

    Requires the publisher's ISO3 'Country Code' and year columns; no fuzzy
    country-name merge. Accepts path or file-like object; each read resets it.
    """
    if hasattr(book, "seek"):
        book.seek(0)
    wide = pd.read_excel(book, sheet_name=sheet)
    wide.columns = [str(c).strip() for c in wide.columns]
    iso_candidate = next((c for c in ("Country Code", "ISO3", "Country code") if c in wide), None)
    if iso_candidate is None:
        raise ValueError(f"Sheet {sheet} is missing an ISO3 country-code column")
    year_cols = [c for c in wide.columns if c.isdigit() and len(c)==4 and 2017 <= int(c) <= 2025]
    if not year_cols:
        raise ValueError(f"Sheet {sheet} contains no year columns in 2017 to 2025")
    tidy = wide[[iso_candidate] + year_cols].melt(id_vars=[iso_candidate], var_name="year", value_name=value_col)
    tidy = tidy.rename(columns={iso_candidate:"iso3"})
    tidy["iso3"] = tidy.iso3.astype(str).str.strip().str.upper()
    tidy["year"] = tidy.year.astype(int)
    tidy[value_col] = pd.to_numeric(tidy[value_col], errors="coerce")
    tidy = tidy[tidy.iso3.str.fullmatch(r"[A-Z]{3}", na=False)].dropna(subset=[value_col])
    if tidy.duplicated(["iso3", "year"]).any():
        raise ValueError(f"Duplicate ISO3-year rows in {sheet}; manual inspection needed")
    return tidy.reset_index(drop=True)


def read_inflation_excel(book) -> pd.DataFrame:
    """Read annual headline and food CPI *inflation rates* in percent.

    If headline sheet is absent, food still works; data are never silently
    imputed, and no country-name fuzzy joins are performed.
    """
    food = _long_excel_sheet(book, "fcpi_a", "food_inflation_pct")
    try:
        headline = _long_excel_sheet(book, "hcpi_a", "headline_inflation_pct")
    except (ValueError, KeyError):
        headline = pd.DataFrame(columns=["iso3", "year", "headline_inflation_pct"])
    merged = food.merge(headline, on=["iso3", "year"], how="left", validate="one_to_one")
    return merged.sort_values(["iso3", "year"]).reset_index(drop=True)


def merged_inflation_change(countries: pd.DataFrame, inflation: pd.DataFrame, year: int) -> pd.DataFrame:
    """Annual food inflation vs year-on-year change in affordability rate.

    Changes are percentage *points*. Do not compare nominal food CPI with
    the change of PPP denominated diet costs as if the latter were inflation.
    """
    subset = countries[["iso3", "country", "region", "year", "CoHD_headcount", "CoHD_PPP"]].copy()
    subset = subset.sort_values(["iso3", "year"])
    prior = subset[["iso3", "year", "CoHD_headcount"]].copy()
    prior["year"] += 1
    prior = prior.rename(columns={"CoHD_headcount": "prior_unafford_pct"})
    subset = subset.merge(prior, on=["iso3", "year"], how="left", validate="one_to_one")
    subset["affordability_change_pp"] = subset.CoHD_headcount - subset.prior_unafford_pct
    subset = subset[subset.year.eq(year)]
    result = subset.merge(inflation, on=["iso3", "year"], how="inner", validate="one_to_one")
    return result.dropna(subset=["food_inflation_pct", "affordability_change_pp"])


def inflation_change_chart(df: pd.DataFrame):
    fig = px.scatter(
        df, x="food_inflation_pct", y="affordability_change_pp", color="region",
        hover_name="country", color_discrete_sequence=active_palette(), opacity=0.8,
        labels={"food_inflation_pct": "Food CPI inflation (annual %)",
                "affordability_change_pp": "Change in unaffordability (pp)", "region": "Region"},
        hover_data={"food_inflation_pct": ":.1f", "affordability_change_pp": ":+.1f"},
    )
    fig.add_hline(y=0, line_dash="dash", line_color=theme_color("#91A4B1", "#7D94A9"))
    fig.add_vline(x=0, line_dash="dash", line_color=theme_color("#91A4B1", "#7D94A9"))
    fig.update_traces(marker=dict(size=9, line=dict(color=theme_color("white", "#1B3043"), width=0.5)))
    return finish(fig, height=465)
