import os
from flask import Flask, render_template, request, redirect, url_for, session
from utils.db import get_user, create_user, update_location

from utils.weather import update_weather_data
from utils.user import authenticate_user, register_user
from dotenv import load_dotenv

import os

load_dotenv()
api_key = os.environ.get('OPENWEATHER_API_KEY')
mongo_uri = os.environ.get('MONGO_URI')
secret_key = os.environ.get('SECRET_KEY')

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('weather'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
        if user:
            session['user_id'] = str(user['_id'])
            return redirect(url_for('weather'))
        
        return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
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
            return redirect(url_for('weather'))
        
        return render_template('register.html', error='Registration failed')
    
    return render_template('register.html')

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    user = get_user({'_id': user_id})
    if request.method == 'POST':
        location = {
            'city': request.form['city'],
            'country': request.form['country']
        }
        update_location(user_id, location)
        user['location'] = location
    update_weather_data(user_id, user['location'])
    # Fetch weather data from MongoDB and pass it to the template
    weather_data = db.weather_data.find({'user_id': user_id}).sort('timestamp', -1).limit(10)
    return render_template('weather.html', user=user, weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)