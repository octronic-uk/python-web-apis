#
# TestUserDB.py
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
import unittest
import datetime
from octronic.webapis.user.test import TestConstants
from octronic.webapis.user.UserDB import UserDB


class TestUserDB(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)

    def setUp(self):
        self.user_db = UserDB()
        self.log = logging.getLogger(self.__class__.__name__)


    def tearDown(self):
        if hasattr(self,'test_user'):
            self.user_db.delete_user(self.test_user)


    def test_create_object(self):
        """
            test Creating a RatedDatabaseConnector object
        """
        self.assertIsNotNone(self.user_db.mongo_collection)


    def test_create_user(self):
        """
            test inserting a user
        """
        self.test_user = self.user_db.create_user(self.test_create_user.__name__, TestConstants.password)
        if self.test_user is not None:
            self.log.info("test_insert_user %s",self.test_user.id)
            self.assertIsNotNone(self.test_user)
        else:
            self.assertTrue(False)


    def test_get_user_by_id(self):
        """
            test retrieving a user by their id
        """
        self.test_user = self.user_db.create_user(self.test_get_user_by_id.__name__, TestConstants.password)
        retrieved_user = self.user_db.get_user(user_id=self.test_user.id)

        if retrieved_user is not None:
            self.log.info("test_get_user_by_id %s",retrieved_user)
            self.assertIsNotNone(retrieved_user)
            self.assertEqual(self.test_user,retrieved_user)
        else:
            self.assertTrue(False)


    def test_get_user_by_username(self):
        """
            test retrieving a user by their username
        """
        uname = TestConstants.username + str(datetime.datetime.now())
        self.test_user = self.user_db.create_user(username=uname, password=TestConstants.password)
        retrieved_user = self.user_db.get_user(username=uname)

        if retrieved_user is not None:
            self.log.info("test_get_user_by_username %s",retrieved_user)
            self.assertIsNotNone(retrieved_user)
            self.assertEquals(self.test_user,retrieved_user)
        else:
            self.assertTrue(False)


    def test_update_user(self):
        self.test_user = self.user_db.create_user(TestConstants.username, TestConstants.password)
        self.assertEqual(self.test_user.username, TestConstants.username)
        new_username = "SomeTotallyNewUsername"
        self.test_user.username = new_username
        self.user_db.update_user(self.test_user)
        retrieved_user = self.user_db.get_user(username=new_username)
        self.assertEqual(self.test_user,retrieved_user)


    def test_delete_user(self):
        self.test_user = self.user_db.create_user(TestConstants.username, TestConstants.password)
        self.assertTrue(self.user_db.user_exists(user_id=self.test_user.id))
        self.user_db.delete_user(self.test_user)
        self.assertFalse(self.user_db.user_exists(user_id=self.test_user.id))


    def test_user_exists(self):
        self.test_user = self.user_db.create_user(TestConstants.username, TestConstants.password)
        self.assertTrue(self.user_db.user_exists(user_id=self.test_user.id))
        self.user_db.delete_user(self.test_user)
        self.assertFalse(self.user_db.user_exists(user_id=self.test_user.id))


# Unit test Harness
if __name__ == '__main__':
    unittest.main()
