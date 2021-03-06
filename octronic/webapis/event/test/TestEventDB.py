#
# TestEventDB.py
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
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
from octronic.webapis.event.EventDB import EventDB
from octronic.webapis.event.test import TestConstants


class TestEventDB(unittest.TestCase):


    def setUp(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.event_tracker_db = EventDB()


    def test_create_object(self):
        """
            test Creating a RatedDatabaseConnector object
        """
        self.assertIsNotNone(self.event_tracker_db)


    def test_insert_event(self):
        """
            test inserting a event record
        """
        test_event = self.event_tracker_db.insert_event(
            TestConstants.user,
            TestConstants.session,
            TestConstants.event
        )

        self.assertIsNotNone(test_event)

        if test_event != None:
            self.log.info("test_insert_event %s",test_event.inserted_id)
            self.assertIsNotNone(test_event.inserted_id)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
