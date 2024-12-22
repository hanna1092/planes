from database_config import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
import uuid
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    numberOfId = db.Column(db.String(150), unique=True, nullable=False)  # numer dokumentu tożsamości
    role = db.Column(db.String(50), nullable=False, default='pax')
    reservations = db.relationship('Reservation', backref='pax', lazy=True)  # pax = pasażer

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)  # unikalny identyfikator
    fromAirport = db.Column(db.String(50), nullable=False)
    destinationAirport = db.Column(db.String(50), nullable=False)
    fromCode = db.Column(db.String(3), nullable=False)
    destinationCode = db.Column(db.String(3), nullable=False)
    airlineCode = db.Column(db.String(2), nullable=False)
    flightNumber = db.Column(db.String(6), nullable=False)
    timeOfDeparture = db.Column(db.DateTime(timezone=True))
    seat = db.Column(db.String(3), nullable=False)
    return_flight_id = db.Column(db.Integer, db.ForeignKey('reservation.id'))
    return_flight = db.relationship('Reservation', remote_side=[id], backref=db.backref('original_flight', uselist=False))
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)  # klucz obcy do Flight
    luggage = db.Column(db.String(50), nullable=False)
    insurance = db.Column(db.String(50), nullable=False)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fromAirport = db.Column(db.String(50), nullable=False)
    destinationAirport = db.Column(db.String(50), nullable=False)
    fromCode = db.Column(db.String(3), nullable=False)
    destinationCode = db.Column(db.String(3), nullable=False)
    airlineCode = db.Column(db.String(2), nullable=False)
    flightNumber = db.Column(db.String(6), nullable=False, unique = True)
    timeOfDeparture = db.Column(db.DateTime(timezone=True))
    delay = db.Column(db.Boolean, default=False)
    taken_seats = db.Column(db.Text) # Tablica miejsc
    reservations = db.relationship('Reservation', backref='flight', lazy=True)  # relacja do Reservation

    def set_taken_seats(self, seats):
        self.taken_seats = json.dumps(seats)

    def get_taken_seats(self):
        if self.taken_seats:
            return self.taken_seats.split(',')
        return []

def CreateSeats():   #przyda się przy inicjalizacji lotu :)
    seatsMap = []
    for i in range(1, 40):
        row = []
        i = str(i)
        for l in ['A', 'B', 'C', 'D', 'E', 'F']:
            row.append(l + i)
        seatsMap.append(row)
    return seatsMap

