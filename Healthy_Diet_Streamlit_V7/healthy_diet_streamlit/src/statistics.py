"""Small statistical helpers without optional SciPy dependency.

Spearman rho is the Pearson correlation of average-ranked, paired non-missing
observations. This matches scipy.stats.spearmanr and pandas Spearman correlation
for the two-series case (including tied ranks and pairwise deletion).
"""
import numpy as np
import pandas as pd


def spearman_corr(x: pd.Series, y: pd.Series) -> float:
    """Spearman rank correlation for aligned numeric Pandas Series.

    Returns NaN for fewer than two valid pairs or a constant variable.
    """
    paired = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
    paired = paired.replace([np.inf, -np.inf], np.nan).dropna()
    if len(paired) < 2 or paired["x"].nunique() < 2 or paired["y"].nunique() < 2:
        return float("nan")
    return float(paired["x"].rank(method="average").corr(
        paired["y"].rank(method="average"), method="pearson"
    ))
