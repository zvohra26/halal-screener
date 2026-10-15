import yfinance as yf

# Industries that fail the business check (matched as keywords in Yahoo's industry name)
HARAM_KEYWORDS = [
    "bank", "insurance", "credit services", "mortgage",
    "gambling", "casino", "tobacco",
    "brewer", "winer", "distiller",
]

DEBT_LIMIT = 0.30   # 30%
CASH_LIMIT = 0.30   # 30%


def get_data(ticker):
    """Pull the numbers we need from Yahoo Finance."""
    info = yf.Ticker(ticker).info
    return {
        "name": info.get("longName", ticker),
        "industry": info.get("industry", "Unknown"),
        "market_cap": info.get("marketCap"),
        "debt": info.get("totalDebt"),
        "cash": info.get("totalCash"),
    }


def business_check(industry):
    """Return True if the industry is allowed."""
    industry = industry.lower()
    for word in HARAM_KEYWORDS:
        if word in industry:
            return False
    return True


def screen(ticker):
    d = get_data(ticker)

    print(f"\n{d['name']} ({ticker.upper()})")
    print(f"Industry: {d['industry']}")

    if not business_check(d["industry"]):
        print("Result: FAIL (business activity not permissible)")
        return

    if not d["market_cap"] or d["debt"] is None or d["cash"] is None:
        print("Result: UNKNOWN (missing financial data)")
        return

    debt_ratio = d["debt"] / d["market_cap"]
    cash_ratio = d["cash"] / d["market_cap"]

    print(f"Debt ratio: {debt_ratio:.1%}  (limit {DEBT_LIMIT:.0%})")
    print(f"Cash ratio: {cash_ratio:.1%}  (limit {CASH_LIMIT:.0%})")

    if debt_ratio < DEBT_LIMIT and cash_ratio < CASH_LIMIT:
        print("Result: PASS")
    else:
        print("Result: FAIL (financial ratios too high)")


for t in ["F", "T", "TSLA", "NVDA", "KO"]:
    screen(t)