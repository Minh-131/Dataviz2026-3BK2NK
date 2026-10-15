# FPN 5.0 – Data dictionary (DataViz 2026)

Sources (cite on dashboard):
- World Bank, Food Prices for Nutrition 5.0 (21/07/2026), CC BY 4.0
- World Bank, World Development Indicators (08/10/2026); Country and Lending Groups (CLASS, 08/10/2026)
- FAO, FAOSTAT Suite of Food Security Indicators (downloaded 15/10/2026), CC BY 4.0
- UNICEF/WHO/World Bank, Joint Child Malnutrition Estimates, country estimates (March 2026)
Costs are per person per day. "PPP" = international (PPP) dollars. Missing values are blank.

## Files
| File | Rows | Content |
|---|---|---|
| fpn_countries.csv | 1,620 (180 countries × 2017–2025) | Country-level data |
| fpn_aggregates.csv | 108 (12 groups × 2017–2025) | World, 7 regions, 4 income groups (`group_type`: world/region/income). Use these for regional charts – do NOT average countries yourself. |
| fpn_coverage.csv | – | Number of countries with data, per indicator per year |
| clean_fpn.py | – | Step 1: cleans the raw FPN download |
| merge_all.py | – | Step 2: adds region, income group, GDP, PoU, stunting (run after clean_fpn.py) |

## Key columns
| Column | Meaning | Unit | Years |
|---|---|---|---|
| country, iso3, year | Country name, ISO3 code (join key), year | – | – |
| CoHD_PPP | Cost of a healthy diet | PPP $/person/day | 2017–2025 |
| CoHD_LCU | Cost of a healthy diet | local currency | 2017–2025 |
| CoHD_headcount | % population who cannot afford a healthy diet | % (0–100) | 2017–2025 |
| CoHD_unafford_n | People who cannot afford a healthy diet | millions | 2017–2025 |
| CoHD_pov | Healthy-diet cost ÷ food poverty line | ratio | 2017–2025 |
| population | Population | people | 2017–2025 |
| region | World Bank region (FY2027 classification) | – | – |
| income_group | World Bank income group (FY2027) | – | – |
| gdp_pc_ppp | GDP per capita, PPP (current international $) – WDI NY.GDP.PCAP.PP.CD | $ | 2017–2025 |
| pou | Prevalence of undernourishment – FAOSTAT, 3-year average assigned to the middle year (e.g. 2021–2023 → 2022) | % | 2017–2024 |
| pou_below_2_5 | TRUE where FAO reports "<2.5"; `pou` is then set to 2.5 (an upper bound, not an exact value) | – | – |
| stunting_pct | Stunting prevalence, children under 5, both sexes – JME modelled estimates (March 2026 file) | % | 2017–2024 |
| CoCA_PPP / CoNA_PPP | Cost of energy-sufficient / nutrient-adequate diet | PPP $/day | 2021 only |
| CoCA_*, CoNA_* (headcount, unafford_n, pov, fexp) | Same measures for energy-sufficient / nutrient-adequate diets | as above | 2021 only |
| CoHD_fexp | Healthy-diet cost ÷ average food expenditure | ratio | 2021 only |
| CoHD_CoCA | Healthy-diet cost ÷ cost of calories from starchy staples | ratio | 2021 only |
| CoHD_{f,v,ss,asf,lns,of}_PPP | Cost of each food group in a healthy diet | PPP $/day | 2021 only |
| CoHD_{…}_prop | Cost share of each food group | fraction (0–1) | 2021 only |
| CoHD_{…}_ss | Food-group cost relative to starchy staples | ratio | 2021 only |
| *_PoP (aggregates file only) | Population-weighted cost for the group | PPP $/day | CoHD_PPP_PoP 2017–2025, rest 2021 |

Food-group codes: f = fruits, v = vegetables, ss = starchy staples, asf = animal-source foods, lns = legumes/nuts/seeds, of = oils & fats.

## Known gaps
- Region names follow the new FY2027 classification ("Middle East, North Africa, Afghanistan & Pakistan"). fpn_aggregates.csv uses the older split ("Middle East & North Africa" + "South Asia"), so country-level region filters will not exactly match FPN regional totals for those two regions.
- Anguilla, Bonaire, Montserrat have no region/income group.
- No PoU or stunting for 2025. PoU missing for ~27 small economies; stunting mostly missing for high-income countries (JME covers 162 countries).
- Income group is the current (FY2027) classification, applied to all years.
- Bonaire (BON) has no population; ~20 small economies have no headcount data.
