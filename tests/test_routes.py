"""
Account API Service Test Suite
"""
import unittest
import logging
from app import app
from app.models import db, Account
from app.common import status

DATABASE_URI = "sqlite:///test.db"

class TestAccountService(unittest.TestCase):
    """Account Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Account.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        """Runs after each test"""
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """It should return the index page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should return health status"""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["status"], "OK")

    def test_create_account(self):
        """It should create a new account"""
        new_account = {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "address": "456 Side St",
            "phone_number": "555-3434"
        }
        resp = self.client.post("/accounts", json=new_account, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        self.assertEqual(data["name"], "Jane Smith")

    def test_get_account_list(self):
        """It should get a list of accounts"""
        self.client.post("/accounts", json={"name": "A", "email": "a@a.com", "address": "X"}, content_type="application/json")
        self.client.post("/accounts", json={"name": "B", "email": "b@b.com", "address": "Y"}, content_type="application/json")
        resp = self.client.get("/accounts")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 2)

    def test_get_account(self):
        """It should read a single account"""
        account = Account(name="Test", email="t@t.com", address="Z").create()
        # Create via API to get real ID
        resp = self.client.post("/accounts", json={"name": "Test", "email": "t@t.com", "address": "Z"}, content_type="application/json")
        account_id = resp.get_json()["id"]
        resp = self.client.get(f"/accounts/{account_id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["name"], "Test")

    def test_update_account(self):
        """It should update an existing account"""
        resp = self.client.post("/accounts", json={"name": "Old Name", "email": "o@o.com", "address": "Old"}, content_type="application/json")
        account_id = resp.get_json()["id"]
        resp = self.client.put(f"/accounts/{account_id}", json={"name": "New Name", "email": "o@o.com", "address": "New"}, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get_json()["name"], "New Name")

    def test_delete_account(self):
        """It should delete an account"""
        resp = self.client.post("/accounts", json={"name": "Delete Me", "email": "d@d.com", "address": "D"}, content_type="application/json")
        account_id = resp.get_json()["id"]
        resp = self.client.delete(f"/accounts/{account_id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_security_headers(self):
        """It should ensure security headers are present"""
        resp = self.client.get("/", environ_overrides={'REMOTE_ADDR': '127.0.0.1'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.headers.get("X-Frame-Options"), "SAMEORIGIN")
        self.assertEqual(resp.headers.get("X-Content-Type-Options"), "nosniff")

    def test_cors_policy(self):
        """It should ensure CORS policy is present"""
        resp = self.client.get("/", environ_overrides={'REMOTE_ADDR': '127.0.0.1'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.headers.get("Access-Control-Allow-Origin"), "*")
