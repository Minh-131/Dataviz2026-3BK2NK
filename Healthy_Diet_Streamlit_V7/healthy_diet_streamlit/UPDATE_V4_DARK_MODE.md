# V4: Dark mode and cleaner typography

## Changes

- Added **🌙 Dark mode** toggle to the sidebar.
- Designed complementary palettes for light and dark backgrounds, KPI cards, callouts, captions, controls and explanations.
- Coordinated Plotly theme across trend lines, scatterplots, bar charts, the world map, axes, hover tooltips, legends and annotations.
- Disabled Streamlit's automatic Plotly color overrides (`theme=None`) so the selected chart appearance is respected.
- Removed decorative typographic en dashes and em dashes from headings, descriptions and help content. Kept normal code syntax and numeric minus signs.
- Retained V3.1's SciPy-free Spearman correlation implementation, the existing data and all eight dashboard tabs.
- Added regression tests for light/dark CSS, Plotly, map colors and scatter annotations.

## Update the existing deployed GitHub repository

The traceback of your earlier deployment used this entrypoint:

`healthy_diet_streamlit_project/healthy_diet_streamlit/app.py`

If the repository still has that layout, replace **these five files** at the same paths on the current deployed branch:

```text
healthy_diet_streamlit/
├── app.py
└── src/
    ├── styles.py
    ├── charts.py
    └── economics.py
```

The patch includes `src/statistics.py` even if the deployed version currently works by installing SciPy. This preserves the V3.1 fix and prevents the earlier `ModuleNotFoundError` from recurring.

For a repository whose `.git` directory is at the outer project root:

```bash
git add healthy_diet_streamlit/app.py healthy_diet_streamlit/src/styles.py healthy_diet_streamlit/src/charts.py healthy_diet_streamlit/src/economics.py healthy_diet_streamlit/src/statistics.py
git commit -m "Add dark mode and clean dashboard typography"
git push origin main
```

If the Streamlit Cloud deployment uses another branch, push to that branch instead of `main`. The Cloud entrypoint remains `healthy_diet_streamlit/app.py` in this layout. No change to CSV files or dependencies is needed.

## Verify after deployment

1. Open the app from a private window. Expand the sidebar if necessary.
2. Turn on **🌙 Dark mode** and check KPI cards, all eight tabs, map, scatterplots, legends, popovers and data tables.
3. Turn it off and confirm that the light theme and chart labels are readable.
4. Change year, filters and selected countries. Confirm all insights and numbers remain correct.
5. Inspect the app logs for import failures. The Spearman calculation still uses `src/statistics.py` and does not require SciPy.

## Testing status

- Python syntax and automated tests can be verified with `python -m pytest -q`.
- Streamlit runtime was not installed in the preparation environment. A final visual check must be performed on your deployed website.
