from app import app
from models import db, User, VehicleTripCalculation, ShippingCalculation, FlightCalculation, ElectricityCalculation


with app.app_context(): 
    db.drop_all()
    db.create_all()
    u1 = User.signup(
    username="Emily",
    password="supersecret",
    email="lsdfsafs@sadfsdf.com"
    )

    u2 = User.signup(
    username="Pasha",
    password="doublesecret",
    email="lsafs@saf.com"
    )

    u2_vehicle_estimate = VehicleTripCalculation(
    user_id=2, 
    distance_value=100, 
    distance_unit='mi', 
    vehicle_model_id="7268a9b7-17e8-4c8d-acca-57059252afe9",
    carbon=81.64,
    emission_unit='lbs'
    )

    u2_shipping_estimate = ShippingCalculation(
    user_id=2, 
    distance_value=100, 
    distance_unit='mi',
    weight_value=10, 
    weight_unit='lb',
    transport_method='truck'
    )

    u2_flight_estimate = FlightCalculation(
    user_id=2, 
    distance_value=700,
    distance_unit='mi',
    )

    u2_electricity_estimate = ElectricityCalculation(
    user_id=2, 
    electricity_value=5, 
    electricity_unit='mwh', 
    country='US'
    )

    db.session.add_all([u1, u2])
    db.session.add_all([u2_vehicle_estimate, u2_shipping_estimate, u2_flight_estimate, u2_electricity_estimate])
    db.session.commit()
