from liquid.model.event import Event


class OutputWrapper:
    def __init__(self, debug=False):
        self.debug = debug

    def save(self, _events):
        if self.debug:
            print("Begin Output:")

        for _event in _events:
            if isinstance(_event, Event):
                print("[%s] %s: %s" % (_event.type.upper(), _event.category, _event.stage))
                print("Begin time: %s" % (_event.start_time))
                for _link in _event.links:
                    print("\t%s - %s" % (_link,  _event.links[_link]))

                if _event.content:
                    print("%s" % _event.content)

        return True
