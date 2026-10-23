"""Extra styles for the story features (takeaways, context bar, flags, Next button, phone hint).

Kept separate from src/styles.py so the V6 design file stays untouched; injected after it.
"""
from src.styles import LIGHT, DARK


def story_css(dark_mode: bool = False) -> str:
    c = DARK if dark_mode else LIGHT
    return """
<style>
.stApp div[data-baseweb="select"] div,.stApp div[data-baseweb="select"] svg {{color:{ink};fill:{ink};}}
.stApp button[kind="primary"] {{background:{primary};border:1px solid {primary};color:{paper};border-radius:3px;margin-top:18px;}}
.plot-explanation .takeaway {{color:{ink};font:1rem/1.55 Georgia,serif;margin:0;}}
.plot-explanation {{margin-bottom:4px;}}
.context-bar {{border-top:1px solid {line};border-bottom:1px solid {line};padding:9px 0;margin:4px 0 8px;font:.84rem Arial,sans-serif;color:{inksoft};}}
.context-bar b {{color:{ink};}}
.mobile-hint {{display:none;}}
.flag-inline {{height:.95em;width:auto;vertical-align:-0.1em;margin:0 .32em 0 .1em;border:1px solid {line};border-radius:2px;}}
.extreme-card h3 .flag {{width:1.15em;height:auto;vertical-align:-0.08em;margin-right:.35em;border:1px solid {line};border-radius:2px;}}
.country-heading {{display:flex;align-items:center;gap:12px;margin:6px 0 2px;font:1.55rem/1.2 Georgia,serif;color:{ink};}}
.country-heading .flag {{width:44px;height:auto;border:1px solid {line};border-radius:2px;}}
.country-heading small {{font:.8rem Arial,sans-serif;color:{muted};margin-left:4px;}}
@media (max-width:700px) {{
  .mobile-hint {{display:block;font:.8rem Arial,sans-serif;color:{inksoft};border:1px dashed {line};padding:8px 10px;margin:6px 0 10px;}}
}}
</style>
""".format(**c)
