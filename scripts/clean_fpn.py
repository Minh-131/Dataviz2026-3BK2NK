import pandas as pd, glob, re
src = glob.glob('/mnt/user-data/uploads/*_Data.csv')[0]
raw = pd.read_csv(src, encoding='cp1252', dtype=str)
raw = raw[raw['Country Code'].notna() & raw['Time'].notna()].copy()   # drop footer rows

id_cols = {'Country Name':'country','Country Code':'iso3','Time':'year'}
series_cols = [c for c in raw.columns if re.search(r'\[.+\]$', c) and c not in ('Classification Name',)]
series_cols = [c for c in series_cols if c not in id_cols]
code = {c: re.search(r'\[(.+)\]$', c).group(1) for c in series_cols}
label = {code[c]: re.sub(r'\s*\[.+\]$', '', c) for c in series_cols}

df = raw[list(id_cols) + series_cols].rename(columns={**id_cols, **code})
df = df.replace('..', pd.NA)
df['year'] = df['year'].astype(float).astype(int)
for c in code.values():
    df[c] = pd.to_numeric(df[c], errors='coerce')
df = df.rename(columns={'NY.GDP.PCAP.PP.CD':'gdp_pc_ppp','NY.GNP.PCAP.PP.CD':'gni_pc_ppp','Pop':'population'})
label['gdp_pc_ppp']=label.pop('NY.GDP.PCAP.PP.CD'); label['gni_pc_ppp']=label.pop('NY.GNP.PCAP.PP.CD'); label['population']=label.pop('Pop')

value_cols = [c for c in df.columns if c not in ('country','iso3','year')]
df = df.sort_values(['iso3','year'])
df.to_csv('fpn_countries_wide.csv', index=False)

long = df.melt(id_vars=['country','iso3','year'], var_name='indicator', value_name='value').dropna(subset=['value'])
long['indicator_name'] = long['indicator'].map(label)
long.to_csv('fpn_countries_long.csv', index=False)

# coverage: number of countries with data per indicator per year
cov = df.groupby('year')[value_cols].count().T
cov.insert(0,'indicator_name',[label[c] for c in cov.index])
cov.index.name='indicator'
cov.to_csv('fpn_coverage.csv')
print(df.shape, df['iso3'].nunique(), 'countries')
pd.set_option('display.width',250); pd.set_option('display.max_rows',100)
print(cov.drop(columns='indicator_name'))

# ---- split aggregates, drop empty cols, write deliverables ----
AGG = {'EAS','ECS','HIC','LCN','LIC','LMC','MEA','NAC','SAS','SSF','UMC','WLD'}
empty = [c for c in value_cols if df[c].notna().sum()==0]
df2 = df.drop(columns=empty)
agg = df2[df2.iso3.isin(AGG)].copy()
agg.insert(2,'group_type', agg.iso3.map(lambda x: 'world' if x=='WLD' else ('income' if x in {'HIC','LIC','LMC','UMC'} else 'region')))
ctry = df2[~df2.iso3.isin(AGG)].drop(columns=[c for c in df2.columns if c.endswith('_PoP')])
import os; out='/mnt/user-data/outputs/fpn_clean'; os.makedirs(out, exist_ok=True)
ctry.to_csv(f'{out}/fpn_countries.csv', index=False)
agg.to_csv(f'{out}/fpn_aggregates.csv', index=False)
cov2 = cov.drop(index=empty); cov2.to_csv(f'{out}/fpn_coverage.csv')
print(ctry.shape, ctry.iso3.nunique(), agg.shape, 'dropped empty:', empty)
print(ctry[['CoHD_f_prop','CoHD_headcount','CoHD_fexp','CoHD_pov']].describe().loc[['min','max']])
