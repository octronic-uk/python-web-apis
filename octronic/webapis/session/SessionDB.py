#
# SessionDB.py
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

import datetime
from octronic.webapis.common.MongoInterface import MongoInterface
from octronic.webapis.common import Constants
from octronic.webapis.session.Session import Session
from bson.objectid import ObjectId


class SessionDB(MongoInterface):


    def __init__(self,
                 host=Constants.localhost,
                 port=Constants.mongo_port,
                 database=Constants.default_db):
        """
            :param host:     Mongo host
            :param port:     Mongo Port
            :param database: Mongo Database
        """
        super().__init__(host=host,port=port,database=database)
        self.mongo_collection = self.mongo_database[Constants.sessions_collection_name]


    def create_session(self, user=None, user_id=None, time_to_live=Constants.time_to_live):
        """
            Insert a session into the user Collection.
            :param user: user id
            :return: Created Session
        """
        now = datetime.datetime.now()
        expire = now + datetime.timedelta(seconds=time_to_live)

        user_arg = None
        if user is not None:
            user_arg = user.id
        elif user_id is not None:
            user_arg = user_id

        if user_arg is not None:
            inserted_session = self.mongo_collection.insert_one({
                Constants.user     : user_arg,
                Constants.created  : now,
                Constants.expire_time    : expire,
            })

            session = self.get_session(session_id=inserted_session.inserted_id)
            return session

        else:
            return None

    def get_session(self, session=None, session_id=None, user_id=None):
        record = None

        if session is not None:
            record = self.mongo_collection.find_one({Constants.mongo_id : session.id})
        elif session_id is not None:
            if type(session_id) is not ObjectId:
                session_id = ObjectId(session_id)
            record = self.mongo_collection.find_one({Constants.mongo_id : ObjectId(session_id) })
        elif user_id is not None:
            if type(user_id) is not ObjectId:
                user_id = ObjectId(user_id)
            record = self.mongo_collection.find_one({Constants.user : user_id })
        else:
            return None

        if record is not None:
            return Session(record=record)
        else:
            return None


    def update_session(self,session):
        self.mongo_collection.update_one(
            {Constants.mongo_id: session.id},
            {
                '$set': {
                    Constants.user: session.user,
                    Constants.expire_time : session.expire_time,
                    Constants.created: session.created,
                }
            }
        )

        session = self.get_session(session=session)
        return session


    def delete_session(self, session=None, user_id=None):
        result = None
        if session is not None:
            result = self.mongo_collection.delete_many({Constants.mongo_id : session.id})
        elif user_id is not None:
            result = self.mongo_collection.delete_many({Constants.user : user_id})

        return result


    def session_exists(self,session=None, session_id=None):
        if session is not None:
           session = self.mongo_collection.find_one({Constants.mongo_id: session.id})
           return session is not None
        elif session_id is not None:
            session = self.mongo_collection.find_one({Constants.mongo_id: session_id})
            return session is not None
        else:
            return False


    def clear_expired_sessions(self):
        return self.mongo_collection.delete_many({
            Constants.expire_time : {
                "$lt" : datetime.datetime.now()
            }
        })
