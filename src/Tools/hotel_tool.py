import requests
from datetime import datetime

BASE_URL = "https://data.xotelo.com/api"
HOTEL_KEY = "YOUR_HOTEL_KEY"  # Replace with actual hotel_key

def get_rates(hotel_key, chk_in, chk_out, currency="INR", rooms=1, adults=1):
    params = {
        "hotel_key": hotel_key,
        "chk_in": chk_in,
        "chk_out": chk_out,
        "currency": currency,
        "rooms": rooms,
        "adults": adults
    }
    response = requests.get(f"{BASE_URL}/rates", params=params)
    response.raise_for_status()
    return response.json()