from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from forms import FlightForm, EditFlightForm
from models import Flight, Reservation
from database_config import db

flights = Blueprint('flights', __name__)

@flights.route('/flights', methods=['GET'])
@login_required
def list_flights():
    flights = Flight.query.all()
    return render_template('flights/list_flights.html', flights=flights)

@flights.route('/flights/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_flight(id):
    flight = Flight.query.get_or_404(id)
    form = EditFlightForm(obj=flight)
    if form.validate_on_submit():
        flight.fromAirport = form.fromAirport.data
        flight.destinationAirport = form.destinationAirport.data
        flight.fromCode = form.fromCode.data
        flight.destinationCode = form.destinationCode.data
        flight.airlineCode = form.airlineCode.data
        flight.flightNumber = form.flightNumber.data
        flight.delay = form.delay.data == 'True'
        db.session.commit()
        flash('Flight updated successfully!', 'success')
        return redirect(url_for('flights.list_flights'))
    return render_template('flights/edit_flight.html', form=form, flight=flight)

@flights.route('/flights/delete/<int:id>', methods=['POST'])
@login_required
def delete_flight(id):
    flight = Flight.query.get_or_404(id)

    reservations_to_delete = Reservation.query.filter_by(flightNumber=flight.flightNumber).all()
    for reservation in reservations_to_delete:
        db.session.delete(reservation)

    db.session.delete(flight)
    db.session.commit()
    flash('Flight and associated reservations deleted successfully!', 'success')
    return redirect(url_for('flights.list_flights'))
