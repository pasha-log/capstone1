import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort, jsonify
import requests
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError 

from models import db, connect_db, User, VehicleTripCalculation, ShippingCalculation, FlightCalculation, ElectricityCalculation

from forms import RegisterForm, LoginForm, VehicleTripForm, ShippingForm, FlightForm, ElectricityForm
from footprint import get_all_vehicle_brands, get_vehicle_estimate, get_shipping_estimate, get_flight_estimate, get_electricity_estimate


CURR_USER_KEY = "curr_user"

SECRET_API_KEY = os.environ.get('CARBON_SECRET_KEY')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///footprint_db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'alsdajjdsad999999')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug = DebugToolbarExtension(app)

connect_db(app)

##############################
# User signup, logout, login #
##############################

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/choices")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/choices")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/")

############## 
# Start page #   
##############  

@app.route('/')
def introduce():
    """Show start_page"""

    return render_template("start.html")

#######################
# Calculation choices #
#######################

@app.route('/choices', methods=['GET'])
def present_choices():
    """Present choices of calculation types to user""" 
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    return render_template("choices.html")

###################
# Add My Car Form #
###################

@app.route('/add_my_car', methods=['GET'])
def choose_vehicle_model_id():
    """User will choose car brand and model in order to get the vehicle_model_id,
    then user gets redirected to main vehicle emissions form""" 

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    BRAND_LIST = get_all_vehicle_brands()

    
    return render_template('calculation_forms/vehicle-form2.html', BRAND_LIST=BRAND_LIST)

@app.route('/get_models/<vehicle_brand_id>', methods=['GET'])
def make_request_for_brand_models(vehicle_brand_id):
    """This route is for providing the app.js file with models without exposing the SECRET_API_KEY"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/") 
    
    response = requests.get(url=f'https://www.carboninterface.com/api/v1/vehicle_makes/{vehicle_brand_id}/vehicle_models', headers={
        'Authorization': f'Bearer {SECRET_API_KEY}',
        'Content-Type': 'application/json'
    })

    data = response.json()

    return(data)

@app.route('/add_my_car/<vehicle_model_id>', methods=['GET'])
def collect_vehicle_model_id(vehicle_model_id):
    """After choosing a vehicle, this route is fired to add the vehicle to our database""" 

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    return redirect(f'/car_trip_form/{vehicle_model_id}' )

##########################
# Carbon Footprint Forms #
##########################

@app.route('/car_trip_form/<vehicle_model_id>', methods=['GET', 'POST'])
def present_vehicle_emissions_form(vehicle_model_id):
    """Now that a user has chosen a specific vehicle, they can now enter data needed for an emissions estimate.
    The vehicle chosen will be added to user's vehicles""" 

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = VehicleTripForm()

    if form.validate_on_submit(): 
        distance_unit = form.distance_unit.data
        distance_value = form.distance_value.data
        # emission_unit = form.emission_unit.data
        emission_unit = request.form.get('emission_unit')

        carbon = get_vehicle_estimate(distance_value, distance_unit, vehicle_model_id, emission_unit)

        # Add new vehicle trip calculation instance into the database.
        new_vehicle_trip = VehicleTripCalculation(user_id=g.user.id, 
        distance_value=distance_value, 
        distance_unit=distance_unit, 
        vehicle_model_id=vehicle_model_id,
        carbon=carbon, 
        emission_unit=emission_unit
        )

        g.user.vehicle_calculations.append(new_vehicle_trip)
        db.session.add(new_vehicle_trip)
        db.session.commit()
        
        user = User.query.get_or_404(g.user.id)
        return render_template('result.html', carbon=carbon, emission_unit=emission_unit, user=user)

    return render_template('calculation_forms/vehicle-trip.html', form=form)

