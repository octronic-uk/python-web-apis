#
# EventApi.py
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
from flask import Flask
from flask import request
from octronic.webapis.event.EventDB import EventDB
from octronic.webapis.event import Constants


events_db = EventDB()
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

@app.route('/event',methods=['POST'])
def api_event():
    """
        Insert an event into the event collection
    """
    log.info("POST on /event")
    if request.headers['Content-Type'] == 'application/json':
        record = request.json
        events_db.insert_event(
            user=record[Constants.user],
            event=record[Constants.event],
            session=record[Constants.session],
        )
        return "event Created", 201
    else:
        log.error("POST on /event, bad request")
        return "Bad Request", 400
