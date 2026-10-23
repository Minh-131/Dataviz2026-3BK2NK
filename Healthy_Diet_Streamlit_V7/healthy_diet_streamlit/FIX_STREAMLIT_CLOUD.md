# Streamlit Cloud ModuleNotFoundError: fixed in V3.1

## Cause

The original V3 used `Series.corr(method="spearman")` in the GDP, inflation,
and nutrition sections. Pandas internally imports `scipy.stats.spearmanr` for
this correlation method, while the V3 requirements file did not include SciPy.
Therefore Streamlit Cloud raised `ModuleNotFoundError`.

## Fix in V3.1

All Spearman calculations now use `src/statistics.py:spearman_corr`.
It ranks the *paired non-missing values* with average rank for ties, and then
computes Pearson correlation. This is mathematically Spearman rho and does not
need SciPy. Fixed `src/economics.py`, `app.py`, and the relevant tests.

No additional package is required for this fix. Existing CSVs and dashboard
insights are preserved.

## Deployment steps

1. Replace the contents of `healthy_diet_streamlit/` in your repository with
   the updated V3.1 project. In particular, upload **the new file**
   `healthy_diet_streamlit/src/statistics.py`, otherwise imports will fail.
2. Commit changes to the branch used by Streamlit Cloud.
3. Check in Streamlit Cloud that the app entrypoint is
   `healthy_diet_streamlit/app.py` (when the GitHub repository has this subfolder).
4. Streamlit Cloud normally redeploys automatically after a push; if needed,
   open Manage app -> Reboot app.

To verify locally from the `healthy_diet_streamlit` directory:

```bash
python -m pip install -r requirements.txt
python -m pip install pytest
python -m pytest -q
python -m streamlit run app.py
```

**Alternative quick fix for the OLD V3**: add `scipy` to
`healthy_diet_streamlit/requirements.txt` and commit it.

Your original error log shows Python 3.14. This missing-dependency error is not
proof Python 3.14 is itself broken. If you want to move to Python 3.12, Streamlit
Community Cloud requires deleting and redeploying the app with the desired
Python version selected in Advanced settings. Save the URL, repo, entrypoint,
and secrets before deleting.
