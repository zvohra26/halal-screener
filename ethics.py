# Ethical flags for CREST.
# Rule: every flag must cite a named outside source with a link.

LAST_UPDATED = "October 2026"

UN_DATABASE_URL = "https://www.ohchr.org/en/press-releases/2026/09/un-human-rights-updates-list-companies-involved-israeli-settlements-occupied"

# US-listed companies in the UN Human Rights Office database of businesses
# involved in activities in Israeli settlements. Only add a company after
# confirming it in the official list. Format: "TICKER": "Name as listed by the UN"
UN_SETTLEMENT_LIST = {
}


def get_flags(ticker, industry):
    """Return a list of ethical flags for a stock. Each flag cites its source."""
    flags = []
    ticker = ticker.upper()

    if "defense" in industry.lower():
        flags.append({
            "category": "Weapons & defense",
            "reason": "Classified in the Aerospace & Defense industry, which includes manufacturers of military aircraft and weapons systems.",
            "source": "Yahoo Finance company profile",
            "url": f"https://finance.yahoo.com/quote/{ticker}/profile",
        })

    if ticker in UN_SETTLEMENT_LIST:
        flags.append({
            "category": "Settlement activity",
            "reason": "Listed in the UN Human Rights Office database of businesses involved in activities in Israeli settlements in the occupied Palestinian territory.",
            "source": "UN Human Rights Office (OHCHR)",
            "url": UN_DATABASE_URL,
        })

    return flags