import base64
import html
import streamlit as st
from screener import analyze, suggest, DEBT_LIMIT, CASH_LIMIT
from ethics import get_flags, LAST_UPDATED, UN_DATABASE_URL

st.set_page_config(page_title="CREST · Halal Stock Screening", page_icon="🛡️", layout="wide")


# ---------- Cached data calls (faster, fewer requests to Yahoo) ----------
@st.cache_data(ttl=3600, show_spinner=False)
def cached_analyze(t):
    return analyze(t)


@st.cache_data(ttl=3600, show_spinner=False)
def cached_suggest(q):
    return suggest(q)


# ---------- Logo (gold shield with a crescent) ----------
LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<defs>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#F3E3B0"/>
<stop offset="1" stop-color="#C9A227"/>
</linearGradient>
<mask id="cut">
<rect width="64" height="64" fill="white"/>
<circle cx="37" cy="27" r="11" fill="black"/>
</mask>
</defs>
<path d="M32 4 L56 12 V30 C56 45 45.5 55.5 32 60 C18.5 55.5 8 45 8 30 V12 Z" fill="url(#gold)"/>
<circle cx="31" cy="32" r="13" fill="#0F3D2E" mask="url(#cut)"/>
</svg>"""
LOGO_URI = "data:image/svg+xml;base64," + base64.b64encode(LOGO_SVG.encode()).decode()

# ---------- Background pattern (faint eight-point star) ----------
PATTERN_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96">
<g fill="none" stroke="#E6DECB" stroke-width="1">
<rect x="28" y="28" width="40" height="40"/>
<rect x="28" y="28" width="40" height="40" transform="rotate(45 48 48)"/>
<circle cx="48" cy="48" r="7"/>
</g>
</svg>"""
PATTERN_URI = "data:image/svg+xml;base64," + base64.b64encode(PATTERN_SVG.encode()).decode()

