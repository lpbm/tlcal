from pymongo import MongoClient
from liquid.persist.eventencoder import EventEncoder
from liquid.model.event import Event


class MongoWrapper:
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        self.db = client.tlcalendar

    def save(self, _events):
        encoder = EventEncoder()
        results = {
            "inserts": 0,
            "updates": 0,
        }
        for _event in _events:
            if isinstance(_event, Event):
                original = self.db.events.find_one({"_id": _event.tl_id})
                if original is None:
                    results['inserts'] += 1
                    result = self.db.events.insert_one(encoder.encode(_event))
                else:
                    results['updates'] += 1
                    result = self.db.events.replace_one(original, encoder.encode(_event))


