"""
Flask Registration Application Documentation

This Flask application provides a simple user registration system with the ability to specify swimming skills 
and connect with other users. It utilizes a JSON file to store user data.

"""

from flask import Flask, render_template, request
import uuid
import json
import os
import re

# Create Flask application
app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# File to store user data
user_data_file = 'user_data.json'

def load_user_data():
    """
    Load user data from the JSON file.

    Returns:
        dict: A dictionary containing user data.
    """
    if os.path.exists(user_data_file):
        with open(user_data_file, 'r') as file:
            users_data = json.load(file)
    else:
        users_data = {}
    return users_data

def save_user_data(users_data):
    """
    Save user data to the JSON file.

    Args:
        users_data (dict): A dictionary containing user data.
    """
    with open(user_data_file, 'w') as file:
        json.dump(users_data, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Render the index page.

    Returns:
        render_template: The rendered index.html template.
    """
    return render_template('index.html'), 200

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """
    Render the registration page.

    Returns:
        render_template: The rendered register.html template.
    """
    return render_template('register.html'), 200

def is_valid_username(username):
    """
    Check if the username is valid.

    Args:
        username (str): The username to be validated.

    Returns:
        bool: True if the username is valid, False otherwise.
    """
    if not (3 <= len(username) <= 8):
        return False

    return bool(re.match("^[a-zA-Z0-9_]+$", username))

@app.route("/get_form_data", methods=['POST'])
def get_form_data():
    """
    Handle form data submission for user registration.

    Returns:
        str: Registration success message or error message.
        int: HTTP status code.
    """
    nick = request.form['nick']
    is_swimmer = request.form.get('is_swimmer_hidden')
    friend_nick = request.form.get('canoe_friend', '').strip()

    if not is_valid_username(nick):
        return render_template('register.html', name_miss_msg="Jméno musí být dlouhé od 3 do 8 znaků a obsahovat pouze písmena, číslice a podtržítko."), 400

    if is_swimmer != "yes":
        return render_template('register.html', name_miss_msg="Zadejte své jméno a označte, že umíte plavat."), 400

    users_data = load_user_data()

    if nick in users_data:
        return render_template('register.html', name_miss_msg="Zadané jméno už existuje."), 400

    user_id = str(uuid.uuid4())

    user_data = {
        "id": user_id,
        "nick": nick,
        "is_swimmer": is_swimmer,
        "friend": None
    }

    if friend_nick and friend_nick in users_data:
        existing_user = users_data[friend_nick]
        existing_user_id = existing_user["id"]
        existing_user['friend'] = nick
        user_data['friend'] = friend_nick
        users_data[friend_nick] = existing_user
        users_data[nick] = user_data
    else:
        users_data[nick] = user_data

    save_user_data(users_data)

    return "Byli jste registrováni", 200

@app.route("/get_participants", methods=['GET'])
def get_participants():
    """
    Render a page displaying registered participants.

    Returns:
        render_template: The rendered participants.html template.
    """
    return render_template('participants.html', participants=load_user_data()), 200

if __name__ == '__main__':
    # Run the application
    app.run(host='0.0.0.0', port=8080, debug=True)
