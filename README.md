# Python Web Apis

This repository contains a set of useful web apis written in Python/Flask. They
are designed to run as standalone apps or with a WSGI such as Gunicorn.

* All `POST` methods accept `Content-Type: application/json` messages with
  parameters defined below.

## EventTracker

An api that allows site events to be recorded.

## Routes

#### POST events to /events with in the following format

  {
    'user'    : '<user_id>',
    'session' : '<session_id>,
    'event'   : '<event>'
  }

## User

An api that provides uesr management (CRUD) functionality.

#### Routes

#### POST to /user to create a user

