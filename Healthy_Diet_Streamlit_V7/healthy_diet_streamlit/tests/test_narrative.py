import pandas as pd
from src.narrative import (
    change_words, span_insight, extremes_insight, paired_correlation_insight,
    group_change_insight, selected_group_insight, selected_country_insight,
)


def test_dynamic_change_and_span():
    assert change_words(20, 15, "percentage points") == "fell by 5.0 percentage points"
    assert change_words(20, 25, "million") == "rose by 5.0 million"
    assert change_words(20, 20, "million") == "was broadly unchanged"
    frame = pd.DataFrame({"year": [2020, 2021], "rate": [20, 10]})
    assert "fell by 10.0 percentage points" in span_insight(frame, "rate", "Unaffordability", "percentage points")


def test_filtered_country_insights():
    frame = pd.DataFrame({
        "country": ["Alpha", "Beta", "Gamma"], "year": [2025]*3,
        "CoHD_headcount": [80, 20, None],
    })
    t = extremes_insight(frame, "CoHD_headcount", "Unable to afford", "%", 2025)
    assert "Alpha" in t and "Beta" in t and "2 countries" in t
    t = selected_country_insight(frame, "CoHD_headcount", 2025, ["Alpha", "Beta"], "%")
    assert "Alpha" in t and "Beta" in t


def test_filtered_aggregates_and_correlation():
    delta = pd.DataFrame({"country": ["R1", "R2"], "change_pp": [-5, 4]})
    assert "R2" in group_change_insight(delta, "change_pp", "percentage points", 2017, 2025)
    groups = pd.DataFrame({"year": [2025]*2, "country": ["R1", "R2"], "rate": [15, 30]})
    assert "R2" in selected_group_insight(groups, "rate", 2025, ["R1", "R2"], "%")
    text = paired_correlation_insight(-0.824, 142, "GDP", "unaffordability")
    assert "strong negative" in text and "142" in text
    assert "Insufficient" in paired_correlation_insight(float("nan"), 0, "x", "y")


def test_group_change_when_no_groups_increase():
    down = pd.DataFrame({"country": ["Low", "High"], "change_pp": [-1.4, -3.8]})
    s = group_change_insight(down, "change_pp", "percentage points", 2017, 2025)
    assert "All changing groups declined" in s and "High" in s
    unchanged = pd.DataFrame({"country": ["A", "B"], "change_pp": [0, 0]})
    assert "unchanged" in group_change_insight(unchanged, "change_pp", "percentage points", 2017, 2017)
