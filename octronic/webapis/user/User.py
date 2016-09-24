#
# user.py
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

from passlib.apps import custom_app_context as pwd_context

from octronic.webapis.user import Constants


class User():

    @classmethod
    def from_record(cls,record):
        return User(
            id = record[Constants.mongo_id],
            username = record[Constants.username],
            password_hash = record[Constants.password_hash],
            created = record[Constants.created],
            email = record[Constants.email]
        )


    def __init__(self, id=None, username=None, password_hash=None, created=None, email=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.created = created
        self.email = email


    def verify_password(self,password):
        return pwd_context.verify(password, self.password_hash)


    def hash_password(self,password):
        self.password_hash = pwd_context.encrypt(password)
        return self.password_hash


    def __repr__(self):
        return "Id: {}\nUn: {}\nCr: {}\nEm: {}".format(self.id, self.username, self.created, self.email)


    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False


    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)
