import os
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from utils.db import get_user, create_user, update_location
from utils.user import authenticate_user, register_user
from utils.weather import fetch_weather_data 


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

#index page routes
@app.route('/')
def index():
    """
    Renders the index page.
    """
    return render_template('index.html')

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
            return redirect(url_for('index'))

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
