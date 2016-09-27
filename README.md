# Python Web Apis

This repository contains a set of useful web apis written in Python/Flask. They
are designed to run as standalone apps or with a WSGI such as Gunicorn.

* All data is persisted in MongoDB using PyMongo. Collections follow the
  name of their corresponding Api.
* All `POST` methods accept `Content-Type: application/json` messages with
  parameters defined below.

## Event

An api that allows site events to be recorded.

### Routes

#### `/event` - POST events with the following format

    {
        'user'    : 'user_id',
        'session' : 'session_id,
        'event'   : 'event'
    }

## Session
## User

An api that provides uesr management (CRUD) functionality.

### Routes
#### POST to /user to create a user

