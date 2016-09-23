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

from Test import TestConstants
from User import User


class TestUser(unittest.TestCase):


    def setUp(self):
        self.log = logging.getLogger(self.__class__.__name__)


    def tearDown(self):
        pass

    def test_hash_verify_password(self):
        user = User(
            username=TestConstants.username,
        )
        user.hash_password(TestConstants.password)
        self.assertIsNotNone(user.password_hash)
        self.assertTrue(user.verify_password(TestConstants.password))

    def test_equality(self):
        user1 = User(id=TestConstants.user,username=TestConstants.username+"1")
        user2 = User(id=TestConstants.user,username=TestConstants.username+"2")
        self.assertEqual(user1,user2)


# Unit Test Harness
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
