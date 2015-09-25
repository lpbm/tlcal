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
                "links": o.links
            }
        return {}

    def decode(self, dict):
        # start_time = datetime.strptime(dict["start_time"], "")
        o = Event()

        o.tl_id = dict["_id"]
        o.start_time = dict["start_time"]
        o.end_time = dict["end_time"]
        o.type = dict["type"]
        o.category = dict["category"]
        o.stage = dict["stage"]
        o.content = dict["content"]
        o.links = dict["links"]

        return o
