import requests
from langchain.tools import tool
import json

@tool
def get_current_weather(city: str) -> str:
    """Fetches the current weather conditions for a specified city using Open-Meteo.
    This tool requires a city name as input and will attempt to find its latitude and longitude
    before fetching weather data.
    Useful for knowing if it's a good time for outdoor activities like fireworks.
    Returns temperature in Celsius, weather description, and wind speed.
    """
    # Step 1: Geocoding - Convert city name to latitude and longitude
    # Open-Meteo doesn't directly support city names, so we use OpenStreetMap Nominatim for geocoding.
    nominatim_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    headers = {
        'User-Agent': 'AlfredGalaAgent/1.0 (https://yourwebsite.com or your_email@example.com)'
    } # Nominatim requires a User-Agent header

    try:
        geo_response = requests.get(nominatim_url, headers=headers)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data:
            return f"Could not find coordinates for city '{city}'. Please ensure it's a valid city name."

        latitude = geo_data[0]['lat']
        longitude = geo_data[0]['lon']
        display_name = geo_data[0]['display_name'] # More accurate city name

    except requests.exceptions.RequestException as e:
        return f"Error during geocoding for {city}: {e}"
    except Exception as e:
        return f"An unexpected error occurred during geocoding: {e}"

    # Step 2: Fetch weather data using latitude and longitude from Open-Meteo
    open_meteo_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&current_weather=true&temperature_unit=celsius&windspeed_unit=ms"
    )

    try:
        weather_response = requests.get(open_meteo_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        if "current_weather" in weather_data:
            current = weather_data["current_weather"]
            temperature = current["temperature"]
            wind_speed = current["windspeed"]
            weather_code = current["weathercode"]

            # Open-Meteo uses WMO Weather interpretation codes
            # You might want a more comprehensive mapping, but this is a start.
            weather_description = {
                0: "Clear sky",
                1: "Mainly clear",
                2: "Partly cloudy",
                3: "Overcast",
                45: "Fog",
                48: "Depositing rime fog",
                51: "Drizzle: Light",
                53: "Drizzle: Moderate",
                55: "Drizzle: Dense intensity",
                56: "Freezing Drizzle: Light",
                57: "Freezing Drizzle: Dense intensity",
                61: "Rain: Slight",
                63: "Rain: Moderate",
                65: "Rain: Heavy intensity",
                66: "Freezing Rain: Light",
                67: "Freezing Rain: Heavy intensity",
                71: "Snow fall: Slight",
                73: "Snow fall: Moderate",
                75: "Snow fall: Heavy intensity",
                77: "Snow grains",
                80: "Rain showers: Slight",
                81: "Rain showers: Moderate",
                82: "Rain showers: Violent",
                85: "Snow showers: Slight",
                86: "Snow showers: Heavy",
                95: "Thunderstorm: Slight or moderate",
                96: "Thunderstorm with slight hail",
                99: "Thunderstorm with heavy hail",
            }.get(weather_code, "Unknown weather condition")

            return (
                f"Current weather in {display_name} (Lat: {latitude}, Lon: {longitude}):\n"
                f"Temperature: {temperature}°C\n"
                f"Description: {weather_description}\n"
                f"Wind Speed: {wind_speed} m/s"
            )
        else:
            return f"No current weather data available for {display_name}."

    except requests.exceptions.RequestException as e:
        return f"Error fetching weather for {display_name}: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    # Test the weather tool
    print("--- Testing Weather Tool with Open-Meteo ---")
    print(get_current_weather("Paris"))
    print("\n------------------------------------------\n")
    print(get_current_weather("New York"))
    print("\n------------------------------------------\n")
    print(get_current_weather("Tokyo"))
    print("\n------------------------------------------\n")
    print(get_current_weather("A_Non_Existent_City_XYZ")) # Test for invalid city