"""Economic insight and optional real-source Excel ingestion tests."""
from io import BytesIO
import pandas as pd
import pytest

from src.data import read_datasets
from src.economics import (
    cross_section, gdp_associations, read_inflation_excel, merged_inflation_change,
    gdp_affordability_chart, cost_vs_affordability_chart, inflation_change_chart,
)


def test_2025_gdp_and_affordability_insights():
    countries, aggregates = read_datasets()
    pair = cross_section(countries, 2025)
    stat = gdp_associations(countries, 2025)
    assert len(pair) == stat['n'] == 142
    assert stat['rho_gdp_vs_unafford'] == pytest.approx(-0.824, abs=0.001)
    assert stat['rho_gdp_vs_diet_cost'] == pytest.approx(-0.081, abs=0.001)
    n = pair.loc[pair.country.eq('Nigeria')].iloc[0]
    cy = pair.loc[pair.country.eq('Cyprus')].iloc[0]
    assert n.CoHD_PPP == cy.CoHD_PPP == pytest.approx(4.18)
    assert n.CoHD_headcount - cy.CoHD_headcount == pytest.approx(79.0)
    group = aggregates.query('group_type=="income" and year==2025').set_index('country')
    assert group.loc['Low-income', 'CoHD_PPP_PoP'] == pytest.approx(4.05)
    assert group.loc['High-income', 'CoHD_PPP_PoP'] == pytest.approx(4.20)
    assert group.loc['Low-income','CoHD_headcount'] == pytest.approx(76.1)
    assert group.loc['High-income','CoHD_headcount'] == pytest.approx(8.1)


def fake_worldbank_workbook():
    # Synthetic unit-test fixture, NOT actual World Bank inflation observations.
    data = pd.DataFrame({
        'Country':['Nigeria','Cyprus','World aggregate'],
        'Country Code':['NGA','CYP','WLD'],
        '2023':[11.0,3.0,4.0], '2024':[12.0,4.0,5.0], '2025':[13.0,5.0,None],
    })
    headline = data.copy()
    headline[['2023','2024','2025']] += 1.0
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as x:
        data.to_excel(x, sheet_name='fcpi_a', index=False)
        headline.to_excel(x, sheet_name='hcpi_a', index=False)
    buf.seek(0)
    return buf


def test_world_bank_excel_read_and_year_alignment():
    inf = read_inflation_excel(fake_worldbank_workbook())
    assert inf.duplicated(['iso3','year']).sum() == 0
    assert inf.query('iso3=="NGA" and year==2025').iloc[0].food_inflation_pct == pytest.approx(13)
    assert inf.query('iso3=="CYP" and year==2024').iloc[0].headline_inflation_pct == pytest.approx(5)
    countries,_ = read_datasets()
    paired = merged_inflation_change(countries, inf, 2025)
    assert set(paired.iso3) == {'NGA','CYP'}
    n = paired.set_index('iso3').loc['NGA']
    raw = countries.set_index(['iso3','year'])
    expected = raw.loc[('NGA',2025),'CoHD_headcount'] - raw.loc[('NGA',2024),'CoHD_headcount']
    assert n.affordability_change_pp == pytest.approx(expected)


def test_chart_builders():
    countries,_ = read_datasets()
    d=cross_section(countries,2025)
    for f in (gdp_affordability_chart,cost_vs_affordability_chart):
        fig=f(d)
        assert len(fig.data)>0
        assert len(fig.to_json())>4000
    inf = read_inflation_excel(fake_worldbank_workbook())
    fig=inflation_change_chart(merged_inflation_change(countries,inf,2025))
    assert len(fig.data)>0
