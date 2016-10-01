#!/usr/bin/env python

#
# setup.py
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

from distutils.core import setup

setup(name='WebApis',
    version='1.0',
    description='Octronic Python Web APIs',
    author="Ash '80' Thompson",
    author_email='ash@octronic.co.uk',
    url='https://octronic.co.uk/',
    packages=[
        'octronic.webapis.common',
        'octronic.webapis.common.test',
        'octronic.webapis.event',
        'octronic.webapis.event.test',
        'octronic.webapis.multifactor',
        'octronic.webapis.multifactor.test',
        'octronic.webapis.user',
        'octronic.webapis.user.test',
    ],
)
