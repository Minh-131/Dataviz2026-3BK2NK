import pandas as pd, glob
U='/mnt/user-data/uploads/'; O='/mnt/user-data/outputs/fpn_clean/'
base = pd.read_csv(O+'fpn_countries.csv').drop(columns=['region','income_group','gdp_pc_ppp','pou','pou_below_2_5','stunting_pct'], errors='ignore')

# 1. WDI GDP per capita PPP
w = pd.read_csv(glob.glob(U+'3e32bb55*_Data.csv')[0], encoding='cp1252', dtype=str)
w = w[w['Series Code']=='NY.GDP.PCAP.PP.CD']
ycols = [c for c in w.columns if '[YR' in c]
g = w.melt(id_vars=['Country Code'], value_vars=ycols, var_name='year', value_name='gdp_pc_ppp')
g['year'] = g.year.str[:4].astype(int)
g['gdp_pc_ppp'] = pd.to_numeric(g.gdp_pc_ppp.replace('..', pd.NA), errors='coerce')
g = g.rename(columns={'Country Code':'iso3'}).dropna(subset=['gdp_pc_ppp'])

# 2. CLASS
c = pd.read_excel(U+'CLASS_2026_10_08.xlsx', sheet_name='List of economies')
c = c[c.Region.notna()][['Code','Region','Income group']].rename(columns={'Code':'iso3','Region':'region','Income group':'income_group'})

# 3. FAOSTAT PoU (3-yr avg -> middle year)
f = pd.read_csv(U+'FAOSTAT_data_en_10-15-2026.csv')
f['year'] = f.Year.str[:4].astype(int) + 1
f['pou_below_2_5'] = f.Value.astype(str).str.startswith('<')
f['pou'] = pd.to_numeric(f.Value.astype(str).str.replace('<',''), errors='coerce')
p = f.rename(columns={'Area Code (ISO3)':'iso3'})[['iso3','year','pou','pou_below_2_5']].dropna(subset=['pou'])

# 4. JME stunting prevalence (both sexes, point estimate)
j = pd.read_excel(U+'jme-country-estimates-march2026.xlsx', sheet_name='Stunting Prevalence')
j = j.rename(columns={'ISO Code':'iso3','Year':'year','Both Sexes - Point Estimates':'stunting_pct'})[['iso3','year','stunting_pct']]
j['stunting_pct'] = pd.to_numeric(j.stunting_pct, errors='coerce'); j = j.dropna()
j['year'] = j.year.astype(int)

m = (base.merge(c, on='iso3', how='left')
         .merge(g, on=['iso3','year'], how='left')
         .merge(p, on=['iso3','year'], how='left')
         .merge(j, on=['iso3','year'], how='left'))
front = ['country','iso3','year','region','income_group','population','gdp_pc_ppp','pou','pou_below_2_5','stunting_pct']
m = m[front + [x for x in m.columns if x not in front]]
m.to_csv(O+'fpn_countries.csv', index=False)

print(m.shape)
print('no region:', m[m.region.isna()].country.unique())
print(m.groupby('year')[['gdp_pc_ppp','pou','stunting_pct','CoHD_headcount']].count())
print('JME years', j.year.min(), j.year.max(), j.iso3.nunique(), '| PoU countries', p.iso3.nunique())
print('unmatched FAO iso3 in FPN:', sorted(set(base.iso3)-set(p.iso3))[:40])
