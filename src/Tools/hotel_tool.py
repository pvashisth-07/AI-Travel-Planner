import requests
from langchain_core.tools import tool

BASE_URL = "https://data.xotelo.com/api"

def get_hotel_key(query: str) -> str:
    """Search for a hotel by name/city and return the first hotel_key."""
    response = requests.get(f"{BASE_URL}/search", params={"query": query})
    response.raise_for_status()
    data = response.json()

    hotels = data.get("result", {}).get("list", [])
    if not hotels:
        raise ValueError(f"No hotels found for query: {query}")
    
    return hotels[0]["hotel_key"], hotels[0]["name"]

def get_rates(hotel_key: str, chk_in: str, chk_out: str, currency: str = "INR", rooms: int = 1, adults: int = 1):
    """Fetch rates for a hotel using hotel_key and booking details."""
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

@tool
def fetch_hotel_rates(query: str, chk_in: str, chk_out: str, currency: str = "INR", rooms: int = 1, adults: int = 1):
    """
    Tool to fetch hotel rates by searching hotel name or city.
    
    Args:
        query: Hotel name or city (e.g., "Taj Palace New Delhi")
        chk_in: Check-in date in YYYY-MM-DD format
        chk_out: Check-out date in YYYY-MM-DD format
        currency: Currency code (default: INR)
        rooms: Number of rooms (default: 1)
        adults: Number of adults (default: 1)
    
    Returns:
        JSON response with hotel rates
    """
    hotel_key, hotel_name = get_hotel_key(query)
    rates = get_rates(hotel_key, chk_in, chk_out, currency, rooms, adults)
    
    return {
        "hotel_name": hotel_name,
        "hotel_key": hotel_key,
        "check_in": chk_in,
        "check_out": chk_out,
        "currency": currency,
        "rooms": rooms,
        "adults": adults,
        "rates": rates
    }