@app.route('/shipping', methods=['GET', 'POST'])
def present_shipping_form(): 
    """User can put in data for calculating emissions from shipping"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/") 

    form = ShippingForm() 

    if form.validate_on_submit(): 
        weight_unit = form.weight_unit.data
        weight_value = form.weight_value.data
        distance_unit = form.distance_unit.data
        distance_value = form.distance_value.data
        # transport_method = form.transport_method.data
        transport_method = request.form.get('transport_method')
        # emission_unit = form.emission_unit.data
        emission_unit = request.form.get('emission_unit')

        new_shipping_order = ShippingCalculation(
            user_id=g.user.id, 
            distance_value=distance_value, 
            distance_unit=distance_unit, 
            weight_value=weight_value,
            weight_unit=weight_unit,
            transport_method=transport_method,
        )

        g.user.shipping_calculations.append(new_shipping_order)
        db.session.add(new_shipping_order)
        db.session.commit()

        carbon = get_shipping_estimate(weight_unit, weight_value, distance_unit, distance_value, transport_method, emission_unit)

        user = User.query.get_or_404(g.user.id)
        return render_template('result.html', carbon=carbon, emission_unit=emission_unit, user=user)

    return render_template('calculation_forms/shipping.html', form=form)

@app.route('/flight', methods=['GET', 'POST'])
def present_flight_form(): 
    """User can put in data for calculating emissions from a flight"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/") 

    form = FlightForm() 

    if form.validate_on_submit(): 
        distance_unit = form.distance_unit.data
        distance_value = form.distance_value.data
        # emission_unit = form.emission_unit.data
        emission_unit = request.form.get('emission_unit')

        new_flight = FlightCalculation(
            user_id=g.user.id, 
            distance_value=distance_value, 
            distance_unit=distance_unit, 
        )

        g.user.flight_calculations.append(new_flight)
        db.session.add(new_flight)
        db.session.commit()

        carbon = get_flight_estimate(distance_unit, distance_value, emission_unit)

        user = User.query.get_or_404(g.user.id)
        return render_template('result.html', carbon=carbon, emission_unit=emission_unit, user=user)

    return render_template('calculation_forms/flights.html', form=form)

@app.route('/electricity', methods=['GET', 'POST'])
def present_electricity_form(): 
    """User can put in data for calculating emissions from electricity consumption"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/") 

    form = ElectricityForm()

    if form.validate_on_submit(): 
        electricity_value=form.electricity_value.data
        electricity_unit=form.electricity_unit.data
        country = form.country.data 
        # emission_unit = form.emission_unit.data 
        emission_unit = request.form.get('emission_unit')

        new_electricity = ElectricityCalculation(
            user_id=g.user.id, 
            electricity_value=electricity_value, 
            electricity_unit=electricity_unit, 
            country=country
        )

        g.user.electricity_calculations.append(new_electricity) 
        db.session.add(new_electricity)
        db.session.commit() 

        carbon = get_electricity_estimate(electricity_value, electricity_unit, country, emission_unit) 

        user = User.query.get_or_404(g.user.id)
        return render_template('result.html', carbon=carbon, emission_unit=emission_unit, user=user)
    
    return render_template('calculation_forms/electricity.html', form=form)

###########
# Profile #
###########

@app.route('/user/<int:user_id>', methods=['GET'])
def show_user_profile(user_id):
    """User should see a list of all their recent calculations, 
    as well as have access to a navbar to perform new calculations. 

    In the future, we want this to have an interactive graph that displays user emissions data over time."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/") 

    user = User.query.get_or_404(user_id)
    return render_template('profile.html', 
    vehicle_calculations=user.vehicle_calculations, 
    shipping_calculations=user.shipping_calculations, 
    flight_calculations=user.flight_calculations, 
    electricity_calculations=user.electricity_calculations,
    user=user
    )

@app.route('/user/data', methods=["GET", "POST"])
def get_user_vehicle_calc_data():
    """This route should return the json data from user vehicle emissions."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/") 

    data = g.user.vehicle_calculations 
    dates = []
    carbon = [] 
    
    for calc in data:
        if calc.emission_unit == 'lbs':
            carbon_kg = calc.carbon / .45
            carbon.append(carbon_kg)
        elif calc.emission_unit == 'g':
            carbon_kg = calc.carbon / 1000
            carbon.append(carbon_kg)
        elif calc.emission_unit == 'mt(metric tonnes)':
            carbon_kg = calc.carbon * 1000
            carbon.append(carbon_kg)
        else: 
            carbon.append(calc.carbon)
        dates.append(calc.timestamp)

    return jsonify({"Carbon": carbon, "Dates": dates})

@app.route('/user/chart', methods=["GET"])
def show_user_carbon_line_chart():
    """User should see a line chart with every type of calculation made, tracking emissions over time."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/") 

    return render_template("chart.html")

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req