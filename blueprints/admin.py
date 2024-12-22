from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from forms import LoginForm, RegisterForm, SearchForm, ReservationForm1, ReservationForm2
from werkzeug.security import check_password_hash, generate_password_hash
from scraping import is_reservation_possible, get_iata_code, airlines_details, airline_code
from datetime import datetime
from sqlalchemy import func
from database_config import db

from decorators import role_required
from models import User, Reservation, Flight

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/panel')
@role_required('admin')
def panel():

    return render_template('admin/panel.html')

@admin.route('/users')
@role_required('admin')
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/flights')
@role_required('admin')
def flights():
    flights = Flight.query.all()
    return render_template('admin/flights.html', flights=flights)

@admin.route('/flight/<number>')
@role_required('admin')
def flight(number):
    flight = Flight.query.filter_by(flightNumber=number).first()
    reservations = Reservation.query.filter_by(flightNumber=number)
    print(reservations)

    reservations = [
        {
            'seat': reservation.seat,
            'passanger': User.query.filter_by(id=reservation.user_id).first(),
            'luggage': reservation.luggage,
            'insurance': reservation.insurance
        }
        for reservation in reservations
    ]
    return render_template('admin/flight.html', flight=flight, reservations=reservations)


@admin.route('/delete-flight/<number>')
@role_required('admin')
def delete_flight(number):
    flight = Flight.query.filter_by(flightNumber=number).first()
    reservations = Reservation.query.filter_by(flightNumber=number).all()
    if reservations:
        for reservation in reservations:
            print(reservation)
            db.session.delete(reservation)
    db.session.commit()
    db.session.delete(flight)
    db.session.commit()
    return redirect(url_for('admin.panel'))