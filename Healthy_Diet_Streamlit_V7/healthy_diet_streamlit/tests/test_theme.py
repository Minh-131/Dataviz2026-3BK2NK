"""Editorial UI and geographic missing-data color regression tests."""
from pathlib import Path
import pandas as pd
from src.styles import get_css, LIGHT, DARK
from src.charts import set_chart_theme, history_line, country_map, TEAL
from src.economics import cost_vs_affordability_chart, cross_section
from src.data import read_datasets


def test_theme_css_contrasts():
    light, dark = get_css(False), get_css(True)
    assert LIGHT['bg'] in light and DARK['bg'] not in light
    assert DARK['bg'] in dark and DARK['ink'] in dark
    assert '.cover' in dark and '.fact-strip' in light and '.chapter-mark' in dark
    assert '[data-baseweb="popover"]' in dark
    assert dark.count('{') == dark.count('}')


def test_plotly_figures_follow_selected_theme():
    data = pd.DataFrame({'year': [2023, 2024], 'cost': [3.8, 4.1]})
    try:
        set_chart_theme(False)
        light = history_line(data,'cost','PPP dollars',color=TEAL)
        assert light.layout.font.color == '#26322D'
        assert light.data[0].line.color == '#537D64'
        set_chart_theme(True)
        dark = history_line(data,'cost','PPP dollars',color=TEAL)
        assert dark.layout.font.color == '#F5F1E6'
        assert dark.data[0].line.color == '#98C2A4'
        assert dark.layout.hoverlabel.font.color == '#F5F1E6'
    finally:
        set_chart_theme(False)


def test_missing_land_is_not_ocean():
    root = Path(__file__).resolve().parents[1]
    countries, _ = read_datasets(root/'data')
    subset = countries.loc[countries.year.eq(2025)].copy()
    for dark in (False, True):
        try:
            set_chart_theme(dark)
            world = country_map(subset, 'CoHD_headcount', 'Unaffordability rate')
            assert world.layout.geo.landcolor == ('#89908D' if dark else '#D4D4D0')
            assert world.layout.geo.oceancolor == ('#0C2635' if dark else '#EAF2F4')
            assert world.layout.geo.showcountries is True
            assert world.layout.geo.landcolor != world.layout.geo.oceancolor
            assert len(world.data[0].locations) == 147
            assert 'ABW' not in set(world.data[0].locations)
            chart = cost_vs_affordability_chart(cross_section(countries,2025))
            assert chart.layout.font.color == ('#F5F1E6' if dark else '#26322D')
        finally:
            set_chart_theme(False)
