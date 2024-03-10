import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB Connection
mongo_uri = os.environ.get('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.weather_project

def get_user(username):
    """
    Retrieves a user document from the users collection based on the username.
    """
    return db.users.find_one({'username': username})

def create_user(username, email, password, location):
    """
    Creates a new user document in the users collection.
    """
    user = {
        'username': username,
        'email': email,
        'password': password,
        'location': location
    }
    
    result = db.users.insert_one(user)
    return result.inserted_id

def update_location(user_id, location):
    """
    Updates the location for a user in the users collection.
    """
    result = db.users.update_one(
        {'_id': user_id},
        {'$set': {'location': location}}
    )
    return result.modified_count