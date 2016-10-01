#
# User.py
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
from octronic.webapis.common import Constants

user_attrs = [
    Constants.mongo_id,
    Constants.username,
    Constants.password_hash,
    Constants.created,
    Constants.email,
    Constants.phone,
    Constants.second_factor
]

class User():
    """User: An object that represents a user in memory."""


    def __init__(self, id=None, username=None, password_hash=None, created=None, email=None, phone=None, second_factor=None, record=None):
        """User initialiser. Can init with variable arguments or from a UserDB Record."""
        if record is not None:
            self.from_record(record)
        else:
            self.id = id
            self.username = username
            self.password_hash = password_hash
            self.created = created
            self.phone = phone
            self.email = email
            self.second_factor = second_factor


    def from_record(self,record):
        """Inflate the User object from a UserDB/Mongo record."""

        # Handle non-existant values
        attrs = {}
        for attr in user_attrs:
            try:
                attrs[attr] = record[attr]
            except KeyError as key_error:
                attrs[attr] = ''
                
        return self.__init__(
            id = attrs[Constants.mongo_id],
            username = attrs[Constants.username],
            password_hash = attrs[Constants.password_hash],
            created = attrs[Constants.created],
            email = attrs[Constants.email],
            phone = attrs[Constants.phone],
            second_factor = attrs[Constants.second_factor]
        )


    def verify_password(self,password):
        """Verify a plaintext password against its stored hash value."""
        return pwd_context.verify(password, self.password_hash)


    def hash_password(self,password):
        """Create a password hash from a plaintext password."""
        self.password_hash = pwd_context.encrypt(password)
        return self.password_hash


    def __repr__(self):
        """Return a string representation of this User."""
        return "Id: {}\nUn: {}\nCr: {}\nEm: {}".format(self.id, self.username, self.created, self.email)


    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False


    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)
