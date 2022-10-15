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
        return userT

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



def connect_db(app): 
    db.app = app 
    db.init_app(app)



class Calculate(db.Model): 
    """This stores every instance of a calculation made""" 

    __tablename__ = 'calculations' 

    id = db.Column(
        db.Integer,
        primary_key=True,
    ) 

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False,
    )

    user = db.relationship('User')

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    type = db.Column(
        db.Text,
        nullable=False
    )

    distance_value = db.Column(
        db.Float, 
        nullable=False,
        default=0
    )

    electricity_value = db.Column(
        db.Float, 
        nullable=False,
        default=0
    )

    weight_value = db.Column(
        db.Float, 
        nullable=False,
        default=0
    )

    country_name = db.Column(
        db.Text,
        default=None,
    )
    
    def __repr__(self):
        return f"<Calculation #{self.id}: {self.user_id}, {self.timestamp}, {self.type}>"


class Vehicle(db.Model):
    """This is the table of a vehicle's make and model"""

    __tablename__ = 'vehicles'

    id = db.Column(
        db.Text,
        primary_key=True,
    ) 

    vehicle_brand = db.Column(
        db.Text, 
        nullable=False,
    )

    vehicle_model + db.Column(
        db.Text,
        nullable=False,
    )

    def __repr__(self):
        return f"<Vehicle #{self.id}: {self.vehicle_brand}, {self.model}, {self.type}>"

if __name__ == '__main__':
    app.run()