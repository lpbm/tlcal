from datetime import timedelta
import re


class Event:
    """
        A simple class for an event
    """
    tl_id = 0
    date_time = None
    icon = ""
    category = ""
    stage = ""
    content = ""
    match_count = 1

    def __init__(self):
        """
        :rtype : Event
        :return:
        """
        self.duration = self.estimate_duration

    def estimate_duration(self):
        """
        return:timedelta
        """
        match_duration = 40
        if len(self.content) > 0:
            m = re.findall(' vs ', self.content)
            if len(m) > 0:
                self.match_count = len(m)

        return timedelta(minutes=self.match_count * match_duration)

    def is_valid(self):
        return (
            ((len(self.category) > 0) or (len(self.stage) > 0)) and
            (self.date_time is not None) and
            (self.tl_id > 0)
        )

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<[%s:%s] @ %s+%s>" % (self.category, self.stage, self.date_time, self.estimate_duration())