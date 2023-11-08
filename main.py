from flask import Flask, render_template, request
import uuid
import json
import os

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# File to store user data
user_data_file = 'user_data.json'

def load_user_data():
    if os.path.exists(user_data_file):
        with open(user_data_file, 'r') as file:
            users_data = json.load(file)
    else:
        users_data = {}
    return users_data

def save_user_data(users_data):
    with open(user_data_file, 'w') as file:
        json.dump(users_data, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html'), 200

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return render_template('register.html'), 200

@app.route("/get_form_data", methods=['POST'])
def get_form_data():
    nick = request.form['nick']
    is_swimmer = request.form.get('is_swimmer_hidden')  # Use get method to handle missing key gracefully
    friend_nick = request.form.get('canoe_friend', '').strip()

    if is_swimmer != "yes":
        return render_template('register.html', name_miss_msg="Zadejte své jméno a označte, že umíte plavat."), 400

    # Load existing user data from the JSON file
    users_data = load_user_data()

    # Generate a unique ID for the user
    user_id = str(uuid.uuid4())

    # Create a dictionary with user data
    user_data = {
        "id": user_id,
        "nick": nick,
        "is_swimmer": is_swimmer,
        "friend": None  # Initialize friend as None
    }

    # If friend's nick is provided, check if it exists in users_data
    if friend_nick and friend_nick in users_data:
        existing_user = users_data[friend_nick]
        existing_user_id = existing_user["id"]
        existing_user['friend'] = nick
        user_data['friend'] = friend_nick
        # Update users_data dictionary with existing user's updated data
        users_data[friend_nick] = existing_user
        users_data[nick] = user_data
    else:
        # Update users_data dictionary with new user data
        users_data[nick] = user_data

    # Save updated user data to the JSON file
    save_user_data(users_data)

    return "Registration successful!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
