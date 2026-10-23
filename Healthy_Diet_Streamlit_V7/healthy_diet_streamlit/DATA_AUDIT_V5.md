# Data audit and research decisions for V5

## Research decision

No additional external country-level dataset is included in this release. The existing `fpn_countries.csv` already contains six food-group PPP cost columns, `CoHD_CoCA`, GDP context, nutrition and healthy diet unaffordability. These were previously underused. Adding Gini, food CPI or poverty surveys without alignment of years, populations, sampling and price-basket concepts could add complexity without a better verified story.

The World Bank global inflation XLSX is a worthwhile future extension (official page: https://www.worldbank.org/en/brief/2025/05/04/inflation-database). The workbook could not be downloaded automatically in this environment; no inflation results have been invented. A real workbook may be uploaded via Wealth & prices.

## Data actually added

`data/food_basket_costs_2021_derived.csv` is a **derived table**, not an independently collected dataset. Its sole source is `data/fpn_countries.csv`. Rebuild it using `python scripts/build_food_basket.py`.

- Source country-year rows: 1,620, including 180 countries/territories in 2017 to 2025.
- Detailed food-group PPP components: **2021 only**. No observed group values for 2017-2020 or 2022-2025 in the provided CSV.
- 2021 countries with all six components, total CoHD PPP and positive six-group sum: **165**.
- Additive food-group sum vs published `CoHD_PPP`: difference at most **0.02 PPP $/day** due to rounding in source.
- Six groups: starchy staples, vegetables, fruits, animal-source foods, legumes/nuts/seeds, oils/fats.
- Computed `_share` fields: each group's 2021 PPP cost divided by the sum of the six food-group PPP costs, multiplied by 100.
- `CoHD_CoCA` = provided healthy diet cost divided by calorie adequacy cost (2021 only); among 174 available countries, **median 3.855** (displayed as 3.85 or 3.86 depending rounding convention).

## Newly demonstrated results

Of countries with valid 2021 group costs and income classifications:

| Group | Available countries | Median share of healthy-diet cost from animal-source foods |
|---|---:|---:|
| Low income | 19 | 38.1% |
| Lower middle income | 37 | 31.2% |
| Upper middle income | 44 | 26.5% |
| High income | 62 | 24.0% |

These are **unweighted medians of country-specific shares** in the set of observed countries. They do not describe actual food purchases, cannot be interpreted causally and should not be generalized beyond the available data without further checks. Three complete observations lack a known income classification and are excluded from the income-median plot.

## Missing-data cartography

Country polygons with a finite selected measure are drawn as choropleth observations. Other land is drawn by Plotly's geographic base as neutral grey (light `#D4D4D0`, dark `#89908D`) and the ocean is drawn separately (light `#EAF2F4`, dark `#0C2635`). A legend explicitly differentiates unavailable data from observations. Countries not represented in the supplied ISO3 table or not supported by Plotly's borders will show as base land as available.

## External methods and sources

- FAO Healthy Diet Basket: https://www.fao.org/interactive/2026/cost-healthy-diet/en/
- FAO CoAHD methods: https://www.fao.org/in-action/coahd/methods/en
- FAO cost-of-healthy-diet statistical methods brief: https://files-faostat.fao.org/production/CAHD/Methods_Brief_FAOSTAT_CoAHD_indicators.pdf
- World Bank Global Database of Inflation: https://www.worldbank.org/en/brief/2025/05/04/inflation-database

## Release limits

The current public Streamlit website is separate from these generated files. V5 source was verified by Python tests and a standalone styled HTML screenshot; the complete Streamlit UI has **not** been tested in a real Streamlit runtime in this environment. Deploy and check navigation, widgets, and responsive layout prior to final submission.
