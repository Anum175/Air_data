import requests

# Replace with your WAQI API token
API_KEY = "d02a0242a98c960354443f1902ab8f9bfa38b239"

# Specify the location (City/Geo-coordinates)
city = "Lahore"  # Example: Lahore, Pakistan

# WAQI API URL
url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"

try:
    # Send request to WAQI API
    response = requests.get(url)
    data = response.json()

    if data.get("status") == "ok":
        aqi = data["data"]["aqi"]  # Air Quality Index
        pollutants = data["data"]["iaqi"]  # Individual pollutants
        print(f"Air Quality Index (AQI) for {city}: {aqi}")
        print("Pollutants:")
        for pollutant, value in pollutants.items():
            print(f"  {pollutant}: {value['v']}")
    else:
        print("Error:", data.get("data"))
except Exception as e:
    print(f"Error fetching data: {e}")
