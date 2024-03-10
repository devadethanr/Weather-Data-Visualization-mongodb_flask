import os
from datetime import datetime
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB Connection
mongo_uri = os.environ.get('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.weather_project

# OpenWeatherMap API
api_key = os.environ.get('OPENWEATHER_API_KEY')
base_url = 'http://api.openweathermap.org/data/2.5/weather'

def fetch_weather_data(city, country):
    """
    Fetches weather data from the OpenWeatherMap API for a given city and country.
    """
    params = {
        'q': f'{city},{country}',
        'appid': api_key,
        'units': 'metric'
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather_data = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'weather_description': data['weather'][0]['description']
        }
        return weather_data
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def update_weather_data(user_id, location):
    """
    Fetches weather data for the given location and updates the weather_data collection in MongoDB.
    """
    weather_data = fetch_weather_data(location['city'], location['country'])
    
    if weather_data:
        data = {
            'user_id': user_id,
            'timestamp': datetime.utcnow(),
            'data': weather_data
        }
        
        db.weather_data.insert_one(data)
        print(f"Weather data updated for user {user_id}")