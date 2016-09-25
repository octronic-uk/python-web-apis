#
# TestSession.py
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
import time
from octronic.webapis.session.Session import Session


class TestSession(unittest.TestCase):


    def setUp(self):
        self.log = logging.getLogger(self.__class__.__name__)


    def tearDown(self):
        pass


    def test_has_expired(self):
        session = Session(time_to_live=5)
        self.log.info(session)
        time.sleep(4)
        self.assertFalse(session.has_expired())
        time.sleep(4)
        self.assertTrue(session.has_expired())


    def test_renew(self):
        session = Session(time_to_live=5)

        self.assertFalse(session.has_expired())
        self.log.info("%d %s",1,session)

        time.sleep(5)
        self.assertTrue(session.has_expired())
        self.log.info("%d %s",2,session)

        session.renew(4)
        self.assertFalse(session.has_expired())
        self.log.info("%d %s",3,session)

        time.sleep(5)
        self.assertTrue(session.has_expired())
        self.log.info("%d %s",4,session)


# Unit test Harness
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()

