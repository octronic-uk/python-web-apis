#
# TestEventApi.py
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

import json
import logging
import unittest
from octronic.webapis.event import EventApi
from octronic.webapis.event.test import TestConstants


class TestEventApi(unittest.TestCase):


    def setUp(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.api_client = EventApi.app.test_client()


    def tearDown(self):
        pass


    def test_insert_event(self):
        full_url = '/event'
        self.log.info("test_insert_event posting to %s", full_url)

        data = json.dumps({
            'user'    : str(TestConstants.user),
            'event'  : TestConstants.event,
            'session' : str(TestConstants.session),
        }).encode('utf-8')

        headers = {
            "Content-Type": "application/json"
        }

        result = self.api_client.post(full_url,headers=headers, data=data)

        self.assertEquals(result.status_code,201)
        self.log.info("test_insert_event result: %s", result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
