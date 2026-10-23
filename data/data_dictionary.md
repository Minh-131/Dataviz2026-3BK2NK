# Data dictionary – The Food Atlas (DataViz 2026, Team 3BK2NK)

**Sources (cite on the dashboard):**
- World Bank, *Food Prices for Nutrition* 5.0 (21 July 2026), CC BY 4.0
- World Bank, *World Development Indicators*, NY.GDP.PCAP.PP.CD (8 October 2026); *Country and Lending Groups*, FY2027 (8 October 2026)
- FAO, *FAOSTAT – Suite of Food Security Indicators* (downloaded 15 October 2026), CC BY 4.0
- UNICEF/WHO/World Bank, *Joint Child Malnutrition Estimates*, country modelled estimates (March 2026)

Costs are per person per day in PPP $ (international dollars, 2021 PPP). Missing values are blank – never zero.

## Files

| File | Rows | Content |
|---|---|---|
| `data/fpn_countries.csv` | 1,620 (180 countries × 2017–2025) | Country-level data, 52 columns |
| `data/fpn_aggregates.csv` | 108 (12 groups × 2017–2025) | World, 7 regions, 4 income groups (`group_type`: world / region / income). Use these for world and regional figures – do not average countries. |
| `raw/` | – | Original downloads; `raw/README.md` explains how to re-download each one |
| `scripts/clean_fpn.py` | – | Step 1: cleans the FPN download, splits countries and aggregates |
| `scripts/merge_all.py` | – | Step 2: adds region, income group, GDP, undernourishment, stunting (safe to re-run) |
| `Healthy_Diet_Streamlit_V7/healthy_diet_streamlit/data/` | – | The dashboard’s own copy of the two CSV files (must stay identical) |
| `scripts/validate_data.py` | – | Step 3: 22 checks on structure, ranges and every headline number; `--compare <folder>` confirms the dashboard copy is identical |

## Key columns

| Column | Meaning | Unit | Years |
|---|---|---|---|
| `country`, `iso3`, `year` | Country name, ISO3 code (join key), year | – | – |
| `region`, `income_group` | World Bank region and income group (FY2027 classification, applied to all years) | – | – |
| `population` | Population | people | 2017–2025 |
| `gdp_pc_ppp` | GDP per capita, PPP (current international $) – WDI NY.GDP.PCAP.PP.CD; a national average, not household income | $ | 2017–2025 |
| `pou` | Prevalence of undernourishment – FAOSTAT 3-year average assigned to the middle year (2021–2023 → 2022) | % | 2017–2024 |
| `pou_below_2_5` | TRUE where FAO reports "<2.5"; `pou` is then 2.5, an upper bound | – | – |
| `stunting_pct` | Stunting, children under 5, both sexes – JME modelled estimates | % | 2017–2024 |
| `CoHD_PPP` | Cost of a healthy diet | PPP $/day | 2017–2025 |
| `CoHD_LCU` | Cost of a healthy diet | local currency | 2017–2025 |
| `CoHD_headcount` | Share of population who cannot afford a healthy diet | % (0–100) | 2017–2025 |
| `CoHD_unafford_n` | People who cannot afford a healthy diet | millions | 2017–2025 |
| `CoHD_pov` | Healthy-diet cost ÷ food poverty line | ratio | 2017–2025 |
| `CoCA_PPP` / `CoNA_PPP` | Cost of an energy-sufficient / nutrient-adequate diet | PPP $/day | 2021 only |
| `CoCA_*`, `CoNA_*` | Headcount, people, poverty and expenditure measures for those two diets | as above | 2021 only |
| `CoHD_fexp` | Healthy-diet cost ÷ average food expenditure | ratio | 2021 only |
| `CoHD_CoCA` | Healthy-diet cost ÷ energy-sufficient diet cost | ratio | 2021 only |
| `CoHD_{f,v,ss,asf,lns,of}_PPP` | Cost of each food group in a healthy diet | PPP $/day | 2021 only |
| `CoHD_{…}_prop` | Cost share of each food group | fraction (0–1) | 2021 only |
| `CoHD_{…}_ss` | Food-group cost relative to starchy staples | ratio | 2021 only |
| `*_PoP` (aggregates only) | Population-weighted cost for the group | PPP $/day | `CoHD_PPP_PoP` 2017–2025, others 2021 |

Food groups: f = fruits, v = vegetables, ss = starchy staples, asf = animal-source foods, lns = legumes, nuts and seeds, of = oils and fats.

## Known limitations

- Regions follow the FY2027 classification ("Middle East, North Africa, Afghanistan & Pakistan"); `fpn_aggregates.csv` uses the older split ("Middle East & North Africa" + "South Asia"), so the two levels differ slightly for those regions.
- Anguilla, Bonaire and Montserrat have no region or income group; Bonaire has no population.
- No undernourishment or stunting values for 2025. Undernourishment is missing for about 27 small economies; stunting is mostly missing for high-income countries (JME covers 162 countries).
- About 33 small economies have no affordability estimate in 2025.

## Rules for the team

- Do not edit files in `data/` by hand – change a script and re-run the pipeline.
- Do not open a CSV in Excel and save it (it changes encodings and number formats).
- After any data change, copy `data/fpn_countries.csv` and `data/fpn_aggregates.csv` into `Healthy_Diet_Streamlit_V7/healthy_diet_streamlit/data/` and run `python scripts/validate_data.py --compare Healthy_Diet_Streamlit_V7/healthy_diet_streamlit/data`.
