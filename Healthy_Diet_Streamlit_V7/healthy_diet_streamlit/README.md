# The Food Atlas – interactive dashboard (Streamlit V7)

The exploration companion to the data story (https://claude.ai/artifact/XEx3UYEenFW9wL8zqdgZJw). Same eight chapters, same data, with a year slider, region and income filters, country comparisons and data downloads.

Live app: https://food-atlas-3bk2nk.streamlit.app/ (Streamlit Cloud entry point: `Healthy_Diet_Streamlit_V7/healthy_diet_streamlit/app.py`).

## Run locally
```
python -m pip install -r requirements.txt pytest
python -m pytest -q
python -m streamlit run app.py
```

## Code
- `app.py` – chapters and text
- `src/styles.py` – editorial design (V6); `src/story_styles.py` – takeaways, flags, Next button
- `src/charts.py`, `src/economics.py`, `src/basket.py` – charts; `src/statistics.py` – Spearman ρ without SciPy
- `src/data.py`, `src/narrative.py`, `src/flags.py` – data loading, insight sentences, country flags
- `data/` – a copy of the cleaned datasets in the repository’s `data/` folder (kept identical by `scripts/validate_data.py --compare`)

See `CHANGELOG_V7.md` for what changed from V6, and the repository’s `data/data_dictionary.md` for every column.
