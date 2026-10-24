"""Independent check of the Analyst's results, in Python (pandas only).

Recomputes every table that analysis/analyst.R writes and compares the two. It also checks the
figures quoted in the report. Run from the repository root:

    python analysis/verify_analysis.py

Run analysis/analyst.R first so the R tables exist; without them only the report figures are checked.
Exit code 0 = everything matches.
"""
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "output"
c = pd.read_csv(ROOT / "data" / "fpn_countries.csv")
a = pd.read_csv(ROOT / "data" / "fpn_aggregates.csv")
problems: list[str] = []


def spearman(x, y) -> float:
    return float(np.corrcoef(pd.Series(x).rank(), pd.Series(y).rank())[0, 1])


def expect(label: str, actual: float, expected: float, tol: float = 0.0015) -> None:
    ok = abs(actual - expected) <= tol
    print(("PASS  " if ok else "FAIL  ") + f"{label}: {actual:.3f} (report {expected})")
    if not ok:
        problems.append(label)


# Figures quoted in the report
y25, y24 = c[c.year.eq(2025)], c[c.year.eq(2024)]
g = y25.dropna(subset=["gdp_pc_ppp", "CoHD_headcount"])
p = y25.dropna(subset=["CoHD_PPP", "CoHD_headcount"])
expect("GDP vs share, Spearman 2025 (142)", spearman(g.gdp_pc_ppp, g.CoHD_headcount), -0.824)
expect("Cost vs share, Spearman 2025 (147)", spearman(p.CoHD_PPP, p.CoHD_headcount), 0.172)
s = y24.dropna(subset=["CoHD_headcount", "stunting_pct"])
expect("Stunting vs share, Spearman 2024 (125)", spearman(s.CoHD_headcount, s.stunting_pct), 0.784)
expect("Stunting vs share, Pearson 2024 (125)", float(np.corrcoef(s.CoHD_headcount, s.stunting_pct)[0, 1]), 0.789)
sg = s.dropna(subset=["gdp_pc_ppp"])
lg = np.log(sg.gdp_pc_ppp)
res = lambda v: v - np.polyval(np.polyfit(lg, v, 1), lg)
expect("Partial correlation controlling log GDP (123)", float(np.corrcoef(res(sg.CoHD_headcount), res(sg.stunting_pct))[0, 1]), 0.411)
loo = [np.corrcoef(s.CoHD_headcount.drop(i), s.stunting_pct.drop(i))[0, 1] for i in s.index]
expect("Leave-one-out Pearson minimum", min(loo), 0.782)
expect("Leave-one-out Pearson maximum", max(loo), 0.803)
w = a[a.iso3.eq("WLD")].set_index("year")
expect("World share 2025 (%)", w.loc[2025, "CoHD_headcount"], 32.7, 0.05)
expect("World people 2025 (mn)", w.loc[2025, "CoHD_unafford_n"], 2692.1, 0.05)
top = y25.dropna(subset=["CoHD_headcount"]).sort_values("CoHD_headcount", ascending=False).iloc[0]
print(("PASS  " if top.country == "South Sudan" else "FAIL  ") + f"Highest share 2025: {top.country} {top.CoHD_headcount}%")
if top.country != "South Sudan":
    problems.append("highest share")

# R tables reproduced in Python
if OUT.exists() and any(OUT.glob("*.csv")):
    r_cov = pd.read_csv(OUT / "coverage.csv")
    py_cov = c.groupby("year")[["CoHD_PPP", "CoHD_headcount", "CoHD_unafford_n", "gdp_pc_ppp", "pou", "stunting_pct"]].count().reset_index()
    same = r_cov.astype(int).equals(py_cov.astype(int))
    print(("PASS  " if same else "FAIL  ") + "coverage.csv identical in R and Python")
    if not same:
        problems.append("coverage.csv")
    r_nc = pd.read_csv(OUT / "nutrition_correlations.csv")
    for _, row in r_nc.iterrows():
        d = c[c.year.eq(row.year)].dropna(subset=["CoHD_headcount", row.outcome])
        expect(f"R nutrition_correlations {row.year} {row.outcome} rho (n={len(d)})", spearman(d.CoHD_headcount, d[row.outcome]), row.spearman_rho, 0.0006)
    r_head = pd.read_csv(OUT / "headline_checks.csv")
    ok = bool(r_head.ok.all())
    print(("PASS  " if ok else "FAIL  ") + f"R headline_checks.csv: {int(r_head.ok.sum())}/{len(r_head)} reproduced")
    if not ok:
        problems.append("headline_checks.csv")
else:
    print("NOTE  analysis/output/ is empty – run analysis/analyst.R to compare the R tables")

print("\nAll checks passed." if not problems else f"\n{len(problems)} check(s) failed: {problems}")
sys.exit(1 if problems else 0)
