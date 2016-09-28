#
# SMTPMailer.py
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

import smtplib
import logging
from email.mime.text import MIMEText
from octronic.webapis.common import Constants


class SMTPMailer():
    """This class is used to send e-mail via smtp using smtplib"""

    def __init__(self, host=Constants.localhost, port=Constants.smtp_port,sender=None):
        """Initialise the obejct with host, port and sender"""
        self.log = logging.getLogger(self.__class__.__name__)
        self.host = host
        self.port = port
        self.sender = sender


    def send(self, subject=None, body=None, to=None):
        """Send an email with subject, body and a list of recipients"""
        self.log.info("Sendig mail to %s",to)
        self.mime_text= MIMEText(body)
        self.mime_text['Subject'] = subject 
        self.mime_text['From'] = self.sender
        self.mime_text['To'] = to

        smtp = smtplib.SMTP(host=self.host,port=self.port)
        result = smtp.sendmail(msg=self.mime_text.as_string(), to_addrs=to, from_addr=self.sender)
        smtp.quit()

        return result


