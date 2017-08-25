from json import JSONDecoder, JSONEncoder

from model.event import Event


class EventEncoder(JSONEncoder, JSONDecoder):
    def encode(self, o):
        if isinstance(o, Event):
            return {
                'cal_id': o.cal_id,
                'start_time': o.start_time,
                'end_time': o.end_time,
                'last_modified_time': o.last_modified_time,
                'type': o.type,
                'category': o.category,
                'stage': o.stage,
                'content': o.content,
                'links': o.links,
                'canceled': o.canceled
            }
        return {}

    def decode(self, s):
        o = Event()

        o.cal_id = s['cal_id']
        o.start_time = s['start_time']
        o.end_time = s['end_time']
        o.type = s['type']
        o.category = s['category']
        o.stage = s['stage']
        o.content = s['content']
        if 'last_modified_time' in s:
            o.last_modified_time = s['last_modified_time']
        if 'links' in s:
            o.links = s['links']
        if 'canceled' in s:
            o.canceled = s['canceled']

        return o
