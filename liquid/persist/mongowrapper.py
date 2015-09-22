from pymongo import MongoClient
from liquid.persist.eventencoder import EventEncoder
from liquid.model.event import Event


class MongoWrapper:
    def __init__(self, debug=False):
        client = MongoClient('mongodb://localhost:27017/')
        self.db = client.tlcalendar
        self.debug = debug

    def save(self, _events):
        encoder = EventEncoder()

        if self.debug:
            print("Begin MongoDB persist:")

        success = {"inserts": 0, "updates": 0}
        failed = {"inserts": 0, "updates": 0}
        skipped = 0

        for _event in _events:
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

        if self.debug:
            print("\tSuccess: Added %d - Updated %d - Skipped %d" % (success["inserts"], success["updates"], skipped))
            print("\tFailures: Added %d - Updated %d" % (failed["inserts"], failed["updates"]))

        return True
