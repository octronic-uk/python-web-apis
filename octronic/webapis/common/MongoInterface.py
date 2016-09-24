#
# MongoInterface.py
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
from pymongo  import MongoClient
from octronic.webapis.common import Constants

class MongoInterface():
    """
        This class will connect to a MongoDB instance used to persist webapi data.
    """
    def __init__(self, host=Constants.localhost,
                 port=Constants.mongo_port,
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
        self.mongo_client = MongoClient(self.host, self.port)
        self.mongo_database = self.mongo_client[self.database]
        self.mongo_collection = None

    def __repr__(self):
        return (
            "Created {}\n"
                "\tHost: {}\n"
                "\tPort: {}\n"
                "\nDatabase: {}".format(
                    self.__class__.__name__,
                    self.host,
                    self.port,
                    self.database
            )
        )