# ---------- Custom styling ----------
st.markdown("""
<style>
.block-container {padding-top: 3.5rem; padding-bottom: 3rem; max-width: 1200px;}
.hero {position: relative; overflow: hidden; background: linear-gradient(135deg, #0F3D2E 0%, #1F7A5A 60%, #2FA37A 100%); color: white; padding: 2.4rem 2.2rem; border-radius: 22px; margin-bottom: 1.8rem; box-shadow: 0 10px 30px rgba(15,61,46,0.25);}
.hero .watermark {position: absolute; right: -30px; top: -20px; width: 300px; opacity: .12;}
.brand {display: flex; align-items: center; gap: .9rem; margin-bottom: .5rem; position: relative;}
.brand img {width: 60px; height: 60px;}
.wordmark {font-size: 2.7rem; font-weight: 800; letter-spacing: .14em; line-height: 1;}
.expansion {font-size: .8rem; letter-spacing: .08em; text-transform: uppercase; color: rgba(255,255,255,0.75); margin-bottom: 1.2rem; position: relative;}
.expansion b {color: #F3E3B0;}
.hero .sub {color: white; font-size: 1.05rem; line-height: 1.5; max-width: 720px; position: relative;}
.hero .who {color: rgba(255,255,255,0.72); font-size: .92rem; margin-top: .6rem; line-height: 1.5; max-width: 720px; position: relative;}
div[data-testid="stButton"] button {border-radius: 999px; border: 1px solid #D9D4C7; background: white; font-weight: 600;}
div[data-testid="stButton"] button:hover {border-color: #1F7A5A; color: #1F7A5A;}
div[data-testid="stVerticalBlockBorderWrapper"] {background: white; border-radius: 18px;}
.card {background: white; border-radius: 18px; padding: 1.6rem; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #ECE8DF; margin-top: 1rem;}
.card .name {font-size: 1.5rem; font-weight: 700;}
.card .industry {color: #6B6B6B; font-size: .9rem; margin-top: .15rem;}
.verdict {display: inline-block; font-weight: 700; padding: .5rem 1.1rem; border-radius: 999px; margin: 1rem 0 .6rem 0;}
.pass {background: #E3F4EC; color: #1F7A5A;}
.fail {background: #FCE8E6; color: #B3261E;}
.unknown {background: #FFF4D6; color: #8A6100;}
.flagged {background: #FFF4D6; color: #8A6100;}
.reason {color: #444; font-size: .95rem; margin: .2rem 0;}
.ratios {display: flex; gap: 1rem; margin-top: 1.2rem; flex-wrap: wrap;}
.ratio {flex: 1; min-width: 200px; background: #F3F0E8; border-radius: 14px; padding: 1rem 1.1rem;}
.ratio .label {font-size: .75rem; color: #6B6B6B; text-transform: uppercase; letter-spacing: .06em;}
.ratio .value {font-size: 1.8rem; font-weight: 700; margin: .2rem 0 .6rem 0;}
.bar {height: 8px; background: #E4E0D6; border-radius: 999px; overflow: hidden;}
.fill {height: 100%; border-radius: 999px;}
.limit {font-size: .75rem; color: #888; margin-top: .4rem;}
.flags {margin-top: 1.4rem; border-top: 1px solid #ECE8DF; padding-top: 1rem;}
.flags-title {font-weight: 700; font-size: .95rem; margin-bottom: .6rem;}
.flag {background: #FFF8E6; border-left: 3px solid #C9A227; border-radius: 8px; padding: .7rem .9rem; margin-bottom: .6rem;}
.flag-cat {font-weight: 700; color: #8A6100; font-size: .9rem;}
.flag-reason {font-size: .88rem; color: #444; margin: .25rem 0;}
.flag-src {font-size: .78rem; color: #777;}
.flag-src a {color: #1F7A5A; text-decoration: none; font-weight: 600;}
.flags-note {font-size: .75rem; color: #999; margin-top: .4rem;}
.srclink {margin-top: 1rem; font-size: .85rem;}
.srclink a {color: #1F7A5A; text-decoration: none; font-weight: 600;}
.empty {background: white; border: 1px dashed #D9D4C7; border-radius: 18px; padding: 2.2rem 1.5rem; text-align: center; margin-top: 1rem;}
.empty .big {font-size: 1.2rem; font-weight: 700; margin-bottom: .4rem;}
.empty .small {color: #6B6B6B; font-size: .92rem; margin-bottom: 1.2rem;}
.legend {display: flex; gap: .6rem; justify-content: center; flex-wrap: wrap;}
.legend span {padding: .4rem .9rem; border-radius: 999px; font-size: .82rem; font-weight: 600;}
.panel {background: white; border-radius: 18px; padding: 1.3rem 1.4rem; border: 1px solid #ECE8DF; box-shadow: 0 4px 20px rgba(0,0,0,0.05); margin-bottom: 1rem;}
.panel-title {font-weight: 700; font-size: 1rem; margin-bottom: .9rem;}
.step {display: flex; gap: .75rem; margin-bottom: .85rem;}
.step-num {flex: 0 0 28px; height: 28px; border-radius: 50%; background: #E3F4EC; color: #1F7A5A; font-weight: 700; display: flex; align-items: center; justify-content: center; font-size: .85rem;}
.step-text {font-size: .87rem; color: #444; line-height: 1.45;}
.step-text b {color: #1A1A1A;}
.stats {display: flex; gap: .6rem;}
.stat {flex: 1; background: #F3F0E8; border-radius: 12px; padding: .75rem .4rem; text-align: center;}
.stat .num {font-size: 1.3rem; font-weight: 800; color: #1F7A5A;}
.stat .lbl {font-size: .68rem; color: #6B6B6B; text-transform: uppercase; letter-spacing: .05em; margin-top: .15rem;}
.src-item {font-size: .86rem; margin-bottom: .6rem; color: #444; line-height: 1.45;}
.src-item a {color: #1F7A5A; font-weight: 600; text-decoration: none;}
.src-note {font-size: .75rem; color: #999; margin-top: .7rem; line-height: 1.45;}
.footer {text-align: center; color: #999; font-size: .8rem; margin-top: 2.5rem;}
@media (max-width: 640px) {.hero .watermark {display: none;}}
.st-key-recent {background: white; border: 1px solid #ECE8DF; border-radius: 18px; padding: 1.1rem 1.2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.05); margin-bottom: 1rem;}
</style>
""", unsafe_allow_html=True)

