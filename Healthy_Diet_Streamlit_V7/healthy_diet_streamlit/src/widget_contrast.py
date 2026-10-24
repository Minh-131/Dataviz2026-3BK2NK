"""Dark-mode contrast compatibility for Streamlit form widgets.

The editorial dark toggle runs independently of the native, light Streamlit
configuration. Selectbox started moving from BaseWeb to React Aria in 1.59, so
styling only ``[data-baseweb="select"]`` no longer reaches the selected value.

Keep this stylesheet LAST (after get_css and story_css). Do not apply the light
control palette to labels, metrics, maps, or plot elements. All form overrides
are active in dark reading mode only.
"""


def widget_contrast_css(dark_mode: bool = False) -> str:
    if not dark_mode:
        return ""
    return """<style>
/* V7.1. Native Streamlit runs with a light theme; provide genuinely legible
   light fields in the editorial dark reading mode. */
.stApp {
  --atlas-control-bg: #EDF3F3;
  --atlas-control-fg: #183537;
  --atlas-control-muted: #526960;
  --atlas-control-border: #93AFA8;
  --atlas-control-hover: #D5E5DE;
  --atlas-chip-bg: #087F85;
  --atlas-chip-fg: #FFFFFF;
}

/* BACKGROUND: React Aria control (>=1.59), plus legacy BaseWeb (<1.59).
   Target form wrappers narrowly; do not color Streamlit widget labels. */
.stApp [data-testid="stSelectbox"] :is([role="combobox"], [data-slot="control"], [data-baseweb="select"] > div),
.stApp [data-testid="stMultiSelect"] :is([role="combobox"], [data-slot="control"], [data-baseweb="select"] > div),
.stApp [data-testid="stSelectbox"] input,
.stApp [data-testid="stTextInput"] input,
.stApp [data-testid="stNumberInput"] input {
  background-color: var(--atlas-control-bg) !important;
  color: var(--atlas-control-fg) !important;
  border-color: var(--atlas-control-border) !important;
  box-shadow: none !important;
}
/* Multiselect search input should blend into the outer field, not look like
   a separate white box next to selected chips. */
.stApp [data-testid="stMultiSelect"] input {
  background: transparent !important;
  color: var(--atlas-control-fg) !important;
  border-color: transparent !important;
  box-shadow: none !important;
}

/* CRITICAL FIX: the selected country / trend indicator lives in a real input
   on React Aria, NOT in [data-baseweb="select"] span. Both the CSS color and
   WebKit text-fill-color must be forced on the input itself. */
.stApp [data-testid="stSelectbox"] input,
.stApp [data-testid="stMultiSelect"] input,
.stApp [data-testid="stSelectbox"] input[role="combobox"],
.stApp [data-testid="stSelectbox"] [role="combobox"] input,
.stApp [data-testid="stSelectbox"] [data-slot="input"],
.stApp [data-testid="stMultiSelect"] [data-slot="input"],
.stApp [data-testid="stSelectbox"] [data-baseweb="select"] input,
.stApp [data-testid="stMultiSelect"] [data-baseweb="select"] input,
.stApp [data-testid="stTextInput"] input,
.stApp [data-testid="stNumberInput"] input {
  color: var(--atlas-control-fg) !important;
  -webkit-text-fill-color: var(--atlas-control-fg) !important;
  caret-color: var(--atlas-control-fg) !important;
  opacity: 1 !important;
}

/* The selected option can also be a non-input value in older Streamlit. */
.stApp [data-testid="stSelectbox"] :is(
    [data-slot="value"], [data-slot="selected-value"],
    [data-baseweb="select"] [role="combobox"],
    [data-baseweb="select"] [role="combobox"] span,
    [data-baseweb="select"] [role="combobox"] div
) {
  color: var(--atlas-control-fg) !important;
  -webkit-text-fill-color: var(--atlas-control-fg) !important;
  opacity: 1 !important;
}
.stApp [data-testid="stSelectbox"] input::placeholder,
.stApp [data-testid="stMultiSelect"] input::placeholder,
.stApp [data-testid="stTextInput"] input::placeholder {
  color: var(--atlas-control-muted) !important;
  -webkit-text-fill-color: var(--atlas-control-muted) !important;
  opacity: 1 !important;
}

/* Background of the multiselect outer shell (the chips retain their own fill). */
.stApp [data-testid="stMultiSelect"] :is([role="combobox"], [data-slot="control"], [data-baseweb="select"] > div) {
  background-color: var(--atlas-control-bg) !important;
  border-color: var(--atlas-control-border) !important;
}
/* Old BaseWeb containers sometimes render the selected text outside role=combobox. */
.stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div,
.stApp [data-testid="stMultiSelect"] [data-baseweb="select"] > div {
  background-color: var(--atlas-control-bg) !important;
  border-color: var(--atlas-control-border) !important;
}

/* Keep selected tags readable and preserve their distinctive teal color. */
.stApp [data-testid="stMultiSelect"] :is([data-baseweb="tag"], [data-testid="stMultiSelectTag"], [data-slot="tag"]) {
  background: var(--atlas-chip-bg) !important;
  border-color: var(--atlas-chip-bg) !important;
  color: var(--atlas-chip-fg) !important;
}
.stApp [data-testid="stMultiSelect"] :is([data-baseweb="tag"], [data-testid="stMultiSelectTag"], [data-slot="tag"]) :is(span, div, button, svg, path) {
  color: var(--atlas-chip-fg) !important;
  -webkit-text-fill-color: var(--atlas-chip-fg) !important;
}

/* Dropdown arrows / clear buttons: SVGs should use the control ink. */
.stApp [data-testid="stSelectbox"] :is([role="combobox"], [data-baseweb="select"]) svg,
.stApp [data-testid="stMultiSelect"] :is([role="combobox"], [data-baseweb="select"]) > svg,
.stApp [data-testid="stSelectbox"] :is([role="combobox"], [data-baseweb="select"]) button {
  color: var(--atlas-control-fg) !important;
  stroke: currentColor;
}

/* OPEN DROPDOWNS: newer Streamlit listboxes can be mounted outside .stApp.
   The stSelectboxVirtualDropdown portal is not a BaseWeb popover. */
body [data-testid="stSelectboxVirtualDropdown"],
body [data-testid="stMultiSelectVirtualDropdown"],
body [data-testid="stSelectboxVirtualDropdown"] [role="option"],
body [data-testid="stMultiSelectVirtualDropdown"] [role="option"],
body [data-baseweb="popover"] [role="listbox"],
body [data-baseweb="popover"] [role="option"] {
  background-color: #EDF3F3 !important;
  color: #183537 !important;
}
body [data-testid="stSelectboxVirtualDropdown"] :is(li, [role="option"], span, p),
body [data-testid="stMultiSelectVirtualDropdown"] :is(li, [role="option"], span, p),
body [data-baseweb="popover"] [role="option"] :is(span, p, div) {
  color: #183537 !important;
  -webkit-text-fill-color: #183537 !important;
}
body [data-testid="stSelectboxVirtualDropdown"] :is(li, [role="option"]):is(:hover, [aria-selected="true"], [data-focused="true"]),
body [data-testid="stMultiSelectVirtualDropdown"] :is(li, [role="option"]):is(:hover, [aria-selected="true"], [data-focused="true"]),
body [data-baseweb="popover"] [role="option"]:is(:hover, [aria-selected="true"]) {
  background-color: #D5E5DE !important;
}

/* Visible keyboard focus, while keeping the color of the main page intact. */
.stApp [data-testid="stSelectbox"] :is(input, [role="combobox"]):focus-visible,
.stApp [data-testid="stMultiSelect"] :is(input, [role="combobox"]):focus-visible {
  outline: 2px solid #397B69 !important;
  outline-offset: 1px;
}
</style>"""
