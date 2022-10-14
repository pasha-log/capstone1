# class Vehicle(db.Model):
#     """This is the table of a vehicle's make and model"""

#     __tablename__ = 'vehicles'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#     ) 

#     vehicle_brand = db.Column(
#         db.Text, 
#         nullable=False,
#     )

#     vehicle_model + db.Column(
#         db.Text,
#         nullable=False,
#     )

#     def __repr__(self):
#         return f"<Vehicle #{self.id}: {self.vehicle_brand}, {self.model}, {self.type}>"

# class Country(db.Model): 
#     """List of all countries""" 

#     __tablename__ = 'countries' 

#     country_name = db.Column(
#         db.Text, 
#         nullable=False,
#         primary_key=True
#     )
# class Vehicle_Trip(db.Model):
#     """This stores the instance of personal vehicle travel calculation"""

#     __tablename__ = 'vehicle_trips'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#     ) 

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id', ondelete='cascade')
#     )

#     vehicle_id = db.Column(
#         db.Integer,
#         db.ForeignKey('vehicles.id')
#     )

#     distance_value = db.Column(
#         db.Float, 
#         nullable=False,
#     )

#     timestamp = db.Column(
#         db.DateTime,
#         nullable=False,
#         default=datetime.utcnow(),
#     )

# class Shipping_Trip(db.Model): 
#     """This stores the instance of a shipping calculation"""

#     __tablename__ = 'shipping_orders' 

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#     ) 

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id', ondelete='cascade')
#     )

#     distance_value = db.Column(
#         db.Float, 
#         nullable=False,
#     )

#     weight_value = db.Column(
#         db.Float, 
#         nullable=False,
#     )

#     timestamp = db.Column(
#         db.DateTime,
#         nullable=False,
#         default=datetime.utcnow(),
#     )

# class Flight(db.Model): 
#     """This stores the instance of a flight calculation"""

#     __tablename__ = 'flights' 

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#     ) 

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id', ondelete='cascade')
#     )

#     distance_value = db.Column(
#         db.Float, 
#         nullable=False,
#     )

#     timestamp = db.Column(
#         db.DateTime,
#         nullable=False,
#         default=datetime.utcnow(),
#     )

# class Electricity(db.Model): 
#     """This stores the instance of a housing electricity calculation"""

#     __tablename__ = 'electricity'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#     ) 

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id', ondelete='cascade')
#     )

#     timestamp = db.Column(
#         db.DateTime,
#         nullable=False,
#         default=datetime.utcnow(),
#     )

#     electricity_value = db.Column(
#         db.Float, 
#         nullable=False,
#     ) 

# class User_Calculation(db.Model):
#     """This associates the user's calculations"""

#     __tablename__ = 'user_calculations'

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey('users.id', ondelete='cascade')
#     )

#     calculation_id = db.Column(
#         db.Integer, 
#         db.ForeignKey('calculations.id')
#     )

#     type = db.Column(
#         db.Text,
#         nullable=False
#     )
    
#     def __repr__(self):
#         return f"<User_Calculation #{self.id}: {self.user_id}, {self.calculation_id}, {self.type}>"