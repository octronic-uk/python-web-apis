import unittest
import logging
import base64
from flask import json
from octronic.webapis.user import UserAPI
from octronic.webapis.user.test import TestConstants
from octronic.webapis.common import Constants
from octronic.webapis.user.UserDB import UserDB


class TestUserAPI(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)


    def setUp(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.user_api = UserAPI.app.test_client()
        self.user_db = UserDB()


    def test_create_user(self):
        user = self.user_db.get_user(username=TestConstants.username)
        if user is not None:
            self.user_db.delete_user(userObject=user)
        self.log.info("test_create_user POST to /user/create")

        data = json.dumps({
            Constants.username: str(TestConstants.username),
            Constants.password: TestConstants.password,
        }).encode('utf-8')

        headers = {
            "Content-Type": "application/json"
        }

        create_user_response = self.user_api.post('/user/create',data=data,headers=headers)
        self.log.info(create_user_response)


    def test_verify_password(self):
        good_response = self.open_with_auth('/user/test_resource')
        self.log.info('test_verify_password %s status: %s',good_response,good_response.status_code)
        self.assertEqual(good_response.status_code,200)

        bad_cred_response = self.open_with_auth('/user/test_resource',username="IncorrectUsername",password="IncorrectPassword")
        self.log.info('test_verify_password %s status: %s',bad_cred_response,bad_cred_response.status_code)
        self.assertEqual(bad_cred_response.status_code,401)

        bad_method_response = self.open_with_auth('/user/test_resource',method='POST')
        self.log.info('test_verify_password bad method: %s status %s',bad_method_response,bad_method_response.status_code)
        self.assertEqual(bad_method_response.status_code,405)


    def open_with_auth(self, url, method='GET', username=TestConstants.username, password=TestConstants.password):
        credential_utf8  = str(username + ":" + password)
        credential_bytes = bytes(credential_utf8,encoding='utf-8')
        credential_b64   = base64.b64encode(credential_bytes)
        credential_b64_string = str(credential_b64,encoding='ascii')
        self.log.info("Open with auth credential string %s",credential_b64_string)

        return self.user_api.open(
            url,
            method=method,
            headers={
                'Authorization': 'Basic ' + credential_b64_string
            }
        )


    def test_get_auth_token(self):
        self.log.info("test_get_auth_token GET to /user/token")
        auth_token_response = self.open_with_auth('/user/token')
        self.log.info("test_get_auth_token %s", auth_token_response)
        self.assertEqual(auth_token_response.status_code,200)


if __name__ is '__main__':
    unittest.main()