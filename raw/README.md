# Raw data – how to download each file

These are the original downloads used to build `data/`. Save each file here **with exactly the name shown**, then run, from the repository root:

```
python scripts/clean_fpn.py
python scripts/merge_all.py
python scripts/validate_data.py
```

| Save as | Source | How to download |
|---|---|---|
| `fpn_databank.csv` | World Bank, Food Prices for Nutrition 5.0 | databank.worldbank.org → Food Prices for Nutrition. Country: select all · Classification: select all · Series: select all · Time: select all → Download options → CSV. Rename the `…_Data.csv` file from the zip. |
| `wdi_gdp_pc_ppp.csv` | World Bank, World Development Indicators | databank.worldbank.org → World Development Indicators. Country: select all · Series: *GDP per capita, PPP (current international $)* (NY.GDP.PCAP.PP.CD) · Time: 2017–2025 → CSV. Rename the `…_Data.csv` file. |
| `CLASS.xlsx` | World Bank, Country and Lending Groups (FY2027) | datahelpdesk.worldbank.org → "World Bank Country and Lending Groups" → *current classification by income in XLSX format*. |
| `faostat_pou.csv` | FAO, FAOSTAT Suite of Food Security Indicators | fao.org/faostat/en/#data/FS. Countries: select all · Elements: Value · Items: *Prevalence of undernourishment (percent)* · Years: 2017 / 2016-2018 onwards · area code **ISO3** · CSV. |
| `jme_country.xlsx` | UNICEF/WHO/World Bank, Joint Child Malnutrition Estimates | who.int → Joint child malnutrition estimates → Latest estimates → *Joint model-based estimates for stunting and overweight*. |

Downloaded 15 October 2026 (FPN 5.0 released 21 July 2026; WDI and CLASS 8 October 2026; JME March 2026).
