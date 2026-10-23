"""Reproducible cross-sectional healthy-diet basket analysis, using 2021 only.

The supplied country CSV contains food-group costs for 2021 only.
Missing costs are never filled with zeros, and group medians are unweighted.
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

GROUPS = {
    'CoHD_ss_PPP': ('Starchy staples', '#C2A669'),
    'CoHD_v_PPP': ('Vegetables', '#537D64'),
    'CoHD_f_PPP': ('Fruits', '#CF715A'),
    'CoHD_asf_PPP': ('Animal-source foods', '#385C85'),
    'CoHD_lns_PPP': ('Legumes, nuts & seeds', '#8C749D'),
    'CoHD_of_PPP': ('Oils & fats', '#988B78'),
}


def basket_rows(frame: pd.DataFrame) -> pd.DataFrame:
    """Retain 2021 country observations with a complete six-part PPP basket."""
    cols = list(GROUPS)
    required = {'country', 'iso3', 'year', 'income_group', 'CoHD_PPP', *cols}
    absent = required.difference(frame.columns)
    if absent:
        raise ValueError(f'Missing food basket columns: {sorted(absent)}')
    subset = frame.loc[frame.year.eq(2021)].dropna(subset=['CoHD_PPP', *cols]).copy()
    subset['basket_sum'] = subset[cols].sum(axis=1)
    subset = subset[subset['basket_sum'].gt(0)].copy()
    for column in cols:
        subset[column + '_share'] = 100 * subset[column] / subset.basket_sum
    return subset


def basket_medians(frame: pd.DataFrame) -> pd.DataFrame:
    """Unweighted country-level median group shares, with exact n per income group."""
    data = basket_rows(frame).dropna(subset=['income_group'])
    data = data.loc[~data.income_group.isin(['Unclassified', 'Unknown'])]
    result = data.groupby('income_group', observed=True).agg(
        median_asf_share=('CoHD_asf_PPP_share', 'median'),
        countries=('iso3', 'nunique'),
    ).reset_index()
    result['order'] = result.income_group.map({'Low income': 0, 'Low-income': 0, 'Lower-middle-income': 1,
                                              'Upper-middle-income': 2, 'High income': 3, 'High-income': 3}).fillna(9)
    return result.sort_values('order').drop(columns='order')


def country_basket_plot(row: pd.Series, dark_mode: bool = False):
    """Six cost components as a bespoke 'plate' ring: no fabricated food categories."""
    parts = list(GROUPS)
    fig = go.Figure(go.Pie(
        labels=[GROUPS[x][0] for x in parts],
        values=[float(row[x]) for x in parts],
        marker=dict(colors=[GROUPS[x][1] for x in parts], line=dict(color='#142027' if dark_mode else '#F9F6F0', width=3)),
        hole=0.65, textposition='outside', textinfo='percent',
        customdata=[f'{row[x]:.2f}' for x in parts],
        hovertemplate='%{label}<br>PPP $%{customdata}/day<br>%{percent} of six-group sum<extra></extra>',
        sort=False,
    ))
    fig.update_layout(
        height=405, margin=dict(l=15,r=15,t=30,b=15),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Georgia, serif',color='#EEE9DD' if dark_mode else '#242A26',size=13),
        showlegend=True, legend=dict(orientation='h', x=0, y=-0.05, title_text='', font=dict(size=11)),
        annotations=[dict(text=f'<b>{row.basket_sum:.2f}</b><br><span style="font-size:12px">PPP $/day</span>',
                          x=.5,y=.5,showarrow=False,font=dict(size=26,color='#EEE9DD' if dark_mode else '#242A26'))],
    )
    return fig


def income_group_plot(frame: pd.DataFrame, dark_mode: bool = False):
    grouped = basket_medians(frame)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=grouped.median_asf_share, y=grouped.income_group,
        mode='markers+text',text=[f'{v:.1f}%  (n={n})' for v,n in zip(grouped.median_asf_share,grouped.countries)],
        textposition='middle right', marker=dict(size=17,color='#D5664D',line=dict(width=2,color='#FBF7EF' if not dark_mode else '#13262A')),
        hovertemplate='%{y}<br>Median ASF share: %{x:.1f}%<extra></extra>',
    ))
    fig.update_layout(
        height=310, margin=dict(l=4,r=105,t=12,b=45),showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial, sans-serif', color='#EBE8E1' if dark_mode else '#32372E',size=13),
        xaxis=dict(title='Median share of diet cost (%)',range=[0,52],showgrid=True,
                   gridcolor='#364843' if dark_mode else '#E7E1D7',zeroline=False),
        yaxis=dict(title='',categoryorder='array',categoryarray=['High income','Upper middle income','Lower middle income','Low income'],
                   showgrid=False),
    )
    return fig


def export_basket(frame: pd.DataFrame, destination: Path) -> pd.DataFrame:
    result = basket_rows(frame)
    keep = ['country','iso3','year','income_group','CoHD_PPP','basket_sum'] + list(GROUPS) + [k+'_share' for k in GROUPS]
    destination.parent.mkdir(parents=True,exist_ok=True)
    result[keep].to_csv(destination,index=False)
    return result
