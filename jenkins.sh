#!/usr/bin/env bash

#
# jenkins.sh
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

PYENV_HOME=./.pyenv/

# Delete previously built virtualenv
if [ -d $PYENV_HOME ]; then
    rm -rf $PYENV_HOME
fi

# Create virtualenv and install necessary packages
virtualenv --no-site-packages $PYENV_HOME
. $PYENV_HOME/bin/activate

echo Using Python: `which python`
echo Using Pip: `which pip`

pip install ez_setup bson pymongo flask passlib flask_httpauth nosexcover pylint flask_cors pycrypto
pip install .

nosetests --with-xcoverage --with-xunit --cover-package=octronic.webapis --cover-erase octronic/webapis/*

pylint -f parseable . | tee pylint.out
