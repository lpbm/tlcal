from model.event import Event


class OutputWrapper:
    def __init__(self, debug=False):
        self.debug = debug

    def save(self, _events):
        for _event in _events:
            if isinstance(_event, Event):
                u_category = _event.category.encode('utf8')
                u_stage = _event.stage.encode('utf8')
                if len(u_stage) == 0:
                    print("[%s] %s" % (_event.type.upper(), u_category))
                else:
                    print("[%s] %s: %s" % (_event.type.upper(), u_category, u_stage))
                print("Begin time: %s" % _event.start_time)
                print("End time: %s" % _event.end_time)
                print("Matches: %d" % _event.match_count)
                for _link in _event.links:
                    print("\t%s - %s" % (_link,  _event.links[_link]))

                if _event.content:
                    print("%s" % _event.content)

                print("")

        return True
