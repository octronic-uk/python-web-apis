#
# JSONConfig.py
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
import json

class JSONConfig():
    """
        This class imports a configuturation file from disk in JSON format.
    """
    filename = None

    def __init__(self, filename=None):
        """
            Initialise the JSONConfig object.
            :param filename: config file to work with.
        """
        self.log = logging.getLogger(self.__class__.__name__)
        if filename is not None:
            self.filename = filename
            self.load_file()
        else:
            self.config = {}


    def load_file(self):
        """
            Load the configuration from self.filename
        """
        if self.filename is None:
            self.log.error("Unable to load config. File Name is not set!")
            return False
        else:
            self.log.debug("Loading config from %s",self.filename)
            try:
                json_file = open(self.filename,'r')
                json_str = json_file.read()
                self.log.debug("parsing json...\n%s",json_str)
                self.config = json.loads(json_str)
                json_file.close()
                return self.config is not None
            except json.decoder.JSONDecodeError as e:
                self.log.error(e)
                return False


    def save_file(self):
        """"
            Save the current state of the configuration to self.filename
        """
        if self.filename is None:
            self.log.error("Cannot save configuration, filename has not been set.")
            return False
        else:
            try:
                json_file = open(self.filename,"w") 
                json_str = json.dump(self.config,json_file)
                json_file.close()
                self.log.info("Configuration file saved to %s",self.filename)
                return True
            except:
                self.log.error("Error saving configuration file %s", self.filename)
                return False

            
    def __setitem__(self, key, value):
        self.config[key] = value


    def __getitem__(self,key):
        return self.config[key]


    def __iter__(self):
        return iter(self.config)


    def keys(self):
        return self.config.keys()


    def values(self):
        return [self[key] for key in self]  


    def itervalues(self):
        return (self[key] for key in self)


