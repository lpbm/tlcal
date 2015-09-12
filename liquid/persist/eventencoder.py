from json import JSONDecoder, JSONEncoder
from liquid.model.event import Event
from datetime import datetime, timedelta


class EventEncoder(JSONEncoder, JSONDecoder):
    def encode(self, o):
        if isinstance(o, Event):
            end_time = o.date_time + o.estimate_duration()
            return {
                "_id" : o.tl_id,
                "start_time": o.date_time,
                "end_time": end_time,
                "icon": o.icon,
                "category": o.category,
                "stage": o.stage,
                "content": o.content,
            }
        return {}

    def decode(self, s):
        dict = JSONDecoder.decode(s)

        start_time = datetime.strptime(dict["start_time"], "")
        o = Event();

        o.tl_id = dict["_id"];
        o.date_time = dict["start_time"];
        o.duration = dict["end_time"] - dict["start_time"];
        o.icon = dict["icon"];
        o.category = dict["category"];
        o.stage = dict["stage"];
        o.content = dict["content"];
        return o
