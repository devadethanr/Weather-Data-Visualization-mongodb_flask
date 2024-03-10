from utils.db import db, get_user, create_user
from bson.objectid import ObjectId
from werkzeug.security import check_password_hash, generate_password_hash

def authenticate_user(username, password):
    """
    Authenticates a user by checking the provided username and password against the database.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        dict: The user document if authentication is successful, otherwise None.
    """
    user = get_user(username)
    if user and check_password_hash(user['password'], password):
        return user
    return None

def register_user(username, email, password, location):
    """
    Registers a new user in the database.

    Args:
        username (str): The username for the new user.
        email (str): The email address for the new user.
        password (str): The password for the new user.
        location (dict): The location information for the new user.

    Returns:
        str or None: The ID of the newly created user if registration is successful, otherwise None.
    """
    # Check if the username or email already exists
    existing_user = db.users.find_one({'$or': [{'username': username}, {'email': email}]})
    if existing_user:
        return None

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create the new user document
    user = {
        'username': username,
        'email': email,
        'password': hashed_password,
        'location': location
    }

    # Insert the new user document into the database
    result = db.users.insert_one(user)
    return str(result.inserted_id)
