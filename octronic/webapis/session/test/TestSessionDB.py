#
# TestSessionDB.py
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
from octronic.webapis.session.test import TestConstants
from octronic.webapis.session.SessionDB import SessionDB


class TestSessionDB(unittest.TestCase):


    def setUp(self):
        self.session_db = SessionDB()
        self.log = logging.getLogger(self.__class__.__name__)


    def test_create_object(self):
        self.assertIsNotNone(self.session_db.mongo_collection)


    def test_create_session(self):
        session = self.session_db.create_session(user_id=TestConstants.user)
        self.log.info("test_create_session: %s",session)
        self.assertIsNotNone(session)


    def test_get_session(self):
        self.session_db.create_session(user_id=TestConstants.user)
        retrieved_sessions = self.session_db.get_session(user_id=TestConstants.user)
        self.assertIsNotNone(retrieved_sessions)


    def test_update_session(self):
        session = self.session_db.create_session(user_id=TestConstants.user)
        updated_session = self.session_db.update_session(session)
        self.assertEqual(session,updated_session)

    def test_delete_session(self):
        session = self.session_db.create_session(user_id=TestConstants.user)
        self.assertTrue(self.session_db.session_exists(session=session))
        self.session_db.delete_sessions(session=session)
        self.assertFalse(self.session_db.session_exists(session=session))


    def test_clear_expired_sessions(self):
        pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
