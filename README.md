# The Food Atlas: The price of eating well

**Team 3BK2NK · Macquarie University DataViz 2026 · Theme: Food · UN SDG 2 (targets 2.1 and 2.2)**

A healthy diet is getting more expensive – yet fewer people are priced out of it. This project follows that paradox from global averages to the countries left behind, and to children’s growth.

| | Link |
|---|---|
| **Data story** (start here) | https://claude.ai/artifact/XEx3UYEenFW9wL8zqdgZJw |
| **Interactive dashboard** (every country and year) | https://food-atlas-3bk2nk.streamlit.app/ |
| **Offline data story** (no internet needed) | [`docs/index.html`](docs/index.html) |
| **PDF version** and **story description** | [`docs/The_Food_Atlas_backup.pdf`](docs/The_Food_Atlas_backup.pdf) · [`docs/The_Food_Atlas_story_description.pdf`](docs/The_Food_Atlas_story_description.pdf) |

Both the story and the dashboard use the same eight chapters – *The paradox, Where, Left behind, Income, not price, The plate, Fed vs. well fed, Explore, Sources and method* – and the same cleaned datasets.

## Repository structure

| Folder | Content |
|---|---|
| `raw/` | Original downloads, with instructions to re-download each one (`raw/README.md`) |
| `scripts/` | `clean_fpn.py` → `merge_all.py` → `validate_data.py` (24 checks, including every headline number) |
| `data/` | Cleaned datasets and `data_dictionary.md` |
| `Healthy_Diet_Streamlit_V7/healthy_diet_streamlit/` | The Streamlit dashboard (entry point `app.py`) |
| `docs/` | The offline data story and PDFs |

## Reproduce the data

```
python scripts/clean_fpn.py
python scripts/merge_all.py
python scripts/validate_data.py --compare Healthy_Diet_Streamlit_V7/healthy_diet_streamlit/data
```

## Run the dashboard locally

```
cd Healthy_Diet_Streamlit_V7/healthy_diet_streamlit
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Data sources

- World Bank, *Food Prices for Nutrition* 5.0 (July 2026), CC BY 4.0
- World Bank, *World Development Indicators* – GDP per capita, PPP (current international $), NY.GDP.PCAP.PP.CD; *Country and Lending Groups*, FY2027
- FAO, *FAOSTAT – Suite of Food Security Indicators* (prevalence of undernourishment), CC BY 4.0
- UNICEF, WHO and World Bank, *Joint Child Malnutrition Estimates*, country modelled estimates (March 2026)

## How to read the numbers

- World, regional and income-group figures are the official population-weighted estimates, not averages of countries.
- Each chart uses the latest year its source covers: affordability and cost 2025, nutrition 2024, food-group costs 2021.
- Correlations (ρ) are Spearman rank correlations across countries, unweighted. They describe associations between countries, not causes, and not individual households.
- 147 of 180 countries have a 2025 affordability estimate; missing countries are never treated as zero.

An independent student project, not an official UN, FAO or World Bank product.
