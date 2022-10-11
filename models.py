"""SQLAlchemy models for Carbon Print Calculator."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    calculations = db.relationship('User_Calculation')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class User_Calculation(db.Model):
    """This associates the user's calculations"""

    __tablename__ = 'user_calculations'

    id = db.Column(
        db.Integer,
        primary_key=True,
    ) 

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    vehicle_trip_id = db.Column(
        db.Integer, 
        db.ForeignKey('vehicle_trips.id')
    )

    def __repr__(self):
        return f"<User_Calculation #{self.id}: {self.user_id}, {self.vehicle_trip_id}>"

class Vehicle(db.Model):
    """This is the table of a vehicle's make and model"""

    __tablename__ = 'vehicles'

    id = db.Column(
        db.Integer,
        primary_key=True,
    ) 

    vehicle_make = db.Column(
        db.Text, 
        nullable=False,
    )

    vehicle_model + db.Column(
        db.Text,
        nullable=False,
    )

class Vehicle_Trip(db.Model):
    """This stores the instance of personal vehicle travel calculation"""

    __tablename__ = 'vehicle_trips'

    id = db.Column(
        db.Integer,
        primary_key=True,
    ) 

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    vehicle_id = db.Column(
        db.Integer,
        db.ForeignKey('vehicles.id')
    )

    distance_unit = db.Column(
        db.Text,
        db.ForeignKey('distance_units.id')
    )

    distance_value = db.Column(
        db.Float, 
        nullable=False,
    )

    carbon_lbs = db.Column(
        db.Float
        nullable=False,
    )

    carbon_kg = db.Column(
        db.Float
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )
