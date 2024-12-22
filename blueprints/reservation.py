from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from forms import LoginForm, RegisterForm, SearchForm, ReservationForm1, ReservationForm2
from werkzeug.security import check_password_hash, generate_password_hash
from scraping import is_reservation_possible, get_iata_code, airlines_details, airline_code, get_airport_name_by_iata
from datetime import datetime
from sqlalchemy import func

from database_config import db
from models import User, Reservation, CreateSeats, Flight

reservation = Blueprint("reservation", __name__)

@reservation.route('/', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if request.method == 'GET':
        return render_template('index.html', form=form, current_user=current_user, len=len, get_iata_code=get_iata_code, list=list)
    
    if request.method == 'POST' and form.validate_on_submit():
        base_code = get_iata_code(form.base_.data)
        to_code = get_iata_code(form.to.data)
        time_of_departure = form.departure.data
        return_departure = form.return_departure.data
        back = form.back.data

        if not base_code and to_code: # no airports found
            flash("Sorry, we are not flying from/to this airport. Please insert another one.")
            return redirect(url_for('reservation.search'))

        if not (len(base_code) == 1 and len(to_code) == 1): # more than one
            return render_template('index.html', form=form, current_user=current_user, base_airports=base_code, to_airports=to_code, len=len, get_iata_code=get_iata_code, list=list)

        
        base_code = list(base_code.values())[0]
        to_code = list(to_code.values())[0]

        if not is_reservation_possible(base_code, to_code):
            flash("Sorry, there are seats on flights between those airports")
            return False
        
        airlines = airlines_details(base_code, to_code)


        if airlines == None:
            flash("Sorry. We don't fly that direction")
            return render_template('index.html', form=form, current_user=current_user, len=len, get_iata_code=get_iata_code, list=list)
        
        return render_template('select_airline.html', 
                                airlines=airlines,
                                base_code=base_code,
                                to_code=to_code, 
                                fromAirport=form.base_.data, 
                                destinationAirport=form.to.data, 
                                current_user=current_user, 
                                airline_code=airline_code,  
                                departure=time_of_departure, 
                                return_departure=return_departure,
                                back=back)

        
        
    #flash("Wrong input data!")
    return redirect(url_for('reservation.search'))

@reservation.route('/select_airline/<string:base_code>/<string:to_code>/<string:airline_code>/<string:fromAirport>/<string:destinationAirport>/<path:departure>/<path:return_departure>/<string:back>', methods=['GET'])
def select_airline(airline_code, base_code, to_code, fromAirport, destinationAirport, departure, return_departure, back):
    return redirect(url_for('reservation.make_reservation',
                            fromAirport=fromAirport,
                            destinationAirport=destinationAirport, 
                            fromCode=base_code, 
                            destinationCode=to_code,
                            airlineCode=airline_code, 
                            departure=departure, 
                            return_departure=return_departure,
                            back=back))

@reservation.route('/reservation/via', methods=['GET', 'POST'])
def make_reservation_via():
    via = request.args.get('via')
    return render_template('via.html', via=via)

@reservation.route('/reservation/data', methods=['GET', 'POST'])
@login_required
def make_reservation():
    form = ReservationForm1()
    fromCode = request.args.get('fromCode')
    destinationCode = request.args.get('destinationCode')
    airline_code = request.args.get('airlineCode')
    departure = request.args.get('departure')
    return_departure = request.args.get('return_departure')
    back = request.args.get('back')
    try:
        departure = datetime.strptime(departure, "%Y-%m-%d %H:%M:%S")
    except:
        departure = datetime.strptime(departure, "%Y-%m-%d")

    if request.method == 'GET':
        return render_template('reservation_data.html', form=form, current_user=current_user)
    if request.method == 'POST' and form.validate_on_submit():
        fromAirport = request.args.get('fromAirport')
        destinationAirport = request.args.get('destinationAirport')
        seats = CreateSeats()
        flight = Flight.query.filter_by(fromCode=fromCode, destinationCode=destinationCode, airlineCode=airline_code).first()
        if not flight:
            return render_template('seats.html', 
                                   seats=seats,
                                   taken_seats=[],  # Brak zarezerwowanych miejsc dla nowego lotu
                                   fromAirport=fromAirport,
                                   destinationAirport=destinationAirport, 
                                   fromCode=fromCode, 
                                   destinationCode=destinationCode,
                                   airlineCode=airline_code, 
                                   departure=departure, 
                                   return_departure=return_departure,
                                   back=back)
        else:
            taken_seats = flight.taken_seats.split(',') if flight.taken_seats else []
            return render_template('seats.html', 
                                   seats=seats,
                                   taken_seats=taken_seats,
                                   fromAirport=fromAirport,
                                   destinationAirport=destinationAirport, 
                                   fromCode=fromCode, 
                                   destinationCode=destinationCode,
                                   airlineCode=airline_code, 
                                   departure=departure, 
                                   return_departure=return_departure,
                                   back=back)

@reservation.route('/reservation/seat-<string:seat>', methods=['GET', 'POST'])
def make_reservation2(seat):
    fromAirport = request.args.get('fromAirport')
    destinationAirport = request.args.get('destinationAirport')
    fromCode = request.args.get('fromCode')
    destinationCode = request.args.get('destinationCode')
    airline_code = request.args.get('airlineCode')
    departure = request.args.get('departure')
    return_departure = request.args.get('return_departure')
    back = request.args.get('back')

    flight = Flight.query.filter_by(fromCode=fromCode, destinationCode=destinationCode, airlineCode=airline_code).filter(Flight.timeOfDeparture == departure).first()
    if not flight:
        return redirect(url_for('reservation.confirm_reservation',
                                fromAirport=fromAirport,
                                destinationAirport=destinationAirport, 
                                fromCode=fromCode, 
                                destinationCode=destinationCode,
                                seat=seat, 
                                airline_code=airline_code, 
                                departure=departure, 
                                return_departure=return_departure,
                                back=back))
    else:
        taken_seats = flight.taken_seats.split(',') if flight.taken_seats else []
        print(taken_seats)
        if seat in taken_seats:
            seats = CreateSeats()
            return render_template('seats.html', 
                                   seats=seats,
                                   taken_seats=taken_seats,
                                   fromAirport=fromAirport,
                                   destinationAirport=destinationAirport, 
                                   fromCode=fromCode, 
                                   destinationCode=destinationCode,
                                   airlineCode=airline_code, 
                                   departure=departure, 
                                   return_departure=return_departure,
                                   back=back)
        else:
            return redirect(url_for('reservation.confirm_reservation',
                                    fromAirport=fromAirport,
                                    destinationAirport=destinationAirport, 
                                    fromCode=fromCode, 
                                    destinationCode=destinationCode,
                                    seat=seat, 
                                    airline_code=airline_code, 
                                    departure=departure, 
                                    return_departure=return_departure,
                                    back=back))

@reservation.route('/reservation/confirm', methods=['GET', 'POST'])
@login_required
def confirm_reservation():
    form = ReservationForm2()
    fromCode = request.args.get('fromCode')
    destinationCode = request.args.get('destinationCode')
    fromAirport = get_airport_name_by_iata(fromCode)
    destinationAirport = get_airport_name_by_iata(destinationCode)
    airline_code = request.args.get('airline_code')
    seat = request.args.get('seat')
    departure_str = request.args.get('departure')
    return_departure = request.args.get('return_departure')
    back = request.args.get('back')
    max_flight_id = db.session.query(func.max(Flight.id)).scalar()
    if not max_flight_id:
        max_flight_id = 0
    

    try:
        departure = datetime.strptime(departure_str, "%Y-%m-%d %H:%M:%S")
    except:
        departure = datetime.strptime(departure_str, "%Y-%m-%d")

    if request.method == 'GET':
        return render_template('reservation2.html', form=form, current_user=current_user)
    
    if request.method == 'POST' and form.validate_on_submit():
        flight = Flight.query.filter_by(fromCode=fromCode, destinationCode=destinationCode, airlineCode=airline_code).filter(Flight.timeOfDeparture == departure).first()

        try:
            id = int(back)
            reservation = Reservation.query.filter_by(id=id).first()
            reservation.seat = seat
            reservation.luggage = form.luggage.data
            reservation.insurance = form.insurance.data
            flight.taken_seats = f"{flight.taken_seats},{seat}" if flight.taken_seats else seat
            db.session.commit()
            return redirect(url_for('reservation.my_reservations')) 

        except ValueError:
            print()

        first_flight = Flight.query.filter_by(flightNumber=back).first()
        if first_flight is None:
            if not flight:
                flight = Flight(
                    fromAirport=fromAirport,
                    destinationAirport=destinationAirport,
                    fromCode=fromCode,
                    destinationCode=destinationCode,
                    airlineCode=airline_code,
                    flightNumber=f"{airline_code}{max_flight_id + 1}",
                    timeOfDeparture=departure,
                    taken_seats=seat,  # Dodanie pierwszego zajętego miejsca
                    reservations=[]
                )
                db.session.add(flight)
                db.session.flush()
            else:
                flight.taken_seats = f"{flight.taken_seats},{seat}" if flight.taken_seats else seat
            
            new_reservation = Reservation(
                user_id=current_user.id,
                fromAirport=fromAirport,
                destinationAirport=destinationAirport,
                fromCode=fromCode,
                destinationCode=destinationCode,
                seat=seat,
                airlineCode=airline_code,
                flight_id=flight.id,
                flightNumber=flight.flightNumber,
                timeOfDeparture=flight.timeOfDeparture,
                luggage=form.luggage.data,
                insurance=form.insurance.data
            )

            try:
                db.session.add(new_reservation)
                flight.reservations.append(new_reservation)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(f'Error: {e}', 'danger')

            if back == "Return":
                seats = CreateSeats()
                return render_template('seats.html', 
                                       seats=seats,
                                       fromAirport=destinationAirport,
                                       destinationAirport=fromAirport, 
                                       fromCode=destinationCode, 
                                       destinationCode=fromCode,
                                       airlineCode=airline_code, 
                                       departure=return_departure, 
                                       return_departure=return_departure,
                                       back=flight.flightNumber)
            else: 
                flash('Reservation created successfully!', 'success')
                return redirect(url_for('reservation.my_reservations')) 
        else:
            if not flight:
                flight = Flight(
                    fromAirport=fromAirport,
                    destinationAirport=destinationAirport,
                    fromCode=fromCode,
                    destinationCode=destinationCode,
                    airlineCode=airline_code,
                    flightNumber=f"{airline_code}{max_flight_id + 1}",
                    timeOfDeparture=departure,
                    reservations=[]
                )
                db.session.add(flight)
                db.session.flush()
            else:
                flight.taken_seats = f"{flight.taken_seats},{seat}" if flight.taken_seats else seat
            
            new_reservation = Reservation(
                user_id=current_user.id,
                fromAirport=fromAirport,
                destinationAirport=destinationAirport,
                fromCode=fromCode,
                destinationCode=destinationCode,
                seat=seat,
                airlineCode=airline_code,
                flight_id=flight.id,
                flightNumber=flight.flightNumber,
                timeOfDeparture=flight.timeOfDeparture,
                luggage=form.luggage.data,
                insurance=form.insurance.data
            )

            try:
                db.session.add(new_reservation)
                return_flight = Reservation.query.filter_by(flightNumber=flight.flightNumber).first()
                first_flight.return_flight = return_flight
                first_flight.return_flight_id = return_flight.id
                flight.reservations.append(new_reservation)
                db.session.commit()
                flash('Reservation created successfully!', 'success')
                return redirect(url_for('reservation.my_reservations')) 
            except Exception as e:
                db.session.rollback()
                flash(f'Error: {e}', 'danger')

    return render_template('reservation2.html', form=form, current_user=current_user)

@reservation.route('/reservation/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_reservation(id):
    reservation = Reservation.query.filter_by(user_id=current_user.id, id=id).first()
    if not reservation:
        flash('Reservation not found.')
        return redirect(url_for('reservation.my_reservations'))

    flight = Flight.query.filter_by(flightNumber = reservation.flightNumber).first()
    seats = CreateSeats()
    taken_seats = []

    if flight and flight.taken_seats:
        taken_seats = flight.taken_seats.split(',')
        if reservation.seat in taken_seats:
            flight.taken_seats = ','.join(taken_seats)
            db.session.commit()

    taken_seats = flight.taken_seats.split(',') if flight and flight.taken_seats else []

    if request.method == 'POST':
        new_seat = request.form.get('seat')
        if new_seat != reservation.seat:
            if reservation.seat in taken_seats:
                taken_seats.remove(reservation.seat)
                flight.taken_seats = ','.join(taken_seats)
                db.session.commit()

            if new_seat not in taken_seats:
                taken_seats.append(new_seat)
                flight.taken_seats = ','.join(taken_seats)
                db.session.commit()

            reservation.seat = new_seat
            reservation.luggage = request.form.get('luggage')
            reservation.insurance = request.form.get('insurance')
            db.session.commit()

            flash('Reservation updated successfully.', 'success')
            return redirect(url_for('reservation.my_reservations'))

    return render_template('seats.html', 
                           seats=seats,
                           taken_seats=taken_seats,
                           fromAirport=reservation.fromAirport,
                           destinationAirport=reservation.destinationAirport, 
                           fromCode=reservation.fromCode, 
                           destinationCode=reservation.destinationCode,
                           airlineCode=reservation.airlineCode, 
                           departure=reservation.timeOfDeparture,
                           back=str(id))


@reservation.route('/reservation/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_reservation(id):
    reservation = Reservation.query.get_or_404(id)
    if reservation.user_id != current_user.id:
        flash('You do not have permission to delete this reservation.')
        return redirect(url_for('reservation.my_reservations'))

    flight = Flight.query.filter_by(id=reservation.flight_id).first()

    if flight and flight.taken_seats:
        taken_seats = flight.taken_seats.split(',') 
        if reservation.seat in taken_seats:
            taken_seats.remove(reservation.seat)  
            flight.taken_seats = ','.join(taken_seats) 
            db.session.commit()

    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation deleted successfully.')
    return redirect(url_for('reservation.my_reservations'))


@reservation.route('/my-reservations', methods=['GET', 'POST'])
@login_required
def my_reservations():
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template('my_reservations.html', reservations=reservations)
