import streamlit as st
from screener import analyze, DEBT_LIMIT, CASH_LIMIT

st.set_page_config(page_title="Halal Stock Screener", page_icon="🌙")

st.title("🌙 Halal Stock Screener")
st.markdown("Check whether a stock passes common **Shariah screening rules** in seconds.")

with st.expander("How does the screening work?"):
    st.markdown(f"""
**1. Business activity:** companies in banking, insurance, alcohol, gambling, or tobacco fail automatically.

**2. Debt ratio:** debt ÷ market cap must be under **{DEBT_LIMIT:.0%}**.

**3. Cash ratio:** cash and short-term investments ÷ market cap must be under **{CASH_LIMIT:.0%}**.

Thresholds follow AAOIFI-style standards. Scholars differ on exact limits.
""")

if "ticker" not in st.session_state:
    st.session_state.ticker = ""

st.write("Try one:")
cols = st.columns(5)
for col, t in zip(cols, ["AAPL", "MSFT", "NVDA", "F", "JPM"]):
    if col.button(t, width="stretch"):
        st.session_state.ticker = t

ticker = st.text_input("Or enter any ticker", key="ticker", placeholder="e.g. TSLA")

if ticker:
    with st.spinner("Pulling live data..."):
        try:
            r = analyze(ticker.strip())
        except Exception:
            st.error("Couldn't fetch data for that ticker. Check the spelling and try again.")
            st.stop()

    if r["name"] == r["ticker"] and r["industry"] == "Unknown":
        st.error(f"Couldn't find a stock with the ticker '{r['ticker']}'. Check the spelling.")
        st.stop()

    with st.container(border=True):
        st.subheader(f"{r['name']} ({r['ticker']})")
        st.caption(f"Industry: {r['industry']}")

        if r["status"] == "PASS":
            st.success("✅ Passes Shariah screening")
        elif r["status"] == "FAIL":
            st.error("❌ Does not pass")
        else:
            st.warning("⚠️ Not enough data to screen this stock")

        for reason in r["reasons"]:
            st.write(f"• {reason}")

        if r["debt_ratio"] is not None:
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Debt ratio", f"{r['debt_ratio']:.1%}", help=f"Limit: {DEBT_LIMIT:.0%}")
                st.progress(min(r["debt_ratio"] / DEBT_LIMIT, 1.0), text="Share of limit used")
            with c2:
                st.metric("Cash ratio", f"{r['cash_ratio']:.1%}", help=f"Limit: {CASH_LIMIT:.0%}")
                st.progress(min(r["cash_ratio"] / CASH_LIMIT, 1.0), text="Share of limit used")

st.divider()
st.caption(
    "For educational purposes only. Not financial or religious advice. "
    "Data from Yahoo Finance and may be delayed or incomplete."
)