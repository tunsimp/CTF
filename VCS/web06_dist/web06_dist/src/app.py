from flask import Flask, render_template, request, redirect, url_for, session
from database import *
from werkzeug.security import generate_password_hash, check_password_hash
import os
from uuid import uuid4
from requests import get

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.jinja_env.autoescape = False

# Initialize the database
init_db()


@app.route('/')
def home():
    if 'username' in session:
        user = get_user(session['username'])
        return redirect(url_for('profile', uid=user[5]))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)
        if user and check_password_hash(user[2], password):  # user[2] is the hashed password field
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password. Please try again.'

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)  # This clears the session
    return redirect(url_for('login'))  # Redirect the user to the login page


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return 'Passwords do not match.'

        existing_user = get_user(username)
        if existing_user:
            return 'Username already exists. Please choose a different one.'

        hashed_password = generate_password_hash(password)
        user_id = str(uuid4())
        insert_user(username, hashed_password, user_id)

        return redirect(url_for('login'))

    return render_template('register.html')


# This should be sufficient (right?)
def filter_xss(value):
    import re
    return re.sub(r'<[^>]*>', '', value)


@app.route('/profile/<uid>', methods=['GET'])
def profile(uid: str):
    user = get_user_id(uid)

    if 'username' not in session:
        return render_template('view_profiles.html', user=user)

    return render_template('profile.html', user=user)


@app.route('/profile/update', methods=['POST'])
def update_profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    email = filter_xss(request.form['email'])
    bio = filter_xss(request.form['bio'])
    update_user(username, email, bio)

    return redirect(url_for('home'))


# Working on it
@app.route('/report_profile/<reported_user_id>', methods=['GET', 'POST'])
def report_profile_view(reported_user_id):
    url=f"http://127.0.0.1:8082/visit/{reported_user_id}"
    get(url)
    return redirect("https://youtu.be/xvFZjo5PgG0")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1337, debug=True)
