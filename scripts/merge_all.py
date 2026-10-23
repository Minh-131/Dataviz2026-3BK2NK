"""Step 2 – Add region, income group, GDP per capita, undernourishment and stunting to data/fpn_countries.csv.

Inputs (see raw/README.md for how to download each file):
  raw/wdi_gdp_pc_ppp.csv   World Bank WDI, NY.GDP.PCAP.PP.CD (current international $)
  raw/CLASS.xlsx           World Bank Country and Lending Groups (sheet "List of economies")
  raw/faostat_pou.csv      FAOSTAT Suite of Food Security Indicators, prevalence of undernourishment, ISO3 codes
  raw/jme_country.xlsx     UNICEF/WHO/World Bank JME country modelled estimates (sheet "Stunting Prevalence")

Safe to run more than once: merged columns are dropped and rebuilt each time.
Run from the repository root, after clean_fpn.py:  python scripts/merge_all.py
"""
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, DATA = ROOT / "raw", ROOT / "data"
MERGED = ["region", "income_group", "gdp_pc_ppp", "pou", "pou_below_2_5", "stunting_pct"]
INPUTS = {name: RAW / name for name in ("wdi_gdp_pc_ppp.csv", "CLASS.xlsx", "faostat_pou.csv", "jme_country.xlsx")}


def gdp() -> pd.DataFrame:
    w = pd.read_csv(INPUTS["wdi_gdp_pc_ppp.csv"], encoding="cp1252", dtype=str)
    w = w[w["Series Code"].eq("NY.GDP.PCAP.PP.CD")]
    years = [c for c in w.columns if "[YR" in c]
    g = w.melt(id_vars=["Country Code"], value_vars=years, var_name="year", value_name="gdp_pc_ppp")
    g["year"] = g.year.str[:4].astype(int)
    g["gdp_pc_ppp"] = pd.to_numeric(g.gdp_pc_ppp.replace("..", pd.NA), errors="coerce")
    return g.rename(columns={"Country Code": "iso3"}).dropna(subset=["gdp_pc_ppp"])


def classification() -> pd.DataFrame:
    c = pd.read_excel(INPUTS["CLASS.xlsx"], sheet_name="List of economies")
    c = c[c.Region.notna()][["Code", "Region", "Income group"]]
    return c.rename(columns={"Code": "iso3", "Region": "region", "Income group": "income_group"})


def undernourishment() -> pd.DataFrame:
    f = pd.read_csv(INPUTS["faostat_pou.csv"])
    f["year"] = f.Year.str[:4].astype(int) + 1          # 3-year average assigned to its middle year
    f["pou_below_2_5"] = f.Value.astype(str).str.startswith("<")
    f["pou"] = pd.to_numeric(f.Value.astype(str).str.replace("<", ""), errors="coerce")  # "<2.5" -> 2.5 (upper bound)
    return f.rename(columns={"Area Code (ISO3)": "iso3"})[["iso3", "year", "pou", "pou_below_2_5"]].dropna(subset=["pou"])


def stunting() -> pd.DataFrame:
    j = pd.read_excel(INPUTS["jme_country.xlsx"], sheet_name="Stunting Prevalence")
    j = j.rename(columns={"ISO Code": "iso3", "Year": "year", "Both Sexes - Point Estimates": "stunting_pct"})
    j = j[["iso3", "year", "stunting_pct"]].assign(stunting_pct=lambda d: pd.to_numeric(d.stunting_pct, errors="coerce"))
    return j.dropna().astype({"year": int})


def main() -> None:
    missing = [str(p.relative_to(ROOT)) for p in INPUTS.values() if not p.exists()]
    if missing:
        sys.exit(f"Missing input files: {missing} – see raw/README.md")
    base = pd.read_csv(DATA / "fpn_countries.csv").drop(columns=MERGED, errors="ignore")
    m = (base.merge(classification(), on="iso3", how="left")
             .merge(gdp(), on=["iso3", "year"], how="left")
             .merge(undernourishment(), on=["iso3", "year"], how="left")
             .merge(stunting(), on=["iso3", "year"], how="left"))
    front = ["country", "iso3", "year", "region", "income_group", "population"] + MERGED[2:]
    m = m[front + [c for c in m.columns if c not in front]]
    m.to_csv(DATA / "fpn_countries.csv", index=False)
    print(f"fpn_countries.csv: {m.shape}")
    print("countries without region:", sorted(m.loc[m.region.isna(), "country"].unique()))
    print(m.groupby("year")[["gdp_pc_ppp", "pou", "stunting_pct", "CoHD_headcount"]].count().to_string())


if __name__ == "__main__":
    main()
