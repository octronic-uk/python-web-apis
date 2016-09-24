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
from octronic.webapis.common import Constants as CommonConstants
from octronic.webapis.user import Constants
from octronic.webapis.user.User import User


class UserDB(MongoInterface):
    """
        This class will connect to a MongoDB instance that holds data for a 'Rated' site.
        The class
    """
    def __init__(self,
                 host=CommonConstants.localhost,
                 port=CommonConstants.mongo_port,
                 database=CommonConstants.default_db):
        """
            :param host:
            :param port:
            :param database:
        """
        super().__init__(host=host, port=port, database=database)
        self.mongo_collection = self.mongo_database[Constants.user_collection_name]
        self.log.info("Created UserDB %s", self)

    def create_user(self,username,password):
        """
            Insert a user into the user Collection.
            :param user_name:
            :return:
        """
        inserted_user = self.mongo_collection.insert_one({
            Constants.username      : username,
            Constants.password_hash : password,
            Constants.email         : "",
            Constants.created          : datetime.now(),
        })
        return self.get_user_by_id(inserted_user.inserted_id)


    def get_user_by_id(self,user_id):
        record = self.mongo_collection.find_one({Constants.mongo_id : ObjectId(user_id)})
        return User(record=record)


    def get_user_by_username(self,username):
        record = self.mongo_collection.find_one({Constants.username : username})
        return User(record=record)


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
        return self.get_user_by_id(userObject.id)


    def delete_user(self,userObject):
        self.mongo_collection.delete_one({Constants.mongo_id : userObject.id})


    def user_exists_by_id(self,user_id):
        result = self.mongo_collection.find({Constants.mongo_id : user_id})
        return result.count() > 0


    def user_exists_by_username(self,username):
        result = self.mongo_collection.find_one({Constants.username, username})
        return result.count() > 0
