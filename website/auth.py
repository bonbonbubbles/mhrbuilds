from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('view_gear.overview'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_data = db.users.find_one({'username': username})
        if user_data:
            email = user_data['email']

        if user_data['email'] and check_password_hash(user_data['password'], password):
            flash('You were successfully logged in', category='success')
            session['email'] = email
            return redirect(url_for('view_gear.overview'))
        else:
            flash('Login failed. Please check your login details and try again.', category='error')
            return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        email_check = db.users.find_one({'email': email})
        username_check = db.users.find_one({'username': username})
        if email_check:
            flash('There is already an account under this email', category='error')
        elif username_check:
            flash('There is already an account under this username', category='error')
        else:
            if len(email) < 4:
                flash('Email is too short', category='error')
            elif password1 != password2:
                flash('Passwords do not match', category='error')
            elif len(password1) < 8:
                flash('Password is too short', category='error')
            else:
                # add user to database
                db.users.insert_one({'email': email, 'username': username, 'password': generate_password_hash(password1)})
                session['email'] = email
                return redirect(url_for('view_gear.overview'))

    return render_template("sign_up.html")