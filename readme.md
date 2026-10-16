# CREST

**Compliance Review of Equities against Shariah Thresholds**

A web app that checks whether a stock is Shariah-compliant using live financial data, and flags ethical concerns from cited outside sources.

**Live app:** https://crest-screener.streamlit.app

## What it does

Enter any ticker or company name. CREST returns:

- **Pass / Fail / Not enough data** based on Shariah screening rules
- **The specific reasons** a stock fails, and the key ratios behind the result
- **Ethical flags** for stocks that pass Shariah screening but raise other concerns, each with a linked source
- **"Did you mean" suggestions** for misspelled tickers, plus search by company name
- **Recently screened** list to quickly revisit stocks

## How the Shariah screening works

A stock must pass two checks:

**1. Business activity.** Companies whose core business is impermissible (conventional banking, insurance, alcohol, gambling, tobacco) fail automatically.

**2. Financial ratios**, based on AAOIFI Shariah Standard No. 21:

| Ratio | Formula | Limit |
|---|---|---|
| Debt ratio | Total debt ÷ market cap | < 30% |
| Cash ratio | Cash and short-term investments ÷ market cap | < 30% |

For example, Ford fails with a debt ratio above 300%, largely because its financing arm borrows heavily to issue interest-bearing car loans.

## Ethical flags

A stock can be Shariah-permissible and still raise ethical concerns for Muslim investors. CREST keeps this separate from the Shariah result: flags never change the pass/fail verdict, and every flag cites a named outside source so users can judge for themselves.

| Flag | Source |
|---|---|
| Weapons & defense | Yahoo Finance industry classification (Aerospace & Defense) |
| Settlement activity | UN Human Rights Office database of businesses involved in Israeli settlements (report A/HRC/63/20, September 2026) |

For example, Airbnb passes the Shariah ratios but is flagged because it appears in the UN database.

## Data sources

- **Market data:** Yahoo Finance, via the open-source `yfinance` library, pulled live and cached for one hour
- **Screening thresholds:** AAOIFI (Accounting and Auditing Organization for Islamic Financial Institutions)
- **Ethical flags:** see table above

## Tech stack

- **Python:** screening logic, ethical flags, ticker search
- **yfinance:** live financial data and fuzzy ticker search
- **Streamlit:** web interface, caching, and hosting
- **HTML/CSS/SVG:** custom styling, result cards, logo, and background pattern

## Limitations

- **Cash ratio is approximate.** Yahoo's cash figure includes all cash and short-term investments, not only interest-bearing holdings.
- **Impure income isn't screened yet.** Free data doesn't break down revenue from impermissible sources, so the common 5% income test is not applied.
- **Business check uses industry keywords**, which can miss companies with significant impermissible revenue outside their main industry.
- **Uses current market cap.** Some standards use a 24–36 month average to reduce volatility.
- **The defense flag is industry-based**, so it can include companies that mainly make commercial aerospace parts.
- **The UN settlement list is a manually maintained snapshot**, refreshed when the UN publishes its annual update. Only US-listed companies are included.
- CREST is not certified by AAOIFI or any Shariah board. It is educational and is not financial or religious advice.

## Future improvements

- Average market cap over time instead of a single-day value
- Impure income screening and a dividend purification calculator
- Portfolio screening: check all holdings at once
- More ethical flag categories, each with a cited source

## Run it locally

```bash
git clone https://github.com/zvohra26/halal-screener.git
cd halal-screener
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```