st.markdown(
    f'<style>.stApp, [data-testid="stAppViewContainer"] {{background-color: #F7F5EF; background-image: url("{PATTERN_URI}");}}</style>',
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown(f"""
<div class="hero">
<img class="watermark" src="{LOGO_URI}" alt="">
<div class="brand"><img src="{LOGO_URI}" alt="CREST logo"><div class="wordmark">CREST</div></div>
<div class="expansion"><b>C</b>ompliance <b>R</b>eview of <b>E</b>quities against <b>S</b>hariah <b>T</b>hresholds</div>
<div class="sub">CREST checks whether a stock is Shariah-compliant. Enter any ticker to see if the company's business and finances meet common Islamic finance standards, and exactly why it passes or fails.</div>
<div class="who">Built for Muslim investors who want to avoid riba and impermissible industries without digging through balance sheets themselves.</div>
</div>
""", unsafe_allow_html=True)

# ---------- State and helpers ----------
if "ticker" not in st.session_state:
    st.session_state.ticker = ""
if "history" not in st.session_state:
    st.session_state.history = []


def set_ticker(t):
    st.session_state.ticker = t


def remember(sym, short):
    rest = [x for x in st.session_state.history if x[0] != sym]
    st.session_state.history = [(sym, short)] + rest[:5]


def verdict_for(r, flags):
    if r["status"] == "PASS" and flags:
        return "flagged", "✓ Passes Shariah screening · ⚠ Ethical concerns flagged", "⚠ Flagged"
    return {
        "PASS": ("pass", "✓ Passes Shariah screening", "✓ Pass"),
        "FAIL": ("fail", "✕ Does not pass", "✕ Fail"),
        "UNKNOWN": ("unknown", "! Not enough data to screen", "! No data"),
    }[r["status"]]


def show_suggestions(query):
    options = cached_suggest(query)
    if options:
        st.write("**Did you mean:**")
        for sym, name in options:
            st.button(f"{sym}  ·  {name}", key=f"sug_{sym}", on_click=set_ticker, args=(sym,))
    else:
        st.caption("No similar stocks found. Try the company name instead, e.g. 'apple'.")


def ratio_block(label, value, limit):
    pct = min(value / limit, 1.0) * 100
    color = "#1F7A5A" if value < limit else "#B3261E"
    return (
        f'<div class="ratio"><div class="label">{label}</div>'
        f'<div class="value">{value:.1%}</div>'
        f'<div class="bar"><div class="fill" style="width:{pct:.0f}%;background:{color};"></div></div>'
        f'<div class="limit">Limit: {limit:.0%}</div></div>'
    )


def flags_block(flags):
    if not flags:
        return ""
    items = "".join(
        f'<div class="flag"><div class="flag-cat">⚠ {html.escape(f["category"])}</div>'
        f'<div class="flag-reason">{html.escape(f["reason"])}</div>'
        f'<div class="flag-src">Source: <a href="{f["url"]}" target="_blank">{html.escape(f["source"])} ↗</a></div></div>'
        for f in flags
    )
    return (
        f'<div class="flags"><div class="flags-title">Ethical flags</div>{items}'
        f'<div class="flags-note">These flags come from outside sources and do not change the Shariah result. Whether they affect your decision is up to you.</div></div>'
    )


# ---------- Page layout: results on the left, info panel on the right ----------
left, right = st.columns([2, 1], gap="large")

with left:
    st.write("**Try one:**")
    cols = st.columns(5)
    for col, t in zip(cols, ["AAPL", "NVDA", "F", "JPM", "LMT"]):
        col.button(t, width="stretch", on_click=set_ticker, args=(t,))

    ticker = st.text_input("Enter a ticker or company name", key="ticker", placeholder="e.g. TSLA or Tesla")

    if not ticker:
        st.markdown(
            '<div class="empty"><div class="big">Screen any stock in seconds</div>'
            '<div class="small">Pick a ticker above or type a company name. You\'ll get one of three results:</div>'
            '<div class="legend"><span class="pass">✓ Passes</span>'
            '<span class="flagged">⚠ Passes, with ethical flags</span>'
            '<span class="fail">✕ Does not pass</span></div></div>',
            unsafe_allow_html=True,
        )
    else:
        query = ticker.strip()
        with st.spinner("Pulling live data..."):
            try:
                r = cached_analyze(query)
            except Exception:
                r = None

        if r is None:
            options = cached_suggest(query)
            if any(sym.upper() == query.upper() for sym, _ in options):
                st.warning(f"{query.upper()} is a real stock, but its data couldn't be loaded right now. Please try again in a minute.")
            else:
                st.error(f"Couldn't find a stock with the ticker '{query.upper()}'.")
                show_suggestions(query)
        else:
            flags = get_flags(r["ticker"], r["industry"])
            cls, text, short = verdict_for(r, flags)
            remember(r["ticker"], short)

            reasons = "".join(f'<div class="reason">• {html.escape(x)}</div>' for x in r["reasons"])
            ratios = ""
            if r["debt_ratio"] is not None:
                ratios = (
                    '<div class="ratios">'
                    + ratio_block("Debt ratio", r["debt_ratio"], DEBT_LIMIT)
                    + ratio_block("Cash ratio", r["cash_ratio"], CASH_LIMIT)
                    + "</div>"
                )

            st.markdown(
                f'<div class="card">'
                f'<div class="name">{html.escape(r["name"])} ({r["ticker"]})</div>'
                f'<div class="industry">{html.escape(r["industry"])}</div>'
                f'<div class="verdict {cls}">{text}</div>'
                f'{reasons}{ratios}{flags_block(flags)}'
                f'<div class="srclink"><a href="https://finance.yahoo.com/quote/{html.escape(r["ticker"])}" target="_blank">View source data on Yahoo Finance ↗</a></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

with right:
    st.markdown(f"""
<div class="panel">
<div class="panel-title">How CREST works</div>
<div class="step"><div class="step-num">1</div><div class="step-text"><b>Business check.</b> Banking, insurance, alcohol, gambling, and tobacco fail automatically.</div></div>
<div class="step"><div class="step-num">2</div><div class="step-text"><b>Debt check.</b> Debt ÷ market cap must be under {DEBT_LIMIT:.0%}.</div></div>
<div class="step"><div class="step-num">3</div><div class="step-text"><b>Cash check.</b> Cash and short-term investments ÷ market cap must be under {CASH_LIMIT:.0%}.</div></div>
<div class="step"><div class="step-num">4</div><div class="step-text"><b>Ethical flags.</b> Cited concerns like weapons or settlement activity, shown separately. They don't change the Shariah result.</div></div>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class="panel">
<div class="panel-title">Screening standard</div>
<div class="stats">
<div class="stat"><div class="num">{DEBT_LIMIT:.0%}</div><div class="lbl">Debt limit</div></div>
<div class="stat"><div class="num">{CASH_LIMIT:.0%}</div><div class="lbl">Cash limit</div></div>
<div class="stat"><div class="num">No. 21</div><div class="lbl">AAOIFI standard</div></div>
</div>
</div>
""", unsafe_allow_html=True)

    if st.session_state.history:
        with st.container(key="recent"):
            st.markdown("**Recently screened**")
            for sym, short in st.session_state.history:
                st.button(f"{sym}  ·  {short}", key=f"recent_{sym}", on_click=set_ticker, args=(sym,), width="stretch")

    st.markdown(f"""
<div class="panel">
<div class="panel-title">Data & sources</div>
<div class="src-item">📈 <b>Market data:</b> <a href="https://finance.yahoo.com" target="_blank">Yahoo Finance</a>, pulled live via the open-source <a href="https://github.com/ranaroussi/yfinance" target="_blank">yfinance</a> library.</div>
<div class="src-item">🕌 <b>Thresholds:</b> <a href="https://aaoifi.com" target="_blank">AAOIFI</a> Shariah Standard No. 21 on shares.</div>
<div class="src-item">⚠️ <b>Ethical flags:</b> Yahoo Finance industry data and the <a href="{UN_DATABASE_URL}" target="_blank">UN Human Rights Office database</a> of businesses involved in Israeli settlements.</div>
<div class="src-note">Ethical data last updated {LAST_UPDATED}. CREST is independent and not certified by AAOIFI or any Shariah board. It approximates these rules with free data and does not yet screen impermissible income.</div>
</div>
""", unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown(
    '<div class="footer">CREST is for educational purposes only. Not financial or religious advice.<br>'
    'Data from Yahoo Finance · Screening thresholds based on AAOIFI Shariah Standard No. 21</div>',
    unsafe_allow_html=True,
)