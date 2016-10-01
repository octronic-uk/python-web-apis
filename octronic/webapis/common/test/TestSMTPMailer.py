#
# TestSMTPMailer.py
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

import unittest
import logging
from octronic.webapis.common import Constants
from octronic.webapis.common.SMTPMailer import SMTPMailer

class TestSMTPMailer(unittest.TestCase):

    def setUp(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.mailer = SMTPMailer(host='octronic.co.uk',port=Constants.smtp_port,sender='two_factor@octronic.co.uk')


    def test_create_object(self):
        self.assertIsNotNone(self.mailer)


    def test_send_mail(self):
        self.log.debug("test_send_mail")
        send_result = self.mailer.send(
            subject='Octronic Two-Factor Unit Test',
            body="Hello form the Octronic Two-Factor Authenticaiton Unit Test",
            to='www@octronic.co.uk'
        )
        self.log.debug(send_result)


if __name__ is '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

