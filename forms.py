from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, RadioField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired, Optional
from flask_login import current_user

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=150)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=4, max=150)])
    email = EmailField('Email', validators=[DataRequired(), Length(min=4, max=150)])
    numberOfId = StringField('Identity Document Number', validators=[DataRequired(), Length(min=4, max=150)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    role = RadioField('Role', choices=["Passanger", "Admin"], default="Passanger")
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SearchForm(FlaskForm):
    base_ = StringField('Base', validators=[DataRequired(), Length(min=3, max=50)])
    to = StringField('To', validators=[DataRequired(), Length(min=3, max=50)])
    departure = DateField('Departure', format='%Y-%m-%d',validators=[DataRequired()])
    return_departure = DateField('Return Departure', format='%Y-%m-%d') 
    back = RadioField('Type of ticket', choices=["One-way", "Return"], validators=[DataRequired()])
    submit = SubmitField('Next')

class ReservationForm1(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=150)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=4, max=150)])
    email = EmailField('Email', validators=[DataRequired(), Length(min=4, max=150)])
    numberOfId = StringField('Identity Document Number', validators=[DataRequired(), Length(min=4, max=150)])
    submit = SubmitField('Next')

class ReservationForm2(FlaskForm):
    luggage = RadioField('Luggage', choices=["Hand Luggage", "Hand Luggage + Checked Luggage"], default="Hand Luggage")
    insurance = RadioField('Insurance', choices=["Insurance", "No insurance"], default="Insurance")
    submit = SubmitField('Next')

class FlightForm(FlaskForm):
    fromAirport = StringField('From Airport', validators=[InputRequired()])
    destinationAirport = StringField('Destination Airport', validators=[InputRequired()])
    fromCode = StringField('From Code', validators=[InputRequired()])
    destinationCode = StringField('Destination Code', validators=[InputRequired()])
    airlineCode = StringField('Airline Code', validators=[InputRequired()])
    flightNumber = StringField('Flight Number', validators=[InputRequired()])
    delay = RadioField('Delay', choices=[('True', 'Yes'), ('False', 'No')], default='False', validators=[InputRequired()])

class EditFlightForm(FlightForm):
    pass
    