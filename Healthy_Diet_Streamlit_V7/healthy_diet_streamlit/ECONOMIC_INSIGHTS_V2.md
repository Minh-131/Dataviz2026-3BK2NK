# V2 | Economic insights and data-source integration (19 October 2026)

## Main finding: *similar diet costs do not imply similar affordability*

| 2025 evidence | Value | Calculation |
|---|---:|---|
| Countries with valid `gdp_pc_ppp`, `CoHD_PPP`, and `CoHD_headcount` | 142 | Drop missing, GDP > 0 |
| Spearman ρ GDP per capita vs unaffordability | **−0.824** | 142 complete country pairs; unweighted |
| Spearman ρ GDP per capita vs minimum healthy diet cost | **−0.081** | Same 142 pairs; unweighted |
| Nigeria healthy-diet cost | **4.18 PPP $/day** | Country CSV `CoHD_PPP` |
| Cyprus healthy-diet cost | **4.18 PPP $/day** | Country CSV `CoHD_PPP` |
| Nigeria unable to afford | **80.5%** | Country CSV `CoHD_headcount` |
| Cyprus unable to afford | **1.5%** | Country CSV `CoHD_headcount` |
| Low-income group weighted cost | **4.05 PPP $/day** | Aggregate CSV `CoHD_PPP_PoP` |
| High-income group weighted cost | **4.20 PPP $/day** | Aggregate CSV `CoHD_PPP_PoP` |
| Low-income group unaffordability | **76.1%** | Aggregate CSV `CoHD_headcount` |
| High-income group unaffordability | **8.1%** | Aggregate CSV `CoHD_headcount` |

**What to say in the dashboard:** Across countries with usable 2025 estimates, GDP per capita is strongly negatively associated with healthy-diet unaffordability. It is barely associated with the minimum daily diet cost. Illustrative contrasts like Nigeria/Cyprus show why measuring prices alone is insufficient.

**What *not* to say:** These correlations do not prove rising GDP causes greater affordability, that *individual* household income explains the entire difference, or that the macro GDP proxy directly measures disposable income. Healthy-diet unaffordability itself depends on income distribution and other basic needs; correlations are descriptive and should not be presented as independent mechanisms. `gdp_pc_ppp` is already in the supplied country CSV; verify whether it exactly matches the requested World Bank indicator `NY.GDP.PCAP.PP.KD` and its release vintage before citation.

## Inflation data still required

The user provided a URL to the World Bank inflation database **but no original Excel data file**. We could not retrieve the Excel workbook into the work environment. For integrity, the new dashboard shows no made-up inflation numbers.

When the official Excel is placed into `data/Inflation-data.xlsx` or uploaded inside the app, the **GDP & Inflation** tab will parse the World Bank `fcpi_a` annual **Food CPI inflation (%)** and optional `hcpi_a` annual **headline CPI inflation (%)** sheets, match by ISO3/year, and show the descriptive country-level relationship between food inflation and the annual change in the unaffordability rate (percentage points). Only joined nonmissing observations count. At least three matches are required to plot.

**Units and methodology:** Food CPI inflation is price growth for a national consumer food basket. `CoHD_PPP` is the minimum daily cost of a diet meeting dietary guidance, expressed in PPP international dollars. They differ in basket, price basis and conversion. Do not label PPP cost growth as food CPI inflation. Never infer causation from a country-year correlation. The inflation page states the actual sample size when the workbook is loaded.

## Recommended 7-page story

1. **Global Story:** Global trend: costly diet despite improved access.
2. **World Map:** Unequal burden worldwide.
3. **Regional & Income Divide:** Same problem, different exposure.
4. **GDP & Inflation (NEW):** Distinguish diet prices from macroeconomic resources, then add actual food CPI when available.
5. **Nutrition Link:** Stunting/PoU in 2024; avoid causal claims.
6. **Country Explorer:** Compare countries, rankings, export.
7. **Data & Methods:** Provenance and meaningful limitations.

## Source links (verify snapshot/version)

- World Bank GDP PPP indicator: https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD
- World Bank Global Database of Inflation: https://www.worldbank.org/en/brief/2025/05/04/inflation-database
- FAO FAOSTAT CoAHD: https://www.fao.org/faostat/en/#data/CAHD
- FAO SOFI 2026 publication: https://www.fao.org/newsroom/detail/un-report--global-hunger-levels-ease-for-third-consecutive-year-as-regional-disparities-persist/
- World Bank food affordability overview 2026: https://blogs.worldbank.org/en/opendata/can-income-keep-up-with-the-rising-cost-of-a-healthy-diet--new-c

## Local commands

```bash
python -m pip install -r requirements.txt
python -m pip install pytest
python -m pytest -q
python -m streamlit run app.py
```

**QA reminder:** The included Excel-fixture tests use **synthetic numbers only** to test the parser and never appear as real World Bank food inflation evidence. Before judging, place the actual World Bank Excel, run tests and visually verify the extra tab. Never commit unverified derived figures to a final presentation.
