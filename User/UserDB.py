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
from bson.objectid import ObjectId
from pymongo import MongoClient
import Constants
from User import User


class UserDB:
    """
        This class will connect to a MongoDB instance that holds data for a 'Rated' site.
        The class
    """
    def __init__(self,host='localhost',port=27017,database='RatedDB',collection='Rated'):
        """
            :param host:
            :param port:
            :param database:
            :param collection:
        """
        self.host = host
        self.port = port
        self.database = database
        self.users_collection = collection + Constants.users_collection_suffix
        self.mongo_client = MongoClient(self.host,self.port)
        self.mongo_database = self.mongo_client[self.database]
        self.mongo_users_collection = self.mongo_database[self.users_collection]


    def create_user(self,username,password):
        """
            Insert a user into the User Collection.
            :param user_name:
            :return:
        """
        inserted_user = self.mongo_users_collection.insert_one({
            Constants.username      : username,
            Constants.password_hash : password,
            Constants.email         : "",
            Constants.created          : datetime.now(),
        })
        return self.get_user_by_id(inserted_user.inserted_id)


    def get_user_by_id(self,user_id):
        record = self.mongo_users_collection.find_one({Constants.mongo_id : ObjectId(user_id)})
        return User.from_record(record)


    def get_user_by_username(self,username):
        record = self.mongo_users_collection.find_one({Constants.username : username })
        return User.from_record(record)


    def update_user(self, userObject):
        record = self.mongo_users_collection.update_one(
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
        result = self.mongo_users_collection.delete_one({Constants.mongo_id : userObject.id })


    def user_exists_by_id(self,user_id):
        result = self.mongo_users_collection.find({Constants.mongo_id : user_id })
        return result.count() > 0


    def user_exists_by_username(self,username):
        result = self.mongo_users_collection.find_one({Constants.username, username })
        return result.count() > 0
