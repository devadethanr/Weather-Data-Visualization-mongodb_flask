import os
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv

from utils.db import get_user, create_user, update_location
from utils.weather import update_weather_data

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

#index page routes
@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)