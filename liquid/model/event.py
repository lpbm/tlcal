from datetime import timedelta
import re


class Event:
    """
        A simple class for an event
    """
    tl_id = 0
    start_time = None
    end_time = None
    type = ""
    category = ""
    stage = ""
    content = ""
    match_count = 1
    links = {}
    canceled = False

    def __init__(self):
        """
        :rtype : Event
        :return:
        """

    def estimate_duration(self):
        """
        I need to fix this, the match duration depends on the event type
        return:timedelta
        """
        match_duration = 40
        if len(self.content) > 0:
            m = re.findall(' vs ', self.content)
            if len(m) > 0:
                self.match_count = len(m)

        duration = timedelta(minutes=self.match_count * match_duration)
        self.end_time = self.start_time + duration
        return duration

    def is_valid(self):
        return (
            ((len(self.category) > 0) or (len(self.stage) > 0)) and
            (self.start_time is not None) and
            (self.tl_id > 0)
        )

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return (
                self.tl_id == other.tl_id and
                self.start_time == other.start_time and
                self.end_time == other.end_time and
                self.type == other.type and
                self.category == other.category and
                self.stage == other.stage and
                self.content == other.content
            )

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<[%s:%s] @ %s-%s>" % (self.category, self.stage, self.start_time, self.end_time)