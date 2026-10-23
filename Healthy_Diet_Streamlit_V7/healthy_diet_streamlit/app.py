"""The Food Atlas: an interactive UN SDG 2 data story.

Run from the repository root: streamlit run app.py
"""
from html import escape

import streamlit as st

from src.flags import flag_img, flag_url, flagify
from src.charts import (
    CORAL, TEAL, set_chart_theme, compare_countries, country_map, group_history,
    history_line, nutrition_scatter, ranked_change, ranks,
)
from src.data import (
    METRICS, change_table, current_world, metric_for_group,
    nutrition_rows, read_datasets, world_rows,
)
from src.economics import (
    cross_section, cost_vs_affordability_chart,
    gdp_affordability_chart, gdp_associations,
)
from src.styles import get_css, LIGHT, DARK
from src.story_styles import story_css
from src.basket import basket_rows, basket_medians, country_basket_plot, income_group_plot, GROUPS
from src.statistics import spearman_corr
from src.narrative import (
    span_insight, percent_change_words, extremes_insight, group_change_insight,
    paired_correlation_insight, selected_group_insight, selected_country_insight,
)

st.set_page_config(
    page_title="The Food Atlas | SDG 2",
    page_icon="📖", layout="wide",
    initial_sidebar_state="expanded",
)
# A session-scoped toggle switches both the Streamlit layout and Plotly figures.
# No theme selection is stored in cookies or external services.
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False
st.markdown(get_css(st.session_state["dark_mode"]), unsafe_allow_html=True)
st.markdown(story_css(st.session_state["dark_mode"]), unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_data():
    return read_datasets()


def chart(fig, alt: str):
    st.plotly_chart(fig, width="stretch", theme=None, config={"displaylogo": False, "scrollZoom": False}, alt=alt)


def explain_plot(how_to_read: str, insight: str, caution: str = ""):
    """One visible takeaway per chart; reading guidance stays one click away."""
    st.markdown('<div class="plot-explanation"><p class="takeaway">' + flagify(escape(insight), NAME_TO_ISO) + '</p></div>',
                unsafe_allow_html=True)
    with st.expander("How to read this chart"):
        st.markdown(escape(how_to_read) + ("\n\n*" + escape(caution) + "*" if caution else ""))


def country_heading(name: str, suffix: str = "") -> None:
    iso = NAME_TO_ISO.get(name)
    st.markdown(f'<div class="country-heading">{flag_img(iso, name, cls="flag") if iso else ""}'
                f'<span>{escape(name)}</span><small>{escape(suffix)}</small></div>', unsafe_allow_html=True)


def callout(text: str, warning: bool = False):
    styling = "insight warning" if warning else "insight"
    st.markdown(f'<div class="{styling}">{flagify(text, NAME_TO_ISO)}</div>', unsafe_allow_html=True)


def section(eyebrow: str, heading: str, description: str):
    st.markdown(f'<div class="section-kicker">{escape(eyebrow)}</div>', unsafe_allow_html=True)
    st.subheader(heading)
    st.caption(description)


try:
    country_df, aggregate_df = load_data()
    NAME_TO_ISO = dict(country_df[["country", "iso3"]].drop_duplicates().values)
except (OSError, ValueError) as exc:
    st.error(f"Cannot load dashboard data: {exc}")
    st.stop()

world = world_rows(aggregate_df)
years = sorted(world.year.unique().tolist())

NAV = [
    "01  The paradox", "02  Where", "03  Left behind",
    "04  Income, not price", "05  The plate", "06  Fed vs. well fed",
    "07  Explore", "08  Sources and method",
]


STORY_URL = "https://claude.ai/artifact/XEx3UYEenFW9wL8zqdgZJw"


def go_to_chapter(index: int) -> None:
    st.session_state["chapter_nav"] = NAV[index]
    st.session_state["scroll_top"] = True
with st.sidebar:
    st.markdown('''<div class="sidebrand">
        <div class="brand-head"><span class="brand-issue">THE FOOD ATLAS / ISSUE 01</span><span class="brand-stamp">SDG 02</span></div>
        <div class="brand">The Food<br><em>Atlas.</em></div>
        <div class="strap">A VISUAL INVESTIGATION OF FOOD, WEALTH AND ACCESS</div>
    </div>''', unsafe_allow_html=True)
    st.link_button("Read the data story →", STORY_URL, use_container_width=True,
                   help="The guided, scroll-through version of this analysis. Opens in a new tab.")
    st.toggle("Dark reading mode", key="dark_mode", help="Switch the entire story and charts to dark mode.")
    st.markdown(f'<div class="nav-kicker"><span>CHAPTER INDEX</span><span>01 / {len(NAV):02d}</span></div>', unsafe_allow_html=True)
    view = st.radio("Explore the chapters", NAV, label_visibility="collapsed", key="chapter_nav")
    chapter_number = NAV.index(view) + 1
    st.markdown(
        f'<div class="reading-position"><div class="reading-position-top"><span>CURRENT CHAPTER</span>'
        f'<strong>{chapter_number:02d} OF {len(NAV):02d}</strong></div>'
        f'<div class="reading-track"><span style="width:{chapter_number / len(NAV) * 100:.2f}%"></span></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="side-tools-heading">READING SETTINGS</div>', unsafe_allow_html=True)
    year = st.select_slider("Reporting year", options=years, value=max(years),
                            disabled=(view == NAV[4]),
                            help="The food-basket chapter is fixed at 2021 because that is the only year with six food-group breakdowns.")
    st.caption("2017 to 2025. Basket components exist only for 2021; nutrition ends in 2024.")
    with st.expander("Reading guide"):
        st.markdown(
            "**Read it in order.** Each chapter ends with a *Next* button, or jump to any chapter above.\n\n"
            "**Change the year** with the slider; charts and insights update together.\n\n"
            "**Hover** over any country, dot or line for exact values. Grey on the map means no estimate, not zero.\n\n"
            "**Three routes in 2 minutes:** 01 The paradox → 04 Income, not price · 02 Where → 03 Left behind · 05 The plate → 06 Fed vs. well fed."
        )
    st.caption("SOURCES / World Bank · FAO · UNICEF, WHO and World Bank")
    st.markdown('<div class="side-footer"><span>THE FOOD ATLAS</span><span>FOOD PRICES FOR NUTRITION</span></div>', unsafe_allow_html=True)

# Sidebar controls are evaluated before we render any figures.
set_chart_theme(st.session_state["dark_mode"])

context_year = 2021 if view == NAV[4] else year
selected_world = current_world(aggregate_df, context_year)
base_world = current_world(aggregate_df, min(years))
wd_cost = float(selected_world.CoHD_PPP_PoP)
wd_rate = float(selected_world.CoHD_headcount)
wd_millions = float(selected_world.CoHD_unafford_n)
active_chapter = NAV.index(view) + 1

st.markdown(f'''<div class="edition-head"><span>FOOD / ECONOMY / INEQUALITY</span>
    <span><b>THE FOOD ATLAS</b> &nbsp; | &nbsp; {context_year}</span></div>
<div class="mobile-hint">Tap <b>&rsaquo;</b> at the top left to open the chapters, or use <b>Next</b> at the end of each chapter.</div>''', unsafe_allow_html=True)
if view == NAV[0]:
    st.markdown(f'''<div class="cover">
  <div class="cover-copy">
    <div class="issue">A global investigation into what nourishment costs</div>
    <h1>The price of <em>eating well.</em></h1>
    <p>A healthy diet has a price. Access to it has a geography.
    Follow the numbers from global trends to household affordability, nutrition and the six foods on a plate.</p>
  </div>
  <div class="cover-art" role="img" aria-label="Abstract concentric circles representing the six food groups in a healthy diet">
    <div class="orbital"></div><div class="orbital two"></div><div class="orbital three"></div>
    <div class="food-symbol">6</div>
    <div class="orbit-caption">SIX FOOD GROUPS</div>
    <div class="art-caption">ONE HEALTHY DIET</div>
  </div>
</div>
<div class="fact-strip">
  <div class="fact"><div class="label">The lowest-cost healthy diet</div>
    <div class="number"><span class="num-value">{wd_cost:.2f}</span><span class="unit">PPP $</span></div>
    <div class="delta">Per person per day, world average / {context_year}</div></div>
  <div class="fact"><div class="label">Share priced out</div>
    <div class="number"><span class="num-value">{wd_rate:.1f}</span><span class="unit">%</span></div>
    <div class="delta">Of the world's population cannot afford it</div></div>
  <div class="fact"><div class="label">People priced out</div>
    <div class="number"><span class="num-value">{wd_millions/1000:.2f}</span><span class="unit">bn</span></div>
    <div class="delta">Cannot afford a healthy diet</div></div>
</div>''', unsafe_allow_html=True)
else:
    st.markdown(f'''<div class="context-bar">World, {context_year}: &nbsp;<b>{wd_cost:.2f} PPP $</b> a day for a healthy diet
    &nbsp;·&nbsp; <b>{wd_rate:.1f}%</b> cannot afford it &nbsp;·&nbsp; <b>{wd_millions/1000:.2f} billion</b> people</div>''',
                unsafe_allow_html=True)
st.markdown(f'<div class="chapter-mark">Chapter {active_chapter:02d} / {len(NAV):02d} &nbsp; &bull; &nbsp; {escape(view[4:])}</div>',
            unsafe_allow_html=True)
if view == NAV[0]:
    st.caption(f"World totals, {context_year}. PPP $ are international dollars adjusted for purchasing power, not cash US dollars. Source: World Bank, Food Prices for Nutrition 5.0 (2026).")
    st.markdown("New here? [Read the data story first](%s) – a guided, five-minute version of this analysis – then come back to explore every country and year." % STORY_URL)


# 1. GLOBAL STORY
if view == NAV[0]:
    section("01 / THE PARADOX", "Prices rose. Fewer people were priced out.",
            "Compare trends in the global population-weighted cost of a healthy diet with the share unable to afford one.")
    initial = world.iloc[0]
    diff_cost = (wd_cost / float(initial.CoHD_PPP_PoP) - 1) * 100
    diff_rate = wd_rate - float(initial.CoHD_headcount)
    if year > min(years):
        cost_word = "rose" if diff_cost >= 0 else "fell"
        rate_word = "fell" if diff_rate <= 0 else "rose"
        link_word = "yet" if (diff_cost >= 0) == (diff_rate <= 0) else "and"
        callout(
            f"Between <b>{min(years)} and {year}</b>, the cost of a healthy diet {cost_word} <b>{abs(diff_cost):.0f}%</b>, from {float(initial.CoHD_PPP_PoP):.2f} to {wd_cost:.2f} PPP $ a day, "
            f"{link_word} the share of people who cannot afford it {rate_word} <b>{abs(diff_rate):.1f} percentage points</b>. "
            "The global average, however, hides who was left behind."
        )
    left, right = st.columns(2)
    clip = world[world.year.le(year)]
    with left:
        st.markdown("#### The cost of a healthy diet keeps climbing")
        chart(history_line(clip, "CoHD_PPP_PoP", "PPP $/person/day", color=CORAL),
              "Annual global population-weighted cost of a healthy diet")
        explain_plot(
            "Each dot is a reporting year; the y-axis shows the population-weighted minimum daily healthy-diet cost in purchasing-power-parity (PPP) dollars.",
            f"Between {min(years)} and {year}, this cost {percent_change_words(initial.CoHD_PPP_PoP, wd_cost)}. ",
            "PPP dollars compare purchasing power across countries; they are not local shop prices.",
        )
    with right:
        st.markdown("#### The share priced out is falling")
        chart(history_line(clip, "CoHD_headcount", "Share who cannot afford (%)", suffix="%", color=TEAL,
                           notes={2020: "2020: the only rise"} if year >= 2020 else None),
              "Annual global percentage unable to afford a healthy diet")
        explain_plot(
            "The y-axis measures the share of the world's population estimated to be unable to afford a healthy diet. Read vertical differences in percentage points (pp).",
            span_insight(clip, "CoHD_headcount", "The global unaffordability rate", "percentage points"),
            "A lower percentage does not necessarily imply that the absolute number affected has fallen.",
        )
    st.markdown(f"#### Still {wd_millions/1000:.1f} billion people cannot afford a healthy diet")
    chart(history_line(clip, "CoHD_unafford_n", "People who cannot afford (millions)", color="#7C69B0"),
          "Annual global number of people unable to afford a healthy diet in millions")
    explain_plot(
        "Each point gives the number of people estimated to be unable to afford a healthy diet, in millions. This measures the scale of the burden rather than its percentage of population.",
        span_insight(clip, "CoHD_unafford_n", "The number of people affected", "million people"),
        "Demographic growth can increase the number affected even if the percentage decreases.",
    )
    if year >= 2020:
        r2019 = current_world(aggregate_df, 2019).CoHD_headcount
        r2020 = current_world(aggregate_df, 2020).CoHD_headcount
        st.caption(f"2020 is the only year the share rose ({r2019:.1f}% → {r2020:.1f}%), coinciding with the COVID-19 pandemic.")

# 2. WORLD MAP
if view == NAV[1]:
    section("02 / WHERE", "Unaffordability is concentrated in Sub-Saharan Africa",
            f"Hover over a country to see its value for {year}. Grey = no estimate.")
    map_metric = st.radio("Map indicator", list(METRICS), horizontal=True, key="map_metric")
    map_col, map_unit, _ = METRICS[map_metric]
    selected_countries = country_df[country_df.year.eq(year)]
    chart(country_map(selected_countries, map_col, map_metric),
          f"World choropleth map colored by {map_metric} in {year}; land with no observation is grey")
    color_key = DARK if st.session_state["dark_mode"] else LIGHT
    st.markdown(f'''<div class="map-legend">
      <span><i class="swatch" style="background:{color_key['missing']}"></i>No observation / grey</span>
      <span><i class="swatch" style="background:{color_key['ocean']}"></i>Ocean / blue-grey</span>
      <span><i class="swatch" style="background:#B96B4D"></i>Observed value / see gradient scale</span>
    </div>''', unsafe_allow_html=True)
    explain_plot(
        f"Each country is coloured by the indicator chosen above. Grey countries have no estimate for {year} – missing data does not mean no problem.",
        extremes_insight(selected_countries, map_col, METRICS[map_metric][2], map_unit, year),
        "Country values are national estimates. Colours show the level in the selected year, not change over time.",
    )
    good = selected_countries.dropna(subset=[map_col])
    if not good.empty:
        hi = good.sort_values(map_col, ascending=False).iloc[0]
        lo = good.sort_values(map_col).iloc[0]
        # Observed levels, not changes: custom cards avoid st.metric's delta arrows.
        st.markdown(f'''
        <div class="extreme-grid" role="group" aria-label="Highest and lowest values for {escape(map_metric)}">
            <article class="extreme-card high">
                <div class="extreme-head"><span>HIGHEST</span><span>01 / MAX</span></div>
                <h3>{flag_img(hi.iso3, hi.country)}{escape(str(hi.country))}</h3>
                <div class="extreme-measure"><strong>{float(hi[map_col]):,.1f}</strong><span>{escape(str(map_unit))}</span></div>
                <div class="extreme-footer">Country estimate / {year}</div>
            </article>
            <article class="extreme-card low">
                <div class="extreme-head"><span>LOWEST</span><span>02 / MIN</span></div>
                <h3>{flag_img(lo.iso3, lo.country)}{escape(str(lo.country))}</h3>
                <div class="extreme-measure"><strong>{float(lo[map_col]):,.1f}</strong><span>{escape(str(map_unit))}</span></div>
                <div class="extreme-footer">Country estimate / {year}</div>
            </article>
        </div>
        ''', unsafe_allow_html=True)
        note = f"{len(good)} countries have an estimate for {year}."
        if map_col == "CoHD_headcount":
            note = f"In {int((good[map_col] > 50).sum())} of {len(good)} countries with an estimate for {year}, more than half the population cannot afford a healthy diet."
        st.caption(note)

# 3. REGIONAL & INCOME
if view == NAV[2]:
    section("03 / WHO’S LEFT BEHIND", "Sub-Saharan Africa is moving the other way",
            f"Change since {min(years)}, by region or income group. Official World Bank group estimates, not averages of countries.")
    group_choice = st.radio("Compare by", ["Region", "Income group"], horizontal=True)
    grp_type = "region" if group_choice == "Region" else "income"
    grp = aggregate_df[aggregate_df.group_type.eq(grp_type)].copy()
    grp_year = grp[grp.year.eq(year)]
    change = change_table(aggregate_df, grp_type, year)
    mleft, mright = st.columns(2)
    with mleft:
        st.markdown(f"#### Change in unaffordability rate, {min(years)} to {year}")
        chart(ranked_change(change, "change_pp", "Percentage-point change"),
              "Change in unaffordability rate by selected grouping")
        explain_plot(
            "Bars show the difference between the selected year and 2017 in unaffordability share. Left of zero (teal) means a lower rate; right of zero (orange) means a higher rate.",
            group_change_insight(change, "change_pp", "percentage points", min(years), year),
            "Rate differences must be expressed in percentage points, not percent growth.",
        )
    with mright:
        st.markdown(f"#### Change in people who cannot afford it, {min(years)} to {year}")
        chart(ranked_change(change, "change_million", "Change in millions"),
              "Change in millions of people unable to afford by selected grouping")
        explain_plot(
            "Bars show the change in the estimated number of people affected (millions) between 2017 and the selected year. Teal indicates a decline; orange indicates an increase.",
            group_change_insight(change, "change_million", "million people", min(years), year),
            "Changes in the number of people include the effects of population changes; do not interpret them as rate changes.",
        )
    if grp_type == "region":
        s = change.loc[change.country.eq("Sub-Saharan Africa")]
        if not s.empty:
            value = float(s.iloc[0].change_million)
            wl_now, wl_base = current_world(aggregate_df, year), base_world
            ssa = aggregate_df[aggregate_df.group_type.eq("region") & aggregate_df.country.eq("Sub-Saharan Africa")].set_index("year")
            share_now = float(ssa.loc[year, "CoHD_unafford_n"]) / float(wl_now.CoHD_unafford_n) * 100
            share_base = float(ssa.loc[min(years), "CoHD_unafford_n"]) / float(base_world.CoHD_unafford_n) * 100
            direction = "more" if value > 0 else "fewer"
            callout(f"<b>Sub-Saharan Africa:</b> <b>{abs(value):,.0f} million {direction} people</b> cannot afford a healthy diet than in {min(years)}. "
                    f"The region now holds <b>{share_now:.0f}% of everyone priced out worldwide</b>, up from {share_base:.0f}%." if share_now > share_base else
                    f"<b>Sub-Saharan Africa:</b> <b>{abs(value):,.0f} million {direction} people</b> cannot afford a healthy diet than in {min(years)}.",
                    warning=value > 0)
    else:
        low = grp_year[grp_year.country.eq("Low-income")]
        high = grp_year[grp_year.country.eq("High-income")]
        if not low.empty and not high.empty:
            gap = float(low.iloc[0].CoHD_headcount - high.iloc[0].CoHD_headcount)
            callout(f"<b>Income divide ({year}):</b> {low.iloc[0].CoHD_headcount:.0f}% of people in low-income countries cannot afford a healthy diet, against {high.iloc[0].CoHD_headcount:.0f}% in high-income countries – a <b>{gap:.1f} percentage-point</b> gap.", warning=True)
    st.markdown("#### Compare group trends")
    metric = st.selectbox("Trend indicator", list(METRICS), key="group_metric")
    trend_col = metric_for_group(metric)
    groups = sorted(grp.country.unique())
    defaults = [g for g in (["Sub-Saharan Africa", "South Asia", "East Asia & Pacific"] if grp_type == "region" else ["Low-income", "Lower-middle-income", "High-income"]) if g in groups]
    selected = st.multiselect("Choose regions or income groups (up to 5)", groups, default=defaults, max_selections=5)
    if selected:
        chart(group_history(grp[grp.year.le(year)], trend_col, METRICS[metric][1], selected,
                            highlight="Sub-Saharan Africa" if grp_type == "region" else "Low-income"),
              "Historical trends for selected group aggregates")
        explain_plot(
            "Each colored line is a region or income group selected above; points are annual estimates, and the unit follows the trend indicator you chose.",
            selected_group_insight(grp, trend_col, year, selected, METRICS[metric][1]),
            "Group values are official population-weighted estimates, not simple averages of countries.",
        )
    else:
        st.info("Select at least one group to see its history.")

# 4. ECONOMICS / AFFORDABILITY
if view == NAV[3]:
    section("04 / INCOME, NOT PRICE", "Same price, different worlds",
            "Compare economic resources, diet costs and the share of people unable to afford a healthy diet.")
    snapshot = cross_section(country_df, year)
    stats = gdp_associations(country_df, year)
    if stats["n"] > 2:
        a, b, c = st.columns(3)
        a.metric("GDP vs share priced out (ρ)", f'{stats["rho_gdp_vs_unafford"]:+.3f}')
        b.metric("GDP vs diet cost (ρ)", f'{stats["rho_gdp_vs_diet_cost"]:+.3f}')
        c.metric("Countries compared", f'{stats["n"]}')
        st.caption("ρ = Spearman rank correlation (−1 to +1). GDP per person: World Bank WDI, PPP, current international $.")
        left, right = st.columns(2)
        with left:
            st.markdown("#### Richer countries have far fewer people priced out")
            chart(gdp_affordability_chart(snapshot),
                  f"Scatter plot GDP per capita versus unable to afford (%) in {year}; GDP axis is logarithmic")
            explain_plot(
                "Each point represents one country with valid GDP, diet-cost and unaffordability data. GDP per capita is on a logarithmic horizontal scale; vertical position is unaffordability rate; color denotes income group.",
                f"The richer the country, the smaller the share priced out (ρ = {stats['rho_gdp_vs_unafford']:.2f} across {stats['n']} countries).",
                "GDP per person is a national average, not household income.",
            )
        with right:
            st.markdown("#### …but a healthy diet costs about the same in rich and poor countries")
            chart(cost_vs_affordability_chart(snapshot),
                  f"Scatter plot healthy diet cost versus unable to afford (%) in {year}")
            cost_rate_rho = spearman_corr(snapshot.CoHD_PPP, snapshot.CoHD_headcount)
            explain_plot(
                "Each point is a country. Horizontal position is the PPP cost of a healthy diet; vertical position is the percentage unable to afford it; colors represent income groups. Hover to inspect a country.",
                f"Price barely predicts who is priced out (ρ = {cost_rate_rho:+.2f}). Income makes the difference.",
                "Similar PPP costs can coexist with very different affordability rates. This plot cannot isolate why.",
            )
        pair = snapshot[snapshot.country.isin(["Nigeria", "Cyprus"])].set_index("country")
        if {"Nigeria", "Cyprus"}.issubset(set(pair.index)):
            a, b = pair.loc["Nigeria"], pair.loc["Cyprus"]
            delta = abs(float(a.CoHD_headcount - b.CoHD_headcount))
            if abs(float(a.CoHD_PPP - b.CoHD_PPP)) <= 0.02:
                callout(f"<b>Nigeria vs Cyprus ({year}):</b> a healthy diet cost the same – <b>{a.CoHD_PPP:.2f} PPP $ a day</b>. "
                        f"Yet <b>{a.CoHD_headcount:.1f}%</b> of Nigerians could not afford it, compared with "
                        f"<b>{b.CoHD_headcount:.1f}%</b> of Cypriots.", warning=True)
        low = aggregate_df[(aggregate_df.year.eq(year)) & aggregate_df.group_type.eq("income") & aggregate_df.country.eq("Low-income")]
        high = aggregate_df[(aggregate_df.year.eq(year)) & aggregate_df.group_type.eq("income") & aggregate_df.country.eq("High-income")]
        if not low.empty and not high.empty:
            lv, hv = low.iloc[0], high.iloc[0]
            callout(f"<b>Income groups ({year}):</b> low-income countries pay about the same for a healthy diet as high-income ones "
                    f"(<b>{lv.CoHD_PPP_PoP:.2f}</b> vs <b>{hv.CoHD_PPP_PoP:.2f} PPP $ a day</b>), but "
                    f"<b>{lv.CoHD_headcount:.1f}%</b> of their people cannot afford it, against <b>{hv.CoHD_headcount:.1f}%</b>.")
        st.caption("Associations across countries, not proof of cause.")
    else:
        st.warning("Not enough paired country GDP/affordability observations for this year.")

# 5. THE FOOD BASKET / data available for 2021 only
if view == NAV[4]:
    section("05 / THE PLATE", "What makes a healthy plate expensive",
            "Six food groups, 2021 – the only year with this level of detail.")
    basket = basket_rows(country_df)
    if basket.empty:
        st.warning("No complete food-group price records are available.")
    else:
        medians = basket_medians(country_df)
        low = medians[medians.income_group.str.replace("-", " ", regex=False).str.lower().eq("low income")]
        high = medians[medians.income_group.str.replace("-", " ", regex=False).str.lower().eq("high income")]
        if not low.empty and not high.empty:
            ll,hh=low.iloc[0],high.iloc[0]
            difference=ll.median_asf_share-hh.median_asf_share
            callout(f"<b>On the plate:</b> animal-source foods make up a median <b>{ll.median_asf_share:.0f}%</b> "
                    f"of a healthy diet's cost in low-income countries, versus <b>{hh.median_asf_share:.0f}%</b> in high-income ones.")
        available_names = sorted(basket.country.tolist())
        suggested = "Nigeria" if "Nigeria" in available_names else available_names[0]
        a,b = st.columns([1, 1.08],gap="large")
        with a:
            st.markdown("#### The cost of one plate")
            selected_name=st.selectbox("Choose a country for the 2021 basket",available_names,
                                       index=available_names.index(suggested),key="basket_country")
            country_heading(selected_name, "2021 healthy diet basket")
            record = basket[basket.country.eq(selected_name)].iloc[0]
            chart(country_basket_plot(record,st.session_state["dark_mode"]),
                  f"Composition of the minimum-cost healthy diet for {selected_name}, 2021, across six food groups")
            group_costs={k:float(record[k]) for k in GROUPS}
            leader=max(group_costs,key=group_costs.get)
            explain_plot("Each coloured slice shows one food group's share of the summed daily PPP cost for "
                         "the selected country's least-cost healthy diet in 2021.",
                         f"In {selected_name}, {GROUPS[leader][0].lower()} have the largest cost share "
                         f"({record[leader + '_share']:.1f}%). The six groups sum to "
                         f"{record.basket_sum:.2f} PPP dollars per person per day.",
                         "Prices refer to least-cost modelled foods, not a household's actual grocery bill. The detailed group benchmark is 2021 only.")
        with b:
            st.markdown("#### A structural difference by income")
            chart(income_group_plot(country_df,st.session_state["dark_mode"]),
                  "Median share of diet cost allocated to animal-source foods by income group, 2021")
            explain_plot("Every dot is the median country-level percentage allocated to animal-source foods "
                         "in that income group. The number of countries is shown after each label.",
                         "The lower the income group, the more animal-source foods weigh on the cost of a healthy diet.",
                         "These are unweighted country medians, not population-weighted global figures. "
                         "Different available-country sets can affect comparisons.")
            st.markdown("#### The nutrition premium")
            premium=country_df.loc[country_df.year.eq(2021),'CoHD_CoCA'].dropna()
            if len(premium):
                st.markdown(f"<div class='insight'>A healthy diet costs a median <b>{premium.median():.1f} times</b> more "
                            f"than a diet that only meets calorie needs ({len(premium)} countries).</div>",
                            unsafe_allow_html=True)
            st.caption("The ratio compares the cheapest healthy diet with the cheapest diet that only meets calorie needs. "
                       "It does not measure what families actually spend.")
        st.download_button("Download the verified 2021 food basket table",
                           basket[['country','iso3','year','income_group','CoHD_PPP','basket_sum']
                                  + list(GROUPS) + [k+'_share' for k in GROUPS]].to_csv(index=False),
                           file_name="food_basket_costs_2021_derived.csv",mime="text/csv")
        st.caption(f"{len(basket)} countries with all six food-group costs, 2021.")

# 4. NUTRITION LINK
if view == NAV[5]:
    section("06 / FED VS. WELL FED", "Being fed is not the same as being well fed",
            "Countries, latest data 2024. Undernourishment = not enough calories. Stunting = children under five too short for their age. SDG targets 2.1 and 2.2.")
    available = sorted([int(y) for y in years if y <= 2024], reverse=True)
    nc1, nc2 = st.columns(2)
    with nc1:
        nyear = st.selectbox("Nutrition reporting year", available, index=0)
    with nc2:
        outcome_name = st.selectbox("Nutrition outcome", ["Under-five stunting (%)", "Prevalence of undernourishment (%)"])
    outcome = "stunting_pct" if outcome_name.startswith("Under-five") else "pou"
    nutrition = nutrition_rows(country_df, nyear, outcome)
    niger = country_df[country_df.iso3.eq("NER") & country_df.year.eq(nyear)]
    if not niger.empty and niger[["pou", "CoHD_headcount", "stunting_pct"]].notna().all(axis=None):
        n0 = niger.iloc[0]
        callout(f"<b>Niger ({nyear}):</b> only <b>{n0.pou:.0f}%</b> of people lack enough calories – but "
                f"<b>{n0.CoHD_headcount:.0f}%</b> cannot afford a healthy diet, and <b>{n0.stunting_pct:.0f}%</b> "
                "of children under five are stunted.", warning=True)
    if len(nutrition) > 2:
        rho = spearman_corr(nutrition["CoHD_headcount"], nutrition[outcome])
        m1, m2 = st.columns(2)
        m1.metric("How closely they move together (ρ)", f"{rho:.2f}", help="Spearman rank correlation across countries: 0 = no relationship, 1 = perfect.")
        m2.metric("Countries compared", f"{len(nutrition)}")
        chart(nutrition_scatter(nutrition, outcome, outcome_name, label="Niger", flag_iso="NER"),
              f"Scatterplot of healthy diet unaffordability and {outcome_name} across countries for {nyear}")
        explain_plot(
            "Each bubble is a country: x = population share unable to afford a healthy diet; y = selected nutrition outcome (%); color = region; bubble size approximately reflects population. Hover for country details.",
            (f"Where healthy diets are less affordable, {'child stunting' if outcome == 'stunting_pct' else 'undernourishment'} "
             f"tends to be {'higher' if rho > 0 else 'lower'} (ρ = {rho:.2f}, {len(nutrition)} countries)."),
            "Undernourishment values are three-year averages. An association across countries, not proof that one causes the other.",
        )
        if outcome == "pou":
            st.caption("Countries reported as \"below 2.5%\" undernourishment are left out of this comparison.")
        else:
            st.caption("Stunting is the SDG 2.2.1 indicator. Only countries with both measures are compared; no values are filled in.")
    else:
        st.warning("Insufficient paired country data for this nutrition comparison.")

# 5. COUNTRY EXPLORER
if view == NAV[6]:
    section("07 / EXPLORE", "Find your own story",
            "Ranking by share and ranking by number of people answer different questions.")
    ec1, ec2, ec3 = st.columns([1.3, 1.3, 1.1])
    with ec1:
        explorer_metric = st.selectbox("Rank by", list(METRICS), key="explorer_metric")
    with ec2:
        regions = sorted(country_df.region.dropna().unique().tolist())
        region_choice = st.selectbox("Region", ["All regions"] + regions)
    with ec3:
        top_n = st.slider("Top countries", min_value=5, max_value=20, value=12)
    explorer_col = METRICS[explorer_metric][0]
    ranked = country_df[country_df.year.eq(year)].copy()
    if region_choice != "All regions":
        ranked = ranked[ranked.region.eq(region_choice)]
    st.markdown(f"#### Top {top_n} countries, {year}")
    chart(ranks(ranked, explorer_col, explorer_metric, top_n, flags=NAME_TO_ISO),
          f"Top countries by {explorer_metric} for {year}")
    valid_rank = ranked.dropna(subset=[explorer_col]).nlargest(top_n, explorer_col)
    if not valid_rank.empty:
        top_row = valid_rank.iloc[0]
        explain_plot(
            "Bars rank countries in the selected region from highest to lower values of the chosen indicator. The region filter only affects the ranking and downloadable table; choose any countries below for the separate trend comparison.",
            f"For {year}, the top observed country in this filtered ranking is {top_row.country} ({top_row[explorer_col]:,.1f} {METRICS[explorer_metric][1]}), among {len(ranked.dropna(subset=[explorer_col]))} countries with this measure.",
            "A high percentage and a high total number describe different types of burden; change the indicator to compare them.",
        )
    else:
        st.info("No countries with this indicator in the selected region/year. Try another region or year.")
    st.markdown("#### One country up close")
    searchable = sorted(country_df.country.unique())
    default_country = "India" if "India" in searchable else searchable[0]
    chosen = st.selectbox("Country or territory", searchable, index=searchable.index(default_country))
    country_heading(chosen, f"2017–{year}")
    choice = country_df[country_df.country.eq(chosen) & country_df.year.le(year)].sort_values("year")
    c1, c2 = st.columns(2)
    with c1:
        chart(history_line(choice, "CoHD_headcount", "Share who cannot afford (%)", suffix="%"),
              f"Healthy-diet unaffordability for {chosen} by year")
        explain_plot(
            "The dots show annual estimates of the share of people unable to afford the diet in your selected country.",
            span_insight(choice, "CoHD_headcount", f"{chosen}'s unaffordability rate", "percentage points"),
        )
    with c2:
        chart(history_line(choice, "CoHD_PPP", "PPP $/person/day", color=CORAL),
              f"Healthy diet daily cost for {chosen} by year")
        explain_plot(
            "The y-axis shows the PPP cost of a healthy diet per person per day for your chosen country.",
            span_insight(choice, "CoHD_PPP", f"{chosen}'s daily healthy-diet cost", "PPP $/person/day"),
            "Country costs are national estimates; the world figure above is population-weighted.",
        )

    st.markdown("#### Compare countries over time")
    possibilities = sorted(country_df.country.unique().tolist())
    default_compare = [c for c in ["India", "Nigeria", "South Sudan"] if c in possibilities]
    selected_c = st.multiselect("Choose up to 5 countries/territories", possibilities, default=default_compare, max_selections=5)
    if selected_c:
        chart(compare_countries(country_df[country_df.year.le(year)], explorer_col, explorer_metric, selected_c, flags=NAME_TO_ISO),
              f"Historical country comparisons for {explorer_metric}")
        explain_plot(
            "A line represents each selected country, with one point per reporting year. Choose up to five countries to compare their trajectories. The lines stop at the selected global year.",
            selected_country_insight(country_df, explorer_col, year, selected_c, METRICS[explorer_metric][1]),
            "Country comparison is independent of the region filter used in the ranking above.",
        )
    else:
        st.info("Select at least one country to see a comparison.")
    st.markdown("#### Download the filtered country data")
    table = ranked[["country", "iso3", "year", "region", "income_group", "CoHD_PPP", "CoHD_headcount", "CoHD_unafford_n"]].copy()
    table = table.sort_values(explorer_col, ascending=False, na_position="last")
    table = table.rename(columns={
        "CoHD_PPP": "Cost (PPP $/person/day)",
        "CoHD_headcount": "Share who cannot afford (%)",
        "CoHD_unafford_n": "People who cannot afford (millions)",
    })
    shown = table.copy()
    shown.insert(0, "Flag", shown.iso3.map(lambda i: flag_url(i, 40)))
    st.dataframe(shown, hide_index=True, width="stretch",
                 column_config={"Flag": st.column_config.ImageColumn("", width="small")})
    st.caption("**Table guide:** rows show all countries in the selected year and region, sorted by the chosen indicator. A blank cell means unavailable data, not zero. The download exports this filtered table, not the charts.")
    st.download_button("⬇️ Download filtered CSV", table.to_csv(index=False).encode("utf-8"),
                       file_name=f"healthy_diet_country_explorer_{year}.csv", mime="text/csv")

# 6. METHODS
if view == NAV[7]:
    section("08 / SOURCES AND METHOD", "Sources and method", "Data definitions, limitations, reproducibility and SDG relevance.")
    st.markdown("""
**Data used**

- `data/fpn_countries.csv`: country-level observations, with ISO3 codes and indicators for 2017 to 2025.
- `data/fpn_aggregates.csv`: official world, regional and income-group estimates for 2017 to 2025.
- `data/food_basket_costs_2021_derived.csv`: derived by the team from the six 2021 food-group costs in the country file (165 complete cases).
- All figures come from official international datasets, cleaned and merged by the team. This is an independent student project, not an official UN, FAO or World Bank product.

**Indicator dictionary**

| Label in dashboard | Column | Meaning |
|---|---|---|
| Share who cannot afford (%) | `CoHD_headcount` | Percent unable to afford a healthy diet |
| People who cannot afford (millions) | `CoHD_unafford_n` | Number affected; values already expressed in millions |
| Country diet cost | `CoHD_PPP` | PPP dollars per person per day |
| World / group diet cost | `CoHD_PPP_PoP` | Population-weighted cost from provided aggregate |
| Under-five stunting | `stunting_pct` | Prevalence of child stunting (%) |
| Prevalence of undernourishment | `pou` | Undernourishment prevalence (%) |
| GDP per person, PPP | `gdp_pc_ppp` | Current international $ (WDI NY.GDP.PCAP.PP.CD); a national average, not household income |

**Analytical safeguards**

- World and group values are the official population-weighted aggregates, not simple averages of countries.
- Rate changes are in **percentage points**; cost growth is in **percent**.
- Missing observations are left missing, not changed to zero.
- The nutrition chapter stops in 2024, the latest year with undernourishment and stunting estimates.
- Six food-group cost components are published only for 2021 (the ICP price benchmark year), so the basket chapter is fixed to 2021.
- `pou_below_2_5` flags a reporting floor; flagged PoU observations are excluded from the PoU scatter/correlation.
- Correlations are descriptive associations across countries, not evidence of causation.
- GDP per person, PPP (current international $) is **not** household disposable income or a food budget.
- PPP dollars are an international purchasing-power unit, not local shop prices.
- Regional totals use the groupings published with the Food Prices for Nutrition data; country filters use the current World Bank classification (FY2027), so the two differ slightly.
- Correlations (ρ) are unweighted: each country counts once, whatever its population. Country-level patterns describe countries, not individual households.
- Coverage: 147 of 180 countries have a 2025 affordability estimate. Missing countries include conflict-affected ones such as Sudan and Somalia, so counts and rankings cover only countries with data.
- Why different years? Affordability and cost run to 2025, nutrition to 2024, and food-group costs exist only for 2021; each chart uses the latest year its source covers.

**UN Sustainable Development Goals**

- **SDG 2.1**: end hunger and ensure access to safe, nutritious and sufficient food.
- **SDG 2.2**: end all forms of malnutrition, including stunting among children under five.
- Food affordability offers useful context, but it is not interchangeable with official SDG 2.1.1 (PoU) or 2.2.1 (stunting).

**Sources**

- World Bank. *Food Prices for Nutrition*, version 5.0 (July 2026). CC BY 4.0.
- World Bank. *World Development Indicators*: GDP per capita, PPP (current international $), [NY.GDP.PCAP.PP.CD](https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.CD) (October 2026).
- World Bank. *Country and Lending Groups*, FY2027 classification (October 2026).
- FAO. *FAOSTAT – Suite of Food Security Indicators*: prevalence of undernourishment (accessed 15 October 2026). CC BY 4.0.
- UNICEF, WHO, World Bank. *Joint Child Malnutrition Estimates*, country modelled estimates (March 2026).
- FAO. [Cost and affordability of a healthy diet: methods](https://www.fao.org/in-action/coahd/methods/en).
- United Nations. [Sustainable Development Goal 2: Zero Hunger](https://sdgs.un.org/goals/goal2).
""")

if active_chapter < len(NAV):
    st.button(f"Next: {NAV[active_chapter][4:]}  →", type="primary", key="next_chapter",
              on_click=go_to_chapter, args=(active_chapter,))
if st.session_state.pop("scroll_top", False):
    _scroll = ("<script>try{const d=window.parent.document;"
                    "(d.querySelector('[data-testid=\"stMain\"]')||d.querySelector('section.main')||d.documentElement).scrollTo(0,0);"
                    "window.parent.scrollTo(0,0);}catch(e){}</script>")
    if hasattr(st, "iframe"):
        st.iframe(_scroll, height=1)
    else:
        import streamlit.components.v1 as components
        components.html(_scroll, height=0)
st.divider()
st.caption("The Food Atlas | Team 3BK2NK, Macquarie University DataViz 2026 | Data: World Bank, FAO, UNICEF/WHO/World Bank")
