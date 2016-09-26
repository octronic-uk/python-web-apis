#
# UserDB.py
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

from datetime import datetime
from octronic.webapis.common.MongoInterface import MongoInterface
from bson.objectid import ObjectId
from octronic.webapis.common import Constants
from octronic.webapis.user.User import User


class UserDB(MongoInterface):
    """
        This class will connect to a MongoDB instance that holds data for a 'Rated' site.
        The class
    """
    def __init__(self,
                 host=Constants.localhost,
                 port=Constants.mongo_port,
                 database=Constants.default_db):
        """
            :param host:
            :param port:
            :param database:
        """
        super().__init__(host=host, port=port, database=database)
        self.mongo_collection = self.mongo_database[Constants.users_collection_name]
        #self.log.info("Created UserDB %s", self)

    def create_user(self,username,password):
        """
            Insert a user into the user Collection.
            :param user_name:
            :return:
        """
        inserted_user = self.mongo_collection.insert_one({
            Constants.username : username,
            Constants.password_hash  : password,
            Constants.email          : "",
            Constants.created  : datetime.now(),
        })

        return self.get_user(user_id=inserted_user.inserted_id)


    def get_user(self,user_id=None,username=None):
        record = None

        if user_id is not None:
            record = self.mongo_collection.find_one({Constants.mongo_id : ObjectId(user_id)})
        elif username is not None:
            record = self.mongo_collection.find_one({Constants.username : username})

        if record is not None:
            return User(record=record)
        else:
            return None


    def update_user(self, userObject):
        self.mongo_collection.update_one(
            {Constants.mongo_id : userObject.id},
            {
                '$set' : {
                    Constants.username : userObject.username,
                    Constants.password_hash : userObject.password_hash,
                    Constants.email : userObject.email,
                }
            }
        )
        return self.get_user(user_id=userObject.id)


    def delete_user(self,userObject):
        self.mongo_collection.delete_one({Constants.mongo_id : userObject.id})


    def user_exists(self, user_id=None, username=None):
        result = None
        if user_id is not None:
            result = self.mongo_collection.find_one({Constants.mongo_id : user_id})
        elif username is not None:
            result = self.mongo_collection.find_one({Constants.username : username})
        return result is not None
