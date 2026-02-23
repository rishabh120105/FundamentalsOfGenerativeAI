import os
import requests
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

# Country → currency
def get_currency(country):
    url = f"https://restcountries.com/v3.1/name/{country}"
    data = requests.get(url).json()

    currency_data = list(data[0]["currencies"].values())[0]
    code = list(data[0]["currencies"].keys())[0]

    return f"{currency_data['name']} ({code})"


# Exchange rate
def get_exchange_rate(currency_code):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{currency_code}"
    data = requests.get(url).json()

    rates = data["conversion_rates"]

    return {
        "USD": rates["USD"],
        "INR": rates["INR"],
        "GBP": rates["GBP"],
        "EUR": rates["EUR"],
    }


# Stock indices mapping
indices_map = {
    "Japan": ["^N225"],
    "India": ["^NSEI"],
    "United States": ["^GSPC"],
    "China": ["000001.SS"],
    "UK": ["^FTSE"],
    "South Korea": ["^KS11"]
}

def get_stock_indices(country):
    indices = indices_map.get(country, [])
    results = {}

    for idx in indices:
        ticker = yf.Ticker(idx)
        hist = ticker.history(period="1d")
        if not hist.empty:
            results[idx] = float(hist["Close"].iloc[-1])

    return results


# Google Maps HQ link
import requests

# Map stock exchange names
exchange_hq = {
    "Japan": "Tokyo Stock Exchange",
    "India": "Bombay Stock Exchange",
    "United States": "New York Stock Exchange",
    "China": "Shanghai Stock Exchange",
    "UK": "London Stock Exchange",
    "South Korea": "Korea Exchange"
}

def get_maps_pin(country):
    try:
        exchange = exchange_hq.get(country)

        if not exchange:
            return "Stock exchange not found."

        # OpenStreetMap geocoding API
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": exchange,
            "format": "json"
        }

        response = requests.get(
            url,
            params=params,
            headers={"User-Agent": "finance-agent"}
        ).json()

        if not response:
            return "Location not found."

        lat = response[0]["lat"]
        lon = response[0]["lon"]

        # Google Maps pin link
        return f"https://www.google.com/maps?q={lat},{lon}"

    except Exception as e:
        return f"Map error: {str(e)}"
