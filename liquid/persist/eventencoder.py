from json import JSONDecoder, JSONEncoder
import json
from liquid.model.event import Event


class EventEncoder(JSONEncoder, JSONDecoder):
    def encode(self, o):
        if isinstance(o, Event):
            return {
                "_id": o.tl_id,
                "start_time": o.start_time,
                "end_time": o.end_time,
                "type": o.type,
                "category": o.category,
                "stage": o.stage,
                "content": o.content,
                "links": o.links,
                "canceled": o.canceled
            }
        return {}

    def decode(self, s):
        # start_time = datetime.strptime(dict["start_time"], "")
        o = Event()

        o.tl_id = s["_id"]
        o.start_time = s["start_time"]
        o.end_time = s["end_time"]
        o.type = s["type"]
        o.category = s["category"]
        o.stage = s["stage"]
        o.content = s["content"]
        if "links" in s:
            o.links = s["links"]
        if "canceled" in s:
            o.canceled = s["canceled"]

        return o
