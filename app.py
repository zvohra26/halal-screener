import base64
import html
import streamlit as st
from screener import analyze, suggest, DEBT_LIMIT, CASH_LIMIT

st.set_page_config(page_title="CREST · Halal Stock Screening", page_icon="🛡️")

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

# ---------- Custom styling ----------
st.markdown("""
<style>
.block-container {padding-top: 4rem; max-width: 760px;}
.hero {background: linear-gradient(135deg, #0F3D2E 0%, #1F7A5A 60%, #2FA37A 100%); color: white; padding: 2.2rem 2rem; border-radius: 20px; margin-bottom: 1.5rem; box-shadow: 0 10px 30px rgba(15,61,46,0.25);}
.brand {display: flex; align-items: center; gap: .9rem; margin-bottom: .5rem;}
.brand img {width: 60px; height: 60px;}
.wordmark {font-size: 2.7rem; font-weight: 800; letter-spacing: .14em; line-height: 1;}
.expansion {font-size: .8rem; letter-spacing: .08em; text-transform: uppercase; color: rgba(255,255,255,0.75); margin-bottom: 1.2rem;}
.expansion b {color: #F3E3B0;}
.hero .sub {color: white; font-size: 1.05rem; line-height: 1.5;}
.hero .who {color: rgba(255,255,255,0.72); font-size: .92rem; margin-top: .6rem; line-height: 1.5;}
div[data-testid="stButton"] button {border-radius: 999px; border: 1px solid #D9D4C7; background: white; font-weight: 600;}
div[data-testid="stButton"] button:hover {border-color: #1F7A5A; color: #1F7A5A;}
.card {background: white; border-radius: 18px; padding: 1.6rem; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #ECE8DF; margin-top: 1rem;}
.card .name {font-size: 1.5rem; font-weight: 700;}
.card .industry {color: #6B6B6B; font-size: .9rem; margin-top: .15rem;}
.verdict {display: inline-block; font-weight: 700; padding: .5rem 1.1rem; border-radius: 999px; margin: 1rem 0 .6rem 0;}
.pass {background: #E3F4EC; color: #1F7A5A;}
.fail {background: #FCE8E6; color: #B3261E;}
.unknown {background: #FFF4D6; color: #8A6100;}
.reason {color: #444; font-size: .95rem; margin: .2rem 0;}
.ratios {display: flex; gap: 1rem; margin-top: 1.2rem; flex-wrap: wrap;}
.ratio {flex: 1; min-width: 200px; background: #F3F0E8; border-radius: 14px; padding: 1rem 1.1rem;}
.ratio .label {font-size: .75rem; color: #6B6B6B; text-transform: uppercase; letter-spacing: .06em;}
.ratio .value {font-size: 1.8rem; font-weight: 700; margin: .2rem 0 .6rem 0;}
.bar {height: 8px; background: #E4E0D6; border-radius: 999px; overflow: hidden;}
.fill {height: 100%; border-radius: 999px;}
.limit {font-size: .75rem; color: #888; margin-top: .4rem;}
.srclink {margin-top: 1rem; font-size: .85rem;}
.srclink a {color: #1F7A5A; text-decoration: none; font-weight: 600;}
.footer {text-align: center; color: #999; font-size: .8rem; margin-top: 2.5rem;}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown(f"""
<div class="hero">
<div class="brand"><img src="{LOGO_URI}" alt="CREST logo"><div class="wordmark">CREST</div></div>
<div class="expansion"><b>C</b>ompliance <b>R</b>eview of <b>E</b>quities against <b>S</b>hariah <b>T</b>hresholds</div>
<div class="sub">CREST checks whether a stock is Shariah-compliant. Enter any ticker to see if the company's business and finances meet common Islamic finance standards, and exactly why it passes or fails.</div>
<div class="who">Built for Muslim investors who want to avoid riba and impermissible industries without digging through balance sheets themselves.</div>
</div>
""", unsafe_allow_html=True)

# ---------- How it works + Sources ----------
info_col, src_col = st.columns([3, 1])

with info_col:
    with st.expander("How does the screening work?"):
        st.markdown(f"""
**1. Business activity:** companies in banking, insurance, alcohol, gambling, or tobacco fail automatically.

**2. Debt ratio:** debt ÷ market cap must be under **{DEBT_LIMIT:.0%}**.

**3. Cash ratio:** cash and short-term investments ÷ market cap must be under **{CASH_LIMIT:.0%}**.

Scholars differ on exact limits. CREST follows common AAOIFI-style thresholds.
""")

with src_col:
    with st.popover("ⓘ Data sources"):
        st.markdown("""
**📈 Market data: Yahoo Finance**

Market cap, total debt, cash and short-term investments, and industry classification are pulled live from [Yahoo Finance](https://finance.yahoo.com) every time you search, using the open-source [yfinance](https://github.com/ranaroussi/yfinance) library.

**🕌 Screening standards: AAOIFI**

Thresholds are based on [AAOIFI](https://aaoifi.com) (Accounting and Auditing Organization for Islamic Financial Institutions) Shariah Standard No. 21 on shares, one of the most widely referenced standards in Islamic finance. It sets a 30% limit on interest-bearing debt and on interest-bearing cash and investments, relative to market value.

**⚖️ Good to know**

CREST is an independent project and is not certified by AAOIFI or any Shariah board. It approximates these rules using free data and does not yet screen impermissible income. Other standards, such as the S&P and MSCI Islamic indexes, use slightly different thresholds. For investment decisions, consult a qualified scholar or a certified screening provider.
""")

# ---------- Input ----------
if "ticker" not in st.session_state:
    st.session_state.ticker = ""


def set_ticker(t):
    st.session_state.ticker = t


st.write("**Try one:**")
cols = st.columns(5)
for col, t in zip(cols, ["AAPL", "MSFT", "NVDA", "F", "JPM"]):
    col.button(t, width="stretch", on_click=set_ticker, args=(t,))

ticker = st.text_input("Enter a ticker or company name", key="ticker", placeholder="e.g. TSLA or Tesla")


def show_suggestions(query):
    options = suggest(query)
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


# ---------- Results ----------
if ticker:
    query = ticker.strip()

    with st.spinner("Pulling live data..."):
        try:
            r = analyze(query)
        except Exception:
            r = None

    if r is None or (r["name"] == r["ticker"] and r["industry"] == "Unknown"):
        st.error(f"Couldn't find a stock with the ticker '{query.upper()}'.")
        show_suggestions(query)
        st.stop()

    verdicts = {
        "PASS": ("pass", "✓ Passes Shariah screening"),
        "FAIL": ("fail", "✕ Does not pass"),
        "UNKNOWN": ("unknown", "! Not enough data to screen"),
    }
    cls, text = verdicts[r["status"]]
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
        f'{reasons}{ratios}'
        f'<div class="srclink"><a href="https://finance.yahoo.com/quote/{html.escape(r["ticker"])}" target="_blank">View source data on Yahoo Finance ↗</a></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ---------- Footer ----------
st.markdown(
    '<div class="footer">CREST is for educational purposes only. Not financial or religious advice.<br>'
    'Data from Yahoo Finance · Screening thresholds based on AAOIFI Shariah Standard No. 21</div>',
    unsafe_allow_html=True,
)