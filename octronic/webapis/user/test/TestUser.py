#
# TestUser.py
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
from octronic.webapis.user.test import TestConstants
from octronic.webapis.user.User import User


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)

    def setUp(self):
        self.log = logging.getLogger(self.__class__.__name__)


    def test_hash_verify_password(self):
        user = User(username=TestConstants.username)
        user.hash_password(TestConstants.password)

        hash_result = user.password_hash
        self.assertIsNotNone(hash_result)

        verify_result = user.verify_password(TestConstants.password)
        self.assertTrue(verify_result)

        self.log.info(
            "\ntest_hash_verity_password\n"
            "Plain:  %s\n"
            "Hashed: %s\n",
            TestConstants.password, user.password_hash
        )


    def test_equality(self):
        user1 = User(id=TestConstants.user, username=TestConstants.username + "1")
        user2 = User(id=TestConstants.user, username=TestConstants.username + "2")
        self.log.info("\ntest_equality - comparing:\n%s\nwith\n%s",user1,user2)
        equality_result = user1 == user2
        self.assertTrue(equality_result)


# Unit test Harness
if __name__ is '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
