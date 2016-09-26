import datetime
import logging
from octronic.webapis.common import Constants

class Session():


    def __init__(self, user_id=None, id=None, created=None, time_to_live=Constants.time_to_live, expire_time=None, record=None):

        self.log = logging.getLogger(self.__class__.__name__)

        if record is not None:
            self.from_record(record)
            self.log.debug("Created from record %s",self)
            return

        self.user = user_id
        self.id = id

        if created is not None:
            self.created = created
        else:
            self.created = datetime.datetime.now()

        if expire_time is not None:
            self.expire_time = expire_time
        else:
            self.set_time_to_live(time_to_live)


    def from_record(self,record):
        self.user = record[Constants.user]
        self.id = record[Constants.mongo_id]
        self.created = record[Constants.created]
        self.expire_time = record[Constants.expire_time]
        self.log.debug("After from record %s",self)


    def has_expired(self):
        now = datetime.datetime.now()
        return now > self.expire_time


    def set_time_to_live(self, seconds):
        self.expire_time =  self.created + datetime.timedelta(seconds=seconds)


    def renew(self,seconds=Constants.time_to_live):
        self.expire_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)


    def __repr__(self):
        return (
            "Session:\n"
                "\tSession: {}\n"
                "\tUser:    {}\n"
                "\tCreated: {}\n"
                "\tExpire:  {}".format(self.id, self.user, self.created, self.expire_time)
        )


    def __eq__(self, other):
        return self.id == other.id