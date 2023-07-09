import requests

link = "https://www.mapquestapi.com/geocoding/v1/address"

key = "4UViK4bt8z9JfhVrmtHAiHhqzkIN3y1n"

response = requests.get(
    "https://www.mapquestapi.com/geocoding/v1/address",
    params={"key": key, "location": "123 Main St."},
)
