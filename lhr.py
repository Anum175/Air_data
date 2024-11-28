import requests
import time
import datetime

# Replace with your WAQI API key
WAQI_API_KEY = "d02a0242a98c960354443f1902ab8f9bfa38b239"


# Function to fetch AQI data for a specific time
def fetch_aqi_data(lat, lon):
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={WAQI_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: Unable to fetch data. Status Code: {response.status_code}, Response: {response.text}")


# Function to fetch hourly data for the last 2 months
def fetch_historical_aqi_hourly(lat, lon):
    end_time = datetime.datetime.utcnow()  # Current UTC time
    start_time = end_time - datetime.timedelta(days=60)  # Start time (60 days ago)

    current_time = start_time
    data = []

    while current_time <= end_time:
        try:
            print(f"Fetching data for {current_time}...")
            result = fetch_aqi_data(lat, lon)

            if result.get("status") == "ok":
                aqi_data = result.get("data", {})
                city = aqi_data.get("city", {}).get("name", "N/A")
                timestamp = aqi_data.get("time", {}).get("s", "N/A")
                aqi = aqi_data.get("aqi", "N/A")
                iaqi = aqi_data.get("iaqi", {})  # Individual pollutants

                # Format the pollutants data
                pollutants = {k: v.get("v", "N/A") for k, v in iaqi.items()}

                # Append hourly data
                data.append({
                    "city": city,
                    "timestamp": timestamp,
                    "aqi": aqi,
                    "pollutants": pollutants
                })
            else:
                print(f"Error: {result.get('data', 'Unknown error')}")
        except Exception as e:
            print(f"Error fetching data for {current_time}: {e}")

        # Increment by one hour
        current_time += datetime.timedelta(hours=1)
        time.sleep(1)  # To avoid hitting API rate limits

    # Save data to a file
    with open("lahore_aqi_hourly.txt", "w") as f:
        for entry in data:
            pollutants = "\n".join([f"{k}: {v}" for k, v in entry["pollutants"].items()])
            entry_text = f"""
City: {entry['city']}
Timestamp: {entry['timestamp']}
AQI: {entry['aqi']}
Pollutants:
{pollutants}
---------------------------------------------
"""
            f.write(entry_text)
    print(f"Saved {len(data)} hourly data points to lahore_aqi_hourly.txt")


# Fetch AQI data for Lahore (coordinates: 31.5497, 74.3436)
fetch_historical_aqi_hourly(31.5497, 74.3436)
