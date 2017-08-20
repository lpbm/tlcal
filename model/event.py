
class Event:
    """
        A simple class for an event
    """
    tl_id = 0
    start_time = None
    end_time = None
    last_modified_time = None
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

    def is_valid(self):
        return (
            # ((len(self.category) > 0) or (len(self.stage) > 0)) and
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
        if self.category is None or self.stage is None or len(self.category) == 0 or len(self.stage) == 0:
            return "<%s-%s>" % (self.start_time, self.end_time)
        else:
            return "<[%s:%s] @ %s-%s>" % (self.category, self.stage, self.start_time, self.end_time)