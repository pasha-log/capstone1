import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError 

from forms import RegisterForm, LoginForm, VehicleTravelForm
from models import db, connect_db, User, User_Calculation, Vehicle_Trip

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///footprint_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'alsdajjdsad999999')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()