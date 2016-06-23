from liquid.model.event import Event


class OutputWrapper:
    def __init__(self, debug=False):
        self.debug = debug

    def save(self, _events):
        if self.debug:
            print("Begin Output:")

        for _event in _events:
            if isinstance(_event, Event):
                u_type  = _event.type.encode('utf8')
                u_category = _event.category.encode('utf8')
                u_stage = _event.stage.encode('utf8')
                print("[%s] %s: %s" % (u_type.upper(), u_category, u_stage))
                print("Begin time: %s" % _event.start_time)
                for _link in _event.links:
                    print("\t%s - %s" % (_link,  _event.links[_link]))

                if _event.content:
                    print("%s" % _event.content)

        return True
