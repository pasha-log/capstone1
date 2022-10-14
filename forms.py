from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField
from wtforms.validators import DataRequired, Email, Length, Optional, AnyOf

class RegisterForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])


class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    personal_vehicle_brand = StringField('(Optional) What is your vehicle brand?', validators=[Optional()])
    personal_vehicle_model = StringField('(Optional) What is your vehicle brand model?', validators=[Optional()])
    country = StringField('(Optional) What country do you live in?', validators=[Optional()])
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class VehicleIDForm(FlaskForm):
    """This form is to collect car information for calculation"""

    vehicle_brand = StringField('What vehicle brand?', validators=[DataRequired()])
    vehicle_model = StringField('What vehicle brand model?', validators=[DataRequired()])
    # personal = BooleanField("This is your personal vehicle", default="checked")


class VehicleTripForm(FlaskForm): 
    """Form for calculating carbon footprint of a car after traveling a certain distance""" 

    distance_value = FloatField('Travel distance', validators=[DataRequired()]) 
    # distance_unit = StringField('Distance unit', validators=[AnyOf(values=['mi', 'km'])])

class ShippingOrderForm(FlaskForm): 
    """This form is for calculating the carbon footprint of some order being shipped""" 

    weight_unit = StringField('Weight unit of shipment', validators = [AnyOf(values=['g', 'lb', 'kg','mt'])])
    weight_value = FloatField('Weight value', validators=[DataRequired()])
    distance_value = FloatField('Travel distance', validators=[DataRequired()]) 
    distance_unit = StringField('Distance unit', validators = [AnyOf(values=['mi', 'km'])])
    transport_method = StringField('The method the shipment is traveling', validators = [AnyOf(values=['ship', 'train', 'truck', 'plane'])])

class FlightForm(FlaskForm): 
    """This form is for calculating a flight's carbon footprint"""

    distance_value = FloatField('Travel distance', validators=[DataRequired()]) 
    distance_unit = StringField('Distance unit', validators = [AnyOf(values=['mi', 'km'])])

class ElectricityForm(FlaskForm): 
    """This form is for calculating a building's electrical carbon footprint""" 

    electricity_unit = StringField('Weight unit of shipment', validators = [AnyOf(values=['kwh', 'mwh'])])
    electricity_value = FloatField('Electricity value', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    
