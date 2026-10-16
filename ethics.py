# Ethical flags for CREST.
# Rule: every flag must cite a named outside source with a link.

LAST_UPDATED = "October 2026"

UN_DATABASE_URL = "https://www.ohchr.org/en/documents/thematic-reports/ahrc6320-database-all-business-enterprises-involved-activities-detailed"

# US-listed companies in the UN Human Rights Office database (report A/HRC/63/20,
# September 2026, Annex I). Format: "TICKER": ("Name as listed by the UN", "Involvement type")
UN_SETTLEMENT_LIST = {
    "ABNB": ("Airbnb Inc.", "Contribution"),
    "BKNG": ("Booking Holdings Inc.", "Contribution"),
    "EXPE": ("Expedia Group Inc.", "Contribution"),
    "MSI": ("Motorola Solutions, Inc.", "Contribution"),
    "RMAX": ("Re/Max Holdings, Inc.", "Direct linkage"),
    "TRIP": ("TripAdvisor, Inc.", "Contribution"),
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
        name, involvement = UN_SETTLEMENT_LIST[ticker]
        flags.append({
            "category": "Settlement activity",
            "reason": (
                f"Listed as \"{name}\" in the UN Human Rights Office's 2026 database of businesses "
                f"involved in activities related to Israeli settlements in the occupied Palestinian "
                f"territory. UN-assessed involvement: {involvement.lower()}."
            ),
            "source": "UN Human Rights Office (OHCHR), report A/HRC/63/20",
            "url": UN_DATABASE_URL,
        })

    return flags