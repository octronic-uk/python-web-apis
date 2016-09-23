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
import unittest
import logging
import EventApi
import Test.TestConstants as TestConstants


class TestEventApi(unittest.TestCase):


    def setUp(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.api_client = EventApi.app.test_client()


    def tearDown(self):
        pass


    def test_insert_event(self):
        full_url = '/api/event'
        self.log.debug("test_insert_event posting to", full_url)

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
        self.log.debug("test_insert_event", result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
