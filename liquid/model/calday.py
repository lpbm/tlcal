from datetime import date as gdate


class CalDay:
    """
    A calendar day
    """
    events = []
    date = None

    def __init__(self, date_=None, events=[]):
        self.events = events

        if date_ is None:
            date_ = gdate.now()

        self.date = date_

    def append(self, event):
        self.events.append(event)

    def __len__(self):
        return len(self.events)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s ->\n %s\n" % (self.date.strftime("%Y-%m-%d"), self.events)
