"""Step 3 – Quality checks on data/ before it is shared or copied into the dashboard.

Checks structure, value ranges and every headline number used in the dashboard and the submission text.
Optionally confirms that the dashboard's own copy of the data is identical:

    python scripts/validate_data.py
    python scripts/validate_data.py --compare Healthy_Diet_Streamlit_V7/healthy_diet_streamlit/data

Exit code 0 = all checks passed, 1 = at least one check failed.
"""
from pathlib import Path
import argparse
import hashlib
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FILES = ("fpn_countries.csv", "fpn_aggregates.csv")
results: list[tuple[bool, str]] = []


def check(ok: bool, message: str) -> None:
    results.append((bool(ok), message))


def close(a: float, b: float, tol: float = 0.05) -> bool:
    return abs(float(a) - float(b)) <= tol


def spearman(x: pd.Series, y: pd.Series) -> float:
    return float(np.corrcoef(x.rank(), y.rank())[0, 1])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", help="folder holding the dashboard's copy of the CSV files")
    args = parser.parse_args()

    c = pd.read_csv(DATA / "fpn_countries.csv")
    a = pd.read_csv(DATA / "fpn_aggregates.csv")

    # Structure
    check(c.shape == (1620, 52), f"fpn_countries.csv shape {c.shape} (expected 1620 × 52)")
    check(c.iso3.nunique() == 180 and sorted(c.year.unique()) == list(range(2017, 2026)), "180 countries × 2017–2025")
    check(not c.duplicated(["iso3", "year"]).any(), "no duplicate country-year rows")
    check(a.shape[0] == 108 and set(a.group_type) == {"world", "region", "income"}, "aggregates: 12 groups × 9 years")
    check(not c.iso3.isin(a.iso3).any(), "no aggregates mixed into the country file")

    # Ranges
    check(c.CoHD_headcount.dropna().between(0, 100).all(), "CoHD_headcount within 0–100 %")
    check(c.CoHD_PPP.dropna().gt(0).all(), "CoHD_PPP positive")
    check(c.pou.dropna().between(0, 100).all() and c.stunting_pct.dropna().between(0, 100).all(), "pou and stunting within 0–100 %")
    check(c.gdp_pc_ppp.dropna().gt(0).all(), "gdp_pc_ppp positive")
    check(c.loc[c.year.eq(2025), ["pou", "stunting_pct"]].isna().all().all(), "no nutrition values invented for 2025")
    groups = [f"CoHD_{g}_PPP" for g in ("f", "v", "ss", "asf", "lns", "of")]
    check(c.loc[c.year.ne(2021), groups].isna().all().all(), "food-group costs exist only for 2021")

    # Headline numbers (fact sheet)
    w = a[a.iso3.eq("WLD")].set_index("year")
    check(close(w.loc[2017, "CoHD_PPP_PoP"], 2.94, 0.005) and close(w.loc[2025, "CoHD_PPP_PoP"], 4.28, 0.005), "world cost 2.94 → 4.28 PPP $")
    check(close(w.loc[2017, "CoHD_headcount"], 41.0) and close(w.loc[2025, "CoHD_headcount"], 32.7), "world share 41.0% → 32.7%")
    check(close(w.loc[2025, "CoHD_unafford_n"], 2692.1, 0.1), "world 2,692.1 million people in 2025")
    s = a[a.iso3.eq("SSF")].set_index("year")
    check(close(s.loc[2025, "CoHD_unafford_n"] - s.loc[2017, "CoHD_unafford_n"], 194.3, 0.1), "Sub-Saharan Africa +194.3 million")
    check(close(s.loc[2025, "CoHD_unafford_n"] / w.loc[2025, "CoHD_unafford_n"] * 100, 35.4, 0.1), "Sub-Saharan Africa 35.4% of world total")
    y25 = c[c.year.eq(2025)].set_index("country")
    check(close(y25.loc["Nigeria", "CoHD_PPP"], 4.18, 0.005) and close(y25.loc["Cyprus", "CoHD_PPP"], 4.18, 0.005), "Nigeria and Cyprus both 4.18 PPP $")
    check(close(y25.loc["Nigeria", "CoHD_headcount"], 80.5) and close(y25.loc["Cyprus", "CoHD_headcount"], 1.5), "Nigeria 80.5% vs Cyprus 1.5%")
    check(int((y25.CoHD_headcount > 50).sum()) == 41 and int(y25.CoHD_headcount.notna().sum()) == 147, "41 of 147 countries above 50%")
    ner = c[c.iso3.eq("NER") & c.year.eq(2024)].iloc[0]
    check(close(ner.pou, 12.9) and close(ner.CoHD_headcount, 86.7) and close(ner.stunting_pct, 48.3), "Niger 2024: 12.9% / 86.7% / 48.3%")
    gdp = y25.dropna(subset=["gdp_pc_ppp", "CoHD_headcount", "CoHD_PPP"])
    check(len(gdp) == 142 and close(spearman(gdp.gdp_pc_ppp, gdp.CoHD_headcount), -0.824, 0.001), "GDP vs share ρ = −0.824 (142)")
    st = c[c.year.eq(2024)].dropna(subset=["CoHD_headcount", "stunting_pct"])
    check(len(st) == 125 and close(spearman(st.CoHD_headcount, st.stunting_pct), 0.784, 0.001), "share vs stunting ρ = 0.784 (125)")

    # Dashboard copy in sync
    if args.compare:
        target = Path(args.compare)
        for name in FILES:
            ours = hashlib.md5((DATA / name).read_bytes()).hexdigest()
            theirs = hashlib.md5((target / name).read_bytes()).hexdigest() if (target / name).exists() else None
            check(ours == theirs, f"{target / name} identical to data/{name}")

    for ok, message in results:
        print(("PASS  " if ok else "FAIL  ") + message)
    failed = sum(not ok for ok, _ in results)
    print(f"\n{len(results) - failed}/{len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
