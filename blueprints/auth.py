from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from forms import LoginForm, RegisterForm
from werkzeug.security import check_password_hash, generate_password_hash

from database_config import db
from models import User

login_manager = LoginManager()

auth = Blueprint("auth", __name__)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(username=form.username.data).first():
            flash('username already taken', 'danger')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(username=form.email.data).first():
            flash('email already taken', 'danger')
            return render_template('register.html', form=form)
        
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2')
        
        if form.role.data == "Admin" and current_user.role == "admin":
            role = "admin"
        else:
            role = "pax"
             
        new_user = User(name = form.name.data, surname = form.surname.data, username=form.username.data, email=form.email.data, password=hashed_password, numberOfId = form.numberOfId.data ,role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form, current_user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))
