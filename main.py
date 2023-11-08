from flask import Flask, render_template, request, jsonify
import json
import os
import uuid

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# Dictionary to store user data
users_data = {}

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
    friend_nick = request.form.get('canoe_friend')

    if is_swimmer != "yes":
        return render_template('register.html', name_miss_msg="Zadejte své jméno a označte, že umíte plavat."), 400

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
    if friend_nick:
        if friend_nick in users_data:
            user_data["friend"] = friend_nick
            users_data[friend_nick]["friend"] = nick
        else:
            return render_template('register.html', name_miss_msg="Zadaná přezdívka kamaráda neexistuje."), 400

    # Update users_data dictionary with new user data
    users_data[user_id] = user_data

    return "Registration successful!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
