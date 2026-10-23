import pytest

from src.data import change_table, current_world, nutrition_rows, read_datasets
from src.statistics import spearman_corr


def test_file_shape_and_unique_keys():
    country, aggregate = read_datasets()
    assert len(country) == 1620
    assert len(aggregate) == 108
    assert not country.duplicated(["iso3", "year"]).any()
    assert not aggregate.duplicated(["group_type", "country", "year"]).any()


def test_global_headline():
    _, aggregate = read_datasets()
    row2017 = current_world(aggregate, 2017)
    row2025 = current_world(aggregate, 2025)
    assert row2017.CoHD_PPP_PoP == pytest.approx(2.94, abs=1e-5)
    assert row2025.CoHD_PPP_PoP == pytest.approx(4.28, abs=1e-5)
    assert row2017.CoHD_headcount == pytest.approx(41.0, abs=1e-4)
    assert row2025.CoHD_headcount == pytest.approx(32.7, abs=1e-4)
    assert row2025.CoHD_unafford_n == pytest.approx(2692.1, abs=1e-3)


def test_regional_and_income_insights():
    _, aggregate = read_datasets()
    reg = change_table(aggregate, "region", 2025)
    ssa = reg.loc[reg.country.eq("Sub-Saharan Africa")].iloc[0]
    assert round(ssa.change_million, 1) == 194.3
    groups = aggregate[(aggregate.year == 2025) & (aggregate.group_type == "income")]
    low = groups[groups.country.eq("Low-income")].iloc[0]
    high = groups[groups.country.eq("High-income")].iloc[0]
    assert round(low.CoHD_headcount - high.CoHD_headcount, 1) == 68.0


def test_nutrition_coverage_and_spearman():
    country, _ = read_datasets()
    df = nutrition_rows(country, 2024, "stunting_pct")
    assert len(df) == 125
    assert round(spearman_corr(df.CoHD_headcount, df.stunting_pct), 3) == 0.784
    assert country[country.year.eq(2025)].stunting_pct.notna().sum() == 0


def test_censored_pou_not_treated_as_exact():
    country, _ = read_datasets()
    df = nutrition_rows(country, 2024, "pou")
    assert not df.pou_below_2_5.astype(str).str.lower().eq("true").any()
