# The Food Atlas: Healthy Food, Unequal Access

An independent interactive UN SDG 2 data story, built using Python, Streamlit and Plotly. Designed for the Food theme of the UN Datathon-style visualization challenge.

## What makes V5 different?

A print-inspired editorial design instead of a typical software metrics dashboard: asymmetric cover, large serif headline, ruled data index, numbered chapters, warm paper palette, optional dark reading mode, and consistent visual explanations.

The World atlas uses a neutral grey **no-data land** layer and a separate **blue-grey ocean** layer, plus a legend. Unavailable observations are never converted to zero.

## Chapters

1. The paradox: global cost, unaffordability and population affected from 2017 to 2025.
2. World atlas: missing-data-aware choropleth and individual country timelines.
3. The divide: regional and income group differences and trends.
4. Wealth & prices: GDP, diet cost, and optional genuine World Bank food inflation Excel.
5. Inside the basket: six-food-group cost composition and nutrition premium, **2021 only**.
6. Nutrition: correlations with stunting and undernourishment through 2024.
7. Country lab: rankings, country time series, and CSV export.
8. Methods: transparent measures, data sources and limitations.
9. Field guide: quick instructions for first-time visitors.

## Installation

From the `healthy_diet_streamlit` folder:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Use the sidebar to change chapters, global reporting year and Light/Dark reading mode. Detailed food-basket observations are fixed to 2021, so the global KPI context also switches to 2021 on that chapter.

## Tests

```bash
python -m pip install pytest
python -m pytest -q
```

## Data

- `data/fpn_countries.csv` and `data/fpn_aggregates.csv`: user-supplied cleaned snapshots, not live APIs.
- `data/food_basket_costs_2021_derived.csv`: transparent derived data from 165 complete country baskets for 2021; regenerate with `python scripts/build_food_basket.py`.
- `data/Inflation-data.xlsx`: optional real World Bank workbook, not included.

**Use caution:** percentage points differ from percent growth; international PPP cost is not food CPI inflation; and national-level correlations are not causal. The 2025 nutrition fields are unavailable in the snapshot. See `DATA_AUDIT_V5.md` for the complete source audit.

## Deploy to Streamlit Cloud

Place this folder under your GitHub repository, set entrypoint to `healthy_diet_streamlit/app.py`, and ensure the dependencies under `healthy_diet_streamlit/requirements.txt` are installed. See `UPDATE_V5_VI.md` for commands and migration precautions.

## Data/method references

- [FAO Cost and Affordability of a Healthy Diet](https://www.fao.org/in-action/coahd/methods/en)
- [FAO The Cost of a Healthy Diet: interactive story](https://www.fao.org/interactive/2026/cost-healthy-diet/en/)
- [World Bank Global Database of Inflation](https://www.worldbank.org/en/brief/2025/05/04/inflation-database)
- [UN Sustainable Development Goal 2](https://sdgs.un.org/goals/goal2)

Educational independent project. Not an official UN or FAO dashboard.


## Design preview images

The `design_previews/` images are **static editorial layout previews** rendered from the V5 HTML/CSS and representative data. They are not screenshots of a running Streamlit instance and do not replace live browser testing.
