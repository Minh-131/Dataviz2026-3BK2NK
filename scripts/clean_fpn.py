"""Step 1 – Clean the raw World Bank Food Prices for Nutrition (FPN 5.0) DataBank export.

Input : raw/fpn_databank.csv   (DataBank → Food Prices for Nutrition → all countries, series, years → CSV)
Output: data/fpn_countries.csv  (country × year, FPN indicators only – run merge_all.py next)
        data/fpn_aggregates.csv (World, 7 regions, 4 income groups)

Run from the repository root:  python scripts/clean_fpn.py
"""
from pathlib import Path
import re
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, DATA = ROOT / "raw", ROOT / "data"
SOURCE = RAW / "fpn_databank.csv"

# World Bank aggregate codes included in the FPN DataBank country list
AGGREGATES = {"EAS", "ECS", "HIC", "LCN", "LIC", "LMC", "MEA", "NAC", "SAS", "SSF", "UMC", "WLD"}
INCOME = {"HIC", "LIC", "LMC", "UMC"}


def main() -> None:
    if not SOURCE.exists():
        sys.exit(f"Missing {SOURCE.relative_to(ROOT)} – see raw/README.md")
    raw = pd.read_csv(SOURCE, encoding="cp1252", dtype=str)
    raw = raw[raw["Country Code"].notna() & raw["Time"].notna()].copy()  # drop DataBank footer rows

    ids = {"Country Name": "country", "Country Code": "iso3", "Time": "year"}
    series = [c for c in raw.columns if re.search(r"\[.+\]$", c) and c not in ids]
    code = {c: re.search(r"\[(.+)\]$", c).group(1) for c in series}

    df = raw[list(ids) + series].rename(columns={**ids, **code}).replace("..", pd.NA)
    df["year"] = df["year"].astype(float).astype(int)
    for c in code.values():
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.rename(columns={"NY.GDP.PCAP.PP.CD": "gdp_pc_ppp", "NY.GNP.PCAP.PP.CD": "gni_pc_ppp", "Pop": "population"})
    df = df.sort_values(["iso3", "year"])

    values = [c for c in df.columns if c not in ("country", "iso3", "year")]
    empty = [c for c in values if df[c].notna().sum() == 0]  # GDP/GNI arrive empty in the FPN export
    df = df.drop(columns=empty)

    agg = df[df.iso3.isin(AGGREGATES)].copy()
    agg.insert(2, "group_type", agg.iso3.map(lambda x: "world" if x == "WLD" else ("income" if x in INCOME else "region")))
    countries = df[~df.iso3.isin(AGGREGATES)].drop(columns=[c for c in df.columns if c.endswith("_PoP")])

    DATA.mkdir(exist_ok=True)
    countries.to_csv(DATA / "fpn_countries.csv", index=False)
    agg.to_csv(DATA / "fpn_aggregates.csv", index=False)
    print(f"countries: {countries.shape} ({countries.iso3.nunique()} countries) | aggregates: {agg.shape}")
    print(f"dropped empty columns: {empty}")


if __name__ == "__main__":
    main()
