import unittest
from octronic.webapis.user import UserAPI

class TestUserAPI(unittest.TestCase):


    def setUp(self):
        self.user_api = UserAPI.app.test_client()
        pass

    def tearDown(self):
        pass


    def test_create_user(self):
        pass


    def test_get_user(self):
        pass


    def test_verify_password(self):
        pass

