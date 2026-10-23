# V5 Release Notes: The Food Atlas

## Design

- Replaced the gradient hero / standard KPI card / 8-tab layout with an asymmetric editorial cover, ruled data strip, large Georgia typography, newspaper-like chapter index and restrained print palette.
- Kept a bespoke dark reading theme.
- Replaced horizontal tabs with 9 chapters in the left navigation, displaying only the active story chapter.
- Styled explanatory copy like journal footnotes rather than generic callout cards.

## Cartography

- Plotly geographic base land with no selected observation: grey `#D4D4D0` in light theme, grey `#89908D` in dark theme.
- Ocean: blue-grey `#EAF2F4` in light theme, deep blue `#0C2635` in dark theme.
- Added clear legend and country borders. Missing values stay missing, not zero.

## New analysis

- New chapter: Inside the basket (2021 only).
- Six food-group shares and a country selector.
- Median animal-source-food share by country income classification with sample-size annotations.
- Median CoHD/CoCA ratio (nutrition premium) and explanatory caveats.
- Derived CSV generated from the previously supplied country CSV, with a reproducibility script.

## Integrity

- Preserved prior GDP, inflation, nutritional, regional and ranking logic.
- 20 Python unit tests pass; all nine app chapters exercised in both reading modes using a mocked UI (18 smoke runs).
- Standalone static HTML previews captured for desktop light, desktop dark and mobile; not a claim that full Streamlit runtime was tested.

## Limitations

- No new external inflation dataset is bundled. Direct download of the official World Bank XLSX was unavailable; upload remains optional.
- The 2021 decomposition must not be treated as 2025 food-basket detail.
- Validate actual Streamlit deployment and browser responsiveness before competition submission.
