"""Regenerate data/food_basket_costs_2021_derived.csv from data/fpn_countries.csv.

Run from healthy_diet_streamlit/: python scripts/build_food_basket.py
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data import read_datasets
from src.basket import export_basket

countries, _ = read_datasets()
target = ROOT/'data'/'food_basket_costs_2021_derived.csv'
result = export_basket(countries, target)
print(f'Created {target.name} with {len(result)} complete 2021 country baskets')
