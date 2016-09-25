import datetime
from octronic.webapis.common import Constants as CommonConstants
from octronic.webapis.session import Constants

class Session():


    def __init__(self, user_id=None, id=None, created=None, expire_after=None,
                 expire_after_sec=Constants.time_to_live, record=None):
        if record is not None:
            self.from_record(record)
        else:
            self.user = user_id
            self.id = id

            if created is not None:
                self.created = created
            else:
                self.created = datetime.datetime.now()

            if expire_after is not None:
                self.expire_after = expire_after
            elif expire_after_sec is not None:
                self.set_expire_after_from_seconds(expire_after_sec)


    def from_record(self,record):
        self.user = record[CommonConstants.user]
        self.id = record[CommonConstants.mongo_id]
        self.created = record[CommonConstants.created]
        self.expire_after = record[Constants.expire_after]


    def has_expired(self):
        now = datetime.datetime.now()
        return now > self.expire_after


    def set_expire_after_from_seconds(self, seconds):
        self.expire_after = datetime.datetime.now() + datetime.timedelta(seconds=seconds)


    def renew(self,seconds=Constants.time_to_live):
        self.set_expire_after_from_seconds(seconds)


    def __repr__(self):
        return (
            "Session:\n"
                "\tSession: {}\n"
                "\tUser:    {}\n"
                "\tCreated: {}\n"
                "\tExpire:  {}".format(self.id, self.user, self.created, self.expire_after)
        )


    def __eq__(self, other):
        return self.id == other.id