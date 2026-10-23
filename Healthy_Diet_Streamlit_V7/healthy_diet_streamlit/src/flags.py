"""Country flag helpers: ISO3 -> flag image URL (images, because flag emoji do not render on Windows)."""
from functools import lru_cache
from html import escape
from pathlib import Path
import re

import pandas as pd

_LOOKUP = Path(__file__).resolve().parent.parent / "data" / "iso3_to_iso2.csv"


@lru_cache(maxsize=1)
def iso2_lookup() -> dict:
    try:
        return dict(pd.read_csv(_LOOKUP).values)
    except OSError:
        return {}


def flag_url(iso3: str, width: int = 80) -> str | None:
    iso2 = iso2_lookup().get(iso3)
    return f"https://flagcdn.com/w{width}/{iso2}.png" if iso2 else None


def flag_img(iso3: str, name: str = "", cls: str = "flag-inline") -> str:
    url = flag_url(iso3)
    if not url:
        return ""
    return f'<img class="{cls}" src="{url}" alt="" aria-hidden="true">'


def flagify(html_text: str, name_to_iso: dict) -> str:
    """Insert a flag before every country name in already-escaped text (longest names first)."""
    names = sorted((n for n in name_to_iso if n), key=len, reverse=True)
    if not names:
        return html_text
    pattern = re.compile(r"(?<![\w&;])(" + "|".join(re.escape(escape(n)) for n in names) + r")(?![\w])")
    unescape = {escape(n): n for n in names}

    def repl(m):
        name = unescape.get(m.group(1), m.group(1))
        return flag_img(name_to_iso[name], name) + m.group(1)
    return pattern.sub(repl, html_text)
