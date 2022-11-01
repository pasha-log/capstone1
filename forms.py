from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional, AnyOf
from footprint import get_all_vehicle_brands

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

# class AddMyCarForm(FlaskForm):
#     """This form is to collect car information for calculation"""

#     # vehicle_brand = StringField('What vehicle brand?', validators=[DataRequired(), AnyOf(values=[get_all_vehicle_brands()])])
#     vehicle_brand = SelectField(label='What vehicle brand?', choices=get_all_vehicle_brands())
#     vehicle_model = StringField('What vehicle brand model?', validators=[DataRequired()])
#     # personal = BooleanField("This is your personal vehicle", default="checked")

class VehicleTripForm(FlaskForm): 
    """Form for calculating carbon footprint of a car after traveling a certain distance""" 

    distance_value = FloatField('Travel distance', validators=[DataRequired()]) 
    distance_unit = SelectField('Distance unit', choices=[('mi', 'mi'), ('km', 'km')], validators=[DataRequired()])
    # emission_unit = SelectField('Carbon dioxide weight unit', choices=[('lbs', 'lbs'), ('kg', 'kg'), ('g', 'g'), ('mt(metric tonnes)', 'mt(metric tonnes)')], validators=[DataRequired()])

class ShippingForm(FlaskForm): 
    """This form is for calculating the carbon footprint of some order being shipped""" 

    weight_value = FloatField('Weight value', validators=[DataRequired()])
    weight_unit = SelectField('Weight unit of shipment', choices = [('lb', 'lb'), ('kg', 'kg'), ('g', 'g'), ('mt', 'mt')], validators=[DataRequired()])
    distance_value = FloatField('Travel distance', validators=[DataRequired()]) 
    distance_unit = SelectField('Distance unit', choices = [('mi', 'mi'), ('km', 'km')], validators=[DataRequired()])
    # transport_method = SelectField('The method the shipment is traveling', choices = [('ship', 'ship'), ('train', 'train'), ('truck', 'truck'), ('plane', 'plane')], validators=[DataRequired()])
    # emission_unit = SelectField('Carbon dioxide weight unit', choices=[('lbs', 'lbs'), ('kg', 'kg'), ('g', 'g'), ('mt(metric tonnes)', 'mt(metric tonnes)')], validators=[DataRequired()])

class FlightForm(FlaskForm): 
    """This form is for calculating a flight's carbon footprint"""

    distance_value = FloatField('Travel distance', validators=[DataRequired()]) 
    distance_unit = SelectField('Distance unit', choices = [('mi', 'mi'), ('km', 'km')], validators=[DataRequired()])
    # emission_unit = SelectField('Carbon dioxide weight unit', choices=[('lbs', 'lbs'), ('kg', 'kg'), ('g', 'g'), ('mt(metric tonnes)', 'mt(metric tonnes)')], validators=[DataRequired()])

class ElectricityForm(FlaskForm): 
    """This form is for calculating a building's electrical carbon footprint""" 

    countries=[('US', 'United States of America'), 
    ('CA', 'Canada'),
    ('AT', 'Austria'),
    ('BE', 'Belgium'),
    ('BG', 'Bulgaria'),
    ('HR', 'Croatia'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czechia'),
    ('DK', 'Denmark'),
    ('EE', 'Estonia'),
    ('FI', 'Finland'),
    ('FR', 'France'),
    ('DE', 'Germany'),
    ('GR', 'Greece'),
    ('GU', 'Hungary'),
    ('IE', 'Ireland'),
    ('IT', 'Italy'),
    ('LV', 'Latvia'),
    ('LT', 'Lithuania'),
    ('LU', 'Luxembourg'),
    ('MT', 'Malta'),
    ('NL', 'Netherlands'),
    ('PL', 'Poland'),
    ('PT', 'Portugal'),
    ('RO', 'Romania'),
    ('SK', 'Slovakia'),
    ('SI', 'Slovenia'),
    ('ES', 'Spain'),
    ('SE', 'Sweden'),
    ('GB', 'United Kingdom')]

    electricity_value = FloatField('Electricity value', validators=[DataRequired()])
    electricity_unit = SelectField('Weight unit of shipment', choices = [('kwh', 'kwh'), ('mwh', 'mwh')], validators=[DataRequired()])
    country = SelectField('Country', choices=countries, validators=[DataRequired()])
    # emission_unit = SelectField('Carbon dioxide weight unit', choices=[('lbs', 'lbs'), ('kg', 'kg'), ('g', 'g'), ('mt(metric tonnes)', 'mt(metric tonnes)')], validators=[DataRequired()])

