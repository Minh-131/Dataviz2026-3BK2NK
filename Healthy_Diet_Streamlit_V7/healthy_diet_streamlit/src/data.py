"""Validated data access for the UN SDG 2 healthy diet affordability dashboard."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
COUNTRY_REQUIRED = {
    "country", "iso3", "year", "region", "income_group", "population",
    "CoHD_headcount", "CoHD_unafford_n", "CoHD_PPP", "stunting_pct", "pou", "pou_below_2_5",
}
AGG_REQUIRED = {
    "country", "iso3", "group_type", "year", "CoHD_headcount",
    "CoHD_unafford_n", "CoHD_PPP_PoP",
}
METRICS = {
    "Share who cannot afford (%)": ("CoHD_headcount", "%", "Share of people unable to afford a healthy diet"),
    "People who cannot afford (millions)": ("CoHD_unafford_n", "million", "People unable to afford a healthy diet"),
    "Cost of a healthy diet (PPP $/day)": ("CoHD_PPP", "PPP $/person/day", "Cost of a healthy diet"),
}


def read_datasets(data_dir: Path = DATA_DIR) -> tuple[pd.DataFrame, pd.DataFrame]:
    countries = pd.read_csv(data_dir / "fpn_countries.csv")
    aggregates = pd.read_csv(data_dir / "fpn_aggregates.csv")
    for title, frame, required, keys in [
        ("Countries", countries, COUNTRY_REQUIRED, ["iso3", "year"]),
        ("Aggregates", aggregates, AGG_REQUIRED, ["group_type", "country", "year"]),
    ]:
        missing = required - set(frame.columns)
        if missing:
            raise ValueError(f"{title} CSV missing mandatory columns: {', '.join(sorted(missing))}")
        if frame.duplicated(keys).any():
            raise ValueError(f"{title} CSV has duplicate key rows: {keys}")
        frame["year"] = pd.to_numeric(frame["year"], errors="raise").astype(int)
        for column in ["CoHD_headcount", "CoHD_unafford_n", "CoHD_PPP"]:
            if column in frame:
                frame[column] = pd.to_numeric(frame[column], errors="coerce")
    countries["region"] = countries["region"].fillna("Unclassified")
    countries["income_group"] = countries["income_group"].fillna("Unclassified")
    return countries, aggregates


def world_rows(aggregates: pd.DataFrame) -> pd.DataFrame:
    world = aggregates[aggregates.group_type.eq("world")].sort_values("year")
    if world.empty:
        raise ValueError("World benchmark missing from aggregates CSV")
    return world


def current_world(aggregates: pd.DataFrame, year: int) -> pd.Series:
    rows = world_rows(aggregates)
    selected = rows[rows.year.eq(year)]
    if selected.empty:
        raise ValueError(f"No world aggregate for {year}")
    return selected.iloc[0]


def metric_for_group(metric_label: str) -> str:
    column = METRICS[metric_label][0]
    if column == "CoHD_PPP":
        return "CoHD_PPP_PoP"  # population-weighted cost from provided aggregate file
    return column


def change_table(aggregates: pd.DataFrame, group_type: str, end_year: int) -> pd.DataFrame:
    group = aggregates[aggregates.group_type.eq(group_type)]
    oldest = int(group.year.min())
    start = group[group.year.eq(oldest)][["country", "CoHD_headcount", "CoHD_unafford_n"]].rename(
        columns={"CoHD_headcount": "start_rate", "CoHD_unafford_n": "start_million"}
    )
    end = group[group.year.eq(end_year)][["country", "CoHD_headcount", "CoHD_unafford_n"]].rename(
        columns={"CoHD_headcount": "end_rate", "CoHD_unafford_n": "end_million"}
    )
    result = start.merge(end, on="country", how="inner")
    result["change_pp"] = result.end_rate - result.start_rate
    result["change_million"] = result.end_million - result.start_million
    return result


def nutrition_rows(countries: pd.DataFrame, year: int, outcome: str) -> pd.DataFrame:
    cols = ["country", "iso3", "year", "region", "population", "CoHD_headcount", outcome]
    df = countries[countries.year.eq(year)][cols].copy()
    df = df.dropna(subset=["CoHD_headcount", outcome]).copy()
    if outcome == "pou":
        # publisher's 2.5% boundary is a left-censored value; do not treat it as precise
        boundary = countries[countries.year.eq(year)][["iso3", "pou_below_2_5"]]
        df = df.merge(boundary, on="iso3", how="left")
        is_left_censored = df["pou_below_2_5"].astype(str).str.lower().eq("true")
        df = df.loc[~is_left_censored].copy()
    return df
