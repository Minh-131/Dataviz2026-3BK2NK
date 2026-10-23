"""Pure, testable narrative helpers for dynamic chart explanations.

No Streamlit dependency. Takeaways reflect the current displayed selections,
not hard-coded 2025 numbers. These are descriptive comparisons only.
"""
from __future__ import annotations

import math
import pandas as pd


def number(value: float, decimals: int = 1) -> str:
    return f"{float(value):,.{decimals}f}"


def change_words(start: float, end: float, unit: str = "", decimals: int = 1) -> str:
    """Natural description of an endpoint change (end minus start)."""
    a, b = float(start), float(end)
    if not (math.isfinite(a) and math.isfinite(b)):
        return "the change is not available"
    delta = b - a
    quantity = number(abs(delta), decimals)
    if abs(delta) < 0.5 * 10 ** (-decimals):
        return "was broadly unchanged"
    return f"{'rose' if delta > 0 else 'fell'} by {quantity}{(' ' + unit) if unit else ''}"


def percent_change_words(start: float, end: float) -> str:
    if pd.isna(start) or pd.isna(end) or float(start) == 0:
        return "a percentage change cannot be calculated"
    change = (float(end) / float(start) - 1) * 100
    return change_words(0, change, "percent", decimals=1)


def span_insight(frame: pd.DataFrame, metric: str, title: str, unit: str, *, decimals: int = 1) -> str:
    """Endpoint insight for a single year-indexed line after removing missing data."""
    valid = frame.dropna(subset=[metric]).sort_values("year")
    if len(valid) == 0:
        return f"No valid observations are available for {title}."
    start, end = valid.iloc[0], valid.iloc[-1]
    if len(valid) == 1:
        return f"{title} in {int(end.year)}: {number(end[metric], decimals)} {unit}."
    phrase = change_words(start[metric], end[metric], unit, decimals)
    return (f"{title} {phrase} from {number(start[metric], decimals)} to "
            f"{number(end[metric], decimals)} between {int(start.year)} and {int(end.year)}.")


def extremes_insight(frame: pd.DataFrame, metric: str, label: str, unit: str, year: int) -> str:
    valid = frame.dropna(subset=[metric, "country"])
    if valid.empty:
        return f"No observed country values are available for {label} in {year}."
    high, low = valid.loc[valid[metric].idxmax()], valid.loc[valid[metric].idxmin()]
    sep = "" if unit == "%" else " "
    return (f"{high.country} has the highest {label[0].lower() + label[1:]} "
            f"({number(high[metric])}{sep}{unit}); {low.country} has the lowest "
            f"({number(low[metric])}{sep}{unit}), among {len(valid)} countries with an estimate for {year}.")


def group_change_insight(frame: pd.DataFrame, metric: str, unit: str, start: int, end: int) -> str:
    valid = frame.dropna(subset=[metric, "country"])
    if valid.empty:
        return "No comparable group observations are available."
    increasing = valid.loc[valid[metric] > 0]
    decreasing = valid.loc[valid[metric] < 0]
    if increasing.empty and decreasing.empty:
        return f"All observed groups were unchanged on this measure between {start} and {end}."
    if not increasing.empty and not decreasing.empty:
        up = increasing.loc[increasing[metric].idxmax()]
        down = decreasing.loc[decreasing[metric].idxmin()]
        return (f"From {start} to {end}, the largest increase was in {up.country} "
                f"(+{number(up[metric])} {unit}); the largest decrease was in "
                f"{down.country} ({number(down[metric])} {unit}).")
    if not decreasing.empty:
        down = decreasing.loc[decreasing[metric].idxmin()]
        return (f"All changing groups declined between {start} and {end}; "
                f"the largest decline was in {down.country} "
                f"({number(down[metric])} {unit}).")
    up = increasing.loc[increasing[metric].idxmax()]
    return (f"All changing groups increased between {start} and {end}; "
            f"the largest increase was in {up.country} (+{number(up[metric])} {unit}).")


def paired_correlation_insight(rho: float, n: int, x_label: str, y_label: str) -> str:
    if n < 3 or not math.isfinite(float(rho)):
        return "Insufficient complete observations to describe this association."
    rho = float(rho)
    strength = "weak" if abs(rho) < 0.3 else "moderate" if abs(rho) < 0.7 else "strong"
    direction = "negative" if rho < 0 else "positive" if rho > 0 else "negligible"
    return (f"Across {n} paired country observations, {x_label} and {y_label} "
            f"show a {strength} {direction} rank association (Spearman ρ = {rho:+.3f}). "
            "This does not establish cause and effect.")


def selected_group_insight(frame: pd.DataFrame, metric: str, year: int, groups: list[str], unit: str) -> str:
    valid = frame.loc[frame.year.eq(year) & frame.country.isin(groups)].dropna(subset=[metric])
    if not len(valid):
        return "No current-year observations are available for the selected groups."
    hi, lo = valid.loc[valid[metric].idxmax()], valid.loc[valid[metric].idxmin()]
    if len(valid) == 1:
        return f"{hi.country}: {number(hi[metric])} {unit} in {year}."
    return (f"In {year}, among your selected groups, {hi.country} has the highest value "
            f"({number(hi[metric])} {unit}), versus {lo.country} at {number(lo[metric])} {unit}.")


def selected_country_insight(frame: pd.DataFrame, metric: str, year: int, countries: list[str], unit: str) -> str:
    valid = frame.loc[frame.year.eq(year) & frame.country.isin(countries)].dropna(subset=[metric])
    if len(valid) == 0:
        return "No valid observations for the selected countries in this year."
    hi = valid.loc[valid[metric].idxmax()]
    if len(valid) == 1:
        return f"{hi.country}: {number(hi[metric])} {unit} in {year}."
    lo = valid.loc[valid[metric].idxmin()]
    return (f"Among the selected countries in {year}, {hi.country} has the highest value "
            f"({number(hi[metric])} {unit}), while {lo.country} has the lowest "
            f"({number(lo[metric])} {unit}).")
