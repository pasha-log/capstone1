"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

import os
from unittest import TestCase

from sqlalchemy.exc import IntegrityError

from models import db, User 

os.environ['DATABASE_URL'] = "postgresql:///footprint-test"

from app import app

with app.app_context():
    db.create_all()

class UserModelTestCase(TestCase):
        """Test views for messages."""

with app.app_context():
    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()
        u = User.signup(
                    username="testuser",
                    password="HASHED_PASSWORD",
                    email="test@test.com",
                )
        uid = 0000
        u.id = uid
        u1 = User.signup(
            username="test1", 
            password="password", 
            email="email1@email.com", 
        )
        uid1 = 1111
        u1.id = uid1
        db.session.add_all([u, u1])
        db.session.commit()
        u = User.query.get(uid)
        u1 = User.query.get(uid1)
        self.u = u 
        self.uid = uid
        self.u1 = u1
        self.uid1 = uid1 
        self.client = app.test_client() 
        def tearDown(self):
            res = super().tearDown()
            db.session.rollback()
            return res
        def test_user_model(self):
            """Does basic model work?"""
            # User should have no messages & no followers
            self.assertEqual(len(self.u.vehicle_calculations), 0)
            self.assertEqual(len(self.u.shipping_calculations), 0)
            self.assertEqual(len(self.u.flight_calculations), 0)
            self.assertEqual(len(self.u.electricity_calculations), 0)
        def test_repr_method(self):
            """Does the repr method work as expected?"""
            self.assertEqual(repr(self.u), f"<User #{self.u.id}: testuser, test@test.com>")
    ########################################################
    # TESTING SIGNING UP
    ########################################################
        def test_valid_user_signup(self):
            """Does User.signup successfully create a new user given valid credentials?"""
            self.assertTrue(isinstance(self.u3.id, int))
            u_test = User.signup("testtesttest", "password", "testtest@test.com")
            uid = 99999
            u_test.id = uid
            db.session.commit()
            u_test = User.query.get(uid)
            self.assertIsNotNone(u_test)
            self.assertEqual(u_test.username, "testtesttest")
            self.assertEqual(u_test.email, "testtest@test.com")
            self.assertNotEqual(u_test.password, "password")
            # Bcrypt strings should start with $2b$
            self.assertTrue(u_test.password.startswith("$2b$"))
            # Does User.signup fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
            with self.assertRaises(IntegrityError) as context:
                u4 = User.signup(
                username="testuser", 
                password="HASHED_PASSWORD4",
                email="test4@test4.com",
                )
                db.session.commit()
            with self.assertRaises(ValueError) as context: 
                u5 = User.signup(
                username="", 
                password="",
                email="",
                )
                db.session.commit()
    #########################################################
    # TESTING AUTHENTICATION
    #########################################################
        def test_valid_authentication(self):
            """Does User.authenticate successfully return a user when given a valid username and password?"""
            u = User.authenticate(self.u1.username, "password")
            self.assertIsNotNone(u)
            self.assertEqual(u.id, self.uid1)
        def test_invalid_username(self):
            """Does User.authenticate fail to return a user when the username is invalid?"""
            self.assertFalse(User.authenticate("badusername", "password"))
        def test_wrong_password(self):
            """Does User.authenticate fail to return a user when the password is invalid?"""
            self.assertFalse(User.authenticate(self.u1.username, "badpassword"))