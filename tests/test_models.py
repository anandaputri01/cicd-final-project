"""
Test cases for Account Model
"""
import logging
import unittest
from app import app
from app.models import Account, db

DATABASE_URI = "sqlite:///test.db"

class TestAccountModel(unittest.TestCase):
    """Test Case for Account Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Account.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_an_account(self):
        """It should Create an account and assert that it exists"""
        account = Account(name="John Doe", email="john@example.com", address="123 Main St", phone_number="555-1212")
        account.create()
        self.assertEqual(len(Account.all()), 1)

    def test_update_an_account(self):
        """It should Update an account"""
        account = Account(name="John Doe", email="john@example.com", address="123 Main St", phone_number="555-1212")
        account.create()
        account.name = "Jane Doe"
        account.update()
        found = Account.find(account.id)
        self.assertEqual(found.name, "Jane Doe")

    def test_delete_an_account(self):
        """It should Delete an account"""
        account = Account(name="John Doe", email="john@example.com", address="123 Main St", phone_number="555-1212")
        account.create()
        self.assertEqual(len(Account.all()), 1)
        account.delete()
        self.assertEqual(len(Account.all()), 0)
