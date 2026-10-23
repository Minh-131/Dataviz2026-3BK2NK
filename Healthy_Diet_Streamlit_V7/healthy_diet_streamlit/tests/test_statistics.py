"""Spearman regression tests for the SciPy-free dashboard implementation."""
import math
import pandas as pd
import pytest

from src.statistics import spearman_corr


def test_perfect_inverse_and_identical_rank():
    a = pd.Series([1, 2, 3, 4])
    assert spearman_corr(a, pd.Series([4, 3, 2, 1])) == pytest.approx(-1.0)
    assert spearman_corr(a, a) == pytest.approx(1.0)


def test_ties_and_paired_missing_values():
    a = pd.Series([1, 2, 2, 4, 5, None])
    b = pd.Series([1, 2, 3, 4, 5, 6])
    assert spearman_corr(a, b) == pytest.approx(0.9746794344808963)
    # Missing values must be dropped before rank calculation.
    assert spearman_corr(a, b) == pytest.approx(spearman_corr(a.iloc[:5], b.iloc[:5]))


def test_degenerate_inputs():
    assert math.isnan(spearman_corr(pd.Series([1, 1, 1]), pd.Series([1, 2, 3])))
    assert math.isnan(spearman_corr(pd.Series([1, None]), pd.Series([3, 5])))
