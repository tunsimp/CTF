from flask import Blueprint, request, url_for,redirect, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, logout_user
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def signup_post():

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first() 

    if user: 
        return redirect(url_for('main.register'))

    new_user = User(username=username, password=generate_password_hash(password, method='scrypt'),role='regular_freak')

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('main.login'))

@auth.route('/login', methods=['POST'])
def login():
    
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('main.login')) 

    login_user(user)
    return redirect(url_for('main.index'))

@auth.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect('/')