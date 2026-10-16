import yfinance as yf

HARAM_KEYWORDS = [
    "bank", "insurance", "credit services", "mortgage",
    "gambling", "casino", "tobacco",
    "brewer", "winer", "distiller",
]

DEBT_LIMIT = 0.30
CASH_LIMIT = 0.30


def get_data(ticker):
    """Pull the numbers we need from Yahoo Finance."""
    info = yf.Ticker(ticker).info
    return {
        "name": info.get("longName", ticker.upper()),
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


def analyze(ticker):
    """Screen a stock and return the results as a dictionary."""
    d = get_data(ticker)
    result = {
        "ticker": ticker.upper(),
        "name": d["name"],
        "industry": d["industry"],
        "debt_ratio": None,
        "cash_ratio": None,
        "status": None,
        "reasons": [],
    }

    if not business_check(d["industry"]):
        result["status"] = "FAIL"
        result["reasons"].append("Business activity is not permissible")
        return result

    if not d["market_cap"] or d["debt"] is None or d["cash"] is None:
        result["status"] = "UNKNOWN"
        result["reasons"].append("Missing financial data")
        return result

    result["debt_ratio"] = d["debt"] / d["market_cap"]
    result["cash_ratio"] = d["cash"] / d["market_cap"]

    if result["debt_ratio"] >= DEBT_LIMIT:
        result["reasons"].append(
            f"Debt ratio {result['debt_ratio']:.1%} is above the {DEBT_LIMIT:.0%} limit"
        )
    if result["cash_ratio"] >= CASH_LIMIT:
        result["reasons"].append(
            f"Cash ratio {result['cash_ratio']:.1%} is above the {CASH_LIMIT:.0%} limit"
        )

    result["status"] = "FAIL" if result["reasons"] else "PASS"
    return result

def suggest(query, limit=5):
    """Return up to `limit` (ticker, company name) pairs similar to the query."""
    try:
        results = yf.Search(query, max_results=10).quotes
    except Exception:
        return []

    options = []
    for q in results:
        if q.get("quoteType") != "EQUITY":
            continue
        symbol = q.get("symbol")
        name = q.get("shortname") or q.get("longname") or ""
        if symbol:
            options.append((symbol, name))
        if len(options) >= limit:
            break
    return options


# This part only runs when you run screener.py directly, not when the website uses it
if __name__ == "__main__":
    while True:
        ticker = input("\nEnter a ticker (or 'q' to quit): ")
        if ticker.lower() == "q":
            break
        print(analyze(ticker))