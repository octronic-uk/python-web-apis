#
# TestJSONConfig.py
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

import unittest
import logging
from octronic.webapis.common.JSONConfig import JSONConfig

class TestJSONConfig(unittest.TestCase):
    """Test script for the JSONConfig Class"""
    test_config_file = 'octronic/webapis/common/test/test_config.json'
    test_config_file_save = 'octronic/webapis/common/test/test_config_save.json'
    test_non_existant_file = 'octronic/webapis/common/test/non_existant_file.json'

    test_key_1 = "Key 1"
    test_key_2 = 32
    test_key_3 = 23.32
    test_key_4 = "Key 4"
    test_key_5 = "Jumbalia"

    test_item_1 = ['an','array','of','strings']
    test_item_2 = "some_val"
    test_item_3 = 33
    test_item_4 = 23.3
    test_item_5 = 'hello'

    application_name_key = 'application_name'
    listen_addresses_key = 'listen_addresses'
    port_key = 'port'

    def setUp(self):
        """Set up individual test cases"""
        self.log = logging.getLogger(self.__class__.__name__)


    def test_create_empty_config(self):
        """Test creating an empty configuration"""
        self.config = JSONConfig()
        self.assertEqual(self.config.config, {})


    def test_loaded_config(self):
        """Test that a loaded config contains correct data"""
        self.config = JSONConfig(filename=self.test_config_file)
        self.assertTrue(self.application_name_key in self.config.keys())
        self.assertTrue(self.listen_addresses_key in self.config.keys())
        self.assertTrue(self.port_key in self.config.keys())


    def test_load_json_file(self):
        """Test loading a file with a valid filename set with self.filename"""
        self.config = JSONConfig()
        self.config.filename = self.test_config_file
        self.log.info("test_load_json_file from %s",self.test_config_file)
        load_result = self.config.load_file()
        self.assertTrue(load_result)


    def test_load_json_file_bad_filename(self):
        """Test loading a file with a bad filename set"""
        self.config = JSONConfig()
        self.config.filename = self.test_non_existant_file
        load_result = self.config.load_file()
        self.assertFalse(load_result)
        

    def test_load_json_file_with_filename(self):
        """Test loading a file with a valid filename passed to load_file"""
        self.config = JSONConfig()
        load_result = self.config.load_file(filename=self.test_config_file)
        self.assertTrue(load_result)


    def test_load_json_file_no_filename(self):
        """Test loading a file with not filename set"""
        self.config = JSONConfig()
        load_result = self.config.load_file()
        self.assertFalse(load_result)


    def test_bracket_overloading(self):
        """Test that bracket operators are overloaded correctly"""
        self.config = JSONConfig()
        self.config[self.test_key_1] = self.test_item_1
        self.config[self.test_key_2] = self.test_item_2
        self.config[self.test_key_3] = self.test_item_3
        self.assertEqual(self.test_item_1, self.config[self.test_key_1])
        self.assertEqual(self.test_item_2, self.config[self.test_key_2])
        self.assertEqual(self.test_item_3, self.config[self.test_key_3])


    def test_save_json_file(self):
        """Test saving a configuration file to disk"""
        self.config = JSONConfig()
        self.config[self.test_key_1] = self.test_item_1
        self.config[self.test_key_2] = self.test_item_2
        self.config[self.test_key_3] = self.test_item_3
        self.config[self.test_key_4] = self.test_item_4
        self.config[self.test_key_5] = self.test_item_5
        self.config.filename = self.test_config_file_save
        self.assertTrue(self.config.save_file())


    def test_save_json_file_no_filename(self):
        """Test failing saving a configuration with no filename set."""
        self.config = JSONConfig()
        self.config[self.test_key_1] = self.test_item_1
        self.config[self.test_key_2] = self.test_item_2
        self.config[self.test_key_3] = self.test_item_3
        self.config[self.test_key_4] = self.test_item_4
        self.config[self.test_key_5] = self.test_item_5
        save_result = self.config.save_file()
        self.assertFalse(save_result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
