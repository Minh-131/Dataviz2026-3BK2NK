# Changes in V3: Guided insights & user instructions

- Added a visible **How to read / Key insight / Note** explanation card under every Plotly chart (including conditional food-inflation figure).
- Insight summaries now recalculate when the visitor switches year, indicator, grouping, selected countries or nutrition measure.
- Added a concise **sidebar Quick guide** and a new **🧭 How to Use** tab, written in English for competition judges.
- Added an extensive Vietnamese instruction document `USER_GUIDE_VI.md`.
- Added `src/narrative.py` with testable functions, and `tests/test_narrative.py`.
- Fixed the country-map drilldown timelines so they stop at the globally selected year, consistent with the How to Use explanation.
- Clearer explanations of PPP vs food CPI, million vs %, missing data, Spearman correlation, nutrition data year and country-vs-global aggregation.
- All existing analytical CSVs and optional inflation workflow retained from V2; no invented data.

## Pre-release checks

- Verify complete extraction metadata and the GDP indicator/vintage against World Bank.
- Run the full app in an environment with Streamlit installed, test plot rendering, controls and mobile layout.
- Run `python -m pytest -q`.
