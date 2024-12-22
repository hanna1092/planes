from flask_bootstrap import Bootstrap
from flask import Flask, render_template, redirect, url_for, flash, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from forms import LoginForm, RegisterForm, SearchForm, ReservationForm1, ReservationForm2
from scraping import is_reservation_possible, get_iata_code, airlines_details, airline_code, get_airport_name_by_iata
from database_config import db
from config import Config
from models import User

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(Config)


# Rejestracja blueprintów
from blueprints.auth import auth, login_manager
from blueprints.reservation import reservation
from blueprints.flights import flights
from blueprints.admin import admin
app.register_blueprint(auth)  
app.register_blueprint(reservation)
app.register_blueprint(flights)
app.register_blueprint(admin)

# Inicjalizacja bazy danych
db.init_app(app)

# Konfiguracja Flask-Login
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Ustawienie widoku logowania

# Funkcja loadera użytkownika
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.errorhandler(404)
def not_found(error):

    return make_response(jsonify({'error': 'Nie znaleziono'}), 404) 

@app.route('/')
def index():
    form=SearchForm()
    return render_template('index.html', form=form, current_user=current_user, len=len, get_iata_code=get_iata_code, list=list)

@app.route('/fleet')
def fleet():
    return render_template('fleet.html')

@app.route('/baggage')
def baggage():
    return render_template('baggage.html')

@app.route('/pets')
def pets():
    return render_template('pets.html')

@app.route('/meals')
def meals():
    return render_template('meals.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy_policy.html')


@app.route('/oslo')
def oslo():
    form=SearchForm()
    return render_template('oslo.html', form=form, current_user=current_user, len=len, get_iata_code=get_iata_code, list=list)

@app.route('/majorca')
def majorca():
    form=SearchForm()
    return render_template('majorca.html', form=form, current_user=current_user, len=len, get_iata_code=get_iata_code, list=list)

@app.route('/paris')
def paris():
    form=SearchForm()
    return render_template('paris.html', form=form, current_user=current_user, len=len, get_iata_code=get_iata_code, list=list)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
