#!/usr/bin/env bash

PYENV_HOME=./.pyenv/

# Delete previously built virtualenv
if [ -d $PYENV_HOME ]; then
    rm -rf $PYENV_HOME
fi

# Create virtualenv and install necessary packages
virtualenv --no-site-packages $PYENV_HOME
. $PYENV_HOME/bin/activate

pip install ez_setup bson pymongo flask passlib flask_httpauth nosexcover pylint
pip install ./octronic/
nosetests --with-xcoverage --with-xunit --cover-package=octronic.webapis --cover-erase
pylint -f parseable / | tee pylint.out