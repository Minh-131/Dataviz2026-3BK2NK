# Analysis (Analyst)

Reproduces every table and statistic in the Analyst’s report, [`docs/Healthy_Diet_Analysis_final.html`](../docs/Healthy_Diet_Analysis_final.html), from the cleaned data in `data/`.

| File | What it does |
|---|---|
| `analyst.R` | Base R, no packages. Writes the tables below and stops with an error if any of the 17 headline numbers in the report is not reproduced. |
| `verify_analysis.py` | Independent re-calculation in Python (pandas) of the report’s statistics, and a comparison with the R tables. |
| `output/` | Tables written by `analyst.R` |

Run from the repository root:

```
Rscript analysis/analyst.R            # or, in RStudio: source("analysis/analyst.R")
python analysis/verify_analysis.py
```

## Output tables

| Table | Content |
|---|---|
| `coverage.csv` | Countries with data, per indicator and year |
| `world_trend.csv` | World cost, share and people, 2017–2025 (official population-weighted aggregate) |
| `aggregate_changes.csv` | Regions and income groups, 2017 vs 2025, change and share of the world total |
| `countries_2025.csv`, `country_changes.csv` | Country values for 2025 and change since 2017 |
| `top10_rate_2025.csv`, `top10_people_2025.csv` | Highest share and largest number of people who cannot afford a healthy diet |
| `income_correlations_2025.csv` | Spearman ρ for GDP, diet cost and affordability, with n |
| `nutrition_2024.csv`, `nutrition_correlations.csv` | Nutrition panel and correlations 2022–2024 |
| `sensitivity_checks.csv` | Robustness of the stunting association (leave-one-out, partial correlation on log GDP, within income groups, PoU without censored values) |
| `headline_checks.csv` | The 17 figures quoted in the report and the story description, expected vs reproduced |

All correlations are across countries, unweighted, on complete cases; they describe associations, not causes.

Rebuilt from the Analyst’s report in October 2026 (the original script files could not be uploaded from the Analyst’s account); every table reproduces the values published in the report.
