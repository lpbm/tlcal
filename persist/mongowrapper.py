from datetime import datetime, timedelta

from pymongo import MongoClient, ReturnDocument
from pymongo.database import Database
from pymongo.errors import PyMongoError

from model.event import Event
#from persist import EventEncoder


class MongoWrapper:
    def __init__(self, debug=False):
        self.debug = debug
        try:
            self.client = MongoClient('mongodb://localhost:27017/?connectTimeoutMS=300')
            self.db = self.client.tlcalendar
            self.db.events.count()
        except PyMongoError:
            self.client = None
            self.db = None

    def save(self, _events, delete=True):
        encoder = EventEncoder()

        success = {"inserts": 0, "updates": 0, "deleted": 0}
        failed = {"inserts": 0, "updates": 0, "deleted": 0}
        skipped = 0

        if not isinstance(self.db, Database):
            print("Could not persist to MongoDB")
            return False

        if self.debug:
            print("Begin MongoDB persist:")

        min_date = datetime.now() + timedelta(weeks=12)
        max_date = datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        ids = []
        types = []

        for _event in _events:
            ids.append(_event.tl_id)
            min_date = min(_event.start_time, min_date)
            max_date = max(_event.start_time, max_date)
            if _event.type not in types:
                types.append(_event.type)

            if isinstance(_event, Event):
                original = self.db.events.find_one({"_id": _event.tl_id})
                if original is None:
                    result = self.db.events.insert_one(encoder.encode(_event))
                    """ :type : pymongo.results.InsertOneResult """
                    if result.inserted_id > 0:
                        success['inserts'] += 1
                    else:
                        failed['inserts'] += 1
                else:
                    _event.canceled = False
                    original_event = encoder.decode(original)
                    if original_event != _event:
                        result = self.db.events.replace_one(original, encoder.encode(_event))
                        """ @type : pymongo.results.UpdateResult """
                        if result.modified_count > 0:
                            success['updates'] += 1
                        else:
                            failed['updates'] += 1
                    else:
                        skipped += 1

        if delete:
            what = {"_id": {"$nin": ids}, "type": {"$in": types}, "start_time": {"$gte": min_date, "$lte": max_date}}
            cursor = self.db.events.find(what)
            for db_event in cursor:
                canceled = self.db.events.find_one_and_update({"_id": db_event["_id"]}, {"$set": {"canceled": True}},
                                                              return_document=ReturnDocument.AFTER)
                if canceled["canceled"]:
                    success['deleted'] += 1
                else:
                    failed['deleted'] += 1

        if self.debug:
            print("SKIP: %d" % skipped)
            print("  OK: INS:%d UPD:%d DEL:%d" % (success["inserts"], success["updates"], success["deleted"]))
            if (failed["inserts"] + failed["updates"] + failed["deleted"]) > 0:
                print(" NOK: INS:%d UPD:%d DEL:%d" % (failed["inserts"], failed["updates"], failed["deleted"]))
        return True