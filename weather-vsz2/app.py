import os
from flask import Flask, render_template, request, redirect, url_for, session
import json
import socket
import requests
from dotenv import load_dotenv
from utils.db import get_user, create_user, update_location
from utils.user import authenticate_user, register_user
from utils.weather import fetch_weather_data 


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
apiKey = 'e5ce83cd46a64d8283a44845240604'


def getCondition(conditionText):
    conditionText = conditionText.lower()
    if "rain with thunder" in conditionText or "thundery" in conditionText:
        return "⛈️"
    elif "rain" in conditionText or "drizzle" in conditionText:
        return "🌧️"
    elif "sun" in conditionText or "sunny" in conditionText or "clear" in conditionText:
        return "☀️"
    elif (
        "cloud" in conditionText
        or "cloudy" in conditionText
        or "overcast" in conditionText
    ):
        return "☁️"
    elif (
        "snow" in conditionText
        or "snowy" in conditionText
        or "sleet" in conditionText
        or "blizzard" in conditionText
    ):
        return "🌨️"
    elif "fog" in conditionText or "foggy" in conditionText or "mist" in conditionText:
        return "🌫️"
    elif "pellets" in conditionText:
        return "❄️"
    else:
        return conditionText


@app.route("/weather/<location>")
def weather(location):
    api = requests.get(
        f"http://api.weatherapi.com/v1/forecast.json?key={apiKey}&q={location}&days=8&aqi=no&alerts=no"
    )
    if api.status_code == 400:
        return redirect("/")
    data = json.loads(api.text)
    current = data["current"]
    location = data["location"]
    day1 = data["forecast"]["forecastday"][1]
    day2 = data["forecast"]["forecastday"][2]
    day3 = data["forecast"]["forecastday"][3]
    day4 = data["forecast"]["forecastday"][4]
    day5 = data["forecast"]["forecastday"][5]
    day6 = data["forecast"]["forecastday"][6]
    day7 = data["forecast"]["forecastday"][7]
    return render_template(
        "weather.html",
        currentTemp=current["temp_c"],
        locationName=location["name"],
        localTime=location["localtime"].split(" ")[1],
        locationRegion=location["region"],
        locationCountry=location["country"],
        currentCondition=getCondition(current["condition"]["text"]),
        data=[
            [
                getCondition(day1["day"]["condition"]["text"]),
                day1["day"]["avgtemp_c"],
                day1["day"]["maxtemp_c"],
                day1["day"]["mintemp_c"],
                day1["date"].replace("-", "/")[5:],
            ],
            [
                getCondition(day2["day"]["condition"]["text"]),
                day2["day"]["avgtemp_c"],
                day2["day"]["maxtemp_c"],
                day2["day"]["mintemp_c"],
                day2["date"].replace("-", "/")[5:],
            ],
            [
                getCondition(day3["day"]["condition"]["text"]),
                day3["day"]["avgtemp_c"],
                day3["day"]["maxtemp_c"],
                day3["day"]["mintemp_c"],
                day3["date"].replace("-", "/")[5:],
            ],
            [
                getCondition(day4["day"]["condition"]["text"]),
                day4["day"]["avgtemp_c"],
                day4["day"]["maxtemp_c"],
                day4["day"]["mintemp_c"],
                day4["date"].replace("-", "/")[5:],
            ],
            [
                getCondition(day5["day"]["condition"]["text"]),
                day5["day"]["avgtemp_c"],
                day5["day"]["maxtemp_c"],
                day5["day"]["mintemp_c"],
                day5["date"].replace("-", "/")[5:],
            ],
            [
                getCondition(day6["day"]["condition"]["text"]),
                day6["day"]["avgtemp_c"],
                day6["day"]["maxtemp_c"],
                day6["day"]["mintemp_c"],
                day6["date"].replace("-", "/")[5:],
            ],
            [
                getCondition(day7["day"]["condition"]["text"]),
                day7["day"]["avgtemp_c"],
                day7["day"]["maxtemp_c"],
                day7["day"]["mintemp_c"],
                day7["date"].replace("-", "/")[5:],
            ],
        ],
    )


#index page routes
@app.route('/')
def index():
    """
    Renders the index page.
    """
    return render_template('index.html')

@app.route("/index_home")
def index_home():
    """_summary_
        render page after login
    Returns:
        _type_: _description_
    """
    return render_template("index_login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles the user login process.

    GET request: Renders the login page.
    POST request: Authenticates the user and creates a session if successful.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = authenticate_user(username, password)
        if user:
            session['user_id'] = str(user['_id'])
            return redirect(url_for('index_home'))

        return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles the user registration process.

    GET request: Renders the registration page.
    POST request: Registers a new user and creates a session if successful.
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        location = {
            'city': request.form['city'],
            'country': request.form['country']
        }

        user_id = register_user(username, email, password, location)
        if user_id:
            session['user_id'] = str(user_id)
            return redirect(url_for('index'))

        return render_template('register.html', error='Registration failed')

    return render_template('register.html')

@app.route('/weather_chart')
def weather_chart():
    """ 
    render the home page after login, which contains the weather data
    """
    city = "London"
    country = "UK"
    weather_data = fetch_weather_data(city, country)  # Fetches current weather data for London
    return render_template('weather_chart.html', weather_data=weather_data)
