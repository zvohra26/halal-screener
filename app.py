import streamlit as st
from screener import analyze, DEBT_LIMIT, CASH_LIMIT

st.set_page_config(page_title="Halal Stock Screener", page_icon="📈")

st.title("Halal Stock Screener")
st.write("Check whether a stock passes common Shariah screening rules (AAOIFI-style ratios).")

ticker = st.text_input("Enter a stock ticker", placeholder="e.g. AAPL")

if ticker:
    with st.spinner("Pulling data..."):
        try:
            r = analyze(ticker.strip())
        except Exception:
            st.error("Couldn't fetch data for that ticker. Check the spelling and try again.")
            st.stop()

    st.subheader(f"{r['name']} ({r['ticker']})")
    st.caption(f"Industry: {r['industry']}")

    if r["status"] == "PASS":
        st.success("PASS")
    elif r["status"] == "FAIL":
        st.error("FAIL")
    else:
        st.warning("UNKNOWN")

    for reason in r["reasons"]:
        st.write(f"- {reason}")

    if r["debt_ratio"] is not None:
        col1, col2 = st.columns(2)
        col1.metric("Debt ratio", f"{r['debt_ratio']:.1%}", help=f"Limit: {DEBT_LIMIT:.0%}")
        col2.metric("Cash ratio", f"{r['cash_ratio']:.1%}", help=f"Limit: {CASH_LIMIT:.0%}")

st.divider()
st.caption(
    "For educational purposes only. Not financial or religious advice. "
    "Scholars differ on screening thresholds."
)