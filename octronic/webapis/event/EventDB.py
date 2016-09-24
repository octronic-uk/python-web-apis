#
# EventDB.py
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
from datetime import datetime
from bson.objectid import ObjectId
from pymongo  import MongoClient
from octronic.webapis.event import Constants


class EventDB:
    """
        This class will connect to a MongoDB instance that holds data for a 'Rated' site.
        The class
    """
    def __init__(self, host=Constants.localhost, port=Constants.default_mongo_port,
                 database=Constants.default_db):
        """
            :param host: Mongo Host
            :param port: Mongo Port
            :param database: Mongo Database
        """
        self.log = logging.getLogger(self.__class__.__name__)
        self.host = host
        self.port = port
        self.database = database
        self.mongo_client = MongoClient(self.host,self.port)
        self.mongo_database = self.mongo_client[self.database]
        self.mongo_events_collection = self.mongo_database[Constants.event_collection_name]
        self.log.info("Created EventDB. Host: %s, Port: %d, Database: %s",self.host,self.port,self.database)

    def insert_event(self, user, session, event):
        '''
            :param user:    user ID
            :param session: Session ID
            :param event:  event to record
            :return:        Inserted Record
        '''
        self.log.info("Inserting event %s %s %s",user,session,event)
        return self.mongo_events_collection.insert_one({
            Constants.user    : ObjectId(user),
            Constants.session : ObjectId(session),
            Constants.event   : event,
            Constants.created : datetime.now()
        })
