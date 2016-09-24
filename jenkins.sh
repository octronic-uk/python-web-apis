#!/usr/bin/env bash

PYENV_HOME=./.pyenv/

# Delete previously built virtualenv
if [ -d $PYENV_HOME ]; then
    rm -rf $PYENV_HOME
fi

# Create virtualenv and install necessary packages
virtualenv --no-site-packages $PYENV_HOME
. $PYENV_HOME/bin/activate

which python
which pip

pip install ez_setup bson pymongo flask passlib flask_httpauth nosexcover pylint
pip install .
nosetests --with-xcoverage --with-xunit --cover-package=octronic.webapis.event.test --cover-erase
nosetests --with-xcoverage --with-xunit --cover-package=octronic.webapis.user.test --cover-erase
pylint -f parseable / | tee pylint.out