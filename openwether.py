import requests

def get_weather_by_coordinates(latitude, longitude, api_key="7b3e66ddd06cc559f2ed56e829e9719a"):
    """Fetch current weather data by coordinates (latitude, longitude)"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    try:
        url = f"{base_url}?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return parse_weather_data(data)
        else:
            print(f"Error: Unable to fetch data (status code: {response.status_code})")
            return None
    except Exception as e:
        print(f"An error occurred while fetching weather data: {e}")
        return None

def parse_weather_data(data):
    try:
        main_data = data["main"]
        weather_data = data["weather"][0]

        weather_info = {
            "temperature": main_data["temp"],  
            "humidity": main_data["humidity"],  
            "pressure": main_data["pressure"], 
            "description": weather_data["description"],  
            "wind_speed": data["wind"]["speed"],  
            "clouds": data["clouds"]["all"],  
        }
        return weather_info
    except KeyError as e:
        print(f"Error parsing weather data: Missing key {e}")
        return None
