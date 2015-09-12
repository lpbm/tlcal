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
            }
        return {}

    def decode(self, s):
        dict = json.loads(s)

        # start_time = datetime.strptime(dict["start_time"], "")
        o = Event();

        o.tl_id = dict["_id"];
        o.start_time = dict["start_time"];
        o.end_time = dict["end_time"];
        o.icon = dict["icon"];
        o.type = dict["type"];
        o.category = dict["category"];
        o.stage = dict["stage"];
        o.content = dict["content"];
        return o
