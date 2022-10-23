"""SQLAlchemy models for Carbon Print Calculator."""
from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

bcrypt = Bcrypt()

 

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.String(70),
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.String(120),
        nullable=False,
        unique=True,
    )

    vehicles = db.relationship("Vehicle")

    vehicle_calculations = db.relationship("VehicleTripCalculation")

    shipping_calculations = db.relationship("ShippingCalculation")

    flight_calculations = db.relationship("FlightCalculation")

    electricity_calculations = db.relationship('ElectricityCalculation')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, password, email):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            email=email,
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

class Vehicle(db.Model):
    """This is the table of a vehicle's make and model"""

    __tablename__ = 'user_vehicles'

    # id = db.Column(
    #     db.Text,
    # ) 

    vehicle_model_id = db.Column(
        db.Text, 
        primary_key=True,
        nullable=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    def __repr__(self):
        return f"<Vehicle #{self.id}: {self.vehicle_model_id} {self.user_id}>"

class VehicleTripCalculation(db.Model): 
    """This stores every instance of a calculation made""" 

    __tablename__ = 'vehicle_calculations' 

    id = db.Column(
        db.Integer,
        primary_key=True,
    ) 

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    distance_value = db.Column(
        db.Float, 
        nullable=False,
    )

    distance_unit = db.Column(
        db.String(2),
        nullable=False
    )

    vehicle_model_id = db.Column(
        db.Text,
        db.ForeignKey('user_vehicles.vehicle_model_id'),
        nullable=False,
    )
    
    def __repr__(self):
        return f"<Calculation #{self.id}: {self.user_id}, {self.timestamp}, {self.distance_value}, {self.vehicle_model_id}>"

class ShippingCalculation(db.Model): 
    """This stores the instance of a shipping calculation"""

    __tablename__ = 'shipping_orders' 

    id = db.Column(
        db.Integer,
        primary_key=True,
    ) 

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    distance_value = db.Column(
        db.Float, 
        nullable=False,
    )

    distance_unit = db.Column(
        db.String(2),
        nullable=False
    ) 

    weight_value = db.Column(
        db.Float, 
        nullable=False,
    )

    weight_unit = db.Column(
        db.Text, 
        nullable=False
    )

    transport_method = db.Column(
        db.Text, 
        nullable=False
    ) 

class FlightCalculation(db.Model): 
    """This stores the instance of a flight calculation"""

    __tablename__ = 'flights' 

    id = db.Column(
        db.Integer,
        primary_key=True,
    ) 

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    distance_value = db.Column(
        db.Float, 
        nullable=False,
    )

    distance_unit = db.Column(
        db.String(2),
        nullable=False
    ) 

class ElectricityCalculation(db.Model): 
    """This stores the instance of a housing electricity calculation"""

    __tablename__ = 'electricity'

    id = db.Column(
        db.Integer,
        primary_key=True,
    ) 

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    electricity_value = db.Column(
        db.Float, 
        nullable=False,
    ) 

    electricity_unit = db.Column(
        db.String(3),
        nullable=False
    )

    country = db.Column(
        db.Text, 
        nullable=False
    )

def connect_db(app): 
    db.app = app 
    db.init_app(app)

if __name__ == '__main__':
    app.run()