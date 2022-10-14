import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError 

from models import db, connect_db, User
# , Calculate
from forms import RegisterForm, LoginForm
# , VehicleIDForm, VehicleTripForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
# app.app_context()

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///footprint_db'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///footprint_db'
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

        return redirect(f"users/{user.id}/choices")

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
            return redirect(f"users/{user.id}")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")

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

@app.route('/users/choices', methods=['GET'])
def present_choices():
    """Present choices of calculation types to user""" 
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    return render_template("choices.html")

##########################
# Carbon Footprint Forms #
##########################

# @app.route('users/vehicle', methods=['GET', 'POST'])
# def record_vehicle_model():
#     """Before vehicle trip calulation, record vehicle info""" 

#     if not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect("/")

#     form = VehicleIDForm()

#     if form.validate_on_submit():
#         calculation = Message(text=form.text.data)
#         calculation = 
#         g.user.messages.append(msg)
#         db.session.commit()

#         vehicle_brand = form.vehicle_brand.data
#         vehicle_model = form.vehicle_model.data

#         return redirect(f"/users/{g.user.id}")

    
#     return render_template('vehicle-form.html', form=form)

# @app.route('users/vehicle-trip', methods=['GET', 'POST'])
# def ask_for_parameters():
#     """Present form for user vehicle carbon footprint calculation"""

#     if not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect("/")
#     form = VehicleTripForm()

#     if form.validate_on_submit():
#         distance_value = form.distance_value.data
#         new_trip = Calculate(user_id=g.user.id, type=vehicle, distance_value=distance_value)

#         new_cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"], image=request.json["image"])
#         db.session.add(new_cupcake)
#         db.session.commit()
#         response_json = jsonify(trip_info=new_trip.serialize_vehicle_trip())
#         return (response_json, 201)

#     return render_template('vehicle-trip.html', form=form)

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req