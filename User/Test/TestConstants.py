#
# TestConstants.py
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
from bson.objectid import ObjectId

user      = ObjectId('221299887766554433221100')
item      = ObjectId('001122334455667788992122')
session   = ObjectId('112233445566778899002122')
title     = "test Title"
content   = "<h2>test Content!</h2>"
thumbnail = "/view/img/64x64.svg"
tags      = ['Tag_'+str(x) for x in range(5)]
action    = "test Action"
username  = "test Username"
email     = "test.email@unittest.local"
vote_up   = "1"
vote_down = "-1"
vote_none = "0"
password  = "_Test%Password_"

item_dict = {
    'title'    : title,
    'content'  : content,
    'thumbnail': thumbnail,
    'user'     : str(user),
    'tags'     : tags,
}