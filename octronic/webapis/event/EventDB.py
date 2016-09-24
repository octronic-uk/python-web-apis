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

from datetime import datetime
from bson.objectid import ObjectId
from octronic.webapis.common import Constants as CommonConstants
from octronic.webapis.event import Constants
from octronic.webapis.common.MongoInterface import MongoInterface


class EventDB(MongoInterface):
    """
        This class will connect to a MongoDB instance that holds data for a 'Rated' site.
        The class
    """
    def __init__(self,
                 host=CommonConstants.localhost,
                 port=CommonConstants.mongo_port,
                 database=CommonConstants.default_db):
        """
            :param host: Mongo Host
            :param port: Mongo Port
            :param database: Mongo Database
        """
        super().__init__(host=host, port=port, database=database)
        self.mongo_collection = self.mongo_database[Constants.collection_name]
        self.log.info("Created EventDB %s",self)

    def insert_event(self, user, session, event):
        '''
            :param user:    user ID
            :param session: Session ID
            :param event:  event to record
            :return:        Inserted Record
        '''
        self.log.info("Inserting event %s %s %s",user,session,event)
        return self.mongo_collection.insert_one({
            CommonConstants.user    : ObjectId(user),
            CommonConstants.session : ObjectId(session),
            CommonConstants.event   : event,
            CommonConstants.created : datetime.now()
        })
