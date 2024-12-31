from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Mail
import re
from .otp import send_email

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                session['email'] = email
                send_email(email)
                return redirect(url_for('auth.mfa'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greter than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 characters. ', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 character.', category='error')
        elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password1):
            flash('Password must include at least one special character.', category='error')
        elif not re.search(r"[0-9]", password1):
            flash('Password must include at least one numeric character.', category='error')
        elif not re.search(r"[A-Z]", password1):
            flash('Password must include at least one upper case letter.', category='error')
        elif not re.search(r"[a-z]", password1):
            flash('Password must include at least one lower case letter.', category='error')
        else:
            
            session['email'] = email
            session['first_name'] = first_name
            session['password'] = password1
            send_email(email)
            return redirect(url_for('auth.mfa'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/2fa', methods=['GET', 'POST'])
def mfa():
    if request.method == 'POST':
        user_otp = request.form.get('otp')
        if 'otp' not in session:
            flash('Session expired. Please request a new OTP', category='error')
            return redirect(url_for('auth.login'))
        if user_otp == session['otp']:
            if session.get("password"):
                new_user = User(email=session['email'], first_name=session['first_name'], password=generate_password_hash(password=session['password'], method='pbkdf2:sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created!', category='succcess')

                session.pop('otp', None)
                session.pop('email', None)
                session.pop('password', None)
                session.pop('first_name', None)
            else:
                user = User.query.filter_by(email=session['email']).first()
                login_user(user, remember=True)
                flash('OTP verified successfully!', category='success')

                session.pop('otp', None)
                session.pop('email', None)
            return redirect(url_for('views.home'))
        else:
            flash('Invalid OTP. Please try again', category='error')
        
    return render_template("2fa.html", user=current_user)

@auth.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if current_user:
        db.session.delete(current_user)
        db.session.commit()
        flash('Your account has been deleted.')
        return redirect(url_for('auth.logout'))
    else:
        flash('Error: Account not found.')
    return render_template("home.html", user=current_user)

@auth.route('/password-reset', methods=['GET', 'POST'])
def password_reset():
    if request.method == "POST":
        action = request.form.get('action')

        if action == 'send_otp':
            email = request.form.get('email')
            user = User.query.filter_by(email=email).first()
            if user:
                session['email'] = email
                send_email(email)
                return render_template("reset.html", user=current_user, email=email)
            else:
                flash('Please enter a valid email address', category='error')
        elif action == 'password_reset':
            user_otp = request.form.get('otp')
            if 'otp' not in session:
                flash('Session expired. Please request a new OTP', category='error')
                return redirect(url_for('auth.password_reset'))

            if user_otp == session['otp']:
                flash('OTP verified')
                return redirect(url_for('auth.new_password'))
            else:
                flash('Invalid OTP. Please try again.', category='error')
    return render_template("reset.html", user=current_user)

@auth.route('/new-password', methods=['GET', 'POST'])
def new_password():
    if request.method == 'POST':
        if 'email' not in session:
            flash('Session expired. Please request a new OTP.', category='error')
            return redirect(url_for('auth.password_reset'))

        email = session['email']
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 character.', category='error')
        elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password1):
            flash('Password must include at least one special character.', category='error')
        elif not re.search(r"[0-9]", password1):
            flash('Password must include at least one numeric character.', category='error')
        elif not re.search(r"[A-Z]", password1):
            flash('Password must include at least one upper case letter.', category='error')
        elif not re.search(r"[a-z]", password1):
            flash('Password must include at least one lower case letter.', category='error')
        else:
            user = User.query.filter_by(email=email).first()
            
            if user:
                user.password = generate_password_hash(password=password1, method='pbkdf2:sha256')
                db.session.commit
                flash('Password has been reset.', category='success')
                return redirect(url_for('auth.login'))
            else:
                flash('User not found.', category='error')
                return redirect(url_for('auth.password_reset'))

    return render_template('new_password.html', user=current_user)