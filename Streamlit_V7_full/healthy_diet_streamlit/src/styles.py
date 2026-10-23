"""A bespoke editorial atlas theme, inspired by print cartography and data journalism (V7: V6 design rebuilt).

No external fonts or images are loaded. Light/dark modes use independent palettes.
"""

LIGHT = dict(bg='#FAF7F0', paper='#FFFEFB', ink='#202B2B', inksoft='#53605B', muted='#68756E',
             line='#DDD9CD', primary='#A43F2B', accent='#E4B76E', side='#EEE9DF',
             wash='#F3EEE4', shade='#E6E1D5', contrast='#183D39', ocean='#EDF3F3', missing='#D4D4D0')
DARK = dict(bg='#111E20', paper='#192B2B', ink='#F5F1E6', inksoft='#D0D5CB', muted='#B0BEB8',
            line='#445452', primary='#E9A381', accent='#F0C979', side='#162628',
            wash='#223537', shade='#344746', contrast='#16302F', ocean='#0C2635', missing='#89908D')


def get_css(dark_mode: bool = False) -> str:
    c = DARK if dark_mode else LIGHT
    return """
<style>
:root, .stApp, [data-testid="stAppViewContainer"] {{
  --background-color:{bg}; --secondary-background-color:{side};
  --text-color:{ink}; --primary-color:{primary}; --border-color:{line};
}}
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
  background:{bg}; color:{ink};
}}
.block-container {{max-width:1370px; padding:1.2rem 3.1rem 4.4rem;}}
[data-testid="stSidebar"], [data-testid="stSidebarContent"] {{background:{side};color:{ink};}}
[data-testid="stSidebar"] {{border-right:1px solid {line};}}
[data-testid="stHeader"] {{background:{bg};}}
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {{font-family:Georgia, 'Times New Roman', serif;color:{ink};letter-spacing:-.035em;}}
.stApp h2 {{font-size:clamp(1.65rem,2.8vw,2.5rem);line-height:1.12;margin:.5rem 0 .4rem;}}
.stApp h3 {{font-size:1.45rem;}}
.stApp p, .stApp li, .stApp label, .stApp small,
.stApp [data-testid="stMarkdownContainer"],.stApp [data-testid="stWidgetLabel"],
.stApp [data-testid="stMetricLabel"] {{color:{ink};}}
.stApp [data-testid="stCaptionContainer"] {{color:{muted};}}
.stApp a {{color:{primary};text-underline-offset:3px;}}
.stApp hr {{border:0;border-top:1px solid {line};}}
.stApp [data-testid="stRadio"] label {{color:{ink};}}
.stApp input, .stApp textarea {{color:{ink};}}
.stApp div[data-baseweb="select"] > div,
.stApp div[data-baseweb="input"] > div,
.stApp div[data-baseweb="base-input"],
.stApp [data-testid="stTextInput"] input,
.stApp [data-testid="stFileUploaderDropzone"] {{background:{paper};border-color:{line};color:{ink};border-radius:3px;}}
.stApp div[data-baseweb="select"] span,.stApp div[data-baseweb="select"] input {{color:{ink};}}
.stApp button[kind="secondary"],.stApp [data-testid="stDownloadButton"] button {{
  background:{paper};color:{ink};border:1px solid {line};border-radius:3px;
}}
.stApp [data-testid="stExpander"] {{background:{paper};border:1px solid {line};border-radius:3px;}}
.stApp [data-testid="stDataFrame"] {{border:1px solid {line};}}
.stApp [data-testid="stPlotlyChart"] {{background:transparent;}}
.stApp [data-testid="stAlert"] {{border-radius:3px;}}
[data-baseweb="popover"] [role="listbox"], [data-baseweb="popover"] [role="option"] {{background:{paper};color:{ink};}}
[data-baseweb="popover"] [role="option"]:hover {{background:{wash};}}

/* Replace the conventional SaaS dashboard cards with a print-editorial cover. */
.edition-head {{display:flex;align-items:center;justify-content:space-between;
  border-top:2px solid {ink};border-bottom:1px solid {line};padding:9px 2px;
  font:700 .66rem/1.4 Arial,sans-serif;letter-spacing:.19em;color:{muted};text-transform:uppercase;}}
.edition-head b {{color:{primary};}}
.cover {{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(205px,.55fr);min-height:310px;
  background:{paper};border-bottom:3px solid {ink};margin:0 0 1.2rem;}}
.cover-copy {{padding:33px 20px 25px 5px;}}
.cover-copy .issue {{font:bold .71rem/1.2 Arial,sans-serif;letter-spacing:.19em;text-transform:uppercase;color:{primary};}}
.cover-copy h1 {{font:normal clamp(2.75rem,5.3vw,5.3rem)/.98 Georgia,serif;
  margin:16px 0 17px;letter-spacing:-.066em;color:{ink};max-width:840px;}}
.cover-copy h1 em {{color:{primary};font-weight:normal;}}
.cover-copy p {{max-width:670px;font:1.04rem/1.63 Arial,sans-serif;color:{inksoft};margin:0;}}
.cover-art {{background:{contrast};color:#F6EFE1;position:relative;display:flex;align-items:center;
 justify-content:center;overflow:hidden;min-height:285px;}}
.cover-art .orbital {{position:absolute;width:260px;height:260px;border:1px solid rgba(235,215,163,.52);border-radius:50%;}}
.cover-art .orbital.two {{width:195px;height:195px;border-color:rgba(235,215,163,.3);}}
.cover-art .orbital.three {{width:125px;height:125px;border-color:rgba(235,215,163,.44);}}
.cover-art .food-symbol {{position:relative;text-align:center;font:italic 3.8rem/1 Georgia,serif;color:#F4D8B0;}}
.cover-art .art-caption {{position:absolute;bottom:20px;font:700 .63rem Arial,sans-serif;letter-spacing:.18em;color:#EED4AD;}}
.cover-art .orbit-caption {{position:absolute;top:20px;right:19px;color:#EED4AD;font:700 .61rem Arial,sans-serif;letter-spacing:.1em;}}

/* No rounded shadow-card grid. Use a ruled three-column index of facts. */
.fact-strip {{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));
  border-top:1px solid {line};border-bottom:1px solid {ink};margin:8px 0 24px;}}
.fact {{padding:15px 20px 17px 0;min-width:0;}}
.fact:not(:last-child) {{border-right:1px solid {line};margin-right:20px;}}
.fact .number {{font:normal clamp(1.6rem,3.1vw,2.85rem)/1.17 Georgia,serif;letter-spacing:-.04em;color:{ink};}}
.fact .number .unit {{color:{primary};}}
.fact .label {{font:bold .65rem/1.4 Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:{muted};margin-bottom:8px;}}
.fact .delta {{font: .77rem/1.4 Arial,sans-serif;color:{muted};margin-top:6px;}}
.chapter-mark {{font:700 .65rem/1.4 Arial,sans-serif;letter-spacing:.18em;text-transform:uppercase;color:{primary};
  margin:16px 0 0;padding-top:14px;border-top:1px solid {ink};}}
.section-kicker {{font:700 .68rem Arial,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:{primary};margin-top:14px;}}
.insight {{margin:12px 0 25px;border-top:1px solid {primary};border-bottom:1px solid {line};
  padding:15px 4px;font:1.04rem/1.64 Georgia,serif;color:{inksoft};background:transparent;}}
.insight b {{color:{ink};}}
.insight.warning {{border-top-color:#CE7658;}}
.plot-explanation {{margin:2px 0 28px;border-top:1px solid {line};padding:13px 4px 3px;
  color:{inksoft};font:.90rem/1.65 Arial,sans-serif;background:transparent;}}
.plot-explanation p {{color:{inksoft};margin:0 0 6px;}}
.plot-explanation strong {{color:{primary};font-weight:700;}}
.plot-explanation .plot-caution {{color:{muted};font-size:.82rem;}}
.map-legend {{display:flex;gap:22px;flex-wrap:wrap;border-top:1px solid {line};
  border-bottom:1px solid {line};padding:10px 0;font: .76rem Arial,sans-serif;color:{inksoft};}}
.map-legend .swatch {{display:inline-block;width:16px;height:12px;vertical-align:middle;margin-right:8px;border:1px solid {inksoft};}}
.stApp div[data-testid="stMetric"] {{border-radius:3px;background:{paper};border:1px solid {line};box-shadow:none;padding:13px 17px;}}
.stApp [data-testid="stMetricValue"] {{color:{ink};font-family:Georgia,serif;}}
.sidebrand {{border-top:3px solid {ink};padding:16px 0 13px;margin-bottom:14px;}}
.sidebrand .brand {{font:normal 1.7rem Georgia,serif;letter-spacing:-.04em;color:{ink};}}
.sidebrand .strap {{font:bold .61rem Arial,sans-serif;letter-spacing:.18em;color:{primary};margin-top:4px;}}
[data-testid="stSidebar"] [role="radiogroup"] label {{border-bottom:1px solid {line};padding:6px 0;}}
[data-testid="stSidebar"] [role="radiogroup"] label p {{font-size:.88rem;}}
/* ---- V6: editorial table of contents in the sidebar ---- */
.sidebrand .brand-head {{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;
  font:700 .6rem/1.3 Arial,sans-serif;letter-spacing:.16em;color:{muted};}}
.sidebrand .brand-stamp {{border:1px solid {primary};color:{primary};padding:2px 6px;border-radius:2px;letter-spacing:.12em;}}
.sidebrand .brand em {{color:{primary};font-style:italic;}}
.nav-kicker, .side-tools-heading {{display:flex;justify-content:space-between;font:700 .6rem/1.3 Arial,sans-serif;
  letter-spacing:.16em;color:{muted};border-top:1px solid {ink};padding-top:9px;margin:14px 0 6px;}}
[data-testid="stSidebar"] [role="radiogroup"] label {{border-bottom:1px solid {line};padding:7px 8px;margin:0;border-radius:2px;
  border-left:3px solid transparent;transition:background .15s;}}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {{background:{wash};}}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {{background:{paper};border-left-color:{primary};}}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {{color:{ink};font-weight:700;}}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:focus-visible) {{outline:2px solid {accent};outline-offset:1px;}}
.reading-position {{margin:12px 0 4px;}}
.reading-position-top {{display:flex;justify-content:space-between;align-items:baseline;font:700 .6rem/1.3 Arial,sans-serif;
  letter-spacing:.16em;color:{muted};}}
.reading-position-top strong {{color:{ink};font-size:.72rem;letter-spacing:.08em;}}
.reading-track {{height:3px;background:{line};margin-top:6px;}}
.reading-track span {{display:block;height:100%;background:{primary};}}
.side-footer {{display:flex;justify-content:space-between;gap:8px;border-top:1px solid {line};margin-top:16px;padding-top:9px;
  font:700 .56rem/1.3 Arial,sans-serif;letter-spacing:.14em;color:{muted};}}
.stApp [data-testid="stSidebar"] [data-testid="stLinkButton"] a {{background:{paper};border:1px solid {primary};border-radius:3px;}}
.stApp [data-testid="stSidebar"] [data-testid="stLinkButton"] a p {{color:{primary};font-weight:700;}}
.stApp [data-testid="stSidebar"] [data-testid="stLinkButton"] a:hover {{background:{wash};}}
/* ---- V6: KPI number and unit never overlap ---- */
.fact .number {{display:flex;align-items:baseline;gap:.22em;flex-wrap:wrap;}}
.fact .number .num-value {{letter-spacing:-.03em;}}
.fact .number .unit {{font-size:.56em;letter-spacing:0;}}
/* ---- V6: highest / lowest cards (levels, not changes) ---- */
.extreme-grid {{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:10px 0 6px;}}
.extreme-card {{background:{paper};border:1px solid {line};border-top:3px solid {primary};padding:13px 16px 14px;border-radius:2px;}}
.extreme-card.low {{border-top-color:{muted};}}
.extreme-head {{display:flex;justify-content:space-between;font:700 .6rem/1.3 Arial,sans-serif;letter-spacing:.16em;color:{muted};}}
.extreme-card h3 {{font:normal 1.6rem/1.2 Georgia,serif;margin:8px 0 4px;color:{ink};letter-spacing:-.02em;}}
.extreme-measure {{display:flex;align-items:baseline;gap:.3em;}}
.extreme-measure strong {{font:normal 1.5rem Georgia,serif;color:{primary};}}
.extreme-measure span {{font:.8rem Arial,sans-serif;color:{muted};}}
.extreme-footer {{font:.72rem Arial,sans-serif;color:{muted};margin-top:6px;border-top:1px solid {line};padding-top:6px;}}
@media (max-width:700px) {{.extreme-grid {{grid-template-columns:1fr;}}}}
.stApp :focus-visible {{outline:2px solid {accent};outline-offset:2px;}}
.stApp table th {{background:{wash};color:{ink};}}
.stApp table td {{border-color:{line};}}
@media (max-width:950px) {{.block-container {{padding-left:1.1rem;padding-right:1.1rem;}}.cover {{grid-template-columns:1fr 210px;}}}}
@media (max-width:700px) {{
  .block-container {{padding:.7rem 1rem 3rem;}}
  .cover {{grid-template-columns:1fr;}}
  .cover-copy {{padding:22px 8px 25px;}}
  .cover-copy h1 {{font-size:2.9rem;}}
  .cover-art {{min-height:130px;}}
  .cover-art .orbital {{width:150px;height:150px;}}
  .cover-art .orbital.two {{width:105px;height:105px;}}
  .cover-art .orbital.three {{width:55px;height:55px;}}
  .cover-art .food-symbol {{font-size:2.4rem;}}
  .fact-strip {{grid-template-columns:1fr;}}
  .fact {{padding:12px 0;border-right:0!important;border-bottom:1px solid {line};margin-right:0!important;}}
}}
</style>
""".format(**c)

CSS = get_css(False)
